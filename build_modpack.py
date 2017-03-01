import re, os #parsing, scaning
import json #for input output
import hashlib #for make_checksum
from urllib.request import urlopen # for web_parsing

"""
V0.0.1 - basic parsing, making dirs and writing summary
V0.0.2 - implented asking for comment, skipping directories in scan, better {debug, printing, summary, making dirs}
V0.0.3 - implented custom_order, new function input_int(which returns some default value, if input is empty)
V0.0.4 - clearer custom_order, name_file > file_name, added moveFiles (which is a total mess), might need redesign of whole json(dict) structure
V0.0.5 - added description (another field added, which is actually comment, previous comment is the description), maybe some more improvements?
V0.0.6 - write meta file to each mod, write to csv, turn off dir_names_with_generated_numbers, get nexus_name from nexus, get desc from skyrimgems
V0.0.7 - removed custom order, making dirs with numbers, def input_int and options to run with arguments
V0.0.8 - Fallout 4 Support, getting Nexus categories
V0.0.9 - lots of rewrites, dropped making directories and summary.csv, purpose is clear now
       - to validate nexus id at lest 3 digits needs to be in file name between - chars
V0.1.0 - first usable thing, split mod_name_validator to build_modpack.py and verify_modpack.py


Verify if file is Nexus mod (by regex /\-(\d{3,})\-/) and collect info about it, do a checksum and save it as modpack_json, which can be used by others using verify_modpack.py
Currently setup for **Skyrim**, for **Fallout 4** support change Game var in Input (line 31+)

Script will scan the current directory (where the script is launched) (or change that in variable target), excluding folders and *.meta files.

TODOs
	when regex fails, try doing more strick check for IDS 01-99 or just verify files for those
	meta files for ModOrganizer loading?
	getting categories from Nexus does not work for adult content, but it works for title, fix it!
		add another option to get categories
		modify function in a way so it tries on each regex, only when categories fails, at least title will be ok
		means no skipping, just not writing categories
"""
#-------------------------------------Input-------------------------------------
#Game = 'Fallout 4'
Game = 'Skyrim'
debug = False
target = os.getcwd()
modpack_json = 'modpack.json' #output
switch_ask_for_description = False
switch_ask_for_comment = False
switch_get_nexus_info = True
if switch_get_nexus_info:
	#skyrimgems search uses nexus_name from Nexus
	#hence its not possible to do search without getting nexus info
	switch_get_skyrimgems_desc = True
#----------------------------------- defs ------------------------------------


def validate_input():
	"""
	validates input and returns:
	game_link and game_link_replacer
	"""
	def nexus_title_replace():
		"""return string used for replacing mod page titles"""
		game_link_replacer = ' at ' + Game + ' Nexus - mods and community'
		return game_link_replacer
	
	#for FO4 no skyrimgems possible, set it global so the variable change is done
	global switch_get_skyrimgems_desc
	if Game == 'Fallout 4':
		game_link = 'fallout4'
		switch_get_skyrimgems_desc = False
	elif Game == 'Skyrim':
		game_link = 'skyrim'
	else:
		print('Game {0} is not recognized as a valid option.\nHit any key to exit.'.format(Game))
		input()
		exit(1)
	game_link_replacer = nexus_title_replace()
	return (game_link, game_link_replacer)


def scan_dir(target):
	"""
	scans directory recursively
	returns file_list, which are paths to the files
	"""
	file_list = []
	blacklist = ['build_modpack.py','.meta', 'mod.info']
	for root, dirs, files in os.walk(target):
		for file in files:
			if any(blacklist_item in file for blacklist_item in blacklist):
				continue
			file_list.append(os.path.join(root, file))
	return file_list

		
def make_checksum(mod_file, chunk_size=1024):
	"""
	Make checksum in sha1 for big files
	from http://stackoverflow.com/questions/1131220/get-md5-hash-of-big-files-in-python
	and http://stackoverflow.com/questions/519633/lazy-method-for-reading-big-file-in-python?noredirect=1&lq=1
	"""
	if debug:
		print('Calculating checksum for', mod_file)
	file_object = open(mod_file, 'rb')
	sha1 = hashlib.sha1();
	"""Lazy function (generator) to read a file piece by piece.
	Default chunk size: 1k."""
	while True:
		data = file_object.read(chunk_size)
		if not data:
			break
		sha1.update(data)
	return sha1.hexdigest()

	
def parse_nexus_mods(mods):
	"""
	returns dict with key of the filename of the mod
	mod is full path
	mod_file_name is just file_name, used as keys in json data
	"""
	def get_nexus_info(nexus_id):
		"""
		Tries to return title and categories from nexus mods like:
		url = 'http://www.nexusmods.com/skyrim/mods/30947/'
		"""
		url = 'http://www.nexusmods.com/' + game_link + '/mods/' + nexus_id + '/'
		try: # handle if url is not reachable error
			foo = urlopen(url)
		except ValueError as url_e:
			print(url_e)
			return None
		html_source = foo.read().decode("utf-8")
        #TODO perhaps use lxml, or BS4?
		title_RE = re.compile('\<title\>(.*)\<\/title\>', re.IGNORECASE|re.DOTALL)
		categories_RE = re.compile('.*searchresults\/\?src_cat=(\d{1,3})\"\>(.*)<\/a\>')
		try:
			categories = categories_RE.search(html_source)
			title = title_RE.search(html_source).group(1)
			#fixes
			if '&#39;' in title:
				title = title.replace('&#39;','\'')
			return(
			title,
			categories.group(1),
			categories.group(2)
			)
		except AttributeError as re_e:
			#print(re_e)
			adult_RE = '\<h2\>Adult-only\scontent<\Sh2>'
			if re.search(adult_RE,html_source):
				print('\nPage {0} is for adults only and requires log-in.\
				\nPlease get nexus_name and its categories yourself.\n'.format(url))
			return (None,None,None)

	def get_skyrimgems_source():
		"""
		Retrieves html source from skyrimgems
		Used later for getting descriptions for the mods
		"""
		try: # handle if url is not reachable error
			foo = urlopen('http://www.skyrimgems.com')
		except ValueError as url_e:
			print(url_e)
			return None
		skyrimgems_source = foo.read().decode('cp852')# this just works
		return skyrimgems_source		
	
	def search_skyrimgems_source(nexus_name): #TODO needs some filtering
		"""
		tries to match mod description with this crazy regex and then tries to do some filtering
		"""
		descriptions_RE = '.*' + nexus_name + '.*\n\s+\<td\s\w+\S+\>(.*)<\Std\>'
		try:
			fetch = re.search(descriptions_RE,skyrimgems_source).group(1)
		except AttributeError as re_e:
			if debug:
				print('"{0}" not found on Skyrim GEMS.'.format(nexus_name))
			return 'N/A'
		#TODO replace by re
		fetch.replace('[<span class="DG">DG</span>+<span class="HF">HF</span>+<span class="DB">DB</span>','[DG+HF+DB]')
		fetch.replace('[<span class="DG">DG</span>] [<span class="DB">DB</span>]', '[DG] [DB]')
		fetch.replace('[<span class="SKSE">SKSE</span>][<span class="DG">DG</span>]', '[SKSE][DG]')
		fetch.replace('[<span class="DG">DG</span> + <span class="DB">DB</span>]', '[DG+DB]')
		fetch.replace('[<span class=\"HF\">HF</span>]','[HF]')
		fetch.replace('[<span class="DB">DB</span>', '[GB]')
		fetch.replace('[<span class="DG">DG</span>]','[DG]')
		fetch.replace('[<span class=\"SKSE\">SKSE</span>]','[SKSE]')
		return fetch
	
	def load_bellow_id_100_data(json_file):
		"""
		load jsons file, should be called only once
		"""
		with open(json_file, 'r') as f:
			data = f.read()
			json_data = json.loads(data)
		return json_data
				
	def search_in_bellow_id_100_data(target, data):
		"""
		goes through data, which are specific structure
		for nexus ids bellow 100
		
		returns id of the mod(the key of data)
		"""
		for i in data.keys():
			if not data[i][0] == None:
				if any(target in file_name for file_name in data[i][0]):
					#print the whole value of the key except the first mod_filename_list
					##print(data[i][1:])
					return i
			
	d = {}
	failed = []
	re_nexus_id = r'\-(\d{3,})\-?' #- at least theree digits and optionaly -
	bellow_id_100_data = None #load only if something fails regex

	#if geting info from Skyrim GEMS, load the page source
	if switch_get_nexus_info and switch_get_skyrimgems_desc:
		skyrimgems_source = get_skyrimgems_source()

	for mod in mods:
		mod_file_name = mod[mod.rfind('\\') + 1:]
		#---------------------- get_name_nexus_id_version ----------------------
		extension = mod_file_name[mod_file_name.rfind('.'):]
		#TODO few more tries?
		try:
			nexus_id = re.search(re_nexus_id, mod_file_name).group(1)
		except AttributeError as re_error_nexus_id:
			print('\nWARNING: Item "{0}" has probably ID bellow 100, trying to check for ids...\n'.format(mod_file_name))
			#try looking if the file_name has nexus_id bellow 100
			if not bellow_id_100_data:
				bellow_id_100_data = load_bellow_id_100_data('skyrim_99ids.json')
			nexus_id = search_in_bellow_id_100_data(mod_file_name, bellow_id_100_data)
			#if failed then skip, the file is surely not for nexus
			if not nexus_id:
				print('\nERROR: For item "{0}" regex failed, skipping\n'.format(mod_file_name))
				failed.append(mod_file_name)
				continue
		re_name_version = re.compile('(.*)-' + nexus_id + '-?(.*)' + extension)
		if debug:
			print('Using re {0} on {1}'.format(re_name_version.pattern, mod_file_name))
		try:
			name = re_name_version.search(mod_file_name).group(1)
		except AttributeError as re_error_mod_name:
			#todo handle cases without no Name
			name = None
		try:
			version = re.search(re_name_version, mod_file_name).group(2)
		except AttributeError as re_error_mod_version:
			version = 'N\A'
		#--------------------------- get_nexus_info ----------------------------
		if switch_get_nexus_info:
			(nexus_name, nexus_modCategoryN, nexus_modCategory) = get_nexus_info(nexus_id)
			if nexus_name:
				nexus_name = nexus_name.replace(game_link_replacer,'')			
			else:
				print('\nFailed to get info from nexusmods.com for {0}\n'.format(name))
				nexus_name, nexus_modCategoryN, nexus_modCategory = None, None, None
		#----------------------------- print info ------------------------------
		if version == 'N\A':
			print('\nValidated {0}\nName:{1}\nID:{2}'.format(mod_file_name, name, nexus_id))
		else:
			print('\nValidated {0}\nName:{1}\nID:{2}\nV:{3}'.format(mod_file_name, name, nexus_id, version))
		if debug:
			print('file_name:', name + '-' + nexus_id + '-' + version + extension)
			print('real_file_name:', mod_file_name)
			print('name:', name)
			print('nexus_id:', nexus_id)
			print('version:', version)
			print('extension:', extension)
			print('Is file_name correct? ', os.path.exists(mod))
			if switch_get_nexus_info:
				print('mod_name:', nexus_name)
				print('nexus_modCategoryN:', nexus_modCategoryN)
				print('nexus_modCategory:', nexus_modCategory)
		#------------------------------ save info ------------------------------
		d[mod_file_name] = {}
		d[mod_file_name]['name'] = name
		d[mod_file_name]['file_name'] = name + '-' + nexus_id + '-' + version + extension
		d[mod_file_name]['sha1'] = make_checksum(mod)
		d[mod_file_name]['modID'] = nexus_id
		d[mod_file_name]['nexus_link'] = 'http://www.nexusmods.com/' + game_link + '/mods/' + nexus_id + '/'
		d[mod_file_name]['version'] = version
		if switch_get_nexus_info:
			d[mod_file_name]['nexus_name'] = nexus_name
			d[mod_file_name]['nexus_categoryN'] = nexus_modCategoryN
			d[mod_file_name]['nexus_category'] = nexus_modCategory
			if switch_get_skyrimgems_desc and nexus_name is not None:
				d[mod_file_name]['skyrimgems_desc'] = search_skyrimgems_source(nexus_name)
		#custom input
		if switch_ask_for_description:
			d[mod_file_name]['description'] = input('Insert your description: ')
		if switch_ask_for_comment:
			d[mod_file_name]['comment'] = input('Insert your comment: ')
	#--------------------------------finalize-----------------------------------
	if debug:
		print('These mods failed to get parsed:', failed)
	return d


def try_save_json(json_file, data):
	"""
	Try to save JSON on Windows
	"""
	try:
		with open(json_file, 'w') as input_file:
			input_file.write(json.dumps(data))
		return True
	except OSError as e:
		print('FAIL: Windows happened:\n  {0}'.format(e))
		return False

		
#-----------------------------------------------------------------------------
if __name__ == "__main__":
	game_link, game_link_replacer = validate_input() #exit if not OK
	#-----------------------------scan current dir------------------------------
	mods_list = scan_dir(target)
	#-------------------------------- get info ---------------------------------
	print('Building modpack from all mod files in', target)
	mods_data = parse_nexus_mods(mods_list)
	#------------------------------- save json ---------------------------------
	if len(mods_data) != 0: #some mod found
		try_save_json(modpack_json, mods_data)
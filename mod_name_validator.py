import re, os # parsing, scaning
from urllib.request import urlopen # for web_parsing
import json
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

validates Nexus Mod files with pattern:
	$name-$nexusid-$version
and creates directories, with pattern:
	$nexusid-$name

TODOs
	hashlib checksums
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

switch_ask_for_description = False
switch_ask_for_comment = False
switch_get_nexus_info = True
if switch_get_nexus_info:
	switch_get_skyrimgems_desc = True #it uses nexus_name from Nexus

target = r'C:\Users\pulec\Downloads\sorter_test'
#target = os.getcwd()

#validate_input
if Game == 'Fallout 4':
	game_link = 'fallout4'
	game_link_replacer = ' at ' + Game + ' Nexus - Mods and community'
	switch_get_skyrimgems_desc = False
elif Game == 'Skyrim':
	game_link = 'skyrim'
	game_link_replacer = ' at ' + Game + ' Nexus - mods and community'
else:
	print('Game {0} is not recognized as a valid option.\nHit any key to exit.'.format(Game))
	input()
	exit()

#---------------------------------- get defs -----------------------------------


def get_skyrimgems_source():
	try: # handle if url is not reachable error
		foo = urlopen('http://www.skyrimgems.com')
	except ValueError as url_e:
		print(url_e)
		return None
	skyrimgems_source = foo.read().decode('cp852')# this just works
	return skyrimgems_source


def parse_nexus_mods(items):
	"""
	returns dict with key of the filename of the mod(might be PITA if you want to access the data)
	"""
	def get_nexus_info(nexus_id):
		#url = 'http://www.nexusmods.com/skyrim/mods/30947/'70656
		url = 'http://www.nexusmods.com/' + game_link + '/mods/' + nexus_id + '/'
		try: # handle if url is not reachable error
			foo = urlopen(url)
		except ValueError as url_e:
			print(url_e)
			return None
		html_source = foo.read().decode("utf-8")
		title_RE = re.compile('<title>(.*?)<\/title>', re.IGNORECASE|re.DOTALL)
		categories_RE = re.compile('.*searchresults\S\?src_cat=(\d{1,3})\"\>(.*)<\Sa\>')
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

	def search_skyrimgems_source(nexus_name): #TODO needs some filtering
		descriptions_RE = '.*' + nexus_name + '.*\n\s+\<td\s\w+\S+\>(.*)<\Std\>'
		try:
			return (re.search(descriptions_RE,skyrimgems_source).group(1))
		except AttributeError as re_e:
			print('"{0}" not found on Skyrim GEMS.'.format(nexus_name))
			return 'N/A'

	d = {}
	directory_names = []
	failed = []
	re_nexus_id = r'\-(\d{3,})\-?' #- at least theree digits and optionaly -

	#if geting info from Skyrim GEMS, load the page source
	if switch_get_nexus_info and switch_get_skyrimgems_desc:
		skyrimgems_source = get_skyrimgems_source()

	for mod in items:
		#---------------------- get_name_nexus_id_version ----------------------
		extension = mod[mod.rfind('.'):]
		#TODO few more tries?
		try:
			nexus_id = re.search(re_nexus_id, mod).group(1)
		except AttributeError as re_error_nexus_id:
			print('\nERROR: For item "{0}" regex failed, skipping\n'.format(mod))
			failed.append(mod)
			continue
		re_name_version = re.compile('(.*)-' + nexus_id + '-?(.*)' + extension)
		if debug:
			print('Using re {0} on {1}'.format(re_name_version.pattern, mod))
		try:
			name = re_name_version.search(mod).group(1)
		except AttributeError as re_error_mod_name:
			#todo handle cases without no Name
			name = None
		try:
			version = re.search(re_name_version, mod).group(2)
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
			print('Valited {0} | {1}.{2}'.format(mod, name, nexus_id))
		else:
			print('Valited {0} | {1}.{2}-{3}'.format(mod, name, nexus_id, version))
		if debug:
			print('file_name:', name + '-' + nexus_id + '-' + version + extension)
			print('real_file_name:', mod)
			print('name:', name)
			print('nexus_id:', nexus_id)
			print('version:', version)
			print('extension:', extension)
			print('Is file_name correct? ', os.path.exists(os.path.join(target,mod)))
			if switch_get_nexus_info:
				print('mod_name:', nexus_name)
				print('nexus_modCategoryN:', nexus_modCategoryN)
				print('nexus_modCategory:', nexus_modCategory)
		#------------------------------ save info ------------------------------
		d[mod] = {}
		d[mod]['name'] = name
		d[mod]['file_name'] = name + '-' + nexus_id + '-' + version + extension
		d[mod]['modID'] = nexus_id
		d[mod]['nexus_link'] = 'http://www.nexusmods.com/' + game_link + '/mods/' + nexus_id + '/'
		d[mod]['version'] = version
		if switch_get_nexus_info:
			d[mod]['nexus_name'] = nexus_name
			d[mod]['nexus_categoryN'] = nexus_modCategoryN
			d[mod]['nexus_category'] = nexus_modCategory
			if switch_get_skyrimgems_desc and nexus_name is not None:
				d[mod]['skyrimgems_desc'] = search_skyrimgems_source(nexus_name)
		#custom input
		if switch_ask_for_description:
			d[mod]['description'] = input('Insert your description: ')
		if switch_ask_for_comment:
			d[mod]['comment'] = input('Insert your comment: ')
		#--------------------------- save dir_names ----------------------------
		if switch_get_nexus_info:
			if nexus_name is None: #failed to get nexus_name, save regular name
				directory_names.append(name + '-' + nexus_id)
			else:
				directory_names.append(nexus_name + '-' + nexus_id)
		else:
			directory_names.append(name + '-' + nexus_id)
	#--------------------------------finalize-----------------------------------
	d['dir_names'] = directory_names
	if debug:
		print('These mods failed to get parsed:', failed)
	return d


#TODO wtf fix this, or don't use it
def mo_friendly_version_parser(v):
	isThereaLetter = False

	def help_with_letter(l):
		if l in char:
			try:
				if v.index(l) == len(v) - 1:
					if debug:
						print(l + ' is already last')
					return None
			except ValueError as e:
				#v.insert(index, char.split('b')[0])
				v.remove(char)
				v.insert(index, char[:char.find(l)])
				while len(v) < 4:
					v.insert(index + 1, '0')
				v.append(char[char.find(l):])

	v = v.replace('v','',)
	v = v.replace('-','.',)
	v = v.split('.')

	for index, char in enumerate(v):
			help_with_letter('a')
			help_with_letter('b')
			help_with_letter('e')

	if debug:
		print('list is',v)
	result = ""

	for item in v:
		isThereaLetter = False
		try:
			if isinstance(int(item), int):
				result += item + '.'
		except ValueError as e2:
				isThereaLetter = True
				result = result[:result.rfind('.')] + v[-1]

	if isThereaLetter:
		return(result)
	else:
		while len(v) < 4:
			v.append('0')
		return('.'.join(v))


#TODO study MO's meta files a bit first
def todo():
	if writeMetaFiles:
		print('Writing meta file to', target + '.meta')
		with open (target + '.meta','w') as meta_file:
			meta_file.write('[General]\n')
			meta_file.write('comment=' + mods[key]['comment'] + '\n')
			meta_file.write('modID=' + mods[key]['modID'] + '\n')
			meta_file.write('name=' + mods[key]['name'] + '\n')
			if switch_get_nexus_info:
				meta_file.write('nexus_name=' + mods[key]['nexus_name'] + '\n')
				meta_file.write('category=' + mods[key]['nexus_categoryN'] + '\n')
			meta_file.write('version=' + mo_friendly_version_parser(mods[key]['version']) + '\n')

#---------------------------------- save def -----------------------------------
def try_save_json(json_file, data):
	try:
		with open(json_file, 'w') as input_file:
			input_file.write(json.dumps(data))
		return True
	except OSError as e:
		print('FAIL: Windows happened:\n  {0}'.format(e))
		return False


if __name__ == "__main__":
	#-----------------------------scan current dir------------------------------
	#get mod_list - names of mod archives from directory target
	mods_list = []
	for item in os.listdir(target):
		#skip meta files
		if '.meta' in item:
			continue
		#skip directories
		if os.path.isfile(os.path.join(target,item)):
			mods_list.append(item)

	#-------------------------------- get info ---------------------------------
	mods = parse_nexus_mods(mods_list)

	#------------------------------- save json ---------------------------------
	if len(mods['dir_names']) != 0: #some mod found
		try_save_json('summary.json', mods)

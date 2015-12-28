import re, os, csv # parsing, scaning, summary
from urllib.request import urlopen # for web_parsing
#V01 - basic parsing, making dirs and writing summary
#V02 - implented asking for comment, skipping directories in scan, better {debug, printing, summary, making dirs}
#V03 - implented custom_order, new function input_int(which returns some default value, if input is empty)
#V04 - clearer custom_order, name_file > file_name, added moveFiles (which is a total mess), might need redesign of whole json(dict) structure
#V05 - added description (another field added, which is actually comment, previous comment is the description), maybe some more improvements?
#V06 - write meta file to each mod, write to csv, turn off dir_names_with_generated_numbers, get modName from nexus, get desc from skyrimgems
#V07 - removed custom order, making dirs with numbers, def input_int and options to run with arguments

"""
validates Nexus Mod files with pattern:
	$name-$nexusid-$version
and creates directories, with pattern:
	$nexusid-$name
"""

""" todo
	look for meta files, pick some information by MO from them?
"""
#-------------------------------------Input-------------------------------------
nexus_id_RE = re.compile('\-(\d{2,})\-') #catch - two digits and - 
number = 1
debug = False
writeSummary = True
makeDirs = True
if makeDirs:
	moveFiles = True
	writeMetaFiles = True
ask_for_description = False
ask_for_comment = False
get_nexus_mod_name = True
if get_nexus_mod_name:
	get_skyrimgems_desc = True #requires modName
#-------------------------------------Defs--------------------------------------


def get_skyrimgems_source():
	try: # handle if url is not reachable error
		foo = urlopen('http://www.skyrimgems.com')
	except ValueError as url_e:	
		print(url_e)
		return None
	skyrimgems_source = foo.read().decode('cp852')# this just works
	return skyrimgems_source

	
def search_skyrimgems_source(modName):
	descriptions_RE = '.*' + modName + '.*\n\s+\<td\s\w+\S+\>([\w\s\',.()&#39;]*)<\Std\>'
	try:
		return re.search(descriptions_RE,skyrimgems_source).group(1)
	except AttributeError as re_e:
		print('"{0}" does not seem to be on Skyrimgems.'.format(modName))
		return 'N/A'


def get_nexus_title_from_web(url):
	#url = 'http://www.nexusmods.com/skyrim/mods/30947/'
	try: # handle if url is not reachable error
		foo = urlopen(url)
	except ValueError as url_e:	
		print(url_e)
		return None
	html_source = foo.read().decode("utf-8")
	title_RE = re.compile('<title>(.*?)</title>', re.IGNORECASE|re.DOTALL)
	try:
		return title_RE.search(html_source).group(1)
	except AttributeError as re_e:
		print(re_e)
		return None


def mo_friendly_version_parser(v):
	debug = False
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


def parse_nexus_mods(items):
	d = {}
	result = []
	global number
	for mod in items:
		extension = mod[mod.rfind('.'):]
		try:
			nexus_id = re.search(nexus_id_RE, mod).group(1)
		except AttributeError as error:
			print('For item "{0}" regex failed, skipping'.format(mod))
			continue
		rest_RE = '(.*)' + '-' + nexus_id + '-(.*)' + extension
		if debug:
			print('Using Re', rest_RE)
		name = re.search(rest_RE, mod).group(1)
		version = re.search(rest_RE, mod).group(2)
		modName = get_nexus_title_from_web(
		'http://www.nexusmods.com/skyrim/mods/' + nexus_id + '/?'
		).replace(' at Skyrim Nexus - mods and community','')
		if debug:
			print('name ',name)
			print('file_name', name + '-' + nexus_id + '-' + version + extension)
			print('mod_name', modName)
			print('Is file_name correct? ', os.path.exists(os.path.join(os.getcwd(),mod)))
			print('extension ',extension)
			print('nexus_id ', nexus_id)
			print('version', version)
		print('Valited ',str(number) + '.' + name + '-' + nexus_id + '-' + version)
		result.append(modName + '-' + nexus_id)
		d[str(number)] = {}
		d[str(number)]['name'] = name
		d[str(number)]['file_name'] = name + '-' + nexus_id + '-' + version + extension
		d[str(number)]['modID'] = nexus_id
		d[str(number)]['nexus_link'] = 'http://www.nexusmods.com/skyrim/mods/' + nexus_id + '/?'
		d[str(number)]['version'] = version
		if ask_for_description:
			d[str(number)]['description'] = input('Insert your description: ')
		else:
			d[str(number)]['description'] = 'INSERT_description'
		if get_nexus_mod_name:
			d[str(number)]['modName'] = modName
			if get_skyrimgems_desc:
				d[str(number)]['skyrimgems_desc'] = search_skyrimgems_source(modName)
		if ask_for_comment:
			d[str(number)]['comment'] = input('Insert your comment: ')
		else:
			d[str(number)]['comment'] = 'place_for_a_comment'
		number += 1
	#--------------------------------finalize-----------------------------------
	d['dir_names'] = result
	return d

#-------------------------------scan current dir--------------------------------
names = []
#skip directories
for item in os.listdir(os.getcwd()):
	#skip meta files
	if '.meta' in item:
		continue
	modPath = os.path.join(os.getcwd(),item)
	if not os.path.isdir(modPath):
		names.append(item)		

if get_nexus_mod_name and get_skyrimgems_desc:
	skyrimgems_source = get_skyrimgems_source()

mods = parse_nexus_mods(names)

#write json
if debug:
	if len(mods['dir_names']) != 0: #some mod found
		with open('summary.json', 'w') as summary__json_file:
			summary__json_file.write(str(mods))

if makeDirs:
	for mod in mods['dir_names']:
		try:
			os.mkdir(mod)
		except OSError as mod_mkdir_err:
			print(mod_mkdir_err)
	if moveFiles:
		for id, key in enumerate(mods):
			if not key == 'dir_names' and os.path.exists(os.path.join(os.getcwd(),mods[key]['file_name'])) is True:
				source = os.path.join(os.getcwd(),mods[key]['file_name'])
				target = os.path.join(os.getcwd(),mods['dir_names'][int(key)-1] + '\\' + mods[key]['file_name'])
				print('Moving ' + source.replace(os.getcwd()+ '\\',''), 'to ' + target.replace(os.getcwd()+ '\\',''))
				try:
					os.rename(source, target)
				except OSError as mods_move_err:
					print('Problem with moving' + mods_move_err.filename)
				if writeMetaFiles:
					print('Writing meta file to', target + '.meta')
					with open (target + '.meta','w') as meta_file:
						meta_file.write('[General]\n')
						meta_file.write('comment=' + mods[key]['comment'] + '\n')
						meta_file.write('modID=' + mods[key]['modID'] + '\n')
						meta_file.write('name=' + mods[key]['name'] + '\n')
						meta_file.write('modName=' + mods[key]['modName'] + '\n')
						meta_file.write('version=' + mo_friendly_version_parser(mods[key]['version']) + '\n')

if writeSummary:
	def writeSummary_func():
		try:
			with open('summary.csv', 'w') as summary_csv_file:
				if get_nexus_mod_name and get_skyrimgems_desc:
					fieldnames = ['modID', 'modName', 'file_name', 'nexus_link' , 'version', 'skyrimgems_desc' ,'description', 'comment']
				elif get_nexus_mod_name:
					fieldnames = ['modID', 'modName', 'file_name', 'nexus_link' , 'version', 'description', 'comment']
				else:
					fieldnames = ['modID', 'name', 'file_name', 'nexus_link' , 'version', 'description', 'comment']
				csv_writer = csv.DictWriter(summary_csv_file,
				delimiter=';',
				lineterminator='\n',
				fieldnames=fieldnames)
				
				csv_writer.writeheader()
				for id, key in enumerate(mods):
					if not key == 'dir_names':
						if get_nexus_mod_name and get_skyrimgems_desc:
							csv_writer.writerow({
							'modID': mods[key]['modID'],
							'modName': mods[key]['modName'],
							'file_name': mods[key]['file_name'],
							'nexus_link': mods[key]['nexus_link'],
							'version': mo_friendly_version_parser((mods[key]['version'])),
							'skyrimgems_desc': mods[key]['skyrimgems_desc'],
							'description': mods[key]['description'],
							'comment': mods[key]['comment'],
							})
						elif get_nexus_mod_name:
							csv_writer.writerow({
							'modID': mods[key]['modID'],
							'modName': mods[key]['modName'],
							'file_name': mods[key]['file_name'],
							'nexus_link': mods[key]['nexus_link'],
							'version': mo_friendly_version_parser((mods[key]['version'])), 
							'description': mods[key]['description'],
							'comment': mods[key]['comment'],
							})
						else:
							csv_writer.writerow({
							'modID': mods[key]['modID'],
							'name': mods[key]['name'],
							'file_name': mods[key]['file_name'],
							'nexus_link': mods[key]['nexus_link'],
							'version': mo_friendly_version_parser((mods[key]['version'])), 
							'description': mods[key]['description'],
							'comment': mods[key]['comment'],
							})
		except PermissionError as opened_csv:
			print(opened_csv)
			print('Close the summary.csv file!')
			input('Close it and try again')
			writeSummary_func()
	if len(mods['dir_names']) != 0: #some mod found
		writeSummary_func()

import json #for input output
import hashlib #for make_checksum
import os #for file operation
import pyunpack #for mod unpack
import re #for do_list_search
import shutil #for copying if rename failes
import tempfile #for unpacking "dirty" mods
try:
	import patool_list_archives
except ValueError as patool_missing:
	print(patool_missing)
	exit(88)
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

Verifies a bunch of mods downloaded from Nexus in a target folder against $modpack.json provided by build_modpack.py.
Mod is verified when checksum of the downloade_file is same as checksum of the entry for the mod in $modpack.json.
Verified mod is then moved (or copied if moving failes) to MO_bin along with MO like meta files (except versions I guess) so Mod Organizer can work with it.


TODOs:
  - Print links for missing files, so users can easilly download them
  - With that make soma kind of summary, how many files verified, etc
  - Mod Organizer doesn't need meta files from us, it can query it allright, might be useful for some mods that got deleted from Nexus
  - do a check first if the files is already copied, or check how shutil does it
  - calculate how much space the copy to MO_bin will take and if there is enough space
  - write plugins.txt, loadorder.txt, skyrim.ini to MO profile
  - Write meta.ini to mod folder based just on the info from json
"""
#-------------------------------------Input-------------------------------------
#not used for now
#Game = 'Fallout 4'
#Game = 'Skyrim'
debug = False
test = False
target = os.getcwd()
modpack_json = 'modpack.json'
MO_downloads = r"d:\SteamLibrary\steamapps\common\Skyrim\Mods\ModOrganizer\downloads"
MO_mods = r"d:\SteamLibrary\steamapps\common\Skyrim\Mods\ModOrganizer\mods"
#mod_MO_name = data[mod_file_name]['name'] + '-' + data[mod_file_name]['modID'] #TODO nexus_name
switch_move_allowed = False
switch_writeMetaFiles = False
if test:
	MO_mods = r"c:\Users\pulec\git\BGames_tools\__TARGET"
#----------------------------------- defs ------------------------------------


def scan_dir(target):
	"""
	scans directory recursively
	returns file_list, which are paths to the files
	"""
	file_list = []
	blacklist = ['.meta', 'mod.info']
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


def try_load_json(json_file):
	"""
	Tries to load valid json
	"""
	try:
		with open(json_file, 'r') as input_file:
			jsondata = json.load(input_file)
		return jsondata
	except FileNotFoundError:
		print('FAIL: File {0} does not exist in this folder'.format(json_file))
		exit(1)
	except json.JSONDecodeError as e:
		print('FAIL: JSON Decode Error:\n  {0}'.format(e))
		exit(2)
		

def verify_mods(mods, data):
	"""
	Does the main thing
	mod is full path
	mod_file_name is just file_name, used as keys in json data
	"""
	#def transfer(mod, target):
	
	def writeMetaFiles(mod_file_name):
		"""
		Writes meta.ini you should get when doing querying info in MO
		"""
		if debug:
			print('Writing meta file to', destination + '.meta')
		with open (destination + '.meta','w') as meta_file:
			meta_file.write('[General]\n')
			#if comments are avaliable
			if data[mod_file_name].get('comment') is True:
				meta_file.write('comment=' + data[mod_file_name]['comment'] + '\n')
			meta_file.write('modID=' + data[mod_file_name]['modID'] + '\n')
			meta_file.write('name=' + data[mod_file_name]['name'] + '\n')
			if data[mod_file_name]['nexus_name'] != None and data[mod_file_name]['nexus_categoryN'] != None:
				meta_file.write('modName=' + data[mod_file_name]['nexus_name'] + '\n')
				meta_file.write('category=' + data[mod_file_name]['nexus_categoryN'] + '\n')
			#TODO revive that special version parsing?
			meta_file.write('version=' + data[mod_file_name]['version'] + '\n')

	def write_meta_ini(target_path):
		"""
		Writes meta.ini to mod folder
		check Horns Are Forever-20861-1-0.7z, it has its own meta.ini!
		14559-Smart Souls 90
		23390-Guard Dialogue Overhaul
		61605-blocksteal redux 1_5
		"""
		if debug:
			print('Writing meta.ini file to', target_path)
		with open(target_path, 'w') as meta_ini_file:
			meta_ini_file.write('[General]\n')
			#if comments are avaliable
			if data[mod_file_name].get('comment') is True:
				meta_ini_file.write('comment=' + data[mod_file_name]['comment'] + '\n') #TODO maybe delete
			meta_ini_file.write('modid=' + data[mod_file_name]['modID'] + '\n')
			meta_ini_file.write('version=' + data[mod_file_name]['version'] + '\n') #TODO revive that special version parsing?
			#newestVersion ignored
			if data[mod_file_name]['nexus_categoryN'] != None:
				meta_ini_file.write('category=' + data[mod_file_name]['nexus_categoryN'] + '\n') #TODO do a MO category map converter
			meta_ini_file.write('installationFile=' + data[mod_file_name]['file_name'] + '\n')
			#ALL IGNORED
			#repository=Nexus
			#ignoredVersion=
			#notes=
			#nexusDescription=
			#lastNexusQuery=
			meta_ini_file.write('\n')
			meta_ini_file.write('[installedFiles]\n')
			meta_ini_file.write('1\modid=' + data[mod_file_name]['modID'] + '\n')
			#ignored
			#1\fileid=1000162106
			#size=1			
	
	def copy_mods(source, destination):
		try:
			copy_main = shutil.copy(source, destination)
			if destination == copy_main:
				if debug:
					print('Copy went OK!')
		except OSError as mods_copy_err:
			print(mods_copy_err)
			print('ERROR: Copying failed, please report')
		#TODO except [Errno 28] No space left on device
	
	def move_mods():
		try:
			os.rename(source, destination)
		except PermissionError as creepy_hands_err:
			print('Cant move file', creepy_hands_err.filename, 'some process is holding it\nTrying to copy')
			copy_mods(source, destination)
		except OSError as mods_move_err:
			print('Problem with moving',mods_move_err.filename)
			#TODO except [Errno 28] No space left on device
		
	def verify_and_unpack_mod_to(mod, target, auto_create_dir=True):
		"""
		Tries to solve all the mess with mods without installers
		
		rules are:
		- done in big OR, nobody cares about big AND, yet
		- on root folder must be any of these dirs or files - dict(root_folder_whitelist)

		note:
			- files outside Data or any other top_dir will not get extracted
			- for example in iWASM V 1-51087-1-0 only what is in Data will be extracted, Images and readme.txt will be ignored
			- SMART packaging like this (more tavel idles v0.5-74799-0-5.zip) gets confusing, luckily it chooses (hopefully everytime) legendary version, which most people should need
			- Optional gets ignored, like in here for example Skyrim Project Optimization - Full Version-32505-1-6.rar
		
			- moved files have old data timestamp, maybe touch them?
		
		known to fail:
			Better Horse Pain Sounds-12608-1.zip
			True Medieval Tavern Music-27425-1-0.rar
			tavern mix-5665-1-0.rar
			
			and perhaps sound specific mods
		"""
		re_allowed_files = r'^[\w\d\-\_\s\.\'\&]+\.[esm|esp|bsa|bsl]+$'
		file_rules = {
				"dirs": ["Interface", "Meshes", "Seq", "Sound", "Textures", "Scripts", "SKSE", "SkyProc Patchers", "Video"],
				"files": [".esm", ".esp", ".bsa", ".bsl"]
			}
		#not used
			##re_main_dirs_files = r'[\\]+((Interface|Meshes|Seq|Sound|Textures|Scripts|SKSE|SkyProc Patchers|Video)|[\w\d\-\_\s\.]+\.[esm|esp|bsa|bsl]+$)'
			##re_data_dir = r'([\\]+)?data' + re_main_dirs_files #search for data
			##re_match_dir = r'^(.*)' + re_main_dirs_files #.* is the wanted group
		docs_rules = {
				"docs_dirs": ["docs", "fomod", "readme", "readmes"],
				"docs": [".docx"]
		}
				
		def do_list_search(a_list, pattern, match = False):
			"""
			excpects a list called:
			
			a_list = patool_list_archives.Archive(mod).list_archive(only_files=True)
			
			searches in the whole_alist by line (filename)
			and by first instance of sucessfull re:
				if match is False
					search for filename in content by re.search
					pattern is regular re, always used with re.IGNORECASE
					returns True or False
				if match is True
					if pattern matched returns match object
			"""
			for line in a_list:
				#list_archive_content returns dict with indexes - stupid 
				filename = line[5]
				if match:
					#if to returns groups
					dig = re.match(pattern, filename, re.IGNORECASE)
					if dig:
						return dig
				else:
					#if just to tell if its there
					found = re.search(pattern, filename, re.IGNORECASE)
					if found:
						return True
			#nothing was sucessfull
			raise UserWarning
		

				
			
		def get_top_dir(list_of_paths):
			"""
			go through the content, and try to identify first line where there is allowed dir
			based on that return a part of that file path which will be used as top_dir
			"""
			not_matched = set()
			for line in list_of_paths:
				for part_of_path in line[5].split(r'\\'):
					#if it was done already it should be in not_matched, otherwise search
					if part_of_path not in not_matched:
						#use lower for non case sensitve
						if any(okdir.lower() in part_of_path.lower() for okdir in file_rules['dirs']):
							if debug:
								print('OK:',line[5])
							#return directory path to extract from
							return(line[5][:line[5].index(part_of_path)])
						else:
							#no dirs validated, try files
							if re.match(re_allowed_files, part_of_path, re.IGNORECASE):
								return(line[5][:line[5].index(part_of_path)])
							if debug:
								print('NOK:', part_of_path)
							not_matched.add(part_of_path)
					else:
						if debug:
							print('SKIP:',part_of_path)
		
		def try_cleanup():
			#all done cleanup
			try:
				tmp_dir.cleanup()
			except PermissionError as pe_clean:
				print("WARNING: Can't remove file: {0}|Please clean it up manually"
				.format(pe_clean.filename))

		list_of_paths = patool_list_archives.Archive(mod).list_archive(only_files=True)
		#if archive has any file_name ([\w\d\-\_\s\.\'\&]+) with allowed extensions in root of archive
		try:
			do_list_search(list_of_paths, re_allowed_files)
			#todo maybe do with match and print which file was determined as OK
			if debug:
				print('GOOD:this mod has esp in root folder')
			archive = pyunpack.Archive(mod)
			archive.extractall(target, auto_create_dir=auto_create_dir)				
			return mod + target 
		except UserWarning:
			#do_list_search didn't find anything
			print('W:no allowed extensions in root of achive')			
		#check if there is any allowed directory in root of archive
		try:
			do_list_search(list_of_paths, r'^(Interface|Meshes|Seq|Sound|Textures|Scripts|SKSE|SkyProc Patchers|Video)')
			#todo maybe do with match and print which dir was determined as OK
			if debug:
				print('GOOD:allowed dirs in root folder')
			archive = pyunpack.Archive(mod)
			archive.extractall(target, auto_create_dir=auto_create_dir)				
			return mod + target
		except UserWarning:
			#do_list_search didn't find anything
			print('W:no allowed data folder in root of archive')
		#do deep validation
		if debug:
				print('trying_to_guess top dir for:', mod)
		tmp_dir = tempfile.TemporaryDirectory(suffix='modpack_unpack')
		top_dir = get_top_dir(list_of_paths)
		if top_dir:
			print('GOOD:in archive everything starting from', top_dir, 'up seems ok')
			print('Unpacking to tmp')
			archive = pyunpack.Archive(mod)
			archive.extractall(tmp_dir.name, auto_create_dir=auto_create_dir)
			print('now moving from tmp ' + top_dir, 'and extracting')
			try:
				shutil.move(tmp_dir.name + r'\\' + top_dir, target)
			except PermissionError as pe_move:
				print("FAIL: Couldn't move file: {0}| WTF?"
				.format(pe_move.filename))
			#TODO again bug when folder already exists
			#except Destination path 'asfsa\Data' already exists			
			try_cleanup()
			return mod + target+r'\\'+top_dir
		else:
			#no topdir, autoextract failed
			return False
				
	for mod in mods:
		mod_file_name = mod[mod.rfind('\\') + 1:]
		if test:
			input('handling ' + mod_file_name)
		if data.get(mod_file_name) is not None:
			mod_checksum = make_checksum(mod)
			if mod_checksum == data[mod_file_name]['sha1']:
				print('[OK]',mod_file_name)
				#if the source file exists
				if os.path.exists(mod) is True:
					#rather move dir_create elsweyr
					#destination = os.path.join(os.getcwd(),MO_downloads + '/' + mod_file_name)
					#destination_dir = os.path.join(os.getcwd(), MO_downloads)
					#if not os.path.exists(destination_dir):
					#	os.makedirs(destination_dir)
					if debug:
						print('Moving {0} to {1}'.format(mod, destination))
					#check mod has installer, then copy it to dl folder
					if data[mod_file_name]["has_installer"]:
						print('Handle',mod_file_name,'yourself')
						copy_mods(mod, MO_downloads + '/' + mod_file_name)
						if switch_writeMetaFiles:
							writeMetaFiles(mod_file_name)
						continue
					#if mod has no installer and correct order (no data dir) unpack it to mods folder
					if data[mod_file_name]['nexus_name'] is not None:
						mod_MO_name = data[mod_file_name]['nexus_name']
					else:
						mod_MO_name = data[mod_file_name]['name']
					#if the target folder already exists do a in increment
					if os.path.exists(os.path.join(MO_mods + r'\\' + mod_MO_name)):
						mod_MO_name += '_ad'
					unpack_sucess = verify_and_unpack_mod_to(mod, MO_mods + r'\\' + mod_MO_name)
					if unpack_sucess is False: #failed to extract the mode
						print('ERROR: Autoextract failed, copying mod', mod_file_name, 'to downloads')
						print('Handle',mod_file_name,'yourself')
						copy_mods(mod, MO_downloads + '/' + mod_file_name)
						if switch_writeMetaFiles:
							writeMetaFiles(mod_file_name)
					else:
						write_meta_ini(MO_mods + r'\\' + mod_MO_name + r'\\meta.ini')
			else:
				print('ERROR:', mod_file_name, 'has different checksum')
		else:
			#TODO this prints which scanned file from directory is not in data
			#it should do it the other way, it needs to be flipped
			print('MOD', mod_file_name, 'is missing')
			#TODO print missing link to download it


if __name__ == "__main__":
	#-----------------------------scan current dir------------------------------
	mods_list = scan_dir(target)
	#------------------------------- load json ---------------------------------
	mods_data = try_load_json(modpack_json)
	#------------------------------- verify json ---------------------------------
	print('Trying to verify and move mods defined in',modpack_json,'to',MO_downloads)
	verify_mods(mods_list, mods_data)
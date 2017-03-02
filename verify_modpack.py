import json #for input output
import hashlib #for make_checksum
import os #for file operation
import pyunpack #for mod unpack
import shutil #for copying if rename failes
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
test = True
target = os.getcwd()
modpack_json = 'modpack.json'
MO_downloads = r"d:\SteamLibrary\steamapps\common\Skyrim\Mods\ModOrganizer\downloads"
MO_mods = r"d:\SteamLibrary\steamapps\common\Skyrim\Mods\ModOrganizer\mods"
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
		return False
		exit(1)
	except json.JSONDecodeError as e:
		print('FAIL: JSON Decode Error:\n  {0}'.format(e))
		exit(2)
		return False
		

def verify_mods(mods, data):
	"""
	Does the main thing
	mod is full path
	mod_file_name is just file_name, used as keys in json data
	"""
	#def transfer(source, target):
	
	def writeMetaFiles(mod_file_name):
		if debug:
			print('Writing meta file to', destination + '.meta')
		with open (destination + '.meta','w') as meta_file:
			meta_file.write('[General]\n')
			#if comments are avaliable
			if data[mod_file_name].get('comment') is True:
				meta_file.write('comment=' + data[mod_file_name]['comment'] + '\n')
			meta_file.write('modID=' + data[mod_file_name]['modID'] + '\n')
			meta_file.write('name=' + data[mod_file_name]['name'] + '\n')
			if data[mod_file_name]['nexus_name'] != None and data[mod_file_name]['nexus_name'] != None:
				meta_file.write('modName=' + data[mod_file_name]['nexus_name'] + '\n')
				meta_file.write('category=' + data[mod_file_name]['nexus_categoryN'] + '\n')
			#TODO revive that special version parsing?
			meta_file.write('version=' + data[mod_file_name]['version'] + '\n')				
	
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
		#TODO HOHOHO, reinvent the wheel here
		"""rules are:

		rules are done in big OR, nobody cares about big AND, yet

		on root folder - dict(root_folder_whitelist)

			double-check:
				mods with dirs optionals
				blacklist: images, why omg?? (iWASM V 1-51087-1-0)

				mods:
				main menu wallpaper replacer HD 1080p now with randomizer **mainmenuwallpapers**
				FamiliarFaces_1.1.5-54509-1-1-5 **vMYC**
				Option C-6594.7z - top_dir is too long
				Enhanced AI Framework-73912-2-5 - data scripts weirdly	
		"""

		root_folder_whitelist = {
				"dirs": ["Interface", "Meshes", "Seq", "Sound", "Textures", "Scripts", "SKSE", "SkyProc Patchers", "Video"],
				"docs": [".docx"],
				"docs_dirs": ["docs", "fomod", "readme", "readmes"],
				"files": [".esm", ".esp", ".bsa", ".bsl"]
			}

		#patool_list_archives stuff
		def do_list_search(re,match = False):
			return patool_list_archives.Archive(mod).search_for_file_in_archive(re, match)
		#bad
		re_main_dirs_files = r'[\\]+((Interface|Meshes|Seq|Sound|Textures|Scripts|SKSE|SkyProc Patchers|Video)|[\w\d\-\_\s\.]+\.[esm|esp|bsa|bsl]+$)'
		#re_data_dir = r'([\\]+)?data' + re_main_dirs_files #search for data
		re_match_dir = r'^(.*)' + re_main_dirs_files #.* is the wanted group
		#good
		re_has_files = '(^[\w\d\-\_\s\.]+\.[esm|esp|bsa|bsl]+)$'
		re_allowed_dirs = r'^(Interface|Meshes|Seq|Sound|Textures|Scripts|SKSE|SkyProc Patchers|Video)'
		#re_has_files_anywhere = r'(^.*\\)?([\w\d\-\_\s\.]+\.[esm|esp|bsa|bsl]+)$'
		match_dir = do_list_search(re_match_dir, match = True)
		if match_dir:
			top_dir = match_dir.group(1)
			if debug:
				print('top_dir is:', top_dir)
			if 'data' in top_dir.lower():
				print('BAD:this mod has a data folder')
				print('extract it, start from data folder and then move')
			if do_list_search(r'^' + top_dir.replace('\\\\','[\\]+').replace('\\','') + re_main_dirs_files): #maybe you are doing this twice
				print('in archive and',top_dir,'files seems ok')
		#if do_list_search(re_data_dir):
		if do_list_search(re_has_files):
			print('GOOD:this mod has esp on root folder')
		if do_list_search(re_allowed_dirs):
			print('GOOD:allowed dirs on root folder')

		#archive = pyunpack.Archive(mod)
		#archive.extractall(target, auto_create_dir=auto_create_dir)
		
	for mod in mods:
		mod_file_name = mod[mod.rfind('\\') + 1:]
		if data.get(mod_file_name) is not None:
			mod_checksum = make_checksum(mod)
			if mod_checksum == data[mod_file_name]['sha1']:
				print('[OK]',mod_file_name)
				#if the source file exists
				source = mod
				if os.path.exists(source) is True:
					destination = os.path.join(os.getcwd(),MO_downloads + '/' + mod_file_name)
					destination_dir = os.path.join(os.getcwd(), MO_downloads)
					if not os.path.exists(destination_dir):
						os.makedirs(destination_dir)
					if debug:
						print('Moving {0} to {1}'.format(source, destination))
					if switch_move_allowed:
						move_mods(source, destination)
					else:
						#if mod has no installer and correct order (no data dir) unpack it to mods folder
						#check = ['has_data_dir', 'has_installer', 'game_data_in_folder']
						if data[mod_file_name]["has_installer"]:
							print('Handle',mod,'yourself')
							#copy mods with installers
							#copy_mods(source, destination)
							continue
						mod_MO_name = data[mod_file_name]['modID'] + '-' + data[mod_file_name]['name']
						verify_and_unpack_mod_to(mod, MO_mods + '\\' + mod_MO_name)
					if switch_writeMetaFiles:
						writeMetaFiles(mod_file_name)
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
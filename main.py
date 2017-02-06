#main V0.4
#V0.1, basic calling defs from modules
#V0.2, some imports and functions here, load json and etc
#V0.3, lot of polishing
#V0.4, less functions, less modules, no subprocess

#for def load_json:
from os.path import exists
from json import load, JSONDecodeError
import hashlib #for verifying
import sys # for exits

#------------------------------------config------------------------------------
json_file = 'config.json'
base_install = True
print_guidance_switch = False
#this is just temporary, this will not be needed TODO
base_utilities_temp_folder = 'tmp'
utilities_download_dir = 'utilities'

#-------------------------------------defs-------------------------------------


#loading the json
def try_load_json(json_file):
	try:
		with open(json_file, 'r') as input_file:
			jsondata = load(input_file)
		return jsondata
	except FileNotFoundError:
		print('FAIL: File {0} does not exist in this folder'.format(json_file))
		return False
	except JSONDecodeError as e:
		print('FAIL: JSON Decode Error:\n  {0}'.format(e))
		return False


def verify(target_dir):
	result = {}
	for utility in input_json['utilities']:
		url = utility['download']
		path = target_dir + '/' + url[url.rfind('/') + 1:]
		crc_config = utility['sha1']
		try:
			if crc_config == hashlib.sha1(open(path,'rb').read()).hexdigest():
				result[utility['name']] = {
				"path" : path,
				"verified" : True,
				"install_path" : utility['install_path']
				.replace('%SkyrimPath%', skyrim_dir)
 				}
			else:
				result[utility['name']] = {
				"verified" : False,
 				}
		except FileNotFoundError:
				result[utility['name']] = {
				"verified" : False,
				}
	return result


def download_utilities(data, target_dir):
	result = {}
	#TODO add checksum hash, so in next run it will skip download
	for utility in input_json['utilities']:
		if data[utility['name']]['verified'] is False:
			print('\nDownloading', utility['name'])
			path = m0prerequisites.download(utility['download'], target_dir)
			if path:
				with open(path, 'rb') as f:
					hex_crc = hashlib.sha1(f.read()).hexdigest()
				result[utility['name']] = {
				"path" : path,
				"crc_sha1" : hex_crc
				 }

	#with open(target_dir + '/' + target_dir + '.sha', 'w') as crc_file:
	#	for utility in result.keys():
	#		crc_file.write('{0} *{1}\n'
	#		.format(result[utility]['crc_sha1'],
	#				result[utility]['path'].replace(target_dir + '/','')))
	return result


def do_both():
	#TODO handle input_json as working memory for operations
	#e.g. add source paths, verify,
	data = {}
	data.update(verify(utilities_download_dir))
	print(data)
	data.update(download_utilities(data, utilities_download_dir))
	return data

#--------maybe no use
def confirm_skyrim_dirs():
	def confirm_dir(msg, default):
		#TODO google how the "or\" works (I forgot...)
		dir = input(msg + ' \n\nIs it ' + default + ' ?\nHit enter to confirm') or\
		default
		return dir
	try:
		skyrim_dir = get_skyrim_dir() #can cause exit 99
	except OSError as e:
		print(e)

	#confirm skyrim_dir
	skyrim_dir = confirm_dir('Enter the full path to Skyrim:',
	skyrim_dir)
	return (skyrim_dir)


#how to unpack mod pack
def print_guidance():
	#TODO write plugins.txt, loadorder.txt, skyrim.ini to MO profile?
	print("Using TES5 Edit cleanup Master files, here is how: http://wiki.step-project.com/User:Neovalen/Skyrim_Revisited_-_Legendary_Edition#Clean_The_Bethesda_ESMs")
	print("When you're finished do a Merged Patch, here is how: https://www.youtube.com/watch?v=BtLolEgVMTg")
	print("When you're finished do a Bashed Patch, here is how: https://www.youtube.com/watch?v=W1Es06MtAZM, http://wiki.step-project.com/Bashed_Patch or https://www.reddit.com/r/skyrimmods/wiki/beginners_guide_quickstart#wiki_create_a_bashed_patch")
	input('Confirm by any key when done')


#--------------------------------import modules--------------------------------
import m0prerequisites
import m1utils_install

if __name__ == "__main__":
	#-------------------------------0. Prerequisites-------------------------------
	try:
		skyrim_dir = m0prerequisites.get_skyrim_dir() #can cause exit 99
	except ValueError:
		print('No registry entry for Skyrim. Run Skyrim at least once')
		print('FAIL: Exit 99')
		sys.exit(99)


	#I guess you don't have to do os.path.exists in the function then
	input_json = try_load_json(json_file)
	if input_json is False:
		#FileNotFoundError or JSONDecodeError
		print('FAIL: Exit 1')
		sys.exit(1)

	data = do_both()
	def test(data):
		#paths for utilities are in dict[utility] key path
		#load SKSE_wanted_files, install paths and MO_config
		print("I would unpack")
		for utility in data.keys():
			print(data[utility]['path'], 'to', data[utility]['install_path'])






	#------------fix from here
	def todo():
		def load_downloaded_utilities():
			for utility in input_json['utilities']:
				if utility['name'] == 'Mod Organizer':
					MO_config = input_json['ModOrganizer.ini']
					MO_destination = utility['install_path'].replace('%SkyrimPath%',skyrim_dir)
					#if MO_destination ends with ModOrganizer, we need to remove it, because the archive is packed as a folder ModOrganizer
					#TODO but if the install_path will not end with ModOrganizer and user will want to extract to C:\SkyrimMods\MO for example
					#the result would be C:\SkyrimMods\MO\ModOrganizer, which might not be an issue, but its not "clean"
					#I just have to know the final destionation of MO so write_MO_ini function will work correctly
					if MO_destination.endswith('ModOrganizer'):
						MO_destination = MO_destination[:MO_destination.rfind('ModOrganizer')]
				if utility['name'] == 'SKSE':
					SKSE_wanted_files = utility['SKSE_wanted_files']


	#------------------------------1. Install base------------------------------
		def install_utilities():
			#TODO install sumarry, what was installed sucessfuly and what not
			m1utils_install.MO_install(sevenzip_path, MO_install_fullpath, MO_destination)
			m1utils_install.SKSE_install(sevenzip_path, SKSE_install_fullpath, SKSE_wanted_files, SKSE_destination)
			m1utils_install.ENB_install(sevenzip_path, ENB_install_fullpath, ENB_destination)
			m1utils_install.TES5E_install(sevenzip_path, TES5E_install_fullpath, TES5E_destination)
			m1utils_install.Mash_install(sevenzip_path, Mash_install_fullpath, Smash_destination)
			m1utils_install.write_MO_ini(MO_destination, MO_config, skyrim_dir)
			##m1utils_install.validate() #validate all
			#all done, delete the bins
			m0prerequisites.cleanup('bin') #DANGEROUS

			if print_guidance_switch:
				print_guidance()

# -----------------------------------3.test------------------------------------
#to unpack backup
##m1utils_install.use_sevenzip(sevenzip_path, 'x','e:\\project\\TES5_Skyrim\\0100-Patches.ready.group\\0100-Patches_test_pack.7z',MO_destination')
#to do a backup
##m1utils_install.use_sevenzip(sevenzip_path, 'a -t7z','d:\\games_stuff\TES5_Skyrim\\0100-Patches.ready.group\\0100-Patches_test_pack.7z','d:\Games\Steam\steamapps\common\Skyrim\Mods\\ModOrganizer\\profiles d:\Games\Steam\steamapps\common\Skyrim\Mods\\ModOrganizer\\overwrite d:\Games\Steam\steamapps\common\Skyrim\Mods\\ModOrganizer\\mods')

"""known issues
	* bin//wget is in use and m0prerequisites tries to overwrite that, TODO fix
		fixed by checking if binaries are already there, CRC check remains
	* MO_install's function paramter MO_destination should be without ModOrganizer at the end
	  because the archive is a packed folder and that will create "unclean" path
	  even if its not "clean" I just have to know the final destionation for write_MO_ini
"""

"""what next
	0.separate package manager which would accept commands:
		$manager install this group (perhaphs this mod?)
		$manager remove the group (or mod)
		$manager list installed
		having local repository, or remote one (dangerous), synced with nexus
	1.unpack group of mods which does not require installation to
		Mod Organizer\Mods folder and
		let user work, meaning let him install his mods folder
		Perhaps unpack profiles as well??

	2.move group of mods which come with Installers to
		Mod Organizer\Downloads folder and
		let user install the mods to his Mods folder
"""
#---------------------------------Return Codes---------------------------------
""" RC
	0 all ok
	1 json_file not found
	2 no 7z binary in ProgramFiles
	99 Skyrim was not yet launched
"""

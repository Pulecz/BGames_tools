#main V0.3
#V0.1, basic calling defs from modules
#V0.2, some imports and functions here, load json and etc
#V0.3, lot of polishing
#TODO, m0prerequisites needs better handling
#TODO write plugins.txt, loadorder.txt, skyrim.ini to MO profile, NMM?
#BIG TODO from json, push mod ids to downloader

#for def load_json:
from os.path import exists
from json import load as jsonload
import os, json #for checking and loading json file
import sys # for exits

#------------------------------------config------------------------------------
json_file = 'config.json'
base_install = True
print_guidance_switch = False
#this is just temporary, this will not be needed TODO
base_utilities_temp_folder = 'tmp'
download_cache_folder = 'utilities'

#-------------------------------------defs-------------------------------------


#loading the json
def try_load_json(json_file):
	try:
		with open(json_file, 'r') as input_file:
			jsondata = jsonload(input_file)
		return jsondata
	except FileNotFoundError:
		print('FAIL: File {0} does not exist in this folder'.format(json_file))
		return False
	except json.decoder.JSONDecodeError as e:
		print('FAIL: JSON Decode Error:\n  {0}'.format(e))
		return False


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

	def download_utilities():
		#TODO add checksum hash, so in next run it will skip download
		for utility in input_json['utilities']:
			print('\nDownloading', utility['name'])
			path = m0prerequisites.download(utility['download'], download_cache_folder)
			if path:
				print('DEBUG:',path)
		#DOWNLOAD ALL UTILITIES
		##MO_install_7zarchive, SKSE_install_7zarchive, ENB_install_archive, TES5E_install_7zarchive, Mash_install_archive = m1download_utils.download_all(wget_path, input_json, download_cache_folder)
		#filenames_list_in_order = m1download_utils.download_all(wget_path, input_json, download_cache_folder)

	download_utilities()

	#------------fix from here
	def todo():



		def load_downloaded_utilities():
			ENB_install_fullpath,
			Mash_install_fullpath,
			MO_install_fullpath,
			SKSE_install_fullpath,
			TES5E_install_fullpath = m1utils_install.get_utilities_paths(download_cache_folder, filenames_list_in_order)
			#load SKSE_wanted_files, install paths and MO_config
			for utility in input_json['utilities']:
				if utility['name'] == 'Mod Organizer':
					MO_destination = utility['install_path'].replace('%SkyrimPath%',skyrim_dir)
					#if MO_destination ends with ModOrganizer, we need to remove it, because the archive is packed as a folder ModOrganizer
					#TODO but if the install_path will not end with ModOrganizer and user will want to extract to C:\SkyrimMods\MO for example
					#the result would be C:\SkyrimMods\MO\ModOrganizer, which might not be an issue, but its not "clean"
					#I just have to know the final destionation of MO so write_MO_ini function will work correctly
					if MO_destination.endswith('ModOrganizer'):
						MO_destination = MO_destination[:MO_destination.rfind('ModOrganizer')]
					if utility['name'] == 'SKSE':
						SKSE_wanted_files = utility['SKSE_wanted_files']
						SKSE_destination = utility['install_path'].replace('%SkyrimPath%',skyrim_dir)
					if utility['name'] == 'ENB':
						ENB_destination = utility['install_path'].replace('%SkyrimPath%',skyrim_dir)
					if utility['name'] == 'TES5Edit':
						TES5E_destination = utility['install_path'].replace('%SkyrimPath%',skyrim_dir)
					if utility['name'] == 'Mator Smash':
						Smash_destination = utility['install_path'].replace('%SkyrimPath%',skyrim_dir)
					MO_config = input_json['ModOrganizer.ini']


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

#dump
def get_base_utils(): #depreceated
	#------------fix from here
	#loads 7zip and wget urls from json
	for base_utility in input_json['base_utilities']:
		if base_utility['name'] == '7zip':
			w7zip_urls = base_utility['download']
		if base_utility['name'] == 'wget':
			wget_urls = base_utility['download']

	#downloads wget and unpack to '//bin' folder
	wget_path = m0prerequisites.unpack_to_bin(m0prerequisites.download(wget_urls,base_utilities_temp_folder))
	#if get_sevenzip_dir function finds 7z installed, it will use it
	#TODO meh, it runs get_sevenzip_dir twice, fix it and make it a whole function
	if isinstance(m0prerequisites.get_sevenzip_dir(), str):
		sevenzip_path = m0prerequisites.get_sevenzip_dir()
		if sevenzip_path.endswith('\\'): #TODO meh mess! search in that directory for proper file and test it, if fail then just do the download
			sevenzip_path += '7z.exe'
	else: # otherwise downloads wget and unpack to '//bin' folder
		sevenzip_path = m0prerequisites.unpack_to_bin(m0prerequisites.download(w7zip_urls,base_utilities_temp_folder))

	print('Base utility for downloading: ' + wget_path) #give it to next module
	print('Base utility for unpacking: '  + sevenzip_path) #give it to next module
	m0prerequisites.cleanup(base_utilities_temp_folder) #remove wget and 7zip downloads, DANGEROUS

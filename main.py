#main V0.1
#TODO, m0prerequisites needs better handling
#TODO, load json here and just give neceasery input to modules
#TODO write plugins.txt, loadorder.txt, skyrim.ini to MO profile, NMM?
#BIG TODO from json, push mod ids to downloader

import os, json
import sys

#------------------------------------config------------------------------------
json_file = 'mod_list_config.json'
wget_in_use_bug = True
#-------------------------------------defs-------------------------------------
#loading the json
def load_json(json_file):
	if os.path.exists(json_file):
		with open(json_file, 'r') as input_file:
			input_json = json.load(input_file)
	else:
		print('FAIL: File {0} does not exist'.format(json_file))
		print('FAIL: Exit 1')
		sys.exit(1)
	return input_json

import m0prerequisites # config for urls of utilities is there, TODO move to JSON
import m1download_utils # path to download the utilities is setup there, also TODO move to JSON
import m2utils_install # loading of this module causes lust for 7z binary, TODO fix a LOT

#-------------------------------0. Prerequisites-------------------------------
m0prerequisites.get_skyrim_dir()

input_json = load_json(json_file) #can cause exit 1 if file not found


for utility in input_json['base_utilities']:
	if utility['name'] == '7zip':
		w7zip_urls = utility['download']
	if utility['name'] == 'wget':
		wget_urls = utility['download']
		

#TODO check what can fail here
if wget_in_use_bug:
	wget_path = 'bin//wget.exe'
else:
	wget_path = m0prerequisites.unpack_to_bin(m0prerequisites.download(wget_urls,'tmp'))
sevenzip_path = m0prerequisites.unpack_to_bin(m0prerequisites.download(w7zip_urls,'tmp'))
#TODO make this nicer and understandable
if isinstance(m0prerequisites.get_sevenzip_dir(), str):
	sevenzip_path = m0prerequisites.get_sevenzip_dir() #meh, needs TODO from function
else:
	sevenzip_path = m0prerequisites.unpack_to_bin(download(w7zip_urls,'tmp'))

print('Base utility for downloading: ' + wget_path) #give it to next module	
print('Base utility for unpacking:'  + sevenzip_path) #give it to next module
m0prerequisites.cleanup()

#DOWNLOAD ALL UTILITIES
m1download_utils.download_all(input_json)
#-------------------------------1. Install base--------------------------------
base_install = True
#TODO install sumarry, what was installed sucessfuly and what not
if base_install:
	skyrim_dir, skyrim_mods_dir = m0prerequisites.confirm_dirs()
	m2utils_install.make_mods_folder_in_base(skyrim_mods_dir) #can cause exit 3
	m2utils_install.MO_install(skyrim_mods_dir)
	m2utils_install.SKSE_install(skyrim_dir, skyrim_mods_dir)
	m2utils_install.ENB_install(skyrim_dir, skyrim_mods_dir)
	m2utils_install.TES5E_install(skyrim_mods_dir)
	m2utils_install.Mash_install(skyrim_mods_dir)
	m2utils_install.write_MO_ini(skyrim_mods_dir)
	#m2utils_install.validate() #validate all

#--------------------------------2. Manual Work--------------------------------
print_guidance = False

if print_guidance:
	print("Using TES5 Edit cleanup Master files, here is how: http://wiki.step-project.com/User:Neovalen/Skyrim_Revisited_-_Legendary_Edition#Clean_The_Bethesda_ESMs")
	print("When you're finished do a Merged Patch, here is how: https://www.youtube.com/watch?v=BtLolEgVMTg")
	print("When you're finished do a Bashed Patch, here is how: https://www.youtube.com/watch?v=W1Es06MtAZM, http://wiki.step-project.com/Bashed_Patch or https://www.reddit.com/r/skyrimmods/wiki/beginners_guide_quickstart#wiki_create_a_bashed_patch")
	input('Confirm by any key when done')


# -----------------------------------3.test------------------------------------
#to unpack backup
##m2utils_install.use_sevenzip('x','e:\\project\\TES5_Skyrim\\0100-Patches.ready.group\\0100-Patches_test_pack.7z',skyrim_mods_dir + '\\ModOrganizer')
#to do a backup
##m2utils_install.use_sevenzip('a -t7z','d:\\games_stuff\TES5_Skyrim\\0100-Patches.ready.group\\0100-Patches_test_pack.7z','d:\Games\Steam\steamapps\common\Skyrim\Mods\\ModOrganizer\\profiles d:\Games\Steam\steamapps\common\Skyrim\Mods\\ModOrganizer\\overwrite d:\Games\Steam\steamapps\common\Skyrim\Mods\\ModOrganizer\\mods')

"""known issues
	bin//wget is in use and m0prerequisites tries to overwrite that, TODO fix
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
	3 failed to create directory skyrim_mods_dir
	99 Skyrim was not yet launched
"""
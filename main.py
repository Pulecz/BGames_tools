#main V0.4
#V0.1 - basic calling defs from modules
#V0.2 - some imports and functions here, load json and etc
#V0.3 - lot of polishing
#V0.4 - less functions, less modules, no subprocess

#------------------------------- import modules --------------------------------
from json import load, JSONDecodeError #for def load_json:
import m0prerequisites
import m1utils_install
import sys # for exits
#------------------------------------config-------------------------------------
json_file = 'utils.json'
utilities_download_dir = 'utilities'
print_guidance_switch = True
#-------------------------------------defs--------------------------------------


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


#how to unpack mod pack
def print_guidance():
	print("Using TES5 Edit cleanup Master files, here is how: http://wiki.step-project.com/User:Neovalen/Skyrim_Revisited_-_Legendary_Edition#Clean_The_Bethesda_ESMs")
	print("When you're finished do a Merged Patch, here is how: https://www.youtube.com/watch?v=BtLolEgVMTg")
	print("When you're finished do a Bashed Patch, here is how: https://www.youtube.com/watch?v=W1Es06MtAZM, http://wiki.step-project.com/Bashed_Patch or https://www.reddit.com/r/skyrimmods/wiki/beginners_guide_quickstart#wiki_create_a_bashed_patch")
	print("Then use verify_modpack.py to get whole modpack to ModOrganizer's download folder and follow the installation procedure described in modpack")
	input('Confirm by any key when done')


if __name__ == "__main__":
	#---------------------------- 0. Prerequisites -----------------------------
	try:
		skyrim_dir = m0prerequisites.get_skyrim_dir()
	except ValueError:
		print('No registry entry for Skyrim. Run Skyrim at least once')
		print('FAIL: Exit 99')
		sys.exit(99)

	input_json = try_load_json(json_file)
	if input_json is False:
		print('FAIL: Exit 1')
		sys.exit(1)

	utilities_data = m0prerequisites.dl_utilities(
	input_json, # for links
	utilities_download_dir, #where to download
	skyrim_dir) #for replacing %SkyrimPath in input_json

	input("Is {0} the correct dir for Skyrim?\nHit enter to confirm or ctrl+c to exit"
	.format(skyrim_dir))

	#----------------------------- 1. Do Install -------------------------------
	m1utils_install.install_utilities(utilities_data)

	mo_destination = utilities_data['Mod Organizer']['install_path']
	mo_config = input_json['ModOrganizer.ini']
	m1utils_install.write_MO_ini(mo_destination, mo_config, skyrim_dir)

	#TODO install sumarry, what was installed sucessfuly and what not
	if print_guidance_switch:
		print_guidance()
# -----------------------------------3.tests------------------------------------
"""
#to unpack backup
use_sevenzip(sevenzip_path, 'x','e:\\project\\TES5_Skyrim\\0100-Patches.ready.group\\0100-Patches_test_pack.7z',MO_destination')

#to do a backup, pack mods,overwrite,profiles
use_sevenzip(sevenzip_path, 'a -t7z','d:\\games_stuff\TES5_Skyrim\\0100-Patches.ready.group\\0100-Patches_test_pack.7z',
'd:\Games\Steam\steamapps\common\Skyrim\Mods\\ModOrganizer\\profiles
d:\Games\Steam\steamapps\common\Skyrim\Mods\\ModOrganizer\\overwrite
d:\Games\Steam\steamapps\common\Skyrim\Mods\\ModOrganizer\\mods')


what next
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
""" 0 all ok
	1 json_file not found
	99 Skyrim was not yet launched
"""

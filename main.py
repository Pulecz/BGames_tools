"""main V0.5
V0.1 - basic calling defs from modules
V0.2 - some imports and functions here, load json and etc
V0.3 - lot of polishing
V0.4 - less functions, less modules, no subprocess
V0.5 - custom_MO_categories and verify_modpack support

todo
	have all utils.json in CONST.py and have a GUI/CLI selector
	print('Done, writing, now writing default MO profile')
		write some SANE skyrimprefs.ini and other SANE defaults

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

#---------------------------------Return Codes---------------------------------
	0 all ok
	1 input error
	2 Unsupported Game
	99 Game was not yet launched - not in registry
"""
#------------------------------- import modules --------------------------------
import CONST #for loading utilities
from json import load, JSONDecodeError #for def load_json:
import m0prerequisites
import m1utils_install
import os
import sys # for exits
#------------------------------------config-------------------------------------
Game = 'Fallout 4'
#Game = 'Skyrim'
utilities_download_dir = 'utilities'

modpack_json = 'modpack.json'
mods_repo = r"s:\new\_need\TES5_Skyrim\MODS.REPO"

custom_MO_categories = 'CONST_data/MO2_FO4_categories.dat'
print_guidance_switch = True
debug = False
#-------------------------------------defs--------------------------------------
def print_guidance():
	"""Helper for user"""
	print("Started Mod Organizer, log in and update to 1.3.11")
	#print("Using TES5 Edit cleanup Master files, here is how: http://wiki.step-project.com/User:Neovalen/Skyrim_Revisited_-_Legendary_Edition#Clean_The_Bethesda_ESMs")
	#print("When you're finished do a Merged Patch, here is how: https://www.youtube.com/watch?v=BtLolEgVMTg")
	#print("When you're finished do a Bashed Patch, here is how: https://www.youtube.com/watch?v=W1Es06MtAZM, http://wiki.step-project.com/Bashed_Patch or https://www.reddit.com/r/skyrimmods/wiki/beginners_guide_quickstart#wiki_create_a_bashed_patch")
	print("Then use verify_modpack.py to get whole modpack to ModOrganizer's download folder and follow the installation procedure described in modpack")
	input('Confirm by any key when done')


if __name__ == "__main__":
	#---------------------------- 0. Prerequisites -----------------------------
	#json_file = 'fo4_utils.json
	#input_json = m2modpack_tools.try_load_json(json_file)
	if Game == 'Fallout 4':
		try:
			game_dir = m0prerequisites.game_dir_from_registry(r"SOFTWARE\WOW6432Node\Bethesda Softworks\Fallout4")
		except ValueError:
			print('No registry entry for Fallout 4. Run Fallout 4 at least once')
			print('ERROR: Exit 99')
			sys.exit(99)
		input_json = CONST.fallout4_utils
		mo_destination = os.environ['LOCALAPPDATA'] + r'\\ModOrganizer\\Fallout 4'
	elif Game == 'Skyrim':
		try:
			game_dir = m0prerequisites.game_dir_from_registry(r"SOFTWARE\WOW6432Node\Bethesda Softworks\skyrim")
		except ValueError:
			print('No registry entry for Skyrim. Run Skyrim at least once')
			print('ERROR: Exit 99')
			sys.exit(99)
		input_json = CONST.skyrim_utils
		mo_destination = utilities_data['Mod Organizer']['install_path']
	else:
		print("ERROR: Unsuported game", Game, ". Exit 2")
		sys.exit(2)

	utilities_data = m0prerequisites.dl_utilities(
	input_json, # for links
	utilities_download_dir, #where to download
	game_dir) #for replacing %SkyrimPath in input_json

	input("Is {0} the correct dir for {1}?\nHit enter to confirm or ctrl+c to exit"
	.format(game_dir, Game))
	#----------------------------- 1. Do Install -------------------------------
	m1utils_install.install_utilities(input_json['game'], utilities_data)
	#---------------------- 2. Handle Mod Organizer Ini ------------------------
	mo_config = input_json['ModOrganizer.ini']

	#make sure destination exist
	if not os.path.exists(mo_destination):
		os.makedirs(mo_destination)
	#do write
	m1utils_install.write_MO_ini(mo_destination, mo_config, game_dir)
	#if any custom categories write them
	if custom_MO_categories:
		if Game == 'Fallout 4':
			m1utils_install.write_MO_categories(custom_MO_categories, os.environ['LOCALAPPDATA'] + r'\\ModOrganizer\\Fallout 4\\categories.dat')
		#TODO if Game == 'Skyrim':

	#TODO install sumarry, what was installed sucessfuly and what not
	if print_guidance_switch:
		print_guidance()

	#TODO pass to verify_modpack
	#categories_content=m1utils_install.load_MO_categories_content(custom_MO_categories)
	#verify_modpack.main(Game, modpack_json, mods_repo, mo_destination, debug=debug)

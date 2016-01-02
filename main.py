import ASI_base_install # loading of this module causes lust for 7z binary

base_install = True

#------------------------------0. Install base----------------------------------
#todo check if Skyrim was launched at least once (so its in a registry and all)
#todo install sumarry, what was installed sucessfuly and what not
if base_install:
	skyrim_dir, skyrim_mods_dir = ASI_base_install.confirm_dirs()
	ASI_base_install.make_mods_folder_in_base() #can cause exit 2
	ASI_base_install.MO_install()
	ASI_base_install.write_MO_ini()
	ASI_base_install.SKSE_install()
	ASI_base_install.ENB_install()
	ASI_base_install.LOOT_install()
	ASI_base_install.WRYE_BASH_install()
	ASI_base_install.TES5E_install()
	#ASI_base_install.validate() #validate all

#-------------------------------1. Manual Work----------------------------------
print_guidance = False

if print_guidance:
	print("Using TES5 Edit cleanup Master files, here is how: http://wiki.step-project.com/User:Neovalen/Skyrim_Revisited_-_Legendary_Edition#Clean_The_Bethesda_ESMs")
	print("When you're finished do a Merged Patch, here is how: https://www.youtube.com/watch?v=BtLolEgVMTg")
	print("When you're finished do a Bashed Patch, here is how: https://www.youtube.com/watch?v=W1Es06MtAZM, http://wiki.step-project.com/Bashed_Patch or https://www.reddit.com/r/skyrimmods/wiki/beginners_guide_quickstart#wiki_create_a_bashed_patch")
	input('Confirm by any key when done')


#--------2. test--------
#to unpack backup
##ASI_base_install.use_sevenzip('x','e:\\project\\TES5_Skyrim\\0100-Patches.ready.group\\0100-Patches_test_pack.7z',skyrim_mods_dir + '\\ModOrganizer')
#to do a backup
##ASI_base_install.use_sevenzip('a -t7z','d:\\games_stuff\TES5_Skyrim\\0100-Patches.ready.group\\0100-Patches_test_pack.7z','d:\Games\Steam\steamapps\common\Skyrim\Mods\\ModOrganizer\\profiles d:\Games\Steam\steamapps\common\Skyrim\Mods\\ModOrganizer\\overwrite d:\Games\Steam\steamapps\common\Skyrim\Mods\\ModOrganizer\\mods')

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
#--------------------------------Return Codes-----------------------------------
""" RC
	0 all ok
	1 no 7z binary in ProgramFiles
	2 failed to create directory skyrim_mods_dir
"""

#--------------------------------Manual Guide-----------------------------------
#in howto

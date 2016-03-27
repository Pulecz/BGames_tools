#m2utils_install V0.4

""" change-log
	V01 - general improvements
	V02 - changed ENB install to 7z, enb and MO install via 7z now, putt local_repo to dict
	V03 - get_sevenzip_bin and write_MO_ini function and some more stuff
	V04 - deleted LOOT and Wrye support, first changes to work with m0prerequisites
"""

""" todos
	todo0 #ASI_base_install.validate()
		- function for validating the installed procedure	
	todo1 read input from config file
	todo2 no installed path in registry, fix
		- (skyrim launched once?, or rather guess folder and ask)
	todo3 ENB_install, do not install enblocal.ini but pick recommended one
		- use DxDiag to determine ram,vram,gpu, etc
		- use ENB_config_install_fullpath to extract correct ini
	todo4 use ENB Manager and Changer
		Mods\enb_manager and copy enbhost.exe and d3d9.dll to ENB Versions\name
	todo5 what about skyrim.ini skyrimprefs.ini?
	todo6 install to paths loaded from JSON
	and just about everything which is marked as #TODO
"""

import sys, os, subprocess, zipfile
from collections import OrderedDict

def get_sevenzip_bin():
	#BIG TODO check what 0prerequisites gives you
	sevenzip_bin = os.getenv('programfiles')+'\\7-Zip\\7z.exe' # or search for it, or just use local
	# check for 7z
	if not os.path.isfile(sevenzip_bin):
		if not os.path.isfile('bin//7za.exe'): #TODO fix hardcoded
			print('No 7z binary downloaded, big FAIL!')
			sys.exit(1)
		else:
			return 'bin//7za.exe' #TODO fix hardcoded
		print('No 7z binary at {0} can\'t extract without it.'.format(sevenzip_bin))
		sys.exit(1)
	return sevenzip_bin

	
def use_sevenzip(action, source, output_dir): #not used in the script, only tested for unpacking backups
	#action = e or x or l
	#source = archive name
	#output_dir = where to extract
	#paramaters = 
		#-y option will always overwrite
	##parameters = ' x "' + TES5E_install_fullpath + '" -o' + skyrim_mods_dir + '\\TES5Edit -y'
	if 'a' in action: #for archive
		sevenzip_command = sevenzip_bin + ' ' + action + ' "' + source + '" ' + output_dir
		#output_dir = list of files to compress
	else:
		sevenzip_command = sevenzip_bin + ' ' + action + ' "' + source + '" -o"' + output_dir + '"'
	sevenzip_subprocess = subprocess.Popen(sevenzip_command, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
	sevenzip_subprocess.communicate()

#--------------------------------Testing Input---------------------------------
#skyrim_dir = 'd:\\Games\\Steam\\steamapps\\common\\Skyrim\\'
#---------------------------------Input Paths----------------------------------
sevenzip_bin = get_sevenzip_bin() #can cause exit 1

#---------------------------------Input Files----------------------------------
#TODO get dynamically from config and from downloaded utilities
#TODO md5sum check
install_repo_dir = os.getcwd() + '\\utilities\\' #TODO fix hardcoded
local_repo = {
	'MO_install_7zarchive' : 'ModOrganizer_v1.3.10.7z', # http://www.nexusmods.com/skyrim/mods/1334/?
	'SKSE_install_7zarchive' : 'skse_1_07_03.7z', # http://skse.silverlock.org
	'ENB_install_archive' : 'enbseries_skyrim_v0305.zip', # http://enbdev.com/download_mod_tesskyrim.htm
	'ENB_config_install' : 'ENBoost 5_0-38649-5-0.zip', # http://www.nexusmods.com/skyrim/mods/38649/?
	'TES5E_install_7zarchive' : 'TES5Edit_3_1_2.7z', # http://www.nexusmods.com/skyrim/mods/25859/?
	'Mash_install_archive' : 'MatorSmash.zip' # https://github.com/matortheeternal/smash/releases/
}

MO_install_fullpath = install_repo_dir + local_repo['MO_install_7zarchive']
SKSE_install_fullpath = install_repo_dir + local_repo['SKSE_install_7zarchive']
ENB_install_fullpath = install_repo_dir + local_repo['ENB_install_archive']
ENB_config_install_fullpath = install_repo_dir + local_repo['ENB_config_install']
TES5E_install_fullpath = install_repo_dir + local_repo['TES5E_install_7zarchive']
Mash_install_fullpath = install_repo_dir + local_repo['Mash_install_archive']

enb_wanted_files = ['WrapperVersion/d3d9.dll', 'WrapperVersion/enbhost.exe']
SKSE_install_source_needed = ['skse_1_07_03\\skse_readme.txt', 'skse_1_07_03\\skse_whatsnew.txt', 'skse_1_07_03\\Data\\scripts\\activemagiceffect.pex', 'skse_1_07_03\\Data\\scripts\\actor.pex', 'skse_1_07_03\\Data\\scripts\\actorbase.pex', 'skse_1_07_03\\Data\\scripts\\actorvalueinfo.pex', 'skse_1_07_03\\Data\\scripts\\alias.pex', 'skse_1_07_03\\Data\\scripts\\ammo.pex', 'skse_1_07_03\\Data\\scripts\\apparatus.pex', 'skse_1_07_03\\Data\\scripts\\armor.pex', 'skse_1_07_03\\Data\\scripts\\armoraddon.pex', 'skse_1_07_03\\Data\\scripts\\art.pex', 'skse_1_07_03\\Data\\scripts\\book.pex', 'skse_1_07_03\\Data\\scripts\\cell.pex', 'skse_1_07_03\\Data\\scripts\\colorcomponent.pex', 'skse_1_07_03\\Data\\scripts\\colorform.pex', 'skse_1_07_03\\Data\\scripts\\combatstyle.pex', 'skse_1_07_03\\Data\\scripts\\constructibleobject.pex', 'skse_1_07_03\\Data\\scripts\\defaultobjectmanager.pex', 'skse_1_07_03\\Data\\scripts\\enchantment.pex', 'skse_1_07_03\\Data\\scripts\\equipslot.pex', 'skse_1_07_03\\Data\\scripts\\faction.pex', 'skse_1_07_03\\Data\\scripts\\flora.pex', 'skse_1_07_03\\Data\\scripts\\form.pex', 'skse_1_07_03\\Data\\scripts\\formlist.pex', 'skse_1_07_03\\Data\\scripts\\formtype.pex', 'skse_1_07_03\\Data\\scripts\\game.pex', 'skse_1_07_03\\Data\\scripts\\gamedata.pex', 'skse_1_07_03\\Data\\scripts\\headpart.pex', 'skse_1_07_03\\Data\\scripts\\ingredient.pex', 'skse_1_07_03\\Data\\scripts\\input.pex', 'skse_1_07_03\\Data\\scripts\\keyword.pex', 'skse_1_07_03\\Data\\scripts\\leveledactor.pex', 'skse_1_07_03\\Data\\scripts\\leveleditem.pex', 'skse_1_07_03\\Data\\scripts\\leveledspell.pex', 'skse_1_07_03\\Data\\scripts\\magiceffect.pex', 'skse_1_07_03\\Data\\scripts\\math.pex', 'skse_1_07_03\\Data\\scripts\\modevent.pex', 'skse_1_07_03\\Data\\scripts\\netimmerse.pex', 'skse_1_07_03\\Data\\scripts\\objectreference.pex', 'skse_1_07_03\\Data\\scripts\\outfit.pex', 'skse_1_07_03\\Data\\scripts\\perk.pex', 'skse_1_07_03\\Data\\scripts\\potion.pex', 'skse_1_07_03\\Data\\scripts\\quest.pex', 'skse_1_07_03\\Data\\scripts\\race.pex', 'skse_1_07_03\\Data\\scripts\\scroll.pex', 'skse_1_07_03\\Data\\scripts\\shout.pex', 'skse_1_07_03\\Data\\scripts\\skse.pex', 'skse_1_07_03\\Data\\scripts\\soulgem.pex', 'skse_1_07_03\\Data\\scripts\\sound.pex', 'skse_1_07_03\\Data\\scripts\\sounddescriptor.pex', 'skse_1_07_03\\Data\\scripts\\spawnertask.pex', 'skse_1_07_03\\Data\\scripts\\spell.pex', 'skse_1_07_03\\Data\\scripts\\stringutil.pex', 'skse_1_07_03\\Data\\scripts\\textureset.pex', 'skse_1_07_03\\Data\\scripts\\treeobject.pex', 'skse_1_07_03\\Data\\scripts\\ui.pex', 'skse_1_07_03\\Data\\scripts\\uicallback.pex', 'skse_1_07_03\\Data\\scripts\\utility.pex', 'skse_1_07_03\\Data\\scripts\\weapon.pex', 'skse_1_07_03\\Data\\scripts\\weather.pex', 'skse_1_07_03\\Data\\scripts\\wornobject.pex', 'skse_1_07_03\\skse_loader.exe', 'skse_1_07_03\\skse_1_9_32.dll', 'skse_1_07_03\\skse_steam_loader.dll']


#----------------------------Prepare Skyrim Folder-----------------------------
#can cause exit 3
def make_mods_folder_in_base(skyrim_mods_dir):
	if os.path.exists(skyrim_mods_dir):
		print('OK: Folder {0} exist'.format(skyrim_mods_dir))
	else:
		print('Making folder {0}'.format(skyrim_mods_dir))
		try:
			os.mkdir(skyrim_mods_dir)
		except OSError as mods_mkdir_err:
			print(mods_mkdir_err)
			sys.exit(3)
#-----------------------------Install ModOrganizer-----------------------------
#this function can also extract the insttaler, but its better to use the archive
def MO_install(skyrim_mods_dir):
	print("Installing ModOrganizer")
	#-y option will always overwrite
	sevenzip_command = sevenzip_bin + ' x "' + MO_install_fullpath + '" -o"' + skyrim_mods_dir + '" -y' #unpack ModOrganizer directory to skyrim_mods_dir
	MO_7z_subprocess = subprocess.Popen(sevenzip_command, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
	MO_7z_subprocess.communicate()


def write_MO_ini(skyrim_mods_dir): #TODO make it dynamic and in JSON
	MO_ini_CE = {
	  "1": {
		"title": "SKSE",
		"custom": "false",
		"toolbar": "false",
		"ownicon": "false"
	  },
	  "2": {
		"title": "Skyrim",
		"custom": "false",
		"toolbar": "false",
		"ownicon": "false"
	  },
	  "3": {
		"title": "Skyrim Launcher",
		"custom": "false",
		"toolbar": "false",
		"ownicon": "false"
	  },
	  "4": {
		"title": "TES5Edit",
		"custom": "true",
		"toolbar": "true",
		"ownicon": "true",
		"binary": skyrim_mods_dir + "/TES5Edit/TES5Edit.exe",
		"arguments": "",
		"workingDirectory": "",
		"closeOnStart": "false",
		"steamAppID": ""
	  },
	  "5": {
		"title": "Smash",
		"custom": "true",
		"toolbar": "true",
		"ownicon": "true",
		"binary": skyrim_mods_dir + "/Smash/MatorSmash.exe",
		"arguments": "",
		"workingDirectory": "",
		"closeOnStart": "false",
		"steamAppID": ""
	  }
	}
	print("Writing ModOrganizer.ini")
	with open(os.path.join(skyrim_mods_dir + '\\ModOrganizer\\ModOrganizer.ini'),'w') as MO_ini: #TODO dynamic path
		#[Plugins]
		MO_ini.write('[Plugins]\n')
		MO_ini.write('BSA%20Extractor\enabled=true\n')
		MO_ini.write('Basic%20diagnosis%20plugin\check_modorder=false\n')
		MO_ini.write('\n')
		#[customExecutables]
		MO_ini.write('[customExecutables]\n')
		MO_ini.write('size=5\n') #TODO calculate size by length of json
		for key in OrderedDict(sorted(MO_ini_CE.items())):
			MO_ini.write(key + '\\title=' + MO_ini_CE[key]['title'] + '\n')
			MO_ini.write(key + '\\custom=' + MO_ini_CE[key]['custom'] + '\n')
			MO_ini.write(key + '\\toolbar=' + MO_ini_CE[key]['toolbar'] + '\n')
			MO_ini.write(key + '\\ownicon=' + MO_ini_CE[key]['ownicon'] + '\n')
			if MO_ini_CE[key]['custom'] == 'true':
				MO_ini.write(key + '\\binary=' + MO_ini_CE[key]['binary'].replace('\\','/') + '\n')
				MO_ini.write(key + '\\arguments=' + MO_ini_CE[key]['arguments'].replace('\\','/') + '\n')
				MO_ini.write(key + '\\workingDirectory=' + MO_ini_CE[key]['workingDirectory'].replace('\\','/') + '\n')
				MO_ini.write(key + '\\closeOnStart=' + MO_ini_CE[key]['closeOnStart'].replace('\\','/') + '\n')
				MO_ini.write(key + '\\steamAppID=' + MO_ini_CE[key]['steamAppID'].replace('\\','/') + '\n')
#---------------------------------Install SKSE---------------------------------
def SKSE_install(skyrim_dir, skyrim_mods_dir):
	print("Installing SKSE")
	#-y option will always overwrite
	#initialize the list of files we want to extract
	source_root = ""
	source_data = ""
	for file in SKSE_install_source_needed:
		if 'skse_1_07_03\\Data\\scripts' in file:
			source_data += file + ' '
		if not 'skse_1_07_03\\Data' in file:
			source_root += file + ' ' 
	#everything from root to root Skyrim Folder
	sevenzip_command_root = sevenzip_bin + ' e "' + SKSE_install_fullpath + '" -o"' + skyrim_dir + '\\" -y ' + source_root
	#everything in data\\scripts to Skyrim\data folder (7z will create the scripts folder)
	sevenzip_command_data = sevenzip_bin + ' e "' + SKSE_install_fullpath + '" -o"' + skyrim_dir + '\\Data\\scripts" -y ' + source_data
	SKSE_7z_subprocess_root = subprocess.Popen(sevenzip_command_root, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
	SKSE_7z_subprocess_root.communicate()
	SKSE_7z_subprocess_data = subprocess.Popen(sevenzip_command_data, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
	SKSE_7z_subprocess_data.communicate()
#---------------------------------Install ENB----------------------------------
def ENB_install(skyrim_dir, skyrim_mods_dir):
	#initialize the list of files we want to extract
	source_root = ""
	for file in enb_wanted_files:
		source_root += file + ' '
	print("Installing ENB")
	sevenzip_command_root = sevenzip_bin + ' e "' + ENB_install_fullpath + '" -o"' + skyrim_dir + '\\" -y ' + source_root
	ENB_7z_subprocess_root = subprocess.Popen(sevenzip_command_root, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
	ENB_7z_subprocess_root.communicate()
#------------------------------Install TES5 Edit-------------------------------
def TES5E_install(skyrim_mods_dir):
	print("Installing TES5 Edit")
	#-y option will always overwrite
	sevenzip_command = sevenzip_bin + ' x "' + TES5E_install_fullpath + '" -o"' + skyrim_mods_dir + '\\TES5Edit" -y'
	TES5E_7z_subprocess = subprocess.Popen(sevenzip_command, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
	TES5E_7z_subprocess.communicate()
#---------------------------------Install Mash---------------------------------
#no need to do this via 7z, Mator packs in zip, so ZipFile library could be used
def Mash_install(skyrim_mods_dir):
	print('Installing Smash')
	#-y option will always overwrite
	sevenzip_command = sevenzip_bin + ' x "' + Mash_install_fullpath + '" -o"' + skyrim_mods_dir + '\\Smash" -y'
	Smash_7z_subprocess = subprocess.Popen(sevenzip_command, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
	Smash_7z_subprocess.communicate()
import sys, os, subprocess, zipfile
from collections import OrderedDict


def get_skyrim_dir():
	wincmd_req_query_skyrim_dir='REG QUERY "HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Bethesda Softworks\skyrim" /v "installed path" /t REG_SZ'
	skyrim_dir_mess = subprocess.check_output(wincmd_req_query_skyrim_dir)
	##rfind('End of search') might depend on language
	skyrim_dir = str(skyrim_dir_mess)[str(skyrim_dir_mess).find('REG_SZ')+6:str(skyrim_dir_mess).rfind('End of search')].strip().replace('\\r\\n\\r\\n','')
	return skyrim_dir

	
def confirm_dir(msg, default):
	dir = input(msg + ' \n\nIs it ' + default + ' ?\nHit enter to confirm') or\
	default
	return dir

	
def get_sevenzip_bin():
	sevenzip_bin = os.getenv('programfiles')+'\\7-Zip\\7z.exe' # or search for it, or just use local
	# check for 7z
	if not os.path.isfile(sevenzip_bin):
		print('No 7z binary at {0} can\'t extract without it.'.format(sevenzip_bin))
		sys.exit(1)
	return sevenzip_bin

	
def use_sevenzip(action, source, output_dir):#
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


def confirm_dirs():
	global skyrim_dir
	global skyrim_mods_dir
	#todo2 check if skyrim was launched at least once
	#if skyrim_launched
	try:
		skyrim_dir = get_skyrim_dir()
	except OSError as e: #todo2
		print(e)

	#confirm skyrim_dir
	skyrim_dir = confirm_dir('Enter the full path to Skyrim:',
	skyrim_dir)
	#confirm skyrim_mods_dir
	skyrim_mods_dir = confirm_dir('\n\nEnter the full path to Skyrim Mods folder:',
	os.path.join(skyrim_dir,mods_dir_name))
	return (skyrim_dir, skyrim_mods_dir)

""" change-log
	V01 - general improvements
	V02 - changed ENB install to 7z, enb and MO install via 7z now, putt local_repo to dict
	V03 - get_sevenzip_bin and write_MO_ini function and some more stuff
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
"""

#-------------------------------Testing Input-----------------------------------
#skyrim_dir = 'd:\\Games\\Steam\\steamapps\\common\\Skyrim\\'
#--------------------------------Input Paths------------------------------------
mods_dir_name = 'Mods'
sevenzip_bin = get_sevenzip_bin() #can cause exit 1

#--------------------------------Input Files------------------------------------
#todo could be in a ini config
#todo md5sum check
install_repo_dir = os.getcwd() + '\\install_repo\\'
local_repo = {
	'MO_install_7zarchive' : 'Mod Organizer v1_3_11-1334-1-3-11.7z', # http://www.nexusmods.com/skyrim/mods/1334/?
	'MO_installer' : 'Mod Organizer v1_3_11 installer-1334-1-3-11.exe', # http://www.nexusmods.com/skyrim/mods/1334/?
	'SKSE_install_7zarchive' : 'skse_1_07_03.7z', # http://skse.silverlock.org
	'SKSE_installer' :'skse_1_07_03_installer.exe',	# http://skse.silverlock.org
	'ENB_install_archive' : 'enbseries_skyrim_v0290.zip', # http://enbdev.com/download_mod_tesskyrim.htm
	'ENB_config_install' : 'ENBoost 5_0-38649-5-0.zip', # http://www.nexusmods.com/skyrim/mods/38649/?
	'LOOT_install_7zarchive' : 'LOOT.v0.8.1.7z', # https://loot.github.io/
	#'LOOT_install_7zarchive' : 'LOOT v0.8.1-53-gaac5583 - Snapshot-5310-0-8-1-53.7z', # using f4 http://www.nexusmods.com/fallout4/mods/5310/?
	'WRYE_BASH_install_7zarchive' : 'Wrye Bash 306 - Standalone Executable-1840-306.7z', # http://www.nexusmods.com/skyrim/mods/1840/
	'TES5E_install_7zarchive' : 'TES5Edit 3.1.2-25859-3-1-2.7z' # http://www.nexusmods.com/skyrim/mods/25859/?
}

##todo local_repo_checksum = {}
MO_install_fullpath = install_repo_dir + local_repo['MO_install_7zarchive']
MO_installer_fullpath = install_repo_dir + local_repo['MO_installer']
SKSE_install_fullpath = install_repo_dir + local_repo['SKSE_install_7zarchive']
SKSE_installer_fullpath = install_repo_dir + local_repo['SKSE_installer']
ENB_install_fullpath = install_repo_dir + local_repo['ENB_install_archive']
ENB_config_install_fullpath = install_repo_dir + local_repo['ENB_config_install']
LOOT_install_fullpath = install_repo_dir + local_repo['LOOT_install_7zarchive']
WRYE_BASH_install_fullpath = install_repo_dir + local_repo['WRYE_BASH_install_7zarchive']
TES5E_install_fullpath = install_repo_dir + local_repo['TES5E_install_7zarchive']

enb_wanted_files = ['WrapperVersion/d3d9.dll', 'WrapperVersion/enbhost.exe']
SKSE_install_source_needed = ['skse_1_07_03\\skse_readme.txt', 'skse_1_07_03\\skse_whatsnew.txt', 'skse_1_07_03\\Data\\scripts\\activemagiceffect.pex', 'skse_1_07_03\\Data\\scripts\\actor.pex', 'skse_1_07_03\\Data\\scripts\\actorbase.pex', 'skse_1_07_03\\Data\\scripts\\actorvalueinfo.pex', 'skse_1_07_03\\Data\\scripts\\alias.pex', 'skse_1_07_03\\Data\\scripts\\ammo.pex', 'skse_1_07_03\\Data\\scripts\\apparatus.pex', 'skse_1_07_03\\Data\\scripts\\armor.pex', 'skse_1_07_03\\Data\\scripts\\armoraddon.pex', 'skse_1_07_03\\Data\\scripts\\art.pex', 'skse_1_07_03\\Data\\scripts\\book.pex', 'skse_1_07_03\\Data\\scripts\\cell.pex', 'skse_1_07_03\\Data\\scripts\\colorcomponent.pex', 'skse_1_07_03\\Data\\scripts\\colorform.pex', 'skse_1_07_03\\Data\\scripts\\combatstyle.pex', 'skse_1_07_03\\Data\\scripts\\constructibleobject.pex', 'skse_1_07_03\\Data\\scripts\\defaultobjectmanager.pex', 'skse_1_07_03\\Data\\scripts\\enchantment.pex', 'skse_1_07_03\\Data\\scripts\\equipslot.pex', 'skse_1_07_03\\Data\\scripts\\faction.pex', 'skse_1_07_03\\Data\\scripts\\flora.pex', 'skse_1_07_03\\Data\\scripts\\form.pex', 'skse_1_07_03\\Data\\scripts\\formlist.pex', 'skse_1_07_03\\Data\\scripts\\formtype.pex', 'skse_1_07_03\\Data\\scripts\\game.pex', 'skse_1_07_03\\Data\\scripts\\gamedata.pex', 'skse_1_07_03\\Data\\scripts\\headpart.pex', 'skse_1_07_03\\Data\\scripts\\ingredient.pex', 'skse_1_07_03\\Data\\scripts\\input.pex', 'skse_1_07_03\\Data\\scripts\\keyword.pex', 'skse_1_07_03\\Data\\scripts\\leveledactor.pex', 'skse_1_07_03\\Data\\scripts\\leveleditem.pex', 'skse_1_07_03\\Data\\scripts\\leveledspell.pex', 'skse_1_07_03\\Data\\scripts\\magiceffect.pex', 'skse_1_07_03\\Data\\scripts\\math.pex', 'skse_1_07_03\\Data\\scripts\\modevent.pex', 'skse_1_07_03\\Data\\scripts\\netimmerse.pex', 'skse_1_07_03\\Data\\scripts\\objectreference.pex', 'skse_1_07_03\\Data\\scripts\\outfit.pex', 'skse_1_07_03\\Data\\scripts\\perk.pex', 'skse_1_07_03\\Data\\scripts\\potion.pex', 'skse_1_07_03\\Data\\scripts\\quest.pex', 'skse_1_07_03\\Data\\scripts\\race.pex', 'skse_1_07_03\\Data\\scripts\\scroll.pex', 'skse_1_07_03\\Data\\scripts\\shout.pex', 'skse_1_07_03\\Data\\scripts\\skse.pex', 'skse_1_07_03\\Data\\scripts\\soulgem.pex', 'skse_1_07_03\\Data\\scripts\\sound.pex', 'skse_1_07_03\\Data\\scripts\\sounddescriptor.pex', 'skse_1_07_03\\Data\\scripts\\spawnertask.pex', 'skse_1_07_03\\Data\\scripts\\spell.pex', 'skse_1_07_03\\Data\\scripts\\stringutil.pex', 'skse_1_07_03\\Data\\scripts\\textureset.pex', 'skse_1_07_03\\Data\\scripts\\treeobject.pex', 'skse_1_07_03\\Data\\scripts\\ui.pex', 'skse_1_07_03\\Data\\scripts\\uicallback.pex', 'skse_1_07_03\\Data\\scripts\\utility.pex', 'skse_1_07_03\\Data\\scripts\\weapon.pex', 'skse_1_07_03\\Data\\scripts\\weather.pex', 'skse_1_07_03\\Data\\scripts\\wornobject.pex', 'skse_1_07_03\\skse_loader.exe', 'skse_1_07_03\\skse_1_9_32.dll', 'skse_1_07_03\\skse_steam_loader.dll']

#---------------------------Prepare Skyrim Folder-------------------------------
#can cause exit 2
def make_mods_folder_in_base():
	if os.path.exists(skyrim_mods_dir):
		print('OK: Folder {0} exist'.format(skyrim_mods_dir))
	else:
		print('Making folder {0} in {1}'.format(mods_dir_name,skyrim_dir))
		try:
			os.mkdir(skyrim_mods_dir)
		except OSError as mods_mkdir_err:
			print(mods_mkdir_err)
			sys.exit(2)
#----------------------------Install ModOrganizer-------------------------------
def MO_installer(): #not automatic, decomissioned
	#todo silent install
	print("Install Mod Organizer correctly or FU")
	print("Launch MO after everything finishes, so it detects executables")
	MO_install_subprocess = subprocess.Popen(MO_installer_fullpath, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
	MO_install_subprocess.wait()
	

def MO_install():
	print("Installing ModOrganizer")
	#-y option will always overwrite
	sevenzip_command = sevenzip_bin + ' x "' + MO_install_fullpath + '" -o"' + skyrim_mods_dir + '" -y' #unpack ModOrganizer directory to skyrim_mods_dir
	MO_7z_subprocess = subprocess.Popen(sevenzip_command, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
	MO_7z_subprocess.communicate()


def write_MO_ini():
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
		"title": "LOOT",
		"custom": "true",
		"toolbar": "true",
		"ownicon": "true",
		"binary": skyrim_mods_dir + "/LOOT/LOOT.exe",
		"arguments": "",
		"workingDirectory": "",
		"closeOnStart": "false",
		"steamAppID": ""

	  },
	  "5": {
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
	  "6": {
		"title": "Wrye Bash",
		"custom": "true",
		"toolbar": "true",
		"ownicon": "true",
		"binary": skyrim_mods_dir + "/Mopy/Wrye Bash.exe",
		"arguments": "",
		"workingDirectory": "",
		"closeOnStart": "false",
		"steamAppID": ""
	  }
	}
	print("Writing ModOrganizer.ini")
	with open(os.path.join(skyrim_mods_dir + '\\ModOrganizer\\ModOrganizer.ini'),'w') as MO_ini:
		#[Plugins]
		MO_ini.write('[Plugins]\n')
		MO_ini.write('BSA%20Extractor\enabled=true\n')
		MO_ini.write('Basic%20diagnosis%20plugin\check_modorder=false\n')
		MO_ini.write('\n')
		#[customExecutables]
		MO_ini.write('[customExecutables]\n')
		MO_ini.write('size=6\n')
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
#--------------------------------Install SKSE-----------------------------------
def SKSE_installer(silent=False): #requires admin rights, decomissioned
	global SKSE_installer_fullpath
	if silent:
		#/S for silent install, tested and ok OK
		SKSE_install_fullpath += ' /S'
		print("Automatic SKSE Install") 
	else:
		print("Please use the wizzard")
	try:
		SKSE_install_subprocess = subprocess.Popen(SKSE_installer_fullpath, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
		SKSE_install_subprocess.wait()
	except OSError as error:
		if error.errno == 22: # requires run as admin
			print ("Calling SKSE Install requires admin rights, skipping")


def SKSE_install():
	print("Installing SKSE")
	#-y option will always overwrite
	source_root = ""
	source_data = ""
	#extract using list of files
	for file in SKSE_install_source_needed:
		if 'skse_1_07_03\\Data\\scripts' in file:
			source_data += file + ' '
		if not 'skse_1_07_03\\Data' in file:
			source_root += file + ' ' 
	#everything from root to root
	sevenzip_command_root = sevenzip_bin + ' e "' + SKSE_install_fullpath + '" -o"' + skyrim_dir + '\\" -y ' + source_root
	#everything in data\\scripts to \data
	sevenzip_command_data = sevenzip_bin + ' e "' + SKSE_install_fullpath + '" -o"' + skyrim_dir + '\\Data\\scripts" -y ' + source_data
	SKSE_7z_subprocess_root = subprocess.Popen(sevenzip_command_root, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
	SKSE_7z_subprocess_root.communicate()
	SKSE_7z_subprocess_data = subprocess.Popen(sevenzip_command_data, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
	SKSE_7z_subprocess_data.communicate()
#--------------------------------Install ENB------------------------------------
def ENB_install():
	source_root = ""
	for file in enb_wanted_files:
		source_root += file + ' '
	print("Installing ENB")
	sevenzip_command_root = sevenzip_bin + ' e "' + ENB_install_fullpath + '" -o"' + skyrim_dir + '\\" -y ' + source_root
	ENB_7z_subprocess_root = subprocess.Popen(sevenzip_command_root, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
	ENB_7z_subprocess_root.communicate()
#--------------------------------Install LOOT-----------------------------------
def LOOT_install():
	print("Installing LOOT")
	#print("WARNING: Installing F4 LOOT version, official does not work on my W10")
	#-y option will always overwrite
	sevenzip_command = sevenzip_bin + ' x "' + LOOT_install_fullpath + '" -o"' + skyrim_mods_dir + '\\LOOT" -y'
	LOOT_7z_subprocess = subprocess.Popen(sevenzip_command, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
	LOOT_7z_subprocess.communicate()
#-----------------------------Install Wrye Bash---------------------------------
def WRYE_BASH_install():
	print("Installing Wrye Bash")
	#-y option will always overwrite
	sevenzip_command = sevenzip_bin + ' x "' + WRYE_BASH_install_fullpath + '" -o"' + skyrim_mods_dir + '\\" -y'
	WRYE_BASH_7z_subprocess = subprocess.Popen(sevenzip_command, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
	WRYE_BASH_7z_subprocess.communicate()
#-----------------------------Install TES5 Edit---------------------------------
def TES5E_install():
	print("Installing TES5 Edit")
	#-y option will always overwrite
	sevenzip_command = sevenzip_bin + ' x "' + TES5E_install_fullpath + '" -o"' + skyrim_mods_dir + '\\TES5Edit" -y'
	TES5E_7z_subprocess = subprocess.Popen(sevenzip_command, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
	TES5E_7z_subprocess.communicate()

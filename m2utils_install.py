#m2utils_install V0.5
#NOT PYTHONIC, 7zip calls can be replaced by lzma https://docs.python.org/3/library/lzma.html

""" change-log
	V01 - general improvements
	V02 - changed ENB install to 7z, enb and MO install via 7z now, putt local_repo to dict
	V03 - get_sevenzip_bin and write_MO_ini function and some more stuff
	V04 - deleted LOOT and Wrye support, first changes to work with m0prerequisites
	V05 - get_sevenzip_bin replaced by logic in main which is TODO function, no config is here, main sends everything, make_mods_folder_in_base deleted, no longer needed
"""

""" todos
	todo0 #m2utils_install.validate()
		- function for validating the installed procedure
	todo1 ENB_install, do not install enblocal.ini but pick recommended one
		- use DxDiag to determine ram,vram,gpu, etc
		- use ENB_config_install_fullpath to extract correct ini
	todo2 use ENB Manager and Changer
		Mods\enb_manager and copy enbhost.exe and d3d9.dll to ENB Versions\name
	and just about everything which is marked as #TODO
"""

import os, subprocess, zipfile #for checking files, calling 7z and unpacking ENB

#-----------------------------Install ModOrganizer-----------------------------
#this is totally crazy and I do this just for fun and its still WIP
def MO_fix_archive(sevenzip_bin, MO_install_fullpath):
	#remove the folder from the archive by renaming each file
	filelist = []
	#get the filelist
	sevenzip_command_list = sevenzip_bin + ' l "' + MO_install_fullpath + '"'
	#I don't like check_output, Popen might be better
	MO_7z_list = str(subprocess.check_output(sevenzip_command_list))
	#fix the output
	for line in MO_7z_list.split('\\r\\n'):
		if 'ModOrganizer\\' in line:
			filelist.append(line[line.find('ModOrganizer\\'):])
	#now lets prepare the string for 7z
	huge_list = ''
	for file in filelist:
		hugelist =+ file + ' '
		hugelist =+ file.replace('ModOrganizer\\','') + ' '
	#remove \ for rename
	import re
	re.sub(r'\s\\', ' ', huge_list)
	#now lets remove '\\' for 7zip
	hugelist = huge_list.replace('\\\\','\\')
	#TODO need to remove the directories names, its first 30 items or so
	sevenzip_command_fix = sevenzip_bin + ' rn "' + MO_install_fullpath + '" ' + huge_list
	with open('aha.bat', 'w') as b: #bat screws things up, run is at subprocess anyway
		b.write(sevenzip_command_fix)
	#MO_7z_subprocess = subprocess.Popen(sevenzip_command_fix, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
	#MO_7z_subprocess.communicate()


#this function can also extract the insttaler, but its better to use the archive
def MO_install(sevenzip_bin, MO_install_fullpath, destination):
	#TODO same as mash and TES5 edit, merge it
	print("Installing ModOrganizer")
	#-y option will always overwrite
	sevenzip_command = sevenzip_bin + ' x "' + MO_install_fullpath + '" -o"' + destination + '" -y' #unpack ModOrganizer directory to destination
	MO_7z_subprocess = subprocess.Popen(sevenzip_command, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
	MO_7z_subprocess.communicate()


def write_MO_ini(MO_destination, MO_config, skyrim_dir):
	print("Writing ModOrganizer.ini")
	with open(os.path.join(MO_destination + '\\ModOrganizer\\ModOrganizer.ini'),'w') as MO_ini: #TODO dynamic path, but this should work
		#[Plugins]
		MO_ini.write('[Plugins]\n')
		for string in MO_config['[Plugins]']:
			MO_ini.write(string + '\n')
		#end writing plugins
		MO_ini.write('\n')
		#[customExecutables]
		MO_ini.write('[customExecutables]\n')
		for key, string in enumerate(MO_config['[customExecutables]']):
			MO_ini.write(str(key + 1) + '\\title=' + string['title'] + '\n')
			MO_ini.write(str(key + 1) + '\\custom=' + string['custom'] + '\n')
			MO_ini.write(str(key + 1) + '\\toolbar=' + string['toolbar'] + '\n')
			MO_ini.write(str(key + 1) + '\\ownicon=' + string['ownicon'] + '\n')
			if string['custom'] == 'true':
				MO_ini.write(str(key + 1) + '\\binary=' + string['binary'].replace('%SkyrimPath%',skyrim_dir).replace('\\','/') + '\n') #TODO make it nicer #TODO the json key is not proper yet
				MO_ini.write(str(key + 1) + '\\arguments=' + string['arguments'].replace('\\','/') + '\n')
				MO_ini.write(str(key + 1) + '\\workingDirectory=' + string['workingDirectory'].replace('\\','/') + '\n')
				MO_ini.write(str(key + 1) + '\\closeOnStart=' + string['closeOnStart'].replace('\\','/') + '\n')
				MO_ini.write(str(key + 1) + '\\steamAppID=' + string['steamAppID'].replace('\\','/') + '\n')
		MO_ini.write('size=' + str(len(MO_config['[customExecutables]'])) + '\n')
#---------------------------------Install SKSE---------------------------------
def SKSE_install(sevenzip_bin, SKSE_install_fullpath, SKSE_wanted_files, skyrim_dir):
	print("Installing SKSE")
	#-y option will always overwrite
	#initialize the list of files we want to extract
	source_root = ""
	source_data = ""
	for file in SKSE_wanted_files:
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
def ENB_install(sevenzip_bin, ENB_install_fullpath, skyrim_dir):
	#initialize the list of files we want to extract
	source_root = ""
	#this can be hardcoded
	enb_wanted_files = ['WrapperVersion/d3d9.dll', 'WrapperVersion/enbhost.exe']
	for file in enb_wanted_files:
		source_root += file + ' '
	print("Installing ENB")
	sevenzip_command_root = sevenzip_bin + ' e "' + ENB_install_fullpath + '" -o"' + skyrim_dir + '\\" -y ' + source_root
	ENB_7z_subprocess_root = subprocess.Popen(sevenzip_command_root, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
	ENB_7z_subprocess_root.communicate()
#------------------------------Install TES5 Edit-------------------------------
def TES5E_install(sevenzip_bin, TES5E_install_fullpath, destination):
	#TODO same as mash, merge it
	print("Installing TES5 Edit")
	#-y option will always overwrite
	sevenzip_command = sevenzip_bin + ' x "' + TES5E_install_fullpath + '" -o"' + destination + '" -y'
	TES5E_7z_subprocess = subprocess.Popen(sevenzip_command, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
	TES5E_7z_subprocess.communicate()
#---------------------------------Install Mash---------------------------------
#no need to do this via 7z, Mator packs in zip, so ZipFile library could be used
def Mash_install(sevenzip_bin, Mash_install_fullpath, destination):
	#TODO same as tes5, merge it
	print('Installing Smash')
	#-y option will always overwrite
	sevenzip_command = sevenzip_bin + ' x "' + Mash_install_fullpath + '" -o"' + destination + '" -y'
	Smash_7z_subprocess = subprocess.Popen(sevenzip_command, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
	Smash_7z_subprocess.communicate()

#-----------------------------might not be needed------------------------------
def use_sevenzip(sevenzip_bin, action, source, output_dir): #not used in the script, only tested for unpacking backups
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

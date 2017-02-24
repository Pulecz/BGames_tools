""" change-log
	V01.0 - general improvements
	V02.0 - changed ENB install to 7z, enb and MO install via 7z now, putt local_repo to dict
	V03.0 - get_sevenzip_bin and write_MO_ini function and some more stuff
	V04.0 - deleted LOOT and Wrye support, first changes to work with m0prerequisites
	V05.0 - get_sevenzip_bin replaced by logic in main which is TODO function, no config is here, main sends everything, make_mods_folder_in_base deleted, no longer needed
	V06.0 - most of it threw out, as there no use of 7z, replaced by pyunpack
	V06.1 - LOOT support added, shortened install_utilities using functions

TODOs
	0 #m1utils_install.validate()
		- function for validating the installed procedure
	1 ENB_install, do not install enblocal.ini but pick recommended one
		- use DxDiag to determine ram,vram,gpu, etc
		- use ENB_config_install_fullpath to extract correct ini
	2 use ENB Manager and Changer
		Mods\enb_manager and copy enbhost.exe and d3d9.dll to ENB Versions\name
	and everything else which is marked as #TODO
"""

import pyunpack #for unpacking, needs patool
import shutil #for move and copy of "dirty" archives
import tempfile #for unpacking "dirty" archives


def write_MO_ini(MO_destination, MO_config, skyrim_dir):
	"""
	Saves ModOrganzier.ini in its specific format
	"""
	print("Writing ModOrganizer.ini")
	with open(MO_destination + r'\\ModOrganizer.ini','w') as MO_ini:
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


def install_utilities(data):
	"""
	Handles intallation of:
		Mod Organizer
		ENB for Skyrim
		TES5Edit
		LOOT
		Mator Smash
		Wrye Bash
	
	and tries to cleanup after "dirty" archives
	"""
	#create tempdir
	tmp_dir = tempfile.TemporaryDirectory(suffix='bgames_tools')
	def unpack_to(target, auto_create_dir=False):
		archive = pyunpack.Archive(data[utility]['path'])
		archive.extractall(target, auto_create_dir=auto_create_dir)
	#TODO FIX if directory to exists, its copies into it and then its to/what
	def move_from(where, what, to):
		print('Moving', what, 'to', to)
		try:
			shutil.move(where + r'\\'+ what, to)
		except shutil.Error as me:
			print("WARNING: {0}".format(me))
	def copy_files(tmp_dir, files):
		for afile in files:
			print("Installing", afile, "to Skyrim's root")
			try:
				shutil.copy(tmp_dir + '\\' + afile, data[utility]['install_path'])
			except PermissionError as pe_copy:
				print("FAIL: Couldn't copy file: {0}| File already exists?"
				.format(pe_copy.filename))
	for utility in data.keys():
		print('Installing', utility)
		if utility == 'Mod Organizer': #shutil.move
			unpack_to(tmp_dir.name)
			move_from(tmp_dir.name, 'ModOrganizer', data[utility]['install_path'])
		elif utility == 'SKSE': #shutil.copy and shutil.move
			#own tempdir for skse
			tmp_dir_skse = tempfile.TemporaryDirectory(suffix='skse')
			unpack_to(tmp_dir_skse.name)
			skse_root_files = ["skse_1_07_03\\skse_1_9_32.dll",
							   "skse_1_07_03\\skse_docs.txt",
							   "skse_1_07_03\\skse_loader.exe",
							   "skse_1_07_03\\skse_papyrus_docs.txt",
							   "skse_1_07_03\\skse_readme.txt",
			        		   "skse_1_07_03\\skse_steam_loader.dll",
			        		   "skse_1_07_03\\skse_whatsnew.txt"]
			#copy root files
			copy_files(tmp_dir_skse.name, skse_root_files)
			#move scripts
			move_from(tmp_dir_skse.name, 'skse_1_07_03\Data\scripts',
			data[utility]['install_path']  + r'\\Data\\scripts')
			#done
			try:
				tmp_dir_skse.cleanup()
			except PermissionError as pe_skse_clean:
				print("WARNING: Can't remove file: {0}|Please clean it up manually"
				.format(pe_skse_clean.filename))
		elif utility == 'ENB': #shutil.copy
			unpack_to(tmp_dir.name)
			copy_files(tmp_dir.name, ['WrapperVersion/d3d9.dll', 'WrapperVersion/enbhost.exe'])
		elif utility == 'LOOT': #shutil.move
			unpack_to(tmp_dir.name)
			move_from(tmp_dir.name, 'loot_0.10.3-0-g0fcf788_dev_Win32', data[utility]['install_path'])
		elif utility == 'Wrye Bash': #shutil.move
			unpack_to(tmp_dir.name)
			move_from(tmp_dir.name, 'Mopy', data[utility]['install_path'])
		else:
			print('Moving', utility, 'to', data[utility]['install_path'])
			unpack_to(data[utility]['install_path'], auto_create_dir=True)

	#all done cleanup
	try:
		tmp_dir.cleanup()
	except PermissionError as pe_clean:
		print("WARNING: Can't remove file: {0}|Please clean it up manually"
		.format(pe_clean.filename))

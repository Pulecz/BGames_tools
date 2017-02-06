#m1utils_install V0.6

""" change-log
	V01 - general improvements
	V02 - changed ENB install to 7z, enb and MO install via 7z now, putt local_repo to dict
	V03 - get_sevenzip_bin and write_MO_ini function and some more stuff
	V04 - deleted LOOT and Wrye support, first changes to work with m0prerequisites
	V05 - get_sevenzip_bin replaced by logic in main which is TODO function, no config is here, main sends everything, make_mods_folder_in_base deleted, no longer needed
	V06 - most of it threw out, as there no use of 7z
"""

""" todos
	todo0 #m1utils_install.validate()
		- function for validating the installed procedure
	todo1 ENB_install, do not install enblocal.ini but pick recommended one
		- use DxDiag to determine ram,vram,gpu, etc
		- use ENB_config_install_fullpath to extract correct ini
	todo2 use ENB Manager and Changer
		Mods\enb_manager and copy enbhost.exe and d3d9.dll to ENB Versions\name
	and just about everything which is marked as #TODO
"""

import shutil
import pyunpack
import tempfile

def write_MO_ini(MO_destination, MO_config, skyrim_dir):
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
	#TODO few stuff needs to be loaded from input_json, clean
	#TODO move to m1
	#create tempdir
	tmp_dir = tempfile.TemporaryDirectory(suffix='bgames_tools')
	for utility in data.keys():
		print('doing',utility)
		if utility == 'Mod Organizer':
			#TODO for MO handle MO_config
			archive = pyunpack.Archive(data[utility]['path'])
			archive.extractall(tmp_dir.name, auto_create_dir=False)
			print('Moving Mod Organizer to',data[utility]['install_path'])
			try:
				#TODO check when it installs to ModOrganizer\ModOrganizer
				shutil.move(tmp_dir.name + r'\ModOrganizer', data[utility]['install_path'])
			except shutil.Error as mo:
				print("WARNING: {0}".format(mo))
		elif utility == 'SKSE':
			#own tempdir for skse
			tmp_dir_skse = tempfile.TemporaryDirectory(suffix='skse')
			#
			archive = pyunpack.Archive(data[utility]['path'])
			archive.extractall(tmp_dir_skse.name, auto_create_dir=False)
			skse_root_files = ["skse_1_07_03\\skse_1_9_32.dll",
							   "skse_1_07_03\\skse_docs.txt",
							   "skse_1_07_03\\skse_loader.exe",
							   "skse_1_07_03\\skse_papyrus_docs.txt",
							   "skse_1_07_03\\skse_readme.txt",
			        		   "skse_1_07_03\\skse_steam_loader.dll",
			        		   "skse_1_07_03\\skse_whatsnew.txt"]
			for skse_file in skse_root_files:
				print("Installing", skse_file, "to Skyrim's root")
				try:
					shutil.copy(tmp_dir_skse.name + '\\' + skse_file, data[utility]['install_path'])
				except PermissionError as pe_skse_copy:
					print("FAIL: Couldn't copy file: {0}| File already exists?"
					.format(pe_skse_copy.filename))
			print('Moving SKSE scripts to',data[utility]['install_path'] + r'\\Data\\scripts')
			try:
				#TODO fix bug, if Skyrim\Data\scripts\ exists, it makes another scripts folder
				shutil.move(tmp_dir_skse.name + r'\skse_1_07_03\Data\scripts',
							data[utility]['install_path'] + r'\\Data\\scripts')
			except shutil.Error as skse_script:
				print("WARNING: {0}".format(skse_script))
			#done
			try:
				tmp_dir_skse.cleanup()
			except PermissionError as pe_skse_clean:
				print("WARNING: Can't remove file: {0}|Please clean it up manually"
				.format(pe_skse_clean.filename))
		elif utility == 'ENB':
			archive = pyunpack.Archive(data[utility]['path'])
			archive.extractall(tmp_dir.name, auto_create_dir=False)
			for enb_file in ['WrapperVersion/d3d9.dll', 'WrapperVersion/enbhost.exe']:
				print("Installing", enb_file, "to Skyrim's root")
				try:
					shutil.copy(tmp_dir.name + '\\' + enb_file, data[utility]['install_path'])
				except PermissionError as pe_enb_copy:
					print("FAIL: Couldn't copy file: {0}| File already exists?"
					.format(pe_enb_copy.filename))
		elif utility == 'Wrye Bash':
			archive = pyunpack.Archive(data[utility]['path'])
			archive.extractall(tmp_dir.name, auto_create_dir=False)
			print('Moving Wrye Bash to',data[utility]['install_path'])
			try:
				shutil.move(tmp_dir.name + r'\Mopy', data[utility]['install_path'])
			except shutil.Error as wryebash:
				print("WARNING: {0}".format(wryebash))
		else:
			print('Moving',utility, 'to', data[utility]['install_path'])
			archive = pyunpack.Archive(data[utility]['path'])
			archive.extractall(data[utility]['install_path'],
							   auto_create_dir=True)

	#all done cleanup
	try:
		tmp_dir.cleanup()
	except PermissionError as pe_clean:
		print("WARNING: Can't remove file: {0}|Please clean it up manually"
		.format(pe_clean.filename))

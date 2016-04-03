#m1download_utils V0.3
#V0.1, basic functionality, download
#V0.2, just definitions here, the control is moved to main.py
#V0.3, no config is here, main sends everything
#NOT PYTHONIC, wget handles urls with bad ssl certificates and the referalls

import subprocess, os

def use_wget(wget_bin, args):#
	wget_command = wget_bin + ' ' + args
	wget_subprocess = subprocess.Popen(wget_command, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
	wget_subprocess.communicate()
	#TODO show wget progress
	#(out, err) = wget_subprocess.communicate()
	#print(out,err)


def download_all(wget_bin, input_json, destination):
	#initialize list for returning list of filenames, must be in ORDER, #TODO use tuple?
	filenames = []
	for utility in input_json['utilities']:
		print('----')
		print('Downloading: ' + utility['download'])
		if utility['name'] == 'Mod Organizer':
			use_wget(wget_bin, '-nc -P '+ destination + ' ' + utility['download'])
			filenames.append(utility['download'][utility['download'].rfind('/') + 1 :])
		##if utility['name'] == 'Nexus Mod Manager': # to be implented
			##use_wget(wget_bin, '-nc -P '+ destination + ' ' + utility['download'])
		if utility['name'] == 'SKSE':
			use_wget(wget_bin, '-nc -P '+ destination + ' ' + utility['download'])
			filenames.append(utility['download'][utility['download'].rfind('/') + 1 :])
		if utility['name'] == 'ENB':
			use_wget(wget_bin, '-nc -P '+ destination + ' --referer="http://enbdev.com/download_mod_tesskyrim.html" ' + utility['download'])
			filenames.append(utility['download'][utility['download'].rfind('/') + 1 :])
		if utility['name'] == 'TES5Edit':
			use_wget(wget_bin, '-nc -P '+ destination + ' --no-check-certificate ' + utility['download'])
			filenames.append(utility['download'][utility['download'].rfind('/') + 1 :])
		if utility['name'] == 'Mator Smash':
			use_wget(wget_bin, '-nc -P '+ destination + ' --no-check-certificate ' + utility['download'])
			filenames.append(utility['download'][utility['download'].rfind('/') + 1 :])
	return filenames
		#BIG TODO do the checks that everything is download correctly

def get_utilities_paths(utilities_location, filenames): #TODO md5sum check
	for file in filenames:
		#TODO this wants specific order, fix that
		#hotfix
		if 'enbseries' in file:
			ENB_install_fullpath = os.path.join(os.getcwd(),utilities_location, file)
			##ENB_install_fullpath = os.path.join(os.getcwd(),utilities_location, ENB_install_archive)
		if 'Mator' in file:
			##Mash_install_fullpath = os.path.join(os.getcwd(),utilities_location, Mash_install_archive)
			Mash_install_fullpath = os.path.join(os.getcwd(),utilities_location, file)
		if 'ModOrganizer' in file:
			##MO_install_fullpath = os.path.join(os.getcwd(),utilities_location, MO_install_7zarchive)
			MO_install_fullpath = os.path.join(os.getcwd(),utilities_location, file)
		##if 'NMM' in file: #to be implented
			#NMM_install_fullpath = os.path.join(os.getcwd(),utilities_location, NMM_install_7zarchive)
		if 'skse' in file:
			##SKSE_install_fullpath = os.path.join(os.getcwd(),utilities_location, SKSE_install_7zarchive)
			SKSE_install_fullpath = os.path.join(os.getcwd(),utilities_location, file)
		if 'TES5' in file:
			##TES5E_install_fullpath = os.path.join(os.getcwd(),utilities_location, TES5E_install_7zarchive)
			TES5E_install_fullpath = os.path.join(os.getcwd(),utilities_location, file)
	return ENB_install_fullpath, Mash_install_fullpath, MO_install_fullpath, SKSE_install_fullpath, TES5E_install_fullpath

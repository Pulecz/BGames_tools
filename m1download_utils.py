#m1download_utils V0.3
#V0.1, basic functionality, download
#V0.2, just definitions here, the control is moved to main.py
#V0.3, no config is here, main sends everything
#V0.4, replaced by proper urllib.request, handling all the cases, no need for this anymore
#NOT PYTHONIC, wget handles urls with bad ssl certificates and the referalls
#TODO this should all be replaced with regular download thing in m0

import subprocess, os #for use_wget and checking files

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

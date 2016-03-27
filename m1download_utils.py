#m1download_utils V0.2
#V0.1, basic functionality, download
#V0.2, just definitions here, the control is moved to main.py
#NOT PYTHONIC, wget handles urls with bad ssl certificates and the referalls

import subprocess

#------------------------------------config------------------------------------
#TODO move this to main.py or json
wget_bin = 'bin//wget.exe'
destination = 'utilities'

#-------------------------------------defs-------------------------------------
def use_wget(args):#
	wget_command = wget_bin + ' ' + args
	wget_subprocess = subprocess.Popen(wget_command, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
	wget_subprocess.communicate()
	#TODO show wget progress
	#(out, err) = wget_subprocess.communicate()
	#print(out,err)


def download_all(input_json):
	for i in input_json['utilities']:
		print('----')
		print('Downloading [no wget status, sorry]: ' + i['download'])
		if 'enb' in (i['download']):
			use_wget('-nc -P '+ destination + ' --referer="http://enbdev.com/download_mod_tesskyrim.html" ' + i['download'])
		elif 'https' in (i['download']):
			use_wget('-nc -P '+ destination + ' --no-check-certificate ' + i['download'])
		else:
			use_wget('-nc -P '+ destination + ' ' + i['download'])


#TODO do the checks that everything is correct
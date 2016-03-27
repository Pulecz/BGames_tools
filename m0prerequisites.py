#m0prerequisities V0.2
#V0.1, basic idea, download and unpack
#V0.2, rewriten to functions, get_sevenzip_dir and cleanup added
#V0.3, just definitions here, the control is moved to main.py
#TODO check the regex
#TODO if wget is there and its CRC check is ok, continue!
#probably push all the Skyrim and software checkers for utilities to here
#get_skyrim_dir is here!

import urllib.request, re
import zipfile, os
import subprocess
import shutil
import sys

urls_regex = re.compile('.*[=\/](.*)')

#------------------------------------config------------------------------------
#TODO put in main config
mods_dir_name = 'Mods'

def get_skyrim_dir(): #can cause exit 99
	#TODO check if this regex path is always the same
	wincmd_req_query_skyrim_dir='REG QUERY "HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Bethesda Softworks\skyrim" /v "installed path" /t REG_SZ'
	try:
		skyrim_dir_mess = subprocess.check_output(wincmd_req_query_skyrim_dir)
	except subprocess.CalledProcessError as e:
		print('No registry entry for Skyrim, either run Skyrim at least once')
		sys.exit(99)
	skyrim_dir = str(skyrim_dir_mess)[str(skyrim_dir_mess)
	.find('REG_SZ')+len('REG_SZ'):str(skyrim_dir_mess)
	.rfind('\\r\\n\\r\\n')] \
	.strip().replace('\\\\','\\')
	return skyrim_dir

def confirm_dir(msg, default):
	#TODO google how or\ works (I forgot...)
	dir = input(msg + ' \n\nIs it ' + default + ' ?\nHit enter to confirm') or\
	default
	return dir

def confirm_dirs():
	global skyrim_dir
	global skyrim_mods_dir
	#run this only if Skyrim was launched first, main.py has to arrange that
	#maybe TODO fix bug
	try:
		skyrim_dir = get_skyrim_dir()
	except OSError as e:
		print(e)

	#confirm skyrim_dir
	skyrim_dir = confirm_dir('Enter the full path to Skyrim:',
	skyrim_dir)
	#confirm skyrim_mods_dir
	skyrim_mods_dir = confirm_dir('\n\nEnter the full path to Skyrim Mods folder:',
	os.path.join(skyrim_dir,mods_dir_name))
	return (skyrim_dir, skyrim_mods_dir)

def get_sevenzip_dir():
	wincmd_req_query_sevenzip_dir='REG QUERY "HKEY_LOCAL_MACHINE\\SOFTWARE\\7-Zip" /v "Path" /t REG_SZ'
	wincmd_req_query_sevenzip_dir64='REG QUERY "HKEY_LOCAL_MACHINE\\SOFTWARE\\7-Zip" /v "Path64" /t REG_SZ'
	'''TODO try:
		sevenzip_dir_mess = subprocess.check_output(wincmd_req_query_sevenzip_dir)
	'''
	sevenzip_dir_mess = subprocess.check_output(wincmd_req_query_sevenzip_dir)
	sevenzip_dir = str(sevenzip_dir_mess)[str(sevenzip_dir_mess)
	.find('REG_SZ')+len('REG_SZ'):str(sevenzip_dir_mess)
	.rfind('\\r\\n\\r\\n')].strip() \
	.replace('\\\\','\\')
	#TODO return false if fail
	return sevenzip_dir


def download(urls, target=''): #input must be list of at least two, TODO...
	#download_try = 0 # TODO some function with try for more mirrors?
	#have to use regex because urls[1][urls[1].rfind('/') + 1:] does not work for wget
	if len(target) > 1:
		if not os.path.exists(target):
				os.mkdir(target)
		target = os.path.join(os.getcwd(), target + '\\')
	try:
		#urllib.request.urlretrieve(#source, #local_target)
		urllib.request.urlretrieve(urls[0], target + re.findall(urls_regex,urls[0])[0])
		#return filename or path
		if len(target) > 1:
			return os.path.join(target, re.findall(urls_regex,urls[0])[0])
		else:
			return re.findall(urls_regex,urls[0])[0]
	except urllib.error.URLError:
		#try second
		print('URL:',urls[0], ' failed, trying another.')
		#urllib.request.urlretrieve(#source, #local_target)
		urllib.request.urlretrieve(urls[1], target + re.findall(urls_regex,urls[1])[0])
		#return filename or path
		if len(target) > 1:
			return os.path.join(target, re.findall(urls_regex,urls[1])[0])
		else:
			return re.findall(urls_regex,urls[1])[0]

def unpack_to_bin(file): #TODO fix hardcoded bin
	if '7za920' in file:
		with zipfile.ZipFile(file, 'r') as archive:
			archive.extract('7za.exe',os.getcwd() + '\\bin')
		return os.getcwd() + '\\bin\\7za.exe' 
	if 'wget' in file:
		with zipfile.ZipFile(file, 'r') as archive:
			archive.extract('wget.exe',os.getcwd() + '\\bin')
		return os.getcwd() + '\\bin\\wget.exe' 
	

def cleanup(): # probably usable in different module
		shutil.rmtree(os.path.join(os.getcwd(),'tmp'))
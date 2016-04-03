#m0prerequisities V0.4
#V0.1, basic idea, download and unpack
#V0.2, rewriten to functions, get_sevenzip_dir and cleanup added
#V0.3, just definitions here, the control is moved to main.py
#V0.4, no config is here, main sends everything, unpack_to_bin does not overwrite, no need for re
#TODO probably push all the Skyrim and software checkers for utilities to here


import os, urllib.request, re
import zipfile
import subprocess
import shutil
import sys # only one use, get_skyrim_dir can return something and main can exit

#TODO check the regex
def download(urls, target=''): #urls must be list of at least two, TODO...
	#download_try = 0 # TODO some function with try for more mirrors?
	urls_regex = re.compile('.*[=\/](.*)') #TODO fix it (URL[URL.rfind('/') + 1 :])
	if len(target) > 1: #only if target is defined
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


def unpack_to_bin(file): #expects specific file name and specific archive
	#TODO instead of os.path.exists, do a CRC check
	if '7za920' in file:
		if not os.path.exists('bin\\7za.exe'):
			with zipfile.ZipFile(file, 'r') as archive:
				archive.extract('7za.exe',os.getcwd() + '\\bin')
		return os.getcwd() + '\\bin\\7za.exe'
	if 'wget' in file:
		if not os.path.exists('bin\\wget.exe'):
			with zipfile.ZipFile(file, 'r') as archive:
				archive.extract('wget.exe',os.getcwd() + '\\bin')
		return os.getcwd() + '\\bin\\wget.exe'
	#TODO if no file is supported, return false or something


def get_sevenzip_dir():
	wincmd_req_query_sevenzip_dir='REG QUERY "HKEY_LOCAL_MACHINE\\SOFTWARE\\7-Zip" /v "Path" /t REG_SZ'
	wincmd_req_query_sevenzip_dir64='REG QUERY "HKEY_LOCAL_MACHINE\\SOFTWARE\\7-Zip" /v "Path64" /t REG_SZ'
	#TODO test it properly
	try:
		sevenzip_dir_mess = subprocess.check_output(wincmd_req_query_sevenzip_dir)
	except subprocess.CalledProcessError as error:
		print(error)
		return False
	sevenzip_dir = str(sevenzip_dir_mess)[str(sevenzip_dir_mess)
	.find('REG_SZ')+len('REG_SZ'):str(sevenzip_dir_mess)
	.rfind('\\r\\n\\r\\n')].strip() \
	.replace('\\\\','\\')
	return sevenzip_dir


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


def confirm_skyrim_dirs():
	def confirm_dir(msg, default):
		#TODO google how the "or\" works (I forgot...)
		dir = input(msg + ' \n\nIs it ' + default + ' ?\nHit enter to confirm') or\
		default
		return dir
	try:
		skyrim_dir = get_skyrim_dir() #can cause exit 99
	except OSError as e:
		print(e)

	#confirm skyrim_dir
	skyrim_dir = confirm_dir('Enter the full path to Skyrim:',
	skyrim_dir)
	return (skyrim_dir)


def cleanup(folder): # probably usable in different module
		shutil.rmtree(os.path.join(os.getcwd(),folder))

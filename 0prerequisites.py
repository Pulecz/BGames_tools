#prerequisities V0.2
#V0.1, basic idea, download and unpack
#V0.2, rewriten to functions, get_sevenzip_dir and cleanup added
#lots of TODOs
#probably push all the Skyrim and software checkers for utilities to here

import urllib.request, re
import zipfile, os
import subprocess
import shutil

curl_urls = [
'http://www.paehl.com/open_source/?download=curl_747_0.zip',
'http://www.paehl.com/open_source/?download=curl_747_1.zip' #mirror 1
]
w7zip_urls = [
'http://7-zip.org/a/7za920.zip',
'http://7-zip.org/a/7za920.zip' #mirror 1
]
urls_regex = re.compile('.*[=\/](.*)')


def download(urls, target=''): #input must be list of at least two, TODO...
	#download_try = 0 # TODO some function with try for more mirrors?
	#have to use regex because urls[1][urls[1].rfind('/') + 1:] does not work for curl
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
		#try two
		print('URL:',urls[0], ' failed, trying another.')
		#urllib.request.urlretrieve(#source, #local_target)
		urllib.request.urlretrieve(urls[1], target + re.findall(urls_regex,urls[1])[0])
		#return filename or path
		if len(target) > 1:
			return os.path.join(target, re.findall(urls_regex,urls[1])[0])
		else:
			return re.findall(urls_regex,urls[1])[0]

def unpack_to_bin(file):
	if '7za920' in file:
		with zipfile.ZipFile(file, 'r') as archive:
			archive.extract('7za.exe',os.getcwd() + '\\bin')
		return os.getcwd() + '\\bin\\7za.exe' 
	if 'curl' in file:
		with zipfile.ZipFile(file, 'r') as archive:
			archive.extractall(os.getcwd() + '\\bin')
		return os.getcwd() + '\\bin\\curl.exe' 
	

def cleanup(): # probably usable in different module
		shutil.rmtree(os.path.join(os.getcwd(),'tmp'))

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
	#todo return false if fail
	return sevenzip_dir

curl_path = unpack_to_bin(download(curl_urls,'tmp'))
sevenzip_path = unpack_to_bin(download(w7zip_urls,'tmp'))
if isinstance(get_sevenzip_dir(), str):
	sevenzip_path = get_sevenzip_dir() #meh, needs todo from function
else:
	sevenzip_path = unpack_to_bin(download(w7zip_urls,'tmp'))

print(curl_path) #give it to next module	
print(sevenzip_path) #give it to next module
cleanup()
#prerequisities V0.1
#V0.1, basic idea, download and unpack
#V0.2, rewriten to functions and added cleanup

#lots of TODOs

import urllib.request
import zipfile, os
import subprocess

curl_urls = [
'http://www.paehl.com/open_source/?download=curl_747_0.zip',
'http://www.paehl.com/open_source/?download=curl_747_1.zip' #mirror 1
]
curl_file_name = 'curl_747_0.zip'

#TODO get this from url
download_try = 0 # TODO some function with try for more mirrors?

try:
	urllib.request.urlretrieve(curl_urls[0], curl_file_name)
except urllib.error.URLError:
	print('URL:',curl_urls[0], ' failed, trying another.')
	urllib.request.urlretrieve(curl_urls[1], curl_file_name)

#unpack curl, #TODO also put in a function
with zipfile.ZipFile(curl_file_name, 'r') as archive:
	archive.extractall(os.getcwd() + '\\bin')

	
#TODO check if 7z is installed
#if not:	
w7zip_urls = [
'http://7-zip.org/a/7za920.zip',
'https://sourceforge.net/projects/sevenzip/files/7-Zip/9.20/7za920.zip/download' #mirror 1
]
#TODO get this from url
w7zip_file_name = '7za920.zip'

try:
	urllib.request.urlretrieve(w7zip_urls[1], w7zip_file_name)
except urllib.error.URLError:
	print('URL:',curl_urls[0], ' failed, trying another.')
	urllib.request.urlretrieve(w7zip_urls[0], w7zip_file_name)

#unpack 7zip
with zipfile.ZipFile(w7zip_file_name, 'r') as archive:
	archive.extractall(os.getcwd() + '\\bin')
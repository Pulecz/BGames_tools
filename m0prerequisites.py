#m0prerequisities V0.4
#V0.1, basic idea, download and unpack
#V0.2, rewriten to functions, get_sevenzip_dir and cleanup added
#V0.3, just definitions here, the control is moved to main.py
#V0.4, no config is here, main sends everything, unpack_to_bin does not overwrite, no need for re
#TODO probably push all the Skyrim and software checkers for utilities to here


import os, urllib.request, re #for checking files and downloading #TODO remove re
from winreg import HKEY_LOCAL_MACHINE, KEY_READ, OpenKey, QueryValueEx #for get_skyrim_dir
import zipfile #for unpack_to_bin
import subprocess # for get_sevenzip_dir
import shutil # for cleanup
import sys # only one use, get_skyrim_dir can return something and main can exit


def download(url, dest):
    def download_with_referer(url, filename, referer):
        #set it up
        req = urllib.request.Request(url)
        req.add_header('Referer', referer)
        urlfile = urllib.request.urlopen(req)

        #write the file
        progress = 0
        f = open(filename, "wb")
        while True:
            data = urlfile.read(4096)
            if not data:
                sys.stdout.write("\n")
                break
            f.write(data)
            progress += len(data)
            sys.stdout.write("\rGot {0} bytes".format(progress))



    def reporthook(blocknum, blocksize, totalsize):
        #progress bar from
        #http://stackoverflow.com/questions/13881092/download-progressbar-for-python-3
    	readsofar = blocknum * blocksize
    	if totalsize > 0:
    		percent = readsofar * 1e2 / totalsize
    		s ="\r%5.1f%% %*d / %d" % (
    			percent, len(str(totalsize)), readsofar, totalsize)
    		sys.stdout.write(s)
    		if readsofar >= totalsize: # near the end
    			sys.stdout.write("\n")
    	else: # total size is unknown
    		sys.stdout.write("read %d\n" % (readsofar,))
    #filename is url from last position of '/', the + 1 is exclude it
    filename = url[url.rfind('/') + 1:]
    target = dest + '/' + filename

    if not os.path.exists(dest):
        try:
            os.mkdir(dest)
        except PermissionError:
            return False

    print("Downloading file {0}".format(filename))
    if 'enbdev.com/' in url:
    	#TODO try to check all was fine?
    	referer = 'http://enbdev.com/download_mod_tesskyrim.html'
    	download_with_referer(url, target, referer)
    	return target
    try:
    	path, header = urllib.request.urlretrieve(url, target, reporthook)
    	return path
    except urllib.error.HTTPError as e:
    	#404
    	print(e)

def get_skyrim_dir():
	#reg_path might be different on 32bit systems
	reg_path = r"SOFTWARE\WOW6432Node\Bethesda Softworks\skyrim"
	reg_value = "installed path"
	try:
		PyHKEY = OpenKey(HKEY_LOCAL_MACHINE, reg_path, 0, KEY_READ)
		skyrim_dir = QueryValueEx(PyHKEY, reg_value)[0]
	except FileNotFoundError:
		print('No key or no value "{0}" in:HKLM\{1}'.format(reg_value, reg_path))
		raise ValueError #leads to exit 99 in main.py
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




def old():
	def get_sevenzip_dir():
		#FUCK THIS, let's use pip/pyunpack
		def do_reg_query(reg_path, reg_value):
			PyHKEY = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path, 0, winreg.KEY_READ)
			sevenzip_dir = winreg.QueryValueEx(PyHKEY, reg_value)[0]
			return sevenzip_dir


		reg_path = r'SOFTWARE\7-Zip'
		reg_value = "Path"
		reg_value_64 = "Path64"

		try:
			sevenzip_dir = do_reg_query(reg_path, reg_value)
		except FileNotFoundError:

			try:
				sevenzip_dir = do_reg_query(reg_path, reg_value_64)
			except FileNotFoundError:
				print('No key or no value "{0}" in:HKLM\{1}'.format(reg_value_64, reg_path))
				raise ValueError

			print('No key or no value "{0}" in:HKLM\{1}'.format(reg_value, reg_path))
			raise ValueError
		return sevenzip_dir


	def unpack_to_bin(file): #expects specific file name and specific archive
		#FUCK THIS, let's use pip/pyunpack
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

	def cleanup(folder): # probably usable in different module
		shutil.rmtree(os.path.join(os.getcwd(),folder))

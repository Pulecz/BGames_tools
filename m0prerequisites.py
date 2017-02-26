""" change-log
	V0.1 - basic idea, download and unpack
	V0.2 - rewriten to functions, get_sevenzip_dir and cleanup added
	V0.3 - just definitions here, the control is moved to main.py
	V0.4 - no config is here, main sends everything, unpack_to_bin does not overwrite, no need for re
	V0.5 - big rewrite, get_skyrim_dir and dl_utilities should handle all Prerequisites

TODOs
	if download() returns False, handle it
"""
from winreg import HKEY_LOCAL_MACHINE, KEY_READ, OpenKey, QueryValueEx #for get_skyrim_dir
import urllib.request, os, sys #for download
import hashlib #for verifying


def get_skyrim_dir():
	"""
	Tries to read HKLM/SOFTWARE\WOW6432Node\Bethesda Softworks\skyrim
	in registry	for value installed_path to return skyrim_dir
	"""
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

	
def dl_utilities(input_json, target_dir, skyrim_dir):
	"""
	Loops over input_json and tries to verify each utility
	If the file has a bad checksum or is not found, its downloaded to target_dir
	Returns dict with info needed for installation
	
	skyrim_dir is needed for correct install_path
	"""
	result = {}
	def download(url, dest):
		"""
		simple urlretrieve with progressbar and makedirs
		supports downloading with referer
		"""
		def download_with_referer(url, filename, referer):
			"""
			raw download with added header for referer
			"""
			#set the header
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
			"""progress bar from
			http://stackoverflow.com/questions/13881092/download-progressbar-for-python-3
			"""
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
			return path #should be same as target
		except urllib.error.HTTPError as e:
			print(e)
			return False
	def call_download(target_dir):
		"""
		call download() and if sucessfull calculates checksum
		and compares with checksum in input_json (crc_config)
		returns dict with checksum, install_path, path and verified
		"""
		hex_crc_same_as_config_crc = True
		print('\nDownloading', utility['name'])
		path = download(utility['download'], target_dir)
		if path:
			with open(path, 'rb') as f:
				hex_crc = hashlib.sha1(f.read()).hexdigest()
				if crc_config != hex_crc:
					print('FAIL: downloaded file checksum has different one the one in config')
					#TODO halt?
					hex_crc_same_as_config_crc = False
			result[utility['name']] = {
			"crc_sha1" : hex_crc,
			"install_path" : utility['install_path']
			.replace('%SkyrimPath%', skyrim_dir),
			"path" : path,
			"verified" : hex_crc_same_as_config_crc
			 }
		return result

	for utility in input_json['utilities']:
		url = utility['download']
		path = target_dir + '/' + url[url.rfind('/') + 1:]
		crc_config = utility['sha1']
		try:
			if crc_config == hashlib.sha1(open(path,'rb').read()).hexdigest():
				result[utility['name']] = {
				"path" : path,
				"verified" : True,
				"install_path" : utility['install_path']
				.replace('%SkyrimPath%', skyrim_dir)
 				}
			else: #not verified
				result.update(call_download(target_dir))
		except FileNotFoundError:
				result.update(call_download(target_dir))
	return result

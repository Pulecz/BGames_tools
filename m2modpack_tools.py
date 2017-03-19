import json #for input output
import hashlib #for make_checksum
import os #for scan_dir

def scan_dir(target):
    #todo also add whitelist just for archives
	"""
	scans directory recursively
	returns file_list, which are paths to the files
	"""
	file_list = []
	blacklist = ['build_modpack.py','.meta', 'mod.info']
	for root, dirs, files in os.walk(target):
		for file in files:
			if any(blacklist_item in file for blacklist_item in blacklist):
				continue
			file_list.append(os.path.join(root, file))
	return file_list


def make_checksum(mod_file, chunk_size=1024):
	"""
	Make checksum in sha1 for big files
	from http://stackoverflow.com/questions/1131220/get-md5-hash-of-big-files-in-python
	and http://stackoverflow.com/questions/519633/lazy-method-for-reading-big-file-in-python?noredirect=1&lq=1
	"""
	if debug:
		print('Calculating checksum for', mod_file)
	file_object = open(mod_file, 'rb')
	sha1 = hashlib.sha1();
	"""Lazy function (generator) to read a file piece by piece.
	Default chunk size: 1k."""
	while True:
		data = file_object.read(chunk_size)
		if not data:
			break
		sha1.update(data)
	return sha1.hexdigest()


def try_load_json(json_file):
	"""
	Tries to load valid json
	"""
	try:
		with open(json_file, 'r') as input_file:
			jsondata = json.load(input_file)
		return jsondata
	except FileNotFoundError:
		print('FAIL: File {0} does not exist in this folder'.format(json_file))
		exit(1)
	except json.JSONDecodeError as e:
		print('FAIL: JSON Decode Error:\n  {0}'.format(e))
		exit(2)


def try_save_json(json_file, data):
	"""
	Try to save JSON on Windows
	"""
	try:
		with open(json_file, 'w') as input_file:
			input_file.write(json.dumps(data))
		return True
	except OSError as e:
		print('FAIL: Windows happened:\n  {0}'.format(e))
		return False

#stolen from https://github.com/ponty/pyunpack/blob/master/pyunpack/__init__.py
#removed EasyProcess, because of UnicodeDecodeErrors
#	happens when decoding stdout from subprocess
#	using just str method instead of decode
#just edited functions for listing and searching instead of just extract
#I suck at classes usage, so don't stone me to death for nonsenses, it works
#TODO catch possible errors while listing or searching
import os.path #for finding files
import subprocess #for calling patool
import re #for searching
import sys #for calling patool

def _fullpath(x):
	"""
	stolen, get absolute path of file
	"""
	x = os.path.expandvars(x)
	x = os.path.expanduser(x)
	x = os.path.normpath(x)
	x = os.path.abspath(x)
	return x


def _exepath(cmd):
	"""
	stolen, do magic search in Windows PATH
	"""
	for p in os.environ['PATH'].split(os.pathsep):
		fullp = os.path.join(p, cmd)
		if os.access(fullp, os.X_OK):
			return fullp


#init
patool_path = _exepath('patool')
if not patool_path:
	raise ValueError('patool not found! Please install patool!')			
	#exit?
			
class Archive(object):
	'''
	:param backend: ``auto``, ``patool`` or ``zipfile``
	:param filename: path to archive file
	'''

	
	def __init__(self, filename, backend='auto'):
		"""
		get nice filename
		no idea what backend and timeout is
		"""
		self.filename = _fullpath(filename)
		self.backend = backend
		self.patool_path = patool_path

		
	def list_archive(self):
		"""
		run patool with list parameter
		returns stdout as a list for each line
		"""
		p = subprocess.run([
			sys.executable,
			self.patool_path,
			'--non-interactive',
			'list',
			self.filename
		], stdout=subprocess.PIPE, stderr = subprocess.PIPE)
		#if p.return_code:
		#	raise PatoolError('patool can not unpack\n' + str(p.stderr))
		return str(p.stdout).split('\\r\\n')

		
	def search_archive(self, pattern):
		"""
		run patool with search parameter
		search is done for content of each file in archive, its hungry!
		returns stdout as a list for each line
		"""
		p = subprocess.run([
			sys.executable,
			self.patool_path,
			'--non-interactive',
			'search',
			pattern,
			self.filename
		], stdout=subprocess.PIPE, stderr = subprocess.PIPE)
		#if p.timeout_happened:
		#	raise PatoolError('patool timeout\n' + str(p.stdout) + '\n' + str(p.stderr))
		return str(p.stdout).split('\\r\\n')

		
	def search_for_file_in_archive(self, pattern):
		"""
		call list_archive and search if filename is in archive
		returns True or False
		"""
		def get_content_from_stdout(stdout_list):
			"""
			get just the contents from list_archive		
			returns list, each file on its own line
			"""
			#find begining of the content
			for ln, lstr in enumerate(stdout_list):
				if 'Date' in lstr and 'Time' in lstr:
					content_start = ln+2
					break
			#find end of the content from reversed list
			for ln, lstr in enumerate(stdout_list[::-1]):
				if '-------------------' in lstr:
					content_end = ln+1
					break
			#reverse content_end index for stdout_list index
			content_end = len(stdout_list) - content_end
			content = stdout_list[content_start:content_end]
			return content
			
	
		def search_for_file_in_content(pattern, content):
			"""
			search for filename in content
			pattern is regular re, always used with re.IGNORECASE
			content_re will extract groups
			0 - all
			1 - Date
			2 - Time
			3 - Attr
			4 - Size
			5 - Compressed (size)
			6 - Name
			"""
			content_re = r'^(\d{4}\-\d+\-\d+)\s+(\d+\:\d+\:\d+)\s+(.{5})\s+(\d+)?\s+(\d+)?\s+(.*)$'
			for line in content:
				line_attributes = re.match(content_re, line)
				if line_attributes:
					filename = line_attributes.group(6)
				else:
					print('ERROR: failed to match', line)
					input('Please report this line\nPress any key to continue')
					continue
				found = re.search(pattern, filename.lower(), re.IGNORECASE)
				if found:
					return True
			return False

		
		content = get_content_from_stdout(self.list_archive())
		return search_for_file_in_content(pattern, content)
"""
When experiencing crashes check what MemoryBlocksLog.log created by MemoryBlockLog-50471 in MO overwrite folders
By default it keeps track of Block1 (512MB) and Block2(256MB) Memory
Block1 is unstable and block2 is stable.

This tool takes the max value of Blcok1 as input and uses it to
calculate what value the DefaultHeapInitialAllocMB should be

if you don't know where your SKSE.ini is download this mod
SKSE ini pre-download for lazy users
http://www.nexusmods.com/skyrim/mods/51038/

and in the mod's SKSE.ini edit the line DefaultHeapInitialAllocMB to output of this tool
Its default value 768 might not be stable for all
"""

import sys
def input():

	"""
	input is max value from file:
	MemoryBlocksLog.log which this mods creates:
	MemoryBlockLog-50471 http://www.nexusmods.com/skyrim/mods/50471

	for example:

		Max	512MB	256MB
		Time			Block1	Block2
		406970.567810	357		254

	wanted value is
	MemoryBlocksLog_max_block1 = 357
	"""
	try:
		MemoryBlocksLog_max_block1 = int(sys.argv[1])
	except ValueError:
		print('Only numbers please')
		sys.exit(1)
	return MemoryBlocksLog_max_block1


def calculate(MemoryBlocksLog_max_block1):
	"""
	Calculates DefaultHeapInitialAllocMB based on:
		- its default value - ScrapHeapSizeMB
		- value from MemoryBlocksLog_max_block1
		- based on some video

	default SKSE file:
		[Display]
		iTintTextureResolution=2048

		[General]
		ClearInvalidRegistrations=1
		EnableDiagnostics=1
		[Memory]
		DefaultHeapInitialAllocMB=768
		ScrapHeapSizeMB=256
	"""
	DefaultHeapInitialAllocMB=768
	ScrapHeapSizeMB=256

	#available_mem is all what SKSE can gives us
	available_mem = DefaultHeapInitialAllocMB - ScrapHeapSizeMB

	#get how much memory is "needed"
	#MemoryBlocksLog_max_block1 is the last memory from last crash
	magic_value = available_mem - MemoryBlocksLog_max_block1
	#lower that by 60mb for stability
	magic_value -= 60

	#write this to your config
	wanted_value = DefaultHeapInitialAllocMB - magic_value
	print('In your SKSE.INI edit this line to:')
	print('DefaultHeapInitialAllocMB={}'.format(wanted_value))


if __name__ == '__main__':
	MemoryBlocksLog_max_block1 = input()
	calculate(MemoryBlocksLog_max_block1)

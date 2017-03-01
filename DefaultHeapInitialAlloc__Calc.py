"""MemoryBlocksLog.log
Max	512MB	256MB
Time			Block1	Block2
406970.567810	357		254
"""
MemoryBlocksLog_max_block1 = 357 #TODO as arg1

"""SKSE.ini
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
print('Change SKSE.INI to:')
print('DefaultHeapInitialAllocMB={}'.format(wanted_value))
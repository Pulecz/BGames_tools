# BGames_tools

## main.py
Script to prepare fresh Skyrim installation for modding.

Skyrim Launcher needs to be run at least once, to create entry in registry.

The script tries to do some of the things described in [Skyrim Revisited - Legendary Edition Guide](http://wiki.step-project.com/User:Neovalen/Skyrim_Revisited_-_Legendary_Edition).

1. Downloads all utilities defined in config.json or checks if they are already downloaded based on checksum
2. Validates the Skyrim folder, prompts user to confirm them or edit them.
3. Unpacks all the utilities to specified install_path, these are specified:
	- [Mod Organizer](http://www.nexusmods.com/skyrim/mods/1334/)
	- [SKSE](http://skse.silverlock.org) - unpacks to Skyrim root folder and scripts to Skyrim/data.
	- [ENB](http://enbdev.com/download_mod_tesskyrim.html) - unpacks 'WrapperVersion/d3d9.dll' and 'WrapperVersion/enbhost.exe' to Skyrim root folder.
	- [Wrye Bash](http://www.nexusmods.com/skyrim/mods/1840/)
	- [TES5Edit](http://www.nexusmods.com/skyrim/mods/25859/)
	- [Mator Smash](https://github.com/matortheeternal/smash/releases)
4. Writes ModOrganizer.ini with paths to other tools and few settings from [here](http://wiki.step-project.com/User:Neovalen/Skyrim_Revisited_-_Legendary_Edition#Configure_Mod_Organizer).
5. If allowed prints some guidance.


## build_modpack.py
Verify if file is Nexus mod (by regex /\-(\d{3,})\-/) and collect info about it, do a checksum and save it as modpack_json, which can be used by others using verify_modpack.py
Currently setup for **Skyrim**, for **Fallout 4** support change Game var in Input (line 31+)

Script will scan the current directory (where the script is launched) (or change that in variable target), excluding folders and *.meta files.


#### Options:
 - Game = 'Fallout 4' or 'Skyrim' (sets the links and few other option for each Game)
 - debug = True (provides additional print information and writes summary.json when finished)
 - switch_ask_for_description = False (asks during scaning for description of the mod)
 - switch_ask_for_comment = False (asks during scanning for comment for the mod)
 - switch_get_nexus_info = True (will get ModName from title of the Nexus page)
 - if switch_get_nexus_info: (following is ignored if get_nexus_mod_name is False)
  - switch_get_skyrimgems_desc = True (will get description from [skyrimgems.com](http://skyrimgems.com/) (experimental))


##### Info gotten from file name:
  - Name = Everything before ModID in filename
  - File Name = what was scanned
  - ModID = Information between Name and Version
  - Version = Everything after ModID in filename
  - Link to Nexus page = http://www.nexusmods.com/$game/mods/ + $ModID $ + /

##### If allowed it will get from web:
  - ModName = because Name of File does not always suggest name of the mod like [here](http://www.nexusmods.com/skyrim/mods/30947) it will get title of the Nexus Page
  - ModCategoryN = Number of category (MO uses it to determine the mod category)
  - ModCategory = Name of the category, used in csv
  - SkyrimGems description - will try to get description about mod from [skyrimgems.com](http://skyrimgems.com/) (experimental)
  
  Categories in meta files are numbered based on Nexus Mods Skyrim categories(I don't have info about FO4 MO yet), after instaling the mods, number in meta of the mods is numbered in Mod Organizers way.

## verify_modpack.py

Verifies a bunch of mods downloaded from Nexus in a target folder against $modpack.json provided by build_modpack.py.
Mod is verified when checksum of the downloade_file is same as checksum of the entry for the mod in $modpack.json.
Verified mod is then moved (or copied if moving failes) to MO_bin along with MO like meta files (except versions I guess) so Mod Organizer can work with it.

Script will scan the current directory (where the script is launched) (or change that in variable target), excluding folders and *.meta files.

#### Options:
 - modpack_json = source.json
 - MO_bin = folder where to put verified files and write meta files
 - debug = True (provides additional print information and writes summary.json when finished)
 - switch_writeMetaFiles = True (if to write nexus info to meta file)
 - switch_get_nexus_info = True (if modpack_json does not have nexus_info, its useless) 
 
##### TODOs
  - Print links for missing files, so users can easilly download them
  - With that make soma kind of summary, how many files verified, etc
  - Mod Organizer doesn't need meta files from us, it can query it allright, might be useful for some mods that got deleted from Nexus


##### Known Bugs
  - Mod pages with adult-content are not accesible without login, therefore if users allows getting information from web, only title can be extracted, only categories will be skipped. Currently in such situation all action are skipped.
  - Some queries for skyrimgems info fail, because is seaches for whole modName, shorter search must be performed

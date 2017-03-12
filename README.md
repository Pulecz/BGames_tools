# BGames_tools

Tries to help with getting some of the Bethesda games playable by installing utilities for modding support and offers some helpers to install "modpacks"

Supported:
* **TES 5 Skyrim**
* **Fallout 4** (***WIP!***)

Ideal usage should be:
* get utils.json for main.py - the one provided here should do for Skyrim
* run main.py - to download all utilities (mainly ModOrganizer) and install them
* get some modpack.json - containing info about all the mods you want to install
* run verify_modpack.py - extracts mods for you, those which have to be installed manually or failed to get extracted will be copied to MO's downloads folder
* open ModOrganizer and follow the modpack's install instructions


## main.py

### Dependencies:
- pyunpack
- patool

Python script to prepare fresh Skyrim installation for modding.

Skyrim Launcher needs to be run at least once, to create entry in registry.

1. Downloads all utilities defined in config.json or checks if they are already downloaded based on checksum
2. Validates the Skyrim folder, prompts user to confirm them or edit the destination.
3. Unpacks all the utilities to specified install_path, these are specified:
	- [Mod Organizer](http://www.nexusmods.com/skyrim/mods/1334/)
	- [SKSE](http://skse.silverlock.org) - unpacks to Skyrim root folder and scripts to Skyrim/data.
	- [ENB](http://enbdev.com/download_mod_tesskyrim.html) - unpacks 'WrapperVersion/d3d9.dll' and 'WrapperVersion/enbhost.exe' to Skyrim root folder.
	- [LOOT](https://loot.github.io/)
	- [Wrye Bash](http://www.nexusmods.com/skyrim/mods/1840/)
	- [TES5Edit](http://www.nexusmods.com/skyrim/mods/25859/)
	- [Mator Smash](https://github.com/matortheeternal/smash/releases)
4. Writes ModOrganizer.ini with launchers to other tools
5. Prints some guidance what to do next.

### Usage
* Install python3 with pip support
* git clone this repo or download as zip
* start cmd in the folder do:
```
pip install -r requirements.txt
```
* to install pyunpack and patool modules
* then check utils.json and run the main.py

## build_modpack.py
Verifies if file is Nexus mod (by regex /\-(\d{3,})\-/) and collects info about it.

Does a checksum and save it as modpack_json('modpack.json'), which can be used by others using verify_modpack.py

Currently setup for **Skyrim**, for **Fallout 4** support change Game variable in Input (line 31+)

Script will scan the current directory (where the script is launched) (or change that in variable target), including all subfolders and excluding *.meta files.

### Usage
* Copy the script to folder with prepared nexus mods
* Run build_modpack.py and check the output json

#### Options:
 - Game = 'Fallout 4' or 'Skyrim' (sets the links and few other option for each Game)
 - debug = True (provides additional print information and writes summary.json when finished)
 - switch_ask_for_description = False (asks during scaning for description of the mod)
 - switch_ask_for_comment = False (asks during scanning for comment for the mod)
 - switch_get_nexus_info = True (will get ModName from title of the Nexus page)
 - if switch_get_nexus_info: (following is ignored if get_nexus_mod_name is False)
  - switch_get_skyrimgems_desc = True (will get description from [skyrimgems.com](http://skyrimgems.com/) (experimental))


##### Info gotten from file name:
	- file_name = what was scanned
	- has_installer = True or False, based on if there is FOMod\ModuleConfig.xml in archive
  - modID = Information between Name and Version
	- name = Everything before ModID in filename
  - nexus_link = http://www.nexusmods.com/$game/mods/ + $ModID $ + /
	- sha1 - checksum of the file_name

	- version = Everything after ModID in filename

##### If allowed it will get from web:
  - ModName = because Name of File does not always suggest name of the mod like [here](http://www.nexusmods.com/skyrim/mods/30947) it will get title of the Nexus Page
  - ModCategoryN = Number of category (MO uses it to determine the mod category)
  - ModCategory = Name of the category, used in csv
  - SkyrimGems description - will try to get description about mod from [skyrimgems.com](http://skyrimgems.com/) (experimental)

  Categories in meta files are numbered based on Nexus Mods Skyrim categories, when extracting the mods, category number gets converted based on categories.dat settings.

## verify_modpack.py

Verifies a bunch of mods downloaded from Nexus in a target folder against $modpack.json provided by build_modpack.py.

Mod is verified when checksum of the downloaded file is same as checksum of the entry for the mod in $modpack.json.

Verified mod is then extracted MO mods folder and meta.ini about the mod is written.

If the Mod has installer or extraction fails for some reason, the install file gets copied to MO download folder and meta file is written to them so MO does not need to make a query for info.

Script will scan the current directory (where the script is launched) (or change that in variable target), including all subfolders and excluding *.meta files.

### Usage
* Copy the script to folder with your "local nexus mods repository" (folders are not supported yet)
* Copy modpack.json from build_modpack.py to the same folder
* Run verify_modpack.py and let it move/copy mods to new folder

#### Options:
 - modpack_json = source.json
 - MO_bin = folder where to put verified files and write meta files
 - debug = True (provides additional print information and writes summary.json when finished)
 - switch_writeMetaFiles = True (if to write nexus info to meta file)
 - switch_get_nexus_info = True (if modpack_json does not have nexus_info, its useless)

##### TODOs
  - Print links for missing files, so users can easily download them
  - With that make soma kind of summary, how many files verified, etc.

##### Known Bugs
  - Mod pages with adult-content are not accesible without login, therefore if users allows getting information from web, only title can be extracted, only categories will be skipped. Currently in such situation all action are skipped.
  - Some queries for skyrimgems info fail, because is seaches for whole modName, shorter search must be performed

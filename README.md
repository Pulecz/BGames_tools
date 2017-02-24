# BGames_tools

Tries to help with gettting some of the Bethesda games playable by installing utilies for modding support and offers some helpers to install "modpacks"

Supported:
* **TES 5 Skyrim**
* **Fallout 4** (***WIP!***)

Ideall usage should be:
* get utils.json for main.py
* run main.py
* get some modpack.json
* run verify_modpack.py
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
* git clone this or download as zip
* start cmd in the folder do:
```
pip install -r requirements.txt
```
* to install pyunpack and patool modules
* then check utils.json and run the main.py

## build_modpack.py
Verifies if file is Nexus mod (by regex /\-(\d{3,})\-/) and collects info about it.

Does a checksum and save it as modpack_json('modpack.json'), which can be used by others using verify_modpack.py

Currently setup for **Skyrim**, for **Fallout 4** support change Game var in Input (line 31+)

Script will scan the current directory (where the script is launched) (or change that in variable target), excluding folders and *.meta files.

### Usage
* Copy the script to folder with prepared nexus mods (folders are not supported yet)
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

Verified mod is then moved (or copied if moving failes) to MO_bin and MO like meta files are written (versions needs to be parsed) so Mod Organizer can work with it.

Script will scan the current directory (where the script is launched) (or change that in variable target), excluding folders and *.meta files.

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
  - Print links for missing files, so users can easilly download them
  - With that make soma kind of summary, how many files verified, etc
  - Mod Organizer doesn't need meta files from us, it can query it allright, might be useful for some mods that got deleted from Nexus


##### Known Bugs
  - Mod pages with adult-content are not accesible without login, therefore if users allows getting information from web, only title can be extracted, only categories will be skipped. Currently in such situation all action are skipped.
  - Some queries for skyrimgems info fail, because is seaches for whole modName, shorter search must be performed
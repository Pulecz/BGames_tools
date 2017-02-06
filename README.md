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


## mod_name_validator.py

Script to sort mods with Nexus Mods names (pattern $nexusid-$name) and write summary.csv with information extracted.

Currently setup for **Skyrim**, for **Fallout 4** support just uncomment line 24 and comment line 25

Script will scan the current directory (where the script is launched), excluding folders and (currently) *.meta files.
Then by using regex /\-(\d{2,})\-/ it will catch any Nexus Mod files and extract information from the name or get additional info from web.

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

##### The scripts does the following:
0. Validates the Game variable and change a option based on that and prepares few variables
  - If Game variable validation fails, scripts tells it to user and awaits confirmation
1. Scans the current working folder (folder where the scripts is used)
2. Try to validate each file through regex filter to validate any mods with Nexus Mod file pattern
3. Collects choosen info about the mod or asks for comment or description if allowed
4. If allowed, script will will create folders with pattern "$ModName-$ModID" and
  - If getting info from Nexus is not allowed (no internet connectivity) the folders will be named "$Name-$ModID.
5. If allowed files will be moved to the created folders
6. If allowed meta files will be created for each mod.
  - Meta files are useful when you move the mod with them to downloads folder of [Mod Organizer](http://www.nexusmods.com/skyrim/mods/1334/) it can read Name, ModName, ModID and version from the meta file, but it often deletes the meta file for some reason first.
  - Comment is also written to meta file. Comment line is not handled by ModOrganizer in any way (it will not delete it from the meta file after querying its own info) AFAIK. Could be useful for something though.
7. If debug is on, then the python's dictionary with all the collected info about mod is written in summary.json (json editors should be able to open it)
8. If writeSummary is allowed, summary.csv is created, if its still open by something that does not allow to manipulate it(Libre Office Calc) scripts tells that to user and asks for confirmation to try saving again.
  - **Warning** if file is not used, it gets simply overwritten

The version is formatted in MO way so version:
  - '2292e' is written as '2.2.9.2e',
  - '4-0-1' as '4.0.1.0'
  - '3-0a' as '3.0.0.0a' and etc.
However this sometimes fails, currently there is no option to turn this off (**todo simple switch**)
This also applies for csv. (**todo also switch**)

Categories in meta files are numbered based on Nexus Mods Skyrim categories(I don't have info about FO4 MO yet), after instaling the mods, number in meta of the mods is numbered in Mod Organizers way.


##### Options:
 - Game = 'Fallout 4' or 'Skyrim' (sets the links and few other option for each Game)
 - debug = True (provides additional print information and writes summary.json when finished)
 - writeSummary = True (writes summary.csv)
 - makeDirs = True (create directories for mod)
 - if makeDirs: (following is ignored if makeDirs is False)
  - moveFiles = True (will move files to their folders)
  - writeMetaFiles = True (meta files for [Mod Organizer](http://www.nexusmods.com/skyrim/mods/1334/))
 - ask_for_description = False (asks during scaning for description of the mod)
 - ask_for_comment = False (asks during scanning for comment for the mod)
 - get_nexus_mod_name = True (will get ModName from title of the Nexus page)
 - if get_nexus_mod_name: (following is ignored if get_nexus_mod_name is False)
  - get_skyrimgems_desc = True (will get description from [skyrimgems.com](http://skyrimgems.com/) (experimental))

Every variable can be changed in first 40 lines.

##### Known Issues
  - Mod Organizer deletes the meta files after (manual) moving them to download folder

##### Known Bugs
  - Version conversion fail at [Full Dialogue Interface](http://www.nexusmods.com/fallout4/mods/1235/) for Fallout 4, because of the "uncommon" versioning
  - Files with pattern $name$version$modid$version get parsed incorrectly as the regex is not sure what is version and what modid. For example SMIM 1-89-8655-1-89.7z, the first 89 is caught with regex /\-(\d{2,})\-/. ...guess I need better regex skills
  - Mod pages with adult-content are not accesible without login, therefore if users allows getting information from web, only title can be extracted, only categories will be skipped. Currently in such situation all action are skipped.
  - Some queries for skyrimgems info fail, because is seaches for whole modName, shorter search must be performed

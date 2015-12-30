# SkyrimModding

### mod_name_validator.py

Script to sort Nexus Mods to folders, with pattern ($nexusid-$name) and write summary.csv with information extracted.

Currently setup for **Skyrim**, for **Fallout 4** support just uncomment line 24 and comment line 25

Script will scan the current directory (where the script is launched), excluding folders and (currently) *.meta files.
Then by using regex /\-(\d{2,})\-/ it will catch any Nexus Mod files and extract information from the name or get additional info from web.

#####Info gotten from file name:
  - Name = Everything before ModID in filename
  - File Name = what was scanned
  - ModID = Information between Name and Version
  - Version = Everything after ModID in filename
  - Link to Nexus page = http://www.nexusmods.com/$game/mods/ + $ModID $ + /

#####If allowed it will get from web:
  - ModName = because Name of File does not always suggest name of the mod like [here](http://www.nexusmods.com/skyrim/mods/30947) it will get title of the Nexus Page
  - ModCategoryN = Number of category (MO uses it to determine the mod category)
  - ModCategory = Name of the category, used in csv
  - SkyrimGems description - will try to get description about mod from [skyrimgems.com](http://skyrimgems.com/) (experimental)

Then if allowed script will create folders with pattern "$ModName-$ModID" and if getting info from Nexus is not allowed (no internet connectivity) the folders will be named "$Name-$ModID.
Files can be moved to those folders and meta files can be created for them. If then moved to downloads folder of [Mod Organizer](http://www.nexusmods.com/skyrim/mods/1334/) it can read Name, ModName, ModID and version from the meta file.
The version is formatted in MO way so version '2292e' is written as '2.2.9.2e', '4-0-1' as '4.0.1.0' and '3-0a' as '3.0.0.0a' and etc. This also applies for csv.
Comment is also written to meta file and script can ask user for comment for each Mod. Comment line is not handled by ModOrganizer in any way as far as I know.
Newly Nexus category number is also written to meta file, MO then chooses its own category for the mod.

#####Options:
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

#####Known Issues
  - Mod Organizer deletes the meta files after (manual) moving them to download folder
  - **TOFIX** Mod pages with adult-content are not accesible without login, therefore if users allows getting information from web, only title can be extracted, only categories will be skipped. Currently in such situation all action are skipped.

#####Known Bugs
  - Version conversion fail at [Full Dialogue Interface](http://www.nexusmods.com/fallout4/mods/1235/) for Fallout 4, because of the "uncommon" versioning
  - Files with pattern $name$version$modid$version get parsed incorrectly as the regex is not sure what is version and what modid. For example SMIM 1-89-8655-1-89.7z, the first 89 is caught with regex /\-(\d{2,})\-/. ...guess I need better regex skills
  


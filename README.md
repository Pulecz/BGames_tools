# SkyrimModding

### main.py
Script to prepare fresh Skyrim installation (Skyrim Launcher needs to be run at least once, to create entry in registry) for modding.
Everything is unpacked using 7z.exe , therefore [7zip](http://www.7-zip.org/) installed in (one of the) Program Files is required.

#####The scripts does the following:
1. Checks if 7z.exe exist in Program Files/7-Zip.
2. Validates the Skyrim and Skyrim Mods folder, prompts user to confirm them or edit them.
3. Unpacks [Mod Organizer](http://www.nexusmods.com/skyrim/mods/1334/)
4. Writes ModOrganizer.ini with paths to other tools and few settings from [here](http://wiki.step-project.com/User:Neovalen/Skyrim_Revisited_-_Legendary_Edition#Configure_Mod_Organizer).
5. Unpacks [SKSE](http://skse.silverlock.org) to Skyrim root folder and scripts to Skyrim/data.
6. Unpacks 'WrapperVersion/d3d9.dll' and 'WrapperVersion/enbhost.exe' from [ENB](http://enbdev.com/download_mod_tesskyrim.html) archive to Skyrim root folder.
7. Unpacks [LOOT](https://loot.github.io/) to Mods Folder.
8. Unpacks [Wrye Bash](http://www.nexusmods.com/skyrim/mods/1840/) to Mods Folder.
9. Unpacks [TES5Edit](http://www.nexusmods.com/skyrim/mods/25859/) to Mods Folder.
10. If allowed prints some guidance.

The rest is future.

If you wish to edit what scripts install, comment or delete one of these lines.

ASI_base_install module is documented in the next section [here](../master/README.md#asi_base_installpy).

Load ASI_base_install module, if 7z does not exist, exit 1 here.
```python
import ASI_base_install # loading of this module causes lust for 7z binary
```
Prompts the user to confirm or edit the directories and loads skyrim_dir and skyrim_mods_dir to script, to be used later.
```python
skyrim_dir, skyrim_mods_dir = ASI_base_install.confirm_dirs()
```
Creates directory in Skyrim folder.
```python
ASI_base_install.make_mods_folder_in_base() #can cause exit 2
```
Unpacks [Mod Organizer](http://www.nexusmods.com/skyrim/mods/1334/)
```python
ASI_base_install.MO_install()
```
Writes ModOrganizer.ini with paths to other tools and few settings from [here](http://wiki.step-project.com/User:Neovalen/Skyrim_Revisited_-_Legendary_Edition#Configure_Mod_Organizer).

Launching MO Installer is possible, but not really necessary, only setting unchecked in installer is handling Nexus Links and shortcut to start menu. User is prompted in first MO's start to handle Nexus links and people who want shortcut can make it. :-)
```python
ASI_base_install.write_MO_ini()
```
Unpacks [SKSE](http://skse.silverlock.org) to Skyrim root folder and scripts to Skyrim/data.

In order to launch installer, admin rights are required if using UAC, therefore is not used.
```python
ASI_base_install.SKSE_install()
```
Unpacks 'WrapperVersion/d3d9.dll' and 'WrapperVersion/enbhost.exe' from [ENB](http://enbdev.com/download_mod_tesskyrim.html) archive to Skyrim root folder.
```python
ASI_base_install.ENB_install()
```
Unpacks [LOOT](https://loot.github.io/) to Mods Folder.
```python
ASI_base_install.LOOT_install()
```
Unpacks [Wrye Bash](http://www.nexusmods.com/skyrim/mods/1840/) to Mods Folder.
```python
ASI_base_install.WRYE_BASH_install()
```
Unpacks [TES5Edit](http://www.nexusmods.com/skyrim/mods/25859/) to Mods Folder.
```python
ASI_base_install.TES5E_install()
```

### ASI_base_install.py

Remains to be done, hopefully in the meantime the script itself is readable as it is.

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

#####The scripts does the following:
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
  
#####Known Bugs
  - Version conversion fail at [Full Dialogue Interface](http://www.nexusmods.com/fallout4/mods/1235/) for Fallout 4, because of the "uncommon" versioning
  - Files with pattern $name$version$modid$version get parsed incorrectly as the regex is not sure what is version and what modid. For example SMIM 1-89-8655-1-89.7z, the first 89 is caught with regex /\-(\d{2,})\-/. ...guess I need better regex skills
  - Mod pages with adult-content are not accesible without login, therefore if users allows getting information from web, only title can be extracted, only categories will be skipped. Currently in such situation all action are skipped.
  - Some queries for skyrimgems info fail, because is seaches for whole modName, shorter search must be performed


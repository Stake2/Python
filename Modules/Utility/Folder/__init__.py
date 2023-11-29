# Folder.py

import os

class Folder():
	def __init__(self):
		from Utility.Global_Switches import Global_Switches as Global_Switches

		# Global Switches dictionary
		self.switches = Global_Switches().switches["Global"]

		self.switches.update({
			"folder": {
				"create": True,
				"delete": True,
				"copy": True,
				"move": True
			}
		})

		if self.switches["testing"] == True:
			for switch in self.switches["folder"]:
				self.switches["folder"][switch] = False

		from Utility.Date import Date as Date
		from Utility.File import File as File
		from Utility.JSON import JSON as JSON

		self.Date = Date()
		self.File = File()
		self.JSON = JSON()

		self.app_settings = self.JSON.Language.app_settings
		self.languages = self.JSON.Language.languages
		self.date = self.Date.date

		self.Define_Folders()

		# Define module folders
		from Utility.Define_Folders import Define_Folders as Define_Folders

		Define_Folders(self)

		self.Define_Texts()
		self.Create_Folders()

	def Define_Folders(self):
		import platform
		import pathlib

		self.module = {
			"name": self.__module__.split(".")[-1],
			"key": self.__module__.split(".")[-1].lower().replace(" ", "_")
		}

		if self.module["name"] == "__main__":
			self.module["name"] = "Folder"

		self.hard_drive_letter = os.path.normpath(pathlib.Path.home().drive) + "/"

		# Root folders
		self.folders = {
			"root": {
				"root": self.hard_drive_letter,
				"hard_drive_letter": self.hard_drive_letter,
				"users": self.Sanitize(pathlib.Path.home().parent),
				"system32": {
					"root": self.Sanitize(os.path.join(os.environ["SystemRoot"], "SysNative" if platform.architecture()[0] == "32bit" else "System32"))
				}
			}
		}

		folder_names = [
			"Program Files",
			"Program Files (x86)",
			"Apps",
			"Art",
			"Mega",
			"Media",
			"Games",
			"XAMPP"
		]

		portuguese_folder_names = {
			"Art": self.JSON.Language.language_texts["art, title()"],
			"Media": self.JSON.Language.language_texts["medias, title()"],
			"Games": self.JSON.Language.language_texts["games, title()"]
		}

		for name in folder_names:
			key = name.lower().replace(" ", "_")

			# If the user language is "Portuguese"
			# And the folder name is inside the Portuguese folder names dictionary
			if (
				self.JSON.Language.system_information["Language"] == "pt" and
				name in portuguese_folder_names
			):
				# Rename the current folder name to its respective Portuguese folder name
				name = portuguese_folder_names[name]

			self.folders["root"][key] = {
				"root": self.folders["root"]["root"] + name + "/"
			}

		if "Media folder" in self.app_settings:
			self.folders["root"]["media"]["root"] = self.app_settings["Media folder"]

		if "Game folder" in self.app_settings:
			self.folders["root"]["games"]["root"] = self.app_settings["Game folder"]

		# "Apps" folders
		self.folders["apps"] = self.folders["root"]["apps"]

		# "Apps" sub folders
		for folder in ["Module files", "Modules", "Shortcuts"]:
			key = folder.lower().replace(" ", "_")

			if folder == "Shortcuts":
				folder = self.JSON.Language.language_texts["shortcuts, title()"]

			self.folders["apps"][key] = {
				"root": os.path.join(self.folders["apps"]["root"], folder + "/")
			}

		self.folders["apps"]["module_files"]["utility"] = {
			"root": self.folders["apps"]["module_files"]["root"] + "Utility/"
		}

		self.folders["apps"]["modules"]["modules"] = self.folders["apps"]["modules"]["root"] + "Modules.json"

		self.folders["apps"]["shortcuts"]["white_shortcuts"] = os.path.join(self.folders["apps"]["shortcuts"]["root"], "Ícone Branco/")

		# Jogos (Games) folders
		self.folders["games"] = self.folders["root"]["games"]

		for folder in ["Shortcuts", "Folders"]:
			key = folder.lower().replace(" ", "_")

			if key == "shortcuts":
				folder = self.JSON.Language.language_texts["shortcuts, title()"]

			if key == "folders":
				folder = self.JSON.Language.language_texts["folders, title()"]

			self.folders["games"][key] = {
				"root": os.path.join(self.folders["games"]["root"], folder + "/")
			}

		# User folders
		self.folders["user"] = {
			"root": self.Sanitize(os.path.join(self.folders["root"]["users"], pathlib.Path.home().name + "/"))
		}

		# "User" sub folders
		for folder in ["AppData", "Downloads", "Pictures", "Videos"]:
			key = folder.lower().replace(" ", "_")

			self.folders["user"][key] = {
				"root": os.path.join(self.folders["user"]["root"], folder + "/")
			}

		# "Downloads" folders
		folders = {
			"Mega": "",
			"Videos": self.JSON.Language.language_texts["videos, title()"]
		}

		for key, folder in folders.items():
			key = key.lower().replace(" ", "_")

			if folder == "":
				folder = self.Capitalize(key)

			self.folders["user"]["downloads"][key] = {
				"root": os.path.join(self.folders["user"]["downloads"]["root"], folder + "/")
			}

		# "AppData" folders
		for folder in ["Local", "Roaming"]:
			key = folder.lower().replace(" ", "_")

			self.folders["user"]["appdata"][key] = {
				"root": os.path.join(self.folders["user"]["appdata"]["root"], folder + "/")
			}

		self.folders["appdata"] = self.folders["user"]["appdata"]

		# System32 subfolders
		self.folders["root"]["system32"]["drivers/etc"] = self.Sanitize(os.path.join(self.folders["root"]["system32"]["root"], "drivers/etc/"))

		# "Art" subfolders
		folders = [
			"Paint Tool SAI",
			"Photoshop",
			"Sony Vegas"
		]

		self.folders["art"] = self.folders["root"]["art"]

		for folder in folders:
			key = folder.lower().replace(" ", "_")

			self.folders["art"][key] = {
				"root": os.path.join(self.folders["art"]["root"], folder + "/")
			}

		# Art "Photoshop" subfolders
		for folder in ["Ana", "Games", "Media", "Operational System", "PHP", "Render", "Stake2", "Stories", "Websites"]:
			key = folder.lower().replace(" ", "_")

			self.folders["art"]["photoshop"][key] = {
				"root": os.path.join(self.folders["art"]["photoshop"]["root"], folder + "/")
			}

		# Art "Sony Vegas" subfolders
		for folder in ["Render", "Story Covers"]:
			key = folder.lower().replace(" ", "_")

			self.folders["art"]["sony_vegas"][key] = {
				"root": os.path.join(self.folders["art"]["sony_vegas"]["root"], folder + "/")
			}

		# XAMPP folder
		self.folders["root"]["xampp"]["xampp-control"] = self.folders["root"]["xampp"]["root"] + "xampp-control.exe"

		# Mega folders
		self.folders["mega"] = {
			"root": self.folders["root"]["mega"]["root"]
		}

		# Mega subfolders
		folders = [
			"Notepad",
			"Image",
			"PHP",
			"Obsidian's Vaults",
			"Stories",
			"Websites"
		]

		for folder in folders:
			key = folder.lower().replace(" ", "_").replace("'", "_")

			if key == "notepad":
				folder = self.JSON.Language.language_texts["notepad, title()"]

			self.folders["mega"][key] = {
				"root": os.path.join(self.folders["mega"]["root"], folder + "/")
			}

		# Mega "Notepad" folders
		self.folders["mega"]["notepad"]["effort"] = {
			"root": os.path.join(self.folders["mega"]["notepad"]["root"], self.JSON.Language.language_texts["effort, title()"] + "/")
		}

		# Mega "Notepad" Effort folders
		folders = {
			"Diary": "",
			"Diary Slim": "",
			"Food": "",
			"Friends": self.JSON.Language.language_texts["friends, title()"],
			"Social_Networks": self.JSON.Language.language_texts["social_networks"],
			"Networks": "",
			"Years": ""
		}

		for key, folder in folders.items():
			key = key.lower().replace(" ", "_")

			if folder == "":
				folder = self.Capitalize(key.replace("_", " "))

			self.folders["mega"]["notepad"]["effort"][key] = {
				"root": os.path.join(self.folders["mega"]["notepad"]["effort"]["root"], folder + "/")
			}

		# Mega "Notepad" Effort Networks folders
		for network in ["Audiovisual Media Network", "Database Network", "Game Network", "Productive Network"]:
			# Network dictionary
			network = {
				"Title": network,
				"Key": network.lower().replace(" ", "_"),
				"Info": "",
				"History": "",
				"Type": "Entry",
				"Entries": "Entries",
				"Subfolders": [
					"Data"
				]
			}

			self.folders["mega"]["notepad"]["effort"]["networks"][network["Key"]] = {
				"root": os.path.join(self.folders["mega"]["notepad"]["effort"]["networks"]["root"], network["Title"] + "/")
			}			

			# "Audiovisual Media Network" subfolders
			if network["Title"] == "Audiovisual Media Network":
				network["Subfolders"].append("Comments")

				network.update({
					"Info": "Media",
					"History": "Watch",
					"Type": "Media"
				})

			# "Database Network" subfolders
			if network["Title"] == "Database Network":
				network.update({
					"Info": None,
					"History": None,
					"Type": None
				})

			# "Game Network" subfolders
			if network["Title"] == "Game Network":
				network.update({
					"Info": None,
					"History": "Play",
					"Type": "Game",
					"Entries": "Sessions"
				})

			# "Productive Network" subfolders
			if network["Title"] == "Productive Network":
				network.update({
					"History": "Task",
					"Type": "Task",
					"Entries": "Tasks"
				})

			# Network subfolder items
			for item in ["Info", "History"]:
				if network[item] != "":
					item_name = item

					if item == "Info" and network["Title"] in ["Database Network", "Game Network"]:
						item_name = "Information"

					if network[item] != None:
						network[item] = network[item] + " " + item_name

					if network[item] == None:
						network[item] = item_name

					network["Subfolders"].append(network[item])

					network[item] = network[item].lower().replace(" ", "_")

			for sub_folder in network["Subfolders"]:
				key = sub_folder.lower().replace(" ", "_")

				self.folders["mega"]["notepad"]["effort"]["networks"][network["Key"]][key] = {
					"root": os.path.join(self.folders["mega"]["notepad"]["effort"]["networks"][network["Key"]]["root"], sub_folder + "/")
				}

			if network["Title"] == "Audiovisual Media Network":
				# "Audiovisual Media Network/Comments" folders
				for item in ["Backups"]:
					key = item.lower().replace(" ", "_")

					self.folders["mega"]["notepad"]["effort"]["networks"][network["Key"]]["comments"][key] = {
						"root": os.path.join(self.folders["mega"]["notepad"]["effort"]["networks"][network["Key"]]["comments"]["root"], item + "/")
					}

				# "Audiovisual Media Network/Watch History" folders
				for item in ["Movies"]:
					key = item.lower().replace(" ", "_")

					self.folders["mega"]["notepad"]["effort"]["networks"][network["Key"]][network["History"]][key] = {
						"root": os.path.join(self.folders["mega"]["notepad"]["effort"]["networks"][network["Key"]][network["History"]]["root"], item + "/")
					}

			if network["Info"] != "":
				# Network "Info" folders and files
				for item in ["Info.json"]:
					key = item.lower().replace(" ", "_").replace(".json", "")

					self.folders["mega"]["notepad"]["effort"]["networks"][network["Key"]][network["Info"]][key] = os.path.join(self.folders["mega"]["notepad"]["effort"]["networks"][network["Key"]][network["Info"]]["root"], item)

			# Network "Data" folders and files
			for item in ["Types.json"]:
				key = item.lower().replace(" ", "_").replace(".json", "")

				self.folders["mega"]["notepad"]["effort"]["networks"][network["Key"]]["data"][key] = os.path.join(self.folders["mega"]["notepad"]["effort"]["networks"][network["Key"]]["data"]["root"], item)

			# "Network History" "History" file
			self.folders["mega"]["notepad"]["effort"]["networks"][network["Key"]][network["History"]]["history"] = os.path.join(self.folders["mega"]["notepad"]["effort"]["networks"][network["Key"]][network["History"]]["root"], "History.json")

			# "Network History" year folders
			for item in [self.date["Units"]["Year"]]:
				key = str(item).lower().replace(" ", "_")

				self.folders["mega"]["notepad"]["effort"]["networks"][network["Key"]][network["History"]][key] = {
					"root": os.path.join(self.folders["mega"]["notepad"]["effort"]["networks"][network["Key"]][network["History"]]["root"], str(item) + "/")
				}

				if network["Type"] != None:
					network["Type"] = " " + network["Type"] + " "

				if network["Type"] == None:
					network["Type"] = " "

				# Per Type folder
				for item in ["Per" + network["Type"] + "Type"]:
					self.folders["mega"]["notepad"]["effort"]["networks"][network["Key"]][network["History"]][key][item] = {
						"root": os.path.join(self.folders["mega"]["notepad"]["effort"]["networks"][network["Key"]][network["History"]][key]["root"], str(item) + "/")
					}

				# Entries.json file
				self.folders["mega"]["notepad"]["effort"]["networks"][network["Key"]][network["History"]][key][network["Entries"].lower()] = self.folders["mega"]["notepad"]["effort"]["networks"][network["Key"]][network["History"]][key]["root"] + network["Entries"] + ".json"

				# Entry list.txt file
				self.folders["mega"]["notepad"]["effort"]["networks"][network["Key"]][network["History"]][key]["entry_list"] = self.folders["mega"]["notepad"]["effort"]["networks"][network["Key"]][network["History"]][key]["root"] + "Entry list.txt"

		# Mega "Notepad" Years folders
		starting_year = 2018
		current_year = self.date["Units"]["Year"]

		for item in range(starting_year, current_year + 1):
			key = str(item).lower().replace(" ", "_")

			self.folders["mega"]["notepad"]["effort"]["years"][key] = {
				"root": os.path.join(self.folders["mega"]["notepad"]["effort"]["years"]["root"], str(item) + "/")
			}

			if key == str(self.date["Units"]["Year"]):
				# Per language years folder
				for language in self.languages["small"]:
					full_language = self.languages["full"][language]

					self.folders["mega"]["notepad"]["effort"]["years"][key][full_language] = {
						"root": self.folders["mega"]["notepad"]["effort"]["years"][key]["root"] + full_language + "/"
					}

				self.folders["mega"]["notepad"]["effort"]["years"]["current_year"] = self.folders["mega"]["notepad"]["effort"]["years"][key]

		# "Notepad" folders dictionary
		self.folders["notepad"] = {}

		for key in self.folders["mega"]["notepad"]:
			self.folders["notepad"][key] = self.folders["mega"]["notepad"][key]

		for key in self.folders["mega"]["notepad"]["effort"]:
			self.folders["notepad"][key] = self.folders["mega"]["notepad"]["effort"][key]

		# Mega "Image" folders
		folders = {
			"Friends": self.JSON.Language.language_texts["friends, title()"],
			"Social_Networks": self.JSON.Language.language_texts["social_networks"],
			"Years": self.Date.language_texts["years, title()"]
		}

		for key, folder in folders.items():
			key = key.lower().replace(" ", "_")

			if folder == "":
				folder = self.Capitalize(key)

			self.folders["mega"]["image"][key] = {
				"root": os.path.join(self.folders["mega"]["image"]["root"], folder + "/")
			}

		# Mega "Image" Years folders
		folders = {
			"Images": self.JSON.Language.language_texts["images, title()"]
		}

		for key, folder in folders.items():
			key = key.lower().replace(" ", "_")

			if folder == "":
				folder = self.Capitalize(key)

			self.folders["mega"]["image"]["years"][key] = {
				"root": os.path.join(self.folders["mega"]["image"]["years"]["root"], folder + "/")
			}

		# Mega "PHP" folders
		for item in ["JSON"]:
			key = item.lower().replace(" ", "_")

			self.folders["mega"]["php"][key] = {
				"root": os.path.join(self.folders["mega"]["php"]["root"], item + "/")
			}

		# Mega "PHP" JSON files
		for item in ["Colors", "URL", "Websites"]:
			key = item.lower().replace(" ", "_")

			self.folders["mega"]["php"]["json"][key] = os.path.join(self.folders["mega"]["php"]["json"]["root"], item + ".json")

		# Mega Obsidian's Vaults folders
		for item in ["Creativity"]:
			key = item.lower().replace(" ", "_")

			self.folders["mega"]["obsidian_s_vaults"][key] = {
				"root": os.path.join(self.folders["mega"]["obsidian_s_vaults"]["root"], item + "/")
			}

		# Mega Obsidian's Vaults/Creativity folders
		for item in ["Literature"]:
			key = item.lower().replace(" ", "_")

			self.folders["mega"]["obsidian_s_vaults"]["creativity"][key] = {
				"root": os.path.join(self.folders["mega"]["obsidian_s_vaults"]["creativity"]["root"], item + "/")
			}

		# Mega Obsidian's Vaults/Creativity/Literature folders
		for item in ["Stories"]:
			key = item.lower().replace(" ", "_")

			self.folders["mega"]["obsidian_s_vaults"]["creativity"]["literature"][key] = {
				"root": os.path.join(self.folders["mega"]["obsidian_s_vaults"]["creativity"]["literature"]["root"], item + "/")
			}

		# Mega Websites folders and files
		for item in ["Website.json", "Images"]:
			key = item.lower().replace(" ", "_").replace(".json", "")

			if "." in item:
				self.folders["mega"]["websites"][key] = os.path.join(self.folders["mega"]["websites"]["root"], item)

			else:
				self.folders["mega"]["websites"][key] = {
					"root": os.path.join(self.folders["mega"]["websites"]["root"], item + "/")
				}

		self.folders["mega"]["websites"]["images"]["story_covers"] = {
			"root": self.folders["mega"]["websites"]["images"]["root"] + "Story Covers/"
		}

		# "Media" folder
		self.folders["media"] = self.folders["root"]["media"]

		# Get website subdomain
		self.website = {}
		self.links = {}

		if self.File.Exist(self.folders["mega"]["websites"]["website"]) == True:
			self.website = self.JSON.To_Python(self.folders["mega"]["websites"]["website"])

			# Create links dictionary with Stake2 Website link
			self.links = {
				"Stake2 Website": "https://" + self.website["subdomain"] + "." + self.website["netlify"] + "/"
			}

	def Define_Texts(self):
		self.texts = self.JSON.To_Python(self.folders["apps"]["module_files"]["utility"][self.module["key"]]["texts"])

		self.language_texts = self.JSON.Language.Item(self.texts)

	def Capitalize(self, text, lower = False):
		text = list(text)

		if lower == False:
			text[0] = text[0].upper()

		if lower == True:
			text[0] = text[0].lower()

		text = "".join(text)

		return text

	def Sanitize(self, path, restricted_characters = False):
		if restricted_characters == False:
			path = os.path.normpath(path).replace("\\", "/")

			if os.path.splitext(path)[-1] == "" and "/" not in path[-1]:
				path += "/"

		if restricted_characters == True:
			restricted_characters = [":", "?", '"', "\\", "/", "|", "*", "<", ">"]

			for character in restricted_characters:
				if character in path:
					path = path.replace(character, "")

		return path

	def Split(self, path):
		return os.path.split(path)

	def Verbose(self, text, item, verbose = False):
		if (
			self.switches["verbose"] == True or
			verbose == True
		):
			import inspect

			print(self.JSON.Language.space_text)
			print(self.module["name"] + "." + inspect.stack()[1][3] + "():")
			print("\t" + text + ":")
			print("\t" + item)

	def Exist(self, path):
		path = self.Sanitize(path)

		if os.path.isdir(path) == True:
			return True

		if os.path.isdir(path) == False:
			return False

	def Type(self, text = None):
		if text == None:
			text = self.language_texts["type_or_paste_the_folder"] + ": "

		print()

		return input(text)

	def Create(self, folder = None, text = None):
		if folder == None:
			folder = self.Type(text)

		folder = self.Sanitize(folder)

		if self.Exist(folder) == True:
			return False

		if (
			self.switches["folder"]["create"] == True and
			self.Exist(folder) == False
		):
			os.mkdir(folder)

			self.Verbose(self.language_texts["folder"].title() + " " + self.language_texts["created"], folder)

			return True

		else:
			self.Verbose(self.language_texts["it_was_not_possible_to_{}_the_folder_permission_not_granted"].format(self.language_texts["create"]), folder, verbose = True)

			return False

	def Create_Folders(self, folders = None, depth = 0):
		if folders == None:
			folders = self.folders

		for value in folders.values():
			if type(value) != dict:
				if os.path.isfile(value) == False and "." not in value:
					self.Create(value)

				if os.path.isfile(value) == False and "." in value:
					self.File.Create(value)

			if type(value) == dict:
				found = self.Create_Folders(value, depth = depth + 1)

	def Delete(self, folder):
		if folder == None:
			folder = self.Type()

		folder = self.Sanitize(folder)

		if self.Exist(folder) == False:
			self.Verbose(self.language_texts["this_folder_does_not_exists"], folder)

			return False

		if self.switches["folder"]["delete"] == True and self.Exist(folder) == True:
			try:
				# Folder is empty
				os.rmdir(folder)

			except OSError:
				import shutil

				# Folder is not empty
				shutil.rmtree(folder)

			self.Verbose(self.language_texts["folder"].title() + " " + self.language_texts["deleted"], folder)

			return True

		else:
			self.Verbose(self.language_texts["it_was_not_possible_to_{}_the_folder_permission_not_granted"].format(self.language_texts["delete"]), folder, verbose = True)

			return False

	def Copy(self, source_folder = None, destination_folder = None):
		if source_folder == None:
			source_folder = self.Type()

		if destination_folder == None:
			destination_folder = self.Type()

		source_folder = self.Sanitize(source_folder)
		destination_folder = self.Sanitize(destination_folder)

		if self.Exist(source_folder) == False:
			self.Verbose(self.language_texts["this_folder_does_not_exists"], source_folder)

			return False

		if self.switches["folder"]["copy"] == True and self.Exist(source_folder) == True:
			from distutils.dir_util import copy_tree
			copy_tree(source_folder, destination_folder)

			self.Verbose(self.language_texts["source_folder"] + ":\n\t" + source_folder + "\n\n\t" + self.language_texts["destination_folder"], destination_folder)

			return True

		else:
			self.Verbose(self.language_texts["it_was_not_possible_to_{}_the_folder_permission_not_granted"].format(self.language_texts["copy"]) + "." + "\n\n\t" + self.language_texts["source_folder"] + ":\n\t" + source_folder + "\n\n\t" + self.language_texts["destination_folder"], destination_folder, verbose = True)

			return False

	def Move(self, source_folder = None, destination_folder = None):
		if source_folder == None:
			source_folder = self.Type()

		if destination_folder == None:
			destination_folder = self.Type()

		source_folder = self.Sanitize(source_folder)
		destination_folder = self.Sanitize(destination_folder)

		if self.Exist(source_folder) == False:
			self.Verbose(self.language_texts["this_folder_does_not_exists"], source_folder)

			return False

		if self.switches["folder"]["move"] == True and self.Exist(source_folder) == True:
			import shutil

			for file_name in os.listdir(source_folder):
				source = os.path.join(source_folder, file_name)
				destination = os.path.join(destination_folder, file_name)

				shutil.move(source, destination)

			self.Verbose(self.language_texts["source_folder"] + ":\n\t" + source_folder + "\n\n\t" + self.language_texts["destination_folder"], destination_folder)

			return True

		else:
			self.Verbose(self.language_texts["it_was_not_possible_to_{}_the_folder_permission_not_granted"].format(self.language_texts["move"]) + "." + "\n\n\t" + self.language_texts["source_folder"] + ":\n\t" + source_folder + "\n\n\t" + self.language_texts["destination_folder"], destination_folder, verbose = True)

			return False

	def List(self, folder, contents_parameter = None):
		contents = contents_parameter

		if contents == None:
			contents = self.contents

		defined_contents = ""

		for item in os.listdir(folder):
			name = item
			item = self.Sanitize(folder + item)
			folder_name = item.split("/")[-2]

			self.contents["size"] += os.stat(folder + "/" + name).st_size

			if os.path.isdir(item) == True:
				if name not in self.contents["folder"]["names"]:
					self.contents["folder"]["names"].append(name)

				if item not in self.contents["folder"]["list"]:
					self.contents["folder"]["list"].append(item)

				defined_contents = contents["folders"]

				if folder_name not in defined_contents:
					defined_contents[folder_name] = {}

				defined_contents[folder_name]["root"] = self.Sanitize(item)

			if os.path.isfile(item) == True:
				item = self.Sanitize(folder + name, check = False)

				if name not in self.contents["file"]["names"]:
					self.contents["file"]["names"].append(name)

				if item not in self.contents["file"]["list"]:
					self.contents["file"]["list"].append(item)

				defined_contents = contents["files"]

				if contents_parameter != None and folder_name not in defined_contents:
					defined_contents[folder_name] = {}

				file_name = os.path.splitext(os.path.basename(item))[0]

				if contents_parameter == None:
					defined_contents[file_name] = item

				if contents_parameter != None:
					defined_contents[folder_name][file_name] = item

		return defined_contents

	def Old_Contents(self, folder, add_none = False):
		folder = self.Sanitize(folder)

		self.contents = {
			"folders": {},
			"root_folders": [],
			"folder_list": [],
			"folder_names": [],
			"files": {},
			"file_list": [],
			"file_names": [],
			"size": 0
		}

		self.contents["root_folders"] = os.listdir(folder)

		for item in self.contents["root_folders"].copy():
			if os.path.isfile(self.Sanitize(folder + item)) == True:
				self.contents["root_folders"].remove(item)

		if self.Exist(folder) == True:
			self.List(folder)

			folders = self.contents["folders"].copy()

			for local_folder in folders:
				self.List(self.contents["folders"][local_folder]["root"], {"folders": self.contents["folders"][local_folder], "files": self.contents["files"]})

				if local_folder not in self.contents["files"]:
					self.contents["files"][local_folder] = {}

				for sub_folder_name in self.contents["folders"][local_folder].copy():
					if sub_folder_name in self.contents["folders"][local_folder]:
						sub_folder = self.contents["folders"][local_folder][sub_folder_name]

						if type(sub_folder) == dict:
							if sub_folder_name not in self.contents["folders"][local_folder]:
								self.contents["folders"][local_folder][sub_folder_name] = {}

							if sub_folder_name not in self.contents["files"][local_folder]:
								self.contents["files"][local_folder][sub_folder_name] = {}

							sub_folder = sub_folder["root"]

						dictionary = self.List(sub_folder, {"folders": self.contents["folders"][local_folder], "files": self.contents["folders"][local_folder]})

						for key in dictionary:
							value = dictionary[key]

							if type(value) == str:
								if os.path.isdir(value) == True:
									self.contents["folders"][local_folder][key] = value

							if type(value) == dict:
								for sub_key in value:
									sub_value = value[sub_key]

									if os.path.isfile(sub_value) == True:
										if key == local_folder:
											self.contents["files"][local_folder][sub_folder_name] = sub_value

										if key != local_folder and type(self.contents["files"][local_folder][sub_folder_name]) != str:
											self.contents["files"][local_folder][sub_folder_name][sub_key] = sub_value

						if "root" in self.contents["files"][local_folder]:
							del self.contents["files"][local_folder]["root"]

						if local_folder in self.contents["files"] and sub_folder_name in self.contents["files"][local_folder] and "root" in self.contents["files"][local_folder][sub_folder_name]:
							del self.contents["files"][local_folder][sub_folder_name]["root"]

						if local_folder in self.contents["folders"][local_folder]:
							del self.contents["folders"][local_folder][local_folder]

		if self.Exist(folder) == False:
			self.Verbose(self.language_texts["this_folder_does_not_exists"], folder)

		return self.contents

	def Remove_Folders(self, dictionary, to_remove):
		for item in to_remove:
			if item in dictionary:
				if type(dictionary) == list:
					dictionary.remove(item)

				if type(dictionary) == dict:
					dictionary.pop(item)

		if type(dictionary) != list:
			for key in dictionary.copy():
				for item in to_remove:
					if type(dictionary[key]) != str:
						if item in dictionary[key]:
							dictionary[key].pop(item)

					if item == key:
						dictionary.pop(key)

		return dictionary

	def Contents(self, folder, add_sub_folders = True, lower_key = False):
		folder = self.Sanitize(folder)
		folder_name = folder.split("/")[-1]

		if folder_name == "":
			folder_name = folder.split("/")[-2]

		contents = {
			"folder": {},
			"file": {},
			"dictionary": {},
			"size": 0
		}

		# Create the folder and file keys
		for key in ["folder", "file"]:
			# Iterate through the sub-keys
			for sub_key in ["list", "names", "dictionary"]:
				# Define the value (list or dictionary)
				value = []

				if sub_key == "dictionary":
					value = {}

				# Create the sub-key
				contents[key][sub_key] = value

		contents["dictionary"]["root"] = folder

		for (root_folder, sub_folders, files) in os.walk(folder, topdown=True):
			root_folder = self.Sanitize(root_folder)

			# Folder name to folder names
			root_folder_name = root_folder.split("/")[-1]

			if root_folder_name == "":
				root_folder_name = root_folder.split("/")[-2]

			if folder.count("/") + 1 == root_folder.count("/"):
				# Folder path to folder list
				contents["folder"]["list"].append(self.Sanitize(root_folder))

				contents["folder"]["names"].append(root_folder_name)

			# Add files to list and names lists
			i = 0
			for file in files:
				file_name = files[i].split(".")[0]

				if (
					len(files[i].split(".")) not in [0, 1] and
					files[i].count(".") > 1
				):
					file_name = ""

					for item in files[i].split("."):
						if item != files[i].split(".")[-1]:
							file_name += item

							if item != files[i].split(".")[-2]:
								file_name += "."

				if "/" not in root_folder[-1]:
					root_folder += "/"

				files[i] = self.Sanitize(root_folder) + files[i]

				# File path to Entry list
				contents["file"]["list"].append(files[i])

				# File name to file names
				contents["file"]["names"].append(file_name)

				i += 1

			# Root folder on dictionary if slash count of root folder is equal to folder plus one slash or equal to folder
			# Add subfolders
			if (
				folder.count("/") + 1 == root_folder.count("/") or
				folder.count("/") == root_folder.count("/")
			):
				if lower_key == True:
					root_folder_name = root_folder_name.lower().replace(" ", "_")

				if (
					root_folder_name not in contents["dictionary"] and
					root_folder_name != folder_name
				):
					contents["dictionary"][root_folder_name] = {}

					if "root" not in contents["dictionary"][root_folder_name]:
						contents["dictionary"][root_folder_name]["root"] = self.Sanitize(root_folder)

				# Add subfiles to dictionary
				i = 0
				for file in files:
					file_name = files[i].split("/")[-1].split(".")[0]

					if (
						len(files[i].split(".")) not in [0, 1] and
						files[i].split("/")[-1].count(".") > 1
					):
						file_name = ""

						for item in files[i].split("/")[-1].split("."):
							if item != files[i].split("/")[-1].split(".")[-1]:
								file_name += item

								if item != files[i].split("/")[-1].split(".")[-2]:
									file_name += "."

					if lower_key == True:
						file_name = file_name.lower().replace(" ", "_").replace(".", "")

					# If file is root file, from folder, add it to the root key
					if folder.count("/") == root_folder.count("/"):
						contents["dictionary"][file_name] = files[i]

					# Add file if root_folder_name key is not string
					if (
						root_folder_name in contents["dictionary"] and
						type(contents["dictionary"][root_folder_name]) != str
					):
						contents["dictionary"][root_folder_name][file_name] = files[i]

					if os.path.isfile(files[i]) == True:
						contents["size"] += os.stat(files[i]).st_size

					i += 1

				contents["size"] += os.stat(root_folder).st_size

			# Root folder on dictionary if slash count of root folder is equal to folder plus two slash or equal to folder
			# Add sub-sub-folders
			if folder.count("/") + 2 == root_folder.count("/"):
				root_folder = self.Sanitize(root_folder)

				root_folder_name = root_folder.split("/")[-3]
				sub_sub_folder_name = root_folder.split("/")[-2]

				if lower_key == True:
					root_folder_name = root_folder_name.lower().replace(" ", "_")
					sub_sub_folder_name = sub_sub_folder_name.lower().replace(" ", "_")

				# Add the sub-sub-folder to dictionary
				if (
					root_folder_name in contents["dictionary"] and
					sub_sub_folder_name not in contents["dictionary"][root_folder_name] and
					sub_sub_folder_name != folder_name and
					type(contents["dictionary"][root_folder_name]) != str
				):
					contents["dictionary"][root_folder_name][sub_sub_folder_name] = {}

					if "root" not in contents["dictionary"][root_folder_name][sub_sub_folder_name]:
						contents["dictionary"][root_folder_name][sub_sub_folder_name]["root"] = self.Sanitize(root_folder)

				# Add the sub-sub-sub-files to dictionary
				i = 0
				for file in files:
					file_name = files[i].split("/")[-1].split(".")[0]

					if (
						len(files[i].split(".")) not in [0, 1] and
						files[i].split("/")[-1].count(".") > 1
					):
						file_name = ""

						for item in files[i].split("/")[-1].split("."):
							if item != files[i].split("/")[-1].split(".")[-1]:
								file_name += item

								if item != files[i].split("/")[-1].split(".")[-2]:
									file_name += "."

					if lower_key == True:
						file_name = file_name.lower().replace(" ", "_").replace(".", "")

					# Add file if root_folder_name key is not string
					if (
						type(contents["dictionary"]) != str and
						root_folder_name in contents["dictionary"] and
						type(contents["dictionary"][root_folder_name]) != str and
						type(contents["dictionary"][root_folder_name][sub_sub_folder_name]) != str
					):
						contents["dictionary"][root_folder_name][sub_sub_folder_name][file_name] = files[i]

					if os.path.isfile(files[i]) == True:
						contents["size"] += os.stat(files[i]).st_size

					i += 1

				contents["size"] += os.stat(root_folder).st_size

			# Root folder on dictionary if slash count of root folder is equal to folder plus three slash or equal to folder
			# Add sub-sub-sub-folders
			if folder.count("/") + 3 == root_folder.count("/"):
				root_folder = self.Sanitize(root_folder)

				root_folder_name = root_folder.split("/")[-4]
				sub_sub_folder_name = root_folder.split("/")[-3]
				sub_sub_sub_folder_name = root_folder.split("/")[-2]

				if lower_key == True:
					root_folder_name = root_folder_name.lower().replace(" ", "_")
					sub_sub_folder_name = sub_sub_folder_name.lower().replace(" ", "_")
					sub_sub_sub_folder_name = sub_sub_sub_folder_name.lower().replace(" ", "_")

				# Add sub-sub-sub-folder to dictionary
				if (
					root_folder_name in contents["dictionary"] and
					sub_sub_folder_name in contents["dictionary"][root_folder_name] and
					type(contents["dictionary"][root_folder_name][sub_sub_folder_name]) != str
				):
					contents["dictionary"][root_folder_name][sub_sub_folder_name][sub_sub_sub_folder_name] = {}

					if "root" not in contents["dictionary"][root_folder_name][sub_sub_folder_name][sub_sub_sub_folder_name]:
						contents["dictionary"][root_folder_name][sub_sub_folder_name][sub_sub_sub_folder_name]["root"] = self.Sanitize(root_folder)

				# Add sub-sub-sub-sub-files to dictionary
				i = 0
				for file in files:
					file_name = files[i].split("/")[-1].split(".")[0]

					if (
						len(files[i].split(".")) not in [0, 1] and
						files[i].split("/")[-1].count(".") > 1
					):
						file_name = ""

						for item in files[i].split("/")[-1].split("."):
							if item != files[i].split("/")[-1].split(".")[-1]:
								file_name += item

								if item != files[i].split("/")[-1].split(".")[-2]:
									file_name += "."

					if lower_key == True:
						file_name = file_name.lower().replace(" ", "_").replace(".", "")

					# Add file if root_folder_name key is not string
					if (
						root_folder_name in contents["dictionary"] and
						sub_sub_folder_name in contents["dictionary"][root_folder_name] and
						sub_sub_sub_folder_name in contents["dictionary"][root_folder_name][sub_sub_folder_name] and
						type(contents["dictionary"][root_folder_name][sub_sub_folder_name]) != str and
						type(contents["dictionary"][root_folder_name][sub_sub_folder_name][sub_sub_sub_folder_name]) != str
					):
						contents["dictionary"][root_folder_name][sub_sub_folder_name][sub_sub_sub_folder_name][file_name] = files[i]

					if os.path.isfile(files[i]) == True:
						contents["size"] += os.stat(files[i]).st_size

					i += 1

				contents["size"] += os.stat(root_folder).st_size

			# Root folder on dictionary if slash count of root folder is equal to folder plus four slash or equal to folder
			# Add sub-sub-sub-sub-folders
			if folder.count("/") + 4 == root_folder.count("/"):
				root_folder = self.Sanitize(root_folder)

				root_folder_name = root_folder.split("/")[-5]
				sub_sub_folder_name = root_folder.split("/")[-4]
				sub_sub_sub_folder_name = root_folder.split("/")[-3]
				sub_sub_sub_sub_folder_name = root_folder.split("/")[-2]

				if lower_key == True:
					root_folder_name = root_folder_name.lower().replace(" ", "_")
					sub_sub_folder_name = sub_sub_folder_name.lower().replace(" ", "_")
					sub_sub_sub_folder_name = sub_sub_sub_folder_name.lower().replace(" ", "_")
					sub_sub_sub_sub_folder_name = sub_sub_sub_sub_folder_name.lower().replace(" ", "_")

				# Add sub-sub-sub-folder to dictionary
				if (
					root_folder_name in contents["dictionary"] and
					sub_sub_folder_name in contents["dictionary"][root_folder_name] and
					sub_sub_sub_folder_name in contents["dictionary"][root_folder_name][sub_sub_folder_name]
				):
					contents["dictionary"][root_folder_name][sub_sub_folder_name][sub_sub_sub_folder_name][sub_sub_sub_sub_folder_name] = {}

					if "root" not in contents["dictionary"][root_folder_name][sub_sub_folder_name][sub_sub_sub_folder_name][sub_sub_sub_sub_folder_name]:
						contents["dictionary"][root_folder_name][sub_sub_folder_name][sub_sub_sub_folder_name][sub_sub_sub_sub_folder_name]["root"] = self.Sanitize(root_folder)

				# Add sub-sub-sub-sub-files to dictionary
				i = 0
				for file in files:
					file_name = files[i].split("/")[-1].split(".")[0]

					if (
						len(files[i].split(".")) not in [0, 1] and
						files[i].split("/")[-1].count(".") > 1
					):
						file_name = ""

						for item in files[i].split("/")[-1].split("."):
							if item != files[i].split("/")[-1].split(".")[-1]:
								file_name += item

								if item != files[i].split("/")[-1].split(".")[-2]:
									file_name += "."

					if lower_key == True:
						file_name = file_name.lower().replace(" ", "_").replace(".", "")

					# Add file if root_folder_name key is not string
					if (
						root_folder_name in contents["dictionary"] and
						sub_sub_folder_name in contents["dictionary"][root_folder_name] and
						sub_sub_sub_folder_name in contents["dictionary"][root_folder_name][sub_sub_folder_name]
					):
						contents["dictionary"][root_folder_name][sub_sub_folder_name][sub_sub_sub_folder_name][sub_sub_sub_sub_folder_name][file_name] = files[i]

					if os.path.isfile(files[i]) == True:
						contents["size"] += os.stat(files[i]).st_size

					i += 1

				contents["size"] += os.stat(root_folder).st_size

		for item in ["folder", "file"]:
			i = 0
			for key in contents[item]["names"]:
				key = key.split(".")[0]

				contents[item]["dictionary"][key] = contents[item]["list"][i]

				i += 1

		return contents
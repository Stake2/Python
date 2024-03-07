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

		folder_names = {
			"Program Files": "",
			"Program Files (x86)": "",
			"Apps": "",
			"Art": "",
			"Mega": "",
			"Media": "medias, title()",
			"Games": "",
			"XAMPP": ""
		}

		portuguese_folder_names = {
			"Art": self.JSON.Language.language_texts["art, title()"],
			"Media": self.JSON.Language.language_texts["medias, title()"],
			"Games": self.JSON.Language.language_texts["games, title()"]
		}

		# Define the language texts dictionary variable for easier typing
		language_texts = self.JSON.Language.language_texts

		# Iterate through the folder names dictionary
		for name in folder_names:
			# Get the key
			key = name.lower().replace(" ", "_").replace("(", "").replace(")", "")

			# Define the folder variable
			folder = name

			# Get the text key
			text_key = name.lower().replace(" ", "_")

			if "_" not in text_key:
				text_key += ", title()"

			if folder_names[name] != "":
				text_key = folder_names[name]

			# If the text key is inside the language texts dictionary
			if text_key in language_texts:
				# Define the folder as the language text
				folder = language_texts[text_key]

			self.folders["root"][key] = {
				"root": self.folders["root"]["root"] + folder + "/"
			}

			# Define the folder dictionary inside the root "Folders" dictionary
			self.folders[key] = {
				"root": self.folders["root"]["root"] + folder + "/"
			}

			# Define the folder dictionary inside the root "Folders" dictionary
			self.folders[name] = {
				"root": self.folders["root"]["root"] + folder + "/"
			}

		if "Media folder" in self.app_settings:
			self.folders["root"]["media"]["root"] = self.app_settings["Media folder"]
			self.folders["Media"]["root"] = self.app_settings["Media folder"]

		if "Game folder" in self.app_settings:
			self.folders["root"]["games"]["root"] = self.app_settings["Game folder"]
			self.folders["Games"]["root"] = self.app_settings["Game folder"]

		# "Program files (x86)" folders
		folder_names = [
			"Foobar2000"
		]

		for folder in folder_names:
			self.folders["Program Files (x86)"][folder] = {
				"root": self.folders["Program Files (x86)"]["root"] + folder + "/"
			}

		# "Apps" sub-folders
		folders = [
			"Module files",
			"Modules",
			"Shortcuts"
		]

		for folder in folders:
			key = folder.lower().replace(" ", "_")

			folder_backup = folder

			if folder == "Shortcuts":
				folder = self.JSON.Language.language_texts["shortcuts, title()"]

			self.folders["apps"][key] = {
				"root": os.path.join(self.folders["apps"]["root"], folder + "/")
			}

			self.folders["Apps"][folder_backup] = {
				"root": os.path.join(self.folders["apps"]["root"], folder + "/")
			}

		self.folders["apps"]["module_files"]["utility"] = {
			"root": self.folders["apps"]["module_files"]["root"] + "Utility/"
		}

		self.folders["apps"]["modules"]["modules"] = self.folders["apps"]["modules"]["root"] + "Modules.json"

		self.folders["apps"]["shortcuts"]["white_shortcuts"] = self.folders["apps"]["shortcuts"]["root"] + self.JSON.Language.language_texts["whites, title()"]

		self.folders["Apps"]["Shortcuts"]["White"] = self.folders["apps"]["shortcuts"]["root"] + self.JSON.Language.language_texts["whites, title()"]

		# Jogos (Games) folders
		folders = {
			"Shortcuts": self.JSON.Language.language_texts["shortcuts, title()"],
			"Folders": self.JSON.Language.language_texts["folders, title()"]
		}

		for key, folder in folders.items():
			self.folders["Games"][key] = {
				"root": self.folders["Games"]["root"] + folder + "/"
			}

		# User folders
		self.folders["user"] = {
			"root": self.Sanitize(self.folders["root"]["users"] + pathlib.Path.home().name + "/")
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

		for item in folders:
			key = item.lower().replace(" ", "_")

			self.folders["art"][key] = {
				"root": self.folders["art"]["root"] + item + "/"
			}

			self.folders["Art"][item] = {
				"root": self.folders["Art"]["root"] + item + "/"
			}

		# Art "Photoshop" subfolders
		folders = [
			"Ana",
			"Media",
			"Operational System",
			"PHP",
			"Render",
			"Stake2",
			"Stories",
			"Websites"
		]

		# Define the dictionary variable for easier typing
		dictionary = self.folders["Art"]["Photoshop"]

		# Iterate through the folders list
		for name in folders:
			# Define the folder name variable
			folder_name = name

			# Define the text key for the name of the folder
			text_key = name.lower().replace(" ", "_")

			if "_" not in text_key:
				text_key += ", title()"

			# If the key is present inside the language texts dictionary
			if text_key in language_texts:
				# Define the folder name variable as the folder name in the user language
				folder_name = language_texts[text_key]

			# Define the folder inside the dictionary
			dictionary[name] = {
				"root": dictionary["root"] + folder_name + "/"
			}

		# Art "Sony Vegas" subfolders
		folders = [
			"Render",
			"Story covers"
		]

		# Define the dictionary variable for easier typing
		dictionary = self.folders["Art"]["Sony Vegas"]

		# Iterate through the folders list
		for name in folders:
			# Define the folder name variable
			folder_name = name

			# Define the text key for the name of the folder
			text_key = name.lower().replace(" ", "_")

			if "_" not in text_key:
				text_key += ", title()"

			# If the key is present inside the language texts dictionary
			if text_key in language_texts:
				# Define the folder name variable as the folder name in the user language
				folder_name = language_texts[text_key]

			# Define the folder inside the dictionary
			dictionary[name] = {
				"root": dictionary["root"] + folder_name + "/"
			}

		# XAMPP folders and files
		self.folders["XAMPP"]["XAMPP Control"] = self.folders["root"]["xampp"]["root"] + "xampp-control.exe"

		# Mega sub-folders
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

				key = "Notepad"

			if key == "image":
				key = "Image"

			self.folders["Mega"][key] = {
				"root": self.folders["Mega"]["root"] + folder + "/"
			}

			self.folders["Mega"][folder] = {
				"root": self.folders["Mega"]["root"] + folder + "/"
			}

		# Mega "Image" dictionary
		self.folders["Image"] = self.folders["Mega"]["Image"]

		# Mega "Notepad" folders
		self.folders["Notepad"] = self.folders["Mega"]["Notepad"]

		# Mega "Notepad" folders
		folders = [
			"Diary",
			"Diary Slim",
			"Friends",
			"Social Networks",
			"Data Networks",
			"Years"
		]

		# Define the dictionary variable for easier typing
		dictionary = self.folders["Notepad"]

		# Iterate through the folders list
		for name in folders:
			# Define the folder name variable
			folder_name = name

			# Define the text key for the name of the folder
			text_key = name.lower().replace(" ", "_")

			if "_" not in text_key:
				text_key += ", title()"

			# If the key is present inside the language texts dictionary
			if text_key in language_texts:
				# Define the folder name variable as the folder name in the user language
				folder_name = language_texts[text_key]

			# Define the folder inside the dictionary
			dictionary[name] = {
				"root": dictionary["root"] + folder_name + "/"
			}

		# Mega "Notepad" Data Networks folders
		networks = {
			"Audiovisual Media": self.JSON.Language.language_texts["audiovisual_media"],
			"Database": self.JSON.Language.language_texts["database, title()"],
			"Games": self.JSON.Language.language_texts["games, title()"],
			"Productivity": self.JSON.Language.language_texts["productivity, title()"]
		}

		for network, folder in networks.items():
			# Network dictionary
			network = {
				"Title": network,
				"Information": "",
				"History": "",
				"Type": "Entry",
				"Entries": "Entries",
				"Subfolders": [
					"Data"
				]
			}

			dictionary = {
				"root": self.folders["Notepad"]["Data Networks"]["root"] + folder + "/"
			}			

			starting_year = 2023

			# "Audiovisual Media" network subfolders
			if network["Title"] == "Audiovisual Media":
				network["Subfolders"].append("Comments")

				network.update({
					"Information": "Media",
					"History": "Watch",
					"Type": "Media"
				})

				starting_year = 2018

			# "Database" network subfolders
			if network["Title"] == "Database":
				network.update({
					"Information": None,
					"History": None,
					"Type": None
				})

			# "Games" network subfolders
			if network["Title"] == "Games":
				network.update({
					"Information": None,
					"History": "Play",
					"Type": "Game",
					"Entries": "Sessions"
				})

				starting_year = 2021

			# "Productivity" network subfolders
			if network["Title"] == "Productivity":
				network.update({
					"History": "Task",
					"Type": "Task",
					"Entries": "Tasks"
				})

				starting_year = 2018

			# Network subfolder items
			for item in ["Information", "History"]:
				if network[item] != "":
					item_name = item

					if (
						item == "Information" and
						network["Title"] in ["Database", "Games"]
					):
						item_name = "Information"

					if (
						item == "Information" and
						network["Title"] == "Audiovisual Media"
					):
						item_name = "information"

					if network[item] != None:
						network[item] = network[item] + " " + item_name

					if network[item] == None:
						network[item] = item_name

					network["Subfolders"].append(network[item])

			for sub_folder in network["Subfolders"]:
				key = sub_folder

				text_key = sub_folder.lower().replace(" ", "_")

				if "_" not in text_key:
					text_key += ", title()"

				if (
					text_key in self.JSON.Language.language_texts and
					sub_folder in ["Media information", "Comments"]
				):
					sub_folder = self.JSON.Language.language_texts[text_key]

				dictionary[key] = {
					"root": dictionary["root"] + sub_folder + "/"
				}

			if network["Title"] == "Audiovisual Media":
				# "Audiovisual Media/Comments" folders
				for item in ["Backups"]:
					dictionary["Comments"][item] = {
						"root": dictionary["Comments"]["root"] + item + "/"
					}

				dictionary["Comments"]["Comments"] = dictionary["Comments"]["root"] + "Comments.json"

				# "Audiovisual Media/Watch History" folders
				for item in ["Movies"]:
					dictionary[network["History"]][item] = {
						"root": dictionary[network["History"]]["root"] + item + "/"
					}

			if network["Information"] != "":
				# Network "Information" folders and files
				for item in ["Information.json"]:
					key = item.replace(".json", "")

					dictionary[network["Information"]][key] = dictionary[network["Information"]]["root"] + item

			# Network "Data" folders and files
			for item in ["Types.json"]:
				key = item.replace(".json", "")

				dictionary["Data"][key] = dictionary["Data"]["root"] + item

			# "Network History" "History" file
			dictionary[network["History"]]["History"] = dictionary[network["History"]]["root"] + "History.json"

			# "Network History" year folders
			current_year = self.date["Units"]["Year"]

			if network["Type"] != None:
				network["Type"] = " " + network["Type"] + " "

			if network["Type"] == None:
				network["Type"] = " "

			for item in range(starting_year, current_year + 1):
				item = str(item)

				dictionary[network["History"]][item] = {
					"root": dictionary[network["History"]]["root"] + str(item) + "/"
				}

				# Per Type folder
				folder = "Per" + network["Type"] + "Type"

				dictionary[network["History"]][item][folder] = {
					"root": dictionary[network["History"]][item]["root"] + folder + "/"
				}

				# "Entries.json" file
				dictionary[network["History"]][item][network["Entries"]] = dictionary[network["History"]][item]["root"] + network["Entries"] + ".json"

				# "Entry list.txt" file
				dictionary[network["History"]][item]["Entry list"] = dictionary[network["History"]][item]["root"] + "Entry list.txt"

			# Define the Network "Folders" dictionary as the local "Folders" dictionary
			self.folders["Notepad"]["Data Networks"][network["Title"]] = dictionary

		# Mega "Notepad" Years folders
		starting_year = 2018
		current_year = self.date["Units"]["Year"]

		create_year_folders = False

		if create_year_folders == True:
			for item in range(starting_year, current_year + 1):
				key = str(item).lower().replace(" ", "_")

				self.folders["Notepad"]["Years"][key] = {
					"root": self.folders["Notepad"]["Years"]["root"] + str(item) + "/"
				}

				if key == str(self.date["Units"]["Year"]):
					# Per language years folder
					for language in self.languages["small"]:
						full_language = self.languages["full"][language]

						self.folders["Notepad"]["Years"][key][full_language] = {
							"root": self.folders["Notepad"]["Years"][key]["root"] + full_language + "/"
						}

					self.folders["Notepad"]["Years"]["current_year"] = self.folders["Notepad"]["Years"][key]

		# Mega "Image" folders
		folders = {
			"Christmas": self.JSON.Language.language_texts["christmas, title()"],
			"Friends": self.JSON.Language.language_texts["friends, title()"],
			"Social Networks": self.JSON.Language.language_texts["social_networks"],
			"Years": self.Date.language_texts["years, title()"]
		}

		for name, folder in folders.items():
			self.folders["Image"][name] = {
				"root": self.folders["Image"]["root"] + folder + "/"
			}

		# Mega Image Christmas folders
		folders = {
			"Theme": self.JSON.Language.language_texts["theme, title()"]
		}

		for name, folder in folders.items():
			self.folders["Image"]["Christmas"][name] = {
				"root": self.folders["Image"]["Christmas"]["root"] + folder + "/"
			}

		# Mega Image "Years" folders
		folders = {
			"Images": self.JSON.Language.language_texts["images, title()"]
		}

		for name, folder in folders.items():
			self.folders["Image"]["Years"][name] = {
				"root": self.folders["Image"]["Years"]["root"] + folder + "/"
			}

		# Mega "PHP" folders
		folders = [
			"JSON"
		]

		for item in folders:
			key = item.lower().replace(" ", "_")

			self.folders["Mega"]["php"][key] = {
				"root": self.folders["Mega"]["php"]["root"] + item + "/"
			}

			self.folders["Mega"]["PHP"][item] = {
				"root": self.folders["Mega"]["PHP"]["root"] + item + "/"
			}

		# Mega "PHP" JSON files
		files = [
			"Colors",
			"URL",
			"Websites"
		]

		for item in files:
			key = item.lower().replace(" ", "_")

			self.folders["Mega"]["php"]["json"][key] = self.folders["Mega"]["php"]["json"]["root"] + item + ".json"

			self.folders["Mega"]["PHP"]["JSON"][item] = self.folders["Mega"]["PHP"]["JSON"]["root"] + item + ".json"

		# Mega "Obsidian's Vaults" folders
		for item in ["Creativity"]:
			self.folders["Mega"]["Obsidian's Vaults"][item] = {
				"root": self.folders["Mega"]["Obsidian's Vaults"]["root"] + item + "/"
			}

		# Mega "Obsidian's Vaults" Creativity folders
		for item in ["Literature"]:
			self.folders["Mega"]["Obsidian's Vaults"]["Creativity"][item] = {
				"root": os.path.join(self.folders["Mega"]["Obsidian's Vaults"]["Creativity"]["root"], item + "/")
			}

		# Mega "Creativity" Literature folders
		for item in ["Stories"]:
			self.folders["Mega"]["Obsidian's Vaults"]["Creativity"]["Literature"][item] = {
				"root": os.path.join(self.folders["Mega"]["Obsidian's Vaults"]["Creativity"]["Literature"]["root"], item + "/")
			}

		# Mega Websites folders and files
		items = {
			"Folders": [
				"CSS",
				"Images"
			],
			"Files": [
				"Website"
			],
			"JSON": [
				"Website"
			]
		}

		# Create the folders
		for item in items["Folders"]:
			key = item.lower().replace(" ", "_")

			folder = self.folders["Mega"]["websites"]["root"] + item + "/"

			self.folders["Mega"]["websites"][key] = {
				"root": folder
			}

			self.folders["Mega"]["Websites"][item] = {
				"root": self.folders["Mega"]["Websites"]["root"] + item + "/"
			}

		# Create the files
		for item in items["Files"]:
			file = self.folders["Mega"]["websites"]["root"] + item + "."

			if item in items["JSON"]:
				file += "json"

			else:
				file += ".txt"

			self.folders["Mega"]["websites"][key] = file
			self.folders["Mega"]["Websites"][item] = file

		# "Colors.css" file inside the "CSS" folder
		self.folders["Mega"]["Websites"]["CSS"]["Colors"] = self.folders["Mega"]["Websites"]["CSS"]["root"] + "Colors.css"

		# Get the website subdomain
		self.website = {}
		self.links = {}

		if self.File.Exist(self.folders["Mega"]["Websites"]["Website"]) == True:
			self.website = self.JSON.To_Python(self.folders["Mega"]["Websites"]["Website"])

			# Create the "Links" dictionary with the Stake2 Website link
			self.links = {
				"Stake2 Website": "https://" + self.website["Sub-domain"] + "." + self.website["Netlify"] + "/"
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

			if (
				os.path.splitext(path)[-1] == "" and
				"/" not in path[-1]
			):
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
			self.Verbose(self.language_texts["it_was_not_possible_to_{}_the_folder_permission_not_granted"].format(self.language_texts["create"]) + "." + "\n\n\t" + self.language_texts["folder, title()"], folder)

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
						sub_sub_folder_name in contents["dictionary"][root_folder_name] and
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
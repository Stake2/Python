# Folder.py

import os
import Utility

class Folder():
	def __init__(self):
		# Import the classes
		self.Import_Classes()

		# Define the folders of the module
		Utility.Define_Folders(object = self)

		# Define the "Switches" dictionary
		self.Define_Switches()

		# Define the folders
		self.Define_Folders()

		# Define the texts of the module
		self.Define_Texts()

		# Create the folders
		self.Create_Folders()

	def Import_Classes(self):
		import importlib

		# ---------- #

		# Define the list of modules to be imported
		modules = [
			"Define_Folders",
			"Global_Switches",
			"JSON",
			"Date",
			"File"
		]

		# Iterate through the list of modules
		for module_title in modules:
			# Import the module
			module = importlib.import_module("." + module_title, "Utility")

			# Get the sub-class
			sub_class = getattr(module, module_title)

			# If the module title is not "Define_Folders"
			if module_title != "Define_Folders":
				# Add the sub-class to the current class
				setattr(self, module_title, sub_class())

			# If the module title is "Define_Folders"
			if module_title == "Define_Folders":
				# Add the sub-class to the "Utility" module
				setattr(Utility, "Define_Folders", sub_class)

		# ---------- #

		# Define the "Language" class as the same class inside the "JSON" class
		self.Language = self.JSON.Language

		# Import some variables from the "Language" class

		# Import the "languages" dictionary
		self.languages = self.Language.languages

		# Import the "user" dictionary
		self.user = self.Language.user

		# ---------- #

		# Get the current date from the "Date" class
		self.date = self.Date.date

	def Define_Switches(self):
		# Get the "Switches" dictionary from the "Global_Switches" module
		self.switches = self.Global_Switches.switches["Global"]

		# Update the "Switches" dictionary, adding the "Folder" dictionary
		self.switches.update({
			"Folder": {
				"Create": True,
				"Delete": True,
				"Copy": True,
				"Move": True
			}
		})

		# If the "Testing" switch is True
		if self.switches["Testing"] == True:
			# Iterate through the switches inside the "Folder" dictionary
			for switch in self.switches["Folder"]:
				# Define them as False
				self.switches["Folder"][switch] = False

	def Define_Folders(self):
		import platform
		import pathlib

		# Define the hard drive letter
		self.hard_drive_letter = os.path.normpath(pathlib.Path.home().drive) + "/"

		# ---------- #

		# Define the root folders

		# Define the folders dictionary with the root folders
		self.folders = {
			"root": self.hard_drive_letter,
			"Hard drive letter": self.hard_drive_letter
		}

		# ---------- #

		# System folders

		# Define the system folders
		folder_names = [
			"Users",
			"Program Files",
			"Program Files (x86)"
		]

		# Define the root folder to use
		root_folder = self.folders

		# Iterate through the list of folder names
		for folder_name in folder_names:
			# Define the key as the folder name
			key = folder_name

			# Define the folder dictionary inside the root "folders" dictionary
			root_folder[key] = {
				"root": root_folder["root"] + folder_name + "/"
			}

		# ---------- #

		# User folders

		# Define the user folder with the user name
		self.folders["User"] = {
			"root": self.folders["Users"]["root"] + self.user["Name"] + "/"
		}

		# Define the user folders
		folder_names = [
			"AppData",
			"Documents",
			"Pictures",
			"Videos",
			"Downloads"
		]

		# Define the root folder to use
		root_folder = self.folders["User"]

		# Iterate through the list of folder names
		for folder_name in folder_names:
			# Define the key as the folder name
			key = folder_name

			# Define the folder dictionary inside the root "folders" dictionary
			root_folder[key] = {
				"root": root_folder["root"] + folder_name + "/"
			}

		# ----- #

		# AppData folders

		# Define the AppData folders
		folder_names = [
			"Local",
			"LocalLow",
			"Roaming"
		]

		# Define the root folder to use
		root_folder = root_folder["AppData"]

		# Iterate through the list of folder names
		for folder_name in folder_names:
			# Define the key as the folder name
			key = folder_name

			# Define the folder dictionary inside the root "folders" dictionary
			root_folder[key] = {
				"root": root_folder["root"] + folder_name + "/"
			}

		# ---------- #

		# "Program files (x86)" folders

		# Define the "Program files (x86)" folders
		folder_names = [
			"Foobar2000"
		]

		# Define the root folder to use
		root_folder = self.folders["Program Files (x86)"]

		# Iterate through the list of folder names
		for folder_name in folder_names:
			# Define the folder dictionary with the root folder
			root_folder[folder_name] = {
				"root": root_folder["root"] + folder_name + "/"
			}

		# Define the "Foobar2000" files
		file_names = [
			"Foobar2000"
		]

		# Define the root folder to use
		root_folder = root_folder["Foobar2000"]

		# Iterate through the list of file names
		for file_name in file_names:
			# Define the file inside the "Foobar2000" folder
			root_folder[file_name] = root_folder["root"] + file_name.lower() + ".exe"

		# ---------- #

		# Folders that Python modules use

		# Define the root folders
		folder_names = [
			"Python",
			"Media",
			"Games",
			"XAMPP",
			"Mega"
		]

		# Define the root folder to use
		root_folder = self.folders

		# Iterate through the list of folder names
		for folder_name in folder_names:
			# Define the key as the folder name
			key = folder_name

			# Define the text key as an empty one
			text_key = ""

			# If the folder name is "Media"
			if folder_name == "Media":
				# Define the text key as "Media" (plural)
				text_key = "media, title(), type: plural"

			# Define the folder name
			folder_name = self.Language.Define_Folder_Name(folder_name, text_key = text_key)

			# Define the folder dictionary inside the root "folders" dictionary
			root_folder[key] = {
				"root": root_folder["root"] + folder_name + "/"
			}

		# ---------- #

		# Python folders

		# Define the Python folders
		folder_names = [
			"Modules",
			"Files",
			"Shortcuts"
		]

		# Define the root folder to use
		root_folder = self.folders["Python"]

		# Iterate through the list of folder names
		for folder_name in folder_names:
			# Define the key as the folder name
			key = folder_name

			# If the key is "Shortcuts"
			if key == "Shortcuts":
				# Change the folder name to its user language variant
				folder_name = self.Language.language_texts["shortcuts, title()"]

			# Define the folder dictionary with the root folder
			root_folder[key] = {
				"root": root_folder["root"] + folder_name + "/"
			}

		# ----- #

		# Utility module folders

		# Remove the "Shortcuts" folder from the local list of folder names
		folder_names.remove("Shortcuts")

		# Iterate through the list of folder names
		for folder_name in folder_names:
			# Define the "Utility" folder inside that folder
			root_folder[folder_name]["Utility"] = {
				"root": root_folder[folder_name]["root"] + "Utility/"
			}

		# ----- #

		# Modules files

		# Define the Modules files
		file_names = [
			"Modules"
		]

		# Define the root folder to use
		root_folder = root_folder["Modules"]

		# Iterate through the list of file names
		for file_name in file_names:
			# Define the file inside the root folder
			root_folder[file_name] = root_folder["root"] + file_name + ".json"

		# ----- #

		# Shortcuts folder

		# Define the Shortcuts folders
		folder_names = {
			"White": "Whites"
		}

		# Define the root folder to use
		root_folder = self.folders["Python"]["Shortcuts"]

		# Iterate through the dictionary of folder names and text keys
		for folder_name, text_key in folder_names.items():
			# Define the key as the folder name
			key = folder_name

			# Define the folder name
			folder_name = self.Language.Define_Folder_Name(text_key)

			# Define the folder dictionary with the root folder
			root_folder[key] = {
				"root": root_folder["root"] + folder_name + "/"
			}

		# ---------- #

		# Games folders

		# Define the Games folders
		folder_names = [
			"Shortcuts",
			"Folders"
		]

		# Define the root folder to use
		root_folder = self.folders["Games"]

		# Iterate through the list of folder names
		for folder_name in folder_names:
			# Define the key as the folder name
			key = folder_name

			# Define the folder name
			folder_name = self.Language.Define_Folder_Name(folder_name)

			# Define the folder dictionary with the root folder
			root_folder[key] = {
				"root": root_folder["root"] + folder_name + "/"
			}

		# ---------- #

		# XAMPP files

		# Define the XAMPP files
		file_names = [
			"XAMPP Control"
		]

		# Define the root folder to use
		root_folder = self.folders["XAMPP"]

		# Iterate through the list of file names
		for file_name in file_names:
			# Define the file inside the root folder
			root_folder[file_name] = root_folder["root"] + file_name.lower().replace(" ", "-") + ".exe"

		# ---------- #

		# Mega folders

		# Define the Mega folders
		folder_names = [
			"Notepad",
			"Images",
			"PHP",
			"Websites",
			"Stories"
		]

		# Define the root folder to use
		root_folder = self.folders

		# Iterate through the list of folder names
		for folder_name in folder_names:
			# Define the key as the folder name
			key = folder_name

			# Define the folder name
			folder_name = self.Language.Define_Folder_Name(folder_name)

			# Define the folder dictionary with the root folder
			root_folder[key] = {
				"root": self.folders["Mega"]["root"] + folder_name + "/"
			}

		# ---------- #

		# Notepad folders

		# Define the Notepad folders
		folder_names = [
			"Diary",
			"Diary Slim",
			"Friends",
			"Social networks",
			"Data Networks",
			"Years"
		]

		# Define the root folder to use
		root_folder = self.folders["Notepad"]

		# Iterate through the list of folder names
		for folder_name in folder_names:
			# Define the key as the folder name
			key = folder_name

			# Define the folder name
			folder_name = self.Language.Define_Folder_Name(folder_name)

			# Define the folder dictionary with the root folder
			root_folder[key] = {
				"root": root_folder["root"] + folder_name + "/"
			}

		# ----- #

		# Data Networks folders

		# Define the Data Network folders
		folder_names = [
			"Productivity",
			"Audiovisual Media",
			"Games",
			"Database"
		]

		# Define the root folder to use
		root_folder = self.folders["Notepad"]["Data Networks"]

		# Iterate through the list of folder names
		for folder_name in folder_names:
			# Define the key as the folder name
			key = folder_name

			# Define the folder name
			folder_name = self.Language.Define_Folder_Name(folder_name)

			# Define the folder dictionary with the root folder
			root_folder[key] = {
				"root": root_folder["root"] + folder_name + "/"
			}

		# ----- #

		# Temporary code:
		# <!--

		# Define the dictionary of data networks
		networks = {
			"Database": self.Language.language_texts["database, title()"],
			"Games": self.Language.language_texts["games, title()"],
			"Productivity": self.Language.language_texts["productivity, title()"]
		}

		for network, folder in networks.items():
			# Define the default network information
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

			# Define the default network dictionary
			dictionary = {
				"root": self.folders["Notepad"]["Data Networks"]["root"] + folder + "/"
			}			

			# Define the default network starting year
			starting_year = 2023

			# Define the "Database" network information
			if network["Title"] == "Database":
				# Add some name information
				network.update({
					"Information": None,
					"History": None,
					"Type": None
				})

			# Define the "Games" network information
			if network["Title"] == "Games":
				# Add some name information
				network.update({
					"Information": "Game",
					"Lowercase information": True,
					"History": "Play",
					"Type": "Game",
					"Entries": "Sessions"
				})

				# Define the starting year as 2021
				starting_year = 2021

			# Define the "Productivity" network information
			if network["Title"] == "Productivity":
				# Remove the "Data" folder from the list of sub-folders
				network["Subfolders"].remove("Data")

				# Add some name information
				network.update({
					"History": "Task",
					"Type": "Task",
					"Entries": "Tasks"
				})

				# Define the starting year as 2018
				starting_year = 2018

			# Define the network sub-folder items
			for item in ["Information", "History"]:
				# If the sub-folder item is not empty
				if network[item] != "":
					# Define the item name as the item
					item_name = item

					# If the item is "Information"
					if item == "Information":
						# If the "Lowercase information" key is not in the network dictionary
						if "Lowercase information" not in network:
							# Define the item name as "Information"
							item_name = "Information"

						# If the "Lowercase information" key is in the network dictionary
						# And it is True
						if (
							"Lowercase information" in network and
							network["Lowercase information"] == True
						):
							# Define the item name as "information" (lowercase)
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

				if text_key in self.Language.language_texts:
					sub_folder = self.Language.language_texts[text_key]

				dictionary[key] = {
					"root": dictionary["root"] + sub_folder + "/"
				}

			if network["Information"] != "":
				# Network "Information" folders and files
				for item in ["Information.json"]:
					key = item.replace(".json", "")

					dictionary[network["Information"]][key] = dictionary[network["Information"]]["root"] + item

			# If the network is not the "Productivity" one
			if network["Title"] != "Productivity":
				# Define the network "Data" folders and files
				for item in ["Types.json"]:
					key = item.replace(".json", "")

					dictionary["Data"][key] = dictionary["Data"]["root"] + item

			# "Network History" "History" file
			dictionary[network["History"]]["History"] = dictionary[network["History"]]["root"] + "History.json"

			# "Network History" year folders
			current_year = self.date["Units"]["Year"]

			if network["Type"] != None:
				network["Type"] = " " + network["Type"].lower() + " "

			if network["Type"] == None:
				network["Type"] = " "

			for item in range(starting_year, current_year + 1):
				item = str(item)

				dictionary[network["History"]][item] = {
					"root": dictionary[network["History"]]["root"] + str(item) + "/"
				}

				# Define the by type folder
				folder = "By" + network["Type"] + "type"

				dictionary[network["History"]][item][folder] = {
					"root": dictionary[network["History"]][item]["root"] + folder + "/"
				}

				# "Entries.json" file
				dictionary[network["History"]][item][network["Entries"]] = dictionary[network["History"]][item]["root"] + network["Entries"] + ".json"

				# "Entry list.txt" file
				dictionary[network["History"]][item]["Entry list"] = dictionary[network["History"]][item]["root"] + "Entry list.txt"

			# Define the Network folders dictionary as the local folders dictionary
			self.folders["Notepad"]["Data Networks"][network["Title"]] = dictionary

		# End of Temporary code
		# -->

		# ---------- #

		# Define the list of folders inside the the Mega "Image" folder
		folders = [
			"Christmas",
			"Diary",
			"Friends",
			"Social networks",
			"Years"
		]

		# Define the root folder as the Mega "Image" folder
		root_folder = self.folders["Images"]

		# Iterate through the local list of folder keys
		for key in folders:
			# Create the text key by converting the key into lowercase and replacing spaces with underscores
			text_key = key.lower().replace(" ", "_")

			# If the underscore character is not inside the text key
			if "_" not in text_key:
				# Add the ", title()" text
				text_key += ", title()"

			# Get the folder name in the user language
			folder_name = self.Language.language_texts[text_key]

			# Define the folder inside the root folder dictionary
			root_folder[key] = {
				"root": root_folder["root"] + folder_name + "/"
			}

		# ----- #

		# Define the Mega image "Christmas" sub-folders
		folders = [
			"Images",
			"Theme"
		]

		# Define the root folder as the "Christmas" image folder
		root_folder = self.folders["Images"]["Christmas"]

		# Iterate through the local list of folder keys
		for key in folders:
			# Define the text key for the key
			text_key = key.lower() + ", title()"

			# Define the user language folder name using the text key
			folder_name = self.Language.language_texts[text_key]

			# Define the folder (the root folder plus the folder name)
			folder = root_folder["root"] + folder_name + "/"

			# Add the folder to the root folder dictionary with the key
			root_folder[key] = {
				"root": folder
			}

		# --- #

		# Define the Mega image Christmas "Theme" files
		files = [
			"Christmas"
		]

		# Define the list of file extensions to use
		file_extensions = [
			"theme",
			"lnk",
			"bat"
		]

		# Define the root folder as the Christmas "Theme" folder
		root_folder = self.folders["Images"]["Christmas"]["Theme"]

		# Iterate through the list of file keys
		for key in files:
			# Define the text key for the key
			text_key = key.lower() + ", title()"

			# Define the user language file name using the text key
			file_name = self.Language.language_texts[text_key]

			# Iterate through the file extensions
			for file_extension in file_extensions:
				# Define the file (the root folder plus the file name and the file extension)
				file = root_folder["root"] + file_name + "." + file_extension

				# Define the new key as the original key plus the file extension
				new_key = key + "." + file_extension

				# Add the file to the root folder dictionary with the new key
				root_folder[new_key] = file

		# ----- #

		# Define the list of folders inside the the "Social networks" folder of the Mega "Image" folder
		folders = [
			"Digital identities"
		]

		# Define the root folder as the "Social networks" folder of the Mega "Image" folder
		root_folder = self.folders["Images"]["Social networks"]

		# Iterate through the local list of folder keys
		for key in folders:
			# Create the text key by converting the key into lowercase and replacing spaces with underscores
			text_key = key.lower().replace(" ", "_")

			# If the underscore character is not inside the text key
			if "_" not in text_key:
				# Add the ", title()" text
				text_key += ", title()"

			# Get the folder name in the user language
			folder_name = self.Language.language_texts[text_key]

			# Define the folder inside the root folder dictionary
			root_folder[key] = {
				"root": root_folder["root"] + folder_name + "/"
			}

		# ----- #

		# Mega Image "Years" folders
		folders = {
			"Images": self.Language.language_texts["images, title()"]
		}

		for key, folder in folders.items():
			self.folders["Images"]["Years"][key] = {
				"root": self.folders["Images"]["Years"]["root"] + folder + "/"
			}

		# Mega "PHP" folders
		folders = [
			"JSON"
		]

		for item in folders:
			key = item.lower().replace(" ", "_")

			folder = self.folders["PHP"]["root"] + item + "/"

			self.folders["PHP"][item] = {
				"root": folder
			}

		# Mega "PHP" JSON files
		files = [
			"Colors",
			"URL",
			"Websites"
		]

		for item in files:
			key = item.lower().replace(" ", "_")

			self.folders["PHP"]["JSON"][item] = self.folders["PHP"]["JSON"]["root"] + item + ".json"

		# Define the Mega "Websites" folders and files
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

			self.folders["Websites"][item] = {
				"root": self.folders["Websites"]["root"] + item + "/"
			}

		# Create the files
		for item in items["Files"]:
			file = self.folders["Websites"]["root"] + item + "."

			if item in items["JSON"]:
				file += "json"

			else:
				file += ".txt"

			self.folders["Websites"][item] = file

		# Define the "Colors.css" file inside the "CSS" folder
		self.folders["Websites"]["CSS"]["Colors"] = self.folders["Websites"]["CSS"]["root"] + "Colors.css"

		# ---------- #

		# Stories folders

		# Define the Stories folders
		folders = {
			"Game Multiverse Bubble": self.Language.language_texts["game_multiverse_bubble"]
		}

		for key, folder in folders.items():
			self.folders["Stories"][key] = {
				"root": self.folders["Stories"]["root"] + folder + "/"
			}

	def Define_Texts(self):
		# Define the "Texts" dictionary
		self.texts = self.JSON.To_Python(self.module["Files"]["Texts"])

		# Define the "Language texts" dictionary
		self.language_texts = self.Language.Item(self.texts)

	def Capitalize(self, text, lower = False):
		text = list(text)

		if lower == False:
			text[0] = text[0].upper()

		if lower == True:
			text[0] = text[0].lower()

		text = "".join(text)

		return text

	def Sanitize(self, path, restricted_characters = False):
		# If the "restricted characters" parameter is False
		if restricted_characters == False:
			# Normalize the path and replace backslashes with forward slashes
			path = os.path.normpath(path).replace("\\", "/")

			# Add a slash at the end of the path if it is not present
			if (
				os.path.splitext(path)[-1] == "" and
				"/" not in path[-1]
			):
				path += "/"

		# If the "restricted characters" parameter is True
		if restricted_characters == True:
			# Remove the restricted characters
			path = self.Remove_Restricted_Characters(path)

		# Return the path
		return path

	def Remove_Restricted_Characters(self, path):
		# Define the list of restricted characters
		restricted_characters = [
			":",
			"?",
			'"',
			"\\",
			"/",
			"|",
			"｜",
			"*",
			"<",
			">"
		]

		# Iterate through the list of characters
		for character in restricted_characters:
			# Remove the character if it exists
			path = path.replace(character, "")

		# Remove leading and trailing spaces
		path = path.strip()

		# Replace multiple spaces with a single space
		path = " ".join(path.split())

		# Return the path
		return path

	def Split(self, path):
		return os.path.split(path)

	def Verbose(self, text, item, verbose = False):
		if (
			self.switches["Verbose"] == True or
			verbose == True
		):
			import inspect

			print()
			print(self.module["Name"] + "." + inspect.stack()[1][3] + "():")
			print("\t" + text + ":")
			print("\t" + item)

	def Current(self, file = None):
		# If the file parameter is None, define the file as "__file__"
		if file == None:
			file = __file__

		# Get the folder from the module file
		folder = self.Sanitize(os.path.dirname(file))

		# Return the folder
		return folder

	def Exists(self, folder):
		# Sanitize the folder path
		folder = self.Sanitize(folder)

		# Checks if the folder exists and returns True if it does or False if it does not
		return os.path.isdir(folder)

	def File_Exists(self, file):
		# Sanitize the file path
		file = self.Sanitize(file)

		# Checks if the file exists and returns True if it does or False if it does not
		return os.path.isfile(file)

	def Type(self, text = None):
		if text == None:
			text = self.language_texts["type_or_paste_the_folder"] + ": "

		print()

		return input(text)

	def Create(self, folder = None, text = None):
		if folder == None:
			folder = self.Type(text)

		folder = self.Sanitize(folder)

		if self.Exists(folder) == True:
			return False

		if (
			self.switches["Folder"]["Create"] == True and
			self.Exists(folder) == False
		):
			os.mkdir(folder)

			self.Verbose(self.language_texts["folder"].title() + " " + self.Language.language_texts["created"], folder)

			return True

		else:
			self.Verbose(self.language_texts["it_was_not_possible_to_{}_the_folder_permission_not_granted"].format(self.Language.language_texts["create"]) + "." + "\n\n\t" + self.language_texts["folder, title()"], folder)

			return False

	def Create_Folders(self, folders = None, depth = 0):
		if folders == None:
			folders = self.folders

		for value in folders.values():
			if type(value) != dict:
				if (
					self.File_Exists(value) == False and
					"." not in value
				):
					self.Create(value)

				if (
					self.File_Exists(value) == False and
					"." in value
				):
					self.File.Create(value)

			if type(value) == dict:
				found = self.Create_Folders(value, depth = depth + 1)

	def Delete(self, folder):
		if folder == None:
			folder = self.Type()

		folder = self.Sanitize(folder)

		if self.Exists(folder) == False:
			self.Verbose(self.language_texts["this_folder_does_not_exists"], folder)

			return False

		if (
			self.switches["Folder"]["Delete"] == True and
			self.Exists(folder) == True
		):
			try:
				# Folder is empty
				os.rmdir(folder)

			except OSError:
				import shutil

				# Folder is not empty
				shutil.rmtree(folder)

			self.Verbose(self.language_texts["folder"].title() + " " + self.Language.language_texts["deleted, feminine"], folder)

			return True

		else:
			self.Verbose(self.language_texts["it_was_not_possible_to_{}_the_folder_permission_not_granted"].format(self.Language.language_texts["delete"]), folder, verbose = True)

			return False

	def Copy(self, source_folder = None, destination_folder = None):
		if source_folder == None:
			source_folder = self.Type()

		if destination_folder == None:
			destination_folder = self.Type()

		source_folder = self.Sanitize(source_folder)
		destination_folder = self.Sanitize(destination_folder)

		if self.Exists(source_folder) == False:
			self.Verbose(self.language_texts["this_folder_does_not_exists"], source_folder)

			return False

		if (
			self.switches["Folder"]["Copy"] == True and
			self.Exists(source_folder) == True
		):
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

		if self.Exists(source_folder) == False:
			self.Verbose(self.language_texts["this_folder_does_not_exists"], source_folder)

			return False

		if (
			self.switches["Folder"]["Move"] == True and
			self.Exists(source_folder) == True
		):
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

			if self.Exists(item) == True:
				if name not in self.contents["folder"]["names"]:
					self.contents["folder"]["names"].append(name)

				if item not in self.contents["folder"]["list"]:
					self.contents["folder"]["list"].append(item)

				defined_contents = contents["folders"]

				if folder_name not in defined_contents:
					defined_contents[folder_name] = {}

				defined_contents[folder_name]["root"] = self.Sanitize(item)

			if self.File_Exists(item) == True:
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
			if self.File_Exists(self.Sanitize(folder + item)) == True:
				self.contents["root_folders"].remove(item)

		if self.Exists(folder) == True:
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
								if self.Exists(value) == True:
									self.contents["folders"][local_folder][key] = value

							if type(value) == dict:
								for sub_key in value:
									sub_value = value[sub_key]

									if self.File_Exists(sub_value) == True:
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

		if self.Exists(folder) == False:
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
			# Add sub-folders
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

					if self.File_Exists(files[i]) == True:
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

					if self.File_Exists(files[i]) == True:
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

					if self.File_Exists(files[i]) == True:
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

					if self.File_Exists(files[i]) == True:
						contents["size"] += os.stat(files[i]).st_size

					i += 1

				contents["size"] += os.stat(root_folder).st_size

		for item in ["folder", "file"]:
			i = 0
			for key in contents[item]["names"]:
				key = key.split(".")[0]

				contents[item]["dictionary"][key] = contents[item]["list"][i]

				i += 1

		# Update the folder and file keys to uppercase
		for key in ["Folder", "File"]:
			# Create the uppercase key
			contents[key] = {}

			# Iterate through the uppercase sub-keys
			for sub_key in ["List", "Names", "Dictionary"]:
				# Create the uppercase sub-key
				contents[key][sub_key] = contents[key.lower()][sub_key.lower()]

		return contents
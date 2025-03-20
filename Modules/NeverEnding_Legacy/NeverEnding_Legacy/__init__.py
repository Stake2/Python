# NeverEnding_Legacy.py

# Import the "importlib" module
import importlib

from copy import deepcopy

class NeverEnding_Legacy(object):
	def __init__(self, select_year = False, create_current_year = True):
		# Import the classes
		self.Import_Classes()

		# Define the folders of the module
		self.folders = self.Define_Folders(object = self).folders

		# Module related methods
		self.Define_Basic_Variables()
		self.Define_Texts()

		# Define the folders and files of the class
		self.Define_Folders_And_Files()

		# Define the dictionaries of the class
		self.Define_Dictionaries()

		# Define the mod authors
		self.Define_Authors()

		# Update the "Mods.json" and "Authors.json" files with their respective dictionaries
		self.Update_Files()

	def Import_Classes(self):
		# Define the list of modules to be imported
		modules = [
			"Define_Folders",
			"JSON"
		]

		# Iterate through the list of modules
		for module_title in modules:
			# Import the module
			module = importlib.import_module("." + module_title, "Utility")

			# Get the sub-class
			sub_class = getattr(module, module_title)

			# If the module title is not "Define_Folders"
			if module_title != "Define_Folders":
				# Run the sub-class to define its variable
				sub_class = sub_class()

			# Add the sub-class to the current module
			setattr(self, module_title, sub_class)

		# Define the "Language" class as the same class inside the "JSON" class
		self.Language = self.JSON.Language

	def Define_Basic_Variables(self):
		# Get the modules list
		self.modules = self.JSON.To_Python(self.folders["Apps"]["Modules"]["Modules"])

		# Create a list of the modules that will not be imported
		remove_list = [
			"Define_Folders",
			"Modules",
			"Language",
			"JSON"
		]

		# Iterate through the Utility modules
		for module_title in self.modules["Utility"]["List"]:
			# If the module title is not inside the remove list
			if module_title not in remove_list:
				# Import the module
				module = importlib.import_module("." + module_title, "Utility")

				# Get the sub-class
				sub_class = getattr(module, module_title)

				# Add the sub-class to the current module
				setattr(self, module_title, sub_class())

		# Get the switches dictionary from the "Global Switches" module
		self.switches = self.Global_Switches.switches["Global"]

		# Get the Languages dictionary
		self.languages = self.Language.languages

		# Get the user language and full user language
		self.user_language = self.Language.user_language
		self.full_user_language = self.Language.full_user_language

		# Define the local "folders" dictionary as the dictionary inside the "Folder" class
		self.folders = self.Folder.folders

		# Get the Sanitize method of the File class
		self.Sanitize = self.File.Sanitize

		# Get the current date from the Date module
		self.date = self.Date.date

	def Define_Texts(self):
		# Define the "Separators" dictionary
		self.separators = {}

		# Create separators from one to ten characters
		for number in range(1, 21):
			# Define the empty string
			string = ""

			# Add separators to it
			while len(string) != number:
				string += "-"

			# Add the string to the Separators dictionary
			self.separators[str(number)] = string

		# Define the "Texts" dictionary
		self.texts = self.JSON.To_Python(self.module["Files"]["Texts"])

		# Define the "Language texts" dictionary
		self.language_texts = self.Language.Item(self.texts)

	def Define_Folders_And_Files(self):
		# Define the root folder as the games folder
		folder = self.folders["Games"]["root"]

		# Get the "Folders" folder
		folder = folder + self.Folder.language_texts["folders, title()"] + "/"

		# Define and create the game folder
		folder = folder + "NeverEnding Legacy/"
		self.Folder.Create(folder)

		# ---------- #

		# Define the "NeverEnding_Legacy" dictionary with the "Folders" key
		self.neverending_legacy = {
			"Folders": {
				"root": folder
			},
			"Authors": {},
			"Mods": {},
			"Github": {
				"Repository": "https://github.com/Stake2/NeverEnding_Legacy/",
				"Raw Github user content": "https://raw.githubusercontent.com/Stake2/NeverEnding_Legacy/refs/heads/main/Mods/"
			}
		}

		# ---------- #

		# Define and create the mods folder
		self.neverending_legacy["Folders"]["Mods"] = {
			"root": self.neverending_legacy["Folders"]["root"] + "Mods/"
		}

		self.Folder.Create(self.neverending_legacy["Folders"]["Mods"]["root"])

		# Define and create the "Authors.json" file
		self.neverending_legacy["Folders"]["Mods"]["Authors"] = self.neverending_legacy["Folders"]["Mods"]["root"] + "Authors.json"
		self.File.Create(self.neverending_legacy["Folders"]["Mods"]["Authors"])

		# Define and create the "Mods.json" file
		self.neverending_legacy["Folders"]["Mods"]["Mods"] = self.neverending_legacy["Folders"]["Mods"]["root"] + "Mods.json"
		self.File.Create(self.neverending_legacy["Folders"]["Mods"]["Mods"])

		# Define and create the "Lists.txt" file
		self.neverending_legacy["Folders"]["Mods"]["Lists"] = self.neverending_legacy["Folders"]["Mods"]["root"] + "Lists.txt"
		self.File.Create(self.neverending_legacy["Folders"]["Mods"]["Lists"])

	def Define_Dictionaries(self):
		# Define a local mods dictionary
		mods = {
			"Numbers": {
				"Total": 0,
				"Per category": {}
			},
			"Categories": {},
			"List": [],
			"Dictionary": {}
		}

		# ---------- #

		# Define the mod categories
		mods["Categories"] = {
			"List": [
				"General mods",
				"Utility mods",
				"Overhaul mods"
			],
			"Dictionary": {}
		}

		# Iterate through the list of mod categories
		for category in mods["Categories"]["List"]:
			# Add the category number to the root "Per category" numbers dictionary
			mods["Numbers"]["Per category"][category] = 0

			# Create the empty mods list of the current category
			mods["Categories"]["Dictionary"][category] = []

		# ---------- #

		# Add the local mods dictionary to the root "Mods" key
		self.neverending_legacy["Mods"] = mods

	def Define_Authors(self):
		# Define a local authors dictionary
		authors = {
			"Numbers": {
				"Total": 0,
				"Mods": {
					"Total": 0,
					"Per category": {
						"General mods": 0,
						"Utility mods": 0,
						"Overhaul mods": 0
					}
				}
			},
			"List": [],
			"Dictionary": {}
		}

		# ---------- #

		# Iterate through the list of mod categories
		for category in self.neverending_legacy["Mods"]["Categories"]["List"]:
			# Add the category number to the root "Per category" numbers dictionary
			authors["Numbers"]["Mods"]["Per category"][category] = 0

		# ---------- #

		# Get the sub-folders of the "Mods" folder
		contents = self.Folder.Contents(self.neverending_legacy["Folders"]["Mods"]["root"])

		# Get the list of authors from the list of folders
		authors["List"] = contents["folder"]["names"]

		# Define a list to remove from the list of authors
		remove_list = [
			"Archive"
		]

		# Iterate through the list of items to remove
		for item in remove_list:
			# If the item is inside the list, remove it
			if item in authors["List"]:
				authors["List"].remove(item)

		# ---------- #

		# Iterate through the list of authors
		for author_name in authors["List"]:
			# Define the local author dictionary
			author = {
				"Name": author_name,
				"Folders": {
					"root": self.neverending_legacy["Folders"]["Mods"]["root"] + author_name + "/"
				},
				"Files": {},
				"Information": {}
			}

			# ----- #

			# Define the "Author.txt" file
			author["Files"]["Author"] = author["Folders"]["root"] + "Author.txt"
			self.File.Create(author["Files"]["Author"])

			# Get the file dictionary from the author file
			dictionary = self.File.Dictionary(author["Files"]["Author"], next_line = True)

			# ----- #

			# Define a list of information keys
			information_keys = [
				"Name",
				"Github",
				"Github repository",
				"Discord server",
				"Website"
			]

			# Define a list of social network keys
			social_network_keys = [
				"Bluesky",
				"Tumblr",
				"Patreon",
				"Pixel Joint",
				"Filter Forge"
			]

			# ----- #

			# Iterate through the keys and values inside the dictionary
			for key, information in dictionary.items():
				# If the key is inside the list of information keys
				if key in information_keys:
					# Add the information to the "Information" dictionary
					author["Information"][key] = information

				# If the key is inside the list of social network keys
				if key in social_network_keys:
					# Create the "Social networks" key if it is not present
					if "Social networks" not in author["Information"]:
						author["Information"]["Social networks"] = {}

					# Add the social network to the dictionary
					author["Information"]["Social networks"][key] = information

			# ----- #

			# Define a local "Archive.txt" file
			archive_file = author["Folders"]["root"] + "Archive.txt"

			# If the file exists
			if self.File.Exist(archive_file) == True:
				# Define the "Archive" dictionary using the archive file
				author = self.Define_Archive(author, archive_file)

			# ----- #

			# Get the mod folders from the author folder
			contents = self.Folder.Contents(author["Folders"]["root"])

			# Define a list of folders to remove from the list of mods of the author
			remove_list = [
				"Github repository files",
				"Website"
			]

			# Iterate through the list of folders to remove
			for folder in remove_list:
				# If the folder is inside the list of folder names, remove it
				if folder in contents["folder"]["names"]:
					contents["folder"]["names"].remove(folder)

			# Define the mods dictionary and set its initial keys, defining the "List" key as the list of mod folders above
			mods = {
				"Numbers": {
					"Total": 0
				},
				"List": contents["folder"]["names"],
				"Dictionary": {}
			}

			# Iterate through the list of mods inside the author folder
			for mod_title in mods["List"]:
				# If the "Github" key is inside the author information dictionary
				if "Github" in author["Information"]:
					# Define the Github link as the author link
					link = author["Information"]["Github"]

				# Else, define it as the website link
				else:
					link = author["Information"]["Website"]

				# Define the local mod dictionary
				mod = {
					"Title": mod_title,
					"Author": {
						"Name": author_name,
						"Link": link
					},
					"Folders": {
						"root": author["Folders"]["root"] + mod_title + "/"
					},
					"Files": {},
					"Information": {}
				}

				# ----- #

				# Define and create the "Files" folder
				mod["Folders"]["Files"] = {
					"root": mod["Folders"]["root"] + "Files/"
				}

				self.Folder.Create(mod["Folders"]["Files"]["root"])

				# ----- #

				# Define a local mod "Information.txt" file
				information_file = mod["Folders"]["root"] + "Information.txt"

				# Define an empty dictionary as the default information dictionary
				dictionary = {}

				# If the file exists
				if self.File.Exist(information_file) == True:
					# Get the file dictionary from the information file
					dictionary = self.File.Dictionary(information_file, next_line = True)

					# Define the list of keys to look for
					keys = [
						"Website",
						"Github repository",
						"Fandom",
						"Discord server",
						"Mod category",
						"Original mod",
						"Fixed mod",
						"jsDelivr",
						"jsDelivr repository",
						"FileGarden"
					]

					# Define the list of duplicate keys
					duplicate_keys = [
						"Website",
						"Github repository",
					]

					# Define the list of splittable keys
					splittable_keys = [
						"jsDelivr",
						"FileGarden"
					]

					# Iterate through the list of keys
					for key in keys.copy():
						# If the key is not inside the file dictionary
						if key not in dictionary:
							# Remove the key from the local list of keys
							keys.remove(key)

					# Iterate through the list of keys
					for key in keys:
						# If the key is not inside the list of duplicate keys
						# Or it is, and the key is inside the author "Information" dictionary
						# And the the mod information is not the same as the author information
						if (
							key not in duplicate_keys or
							key in duplicate_keys and
							key in author["Information"] and
							dictionary[key] != author["Information"][key]
						):
							# If the key is inside the list of splittable keys
							if key in splittable_keys:
								# Split the information value into a Python list
								dictionary[key] = dictionary[key].split(", ")

							# Add the mod information key to the "Information" dictionary
							mod["Information"][key] = dictionary[key]

					# Define the file inside the "Files" dictionary
					mod["Files"]["Information"] = information_file

				# Define a local mod "Archive.txt" file
				archive_file = mod["Folders"]["root"] + "Archive.txt"

				# If the file exists
				if self.File.Exist(archive_file) == True:
					# Define the "Archive" dictionary using the archive file
					mod = self.Define_Archive(mod, archive_file)

				# ----- #

				# Define the "JavaScript files.txt" file
				mod["Files"]["JavaScript files"] = mod["Folders"]["root"] + "JavaScript files.txt"

				# Get the file lines from the JavaScript file
				files = self.File.Contents(mod["Files"]["JavaScript files"])["lines"]

				# Add them to the "JavaScript files" key
				mod["JavaScript files"] = files

				# ----- #

				# Define a local "Additional files.txt" file
				additional_files_file = mod["Folders"]["root"] + "Additional files.txt"

				# If the file exists
				if self.File.Exist(additional_files_file) == True:
					# Get the file lines from the additional files file
					files = self.File.Contents(additional_files_file)["lines"]

					# Define the empty "Additional files" dictionary
					mod["Additional files"] = {}

					# Iterate through the list of files
					for file in files:
						# Get the file name
						file_name = self.File.Name(file)

						# Add the file to the "Additional files" dictionary using the file name as a key
						mod["Additional files"][file_name] = file

					# Define the file inside the "Files" dictionary
					mod["Files"]["Additional files"] = additional_files_file

				# ----- #

				# Define a shortcut for the key
				key = "Replaces data.js"

				# If the key is inside the dictionary
				if key in dictionary:
					# Define the value of the key as True or False
					value = self.Input.Define_Yes_Or_No(dictionary[key])

					dictionary[key] = value

				# Else, define it as False
				else:
					dictionary[key] = False

				# Add the "Replaces data.js" key to the root of the mod dictionary
				mod[key] = dictionary[key]

				# ----- #

				# Add the local mod dictionary to the root mod dictionary
				mods["Dictionary"][mod_title] = mod

				# ----- #

			# Update the number of mods
			mods["Numbers"]["Total"] = len(mods["List"])

			# Define the root "Mods" dictionary as the local mods dictionary
			author["Mods"] = mods

			# ----- #

			# Add the local author dictionary to the root authors dictionary
			authors["Dictionary"][author_name] = author

		# ---------- #

		# Update the number of authors inside the "Authors" dictionary
		authors["Numbers"]["Total"] = len(authors["List"])

		# Add the local authors dictionary to the root "Authors" key
		self.neverending_legacy["Authors"] = authors

	def Define_Archive(self, dictionary, archive_file):
		# Get the file dictionary from the archive file
		file_dictionary = self.File.Dictionary(archive_file, next_line = True)

		# Define the "Archive" dictionary
		# Importing the "Archive author", "Github", and "Github repository" keys from inside the local file dictionary
		dictionary["Archive"] = {
			"Archiver": {
				"Name": file_dictionary["Archive author"],
				"Profile": file_dictionary["Github"],
			},
			"Github repository": file_dictionary["Github repository"]
		}

		# If the "Github.io" key is inside the file dictionary
		if "Github.io" in file_dictionary:
			# Add the key to the local "Archiver" dictionary
			dictionary["Archive"]["Archiver"]["Github.io"] = file_dictionary["Github.io"]

		# Define the file inside the "Files" dictionary
		dictionary["Files"]["Archive"] = archive_file

		# Return the information dictionary
		return dictionary

	def Update_Files(self):
		# Define a shortcut for the root "Authors" dictionary
		authors = self.neverending_legacy["Authors"]

		# Define a shortcut for the root "Mods" dictionary
		mods = self.neverending_legacy["Mods"]

		# ---------- #

		# Iterate through the dictionary of authors
		for name, author in self.neverending_legacy["Authors"]["Dictionary"].items():
			# Get the author mods
			author_mods = author["Mods"]

			# Iterate through the author mods
			for mod_title, mod in author_mods["Dictionary"].items():
				# Get the category of the mod
				mod_category = mod["Information"]["Mod category"] + " mods"

				# Add one to the category number of the mod
				mods["Numbers"]["Per category"][mod_category] += 1

				# Add the mod to the list of mods in the same category
				mods["Categories"]["Dictionary"][mod_category].append(mod_title)

				# ----- #

				# Add the mod title to the list of mods
				mods["List"].append(mod_title)

				# Add the local mod dictionary to the root mod dictionary
				mods["Dictionary"][mod_title] = mod
			
		# Update the number of mods inside the "Mods" dictionary
		mods["Numbers"]["Total"] = len(mods["List"])

		# Update the mod "Numbers" dictionary inside the local authors dictionary
		authors["Numbers"]["Mods"] = mods["Numbers"]

		# ---------- #

		# Add the local mods dictionary to the root "Mods" key
		self.neverending_legacy["Mods"] = mods

		# Make a local copy of the mods dictionary
		mods_dictionary = deepcopy(mods)

		# Iterate through the dictionary of mods
		for mod_title, mod in mods_dictionary["Dictionary"].items():
			# Remove some keys
			mod.pop("Folders")
			mod.pop("Files")

			# Update the root mod dictionary
			mods_dictionary["Dictionary"][mod_title] = mod

		# Write the updated local copy of the "Mods" dictionary into the "Mods.json" file
		self.JSON.Edit(self.neverending_legacy["Folders"]["Mods"]["Mods"], mods_dictionary)

		# ---------- #

		# Define the root "Authors" dictionary as the local one
		self.neverending_legacy["Authors"] = authors

		# Make a local copy of the authors dictionary
		authors_dictionary = deepcopy(authors)

		# Iterate through the dictionary of authors
		for name, author in authors_dictionary["Dictionary"].items():
			# Remove some keys
			author.pop("Folders")
			author.pop("Files")

			# Get the author mods
			author_mods = author["Mods"]

			# Iterate through the author mods
			for mod_title, mod in author_mods["Dictionary"].items():
				# Remove some keys
				mod.pop("Folders")
				mod.pop("Files")

				# Update mod dictionary
				author["Mods"]["Dictionary"][mod_title] = mod

			# Update the root authors dictionary
			authors_dictionary["Dictionary"][name] = author

		# Write the updated local copy of the "Authors" dictionary into the "Authors.json" file
		self.JSON.Edit(self.neverending_legacy["Folders"]["Mods"]["Authors"], authors_dictionary)

		# ---------- #

		# Define some switches
		translate = False
		enumerate = True

		# Define the text variable as a five dash space separator and some line breaks
		text = self.separators["5"] + "\n\n"

		# Define the default language text
		language = "en"

		# If the "translate" switch is True
		if translate == True:
			language = self.user_language

		# Define the language text based on the defined language
		language_text = self.texts["lists_of_authors_and_their_mods"][language]

		# Add a text explaining about the text file
		text += language_text + "\n\n"

		# Add some line breaks and a separator
		text += self.separators["3"] + "\n\n"

		# Define the language text based on the defined language
		language_text = self.Language.texts["authors, title()"][language]

		# Add the "Authors" text with the number of authors and a line break to the text variable
		text += language_text + " ({}):".format(str(authors["Numbers"]["Total"])) + "\n"

		# Add the list of authors
		text += self.Text.From_List(authors["List"], next_line = True)

		# Add some line breaks and a separator
		text += "\n\n" + self.separators["3"] + "\n\n"

		# Define the language text based on the defined language
		language_text = self.Language.texts["mods, title()"][language]

		# Add the "Mods" text with the number of mods and a line break
		text += language_text + " ({}):".format(str(mods["Numbers"]["Total"])) + "\n\n"

		# Iterate through the dictionary of authors
		for name, author in authors_dictionary["Dictionary"].items():
			# Add the author name to the text
			text += name

			# Get the mods of the author
			author_mods = author["Mods"]

			# If the number of author mods is greater than two
			if author_mods["Numbers"]["Total"] > 2:
				# Add the number to the text
				text += " ({})".format(str(author["Mods"]["Numbers"]["Total"]))

			# Add a line break to the text
			text += ":\n"

			# Iterate through the author mods
			m = 1
			for mod_title, mod in author_mods["Dictionary"].items():
				# If the "enumerate" switch is True
				# And the number of author mods is greater than one
				if (
					enumerate == True and
					author_mods["Numbers"]["Total"] > 1
				):
					# Add the mod number to the text
					text += str(m) + " - "

				# Add the mod title to the text along with the mod number
				text += mod_title

				# If the mod is not the last one
				if mod_title != list(author_mods["Dictionary"].keys())[-1]:
					# Add two line breaks to the text
					text += "\n"

				# Add one to the "m" variable
				m += 1

			# Add the mods to the text
			#text += self.Text.From_List(author_mods["List"], next_line = True)

			# If the author is not the last one
			if name != list(authors["Dictionary"].keys())[-1]:
				# Add two line breaks to the text
				text += "\n\n"

		# Write the lists text into the "Lists.txt" file
		self.File.Edit(self.neverending_legacy["Folders"]["Mods"]["Lists"], text)
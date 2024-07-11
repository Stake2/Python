# Social_Networks.py

# Import the "importlib" module
import importlib

from copy import deepcopy

class Social_Networks(object):
	def __init__(self):
		# Import the classes
		self.Import_Classes()

		# Define the folders of the module
		self.folders = self.Define_Folders(object = self).folders

		# Module related methods
		self.Define_Basic_Variables()
		self.Define_Texts()

		# Folders, files, lists, and dictionaries methods
		self.Define_Folders_And_Files()

		# Class methods

		# Define the "Information items" dictionary
		self.Define_Information_Items_Dictionary()

		# Define the "Social Networks" dictionary
		self.Define_Social_Networks_Dictionary()

		# Define the information items
		self.Define_Information_Items()

		# Update the social networks file
		self.Update_Social_Networks_File()

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
		# Define the "Texts" dictionary
		self.texts = self.JSON.To_Python(self.module["Files"]["Texts"])

		# Define the "Language texts" dictionary
		self.language_texts = self.Language.Item(self.texts)

		# Define the "Separators" dictionary
		self.separators = {}

		# Create separators from one to ten characters
		for number in range(1, 11):
			# Define the empty string
			string = ""

			# Add separators to it
			while len(string) != number:
				string += "-"

			# Add the string to the Separators dictionary
			self.separators[str(number)] = string

	def Define_Folders_And_Files(self):
		# Define the "Social Networks" folder dictionary
		self.folders["Social Networks"] = {
			"Text": {
				"root": self.folders["Notepad"]["Social Networks"]["root"]
			},
			"Image": {
				"root": self.folders["Image"]["Social Networks"]["root"]
			}
		}

		# ---------- #

		# Social Networks text "Database" folder
		self.folders["Social Networks"]["Text"]["Database"] = {
			"root": self.folders["Social Networks"]["Text"]["root"] + self.Language.language_texts["database, title()"] + "/"
		}

		# Database "Information items.json" file
		self.folders["Social Networks"]["Text"]["Database"]["Information items"] = self.folders["Social Networks"]["Text"]["Database"]["root"] + "Information items.json"
		self.File.Create(self.folders["Social Networks"]["Text"]["Database"]["Information items"])

		# "Social Networks.json" file
		self.folders["Social Networks"]["Text"]["Social Networks"] = self.folders["Social Networks"]["Text"]["root"] + "Social Networks.json"
		self.File.Create(self.folders["Social Networks"]["Text"]["Social Networks"])

		# "Social Networks list.txt" file
		self.folders["Social Networks"]["Text"]["Social Networks list"] = self.folders["Social Networks"]["Text"]["root"] + self.language_texts["social_networks_list"] + ".txt"
		self.File.Create(self.folders["Social Networks"]["Text"]["Social Networks list"])

		# ---------- #

		# Social Networks image "Digital Identities" folder
		self.folders["Social Networks"]["Image"]["Digital Identities"] = {
			"root": self.folders["Social Networks"]["Image"]["root"] + self.Language.language_texts["digital_identities"] + "/"
		}

		self.Folder.Create(self.folders["Social Networks"]["Image"]["Digital Identities"]["root"])

	def Define_Information_Items_Dictionary(self):
		# Define the "Information items" dictionary
		self.information_items = {
			"Numbers": {
				"Total": 0
			},
			"List": [],
			"Lists": {
				"Exact match": [],
				"Remove from search": [],
				"Do not ask for item": [],
				"Select": []
			},
			"Gender": {
				"Items": [
					"The",
					"This",
					"Part of"
				],
				"Masculine": [],
				"Feminine": []
			},
			"Formats": {},
			"Additional items": {},
			"Dictionary": {}
		}

		# Read the "Information items.json" file if it is not empty
		file = self.folders["Social Networks"]["Text"]["Database"]["Information items"]

		if self.File.Contents(file)["lines"] != []:
			self.information_items = self.JSON.To_Python(file)

	def Define_Social_Networks_Dictionary(self):
		# Define the default "Social Networks" dictionary
		self.social_networks = {
			"Numbers": {
				"Total": 0,
				"By year": {}
			},
			"List": [],
			"Dictionary": {}
		}

		# Read the "Social Networks.json" file if it is not empty
		file = self.folders["Social Networks"]["Text"]["Social Networks"]

		if self.File.Contents(file)["lines"] != []:
			self.social_networks = self.JSON.To_Python(file)

		# ---------- #

		# Define the default "File names" dictionary
		dictionary = {
			"List": [
				"Information",
				"Items",
				"Profile",
				"Settings",
				"Image folders",
				"Social Network"
			],
			"Dictionary": {}
		}

		# Iterate through the file names list
		for file_name in dictionary["List"]:
			# Create the file name dictionary
			dict_ = {}

			# Define the text key
			text_key = file_name.lower().replace(" ", "_")

			addon = ""

			if "_" not in text_key:
				addon = ", title()"

			# Iterate through the small languages list
			for language in self.languages["small"]:
				# Define the language file name text
				dict_[language] = self.Language.texts[text_key + addon][language]

			if "s" not in text_key:
				text_key += "s"

			# Define the plural texts of the file name
			dict_["Plural"] = {}

			# Iterate through the small languages list
			for language in self.languages["small"]:
				dict_["Plural"][language] = self.Language.texts[text_key + addon][language]

			# Add the file name dictionary to the root "File names" dictionary
			dictionary["Dictionary"][file_name] = dict_

		# Define the "File names" key as the local "File names" dictionary
		self.social_networks["File names"] = dictionary

		# ---------- #

		# Define the default "Link types" dictionary
		dictionary = {
			"Numbers": {
				"Total": 0,
			},
			"List": [
				"Home",
				"Profile"
			],
			"Dictionary": {}
		}

		# Iterate through the link types list
		for link_type in dictionary["List"]:
			# Create the link type dictionary
			dict_ = {}

			# Define the text key
			text_key = link_type.lower().replace(" ", "_")

			addon = ""

			if "_" not in text_key:
				addon = ", title()"

			# Iterate through the small languages list
			for language in self.languages["small"]:
				# Define the language link type text
				dict_[language] = self.Language.texts[text_key + addon][language]

			# Add the file name dictionary to the root "Link types" dictionary
			dictionary["Dictionary"][link_type] = dict_

		# Get the number of link types
		dictionary["Numbers"]["Total"] = len(dictionary["List"])

		# Define the "Link types" key as the local "Link types" dictionary
		self.social_networks["Link types"] = dictionary

		# ---------- #

		# Get the list of social networks
		self.social_networks["List"] = self.JSON.To_Python(self.folders["Social Networks"]["Text"]["Social Networks"])["List"]

		# Write the Social Networks list to the "Social Networks list.txt" file
		text_to_write = self.Text.From_List(self.social_networks["List"], break_line = True)

		self.File.Edit(self.folders["Social Networks"]["Text"]["Social Networks list"], text_to_write, "w")

		# Get the number of social networks
		self.social_networks["Numbers"]["Total"] = len(self.social_networks["List"])

		# Reset the numbers on the "By year" dictionary to zero
		for year in self.social_networks["Numbers"]["By year"]:
			self.social_networks["Numbers"]["By year"][year] = 0

		# ---------- #

		# Reset the Social Networks dictionary
		self.social_networks["Dictionary"] = {}

		# Iterate through the social networks list
		for social_network in self.social_networks["List"]:
			# Create the local "Social Network" dictionary
			dictionary = {
				"Name": social_network,
				"Folders": {},
				"Files": {},
				"Information": {},
				"Settings": {
					"Create image folders": True
				}
			}

			# Define and create the social network folders and files
			for item in ["Text", "Image"]:
				# Define the item key inside the "Files" dictionary
				dictionary["Files"][item] = {}

				# Define the root folder
				folder = self.folders["Social Networks"][item]["root"] + social_network + "/"

				# Create the folders dictionary
				dict_ = {
					"root": folder
				}

				self.Folder.Create(dict_["root"])

				# Iterate through the friend file names
				for key, file_name_dictionary in self.social_networks["File names"]["Dictionary"].items():
					# Define the file name
					file_name = file_name_dictionary

					if key == "Information":
						file_name = file_name["Plural"]

					# Define the file name language
					language = self.user_language

					if key in ["Items", "Social Network"]:
						language = "en"

					file_name = file_name[language]

					# Define the extension
					extension = "txt"

					if key in ["Items", "Social Network"]:
						extension = "json"

					# Define the file
					dict_[key] = dict_["root"] + file_name + "." + extension

					# If the key is not "Settings" nor "Image folders"
					# Or the key is "Image folders"
					# And the "Create image folders" settings is True
					if (
						key not in ["Settings", "Image folders"] or
						key == "Image folders" and
						dictionary["Settings"]["Create image folders"] == True
					):
						# If the item is "Text"
						# Or the key is "Social Network"
						if (
							item == "Text" or
							key == "Social Network"
						):
							# Create the file
							self.File.Create(dict_[key])

							# Add the file to the "Files" dictionary
							dictionary["Files"][key] = dict_[key]

						# Add the file to the "Files" dictionary
						dictionary["Files"][item][key] = dict_[key]

					# If the file is the settings file
					# And the settings file exists
					if (
						key == "Settings" and
						self.File.Exist(dict_[key]) == True
					):
						# Add the file to the "Files" dictionary
						dictionary["Files"][item][key] = dict_[key]
					
						# Read the settings file
						settings = self.File.Dictionary(dictionary["Files"]["Text"][key], next_line = True)

						# Define a local empty dictionary
						new_settings = {}

						# Define the texts dictionary for easier typing
						texts_dictionary = self.Language.texts

						# Iterate through the settings list
						for setting in self.texts["settings, type: list"]:
							# Get the English and language setting texts
							english_text = texts_dictionary[setting]["en"]

							language_text = texts_dictionary[setting][self.user_language]

							# If the language setting is inside the Settings dictionary
							if language_text in settings:
								# Add the setting value to the Settings dictionary, with the English key
								new_settings[english_text] = settings[language_text]

						dictionary["Settings"] = new_settings

				# Define the folders dictionary as the local folders dictionary
				dictionary["Folders"][item] = dict_

			# Add the keys of the "Text" folders dictionary to the root folders dictionary
			dictionary["Folders"].update(dictionary["Folders"]["Text"])

			# Update the Social Network "Information" only with the data on the files inside the Text folder
			# To get the most up-to-date information

			# Get the information dictionary (translating the keys to English)
			dictionary["Information"] = self.Information(file = dictionary["Files"]["Information"])

			# ---------- #

			# Get the social network information items
			items = self.JSON.To_Python(dictionary["Files"]["Items"])

			# Update the number of information items
			items["Numbers"]["Total"] = len(items["List"])

			# Update the items list of the root information items with the local items list of the Social Network
			for item in items["List"]:
				if item not in self.information_items["List"]:
					self.information_items["List"].append(item)

			# Update the "Exact match" list of the root information items with the "Exact match" list of the Social Network
			list_ = []

			for item in items["Lists"]["Exact match"]:
				if item not in self.information_items["Lists"]["Exact match"]:
					list_.append(item)

			self.information_items["Lists"]["Exact match"][social_network] = list_

			# Update the gender lists of the root information items with the gender lists of the Social Network
			for gender in ["Masculine", "Feminine"]:
				for item in items["Gender"][gender]:
					if item not in self.information_items["Gender"][gender]:
						self.information_items["Gender"][gender].append(item)

			# Update the "Formats" dictionary of the root information items with the "Formats" dictionary of the Social Network
			self.information_items["Formats"][social_network] = items["Formats"]

			if "Additional items" in items:
				additional_items = {}
				
				# Iterate through the "Additional items" dictionary
				for key, additional_item in items["Additional items"].items():
					if "{Social Network link}" in additional_item:
						additional_item = additional_item.replace("{Social Network link}", dictionary["Information"]["Link"][:-1])

					additional_items[key] = additional_item

				# Update the "Additional items" dictionary of the root information items with the "Additional items" dictionary of the Social Network
				self.information_items["Additional items"][social_network] = additional_items

			# If the "Do not ask for item" list exists
			if "Do not ask for item" in items["Lists"]:
				# Update the "Do not ask for item" list of the root information items with the "Do not ask for item" list of the Social Network
				for item in items["Lists"]["Do not ask for item"]:
					if item not in self.information_items["Lists"]["Do not ask for item"]:
						self.information_items["Lists"]["Do not ask for item"].append(item)

			# Iterate through the information items list
			for item in items["List"]:
				# If the item is "Profile link" or "Message link"
				if item in ["Profile link", "Message link"]:
					if item not in self.information_items["Lists"]["Do not ask for item"]:
						self.information_items["Lists"]["Do not ask for item"].append(item)

			# Update the "Items.json" file of the Social Network
			self.JSON.Edit(dictionary["Files"]["Items"], items)

			# Define the "Information items" dictionary of the Social Network as the local "Information items" dictionary
			dictionary["Information items"] = items

			# ---------- #

			# Get the user profile
			dictionary["Profile"] = self.Information(file = dictionary["Files"]["Profile"])

			# Create the "Links" dictionary
			dictionary["Profile"]["Links"] = {}

			# Add links to the dictionary above
			for link_type in ["Profile", "Message"]:
				key = link_type + " link"

				if key in dictionary["Profile"]:
					link = dictionary["Profile"][key]

					dictionary["Profile"]["Links"][link_type] = link

			# Get the image folders list from its file if it exists
			if "Image folders" in dictionary["Files"]:
				dictionary["Image folders"] = self.File.Contents(dictionary["Files"]["Image folders"])["lines"]

			# ---------- #

			# Copy the "Information" and "Profile" files of the Social Network text folder into the image folder
			# If the lengths of the files are different
			for file_name in ["Information", "Profile"]:
				files = {}

				for item in ["Text", "Image"]:
					file = dictionary["Files"][item][file_name]

					files[item] = {
						"File": file,
						"Size": self.File.Contents(file)["size"]
					}

				if files["Text"]["Size"] != files["Image"]["Size"]:
					self.File.Copy(files["Text"]["File"], files["Image"]["File"])

			# Define the "Social Network" dictionary as the local "Social Network" dictionary
			self.social_networks["Dictionary"][social_network] = dictionary

		# Iterate through the social networks list
		for social_network in self.social_networks["List"]:
			# Get the Social Network dictionary
			social_network = self.social_networks["Dictionary"][social_network]

			# Get the Social Network Information dictionary
			information = self.Information(social_network["Information"])

			# Get the release year
			release_year = information["Release"].split("/")[-1]

			# If the release year is not in the Social Networks "Numbers" dictionary
			if release_year not in self.social_networks["Numbers"]["By year"]:
				# Add it
				self.social_networks["Numbers"]["By year"][release_year] = 1

			# Else, add one to it
			else:
				self.social_networks["Numbers"]["By year"][release_year] += 1

		import collections

		# Sort the met by year numbers keys
		self.social_networks["Numbers"]["By year"] = dict(collections.OrderedDict(sorted(self.social_networks["Numbers"]["By year"].items())))

	def Define_Information_Items(self):
		# Define the local "Information items" dictionary as the "Information items" dictionary
		dictionary = self.information_items

		# Get the number of information items
		dictionary["Numbers"]["Total"] = len(dictionary["List"])

		# Reset the "Dictionary" key to be an empty dictionary
		dictionary["Dictionary"] = {}

		# Iterate through the information items list
		for key in dictionary["List"]:
			# Create the information item dictionary
			dict_ = {
				"Name": key
			}

			# Define the text key
			text_key = key.lower().replace(" ", "_")

			addon = ""

			if "_" not in text_key:
				addon += ", title()"

			# Iterate through the small languages list
			for language in self.languages["small"]:
				# Define the correct texts dictionary
				texts_dictionary = self.Language.texts

				if text_key in self.texts:
					texts_dictionary = self.texts

				# Get the text
				text = texts_dictionary[text_key + addon][language]

				# Define the language information item inside the local "dict_" dictionary
				dict_[language] = text

				# If the language dictionary is not inside the "Lists" dictionary of the "Information items" dictionary
				if language not in dictionary["Lists"]:
					# Create it
					dictionary["Lists"][language] = []

				# If the text is not inside the language "Lists" dictionary of the "Information items" dictionary
				if text not in dictionary["Lists"][language]:
					# Add it
					dictionary["Lists"][language].append(text)

			# Define the plural versions of the information item
			dict_["Plural"] = {}

			# Update the text key
			text_key_backup = text_key + addon

			if "s" not in text_key[-1]:
				text_key += "s"

			text_key += addon

			if text_key not in self.Language.texts:
				text_key = text_key.replace(addon, "")
				text_key = text_key[:-1]

				text_key += addon + ", type: plural"

			if text_key not in self.Language.texts:
				text_key = text_key_backup

			# Iterate through the small languages list
			for language in self.languages["small"]:
				dict_["Plural"][language] = self.Language.texts[text_key][language]

			# Define the "Gender" key
			dict_["Gender"] = {
				"Text": "",
				"Words": {}
			}

			# Define the gender words of the information item
			words = {}

			for item in dictionary["Gender"]["Items"]:
				text_key = item.lower().replace(" ", "_")

				# Define the gender
				if key in dictionary["Gender"]["Masculine"]:
					gender = "masculine"

				if key in dictionary["Gender"]["Feminine"]:
					gender = "feminine"

				words[item] = self.Language.texts["genders, type: dict"][self.user_language][gender][text_key]

				# Define the gender inside the "Gender" dictionary
				dict_["Gender"]["Text"] = gender

			# Update the gender "Words" dictionary inside the root information item dictionary
			dict_["Gender"]["Words"] = words

			# Define the format of the information item
			dict_["Format"] = {
				"Regex": "",
				"Example": ""
			}

			# If the key is in the "Formats" dictionary, use the format dictionary inside it
			if key in dictionary["Formats"]:
				dict_["Format"] = dictionary["Formats"][key]

			# Define the "States" dictionary of the information item
			dict_["States"] = {
				"Exact match": False,
				"Ask for information": True
			}

			# Update the "Exact match" key
			if key in dictionary["Lists"]["Exact match"]:
				dict_["States"]["Exact match"] = True

			# Update the "Ask for information" key
			if (
				"Do not ask for item" in dictionary["Lists"] and
				key in dictionary["Lists"]["Do not ask for item"]
			):
				dict_["States"]["Ask for information"] = False

			# Add the information item dictionary to the root "Information items" dictionary
			dictionary["Dictionary"][key] = dict_

		# Define the "Information items" dictionary as the local "Information items" dictionary
		self.information_items = dictionary

		# Iterate through the social networks list
		for key, social_network in self.social_networks["Dictionary"].items():
			# Create the Local "Information items" dictionary using the Social Network "Information items" dictionary as a base
			information_items = deepcopy(social_network["Information items"])

			# Create the "Dictionary" key
			information_items["Dictionary"] = {}

			# Iterate through the Social Network information items list
			for item in social_network["Information items"]["List"]:
				# If the item is inside the root "Information items" dictionary
				if item in self.information_items["Dictionary"]:
					# Define the local item dictionary as the item dictionary inside the root "Information items" dictionary
					information_items["Dictionary"][item] = self.information_items["Dictionary"][item]

				if key in self.information_items["Additional items"]:
					# Create the "Templates" key inside the "Information items" dictionary of the Social Network
					information_items["Templates"] = self.information_items["Additional items"][key]

			# Define the Social Network "Information items" dictionary as the Local "Information items" dictionary
			social_network["Information items"] = information_items

			# Remove the unused keys of the Social Network "Information items" dictionary
			to_remove = [
				"Lists",
				"Gender",
				"Formats",
				"Additional items"
			]

			for item in to_remove:
				social_network["Information items"].pop(item)

			# Translate the keys of the "Information.txt" file to English
			social_network["Information"] = self.Information(file = social_network["Files"]["Information"])

			# Translate the keys of the "Profile.txt" file to English
			social_network["Profile"] = self.Information(file = social_network["Files"]["Profile"])

			link_additional_items = []

			# Create the "Links" dictionary
			social_network["Profile"]["Links"] = {}

			# Add links to the dictionary above
			for link_type in ["Profile", "Message"]:
				link_key = link_type + " link"

				if link_key in social_network["Profile"]:
					link = social_network["Profile"][link_key]

					social_network["Profile"]["Links"][link_type] = link

				link_additional_items.append(link_key)

			# Define the "profile" variable for faster typing
			profile = social_network["Profile"]

			# Iterate through the additional items dictionary
			for sub_key, additional_item in self.information_items["Additional items"][key].items():
				# If the additional item key is not inside the "link additional items" list
				if sub_key not in link_additional_items:
					# For each item inside the information items list
					for item in information_items["List"]:
						# If the item with brackets around is inside the additinal item (maybe a link with format strings)
						if "{" + item + "}" in additional_item:
							# Format the format string with the item data gotten from the user profile dictionary
							additional_item = additional_item.replace("{" + item + "}", profile[item])

					# Add the additional item to the "Links" dictionary if the additional item contains the Social Network link
					if social_network["Information"]["Link"] in additional_item:
						social_network["Profile"]["Links"][sub_key] = additional_item

			# ---------- #

			# Make a local copy of the "Social Network" dictionary
			local_dictionary = deepcopy(social_network)

			# Define the root keys to remove
			to_remove = [
				"Folders",
				"Files",
				"Information items"
			]

			# Iterate through the "root keys to remove" list and remove the keys
			for sub_key in to_remove:
				local_dictionary.pop(sub_key)

			# Update the "Social Network.json" file with the updated and local "Social Network" dictionary
			self.JSON.Edit(social_network["Folders"]["Social Network"], local_dictionary)

			# Update the image "Social Network.json" file with the updated and local "Social Network" dictionary
			self.JSON.Edit(social_network["Folders"]["Image"]["Social Network"], local_dictionary)

			# ---------- #

			# Update the root "Social Network" dictionary
			self.social_networks["Dictionary"][key] = social_network

		# ---------- #

		import collections

		# Sort the dictionary keys
		self.information_items["Lists"]["Exact match"] = dict(collections.OrderedDict(sorted(self.information_items["Lists"]["Exact match"].items())))
		self.information_items["Formats"] = dict(collections.OrderedDict(sorted(self.information_items["Formats"].items())))
		self.information_items["Additional items"] = dict(collections.OrderedDict(sorted(self.information_items["Additional items"].items())))

		# Create a local Information items dictionary
		local_dictionary = deepcopy(self.information_items)

		# Iterate through the small languages list
		for language in self.languages["small"]:
			# Remove the language items lists
			local_dictionary["Lists"].pop(language)

		# Update the "Information items.json" file with the updated and local "Information items" dictionary
		self.JSON.Edit(self.folders["Social Networks"]["Text"]["Database"]["Information items"], local_dictionary)

		# ---------- #

		# Sort the dictionary keys
		self.social_networks["Dictionary"] = dict(collections.OrderedDict(sorted(self.social_networks["Dictionary"].items())))

	def Update_Social_Networks_File(self):
		# Create a local "Social Networks" dictionary
		local_dictionary = deepcopy(self.social_networks)

		# Define the root keys to remove
		to_remove = [
			"File names",
			"Link types"
		]

		# Iterate through the "root keys to remove" list and remove the keys
		for key in to_remove:
			local_dictionary.pop(key)

		# Define the social network keys to remove
		to_remove = [
			"Folders",
			"Files",
			"Settings"
		]

		# Iterate through the social networks list
		for social_network in self.social_networks["List"]:
			# Remove the unused social network keys
			for key in to_remove:
				local_dictionary["Dictionary"][social_network].pop(key)

			# Remove the "Dictionary" key of the "Information items" dictionary
			local_dictionary["Dictionary"][social_network]["Information items"].pop("Dictionary")

		# Update the "Social Networks.json" file with the updated and local "Social Networks" dictionary
		self.JSON.Edit(self.folders["Social Networks"]["Text"]["Social Networks"], local_dictionary)

	def Information(self, information = None, file = None, information_items = None, to_user_language = False):
		if file != None:
			information = self.File.Dictionary(file, next_line = True)

		if information_items == None:
			information_items = self.information_items

		dictionary = {}

		for information_key, value in information.items():
			correct_key = information_key

			for key, information_item in self.information_items["Dictionary"].items():
				language_key = information_item[self.user_language]

				if (
					key == information_key or
					information_key == information_item[self.user_language]
				):
					correct_key = key

					if to_user_language == True:
						correct_key = language_key

			dictionary[correct_key] = value

		return dictionary

	def Select_Social_Network(self, social_network = None, social_networks = None, select_social_network = True, show_text = None, select_text = None):
		if social_networks == None:
			social_networks = self.social_networks

		if show_text == None:
			show_text = self.language_texts["social_networks"]

		if select_text == None:
			select_text = self.language_texts["select_one_social_network_to_use"]

		if select_social_network == True:
			if social_network == None:
				self.social_network = self.Input.Select(social_networks["List"], show_text = show_text, select_text = select_text)["option"]

			if social_network != None:
				if type(social_network) == dict:
					social_network = social_network["Name"]

				self.social_network = social_network

			if self.social_network in self.social_networks["Dictionary"]:
				self.social_network = self.social_networks["Dictionary"][self.social_network]

				return self.social_network

			else:
				return None

		else:
			return None

	def Type_Social_Network_Information(self, first_separator = True):
		if first_separator == True:
			# Show a separator
			print()
			print(self.separators["5"])

		# Define the information text
		information_text = self.language_texts["please_type_the_social_network_profile_information"] + ' "{}":'

		# Format the information text
		information_text = information_text.format(self.social_network["Name"])

		# Show the information text
		print()
		print(information_text)

		# Define the Social Network Profile dictionary
		self.social_network["Profile"] = {}

		# Define the test information dictionary for testing
		test_information = {
			"Discord": {
				"Username": "Username of Discord",
				"Handle": "handle_of_discord",
				"Originally": "Originally#0001",
				"ID": "100000000000000000",
				"Message ID": "100000000000000000",
				"Member since": "13/06/2015",
				"Pronouns": ""
			}
		}

		# Reset the test information dictionary to test manually typing the information
		#test_information = {}

		# Define the default information value
		information = ""

		# Iterate through the Information items dictionary
		for key, information_item in self.social_network["Information items"]["Dictionary"].items():
			# If the information item is not inside the "Remove from search" list
			if key not in self.information_items["Lists"]["Remove from search"]:
				# Get the language information item
				language_information_item = information_item[self.user_language]

				# If the user needs to type the information
				if information_item["States"]["Ask for information"] == True:
					# Define the "accept_enter" variable
					accept_enter = False

					if information_item["Format"]["Regex"] == "":
						accept_enter = True

					# Get the information item format
					item_format = None

					if key in self.information_items["Formats"][self.social_network["Name"]]:
						item_format = self.information_items["Formats"][self.social_network["Name"]][key]

					if (
						self.switches["Testing"] == False or
						self.switches["Testing"] == True and
						self.social_network["Name"] not in test_information
					):
						# Ask the user for the information
						information = self.Input.Type(language_information_item, accept_enter = accept_enter, next_line = True, tab = "\t", regex = item_format)

					if (
						self.switches["Testing"] == True and
						self.social_network["Name"] in test_information and
						key in test_information[self.social_network["Name"]]
					):
						information = test_information[self.social_network["Name"]][key]

					# Define the information as "[Empty]" if it is empty
					if information == "":
						information = "[{}]".format(self.Language.language_texts["empty, title()"])

				# If the information item is inside the "Additional items" dictionary
				if key in self.information_items["Additional items"][self.social_network["Name"]]:
					# Get the additional item template of the information item
					additional_item = self.information_items["Additional items"][self.social_network["Name"]][key]

					# Get the format information item
					format_item = additional_item.split("{")[1].split("}")[0]

					# Remove the format item from the additional item template
					additional_item = additional_item.replace(format_item, "")

					# Define the information with the formatted additional item template
					information = additional_item.format(self.social_network["Profile"][format_item])

				if (
					self.switches["Testing"] == True and
					test_information != {} and
					self.social_network["Name"] in test_information
				):
					print()
					print(language_information_item + ":")
					print("\t" + information)

				# Add the information to the Social Network "Information" dictionary, with the information item key
				self.social_network["Profile"][key] = information

		print()
		print("-----")

		return self.social_network
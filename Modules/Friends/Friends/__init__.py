# Friends.py

# Import some useful modules
import importlib
from copy import deepcopy

# Define the main "Friends" class
class Friends(object):
	def __init__(self):
		# Define the variables of the class
		self.Define_Variables()

		# Import some usage classes
		self.Import_Usage_Classes()

		# Folders and files method
		self.Define_Folders_And_Files()

		# Define the "history" dictionary of the friends database
		self.Define_History()

		# Define the "Information items" dictionary
		self.Define_Information_Items()

		# Define the "Friends" dictionary
		self.Define_Friends_Dictionary()

	def Define_Variables(self):
		# Import the "JSON" class
		from Utility.JSON import JSON as JSON

		# Instance it and add it to the current class
		self.JSON = JSON()

		# Import the "folders" dictionary from the "JSON" class
		self.folders = self.JSON.folders

		# ---------- #

		# Get the dictionary of Python modules
		self.modules = self.JSON.To_Python(self.folders["Python"]["Modules"]["Modules"])

		# Iterate through the list of utility classes
		for class_title in self.modules["Utility"]["List"]:
			# If the class is not already inside the self class (Friends)
			# And the class title is not inside the list of optional classes
			if (
				hasattr(self, class_title) == False and
				class_title not in self.modules["Utility"]["Optional"]
			):
				# Import the module of the class
				module = importlib.import_module("." + class_title, "Utility")

				# Get the class object inside the module
				class_object = getattr(module, class_title)

				# If the class title is not "Modules"
				if class_title != "Modules":
					# Run the class object to define its attributes
					class_object = class_object()

				# Add the class object to the root class
				setattr(self, class_title, class_object)

		# ---------- #

		# Define the module dictionary and the module folders and files
		self.Modules(class_object = self)

		# ---------- #

		# Import the switches dictionary from the "Global Switches" class
		self.switches = self.Global_Switches.switches["Global"]

		# ---------- #

		# Define the "Language" class as the same class inside the "JSON" class
		self.Language = self.JSON.Language

		# Import some attributes from the "Language" class

		# Import the "languages" dictionary
		self.languages = self.Language.languages

		# Import the "language" dictionary
		self.language = self.Language.language

		# Import the "separators" dictionary
		self.separators = self.Language.separators

		# ---------- #

		# Import the "folders" dictionary from the "Folder" class
		self.folders = self.Folder.folders

		# ---------- #

		# Get the current date from the "Date" class
		self.date = self.Date.date

		# Create a shortcut to the current year number
		self.current_year = self.date["Units"]["Year"]

		# ---------- #

		# Define the "Texts" dictionary
		self.texts = self.JSON.To_Python(self.module["Files"]["Texts"])

		# Define the "Language texts" dictionary
		self.language_texts = self.Language.Item(self.texts)

	def Import_Usage_Classes(self):
		# Define the list of classes to be imported
		self.classes = [
			"Social_Networks"
		]

		# Iterate through the list of classes to import
		for class_title in self.classes:
			# Import the module of the class
			module = importlib.import_module("." + class_title, class_title)

			# Get the class object inside the module
			class_object = getattr(module, class_title)

			# Run the class to define its variables
			class_object = class_object()

			# Iterate through the list of utility modules
			for module_title in self.modules["Utility"]["List"]:
				# If the module title is not inside the defined list
				# And the module attribute is inside the self class (Friends)
				if (
					module_title not in ["Language", "Modules"] and
					hasattr(self, module_title) == True
				):
					# Get the class object inside the module
					local_sub_class = getattr(self, module_title)

					# Add the class object to the root class
					setattr(class_object, module_title, local_sub_class)

			# If the sub-class has a list of classes
			if hasattr(class_object, "classes") == True:
				# Get the list of classes of the current class
				current_class_classes = getattr(class_object, "classes")

				# Define a copy of the list of classes
				classes_copy = self.classes.copy()

				# Remove the current class
				classes_copy.remove(class_title)

				# Iterate through the local list of classes
				for local_class_title in classes_copy:
					# If the local class title is inside the list of classes of the current class
					# And it also is inside this class (Watch_History)
					if (
						local_class_title in current_class_classes and
						hasattr(self, local_class_title) != None
					):
						# Give the local class to the current class
						setattr(class_object, local_class_title, getattr(self, local_class_title))

			# Add the class object to the root class
			setattr(self, class_title, class_object)

		# ---------- #

		# Define the list of variables to import
		to_import = [
			"social_networks",
			"Select_Social_Network"
		]

		# Iterate through them
		for variable_title in to_import:
			# Get the variable from the "Social_Networks" class
			variable = getattr(self.Social_Networks, variable_title)

			# Add it to this class (Friends)
			setattr(self, variable_title, variable)

	def Define_Folders_And_Files(self):
		# Define the "Friends" folders dictionary
		# And also define and create the root "Friends" folder in the root of the drive
		self.folders["Friends"] = {
			"root": self.folders["root"] + self.Language.language_texts["friends, title()"] + "/"
		}

		self.Folder.Create(self.folders["Friends"]["root"])

		# ---------- #

		# Define and create the friends "Database" folder
		self.folders["Friends"]["Database"] = {
			"root": self.folders["Friends"]["root"] + self.Language.language_texts["database, title()"] + "/"
		}

		self.Folder.Create(self.folders["Friends"]["Database"]["root"])

		# Define and create the database "Information items.json" file
		file = self.folders["Friends"]["Database"]["root"] + "Information items.json"
		self.File.Create(file)

		self.folders["Friends"]["Database"]["Information items"] = file

		# Define and create the root "Friends.json" file
		file = self.folders["Friends"]["root"] + "Friends.json"
		self.File.Create(file)

		self.folders["Friends"]["Friends"] = file

		# Define and create the root "Friends list.txt" file
		file = self.folders["Friends"]["root"] + self.language_texts["friends_list"] + ".txt"
		self.File.Create(file)

		self.folders["Friends"]["Friends list"] = file

	def Define_History(self):
		# Define the "History" dictionary
		self.history = {
			"Class title": self.language_texts["Friends"],
			"Key": "",
			"Numbers": {
				"Known people": "By year"
			},
			"Folder": self.folders["Friends"]["root"]
		}

	def Define_Information_Items(self):
		# Define the local "Information items" dictionary
		information_items = {
			"Numbers": {
				"Total": 0
			},
			"List": [],
			"Lists": {
				"Exact match": [],
				"Select": [],
				"Do not ask for item": [],
				"Accept enter": []
			},
			"Gender": {
				"Items": [
					"The",
					"This",
					"Part of"
				]
			},
			"Formats": {},
			"Dictionary": {}
		}

		# Create a shortcut to the database "Information items.json" file
		file = self.folders["Friends"]["Database"]["Information items"]

		# If the "Information items.json" file is not empty
		if self.File.Contents(file)["Lines"] != []:
			# Define it as the local "Information items" dictionary
			information_items = self.JSON.To_Python(file)

		# Get the number of information items
		information_items["Numbers"]["Total"] = len(information_items["List"])

		# Reset the "Dictionary" key to be an empty dictionary
		information_items["Dictionary"] = {}

		# Iterate through the information items list
		for name in information_items["List"]:
			# Create the information item dictionary
			information_item = {
				"Name": name
			}

			# Define the text key based on the information item
			text_key = name.lower().replace(" ", "_")

			# Define the text addon
			text_addon = ""

			# If the underline is not inside the text key, add the ", title()" text to the text addon
			if "_" not in text_key:
				text_addon = ", title()"

			# Iterate through the list of small languages
			for language in self.languages["Small"]:
				# Get the information item text
				text = self.Language.texts[text_key + text_addon][language]

				# Define the language information item inside the local "information item" dictionary
				information_item[language] = text

				# If the language dictionary is not inside the "Lists" dictionary of the "Information items" dictionary
				if language not in information_items["Lists"]:
					# Create it
					information_items["Lists"][language] = []

				# If the text is not inside the language "Lists" dictionary of the "Information items" dictionary
				if text not in information_items["Lists"][language]:
					# Add it
					information_items["Lists"][language].append(text)

			# Define the plural versions of the information item
			information_item["Plural"] = {}

			# Create a backup for the text key
			text_key_backup = text_key + text_addon

			# If the "s" (plural) character is not inside the text key, add it
			if "s" not in text_key[-1]:
				text_key += "s"

			# Add the text addon to the text key (might be a empty string or the ", title()" text)
			text_key += text_addon

			# If the text key is not inside the "texts" dictionary of the "Language" utility class
			if text_key not in self.Language.texts:
				# Remove the text addon
				text_key = text_key.replace(text_addon, "")

				# Remove the last character, which is "s" (plural)
				text_key = text_key[:-1]

				# Add the text addon back and ", type: plural"
				text_key += text_addon + ", type: plural"

			# If the text key is still not inside the "texts" dictionary of the "Language" utility class
			if text_key not in self.Language.texts:
				# Then change the text key back to its original version
				text_key = text_key_backup

			# Iterate through the list of small languages
			for language in self.languages["Small"]:
				# Add the plural text to the "Plural" dictionary of the information item dictionary
				information_item["Plural"][language] = self.Language.texts[text_key][language]

			# Define the "Gender" dictionary of the information item
			information_item["Gender"] = {
				"Text": "",
				"Words": {}
			}

			# Define the "Format" dictionary of the information item
			information_item["Format"] = {
				"Regex": "",
				"Example": ""
			}

			# If the information item is inside the root "Formats" dictionary
			if name in information_items["Formats"]:
				# Define the information item format as the one inside the root dictionary
				information_item["Format"] = information_items["Formats"][name]

			# Define the "States" dictionary of the information item
			information_item["States"] = {
				"Exact match": False,
				"Select": False,
				"Ask for information": True
			}

			# If the information item is inside the "Do not ask for item" list
			if name in information_items["Lists"]["Do not ask for item"]:
				# Change its "Ask for information" state to False
				information_item["States"]["Ask for information"] = False

			# Create a local copy of the root "States" dictionary
			states = deepcopy(information_item["States"])

			# Remove the "Ask for information" state since it already has been defined previously
			states.pop("Ask for information")

			# Iterate through the list of states
			for state in states:
				# If the information item is inside the list of the current state
				if name in information_items["Lists"][state]:
					# Change the current state of the information item to True
					# (For example, if the information item is inside the "Exact match" list, its "Exact match" state will be True
					# The same happens for the "Select" state)
					information_item["States"][state] = True

			# If the "Select" state of the information item is True
			if information_item["States"]["Select"] == True:
				# Define the "Select" dictionary
				information_item["Select"] = {
					# The lists from which the information will be selected
					# For example: Lists of genders, lists of sexualities
					"List": {
						"English": [],
						"Language": []
					},

					# The singular and plural texts for the information item
					# For example: ["Gender", "Genders"], ["Sexuality", "Sexualities"]
					# The singular text is used for the select text, and the plural is used for the show text
					"Texts": {
						"Singular": information_item[self.language["Small"]],
						"Plural": information_item["Plural"][self.language["Small"]]
					}
				}

				# If the information item is not "Origin social network"
				if name != "Origin social network":
					# Define the text key for the list of options
					text_key = information_item["Plural"]["en"].lower().replace(" ", "_")

					# Add the ", type: list" text to find the list of option
					text_key += ", type: list"

				# Iterate through the list of languages inside the "Select" list
				for item in information_item["Select"]["List"]:
					# Define the local language as the English language
					language = "en"

					# If the current item is "Language"
					if item == "Language":
						# Then define the local language as the user language
						language = self.language["Small"]

					# If the information item is not "Origin social network"
					if name != "Origin social network":
						# Get the list of options using the text key and the current language
						local_list = self.Language.texts[text_key][language]

					# If the information item is "Origin social network"
					if name == "Origin social network":
						# Create a copy of the root "social networks" dictionary
						social_networks = deepcopy(self.social_networks)

						# Add the "Custom social network" item to the local list of social network
						social_networks["List"].append(self.texts["custom_social_network"][language])

						# Define the local list as the local list of social networks
						local_list = social_networks["List"]

						# Define the "Custom select text" of the "Select" dictionary as "Select the social network where you met {}"
						information_item["Select"]["Texts"]["Custom select text"] = self.language_texts["select_the_social_network_where_you_met_{}"]

					# Define the root "Select" list as the local list
					information_item["Select"]["List"][item] = local_list

			# Add the local information item dictionary to the root "Information items" dictionary
			information_items["Dictionary"][name] = information_item

		# Iterate through the list of information items
		for name, information_item in information_items["Dictionary"].items():
			# Define the local gender "Words" dictionary
			words = {}

			# Iterate through the items inside the gender "Items" dictionary
			for item in information_items["Gender"]["Items"]:
				# If the information item is inside the "Masculine" list, define the local gender as "masculine"
				if name in information_items["Gender"]["Masculine"]:
					gender = "masculine"

				# If the information item is inside the "Feminine" list, define the local gender as "feminine"
				if name in information_items["Gender"]["Feminine"]:
					gender = "feminine"

				# Update the gender text inside the "Gender" dictionary of the information item dictionary
				information_items["Dictionary"][name]["Gender"]["Text"] = gender

				# Define the text key for the item
				text_key = item.lower().replace(" ", "_")

				# Define the empty item dictionary
				words[item] = {}

				# Iterate through the list of small languages
				for language in self.languages["Small"]:
					# If the language dictionary does not exist, create it
					if language not in words[item]:
						words[item][language] = {}

					# Define the gender text of the item in the current language
					words[item][language] = self.Language.texts["genders, type: dictionary"][language][gender][text_key]

			# Update the gender "Words" dictionary inside the information item dictionary
			information_items["Dictionary"][name]["Gender"]["Words"] = words

		# Define the root "Information items" dictionary as the local "information items" dictionary
		self.information_items = information_items

		# Create a local copy of the root "Information items" dictionary
		local_dictionary = deepcopy(self.information_items)

		# Iterate through the list of small languages
		for language in self.languages["Small"]:
			# Remove the language list from the "Lists" dictionary
			local_dictionary["Lists"].pop(language)

		# Update the "Information items.json" file with the updated and local copy of the "Information items" dictionary
		self.JSON.Edit(self.folders["Friends"]["Database"]["Information items"], local_dictionary)

	def Define_Friends_Dictionary(self):
		# Define the default "Friends" dictionary
		self.friends = {
			"Numbers": {
				"Total": 0,
				"By year": {}
			},
			"List": [],
			"Met by year": {},
			"Dictionary": {}
		}

		# Create a shortcut to the root "Friends.json" file
		file = self.folders["Friends"]["Friends"]

		# If the "Friends.json" file is not empty
		if self.File.Contents(file)["Lines"] != []:
			# Define it as the root "Friends" dictionary
			self.friends = self.JSON.To_Python(file)

		# ---------- #

		# Define the default "File names" dictionary
		file_names = {
			"Names": [
				"Information",
				"Social network"
			],
			"Dictionary": {}
		}

		# Iterate through the list of file names
		for name in file_names["Names"]:
			# Create the local file name dictionary
			file_name = {}

			# Define the text key for the file name text
			text_key = name.lower().replace(" ", "_")

			# Define the text addon
			text_addon = ""

			# If the underline is not inside the text key, add the ", title()" text to the text addon
			if "_" not in text_key:
				text_addon = ", title()"

			# Iterate through the list of small languages
			for language in self.languages["Small"]:
				# Define the language file name text
				file_name[language] = self.Language.texts[text_key + text_addon][language]

			# If the "s" (plural) character is not inside the text key, add it
			if "s" not in text_key[-1]:
				text_key += "s"

			# Define the plural versions of the file name text
			file_name["Plural"] = {}

			# Iterate through the list of small languages
			for language in self.languages["Small"]:
				# Add the plural file name text to the "Plural" dictionary of the file name dictionary
				file_name["Plural"][language] = self.Language.texts[text_key + text_addon][language]

			# Add the file name dictionary to the root "File names" dictionary
			file_names["Dictionary"][name] = file_name

		# Define the friend "File names" key as the local "file names" dictionary
		self.friends["File names"] = file_names

		# ---------- #

		# Get the sub-folders of the "Friends" folder
		contents = self.Folder.Contents(self.folders["Friends"]["root"])

		# Define the list of friends as the list of folders
		self.friends["List"] = contents["Folder"]["Names"]

		# Define a list of folders to remove from the list
		remove_list = [
			"Archive",
			"Database"
		]

		# Iterate through the list of folders to remove
		for folder_name in remove_list:
			# Create the text key by converting the folder into lowercase and replacing spaces with underscores
			text_key = folder_name.lower().replace(" ", "_")

			# If the underscore character is not inside the text key
			if "_" not in text_key:
				# Add the ", title()" text
				text_key += ", title()"

			# If the text key is inside the language texts dictionary of the "Language" utility class
			if text_key in self.Language.language_texts:
				# Get the folder name in the user language
				folder_name = self.Language.language_texts[text_key]

			# If the folder is inside the list of friends
			if folder_name in self.friends["List"]:
				# Remove it
				self.friends["List"].remove(folder_name)

		# ---------- #

		# Write the list of friends to the "Friends list.txt" file
		text_to_write = self.Text.From_List(self.friends["List"])

		self.File.Edit(self.folders["Friends"]["Friends list"], text_to_write, "w")

		# Get the total number of friends
		self.friends["Numbers"]["Total"] = len(self.friends["List"])

		# Add all years from 2018 to the current year to the "By year" numbers dictionary
		for year in self.Date.Create_Years_List(start = 2018, function = str):
			self.friends["Numbers"]["By year"][year] = 0

		# Iterate through the years inside the "By year" numbers dictionary
		for year in self.friends["Numbers"]["By year"]:
			# Reset the year number to be zero
			self.friends["Numbers"]["By year"][year] = 0

		# ---------- #

		import collections

		# Reset the friends "Dictionary" to be empty
		# (The dictionary obtained from the "Friends.json" file may already be populated)
		self.friends["Dictionary"] = {}

		# Iterate through the list of friends
		for name in self.friends["List"]:
			# Create the local "friend" dictionary
			friend = {
				"Name": name,
				"Folders": {},
				"Files": {},
				"Information": {},
				"Social networks": {}
			}

			# Define and create the friend folder
			folder = self.folders["Friends"]["root"] + name + "/"
			self.Folder.Create(folder)

			# Create the friend folders dictionary
			folders = {
				"root": folder
			}

			# Define and create the friend "Social networks" folder
			folders["Social networks"] = {
				"root": folders["root"] + self.Language.language_texts["social_networks"] + "/"
			}

			self.Folder.Create(folders["Social networks"]["root"])

			# Iterate through the list of friend file names
			for key, dictionary in self.friends["File names"]["Dictionary"].items():
				# Define the file name as its plural version in the user language
				file_name = dictionary["Plural"][self.language["Small"]]

				# Define the folders dictionary as the root one
				folders_dictionary = folders

				# If the file name is "Social networks"
				if key == "Social network":
					# Change the folders dictionary to be the "Social networks" one
					folders_dictionary = folders["Social networks"]

					# Change the file name to be its English version ("Social networks")
					key = dictionary["Plural"]["en"]

				# Define the file and create it
				folders_dictionary[key] = folders_dictionary["root"] + file_name + ".txt"
				self.File.Create(folders_dictionary[key])

				# If the file name is "Information"
				if key == "Information":
					# Add it normally to the friend "Files" dictionary
					friend["Files"][key] = folders_dictionary[key]

				# If the file name is "Social networks"
				if key == "Social networks":
					# Create a dictionary for the "Social networks" files
					friend["Files"][key] = {
						# And define the "List" key as the "Social networks.txt" file
						"List": folders_dictionary[key]
					}

			# Define and create the friend "Media" folder
			folders["Media"] = {
				"root": folders["root"] + self.Language.language_texts["media, title(), type: plural"] + "/"
			}

			self.Folder.Create(folders["Media"]["root"])

			# Define the root friend "Folders" dictionary as the local one
			friend["Folders"] = folders

			# ----- #

			# Get the friend information dictionary using the friend "Information.txt" file
			friend_information = self.Information(file = friend["Files"]["Information"])

			# Add the information keys and values to the friend "Information" dictionary
			for key, value in friend_information.items():
				friend["Information"][key] = value

			# Define the local dictionary of locations
			locations = {
				"Hometown": {},
				"Residence": {}
			}

			# Define the local list of location fields
			location_fields = [
				"City",
				"State",
				"Country"
			]

			# Itearate through the list of locations
			for location in locations.copy():
				# Define the key as the location
				key = location

				# If the key is "Residence", add " place" to change the key to "Residence place"
				if key == "Residence":
					key += " place"

				# Get the friend location from the friend "Information" dictionary and split it by the " - " string
				# Split format: "[City] - [State] - [Country]"
				fields = friend["Information"][key].split(" - ")

				# Itearate through the location fields inside the list of location fields
				# Items: [City, State, Country]
				# Split format: "City - State - Country"
				i = 0
				for location_field in fields:
					# Get the location field key
					# Can be "City", "State", or "Country"
					field_key = location_fields[i]

					# Define the location field inside the current location dictionary with the field key, using the "i" number to get the correct field
					# Example: place can be "City", 
					locations[location][field_key] = fields[i]

					# Add one to the "i" number
					i += 1

			# Add the "Locations" dictionary to the friend "Information" dictionary, and add it after the "Residence place" key
			key_value = {
				"Locations": locations
			}

			friend["Information"] = self.JSON.Add_Key_After_Key(friend_information, key_value, after_key = "Residence place")

			# Add the "Year I met" key to the friend "Information" dictionary
			friend["Information"]["Year I met"] = friend["Information"]["Date I met"].split("/")[-1]

			# ---------- #

			# Create a local copy of the friend "Information" dictionary
			information = deepcopy(friend["Information"])

			# Remove the "Locations" key
			information.pop("Locations")

			# Translate the information keys into the user language
			# (The friend information values are already in the user language, so they do not need to be translated)
			information = self.Information(information, to_user_language = True)

			# Update the friend "Information.txt" file with the friend "Information" dictionary translated into the user language and converted to a text
			text_to_write = self.Text.From_Dictionary(information, next_line = True)

			self.File.Edit(friend["Files"]["Information"], text_to_write, "w")

			# ---------- #

			# Create a shortcut to the social networks folder of the friend
			folder = friend["Folders"]["Social networks"]["root"]

			# List the social networks of the friend
			social_networks = self.Folder.Contents(folder)["folder"]["names"]

			# Iterate through the list of social networks of the friend
			for item in social_networks.copy():
				# If the social network is not inside the root list of social networks (the "Social networks" database)
				if item not in self.social_networks["List"]:
					# Remove it from the list of social networks of the friend
					social_networks.remove(item)

			# Update the friend "Social networks.txt" file with the list above
			text_to_write = self.Text.From_List(social_networks)

			self.File.Edit(friend["Files"]["Social networks"]["List"], text_to_write, "w")

			# Create a "Social networks" dictionary for the friend
			friend["Social networks"] = {
				"Numbers": {
					"Total": 0
				},
				"List": social_networks,
				"Dictionary": {}
			}

			# ---------- #

			# Sort the list of social networks of the friend in alphabetical order, ignoring capitalization
			friend["Social networks"]["List"] = sorted(friend["Social networks"]["List"], key = str.lower)

			# Sort the dictionary of social networks of the friend by its keys in ascending order
			friend["Social networks"]["Dictionary"] = dict(collections.OrderedDict(sorted(friend["Social networks"]["Dictionary"].items())))

			# Iterate through the list of social networks of the friend
			for social_network in friend["Social networks"]["List"]:
				# Update the root "social network" with the dictionary of the current social network
				self.social_network = self.Select_Social_Network(social_network)

				# Define and create the social network folder
				folders = {
					"root": friend["Folders"]["Social networks"]["root"] + social_network + "/"
				}

				self.Folder.Create(folders["root"])

				# Define and create the social network "Profile.txt" file
				folders["Profile"] = folders["root"] + self.Language.language_texts["profile, title()"] + ".txt"
				self.File.Create(folders["Profile"])

				# Create a shortcut to the social network "Profile.txt" file
				file = folders["Profile"]

				# Add the social network folders dictionary to the friend "Folders" dictionary
				friend["Folders"]["Social networks"][social_network] = folders

				# Create the social network files inside the friend "Files" dictionary
				friend["Files"]["Social networks"][social_network] = {
					# And also add the social network "Profile.txt" file to it
					"Profile": file
				}

				# Define the parameters to use in the "Information" method of the "Social networks" class
				parameters = {
					"file": file,
					"information_items": self.social_network["Information items"]
				}

				# Run the "Information" method of the "Social Networks" class to get the social network information dictionary with the keys in English
				friend["Social networks"]["Dictionary"][social_network] = self.Social_Networks.Information(**parameters)

				# If the "Image folders" key is inside the social network dictionary
				if "Image folders" in self.social_network:
					# Define the root image folder
					image_folder = friend["Folders"]["Social networks"][social_network]["root"]

					# Create the social network image folders
					for folder in self.social_network["Image folders"]:
						# Define and create the image folder
						folder = image_folder + folder + "/"
						self.Folder.Create(folder)

			# Update the total number of social networks of the friend
			friend["Social networks"]["Numbers"]["Total"] = len(friend["Social networks"]["List"])

			# Define the root friend dictionary as the local friend dictionary
			self.friends["Dictionary"][name] = friend

		# ---------- #

		# Iterate through the list of friends
		for name in self.friends["List"]:
			# Get the friend dictionary
			friend = self.friends["Dictionary"][name]

			# Get the friend "Information" dictionary with its keys in English
			information = self.Information(friend["Information"])

			# Get the "met year" from the "Date I met"
			met_year = information["Date I met"].split("/")[-1]

			# If the met year is not in the friends numbers "By year" dictionary
			if met_year not in self.friends["Numbers"]["By year"]:
				# Add it
				self.friends["Numbers"]["By year"][met_year] = 1

			# Else, add one to it
			else:
				self.friends["Numbers"]["By year"][met_year] += 1

			# If the met year is not in the friends "Met by year" dictionary
			if met_year not in self.friends["Met by year"]:
				# Add the year list and the friend inside it
				self.friends["Met by year"][met_year] = [
					friend["Name"]
				]

			# Else, add the friend to the existing "Met by year" list
			else:
				if friend["Name"] not in self.friends["Met by year"][met_year]:
					self.friends["Met by year"][met_year].append(friend["Name"])

			# Remove the friend from other "Met by year" lists
			for year, met_by_year in self.friends["Met by year"].items():
				# If the year is not the met year
				# And the friend is inside the "Met by year" list
				if (
					year != met_year and
					friend["Name"] in met_by_year
				):
					# Remove the friend from the "Met by year" list
					self.friends["Met by year"][year].remove(friend["Name"])

		# Iterate through the years and numbers inside the "By year" dictionary
		for year, number in deepcopy(self.friends["Numbers"]["By year"]).items():
			# If the year is not the current one
			# And the friend count of the year is zero
			if (
				year != self.current_year and
				number == 0
			):
				# Remove the zero-count year
				self.friends["Numbers"]["By year"].pop(year)

		# Create a copy of the "Met by year" dictionary
		met_by_year = deepcopy(self.friends["Met by year"])

		# Iterate through the year lists inside the "Met by year" dictionary
		for year, year_list in met_by_year.items():
			# Iterate through the friends inside the year list
			for friend in year_list:
				# If the friend is not inside the year list
				if friend not in self.friends["List"]:
					# Remove the Friend
					self.friends["Met by year"][year].remove(friend)

		# Iterate through the year lists inside the "Met by year" dictionary
		for year, year_list in met_by_year.items():
			# If the year list is empty
			if year_list == []:
				# Remove it
				self.friends["Met by year"].pop(year)

			# Else, sort the list alphabetically, ignoring capitalization
			else:
				self.friends["Met by year"][year] = sorted(self.friends["Met by year"][year], key = str.lower)

		# Sort the "Met by year" numbers dictionary by their year keys in ascending order
		self.friends["Numbers"]["By year"] = dict(collections.OrderedDict(sorted(self.friends["Numbers"]["By year"].items())))

		# Sort the friends grouped by their year keys in ascending order
		self.friends["Met by year"] = dict(collections.OrderedDict(sorted(self.friends["Met by year"].items())))

		# Sort the list of friends by their names, alphabetically and ignoring capitalization
		self.friends["List"] = sorted(self.friends["List"], key = str.lower)

		# Sort the dictionary of friends alphabetically by its friend-name keys
		self.friends["Dictionary"] = dict(collections.OrderedDict(sorted(self.friends["Dictionary"].items())))

		# ---------- #

		# Create a local copy of the "Friends" dictionary
		local_dictionary = deepcopy(self.friends)

		# Remove the "File names" key
		local_dictionary.pop("File names")

		# Define a list of keys to remove
		to_remove = [
			"Folders",
			"Files",
			"Gender"
		]

		# Iterate through the friend names and dictionaries
		for name, friend in self.friends["Dictionary"].items():
			# Iterate through the list of keys to remove
			for key in to_remove:
				# If the key is inside the friend dictionary
				if key in friend:
					local_dictionary["Dictionary"][name].pop(key)

		# Update the "Friends.json" file with the updated and local copy of the "Friends" dictionary
		self.JSON.Edit(self.folders["Friends"]["Friends"], local_dictionary)

	def Information(self, information = None, file = None, information_items = None, to_user_language = False):
		# If the file parameter is not None, get the information dictionary from it
		if file != None:
			information = self.File.Dictionary(file, next_line = True)

		# If the information items parameter is None, define it as the default root information items dictionary
		if information_items == None:
			information_items = self.information_items

		# Define the local empty dictionary
		dictionary = {}

		# Iterate through the language keys and values of the information dictionary
		for information_key, value in information.items():
			# Define the correct (original) key
			correct_key = information_key

			# Iterate through the English keys and values of the root default information items dictionary
			for key, information_item in self.information_items["Dictionary"].items():
				# Get the language key of the information item
				language_key = information_item[self.language["Small"]]

				# If the local current (English) key is the same as the root (user language) key
				# Or the root (user language) key is the same as the language key
				if (
					key == information_key or
					information_key == language_key
				):
					# Define the correct key as the current English key
					correct_key = key

					# If the "to user language" parameter is True
					if to_user_language == True:
						# Define the key as the user language key
						correct_key = language_key

			# Add the information to the dictionary with the correct and selected key, be it English or user language
			dictionary[correct_key] = value

		# Return the information dictionary with the updated keys
		return dictionary

	def Select_File_Name(self):
		# Define the show and select text
		show_text = self.File.language_texts["file_names"]
		select_text = self.File.language_texts["select_one_file_name"]

		# Define the English options list
		options = list(self.friends["File names"]["Dictionary"].keys())

		# Define the language options list
		language_options = []

		for key, dict_ in self.friends["File names"]["Dictionary"].items():
			language_options.append(dict_["Plural"][self.language["Small"]])

		# Select a file name
		option = self.Input.Select(options, language_options = language_options, show_text = show_text, select_text = select_text)["option"]

		# Get the file name dictionary
		self.file_name = self.friends["File names"]["Dictionary"][option]

		return self.file_name

	def Select_Information_Item(self, information_items = None, information_item = None, type_information = True, type_text = None):
		# Get the information items dictionary if it is None
		if information_items == None:
			information_items = self.information_items

		# Define the Information items to be selected
		options = information_items["Lists"]["en"]

		# Remove the information items that wish to be removed
		if "Remove from search" in information_items["Lists"]:
			for item in information_items["Lists"]["Remove from search"]:
				options.remove(item)

		# Define the language options
		language_options = []

		for option in options:
			option = information_items["Dictionary"][option][self.language["Small"]]

			language_options.append(option)

		# If the "information_item" parameter is None
		if information_item == None:
			# Show a separator
			print()
			print(self.separators["5"])

		# Define the show and select text
		show_text = self.Language.language_texts["information_items"]
		select_text = self.Language.language_texts["select_the_information_item"]

		# If the "information_item" parameter is None
		if information_item == None:
			# Select an information item
			option = self.Input.Select(options, language_options = language_options, show_text = show_text, select_text = select_text)["option"]

		# Else, use the "information_item" parameter
		else:
			option = information_item

		# If the option is a string
		if type(option) == str:
			# Get the information item dictionary
			information_item = information_items["Dictionary"][option]

		# If the option is a dictionary
		if type(option) == dict:
			# Define the information item dictionary as the option dictionary
			information_item = option

		# Define the default information value
		information = ""

		# If the "type_information" is True
		if type_information == True:
			# Type the selected friend or social network information

			# If the information item is not inside the "Select" list
			if information_item["Name"] not in information_items["Lists"]["Select"]:
				if type_text == None:
					# Define the type text
					type_text = self.language_texts["type_{}"].format(information_item["Gender"]["Words"]["The"][self.language["Small"]] + " " + information_item[self.language["Small"]].lower())

				# Define the "accept_enter" variable
				accept_enter = False

				# Only accept enter if the information item is inside the "Accept enter" list
				# Or it has no format
				# And it is not the "Name" information item
				if (
					"Accept enter" in information_items["Lists"] and
					information_item["Name"] in information_items["Lists"]["Accept enter"] or
					information_item["Format"]["Regex"] == "" and
					information_item["Name"] != "Name"
				):
					accept_enter = True

				# If the "Accept enter" key is inside the Information items dictionary
				if "Accept enter" in information_items:
					# Update the "accept_enter" variable with its value
					accept_enter = information_items["Accept enter"]

				# If the information needs to be requested from the user:
				if information_item["States"]["Ask for information"] == True:
					# If the "Testing" switch is False
					# Or it is True
					# And the "Test information" dictionary exists
					# And the information item is not inside the "Test information" dictionary
					# Or the "Testing" switch is False
					# And the "Test information" dictionary does not exist
					if (
						self.switches["Testing"] == False
						or (
							self.switches["Testing"] == True and
							"Test information" in information_item and
							information_item["Name"] not in information_item["Test information"]
						)
						or (
							self.switches["Testing"] == True and
							"Test information" not in information_item
						)
					):
						# Ask the user for the information
						# Defining the "accept_enter" variable as the above value
						# Asking for input in the next line, to make it easier to read (next_line = True)
						# Adding a tab to push the input part more to the right
						# And forcing the format of the information item Regex, if it is not empty (regex = [Format])
						information = self.Input.Type(type_text, accept_enter = accept_enter, next_line = True, tab = "\t", regex = information_item["Format"])

					# If the "Testing" switch is True
					# And the "Test information" dictionary exists
					# And the information item is inside "Test information" dictionary
					if (
						self.switches["Testing"] == True and
						"Test information" in information_item and
						information_item["Name"] in information_item["Test information"]
					):
						# Define the information as the text information
						information = information_item["Test information"][information_item["Name"]]

					# If the information is empty
					if information == "":
						# Create a shortcut to the empty text and add brackets around it
						empty_text = "[{}]".format(self.Language.language_texts["empty, title()"])

						# Define the information as the empty text
						information = empty_text

						# If the "Testing" switch is False
						if self.switches["Testing"] == False:
							# Show the empty information
							print("\t" + information)

			# Else, ask user to select an item from the list of information
			else:
				# Get the "Select" dictionary of the information item
				select = information_item["Select"]

				select_text = select["Texts"]["Singular"]

				# If the information item is "Origin social network"
				if information_item["Name"] == "Origin social network":
					# Define the genders list for faster typing
					genders = self.Language.texts["genders, type: list"]

					# Iterate through the genders list
					i = 0
					for gender in genders[self.language["Small"]]:
						# If the language gender inside the list is the same as the gender of the friend
						if gender == information_item["Friend"]["Gender"]:
							# Get the Friend gender in English
							friend_gender = genders["en"][i].lower()

						i += 1

					# Define the "the friend" and select text
					the_friend_text = self.language_texts["the_friend" + ", " + friend_gender]

					select_text = self.language_texts["select_the_social_network_where_you_met_{}"].format(the_friend_text)

				# If the "Testing" switch is False
				# Or it is True
				# And the "Test information" dictionary exists
				# And the information item is not inside the "Test information" dictionary
				if (
					self.switches["Testing"] == False or
					self.switches["Testing"] == True and
					"Test information" in information_item and
					information_item["Name"] not in information_item["Test information"]
				):
					# Ask the user to select an item from the list of options
					information = self.Input.Select(select["List"]["English"], language_options = select["List"]["Language"], show_text = select["Texts"]["Plural"], select_text = select_text)

				# If the "Testing" switch is True
				# And the "Test information" dictionary exists
				# And the information item is inside "Test information" dictionary
				if (
					self.switches["Testing"] == True and
					"Test information" in information_item and
					information_item["Name"] in information_item["Test information"]
				):
					# Create a shortcut to the test information
					test_information = information_item["Test information"][information_item["Name"]]

					# Define the information dictionary as the test information
					information = {
						"option": test_information,
						"language_option": test_information
					}

				# If the selected option is "Custom social network"
				if information["option"] == "Custom social network":
					# Define the type text for the information item
					type_text = self.language_texts["type_{}"].format(information_item["Gender"]["Words"]["The"][self.language["Small"]] + " " + self.language_texts["custom_origin_social_network"])

					# If the "Testing" switch is False
					# Or it is True
					# And the "Test information" dictionary exists
					# And the "Custom social network" key is not inside the "Test information" dictionary
					if (
						self.switches["Testing"] == False or
						self.switches["Testing"] == True and
						"Test information" in information_item and
						"Custom social network" not in information_item["Test information"]
					):
						# Ask the user to type the information
						information = self.Input.Type(type_text, accept_enter = False, next_line = True, tab = "\t")

					# If the "Testing" switch is True
					# And the "Test information" dictionary exists
					# And the "Custom social network" key is inside "Test information" dictionary
					if (
						self.switches["Testing"] == True and
						"Test information" in information_item and
						"Custom social network" in information_item["Test information"]
					):
						information = information_item["Test information"]["Custom social network"]

				# Else, get the "language option" from the option dictionary
				else:
					information = information["language_option"]

				# If the information item is "Origin social network"
				if information_item["Name"] == "Origin social network":
					# Define the question text
					question = self.language_texts["add_additional_information_about_the_origin_social_network"]

					# Ask if the user wants to add additional information to the origin social network
					add_additional_information = True

					if self.switches["Testing"] == False:
						# Ask if the user wants to add additional information about the Origin social network
						add_additional_information = self.Input.Yes_Or_No(question = question)

					# If the user wants to add additional information
					if add_additional_information == True:
						information_key = "Additional information of origin social network"

						# Define the type text
						type_text = self.language_texts["type_the_additional_information"]

						# If the "Testing" switch is False
						# Or it is True
						# And the "Test information" dictionary exists
						# And the information key is not inside the "Test information" dictionary
						if (
							self.switches["Testing"] == False or
							self.switches["Testing"] == True and
							"Test information" in information_item and
							information_key not in information_item["Test information"]
						):
							# Ask the user to type the text
							text = self.Input.Type(type_text)

						# If the "Testing" switch is True
						# And the "Test information" dictionary exists
						# And the information key is inside the "Test information" dictionary
						if (
							self.switches["Testing"] == True and
							"Test information" in information_item and
							information_key in information_item["Test information"]
						):
							# Define the text as the test information
							text = information_item["Test information"][information_key]

						# Add the additional information
						information += " - " + text

		# If the "Testing" switch is True
		# And the information is not empty
		# And the "Test information" dictionary exists
		# And it is not empty
		if (
			self.switches["Testing"] == True and
			information != "" and
			"Test information" in information_item and
			information_item["Test information"] != {}
		):
			# Show a space, the information item name, and the information with a tab
			print()
			print(information_item[self.language["Small"]] + ":")
			print("\t" + information)

		# Return a dictionary with the information "Item" dictionary and the "Information" text (the value)
		return {
			"Item": information_item,
			"Information": information
		}

	def Select_Friend(self, friends_list = None, select_text = None, states = None):
		# Get the friends list if it is None
		if friends_list == None:
			friends_list = self.friends["List"]

		# Define the show and select text
		show_text = self.language_texts["friends, title()"]

		if select_text == None:
			select_text = self.language_texts["select_one_friend"]

		# Select the friend
		friend = self.Input.Select(friends_list, show_text = show_text, select_text = select_text)["option"]

		# Get the Friend dictionary
		self.friend = self.friends["Dictionary"][friend]

		# If the "states" parameter is not None
		# And the "Selected a Friend" state is inside the States dictionary
		if (
			states != None and
			"Selected a Friend" in states
		):
			# Update the value of the state to True
			states["Selected a Friend"] = True

		# Return the dictionary with the Friend and States dictionaries
		return {
			"Friend": self.friend,
			"States": states
		}
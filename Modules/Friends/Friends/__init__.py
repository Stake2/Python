# Friends.py

# Import the "importlib" module
import importlib

from copy import deepcopy

class Friends(object):
	def __init__(self):
		# Import the classes
		self.Import_Classes()

		# Define the folders of the module
		self.folders = self.Define_Folders(object = self).folders

		# Module related methods
		self.Define_Basic_Variables()
		self.Define_Texts()

		# Import the usage classes
		self.Import_Usage_Classes()

		# Folders and files method
		self.Define_Folders_And_Files()

		# Class methods

		# Define the "Information items" dictionary
		self.Define_Information_Items()

		# Define the "Friends" dictionary
		self.Define_Friends_Dictionary()

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

	def Import_Usage_Classes(self):
		# Define the classes to be imported
		classes = [
			"Social_Networks"
		]

		# Import them
		for title in classes:
			# Import the module
			module = importlib.import_module("." + title, title)

			# Get the sub-class
			sub_class = getattr(module, title)

			# Add the sub-class to the current module
			setattr(self, title, sub_class())

		# Define the "Social Networks" dictionary of this module as the "Social Networks" dictionary of the "Social_Networks" module
		self.social_networks = self.Social_Networks.social_networks

		# Get the "Select_Social_Network" method of the "Social_Networks" module
		self.Select_Social_Network = self.Social_Networks.Select_Social_Network

	def Define_Folders_And_Files(self):
		# Define the "Friends" folder dictionary
		self.folders["Friends"] = {
			"Text": {
				"root": self.folders["Notepad"]["Friends"]["root"]
			},
			"Image": {
				"root": self.folders["Image"]["Friends"]["root"]
			}
		}

		# ---------- #

		# Friends text "Database" folder
		self.folders["Friends"]["Text"]["Database"] = {
			"root": self.folders["Friends"]["Text"]["root"] + self.Language.language_texts["database, title()"] + "/"
		}

		self.Folder.Create(self.folders["Friends"]["Text"]["Database"]["root"])

		# Database "Information items.json" file
		self.folders["Friends"]["Text"]["Database"]["Information items"] = self.folders["Friends"]["Text"]["Database"]["root"] + "Information items.json"
		self.File.Create(self.folders["Friends"]["Text"]["Database"]["Information items"])

		# "Friends.json" file
		self.folders["Friends"]["Text"]["Friends"] = self.folders["Friends"]["Text"]["root"] + "Friends.json"
		self.File.Create(self.folders["Friends"]["Text"]["Friends"])

		# "Friends list.txt" file
		self.folders["Friends"]["Text"]["Friends list"] = self.folders["Friends"]["Text"]["root"] + self.language_texts["friends_list"] + ".txt"
		self.File.Create(self.folders["Friends"]["Text"]["Friends list"])

		# ---------- #

		# Define the "History" dictionary
		self.history = {
			"Key": "",
			"Numbers": {
				"Known people": "By year"
			},
			"Folder": self.folders["Friends"]["Text"]["root"]
		}

	def Define_Information_Items(self):
		# Define the "Information items" dictionary
		dictionary = {
			"Numbers": {
				"Total": 0
			},
			"List": [],
			"Lists": {
				"Exact match": [],
				"Select": [],
				"Do not ask for item": []
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

		# Read the "Information items.json" file if it is not empty
		file = self.folders["Friends"]["Text"]["Database"]["Information items"]

		if self.File.Contents(file)["lines"] != []:
			dictionary = self.JSON.To_Python(file)

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

			# Define the text addon
			addon = ""

			if "_" not in text_key:
				addon = ", title()"

			# Iterate through the small languages list
			for language in self.languages["small"]:
				# Get the information text
				text = self.Language.texts[text_key + addon][language]

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

			# Update the back of the text key
			text_key_backup = text_key + addon

			if "s" not in text_key[-1]:
				text_key += "s"

			# Add the text addon (might be a empty string or the ", title()" text)
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
				"Select": False,
				"Ask for information": True
			}

			# If the information item is inside the "Do not ask for item" list
			if key in dictionary["Lists"]["Do not ask for item"]:
				dict_["States"]["Ask for information"] = False

			# Create a local copy of the "States" dictionary
			states = deepcopy(dict_["States"])
			states.pop("Ask for information")

			# Iterate through the state keys
			for state in states:
				# Update the value of the key to True
				if key in dictionary["Lists"][state]:
					dict_["States"][state] = True

			# Define the options list if the information item needs to be selected from a list
			if dict_["States"]["Select"] == True:
				# Define the "Select" dictionary
				dict_["Select"] = {
					"List": {
						"English": [],
						"Language": []
					},
					"Texts": {
						"Singular": dict_[self.user_language],
						"Plural": dict_["Plural"][self.user_language]
					}
				}

				# If the information item key is not "Origin Social Network"
				if key != "Origin Social Network":
					# Define the text key for the options list
					text_key = dict_["Plural"]["en"].lower().replace(" ", "_") + ", type: list"

					# Define the object from where the "texts" dictionary will be gotten
					object = self.Language

					# Define the lists of options
					for item in dict_["Select"]["List"]:
						# Define the local texts dictionary
						language = "en"

						if item == "Language":
							language = self.user_language

						# Define the lists of options inside the "List" key
						dict_["Select"]["List"][item] = object.texts[text_key][language]

				# If the information item key is "Origin Social Network"
				if key == "Origin Social Network":
					# Iterate through the keys of the "List" dictionary
					for item in dict_["Select"]["List"]:
						# Define the local list of Social Networks
						social_networks = deepcopy(self.social_networks)

						language = "en"

						if item == "Language":
							language = self.user_language

						# Add the "Custom Social Network" item to the list above
						social_networks["List"].append(self.texts["custom_social_network"][language])

						# Define the lists of options inside the "List" key
						dict_["Select"]["List"][item] = social_networks["List"]

					dict_["Select"]["Texts"]["Custom select text"] = self.language_texts["select_the_social_network_where_you_met_{}"]

			# Add the information item dictionary to the root "Information items" dictionary
			dictionary["Dictionary"][key] = dict_

		# Iterate through the information items list
		for key, dict_ in dictionary["Dictionary"].items():
			# Define the local gender "Words" dictionary
			dict_ = {}

			# Define the gender words of the information item
			for item in dictionary["Gender"]["Items"]:
				text_key = item.lower().replace(" ", "_")

				# Define the gender
				if key in dictionary["Gender"]["Masculine"]:
					gender = "masculine"

				if key in dictionary["Gender"]["Feminine"]:
					gender = "feminine"

				# Get the gender words dictionary
				dict_[item] = self.Language.texts["genders, type: dict"][self.user_language][gender][text_key]

				# Define the gender inside the "Gender" dictionary
				dictionary["Dictionary"][key]["Gender"]["Text"] = gender

			# Update the gender "Words" dictionary inside the root information item dictionary
			dictionary["Dictionary"][key]["Gender"]["Words"] = dict_

		# Define the "Information items" dictionary as the local "Information items" dictionary
		self.information_items = dictionary

		# Create a local "Information items" dictionary
		local_dictionary = deepcopy(self.information_items)

		# Iterate through the small languages list
		for language in self.languages["small"]:
			# Remove the language items lists
			local_dictionary["Lists"].pop(language)

		# Update the "Information items.json" file with the updated and local "Information items" dictionary
		self.JSON.Edit(self.folders["Friends"]["Text"]["Database"]["Information items"], local_dictionary)

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

		# Read the "Friends.json" file if it is not empty
		file = self.folders["Friends"]["Text"]["Friends"]

		if self.File.Contents(file)["lines"] != []:
			self.friends = self.JSON.To_Python(file)

		# ---------- #

		# Define the default "File names" dictionary
		dictionary = {
			"Names": [
				"Information",
				"Social Network"
			],
			"Dictionary": {}
		}

		# Iterate through the file names list
		for file_name in dictionary["Names"]:
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

			if "s" not in text_key[-1]:
				text_key += "s"

			# Define the plural texts of the file name
			dict_["Plural"] = {}

			# Iterate through the small languages list
			for language in self.languages["small"]:
				dict_["Plural"][language] = self.Language.texts[text_key + addon][language]

			# Add the file name dictionary to the root "File names" dictionary
			dictionary["Dictionary"][file_name] = dict_

		# Define the "File names" key as the local "File names" dictionary
		self.friends["File names"] = dictionary

		# ---------- #

		# Get the list of social networks
		self.friends["List"] = self.JSON.To_Python(self.folders["Friends"]["Text"]["Friends"])["List"]

		# Write the friends list to the "Friends list.txt" file
		text_to_write = self.Text.From_List(self.friends["List"], break_line = True)

		self.File.Edit(self.folders["Friends"]["Text"]["Friends list"], text_to_write, "w")

		# Get the number of friends
		self.friends["Numbers"]["Total"] = len(self.friends["List"])

		# Add all years since 2018 to the "By year" list
		for year in self.Date.Create_Years_List(function = str):
			self.friends["Numbers"]["By year"][year] = 0

		# Reset the numbers on the "By year" dictionary to zero
		for year in self.friends["Numbers"]["By year"]:
			self.friends["Numbers"]["By year"][year] = 0

		# ---------- #

		import collections

		# Reset the Friends dictionary
		self.friends["Dictionary"] = {}

		# Iterate through the friends list
		for friend in self.friends["List"]:
			# Create the local "Friend" dictionary
			dictionary = {
				"Name": friend,
				"Folders": {},
				"Files": {},
				"Information": {},
				"Social Networks": {},
				"Gender": {
					"Text": "",
					"Words": {}
				}
			}

			# Iterate through the folder type list
			for item in ["Text", "Image"]:
				# Define the item key inside the "Files" dictionary
				dictionary["Files"][item] = {}

				# Define the root folder
				folder = self.folders["Friends"][item]["root"] + friend + "/"

				# Create the folders dictionary
				dict_ = {
					"root": folder
				}

				self.Folder.Create(dict_["root"])

				# Create the "Social Networks" folder
				dict_["Social Networks"] = {
					"root": dict_["root"] + self.Language.language_texts["social_networks"] + "/"
				}

				self.Folder.Create(dict_["Social Networks"]["root"])

				# Iterate through the friend file names
				for key, file_name_dictionary in self.friends["File names"]["Dictionary"].items():
					# Define the file name and folder
					file_name = file_name_dictionary["Plural"][self.user_language]

					folder_dictionary = dict_

					# Define the folder for the "Social Networks.txt" file
					if key == "Social Network":
						folder_dictionary = dict_["Social Networks"]

						key = file_name_dictionary["Plural"]["en"]

					# Define the file and create it
					folder_dictionary[key] = folder_dictionary["root"] + file_name + ".txt"
					self.File.Create(folder_dictionary[key])

					# Add the file to the "Files" dictionary
					dictionary["Files"][item][key] = folder_dictionary[key]

					# If the item is "Text"
					if item == "Text":
						# Add the file to the "Files" dictionary
						if key == "Information":
							dictionary["Files"][key] = folder_dictionary[key]

						# Add the file to the "Files" dictionary
						if key == "Social Networks":
							dictionary["Files"][key] = {
								"List": folder_dictionary[key]
							}

				if item == "Image":
					# Create the image "Media" folder
					dict_["Media"] = {
						"root": dict_["root"] + self.Language.language_texts["media, title()"] + "/"
					}

					self.Folder.Create(dict_["Media"]["root"])

				# Define the folders dictionary as the local folders dictionary
				dictionary["Folders"][item] = dict_

			# Add the keys of the "Text" folders dictionary to the root folders dictionary
			dictionary["Folders"].update(dictionary["Folders"]["Text"])

			# Update the Friend "Information" only with the data on the files inside the Text folder
			# To get the most up-to-date information

			# Get the information dictionary
			information = self.Information(file = dictionary["Files"]["Information"])

			# Add the information to the "Information" dictionary
			for information_key, value in information.items():
				dictionary["Information"][information_key] = value

			# Create the "Places" dictionary
			places = {
				"Hometown": {},
				"Residence": {}
			}

			items = [
				"City",
				"State",
				"Country"
			]

			# Itearate through the places
			for place in places.copy():
				key = place

				if key == "Residence":
					key += " place"

				split = dictionary["Information"][key].split(" - ")

				# Itearate through the place items
				i = 0
				for item in split:
					key = items[i]

					places[place][key] = split[i]

					i += 1

			# Add the "Places" dictionary to the friend "Information" dictionary
			# After the "Residence place" key
			key_value = {
				"Places": places
			}

			dictionary["Information"] = self.JSON.Add_Key_After_Key(information, key_value, after_key = "Residence place")

			# Add the "Year I met" key
			dictionary["Information"]["Year I met"] = dictionary["Information"]["Date I met"].split("/")[-1]

			# ---------- #

			# Make a local copy of the Friend "Information" dictionary
			information = deepcopy(dictionary["Information"])

			# Remove the "Places" key
			information.pop("Places")

			# Translate the keys to the user language
			information = self.Information(information, to_user_language = True)

			# Iterate through the folder type list
			for item in ["Text", "Image"]:
				# Write to the "Information.txt" file
				text_to_write = self.Text.From_Dictionary(information, next_line = True)

				self.File.Edit(dictionary["Files"][item]["Information"], text_to_write, "w")

			# ---------- #

			# List the Social Networks
			social_networks_list = self.Folder.Contents(dictionary["Folders"]["Social Networks"]["root"])["folder"]["names"]

			# Remove the Social Networks that are not inside the Social Networks database
			for item in social_networks_list.copy():
				if item not in self.social_networks["List"]:
					social_networks_list.remove(item)

			# Update the "Social Networks.txt" file with the list above
			text_to_write = self.Text.From_List(social_networks_list, break_line = True)

			self.File.Edit(dictionary["Files"]["Social Networks"]["List"], text_to_write, "w")

			# Create a "Social Networks" information dictionary
			dictionary["Social Networks"] = {
				"Numbers": {
					"Total": 0
				},
				"List": social_networks_list,
				"Dictionary": {}
			}

			# ---------- #

			# Update the "Information" and "Social Networks" files of the Friend image folder if the file inside the text folder is different
			for file_name in ["Information", "Social Networks"]:
				files = {}

				for item in ["Text", "Image"]:
					file = dictionary["Files"][item][file_name]

					files[item] = {
						"File": file,
						"Size": self.File.Contents(file)["size"]
					}

				if files["Text"]["Size"] != files["Image"]["Size"]:
					self.File.Copy(files["Text"]["File"], files["Image"]["File"])

			# ---------- #

			# Sort the Social Networks list
			dictionary["Social Networks"]["List"] = sorted(dictionary["Social Networks"]["List"], key = str.lower)

			# Sort the Social Networks dictionary
			dictionary["Social Networks"]["Dictionary"] = dict(collections.OrderedDict(sorted(dictionary["Social Networks"]["Dictionary"].items())))

			# Social Network folders and profile file creation
			for social_network in dictionary["Social Networks"]["List"]:
				# Update the "self.social_network" variable
				self.social_network = self.Select_Social_Network(social_network)

				# Create the empty "dict_" dictionary for the social network folders
				dict_ = {}

				# Create the empty "Files" dictionary
				files = {}

				# Create the Social Network folders
				for item in ["Text", "Image"]:
					# Create the item folders dictionary
					dict_ = {
						"root": dictionary["Folders"][item]["Social Networks"]["root"] + social_network + "/"
					}

					self.Folder.Create(dict_["root"])

					# Create the "Profile.txt" file
					dict_["Profile"] = dict_["root"] + self.Language.language_texts["profile, title()"] + ".txt"

					self.File.Create(dict_["Profile"])

					# Add the profile file to the "Files" dictionary
					dictionary["Files"]["Social Networks"][social_network] = {
						"Profile": dict_["Profile"]
					}

					# Define the file for easier typing
					file = dict_["Profile"]

					# Define the File dictionary and size
					files[item] = {
						"File": file,
						"Size": self.File.Contents(file)["size"]
					}

					dictionary["Folders"][item]["Social Networks"][social_network] = dict_

				# Update the "Profile" social network file of the Friend image folder if the file inside the text folder is different
				if files["Text"]["Size"] != files["Image"]["Size"]:
					self.File.Copy(files["Text"]["File"], files["Image"]["File"])

				# Get the data of the Social Network
				file = dictionary["Files"]["Social Networks"][social_network]["Profile"]

				dictionary["Social Networks"]["Dictionary"][social_network] = self.Information(file = file, information_items = self.social_network["Information items"])

				# Create the Social Network image sub-folders
				if "Image folders" in self.social_network:
					# Define the root image folder
					image_folder = dictionary["Folders"]["Image"]["Social Networks"][social_network]["root"]

					# Create the image sub-folders
					for folder in self.social_network["Image folders"]:
						folder = image_folder + folder + "/"
	
						self.Folder.Create(folder)

			# Update the number of Social Networks
			dictionary["Social Networks"]["Numbers"]["Total"] = len(dictionary["Social Networks"]["List"])

			# Define the "Friend" dictionary as the local "Friend" dictionary
			self.friends["Dictionary"][friend] = dictionary

		# ---------- #

		# Iterate through the friends list
		for friend in self.friends["List"]:
			# Get the Friend dictionary
			friend = self.friends["Dictionary"][friend]

			# Get the Friend Information dictionary
			information = self.Information(friend["Information"])

			# Get the met year
			met_year = information["Date I met"].split("/")[-1]

			# If the met year is not in the Friends "Numbers" dictionary
			if met_year not in self.friends["Numbers"]["By year"]:
				# Add it
				self.friends["Numbers"]["By year"][met_year] = 1

			# Else, add one to it
			else:
				self.friends["Numbers"]["By year"][met_year] += 1

			# If the met year is not in the Friends "Met by year" dictionary
			if met_year not in self.friends["Met by year"]:
				# Add it
				self.friends["Met by year"][met_year] = [
					friend["Name"]
				]

			# Else, add the friend to the existing met by year list
			else:
				if friend["Name"] not in self.friends["Met by year"][met_year]:
					self.friends["Met by year"][met_year].append(friend["Name"])

			# Remove the friend from other "Met by year" lists
			for year, list_ in self.friends["Met by year"].items():
				# If the year is not the meat year
				# And the friend is inside the list
				if (
					year != met_year and
					friend["Name"] in list_
				):
					self.friends["Met by year"][year].remove(friend["Name"])

		# Iterate through the year numbers inside the "By year" dictionary
		for year in self.friends["Numbers"]["By year"].copy():
			# If the year is before "2018"
			# And a "Met by year" list of the year does not exist
			if (
				int(year) < 2018 and
				year not in self.friends["Met by year"]
			):
				# Remove its key
				self.friends["Numbers"]["By year"].pop(year)

		# Iterate through the year lists inside the "Met by year" dictionary
		for year, list_ in self.friends["Met by year"].copy().items():
			# Iterate through the friends inside the year list
			for friend in list_:
				# If the Friend is not inside the year list
				if friend not in self.friends["List"]:
					# Remove the Friend
					self.friends["Met by year"][year].remove(friend)

		# Iterate through the year lists inside the "Met by year" dictionary
		for year, list_ in self.friends["Met by year"].copy().items():
			# If the year list is empty
			if list_ == []:
				# Remove it
				self.friends["Met by year"].pop(year)

			else:
				# Sort the list
				self.friends["Met by year"][year] = sorted(self.friends["Met by year"][year], key = str.lower)

		# Sort the met by year numbers keys
		self.friends["Numbers"]["By year"] = dict(collections.OrderedDict(sorted(self.friends["Numbers"]["By year"].items())))

		# Sort the met by year lists keys
		self.friends["Met by year"] = dict(collections.OrderedDict(sorted(self.friends["Met by year"].items())))

		# Sort the Friends list
		self.friends["List"] = sorted(self.friends["List"], key = str.lower)

		# Sort the Friends dictionary
		self.friends["Dictionary"] = dict(collections.OrderedDict(sorted(self.friends["Dictionary"].items())))

		# ---------- #

		# List the folders inside the Friends image folder
		image_folders = self.Folder.Contents(self.folders["Friends"]["Image"]["root"])["folder"]["dictionary"]

		# Remove the non-friend folders from the above list
		to_remove = [
			"Arquivo",
			"Rubbish"
		]

		# Iterate through the "items to remove" list
		for item in to_remove:
			# If the item is inside the image folders dictionary
			if item in image_folders:
				# Remove it
				image_folders.pop(item)

		# Iterate through the image folders dictionary
		for key, folder in image_folders.items():
			if key not in self.friends["List"]:
				self.Folder.Delete(folder)

		# ---------- #

		# Create a local "Friends" dictionary
		local_dictionary = deepcopy(self.friends)

		# Remove the "File names" key
		local_dictionary.pop("File names")

		# Define the keys to remove
		to_remove = [
			"Folders",
			"Files",
			"Gender"
		]

		# Iterate through the friends list
		for friend in self.friends["List"]:
			# Remove the unused keys
			for key in to_remove:
				local_dictionary["Dictionary"][friend].pop(key)

		# Update the "Friends.json" file with the updated and local "Friends" dictionary
		self.JSON.Edit(self.folders["Friends"]["Text"]["Friends"], local_dictionary)

	def Information(self, information = None, file = None, information_items = None, to_user_language = False):
		if file != None:
			information = self.File.Dictionary(file, next_line = True)

		if information_items == None:
			information_items = self.information_items

		dictionary = {}

		for information_key, value in information.items():
			correct_key = ""

			for key, information_item in information_items["Dictionary"].items():
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

	def Select_File_Name(self):
		# Define the show and select text
		show_text = self.File.language_texts["file_names"]
		select_text = self.File.language_texts["select_one_file_name"]

		# Define the English options list
		options = list(self.friends["File names"]["Dictionary"].keys())

		# Define the language options list
		language_options = []

		for key, dict_ in self.friends["File names"]["Dictionary"].items():
			language_options.append(dict_["Plural"][self.user_language])

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

		language_options = []

		for option in options:
			option = information_items["Dictionary"][option][self.user_language]

			language_options.append(option)

		# If the "information_item" parameter is None
		if information_item == None:
			# Show a separator
			print()
			print(self.separators["5"])

		# Define the show and select text
		show_text = self.Language.language_texts["information_items"]
		select_text = self.language_texts["select_the_information_item"]

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
			# Type the selected Friend or Social Network information

			# If the information item is not inside the "Select" list
			if information_item["Name"] not in information_items["Lists"]["Select"]:
				if type_text == None:
					# Define the type text
					type_text = self.language_texts["type_{}"].format(information_item["Gender"]["Words"]["The"] + " " + information_item[self.user_language].lower())

				# Define the "accept_enter" variable
				accept_enter = False

				if information_item["Format"]["Regex"] == "":
					accept_enter = True

				# Only accept enter if the information item has no format
				# And it is not the "Name" information item
				if (
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
					# If the "testing" switch is False
					# Or it is True and the information item is not inside the "Test information" dictionary
					if (
						self.switches["Testing"] == False or
						self.switches["Testing"] == True and
						information_item["Name"] not in information_item["Test information"]
					):
						# Ask the user for the information
						# Defining the "accept_enter" variable as the above value
						# Asking for input in the next line, to make it easier to read (next_line = True)
						# Adding a tab to push the input part more to the right
						# And forcing the format of the information item Regex, if it is not empty (regex = [Format])
						information = self.Input.Type(type_text, accept_enter = accept_enter, next_line = True, tab = "\t", regex = information_item["Format"])

					# If the "testing" switch is True
					# And the information item is inside "Test information" dictionary
					if (
						self.switches["Testing"] == True and
						information_item["Name"] in information_item["Test information"]
					):
						information = information_item["Test information"][information_item["Name"]]

					# Define the information as "[Empty]" if it is empty
					if information == "":
						information = "[{}]".format(self.Language.language_texts["empty, title()"])

			# Else, ask user to select an item from the list of information
			else:
				# Get the "Select" dictionary of the information item
				select = information_item["Select"]

				select_text = select["Texts"]["Singular"]

				# If the information item is "Origin Social Network"
				if information_item["Name"] == "Origin Social Network":
					# Define the genders list for easier typing
					genders = self.Language.texts["genders, type: list"]

					# Iterate through the genders list
					i = 0
					for gender in genders[self.user_language]:
						# If the language gender inside the list is the same as the gender of the friend
						if gender == information_item["Friend"]["Gender"]:
							# Get the Friend gender in English
							friend_gender = genders["en"][i].lower()

						i += 1

					# Define the "the friend" and select text
					the_friend_text = self.language_texts["the_friend" + ", " + friend_gender]

					select_text = self.language_texts["select_the_social_network_where_you_met_{}"].format(the_friend_text)

				# If the "testing" switch is False
				# Or it is True and the information item is not inside the "Test information" dictionary
				if (
					self.switches["Testing"] == False or
					self.switches["Testing"] == True and
					information_item["Name"] not in information_item["Test information"]
				):
					# Ask the user to select an item from the list of options
					information = self.Input.Select(select["List"]["English"], language_options = select["List"]["Language"], show_text = select["Texts"]["Plural"], select_text = select_text)

				# If the "testing" switch is True
				# And the information item is inside "Test information" dictionary
				if (
					self.switches["Testing"] == True and
					information_item["Name"] in information_item["Test information"]
				):
					information = {
						"option": information_item["Test information"][information_item["Name"]],
						"language_option": information_item["Test information"][information_item["Name"]]
					}

				# If the selected option is "Custom Social Network"
				if information["option"] == "Custom Social Network":
					# Define the type text for the information item
					type_text = self.language_texts["type_{}"].format(information_item["Gender"]["Words"]["The"] + " " + self.language_texts["custom_origin_social_network"])

					# If the "testing" switch is False
					# Or it is True and the "Custom Social Network" key is not inside the "Test information" dictionary
					if (
						self.switches["Testing"] == False or
						self.switches["Testing"] == True and
						"Custom Social Network" not in information_item["Test information"]
					):
						# Ask the user to type the information
						information = self.Input.Type(type_text, accept_enter = False, next_line = True, tab = "\t")

					# If the "testing" switch is True
					# And the "Custom Social Network" key is inside "Test information" dictionary
					if (
						self.switches["Testing"] == True and
						"Custom Social Network" in information_item["Test information"]
					):
						information = information_item["Test information"]["Custom Social Network"]

				# Else, get the "language option" from the option dictionary
				else:
					information = information["language_option"]

				# If the information item is "Origin Social Network"
				if information_item["Name"] == "Origin Social Network":
					# Define the question text
					question = self.language_texts["add_additional_information_about_the_origin_social_network"]

					# Ask if the user wants to add additional information to the origin Social Network
					add_additional_information = True

					if self.switches["Testing"] == False:
						# Ask if the user wants to add additional information about the Origin Social Network
						add_additional_information = self.Input.Yes_Or_No(question = question)

					# If the user wants to add additional information
					if add_additional_information == True:
						information_key = "Additional information of Origin Social Network"

						# Define the type text
						type_text = self.language_texts["type_the_additional_information"]

						if (
							self.switches["Testing"] == False or
							self.switches["Testing"] == True and
							information_key not in information_item["Test information"]
						):
							# Ask for the additional information
							text = self.Input.Type(type_text)

						if (
							self.switches["Testing"] == True and
							information_key in information_item["Test information"]
						):
							text = information_item["Test information"][information_key]

						# Add the additional information
						information += " - " + text

		# Show the information item and information if the "testing" switch is True
		if (
			self.switches["Testing"] == True and
			information != "" and
			information_item["Test information"] != {}
		):
			print()
			print(information_item[self.user_language] + ":")
			print("\t" + information)

		# Return the dictionary with the Information item dictionary and the information text
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
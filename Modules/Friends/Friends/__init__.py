# Friends.py

# Import the "importlib" module
import importlib

from copy import deepcopy

class Friends(object):
	def __init__(self, current_year = None, social_network = None, remove_social_networks_with_no_friends = False):
		# Define the module folders
		from Utility.Define_Folders import Define_Folders as Define_Folders

		Define_Folders(self)

		if current_year != None:
			self.date["Units"]["Year"] = current_year

		if social_network != None:
			self.social_network = social_network

		# Import classes method
		self.Import_Classes()

		# Module related methods
		self.Define_Basic_Variables()
		self.Define_Texts()

		# Folders and files method
		self.Define_Folders_And_Files()

		# Class methods
		self.Define_Information_Items()
		self.Define_Friends_Dictionary()

	def Import_Classes(self):
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

			# Add the sub-clas to the current module
			setattr(self, title, sub_class())

		# Create the Social Networks dictionary
		self.social_networks = self.Social_Networks.social_networks

	def Define_Basic_Variables(self):
		from copy import deepcopy

		# Import the JSON module
		from Utility.JSON import JSON as JSON

		self.JSON = JSON()

		# Get the modules list
		self.modules = self.JSON.To_Python(self.folders["apps"]["modules"]["modules"])

		# Create a list of the modules that will not be imported
		remove_list = [
			"Define_Folders",
			"JSON",
			"Language"
		]

		# Iterate through the Utility modules
		for module_title in self.modules["Utility"]["List"]:
			# If the module title is not inside the remove list
			if module_title not in remove_list:
				# Import the module
				module = importlib.import_module("." + module_title, "Utility")

				# Get the sub-class
				sub_class = getattr(module, module_title)

				# Add the sub-clas to the current module
				setattr(self, module_title, sub_class())

		# Make a backup of the module folders
		self.module_folders = {}

		for item in ["modules", "module_files"]:
			self.module_folders[item] = deepcopy(self.folders["apps"][item][self.module["key"]])

		# Define the local folders dictionary as the Folder folders dictionary
		self.folders = self.Folder.folders

		# Restore the backup of the module folders
		for item in ["modules", "module_files"]:
			self.folders["apps"][item][self.module["key"]] = self.module_folders[item]

		# Get the switches dictionary from the "Global Switches" module
		self.switches = self.Global_Switches.switches["Global"]

		# Get the Languages dictionary
		self.languages = self.JSON.Language.languages

		# Get the user language and full user language
		self.user_language = self.JSON.Language.user_language
		self.full_user_language = self.JSON.Language.full_user_language

		# Get the Sanitize method of the File class
		self.Sanitize = self.File.Sanitize

		# Get the current date from the Date module
		self.date = self.Date.date

	def Define_Texts(self):
		self.texts = self.JSON.To_Python(self.folders["apps"]["module_files"][self.module["key"]]["texts"])

		self.language_texts = self.JSON.Language.Item(self.texts)

		self.large_bar = "-----"
		self.dash_space = "-"

	def Define_Folders_And_Files(self):
		# Define the "Friends" folder dictionary
		self.folders["Friends"] = {
			"Text": {
				"root": self.folders["notepad"]["friends"]["root"]
			},
			"Image": {
				"root": self.folders["mega"]["image"]["friends"]["root"]
			}
		}

		# Friends text "Database" folder
		self.folders["Friends"]["Text"]["Database"] = {
			"root": self.folders["Friends"]["Text"]["root"] + "Database/"
		}

		self.Folder.Create(self.folders["Friends"]["Text"]["Database"]["root"])

		# Database "Information items.json" file
		self.folders["Friends"]["Text"]["Database"]["Information items"] = self.folders["Friends"]["Text"]["Database"]["root"] + self.JSON.Language.texts["information_items"]["en"] + ".json"
		self.File.Create(self.folders["Friends"]["Text"]["Database"]["Information items"])

		# "Friends.json" file
		self.folders["Friends"]["Text"]["Friends"] = self.folders["Friends"]["Text"]["root"] + "Friends.json"
		self.File.Create(self.folders["Friends"]["Text"]["Friends"])

		# "Friends list.txt" file
		self.folders["Friends"]["Text"]["Friends list"] = self.folders["Friends"]["Text"]["root"] + self.language_texts["friends_list"] + ".txt"
		self.File.Create(self.folders["Friends"]["Text"]["Friends list"])

		# Define the "History" dictionary
		self.history = {
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
				"Select": []
			},
			"Genders": {
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

		# Define the "Exact match" information items list
		dictionary["Lists"]["Exact match"] = [
			self.JSON.Language.texts["name, title()"]["en"],
			self.JSON.Language.texts["age, title()"]["en"],
			self.JSON.Language.texts["hometown, title()"]["en"],
			self.JSON.Language.texts["residence_place"]["en"]
		]

		# Reset the "Dictionary" key to be an empty dictionary
		dictionary["Dictionary"] = {}

		# Iterate through the information items list
		for key in dictionary["List"]:
			# Create the information item dictionary
			dict_ = {}

			# Define the text key
			text_key = key.lower().replace(" ", "_")

			addon = ""

			if "_" not in text_key:
				addon = ", title()"

			# Iterate through the small languages list
			for language in self.languages["small"]:
				text = self.JSON.Language.texts[text_key + addon][language]

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

			if text_key not in self.JSON.Language.texts:
				text_key = text_key.replace(addon, "")
				text_key = text_key[:-1]

				text_key += addon + ", type: plural"

			if text_key not in self.JSON.Language.texts:
				text_key = text_key_backup

			# Iterate through the small languages list
			for language in self.languages["small"]:
				dict_["Plural"][language] = self.JSON.Language.texts[text_key][language]

			# Define the "Genders" key"
			dict_["Genders"] = {}

			# Define the format of the information item
			dict_["Format"] = ""

			if key in dictionary["Formats"]:
				dict_["Format"] = dictionary["Formats"][key]

			# Define the "States" dictionary of the information item
			dict_["States"] = {
				"Exact match": False,
				"Select": False
			}

			# Iterate through the state keys
			for state in dict_["States"]:
				# Update the value of the key to True
				if state in dictionary["Lists"][state]:
					dict_["States"][state] = True

			# Add the information item dictionary to the root "Information items" dictionary
			dictionary["Dictionary"][key] = dict_

		# Iterate through the information items list
		for key, dict_ in dictionary["Dictionary"].items():
			# Define the local gender "Words" dictionary
			dict_ = {}

			# Define the gender words of the information item
			for item in dictionary["Genders"]["Items"]:
				text_key = item.lower().replace(" ", "_")

				# Define the gender
				if key in dictionary["Genders"]["Masculine"]:
					gender = "masculine"

				if key in dictionary["Genders"]["Feminine"]:
					gender = "feminine"

				dict_[item] = self.JSON.Language.texts["genders, type: dict"][self.user_language][gender][text_key]

			# Update the gender "Words" dictionary inside the root information item dictionary
			dictionary["Dictionary"][key]["Genders"]["Words"] = dict_

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
				dict_[language] = self.JSON.Language.texts[text_key + addon][language]

			if "s" not in text_key[-1]:
				text_key += "s"

			# Define the plural texts of the file name
			dict_["Plural"] = {}

			# Iterate through the small languages list
			for language in self.languages["small"]:
				dict_["Plural"][language] = self.JSON.Language.texts[text_key + addon][language]

			# Add the file name dictionary to the root "File names" dictionary
			dictionary["Dictionary"][file_name] = dict_

		# Define the "File names" key as the local "File names" dictionary
		self.friends["File names"] = dictionary

		# List the friend folders, populating the friends list
		self.friends["List"] = self.Folder.Contents(self.folders["Friends"]["Text"]["root"])["folder"]["names"]

		# Remove the non-friend folders from the above list
		to_remove = [
			"Archive",
			"Database"
		]

		for item in to_remove:
			if item in self.friends["List"]:
				self.friends["List"].remove(item)

		# Write the friends list to the "Friends list.txt" file
		text_to_write = self.Text.From_List(self.friends["List"])

		self.File.Edit(self.folders["Friends"]["Text"]["Friends list"], text_to_write, "w")

		# Get the number of friends
		self.friends["Numbers"]["Total"] = len(self.friends["List"])

		# Check if all the years are inside the friends met by year list
		for year in self.Date.Create_Years_List(function = str):
			self.friends["Numbers"]["By year"][year] = 0

			if year not in self.friends["Met by year"]:
				self.friends["Met by year"][year] = []

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

		import collections

		# Sort the met by year numbers keys
		self.friends["Numbers"]["By year"] = dict(collections.OrderedDict(sorted(self.friends["Numbers"]["By year"].items())))

		# Sort the met by year lists keys
		self.friends["Met by year"] = dict(collections.OrderedDict(sorted(self.friends["Met by year"].items())))

		# ---------- #

		# Iterate through the friends list
		for friend in self.friends["List"]:
			# Create the "Friend" dictionary
			dictionary = {
				"Name": friend,
				"Folders": {},
				"Files": {},
				"Information": {},
				"Social Networks": {}
			}

			# Define and create the friend folders and files
			for item in ["Text", "Image"]:
				# Define the item key inside the "Files" dictionary
				dictionary["Files"][item] = {}

			# Define and create the friend folders and files
			for item in ["Text", "Image"]:
				folder = self.folders["Friends"][item]["root"] + friend + "/"

				# Create the folders dictionary
				dict_ = {
					"root": folder
				}

				self.Folder.Create(dict_["root"])

				# Create the "Social Networks" folder
				dict_["Social Networks"] = {
					"root": dict_["root"] + self.JSON.Language.language_texts["social_networks"] + "/"
				}

				self.Folder.Create(dict_["Social Networks"]["root"])

				# Iterate through the friend file names
				for key in self.friends["File names"]["Dictionary"]:
					file_name_dictionary = self.friends["File names"]["Dictionary"][key]

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

					dictionary["Files"][item][key] = folder_dictionary[key]

					# If the item is "Text"
					if item == "Text":
						# Add the file to the "Files" dictionary
						if key == "Information":
							dictionary["Files"][key] = folder_dictionary[key]

						if key == "Social Networks":
							dictionary["Files"][key] = {
								"List": folder_dictionary[key]
							}

				if item == "Image":
					# Create the image "Media" folder
					dict_["Media"] = {
						"root": dict_["root"] + self.JSON.Language.language_texts["media, title()"] + "/"
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

			# List the Social Networks
			social_networks_list = self.Folder.Contents(dictionary["Folders"]["Social Networks"]["root"])["folder"]["names"]

			# Remove the Social Networks that are not inside the Social Networks database
			for item in social_networks_list.copy():
				if item not in self.social_networks["List"]:
					social_networks_list.remove(item)

			# Update the "Social Networks.txt" file with the list above
			text_to_write = self.Text.From_List(social_networks_list)

			self.File.Edit(dictionary["Files"]["Social Networks"]["List"], text_to_write, "w")

			# Create a "Social Networks" information dictionary
			dictionary["Social Networks"] = {
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

			# Social Network folders and profile file creation
			for social_network in dictionary["Social Networks"]["List"]:
				# Update the "self.social_network" variable
				self.Select_Social_Network(social_network)

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

					# Create the "Profile.txt" file
					dict_["Profile"] = dict_["root"] + self.JSON.Language.language_texts["profile, title()"] + ".txt"

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

			# Define the "Friend" dictionary as the local "Friend" dictionary
			self.friends["Dictionary"][friend] = dictionary

		# ---------- #

		# Create a local "Friends" dictionary
		local_dictionary = deepcopy(self.friends)

		# Remove the "File names" key
		local_dictionary.pop("File names")

		# Define the keys to remove
		to_remove = [
			"Folders",
			"Files"
		]

		# Iterate through the friends list
		for friend in self.friends["List"]:
			# Remove the unused keys
			for key in to_remove:
				local_dictionary["Dictionary"][friend].pop(key)

		# Update the "Friends.json" file with the updated and local "Friends" dictionary
		self.JSON.Edit(self.folders["Friends"]["Text"]["Friends"], local_dictionary)

	def Information(self, information = None, file = None, information_items = None):
		if file != None:
			information = self.File.Dictionary(file, next_line = True)

		if information_items == None:
			information_items = self.information_items

		dictionary = {}

		for information_key, value in information.items():
			correct_key = ""

			for key, information_item in information_items["Dictionary"].items():
				if (
					key == information_key or
					information_key == information_item[self.user_language]
				):
					correct_key = key

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

	def Select_Friend(self, friends_list = None, select_text = None, first_space = True, second_space = True):
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

		if hasattr(self, "states") == True:
			self.states["Selected a friend"] = True

		return self.friend

	def Select_Social_Network(self, social_network = None, select_social_network = True, social_networks = None, select_text = None):
		if social_networks == None:
			social_networks = self.social_networks

		self.social_network = self.Social_Networks.Select_Social_Network(social_network = social_network, select_social_network = select_social_network, social_networks = social_networks, select_text = select_text)

		return self.social_network
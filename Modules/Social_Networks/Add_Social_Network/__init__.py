# Add_Social_Network.py

from Social_Networks.Social_Networks import Social_Networks as Social_Networks

from copy import deepcopy
import collections

class Add_Social_Network(Social_Networks):
	def __init__(self):
		super().__init__()

		# Show a separator
		print()
		print(self.separators["5"])

		# Ask the user to type the information of the new Social Network to be added
		self.Type_Information()

		# Define the information items of the Social Network
		self.Define_The_Information_Items()

		# Ask for the profile of the user for the newly created Social Network
		self.Add_Social_Network_Profile()

		# Define the folders and files of the Social Network
		self.Define_Social_Network_Folders_And_Files()

		# Write to them
		self.Write_To_Files()

		# Show the information about the newly added Social Network
		self.Show_Information()

		# Run the root class to update the folders and files of all Social Networks
		# And also the "Social Networks.json" file
		super().__init__()

	def Type_Information(self):
		# Show the "Please type the information of the Social Network" text
		print()
		print(self.language_texts["please_type_the_information_of_the_social_network"] + ":")

		# Define the default and empty Social Network dictionary
		self.social_network = {
			"Name": "",
			"Folders": {},
			"Files": {},
			"Information": {},
			"Information items": {},
			"Settings": {
				"Create image folders": True
			},
			"Profile": {}
		}

		# Define the test information dictionary for testing
		self.test_information = {
			"Name": "The Social Network",
			"Creators": "Stake2",
			"Company": "Stake2 Inc",
			"Release date": "01/01/2024",
			"Written in": "Cliente: PHP, Servidor: Python",
			"Engine": "Cliente da web: Electron, Cliente do mobile: React Native",
			"Operating system": "Microsoft Windows, macOS, Linux, Android, iOS, navegadores da web",
			"Link": "https://thestake2.netlify.app/stake2/",
			"Opening link": ""
		}

		# Reset the test information dictionary to test manually typing the information
		#self.test_information = {}

		# Iterate through the social network information items list
		for key in self.information_items["Lists"]["Social Network information"]:
			# Get the information item dictionary
			information_item = self.information_items["Dictionary"][key]

			# Get the language information item
			language_information_item = information_item[self.user_language]

			# Define the "Test information" dictionary inside the "Information item" dictionary
			information_item["Test information"] = self.test_information

			# Define the type text
			type_text = None

			# If the information does not need to be selected
			if information_item["States"]["Select"] == False:
				# Define the type text as the information item in the user language
				type_text = language_information_item

			# If the information item is not 
			# Select the information using the "Select_Information_Item" root method
			information = self.Select_Information_Item(information_item = information_item, type_text = type_text)["Information"]

			# If the information is not equal to an empty string
			if information != "":
				# Add the information to the Social Network "Information" dictionary, with the information item key
				self.social_network["Information"][key] = information

			# If the information item is "Name"
			if key == "Name":
				# Update the "Name" key of the Social Network dictionary
				self.social_network["Name"] = information

		# ---------- #

		# Define the "[Empty]" text
		empty = "[{}]".format(self.Language.language_texts["empty, title()"])

		# Iterate through the social network information items list
		for key in self.information_items["Lists"]["Social Network information"]:
			# Get the information
			information = self.social_network["Information"][key]

			# If the information is empty, remove it
			if information in ["", empty]:
				self.social_network["Information"].pop(key)

	def Define_The_Information_Items(self):
		# Define the information items dictionary as the default one
		self.social_network["Information items"] = self.default_dictionaries["Information items"]

		# ---------- #

		# Show a five dash space separator
		print()
		print(self.separators["5"])

		# Ask the user if it wants to select pre-existing information items or create their own

		# Define the options
		options = [
			"Select",
			"Create"
		]

		language_options = [
			self.language_texts["use_pre_existing_information_items"],
			self.language_texts["create_new_information_items"]
		]

		# Ask the user to select the mode
		mode = self.Input.Select(options, language_options = language_options)["Option"]["Original"]

		# If the mode is "Select"
		if mode == "Select":
			# Make a copy of the root information items dictionary
			information_items = deepcopy(self.information_items)

			# Define the local list of language items
			language_information_items = []

			# ---------- #

			# Define the "To remove" list
			to_remove = information_items["Lists"]["Social Network information"]

			# Remove some keys that should not be removed
			to_remove.remove("Name")
			to_remove.remove("Link")

			# Define the "To remove" list in the information items dictionary
			information_items["Lists"]["To remove"] = to_remove

			# ---------- #

			# Add the "Finish selection" option to the list
			information_items["Lists"]["en"].append("Finish selection")

			# Create the "Finish selection" dictionary
			information_items["Dictionary"]["Finish selection"] = {
				"Name": "Finish selection",
				self.user_language: "[" + self.Language.language_texts["finish_selection"] + "]"
			}

			# ---------- #

			# Define the default information item
			information_item = {
				"Name": ""
			}

			# While that variable is not "Finish selection"
			while information_item["Name"] != "Finish selection":
				# Show a five dash space separator
				print()
				print(self.separators["5"])
				print()

				# Show the list of language items
				print(self.Language.language_texts["list, title()"] + ":")

				# If the list is not empty
				if language_information_items != []:
					for item in language_information_items:
						print("\t" + item)

				# Else, show the "[Empty]" text with a tab
				else:
					print("\t" + "[" + self.Language.language_texts["empty, title()"] + "]")

				# Ask the user to select information items
				information_item = self.Select_Information_Item(information_items, type_information = False, first_separator = False)["Item"]

				# ---------- #

				# If the information item is not "Finish selection"
				if information_item["Name"] != "Finish selection":
					# Add the item to the information items list
					self.social_network["Information items"]["List"].append(information_item["Name"])

					# Add the language item to the list of language items
					language_information_items.append(information_item[self.user_language])

				# ---------- #

				# If the name is inside the English information item list
				if information_item["Name"] in information_items["Lists"]["en"]:
					# Remove the selected information item from the local dictionary
					information_items["Lists"]["en"].remove(information_item["Name"])

			# ---------- #

			# Count the number of information items
			self.social_network["Information items"]["Numbers"]["Total"] = len(self.social_network["Information items"]["List"])

			# Iterate through the information items inside the list of the social network
			for item in self.social_network["Information items"]["List"]:
				# Iterate through the keys and lists in the "Lists" dictionary
				for key, list_ in information_items["Lists"].items():
					# If the current item is inside the local list
					if item in list_:
						# Add it to the list of the social network
						self.social_network["Information items"]["Lists"][key].append(item)

				# If the item is inside the "Accept enter" dictionary
				if item in information_items["Accept enter"]:
					# Add it to the dictionary of the social network
					self.social_network["Information items"]["Accept enter"][item] = information_items["Accept enter"][item]

				# Iterate through the list of genders
				for gender in ["Masculine", "Feminine"]:
					# If the item is inside the list of the current gender
					if item in information_items["Gender"][gender]:
						# Add it to the list of the social network
						self.social_network["Information items"]["Gender"][gender].append(item)

				# Ask if the item has a format
				has_format = self.Input.Yes_Or_No(self.language_texts["does_the_information_item_has_a_format"])

				# If the answer is yes
				if has_format == True:
					# Ask for the Regex format and example
					# Then add it to the root and social network "Formats" dictionary
					print()

				# Define the default "has additional items" variable
				has_additional_items = False

				# Define the list of link types
				link_types = [
					"Profile link",
					"Message link"
				]

				# If the item is not "Profile link" or "Message link"
				if item not in link_types:
					# Ask if the item has additional items
					has_additional_items = self.Input.Yes_Or_No(self.language_texts["does_the_information_item_has_additional_items"])

				# If the answer is yes
				# Or the item is inside the list of link types
				if (
					has_additional_items == True or
					item in link_types
				):
					# Ask for the additional item
					# Add it to the root and social network "Additional items" dictionary
					# Also tell about using the "{Social Network link}" and "{[Item]}" format strings
					print()

			# ---------- #

			# Define the dictionaries of the information items
			self.social_network["Information items"] = self.Define_Information_Item_Dictionary(self.social_network["Information items"])

		# If the mode is "Create"
		if mode == "Create":
			self.Create_Information_Items()

	def Create_Information_Items(self):
		print()

	def Add_Social_Network_Profile(self):
		# Asks for the user to type information about the Social Network profile
		self.social_network = self.Type_Social_Network_Information(social_network = self.social_network)

	def Define_Social_Network_Folders_And_Files(self):
		# Add the Social Network to the social networks list
		if self.social_network["Name"] not in self.social_networks["List"]:
			self.social_networks["List"].append(self.social_network["Name"])

		# Define and create the social network folders and files
		for item in ["Text", "Image"]:
			# Define the item key inside the "Files" dictionary
			self.social_network["Files"][item] = {}

			# Define the root folder
			folder = self.folders["Social Networks"][item]["root"] + self.social_network["Name"] + "/"

			# Create the folders dictionary
			dict_ = {
				"root": folder
			}

			self.Folder.Create(dict_["root"])

			# Define and create the social network folders and files
			for item in ["Text", "Image"]:
				# Define the item key inside the "Files" dictionary
				self.social_network["Files"][item] = {}

				# Define the root folder
				folder = self.folders["Social Networks"][item]["root"] + self.social_network["Name"] + "/"

				# Create the folders dictionary
				dict_ = {
					"root": folder
				}

				self.Folder.Create(dict_["root"])

				# Iterate through the social network file names
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
						self.social_network["Settings"]["Create image folders"] == True
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
							self.social_network["Files"][key] = dict_[key]

						# Add the file to the "Files" dictionary
						self.social_network["Files"][item][key] = dict_[key]

					# If the file is the settings file
					# And the settings file exists
					if (
						key == "Settings" and
						self.File.Exist(dict_[key]) == True
					):
						# Add the file to the "Files" dictionary
						self.social_network["Files"][item][key] = dict_[key]
					
						# Read the settings file
						settings = self.File.Dictionary(self.social_network["Files"]["Text"][key], next_line = True)

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

						self.social_network["Settings"] = new_settings

				# Define the folders dictionary as the local folders dictionary
				self.social_network["Folders"][item] = dict_

		# Add the keys of the "Text" folders dictionary to the root folders dictionary
		self.social_network["Folders"].update(self.social_network["Folders"]["Text"])

		# ---------- #

		# Define the list of file names
		file_names = [
			"Information",
			"Profile",
			"Social Network"
		]

		# Update the social network files of the image folder if the file inside the text folder is different
		for file_name in file_names:
			# Define the empty files dictionary
			files = {}

			# Iterate through the folder type list
			for item in ["Text", "Image"]:
				# Get the file of the folder type with the file name
				file = self.social_network["Files"][item][file_name]

				# Define the file dictionary with the file and file size
				files[item] = {
					"File": file,
					"Size": self.File.Contents(file)["size"]
				}

			# If the size of the file on the text folder is different than the file of the image folder
			if files["Text"]["Size"] != files["Image"]["Size"]:
				# Replace the file on the image folder with the one on the text folder, updating the file
				self.File.Copy(files["Text"]["File"], files["Image"]["File"])

		# ---------- #

		# Update the number of Social Networks
		self.social_networks["Numbers"]["Total"] = len(self.social_networks["List"])

		# Add the social network dictionary to the root dictionary of the "Social Networks" dictionary
		self.social_networks["Dictionary"][self.social_network["Name"]] = self.social_network

		# Sort the "By year" numbers keys
		self.social_networks["Numbers"]["By year"] = dict(collections.OrderedDict(sorted(self.social_networks["Numbers"]["By year"].items())))

		# Sort the Social Networks list
		self.social_networks["List"] = sorted(self.social_networks["List"], key = str.lower)

		# Sort the Social Networks dictionary
		self.social_networks["Dictionary"] = dict(collections.OrderedDict(sorted(self.social_networks["Dictionary"].items())))

	def Write_To_Files(self):
		# Make a local copy of the Social Network "Information" dictionary
		information = deepcopy(self.social_network["Information"])

		# Translate the keys to the user language
		# Using the "Information" method of the "Social Networks" class
		information = self.Information(information, to_user_language = True)

		# Iterate through the folder type list
		for item in ["Text", "Image"]:
			# Transform the dictionary into a text string with lines separating each one of the keys
			text_to_write = self.Text.From_Dictionary(information, next_line = True)

			# Write to the "Information.txt" file
			self.File.Edit(self.social_network["Files"][item]["Information"], text_to_write, "w")

		# ---------- #

		# Write to the "Items.json" file
		self.JSON.Edit(self.social_network["Files"]["Items"], self.social_network["Information items"])

		# ---------- #

		# Update the "Social Networks.json" file with the updated and local "Social Networks" dictionary
		self.Update_Social_Networks_File()

	def Show_Information(self):
		# Show a five dash space separator
		print()
		print(self.separators["5"])
		print()

		# Define the text to show
		text_key = "you_added_this_social_network_to_the_social_networks_database"

		# Show the text in the user language
		# Along with the Social network name
		print(self.language_texts[text_key] + ":")
		print("\t" + self.social_network["Name"])

		# ---------- #

		# List the keys of the "Information items" dictionary
		keys = list(self.social_network["Information items"]["Dictionary"].keys())

		# Define the "information" variable for easier typing
		information = self.social_network["Information"]

		# Iterate through the "Information items" dictionary
		for key, information_item in self.social_network["Information items"]["Dictionary"].items():
			# Define the language information item
			language_information_item = information_item[self.user_language]

			# Get the current information
			current_information = information[key]

			# If the information item is not the first one
			if key != keys[0]:
				# Show a space
				print()

			# Show the language information item and the current information
			print(language_information_item + ":")

			# Define the current information as the "Empty" text if it is empty
			if current_information == "":
				current_information = self.Language.language_texts["empty, title()"]

			# Show the current information with one tab
			print("\t" + current_information)

		# Show a final separator
		print()
		print(self.separators["5"])
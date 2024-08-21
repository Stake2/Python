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
			"Profile": {},
			"Image folders": []
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
			"Link": "https://thestake2.netlify.app/",
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

		# ---------- #

		# Ask for the image folders of the social network
		has_image_folders = self.Input.Yes_Or_No(self.language_texts["do_the_social_network_profiles_need_image_folders"])

		# Update the "Create image folders" setting
		self.social_network["Settings"]["Create image folders"] = has_image_folders

		# If the setting is True
		if has_image_folders == True:
			# Define the "folder" variable as an empty string
			folder = ""

			# While it is not "f" (the finish text)
			while folder != "f":
				# Show the list of folders
				self.Show_The_List_Of_Folders()

				# Define the input text
				input_text = self.Language.language_texts["type_the_image_folder"] + ":" + "\n" + \
				"(" + self.language_texts["type_f_to_finish_adding"] + ")"
				
				# Ask the user to type the image folder
				folder = self.Input.Type(input_text, next_line = True)

				# If the folder is not "f" (the finish text)
				if folder != "f":
					# Add the folder to the list
					self.social_network["Image folders"].append(folder)

	def Show_The_List_Of_Folders(self):
		# Show a separator
		print()
		print(self.separators["5"])
		print()

		# Show the list of folders
		print(self.Language.language_texts["folders, title()"] + ":")

		# If the list is not empty
		if self.social_network["Image folders"] != []:
			for item in self.social_network["Image folders"]:
				print("\t" + item)

		# Else, show the "[Empty]" text with a tab
		else:
			print("\t" + "[" + self.Language.language_texts["empty, title()"] + "]")

	def Define_The_Information_Items(self):
		# Define the information items dictionary as the default one
		self.social_network["Information items"] = self.default_dictionaries["Information items"]

		# Add the social network dictionary to the keys in the information item dictionary
		self.information_items["Formats"][self.social_network["Name"]] = {}
		self.information_items["Additional items"][self.social_network["Name"]] = {}

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
			self.Select_Information_Items()

		# If the mode is "Create"
		if mode == "Create":
			self.Create_Information_Items()

	def Select_Information_Items(self):
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

		# Define the "i" number variable
		i = 0

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

			# ---------- #

			# Get the language information item
			language_information_item = language_information_items[i]

			# Show a five dash space separator
			print()
			print(self.separators["5"])
			print()

			# Show the item
			print(self.Language.language_texts["item, title()"] + ":")
			print("\t" + language_information_item)

			if self.switches["Testing"] == False:
				# Ask if the item has a format
				has_format = self.Input.Yes_Or_No(self.language_texts["does_the_information_item_has_a_format"])

			if self.switches["Testing"] == True:
				has_format = False

			# If the answer is yes
			if has_format == True:
				# Ask the user for the regex format
				regex = {
					"Format": self.Input.Type(self.language_texts["type_the_regex_format"]),
					"Example": self.Input.Type(self.language_texts["type_an_example_of_the_format"]),
				}

				# If the item dictionary is not present, add it
				if item not in self.social_network["Information items"]["Formats"]:
					self.social_network["Information items"]["Formats"][item] = regex

			# ---------- #

			# Define the default "has additional items" variable
			has_additional_items = False

			# Define the list of link types
			link_types = [
				"Profile link",
				"Message link"
			]

			# If the item is not "Profile link" or "Message link"
			if item not in link_types:
				if self.switches["Testing"] == False:
					# Ask if the item has additional items
					has_additional_items = self.Input.Yes_Or_No(self.language_texts["does_the_information_item_has_additional_items"])

				if self.switches["Testing"] == True:
					has_additional_items = False

			# If the answer is yes
			# Or the item is inside the list of link types
			if (
				has_additional_items == True or
				item in link_types
			):
				# Define the type text and add the explanation text
				type_text = self.language_texts["type_the_additional_item"] + ":" + "\n"
				type_text += "(" + self.language_texts["you_can_use_the_{}_format_string_to_place_the_social_network_link, type: explanation"] + "\n" + \
				"\n" + \
				self.Language.language_texts["list, title()"] + ": [List]" + ")"

				# Define the list of items
				items = deepcopy(self.social_network["Information items"]["List"])

				# Iterate through the list to add the format symbols
				c = 0
				for x in items:
					items[c] = "{" + items[c] + "}"

					c += 1

				# Transform the list into a text string
				items = self.Text.From_List(items)

				# Format the type text
				type_text = type_text.format(*[
					'"' + "{Social Network link}" + '"',
					'"' + "{[Item]}" + '"'
				])

				# Replace the "[List]" format text with the actual list of items
				type_text = type_text.replace("[List]", items)

				# Define the default empty additional item
				additional_item = ""

				if self.switches["Testing"] == False:
					# Ask the user for the additional item
					additional_item = self.Input.Type(type_text, next_line = True)

				if (
					self.switches["Testing"] == True and
					item in ["Profile link", "Message link"]
				):
					if item == "Profile link":
						format_item = "/users"

					if item == "Message link":
						format_item = "/messages"

					additional_item = "{Social Network link}" + "{}".format(format_item) + "/{Handle}"

					print()
					print(type_text + ":")
					print()
					print("[" + additional_item + "]")

				# If the additional item is not empty
				if additional_item != "":
					# Add the additional item to the root additional items dictionary
					self.information_items["Additional items"][self.social_network["Name"]][item] = additional_item

					# Add the additional item to the social network additional items dictionary
					self.social_network["Information items"]["Additional items"][item] = additional_item

			# Add one to the "i" number variable
			i += 1

		# ---------- #

		# Define the default "has custom additional items" variable
		has_custom_additional_items = False

		if self.switches["Testing"] == False:
			# Define the input text
			input_text = self.language_texts["does_the_social_network_has_custom_additional_items"] + "?" + "\n" + \
			"(" + self.language_texts["like_custom_profile_or_message_links"] + ")" + "\n"

			# Ask if the social network has custom additional items
			has_custom_additional_items = self.Input.Yes_Or_No(input_text)

		if self.switches["Testing"] == True:
			has_custom_additional_items = False

		# ---------- #

		# Define the dictionaries of the information items
		self.social_network["Information items"] = self.Define_Information_Item_Dictionary(self.social_network["Information items"])

	def Create_Information_Items(self):
		print()

	def Add_Social_Network_Profile(self):
		# Iterate through the "Additional items" dictionary
		for key, additional_item in self.information_items["Additional items"][self.social_network["Name"]].items():
			if "{Social Network link}" in additional_item:
				additional_item = additional_item.replace("{Social Network link}", self.social_network["Information"]["Link"][:-1])

			# Update the additional item in the root dictionary
			self.information_items["Additional items"][self.social_network["Name"]][key] = additional_item

		# ---------- #

		# Asks for the user to type information about the Social Network profile
		self.social_network = self.Type_Social_Network_Information(social_network = self.social_network)

		# ---------- #

		# Iterate through the "Additional items" dictionary
		for key, additional_item in self.information_items["Additional items"][self.social_network["Name"]].items():
			# Get the format information item
			format_item = additional_item.split("{")[1].split("}")[0]

			# Remove the format item from the additional item template
			additional_item = additional_item.replace(format_item, "")

			# Define the information with the formatted additional item template
			information = additional_item.format(self.social_network["Profile"][format_item])

			# Update the additional item in the "Profile" dictionary
			self.social_network["Profile"][key] = information

		# ---------- #

		# Create the "Links" dictionary
		self.social_network["Profile"]["Links"] = {}

		# Add links to the dictionary above
		for link_type in ["Profile", "Message"]:
			key = link_type + " link"

			if key in self.social_network["Profile"]:
				link = self.social_network["Profile"][key]

				self.social_network["Profile"]["Links"][link_type] = link

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

		# ---------- #

		# Make a local copy of the Social Network "Profile" dictionary
		profile = deepcopy(self.social_network["Profile"])

		# Remove the "Links" key
		profile.pop("Links")

		# Translate the keys to the user language
		# Using the "Information" method of the "Social Networks" class
		profile = self.Information(profile, to_user_language = True)

		# Iterate through the folder type list
		for item in ["Text", "Image"]:
			# Transform the "Information" dictionary into a text string with lines separating each one of the keys
			text_to_write = self.Text.From_Dictionary(information, next_line = True)

			# Write to the "Information.txt" file
			self.File.Edit(self.social_network["Files"][item]["Information"], text_to_write, "w")

			# ---------- #

			# Transform the "Profile" dictionary into a text string with lines separating each one of the keys
			text_to_write = self.Text.From_Dictionary(profile, next_line = True)

			# Write to the "Profile.txt" file
			self.File.Edit(self.social_network["Files"][item]["Profile"], text_to_write, "w")

		# ---------- #

		# Write to the "Items.json" file
		self.JSON.Edit(self.social_network["Files"]["Items"], self.social_network["Information items"])

		# ---------- #

		# Make a local copy of the "Social Network" dictionary
		local_dictionary = deepcopy(self.social_network)

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
		self.JSON.Edit(self.social_network["Folders"]["Social Network"], local_dictionary)

		# Update the image "Social Network.json" file with the updated and local "Social Network" dictionary
		self.JSON.Edit(self.social_network["Folders"]["Image"]["Social Network"], local_dictionary)

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
		print()

		# Show the "Information" text
		print(self.Language.language_texts["informations, title()"] + ":")
		print()

		# ---------- #

		# Show the information of the social network

		# Define the "information" variable for easier typing
		information = self.social_network["Information"]

		# List the keys of the "Information items" dictionary
		keys = self.information_items["Lists"]["Social Network information"]

		# Iterate through the list of keys
		for key in keys:
			# If the key is not in the "Information" dictionary, remove it
			if key not in information:
				keys.remove(key)

		# Iterate through the "Social Network information" items list
		for key in keys:
			# If the information item is in the root dictionary
			if key in self.information_items["Dictionary"]:
				# Get the information item from it
				information_item = self.information_items["Dictionary"][key]

			# Else, get it from the local social network dictionary
			else:
				information_item = self.social_network["Information items"]["Dictionary"][key]

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

		# ---------- #

		# Show a five dash space separator
		print()
		print(self.separators["5"])
		print()

		# Show the information of the social network profile

		# Show the "Profile" text
		print(self.Language.language_texts["profile, title()"] + ":")
		print()

		# Define the "profile" variable for easier typing
		profile = self.social_network["Profile"]

		# Define the list of keys
		keys = list(self.social_network["Information items"]["Dictionary"].keys())

		# Iterate through the list of keys
		for key in keys:
			# If the key is in the "Social Network information" list
			# Or it is not in the "Profile" dictionary, remove it
			if (
				key in self.information_items["Lists"]["Social Network information"] or
				key not in profile
			):
				keys.remove(key)

		# Iterate through the "Social Network profile" items list
		for key in keys:
			# If the information item is in the root dictionary
			if key in self.information_items["Dictionary"]:
				# Get the information item from it
				information_item = self.information_items["Dictionary"][key]

			# Else, get it from the local social network dictionary
			else:
				information_item = self.social_network["Information items"]["Dictionary"][key]

			# Define the language information item
			language_information_item = information_item[self.user_language]

			# Get the current profile information
			current_information = profile[key]

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
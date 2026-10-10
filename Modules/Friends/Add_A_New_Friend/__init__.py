# Add_A_New_Friend.py

from Friends.Friends import Friends as Friends

from copy import deepcopy
import collections

class Add_A_New_Friend(Friends):
	def __init__(self):
		super().__init__()

		# Define the root dictionary
		self.dictionary = {
			"States": {
				"Add social networks": False,
				"Add more social networks": True,
				"Add social network to existing friend folder": False,
				"Friend already existed": False
			}
		}

		# Show a five dash space separator
		print()
		print(self.separators["5"])

		# Define the "Ask to add" switch
		self.ask_to_add = False

		# If the "Ask to add" switch is True
		if self.ask_to_add == True:
			# Ask the user if they want to add social networks to an existing friend folder
			self.dictionary["States"]["Add social network to existing friend folder"] = self.Input.Yes_Or_No(self.language_texts["add_social_network_to_friend_folder"])

		# If the user wants to add social networks to an existing friend folder
		if self.dictionary["States"]["Add social network to existing friend folder"] == True:
			# Show a five dash space separator
			print()
			print(self.separators["5"])

			# Select a friend to add a social network to their folder
			self.Select_Friend()

		# If not
		if self.dictionary["States"]["Add social network to existing friend folder"] == False:
			# Ask the user to type the information of the new friend that is going to be added
			self.Type_Friend_Information()

		# Add the social networks of the friend by typing their information
		self.Add_Social_Networks()

		# Define the folders and files of the Friend
		self.Define_Friend_Folders_And_Files()

		# Write to them
		self.Write_To_Files()

		# Show the information about the newly added Friend
		# Or the new social networks added to an existing friend folder
		self.Show_Information()

		# Run the root class to update the folders and files of all Friends
		# And also the "Friends.json" file
		super().__init__()

	def Type_Friend_Information(self):
		# If the "Ask to add" switch is True
		if self.ask_to_add == True:
			# Show a five dash space separator
			print()
			print(self.separators["5"])

		# Show a separator the "Please type the information of the friend" text
		print()
		print(self.language_texts["please_type_the_information_of_the_friend"] + ":")

		# Define the default and empty Friend dictionary
		self.friend = {
			"Name": "",
			"Folders": {},
			"Files": {},
			"Information": {},
			"Social networks": {
				"Numbers": {
					"Total": 0
				},
				"List": [],
				"Dictionary": {}
			}
		}

		# Define the test information dictionary for testing
		self.dictionary["Test information"] = {
			"Name": "Name of the Friend",
			"Age": "18",
			"Gender": "Masculino",
			"Sexuality": "Heterossexual",
			"Date of birth": "01/01/2000",
			"Height": "",
			"Hometown": "? - California - United States",
			"Residence place": "? - California - United States",
			"Date I met": "12:00 01/01/2000",
			"Origin social network": "Discord",
			"Additional information of origin social network": 'Server: "A server of Discord"'
		}

		# Reset the test information dictionary to test manually typing the information
		#self.dictionary["Test information"] = {}

		# Iterate through the Information items dictionary
		for key, information_item in self.information_items["Dictionary"].items():
			# Get the language information item
			language_information_item = information_item[self.language["Small"]]

			# If the information item is "Origin social network"
			if key == "Origin social network":
				# Define the "Friend" dictionary inside the "Information item" dictionary
				# With the Friend gender
				information_item["Friend"] = {
					"Gender": self.friend["Information"]["Gender"]
				}

			# Define the "Test information" dictionary inside the "Information item" dictionary
			information_item["Test information"] = self.dictionary["Test information"]

			# Define the type text
			type_text = None

			# If the information does not need to be selected
			if information_item["States"]["Select"] == False:
				# Define the type text as the information item in the user language
				type_text = language_information_item

			# Select the information using the "Select_Information_Item" root method
			information = self.Select_Information_Item(information_item = information_item, type_text = type_text)["Information"]

			# If the information is not equal to an empty string
			if information != "":
				# Add the information to the Friend "Information" dictionary, with the information item key
				self.friend["Information"][key] = information

			# If the information item is "Name"
			if key == "Name":
				# Update the "Name" key of the Friend dictionary
				self.friend["Name"] = information

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
			fields = self.friend["Information"][key].split(" - ")

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

		self.friend["Information"] = self.JSON.Add_Key_After_Key(self.friend["Information"], key_value, after_key = "Residence place")

		# Add the "Year I met" key to the friend "Information" dictionary
		self.friend["Information"]["Year I met"] = self.friend["Information"]["Date I met"].split("/")[-1]

		# Show a separator
		print()
		print(self.separators["5"])

	def Add_Social_Networks(self):
		# Create a copy of the root "Social networks" dictionary
		self.social_networks_copy = deepcopy(self.social_networks)

		# If the user wants to add a social network to an existing friend folder
		if self.dictionary["States"]["Add social network to existing friend folder"] == True:
			# Create the "New social networks" dictionary
			self.dictionary["New social networks"] = {
				"Numbers": {
					"Total": 0
				},
				"List": [],
				"Dictionary": {}
			}

			# Iterate through the list of social networks of the friend
			for social_network in self.friend["social networks"]["List"]:
				# If the social network is inside the list of social networks inside the copy of the social networks dictionary
				if social_network in self.social_networks_copy["List"]:
					# Remove it
					self.social_networks_copy["List"].remove(social_network)

		# While the "Add more social networks" state is True
		loop_number = 0
		while self.dictionary["States"]["Add more social networks"] == True:
			# Add the new social network and store it in the "added social network" variable
			self.added_social_network = self.Add_Social_Network()

			# If the user does not want to add a social network to an existing friend folder (a new friend is being added)
			# And the while loop is at the beginning
			if (
				self.dictionary["States"]["Add social network to existing friend folder"] == False and
				loop_number == 0
			):
				# Ask the user if they want to add social networks to the friend folder and update the "Add social networks" state
				self.dictionary["States"]["Add social networks"] = self.Input.Yes_Or_No(self.language_texts["add_social_networks"])

				# If the user does not want to add social networks to the friend folder
				if self.dictionary["States"]["Add social networks"] == False:
					# Define the "Add more social networks" state as False to stop the while loop
					self.dictionary["States"]["Add more social networks"] = False

			# If the user wants to add social networks to the friend folder
			# And the while loop is not at the beginning
			if (
				self.dictionary["States"]["Add social networks"] == True and
				loop_number != 0
			):
				# Ask if the user wants to add more social networks to the friend folder
				self.dictionary["States"]["Add more social networks"] = self.Input.Yes_Or_No(self.language_texts["add_more_social_networks"])

			# Add one to the loop number
			loop_number += 1

		# Sort the list of social networks of the friend by their names, alphabetically and ignoring capitalization
		self.friend["Social networks"]["List"] = sorted(self.friend["Social networks"]["List"], key = str.lower)

		# Sort the dictionary of social networks by their keys in ascending order
		self.friend["Social networks"]["Dictionary"] = dict(collections.OrderedDict(sorted(self.friend["Social networks"]["Dictionary"].items())))

	def Add_Social_Network(self):
		# Define the select text
		select_text = self.language_texts["select_a_social_network_to_add_it_to_the_friend_folder"]

		# Define the "first separator" switch as True
		first_separator = True

		# Define the local social network initially as None
		social_network = None

		# If the list of social networks of the friend is empty
		if self.friend["Social networks"]["List"] == []:
			# Define the first social network to be added as the origin social network
			variable = self.friend["Information"]["Origin social network"].split(" - ")[0]

			# If the origin social network is inside the list of social networks
			if variable in self.social_networks["List"]:
				# Define the local social network as the origin social network
				social_network = variable

			# Change the "first separator" switch to False
			first_separator = False

		# Select the social network and get its dictionary
		self.social_network = self.Select_Social_Network(social_network = social_network, social_networks = self.social_networks_copy, select_text = select_text)

		# If the social network is not inside the list of social networks of the friend
		if self.social_network["Name"] not in self.friend["Social networks"]["List"]:
			# Asks for the user to type information about the selected social network profile
			self.social_network = self.Social_Networks.Type_Social_Network_Information(social_network = self.social_network, first_separator = first_separator)

			# Add the social network to the list of social networks
			self.friend["Social networks"]["List"].append(self.social_network["Name"])

			# Update the number of social networks
			self.friend["Social networks"]["Numbers"]["Total"] = len(self.friend["Social networks"]["List"])

			# Add it to the social networks dictionary
			self.friend["Social networks"]["Dictionary"][self.social_network["Name"]] = deepcopy(self.social_network["Profile"])

			# Remove the selected social network from the list of social networks
			self.social_networks_copy["List"].remove(self.social_network["Name"])

			# If the user wants to add social networks to an existing friend
			if self.dictionary["States"]["Add social network to existing friend folder"] == True:
				# Add the social network to the "New social networks" list
				self.dictionary["New social networks"]["List"].append(self.social_network["Name"])

				# Update the number of new social networks
				self.dictionary["New social networks"]["Numbers"]["Total"] = len(self.dictionary["New social networks"]["List"])

				# Add the social network to the "New social networks" dictionary
				self.dictionary["New social networks"]["Dictionary"][self.social_network["Name"]] = deepcopy(self.social_network["Profile"])

			# Return the "Added social network" variable as True
			return True

		# If the social network is inside the list of social networks of the friend
		if self.social_network["Name"] in self.friend["Social networks"]["List"]:
			# Return the "Added social network" variable as False
			return False

	def Define_Friend_Folders_And_Files(self):
		# If the friend already existed in the database of friends
		if self.friend["Name"] in self.friends["List"]:
			# Change the "Friend already existed" state
			self.dictionary["States"]["Friend already existed"] = True

		# Else, add the friend to the friends list
		if self.friend["Name"] not in self.friends["List"]:
			self.friends["List"].append(self.friend["Name"])

		# Define and create the friend folder
		folder = self.folders["Friends"]["root"] + self.friend["Name"] + "/"
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
				self.friend["Files"][key] = folders_dictionary[key]

			# If the file name is "Social networks"
			if key == "Social networks":
				# Create a dictionary for the "Social networks" files
				self.friend["Files"][key] = {
					# And define the "List" key as the "Social networks.txt" file
					"List": folders_dictionary[key]
				}

		# Define and create the friend "Media" folder
		folders["Media"] = {
			"root": folders["root"] + self.Language.language_texts["media, title(), type: plural"] + "/"
		}

		self.Folder.Create(folders["Media"]["root"])

		# Define the root friend "Folders" dictionary as the local one
		self.friend["Folders"] = folders

		# ---------- #

		# Iterate through the list of social networks of the friend
		for social_network in self.friend["Social networks"]["List"]:
			# Update the root "social network" with the dictionary of the current social network
			self.social_network = self.Select_Social_Network(social_network)

			# Define and create the social network folder
			folders = {
				"root": self.friend["Folders"]["Social networks"]["root"] + social_network + "/"
			}

			self.Folder.Create(folders["root"])

			# Define and create the social network "Profile.txt" file
			folders["Profile"] = folders["root"] + self.Language.language_texts["profile, title()"] + ".txt"
			self.File.Create(folders["Profile"])

			# Create a shortcut to the social network "Profile.txt" file
			file = folders["Profile"]

			# Add the social network folders dictionary to the friend "Folders" dictionary
			self.friend["Folders"]["Social networks"][social_network] = folders

			# Create the social network files inside the friend "Files" dictionary
			self.friend["Files"]["Social networks"][social_network] = {
				# And also add the social network "Profile.txt" file to it
				"Profile": file
			}

			# If the "Image folders" key is inside the social network dictionary
			if "Image folders" in self.social_network:
				# Define the root image folder
				image_folder = self.friend["Folders"]["Social networks"][social_network]["root"]

				# Create the social network image folders
				for folder in self.social_network["Image folders"]:
					# Define and create the image folder
					folder = image_folder + folder + "/"
					self.Folder.Create(folder)

		# ---------- #

		# Update the total number of social networks of the friend
		self.friend["Social networks"]["Numbers"]["Total"] = len(self.friend["Social networks"]["List"])

		# Define the root friend dictionary as the local friend dictionary
		self.friends["Dictionary"][self.friend["Name"]] = self.friend

		# Sort the "Met by year" numbers dictionary by their year keys in ascending order
		self.friends["Numbers"]["By year"] = dict(collections.OrderedDict(sorted(self.friends["Numbers"]["By year"].items())))

		# Sort the friends grouped by their year keys in ascending order
		self.friends["Met by year"] = dict(collections.OrderedDict(sorted(self.friends["Met by year"].items())))

		# Sort the list of friends by on their names, alphabetically and ignoring capitalization
		self.friends["List"] = sorted(self.friends["List"], key = str.lower)

		# Sort the dictionary of friends alphabetically by its friend-name keys
		self.friends["Dictionary"] = dict(collections.OrderedDict(sorted(self.friends["Dictionary"].items())))

	def Write_To_Files(self):
		# Create a local copy of the friend "Information" dictionary
		information = deepcopy(self.friend["Information"])

		# Remove the "Locations" key
		information.pop("Locations")

		# Translate the information keys into the user language
		# (The friend information values are already in the user language, so they do not need to be translated)
		information = self.Information(information, to_user_language = True)

		# Update the friend "Information.txt" file with the friend "Information" dictionary translated into the user language and converted to a text
		text_to_write = self.Text.From_Dictionary(information, next_line = True)

		self.File.Edit(self.friend["Files"]["Information"], text_to_write, "w")

		# Iterate through the list of social networks of the friend
		for social_network in self.friend["Social networks"]["List"]:
			# Get the "Information" dictionary of the social network
			information = self.friend["Social networks"]["Dictionary"][social_network]

			# Translate the information keys to the user language (using the "Information" method of the "Social networks" class)
			information = self.Social_Networks.Information(information, to_user_language = True)

			# Transform the dictionary into a text string
			text_to_write = self.Text.From_Dictionary(information, next_line = True)

			# Get the social network "Profile.txt" file
			file = self.friend["Folders"]["Social networks"][social_network]["Profile"]

			# Write the friend profile information into it
			self.File.Edit(file, text_to_write, "w")

		# ---------- #

		# List the social networks of the friend
		social_networks = self.friend["Social networks"]["List"]

		# Iterate through the list of social networks of the friend
		for item in social_networks.copy():
			# If the social network is not inside the root list of social networks (the "Social networks" database)
			if item not in self.social_networks["List"]:
				# Remove it from the list of social networks of the friend
				social_networks.remove(item)

		# Update the "Social networks.txt" file of the friend with the list above
		text_to_write = self.Text.From_List(social_networks)

		self.File.Edit(self.friend["Files"]["Social networks"]["List"], text_to_write, "w")

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

	def Show_Information(self):
		# Show a five dash space separator
		print()
		print(self.separators["5"])
		print()

		# Define the text to show
		text_key = "you_added_this_friend_to_the_friends_database"

		# If the Friend already existed in the Friends database
		if self.dictionary["States"]["Friend already existed"] == True:
			# Define another text
			text_key = "this_friend_already_existed_on_the_friends_database"

		# Show the text in the user language
		# Along with the Friend name
		print(self.language_texts[text_key] + ":")
		print("\t" + self.friend["Name"])

		# ---------- #

		# If the user does not want to add social networks to an existing Friend
		if self.dictionary["States"]["Add social network to existing friend folder"] == False:
			print()

			# Show the information of the Friend
			print(self.language_texts["friend_information"] + ":")

			# Define the information items keys list
			keys = list(self.information_items["Dictionary"].keys())

			# Iterate through the Information items dictionary
			for key, information_item in self.information_items["Dictionary"].items():
				# Get the Friend information
				information = self.friend["Information"][key]

				# Show the information item name in the user language
				print("\t" + information_item[self.language["Small"]] + ":")

				# Show the Friend information
				print("\t" + information)

				# If the information item is not the last one
				if key != keys[-1]:
					# Show a space separator
					print()

		# ---------- #

		# Define the texts dictionary for faster typing
		texts_dictionary = self.Language.language_texts

		# Define the local social networks dictionary
		social_networks = self.friend["Social networks"]

		# If the user wants to add social networks to an existing friend
		if self.dictionary["States"]["Add social network to existing friend folder"] == True:
			social_networks = self.dictionary["New social networks"]

		# Define the "Text by number" dictionary
		text_key = "social_network_information"

		# If the user wants to add social networks to an existing friend
		if self.dictionary["States"]["Add social network to existing friend folder"] == True:
			text_key = "added_social_network_information"

		plural_text_key = text_key.replace("network", "networks")

		dictionary = {
			"Number": social_networks["Numbers"]["Total"],
			"Singular": texts_dictionary[text_key],
			"Plural": texts_dictionary[plural_text_key]
		}

		# Define the text to show
		text_to_show = self.Text.By_Number(dictionary["Number"], dictionary["Singular"], dictionary["Plural"])

		# Show the text
		print()
		print(text_to_show + ":")

		# Define the two tabs variable
		two_tabs = "\t\t"

		# Iterate through the list of social networks
		for social_network in social_networks["List"]:
			# Update the "self.social_network" variable
			self.social_network = self.Select_Social_Network(social_network)

			# Show the social network name
			print()
			print("\t" + social_network + ":")

			# Define the "information" variable for faster typing
			information = social_networks["Dictionary"][social_network]

			# List the keys of the "Information items" dictionary
			keys = list(self.social_network["Information items"]["Dictionary"].keys())

			# Iterate through the "Information items" dictionary
			for key, information_item in self.social_network["Information items"]["Dictionary"].items():
				# Define the language information item
				language_information_item = information_item[self.language["Small"]]

				# Get the current information
				current_information = information[key]

				# If the information item is not the first one
				if key != keys[0]:
					# Show a space
					print()

				# Show the language information item and the current information
				print(two_tabs + language_information_item + ":")

				# Define the current information as the "Empty" text if it is empty
				if current_information == "":
					current_information = self.Language.language_texts["empty, title()"]

				# Show the current information with two tabs
				print(two_tabs + current_information)

		# Show a final separator
		print()
		print(self.separators["5"])
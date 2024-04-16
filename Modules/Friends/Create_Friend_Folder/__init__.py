# Create_Friend_Folder.py

from Friends.Friends import Friends as Friends

from copy import deepcopy
import collections

class Create_Friend_Folder(Friends):
	def __init__(self):
		super().__init__()

		# Define the root dictionary
		self.dictionary = {
			"States": {
				"Add Social Networks": False,
				"Add more Social Networks": True,
				"Add Social Network to existing friend folder": False,
				"Friend already existed": False
			}
		}

		# Show a separator
		print()
		print(self.separators["5"])

		# Ask the user if they want to add Social Networks to an existing friend folder
		self.dictionary["States"]["Add Social Network to existing friend folder"] = self.Input.Yes_Or_No(self.language_texts["add_social_network_to_friend_folder"])

		# If the user wants to add Social Networks to an existing friend folder, select a Friend to do that
		if self.dictionary["States"]["Add Social Network to existing friend folder"] == True:
			print()
			print(self.separators["5"])

			self.Select_Friend()

		# If not, type the information of the new Friend to be added
		if self.dictionary["States"]["Add Social Network to existing friend folder"] == False:
			self.Type_Friend_Information()

		# Add the Social Networks (typing their information)
		self.Add_Social_Networks()

		# Define the folders and files of the Friend
		self.Define_Friend_Folders_And_Files()

		# Write to them
		self.Write_To_Files()

		# Show the information about the newly added Friend
		# Or the new Social Networks added to an existing friend folder
		self.Show_Information()

		# Run the root class to update the folders and files of all Friends
		# And also the "Friends.json" file
		super().__init__()

	def Type_Friend_Information(self):
		# Show a separator and the "Please type the information of the Friend" text
		print()
		print(self.separators["5"])
		print()
		print(self.language_texts["please_type_the_information_of_the_friend"] + ":")

		# Define the default and empty Friend dictionary
		self.friend = {
			"Name": "",
			"Folders": {},
			"Files": {},
			"Information": {},
			"Social Networks": {
				"Numbers": {
					"Total": 0
				},
				"List": [],
				"Dictionary": {}
			},
			"Gender": {
				"Text": "",
				"Words": {}
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
			"Origin Social Network": "Discord",
			"Additional information of Origin Social Network": 'Server: "A server of Discord"'
		}

		# Reset the test information dictionary to test manually typing the information
		#self.dictionary["Test information"] = {}

		# Iterate through the Information items dictionary
		for key, information_item in self.information_items["Dictionary"].items():
			# Get the language information item
			language_information_item = information_item[self.user_language]

			# If the information item is "Origin Social Network"
			if key == "Origin Social Network":
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

			split = self.friend["Information"][key].split(" - ")

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

		self.friend["Information"] = self.JSON.Add_Key_After_Key(self.friend["Information"], key_value, after_key = "Residence place")

		# Add the "Year I met" key
		self.friend["Information"]["Year I met"] = self.friend["Information"]["Date I met"].split("/")[-1]

		# Show a separator
		print()
		print(self.separators["5"])

	def Add_Social_Networks(self):
		# Create a local copy of the Social Networks dictionary
		self.social_networks_copy = deepcopy(self.social_networks)

		# If the user wants to add a Social Network to an existing friend folder
		if self.dictionary["States"]["Add Social Network to existing friend folder"] == True:
			# Create the "New Social Networks" dictionary
			self.dictionary["New Social Networks"] = {
				"Numbers": {
					"Total": 0
				},
				"List": [],
				"Dictionary": {}
			}

			# Iterate through the list of Social Networks of the Friend
			for social_network in self.friend["Social Networks"]["List"]:
				# If the Social Network is inside the local copy of the Social Networks dictionary
				if social_network in self.social_networks_copy["List"]:
					self.social_networks_copy["List"].remove(social_network)

		# Add Social Networks to an existing Friend or the newly added Friend
		i = 0
		while self.dictionary["States"]["Add more Social Networks"] == True:
			# Add the Social Network
			self.added_social_network = self.Add_Social_Network()

			if i == 0:
				# Ask the user if they want to add Social Networks to the Friend
				self.dictionary["States"]["Add Social Networks"] = self.Input.Yes_Or_No(self.language_texts["add_social_networks"])

				# If the user do not want to add Social Networks
				if self.dictionary["States"]["Add Social Networks"] == False:
					# Define the "Add more Social Networks" state as False
					self.dictionary["States"]["Add more Social Networks"] = False

			if (
				self.dictionary["States"]["Add Social Networks"] == True and
				self.switches["testing"] == False and
				i != 0
			):
				# Ask if the user wants to add more Social Networks
				self.dictionary["States"]["Add more Social Networks"] = self.Input.Yes_Or_No(self.language_texts["add_more_social_networks"])

			if (
				self.switches["testing"] == True and
				self.friend["Social Networks"]["List"] == ["Discord", "Facebook"]
			):
				self.dictionary["States"]["Add more Social Networks"] = False

			i += 1

		# Sort the Social Networks list
		self.friend["Social Networks"]["List"] = sorted(self.friend["Social Networks"]["List"], key = str.lower)

		# Sort the Social Networks dictionary
		self.friend["Social Networks"]["Dictionary"] = dict(collections.OrderedDict(sorted(self.friend["Social Networks"]["Dictionary"].items())))

	def Add_Social_Network(self):
		# Define the select text
		select_text = self.language_texts["select_a_social_network_to_add_it_to_the_friend_folder"]

		first_separator = True

		# Define the default Social Network
		social_network = None

		# If the Social Networks list of the Friend is empty
		if self.friend["Social Networks"]["List"] == []:
			# Define the first Social Network to be added as the origin Social Network
			variable = self.friend["Information"]["Origin Social Network"].split(" - ")[0]

			# If the origin Social Network is inside the Social Networks list
			if variable in self.social_networks["List"]:
				# Define the "social_network" as the origin Social Network
				social_network = variable

			first_separator = False

		# Select the Social Network and get its dictionary
		self.social_network = self.Select_Social_Network(social_network = social_network, social_networks = self.social_networks_copy, select_text = select_text)

		# If the Social Network is not inside the list of Social Networks of the Friend
		if self.social_network["Name"] not in self.friend["Social Networks"]["List"]:
			# Asks for the user to type information about the selected Social Network
			self.social_network = self.Social_Networks.Type_Social_Network_Information(first_separator = first_separator)

			# Add the Social Network to the Social Networks list
			self.friend["Social Networks"]["List"].append(self.social_network["Name"])

			# Update the number of Social Networks
			self.friend["Social Networks"]["Numbers"]["Total"] = len(self.friend["Social Networks"]["List"])

			# Add it to the Social Networks dictionary
			self.friend["Social Networks"]["Dictionary"][self.social_network["Name"]] = deepcopy(self.social_network["Profile"])

			# Remove the selected Social Network from the list of Social Networks
			self.social_networks_copy["List"].remove(self.social_network["Name"])

			# If the user wants to add Social Networks to an existing Friend
			if self.dictionary["States"]["Add Social Network to existing friend folder"] == True:
				# Add the Social Network to the "New Social Networks" list
				self.dictionary["New Social Networks"]["List"].append(self.social_network["Name"])

				# Update the number of new Social Networks
				self.dictionary["New Social Networks"]["Numbers"]["Total"] = len(self.dictionary["New Social Networks"]["List"])

				# Add the Social Network to the "New Social Networks" dictionary
				self.dictionary["New Social Networks"]["Dictionary"][self.social_network["Name"]] = deepcopy(self.social_network["Profile"])

			# Return the "Added Social Network" variable as True
			return True

		# If the Social Network is inside the list of Social Networks of the Friend
		if self.social_network["Name"] in self.friend["Social Networks"]["List"]:
			# Return the "Added Social Network" variable as False
			return False

	def Define_Friend_Folders_And_Files(self):
		# If the Friend already existed in the Friends database
		if self.friend["Name"] in self.friends["List"]:
			# Change the "Friend already existed" state
			self.dictionary["States"]["Friend already existed"] = True

		# Else, add the Friend to the friends list
		if self.friend["Name"] not in self.friends["List"]:
			self.friends["List"].append(self.friend["Name"])

		# Define and create the friend folder type dictionaries
		for item in ["Text", "Image"]:
			# Define the item key inside the "Files" dictionary
			self.friend["Files"][item] = {}

		# Define and create the friend folders and files
		for item in ["Text", "Image"]:
			folder = self.folders["Friends"][item]["root"] + self.friend["Name"] + "/"

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

				self.friend["Files"][item][key] = folder_dictionary[key]

				# If the item is "Text"
				if item == "Text":
					# Add the file to the "Files" dictionary
					if key == "Information":
						self.friend["Files"][key] = folder_dictionary[key]

					if key == "Social Networks":
						self.friend["Files"][key] = {
							"List": folder_dictionary[key]
						}

			if item == "Image":
				# Create the image "Media" folder
				dict_["Media"] = {
					"root": dict_["root"] + self.Language.language_texts["media, title()"] + "/"
				}

				self.Folder.Create(dict_["Media"]["root"])

			# Define the folders dictionary as the local folders dictionary
			self.friend["Folders"][item] = dict_

		# Add the keys of the "Text" folders dictionary to the root folders dictionary
		self.friend["Folders"].update(self.friend["Folders"]["Text"])

		# ---------- #

		# Update the "Information" and "Social Networks" files of the Friend image folder if the file inside the text folder is different
		for file_name in ["Information", "Social Networks"]:
			files = {}

			# Iterate through the folder type list
			for item in ["Text", "Image"]:
				file = self.friend["Files"][item][file_name]

				files[item] = {
					"File": file,
					"Size": self.File.Contents(file)["size"]
				}

			if files["Text"]["Size"] != files["Image"]["Size"]:
				self.File.Copy(files["Text"]["File"], files["Image"]["File"])

		# ---------- #

		# Social Network folders and profile file creation
		for social_network in self.friend["Social Networks"]["List"]:
			# Update the "self.social_network" variable
			self.social_network = self.Select_Social_Network(social_network)

			# Create the empty "dict_" dictionary for the social network folders
			dict_ = {}

			# Create the empty "Files" dictionary
			files = {}

			# Iterate through the folder type list
			for item in ["Text", "Image"]:
				# Create the item folders dictionary
				dict_ = {
					"root": self.friend["Folders"][item]["Social Networks"]["root"] + social_network + "/"
				}

				self.Folder.Create(dict_["root"])

				# Create the "Profile.txt" file
				dict_["Profile"] = dict_["root"] + self.Language.language_texts["profile, title()"] + ".txt"

				self.File.Create(dict_["Profile"])

				# Add the profile file to the "Files" dictionary
				self.friend["Files"]["Social Networks"][social_network] = {
					"Profile": dict_["Profile"]
				}

				# Define the file for easier typing
				file = dict_["Profile"]

				# Define the File dictionary and size
				files[item] = {
					"File": file,
					"Size": self.File.Contents(file)["size"]
				}

				self.friend["Folders"][item]["Social Networks"][social_network] = dict_

			# Update the "Profile" social network file of the Friend image folder if the file inside the text folder is different
			if files["Text"]["Size"] != files["Image"]["Size"]:
				self.File.Copy(files["Text"]["File"], files["Image"]["File"])

			# Create the Social Network image sub-folders
			if "Image folders" in self.social_network:
				# Define the root image folder
				image_folder = self.friend["Folders"]["Image"]["Social Networks"][social_network]["root"]

				# Create the image sub-folders
				for folder in self.social_network["Image folders"]:
					folder = image_folder + folder + "/"

					self.Folder.Create(folder)

		# Update the number of Social Networks
		self.friend["Social Networks"]["Numbers"]["Total"] = len(self.friend["Social Networks"]["List"])

		# Define the "Friend" dictionary as the local "Friend" dictionary
		self.friends["Dictionary"][self.friend["Name"]] = self.friend

		# Sort the met by year numbers keys
		self.friends["Numbers"]["By year"] = dict(collections.OrderedDict(sorted(self.friends["Numbers"]["By year"].items())))

		# Sort the met by year lists keys
		self.friends["Met by year"] = dict(collections.OrderedDict(sorted(self.friends["Met by year"].items())))

		# Sort the Friends list
		self.friends["List"] = sorted(self.friends["List"], key = str.lower)

		# Sort the Friends dictionary
		self.friends["Dictionary"] = dict(collections.OrderedDict(sorted(self.friends["Dictionary"].items())))

	def Write_To_Files(self):
		# Make a local copy of the Friend "Information" dictionary
		information = deepcopy(self.friend["Information"])

		# Remove the "Places" key
		information.pop("Places")

		# Translate the keys to the user language
		# Using the "Information" method of the "Friends" class
		information = self.Information(information, to_user_language = True)

		# Iterate through the folder type list
		for item in ["Text", "Image"]:
			# Transform the dictionary into a text string
			text_to_write = self.Text.From_Dictionary(information, next_line = True)

			# Write to the "Information.txt" file
			self.File.Edit(self.friend["Files"][item]["Information"], text_to_write, "w")

		# Write to the "Profile.txt" files of the Social Networks
		for social_network in self.friend["Social Networks"]["List"]:
			# Get the "Information" dictionary of the Social Network
			information = self.friend["Social Networks"]["Dictionary"][social_network]

			# Translate the keys to the user language
			# Using the "Information" method of the "Social_Networks" class
			information = self.Social_Networks.Information(information, to_user_language = True)

			# Transform the dictionary into a text string
			text_to_write = self.Text.From_Dictionary(information, next_line = True)

			# Iterate through the folder type list
			for item in ["Text", "Image"]:
				# Get the "Information.txt" file
				file = self.friend["Folders"][item]["Social Networks"][social_network]["Profile"]

				# Write to it
				self.File.Edit(file, text_to_write, "w")

		# ---------- #

		# List the Social Networks
		social_networks_list = self.friend["Social Networks"]["List"]

		# Remove the Social Networks that are not inside the Social Networks database
		for item in social_networks_list.copy():
			if item not in self.social_networks["List"]:
				social_networks_list.remove(item)

		# Update the "Social Networks.txt" file with the list above
		text_to_write = self.Text.From_List(social_networks_list, break_line = True)

		self.File.Edit(self.friend["Files"]["Social Networks"]["List"], text_to_write, "w")

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

	def Show_Information(self):
		# Show a separator
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

		# If the user does not want to add Social Networks to an existing Friend
		if self.dictionary["States"]["Add Social Network to existing friend folder"] == False:
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
				print("\t" + information_item[self.user_language] + ":")

				# Show the Friend information
				print("\t" + information)

				# If the information item is not the last one
				if key != keys[-1]:
					# Show a space separator
					print()

		# ---------- #

		# Define the texts dictionary for easier typing
		texts_dictionary = self.Language.language_texts

		# Define the local Social Networks dictionary
		social_networks = self.friend["Social Networks"]

		# If the user wants to add Social Networks to an existing Friend
		if self.dictionary["States"]["Add Social Network to existing friend folder"] == True:
			social_networks = self.dictionary["New Social Networks"]

		# Define the "Text by number" dictionary
		text_key = "social_network_information"

		# If the user wants to add Social Networks to an existing Friend
		if self.dictionary["States"]["Add Social Network to existing friend folder"] == True:
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

		# Iterate through the Social Networks list
		two_tabs = "\t\t"

		# Iterate through the Social Networks list
		for social_network in social_networks["List"]:
			# Update the "self.social_network" variable
			self.social_network = self.Select_Social_Network(social_network)

			# Show the Social Network name
			print()
			print("\t" + social_network + ":")

			# Define the "information" variable for easier typing
			information = social_networks["Dictionary"][social_network]

			# List the keys of the "Information items" dictionary
			keys = list(self.social_network["Information items"]["Dictionary"].keys())

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
				print(two_tabs + language_information_item + ":")

				if current_information == "":
					current_information = self.Language.language_texts["empty, title()"]

				print(two_tabs + current_information)

		# Show a final separator
		print()
		print(self.separators["5"])
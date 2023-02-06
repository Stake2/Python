# Friends.py

from Social_Networks.Social_Networks import Social_Networks as Social_Networks

class Friends(object):
	def __init__(self, current_year = None, select_social_network = True, social_network = None, remove_social_networks_with_no_friends = False):
		self.Import_Modules()
		self.Define_Module_Folder()
		self.Define_Texts()

		if current_year != None:
			self.date["year"] = current_year

		if social_network != None:
			self.social_network = social_network

		self.Social_Networks = Social_Networks()

		self.social_networks = None
		self.social_networks_with_friends = None

		if remove_social_networks_with_no_friends == True:
			self.social_networks = self.Social_Networks.social_networks

		self.Define_Folders_And_Files()
		self.Define_Lists_And_Dictionaries()
		self.Define_Friend_Dictionaries()

		if remove_social_networks_with_no_friends == True:
			self.all_friend_social_networks = []

			for friend in self.friends:
				self.friend_social_networks = self.friend_data[friend][self.Social_Networks.texts["social_networks"]["en"]]["List"]

				self.all_friend_social_networks.extend(self.friend_social_networks)

			self.social_networks_with_friends = self.social_networks.copy()

			for key in self.social_networks:
				if key not in self.all_friend_social_networks + ["Names"]:
					self.social_networks_with_friends.pop(key)

		self.Select_Social_Network(self.social_networks_with_friends, select_social_network = select_social_network)

	def Import_Modules(self):
		from Utility.Modules import Modules as Modules

		# Get modules dictionary
		self.modules = Modules().Set(self)

	def Define_Module_Folder(self):
		self.module = {
			"name": self.__module__,
		}

		if "." in self.module["name"]:
			self.module["name"] = self.module["name"].split(".")[0]

		self.module["key"] = self.module["name"].lower()

		for item in ["module_files", "modules"]:
			self.folders["apps"][item][self.module["key"]] = self.folders["apps"][item]["root"] + self.module["name"] + "/"
			self.Folder.Create(self.folders["apps"][item][self.module["key"]])

			self.folders["apps"][item][self.module["key"]] = self.Folder.Contents(self.folders["apps"][item][self.module["key"]], lower_key = True)["dictionary"]

	def Define_Texts(self):
		self.texts = self.JSON.To_Python(self.folders["apps"]["module_files"][self.module["key"]]["texts"])

		self.language_texts = self.Language.Item(self.texts)

		self.large_bar = "-----"
		self.dash_space = "-"

	def Define_Folders_And_Files(self):
		# Folders
		self.friends_text_folder = self.folders["notepad"]["effort"]["root"] + self.texts["friends, en - pt, title()"] + "/"
		self.Folder.Create(self.friends_text_folder)

		self.friends_database_folder = self.friends_text_folder + "Database/"
		self.Folder.Create(self.friends_database_folder)

		self.friends_information_folder = self.friends_database_folder + self.texts["information, en - pt, title()"] + "/"
		self.Folder.Create(self.friends_information_folder)

		self.friends_year_numbers_folder = self.friends_database_folder + self.texts["year_numbers, en - pt, capitalize()"] + "/"
		self.Folder.Create(self.friends_year_numbers_folder)

		self.friends_image_folder = self.folders["mega"]["image"]["root"] + self.texts["friends, en - pt, title()"] + "/"
		self.Folder.Create(self.friends_image_folder)

		# Files
		self.friends_file = self.friends_database_folder + self.texts["friends, en - pt, title()"] + ".txt"
		self.File.Create(self.friends_file)

		self.friends_number_file = self.friends_database_folder + self.texts["number, en - pt, title()"] + ".txt"
		self.File.Create(self.friends_number_file)

		self.information_items_file = self.friends_database_folder + self.texts["information_items"]["en"] + ".json"
		self.File.Create(self.information_items_file)

		self.information_file = self.friends_information_folder + self.texts["information, title()"]["en"] + ".json"
		self.File.Create(self.information_file)

	def Define_Lists_And_Dictionaries(self):
		# Lists
		self.file_names = {}

		file_types = ["information", "social_network"]

		# Create file names
		for key in ["en", "language", "language_singular"]:
			self.file_names[key] = []

			for file_type in file_types:
				sub_key = file_type

				if file_type == "social_network" and key != "language_singular":
					sub_key += "s"

				if file_type != "social_network":
					sub_key += ", title()"

				if sub_key in self.texts:
					value = self.texts[sub_key]

				else:
					value = self.Social_Networks.texts[sub_key]

				if key == "en":
					value = value["en"]

				if key != "en":
					value = value[self.user_language]

				self.file_names[key].append(value)

		# Add information items list to texts dictionary
		self.texts["information_items, type: list"] = self.JSON.To_Python(self.information_items_file)

		dict_ = {}

		i = 0
		for information_item in self.texts["information_items, type: list"]["en"]:
			key = information_item.lower().replace(" ", "_")

			dict_[key] = {}

			for language in self.texts["information_items, type: list"]:
				if language not in ["formats", "plural"]:
					dict_[key][language] = self.texts["information_items, type: list"][language][i]

			i += 1

		# Add information items to texts dictionary
		self.texts.update(dict_)

		# Add information items to texts JSON file
		self.JSON.Edit(self.folders["apps"]["module_files"][self.module["key"]]["texts"], self.texts)

		self.exact_match_information_items = [
			self.texts["name"]["en"],
			self.texts["age"]["en"],
			self.texts["hometown"]["en"],
			self.texts["residence_place"]["en"],
		]

		# List Friend folders
		self.friends_folders = self.Folder.Contents(self.friends_text_folder)["folder"]["names"]

		# Remove non-Friend folders from the above list
		for item in ["Database", "Pre-Friends", "Archive"]:
			if item in self.friends_folders:
				self.friends_folders.remove(item)

		# Gets the number of Friends
		self.friends_number = str(len(self.friends_folders))

		# Writes the Friends to the Friends file
		self.File.Edit(self.friends_file, self.Text.From_List(self.friends_folders), "w")

		# Writes the number of Friends to the Friends number file
		self.File.Edit(self.friends_number_file, self.friends_number, "w")

		self.friends = self.friends_folders

		# Dictionaries
		i = 0
		for information_item in self.texts["information_items, type: list"]["en"]:
			self.texts["information_items, type: list"][information_item] = self.texts["information_items, type: list"]["formats"][i]

			i += 1

		# Gender letters
		self.gender_letters = {}

		self.gender_items = ["the", "this", "part_of"]

		for item in self.gender_items:
			self.gender_letters[item] = {}

		# Information items that have the masculine gender in Portuguese
		self.portuguese_o_letter_items = [
			self.texts["name"]["en"],
			self.texts["gender"]["en"],
			self.texts["birthday"]["en"],
			self.texts["residence_place"]["en"],
		]

		# Define gender letters by information item in Portuguese
		for information_item in self.texts["information_items, type: list"]["en"]:
			if information_item in self.portuguese_o_letter_items:
				for item in self.gender_items:
					self.gender_letters[item][information_item] = self.language_texts[item + ", masculine"]

			if information_item not in self.portuguese_o_letter_items:
				for item in self.gender_items:
					self.gender_letters[item][information_item] = self.language_texts[item + ", feminine"]

	def Define_Friend_Dictionaries(self):
		self.friend_folders = {}
		self.friend_files = {}
		self.friend_data = {}
		self.year_friends_numbers = {}

		# Friends folders, files, and data dictionaries filling
		for friend in self.friends:
			self.friend_folders[friend] = {}
			self.friend_files[friend] = {}
			self.friend_data[friend] = {}

			self.friend_files[friend][self.Social_Networks.texts["social_network"]["en"]] = {}

			# Friends folders
			self.friend_folders[friend]["Text"] = {}

			self.friend_folders[friend]["Text"]["root"] = self.friends_text_folder + friend + "/"
			self.Folder.Create(self.friend_folders[friend]["Text"]["root"])

			self.friend_folders[friend]["Text"][self.Social_Networks.texts["social_networks"]["en"]] = self.friend_folders[friend]["Text"]["root"] + self.Social_Networks.texts["social_networks, en - pt, title()"] + "/"
			self.Folder.Create(self.friend_folders[friend]["Text"][self.Social_Networks.texts["social_networks"]["en"]])

			# Image folders
			self.friend_folders[friend]["Image"] = {}

			self.friend_folders[friend]["Image"]["root"] = self.friends_image_folder + friend + "/"
			self.Folder.Create(self.friend_folders[friend]["Image"]["root"])

			self.friend_folders[friend]["Image"][self.Social_Networks.texts["social_networks"]["en"]] = self.friend_folders[friend]["Image"]["root"] + self.Social_Networks.texts["social_networks, en - pt, title()"] + "/"
			self.Folder.Create(self.friend_folders[friend]["Image"][self.Social_Networks.texts["social_networks"]["en"]])

			# Friend file names iteration
			for file_name in self.file_names["en"]:
				key = file_name

				text_folder = self.friend_folders[friend]["Text"]["root"]

				if file_name == self.Social_Networks.texts["social_networks"]["en"]:
					text_folder = self.friend_folders[friend]["Text"][self.Social_Networks.texts["social_networks"]["en"]]
					self.Folder.Create(text_folder)

					file_name = self.Social_Networks.texts["social_networks, en - pt, title()"]

				# Friends files
				self.friend_files[friend][key] = text_folder + file_name + ".txt"
				self.File.Create(self.friend_files[friend][key])

				if key == self.Social_Networks.texts["social_networks"]["en"]:
					social_networks = self.Folder.Contents(text_folder)["folder"]["names"]
					self.File.Edit(self.friend_files[friend][key], self.Text.From_List(social_networks), "w")

				# Friends data
				if key == self.Social_Networks.texts["social_networks"]["en"]:
					self.friend_data[friend][key] = {}
					self.friend_data[friend][key]["List"] = self.File.Contents(self.friend_files[friend][key])["lines"]

					self.friend_data[friend][key]["Data"] = {}						

				if key != self.Social_Networks.texts["social_networks"]["en"]:
					self.friend_data[friend][key] = self.File.Dictionary(self.friend_files[friend][key], next_line = True)

			# Social Network folders and profile file creation
			for social_network in self.friend_data[friend][self.Social_Networks.texts["social_networks"]["en"]]["List"]:
				self.friend_files[friend][self.Social_Networks.texts["social_network"]["en"]][social_network] = {}

				self.Select_Social_Network(social_network, True)

				# Text folder
				text_folder = self.friend_folders[friend]["Text"][self.Social_Networks.texts["social_networks"]["en"]] + social_network + "/"
				self.Folder.Create(text_folder)

				# Text profile file
				text_profile_file = text_folder + self.texts["profile, title()"]["en"] + ".txt"
				self.File.Create(text_profile_file)

				# Image folder
				image_folder = self.friend_folders[friend]["Image"][self.Social_Networks.texts["social_networks"]["en"]] + social_network + "/"
				self.Folder.Create(image_folder)

				# Image profile file
				image_profile_file = image_folder + self.texts["profile, title()"]["en"] + ".txt"
				self.File.Create(image_profile_file)

				# Definition of keys
				self.friend_files[friend][self.Social_Networks.texts["social_network"]["en"]][social_network]["Text profile"] = text_profile_file
				self.friend_files[friend][self.Social_Networks.texts["social_network"]["en"]][social_network]["Image profile"] = image_profile_file

				# Definition of Social Network data
				self.friend_data[friend][key]["Data"][social_network] = self.File.Dictionary(self.friend_files[friend][self.Social_Networks.texts["social_network"]["en"]][social_network]["Text profile"], next_line = True)

				if "data" in self.social_network:
					for folder in self.social_network["data"]["Image folders"]:
						sub_image_folder = image_folder + folder + "/"
						self.Folder.Create(sub_image_folder)

			self.Folder.Copy(self.friend_folders[friend]["Text"]["root"], self.friend_folders[friend]["Image"]["root"])

			# Definition of the year I met the Friend
			self.year_i_met = self.friend_data[friend]["Information"]["Date I met"].split("/")[-1]

			if self.year_i_met not in self.year_friends_numbers:
				self.year_friends_numbers[self.year_i_met] = 0

			if self.year_i_met in self.year_friends_numbers:
				self.year_friends_numbers[self.year_i_met] += 1

		for year in range(2018, self.date["year"] + 1):
			if str(year) not in self.year_friends_numbers:
				self.year_friends_numbers[str(year)] = 0

		for year in self.year_friends_numbers:
			year_folder = self.friends_year_numbers_folder + year + "/"
			self.Folder.Create(year_folder)

			number_file = year_folder + self.texts["number, en - " + self.user_language + ", title()"] + ".txt"
			self.File.Create(number_file)

			number = str(self.year_friends_numbers[year])

			self.File.Edit(number_file, number, "w")

		# Define information dictionary
		self.information = {}

		for information_item in self.texts["information_items, type: list"]["en"]:
			# Define and create information item file if it does not exist
			information_item_file = self.friends_information_folder + information_item + ".txt"
			self.File.Create(information_item_file)

			information_list = []

			# Iterate through Friends list
			for friend in self.friends:
				# Add Friend key to information dictionary
				if friend not in self.information:
					self.information[friend] = {}

				# Get information from Friend data
				if information_item in self.friend_data[friend]["Information"]:
					information = self.friend_data[friend]["Information"][information_item]

				# If information is not present, use the "Not filled" value
				if information_item not in self.friend_data[friend]["Information"]:
					information = self.language_texts["not_filled"]

				# Add information to Friend dictionary on Information dictionary
				self.information[friend][information_item] = information

				# Add information to list
				information_list.append(information)

			# Edit information file of information item
			text_to_write = self.Text.From_List(information_list)
			self.File.Edit(information_item_file, text_to_write, "w")

		# Edit Information.json file to add JSON dictionary
		self.JSON.Edit(self.information_file, self.information)

		self.current_year_friends_number = self.year_friends_numbers[str(self.date["year"])]

	def Select_Friend(self, friends = None, select_text = None, first_space = True, second_space = True):
		if friends != None:
			self.friends = friends

		show_text = self.language_texts["friends, title()"]

		if select_text == None:
			select_text = self.language_texts["select_one_friend"]

		self.option_info = self.Input.Select(self.friends, show_text = show_text, select_text = select_text)

		self.friend = self.option_info["option"]
		self.friend_number = self.option_info["number"]

		self.friend_information = self.File.Dictionary(self.friend_files[self.friend]["Information"], next_line = True)

		if "List" in self.friend_data[self.friend][self.Social_Networks.texts["social_networks"]["en"]]:
			self.friend_social_networks = self.friend_data[self.friend][self.Social_Networks.texts["social_networks"]["en"]]["List"]

	def Select_Social_Network(self, social_network = None, select_social_network = True, social_networks = None, select_text = None):
		if social_networks == None:
			social_networks = self.social_networks

		self.social_network = self.Social_Networks.Select_Social_Network(social_network = social_network, select_social_network = select_social_network, social_networks = social_networks, select_text = select_text)

		return self.social_network
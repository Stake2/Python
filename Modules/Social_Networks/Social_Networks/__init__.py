# Social_Networks.py

class Social_Networks(object):
	def __init__(self):
		self.Define_Basic_Variables()

		# Define module folders
		from Utility.Define_Folders import Define_Folders as Define_Folders

		Define_Folders(self)

		self.Define_Texts()

		self.Define_Folders_And_Files()
		self.Define_Lists_And_Dictionaries()
		self.Define_Social_Network_Dictionaries()

	def Define_Basic_Variables(self):
		from Utility.Global_Switches import Global_Switches as Global_Switches

		from Utility.File import File as File
		from Utility.Folder import Folder as Folder
		from Utility.Date import Date as Date
		from Utility.Input import Input as Input
		from Utility.JSON import JSON as JSON
		from Utility.Text import Text as Text

		self.switches = Global_Switches().switches["Global"]

		self.File = File()
		self.Folder = Folder()
		self.Date = Date()
		self.Input = Input()
		self.JSON = JSON()
		self.Text = Text()

		self.languages = self.JSON.Language.languages

		self.user_language = self.JSON.Language.user_language
		self.full_user_language = self.JSON.Language.full_user_language

		self.Sanitize = self.File.Sanitize

		self.folders = self.Folder.folders

		self.date = self.Date.date

	def Define_Texts(self):
		self.texts = self.JSON.To_Python(self.folders["apps"]["module_files"][self.module["key"]]["texts"])

		self.language_texts = self.JSON.Language.Item(self.texts)

		self.large_bar = "-----"
		self.dash_space = "-"

	def Define_Folders_And_Files(self):
		# Folders
		self.social_networks_text_folder = self.folders["notepad"]["effort"]["root"] + self.texts["social_networks"]["en"] + "/"
		self.Folder.Create(self.social_networks_text_folder)

		self.social_networks_database_folder = self.social_networks_text_folder + "Database/"
		self.Folder.Create(self.social_networks_database_folder)

		self.social_networks_image_folder = self.folders["mega"]["image"]["root"] + self.texts["social_networks"]["en"] + "/"
		self.Folder.Create(self.social_networks_image_folder)

		self.digital_identities_folder = self.social_networks_image_folder + "Digital identities/"
		self.Folder.Create(self.digital_identities_folder)

		# Files
		self.social_networks_file = self.social_networks_database_folder + self.texts["social_networks"]["en"] + ".txt"
		self.File.Create(self.social_networks_file)

		self.social_networks_links_file = self.social_networks_database_folder + "Links.txt"
		self.File.Create(self.social_networks_links_file)

	def Define_Lists_And_Dictionaries(self):
		# Lists
		self.social_networks = {
			"Names": self.File.Contents(self.social_networks_file)["lines"],
			"Links": [],
			"Information items": {},
		}

		for language in self.languages["small"]:
			self.social_networks["Information items"][language] = []

		self.file_names = {}

		file_name_keys = ["information", "information_item", "image_folder", "profile", "setting"]

		for key in ["en", "language", "language_singular"]:
			self.file_names[key] = []

			for file_name_key in file_name_keys:
				sub_key = file_name_key

				if key != "language_singular" and sub_key != "information":
					sub_key += "s"

				if file_name_key in ["information", "profile", "setting"]:
					sub_key += ", title()"

				value = self.texts[sub_key]

				if key == "en":
					value = value["en"]

				if key != "en":
					value = value[self.user_language]

				self.file_names[key].append(value)

		self.file_names["en"][-2] = self.texts["profile, title()"]["en"]

	def Define_Social_Network_Dictionaries(self):
		# Dictionaries
		self.texts["information_items, type: list"] = {}

		dict_keys = ["folders", "files", "data", "links"]

		# Social Networks iteration
		for social_network in self.social_networks["Names"]:
			self.social_networks[social_network] = {}
			self.social_networks[social_network]["Name"] = social_network

			# Create dictionary keys
			for item in dict_keys:
				self.social_networks[social_network][item] = {}

			# Text folder
			self.social_networks[social_network]["folders"]["Text"] = self.social_networks_text_folder + social_network + "/"
			self.Folder.Create(self.social_networks[social_network]["folders"]["Text"])

			# Settings
			settings = {
				self.texts["image_folders"]["en"]: True,
			}

			if self.File.Exist(self.social_networks[social_network]["folders"]["Text"] + "Settings.txt") == True:
				settings = self.File.Dictionary(self.social_networks[social_network]["folders"]["Text"] + "Settings.txt", next_line = True)

			if settings[self.texts["image_folders"]["en"]] == True:
				# Image folder
				self.social_networks[social_network]["folders"]["Image"] = self.social_networks_image_folder + social_network + "/"
				self.Folder.Create(self.social_networks[social_network]["folders"]["Image"])

			# Social Network files
			for file_name in self.file_names["en"]:
				self.social_networks[social_network]["files"][file_name] = self.social_networks[social_network]["folders"]["Text"] + file_name + ".txt"

				if file_name == self.texts["information_items"]["en"]:
					self.social_networks[social_network]["files"][file_name] = self.social_networks[social_network]["files"][file_name].replace("txt", "json")

				# If the file name is not "Settings", create file
				if file_name != self.texts["settings, title()"]["en"]:
					self.File.Create(self.social_networks[social_network]["files"][file_name])

				# If the file name is "Settings" and file does not exist, delete key from dictionary
				if file_name == self.texts["settings, title()"]["en"] and self.File.Exist(self.social_networks[social_network]["folders"]["Text"] + file_name + ".txt") == False:
					del self.social_networks[social_network]["files"][file_name]

				# If file name in dictionary and file exists
				if file_name in self.social_networks[social_network]["files"] and self.File.Exist(self.social_networks[social_network]["files"][file_name]) == True:
					# If file uses dictionary format
					if file_name in [self.JSON.Language.texts["information, title()"]["en"], self.texts["profile, title()"]["en"], self.texts["settings, title()"]["en"]]:
						self.social_networks[social_network]["data"][file_name] = self.File.Dictionary(self.social_networks[social_network]["files"][file_name], next_line = True)

					# If file uses list format
					if file_name == self.texts["image_folders"]["en"]:
						self.social_networks[social_network]["data"][file_name] = self.File.Contents(self.social_networks[social_network]["files"][file_name])["lines"]

					# If file uses JSON format
					if file_name == self.texts["information_items"]["en"]:
						self.social_networks[social_network]["data"][file_name] = self.JSON.To_Python(self.social_networks[social_network]["files"][file_name])

			# Add information items to root information items key
			for key in self.social_networks[social_network]["data"]["Information items"]:
				# If type of information items key is list, add to list
				self.social_networks[social_network]["data"]["Information items"] = self.JSON.To_Python(self.social_networks[social_network]["files"]["Information items"])

				for item in self.social_networks[social_network]["data"]["Information items"][key]:
					if item not in self.social_networks["Information items"][key]:
						self.social_networks["Information items"][key].append(item)

			# Add Social Network link to links list
			self.social_networks["Links"].append(self.social_networks[social_network]["data"]["Information"]["Link"])

			# Social Network profile
			self.social_networks[social_network]["profile"] = {}
			self.social_networks[social_network]["profile"].update(self.social_networks[social_network]["data"]["Profile"])

			for key in self.social_networks[social_network]["data"]["Information"]:
				value = self.social_networks[social_network]["data"]["Information"][key]

				key = key.lower()

				if "link" in key and "{" in value:
					link = value.split("{")[0]
					information_key = value.split("{")[-1].split("}")[0]

					information = self.social_networks[social_network]["data"]["Profile"][information_key]

					if information_key == "Number":
						information = information.replace(" ", "").replace("-", "")

					key = key.replace(" link", "")

					self.social_networks[social_network]["profile"][key] = link + information

			# Social Network normal, profile, and message links
			for key in ["Link", "Profile", "Message"]:
				item = key

				key = key.lower()

				self.social_networks[social_network]["links"][key] = "None"

				if "Link" not in item:
					item += " link"

				# If item is in Social Network information, add it to the Social Networks links sub-dictionary
				if item in self.social_networks[social_network]["data"]["Information"]:
					self.social_networks[social_network]["links"][key] = self.social_networks[social_network]["data"]["Information"][item]

				if item in self.social_networks[social_network]:
					self.social_networks[social_network][item] = self.social_networks[social_network]["links"][key]

		# Add information items list and dict to texts dictionary
		self.texts["information_items, type: list"] = self.social_networks["Information items"]

		dict_ = {}

		i = 0
		for information_item in self.texts["information_items, type: list"]["en"]:
			key = information_item.lower().replace(" ", "_")

			dict_[key] = {}
			dict_[key]["en"] = information_item

			for language in self.texts["information_items, type: list"]:
				dict_[key][language] = self.texts["information_items, type: list"][language][i]

			i += 1

		# Add information items to texts dictionary
		self.texts.update(dict_)

		# Add information items to texts JSON file
		self.JSON.Edit(self.folders["apps"]["module_files"][self.module["key"]]["texts"], self.texts)

		# Update Social Networks links file
		self.File.Edit(self.social_networks_links_file, self.Text.From_List(self.social_networks["Links"]), "w")

		# Gender letters
		self.gender_letters = {}
		self.user_name_items = {}

		self.gender_items = ["the", "this", "part_of"]

		for item in self.gender_items:
			self.gender_letters[item] = {}

		i = 0
		for information_item in self.texts["information_items, type: list"]["en"]:
			for item in self.gender_items:
				self.gender_letters[item][information_item] = self.language_texts[item + ", masculine"]

			if information_item in ["Nick and Tag", "Username", "Handle", "Contact name"]:
				self.user_name_items[information_item] = self.texts["information_items, type: list"]["en"]

		# Create link types per language, home and profile
		self.link_types = {}

		for language in self.languages["small"]:
			self.link_types[language] = []
			self.link_types[language].append(self.texts["home, title()"][language])
			self.link_types[language].append(self.texts["profile, title()"][language])

		self.link_types_map = {
			self.texts["home, title()"]["en"]: "Link",
			self.texts["profile, title()"]["en"]: "Profile link",
		}

	def Select_Social_Network(self, social_network = None, select_social_network = True, social_networks = None, show_text = None, select_text = None):
		if social_networks == None:
			social_networks = self.social_networks

		if show_text == None:
			show_text = self.language_texts["social_networks"]

		if select_text == None:
			select_text = self.language_texts["select_one_social_network_to_use"]

		if select_social_network == True:
			if social_network == None:
				self.social_network = self.Input.Select(social_networks["Names"], show_text = show_text, select_text = select_text)["option"]

			if social_network != None:
				self.social_network = social_network

			if self.social_network in social_networks:
				self.social_network = social_networks[self.social_network]

				return self.social_network

			else:
				return {}

		else:
			return {}

	def Type_Social_Network_Information(self):
		print()
		print("-----")
		print()
		print(self.language_texts["please_type_the_social_network_profile_information"] + ":")

		self.social_network_information = {}
		self.social_network_information[self.social_network["Name"]] = {}

		i = 0
		for information_item in self.social_network["data"][self.texts["information_items"]["en"]]["en"]:
			language_information_item = self.social_network["data"][self.texts["information_items"]["en"]][self.user_language][i]

			information = self.Input.Type(language_information_item, next_line = True)

			self.social_network_information[self.social_network["Name"]][information_item] = information

			# Format Social Network link if information_item is present in Social Network data values
			for social_network_information_item in list(self.social_network["data"]["Information"].values()):
				if information_item in ["Profile link", "Message link", "Message ID"] and information_item in social_network_information_item:
					information = social_network_information_item.replace("{" + information_item + "}", "") + information

				if information_item in self.social_network["data"]["Information"]["Profile link"]:
					link = self.social_network["data"]["Information"]["Profile link"]
					self.social_network_information[self.social_network["Name"]]["Profile link"] = link.replace("{" + information_item + "}", "") + information

				if information_item in self.social_network["data"]["Information"]["Message link"]:
					link = self.social_network["data"]["Information"]["Message link"]
					self.social_network_information[self.social_network["Name"]]["Message link"] = link.replace("{" + information_item + "}", "") + information

			i += 1

		print()
		print("-----")
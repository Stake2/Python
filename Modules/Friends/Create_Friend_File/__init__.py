# Create_Friend_File.py

from Friends.Friends import Friends as Friends

class Create_Friend_File(Friends):
	def __init__(self):
		super().__init__()

		# Ask if the user wants to add Social Networks to an existing Friend folder
		self.add_social_network = self.Input.Yes_Or_No(self.language_texts["add_social_network_to_friend_folder"])

		# If the user wants to add Social Networks, select a Friend to do that
		if self.add_social_network == True:
			self.Select_Friend()

		# If not, type the information of the new added Friend
		if self.add_social_network == False:
			self.Type_Friend_Information()

		self.add_more_social_networks = True

		# Add Social Networks to an existing Friend or the newly added Friend
		self.friend_social_networks = {}

		while self.add_more_social_networks == True:
			self.Add_Social_Network()

			self.add_more_social_networks = self.Input.Yes_Or_No(self.language_texts["add_more_social_networks"])

		self.Define_Friend_Folders_And_Files()
		self.Write_To_Files()

		# Defines the information and fills the Friend-related dictionaries
		super().__init__()

		self.Show_Information()

	def Type_Friend_Information(self):
		print()
		print(self.large_bar)
		print()
		print(self.language_texts["please_type_the_information_of_the_friend"] + ":")

		self.friend_information = {}

		i = 0
		for information_item in self.information_items["en"]:
			key = information_item.lower().replace(" ", "_")

			language_information_item = self.information_items[self.user_language][i]
			language_information_item_format = self.information_items[information_item]

			if key + ", type: list" not in self.language_texts and information_item != self.texts["origin_social_network"]["en"]:
				friend_information = self.Input.Type(language_information_item, accept_enter = True, next_line = True, regex = language_information_item_format)

			if key + ", type: list" in self.language_texts:
				plural_text = self.information_items["plural"][self.user_language][i]

				friend_information = self.Input.Select(self.texts[key + ", type: list"]["en"], language_options = self.language_texts[key + ", type: list"], show_text = plural_text, select_text = language_information_item)["option"]

			if information_item == self.texts["origin_social_network"]["en"]:
				select_text = self.language_texts["select_the_social_network_where_you_met_{}"].format(self.language_texts["the_friend" + ", " + self.friend_information["Gender"].lower()])
				friend_information = self.Select_Social_Network(select_text = select_text)["Name"]

				question = self.language_texts["add_additional_information_about_origin_social_network"]
				self.add_additional_information = self.Input.Yes_Or_No(question = question)

				if self.add_additional_information == True:
					type_text = self.language_texts["type_the_additional_information"]
					friend_information += " - " + self.Input.Type(type_text)

			self.friend_information[information_item] = friend_information

			i += 1

		print()
		print(self.large_bar)

	def Add_Social_Network(self):
		select_text = self.language_texts["select_a_social_network_to_add_it_to_the_friend_folder"]

		self.Select_Social_Network(select_text = select_text)

		# The user types information about the selected Social Network
		self.Social_Networks.Type_Social_Network_Information()

		self.friend_social_networks.update(self.Social_Networks.social_network_information)

	def Define_Friend_Folders_And_Files(self):
		self.friend = self.friend_information["Name"]

		self.friend_already_existed = False

		if self.friend in self.friends:
			self.friend_already_existed = True

		if self.friend not in self.friends:
			self.friends.append(self.friend)

		self.friend_files[self.friend] = {}

		self.friend_folders[self.friend] = {
			"Text": {},
			"Image": {}
		}

		# Define the text folder
		self.friend_folders[self.friend]["Text"]["root"] = self.folders["Friends"]["Text"]["root"] + self.friend + "/"
		self.Folder.Create(self.friend_folders[self.friend]["Text"]["root"])

		# Define the image folder
		self.friend_folders[self.friend]["Image"]["root"] = self.folders["Friends"]["Image"]["root"] + self.friend + "/"
		self.Folder.Create(self.friend_folders[self.friend]["Image"]["root"])

		# Define the Social Networks folder
		self.friend_folders[self.friend]["Text"]["Social Networks"] = self.friend_folders[self.friend]["Text"]["root"] + self.Social_Networks.language_texts["social_networks, title()"] + "/"
		self.Folder.Create(self.friend_folders[self.friend]["Text"]["Social Networks"])

		# Friend file names iteration
		for key, dict_ in self.friends["File names"]["Dictionary"].items():
			file_name = dict_["Plural"][self.user_language]

			folder = self.friend_folders[self.friend]["Text"]["root"]

			if file_name == "Social Networks":
				folder = self.friend_folders[self.friend]["Text"]["Social Networks"]

			self.friend_files[self.friend][key] = folder + file_name + ".txt"

			self.File.Create(self.friend_files[self.friend][key])

	def Write_To_Files(self):
		# Friend file names iteration
		for key, dict_ in self.friends["File names"]["Dictionary"].items():
			file_name = dict_["Plural"][self.user_language]

			file = self.friend_files[self.friend][key]

			if file_name == "Information":
				self.File.Edit(file, self.Text.From_Dictionary(self.friend_information, next_line = True), "w")

			if file_name == "Social Networks":
				for social_network in self.friend_social_networks:
					social_network_information = self.friend_social_networks[social_network]

					folder = self.friend_folders[self.friend]["Text"]["Social Networks"] + social_network + "/"
					self.Folder.Create(folder)

					file = folder + self.JSON.Language.texts["profile, title()"]["en"] + ".txt"
					self.File.Create(file)

					self.File.Edit(file, self.Text.From_Dictionary(social_network_information, next_line = True), "w")

		# Transform the list of Friend Social Networks into a string and write it into the "Social Networks" file
		text_to_write = self.Text.From_List(list(self.friend_social_networks.keys()))

		self.File.Edit(self.friend_files[self.friend]["Social Networks"], text_to_write, "w")

		# Copy the contents of the text folder into the image folder
		self.File.Copy(self.friend_folders[self.friend]["Text"]["root"], self.friend_folders[self.friend]["Image"]["root"])

		if self.switches["verbose"] == True:
			print()
			print("Folders: " + self.JSON.From_Python(self.friend_folders[self.friend]))
			print()
			print("Files: " + self.JSON.From_Python(self.friend_files[self.friend]))

	def Show_Information(self):
		print()
		print(self.large_bar)
		print()

		text_to_show = "you_added_this_friend_to_the_friends_list"

		if self.friend_already_existed == True:
			text_to_show = "this_friend_already_existed_on_the_friends_list"

		print(self.language_texts[text_to_show] + ":")
		print(self.friend)
		print()

		print(self.language_texts["friend_information"] + ":")

		i = 0
		for information_item in self.friend_information:
			information = self.friend_information[information_item]

			print("\t" + self.information_items[self.user_language][i] + ":")
			print("\t" + information)

			if information != list(self.friend_information.keys())[-1]:
				print()

			i += 1

		text_to_show = self.Text.By_Number(len(list(self.friend_social_networks.keys())), self.Social_Networks.language_texts["social_network_information"], self.Social_Networks.language_texts["social_networks_information"])

		print(text_to_show + ":")

		for social_network in self.friend_social_networks:
			social_network_information = self.friend_social_networks[social_network]

			print("\t" + social_network + ":")

			i = 0
			for information_item in self.Social_Networks.texts["information_items, type: list"]["en"]:
				if information_item in social_network_information:
					language_information_item = self.Social_Networks.texts["information_items, type: list"][self.user_language][i]

					information = social_network_information[information_item]

					print("\t\t" + language_information_item + ":")
					print("\t\t" + information)
					print()

				i += 1

		print(self.large_bar)

		self.Input.Type(self.JSON.Language.language_texts["press_enter_when_you_finish_reading_the_info_summary"])
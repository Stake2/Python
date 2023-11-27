# Show_Friend_Information.py

from Friends.Friends import Friends as Friends

from Friends.Open_Friend_File import Open_Friend_File as Open_Friend_File

class Show_Friend_Information(Friends):
	def __init__(self):
		super().__init__()

		self.Select_File_Type()
		self.Create_Information_Items()
		self.Select_Information_Item()
		self.Show_Information()

	def Select_File_Type(self):
		self.information_item_dict = {
			self.JSON.Language.texts["information, title()"]["en"]: {
				"English": self.information_items["en"],
				self.full_user_language: self.information_items["information_items, type: dict, en: " + self.user_language],
			},

			"Social Networks": {
				"English": self.Social_Networks.texts["information_items, type: list"]["en"],
				self.full_user_language: self.Social_Networks.texts["information_items, type: list"]["information_items, type: dict, en: " + self.user_language]
			}
		}

		self.file_name = Open_Friend_File(run_as_module = True).file_name_dict["file_name"]["en"]

		self.english_information_items = self.information_item_dict[self.file_name]["English"]

		self.information_items[self.user_language] = self.information_item_dict[self.file_name][self.full_user_language]
		self.language_information_items_backup = self.information_items[self.user_language].copy()

	def Create_Information_Items(self):
		self.friend_information_items = {}
		self.friend_social_networks = {}

		for friend in self.friends:
			self.friend_information_items[friend] = {}

			friend_data = self.friend_data[friend][self.file_name]

			if self.file_name == self.JSON.Language.texts["information, title()"]["en"]:
				self.friend_social_networks[friend] = {"None": None}

			if self.file_name == "Social Networks":
				self.friend_social_networks[friend] = friend_data["List"]

				friend_data = friend_data["Data"]

			friend_sub_data = friend_data

			for social_network in self.friend_social_networks[friend]:
				if self.file_name == "Social Networks":
					self.friend_information_items[friend][social_network] = {}

					friend_sub_data = friend_data[social_network]

				for information_item in self.english_information_items:
					if information_item in friend_sub_data:
						if self.file_name == self.JSON.Language.texts["information, title()"]["en"]:
							self.friend_information_items[friend][information_item] = friend_sub_data[information_item]

						if self.file_name == "Social Networks":
							self.friend_information_items[friend][social_network][information_item] = friend_sub_data[information_item]

		self.social_networks_information_items = {}

		self.friend_social_networks_backup = self.friend_social_networks.copy()

		for friend in self.friends:
			for social_network in self.friend_social_networks_backup[friend]:
				for information_item in self.english_information_items:
					if self.file_name == self.JSON.Language.texts["information, title()"]["en"]:
						friend_information_items = self.friend_information_items[friend]

					if self.file_name == "Social Networks":
						friend_information_items = self.friend_information_items[friend][social_network]

					if information_item in friend_information_items:
						if information_item not in self.social_networks_information_items:
							self.social_networks_information_items[information_item] = ""

						if self.file_name == "Social Networks" and social_network not in self.social_networks_information_items[information_item]:
							self.social_networks_information_items[information_item] += social_network

							string = self.social_networks_information_items[information_item]

							if string.split()[len(string)-2:] != ", ":
								self.social_networks_information_items[information_item] += ", "

		for friend in self.friends:
			for information_item in self.english_information_items.copy():
				if information_item not in self.social_networks_information_items:
					if information_item in self.english_information_items:
						self.english_information_items.remove(information_item)

					if information_item in self.information_items[self.user_language]:
						self.information_items[self.user_language].pop(information_item)

		if self.file_name == "Social Networks":
			for friend in self.friends:
				for social_network in self.friend_social_networks[friend]:
					for information_item in self.english_information_items:
						string = self.social_networks_information_items[information_item]

						if string[len(string)-2:] == ", ":
							self.social_networks_information_items[information_item] = string[:-2]

						self.information_items[self.user_language][information_item] = self.social_networks_information_items[information_item] + ": " + self.language_information_items_backup[information_item]

	def Select_Information_Item(self):
		show_text = self.language_texts["information_items"]
		select_text = self.language_texts["select_one_information_item"]

		self.option_info = self.Input.Select(self.english_information_items, list(self.information_items[self.user_language].values()), show_text = show_text, select_text = select_text)

		self.information_item = self.option_info["option"]
		self.information_item_number = self.option_info["number"]

		if self.file_name == "Social Networks":
			self.language_information_item_with_social_network = self.information_items[self.user_language][self.information_item]

		self.language_information_item = self.information_items[self.user_language].copy()[self.information_item]

		for friend in self.friends.copy():
			for social_network in self.friend_social_networks[friend].copy():
				if self.file_name == self.JSON.Language.texts["information, title()"]["en"]:
					friend_information_items = self.friend_information_items[friend]

				if self.file_name == "Social Networks":
					friend_information_items = self.friend_information_items[friend][social_network]

				if self.information_item not in friend_information_items and social_network in self.friend_social_networks[friend]:
					self.friend_social_networks[friend].remove(social_network)

		for friend in self.friends.copy():
			if self.friend_social_networks[friend] == []:
				self.friends.remove(friend)
				self.friend_social_networks.pop(friend)
				self.friend_information_items.pop(friend)

	def Show_Information(self):
		print()
		print(self.large_bar)

		for friend in self.friend_information_items:
			print()
			print(friend + ":")
			print()

			for social_network in self.friend_social_networks[friend]:
				friend_information_items = self.friend_information_items[friend]

				if self.file_name == "Social Networks":
					friend_information_items = friend_information_items[social_network]

				i = 0
				for information_item in friend_information_items:
					if information_item == self.information_item:
						information = friend_information_items[information_item]

						if self.file_name == "Social Networks":
							if social_network != self.friend_social_networks[friend][0]:
								print()

							print(self.JSON.Language.language_texts["social_network"] + ":")
							print(social_network)
							print()

						print(self.language_information_item.split(": ")[-1] + ":")
						print(information)
						print()

						if self.file_name == self.JSON.Language.texts["information, title()"]["en"]:
							print("---")

						if self.file_name == "Social Networks":
							if len(self.friend_social_networks[friend]) == 1 or \
								len(self.friend_social_networks[friend]) > 1 and social_network == self.friend_social_networks[friend][-1]:
								print("---")

							if len(self.friend_social_networks[friend]) > 1 and social_network != self.friend_social_networks[friend][-1]:
								print("-")

					i += 1
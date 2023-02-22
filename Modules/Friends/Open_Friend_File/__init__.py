# Open_Friend_File.py

from Friends.Friends import Friends as Friends

from Social_Networks.Social_Networks import Social_Networks as Social_Networks

import re

class Open_Friend_File(Friends):
	def __init__(self, run_as_module = False, social_network = None, open_social_network_file = None):
		super().__init__(select_social_network = False, social_network = social_network, remove_social_networks_with_no_friends = True)

		self.run_as_module = run_as_module

		if open_social_network_file == None or self.run_as_module == True:
			self.Select_File_Type()

		if self.run_as_module == False:
			self.singular_file_type = self.singular_file_type.lower()

			if self.singular_file_type == self.Social_Networks.language_texts["social_network"].lower():
				self.singular_file_type = self.singular_file_type.title()

			self.search_for_friend_file = self.Input.Yes_Or_No(self.language_texts["search_for_friend_{}_file"].format(self.singular_file_type))

			if self.open_social_network_file == True:
				select_text = self.language_texts["select_one_social_network_to_open_its_profile_file"]

				self.Select_Social_Network(social_networks = self.social_networks_with_friends, select_social_network = True, select_text = select_text)

		self.selected_friend = False
		self.exact_match = False
		self.found_friend_file = False
		self.search_failed = False

		if self.run_as_module == False:
			if self.search_for_friend_file == True:
				self.Search_Friend_File()

			if self.search_for_friend_file == False:
				self.Select_Friend()
				self.selected_friend = True
				self.found_friend_file = True

			self.Define_Friend_File()

			self.Open_Friend_File()

			if self.found_friend_file == False:
				self.Select_Social_Network(social_networks = self.social_networks_with_friends, second_space = False)

				self.Select_Friend()

				self.selected_friend = True
				self.found_friend_file = True

				self.Define_Friend_File()
				self.Open_Friend_File()

	def Select_File_Type(self):
		self.open_social_network_file = False

		show_text = self.language_texts["file_types"]
		select_text = self.language_texts["select_one_file_type"]

		self.option_info = self.Input.Select(self.file_names["en"], language_options = self.file_names["language"], show_text = show_text, select_text = select_text)

		self.file_type = self.option_info["option"]
		self.language_file_type = self.file_names["language"][self.option_info["number"]].lower()
		self.singular_file_type = self.file_names["language_singular"][self.option_info["number"]]

		if self.file_type == self.JSON.Language.texts["information, title()"]["en"]:
			self.singular_file_type = self.singular_file_type.lower()

		if self.file_type == self.Social_Networks.texts["social_networks"]["en"]:
			self.open_social_network_file = True

		self.file_type_dict = {
			"file_type": self.file_type,
			"language_file_type": self.language_file_type,
			"singular_file_type": self.singular_file_type,
		}

	def Search_Friend_File(self):
		self.options = self.texts["information_items, type: list"]["en"]
		self.language_options = self.texts["information_items, type: list"][self.user_language]

		if self.open_social_network_file == True:
			self.options = self.social_network["data"]["Information items"]["en"]
			self.language_options = self.social_network["data"]["Information items"][self.user_language]
			self.gender_letters = self.Social_Networks.gender_letters

		first_space = False

		if self.open_social_network_file == True:
			first_space = True

		show_text = self.language_texts["information_items"]
		self.select_text = self.language_texts["select_the_information"]

		self.option_info = self.Input.Select(self.options, language_options = self.language_options, show_text = show_text, select_text = self.select_text)

		self.attribute_name = self.option_info["option"]
		self.language_attribute_name = self.option_info["language_option"].lower()

		if self.attribute_name in self.exact_match_information_items:
			self.exact_match = True

		self.the_text = self.gender_letters["the"][self.attribute_name]
		self.this_text = self.gender_letters["this"][self.attribute_name]
		self.part_of_text = self.gender_letters["part_of"][self.attribute_name]

		type_text = self.language_texts["type_{}"].format(self.the_text + " " + self.language_attribute_name)

		self.information_to_use = self.Input.Type(type_text)

		self.found_friend_files = []
		self.found_friend_names = []

		i = 0
		for friend in self.friends:
			self.friend_file = self.friend_files[friend][self.file_type]
			self.friend_information = self.friend_data[friend][self.file_type]

			if self.open_social_network_file == True and self.social_network["Name"] in self.friend_information["Data"]:
				self.friend_file = self.friend_files[friend][self.Social_Networks.texts["social_network"]["en"]][self.social_network["Name"]]["Text profile"]
				self.friend_information = self.friend_information["Data"][self.social_network["Name"]]

			search = []

			if self.exact_match == True:
				search = re.findall(r"\b" + self.information_to_use + r"\b", self.friend_information[self.attribute_name], re.IGNORECASE)

			if self.exact_match == False:
				if self.attribute_name in self.friend_information and self.information_to_use in self.friend_information[self.attribute_name]:
					search.append(self.information_to_use)

			if search != []:
				self.found_friend_files.append(self.friend_file)
				self.found_friend_names.append(friend)

				self.found_friend_file = True

				self.friend_number = i

			if search == []:
				self.search_failed = True

			i += 1

		if self.found_friend_file == True:
			self.friend = self.found_friend_names[0]
			self.friend_file = self.found_friend_files[0]

			if len(self.found_friend_files) >= 2:
				self.choice_text = self.language_texts["select_a_friend_from_the_list_of_found_friends"]

				self.Select_Friend(self.choice_text, self.found_friend_names)

	def Define_Friend_File(self):
		if self.open_social_network_file == False:
			if self.search_for_friend_file == True and self.found_friend_file == True:
				if self.found_friend_files == []:
					self.friend_file = self.friend_files[self.friend]["Information"]

					self.found_friend_file = True

				if self.found_friend_files != []:
					self.friend_file = self.found_friend_files[0]

					self.found_friend_file = True

			if self.search_for_friend_file == False:
				self.friend_file = self.friend_files[self.friend]["Information"]

				self.found_friend_file = True

		if self.open_social_network_file == True and self.selected_friend == True:
			if self.search_for_friend_file == True or self.search_for_friend_file == False:
				self.friend_file = self.friend_files[self.friend][self.Social_Networks.texts["social_network"]["en"]][self.social_network["Name"]]["Text profile"]

				self.found_friend_file = True

	def Open_Friend_File(self):
		if self.open_social_network_file == True and self.search_for_friend_file == True:
			self.language_attribute_name = self.language_attribute_name + " " + self.language_texts["of_the_social_network"] + ' "' + self.social_network["Name"] + '"'

		show_text = self.language_texts["opening_this_{}_friend_file"].format(self.singular_file_type) + ":\n"

		if self.found_friend_file == True and self.selected_friend == True:
			show_text += self.friend_file

		if self.search_for_friend_file == True and self.selected_friend == False:
			if self.found_friend_file == True:
				found_in_friend_file_template = self.language_texts["found_{}"] + "{}:\n" + "{}" + "\n\n" + self.language_texts["on_the_friend_{}_file_below"] + ":\n" + "{}"

				show_text = found_in_friend_file_template.format(self.part_of_text, " " + self.language_attribute_name, self.information_to_use, self.singular_file_type, self.friend_file)

			if self.found_friend_file == False:
				cannot_find_in_friend_files_template = self.language_texts["could_not_find_{}_in_friend_{}_files"] + ":\n" + "{}" + "\n\n" + self.language_texts["executing_the_method_to_select_a_friend_{}_file"] + "..."

				show_text = cannot_find_in_friend_files_template.format(self.this_text + " " + self.language_attribute_name, self.singular_file_type, self.information_to_use, self.singular_file_type)

		print()
		print(show_text)

		if self.found_friend_file == True:
			self.File.Open(self.friend_file)
# Open_Social_Network.py

from Social_Networks.Social_Networks import Social_Networks as Social_Networks

from Block_Websites.Unblock import Unblock as Unblock

class Open_Social_Network(Social_Networks):
	def __init__(self, open_social_networks = False, option_info = None, social_network_parameter = None, custom_link = None, unblock = True, first_space = True, second_space = True):
		super().__init__()

		self.open_social_networks = open_social_networks
		self.option_info = option_info
		self.custom_link = custom_link
		self.first_space = first_space
		self.second_space = second_space

		social_networks = self.social_networks

		if self.open_social_networks == False:
			social_networks = [""]

		self.social_networks_list = False

		if first_space == True:
			print()

		self.social_network_list = []

		if type(social_network_parameter) == str:
			self.social_network_list = [social_network_parameter]

		if type(social_network_parameter) == list:
			self.social_network_list = social_network_parameter

		self.custom_link_backup = self.custom_link

		for social_network in social_networks:
			if self.open_social_networks == False and social_network_parameter == None:
				self.social_network_list = [None]

			i = 0
			for social_network in self.social_network_list:
				if len(self.social_network_list) > 1:
					self.custom_link = self.custom_link_backup[i]

				if i == 1:
					print()

				self.social_network_link = self.custom_link

				self.Define_Social_Network(social_network)

				self.link_type = None
				self.link_type_key = None
				self.language_link_type = "link"

				if len(self.social_network_list) == 1:
					self.Define_Link_Type()
					self.Define_Social_Network_Link()

					if self.open_social_networks == True:
						print()

				if i == 0 and unblock == True:
					self.Unlock_Social_Network()

				self.Open_Social_Network()

				i += 1

		if social_network_parameter != None and self.second_space == True:
			print()

	def Define_Social_Network(self, social_network):
		select_text = self.language_texts["select_one_social_network_to_open"]

		self.social_network = self.Select_Social_Network(social_network = social_network, select_text = select_text)

		if social_network == None:
			self.social_network_list = [self.social_network["Name"]]

	def Unlock_Social_Network(self):
		Unblock(websites = self.social_network_list)

	def Define_Link_Type(self):
		if self.option_info != None:
			option_info = {
				"option": self.texts[self.option_info["type"] + ", title()"]["en"],
				"language_option": self.language_texts[self.option_info["type"] + ", title()"],
			}

		show_text = self.language_texts["link_types"]
		select_text = self.language_texts["select_one_link_type_to_open"]

		if self.open_social_networks == False and self.option_info == None and self.custom_link == None:
			option_info = self.Input.Select(self.link_types["en"], language_options = self.link_types[self.user_language], show_text = show_text, select_text = select_text)

		if self.custom_link != None:
			option_info = {"option": "", "language_option": ""}

		self.link_type = option_info["option"]

		if self.custom_link == None:
			self.language_link_type = option_info["language_option"]

		self.link_type_key = ""

		if self.custom_link == None:
			self.link_type_key = self.link_types_map[self.link_type]

	def Define_Social_Network_Link(self):
		if self.custom_link == None:
			if self.link_type_key in self.social_network["data"]["Information"]:
				self.social_network_link = self.social_network["data"]["Information"][self.link_type_key]

			if self.link_type == self.texts["profile, title()"]["en"] and self.link_type_key in self.social_network["data"]["Information"]:
				self.user_information = {}

				self.social_network_link = self.social_network["data"]["Profile"][self.link_type_key]

				added_user_information = False

				for user_name_item in self.user_name_items:
					language_user_name_item = self.user_name_items[user_name_item]

					if user_name_item in self.user_information and added_user_information == False:
						self.language_link_type += ' "' + self.user_information[language_user_name_item] + '"'

						added_user_information = True

					if language_user_name_item in list(self.user_information.keys()) and added_user_information == False:
						self.language_link_type += ' "' + self.user_information[language_user_name_item] + '"'

						added_user_information = True

		if "Program file" in self.social_network["data"]["Information"]:
			self.social_network_link = self.social_network["data"]["Information"]["Program file"]
			self.language_texts["opening_{}_on_its_{}_page_with_this_link"] = self.language_texts["opening_{}_on_its_{}_page_with_this_link"].split(" {}")[0] + " {}"

	def Open_Social_Network(self):
		print(self.language_texts["opening_{}_on_its_{}_page_with_this_link"].format(self.social_network["Name"], self.language_link_type.lower()) + ":")
		print("\t" + self.social_network_link)

		if self.link_type == self.texts["profile, title()"]["en"] and self.link_type_key in self.social_network["data"]["Information"]:
			for key in self.user_information:
				print()
				print("\t" + key + ":")
				print("\t\t" + self.user_information[key])

		if self.switches["testing"] == False:
			self.File.Open(self.social_network_link)
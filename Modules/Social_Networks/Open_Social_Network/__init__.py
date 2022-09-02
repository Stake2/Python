# Open_Social_Network.py

from Script_Helper import *

from Social_Networks.Social_Networks import Social_Networks as Social_Networks

class Open_Social_Network(Social_Networks):
	def __init__(self, open_social_networks = False, link_type = None):
		super().__init__()

		self.open_social_networks = open_social_networks
		self.link_type = link_type

		if self.open_social_networks == False:
			self.social_network = None

			self.Define_Social_Network()
			self.Define_Link_Type()
			self.Define_Social_Network_Link()
			self.Open_Social_Network()

		if self.open_social_networks == True:
			for self.social_network in self.social_networks:
				self.Define_Social_Network()
				self.Define_Link_Type()
				self.Define_Social_Network_Link()

				print()

				self.Open_Social_Network()

	def Define_Social_Network(self):
		self.choice_text = Language_Item_Definer("Select one {} to open", "Selecione uma {} para abrir").format(self.language_social_network_text)

		self.social_network_dictionary = self.Select_Social_Network(social_network = self.social_network, choice_text = self.choice_text)

		if self.social_network_dictionary != None and self.social_network_dictionary != {}:
			self.social_network = self.social_network_dictionary["social_network"]
			self.social_network_info = self.social_network_dictionary["social_network_info"]
			self.social_network_information = self.social_network_info["Data"]["Information"]

	def Define_Link_Type(self):
		self.choice_list = self.social_network_link_types
		self.language_choice_list = Language_Item_Definer(self.social_network_link_types, self.portuguese_social_network_link_types)

		self.choice_text = Language_Item_Definer("Select one link type to open", "Selecione um tipo de link para abrir")

		if self.open_social_networks == False:
			self.choice_info = Select_Choice_From_List(self.language_choice_list, alternative_choice_text = self.choice_text, second_choices_list = self.choice_list, return_second_item_parameter = True, add_none = True, return_number = True)

		if self.open_social_networks == True:
			self.choice_info = [self.link_type]

		self.link_type = self.choice_info[0]
		self.language_link_type = self.social_network_link_types[self.link_type]

		self.link_type_key = self.link_types_map[self.link_type]

	def Define_Social_Network_Link(self):
		self.social_network_link = None

		if self.link_type_key in self.social_network_information:
			self.social_network_link = self.social_network_information[self.link_type_key]

		if self.link_type == "Profile" and self.link_type_key in self.social_network_information:
			self.social_network_profile = self.social_network_info["Data"][self.link_type]

			self.user_information = {}

			for user_information_item in self.user_information_items:
				language_user_information_item = self.user_information_items[user_information_item]

				if user_information_item in self.social_network_profile:
					self.user_information[Language_Item_Definer(user_information_item, language_user_information_item)] = self.social_network_profile[user_information_item]

			self.information_item_to_use = self.social_network_information[self.link_type_key].split("{")[1].split("}")[0]

			self.social_network_link = self.social_network_link.replace("{" + self.information_item_to_use + "}", "")

			self.social_network_link += self.social_network_profile[self.information_item_to_use]

			added_user_information = False

			for user_name_item in self.user_name_items:
				language_user_name_item = self.user_name_items[user_name_item]

				if user_name_item in self.user_information and added_user_information == False:
					self.language_link_type += ' "' + self.user_information[language_user_name_item] + '"'

					added_user_information = True

				if language_user_name_item in self.user_information and added_user_information == False:
					self.language_link_type += ' "' + self.user_information[language_user_name_item] + '"'

					added_user_information = True

		if "Program file" in self.social_network_information:
			self.social_network_link = self.social_network_information["Program file"]
			self.opening_social_network_template = self.opening_social_network_template.replace(" " + Language_Item_Definer("on its {} page, with this link", "em sua página de {}, com este link"), "")

	def Open_Social_Network(self):
		print(self.opening_social_network_template.format(self.social_network, self.language_link_type) + ":")
		print("\t" + self.social_network_link)

		if self.link_type == "Profile" and self.link_type_key in self.social_network_information:
			for key in self.user_information:
				print()
				print("\t\t" + key + ":")
				print("\t\t\t" + self.user_information[key])

		if self.global_switches["testing_script"] == False:
			Open_Link(self.social_network_link)
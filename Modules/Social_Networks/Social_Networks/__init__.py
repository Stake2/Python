# Social_Networks.py

from Script_Helper import *

class Social_Networks(object):
	def __init__(self, parameter_switches = None):
		# Verbose variable
		self.verbose = False

		self.testing_script = False

		self.parameter_switches = parameter_switches

		self.Define_Basic_Variables()

		self.Define_Texts()
		self.Define_Folders_And_Files()
		self.Define_Lists_And_Dictionaries()

	def Define_Basic_Variables(self):
		self.option = True

		# Global Switches dictionary
		self.global_switches = {
			"write_to_file": self.option,
			"create_files": self.option,
			"create_folders": self.option,
			"move_files": self.option,
			"verbose": self.verbose,
			"testing_script": self.testing_script,
		}

		if self.parameter_switches != None:
			self.global_switches = self.parameter_switches
			self.testing_script = self.global_switches["testing_script"]

		#if self.global_switches["testing_script"] == True:
		#	print(Language_Item_Definer("Testing script: Yes", "Testando script: Sim"))

		if self.global_switches["verbose"] == True:
			print(Language_Item_Definer("Verbose on", "Verbose ligado") + ".")

		if self.global_switches["testing_script"] == True:
			self.global_switches["write_to_file"] = False
			self.global_switches["create_files"] = False
			self.global_switches["move_files"] = False

		self.dot_text = ".txt"
		self.dash_separator = " - "
		self.comma_separator = ", "

	def Define_Texts(self):
		self.english_social_network_text = "Social Network"
		self.portuguese_social_network_text = "Rede Social"

		self.english_social_networks_text = self.english_social_network_text + "s"
		self.portuguese_social_networks_text = self.portuguese_social_network_text.replace("de", "des").replace("al", "ais")

		self.language_social_network_text = Language_Item_Definer(self.english_social_network_text, self.portuguese_social_network_text)
		self.language_social_networks_text = Language_Item_Definer(self.english_social_networks_text, self.portuguese_social_networks_text)

		self.mixed_social_network_text = self.english_social_network_text + self.dash_separator + self.portuguese_social_network_text
		self.mixed_social_networks_text = self.english_social_networks_text + self.dash_separator + self.portuguese_social_networks_text

		self.english_number_text = "Number"
		self.portuguese_number_text = "Número"

		self.english_numbers_text = self.english_number_text + "s"
		self.portuguese_numbers_text = self.portuguese_number_text + "s"

		self.number_text = Language_Item_Definer(self.english_number_text, self.portuguese_number_text)

		self.mixed_number_text = self.english_number_text + self.dash_separator + self.portuguese_number_text
		self.mixed_numbers_text = self.english_numbers_text + self.dash_separator + self.portuguese_numbers_text

		self.english_information_text = "Information"
		self.portuguese_information_text = "Informação"

		self.mixed_information_text = self.english_information_text + self.dash_separator + self.portuguese_information_text

		self.opening_social_network_template = Language_Item_Definer("Opening {} on its {} page, with this link", "Abrindo {} em sua página de {}, com este link")

	def Define_Folders_And_Files(self):
		# Folders
		self.mega_folder = mega_folder
		self.notepad_effort_folder = notepad_folder_effort

		self.mega_image_folder = self.mega_folder + "Image/"

		# Social Networks Folders
		self.social_networks_text_folder = self.notepad_effort_folder + self.english_social_networks_text + "/"
		Create_Folder(self.social_networks_text_folder, self.global_switches)

		self.social_networks_image_folder = self.mega_image_folder + self.english_social_networks_text + "/"
		Create_Folder(self.social_networks_image_folder, self.global_switches)

		self.digital_identities_folder = self.social_networks_image_folder + "Digital Identities/"
		Create_Folder(self.digital_identities_folder, self.global_switches)

		# Social Networks Files
		self.social_networks_file = self.social_networks_text_folder + self.english_social_networks_text + self.dot_text
		Create_Text_File(self.social_networks_file, self.global_switches)

	def Define_Lists_And_Dictionaries(self):
		# Lists
		self.social_networks = Create_Array_Of_File(self.social_networks_file)

		self.list_file_names = [
			"Information Items",
			"Portuguese Information Items",
			"Image Folders",
		]

		self.dictionary_file_names = [
			self.english_information_text,
			"Profile",
			"Settings",
		]

		# Dictionaries
		self.social_network_folders = {}
		self.social_network_files = {}
		self.social_network_data = {}

		self.social_networks_data = {}
		self.social_networks_data["Profile links"] = []
		self.social_networks_data["Language Information Items"] = {}

		self.social_network_links = {}

		for social_network in self.social_networks:
			# Text Folder
			text_folder = self.social_networks_text_folder + social_network + "/"
			Create_Folder(text_folder, self.global_switches)

			# Database Folder
			database_folder = self.social_networks_text_folder + social_network + "/"
			Create_Folder(database_folder, self.global_switches)

			# Image Folder
			image_folder = self.social_networks_image_folder + social_network + "/"
			Create_Folder(image_folder, self.global_switches)

			self.social_network_folders[social_network] = {}
			self.social_network_files[social_network] = {}
			self.social_network_data[social_network] = {}

			self.social_network_folders[social_network]["Text"] = text_folder
			self.social_network_folders[social_network]["Database"] = database_folder
			self.social_network_folders[social_network]["Image"] = image_folder

			settings = {}

			settings["Has Image Folders"] = True

			if is_a_file(database_folder + "Settings" + self.dot_text) == True:
				settings = Make_Setting_Dictionary(database_folder + "Settings" + self.dot_text, read_file = True, next_line_value = True)

				if "Has Image Folders" in settings and settings["Has Image Folders"] == False:
					settings["Has Image Folders"] = False

			# Database Files
			for file_name in self.list_file_names + self.dictionary_file_names:
				if file_name != "Settings":
					self.social_network_files[social_network][file_name] = database_folder + file_name + self.dot_text
					Create_Text_File(self.social_network_files[social_network][file_name], self.global_switches)

				if file_name == "Settings":
					if is_a_file(database_folder + file_name + self.dot_text) == True:
						self.social_network_files[social_network][file_name] = database_folder + file_name + self.dot_text

				if social_network in self.social_network_files and file_name in self.social_network_files[social_network] and is_a_file(self.social_network_files[social_network][file_name]) == True:
					if file_name in self.dictionary_file_names:
						self.social_network_data[social_network][file_name] = Make_Setting_Dictionary(self.social_network_files[social_network][file_name], read_file = True, define_yes_or_no = True, next_line_value = True)

					if file_name in self.list_file_names:
						self.social_network_data[social_network][file_name] = Create_Array_Of_File(self.social_network_files[social_network][file_name])

			if self.global_switches["verbose"] == True:
				print()
				print(self.social_network_data["Information"][social_network])

			# Social Networks Data
			list_ = ["Link", "Profile link", "Message link"]

			self.social_network_links[social_network] = {}

			for item in list_:
				self.social_network_links[social_network][item.split(" ")[0]] = "None"

				if item in self.social_network_data[social_network]["Information"]:
					link = self.social_network_data[social_network]["Information"][item]

					self.social_network_links[social_network][item.split(" ")[0]] = link

			if "Profile link" in self.social_network_data[social_network]["Profile"]:
				self.social_networks_data["Profile links"].append(self.social_network_data["Information"][social_network]["Profile link"])

		self.information_items_translated_to_portuguese = {}

		for social_network in self.social_networks:
			self.social_networks_data["Language Information Items"][social_network] = {}

			if self.global_switches["verbose"] == True:
				print()
				print(social_network + ":")

			i = 0
			for information_item in self.social_network_data[social_network]["Information Items"]:
				if information_item not in self.information_items_translated_to_portuguese:
					self.information_items_translated_to_portuguese[information_item] = self.social_network_data[social_network]["Portuguese Information Items"][i]

				if information_item not in self.social_networks_data["Language Information Items"]:
					self.social_networks_data["Language Information Items"][social_network][information_item] = self.information_items_translated_to_portuguese[information_item]

				if self.global_switches["verbose"] == True:
					print("\t" + information_item + ", " + self.social_network_data[social_network]["Portuguese Information Items"][i])

				i += 1

		self.information_item_gender_letters = {}
		self.information_item_gender_letters["the"] = {}
		self.information_item_gender_letters["this"] = {}

		self.language_friends_information_headers = []

		self.user_information_items = {}
		self.user_name_items = {}

		for information_item in self.information_items_translated_to_portuguese:
			language_information_item = self.information_items_translated_to_portuguese[information_item]

			self.language_friends_information_headers.append(Language_Item_Definer(information_item, language_information_item))

			self.information_item_gender_letters["the"][information_item] = Language_Item_Definer("the", "o")
			self.information_item_gender_letters["this"][information_item] = Language_Item_Definer("this", "este")

			self.user_information_items[information_item] = language_information_item

			if information_item in ["Nick and Tag", "Username", "Handle", "Contact name"]:
				self.user_name_items[information_item] = language_information_item

		self.social_network_link_types = {
			"Home": "Início",
			"Profile": "Perfil",
		}

		self.portuguese_social_network_link_types = [
			"Início",
			"Perfil",
		]

		self.link_types_map = {
			"Home": "Link",
			"Profile": "Profile link",
		}

	def Select_Social_Network(self, social_network = None, select_social_network = True, social_networks = None, choice_text = None, first_space = False, second_space = False):
		self.choice_text = choice_text

		if self.choice_text == None:
			self.choice_text = Language_Item_Definer("Select one Social Network to use", "Selecione uma Rede Social para usar")

		if social_networks != None:
			self.social_networks = social_networks

		if select_social_network == True:
			if social_network == None:
				self.social_network = Select_Choice_From_List(self.social_networks, alternative_choice_text = self.choice_text, second_choices_list = self.social_networks, return_second_item_parameter = True, add_none = True, return_number = True, first_space = first_space, second_space = second_space)[0]

			if social_network != None:
				self.social_network = social_network

			return self.Define_Social_Network_Variables(self.social_network)

		else:
			return {}

	def Define_Social_Network_Variables(self, social_network):
		self.social_network = social_network

		self.social_network_info = {}

		self.social_network_info["Folder"] = {}
		self.social_network_info["Folder"]["Text"] = self.social_network_folders[self.social_network]["Text"]
		self.social_network_info["Folder"]["Database"] = self.social_network_folders[self.social_network]["Database"]
		self.social_network_info["Folder"]["Image"] = self.social_network_folders[self.social_network]["Image"]

		self.social_network_info["Files"] = {}
		self.social_network_info["Data"] = {}

		for file_name in self.list_file_names + self.dictionary_file_names:
			if social_network in self.social_network_files and file_name in self.social_network_files[social_network]:
				self.social_network_info["Files"][file_name] = self.social_network_files[self.social_network][file_name]

				if is_a_file(self.social_network_info["Files"][file_name]) == True:
					self.social_network_info["Data"][file_name] = self.social_network_data[self.social_network][file_name]

		self.social_network_info["Data"]["Language Information Items"] = list(self.social_networks_data["Language Information Items"][social_network].values())

		return {
			"social_network": self.social_network,
			"social_network_info": self.social_network_info,
		}
# Social_Networks.py

from Script_Helper import *

class Social_Networks(object):
	def __init__(self, parameter_switches = None):
		# Verbose variable
		self.verbose = True

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

		self.mixed_social_network_text = self.english_social_network_text + self.dash_separator + self.portuguese_social_network_text
		self.mixed_social_networks_text = self.english_social_networks_text + self.dash_separator + self.portuguese_social_networks_text

		self.english_friend_text = "Friend"
		self.portuguese_friend_text = "Amigo"

		self.english_friends_text = self.english_friend_text + "s"
		self.portuguese_friends_text = self.portuguese_friend_text + "s"

		self.mixed_friend_text = self.english_friend_text + self.dash_separator + self.portuguese_friend_text
		self.mixed_friends_text = self.english_friends_text + self.dash_separator + self.portuguese_friends_text

		self.english_number_text = "Number"
		self.portuguese_number_text = "Número"

		self.english_numbers_text = self.english_number_text + "s"
		self.portuguese_numbers_text = self.portuguese_number_text + "s"

		self.number_text = Language_Item_Definer(self.english_number_text, self.portuguese_number_text)

		self.mixed_number_text = self.english_number_text + self.dash_separator + self.portuguese_number_text
		self.mixed_numbers_text = self.english_numbers_text + self.dash_separator + self.portuguese_numbers_text

	def Define_Folders_And_Files(self):
		# Folders
		self.mega_folder = mega_folder
		self.notepad_effort_folder = notepad_folder_effort

		self.mega_image_folder = self.mega_folder + "Image/"

		# Friends Folders
		self.friends_text_folder = self.notepad_effort_folder + self.mixed_friends_text + "/"
		Create_Folder(self.friends_text_folder, self.global_switches)

		self.friends_database_folder = self.friends_text_folder + "Database/"
		Create_Folder(self.friends_database_folder, self.global_switches)

		self.friends_information_folder = self.friends_database_folder + "Information/"
		Create_Folder(self.friends_information_folder, self.global_switches)

		self.friends_image_folder = self.mega_image_folder + self.mixed_friends_text + "/"
		Create_Folder(self.friends_image_folder, self.global_switches)

		# Social Networks Folders
		self.social_networks_text_folder = self.notepad_effort_folder + self.english_social_networks_text + "/"
		Create_Folder(self.social_networks_text_folder, self.global_switches)

		self.social_networks_image_folder = self.mega_image_folder + self.english_social_networks_text + "/"
		Create_Folder(self.social_networks_image_folder, self.global_switches)

		self.digital_identities_folder = self.social_networks_image_folder + "Digital Identities/"
		Create_Folder(self.digital_identities_folder, self.global_switches)

		# Files

		# Friends Files
		self.friends_file = self.friends_database_folder + self.mixed_friends_text + self.dot_text
		Create_Text_File(self.friends_file, self.global_switches)

		self.friends_number_file = self.friends_database_folder + self.mixed_number_text + self.dot_text
		Create_Text_File(self.friends_number_file, self.global_switches)

		self.friends_information_headers_file = self.friends_database_folder + "Information Headers" + self.dot_text
		Create_Text_File(self.friends_information_headers_file, self.global_switches)

		# Social Networks Files
		self.social_networks_file = self.social_networks_text_folder + self.english_social_networks_text + self.dot_text
		Create_Text_File(self.social_networks_file, self.global_switches)

	def Define_Lists_And_Dictionaries(self):
		# Lists
		self.social_networks = Create_Array_Of_File(self.social_networks_file)
		self.friends_information_headers = Create_Array_Of_File(self.friends_information_headers_file)

		self.list_file_names = [
			"Parameters",
			"Image Folders",
		]

		self.dictionary_file_names = [
			"Information",
			"Profile",
			"Settings",
		]

		self.friend_file_names = [
			"Information",
			self.english_social_networks_text,
		]

		self.friends = Create_Array_Of_File(self.friends_file)
		self.friends_number = Create_Array_Of_File(self.friends_number_file)

		if self.friends_number != []:
			self.friends_number = self.friends_number[0]

		# Dictionaries
		self.social_network_folders = {}
		self.social_network_folders["Text"] = {}
		self.social_network_folders["Database"] = {}
		self.social_network_folders["Image"] = {}

		self.social_network_files = {}
		self.social_network_data = {}

		for file_name in self.list_file_names + self.dictionary_file_names:
			self.social_network_files[file_name] = {}
			self.social_network_data[file_name] = {}

		self.social_networks_data = {}
		self.social_networks_data["Links"] = []
		self.social_networks_data["Profile links"] = []
		self.social_networks_data["Message links"] = []

		self.social_network_links = {}
		self.social_network_profile_links = {}
		self.social_network_message_links = {}

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

			self.social_network_folders["Text"][social_network] = text_folder
			self.social_network_folders["Database"][social_network] = database_folder
			self.social_network_folders["Image"][social_network] = image_folder

			settings = Make_Setting_Dictionary(database_folder + "Settings" + self.dot_text, read_file = True, next_line_value = True)

			if "Has Image Folders" not in settings:
				settings["Has Image Folders"] = True

			if "Has Image Folders" in settings and settings["Has Image Folders"] == False:
				settings["Has Image Folders"] = False

			# Database Files
			for file_name in self.list_file_names + self.dictionary_file_names:
				self.social_network_files[file_name][social_network] = database_folder + file_name + self.dot_text

				if settings["Has Image Folders"] == True:
					Create_Text_File(self.social_network_files[file_name][social_network], self.global_switches)

				if is_a_file(self.social_network_files[file_name][social_network]) == True:
					if file_name in self.dictionary_file_names:
						self.social_network_data[file_name][social_network] = Make_Setting_Dictionary(self.social_network_files[file_name][social_network], read_file = True, define_yes_or_no = True, next_line_value = True)

					if file_name in self.list_file_names:
						self.social_network_data[file_name][social_network] = Create_Array_Of_File(self.social_network_files[file_name][social_network])

			if self.global_switches["verbose"] == True:
				print()
				print(self.social_network_data["Information"][social_network])

			# Social Networks Data
			list_ = ["Link", "Profile link", "Message link"]

			for item in list_:
				if item in self.social_network_data["Information"][social_network]:
					self.social_networks_data[item + "s"].append(self.social_network_data["Information"][social_network][item])

			if "Profile link" in self.social_network_data["Profile"][social_network]:
				self.social_networks_data["Profile links"].append(self.social_network_data["Information"][social_network]["Profile link"])

		self.friends_data = {}
		self.friends_folders = {}
		self.friends_files = {}

		# Friends Folders, Files, and Data dictionaries filling
		for friend in self.friends:
			self.friends_folders[friend] = {}
			self.friends_files[friend] = {}
			self.friends_data[friend] = {}

			# Friends Folders
			self.friends_folders[friend]["Text"] = {}

			self.friends_folders[friend]["Text"]["Root"] = self.friends_text_folder + friend + "/"
			Create_Folder(self.friends_folders[friend]["Text"]["Root"], self.global_switches)

			self.friends_folders[friend]["Text"][self.english_social_networks_text] = self.friends_folders[friend]["Text"]["Root"] + self.mixed_social_networks_text + "/"
			Create_Folder(self.friends_folders[friend]["Text"][self.english_social_networks_text], self.global_switches)

			self.friends_folders[friend]["Image"] = {}

			self.friends_folders[friend]["Image"]["Root"] = self.friends_image_folder + friend + "/"
			Create_Folder(self.friends_folders[friend]["Image"]["Root"], self.global_switches)

			self.friends_folders[friend]["Image"][self.english_social_networks_text] = self.friends_folders[friend]["Image"]["Root"] + self.mixed_social_networks_text + "/"
			Create_Folder(self.friends_folders[friend]["Image"][self.english_social_networks_text], self.global_switches)

			for file_name in self.friend_file_names:
				key = file_name

				text_folder = self.friends_folders[friend]["Text"]["Root"]

				if file_name == self.english_social_networks_text:
					text_folder = self.friends_folders[friend]["Text"][self.english_social_networks_text]
					Create_Folder(text_folder, self.global_switches)

					file_name = self.mixed_social_networks_text

				# Friends Files
				self.friends_files[friend][key] = text_folder + file_name + self.dot_text
				Create_Text_File(self.friends_files[friend][key], self.global_switches)

				image_folder = self.friends_folders[friend]["Image"][self.english_social_networks_text]
				image_folder_file = self.friends_folders[friend]["Image"]["Root"] + file_name + self.dot_text

				if key == self.english_social_networks_text:
					image_folder = self.friends_folders[friend]["Image"][self.english_social_networks_text]
					image_folder_file = image_folder + self.mixed_social_networks_text + self.dot_text

				if Read_String(self.friends_files[friend][key]) != Read_String(image_folder_file):
					Copy_File(self.friends_files[friend][key], image_folder_file, self.global_switches)

				# Friends Data
				if key == self.english_social_networks_text:
					self.friends_data[friend][key] = Create_Array_Of_File(self.friends_files[friend][key])

				if key != self.english_social_networks_text:
					self.friends_data[friend][key] = Make_Setting_Dictionary(self.friends_files[friend][key], read_file = True, define_yes_or_no = True, next_line_value = True)

			# Social Network folders and profile file creation
			for social_network in self.friends_data[friend][self.english_social_networks_text]:
				# Text Folder
				text_folder = self.friends_folders[friend]["Text"][self.english_social_networks_text] + social_network + "/"
				Create_Folder(text_folder, self.global_switches)

				# Image Folder
				image_folder = self.friends_folders[friend]["Image"][self.english_social_networks_text] + social_network + "/"
				Create_Folder(image_folder, self.global_switches)

				image_profile_file = image_folder + "Profile" + self.dot_text

				profile_file = text_folder + "Profile" + self.dot_text
				Create_Text_File(profile_file, self.global_switches)

				if Read_String(profile_file) != Read_String(image_profile_file):
					Copy_File(profile_file, image_profile_file, self.global_switches)

				profile = Make_Setting_Dictionary(profile_file, read_file = True, next_line_value = True)

				if self.global_switches["verbose"] == False and profile != {}:
					Dict_Print(profile = profile, second_space = True)

			if self.global_switches["verbose"] == False:
				Dict_Print(friends_data = self.friends_data[friend])

		for header in self.friends_information_headers:
			information_file = self.friends_information_folder + header + self.dot_text
			Create_Text_File(information_file, self.global_switches)

			if Create_Array_Of_File(information_file) == []:
				information_list = []

				for friend in self.friends:
					information = "Not filled - Não preenchido"

					if header in self.friends_data[friend]["Information"]:
						information = self.friends_data[friend]["Information"][header]

					information_list.append(information)

				text_to_write = Stringfy_Array(information_list, add_line_break = True)

				if text_to_write != Read_String(information_file):
					Write_To_File(information_file, text_to_write, self.global_switches)
# Fill_Experienced_Media_Files.py

from Script_Helper import *

from Year_Summary_Manager.Year_Summary_Manager import Year_Summary_Manager as Year_Summary_Manager

class Fill_Experienced_Media_Files(Year_Summary_Manager):
	def __init__(self, language_year_folders):
		super().__init__(select_year = False)

		self.language_year_folders = language_year_folders

		self.Define_Experienced_Media_Folders()
		self.Select_Experienced_Media_Folder()
		self.Define_Media_Info()

	def Define_Experienced_Media_Folders(self):
		self.experienced_media_folders = {}

		for language in self.language_year_folders:
			self.experienced_media_folders[language] = self.language_year_folders[language] + self.year_folder_texts["Experienced Media"][language] + "/"
			Create_Folder(self.experienced_media_folders[language], self.global_switches["create_folders"])

		self.experienced_media_sub_folders = {}

		for language in self.language_year_folders:
			folder_names = self.experienced_media_sub_folder_names[language]
			self.experienced_media_sub_folders[language] = {}

			i = 0
			while i <= len(folder_names) - 1:
				folder_name = folder_names[i]

				folder = self.experienced_media_folders[language] + folder_name + "/"
				Create_Folder(folder, self.global_switches["create_folders"])

				self.experienced_media_sub_folders[language][folder_name] = folder

				i += 1

		self.experienced_media_database_folder = self.experienced_media_folders[full_language_en] + "Database/"
		self.experienced_media_database_folders = {}

		Create_Folder(self.experienced_media_database_folder, self.global_switches["create_folders"])

		language = "English"
		folders = self.experienced_media_sub_folders[language]
		folder_names = self.experienced_media_sub_folder_names[language]
		self.experienced_media_database_folders[language] = {}
		database_folder = self.experienced_media_folders[language] + "Database/"
		Create_Folder(database_folder, self.global_switches["create_folders"])

		i = 0
		while i <= len(folder_names) - 1:
			folder_name = folder_names[i]

			folder = database_folder + folder_name + "/"
			Create_Folder(folder, self.global_switches["create_folders"])

			self.experienced_media_database_folders[language][folder_name] = folder

			i += 1

	def Select_Experienced_Media_Folder(self):
		self.folders = []
		self.folder_names = []
		self.folder_numbers = {}

		self.full_language = Language_Item_Definer(full_language_en, full_language_pt)

		i = 0
		for folder_name in self.experienced_media_sub_folders[self.full_language]:
			folder = self.experienced_media_sub_folders[self.full_language][folder_name]

			if Language_Item_Definer("Music", "Música") in folder_name:
				self.folder_names.append(folder_name)
				self.folders.append(folder)

			self.folder_numbers[folder] = i

			i += 1

		first_list = self.folder_names
		second_list = self.folders
		self.choice_text = Language_Item_Definer("Select one Experienced Media folder to use", "Selecione uma pasta de Mídia Experimentada para usar")
		self.choice_info = Select_Choice_From_List(first_list, local_script_name, self.choice_text, second_choices_list = second_list, return_second_item_parameter = True, add_none = True, return_number = True, first_space = False)

		self.selected_folder = self.choice_info[0]
		self.selected_folder_name = self.experienced_media_sub_folder_names[full_language_en][self.folder_numbers[self.selected_folder]]
		self.database_folder = self.experienced_media_database_folders[full_language_en][self.selected_folder_name]

		self.experienced_media_database_file_names_ = self.experienced_media_database_file_names[self.selected_folder_name]
		self.experienced_media_database_file_names_language_ = self.experienced_media_database_file_names_language[self.selected_folder_name][self.full_language]

		self.experienced_media_number_file = self.database_folder + "Number" + self.dot_text
		Create_Text_File(self.experienced_media_number_file, self.global_switches["create_files"])

		for file_name in self.experienced_media_database_file_names_:
			file = self.database_folder + file_name + self.dot_text
			Create_Text_File(file, self.global_switches["create_files"])

		if self.global_switches["verbose"] == True:
			print(Language_Item_Definer("Folder Name", "Nome da Pasta") + ":")
			print(self.selected_folder_name)
			print()

			print(Language_Item_Definer("Selected Folder", "Pasta Selecionada") + ": ")
			print(self.selected_folder)
			print()

			print(Language_Item_Definer("Database Folder", "Pasta do Banco de Dados") + ": ")
			print(self.database_folder)
			print()

	def Define_Media_Info(self):
		self.parameter_dict = {}
		self.parameter_dict_translated = {}
		self.database_files = {}

		self.media_info_files = List_Files(self.experienced_media_folders[full_language_en] + "Music/", add_none = False)
		self.media_info_filenames = List_Filenames(self.experienced_media_folders[full_language_en] + "Music/", add_none = False)

		self.media_info_files.remove("C:/Mega/Bloco De Notas/Dedicação/Years/2021/English/Experienced Media/Music/Song Number.txt")
		self.media_info_filenames.remove("Song Number")

		array = []
		for file_number in [int(x.split(". ")[0]) for x in self.media_info_filenames]:
			array.append(file_number)

		array = sorted(array)

		self.files = [1, 2]

		print()

		self.parameter_strings = {}

		for file_name in self.experienced_media_database_file_names_:
			self.parameter_strings[file_name] = ""

		self.remote_links_list = [
		"SoundCloud Links",
		"YouTube Links",
		"SoundCloud Playlist Links",
		"YouTube Playlist Links",
		]

		file_number = 1
		for file in self.media_info_files:
			for self.file in self.media_info_files:
				if "/" + str(array[file_number - 1]) + ". " in self.file:
					Open_Text_File(self.file)

			i = 0
			for file_name in self.experienced_media_database_file_names_:
				self.current_media_number = str(i)
				parameter_name = self.experienced_media_database_file_names_[i]
				parameter_name_text = self.experienced_media_database_file_names_language_[i]
				parameter_name_translated = self.experienced_media_database_file_names_language[self.selected_folder_name + " Translated"][self.full_language][parameter_name][i]

				self.database_files[parameter_name] = self.database_folder + parameter_name + self.dot_text

				if parameter_name not in self.remote_links_list:
					parameter_name_text = parameter_name_text.lower()

				if parameter_name not in self.experienced_media_parameters_not_to_ask[self.selected_folder_name]:
					parameter = Select_Choice(Language_Item_Definer("Type the ", "Digite {} ".format(Define_Text_By_Text(parameter_name_text.split(" ")[0], "o", "os"))) + parameter_name_text, first_space = False, second_space = False)

				else:
					parameter = self.parameter_dict[self.experienced_media_parameter_values[self.selected_folder_name][parameter_name]]

				self.parameter_dict[parameter_name] = parameter
				self.parameter_dict_translated[parameter_name_translated] = parameter

				if parameter_name == "SoundCloud Playlist Links":
					self.parameter_dict[parameter_name] = "{}?in=stake2/sets/dubstep-2021".format(self.parameter_dict["SoundCloud Links"])

				if parameter_name == "YouTube Playlist Links":
					self.parameter_dict[parameter_name] = "{}&list=PLh4DEvPQ2wKM2Jqz95-o6u6pRtLyfdVp9&index=".format(self.parameter_dict["YouTube Links"]) + str(file_number)

				if parameter_name == "Channel":
					local_parameter = parameter.replace("\r\n", "\n")
					split = local_parameter.splitlines()
					split[0] = split[0] + ": "

					s = 0
					for thing in split:
						if len(split) > 1 and thing != split[0] and thing != split[-1]:
							split[s] = split[s] + ", "

						s += 1

					self.parameter_dict[parameter_name] = Stringfy_Array(split)

				if self.parameter_strings[file_name] == "":
					self.parameter_strings[file_name] += self.parameter_dict[parameter_name]

				else:
					self.parameter_strings[file_name] += "\n" + self.parameter_dict[parameter_name]

				text_to_append = self.parameter_dict[parameter_name]
				Append_To_File(self.database_files[parameter_name], text_to_append, True, check_file_length = True)

				i += 1

			file_number += 1
			print()

		i = 0
		for file_name in self.experienced_media_database_file_names_:
			file = self.database_files[file_name]
			parameter = self.parameter_dict[file_name]

			text_to_write = self.parameter_strings[file_name]

			print()
			print([text_to_write])
			print(file)

			if text_to_write != Read_String(file):
				Write_To_File(file, text_to_write, self.global_switches)

			i += 1
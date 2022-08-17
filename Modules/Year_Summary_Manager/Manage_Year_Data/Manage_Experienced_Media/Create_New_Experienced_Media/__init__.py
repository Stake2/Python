# Create_New_Experienced_Media.py

from Script_Helper import *

from Year_Summary_Manager.Year_Summary_Manager import Year_Summary_Manager as Year_Summary_Manager

import re

class Create_New_Experienced_Media(Year_Summary_Manager):
	def __init__(self, variables_dict):
		super().__init__(select_year = False)

		self.variables_dict = variables_dict
		self.language_year_folders = self.variables_dict["language_year_folders"]
		self.experienced_media_sub_folders = self.variables_dict["experienced_media_sub_folders"]
		self.full_language = self.variables_dict["full_language"]
		self.experienced_media_database_folders = self.variables_dict["experienced_media_database_folders"]

		self.Select_Experienced_Media_Folder()
		self.Ask_For_Media_Info()
		self.Define_Media_Variables()
		self.Write_To_Files()

		print("\n---\n")
		print(self.texts_to_write[self.full_language])

		print()
		input(Language_Item_Definer("Press Enter when you finish reading the Info Summary", "Pressione Enter quando terminar de ler o Resumo de Informações") + ": ")
		print()
		print("---")

	def Select_Experienced_Media_Folder(self):
		self.folders = []
		self.folder_names = []
		self.folder_numbers = {}

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

		if is_a_file(self.experienced_media_number_file) == False:
			Write_To_File(self.experienced_media_number_file, "0", self.global_switches)

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

	def Ask_For_Media_Info(self):
		self.parameter_dict = {}
		self.parameter_dict_translated = {}
		self.database_files = {}

		self.remote_links_list = [
		"SoundCloud Links",
		"YouTube Links",
		"SoundCloud Playlist Links",
		"YouTube Playlist Links",
		]

		i = 0
		for file_name in self.experienced_media_database_file_names_:
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

			i += 1

	def Define_Media_Variables(self):
		self.current_media_number = str(int(Create_Array_Of_File(self.experienced_media_number_file)[0]) + 1)

		name = Remove_Non_File_Characters(self.parameter_dict["Name"])

		if "." in name:
			name = name.replace(".", "")

		self.file_name = self.current_media_number + ". " + name + self.dot_text

		self.files = {}

		for language in self.language_year_folders:
			folder_name = self.experienced_media_sub_folder_names[language][self.folder_numbers[self.selected_folder]]

			self.files[language] = self.experienced_media_sub_folders[language][folder_name] + self.file_name

		for file in self.files.values():
			Create_Text_File(file, self.global_switches["create_files"])

		if self.global_switches["verbose"] == True:
			print()
			print(Language_Item_Definer("Parameter Dict", "Dicionário de Parâmetros") + ":")
			Dict_Print(self.parameter_dict)
			print()

			print(Language_Item_Definer("Files", "Arquivos") + ":")
			Dict_Print(self.files)
			print()

			print(Language_Item_Definer("Database Files", "Arquivos do Banco de Dados") + ":")
			Dict_Print(self.database_files)

	def Write_To_Files(self):
		texts_to_replace = [
		"» Follow ",
		"● Follow ",
		"→ ",
		"Follow ",
		"\nFollow ",
		"» Connect with ",
		"\r\n---\r\n",
		"---",
		" 🎧",
		" 🎤",
		" 💿",
		" ►",
		"▼ ",
		" 📢",
		"\u200b\u200b",
		]

		string = ""

		i = 0
		for line in self.parameter_dict["Artist"].splitlines():
			c = 0
			while c <= len(texts_to_replace) - 1:
				line = line.replace(texts_to_replace[c], "")

				c += 1

			string += line

			if line != self.parameter_dict["Artist"].splitlines()[-1]:
				string += "\n"

			i += 1

		self.parameter_dict["Artist"] = string

		self.has_remix_artist = False

		if "(VIP)" not in self.parameter_dict["Name"] and "(vip)" not in self.parameter_dict["Name"]:
			try:
				self.remix_artist_name = "(" + re.split("[(]", self.parameter_dict["Name"])[1]

				if "ft. " in self.remix_artist_name or "FT. " in self.remix_artist_name or "Feat" in self.remix_artist_name:
					self.remix_artist_name = self.remix_artist_name.replace("ft. ", "").replace("FT. ", "").replace("Feat ", "")

				self.has_remix_artist = True

			except IndexError:
				self.has_remix_artist = False	

		if self.has_remix_artist == True:
			self.remix_artist_name = self.remix_artist_name.replace("(", "")
			self.remix_artist_name = self.remix_artist_name.replace(")", "")
			self.remix_artist_name = self.remix_artist_name.replace(" Remix", "")
			self.remix_artist_name = "\n" + self.remix_artist_name + "\n"

		else:
			self.remix_artist_name = ""

		self.artist_name = self.parameter_dict["Name"].split(" - ")[0]

		array = self.parameter_dict["Artist"].splitlines()
		array.insert(0, self.artist_name + "\n" + self.remix_artist_name)
		self.parameter_dict["Artist"] = Stringfy_Array(array, add_line_break = True)

		if "Feat. " in self.parameter_dict["Artist"]:
			self.parameter_dict["Artist"] = self.parameter_dict["Artist"].replace("Feat. ", "")

		i = 0
		for file in self.database_files:
			file_name = file
			file = self.database_files[file_name]
			parameter = self.parameter_dict[file_name]
			text_to_format = self.experienced_media_format_texts[self.selected_folder_name][i]

			text_to_append = parameter

			if file_name == "Artist":
				text_to_append = self.artist_name

				if self.has_remix_artist == True:
					text_to_append += ", " + self.remix_artist_name.replace("\n", "")

				print(text_to_append)

			if file_name == "SoundCloud Playlist Links":
				text_to_append = "{}?in=stake2/sets/dubstep-{}".format(self.parameter_dict["SoundCloud Links"], current_year)

			if file_name == "YouTube Playlist Links":
				text_to_append = "{}&list=PLh4DEvPQ2wKMoex4j0pFrM6gl77VePMCD&index=".format(self.parameter_dict["YouTube Links"]) + str(self.current_media_number)

			if text_to_append not in Create_Array_Of_File(file):
				Append_To_File(file, text_to_append, self.global_switches, check_file_length = True)

			i += 1

		for file in self.files.values():
			Create_Text_File(file, self.global_switches["create_files"])

		self.texts_to_write = {}

		for language in self.language_year_folders:
			string = ""

			i = 0
			while i <= len(self.experienced_media_format_texts[self.selected_folder_name]) - 1:				
				file_name = list(self.database_files.keys())[i]
				text_to_format = self.experienced_media_format_texts[self.selected_folder_name][i]
				parameter = self.parameter_dict[file_name]

				if file_name == "SoundCloud Playlist Links":
					parameter = self.parameter_dict["SoundCloud Links"]

				if file_name == "YouTube Playlist Links":
					parameter = self.parameter_dict["YouTube Links"]

				text_to_append = text_to_format.format(parameter)

				if file_name == "YouTube Playlist Links":
					text_to_append = text_to_append.replace("index=", "index=" + self.current_media_number)

				string += text_to_append

				i += 1

			self.texts_to_write[language] = string

			i = 0
			while i <= len(self.experienced_media_format_texts[self.selected_folder_name]) - 1:
				file_name = list(self.database_files.keys())[i]

				file = self.files[language]
				Create_Text_File(file)

				text_to_write = self.texts_to_write[language]

				if Read_String(file) != text_to_write:
					Write_To_File(file, text_to_write, self.global_switches)

				i += 1

		text_to_write = str(self.current_media_number)

		if Read_String(self.experienced_media_number_file) != text_to_write:
			Write_To_File(self.experienced_media_number_file, text_to_write, self.global_switches)
# Register_Played_Time.py

from Script_Helper import *

from os.path import expanduser

from GamePlayer.GamePlayer import GamePlayer as GamePlayer

from Diary_Slim.Write_On_Diary_Slim_Module import Write_On_Diary_Slim_Module as Write_On_Diary_Slim_Module

from Block_Websites.Unblock import Unblock as Unblock

class Register_Played_Time(GamePlayer):
	def __init__(self, texts_to_use, variables_dict):
		super().__init__()

		self.texts_to_use = texts_to_use
		self.variables_dict = variables_dict

		self.media_type_files_folder = self.variables_dict["media_type_files_folder"]
		self.game_files_folder = self.variables_dict["game_files_folder"]
		self.media_type_folders_folder = self.variables_dict["media_type_folders_folder"]
		self.game_name = self.variables_dict["game_name"]
		self.game_type = self.variables_dict["game_type"]
		self.game_genre = self.variables_dict["game_genre"]

		self.when_played = self.texts_to_use["Times"]
		self.time_spent = self.texts_to_use["Time Spent"]

		self.functions_to_use = {}

		for text in self.texts_to_use:
			self.functions_to_use[text] = Append_To_File

			if text == "Number":
				self.functions_to_use[text] = Write_To_File

			if text not in ["Game Types", "Played Time English", "Played Time Português Brasileiro"]:
				file = self.media_type_files_folder + text + self.dot_text

				if text != "Number":				
					Create_Text_File(file, self.global_switches["create_files"])

				if text == "Number" and is_a_file(file) == False:
					Write_To_File(file, "0", self.global_switches)

		self.Check_First_Played_In_Year()
		self.Register_On_Root_Files()
		self.Register_On_Game_Files_Folder()
		self.Register_On_Played_Texts_Folder()
		self.Register_On_Per_Media_Type_Files()
		self.Create_File_In_All_Files_Folder()
		self.Create_Per_Media_Type_Folders_Files()

		if self.global_switches["testing_script"] == False:
			self.Post_Status_On_WhatsApp()

		self.Register_On_Diary_Slim()
		self.Show_Info_Summary()

	def Check_First_Played_In_Year(self):
		# Check if the played game is the first played game on the year
		# If it is, then it registers it on the "Firsts of the year" folder on the current year folder

		self.firsts_of_the_year_language_texts = {
		full_language_en: "Firsts Of The Year",
		full_language_pt: "Primeiros Do Ano",
		}

		self.media_language_texts = {
		full_language_en: "Media/Game",
		full_language_pt: "Mídia/Jogo",
		}

		self.firsts_of_the_year_folders = {}
		self.firsts_of_the_year_media_folders = {}
		self.firsts_of_the_year_media_type_folders = {}

		for full_language in full_languages_not_none:
			self.firsts_of_the_year_folders[full_language] = current_notepad_year_folder + full_language + "/" + self.firsts_of_the_year_language_texts[full_language] + "/"
			self.firsts_of_the_year_media_folders[full_language] = self.firsts_of_the_year_folders[full_language] + self.media_language_texts[full_language] + "/"
			self.firsts_of_the_year_media_type_folders[full_language] = self.firsts_of_the_year_media_folders[full_language] + self.game_type + "/"

			Create_Folder(self.firsts_of_the_year_folders[full_language], self.global_switches["create_folders"])
			Create_Folder(self.firsts_of_the_year_media_folders[full_language], self.global_switches["create_folders"])
			Create_Folder(self.firsts_of_the_year_media_type_folders[full_language], self.global_switches["create_folders"])

		self.texts_to_use["Number"] = str(self.texts_to_use["Number"])

		self.first_experienced_media_file_name = str(self.texts_to_use["Number"]) + ". " + Remove_Non_File_Characters(self.game_name) + " " + Text_Replacer(Text_Replacer(str(self.texts_to_use["Times"]), ":", ";"), "/", "-")

		self.media_type_game_number_file = self.media_type_files_folder + "Number" + self.dot_text

		if is_a_file(self.media_type_game_number_file) == False:
			Write_To_File(self.media_type_game_number_file, "0", self.global_switches)

		self.media_type_experienced_number = int(Create_Array_Of_File(self.media_type_game_number_file)[0]) + 1

		self.is_first_experienced_media_per_type = False
		Create_Text_File(self.media_type_files_folder + "Games" + self.dot_text, self.global_switches["create_files"])

		if len(Create_Array_Of_File(self.media_type_files_folder + "Games" + self.dot_text)) == 0:
			self.is_first_experienced_media_per_type = True

		if self.is_first_experienced_media_per_type == True:
			for full_language in full_languages_not_none:
				media_type_folder = self.firsts_of_the_year_media_type_folders[full_language]
				self.first_experienced_media_file = media_type_folder + self.first_experienced_media_file_name + self.dot_text
				Create_Text_File(self.first_experienced_media_file, self.global_switches["create_files"])

				self.language_game_type = ""

				if ", " in self.game_type:
					self.language_game_type = "\n" + self.game_type.split(", ")[Language_Item_Definer(0, 1, full_language)]

				self.text_to_write = self.texts_to_use["Number"] + ", " + str(self.media_type_experienced_number) + "\n\n" + self.game_name + "\n\n" + self.game_type + self.language_game_type + "\n\n" + self.texts_to_use["Times"] + "\n\n" + self.texts_to_use["Time Spent"]
				Write_To_File(self.first_experienced_media_file, self.text_to_write, self.global_switches)

				if self.global_switches["verbose"] == True:
					print()
					print(self.first_experienced_media_file)
					print("[" + self.text_to_write + "]")

	def Register_On_Root_Files(self):
		# Write to root text files

		for text in self.texts_to_use:
			file = self.game_played_time_files[text]
			Create_Text_File(file, self.global_switches["create_files"])
			text_to_use = str(self.texts_to_use[text])

			Write_Function = self.functions_to_use[text]

			if Write_Function == Write_To_File:
				Write_Function(file, text_to_use, self.global_switches)

			if Write_Function == Append_To_File:
				Write_Function(file, text_to_use, self.global_switches, check_file_length = True)

			if self.global_switches["verbose"] == True:
				print("\n---\n")
				print(text)
				print(self.texts_to_use[text])
				print(file)

	def Register_On_Game_Files_Folder(self):
		# Append to "Game Files" folder text file

		self.game_files_file = self.game_files_folder + Remove_Non_File_Characters(self.game_name).replace(".", "") + self.dot_text
		Create_Text_File(self.game_files_file, self.global_switches["create_files"])

		text_to_append = self.texts_to_use["Played Time " + full_language_pt].replace("o jogo \"" + self.game_name + "\" ", "")
		Append_To_File(self.game_files_file, text_to_append, self.global_switches, check_file_length = True)

		if self.global_switches["verbose"] == True:
			print("\n---\n")
			print(text_to_append)
			print(self.game_files_file)

	def Register_On_Played_Texts_Folder(self):
		# Append to "Played Texts - Textos de Jogatina" folder text files

		for language in full_languages_not_none:
			self.played_texts_file = self.played_texts_folder + language + self.dot_text

			text_to_append = self.texts_to_use["Played Time " + language]
			Append_To_File(self.played_texts_file, text_to_append, self.global_switches, check_file_length = True)

			if self.global_switches["verbose"] == True:
				print("\n---\n")
				print(text_to_append)
				print(self.played_texts_file)

	def Register_On_Per_Media_Type_Files(self):
		# Write to "Per Media Type/Files" text files

		Append_To_File(self.media_type_files_folder + "Games" + self.dot_text, self.texts_to_use["Games"], self.global_switches, check_file_length = True)
		Append_To_File(self.media_type_files_folder + "Times" + self.dot_text, self.texts_to_use["Times"], self.global_switches, check_file_length = True)
		Append_To_File(self.media_type_files_folder + "Time Spent" + self.dot_text, self.texts_to_use["Time Spent"], self.global_switches, check_file_length = True)

		self.per_media_type_games_number = str(int(Create_Array_Of_File(self.media_type_files_folder + "Number" + self.dot_text)[0]) + 1)
		text_to_write = self.per_media_type_games_number
		Write_To_File(self.media_type_files_folder + "Number" + self.dot_text, text_to_write, self.global_switches)

		if self.global_switches["verbose"] == True:
			print("\n---\n")
			print(self.texts_to_use["Games"])
			print(self.media_type_files_folder + "Games" + self.dot_text)

			print()
			print(self.texts_to_use["Times"])
			print(self.media_type_files_folder + "Times" + self.dot_text)

			print()
			print(self.texts_to_use["Time Spent"])
			print(self.media_type_files_folder + "Time Spent" + self.dot_text)

			print()
			print(text_to_write)
			print(self.media_type_files_folder + "Number" + self.dot_text)
			print("\n---\n")

	def Create_File_In_All_Files_Folder(self):
		# Create text file in "All Played Files" folder

		self.played_game_file_name = self.texts_to_use["Times"].replace(":", ";").replace("/", "-")

		self.all_played_files_file = self.all_played_files_folder + str(self.texts_to_use["Number"]) + " " + Remove_Non_File_Characters(self.game_name) + self.dot_text
		Create_Text_File(self.all_played_files_file, self.global_switches["create_files"])

		text_to_write = self.game_name + "\n" + self.game_type + "\n" + self.texts_to_use["Times"] + "\n" + self.texts_to_use["Time Spent"] + "\n" + str(self.texts_to_use["Number"])
		Write_To_File(self.all_played_files_file, text_to_write, self.global_switches)

		if self.global_switches["verbose"] == True:
			print()
			print(text_to_write)
			print(self.all_played_files_file)
			print("\n---\n")

	def Create_Per_Media_Type_Folders_Files(self):
		# Create text files in "Per Media Type/Folders" folders

		self.all_files_folder = self.media_type_folders_folder + "All Files/"
		Create_Folder(self.all_files_folder, self.global_switches["create_folders"])

		self.game_media_type_folder = self.media_type_folders_folder + Remove_Non_File_Characters(self.game_name) + "/"
		Create_Folder(self.game_media_type_folder, self.global_switches["create_folders"])

		self.all_files_file = self.all_files_folder + Remove_Non_File_Characters(self.game_name) + " " + self.played_game_file_name + self.dot_text
		Create_Text_File(self.all_files_file, self.global_switches["create_files"])

		self.game_folder_file = self.game_media_type_folder + self.played_game_file_name + self.dot_text
		Create_Text_File(self.game_folder_file, self.global_switches["create_files"])

		text_to_write = self.game_name + "\n" + self.texts_to_use["Times"] + "\n" + self.texts_to_use["Time Spent"] + "\n" + self.per_media_type_games_number
		Write_To_File(self.all_files_file, text_to_write, self.global_switches)

		if self.global_switches["verbose"] == True:
			print()
			print(text_to_write)
			print(self.all_files_file)

		Write_To_File(self.game_folder_file, text_to_write, self.global_switches)

		if self.global_switches["verbose"] == True:
			print()
			print(text_to_write)
			print(self.game_folder_file)

		# ---------- #

	def Register_On_Diary_Slim(self):
		posted_on_whatsapp_text = "Postei print do jogo no status do WhatsApp, Instagram, Facebook, e tweet no Twitter."

		text_to_write = self.texts_to_use["Played Time " + full_language_pt] + "." + "\n\n" + posted_on_whatsapp_text
		self.diary_slim_text = Write_On_Diary_Slim_Module(text_to_write, self.texts_to_use["Times"], self.global_switches, show_text = False, return_show_text = True)

	def Post_Status_On_WhatsApp(self):
		self.post_on_whatsapp = Yes_Or_No_Definer(Language_Item_Definer("Post on", "Postar no") + " WhatsApp", second_space = False)

		if self.post_on_whatsapp == True:
			print()

			if self.global_switches["testing_script"] == False:
				Unblock(module_execution = True, options = "WhatsApp")

				Open_Link(self.whatsapp_link)

			Select_Choice(Language_Item_Definer("Press Enter to copy played text", "Pressione Enter para copiar texto de jogatina"), enter_equals_empty = True, first_space = False)

			Copy_Text(self.texts_to_use["Times"] + ":\n" + self.texts_to_use["Played Time " + full_language_pt] + ".")

			Select_Choice(Language_Item_Definer("Press Enter to open system pictures folder", "Pressione Enter para abrir a pasta de fotos do sistema"), enter_equals_empty = True, first_space = False, second_space = False)

			self.images_folder = Sanitize_File_Path(expanduser("~")).replace("/", "\\") + "Pictures"

			if self.global_switches["testing_script"] == False:
				os.system('explorer.exe "' + self.images_folder + '"')

	def Show_Info_Summary(self):
		self.played_text = self.playing_texts_language["played_the_game_for"].format(self.game_genre, self.game_name, self.variables_dict["array_to_use"][Language_Item_Definer(full_language_en, full_language_pt)], self.texts_to_use["Times"])

		print("\n-----\n")

		print(self.played_text)

		print()
		print(Language_Item_Definer("Choosen game", "Jogo escolhido") + ": ")
		print(self.game_name)

		print()
		print(self.global_texts_language["game_genre"] + ": ")
		print(self.game_genre)

		print()
		print(Language_Item_Definer("When played", "Quando jogou") + ": ")
		print(self.when_played)

		print()
		print(Language_Item_Definer("For how many time", "Por quanto tempo") + ": ")
		print(self.time_spent)

		print()
		print(self.diary_slim_text)

		print()
		print("-----")

		print()
		input(Language_Item_Definer("Press Enter when you finish reading the Info Summary", "Pressione Enter quando terminar de ler o Resumo de Informações") + ": ")
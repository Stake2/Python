# Register_Playing_Time.py

from GamePlayer.GamePlayer import GamePlayer as GamePlayer

from Social_Networks.Open_Social_Network import Open_Social_Network as Open_Social_Network

from Diary_Slim.Write_On_Diary_Slim_Module import Write_On_Diary_Slim_Module as Write_On_Diary_Slim_Module

class Register_Playing_Time(GamePlayer):
	def __init__(self, game_dictionary):
		super().__init__()

		self.game_dictionary = game_dictionary
		self.game = self.game_dictionary["game"]
		self.texts_to_use = self.game_dictionary["texts"]

		self.Check_First_Played_In_Year()

		self.Register_On_Root_Files()

		# Root folders
		self.Create_File_In_All_Files_Folder()
		self.Register_On_Game_Files_Folder()
		self.Register_On_Played_Texts_Folder()

		# Per Media Type folders
		self.Register_On_Per_Media_Type_Files()
		self.Create_Per_Media_Type_Folders_Files()

		self.Register_On_Diary_Slim()

		self.Post_On_Social_Networks()

		self.game_dictionary["show_text"] = self.language_texts["game, title()"]

		self.Show_Game_Information(self.game_dictionary)

	def Check_First_Played_In_Year(self):
		# Check if the played game is the first played game on the year
		# If it is, then it registers it on the "Firsts Of The Year" folder on the current year folder

		self.firsts_of_the_year_folders = {
			"root": {},
			"media": {},
			"media_type": {},
		}

		i = 0
		for language in self.small_languages:
			full_language = self.full_languages[language]

			self.firsts_of_the_year_folders["root"][language] = self.notepad_folders["years"]["current_year"]["root"] + full_language + "/" + self.texts["firsts_of_the_year"][language] + "/"
			self.Folder.Create(self.firsts_of_the_year_folders["root"][language])

			self.firsts_of_the_year_folders["media"][language] = self.firsts_of_the_year_folders["root"][language] + self.texts["media"][language] + "/" + self.texts["game, title()"][language] + "/"
			self.Folder.Create(self.firsts_of_the_year_folders["media"][language])

			self.firsts_of_the_year_folders["media_type"][language] = self.firsts_of_the_year_folders["media"][language] + self.game["category"]["name"] + "/"
			self.Folder.Create(self.firsts_of_the_year_folders["media_type"][language])

			i += 1

		self.file_name = {
			"numbered": str(self.texts_to_use["Number"]) + ". " + self.game["sanitized_name"],
			"time": self.texts_to_use["Times"].replace(":", ";").replace("/", "-"),
			"full": str(self.texts_to_use["Number"]) + ". " + self.game["sanitized_name"] + " " + self.texts_to_use["Times"].replace(":", ";").replace("/", "-")
		}

		self.media_type_game_number_file = self.game["category"]["media_type_files_folder"] + "Number.txt"

		if self.File.Exist(self.media_type_game_number_file) == False:
			self.File.Edit(self.media_type_game_number_file, "0", "w")

		self.per_media_type_played_number = str(int(self.File.Contents(self.media_type_game_number_file)["lines"][0]) + 1)

		self.first_game_played_in_year = False

		if len(self.File.Contents(self.game["category"]["media_type_files_folder"] + "Games.txt")["lines"]) == 0:
			self.first_game_played_in_year = True

		self.texts_to_use["full_played_text"] = str(self.texts_to_use["Number"]) + ", " + str(self.per_media_type_played_number) + "\n\n" + self.game["name"] + "\n\n" + self.game["category"]["name"] + "\n"

		if self.game["category"]["names"][self.user_language] != self.game["category"]["name"]:
			self.texts_to_use["full_played_text"] += self.game["category"]["names"][self.user_language] + "\n"

		self.texts_to_use["full_played_text"] += "\n" + self.texts_to_use["Times"] + "\n\n" + self.texts_to_use["Time spent"]

		if self.first_game_played_in_year == True:
			for language in self.small_languages:
				media_type_folder = self.firsts_of_the_year_folders["media_type"][language]

				self.first_game_played_in_year_file = media_type_folder + self.file_name["full"] + ".txt"
				self.File.Create(self.first_game_played_in_year_file)

				self.File.Edit(self.first_game_played_in_year_file, self.texts_to_use["full_played_text"], "w")

	def Register_On_Root_Files(self):
		# Write to root text files

		for file_name in self.game_played_file_names:
			file = self.game_played_files[file_name]
			self.File.Create(file)

			mode = "a"

			if file_name == "Number":
				mode = "w"

			self.File.Edit(file, str(self.texts_to_use[file_name]), mode)

	def Create_File_In_All_Files_Folder(self):
		# Create text file in "All Played Files" folder
		self.all_played_files_file = self.folders["play_history"]["played"]["all_played_files"] + self.file_name["numbered"].replace(".", "") + ".txt"
		self.File.Create(self.all_played_files_file)

		self.File.Edit(self.all_played_files_file, self.texts_to_use["full_played_text"], "w")

	def Register_On_Game_Files_Folder(self):
		# Append to "Game Files" folder text file

		self.game_files_file = self.folders["play_history"]["played"]["game_files"] + self.game["sanitized_name"] + ".txt"
		self.File.Create(self.game_files_file)

		# Split
		text_to_append = self.texts_to_use[self.translated_languages[self.user_language]["en"] + " played time"]

		text_to_append = text_to_append.replace(" " + self.language_texts["the_{}_game_called_{}"].format(self.game["category"]["names"][self.user_language], self.game["name"]), "")

		self.File.Edit(self.game_files_file, text_to_append, "a")

	def Register_On_Played_Texts_Folder(self):
		for language in self.small_languages:
			full_language = self.full_languages[language]

			file = self.folders["play_history"]["played"]["current_year"]["played_texts"] + full_language + ".txt"

			text = self.texts_to_use[self.translated_languages[language]["en"] + " played time"]

			self.File.Edit(file, text, "a")

	def Register_On_Per_Media_Type_Files(self):
		# Write to "Per Media Type/Files" text files
		for file_name in self.game_played_media_type_file_names:
			if file_name != "Number":
				self.File.Edit(self.game["category"]["media_type_files_folder"] + file_name + ".txt", self.texts_to_use[file_name], "a")

		self.File.Edit(self.game["category"]["media_type_files_folder"] + "Number.txt", self.per_media_type_played_number, "w")

	def Create_Per_Media_Type_Folders_Files(self):
		# Create text files in "Per Media Type/Folders" folders
		self.game_media_type_folder = self.game["category"]["media_type_folders_folder"] + self.game["sanitized_name"] + "/"
		self.Folder.Create(self.game_media_type_folder)

		self.apps_folders["module_files"][self.module["key"]]["folders"] = self.game_media_type_folder + self.file_name["time"] + ".txt"
		self.File.Create(self.apps_folders["module_files"][self.module["key"]]["folders"])

		self.File.Edit(self.apps_folders["module_files"][self.module["key"]]["folders"], self.texts_to_use["full_played_text"], "w")

		# Copy the "media type folders folder" to the "experienced media type folder" on current year text folder
		self.experienced_media_folder = self.notepad_folders["years"]["current_year"]["experienced_media"] + self.texts["games, title()"]["en"] + "/"
		self.Folder.Create(self.experienced_media_folder)

		self.experienced_media_type_folder = self.experienced_media_folder + self.game["category"]["name"] + "/"
		self.Folder.Create(self.experienced_media_type_folder)

		self.Folder.Copy(self.game_media_type_folder, self.experienced_media_type_folder)

	def Register_On_Diary_Slim(self):
		self.posted_on_social_networks_text = "Postei a print do jogo no status do WhatsApp, Instagram, Facebook, e tweet no Twitter."

		self.played_game_text = self.texts_to_use[self.translated_languages[self.user_language]["en"] + " played time"] + "."

		text_to_write = self.played_game_text + "\n\n" + self.posted_on_social_networks_text
		self.game_dictionary["diary_slim_text"] = Write_On_Diary_Slim_Module(text_to_write, self.texts_to_use["Times"], show_text = False)

	def Post_On_Social_Networks(self):
		self.social_networks = [
			"WhatsApp",
			"Instagram",
			"Facebook",
			"Twitter",
		]

		self.social_networks_string = self.Text.From_List(self.social_networks, break_line = False, separator = ", ")

		self.post_on_social_networks_text = self.language_texts["post_on_the_social_networks"] + " (" + self.social_networks_string + ")"

		self.post_on_social_networks = self.Input.Yes_Or_No(self.post_on_social_networks_text)

		if self.post_on_social_networks == True:
			Open_Social_Network(option_info = {"type": "profile"}, social_network_parameter = "WhatsApp", second_space = False)

			self.Input.Type(self.language_texts["press_enter_to_copy_the_played_text"])

			self.Text.Copy(self.texts_to_use["Times"] + ":\n" + self.played_game_text)
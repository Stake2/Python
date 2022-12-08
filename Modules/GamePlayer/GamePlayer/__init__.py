# GamePlayer.py

from Global_Switches import Global_Switches as Global_Switches

from Language import Language as Language
from File import File as File
from Folder import Folder as Folder
from Date import Date as Date
from Input import Input as Input
from Text import Text as Text

class GamePlayer(object):
	def __init__(self, parameter_switches = None):
		self.parameter_switches = parameter_switches

		self.Define_Basic_Variables()
		self.Define_Module_Folder()
		self.Define_Texts()

		self.Define_Folders_And_Files()
		self.Define_Lists()
		self.Create_Games_List()

	def Define_Basic_Variables(self):
		# Global Switches dictionary
		self.global_switches = Global_Switches().global_switches

		if self.parameter_switches != None:
			self.global_switches.update(self.parameter_switches)

		self.Language = Language(self.global_switches)
		self.File = File(self.global_switches)
		self.Folder = Folder(self.global_switches)
		self.Date = Date(self.global_switches)
		self.Input = Input(self.global_switches)
		self.Text = Text(self.global_switches)

		self.app_settings = self.Language.app_settings
		self.languages = self.Language.languages
		self.small_languages = self.languages["small"]
		self.full_languages = self.languages["full"]
		self.translated_languages = self.languages["full_translated"]

		self.user_language = self.Language.user_language
		self.full_user_language = self.Language.full_user_language

		self.Sanitize = self.File.Sanitize

		self.folders = self.Folder.folders
		self.root_folders = self.folders["root"]
		self.user_folders = self.folders["user"]
		self.apps_folders = self.folders["apps"]
		self.mega_folders = self.folders["mega"]
		self.notepad_folders = self.folders["notepad"]

		self.date = self.Date.date

	def Define_Module_Folder(self):
		name = self.__module__

		if "." in name:
			name = name.split(".")[0]

		self.module_text_files_folder = self.apps_folders["app_text_files"] + name + "/"
		self.Folder.Create(self.module_text_files_folder)

		self.texts_file = self.module_text_files_folder + "Texts.json"
		self.File.Create(self.texts_file)

	def Define_Texts(self):
		self.texts = self.Language.JSON_To_Python(self.texts_file)

		self.language_texts = self.Language.Item(self.texts)

		self.large_bar = "-----"
		self.dash_space = "-"

	def Define_Folders_And_Files(self):
		# Folders

		# Play History folders
		self.play_history_folder = self.notepad_folders["networks"]["game_network"] + "Play History/"
		self.Folder.Create(self.play_history_folder)

		self.played_folder = self.play_history_folder + "Played/"
		self.Folder.Create(self.played_folder)

		# Current year played folders
		self.current_year_played_folder = self.played_folder + str(self.date["year"]) + "/"
		self.Folder.Create(self.current_year_played_folder)

		self.played_texts_folder = self.current_year_played_folder + self.language_texts["played_texts, en - pt, capitalize()"] + "/"
		self.Folder.Create(self.played_texts_folder)

		self.all_played_files_folder = self.current_year_played_folder + self.texts["all_played_files"]["en"] + "/"
		self.Folder.Create(self.all_played_files_folder)

		self.game_files_folder = self.current_year_played_folder + "Game Files/"
		self.Folder.Create(self.game_files_folder)

		self.per_media_type_folder = self.current_year_played_folder + "Per Media Type/"
		self.Folder.Create(self.per_media_type_folder)

		# Per Media Type files
		self.per_media_type_files_folder = self.per_media_type_folder + "Files/"
		self.Folder.Create(self.per_media_type_files_folder)

		# Per Media Type folders
		self.per_media_type_folders_folder = self.per_media_type_folder + "Folders/"
		self.Folder.Create(self.per_media_type_folders_folder)

		# Media Network Data
		self.media_network_data_folder = self.notepad_folders["networks"]["game_network"] + "Media Network Data/"
		self.Folder.Create(self.play_history_folder)

		# Files

		# Game folders file
		self.game_folders_file = self.module_text_files_folder + "Folders.txt"
		self.File.Create(self.game_folders_file)

		

		# Game categories file
		self.game_categories_file = self.media_network_data_folder + "Game categories.txt"
		self.File.Create(self.game_categories_file)

	def Define_Lists(self):
		self.game_folder_text = self.File.Contents(self.game_folders_file)["lines"]

		self.game_played_file_names = [
			"Games",
			"Game categories",
			"Number",
			"Times",
			"Time spent",
		]

		self.game_played_media_type_file_names = self.game_played_file_names.copy()
		self.game_played_media_type_file_names.remove("Game categories")

		# Game played files
		self.game_played_files = {}

		for file_name in self.game_played_file_names:
			self.game_played_files[file_name] = self.current_year_played_folder + file_name + ".txt"

		for language in self.small_languages:
			full_language = self.full_languages[language]
			translated_language = self.translated_languages[language]["en"]

			self.game_played_files[translated_language + " played time"] = self.played_texts_folder + full_language + ".txt"

		# Create files or write zero to empty number files
		for file_name in self.game_played_files:
			file = self.game_played_files[file_name]

			if file_name != "Number":
				self.File.Create(file)

			if file_name == "Number" and self.File.Exist(file) == False:
				self.File.Edit(file, "0", "w")

		# Current year played times per language to be used in "Years.Create_Year_Summary" class
		self.current_year_played_time_language = {}

		for language in self.small_languages:
			translated_language = self.translated_languages[language]["en"   ]

			self.current_year_played_time_language[language] = []

			for played_time in self.File.Contents(self.game_played_files[translated_language + " played time"])["lines"]:
				self.current_year_played_time_language[language].append(played_time)

		self.current_year_played_number = self.File.Contents(self.game_played_files["Number"])["lines"][0]

		for game_category in self.File.Contents(self.game_categories_file)["lines"]:
			# Create Media Type files folder
			self.media_type_files_folder = self.per_media_type_files_folder + game_category + "/"
			self.Folder.Create(self.media_type_files_folder)

			# Create Media Type files
			for file_name in self.game_played_media_type_file_names:
				file = self.media_type_files_folder + file_name + ".txt"

				if file_name != "Number":
					self.File.Create(file)

				if file_name == "Number" and self.File.Exist(file) == False:
					self.File.Edit(file, "0", "w")

			# Create Media Type folders folder
			self.media_type_folders_folder = self.per_media_type_folders_folder + game_category + "/"
			self.Folder.Create(self.media_type_folders_folder)

	def Create_Games_List(self):
		self.has_multiple_game_folders = False

		if len(self.game_folder_text) > 1:
			self.has_multiple_game_folders = True

		self.games = {
			"folder": {
				"list": [],
				"list_with_numbers": [],
				"names": [],
				"file_number": [],
			},
			"files": {},
		}

		# Game folder names file
		self.games["files"]["Folder names"] = self.module_text_files_folder + "Folder names.json"
		self.File.Create(self.games["files"]["Folder names"])

		self.games["Folder names"] = self.Language.JSON_To_Python(self.games["files"]["Folder names"])

		if len(self.game_folder_text) != 0:
			for folder in self.game_folder_text:
				folder = self.root_folders["hard_drive_letter"] + folder
				self.Folder.Create(folder)

				folder_name = folder.split("/")[-2]

				contents = self.Folder.Contents(folder)

				file_number = str(len(contents["file"]["list"]))
				number_text = self.Text.By_Number(file_number, self.language_texts["game"], self.language_texts["games"])

				if int(file_number) != 0:
					# Folder
					self.games["folder"]["list"].append(folder)
					self.games["folder"]["list_with_numbers"].append(folder_name + " ({})".format(file_number + " " + number_text))
					self.games["folder"]["names"].append(folder_name)
					self.games["folder"]["file_number"].append(file_number)

					# Game files
					self.games["files"][folder_name] = {
						"list": contents["file"]["list"],
						"names": contents["file"]["names"],
					}

	def Show_Game_Information(self, game_dictionary):
		print()
		print("-----")
		print()

		print(game_dictionary["show_text"] + ":")
		print(game_dictionary["game"]["name"])
		print()

		print(self.language_texts["game_folder"] + ":")
		print(game_dictionary["game"]["category"]["folder"])
		print()

		print(self.language_texts["game_file"] + ":")
		print(game_dictionary["game"]["file"])
		print()

		print(self.language_texts["game_category"] + ":")
		print(game_dictionary["game"]["category"]["names"][self.user_language])
		print()

		if "texts" in game_dictionary:
			print(self.language_texts["when_finished_playing"] + ":")
			print(game_dictionary["texts"]["Times"])
			print()

			print(self.language_texts["for_how_much_time"] + ":")
			print(game_dictionary["texts"]["Time spent"])
			print()

			print(game_dictionary["diary_slim_text"])
			print()

		print(self.large_bar)

		if "texts" in game_dictionary:
			self.Input.Type(self.Language.language_texts["press_enter_when_you_finish_reading_the_info_summary"])
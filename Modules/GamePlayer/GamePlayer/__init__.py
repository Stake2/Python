# GamePlayer.py

from Utility.Global_Switches import Global_Switches as Global_Switches

from Utility.Language import Language as Language
from Utility.File import File as File
from Utility.Folder import Folder as Folder
from Utility.Date import Date as Date
from Utility.Input import Input as Input
from Utility.JSON import JSON as JSON
from Utility.Text import Text as Text

class GamePlayer(object):
	def __init__(self):
		self.Define_Basic_Variables()

		# Define module folders
		from Utility.Define_Folders import Define_Folders as Define_Folders

		Define_Folders(self)

		self.Define_Texts()

		self.Define_Folders_And_Files()
		self.Define_Lists_And_Dictionaries()
		self.Create_Games_List()

	def Define_Basic_Variables(self):
		self.switches = Global_Switches().switches["global"]

		self.Language = Language()
		self.File = File()
		self.Folder = Folder()
		self.Date = Date()
		self.Input = Input()
		self.JSON = JSON()
		self.Text = Text()

		self.languages = self.Language.languages

		self.user_language = self.Language.user_language
		self.full_user_language = self.Language.full_user_language

		self.Sanitize = self.File.Sanitize

		self.folders = self.Folder.folders

		self.date = self.Date.date

	def Define_Texts(self):
		self.texts = self.JSON.To_Python(self.folders["apps"]["module_files"][self.module["key"]]["texts"])

		self.language_texts = self.Language.Item(self.texts)

		self.large_bar = "-----"
		self.dash_space = "-"

	def Define_Folders_And_Files(self):
		# Folders

		# Play History folders
		self.folders["play_history"] = {
			"root": self.folders["notepad"]["networks"]["game_network"]["root"] + "Play History/",
		}

		self.Folder.Create(self.folders["play_history"]["root"])

		self.folders["play_history"]["played"] = {
			"root": self.folders["play_history"]["root"] + "Played/",
		}

		self.Folder.Create(self.folders["play_history"]["played"]["root"])

		# Current year played folders
		self.folders["play_history"]["played"]["current_year"] = {
			"root": self.folders["play_history"]["played"]["root"] + str(self.date["year"]) + "/",
		}

		self.Folder.Create(self.folders["play_history"]["played"]["current_year"]["root"])

		self.folders["play_history"]["played"]["current_year"]["played_texts"] = self.folders["play_history"]["played"]["current_year"]["root"] + self.language_texts["played_texts, en - pt, capitalize()"] + "/"

		self.Folder.Create(self.folders["play_history"]["played"]["current_year"]["played_texts"])

		self.folders["play_history"]["played"]["all_played_files"] = self.folders["play_history"]["played"]["current_year"]["root"] + self.texts["all_played_files"]["en"] + "/"
		self.Folder.Create(self.folders["play_history"]["played"]["all_played_files"])

		self.folders["play_history"]["played"]["game_files"] = self.folders["play_history"]["played"]["current_year"]["root"] + "Game Files/"
		self.Folder.Create(self.folders["play_history"]["played"]["game_files"])

		self.folders["play_history"]["played"]["per_media_type"] = {
			"root": self.folders["play_history"]["played"]["current_year"]["root"] + "Per Media Type/",
		}

		self.Folder.Create(self.folders["play_history"]["played"]["per_media_type"]["root"])

		# Per Media Type files
		self.folders["play_history"]["played"]["per_media_type"]["files"] = self.folders["play_history"]["played"]["per_media_type"]["root"] + "Files/"
		self.Folder.Create(self.folders["play_history"]["played"]["per_media_type"]["files"])

		# Per Media Type folders
		self.folders["play_history"]["played"]["per_media_type"]["folders"] = self.folders["play_history"]["played"]["per_media_type"]["root"] + "Folders/"
		self.Folder.Create(self.folders["play_history"]["played"]["per_media_type"]["folders"])

		# Media Network Data
		self.folders["notepad"]["networks"]["game_network"]["media_network_data"] = {
			"root": self.folders["notepad"]["networks"]["game_network"]["root"] + "Media Network Data/",
		}

		self.Folder.Create(self.folders["notepad"]["networks"]["game_network"]["media_network_data"]["root"])

		# Files

		# Game folder names file
		self.folders["apps"]["module_files"][self.module["key"]]["folder_names"] = self.folders["apps"]["module_files"][self.module["key"]]["root"] + "Folder names.json"
		self.File.Create(self.folders["apps"]["module_files"][self.module["key"]]["folder_names"])

		# Game folders file
		self.folders["apps"]["module_files"][self.module["key"]]["folders"] = self.folders["apps"]["module_files"][self.module["key"]]["root"] + "Folders.txt"
		self.File.Create(self.folders["apps"]["module_files"][self.module["key"]]["folders"])

		# Game names file
		self.folders["apps"]["module_files"][self.module["key"]]["game_names"] = self.folders["apps"]["module_files"][self.module["key"]]["root"] + "Game names.json"
		self.File.Create(self.folders["apps"]["module_files"][self.module["key"]]["game_names"])

		# Game categories file
		self.folders["notepad"]["networks"]["game_network"]["media_network_data"]["game_categories"] = self.folders["notepad"]["networks"]["game_network"]["media_network_data"]["root"] + "Game categories.txt"
		self.File.Create(self.folders["notepad"]["networks"]["game_network"]["media_network_data"]["game_categories"])

	def Define_Lists_And_Dictionaries(self):
		# Lists
		self.game_folder_text = self.File.Contents(self.folders["apps"]["module_files"][self.module["key"]]["folders"])["lines"]

		self.game_played_file_names = [
			"Games",
			"Game categories",
			"Number",
			"Times",
			"Time spent",
		]

		self.game_played_media_type_file_names = self.game_played_file_names.copy()
		self.game_played_media_type_file_names.remove("Game categories")

		# Dictionaries

		# Game played files
		self.game_played_files = {}

		for file_name in self.game_played_file_names:
			self.game_played_files[file_name] = self.folders["play_history"]["played"]["current_year"]["root"] + file_name + ".txt"

		for language in self.languages["small"]:
			full_language = self.languages["full"][language]
			translated_language = self.languages["full_translated"][language]["en"]

			self.game_played_files[translated_language + " played time"] = self.folders["play_history"]["played"]["current_year"]["played_texts"] + full_language + ".txt"

		# Create files or write zero to empty number files
		for file_name in self.game_played_files:
			file = self.game_played_files[file_name]

			if file_name != "Number":
				self.File.Create(file)

			if file_name == "Number" and self.File.Exist(file) == False:
				self.File.Edit(file, "0", "w")

		# Current year played times per language to be used in "Years.Create_Year_Summary" class
		self.current_year_played_time_language = {}

		for language in self.languages["small"]:
			translated_language = self.languages["full_translated"][language]["en"   ]

			self.current_year_played_time_language[language] = []

			for played_time in self.File.Contents(self.game_played_files[translated_language + " played time"])["lines"]:
				self.current_year_played_time_language[language].append(played_time)

		self.current_year_played_number = self.File.Contents(self.game_played_files["Number"])["lines"][0]

		for game_category in self.File.Contents(self.folders["notepad"]["networks"]["game_network"]["media_network_data"]["game_categories"])["lines"]:
			# Create Media Type files folder
			self.media_type_files_folder = self.folders["play_history"]["played"]["per_media_type"]["files"] + game_category + "/"
			self.Folder.Create(self.media_type_files_folder)

			# Create Media Type files
			for file_name in self.game_played_media_type_file_names:
				file = self.media_type_files_folder + file_name + ".txt"

				if file_name != "Number":
					self.File.Create(file)

				if file_name == "Number" and self.File.Exist(file) == False:
					self.File.Edit(file, "0", "w")

			# Create Media Type folders folder
			self.media_type_folders_folder = self.folders["play_history"]["played"]["per_media_type"]["folders"] + game_category + "/"
			self.Folder.Create(self.media_type_folders_folder)

		self.game_names = self.JSON.To_Python(self.folders["apps"]["module_files"][self.module["key"]]["game_names"])

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

		self.games["Folder names"] = self.JSON.To_Python(self.folders["apps"]["module_files"][self.module["key"]]["folder_names"])

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
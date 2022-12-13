# Project_Zomboid.py

from Global_Switches import Global_Switches as Global_Switches

from Language import Language as Language
from File import File as File
from Folder import Folder as Folder
from Date import Date as Date
from Input import Input as Input
from Text import Text as Text

class Project_Zomboid(object):
	def __init__(self, parameter_switches = None):
		self.parameter_switches = parameter_switches

		self.Define_Basic_Variables()
		self.Define_Module_Folder()
		self.Define_Texts()

		self.Define_Folders_And_Files()
		self.Define_Lists_And_Dictionaries()

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
		self.media_multiverse_folder = self.mega_folders["stories"]["root"] + "Others/Media Multiverse/"
		self.Folder.Create(self.media_multiverse_folder)

		self.media_multiverse_games_folder = self.media_multiverse_folder + "Games - Jogos/"
		self.Folder.Create(self.media_multiverse_games_folder)

		self.project_zomboid_folder = self.media_multiverse_games_folder + "Project Zomboid/"
		self.Folder.Create(self.project_zomboid_folder)

		self.database_folder = self.project_zomboid_folder + "Database/"
		self.Folder.Create(self.database_folder)

		self.predefined_values_file = self.module_text_files_folder + "Predefined values.json"
		self.File.Create(self.predefined_values_file)

	def Define_Lists_And_Dictionaries(self):
		self.kentucky_city_names = [
			"Muldraugh, KY",
			"Riverside, KY",
			"Rosewood, KY",
			"West Point, KY",
		]

		self.kentucky_cities = {}

		for city in self.kentucky_city_names:
			self.kentucky_cities[city] = {}

			self.kentucky_cities[city]["folder"] = self.project_zomboid_folder + city + "/"
			self.Folder.Create(self.kentucky_cities[city]["folder"])

			self.kentucky_cities[city]["database_folder"] = self.database_folder + city + "/"
			self.Folder.Create(self.kentucky_cities[city]["database_folder"])

			self.kentucky_cities[city]["survivors_file"] = self.kentucky_cities[city]["database_folder"] + "Survivors.txt"
			self.File.Create(self.kentucky_cities[city]["survivors_file"])

			self.kentucky_cities[city]["survivors"] = self.File.Contents(self.kentucky_cities[city]["survivors_file"])["lines"]
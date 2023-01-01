# Diary.py

from Global_Switches import Global_Switches as Global_Switches

from Language import Language as Language
from File import File as File
from Folder import Folder as Folder
from Date import Date as Date
from Input import Input as Input
from Text import Text as Text

class Diary():
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
		self.module = {
			"name": self.__module__,
		}

		if "." in self.module["name"]:
			self.module["name"] = self.module["name"].split(".")[0]

		self.module["key"] = self.module["name"].lower()

		self.apps_folders["modules"][self.module["key"]] = {
			"root": self.apps_folders["modules"]["root"] + self.module["name"] + "/",
		}

		self.apps_folders["module_files"][self.module["key"]] = {
			"root": self.apps_folders["module_files"]["root"] + self.module["name"] + "/",
		}

		for item in ["module_files", "modules"]:
			self.apps_folders[item][self.module["key"]] = self.apps_folders[item]["root"] + self.module["name"] + "/"
			self.apps_folders[item][self.module["key"]] = self.Folder.Contents(self.apps_folders[item][self.module["key"]], lower_key = True)["dictionary"]

	def Define_Texts(self):
		self.texts = self.Language.JSON_To_Python(self.apps_folders["module_files"][self.module["key"]]["texts"])

		self.language_texts = self.Language.Item(self.texts)

		self.large_bar = "-----"
		self.dash_space = "-"

	def Define_Folders_And_Files(self):
		# Folders
		self.diary_chapters_folder = self.mega_folders["notepad"]["effort"]["diary"]["root"] + "Chapters/"
		self.Folder.Create(self.diary_chapters_folder)

		# Files
		self.diary_file = self.mega_folders["notepad"]["effort"]["diary"]["root"] + "Diary.txt"
		self.File.Create(self.diary_file)

		self.diary_number_file = self.mega_folders["notepad"]["effort"]["diary"]["root"] + "Number.txt"
		self.File.Create(self.diary_number_file)

		self.current_diary_file = self.mega_folders["notepad"]["effort"]["diary"]["root"] + "Current File.txt"
		self.File.Create(self.current_diary_file)

	def Define_Lists_And_Dictionaries(self):
		# Lists
		self.current_diary_text_file = self.File.Contents(self.current_diary_file)["lines"][0]

		self.diary_number = self.File.Contents(self.diary_number_file)["lines"][0]

		self.presenters = [
			"Izaque",
			"Nodus",
			"Ted",
		]

		self.presenter_numbers = [
			"1",
			"2",
			"3",
		]

		self.finish_texts = [
			"f",
			"finish",
			"stop",
			"parar",
			"terminar",
			"completar",
			"acabar",
		]

		list_ = [
			'{}: {}',
			"{}: //{}",
			"{}: ~{}",
		]

		# Dictionaries
		self.presenter_format_texts = {}

		i = 0
		for presenter in self.presenters:
			self.presenter_format_texts[presenter] = list_[i]

			i += 1
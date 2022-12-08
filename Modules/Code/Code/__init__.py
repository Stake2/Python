# Code.py

from Global_Switches import Global_Switches as Global_Switches

from Language import Language as Language
from File import File as File
from Folder import Folder as Folder
from Date import Date as Date
from Input import Input as Input
from Text import Text as Text

class Code(object):
	def __init__(self, parameter_switches = None):
		self.parameter_switches = parameter_switches

		self.Define_Basic_Variables()
		self.Define_Module_Folder()
		self.Define_Texts()

		self.Define_Folders()
		self.Define_Lists()

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

		self.code_footer = "\n" + self.large_bar + "\n"

	def Define_Folders(self):
		self.programming_network_folder = self.notepad_folders["effort"]["networks"]["root"] + "Programming Network/"
		self.Folder.Create(self.programming_network_folder)

		self.database_folder = self.programming_network_folder + "Database/"
		self.Folder.Create(self.database_folder)

		self.database_file_names = [
			"Programming languages",
		]

		self.database_files = {}

		for file_name in self.database_file_names:
			self.database_files[file_name] = self.database_folder + file_name + ".txt"
			self.File.Create(self.database_files[file_name])

	def Define_Lists(self):
		self.programming_languages = self.File.Contents(self.database_files["Programming languages"])["lines"]

		self.programming_language_folders = {}

		for programming_language in self.programming_languages:
			self.programming_language_folders[programming_language] = self.database_folder + programming_language + "/"
			self.Folder.Create(self.programming_language_folders[programming_language])

		self.basic_functions = {
			"self.File.Open": self.File.Open,
			"self.Text.Open_Link": self.Text.Open_Link,
			"self.File.Close": self.File.Close,
		}

		self.programming_mode_item_names = [
			"Tools",
			"Custom tools",
			"First function",
			"Final function",
			"Setting file",
			"Modes",
		]

		self.tool_sub_names = [
			self.language_texts["programs_to_close"],
			self.language_texts["function, title()"],
			self.language_texts["close_tool"],
		]
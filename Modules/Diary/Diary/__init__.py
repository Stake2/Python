# Diary.py

from Utility.Global_Switches import Global_Switches as Global_Switches

from Utility.Language import Language as Language
from Utility.File import File as File
from Utility.Folder import Folder as Folder
from Utility.Date import Date as Date
from Utility.Input import Input as Input
from Utility.JSON import JSON as JSON
from Utility.Text import Text as Text

class Diary():
	def __init__(self):
		self.Define_Basic_Variables()

		# Define module folders
		from Utility.Define_Folders import Define_Folders as Define_Folders

		Define_Folders(self)

		self.Define_Texts()

		self.Define_Folders_And_Files()
		self.Define_Lists_And_Dictionaries()

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
		self.diary_chapters_folder = self.folders["mega"]["notepad"]["effort"]["diary"]["root"] + "Chapters/"
		self.Folder.Create(self.diary_chapters_folder)

		# Files
		self.diary_file = self.folders["mega"]["notepad"]["effort"]["diary"]["root"] + "Diary.txt"
		self.File.Create(self.diary_file)

		self.diary_number_file = self.folders["mega"]["notepad"]["effort"]["diary"]["root"] + "Number.txt"
		self.File.Create(self.diary_number_file)

		self.current_diary_file = self.folders["mega"]["notepad"]["effort"]["diary"]["root"] + "Current File.txt"
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
# Diary.py

class Diary():
	def __init__(self):
		self.Import_Modules()
		self.Define_Module_Folder()
		self.Define_Texts()

		self.Define_Folders_And_Files()
		self.Define_Lists_And_Dictionaries()

	def Import_Modules(self):
		from Utility.Modules import Modules as Modules

		# Get modules dictionary
		self.modules = Modules().Set(self)

	def Define_Module_Folder(self):
		self.module = {
			"name": self.__module__,
		}

		if "." in self.module["name"]:
			self.module["name"] = self.module["name"].split(".")[0]

		self.module["key"] = self.module["name"].lower()

		for item in ["module_files", "modules"]:
			self.folders["apps"][item][self.module["key"]] = self.folders["apps"][item]["root"] + self.module["name"] + "/"
			self.Folder.Create(self.folders["apps"][item][self.module["key"]])

			self.folders["apps"][item][self.module["key"]] = self.Folder.Contents(self.folders["apps"][item][self.module["key"]], lower_key = True)["dictionary"]

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
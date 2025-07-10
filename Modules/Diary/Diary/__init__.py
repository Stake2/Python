# Diary.py

# Import the "importlib" module
import importlib

class Diary():
	def __init__(self):
		# Import the classes
		self.Import_Classes()

		# Define the folders of the module
		self.folders = self.Define_Folders(object = self).folders

		# Module related methods
		self.Define_Basic_Variables()
		self.Define_Texts()

		# Folders, files, lists, and dictionaries methods
		self.Define_Folders_And_Files()
		self.Define_Lists_And_Dictionaries()

	def Import_Classes(self):
		# Define the list of modules to be imported
		modules = [
			"Define_Folders",
			"JSON"
		]

		# Iterate through the list of modules
		for module_title in modules:
			# Import the module
			module = importlib.import_module("." + module_title, "Utility")

			# Get the sub-class
			sub_class = getattr(module, module_title)

			# If the module title is not "Define_Folders"
			if module_title != "Define_Folders":
				# Run the sub-class to define its variable
				sub_class = sub_class()

			# Add the sub-class to the current module
			setattr(self, module_title, sub_class)

		# Define the "Language" class as the same class inside the "JSON" class
		self.Language = self.JSON.Language

	def Define_Basic_Variables(self):
		# Get the dictionary of modules
		self.modules = self.JSON.To_Python(self.folders["Apps"]["Modules"]["Modules"])

		# Create a list of the modules that will not be imported
		remove_list = [
			"Define_Folders",
			"Modules",
			"Language",
			"JSON"
		]

		# Iterate through the list of utility modules
		for module_title in self.modules["Utility"]["List"]:
			# If the module title is not inside the remove list
			if module_title not in remove_list:
				# Import the module
				module = importlib.import_module("." + module_title, "Utility")

				# Get the sub-class of the module
				sub_class = getattr(module, module_title)

				# Add the sub-class to the current class
				setattr(self, module_title, sub_class())

		# ---------- #

		# Get the switches dictionary from the "Global Switches" class
		self.switches = self.Global_Switches.switches["Global"]

		# ---------- #

		# Import some variables from the "Language" class

		# Import the "languages" dictionary
		self.languages = self.Language.languages

		# Import the "language" dictionary
		self.language = self.Language.language

		# Import the "separators" dictionary
		self.separators = self.Language.separators

		# ---------- #

		# Import the "folders" dictionary from the "Folder" class
		self.folders = self.Folder.folders

		# ---------- #

		# Import the "Sanitize" method from the "File" class
		self.Sanitize = self.File.Sanitize

		# ---------- #

		# Get the current date from the "Date" class
		self.date = self.Date.date

	def Define_Texts(self):
		# Define the "Texts" dictionary
		self.texts = self.JSON.To_Python(self.module["Files"]["Texts"])

		# Define the "Language texts" dictionary
		self.language_texts = self.Language.Item(self.texts)

	def Define_Folders_And_Files(self):
		# Folders
		self.diary_chapters_folder = self.folders["Notepad"]["Diary"]["root"] + "Chapters/"
		self.Folder.Create(self.diary_chapters_folder)

		# Files
		self.diary_file = self.folders["Notepad"]["Diary"]["root"] + "Diary.txt"
		self.File.Create(self.diary_file)

		self.diary_number_file = self.folders["Notepad"]["Diary"]["root"] + "Number.txt"
		self.File.Create(self.diary_number_file)

		self.current_diary_file = self.folders["Notepad"]["Diary"]["root"] + "Current File.txt"
		self.File.Create(self.current_diary_file)

	def Define_Lists_And_Dictionaries(self):
		# Lists
		self.current_diary_text_file = self.File.Contents(self.current_diary_file)["lines"][0]

		self.diary_number = self.File.Contents(self.diary_number_file)["lines"][0]

		self.presenters = [
			"Izaque",
			"Nodus",
			"Ted"
		]

		self.presenter_numbers = [
			"1",
			"2",
			"3"
		]

		self.finish_texts = [
			"f",
			"finish",
			"stop",
			"parar",
			"terminar",
			"completar",
			"acabar"
		]

		list_ = [
			'{}: {}',
			"{}: //{}",
			"{}: ~{}"
		]

		# Dictionaries
		self.presenter_format_texts = {}

		i = 0
		for presenter in self.presenters:
			self.presenter_format_texts[presenter] = list_[i]

			i += 1
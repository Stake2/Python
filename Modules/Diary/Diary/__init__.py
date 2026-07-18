# Diary.py

# Import some useful modules
import importlib

# Define the main "Diary" class
class Diary():
	def __init__(self):
		# Define the variables of the class
		self.Define_Variables()

		# Folders, files, lists, and dictionaries methods
		self.Define_Folders_And_Files()
		self.Define_Lists_And_Dictionaries()

	def Define_Variables(self):
		# Import the "JSON" class
		from Utility.JSON import JSON as JSON

		# Instance it and add it to the current class
		self.JSON = JSON()

		# Import the "folders" dictionary from the "JSON" class
		self.folders = self.JSON.folders

		# ---------- #

		# Get the dictionary of Python modules
		self.modules = self.JSON.To_Python(self.folders["Python"]["Modules"]["Modules"])

		# Define a list of utility classes to not import
		do_not_import = [
			"Text"
		]

		# Iterate through the list of utility classes
		for class_title in self.modules["Utility"]["List"]:
			# If the class is not already inside the self class (Diary)
			if hasattr(self, class_title) == False:
				# If the class title is not inside the list of utility classes to not import
				# And it is is not inside the list of optional classes
				if (
					class_title not in do_not_import and
					class_title not in self.modules["Utility"]["Optional"]
				):
					# Import the module of the class
					module = importlib.import_module("." + class_title, "Utility")

					# Get the class object inside the module
					class_object = getattr(module, class_title)

					# If the class title is not "Modules"
					if class_title != "Modules":
						# Run the class object to define its attributes
						class_object = class_object()

					# Add the class object to the root class
					setattr(self, class_title, class_object)

		# ---------- #

		# Define the module dictionary and the module folders and files
		self.Modules(class_object = self)

		# ---------- #

		# Import the switches dictionary from the "Global Switches" class
		self.switches = self.Global_Switches.switches["Global"]

		# ---------- #

		# Define the "Language" class as the same class inside the "JSON" class
		self.Language = self.JSON.Language

		# Import some attributes from the "Language" class

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

		# Get the current date from the "Date" class
		self.date = self.Date.date

		# ---------- #

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
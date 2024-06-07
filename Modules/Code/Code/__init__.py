# Code.py

# Import the "importlib" module
import importlib

import Utility

class Code(object):
	def __init__(self):
		# Import the classes
		self.Import_Classes()

		# Define the folders of the module
		self.folders = Utility.Define_Folders(object = self).folders

		# Module related methods
		self.Define_Basic_Variables()
		self.Define_Texts()

		# Folders, lists, and dictionaries methods
		self.Define_Folders()
		self.Define_Lists_And_Dictioinaries()

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
				# Add the sub-class to the current module
				setattr(self, module_title, sub_class())

			# If the module title is "Define_Folders"
			if module_title == "Define_Folders":
				# Add the sub-class to the "Utility" module
				setattr(Utility, "Define_Folders", sub_class)

		# Define the "Language" class as the same class inside the "JSON" class
		self.Language = self.JSON.Language

	def Define_Basic_Variables(self):
		# Get the modules list
		self.modules = self.JSON.To_Python(self.folders["Apps"]["Modules"]["Modules"])

		# Create a list of the modules that will not be imported
		remove_list = [
			"Define_Folders",
			"Modules",
			"Language",
			"JSON"
		]

		# Iterate through the Utility modules
		for module_title in self.modules["Utility"]["List"]:
			# If the module title is not inside the remove list
			if module_title not in remove_list:
				# Import the module
				module = importlib.import_module("." + module_title, "Utility")

				# Get the sub-class
				sub_class = getattr(module, module_title)

				# Add the sub-class to the current module
				setattr(self, module_title, sub_class())

		# Get the switches dictionary from the "Global Switches" module
		self.switches = self.Global_Switches.switches["Global"]

		# Get the Languages dictionary
		self.languages = self.Language.languages

		# Get the user language and full user language
		self.user_language = self.Language.user_language
		self.full_user_language = self.Language.full_user_language

		# Define the local folders dictionary as the Folder folders dictionary
		self.folders = self.Folder.folders

		# Get the Sanitize method of the File class
		self.Sanitize = self.File.Sanitize

		# Get the current date from the Date module
		self.date = self.Date.date

	def Define_Texts(self):
		# Define the "Texts" dictionary
		self.texts = self.JSON.To_Python(self.module["Files"]["Texts"])

		# Define the "Language texts" dictionary
		self.language_texts = self.Language.Item(self.texts)

		# Define the "Separators" dictionary
		self.separators = {}

		# Create separators from one to ten characters
		for number in range(1, 11):
			# Define the empty string
			string = ""

			# Add separators to it
			while len(string) != number:
				string += "-"

			# Add the string to the Separators dictionary
			self.separators[str(number)] = string

		self.code_footer = "\n" + self.separators["5"] + "\n"

	def Define_Folders(self):
		self.programming_network_folder = self.folders["Notepad"]["Data Networks"]["root"] + self.Language.language_texts["programming, title()"] + "/"
		self.Folder.Create(self.programming_network_folder)

		self.programming_network_file_names = [
			"Programming languages",
		]

		self.programming_network_files = {}

		for file_name in self.programming_network_file_names:
			self.programming_network_files[file_name] = self.programming_network_folder + file_name + ".txt"
			self.File.Create(self.programming_network_files[file_name])

	def Define_Lists_And_Dictioinaries(self):
		self.programming_languages = self.File.Contents(self.programming_network_files["Programming languages"])["lines"]

		self.programming_language_folders = {}

		for programming_language in self.programming_languages:
			self.programming_language_folders[programming_language] = self.programming_network_folder + programming_language + "/"
			self.Folder.Create(self.programming_language_folders[programming_language])

		self.basic_functions = {
			"System.Open_Link": self.System.Open_Link
		}

		self.programming_mode_item_names = [
			"Tools",
			"Custom tools",
			"First function",
			"Final function",
			"Setting file",
			"Modes"
		]

		self.tool_sub_names = [
			self.language_texts["programs_to_close"],
			self.language_texts["function, title()"],
			self.language_texts["close_tool"]
		]
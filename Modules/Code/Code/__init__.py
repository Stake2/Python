# Code.py

class Code(object):
	def __init__(self):
		# Define the module folders
		from Utility.Define_Folders import Define_Folders as Define_Folders

		Define_Folders(self)

		self.Define_Basic_Variables()

		self.Define_Texts()

		self.Define_Folders()
		self.Define_Lists_And_Dictioinaries()

	def Define_Basic_Variables(self):
		from copy import deepcopy

		# Import the JSON module
		from Utility.JSON import JSON as JSON

		self.JSON = JSON()

		# Get the modules list
		self.modules = self.JSON.To_Python(self.folders["apps"]["modules"]["modules"])

		# Import the "importlib" module
		import importlib

		# Create a list of the modules that will not be imported
		remove_list = [
			"Define_Folders",
			"Language"
		]

		# Iterate through the Utility modules
		for module_title in self.modules["Utility"]["List"]:
			# If the module title is not inside the remove list
			if module_title not in remove_list:
				# Import the module
				module = importlib.import_module("." + module_title, "Utility")

				# Get the sub-class
				sub_class = getattr(module, module_title)

				# Add the sub-clas to the current module
				setattr(self, module_title, sub_class())

		# Make a backup of the module folders
		self.module_folders = {}

		for item in ["modules", "module_files"]:
			self.module_folders[item] = deepcopy(self.folders["apps"][item][self.module["key"]])

		# Define the local folders dictionary as the Folder folders dictionary
		self.folders = self.Folder.folders

		# Restore the backup of the module folders
		for item in ["modules", "module_files"]:
			self.folders["apps"][item][self.module["key"]] = self.module_folders[item]

		# Get the switches dictionary from the "Global Switches" module
		self.switches = self.Global_Switches.switches["Global"]

		# Get the Languages dictionary
		self.languages = self.JSON.Language.languages

		# Get the user language and full user language
		self.user_language = self.JSON.Language.user_language
		self.full_user_language = self.JSON.Language.full_user_language

		# Get the Sanitize method of the File class
		self.Sanitize = self.File.Sanitize

		# Get the current date from the Date module
		self.date = self.Date.date

	def Define_Texts(self):
		self.texts = self.JSON.To_Python(self.folders["apps"]["module_files"][self.module["key"]]["texts"])

		self.language_texts = self.JSON.Language.Item(self.texts)

		self.large_bar = "-----"
		self.dash_space = "-"

		self.code_footer = "\n" + self.large_bar + "\n"

	def Define_Folders(self):
		self.programming_network_folder = self.folders["notepad"]["effort"]["networks"]["root"] + "Programming Network/"
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
			"self.System.Open": self.System.Open,
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
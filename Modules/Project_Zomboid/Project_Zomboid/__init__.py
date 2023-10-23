# Project_Zomboid.py

class Project_Zomboid(object):
	def __init__(self):
		# Define the module folders
		from Utility.Define_Folders import Define_Folders as Define_Folders

		Define_Folders(self)

		self.Define_Basic_Variables()

		self.Define_Texts()

		self.Define_Folders_And_Files()
		self.Define_Lists_And_Dictionaries()

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

	def Define_Folders_And_Files(self):
		self.media_multiverse_folder = self.folders["mega"]["stories"]["root"] + "Others/Media Multiverse/"
		self.Folder.Create(self.media_multiverse_folder)

		self.media_multiverse_games_folder = self.media_multiverse_folder + self.JSON.Language.language_texts["games, title()"] + "/"
		self.Folder.Create(self.media_multiverse_games_folder)

		self.project_zomboid_folder = self.media_multiverse_games_folder + "Project Zomboid/"
		self.Folder.Create(self.project_zomboid_folder)

		self.database_folder = self.project_zomboid_folder + "Database/"
		self.Folder.Create(self.database_folder)

		self.predefined_values_file = self.folders["apps"]["module_files"][self.module["key"]]["root"] + "Predefined values.json"
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
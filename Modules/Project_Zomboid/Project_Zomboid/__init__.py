# Project_Zomboid.py

class Project_Zomboid(object):
	def __init__(self):
		self.Define_Basic_Variables()

		# Define module folders
		from Utility.Define_Folders import Define_Folders as Define_Folders

		Define_Folders(self)

		self.Define_Texts()

		self.Define_Folders_And_Files()
		self.Define_Lists_And_Dictionaries()

	def Define_Basic_Variables(self):
		from Utility.Global_Switches import Global_Switches as Global_Switches

		from Utility.File import File as File
		from Utility.Folder import Folder as Folder
		from Utility.Date import Date as Date
		from Utility.Input import Input as Input
		from Utility.JSON import JSON as JSON
		from Utility.Text import Text as Text

		self.switches = Global_Switches().switches["global"]

		self.File = File()
		self.Folder = Folder()
		self.Date = Date()
		self.Input = Input()
		self.JSON = JSON()
		self.Text = Text()

		self.languages = self.JSON.Language.languages

		self.user_language = self.JSON.Language.user_language
		self.full_user_language = self.JSON.Language.full_user_language

		self.Sanitize = self.File.Sanitize

		self.folders = self.Folder.folders

		self.date = self.Date.date

	def Define_Texts(self):
		self.texts = self.JSON.To_Python(self.folders["apps"]["module_files"][self.module["key"]]["texts"])

		self.language_texts = self.JSON.Language.Item(self.texts)

		self.large_bar = "-----"
		self.dash_space = "-"

	def Define_Folders_And_Files(self):
		self.media_multiverse_folder = self.folders["mega"]["stories"]["root"] + "Others/Media Multiverse/"
		self.Folder.Create(self.media_multiverse_folder)

		self.media_multiverse_games_folder = self.media_multiverse_folder + "Games - Jogos/"
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
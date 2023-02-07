# Project_Zomboid.py

class Project_Zomboid(object):
	def __init__(self):
		self.Import_Modules()
		self.Define_Module_Folder()
		self.Define_Texts()

		self.Define_Folders_And_Files()
		self.Define_Lists_And_Dictionaries()

	def Import_Modules(self):
		self.modules = self.Modules.Set(self)

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
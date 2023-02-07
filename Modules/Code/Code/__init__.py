# Code.py

class Code(object):
	def __init__(self):
		self.Import_Modules()
		self.Define_Module_Folder()
		self.Define_Texts()

		self.Define_Folders()
		self.Define_Lists_And_Dictioinaries()

	def Import_Modules(self):
		self.modules = self.Modules.Set(self, utility_modules = ["Diary_Slim"])

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
# Code.py

class Code(object):
	def __init__(self):
		self.Define_Basic_Variables()

		# Define module folders
		from Utility.Define_Folders import Define_Folders as Define_Folders

		Define_Folders(self)

		self.Define_Texts()

		self.Define_Folders()
		self.Define_Lists_And_Dictioinaries()

	def Define_Basic_Variables(self):
		from Utility.Global_Switches import Global_Switches as Global_Switches

		from Utility.File import File as File
		from Utility.Folder import Folder as Folder
		from Utility.Date import Date as Date
		from Utility.Input import Input as Input
		from Utility.JSON import JSON as JSON
		from Utility.Text import Text as Text

		self.switches = Global_Switches().switches["Global"]

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
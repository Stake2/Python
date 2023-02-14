# Tasks.py

class Tasks(object):
	def __init__(self):
		self.Define_Basic_Variables()

		# Define module folders
		from Utility.Define_Folders import Define_Folders as Define_Folders

		Define_Folders(self)

		self.Define_Texts()

		from Years.Years import Years as Years

		# Load Years module
		self.Years = Years(self.switches)

		self.Define_Folders_And_Files()

		self.Define_Types()
		self.Define_Registry_Format()

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
		self.current_year = self.Years.current_year

		# Folders dictionary
		self.folders = self.Folder.Contents(self.folders["notepad"]["networks"]["productive_network"]["root"], lower_key = True)["dictionary"]

		self.folders["task_history"]["current_year"] = self.folders["task_history"][str(self.date["year"])]

	def Define_Types(self):
		self.task_types = self.JSON.To_Python(self.folders["data"]["types"])

		# Iterate through English plural task types list
		i = 0
		for plural_task_type in self.task_types["plural"]["en"]:
			key = plural_task_type.lower().replace(" ", "_")

			# Create task type dictionary
			self.task_types[plural_task_type] = {
				"singular": {},
				"plural": {},
				"folders": {},
				"subfolders": {},
				"item_folders": {},
				"items": {}
			}

			# Define singular and plural types
			for language in self.languages["small"]:
				for item in ["singular", "plural"]:
					self.task_types[plural_task_type][item][language] = self.task_types[item][language][i]

			# Create "Per task type" task type folder
			self.folders["task_history"]["current_year"]["per_task_type"][key] = {
				"root": self.folders["task_history"]["current_year"]["per_task_type"]["root"] + plural_task_type + "/"
			}

			self.Folder.Create(self.folders["task_history"]["current_year"]["per_task_type"][key]["root"])

			# Create "Tasks.json" file in "Per task type" task type folder
			self.folders["task_history"]["current_year"]["per_task_type"][key]["tasks"] = self.folders["task_history"]["current_year"]["per_task_type"][key]["root"] + "Tasks.json"
			self.File.Create(self.folders["task_history"]["current_year"]["per_task_type"][key]["tasks"])

			# Create "Entry list.txt" file in "Per task type" task type folder
			self.folders["task_history"]["current_year"]["per_task_type"][key]["entry_list"] = self.folders["task_history"]["current_year"]["per_task_type"][key]["root"] + "Entry list.txt"
			self.File.Create(self.folders["task_history"]["current_year"]["per_task_type"][key]["entry_list"])

			# Create "Files" folder on "Per task type" task type folder
			self.folders["task_history"]["current_year"]["per_task_type"][key]["files"] = {
				"root": self.folders["task_history"]["current_year"]["per_task_type"][key]["root"] + "Files/"
			}

			self.Folder.Create(self.folders["task_history"]["current_year"]["per_task_type"][key]["files"]["root"])

			# Define type folders and files
			self.task_types[plural_task_type]["folders"] = {
				"per_task_type": self.folders["task_history"]["current_year"]["per_task_type"][key]
			}

			# Define task type subfolders
			for language in self.languages["small"]:
				for item in ["Art", "Programming"]:
					if plural_task_type in self.task_types["subfolders, type: dict"][item]:
						self.task_types[plural_task_type]["subfolders"][language] = self.JSON.Language.texts[item.lower() + ", title()"][language]

				# Define task item folders
				self.task_types[plural_task_type]["item_folders"][language] = self.task_types["items, type: dict"][language][plural_task_type]

			i += 1

	def Define_Registry_Format(self):
		from copy import deepcopy

		# Define default Tasks dictionary template
		self.template = {
			"Numbers": {
				"Total": 0,
			},
			"Entries": [],
			"Dictionary": {}
		}

		self.dictionaries = {
			"Tasks": deepcopy(self.template),
			"Task": {},
			"Task Type": {}
		}

		# If Tasks.json is not empty, get Tasks dictionary from it
		if self.File.Contents(self.folders["task_history"]["current_year"]["tasks"])["lines"] != [] and self.JSON.To_Python(self.folders["task_history"]["current_year"]["tasks"])["Entries"] != []:
			self.dictionaries["Tasks"] = self.JSON.To_Python(self.folders["task_history"]["current_year"]["tasks"])

		self.JSON.Edit(self.folders["task_history"]["current_year"]["tasks"], self.dictionaries["Tasks"])

		# Iterate through English plural task types list
		for plural_task_type in self.task_types["plural"]["en"]:
			key = plural_task_type.lower().replace(" ", "_")

			# Define default task type dictionary
			self.dictionaries["Task Type"][plural_task_type] = deepcopy(self.template)

			# If task type "Tasks.json" is not empty, get task type Tasks dictionary from it
			if self.File.Contents(self.folders["task_history"]["current_year"]["per_task_type"][key]["tasks"])["lines"] != [] and self.JSON.To_Python(self.folders["task_history"]["current_year"]["per_task_type"][key]["tasks"])["Entries"] != []:
				self.dictionaries["Task Type"][plural_task_type] = self.JSON.To_Python(self.folders["task_history"]["current_year"]["per_task_type"][key]["tasks"])

			self.JSON.Edit(self.folders["task_history"]["current_year"]["per_task_type"][key]["tasks"], self.dictionaries["Task Type"][plural_task_type])

	def Define_States_Dictionary(self, dictionary):
		dict_ = {}

		keys = [
			"First Task In Year",
			"First Task Type Task In Year"
		]

		for key in keys:
			if dictionary["States"][key] == True:
				state = True

				key = key.title()

				dict_[key] = state

		return dict_
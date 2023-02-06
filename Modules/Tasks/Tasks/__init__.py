# Tasks.py

from Years.Years import Years as Years

from copy import deepcopy

class Tasks(object):
	def __init__(self):
		self.Import_Modules()
		self.Define_Module_Folder()
		self.Define_Texts()

		# Load Years module
		self.Years = Years(select_year = False)

		self.Define_Folders_And_Files()
		self.Define_Tasks_Files()

	def Import_Modules(self):
		from Utility.Modules import Modules as Modules

		# Get modules dictionary
		self.modules = Modules().Set(self)

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
		self.current_year = self.Years.current_year

		# Folders dictionary
		self.folders = self.Folder.Contents(self.folders["notepad"]["networks"]["productive_network"]["root"], lower_key = True)["dictionary"]

		self.folders["task_history"]["current_year"] = self.folders["task_history"][str(self.date["year"])]

	def Define_Tasks_Files(self):
		self.task_types = self.JSON.To_Python(self.folders["network_data"]["task_types"])

		# Define default Episodes dictionary template
		self.template = {
			"Number": 0,
			"Number. Task Type (Time)": [],
			"Dictionary": {},
			"Lists": {
				"Titles": {},
				"Types": [],
				"Times": {
					"ISO8601": [],
					"Language DateTime": {}
				}
			}
		}

		self.tasks = self.template.copy()

		# Add language lists to task titles and task Language DateTime dictionaries
		for language in self.languages["small"]:
			self.tasks["Lists"]["Titles"][language] = []
			self.tasks["Lists"]["Times"]["Language DateTime"][language] = []

		# If Tasks.json is not empty, get Tasks dictionary from it
		if self.File.Contents(self.folders["task_history"]["current_year"]["tasks"])["lines"] != []:
			self.tasks = self.JSON.To_Python(self.folders["task_history"]["current_year"]["tasks"])

		# If Tasks.json is empty, write default Tasks dictionary inside it
		if self.File.Contents(self.folders["task_history"]["current_year"]["tasks"])["lines"] == []:
			self.JSON.Edit(self.folders["task_history"]["current_year"]["tasks"], self.tasks)

		# Define default Task Type Tasks dictionary
		self.task_type_tasks = {}

		# Iterate through English task types list
		for task_type in self.task_types["en"]:
			key = task_type.lower().replace(" ", "_")

			# Create "Per Task Type" task type folder
			self.folders["task_history"]["current_year"]["per_task_type"][key] = {
				"root": self.folders["task_history"]["current_year"]["per_task_type"]["root"] + task_type + "/"
			}

			self.Folder.Create(self.folders["task_history"]["current_year"]["per_task_type"][key]["root"])

			# Create "Files" folder on "Per Task Type" task type folder
			self.folders["task_history"]["current_year"]["per_task_type"][key]["files"] = {
				"root": self.folders["task_history"]["current_year"]["per_task_type"][key]["root"] + "Files/"
			}

			self.Folder.Create(self.folders["task_history"]["current_year"]["per_task_type"][key]["files"]["root"])

			# Create "Tasks.json" file in "Per Task Type" task type folder
			self.folders["task_history"]["current_year"]["per_task_type"][key]["tasks"] = self.folders["task_history"]["current_year"]["per_task_type"][key]["root"] + "Tasks.json"

			self.File.Create(self.folders["task_history"]["current_year"]["per_task_type"][key]["tasks"])

			# Define default task type dictionary
			self.task_type_tasks[task_type] = deepcopy(self.template)
			self.task_type_tasks[task_type]["Lists"].pop("Types")

			# Add language lists to titles and task Language DateTime dictionaries
			for language in self.languages["small"]:
				self.task_type_tasks[task_type]["Lists"]["Titles"][language] = []
				self.task_type_tasks[task_type]["Lists"]["Times"]["Language DateTime"][language] = []

			# If Task Type Tasks.json is not empty, get Task Type Tasks dictionary from it
			if self.File.Contents(self.folders["task_history"]["current_year"]["per_task_type"][key]["tasks"])["lines"] != []:
				self.task_type_tasks[task_type] = self.JSON.To_Python(self.folders["task_history"]["current_year"]["per_task_type"][key]["tasks"])

			# If Task Type Tasks.json is empty, write default Task Type Tasks dictionary inside it
			if self.File.Contents(self.folders["task_history"]["current_year"]["per_task_type"][key]["tasks"])["lines"] == []:
				self.JSON.Edit(self.folders["task_history"]["current_year"]["per_task_type"][key]["tasks"], self.task_type_tasks[task_type])

			# Create "File list.txt" file in "Per Task Type" task type folder
			self.folders["task_history"]["current_year"]["per_task_type"][key]["file_list"] = self.folders["task_history"]["current_year"]["per_task_type"][key]["root"] + "File list.txt"

			self.File.Create(self.folders["task_history"]["current_year"]["per_task_type"][key]["file_list"])

	def Define_States_Dictionary(self, dictionary):
		dict_ = {}

		keys = [
			"first_task_in_year",
			"first_task_type_task_in_year"
		]

		for key in keys:
			if dictionary["register"]["states"][key] == True:
				state = True

				key = key.title()

				dict_[key] = state

		return dict_
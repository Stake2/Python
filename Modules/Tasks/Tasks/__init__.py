# Tasks.py

from Utility.Global_Switches import Global_Switches as Global_Switches

from Utility.Language import Language as Language
from Utility.File import File as File
from Utility.Folder import Folder as Folder
from Utility.Date import Date as Date
from Utility.Input import Input as Input
from Utility.JSON import JSON as JSON
from Utility.Text import Text as Text

from Years.Years import Years as Years

from copy import deepcopy

class Tasks(object):
	def __init__(self):
		self.Define_Basic_Variables()

		# Define module folders
		from Utility.Define_Folders import Define_Folders as Define_Folders

		Define_Folders(self)

		self.Define_Texts()

		# Load Years module
		self.Years = Years(self.switches, select_year = False)

		self.Define_Folders_And_Files()
		self.Define_Tasks_Files()

	def Define_Basic_Variables(self):
		self.switches = Global_Switches().switches["global"]

		self.Language = Language()
		self.File = File()
		self.Folder = Folder()
		self.Date = Date()
		self.Input = Input()
		self.JSON = JSON()
		self.Text = Text()

		self.languages = self.Language.languages

		self.user_language = self.Language.user_language
		self.full_user_language = self.Language.full_user_language

		self.Sanitize = self.File.Sanitize

		self.folders = self.Folder.folders

		self.date = self.Date.date

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

			# Create "Entry list.txt" file in "Per Task Type" task type folder
			self.folders["task_history"]["current_year"]["per_task_type"][key]["entry_list"] = self.folders["task_history"]["current_year"]["per_task_type"][key]["root"] + "Entry list.txt"

			self.File.Create(self.folders["task_history"]["current_year"]["per_task_type"][key]["entry_list"])

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
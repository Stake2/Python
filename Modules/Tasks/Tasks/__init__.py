# Tasks.py

from Global_Switches import Global_Switches as Global_Switches

from Language import Language as Language
from File import File as File
from Folder import Folder as Folder
from Date import Date as Date
from Input import Input as Input
from JSON import JSON as JSON
from Text import Text as Text

class Tasks(object):
	def __init__(self, parameter_switches = None):
		self.parameter_switches = parameter_switches

		self.Define_Basic_Variables()
		self.Define_Module_Folder()
		self.Define_Texts()

		self.Define_Folders_And_Files()
		self.Define_Lists_And_Dicitionaries()

	def Define_Basic_Variables(self):
		# Global Switches dictionary
		self.global_switches = Global_Switches().global_switches

		if self.parameter_switches != None:
			self.global_switches.update(self.parameter_switches)

		self.Language = Language(self.global_switches)
		self.File = File(self.global_switches)
		self.Folder = Folder(self.global_switches)
		self.Date = Date(self.global_switches)
		self.Input = Input(self.global_switches)
		self.JSON = JSON(self.global_switches)
		self.Text = Text(self.global_switches)

		self.app_settings = self.Language.app_settings
		self.languages = self.Language.languages
		self.small_languages = self.languages["small"]
		self.full_languages = self.languages["full"]
		self.translated_languages = self.languages["full_translated"]

		self.user_language = self.Language.user_language
		self.full_user_language = self.Language.full_user_language

		self.Sanitize = self.File.Sanitize

		self.folders = self.Folder.folders
		self.root_folders = self.folders["root"]
		self.user_folders = self.folders["user"]
		self.apps_folders = self.folders["apps"]
		self.mega_folders = self.folders["mega"]
		self.notepad_folders = self.folders["notepad"]

		self.date = self.Date.date

	def Define_Module_Folder(self):
		self.module = {
			"name": self.__module__,
		}

		if "." in self.module["name"]:
			self.module["name"] = self.module["name"].split(".")[0]

		self.module["key"] = self.module["name"].lower()

		self.apps_folders["modules"][self.module["key"]] = {
			"root": self.apps_folders["modules"]["root"] + self.module["name"] + "/",
		}

		self.apps_folders["module_files"][self.module["key"]] = {
			"root": self.apps_folders["module_files"]["root"] + self.module["name"] + "/",
		}

		for item in ["module_files", "modules"]:
			self.apps_folders[item][self.module["key"]] = self.apps_folders[item]["root"] + self.module["name"] + "/"
			self.apps_folders[item][self.module["key"]] = self.Folder.Contents(self.apps_folders[item][self.module["key"]], lower_key = True)["dictionary"]

	def Define_Texts(self):
		self.texts = self.JSON.To_Python(self.apps_folders["module_files"][self.module["key"]]["texts"])

		self.language_texts = self.Language.Item(self.texts)

		self.large_bar = "-----"
		self.dash_space = "-"

	def Define_Folders_And_Files(self):
		# Folders dictionary
		self.folders = self.Folder.Contents(self.notepad_folders["networks"]["productive_network"]["root"], lower_key = True)["dictionary"]

		self.folders["task_history"]["current_year"] = self.folders["task_history"][str(self.date["year"])]

	def Define_Lists_And_Dicitionaries(self):
		self.task_types = self.JSON.To_Python(self.folders["media_network_data"]["task_types"])

		# Define default Tasks dictionary
		self.tasks = {
			"Number": 0,
			"Types": [],
			"Titles": {},
			"Times": {
				"ISO8601": [],
				"Language DateTime": {},
			},
			"Number. Task Type (Time)": [],
		}

		# Add language lists to task titles and task Language DateTime dictionaries
		for language in self.small_languages:
			self.tasks["Titles"][language] = []
			self.tasks["Times"]["Language DateTime"][language] = []

		# If Tasks.json is not empty, get Tasks dictionary from it
		if self.File.Contents(self.folders["task_history"]["current_year"]["tasks"])["lines"] != []:
			self.tasks = self.JSON.To_Python(self.folders["task_history"]["current_year"]["tasks"])

		# If Tasks.json is empty, write default Tasks dictionary inside it
		if self.File.Contents(self.folders["task_history"]["current_year"]["tasks"])["lines"] == []:
			self.JSON.Edit(self.folders["task_history"]["current_year"]["tasks"], self.tasks)

	def Add_Task_Types_To_Tasks(self):
		# Iterate through English task types list
		for task_type in self.task_types["en"]:
			# Create "Per Task Type" task type folder
			self.folders["task_history"]["current_year"]["per_task_type"][task_type] = {
				"root": self.folders["task_history"]["current_year"]["per_task_type"]["root"] + task_type + "/"
			}

			self.Folder.Create(self.folders["task_history"]["current_year"]["per_task_type"][task_type]["root"])

			# Create "Files" folder on "Per Task Type" task type folder
			self.folders["task_history"]["current_year"]["per_task_type"][task_type]["files"] = {
				"root": self.folders["task_history"]["current_year"]["per_task_type"][task_type]["root"] + "Files/"
			}

			self.Folder.Create(self.folders["task_history"]["current_year"]["per_task_type"][task_type]["files"]["root"])

			# Create "Tasks.json" file in "Per Task Type" task type folder
			self.folders["task_history"]["current_year"]["per_task_type"][task_type]["tasks"] = self.folders["task_history"]["current_year"]["per_task_type"][task_type]["root"] + "Tasks.json"

			self.File.Create(self.folders["task_history"]["current_year"]["per_task_type"][task_type]["tasks"])

			# Get Tasks dictionary from Tasks.json file if it is not empty
			if self.File.Contents(self.folders["task_history"]["current_year"]["per_task_type"][task_type]["tasks"])["lines"] != []:
				self.tasks[task_type] = self.JSON.To_Python(self.folders["task_history"]["current_year"]["per_task_type"][task_type]["tasks"])

			# Define default task type dictionary if Tasks.json file is empty
			if self.File.Contents(self.folders["task_history"]["current_year"]["per_task_type"][task_type]["tasks"])["lines"] == []:
				self.tasks[task_type] = {
					"Number": 0,
					"Titles": {}
				}

				for language in self.small_languages:
					self.tasks[task_type]["Titles"][language] = []

				# Create times list key
				self.tasks[task_type]["Times"] = {
					"ISO8601": [],
					"Language DateTime": {}
				}

				for language in self.small_languages:
					self.tasks[task_type]["Times"]["Language DateTime"][language] = []

				self.tasks[task_type]["Number. Task Type (Time)"] = []

				# Write default Tasks dictionary inside "Tasks.json" file
				self.JSON.Edit(self.folders["task_history"]["current_year"]["per_task_type"][task_type]["tasks"], self.tasks[task_type])

			# Create "Task list.txt" file in "Per Task Type" task type folder
			self.folders["task_history"]["current_year"]["per_task_type"][task_type]["task_list"] = self.folders["task_history"]["current_year"]["per_task_type"][task_type]["root"] + "Task list.txt"

			self.File.Create(self.folders["task_history"]["current_year"]["per_task_type"][task_type]["task_list"])
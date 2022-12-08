# Tasks.py

from Global_Switches import Global_Switches as Global_Switches

from Language import Language as Language
from File import File as File
from Folder import Folder as Folder
from Date import Date as Date
from Input import Input as Input
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
		name = self.__module__

		if "." in name:
			name = name.split(".")[0]

		self.module_text_files_folder = self.apps_folders["app_text_files"] + name + "/"
		self.Folder.Create(self.module_text_files_folder)

		self.texts_file = self.module_text_files_folder + "Texts.json"
		self.File.Create(self.texts_file)

	def Define_Texts(self):
		self.texts = self.Language.JSON_To_Python(self.texts_file)

		self.language_texts = self.Language.Item(self.texts)

		self.large_bar = "-----"
		self.dash_space = "-"

	def Define_Folders_And_Files(self):
		# Folders dictionary
		self.folders = {
			"root": self.notepad_folders["networks"]["productive_network"],
		}

		self.Folder.Create(self.folders["root"])

		# Media Network Data folder
		self.folders["Media Network Data"] = {
			"root": self.folders["root"] + "Media Network Data/",
		}

		self.Folder.Create(self.folders["Media Network Data"]["root"])

		# Task Types file
		self.folders["Media Network Data"]["Task Types"] = self.folders["Media Network Data"]["root"] + self.texts["task_types"]["en"] + ".json"
		self.File.Create(self.folders["Media Network Data"]["root"])

		# Task History folder
		self.folders["Task History"] = {
			"root": self.folders["root"] + "Task History/",
		}

		self.Folder.Create(self.folders["Task History"]["root"])

		# Current year Task History folder
		self.folders["Task History"][str(self.date["year"])] = {
			"root": self.folders["Task History"]["root"] + str(self.date["year"]) + "/",
		}

		self.Folder.Create(self.folders["Task History"][str(self.date["year"])]["root"])

		# Create files on the current year Task History folder
		for item in ["Number", "Task Types", "Tasks", "Tasks.json", "Times"]:
			self.folders["Task History"][str(self.date["year"])][item] = self.folders["Task History"][str(self.date["year"])]["root"] + item

			if ".json" not in item:
				self.folders["Task History"][str(self.date["year"])][item] += ".txt"

			self.File.Create(self.folders["Task History"][str(self.date["year"])][item])

		# Write to number file if it is empty
		if self.File.Contents(self.folders["Task History"][str(self.date["year"])]["Number"])["lines"] == []:
			self.File.Edit(self.folders["Task History"][str(self.date["year"])]["Number"], "0", "w")

		# All Tasks Files folder
		self.folders["Task History"][str(self.date["year"])]["All Task Files"] = self.folders["Task History"][str(self.date["year"])]["root"] + "All Task Files/"
		self.Folder.Create(self.folders["Task History"][str(self.date["year"])]["All Task Files"])

		# Per Task Type folder
		self.folders["Task History"][str(self.date["year"])]["Per Task Type"] = {
			"root": self.folders["Task History"][str(self.date["year"])]["root"] + "Per Task Type/",
		}

		self.Folder.Create(self.folders["Task History"][str(self.date["year"])]["Per Task Type"]["root"])

		# Per Task Type subfolders
		for item in ["Files", "Folders"]:
			self.folders["Task History"][str(self.date["year"])]["Per Task Type"][item] = {
				"root": self.folders["Task History"][str(self.date["year"])]["Per Task Type"]["root"] + item + "/",
			}

			self.Folder.Create(self.folders["Task History"][str(self.date["year"])]["Per Task Type"][item]["root"])

	def Define_Lists_And_Dicitionaries(self):
		self.task_types = self.Language.JSON_To_Python(self.folders["Media Network Data"]["Task Types"])

		# Per Task Type sub-sub-folders
		for task_type in self.task_types["en"]:
			for item in ["Files", "Folders"]:
				self.folders["Task History"][str(self.date["year"])]["Per Task Type"][item][task_type] = {
					"root": self.folders["Task History"][str(self.date["year"])]["Per Task Type"][item]["root"] + task_type + "/",
				}

				self.Folder.Create(self.folders["Task History"][str(self.date["year"])]["Per Task Type"][item][task_type]["root"])

				for file_name in ["Number", "Task Types", "Tasks", "Tasks.json", "Times"]:
					self.folders["Task History"][str(self.date["year"])]["Per Task Type"][item][task_type][file_name] = self.folders["Task History"][str(self.date["year"])]["Per Task Type"][item][task_type]["root"] + file_name

					if ".json" not in file_name:
						self.folders["Task History"][str(self.date["year"])]["Per Task Type"][item][task_type][file_name] += ".txt"

					self.Folder.Create(self.folders["Task History"][str(self.date["year"])]["Per Task Type"][item][task_type][file_name])
# Diary_Slim.py

from Global_Switches import Global_Switches as Global_Switches

from Language import Language as Language
from File import File as File
from Folder import Folder as Folder
from Date import Date as Date
from Input import Input as Input
from Text import Text as Text

class Diary_Slim():
	def __init__(self, parameter_switches = None):
		self.parameter_switches = parameter_switches

		self.Define_Basic_Variables()
		self.Define_Module_Folder()
		self.Define_Texts()

		self.Define_Folders_And_Files()
		self.Define_Lists_And_Dictionaries()

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
		self.texts = self.Language.JSON_To_Python(self.apps_folders["module_files"][self.module["key"]]["texts"])

		self.language_texts = self.Language.Item(self.texts)

		self.large_bar = "-----"
		self.dash_space = "-"

		self.text_header_prototype = "- Diário Slim, {} -"
		self.day_of_of_text = "Dia {} de {} de {}"
		self.today_is_text_header_prototype = "Hoje é {}, " + self.day_of_of_text + "."

	def Define_Folders_And_Files(self):
		# Folders
		self.diary_slim_data_folder = self.mega_folders["notepad"]["effort"]["diary_slim"]["root"] + "Data/"
		self.Folder.Create(self.diary_slim_data_folder)

		self.state_texts_folder = self.diary_slim_data_folder + "State texts/"
		self.Folder.Create(self.state_texts_folder)

		self.database_folder = self.mega_folders["notepad"]["effort"]["diary_slim"]["root"] + "Database/"
		self.Folder.Create(self.database_folder)

		self.year_folders = self.Date.Create_Years_List("dict", 2020, function = str, string_format = self.mega_folders["notepad"]["effort"]["diary_slim"]["root"] + "{}" + "/")

		for folder in self.year_folders.values():
			self.Folder.Create(folder)

		self.database_year_folders = self.Date.Create_Years_List("dict", 2020, function = str, string_format = self.database_folder + "{}" + "/")

		for folder in self.database_year_folders.values():
			self.Folder.Create(folder)

		self.current_year_folder = self.year_folders[self.date["year"]]
		self.Folder.Create(self.current_year_folder)

		# Current month folder
		self.month_folder_name = str(self.Text.Add_Leading_Zeros(self.date["month"])) + " - " + self.date["month_name"]

		self.current_month_folder = self.current_year_folder + self.month_folder_name + "/"
		self.Folder.Create(self.current_month_folder)

		# Current month database folder
		self.current_month_database_folder = self.database_year_folders[self.date["year"]] + self.month_folder_name + "/"
		self.Folder.Create(self.current_month_database_folder)

		# Files
		self.slim_texts_file = self.diary_slim_data_folder + "Slim texts.json"
		self.File.Create(self.slim_texts_file)

		self.file_names_file = self.database_folder + "File names.txt"
		self.File.Create(self.file_names_file)

		self.year_folders_file = self.database_folder + "Year folders.txt"
		self.File.Create(self.year_folders_file)

		self.month_folders_file = self.database_folder + "Month folders.txt"
		self.File.Create(self.month_folders_file)

		# Current year database file
		self.current_year_file_names_file = self.database_year_folders[self.date["year"]] + "Year file names.txt"
		self.File.Create(self.current_year_file_names_file)

		# Current month database file
		self.current_month_file_names_file = self.current_month_database_folder + "Month file names.txt"
		self.File.Create(self.current_month_file_names_file)

		self.current_diary_slim_file = self.mega_folders["notepad"]["effort"]["diary_slim"]["root"] + "Current file.txt"
		self.File.Create(self.current_diary_slim_file)

		self.things_to_do_file = self.diary_slim_data_folder + "Things to do.txt"
		self.File.Create(self.things_to_do_file)

		self.things_done_texts_file = self.diary_slim_data_folder + "Things done texts.txt"
		self.File.Create(self.things_done_texts_file)

		self.diary_slim_header_file = self.apps_folders["module_files"][self.module_name_lower]["root"] + "Header.txt"
		self.File.Create(self.diary_slim_header_file)

	def Define_Lists_And_Dictionaries(self):
		# Lists
		self.current_diary_slim = self.File.Contents(self.current_diary_slim_file)["lines"][0]

		self.diary_slim_header = self.File.Contents(self.diary_slim_header_file)["string"]

		# Dictionaries
		self.states = {
			"order_names": [
				"first",
				"second",
				"current",
			],
			"names": [],
			"folders": self.Folder.Contents(self.state_texts_folder),
		}

		i = 0
		for state in self.states["folders"]["folder"]["names"]:
			# Read state names
			names = self.Language.JSON_To_Python(self.states["folders"]["folder"]["list"][i] + "Names.json")
			state = names[self.user_language]

			# Add state name to names list
			self.states["names"].append(state)

			# Create state dictionary and sub-keys
			self.states[state] = {}
			self.states[state]["files"] = {}
			self.states[state]["texts"] = {}

			# Add state names file and dictionary
			self.states[state]["files"]["names"] = self.states["folders"]["folder"]["list"][i] + "Names.json"
			self.states[state]["names"] = names

			# List orders of state, add file and list or dictionary to order dictionary
			for order_name in self.states["order_names"]:
				self.states[state]["files"][order_name] = self.states["folders"]["folder"]["list"][i] + order_name.capitalize() + "."

				if order_name == "current":
					self.states[state]["files"][order_name] += "txt"
					function = self.File.Contents

				if order_name != "current":
					self.states[state]["files"][order_name] += "json"
					function = self.Language.JSON_To_Python

				self.states[state]["texts"][order_name] = function(self.states[state]["files"][order_name])

				if order_name == "current":
					self.states[state]["texts"][order_name] = self.states[state]["texts"][order_name]["lines"]

			i += 1

	def Update_State(self, selected_state = None, new_order = ""):
		for state in self.states["names"]:
			state_texts = self.states[state]["texts"]

			# Define current state file
			current_state_file = self.states[state]["files"]["current"]
			string = self.File.Contents(current_state_file)["string"]

			# If new order is not empty, get the order from state_texts dictionary
			if new_order != "":
				new_order = state_texts[new_order][self.user_language]

			# Write the new order if the state is equal to the selected state
			# If the state is equal to none, or if the selected state is equal to none
			if state == selected_state or state == None or selected_state == None:
				self.File.Edit(current_state_file, new_order, "w")

	def Open_Current_Diary_Slim(self):
		self.File.Open(self.current_diary_slim)
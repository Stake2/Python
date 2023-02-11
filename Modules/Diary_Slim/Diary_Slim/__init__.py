# Diary_Slim.py

class Diary_Slim():
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

		self.text_header_prototype = "- Diário Slim, {} -"
		self.day_of_of_text = "Dia {} de {} de {}"
		self.today_is_text_header_prototype = "Hoje é {}, " + self.day_of_of_text + "."

	def Define_Folders_And_Files(self):
		# Folders
		self.diary_slim_data_folder = self.folders["mega"]["notepad"]["effort"]["diary_slim"]["root"] + "Data/"
		self.Folder.Create(self.diary_slim_data_folder)

		self.state_texts_folder = self.diary_slim_data_folder + "State texts/"
		self.Folder.Create(self.state_texts_folder)

		self.database_folder = self.folders["mega"]["notepad"]["effort"]["diary_slim"]["root"] + "Database/"
		self.Folder.Create(self.database_folder)

		self.year_folders = self.Date.Create_Years_List("dict", 2020, function = str, string_format = self.folders["mega"]["notepad"]["effort"]["diary_slim"]["root"] + "{}" + "/")

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

		self.current_diary_slim_file = self.folders["mega"]["notepad"]["effort"]["diary_slim"]["root"] + "Current file.txt"
		self.File.Create(self.current_diary_slim_file)

		self.things_to_do_file = self.diary_slim_data_folder + "Things to do.txt"
		self.File.Create(self.things_to_do_file)

		self.things_done_texts_file = self.diary_slim_data_folder + "Things done texts.txt"
		self.File.Create(self.things_done_texts_file)

		self.diary_slim_header_file = self.folders["apps"]["module_files"][self.module["key"]]["root"] + "Header.txt"
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
			names = self.JSON.To_Python(self.states["folders"]["folder"]["list"][i] + "Names.json")
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
					function = self.JSON.To_Python

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
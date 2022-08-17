# Diary_Slim.py

from Script_Helper import *

class Diary_Slim():
	def __init__(self, parameter_switches = None):
		# Verbose variable
		self.verbose = False

		self.testing_script = False

		self.parameter_switches = parameter_switches

		self.Define_Basic_Variables()
		self.Define_Diary_Slim_Variables()
		self.Define_Double_State_Texts()

	def Define_Basic_Variables(self):
		self.option = True

		# Global Switches dictionary
		self.global_switches = {
			"write_to_file": self.option,
			"create_files": self.option,
			"create_folders": self.option,
			"move_files": self.option,
			"verbose": self.verbose,
			"testing_script": self.testing_script,
		}

		if self.parameter_switches != None:
			self.global_switches = self.parameter_switches
			self.testing_script = self.global_switches["testing_script"]

		if self.global_switches["testing_script"] == True:
			print(Language_Item_Definer("Testing script: Yes", "Testando script: Sim"))

		if self.global_switches["verbose"] == True:
			print(Language_Item_Definer("Verbose on", "Verbose ligado") + ".")

		if self.global_switches["testing_script"] == True:
			self.global_switches["write_to_file"] = False
			self.global_switches["create_files"] = False

		self.dot_text = ".txt"

	def Define_Diary_Slim_Variables(self):
		self.diary_slim_folder = notepad_folder_effort + "Diary Slim/"
		Create_Folder(self.diary_slim_folder, self.global_switches["create_folders"])

		self.diary_slim_data_folder = self.diary_slim_folder + "Slim Data/"
		Create_Folder(self.diary_slim_data_folder, self.global_switches["create_folders"])

		self.diary_slim_double_state_texts_folder = self.diary_slim_data_folder + "Double State Texts/"
		Create_Folder(self.diary_slim_double_state_texts_folder, self.global_switches["create_folders"])

		self.diary_slim_database_folder = self.diary_slim_folder + "Slim Database/"
		Create_Folder(self.diary_slim_database_folder, self.global_switches["create_folders"])

		self.all_file_names_file = self.diary_slim_database_folder + "All File Names" + self.dot_text
		Create_Text_File(self.all_file_names_file, self.global_switches["create_files"])

		self.all_year_folders_file = self.diary_slim_database_folder + "All Year Folders" + self.dot_text
		Create_Text_File(self.all_year_folders_file, self.global_switches["create_files"])

		self.all_month_folders_file = self.diary_slim_database_folder + "All Month Folders" + self.dot_text
		Create_Text_File(self.all_month_folders_file, self.global_switches["create_files"])

		self.diary_slim_year_folders = {}
		Add_Years_To_Array(self.diary_slim_year_folders, str, "dict", self.diary_slim_folder + "{}" + "/", 2020)

		for folder in self.diary_slim_year_folders.values():
			Create_Folder(folder, self.global_switches["create_folders"])

		self.diary_slim_database_year_folders = {}
		Add_Years_To_Array(self.diary_slim_database_year_folders, str, "dict", self.diary_slim_database_folder + "{}" + "/", 2020)

		for folder in self.diary_slim_database_year_folders.values():
			Create_Folder(folder, self.global_switches["create_folders"])

		self.diary_slim_current_year_folder = self.diary_slim_year_folders[str(current_year)]
		Create_Folder(self.diary_slim_current_year_folder, self.global_switches["create_folders"])

		self.current_diary_slim_file = self.diary_slim_folder + "Current File" + self.dot_text
		Create_Text_File(self.current_diary_slim_file, self.global_switches["create_files"])

		self.current_diary_slim = Create_Array_Of_File(self.current_diary_slim_file)[0]

		self.diary_slim_things_to_do_file = self.diary_slim_data_folder + "Things To Do" + self.dot_text
		Create_Text_File(self.diary_slim_things_to_do_file, self.global_switches["create_files"])

		self.diary_slim_things_done_texts_file = self.diary_slim_data_folder + "Things Done Texts" + self.dot_text
		Create_Text_File(self.diary_slim_things_done_texts_file, self.global_switches["create_files"])

		self.state_file_names = ["First", "Second", "Current"]
		self.state_names = []
		self.state_files = {}
		self.state_texts = {}

		self.state_folders = List_Folder(self.diary_slim_double_state_texts_folder)

		for folder in self.state_folders:
			folder_name = folder
			folder = self.diary_slim_double_state_texts_folder + folder + "/"

			self.state_names.append(folder_name)

			files = [
			folder + "First State" + self.dot_text,
			folder + "Second State" + self.dot_text,
			folder + "Current State" + self.dot_text,
			]

			self.state_files[folder_name] = {}

			i = 0
			for file_name in self.state_file_names:
				file_name = file_name + " State"
				self.state_files[folder_name][file_name] = files[i]

				i += 1

		for folder in self.state_folders:
			self.state_texts[folder_name] = {}

			for file_name in self.state_file_names:
				file_name = file_name + " State"
				self.state_texts[folder_name][file_name] = Create_Array_Of_File(self.state_files[folder][file_name])

				if self.state_texts[folder_name][file_name] != []:
					self.state_texts[folder_name][file_name] = self.state_texts[folder_name][file_name][0]

	def Define_Double_State_Texts(self):
		self.english_states = {}
		self.portuguese_states = {}

		for state in self.state_names:
			state_texts = self.state_texts[state]
			self.current_state = state_texts["Current State"]
			self.current_state_backup = state_texts["Current State"]
			self.current_english_state = state_texts["Current State"]
			self.current_portuguese_state = state_texts["Current State"]

			changed_state = False

			if self.current_state_backup != []:
				self.current_english_state = Split_Text_By_Language(global_language, self.current_english_state, 0)
				self.current_portuguese_state = Split_Text_By_Language(global_language, self.current_portuguese_state, 1)

			if self.current_state_backup == []:
				key = "First State"
				self.current_state = state_texts[key]
				self.current_english_state = Split_Text_By_Language(global_language, state_texts[key], 0)
				self.current_portuguese_state = Split_Text_By_Language(global_language, state_texts[key], 1)

				changed_state = True

			if self.current_state_backup == state_texts["First State"] and changed_state == False:
				key = "Second State"
				self.current_state = state_texts[key]
				self.current_english_state = Split_Text_By_Language(global_language, state_texts[key], 0)
				self.current_portuguese_state = Split_Text_By_Language(global_language, state_texts[key], 1)

				changed_state = True

			self.english_states[state] = self.current_english_state
			self.portuguese_states[state] = self.current_portuguese_state

		self.language_first_state_text = Language_Item_Definer("first state", "primeiro estado")
		self.language_second_state_text = Language_Item_Definer("second state", "segundo estado")

		self.state_position_names = {}

		for state in self.state_names:
			state_texts = self.state_texts[state]
			first_state_text = state_texts["First State"]
			second_state_text = state_texts["Second State"]

			for file_name in self.state_file_names:
				self.state_position_names[state] = {}
				self.state_position_names[state][first_state_text] = self.language_first_state_text
				self.state_position_names[state][second_state_text] = self.language_second_state_text

	def Change_Double_State_Texts(self, module_current_state = None, reset_current_state = False):
		self.module_current_state = module_current_state

		for folder in self.state_folders:
			current_state_file = self.state_files[folder]["Current State"]
			self.file_current_state = Create_Array_Of_File(current_state_file)

			if self.file_current_state != []:
				self.file_current_state = self.file_current_state[0]

			text_to_write = None

			if self.file_current_state != self.module_current_state and reset_current_state == False:
				text_to_write = self.module_current_state

			if reset_current_state == True:
				text_to_write = ""

			if text_to_write != None:
				Write_To_File(current_state_file, text_to_write, self.global_switches)

	def Open_Current_Diary_Slim(self):
		Open_Text_File(self.current_diary_slim)
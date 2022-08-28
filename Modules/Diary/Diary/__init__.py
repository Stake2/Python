# Diary.py

from Script_Helper import *

class Diary():
	def __init__(self, parameter_switches = None):
		# Verbose variable
		self.verbose = False

		self.testing_script = False

		self.parameter_switches = parameter_switches

		self.Define_Basic_Variables()
		self.Define_Diary_Variables()

	def Define_Basic_Variables(self):
		self.option = True

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

	def Define_Diary_Variables(self):
		self.diary_folder = notepad_diary_folder
		Create_Folder(self.diary_folder, self.global_switches)

		self.diary_chapters_folder = self.diary_folder + "Chapters/"
		Create_Folder(self.diary_chapters_folder, self.global_switches)

		self.diary_file = self.diary_folder + "Diary" + self.dot_text
		Create_Text_File(self.diary_file, self.global_switches)

		self.diary_number_file = self.diary_folder + "Number" + self.dot_text
		Create_Text_File(self.diary_number_file, self.global_switches)

		self.current_diary_file = self.diary_folder + "Current File" + self.dot_text
		Create_Text_File(self.current_diary_file, self.global_switches)

		self.current_diary_text_file = Create_Array_Of_File(self.current_diary_file)[0]

		self.diary_number = Create_Array_Of_File(self.diary_number_file)[0]

		self.characters = {
		"Izaque": "Izaque",
		"Nodus": "Nodus",
		"Ted": "Ted",
		}

		self.lower_characters = {
		"Izaque": "izaque",
		"Nodus": "nodus",
		"Ted": "ted",
		}

		self.character_format_texts = {
		"Izaque": '{}: "{}."',
		"Nodus": "{}: //{}.",
		"Ted": "{}: ~{}.",
		}

		self.finish_texts = [
		"f",
		"finish",
		"t",
		"terminar",
		"c",
		"completar",
		"acabar",
		]
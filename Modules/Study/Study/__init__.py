# Study.py

from Script_Helper import *

class Study(object):
	def __init__(self, parameter_switches = None):
		# Verbose variable
		self.verbose = False

		self.testing_script = True

		self.parameter_switches = parameter_switches

		self.Define_Basic_Variables()
		self.Define_Folders()
		self.Define_Lists()
		self.Define_Texts()

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

	def Define_Folders(self):
		name = __name__

		if "." in __name__:
			name = __name__.split(".")[0]

		self.module_text_files_folder = script_text_files_folder + name + "/"
		Create_Folder(self.module_text_files_folder, self.global_switches)

		self.study_network_folder = networks_folder + "Study Network/"
		Create_Folder(self.study_network_folder, self.global_switches)

		self.database_folder = self.study_network_folder + "Database/"
		Create_Folder(self.database_folder, self.global_switches)

		self.database_file_names = [
		"Courses",
		]

		self.database_files = {}

		for file_name in self.database_file_names:
			self.database_files[file_name] = self.database_folder + file_name + self.dot_text
			Create_Text_File(self.database_files[file_name], self.global_switches)

	def Define_Lists(self):
		self.course_settings = Make_Setting_Dictionary(self.database_files["Courses"], read_file = True)

		self.courses = []
		self.course_data_list = {}

		self.parameter_names = [
		"Programming Language",
		"Mode Number",
		"Helper",
		]

		for key in list(self.course_settings.keys()):
			self.courses.append(key)

			self.course_data_list[key] = {}

			i = 0
			for parameter in self.parameter_names:
				self.course_data_list[key][parameter] = self.course_settings[key].split(", ")[i]

				i += 1

	def Define_Texts(self):
		self.language_module_texts = {}
		self.language_module_texts[full_language_en] = {}
		self.language_module_texts[full_language_pt] = {}

		self.language_module_texts[full_language_en]["Select one course"] = "Select one course to study"
		self.language_module_texts[full_language_pt]["Select one course"] = "Selecione um curso para estudar"

		self.module_texts = self.language_module_texts[Language_Item_Definer(full_language_en, full_language_pt)]
# Tasks.py

from Script_Helper import *

class Tasks(object):
	def __init__(self, parameter_switches = None):
		# Verbose variable
		self.verbose = False

		self.testing_script = False

		self.parameter_switches = parameter_switches

		self.Define_Basic_Variables()
		self.Define_Texts()
		self.Define_Folders()

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
		self.media_type_separator = " - "
		self.media_info_setting_separator = ": "

	def Define_Texts(self):
		self.english_task_text = "Task"
		self.portuguese_task_text = "Tarefa"
		self.task_text = Language_Item_Definer(self.english_task_text, self.portuguese_task_text)

		self.english_tasks_text = self.english_task_text + "s"
		self.portuguese_tasks_text = self.portuguese_task_text + "s"
		self.tasks_text = Language_Item_Definer(self.english_tasks_text, self.portuguese_tasks_text)

		self.number_english_text = "Number"
		self.number_portuguese_text = "Número"
		self.number_text = Language_Item_Definer(self.number_english_text, self.number_portuguese_text)
		self.numbers_english_text = self.number_english_text + "s"
		self.numbers_portuguese_text = self.number_english_text + "s"

		self.per_media_type_english_text = "Per Media Type"
		self.folders_english_text = "Folders"
		self.files_english_text = "Files"
		self.times_english_text = "Times"

		self.experienced_texts = [
		self.english_tasks_text,
		"Task Types",
		self.times_english_text,
		self.number_english_text,
		]

	def Define_Folders(self):
		self.media_network_folder = networks_folder + "Productive Network/"
		self.media_network_data_folder = self.media_network_folder + "Media Network Data/"

		self.media_network_parameters_file = self.media_network_data_folder + "Parameters" + self.dot_text
		self.media_network_parameters = Make_Setting_Dictionary(Create_Array_Of_File(self.media_network_parameters_file), self.media_info_setting_separator)
		self.item_type = self.media_network_parameters["Type"]
		self.past_action = self.media_network_parameters["Past Action"]

		self.media_types_file = self.media_network_data_folder + self.item_type + " Types" + self.dot_text
		self.media_types = Create_Array_Of_File(self.media_types_file)

		self.language_media_types = []

		for media_type in self.media_types:
			if " - " in media_type:
				media_type = media_type.split(" - ")[Language_Item_Definer(0, 1)]

			self.language_media_types.append(media_type)

		self.media_info_folder = self.media_network_folder + self.item_type + " Info/"

		self.media_history_name = self.item_type + " History"
		self.media_history_folder = self.media_network_folder + self.media_history_name + "/"
		self.media_history_experienced_folder = self.media_history_folder + self.past_action + "/"

		self.current_year_experienced_media_folder = self.media_history_experienced_folder + current_year + "/"
		Create_Folder(self.current_year_experienced_media_folder, self.global_switches)

		self.total_experienced_number_current_year_file = self.current_year_experienced_media_folder + self.number_english_text + self.dot_text

		if is_a_file(self.total_experienced_number_current_year_file) == False:
			Write_To_File(self.total_experienced_number_current_year_file, "0", self.global_switches)

		self.all_experienced_files_current_year_folder = self.current_year_experienced_media_folder + "All {} Files".format(self.past_action) + "/"
		Create_Folder(self.all_experienced_files_current_year_folder, self.global_switches)

		# Task files array creator
		self.experienced_files = {}
		For_Append_With_Key(self.experienced_texts, self.experienced_files, value_string = self.current_year_experienced_media_folder + "{}" + self.dot_text)

		for file in list(self.experienced_files.values()):
			Create_Text_File(file)

		self.per_media_type_current_year_folder = self.current_year_experienced_media_folder + self.per_media_type_english_text + "/"
		self.per_media_type_files_folder = self.per_media_type_current_year_folder + self.files_english_text + "/"
		self.per_media_type_folders_folder = self.per_media_type_current_year_folder + self.folders_english_text + "/"

		Create_Folder(self.per_media_type_current_year_folder, self.global_switches)
		Create_Folder(self.per_media_type_files_folder, self.global_switches)
		Create_Folder(self.per_media_type_folders_folder, self.global_switches)

		# Per Media Type folder folders dictionary
		self.per_media_type_folder_folders_dict = {}

		for media_type in self.media_types:
			self.per_media_type_folder_folders_dict[media_type] = self.per_media_type_folders_folder + media_type + "/"
			Create_Folder(self.per_media_type_folder_folders_dict[media_type], self.global_switches)

		# Per Media Type files folder dictionary
		self.per_media_type_files_folders = {}

		for media_type in self.media_types:
			self.per_media_type_files_folders[media_type] = self.per_media_type_files_folder + media_type + "/"
			Create_Folder(self.per_media_type_files_folders[media_type], self.global_switches)

		# Per Media Type task files
		self.per_media_type_task_files = {}

		for media_type in self.media_types:
			self.per_media_type_task_files[media_type] = self.per_media_type_files_folders[media_type] + "Tasks" + self.dot_text
			Create_Text_File(self.per_media_type_task_files[media_type], self.global_switches)

		# Per Media Type time files
		self.per_media_type_time_files = {}

		for media_type in self.media_types:
			self.per_media_type_time_files[media_type] = self.per_media_type_files_folders[media_type] + "Times" + self.dot_text
			Create_Text_File(self.per_media_type_time_files[media_type], self.global_switches)

		# Per Media Type number files
		self.per_media_type_number_files = {}

		for media_type in self.media_types:
			self.per_media_type_number_files[media_type] = self.per_media_type_files_folders[media_type] + "Number" + self.dot_text

			if is_a_file(self.per_media_type_number_files[media_type]) == False:
				Write_To_File(self.per_media_type_number_files[media_type], "0", self.global_switches)
# Code.py

from Script_Helper import *

class Code(object):
	def __init__(self, parameter_switches = None):
		# Verbose variable
		self.verbose = False

		self.testing_script = False

		self.parameter_switches = parameter_switches

		self.Define_Basic_Variables()

		self.Define_Texts()
		self.Define_Folders()
		self.Define_Lists()

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

	def Define_Texts(self):
		the_tool_text = Language_Item_Definer("the programming tool", "a ferramenta de programação")

		self.texts_dictionary = {}
		self.texts_dictionary["Opening tool format text"] = Language_Item_Definer("Opening ", "Abrindo ") + the_tool_text + ' \"{}\"...'
		self.texts_dictionary["Closing tool format text"] = Language_Item_Definer("Closing ", "Fechando ") + the_tool_text + ' \"{}\"...'
		self.texts_dictionary["Executed first function, exit"] = Language_Item_Definer("First function executed, open the script again to select another function", "Primeira função executada, abra o script novamente para selecionar outra função") + "."

		self.large_bar = "-----"

		self.code_footer = "\n" + self.large_bar + "\n"

	def Define_Folders(self):
		name = __name__

		if "." in __name__:
			name = __name__.split(".")[0]

		self.module_text_files_folder = script_text_files_folder + name + "/"
		Create_Folder(self.module_text_files_folder, self.global_switches)

		self.programming_network_folder = networks_folder + "Programming Network/"
		Create_Folder(self.programming_network_folder, self.global_switches)

		self.database_folder = self.programming_network_folder + "Database/"
		Create_Folder(self.database_folder, self.global_switches)

		self.database_file_names = [
		"Programming Languages",
		]

		self.database_files = {}

		for file_name in self.database_file_names:
			self.database_files[file_name] = self.database_folder + file_name + self.dot_text
			Create_Text_File(self.database_files[file_name], self.global_switches)

	def Define_Lists(self):
		self.programming_languages = Create_Array_Of_File(self.database_files["Programming Languages"])

		self.programming_language_folders = {}

		for programming_language in self.programming_languages:
			self.programming_language_folders[programming_language] = self.database_folder + programming_language + "/"
			Create_Folder(self.programming_language_folders[programming_language], self.global_switches)

		self.basic_functions = {
			"Open_File": Open_File,
			"Open_Link": Open_Link,
			"Close_Program": Close_Program,
		}

		self.programming_mode_item_names = [
		"Tools",
		"Custom Tools",
		"First Function",
		"Final Function",
		"Setting File",
		]

		self.programming_mode_setting_names = []

		for item_name in self.programming_mode_item_names:
			self.programming_mode_setting_names.append("Has " + item_name)

		self.programming_language_setting_names = []

		for item_name in self.programming_mode_item_names:
			self.programming_language_setting_names.append("Has " + item_name)

		self.programming_language_setting_names.append("Has Modes")

		self.language_name_texts = [
		"English Name",
		"Portuguese Name"
		]

		self.tool_sub_names = [
		"Programs To Close",
		"Function",
		"Close Tool",
		]
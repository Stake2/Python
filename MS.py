# Module_Selector.py

from Global_Switches import Global_Switches as Global_Switches

from Language import Language as Language
from File import File as File
from Folder import Folder as Folder
from Input import Input as Input
from Text import Text as Text

import importlib
import argparse
import inspect

class Main():
	def __init__(self):
		self.Define_Basic_Variables()
		self.Define_Module_Folder()
		self.Define_Texts()

		self.parser = argparse.ArgumentParser()
		self.parser.add_argument("-testing", "--testing", action="store_true", help="Activates the testing mode of modules")
		self.parser.add_argument("-verbose", "--verbose", action="store_true", help="Activates the verbose mode of modules")
		self.parser.add_argument("-user_information", "--user-information", "-userinformation", action="store_true", help="Activates the showing of user information on the Language class")

		self.Get_Modules()
		self.Check_Arguments_And_Switches()

		if self.has_arguments == False:
			self.Select_Module()

		if self.has_arguments == True:
			self.Check_Arguments()

		self.Switch()
		self.Run_Module(self.module)
		self.Reset_Switch()

	def Define_Basic_Variables(self):
		self.Global_Switches = Global_Switches()

		self.global_switches = self.Global_Switches.global_switches
		self.switches_file = self.Global_Switches.switches_file
		self.switches = ["testing", "verbose", "user_information"]

		self.Language = Language(self.global_switches)
		self.File = File(self.global_switches)
		self.Folder = Folder(self.global_switches)
		self.Input = Input(self.global_switches)
		self.Text = Text(self.global_switches)

		self.folders = self.Folder.folders
		self.root_folders = self.folders["root"]
		self.user_folders = self.folders["user"]
		self.apps_folders = self.folders["apps"]
		self.mega_folders = self.folders["mega"]
		self.notepad_folders = self.folders["notepad"]

	def Define_Module_Folder(self):
		self.module_name = self.__module__

		if "." in self.module_name:
			self.module_name = self.module_name.split(".")[0]

		if __name__ == "__main__":
			self.module_name = "Module_Selector"

		self.module_name_lower = self.module_name.lower()

		self.apps_folders["app_text_files"][self.module_name_lower] = {
			"root": self.apps_folders["app_text_files"]["root"] + self.module_name + "/",
		}

		self.Folder.Create(self.apps_folders["app_text_files"][self.module_name_lower]["root"])

		self.apps_folders["app_text_files"][self.module_name_lower]["texts"] = self.apps_folders["app_text_files"][self.module_name_lower]["root"] + "Texts.json"
		self.File.Create(self.apps_folders["app_text_files"][self.module_name_lower]["texts"])

	def Define_Texts(self):
		self.texts = self.Language.JSON_To_Python(self.apps_folders["app_text_files"][self.module_name_lower]["texts"])

		self.language_texts = self.Language.Item(self.texts)

		self.large_bar = "-----"
		self.dash_space = "-"

	def Get_Modules(self):
		self.modules = self.File.Contents(self.apps_folders["modules"]["usage_modules"])["lines"]

		self.test_modules = True

		for module_name in self.modules:
			module_name_lower = module_name.lower()

			# Import module to test for and syntax errors
			if self.test_modules == True:
				module = importlib.import_module(module_name)

			self.parser.add_argument("-" + module_name_lower, "--" + module_name_lower, action="store_true", help='Runs the "' + module_name + '" module')

	def Check_Arguments_And_Switches(self):
		self.arguments = self.parser.parse_args()

		self.has_arguments = False

		for argument, state in inspect.getmembers(self.arguments):
			if argument not in self.switches and state == True:
				self.has_arguments = True

		self.has_switches = False

		for switch in self.switches:
			if hasattr(self.arguments, switch) and getattr(self.arguments, switch) == True:
				self.has_switches = True

	def Select_Module(self):
		show_text = self.language_texts["modules, title()"]
		select_text = self.language_texts["select_a_module_from_the_list"]

		self.module = self.Input.Select(self.modules, show_text = show_text, select_text = select_text)["option"]

	def Check_Arguments(self):
		for module in self.modules:
			module_lower = module.lower()

			if hasattr(self.arguments, module_lower) and getattr(self.arguments, module_lower) == True:
				self.module = module

	def Switch(self):
		self.reset_dictionary = {
			"testing": False,
			"verbose": False,
			"user_information": False,
		}

		# Update Switches file if there are Switch arguments
		if self.has_switches == True:
			self.arguments_dictionary = self.Language.JSON_To_Python(self.switches_file)

			for switch in self.switches:
				if hasattr(self.arguments, switch) and getattr(self.arguments, switch) == True:
					self.arguments_dictionary[switch] = getattr(self.arguments, switch)

			# Update Switches file
			from File import File as File

			self.File = File(self.reset_dictionary)

			# Edit Switches.txt file
			self.File.Edit(self.switches_file, self.Language.Python_To_JSON(self.arguments_dictionary), "w")

			# Show Global Switches
			self.File.Language.Show_Global_Switches(self.arguments_dictionary, show_ending = True)

		# Reset Switches file if no Switch argument is present
		if self.has_switches == False:	
			from File import File as File
			from Text import Text as Text

			self.File = File(self.reset_dictionary)
			self.Text = Text(self.reset_dictionary)

			# Reset
			self.File.Edit(self.switches_file, self.Language.Python_To_JSON(self.reset_dictionary), "w")

	def Run_Module(self, module_name):
		self.module = importlib.import_module(self.module)

		self.module.Run()

	def Reset_Switch(self):
		# Update switches file with the state of the switches before execution of modules
		from File import File as File

		self.dictionary = {
			"testing": False,
			"verbose": False,
			"user_information": False,
		}

		self.File = File(self.dictionary)

		self.File.Edit(self.switches_file, self.Language.Python_To_JSON(self.dictionary), "w")

if __name__ == "__main__":
	Main()
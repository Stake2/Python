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

		self.Define_Parser()
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

		self.reset_switches = {
			"testing": False,
			"verbose": False,
			"user_information": False,
		}

		self.switches_file = self.Global_Switches.switches_file
		self.switches = ["testing", "verbose", "user_information"]

		self.Language = Language(self.reset_switches)
		self.File = File(self.reset_switches)
		self.Folder = Folder(self.reset_switches)
		self.Input = Input(self.reset_switches)
		self.Text = Text(self.reset_switches)

		self.app_settings = self.Language.app_settings
		self.languages = self.Language.languages
		self.small_languages = self.languages["small"]
		self.full_languages = self.languages["full"]
		self.translated_languages = self.languages["full_translated"]

		self.user_language = self.Language.user_language
		self.full_user_language = self.Language.full_user_language

		self.folders = self.Folder.folders
		self.root_folders = self.folders["root"]
		self.user_folders = self.folders["user"]
		self.apps_folders = self.folders["apps"]
		self.mega_folders = self.folders["mega"]
		self.notepad_folders = self.folders["notepad"]

	def Define_Module_Folder(self):
		self.module = {
			"name": self.__module__,
		}

		if __name__ == "__main__":
			self.module["name"] = "Module_Selector"

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

	def Define_Parser(self):
		# Define prefix
		self.argparse = {
			"prefix": "-",
			"ArgumentParser": {
				"prog": self.module["name"] + ".py",
				"description": self.language_texts["description_executes_the_module_specified_in_the_optional_arguments"],
				"epilog": self.language_texts["epilogue_and_that_is_how_you_execute_a_module_using_the_{}"].format(self.module["name"]),
				"formatter_class": argparse.RawDescriptionHelpFormatter,
				"add_help": False,
			},
			"default_arguments": {
				"help": {
					"list": ["help"],
					"text_key": "shows_this_help_text_and_ends_the_program_execution",
					"action": "help",
				},
				"testing": ["testing"],
				"verbose": ["verbose"],
				"user_information": {
					"list": ["user_information", "userinfo", "user"],
					"text_key": "activates_the_displaying_of_user_information_on_the_language_class",
				},
			},
			"default_options": {
				"action": "store_true",
				"help": self.language_texts["activates_the_{}_mode_of_the_modules"],
			}
		}

		self.parser = argparse.ArgumentParser(**self.argparse["ArgumentParser"])

		self.Add_Argument(self.argparse["default_arguments"], self.argparse["default_options"])

	def Add_Argument(self, dictionary, options):
		# Add arguments to ArgumentParser
		keys = list(dictionary.keys())

		for key in keys:
			dict_ = options.copy()

			# Get list of arguments
			if type(dictionary[key]) != dict:
				dict_["list"] = dictionary[key]

				dict_["help"] = dict_["help"].format(self.language_texts[key + ", title()"])

			if type(dictionary[key]) == dict:
				argument_dictionary = dictionary[key]

				if "text" not in argument_dictionary:
					dict_["help"] = self.language_texts[argument_dictionary["text_key"]]

				if "text" in argument_dictionary:
					dict_["help"] = argument_dictionary["text"]

				if "action" in argument_dictionary:
					dict_["action"] = argument_dictionary["action"]

				dict_["list"] = argument_dictionary["list"]

				if "{}" in dict_["help"]:
					dict_["help"] = dict_["help"].format(argument_dictionary["name"])

			# Add arguments per language
			if len(keys) > 1:
				for language in self.small_languages:
					if language != "en":
						if key in self.texts:
							text = self.texts[key]

						if key + ", title()" in self.texts:
							text = self.texts[key + ", title()"]

						text = text[language].lower()

						if text not in dict_["list"]:
							dict_["list"].append(text.replace(" ", ""))

							if text.split(" ")[0] != text:
								dict_["list"].append(text.split(" ")[0])

			i = 0
			for item in dict_["list"]:
				dict_["list"][i] = self.argparse["prefix"] + dict_["list"][i]

				i += 1

			tuple_ = tuple(dict_["list"])

			dict_.pop("list")

			self.parser.add_argument(*tuple_, **dict_)

	def Get_Modules(self):
		self.modules = self.File.Contents(self.apps_folders["modules"]["usage_modules"])["lines"]

		self.test_modules = True

		for module_name in self.modules:
			module = {
				"name": module_name,
				"key": module_name.lower(),
				"module": importlib.import_module(module_name),
			}

			module.update({
				"dictionary": {
					module["name"]: {
						"name": module["name"],
						"list": [module["key"]],
						"text_key": "executes_the_{}_module"
					}
				}
			})

			# Add custom argument names from module
			if hasattr(module["module"], "arguments") == True and type(module["module"].arguments) == list:
				arguments = module["module"].arguments

				for argument in arguments:
					module["dictionary"][module["name"]]["list"].append(argument)

			self.Add_Argument(module["dictionary"], self.argparse["default_options"])

			# Add additional arguments from module
			if hasattr(module["module"], "arguments") == True and type(module["module"].arguments) == dict:
				arguments = module["module"].arguments

				for key in arguments:
					dict_ = arguments[key]

					dictionary = {
						key: {
							"list": [key],
							"text": dict_["text"]
						}
					}

					if "{module}" in dictionary[key]["text"]:
						dictionary[key]["text"] = dictionary[key]["text"].replace("{module}", '"' + module["name"] + '"')

					self.Add_Argument(dictionary, self.argparse["default_options"])

		# Add "Language" module argument
		dictionary = {
			"Language": {
				"list": ["language"],
				"text": "Language"
			}
		}

		self.Add_Argument(dictionary, self.argparse["default_options"])

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

		option = self.Input.Select(self.modules, show_text = show_text, select_text = select_text)["option"]

		self.module = {
			"name": option,
			"key": option.lower()
		}

	def Check_Arguments(self):
		for module in self.modules:
			module_lower = module.lower()

			if hasattr(self.arguments, module_lower) and getattr(self.arguments, module_lower) == True:
				self.module = {
					"name": module,
					"key": module.lower(),
				}

	def Switch(self):
		# Update Switches file if there are Switch arguments
		if self.has_switches == True:
			self.arguments_dictionary = self.reset_switches.copy()

			for switch in self.switches:
				if hasattr(self.arguments, switch) and getattr(self.arguments, switch) == True:
					self.arguments_dictionary[switch] = getattr(self.arguments, switch)	

			# Define File module to show Global Switches
			self.File = File(self.arguments_dictionary, show_global_switches = True)

			# Define File module again to be able to write the new switches
			self.File = File(self.reset_switches)

			# Edit Switches.txt file
			self.File.Edit(self.switches_file, self.Language.Python_To_JSON(self.arguments_dictionary), "w")

		# Reset Switches file if no Switch argument is present
		if self.has_switches == False:	
			self.File.Edit(self.switches_file, self.Language.Python_To_JSON(self.reset_switches), "w")

	def Run_Module(self, module):
		if module["name"] != "Module_Selector":
			self.module = importlib.import_module(module["name"])

			if getattr(self.arguments, "check") == False and getattr(self.arguments, "set") == False or getattr(self.arguments, "set") == True:
				self.module.Run()

			if getattr(self.arguments, "check") == True:
				self.module.Run(register_time = False)

		if getattr(self.arguments, "language") == True:
			self.Language.Create_Language_Text()

	def Reset_Switch(self):
		# Update switches file with the state of the switches before execution of modules
		self.File = File(self.reset_switches)

		self.File.Edit(self.switches_file, self.Language.Python_To_JSON(self.reset_switches), "w")

if __name__ == "__main__":
	Main()
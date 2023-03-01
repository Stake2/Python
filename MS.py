# Module_Selector.py

import importlib
import argparse
import inspect

class Module_Selector():
	def __init__(self):
		self.Define_Basic_Variables()

		from Utility.Define_Folders import Define_Folders as Define_Folders

		Define_Folders(self)

		self.Define_Texts()

		self.Define_Parser()
		self.Get_Modules()
		self.Check_Arguments_And_Switches()
		self.Reset_Switch()

		if self.has_arguments == False:
			self.Select_Module()

		if self.has_arguments == True:
			self.Check_Arguments()

		self.Switch()
		self.Run_Module(self.module)
		self.Reset_Switch()

	def Define_Basic_Variables(self):
		from Utility.Global_Switches import Global_Switches as Global_Switches

		self.Global_Switches = Global_Switches()
		self.switches = self.Global_Switches.switches

		self.reset_switches = {
			"testing": False,
			"verbose": False,
			"user_information": False,
		}

		from Utility.Input import Input as Input
		from Utility.JSON import JSON as JSON

		self.Input = Input()
		self.JSON = JSON()
		self.Language = self.JSON.Language

		self.languages = self.Language.languages
		self.user_language = self.Language.user_language

	def Define_Texts(self):
		self.texts = self.JSON.To_Python(self.folders["apps"]["module_files"][self.module["key"]]["texts"])

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
				"add_help": False
			},
			"default_arguments": {
				"help": {
					"list": ["help"],
					"text_key": "shows_this_help_text_and_ends_the_program_execution",
					"action": "help"
				},
				"testing": ["testing"],
				"verbose": ["verbose"],
				"user_information": {
					"list": ["user_information", "userinfo", "user"],
					"text_key": "activates_the_displaying_of_user_information_on_the_language_class"
				},
				"module": {
					"list": ["module"],
					"text_key": "stores_the_module_to_be_executed",
					"options": {
						"action": "store",
						"help": self.language_texts["stores_the_module_to_be_executed"]
					},
					"language_text": False
				}
			},
			"default_options": {
				"action": "store_true",
				"help": self.language_texts["activates_the_{}_mode_of_the_modules"],
			}
		}

		self.parser = argparse.ArgumentParser(**self.argparse["ArgumentParser"])

		for argument in self.argparse["default_arguments"].values():
			options = self.argparse["default_options"]

			if "options" in argument:
				options = argument["options"]

			self.Add_Argument(argument, options)

	def Add_Argument(self, argument, options):
		options = options.copy()

		if type(argument) == list:
			argument = argument[0]

			options.update({
				"list": [argument],
				"help": options["help"].format(self.language_texts[argument + ", title()"])
			})

		if type(argument) not in [list, str]:
			if "text" not in argument:
				options["help"] = self.language_texts[argument["text_key"]]

			if "text" in argument:
				options["help"] = argument["text"]

			if "action" in argument:
				options["action"] = argument["action"]

			options["list"] = argument["list"]

			if "{}" in options["help"]:
				options["help"] = options["help"].format(argument["title"])

			if "language_text" in argument:
				options["language_text"] = argument["language_text"]

		if type(argument) == dict:
			argument = argument["list"][0]

		# Add arguments per language
		for language in self.languages["small"]:
			if language != "en":
				text = argument

				if argument in self.texts:
					text = self.texts[argument]

				if argument + ", title()" in self.texts:
					text = self.texts[argument + ", title()"]

				if type(text) == dict:
					if language in text:
						text = text[language].lower()

					else:
						text = text[self.user_language].lower()

				if text not in options["list"] and "language_text" not in options:
					options["list"].append(text.replace(" ", ""))

					if text.split(" ")[0] != text:
						options["list"].append(text.split(" ")[0])

		# Add prefix to options
		i = 0
		for item in options["list"]:
			options["list"][i] = self.argparse["prefix"] + options["list"][i]

			i += 1

		# Transform list of arguments into a tuple
		tuple_ = tuple(options["list"])

		# Remove list from options dictionary
		options.pop("list")

		if "language_text" in options:
			options.pop("language_text")

		self.parser.add_argument(*tuple_, **options)

	def Get_Modules(self):
		self.modules = self.JSON.To_Python(self.folders["apps"]["modules"]["modules"])

		# Iterate through usage modules list
		for title in self.modules["usage"]["list"]:
			self.modules["usage"][title] = {
				"title": title,
				"key": title.lower(),
				"list": [title.lower()],
				"text_key": "executes_the_{}_module",
				"module": importlib.import_module(title)
			}

			# Add custom argument names from module
			if hasattr(self.modules["usage"][title]["module"], "arguments") == True and type(self.modules["usage"][title]["module"].arguments) == list:
				arguments = self.modules["usage"][title]["module"].arguments

				for argument in arguments:
					self.modules["usage"][title]["list"].append(argument)

			self.Add_Argument(self.modules["usage"][title], self.argparse["default_options"])

			# Add separate arguments from module
			if hasattr(self.modules["usage"][title]["module"], "separate_arguments") == True:
				separate_arguments = self.modules["usage"][title]["module"].separate_arguments

				for key in separate_arguments:
					dictionary = {
						"list": [key],
						"text": self.language_texts[self.modules["usage"][title]["key"] + "." + key]
					}

					if "{module}" in dictionary["text"]:
						dictionary["text"] = dictionary["text"].replace("{module}", '"' + self.modules["usage"][title]["title"] + '"')

					self.Add_Argument(dictionary, self.argparse["default_options"])

		# Add "Language" module argument
		dictionary = {
			"title": "Language",
			"list": ["language"],
			"text_key": "executes_the_{}_module"
		}

		self.texts["language, title()"] = self.Language.texts["language, title()"]

		self.Add_Argument(dictionary, self.argparse["default_options"])

	def Check_Arguments_And_Switches(self):
		self.arguments = self.parser.parse_args()

		self.has_arguments = False

		for argument, state in inspect.getmembers(self.arguments):
			if argument not in list(self.switches["reset"].keys()):
				if state == True or argument == "module" and state != None:
					self.has_arguments = True

		self.has_switches = False

		for switch in list(self.switches["reset"].keys()):
			if hasattr(self.arguments, switch) and getattr(self.arguments, switch) == True:
				self.has_switches = True

	def Select_Module(self):
		show_text = self.language_texts["modules, title()"]
		select_text = self.language_texts["select_a_module_from_the_list"]

		option = self.Input.Select(self.modules["usage"]["list"], show_text = show_text, select_text = select_text)["option"]

		self.Define_Module(option)

	def Check_Arguments(self):
		for module in self.modules["usage"]["list"]:
			module_lower = module.lower()

			possible_options = [
				module,
				module.lower(),
				module.upper(),
				module.title(),
				module.capitalize(),
				module.replace("_", " ").lower(),
				module.replace("_", " ").upper(),
				module.replace("_", " ").title(),
				module.replace("_", " ").capitalize()
			]

			if (
				hasattr(self.arguments, module_lower) and getattr(self.arguments, module_lower) == True or
				hasattr(self.arguments, "module") and getattr(self.arguments, "module") in possible_options
			):
				self.Define_Module(module)

	def Define_Module(self, option):
		self.module = {
			"title": option,
			"key": option.lower(),
			"module": self.modules["usage"][option]["module"]
		}

	def Switch(self):
		# Update Switches file if there are Switch arguments
		if self.has_switches == True:
			self.switches["edited"] = self.switches["reset"].copy()

			for switch in self.switches["global"].keys():
				if hasattr(self.arguments, switch) and getattr(self.arguments, switch) == True:
					self.switches["edited"][switch] = getattr(self.arguments, switch)	

			# Show global switches
			self.Show_Global_Switches()

			if self.switches["edited"]["user_information"] == True:
				self.Language.Show_User_Information()

			# Edit Switches.json file
			self.Global_Switches.Switch(self.switches["edited"])

	def Show_Global_Switches(self):
		has_true_variables = False

		for switch in self.switches["global"].keys():
			if switch in self.switches["edited"] and self.switches["edited"][switch] == True:
				has_true_variables = True

		if has_true_variables == True:
			print()
			print("-----")
			print()

		for switch in self.switches["global"].keys():
			if switch in self.switches["edited"] and self.switches["edited"][switch] == True and switch != "user_information":
				print(self.language_texts[switch + ", type: explanation"])

		if has_true_variables == True and self.switches["edited"]["user_information"] == False:
			print()
			print("-----")

	def Run_Module(self, module):
		if "title" in module and module["title"] != "Module_Selector":
			if module["title"] == "Food_Time" and getattr(self.arguments, "check") == True:
				setattr(self.module["module"].Run, "register_time", False)

			self.module["module"].Run()

		if getattr(self.arguments, "language") == True:
			self.Language.Create_Language_Text()

	def Reset_Switch(self):
		self.Global_Switches.Reset()

if __name__ == "__main__":
	Module_Selector()
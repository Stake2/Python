# Module_Selector.py

import argparse
import inspect

class Main():
	def __init__(self):
		self.Import_Modules()
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

	def Import_Modules(self):
		from Utility.Modules.Set import Set as Modules

		self.Modules = Modules()

		self.modules = self.Modules.Set(self, utility_modules = ["Folder", "Language", "JSON"])

	def Define_Module_Folder(self):
		self.module = {
			"name": self.__module__,
		}

		if __name__ == "__main__":
			self.module["name"] = "Module_Selector"

		if "." in self.module["name"]:
			self.module["name"] = self.module["name"].split(".")[0]

		self.module["key"] = self.module["name"].lower()

		self.folders["apps"]["modules"][self.module["key"]] = {
			"root": self.folders["apps"]["modules"]["root"] + self.module["name"] + "/",
		}

		self.folders["apps"]["module_files"][self.module["key"]] = {
			"root": self.folders["apps"]["module_files"]["root"] + self.module["name"] + "/",
		}

		for item in ["module_files", "modules"]:
			self.folders["apps"][item][self.module["key"]] = self.folders["apps"][item]["root"] + self.module["name"] + "/"
			self.folders["apps"][item][self.module["key"]] = self.Folder.Contents(self.folders["apps"][item][self.module["key"]], lower_key = True)["dictionary"]

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
				}
			},
			"default_options": {
				"action": "store_true",
				"help": self.language_texts["activates_the_{}_mode_of_the_modules"],
			}
		}

		self.parser = argparse.ArgumentParser(**self.argparse["ArgumentParser"])

		for argument in self.argparse["default_arguments"].values():
			self.Add_Argument(argument, self.argparse["default_options"])

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
					text = text[language].lower()

				if text not in options["list"]:
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

		self.parser.add_argument(*tuple_, **options)

	def Get_Modules(self):
		# Iterate through usage modules list
		for module in self.modules["usage"]["list"]:
			module = self.modules["usage"][module]

			# Add custom argument names from module
			if hasattr(module["module"], "arguments") == True and type(module["module"].arguments) == list:
				arguments = module["module"].arguments

				for argument in arguments:
					module["list"].append(argument)

			self.Add_Argument(module, self.argparse["default_options"])

			# Add separate arguments from module
			if hasattr(module["module"], "separate_arguments") == True:
				separate_arguments = module["module"].separate_arguments

				for key in separate_arguments:
					dictionary = {
						"list": [key],
						"text": self.language_texts[module["key"] + "." + key]
					}

					if "{module}" in dictionary["text"]:
						dictionary["text"] = dictionary["text"].replace("{module}", '"' + module["title"] + '"')

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
			if argument not in list(self.switches["reset"].keys()) and state == True:
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

			if hasattr(self.arguments, module_lower) and getattr(self.arguments, module_lower) == True:
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
		if module["title"] != "Module_Selector":
			setattr(self.module["module"].Run, "Modules", self.Modules)

			if getattr(self.arguments, "check") == False:
				self.module["module"].Run()

			if getattr(self.arguments, "check") == True:
				self.module["module"].Run(register_time = False)

		if getattr(self.arguments, "language") == True:
			self.Language.Create_Language_Text()

	def Reset_Switch(self):
		self.Global_Switches.Reset()

if __name__ == "__main__":
	Main()
# Module_Selector.py

import importlib
import inspect

# Import the "deepcopy" module
from copy import deepcopy

class Module_Selector():
	def __init__(self):
		# Import the classes
		self.Import_Classes()

		# Define the folders of the module
		self.Define_Folders(object = self)

		# Defines the basic variables
		self.Define_Basic_Variables()

		# Define the texts of the module
		self.Define_Texts()

		# Define the parser
		self.Define_Parser()

		# Reset the switches
		self.Reset_Switches()

		# Get the modules
		self.Get_Modules()

		# Check the arguments and switches
		self.Check_Arguments_And_Switches()

		# If the class does not has arguments
		if self.has_arguments == False:
			# Ask the user to select a module from the list
			self.Select_Module()

		# If the class has arguments
		if self.has_arguments == True:
			# Check them
			self.Check_Arguments()

		# Switch the switches
		self.Switch()

		# Run the module
		self.Run_Module(self.module)

		# Reset the switches again
		self.Reset_Switches()

	def Import_Classes(self):
		# Define the list of modules to be imported
		modules = [
			"Define_Folders",
			"Global_Switches",
			"Modules",
			"JSON",
			"Input",
			"Folder"
		]

		# Iterate through the list of modules
		for module_title in modules:
			# Import the module
			module = importlib.import_module("." + module_title, "Utility")

			# Get the sub-class
			sub_class = getattr(module, module_title)

			# If the module title is not in the defined list
			if module_title not in ["Define_Folders", "Modules"]:
				# Run the sub-class to define its variable
				sub_class = sub_class()

			# Add the sub-class to the current module
			setattr(self, module_title, sub_class)

		# Define the "Language" class as the same class inside the "JSON" class
		self.Language = self.JSON.Language

		# Define the local "folders" dictionary as the dictionary inside the "Folder" class
		self.folders = self.Folder.folders

	def Define_Basic_Variables(self):
		# Get the "Switches" dictionary
		self.switches = self.Global_Switches.switches

		# Copy the reset switches from the "Global_Switches" module
		self.reset_switches = deepcopy(self.switches["Reset"])

		# Get the languages and the user language from the "Language" class
		self.languages = self.Language.languages
		self.user_language = self.Language.user_language

	def Define_Texts(self):
		# Define the "Texts" dictionary
		self.texts = self.JSON.To_Python(self.module["Files"]["Texts"])

		# Define the "Language texts" dictionary
		self.language_texts = self.Language.Item(self.texts)

		# Define the "Separators" dictionary
		self.separators = {}

		# Create separators from one to ten characters
		for number in range(1, 11):
			# Define the empty string
			string = ""

			# Add separators to it
			while len(string) != number:
				string += "-"

			# Add the string to the Separators dictionary
			self.separators[str(number)] = string

	def Define_Parser(self):
		# Import the "argparse" module
		import argparse

		# Define the "argument_parser" dictionary
		# With the configuration for the ArgumentParser
		# The default arguments, and the default options
		self.argument_parser = {
			"Prefix": "-",
			"ArgumentParser": {
				"prog": self.module["Name"] + ".py",
				"description": self.language_texts["description_executes_the_module_specified_in_the_optional_arguments"],
				"epilog": self.language_texts["epilogue_and_that_is_how_you_execute_a_module_using_the_{}"].format(self.module["Name"]),
				"formatter_class": argparse.RawDescriptionHelpFormatter,
				"add_help": False
			},
			"Default arguments": {
				"help": {
					"List": ["help"],
					"Text key": "shows_this_help_text_and_ends_the_program_execution",
					"Action": "help"
				},
				"testing": [
					"testing",
					"Testing"
				],
				"verbose": [
					"verbose",
					"Verbose"
				],
				"user_information": {
					"List": [
						"user_information",
						"userinfo",
						"user"
					],
					"Text key": "activates_the_displaying_of_user_information_on_the_language_class"
				},
				"module": {
					"List": [
						"module"
					],
					"Text key": "stores_the_module_to_be_executed",
					"Options": {
						"Action": "store",
						"Help": self.language_texts["stores_the_module_to_be_executed"]
					},
					"Language text": False
				},
				"update_modules": {
					"List": [
						"update_modules"
					],
					"Text key": "updates_the_json_file_of_the_modules",
					"Options": {
						"Action": "store_true",
						"Help": self.language_texts["updates_the_json_file_of_the_modules"]
					},
					"Language text": False
				}
			},
			"Default options": {
				"Action": "store_true",
				"Help": self.language_texts["activates_the_{}_mode_of_the_modules"]
			}
		}

		# Initiate the Argument Parser
		self.argument_parser["Parser"] = argparse.ArgumentParser(**self.argument_parser["ArgumentParser"])

		# Iterate through the default arguments list
		for argument in self.argument_parser["Default arguments"].values():
			# Get the default options dictionary
			options = self.argument_parser["Default options"]

			# If the argument has a custom options dictionary, use it
			if "Options" in argument:
				options = argument["Options"]

			# Add the argument to the Argument Parser
			self.Add_Argument(argument, options)

	def Add_Argument(self, argument, options):
		# Make a copy of the options dictionary to not modify it
		options = deepcopy(options)

		# If the type of argument is a list
		# That means the argument contains only the key, not any additional info
		if type(argument) == list:
			# Get the argument key
			argument = argument[0]

			# Update the options with the argument key
			# And help text gotten from the Language texts dictionary
			options.update({
				"List": [argument],
				"Help": options["Help"].format(self.language_texts[argument + ", title()"])
			})

		# If the type of argument is a dictionary
		# That means the argument contains the key and additional info about the argument
		# Such as a custom help text, custom action, and language text and key
		if type(argument) == dict:
			# If the "Is module" key is inside the argument
			# And the argument is a module argument (True)
			# Then define its text key as "executes_the_{}_module"
			if (
				"Is module" in argument and
				argument["Is module"] == True
			):
				argument["Text key"] = "executes_the_{}_module"

			# if there is a custom help text of the argument, use it
			if "Text" in argument:
				options["Help"] = argument["Text"]

			# If the "Text key" key is inside the argument
			# Then use the help text from the Language texts dictionary, using the text key
			if "Text key" in argument:
				options["Help"] = self.language_texts[argument["Text key"]]

			# Define the list of keys to get from the argument dictionary
			keys = [
				"Text",
				"Action",
				"List",
				"Language text"
			]

			# If the title is not inside the argument dictionary
			# And the "List" key is inside the dictionary
			# Make a title from the first item on the key list, making the first letter uppercase
			if (
				"Title" not in argument and
				"List" in argument
			):
				argument["Title"] = argument["List"][0].title()

			# If the "List" key is not inside the argument dictionary
			# And the "Title" key is inside the dictionary
			# Make a new list with only the title
			if (
				"List" not in argument and
				"Title" in argument
			):
				argument["List"] = [
					argument["Title"].lower()
				]

			# Iterate through the keys list
			for item in keys:
				# If the item is inside the argument dictionary
				if item in argument:
					# Add it to the options dictionary
					options[item] = argument[item]

			# If the format characters are inside the help text, format them with the argument title
			if "{}" in options["Help"]:
				options["Help"] = options["Help"].format(argument["Title"])

			# Transform the argument into its first key
			# All variables from the argument dictionary have already been added to the options dictionary
			# So it is safe to replace this variable now
			argument = argument["List"][0]

		# Add the arguments per language
		# Not the English language, the other languages such as the user language (when it is not English)
		for language in self.languages["small"]:
			# If the language is not English
			if language != "en":
				# Define the text as the argument
				text = argument

				# If the argument is inside the texts dictionary
				# Get the text from it
				if argument in self.texts:
					text = self.texts[argument]

				# If the argument with the ", title()" text specifier is inside the texts dictionary
				# Get the text from it
				if argument + ", title()" in self.texts:
					text = self.texts[argument + ", title()"]

				# If the type of text (argument) is a dict
				if type(text) == dict:
					# If the language text is inside the text dictionary
					# Get the language text from it
					if language in text:
						text = text[language].lower()

					# Else, define the text as the text in the user language
					else:
						text = text[self.user_language].lower()

				# If the language text is not inside the options key list
				# And "Language text" key is not inside the options dictionary
				if (
					text not in options["List"] and
					"Language text" not in options
				):
					# Add the language text to the options key list
					# And replace the spaces with nothing
					options["List"].append(text.replace(" ", ""))

					# If the first word of the text is not the same text
					# (That means there are spaces on the text, such as a phrase)
					# Then add the first word of the text to the list key
					# (Arguments can not contain spaces)
					if text.split(" ")[0] != text:
						options["List"].append(text.split(" ")[0])

		# Replace each argument key of the list with the same key but with the prefix of the Argument Parser
		i = 0
		for item in options["List"].copy():
			options["List"][i] = self.argument_parser["Prefix"] + options["List"][i]

			i += 1

		# Transform the list of arguments into a tuple
		# To be used correctly by the Argument Parser
		tuple_ = tuple(options["List"])

		# Remove the keys that can not be used by the Parser
		unused_keys = [
			"Language text",
			"List",
			"Text"
		]

		for key in unused_keys:
			if key in options:
				options.pop(key)

		# Transform all keys in the "options" dictionary to lowercase
		# For the parser to have the correct keys
		dict_ = {}

		for key, value in options.items():
			dict_[key.lower()] = value

		options = dict_

		# Add the arguments to the parser, using the tuple of keys
		# And the options, such as action, help, and text
		self.argument_parser["Parser"].add_argument(*tuple_, **options)

	def Get_Modules(self):
		# Get the list of modules from the "Modules.json" file
		self.modules = self.JSON.To_Python(self.folders["Apps"]["Modules"]["Modules"])

		# Iterate through the usage modules list
		for title in self.modules["Usage"]["List"]:
			# Create the module dictionary with all its information
			module = {
				"Key": title.lower(),
				"Title": title,
				"List": [
					title.lower()
				],
				"Module": importlib.import_module(title),
				"Folders": {
					"Texts": {
						"root": self.folders["Apps"]["Module files"]["root"] + title + "/"
					}
				},
				"Is module": True
			}

			# Add the "Modules" to the "Run" class of the current module
			setattr(module["Module"].Run, "Modules", self.Modules)

			# Define the "Texts.json" file of the module
			module["Folders"]["Texts"]["Texts"] = module["Folders"]["Texts"]["root"] + "Texts.json"

			# Add the alternate argument names from the module if they exist
			if (
				hasattr(module["Module"], "alternate_arguments") == True and
				type(module["Module"].alternate_arguments) == list
			):
				# Get the list of alternate arguments
				arguments = module["Module"].alternate_arguments

				# Add them to the arguments list
				for argument in arguments:
					module["List"].append(argument)

			# Add the module argument to the Argument Parser, with the default options (such as action and help text)
			self.Add_Argument(module, self.argument_parser["Default options"])

			# Add the custom arguments from the module if they exist
			if hasattr(module["Module"], "custom_arguments") == True:
				# Get the list of custom arguments
				custom_arguments = module["Module"].custom_arguments

				# Create the key for the custom arguments inside the module dictionary
				module["Custom arguments"] = {}

				# Make the argument keys list
				# (If the custom arguments is a list)
				keys = custom_arguments

				# If the custom arguments variable is a dictionary
				if type(custom_arguments) == dict:
					# Then get the dictionary keys
					keys = custom_arguments.keys()

				# Iterate through the custom arguments keys list
				for key in keys:
					# If the custom arguments variable is a dictionary
					if type(custom_arguments) == dict:
						# Get the argument dictionary from it
						argument = custom_arguments[key]

					# Make an argument dictionary containing the argument key list and text
					dictionary = {
						"Title": title.lower() + "." + key
					}

					# Read the "Texts.json" file of the module to get its texts
					module["Texts"] = self.JSON.To_Python(module["Folders"]["Texts"]["Texts"])

					# Get the text for the custom argument
					dictionary["Text"] = module["Texts"][key][self.user_language]

					# If there is the "{module}" format text on the argument text
					# Replace it with the module title
					if "{module}" in dictionary["Text"]:
						dictionary["Text"] = dictionary["Text"].replace("{module}", '"' + title + '"')

					# If the custom arguments variable is a dictionary
					if type(custom_arguments) == dict:
						# Import each key from the argument dictionary if it is not already present
						for argument_key in argument.keys():
							if argument_key not in dictionary:
								dictionary[argument_key] = argument[argument_key]

					# Add the module argument to the Argument Parser, with the default options (such as action and help text)
					self.Add_Argument(dictionary, self.argument_parser["Default options"])

					# Add the custom argument dictionary to the "custom arguments" dictionary
					module["Custom arguments"][key] = dictionary

				# Remove the Texts dictionary because it will not be used anymore
				module.pop("Texts")

			# Define the module title key in the "Usage" modules dictionary as the local module dictionary
			self.modules["Usage"][title] = module

		# Add the "Language" module argument
		dictionary = {
			"List": [
				"language"
			],
			"Is module": True
		}

		self.texts["language, title()"] = self.Language.texts["language, title()"]

		# Add the module argument to the Argument Parser, with the default options (such as action and help text)
		self.Add_Argument(dictionary, self.argument_parser["Default options"])

	def Check_Arguments_And_Switches(self):
		# Get the arguments dictionary
		self.arguments = self.argument_parser["Parser"].parse_args()

		self.has_arguments = False

		# Iterate through the arguments and states list
		for argument, state in inspect.getmembers(self.arguments):
			# If the argument is not in the switches list
			# Then it must be a module or a custom argument of a module
			if argument not in list(self.switches["Reset"].keys()):
				# If the state of the argument is True
				# Or the argument is the "module" argument
				# And the state is not equal to None
				if (
					state == True or
					argument == "module" and
					state != None
				):
					# Then the Parser contains arguments
					self.has_arguments = True

		self.has_switches = False

		# Iterate through the switches list
		for switch in list(self.switches["Reset"].keys()):
			# Lower the switch
			switch = switch.lower()

			# If the arguments contain the switch and the state of the switch is True
			if (
				hasattr(self.arguments, switch) and
				getattr(self.arguments, switch) == True
			):
				# Then the Parser contains arguments that are also switches
				self.has_switches = True

	def Select_Module(self):
		# Define the show and select textes to select a module
		show_text = self.language_texts["modules, title()"]
		select_text = self.language_texts["select_a_module_from_the_list"]

		# Select the module
		module = self.Input.Select(self.modules["Usage"]["List"], show_text = show_text, select_text = select_text)["option"]

		# Define the dictionary and information of the module
		self.Define_Module(module)

	def Check_Arguments(self):
		# Iterate through the Usage modules list
		for module in self.modules["Usage"]["List"]:
			# Transform the module title into lowercase
			module_lower = module.lower()

			# Make a list of possible options for the module title
			# The user could have written the module title as:
			# "Module_Title" (normal), "module_title" (lower), "Module_title" (capitalize)
			# 
			# Or without an underscore:
			# "Module Title" (normal), "module title" (lower), "Module title" (capitalize)
			possible_options = [
				module,
				module.lower(),
				module.capitalize(),

				module.replace("_", " "),
				module.replace("_", " ").lower(),
				module.replace("_", " ").capitalize()
			]

			# If the arguments contain the lowercase version of the module
			# And the module argument is True
			# That means the user wrote the command as:
			# python MS.py -module_title
			# 
			# Or if the arguments contain the "module" argument
			# And the argument value is inside the possible module title options
			# That means the user wrote the command as:
			# python MS.py -module Module_Title
			# Or any of the other options
			if (
				hasattr(self.arguments, module_lower) and
				getattr(self.arguments, module_lower) == True or
				hasattr(self.arguments, "module") and
				getattr(self.arguments, "module") in possible_options
			):
				# Define the module dictionary and its information
				self.Define_Module(module)

	def Define_Module(self, module):
		# Define the module dictionary with its title, key, and module
		self.module = self.modules["Usage"][module]

	def Switch(self):
		# Update the "Switches.json" file if there are switch arguments
		if self.has_switches == True:
			# Make a copy of the reset (default) switches and add it to the "edited" key
			self.switches["Edited"] = deepcopy(self.switches["Reset"])

			# Iterate through the global switches keys list
			for switch in self.switches["Global"].keys():
				# Define the key
				key = switch

				# Lower the switch
				switch = switch.lower()

				# If the arguments list has the switch
				# And the switch is True
				if (
					hasattr(self.arguments, switch) and
					getattr(self.arguments, switch) == True
				):
					# Update the switch inside the edited switches dictionary
					self.switches["Edited"][key] = getattr(self.arguments, switch)

			# Show the global switches
			self.Show_Global_Switches()

			# If the "User information" switch is on
			# Execute the "Show_User_Information" method of the "Language" class
			if self.switches["Edited"]["User information"] == True:
				self.Language.Show_User_Information()

			# Edit the "Switches.json" file with the updated switches
			self.Global_Switches.Switch(self.switches["Edited"])

	def Show_Global_Switches(self):
		has_true_variables = False

		# Iterate through the global switches keys list
		for switch in self.switches["Global"].keys():
			# If the switch is inside the edited switches dictionary
			# And the switch is True
			if (
				switch in self.switches["Edited"] and
				self.switches["Edited"][switch] == True
			):
				# Then at least one switch is True (activated)
				has_true_variables = True

		# If any switch is True (activated)
		# Then show a first space and dash separator
		if has_true_variables == True:
			print()
			print("-----")
			print()

		# Iterate through the global switches keys list
		for switch in self.switches["Global"].keys():
			# Define the key
			key = switch

			# Lower the switch
			switch = switch.lower()

			# If the switch is inside the edited switches dictionary
			# And the switch is True
			# And the switch is not the "User information" one
			if (
				key in self.switches["Edited"] and
				self.switches["Edited"][key] == True and
				key != "User information"
			):
				# Show the switch explanation text to the user
				print(self.language_texts[switch + ", type: explanation"])

		# If any switch is True (activated)
		# And the "User information" is off
		# Then show a final space and dash separator
		# (If the "User information" switch is on, it provides its own final separator)
		if (
			has_true_variables == True and
			self.switches["Edited"]["User information"] == False
		):
			print()
			print("-----")

	def Run_Module(self, module):
		# If the "Title" key is inside the module dictionary
		# And the module is not the "Module_Selector" one
		if (
			"Title" in module and
			module["Title"] != "Module_Selector"
		):
			# If the module has custom arguments
			if "Custom arguments" in module:
				# Define the "has custom key" switch
				has_custom_key = False

				# Get the custom argument items (keys and values)
				items = deepcopy(module["Custom arguments"]).items()

				# Iterate through the keys and values
				for key, argument in items:
					# If the custom argument is inside the list of arguments
					if hasattr(self.arguments, argument["Title"]) == True:
						# Replace the "Title" key with the "Key" key, having the same value
						key_value = {
							"Key": module["Custom arguments"][key]["Title"]
						}

						module["Custom arguments"][key] = self.JSON.Add_Key_After_Key(module["Custom arguments"][key], key_value, after_key = "Title")

						# Remove the old "Title" key
						module["Custom arguments"][key].pop("Title")

						# Get the value of the custom argument
						# And add it to its dictionary inside the "custom arguments" dictionary
						module["Custom arguments"][key]["Value"] = getattr(self.arguments, argument["Title"])

						# If the argument does not contains a custom (renamed) key
						if "Custom key" not in argument:
							# Make a default custom key with the original key, in title mode
							# Replace underscores with spaces, and remove the module title and the dot
							custom_key = module["Custom arguments"][key]["Key"].replace(module["Key"] + ".", "")
							custom_key = custom_key.title().replace("_", " ")

							argument["Custom key"] = custom_key

						# If the argument contains a custom (renamed) key
						if "Custom key" in argument:
							# Make a disposable dictionary
							if "Disposable dictionary" not in module:
								module["Disposable dictionary"] = {}

							# Get the custom key
							custom_key = argument["Custom key"]

							# Copy the dictionary of the custom argument to the disposable dictionary
							module["Disposable dictionary"][custom_key] = module["Custom arguments"][key]

							# Define the "has_custom_key" switch as True
							if has_custom_key == False:
								has_custom_key = True

				# If any custom argument has a custom key
				if has_custom_key == True:
					# Replace the "custom arguments" dictionary with the disposable one
					# With the renamed/replaced keys
					module["Custom arguments"] = module["Disposable dictionary"]

					# Remove the disposable dictionary from the module dictionary
					module.pop("Disposable dictionary")

				# Add the arguments inside the "Run" class of the module
				setattr(self.module["Module"].Run, "arguments", module["Custom arguments"])

			# Run the selected module
			self.module["Module"].Run()

		# If the "language" argument is present in the arguments list
		# Then run the "Create_Language_Text" method of the "Language" class
		if getattr(self.arguments, "language") == True:
			self.Language.Create_Language_Text()

	def Reset_Switches(self):
		# Reset the switches
		self.Global_Switches.Reset()

if __name__ == "__main__":
	Module_Selector()
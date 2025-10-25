# JSON.py

import os

class JSON():
	def __init__(self):
		# Import the classes
		self.Import_Classes()

		# Define the folders of the module
		self.folders = self.Define_Folders(object = self).folders

		# Define the "Switches" dictionary
		self.Define_Switches()

		# Define the texts of the module
		self.Define_Texts()

	def Import_Classes(self):
		import importlib

		# ---------- #

		# Define the list of modules to be imported
		modules = [
			"Define_Folders",
			"Global_Switches",
			"Language"
		]

		# Iterate through the list of modules
		for module_title in modules:
			# Import the module
			module = importlib.import_module("." + module_title, "Utility")

			# Get the sub-class
			sub_class = getattr(module, module_title)

			# If the module title is not "Define_Folders"
			if module_title != "Define_Folders":
				# Run the sub-class to define its variable
				sub_class = sub_class()

			# Add the sub-class to the current module
			setattr(self, module_title, sub_class)

	def Define_Switches(self):
		# Get the "Switches" dictionary from the "Global_Switches" module
		self.switches = self.Global_Switches.switches["Global"]

		# Update the "Switches" dictionary, adding the "File" dictionary
		self.switches.update({
			"File": {
				"Create": True,
				"Edit": True
			}
		})

		# If the "Testing" switch is True
		if self.switches["Testing"] == True:
			# Iterate through the switches inside the "File" dictionary
			for switch in self.switches["File"]:
				# Define them as False
				self.switches["File"][switch] = False

	def Define_Texts(self):
		# Define the "Texts" dictionary
		self.texts = self.To_Python(self.module["Files"]["Texts"])

		# Define the "Language texts" dictionary
		self.language_texts = self.Language.Item(self.texts)

		# Define the "Date" utility dictionary
		self.folders["Apps"]["Module files"]["Utility"]["Date"] = {
			"Texts": self.folders["Apps"]["Module files"]["Utility"]["root"] + "Date/Texts.json"
		}

		# Define the "Date texts" dictionary
		self.date_texts = self.To_Python(self.folders["Apps"]["Module files"]["Utility"]["Date"]["Texts"])

	def Sanitize(self, path):
		path = os.path.normpath(path).replace("\\", "/")

		if (
			"/" not in path[-1] and
			os.path.splitext(path)[-1] == ""
		):
			path += "/"

		return path

	def Verbose(self, text, item, verbose = None):
		if (
			self.switches["Verbose"] == True and
			verbose == None or
			verbose == True
		):
			import inspect

			print()
			print(self.module["Name"] + "." + inspect.stack()[1][3] + "():")
			print("\t" + text + ":")
			print("\t" + item)

	def File_Exists(self, file):
		# Sanitize the file path
		file = self.Sanitize(file)

		# Checks if the file exists and returns True if it does or False if it does not
		return os.path.isfile(file)

	def Contents(self, file):
		file = self.Sanitize(file)

		contents = {
			"lines": [],
			"lines_none": [None],
			"string": "",
			"size": 0,
			"length": 0,
		}

		if self.File_Exists(file) == True:
			contents["string"] = open(file, "r", encoding = "utf8").read()
			contents["size"] += os.path.getsize(file)

			for line in open(file, "r", encoding = "utf8").readlines():
				line = line.replace("\n", "")

				contents["lines"].append(line)
				contents["lines_none"].append(line)

			contents["length"] = len(contents["lines"])

		if self.File_Exists(file) == False:
			self.Verbose(self.language_texts["this_file_does_not_exists"], file)

		return contents

	def Edit(self, file, text, next_line = True, verbose = None, full_verbose = False, edit = False):
		# Sanitize the file path
		file = self.Sanitize(file)

		# Get the contents of the file
		contents = self.Contents(file)

		# Transform the text into the JSON format
		text = self.From_Python(text)

		# Get the verbose text for the file
		verbose_text = self.Language.Check_Text_Difference(contents, text, full_verbose = full_verbose)

		# Define the file text as the file plus two line breaks, one tab, and the verbose text
		file_text = file + "\n" + \
		"\n" + \
		"\t" + verbose_text

		# If the file exists
		if self.File_Exists(file) == True:
			# If the file "Edit" switch is True
			# Or the "edit" parameter is True
			if (
				self.switches["File"]["Edit"] == True or
				edit == True
			):
				# If the file text string is not equal to the parameter text
				if contents["string"] != text:
					# Open the file handle
					edit = open(file, "w", encoding = "UTF8")

					# Write the text into the file
					edit.write(text)

					# Close the file handle
					edit.close()

					# Define the show text to tell the user that the file was edited
					show_text = self.language_texts["file, title()"] + " " + self.language_texts["edited, masculine"]

			# If the file "Edit" switch is False
			# And the "edit" parameter is False
			if (
				self.switches["File"]["Edit"] == False and
				edit == False
			):
				# Define the show text to tell the user that it was not possible to edit the file due to lack of permissions
				show_text = self.language_texts["it_was_not_possible_to_{}_the_file_permission_not_granted"].format(self.language_texts["edit"])

			# If the file text string is not equal to the parameter text
			if contents["string"] != text:
				# Show the verbose text
				self.Verbose(show_text, file_text, verbose = verbose)

			# If the file "Edit" switch is True
			# And the "edit" parameter is True
			if (
				self.switches["File"]["Edit"] == True or
				edit == True
			):
				return True

			# If the file "Edit" switch is False
			# And the "edit" parameter is False
			if (
				self.switches["File"]["Edit"] == False and
				edit == False
			):
				return False

		# If the file does not exist
		if self.File_Exists(file) == False:
			# Show the verbose text to tell the user that the file does not exist and return False
			self.Verbose(self.language_texts["this_file_does_not_exists"], file_text, verbose = verbose)

			return False

	def Dumps(self, items):
		# Import the json module
		import json

		# Dump the items
		items = json.dumps(items, indent = "\t", ensure_ascii = False)

		# Return the items
		return items

	def From_Python(self, items_parameter):
		# Import some useful modules
		import json
		from copy import deepcopy
		import datetime
		import types

		if type(items_parameter) == dict:
			items_parameter = dict(items_parameter)

			for key, value in items_parameter.items():
				if (
					type(value).__name__ in ["Credentials", "Resource"] or
					type(value) not in [int, dict, list]
				):
					items_parameter[key] = str(value)

		items = deepcopy(items_parameter)

		if isinstance(items, datetime.datetime) == True:
			items = [
				self.Date_To_String(items)
			]

		if type(items) == dict:
			for key in items:
				value = items[key]

				if isinstance(items[key], datetime.datetime) == True:
					items[key] = self.Date_To_String(items[key])

				if type(value) not in [str, int, list, dict, bool, None]:
					if isinstance(value, datetime.datetime) == False:
						items[key] = str(value)

					if isinstance(value, datetime.datetime) == True:
						items[key] = self.Date_To_String(items[key])

				if type(value) == dict:
					for sub_key in value:
						if "_PytzShimTimezone" in str(items[key][sub_key]):
							items[key][sub_key] = str(items[key][sub_key])

						if type(items[key][sub_key]) not in [str, int, list, dict, bool, None]:
							if isinstance(items[key][sub_key], datetime.datetime) == False:
								items[key][sub_key] = str(items[key][sub_key])

							if isinstance(items[key][sub_key], datetime.datetime) == True:
								items[key][sub_key] = self.Date_To_String(items[key][sub_key])

						if type(items[key][sub_key]) == dict:
							for sub_sub_key in items[key][sub_key]:
								if "_PytzShimTimezone" in str(items[key][sub_key][sub_sub_key]):
									items[key][sub_key][sub_sub_key] = str(items[key][sub_key][sub_sub_key])

								if type(items[key][sub_key][sub_sub_key]) not in [str, int, list, dict, bool, None]:
									if isinstance(items[key][sub_key][sub_sub_key], datetime.datetime) == False:
										items[key][sub_key][sub_sub_key] = str(items[key][sub_key][sub_sub_key])

									if isinstance(items[key][sub_key][sub_sub_key], datetime.datetime) == True:
										items[key][sub_key][sub_sub_key] = self.Date_To_String(items[key][sub_key][sub_sub_key])

								if isinstance(items[key][sub_key][sub_sub_key], datetime.datetime) == True:
									items[key][sub_key][sub_sub_key] = self.Date_To_String(items[key][sub_key][sub_sub_key])

		if type(items) == list:
			i = 0
			for item in items:
				if isinstance(items[i], datetime.datetime) == True:
					items[i] = self.Date_To_String(items[i])

				else:
					items[i] = str(items[i])

				i += 1

		if type(items) == str:
			items = self.To_Python(items)

		# Dump the items
		items = self.Dumps(items)

		# Return the items
		return items

	def Date_To_String(self, date, format = ""):
		import datetime

		if isinstance(date, datetime.datetime) == False:
			date = date["Object"]

		if format == "":
			format = self.date_texts["default_format"]

			if date.strftime("%Z") == "UTC":
				format += "Z"

			else:
				format += "%z"

		return date.strftime(format)

	def To_Python(self, item):
		# Import the json module
		import json

		# If the item is a file
		if self.File_Exists(item) == True:
			# Sanitize the file path
			item = self.Sanitize(item)

			# Convert the file text into a Python dictionary
			dictionary = json.load(open(item, encoding = "utf8"))

		# If the item is not a file
		if self.File_Exists(item) == False:
			# Convert the JSON dictionary into a Python dictionary
			dictionary = json.loads(item)

		# Return the Python dictionary
		return dictionary

	def Show(self, json, return_text = False):
		# Convert the JSON from Python to JSON text
		json = self.From_Python(json)

		# If the "return text" parameter is False, show the text
		if return_text == False:
			print(json)

		# If it is True, return the text
		if return_text == True:
			return json

	def Copy(self, json, verbose = True):
		# Convert the JSON from Python to JSON text
		text = self.From_Python(json)

		# Import the "pyperclip" module
		import pyperclip

		# Copy the JSON
		pyperclip.copy(text)

		# Show the verbose text about the copied text
		self.Verbose(self.Language.language_texts["copied_text"], "[" + text + "]", verbose = verbose)

	def Add_Key_After_Key(self, dictionary, key_value, after_key = None, number_to_add = 1, add_to_end = False, remove_after_key = False):
		keys = list(dictionary.keys())
		values = list(dictionary.values())

		if "key" not in key_value:
			key_value["key"] = list(key_value.keys())[0]
			key_value["value"] = list(key_value.values())[0]

		i = 0
		for key in keys.copy():
			if (
				key_value["key"] not in keys and
				key == after_key or
				add_to_end == True
			):
				if add_to_end == True:
					number = len(keys)

				else:
					number = i + number_to_add

				keys.insert(number, key_value["key"])
				values.insert(number, key_value["value"])

			if key_value["key"] in keys and key == key_value["key"]:
				values[i] = key_value["value"]

			i += 1

		dictionary = dict(zip(keys, values))

		if remove_after_key == True:
			dictionary.pop(after_key)

		return dictionary

	def Sort_Item_List(self, items, order):
		# Define the new items as an empty dictionary
		new_items = {}

		# If the items is a list
		if type(items) == list:
			# Update it to be an empty list
			new_items = []

		# Iterate through the items in the order list
		i = 0
		for item in order:
			# If the items is a dictionary
			if type(items) == dict:
				# Get the value from the dictionary of items
				value = items[item]

				# Add the key and value to the new dictionary of items
				new_items[item] = value

			# If the items is a list
			if type(items) == list:
				# Get the value from the items list
				value = items[i]

				# Add the key and value to the new list of items
				new_items.append(value)

			# Add it to the "i" number
			i += 1

		# Return the new items list
		return new_items

	def Remove_Duplicates_From_List(self, items):
		# Define the new items list
		new_items = []

		# Iterate through the items inside the original list
		for item in items:
			# If the item is not present in the new items list
			if item not in new_items:
				new_items.append(item)

		# Return the new items list
		return new_items
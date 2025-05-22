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

	def Exist(self, file):
		file = self.Sanitize(file)

		if os.path.isfile(file) == True:
			return True

		if os.path.isfile(file) == False:
			return False

	def Contents(self, file):
		file = self.Sanitize(file)

		contents = {
			"lines": [],
			"lines_none": [None],
			"string": "",
			"size": 0,
			"length": 0,
		}

		if self.Exist(file) == True:
			contents["string"] = open(file, "r", encoding = "utf8").read()
			contents["size"] += os.path.getsize(file)

			for line in open(file, "r", encoding = "utf8").readlines():
				line = line.replace("\n", "")

				contents["lines"].append(line)
				contents["lines_none"].append(line)

			contents["length"] = len(contents["lines"])

		if self.Exist(file) == False:
			self.Verbose(self.language_texts["this_file_does_not_exists"], file)

		return contents

	def Edit(self, file, text, next_line = True, verbose = None, edit = False):
		file = self.Sanitize(file)

		contents = self.Contents(file)

		text = self.From_Python(text)

		verbose_text = self.Language.Check_Text_Difference(contents, text)

		file_text = file + "\n\n\t" + verbose_text

		if self.Exist(file) == True:
			if (
				self.switches["File"]["Edit"] == True or
				edit == True
			):
				if contents["string"] != text:
					edit = open(file, "w", encoding = "UTF8")
					edit.write(text)
					edit.close()

					show_text = self.language_texts["file, title()"] + " " + self.language_texts["edited, masculine"]

			if self.switches["File"]["Edit"] == False:
				show_text = self.language_texts["it_was_not_possible_to_{}_the_file_permission_not_granted"].format(self.language_texts["edit"])

			if contents["string"] != text:
				self.Verbose(show_text, file_text, verbose = verbose)

			if self.switches["File"]["Edit"] == True:
				return True

			if self.switches["File"]["Edit"] == False:
				return False

		if self.Exist(file) == False:
			self.Verbose(self.language_texts["this_file_does_not_exists"], file_text, verbose = verbose)

			return False

	def From_Python(self, items_parameter):
		import json
		from copy import deepcopy

		items = deepcopy(items_parameter)

		if type(items) == dict:
			import datetime

			for key in items:
				value = items[key]

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
				items[i] = str(items[i])

				i += 1

		if type(items) == str:
			items = self.To_Python(items)

		return json.dumps(items, indent = "\t", ensure_ascii = False)

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
		import json

		if os.path.isfile(item) == True:
			item = self.Sanitize(item)

			dictionary = json.load(open(item, encoding = "utf8"))

		if os.path.isfile(item) == False:
			dictionary = json.loads(item)

		return dictionary

	def Show(self, json, return_text = False):
		json = self.From_Python(json)

		if return_text == False:
			print(json)

		if return_text == True:
			return json

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
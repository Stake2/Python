# JSON.py

# Import some useful modules
import os
import datetime
import json
import inspect

class JSON():
	def __init__(self):
		# Import the classes
		self.Import_Classes()

		# Define the folders of the module
		self.folders = self.Define_Folders(object = self, create_texts = False).folders

		# Define the "Switches" dictionary
		self.Define_Switches()

		# Define the module texts
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
		# Define the "Date" utility dictionary
		self.folders["Apps"]["Module files"]["Utility"]["Date"] = {
			"Texts": self.folders["Apps"]["Module files"]["Utility"]["root"] + "Date/Texts.json"
		}

		# Define the "Date texts" text dictionary
		self.date_texts = self.To_Python(self.folders["Apps"]["Module files"]["Utility"]["Date"]["Texts"])

	def Sanitize(self, path):
		# Replace double backwards slashes with one forward slash
		path = os.path.normpath(path).replace("\\", "/")

		# If there is no forward slash in the path
		# And the last character returned by the "splittext" method is an empty string
		if (
			"/" not in path[-1] and
			os.path.splitext(path)[-1] == ""
		):
			# Add a forward slash to the end of the path
			path += "/"

		# Return the path
		return path

	def Verbose(self, text, item, verbose = None):
		# If the "Verbose" switch is True
		# And the verbose parameter is None
		# Or the verbose parameter is True
		if (
			self.switches["Verbose"] == True and
			verbose == None or
			verbose == True
		):
			# Get the name of the method which ran this method (the "Verbose" one)
			runner_method_name = inspect.stack()[1][3]

			# Show the module name (JSON) and the method which ran this method (the "Verbose" one)
			print()
			print(self.module["Name"] + "." + runner_method_name + "():")

			# Show the verbose text
			print("\t" + text + ":")

			# Show the verbose item
			print("\t" + item)

	def File_Exists(self, file):
		# Sanitize the file path
		file = self.Sanitize(file)

		# Checks if the file exists and returns the boolean
		return os.path.isfile(file)

	def File_Open(self, file, mode = "r", encoding = "UTF8"):
		# Open the file with the mode and encoding
		return open(file, mode, encoding = encoding)

	def File_Contents(self, file):
		# Sanitize the file path
		file = self.Sanitize(file)

		# Define the contents dictionary
		contents = {
			"Lines": [],
			"String": "",
			"Size": 0,
			"Length": 0
		}

		# If the file exists
		if self.File_Exists(file) == True:
			# Open the file handle in read mode (the default mode)
			file_handle = self.File_Open(file)

			# Iterate through the lines inside the file
			for line in file_handle.readlines():
				# Remove the line break from the line
				line = line.replace("\n", "")

				# Add the line to the list of lines
				contents["Lines"].append(line)

			# Reset cursor to the beginning of the file before getting the file string
			file_handle.seek(0)

			# Read the file and get its string
			contents["String"] = file_handle.read()

			# Close the file handle
			file_handle.close()

			# Get the size of the file
			contents["Size"] = os.path.getsize(file)

			# Get the length of the file
			contents["Length"] = len(contents["Lines"])

		# If the file does not exist
		if self.File_Exists(file) == False:
			# Show the verbose text saying that the file does not exist
			self.Verbose(self.Language.language_texts["this_file_does_not_exists"], file)

		# Return the contents dictionary
		return contents

	def Edit(self, file, text, next_line = True, verbose = None, full_verbose = False, edit = False):
		# Sanitize the file path
		file = self.Sanitize(file)

		# Get the contents of the file
		contents = self.File_Contents(file)

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
			# Or the edit parameter is True
			if (
				self.switches["File"]["Edit"] == True or
				edit == True
			):
				# If the file text string is not equal to the parameter text
				if contents["String"] != text:
					# Open the file handle in write mode
					edit = self.File_Open(file, "w")

					# Write the text into the file
					edit.write(text)

					# Close the file handle
					edit.close()

					# Define the show text to tell the user that the file was edited
					show_text = self.Language.language_texts["file, title()"] + " " + self.Language.language_texts["edited, masculine"]

			# If the file "Edit" switch is False
			# And the "edit" parameter is False
			if (
				self.switches["File"]["Edit"] == False and
				edit == False
			):
				# Define the show text to tell the user that it was not possible to edit the file due to lack of permissions
				show_text = self.Language.language_texts["it_was_not_possible_to_{}_the_file_permission_not_granted"].format(self.Language.language_texts["edit"])

			# If the file text string is not equal to the parameter text
			if contents["String"] != text:
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
			self.Verbose(self.Language.language_texts["this_file_does_not_exists"], file_text, verbose = verbose)

			return False

	def Dumps(self, items):
		# Dump the items
		items = json.dumps(items, indent = "\t", ensure_ascii = False)

		# Return the items
		return items

	def From_Python(self, items, testing = False):
		# Import some useful modules
		from copy import deepcopy
		import types

		# If the items parameter is a dictionary
		if type(items) == dict:
			# Convert it into a dictionary using the "dict" function
			items = dict(items)

			# Iterate through the keys and values of the items dictionary
			for key, value in items.items():
				# If the type name of the value is either "Credentials" or "Resource"
				# Or it is not a number, a dictionary, or a list
				if (
					type(value).__name__ in ["Credentials", "Resource"] or
					type(value) not in [int, dict, list]
				):
					# Convert it to a string
					items[key] = str(value)

				# Get the name of the method which ran this method (the "From_Python" one)
				runner_method_name = inspect.stack()[1][3]

				# If the value is a dictionary
				# And the runner method is "Show"
				# And the local testing switch is True
				if (
					type(value) == dict and
					runner_method_name == "Show" and
					testing == True
				):
					# Convert the objects of the value into strings
					value = self.Convert_Objects(value)

				# Update the value inside the root dictionary
				items[key] = value

		# Make a copy of the items parameter
		items_copy = deepcopy(items)

		# If the items parameter is a datetime object
		if self.Is_Datetime(items_copy) == True:
			# Convert it into a list with the first item being the items converted into a date string
			items_copy = [
				self.Date_To_String(items_copy)
			]

		# If the items parameter is a dictionary
		if type(items_copy) == dict:
			# Iterate through its keys and values
			for key, value in items_copy.items():
				# Check the value for a datetime to convert it correctly
				value = self.Check_Datetime(value)

				# Update the value inside the root dictionary
				items_copy[key] = value

				# If the value is a dictionary
				if type(value) == dict:
					# Iterate through its sub-keys and sub-values
					for sub_key, sub_value in value.items():
						# Check the sub-value for a datetime to convert it correctly
						sub_value = self.Check_Datetime(sub_value)

						# Update the sub-value inside the root dictionary
						value[sub_key] = sub_value

						# If the sub-value is a dictionary
						if type(sub_value) == dict:
							# Iterate through its sub-sub-keys and sub-sub-values
							for sub_sub_key, sub_sub_value in sub_value.items():
								# Check the sub-sub-value for a datetime to convert it correctly
								sub_sub_value = self.Check_Datetime(sub_sub_value)

								# If the sub-sub-value is a dictionary
								if type(sub_sub_value) == dict:
									# Iterate through its sub-sub-sub-keys and sub-sub-sub-values
									for sub_sub_sub_key, sub_sub_sub_value in sub_sub_value.items():
										# Check the sub-sub-sub-value for a datetime to convert it correctly
										sub_sub_sub_value = self.Check_Datetime(sub_sub_sub_value)

										# If the sub-sub-sub-value is a dictionary
										if type(sub_sub_sub_value) == dict:
											# Iterate through its sub-sub-sub-sub-keys and sub-sub-sub-values
											for sub_sub_sub_sub_key, sub_sub_sub_sub_value in sub_sub_sub_value.items():
												# Check the sub-sub-sub-sub-value for a datetime to convert it correctly
												sub_sub_sub_sub_value = self.Check_Datetime(sub_sub_sub_sub_value)

												# Update the sub-sub-sub-value inside the root dictionary
												sub_sub_sub_value[sub_sub_sub_sub_key] = sub_sub_sub_sub_value

										# Update the sub-sub-sub-value inside the root dictionary
										sub_sub_value[sub_sub_sub_key] = sub_sub_sub_value

								# Update the sub-sub-value inside the root dictionary
								sub_value[sub_sub_key] = sub_sub_value

						# Update the sub-value inside the root dictionary
						value[sub_key] = sub_value

				# Update the value inside the root dictionary
				items_copy[key] = value

		# If the items parameter is a list
		if type(items_copy) == list:
			# Iterate through the items in the list
			i = 0
			for item in items_copy:
				# If the item is not a datetime object, convert it into a date string
				if self.Is_Datetime(item) == True:
					item = self.Date_To_String(item)

				# If not, convert it into a string
				else:
					item = str(item)

				# Update the item in the root list
				items_copy[i] = item

				# Add one to the "i" number
				i += 1

		# If the items parameter is a string
		if type(items_copy) == str:
			# Convert it into a Python object
			items_copy = self.To_Python(items_copy)

		# Dump the items
		items_copy = self.Dumps(items_copy)

		# Return the items dictionary
		return items_copy

	def Is_Datetime(self, item):
		# Return the boolean saying if the item is a datetime or time object or not
		return isinstance(item, (datetime.datetime, datetime.time))

	def Check_Datetime(self, item):
		# If the "_PytzShimTimezone" string is present in the item, convert it into a string
		if "_PytzShimTimezone" in str(item):
			item = str(item)

		# If the value is not a string, number, list, dictionary, boolean, or None
		if type(item) not in [str, int, list, dict, bool, None]:
			# If the item is not a datetime object, convert it into a string
			if self.Is_Datetime(item) == False:
				item = str(item)

			# If it is, convert it into a date string
			if self.Is_Datetime(item) == True:
				item = self.Date_To_String(item)

		# Return the item
		return item

	def Date_To_String(self, date, format = ""):
		# If the item is not a datetime object, get the datetime object from the "Object" key
		if self.Is_Datetime(date) == False:
			date = date["Object"]

		# If the date format is empty
		if format == "":
			# Get the default date format
			format = self.date_texts["default_format"]

			# If the timezone is "UTC"
			if date.strftime("%Z") == "UTC":
				# Add the "Z" to the format
				format += "Z"

			# If not, add the timezone character
			else:
				format += "%z"

		# Convert the datetime object into a string using the defined format and return it
		return date.strftime(format)

	def Convert_Objects(self, value):
		# Iterate through its sub-keys and sub-values
		for sub_key, sub_value in value.items():
			# Get the type name of the sub-value
			type_name = type(sub_value).__name__

			# If the sub-value is a module, function, class, or method
			if type_name in ["module", "function", "type", "method"]:
				# Convert it into a string
				sub_value = str(sub_value)

			# Update the sub-value inside the root dictionary
			value[sub_key] = sub_value

			# If the sub-value is a dictionary
			if type(sub_value) == dict:
				# Iterate through its sub-sub-keys and sub-sub-values
				for sub_sub_key, sub_sub_value in sub_value.items():
					# Get the type name of the sub-sub-value
					type_name = type(sub_sub_value).__name__

					# If it is a module
					if type_name == "module":
						# Get the root module
						root_module = sub_sub_value.__name__.split(".")[0]

						# Get the module
						module = sub_sub_value.__name__.split(".")[1]

						# Define the sub-sub-value as the root module plus the module
						sub_sub_value = str(root_module) + "." + str(module)

					# If it is a type (class)
					if type_name == "type":
						# Get the module of the class
						module = str(sub_sub_value.__module__).split(".")[0]

						# Get the name of the class
						class_name = str(sub_sub_value.__module__).split(".")[-1]

						# Define the sub-module as the class name
						sub_module = class_name

						# Define the sub-sub-value as the three variables above added together
						sub_sub_value = str(module) + "." + str(sub_module) + "." + str(class_name) + "()"

					# If the sub-sub-value is a dictionary
					if type(sub_sub_value) == dict:
						for sub_sub_sub_key, sub_sub_sub_value in sub_sub_value.items():
							# Make a copy of the original sub-sub-value
							sub_sub_value = sub_sub_value.copy()

							# Get the type name of the sub-sub-sub-value
							type_name = type(sub_sub_sub_value).__name__

							# If the sub-sub-sub-value is a module, function, class, or method
							if type_name in ["module", "function", "type", "method"]:
								# If it is a method
								if type_name == "method":
									# Get its class
									method_class = sub_sub_sub_value.__self__.__class__

									# Get the module of the class
									module = method_class.__module__.split(".")[0]

									# Get the name of the class
									method_class = method_class.__name__

									# Get the method name
									method_name = sub_sub_sub_value.__name__

									# Define the sub-sub-sub-value as the two variables above added together
									sub_sub_sub_value = str(module) + "." + str(method_class) + "." + str(method_name) + "()"

								# Convert it into a string
								sub_sub_sub_value = str(sub_sub_sub_value)

							# Update the sub-sub-sub-value inside the root dictionary
							sub_sub_value[sub_sub_sub_key] = sub_sub_sub_value

					# Update the sub-sub-value inside the root dictionary
					sub_value[sub_sub_key] = sub_sub_value

			# Update the sub-value inside the root dictionary
			value[sub_key] = sub_value

		# Return the value
		return value

	def To_Python(self, item):
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

	def Show(self, json, return_text = False, testing = False):
		# Convert the JSON from Python to JSON text
		json = self.From_Python(json, testing = testing)

		# If the "return text" parameter is False, show the text
		if return_text == False:
			print(json)

		# If it is True, return the text
		if return_text == True:
			return json

	def Copy(self, json):
		# Convert the JSON from Python to JSON text
		text = self.From_Python(json)

		# Import the "pyperclip" module
		import pyperclip

		# Copy the JSON
		pyperclip.copy(text)

		# Show the verbose text about the copied text
		# (Never show it because the JSON dictionaries are frequently extensive)
		self.Verbose(self.Language.language_texts["copied_text"], "[" + text + "]", verbose = False)

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

	def List_Has_Only_Numbers(self, items):
		return all(isinstance(item, int) for item in items)

	def Sort_Item_List(self, items, order):
		# Define the new items as an empty dictionary
		new_items = {}

		# If the items is a list
		if type(items) == list:
			# Update it to be an empty list
			new_items = []

		# If the items is a dictionary
		if type(items) == dict:
			# List the keys and values
			keys = list(items.keys())
			values = list(items.values())

		# If the order is a list of only numbers
		if self.List_Has_Only_Numbers(order) == True:
			# Iterate through the orders
			i = 0
			for item in order.copy():
				# Remove one from the order number to make it access the list correcly (starting from zero)
				item -= 1

				# Update the order in the list
				order[i] = item

				# Add one to the "i" number
				i += 1

		# Iterate through the items in the order list
		i = 0
		for item in order:
			# If the items is a dictionary
			if type(items) == dict:
				# If the item is a string
				if type(item) == str:
					# Get the value from the dictionary of items
					value = items[item]

					# Add the key and value to the new dictionary of items
					new_items[item] = value

				# If the item is a number
				if type(item) == int:
					# Get the key and value from their respective lists
					key = keys[item]
					value = values[item]

					# Add the key and value to the new dictionary of items
					new_items[key] = value

			# If the items is a list
			if type(items) == list:
				# Get the value from the items list
				value = items[i]

				# If the order is a list of only numbers
				if self.List_Has_Only_Numbers(order) == True:
					# Get the value from the items list using the order
					value = items[item]

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
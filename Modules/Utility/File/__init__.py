# File.py

import os

class File():
	def __init__(self):
		# Import the classes
		self.Import_Classes()

		# Define the folders of the module
		self.Define_Folders(object = self)

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
			"JSON"
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

		# ---------- #

		# Define the "Language" class as the same class inside the "JSON" class
		self.Language = self.JSON.Language

	def Define_Switches(self):
		# Get the "Switches" dictionary from the "Global_Switches" module
		self.switches = self.Global_Switches.switches["Global"]

		# Update the "Switches" dictionary, adding the "File" dictionary
		self.switches.update({
			"File": {
				"Create": True,
				"Delete": True,
				"Copy": True,
				"Move": True,
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
		self.texts = self.JSON.To_Python(self.module["Files"]["Texts"])

		# Define the "Language texts" dictionary
		self.language_texts = self.Language.Item(self.texts)

	def Sanitize(self, path, restricted_characters = False):
		# If the "restricted characters" parameter is False
		if restricted_characters == False:
			# Normalize the path and replace backslashes with forward slashes
			path = os.path.normpath(path).replace("\\", "/")

		# If the "restricted characters" parameter is True
		if restricted_characters == True:
			# Remove the restricted characters
			path = self.Remove_Restricted_Characters(path)

		# Return the path
		return path

	def Remove_Restricted_Characters(self, path):
		# Define the list of restricted characters
		restricted_characters = [
			":",
			"?",
			'"',
			"\\",
			"/",
			"|",
			"｜",
			"*",
			"<",
			">"
		]

		# Iterate through the list of characters
		for character in restricted_characters:
			# Remove the character if it exists
			path = path.replace(character, "")

		# Remove leading and trailing spaces
		path = path.strip()

		# Remove double spaces
		path = path.replace("  ", " ")

		# Replace multiple spaces with a single space
		path = " ".join(path.split())

		# Return the path
		return path

	def Name(self, file):
		# Sanitize the file
		file = self.Sanitize(file)

		# Get the file name
		file_name = os.path.splitext(os.path.basename(file))[0]

		# Return it
		return file_name

	def Folder(self, file):
		# Sanitize the file
		file = self.Sanitize(file)

		# Split the file to get the folders
		split = file.split("/")

		# Define the folder as an empty string
		folder = ""

		# Add each sub-folder with a slash to the empty string above
		for i in split:
			if i != split[-1]:
				folder += i + "/"

		# Return the folder
		return folder

	def Verbose(self, text, item, verbose = False):
		if (
			self.switches["Verbose"] == True or
			verbose == True
		):
			import inspect

			method_ = inspect.stack()[1][3]

			print("")
			print(self.module["Name"] + "." + method_ + "():")
			print("\t" + text + ":")
			print("\t" + item)

	def Exists(self, file):
		# Sanitize the file path
		file = self.Sanitize(file)

		# Checks if the file exists and returns True if it does or False if it does not
		return os.path.isfile(file)

	def Type(self, text = None):
		if text == None:
			text = self.language_texts["type_or_paste_the_file"] + ": "

		print()

		return input(text)

	def Create(self, file):
		file = self.Sanitize(file)

		if self.Exists(file) == True:
			return False

		if (
			self.switches["File"]["Create"] == True and
			self.Exists(file) == False
		):
			create = open(file, "w", encoding = "utf8")
			create.close()

			self.Verbose(self.language_texts["file, title()"] + " " + self.language_texts["created, masculine"], file)

			return True

		if self.switches["File"]["Create"] == False:
			self.Verbose(self.language_texts["it_was_not_possible_to_{}_the_file_permission_not_granted"].format(self.language_texts["create"]) + "." + "\n\n\t" + self.language_texts["file, title()"], file)

			return False

	def Delete(self, file):
		file = self.Sanitize(file)

		if self.Exists(file) == False:
			self.Verbose(self.language_texts["this_file_does_not_exist"], file)

			return False

		if (
			self.switches["File"]["Delete"] == True and
			self.Exists(file) == True
		):
			os.remove(file)

			self.Verbose(self.language_texts["file, title()"] + " " + self.language_texts["deleted, masculine"], file)

			return True

		if self.switches["File"]["Delete"] == False:
			self.Verbose(self.language_texts["it_was_not_possible_to_{}_the_file_permission_not_granted"].format(self.language_texts["delete"]) + "." + "\n\n\t" + self.language_texts["file, title()"], file, verbose = True)

			return False

	def Copy(self, source_file = None, destination_file = None):
		if source_file == None:
			source_file = self.Type()

		if destination_file == None:
			destination_file = self.Type()

		source_file = self.Sanitize(source_file)
		destination_file = self.Sanitize(destination_file)

		if self.Exists(source_file) == False:
			self.Verbose(self.language_texts["this_file_does_not_exist"], source_file)

			return False

		if (
			self.switches["File"]["Copy"] == True and
			self.Exists(source_file) == True
		):
			import shutil
			shutil.copy(source_file, destination_file)

			self.Verbose(self.language_texts["source_file"] + ":\n\t" + source_file + "\n\n" + self.language_texts["destination_file"], destination_file)

			return True

		if self.switches["File"]["Copy"] == False:
			self.Verbose(self.language_texts["it_was_not_possible_to_{}_the_file_permission_not_granted"].format(self.language_texts["copy"]) + "." + "\n\n\t" + self.language_texts["source_file"] + ":\n\t" + source_file + "\n\n\t" + self.language_texts["destination_file"], destination_file, verbose = True)

			return False

	def Move(self, source_file = None, destination_file = None):
		if source_file == None:
			source_file = self.Type()

		if destination_file == None:
			destination_file = self.Type()

		source_file = self.Sanitize(source_file)
		destination_file = self.Sanitize(destination_file)

		if (
			self.Exists(source_file) == True and
			source_file != destination_file
		):
			if (
				self.switches["File"]["Move"] == True and
				self.Exists(source_file) == True
			):
				import shutil
				shutil.move(source_file, destination_file)

				self.Verbose(self.language_texts["source_file"] + ":\n\t" + source_file + "\n\n" + self.language_texts["destination_file"], destination_file)

				return True

			if self.switches["File"]["Move"] == False:
				self.Verbose(self.language_texts["it_was_not_possible_to_{}_the_file_permission_not_granted"].format(self.language_texts["move"]) + "." + "\n\n\t" + self.language_texts["source_file"] + ":\n\t" + source_file + "\n\n\t" + self.language_texts["destination_file"], destination_file, verbose = True)

				return False

		else:
			return False

	def Edit(self, file, text, mode = "w", next_line = True, verbose = None, full_verbose = False):
		# Sanitize the file path
		file = self.Sanitize(file)

		# Get the contents of the file
		contents = self.Contents(file)

		# Define a shortcut to the file length
		length = contents["length"]

		# Define the line break as an empty string
		line_break = ""

		# If the "next line" parameter is True
		# And the file length is not zero
		# And the mode is "a" (append)
		if (
			next_line == True and
			length != 0 and
			mode == "a"
		):
			# Define the line break as the new line caracter
			line_break = "\n"

		# Get the verbose text for the file
		verbose_text = self.Language.Check_Text_Difference(contents, text, full_verbose = full_verbose)

		# Add the line break to the text
		text = line_break + text

		# Define the file text as the file plus two line breaks, one tab, and the verbose text
		file_text = file + "\n" + \
		"\n" + \
		"\t" + verbose_text
		
		# If the file exists
		if self.Exists(file) == True:
			# If the file "Edit" switch is True
			# And the file text string is not equal to the parameter text
			if (
				self.switches["File"]["Edit"] == True and
				contents["string"] != text
			):
				# Open the file handle
				edit = open(file, mode, encoding = "UTF8")

				# Write the text into the file
				edit.write(text)

				# Close the file handle
				edit.close()

				# Define the show text to tell the user that the file was edited
				show_text = self.language_texts["file, title()"] + " " + self.language_texts["edited, masculine"]

			# If the file "Edit" switch is False
			if self.switches["File"]["Edit"] == False:
				# Define the show text to tell the user that it was not possible to edit the file due to lack of permissions
				show_text = self.language_texts["it_was_not_possible_to_{}_the_file_permission_not_granted"].format(self.language_texts["edit"])

			# If the file text string is not equal to the parameter text
			if contents["string"] != text:
				# Show the verbose text
				self.Verbose(show_text, file_text, verbose = verbose)

			# If the file "Edit" switch is True, return True
			if self.switches["File"]["Edit"] == True:
				return True

			# If the file "Edit" switch is False, return False
			if self.switches["File"]["Edit"] == False:
				return False

		if self.Exists(file) == False:
			self.Verbose(self.language_texts["this_file_does_not_exist"], file_text)

			return False

	def Contents(self, file):
		file = self.Sanitize(file)

		contents = {
			"lines": [],
			"lines_none": [None],
			"string": "",
			"size": 0,
			"length": 0
		}

		if self.Exists(file) == True:
			contents["string"] = open(file, "r", encoding = "utf8").read()
			contents["size"] += os.path.getsize(file)

			for line in open(file, "r", encoding = "utf8").readlines():
				line = line.replace("\n", "")

				contents["lines"].append(line)
				contents["lines_none"].append(line)

			contents["length"] = len(contents["lines"])

		# Temporary:
		# Add the title case to the "Lines", "String", and "Length" keys
		for key in ["Lines", "String", "Length"]:
			contents[key] = contents[key.lower()]

		if self.Exists(file) == False:
			self.Verbose(self.language_texts["this_file_does_not_exist"], file)

		return contents

	def Split(self, lines = None, dict_ = None, text = None, separator = ": ", next_line = False, convert = None):
		if next_line == False:
			split = text.split(separator)

			key = split[0]

			if key != "":
				if " " in key[-1]:
					key = key[:-1]

				if " " in key[0]:
					key = key[1:]

			value = split[text.count(separator)]

			if convert != None:
				value = convert(value)

			if text.count(separator) == 2:
				value = split[1] + separator + value

			if text.count(separator) >= 3:
				split.pop(0)
				value = ""

				for item in split:
					value += item

					if item != split[-1]:
						value += separator

			if separator in key:
				key = key.replace(separator, "")

		if next_line == True:
			i = 0
			for line in lines:
				try:
					if separator in line and lines[i + 1] != "":
						key = line.replace(separator, "")

						value = lines[i + 1]

						if convert != None:
							value = convert(value)

						dict_[key] = value

				except:
					pass

				i += 1

		if next_line == False:
			return [key, value]

	def Dictionary(self, file, dictionary_separators = ": ", next_line = False, convert = None, true_or_false = False):
		file = self.Sanitize(file)

		if (
			next_line == True and
			dictionary_separators == ": "
		):
			dictionary_separators = [":"]

		if type(dictionary_separators) == str:
			dictionary_separators = [dictionary_separators]

		dictionary = {}

		lines = self.Contents(file)["lines"]
		string = self.Contents(file)["string"]

		if self.Exists(file) == True:
			if next_line == False:
				import re

				for line in lines:
					for dictionary_separator in dictionary_separators:
						if re.findall(r"\b" + dictionary_separator + r"\b", line, re.IGNORECASE):
							key, value = self.Split(text = line, separator = dictionary_separator)

							if convert != None:
								value = convert(value)

							if true_or_false == True:
								if value == "True":
									value = True

								if value == "False":
									value = False

							dictionary[key] = value

						elif dictionary_separator in line:
							key, value = self.Split(text = line, separator = dictionary_separator)

							if convert != None:
								value = convert(value)

							dictionary[key] = value

			if next_line == True:
				for dictionary_separator in dictionary_separators:
					self.Split(lines = lines, dict_ = dictionary, separator = dictionary_separator, next_line = next_line, convert = convert)

		if self.Exists(file) == False:
			self.Verbose(self.language_texts["this_file_does_not_exist"], file)

		return dictionary

	def Open(self, item, open = False):
		if "https" not in item:
			item = self.Sanitize(item)

		self.Verbose(self.language_texts["opening, title()"], item, verbose = True)

		if self.switches["Testing"] == False or open == True:
			os.startfile(item)

	def Close(self, program):
		import psutil

		for process in (process for process in psutil.process_iter() if program.split("\\")[program.count("\\")] in process.name()):
			process.kill()
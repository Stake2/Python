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
		if restricted_characters == False:
			path = os.path.normpath(path).replace("\\", "/")

		if restricted_characters == True:
			self.restricted_characters_list = [":", "?", '"', "\\", "/", "|", "*", "<", ">"]

			for character in self.restricted_characters_list:
				if character in path:
					path = path.replace(character, "")

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

	def Exist(self, file):
		file = self.Sanitize(file)

		if os.path.isfile(file) == True:
			return True

		if os.path.isfile(file) == False:
			return False

	def Type(self, text = None):
		if text == None:
			text = self.language_texts["type_or_paste_the_file"] + ": "

		print()

		return input(text)

	def Create(self, file):
		file = self.Sanitize(file)

		if self.Exist(file) == True:
			return False

		if (
			self.switches["File"]["Create"] == True and
			self.Exist(file) == False
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

		if self.Exist(file) == False:
			self.Verbose(self.language_texts["this_file_does_not_exists"], file)

			return False

		if (
			self.switches["File"]["Delete"] == True and
			self.Exist(file) == True
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

		if self.Exist(source_file) == False:
			self.Verbose(self.language_texts["this_file_does_not_exists"], source_file)

			return False

		if (
			self.switches["File"]["Copy"] == True and
			self.Exist(source_file) == True
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

		if self.Exist(source_file) == False:
			self.Verbose(self.language_texts["this_file_does_not_exists"], source_file)

			return False

		if (
			self.switches["File"]["Move"] == True and
			self.Exist(source_file) == True
		):
			import shutil
			shutil.move(source_file, destination_file)

			self.Verbose(self.language_texts["source_file"] + ":\n\t" + source_file + "\n\n" + self.language_texts["destination_file"], destination_file)

			return True

		if self.switches["File"]["Move"] == False:
			self.Verbose(self.language_texts["it_was_not_possible_to_{}_the_file_permission_not_granted"].format(self.language_texts["move"]) + "." + "\n\n\t" + self.language_texts["source_file"] + ":\n\t" + source_file + "\n\n\t" + self.language_texts["destination_file"], destination_file, verbose = True)

			return False

	def Edit(self, file, text, mode = "w", next_line = True, verbose = None):
		file = self.Sanitize(file)

		contents = self.Contents(file)
		length = contents["length"]

		line_break = ""

		if (
			next_line == True and
			length != 0 and
			mode == "a"
		):
			line_break = "\n"

		verbose_text = self.Language.Check_Text_Difference(contents, text)

		text = line_break + text

		file_text = file + "\n" + \
		"\n" + \
		"\t" + verbose_text

		if self.Exist(file) == True:
			if (
				self.switches["File"]["Edit"] == True and
				contents["string"] != text
			):
				edit = open(file, mode, encoding = "UTF8")
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
			self.Verbose(self.language_texts["this_file_does_not_exists"], file_text)

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

		if self.Exist(file) == True:
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

		if self.Exist(file) == False:
			self.Verbose(self.language_texts["this_file_does_not_exists"], file)

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
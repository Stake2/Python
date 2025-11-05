# File.py

# Import some useful modules
import os
import shutil

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

		# Add each sub-folder with a forward slash to the empty string above
		for item in split:
			# If the item is not the last item in the split list
			if item != split[-1]:
				# Add the item and a forward slash
				folder += item + "/"

		# Return the folder
		return folder

	def Verbose(self, text, item, verbose = None):
		# If the "Verbose" switch is True
		# And the verbose parameter is None
		# Or the verbose parameter is True
		if (
			self.switches["Verbose"] == True and
			verbose == None or
			verbose == True
		):
			import inspect

			# Get the name of the method which ran this method (the "Verbose" one)
			runner_method_name = inspect.stack()[1][3]

			# Show the module name (JSON) and the method which ran this method (the "Verbose" one)
			print()
			print(self.module["Name"] + "." + runner_method_name + "():")

			# Show the verbose text
			print("\t" + text + ":")

			# Show the verbose item
			print("\t" + item)

	def Exists(self, file):
		# Sanitize the file path
		file = self.Sanitize(file)

		# Checks if the file exists and returns True if it does or False if it does not
		return os.path.isfile(file)

	def Type(self, text = None):
		# If the text parameter is None
		if text == None:
			# Define the text as "Type or paste the file:"
			text = self.language_texts["type_or_paste_the_file"] + ": "

		# Show a space
		print()

		# Ask for the file
		file = input(text)

		# Return it
		return file

	def File_Open(self, file, mode = "r", encoding = "UTF8"):
		# Open the file with the mode and encoding
		return open(file, mode, encoding = encoding)

	def Create(self, file):
		# Sanitize the file path
		file = self.Sanitize(file)

		# If the file already exists, return False
		if self.Exists(file) == True:
			return False

		# If the file does not exist
		# And the "Create" file switch is True
		if (
			self.Exists(file) == False and
			self.switches["File"]["Create"] == True
		):
			# Open the file handle in write mode to create it
			create = self.File_Open(file, "w")

			# Close the file handle
			create.close()

			# Show the verbose text saying that the file was created
			self.Verbose(self.Language.language_texts["file, title()"] + " " + self.Language.language_texts["created, masculine"], file)

			return True

		# If the "Create" file switch is False
		if self.switches["File"]["Create"] == False:
			# Define the verbose text to tell the user that the file was not created due to the lack of permissions
			verbose_text = self.Language.language_texts["it_was_not_possible_to_{}_the_file_permission_not_granted"].format(self.Language.language_texts["create"]) + "." + "\n\n\t" + self.Language.language_texts["file, title()"]

			# Show the verbose text
			self.Verbose(verbose_text, file)

			return False

	def Delete(self, file):
		# Sanitize the file path
		file = self.Sanitize(file)

		# If the file does not exist
		if self.Exists(file) == False:
			# Show the verbose text saying that the file does not exist and thus can not be deleted
			self.Verbose(self.language_texts["this_file_does_not_exist"], file)

			return False

		# If the file exists
		# And the "Delete" file switch is True
		if (
			self.Exists(file) == True and
			self.switches["File"]["Delete"] == True
		):
			# Delete the file
			os.remove(file)

			# Show the verbose text saying that the file was deleted
			self.Verbose(self.Language.language_texts["file, title()"] + " " + self.Language.language_texts["deleted, masculine"], file)

			return True

		# If the "Delete" file switch is False
		if self.switches["File"]["Delete"] == False:
			# Define the verbose text to tell the user that the file was not deleted due to the lack of permissions
			verbose_text = self.Language.language_texts["it_was_not_possible_to_{}_the_file_permission_not_granted"].format(self.Language.language_texts["delete"]) + "." + "\n\n\t" + self.Language.language_texts["file, title()"]

			# Show the verbose text
			self.Verbose(verbose_text, file, verbose = True)

			return False

	def Define_Source_And_Destionation_Files(self, source_file = None, destination_file = None):
		# If the source file is None, ask for the user to type or paste it
		if source_file == None:
			source_file = self.Type()

		# If the destination file is None, ask for the user to type or paste it
		if destination_file == None:
			destination_file = self.Type()

		# Sanitize both the source and destination files
		source_file = self.Sanitize(source_file)
		destination_file = self.Sanitize(destination_file)

		# Return both files
		return source_file, destination_file

	def Copy(self, source_file = None, destination_file = None):
		# Define the source and destination files
		source_file, destination_file = self.Define_Source_And_Destionation_Files(source_file, destination_file)

		# If the file does not exist
		if self.Exists(source_file) == False:
			# Show the verbose text saying that the file does not exist and thus can not be copied
			self.Verbose(self.language_texts["this_file_does_not_exist"], source_file)

			return False

		# If the file exists
		# And the "Copy" file switch is True
		if (
			self.Exists(source_file) == True and
			self.switches["File"]["Copy"] == True
		):
			# Copy the file to the destination folder
			shutil.copy(source_file, destination_file)

			# Show the verbose text saying that the file was copied
			self.Verbose(self.language_texts["source_file"] + ":\n\t" + source_file + "\n\n" + self.language_texts["destination_file"], destination_file)

			return True

		# If the "Copy" file switch is False
		if self.switches["File"]["Copy"] == False:
			# Define the verbose text to tell the user that the file was not copied due to the lack of permissions
			verbose_text = self.Language.language_texts["it_was_not_possible_to_{}_the_file_permission_not_granted"].format(self.language_texts["copy"]) + "." + "\n\n\t" + self.Language.language_texts["file, title()"]

			# Show the verbose text
			self.Verbose(verbose_text, destination_file, verbose = True)

			return False

	def Move(self, source_file = None, destination_file = None):
		# Define the source and destination files
		source_file, destination_file = self.Define_Source_And_Destionation_Files(source_file, destination_file)

		# If the file exists
		# And the source file is not the same as the destination file
		if (
			self.Exists(source_file) == True and
			source_file != destination_file
		):
			# And the "Move" file switch is True
			if self.switches["File"]["Move"] == True:
				# Move the file to the destination folder
				shutil.move(source_file, destination_file)

				# Show the verbose text saying that the file was moved
				self.Verbose(self.language_texts["source_file"] + ":\n\t" + source_file + "\n\n" + self.language_texts["destination_file"], destination_file)

				return True

			# If the "Move" file switch is False
			if self.switches["File"]["Move"] == False:
				# Define the verbose text to tell the user that the file was not copied due to the lack of permissions
				verbose_text = self.Language.language_texts["it_was_not_possible_to_{}_the_file_permission_not_granted"].format(self.language_texts["move"]) + "." + "\n\n\t" + self.language_texts["source_file"] + ":\n\t" + source_file + "\n\n\t" + self.language_texts["destination_file"]

				# Show the verbose text
				self.Verbose(verbose_text, destination_file, verbose = True)

				return False

		# If the file exists and the source file is the same as the destination file
		else:
			return False

	def Contents(self, file):
		# Sanitize the file path
		file = self.Sanitize(file)

		# Define the contents dictionary
		contents = {
			"lines": [],
			"string": "",
			"size": 0,
			"length": 0
		}

		# If the file exists
		if self.Exists(file) == True:
			# Open the file handle in read mode (the default mode)
			file_handle = self.File_Open(file)

			# Iterate through the lines inside the file
			for line in file_handle.readlines():
				# Remove the line break from the line
				line = line.replace("\n", "")

				# Add the line to the list of lines
				contents["lines"].append(line)

			# Reset cursor to the beginning of the file before getting the file string
			file_handle.seek(0)

			# Read the file and get its string
			contents["string"] = file_handle.read()

			# Close the file handle
			file_handle.close()

			# Get the size of the file
			contents["size"] += os.path.getsize(file)

			# Get the length of the file
			contents["length"] = len(contents["lines"])

		# Temporary:
		# Add the title case to the "Lines", "String", and "Length" keys
		for key in ["Lines", "String", "Length"]:
			contents[key] = contents[key.lower()]

		# If the file does not exist
		if self.Exists(file) == False:
			# Show the verbose text saying that the file does not exist and thus can not be [checked]
			self.Verbose(self.language_texts["this_file_does_not_exist"], file)

		# Return the contents dictionary
		return contents

	def Edit(self, file, text, mode = "w", next_line = True, verbose = None, full_verbose = False):
		# Sanitize the file path
		file = self.Sanitize(file)

		# Get the contents of the file
		contents = self.Contents(file)

		# Define a shortcut to the file length
		length = contents["Length"]

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
				edit = self.File_Open(file, mode)

				# Write the text into the file
				edit.write(text)

				# Close the file handle
				edit.close()

				# Define the show text to tell the user that the file was edited
				show_text = self.Language.language_texts["file, title()"] + " " + self.Language.language_texts["edited, masculine"]

			# If the file "Edit" switch is False
			if self.switches["File"]["Edit"] == False:
				# Define the show text to tell the user that it was not possible to edit the file due to the lack of permissions
				show_text = self.Language.language_texts["it_was_not_possible_to_{}_the_file_permission_not_granted"].format(self.Language.language_texts["edit"])

			# If the file text string is not equal to the parameter text
			if contents["String"] != text:
				# Show the verbose text
				self.Verbose(show_text, file_text, verbose = verbose)

			# If the file "Edit" switch is True, return True
			if self.switches["File"]["Edit"] == True:
				return True

			# If the file "Edit" switch is False, return False
			if self.switches["File"]["Edit"] == False:
				return False

		# If the file does not exist
		if self.Exists(file) == False:
			# Show the verbose text saying that the file does not exist and thus can not be edited
			self.Verbose(self.language_texts["this_file_does_not_exist"], file_text)

			return False

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
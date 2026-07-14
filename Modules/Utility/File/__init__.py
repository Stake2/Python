# File.py

# Import some useful modules
import os
import shutil

# Define the main "File" class
class File():
	def __init__(self):
		# Define the variables of the class
		self.Define_Variables()

	def Define_Variables(self):
		import importlib

		# Define the list of modules to be imported
		classes = [
			"Modules",
			"Global_Switches",
			"JSON"
		]

		# Iterate through the list of classes to import
		for class_title in classes:
			# Import the module of the class
			module = importlib.import_module("." + class_title, "Utility")

			# Get the class object inside the module
			class_object = getattr(module, class_title)

			# If the class title is not "Modules"
			if class_title != "Modules":
				# Run the class object to define its attributes
				class_object = class_object()

			# Add the class object to the root class
			setattr(self, class_title, class_object)

		# ---------- #

		# Define the "Language" class as the same class inside the "JSON" class
		self.Language = self.JSON.Language

		# ---------- #

		# Define the module dictionary and the module folders and files
		self.Modules(class_object = self, utility_mode = True)

		# ---------- #

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

		# ---------- #

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

	def Split_Text(self, file):
		# Sanitize the file
		file = self.Sanitize(file)

		# Split it
		text = os.path.splitext(os.path.basename(file))

		# Return the text
		return text

	def Name(self, file):
		# Get the file name
		file_name = self.Split_Text(file)[0]

		# Return it
		return file_name

	def Extension(self, file, remove_dot = False):
		# Get the file extension with the dot
		file_extension = self.Split_Text(file)[1]

		# If the "remove dot" parameter is True
		if remove_dot == True:
			# Remove the dot
			file_extension = file_extension[1:]

		# Return the file extension
		return file_extension

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
			print(self.module["Module"] + "." + runner_method_name + "():")

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

		# Define the source and destination file texts
		file_text = self.language_texts["source_file"] + ":\n\t" + source_file + "\n\n\t" + self.language_texts["destination_file"]

		# If the file exists
		# And the "Copy" file switch is True
		if (
			self.Exists(source_file) == True and
			self.switches["File"]["Copy"] == True
		):
			# Copy the file to the destination folder
			shutil.copy(source_file, destination_file)

			# Show the verbose text saying that the file was copied
			self.Verbose(file_text, destination_file)

			return True

		# If the "Copy" file switch is False
		if self.switches["File"]["Copy"] == False:
			# Define the verbose text to tell the user that the file was not copied due to the lack of permissions
			verbose_text = self.Language.language_texts["it_was_not_possible_to_{}_the_file_permission_not_granted"].format(self.language_texts["copy"]) + "." + "\n\n\t" + file_text

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
			# Define the source and destination file texts
			file_text = self.language_texts["source_file"] + ":\n\t" + source_file + "\n\n\t" + self.language_texts["destination_file"]

			# And the "Move" file switch is True
			if self.switches["File"]["Move"] == True:
				# Move the file to the destination folder
				shutil.move(source_file, destination_file)

				# Show the verbose text saying that the file was moved
				self.Verbose(file_text, destination_file)

				return True

			# If the "Move" file switch is False
			if self.switches["File"]["Move"] == False:
				# Define the verbose text to tell the user that the file was not copied due to the lack of permissions
				verbose_text = self.Language.language_texts["it_was_not_possible_to_{}_the_file_permission_not_granted"].format(self.language_texts["move"]) + "." + "\n\n\t" + file_text

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

		# Create a shortcut to the file length
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

	def Text_From_List(self, items, genders = [], language = None, lower = False, next_line = True, and_text = True, or_text = False, quotes = False):
		# Define the text initially as an empty string
		text = ""

		# Define the texts dictionary as the "language texts" dictionary of the "Language" utility class
		texts = self.Language.language_texts

		# If the "language" parameter is not None
		if language != None:
			# Define the texts dictionary as the "texts" dictionary of the "Language" utility class
			texts = self.Language.texts

		# Iterate through the indexes and items inside the list of items
		for index, item in enumerate(items):
			# Create a backup of the item
			item_backup = item

			# If the list of genders is not empty
			if genders != []:
				# Get the current gender
				gender = genders[index]

				# Define the text key for the prefix as the "of_{}" text
				text_key = "of_{}"

				# Get the prefix text using the text key
				prefix_text = texts[text_key]

				# If the "language" parameter is not None
				if language != None:
					# Get the text in the correct language
					prefix_text = prefix_text[language]

				# If the current gender is inside the prefix text
				if gender in prefix_text:
					# Get the text in the currrent gender
					prefix_text = prefix_text[gender]

			# If the item backup is the last one inside the list
			# And the "next line" parameter is False
			if (
				item_backup == items[-1] and
				next_line == False
			):
				# If the list of items is two or greater than two
				if (
					len(items) == 2 or
					len(items) > 2
				):
					# Define the separator text as an empty string
					separator_text = ""

					# If the "and text" parameter is True, define the separator text as "and"
					if and_text == True:
						separator_text = texts["and"]

					# If the "or text" parameter is True, define the separator text as "or"
					if or_text == True:
						separator_text = texts["or"]

					# If the "language" parameter is not None
					# And the separator text is not empty
					if (
						language != None and
						separator_text != ""
					):
						# Get the separator text in the correct language
						separator_text = separator_text[language]

					# If the separator is not empty, add the separator to the text first
					if separator_text != "":
						text += separator_text + " "

			# If the "lower" parameter is True, then convert the item into lowercase
			if lower == True:
				item = item.lower()

			# If the "quotes" parameter is True, add quotes around the item
			if quotes == True:
				item = '"' + item + '"'

			# If the list of genders is not empty
			if genders != []:
				# If the "language" parameter is not English
				# Or it is
				# And the item is the first one
				if (
					language != "en" or
					language == "en" and
					index == 0
				):
					# Format the item using the prefix text
					item = prefix_text.format(item)

			# If the item index is not the last one inside the list
			# And the "next line" parameter is False
			if (
				index != len(items) - 1 and
				next_line == False
			):
				# If the number of items is two
				if len(items) == 2:
					# Add a space to the end of the item
					item += " "

				# If the number of items is greater than two
				if len(items) > 2:
					# Add a comma and a space to the end of the item
					item += ", "

			# If the item index is not the last one inside the list
			# And the "next line" parameter is True
			if (
				index < len(items) - 1 and
				next_line == True
			):
				# Add a line break to the item
				item += "\n"

			# If the item backup is an empty string
			# And the "next line" parameter is True
			if (
				item_backup == "" and
				next_line == True
			):
				# Define the item as the line break
				item = "\n"

			# Add the item to the text
			text += item

		# Return the full text
		return text

	def Dictionary_2(self, file, convert_lists_into_texts = False, convert_single_lists = False):
		# Sanitize the file path
		file = self.Sanitize(file)

		# Get the contents of the file
		contents = self.Contents(file)

		# Get the list of lines of the file
		lines = contents["Lines"]

		# Define the empty dictionary
		dictionary = {}

		# Define the current key as an empty string
		current_key = ""

		# Iterate through the list of lines of the file
		for line in lines:
			# If the line is not empty and it ends with a colon
			if line.endswith(":"):
				# Define the current key as the line
				current_key = line.replace(":", "")

				# Create the list inside the current key
				dictionary[current_key] = []

			# If the line is not a key
			# And the current key is defined
			elif current_key != "":
				# Add the line to the current list
				dictionary[current_key].append(line)

		# Iterate through the keys and values
		for key, value in dictionary.items():
			# If the last line inside the value is an empty string
			if value[-1] == "":
				# Remove it
				value.pop(-1)

			# If the "convert lists into texts" parameter is True
			if convert_lists_into_texts == True:
				# Convert the value list into a text
				value = self.Text_From_List(value)

			# If the "convert single lists" parameter is True
			# And the number of items inside the value is only one
			if (
				convert_single_lists == True and
				len(value) == 1
			):
				# Update the value to be only the first item
				value = value[0]

			# Update the value inside the root dictionary to be local value
			dictionary[key] = value

		# Return the dictionary
		return dictionary
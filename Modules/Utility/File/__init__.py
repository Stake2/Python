# File.py

import os

class File():
	def __init__(self):
		from Utility.Global_Switches import Global_Switches as Global_Switches

		# Global Switches dictionary
		self.switches = Global_Switches().switches["global"]

		self.switches.update({
			"file": {
				"create": True,
				"delete": True,
				"copy": True,
				"move": True,
				"edit": True
			}
		})

		if self.switches["testing"] == True:
			for switch in self.switches["file"]:
				self.switches["file"][switch] = False

		# Define module folders
		from Utility.Define_Folders import Define_Folders as Define_Folders

		Define_Folders(self)

		from Utility.JSON import JSON as JSON

		self.JSON = JSON()

		self.Define_Texts()

	def Define_Texts(self):
		self.texts = self.JSON.To_Python(self.folders["apps"]["module_files"]["utility"][self.module["key"]]["texts"])

		self.language_texts = self.JSON.Language.Item(self.texts)

	def Sanitize(self, path, restricted_characters = False):
		if restricted_characters == False:
			path = os.path.normpath(path).replace("\\", "/")

		if restricted_characters == True:
			restricted_characters = [":", "?", '"', "\\", "/", "|", "*", "<", ">"]

			for character in restricted_characters:
				if character in path:
					path = path.replace(character, "")

		return path

	def Name(self, file):
		file = self.Sanitize(file)

		return os.path.splitext(os.path.basename(file))[0]

	def Verbose(self, text, item, verbose = False):
		if self.switches["verbose"] == True or verbose == True:
			import inspect

			print()
			print(self.module["name"] + "." + inspect.stack()[1][3] + "():")
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

		if self.switches["file"]["create"] == True and self.Exist(file) == False:
			create = open(file, "w", encoding = "utf8")
			create.close()

			self.Verbose(self.language_texts["file, title()"] + " " + self.language_texts["created, masculine"], file)

			return True

		if self.switches["file"]["create"] == False:
			self.Verbose(self.language_texts["it_was_not_possible_to_{}_the_file_permission_not_granted"].format(self.language_texts["create"]) + "." + "\n\n\t" + self.language_texts["file, title()"], file)

			return False

	def Delete(self, file):
		file = self.Sanitize(file)

		if self.Exist(file) == False:
			self.Verbose(self.language_texts["this_file_does_not_exists"], file)

			return False

		if self.switches["file"]["delete"] == True and self.Exist(file) == True:
			os.remove(file)

			self.Verbose(self.language_texts["file, title()"] + " " + self.language_texts["deleted, masculine"], file)

			return True

		if self.switches["file"]["delete"] == False:
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

		if self.switches["file"]["copy"] == True and self.Exist(source_file) == True:
			import shutil
			shutil.copy(source_file, destination_file)

			self.Verbose(self.language_texts["source_file"] + ":\n" + source_folder + "\n\n" + self.language_texts["destination_file"], destination_folder)

			return True

		if self.switches["file"]["copy"] == False:
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

		if self.switches["file"]["move"] == True and self.Exist(source_file) == True:
			import shutil
			shutil.move(source_file, destination_file)

			self.Verbose(self.language_texts["source_file"] + ":\n" + source_file + "\n\n" + self.language_texts["destination_file"], destination_file)

			return True

		if self.switches["file"]["move"] == False:
			self.Verbose(self.language_texts["it_was_not_possible_to_{}_the_file_permission_not_granted"].format(self.language_texts["move"]) + "." + "\n\n\t" + self.language_texts["source_file"] + ":\n\t" + source_file + "\n\n\t" + self.language_texts["destination_file"], destination_file, verbose = True)

			return False

	def Text_From_List(self, list_, break_line = True, separator = ""):
		string = ""

		i = 0
		for item in list_:
			string += item

			if i != len(list_) - 1:
				if separator != "":
					string += separator

				if break_line == True:
					string += "\n"

			i += 1

		return string

	def Text_Difference(self, file_text, text_lines_to_write):
		if type(file_text) == dict:
			file_text = file_text["lines"]

		if type(text_lines_to_write) == str:
			text_lines_to_write = text_lines_to_write.splitlines()

		# Make the text difference between the text inside the file and the text to be written
		text_difference = []

		line_text = self.JSON.Language.language_texts["line, title()"]

		template = "\t\t" + line_text + " {}:"

		text_lines_number = str(len(text_lines_to_write))
		file_lines_number = len(file_text)

		i = 0
		for line in text_lines_to_write:
			add = False

			# If the number of file lines is greater than or equal to number of text lines
			# Or the number of file lines is lesser than the number of text lines
			if (
				len(file_text) >= len(text_lines_to_write) or \
				len(file_text) < len(text_lines_to_write)
			):
				# If the number of file lines is greater than or equal to number of text lines
				if len(file_text) >= len(text_lines_to_write):
					# And the current file line is not the same as the text line
					if file_text[i] != text_lines_to_write[i]:
						# Add the line to the text difference list
						add = True

					# And the line is not inside the file lines list or the line is empty
					if line not in file_text or line == "":
						# Add the line to the text difference list
						add = True

				# If the number of file lines is lesser than the number of text lines
				if len(file_text) < len(text_lines_to_write):
					# And the line is not inside the file lines list or the line is empty
					if line not in file_text or line == "":
						# Add the line to the text difference list
						add = True

				# Add the line to the text difference list
				if add == True:
					number_string = str(i + 1)

					if len(text_lines_to_write) < len(file_text):
						number_string = str(file_lines_number + 1)

						file_lines_number += 1

					while len(number_string) < len(text_lines_number):
						number_string = " " + number_string

					line = template.format(number_string) + " " + line

					# If the "i" number is greater than the number of file lines
					# Or the number of text lines is lesser than the number of file lines
					# Add the "+ " text to show that it is a new line
					if (i + 1) > len(file_text) or len(text_lines_to_write) < len(file_text):
						symbol = "+"

					# If the "i" number is lesser than or equal to the number of file lines
					# And the number of text lines is greater than the number of file lines
					# Add the "~ " text to show that it is a modified line
					if (i + 1) <= len(file_text) and len(text_lines_to_write) > len(file_text):
						symbol = "~"

					line = line.replace(line_text, symbol + " " + line_text)

					# Add the line to the text difference list
					text_difference.append(line)

			i += 1

		text_difference = self.Text_From_List(text_difference)

		return text_difference

	def Edit(self, file, text, mode = "w", next_line = True, verbose = None):
		file = self.Sanitize(file)

		contents = self.Contents(file)
		length = contents["length"]

		line_break = ""

		if next_line == True and length != 0 and mode == "a":
			line_break = "\n"

		text_backup = text

		text = line_break + text

		maximum_lines = 20

		# If the number of lines is lesser or equal to the maximum number of lines to show
		# Or the file is empty
		# Show the full text to be written (text inside file plus new text)
		if len(contents["lines"]) <= maximum_lines or contents["lines"] == []:
			verbose_text = self.JSON.Language.language_texts["text, title()"] + ":\n[" + text + "]"

		# If the number of lines is greater than the maximum number of lines to show
		# And the file is not empty
		# Show only the text difference
		if len(contents["lines"]) > maximum_lines and contents["lines"] != []:
			# Make the text difference between the text inside the file and the text to be written
			text_difference = self.Text_Difference(contents, text_backup)

			verbose_text = self.JSON.Language.language_texts["text_difference"] + ":\n\t[\n" + text_difference + "\n\t]"

		file_text = file + "\n\n\t" + verbose_text

		if self.Exist(file) == True:
			if self.switches["file"]["edit"] == True and contents["string"] != text:
				edit = open(file, mode, encoding = "UTF8")
				edit.write(text)
				edit.close()

				show_text = self.language_texts["file, title()"] + " " + self.language_texts["edited, masculine"]

			if self.switches["file"]["edit"] == False:
				show_text = self.language_texts["it_was_not_possible_to_{}_the_file_permission_not_granted"].format(self.language_texts["edit"])

			if contents["string"] != text:
				self.Verbose(show_text, file_text, verbose = verbose)

			if self.switches["file"]["edit"] == True:
				return True

			if self.switches["file"]["edit"] == False:
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

		if next_line == True and dictionary_separators == ": ":
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

		if self.switches["testing"] == False or open == True:
			os.startfile(item)

	def Close(self, program):
		import psutil

		for process in (process for process in psutil.process_iter() if program.split("\\")[program.count("\\")] in process.name()):
			process.kill()
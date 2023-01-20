# File.py

from Global_Switches import Global_Switches as Global_Switches

from Language import Language as Language
from JSON import JSON as JSON

import os
import re
import subprocess
import shutil
import psutil

class File():
	def __init__(self, parameter_switches = None, show_global_switches = False):
		# Global Switches dictionary
		self.global_switches = Global_Switches().global_switches

		self.global_switches.update({
			"file": {
				"create": True,
				"delete": True,
				"copy": True,
				"move": True,
				"edit": True,
			},
		})

		if parameter_switches != None:
			self.global_switches.update(parameter_switches)

			if "testing" in self.global_switches and self.global_switches["testing"] == True:
				for switch in self.global_switches["file"]:
					self.global_switches["file"][switch] = False

		self.Language = Language(self.global_switches, show_global_switches = show_global_switches)
		self.JSON = JSON(self.global_switches)

		self.Define_Folders()
		self.Define_Texts()

	def Define_Folders(self):
		self.app_text_files_folder = self.Language.app_text_files_folder

		self.module = {
			"name": self.__module__,
		}

		if "." in self.module["name"]:
			self.module["name"] = self.module["name"].split(".")[0]

		if self.module["name"] == "__main__":
			self.module["name"] = "File"

		self.module_text_files_folder = self.app_text_files_folder + self.module["name"] + "/"

		self.texts_file = self.module_text_files_folder + "Texts.json"

	def Define_Texts(self):
		self.texts = self.JSON.To_Python(self.texts_file)

		self.language_texts = self.Language.Item(self.texts)

	def Sanitize(self, path, restricted_characters = False):
		if restricted_characters == False:
			path = os.path.normpath(path).replace("\\", "/")

		if restricted_characters == True:
			restricted_characters = [":", "?", '"', "\\", "/", "|", "*", "<", ">"]

			for character in restricted_characters:
				if character in path:
					path = path.replace(character, "")

		return path

	def Verbose(self, text, item, verbose = False):
		if self.global_switches["verbose"] == True or verbose == True:
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

		if self.global_switches["file"]["create"] == True and self.Exist(file) == False:
			create = open(file, "w", encoding = "utf8")
			create.close()

			self.Verbose(self.language_texts["file, title()"] + " " + self.language_texts["created, masculine"], file)

			return True

	def Delete(self, file):
		file = self.Sanitize(file)

		if self.Exist(file) == False:
			self.Verbose(self.language_texts["this_file_does_not_exists"], file)

			return False

		if self.global_switches["file"]["delete"] == True and self.Exist(file) == True:
			os.remove(file)

			self.Verbose(self.language_texts["file, title()"] + " " + self.language_texts["deleted, masculine"], file)

			return True

		else:
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

		if self.global_switches["file"]["copy"] == True and self.Exist(source_file) == True:
			shutil.copy(source_file, destination_file)

			self.Verbose(self.language_texts["source_file"] + ":\n" + source_folder + "\n\n" + self.language_texts["destination_file"], destination_folder)

			return True

		else:
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

		if self.global_switches["file"]["move"] == True and self.Exist(source_file) == True:
			shutil.move(source_file, destination_file)

			self.Verbose(self.language_texts["source_file"] + ":\n" + source_file + "\n\n" + self.language_texts["destination_file"], destination_file)

			return True

		else:
			self.Verbose(self.language_texts["it_was_not_possible_to_{}_the_file_permission_not_granted"].format(self.language_texts["move"]) + "." + "\n\n\t" + self.language_texts["source_file"] + ":\n\t" + source_file + "\n\n\t" + self.language_texts["destination_file"], destination_file, verbose = True)

			return False

	def Edit(self, file, text, mode, next_line = True, parameter_switches = None):
		if parameter_switches != None:
			self.__init__(parameter_switches)

		file = self.Sanitize(file)

		contents = self.Contents(file)
		length = contents["length"]

		line_break = ""

		if next_line == True and length != 0 and mode == "a":
			line_break = "\n"

		text = line_break + text

		file_text = file + "\n\n\t" + self.language_texts["text, title()"] + ":\n[" + text + "]"

		if self.Exist(file) == True:
			if self.global_switches["file"]["edit"] == True and contents["string"] != text:
				edit = open(file, mode, encoding = "UTF8")
				edit.write(text)
				edit.close()

				show_text = self.language_texts["file, title()"] + " " + self.language_texts["edited, masculine"]

			if self.global_switches["file"]["edit"] == False:
				show_text = self.language_texts["it_was_not_possible_to_{}_the_file_permission_not_granted"].format(self.language_texts["edit"])

			if contents["string"] != text:
				self.Verbose(show_text, file_text)

			if self.global_switches["file"]["edit"] == True:
				return True

			if self.global_switches["file"]["edit"] == False:
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

	def Open(self, file):
		file = self.Sanitize(file)

		os.startfile(file)

	def Close(self, program):
		for process in (process for process in psutil.process_iter() if program.split("\\")[program.count("\\")] in process.name()):
			process.kill()
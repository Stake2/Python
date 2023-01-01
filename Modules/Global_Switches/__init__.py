# Global_Switches.py

import os
import pathlib
import platform
import re
import json

class Global_Switches():
	def __init__(self, parameter_switches = None):
		# Global Switches dictionary
		self.global_switches = {}

		self.Define_Folders()

		self.dictionary = self.JSON_To_Python(self.switches_file)

		for key in self.dictionary:
			changed_key = key.lower().replace(" ", "_")

			value = self.dictionary[key]

			if value in ["True", "true", "Yes", "yes", "Sim", "sim"]:
				value = True

			if value in ["False", "false", "No", "no", "Não", "não"]:
				value = False

			self.global_switches[changed_key] = value

	def Define_Folders(self):
		self.hard_drive_letter = os.path.normpath(pathlib.Path.home().drive) + "/"

		if platform.release() == "10":
			self.hard_drive_letter = "D:/"

		self.apps_folder = self.hard_drive_letter + "Apps/"
		self.app_text_files_folder = self.apps_folder + "Module Files/"

		name = __name__

		if "." in __name__:
			name = __name__.split(".")[0]

		if name == "__main__":
			name = "Global_Switches"

		self.module_text_files_folder = self.app_text_files_folder + name + "/"

		self.switches_file = self.module_text_files_folder + "Switches.json"

	def Sanitize(self, path, restricted_characters = False):
		if restricted_characters == False:
			path = os.path.normpath(path).replace("\\", "/")

		if restricted_characters == True:
			restricted_characters = [":", "?", '"', "\\", "/", "|", "*", "<", ">"]

			for character in restricted_characters:
				if character in path:
					path = path.replace(character, "")

		return path

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

		return dictionary

	def JSON_To_Python(self, file):
		file = self.Sanitize(file)

		dictionary = json.load(open(file, encoding = "utf8"))

		return dictionary
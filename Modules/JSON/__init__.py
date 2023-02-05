# JSON.py

from Global_Switches import Global_Switches as Global_Switches

from Language import Language as Language

import os
import locale
import re
import pathlib
import json
import platform

class JSON():
	def __init__(self, parameter_switches = None, show_global_switches = False):
		# Global Switches dictionary
		self.global_switches = Global_Switches().global_switches

		self.global_switches.update({
			"file": {
				"create": True,
				"edit": True
			}
		})

		if parameter_switches != None:
			self.global_switches.update(parameter_switches)

			if "testing" in self.global_switches and self.global_switches["testing"] == True:
				for switch in self.global_switches["file"]:
					self.global_switches["file"][switch] = False

		self.Language = Language(self.global_switches)

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
			self.module["name"] = "Input"

		self.module_text_files_folder = self.app_text_files_folder + self.module["name"] + "/"

		self.texts_file = self.module_text_files_folder + "Texts.json"

	def Define_Texts(self):
		self.texts = self.To_Python(self.texts_file)

		self.language_texts = self.Language.Item(self.texts)

	def Sanitize(self, path):
		path = os.path.normpath(path).replace("\\", "/")

		if "/" not in path[-1] and os.path.splitext(path)[-1] == "":
			path += "/"

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

	def Create(self, file):
		file = self.Sanitize(file)

		if self.Exist(file) == True:
			return False

		if self.global_switches["file"]["create"] == True and self.Exist(file) == False:
			create = open(file, "w", encoding = "utf8")
			create.close()

			self.Verbose(self.language_texts["file, title()"] + " " + self.language_texts["created, masculine"], file)

			return True

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

	def Edit(self, file, text, next_line = True, parameter_switches = None):
		if parameter_switches != None:
			self.__init__(parameter_switches)

		file = self.Sanitize(file)

		contents = self.Contents(file)

		text = self.From_Python(text)

		file_text = file + "\n\n\t" + self.language_texts["text, title()"] + ":\n[" + text + "]"

		if self.Exist(file) == True:
			if self.global_switches["file"]["edit"] == True and contents["string"] != text:
				edit = open(file, "w", encoding = "UTF8")
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

	def From_Python(self, items):
		if type(items) != str:
			import types as Types

			for key in items:
				value = items[key]

				if type(value) not in [str, int, list, dict, bool, None]:
					items[key] = str(value)

		if type(items) == str:
			items = self.To_Python(items)

		return json.dumps(items, indent = 4, ensure_ascii = False)

	def To_Python(self, item):
		if os.path.isfile(item) == True:
			item = self.Sanitize(item)

			dictionary = json.load(open(item, encoding = "utf8"))

		if os.path.isfile(item) == False:
			dictionary = json.loads(item)

		return dictionary

	def Show(self, json):
		print(self.From_Python(json))
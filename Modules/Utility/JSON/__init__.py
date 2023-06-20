# JSON.py

import os

class JSON():
	def __init__(self):
		from Utility.Global_Switches import Global_Switches as Global_Switches

		# Global Switches dictionary
		self.switches = Global_Switches().switches["global"]

		self.switches.update({
			"file": {
				"create": True,
				"edit": True
			}
		})

		if self.switches["testing"] == True:
			for switch in self.switches["file"]:
				self.switches["file"][switch] = False

		# Define module folders
		from Utility.Define_Folders import Define_Folders as Define_Folders

		Define_Folders(self)

		self.folders["apps"]["module_files"]["utility"]["date"] = {
			"texts": self.folders["apps"]["module_files"]["utility"]["root"] + "Date/Texts.json"
		}

		from Utility.Language import Language as Language

		self.Language = Language()

		self.Define_Texts()

	def Define_Texts(self):
		self.texts = self.To_Python(self.folders["apps"]["module_files"]["utility"][self.module["key"]]["texts"])
		self.date_texts = self.To_Python(self.folders["apps"]["module_files"]["utility"]["date"]["texts"])

		self.language_texts = self.Language.Item(self.texts)

	def Sanitize(self, path):
		path = os.path.normpath(path).replace("\\", "/")

		if "/" not in path[-1] and os.path.splitext(path)[-1] == "":
			path += "/"

		return path

	def Verbose(self, text, item, verbose = None):
		if self.switches["verbose"] == True and verbose == None or verbose == True:
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

		line_text = self.Language.language_texts["line, title()"]

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

	def Edit(self, file, text, next_line = True, verbose = None):
		file = self.Sanitize(file)

		contents = self.Contents(file)

		text = self.From_Python(text)

		maximum_lines = 20

		# If the number of lines is lesser or equal to the maximum number of lines to show
		# Or the file is empty
		# Show the full text to be written (text inside file plus new text)
		if len(contents["lines"]) <= maximum_lines or contents["lines"] == []:
			verbose_text = self.Language.language_texts["text, title()"] + ":\n[" + text + "]"

		# If the number of lines is greater than the maximum number of lines to show
		# And the file is not empty
		# Show only the text difference
		if len(contents["lines"]) > maximum_lines and contents["lines"] != []:
			# Make the text difference between the text inside the file and the text to be written
			text_difference = self.Text_Difference(contents, text)

			verbose_text = self.Language.language_texts["text_difference"] + ":\n\t[\n" + text_difference + "\n\t]"

		file_text = file + "\n\n\t" + verbose_text

		if self.Exist(file) == True:
			if self.switches["file"]["edit"] == True and contents["string"] != text:
				edit = open(file, "w", encoding = "UTF8")
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

	def Show(self, json):
		print(self.From_Python(json))

	def Add_Key_After_Key(self, dictionary, key_value, after_key = None, number_to_add = 1, add_to_end = False):
		keys = list(dictionary.keys())
		values = list(dictionary.values())

		i = 0
		for key in keys.copy():
			if key_value["key"] not in keys and key == after_key or add_to_end == True:
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

		return dictionary
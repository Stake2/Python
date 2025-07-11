# Input.py

import re

class Input():
	def __init__(self):
		# Import the classes
		self.Import_Classes()

		# Define the folders of the module
		self.Define_Folders(object = self, files = ["Switches"])

		# Define the texts of the module
		self.Define_Texts()

	def Import_Classes(self):
		import importlib

		# ---------- #

		# Define the list of modules to be imported
		modules = [
			"Define_Folders",
			"Global_Switches",
			"File",
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

		# Import some variables from the "Language" class

		# Import the "languages" dictionary
		self.languages = self.Language.languages

	def Define_Texts(self):
		# Define the "Texts" dictionary
		self.texts = self.JSON.To_Python(self.module["Files"]["Texts"])

		# Define the "Language texts" dictionary
		self.language_texts = self.Language.Item(self.texts)

	def Select(self, options, language_options = None, show_text = None, select_text = None, add_colon = True, select_text_colon = True, function = True, first_space = True):
		from copy import deepcopy

		if (
			show_text != None and
			add_colon == True and
			show_text[-1] + show_text[-2] != ": " and
			show_text[-1] != "?"
		):
			show_text += ": "

		if (
			select_text != None and
			select_text[-1] + select_text[-2] != ": "
		):
			if (
				add_colon == True or
				select_text_colon == True
			):
				select_text += ": "

		if show_text == None:
			show_text = self.language_texts["options, title()"] + ": "

		if select_text == None:
			select_text = self.language_texts["select_an_option_from_the_list"] + ": "

		if first_space == True:
			print()

		print(show_text)

		list_ = options.copy()

		if language_options != None:
			list_ += language_options.copy()

		numbers = []

		text = ""

		i = 0
		for option in options:
			if language_options != None:
				option = language_options[i]

				if type(option) == str:
					list_.append(option.lower())
					list_.append(option[0].lower())

			if (
				"\n" in option and
				len(text) >= 2 and
				text[-2] + text[-1] != "\n\n"
			):
				text += "\n"

			if type(option) == dict:
				option = self.JSON.Show(deepcopy(option), return_text = True)

			text += "[" + str(i + 1) + "]" + " - " + option

			if option != options[-1]:
				text += "\n"

			if (
				"\n" in option and
				text[-2] + text[-1] != "\n\n"
			):
				text += "\n"

			numbers.append(i)
			numbers.append(str(i))

			i += 1

		if text[-1] != "\n":
			text += "\n"

		print(text)

		letters = []

		for option in options:
			if type(option) == str:
				letters.append(option[0].lower())

		list_ += letters
		list_ += numbers

		option = ""

		while option in ["", " "]:
			option = input(select_text)

		found_option = False

		try:
			option = int(option)
			option_number = option - 1
			self.option_number_backup = option_number

			try:
				option = options[option_number]
				found_option = True

			except IndexError:
				option = 1000

				while option not in list_:
					try:
						option = int(input(select_text))

					except ValueError:
						option = str(option)

				option_number = option - 1
				option = options[option_number]
				found_option = True

		except ValueError:
			option = str(option)

			while option not in list_:
				option = input(select_text)

				try:
					option = int(option)
					option_number = option - 1

				except ValueError:
					option = str(option)

		possible_options = [option]

		if type(option) == str and found_option == False:
			possible_options.extend([
				str(option),
				str(option.lower()),
				str(option.title()),
				str(option.capitalize()),
				str(option.lower().title()),
				str(option.title()),
				str(option.capitalize())
			])

		i = 0
		for possible_option in possible_options:
			if type(possible_option) == str and found_option == False:
				if language_options != None:
					for option_ in language_options:
						if re.findall(possible_option, option_, re.IGNORECASE) != []:
							option = option_

							found_option = True

				if language_options == None:
					for option_ in options:
						if re.findall(possible_option, option_, re.IGNORECASE) != []:
							option = option_

							found_option = True
			i += 1

		if type(option) == str:
			i = 0
			for option_ in options:
				if option == option_:
					option_number = i

				i += 1

		dictionary = {
			"option": option,
			"language_option": option,
			"Language option": option,
			"number": option_number,
			"Number": option_number,
			"Option": {
				"Original": option,
				"Language": option,
				"Number": option_number
			}
		}

		if hasattr(self, "option_number_backup") == True:
			dictionary["number_backup"] = self.option_number_backup

		if language_options != None:
			dictionary["language_option"] = language_options[dictionary["number"]]

			dictionary["Option"]["Language"] = language_options[dictionary["Option"]["Number"]]

		if found_option == True:
			print()
			print(self.language_texts["you_selected_this_option"] + ":")

			if (
				language_options != None and
				str(option) != dictionary["language_option"]
			):
				print("\t" + dictionary["language_option"])

				if type(option) == dict:
					option = self.JSON.Show(deepcopy(option), return_text = True)

				print("\t" + str(option))

			if (
				language_options == None or
				str(option) == dictionary["language_option"]
			):
				print("\t" + str(option))

			if (
				function == True and
				type(option) in [function, type]
			):
				option()

		return dictionary

	def Define_Yes_Or_No(self, response, inverse = False):
		# Define the list of yes answers
		yes_answers = [
			"Yes",
			"yes",
			self.language_texts["yes, title()"],
			self.language_texts["yes, title()"].lower()
		]

		# Define the list of no answers
		no_answers = [
			"No",
			"no",
			self.language_texts["no, title()"],
			self.language_texts["no, title()"].lower()
		]

		# If the inverse parameter is False
		if inverse == False:
			# If the response is in the list of yes answers, return True
			if response in yes_answers:
				return True

			# If the response is in the list of no answers, return False
			if response in no_answers:
				return False

		# If the inverse parameter is True
		if inverse == True:
			# If the response is True, return "Yes"
			if response == True:
				return "Yes"

			# If the response is False, return "No"
			if response == False:
				return "No"

	def Yes_Or_No(self, question, convert_to_text = False, first_space = True):
		options = [
			self.language_texts["yes, title()"],
			self.language_texts["no, title()"]
		]

		if type(question) == dict:
			question = self.Language.Item(question)

		if "?" not in question:
			question += "?"

		option = self.Select(options, show_text = question, select_text = self.language_texts["select_{}_or_{}_(number_or_word)"], first_space = first_space, add_colon = False)["option"]

		option = self.Define_Yes_Or_No(option)

		if convert_to_text == True:
			if option == True:
				option = self.language_texts["yes, title()"]

			if option == False:
				option = self.language_texts["no, title()"]

		return option

	def Type(self, text = None, add_colon = True, accept_enter = True, next_line = False, tab = "", regex = None, first_space = True):
		if text == None:
			text = self.language_texts["type_or_paste_the_text"]

		if (
			add_colon == True and
			":" not in text[-1] and
			text[-2] + text[-1] != ": " and
			text[-1] != "\n" and
			text[-1] != "\t"
		):
			text += ": "

		if isinstance(text, dict):
			text = self.Language.Item(text)

		if first_space == True:
			print()

		local_text = text

		if next_line == True:
			print(text)

			local_text = ""

		if (
			isinstance(regex, str) and
			"; " in regex
		):
			split = regex.split("; ")

			regex = {
				"Regex": split[0],
				"Example": split[1]
			}

		if accept_enter == True:
			typed = input(tab + local_text)

		if accept_enter == False:
			typed = ""

			i = 0
			while typed == "":
				if i != 0:
					print()
					print(text)

				typed = input(tab + local_text)

				if i == 0:
					i += 1

		if (
			regex != None and
			regex["Regex"] != "" and
			accept_enter == False
		):
			search = re.search(regex["Regex"], typed)

			while search == None:
				new_text = text

				if ": " in text:
					example_text = self.Language.language_texts["example, title()"] + ': "' + regex["Example"] + '"'

					try:
						int(regex["Example"])

						example_text += ", " + self.Language.language_texts["length, title()"] + ": " + str(len(regex["Example"]))

					except ValueError:
						pass

					new_text = new_text.replace(": ", " (" + example_text + "):")

					if next_line == True:
						new_text += "\n" + tab

				typed = self.Type(new_text, next_line, accept_enter = False, first_space = first_space)

				search = re.search(regex["Regex"], typed)

		return typed

	def Capitalize(self, text):
		text = list(text)
		text[0] = text[0].upper()
		text = "".join(text)

		return text

	def Lines(self, show_text_parameter = None, length = None, line_options_parameter = None, line_texts = [], accept_enter = True, no_space = False, backup_file = None, first_space = True, second_space = False):
		show_text = show_text_parameter

		if show_text_parameter == None:
			show_text = self.language_texts["type_the_lines_of_text"] + ": "

		line_options = {
			"print": False,
			"enumerate": False,
			"enumerate_text": False,
			"capitalize": False,
			"dots": False,
			"show_finish_text": True,
			"next_line": True,
			"colon": True,
			"first_space": first_space,
			"second_space": second_space
		}

		if line_options_parameter != None:
			for key in line_options:
				if key in line_options_parameter:
					line_options[key] = line_options_parameter[key]

		finish_keywords = self.language_texts["finish_keywords, type: list"]

		last_text_items = ["?", "!", ":", ";", "."]

		if line_options["first_space"] == True:
			print()

		if (
			line_options["next_line"] == True and
			line_options["enumerate"] == False
		):
			text = show_text

			if ":" not in text:
				text += ":"

			print(text)

		if (
			length == None and
			line_options["show_finish_text"] == True
		):
			keywords = str(finish_keywords).replace("'", '"').replace("[", "").replace("]", "")

			print("--------------------")
			print()
			print("(" + self.language_texts["to_finish_typing_please_type_one_of_the_texts_below"] + ":")
			print(keywords + ")")

		if show_text_parameter == None:
			print()
			print("--------------------")

		if (
			length == None and
			line_options["show_finish_text"] == True and
			show_text_parameter != None and
			show_text_parameter[0] != "\n" and
			line_options["second_space"] == True
		):
			print()

		contents = {
			"lines": [],
			"string": "",
			"length": 0
		}

		line = ""

		i = 0
		while (
			line not in finish_keywords and
			contents["length"] != length
		):
			if (
				line_options["next_line"] == True or
				line_options["enumerate"] == True
			):
				if (
					line_options["enumerate"] == True and
					i == 0
				):
					print(show_text)

				type_text = ""

				if (
					length != None and
					length != 1
				):
					type_text += "\n"

				if line_options["enumerate"] == True:
					type_text += str(contents["length"] + 1)

				if length != None:
					type_text += "/" + str(length)

				if (
					line_options["enumerate"] == True and
					line_texts == [] and
					":" not in type_text or
					length != None and
					line_texts == [] and
					":" not in type_text
				):
					type_text += ": "

				if line_texts != []:
					type_text += " - " + line_texts[i] + ":\n"

			if (
				line_options["next_line"] == False and
				line_options["enumerate"] == False
			):
				if line_options["print"] == False:
					if line == "":
						type_text = show_text

					if line != "":
						type_text = ""

				if (
					line == "" and
					line_options["print"] == True
				):
					if line_options["show_finish_text"] == True:
						print()

					print(show_text)

					type_text = ""

			line = self.Type(type_text, add_colon = False, first_space = False)

			if line not in finish_keywords:
				if line != "":
					if (
						"capitalize" in line_options and
						line_options["capitalize"] == True
					):
						line = self.Capitalize(line)

					if (
						line_options["dots"] == True and
						line[-1] not in last_text_items
					):
						line += "."

				if (
					"enumerate_text" in line_options and
					line_options["enumerate_text"] == True
				):
					line = str(contents["length"] + 1) + ": " + line

				if (
					accept_enter == False and
					line != "" or
					accept_enter == True
				):
					contents["lines"].append(line)

					if backup_file != None:
						self.File.Edit(backup_file, line, "a")

					if (
						length == None or
						length != None and
						contents["length"] != length - 1
					):
						line += "\n"

					contents["string"] += line

					contents["length"] += 1

			i += 1

		if (
			contents["string"] != "" and
			"\n" in contents["string"][-1]
		):
			contents["string"] = contents["string"][:-1]

		if show_text_parameter == None:
			print("--------------------")
			print()
			print(self.language_texts["you_finished_typing_the_lines_of_text"] + ".")

		return contents
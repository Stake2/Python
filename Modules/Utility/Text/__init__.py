# Text.py

import os

class Text():
	def __init__(self):
		# Import the classes
		self.Import_Classes()

		# Define the folders of the module
		self.Define_Folders(object = self,)

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

		# ---------- #

		# Define the "Language" class as the same class inside the "JSON" class
		self.Language = self.JSON.Language

	def Define_Switches(self):
		# Define the "Switches" dictionary
		self.switches = {
			"Verbose": True
		}

	def Verbose(self, text, item, verbose = True):
		if (
			self.switches["Verbose"] == True or
			verbose == True
		):
			import inspect

			print()
			print(self.module["Name"] + "." + inspect.stack()[1][3] + "():")
			print("\t" + text + ":")
			print("\t" + item)

	def Define_Texts(self):
		# Define the "Texts" dictionary
		self.texts = self.JSON.To_Python(self.module["Files"]["Texts"])

		# Define the "Language texts" dictionary
		self.language_texts = self.Language.Item(self.texts)

	def Add_Leading_Zeroes(self, number):
		if int(number) <= 9:
			number = str("0" + str(number))

		return number

	def Remove_Leading_Zeroes(self, number):
		# If the number is lesser than or equal to nine
		# And the zero number is inside the number
		if (
			int(number) <= 9 and
			"0" in str(number)
		):
			# Remove the zero number
			number = str(number)[1:]

		# Return the number
		return number

	def By_Number(self, number, singular, plural):
		# If the type of the number is a list
		if type(number) == list:
			# Define it as the length of the list
			number = len(number)

		# If the number is lesser than or equal to one
		if int(number) <= 1:
			# Define the text as the singular one
			text = singular

		# If the number is greater than or equal to two
		if int(number) >= 2:
			# Define the text as the plural one
			text = plural

		# Return the defined text
		return text

	def Lower(self, text):
		return text.lower()

	def Replace(self, text, replace, with_):
		return text.replace(replace, with_)

	def Title(self, text):
		return text.title()

	def Capitalize(self, text, lower = False):
		text = list(text)

		if lower == False:
			text[0] = text[0].upper()

		if lower == True:
			text[0] = text[0].lower()

		text = "".join(text)

		return text

	def Copy(self, text, verbose = True):
		# If the text is a list, convert it to a text
		if type(text) == list:
			text = self.From_List(text, next_line = True)

		# If the text is a dictionary, convert it to a text
		if type(text) == dict:
			text = self.From_Dictionary(text)

		# Import the "pyperclip" module
		import pyperclip

		# Copy the text
		pyperclip.copy(text)

		# Show the verbose text about the copied text
		self.Verbose(self.Language.language_texts["copied_text"], "[" + text + "]", verbose = verbose)

	def From_List(self, list_, language = None, lower = False, next_line = False, and_text = True, or_text = False, quotes = False):
		text = ""

		text_list = self.Language.language_texts

		if language != None:
			text_list = self.Language.texts

		for item in list_:
			item_backup = item

			if (
				item_backup == list_[-1] and
				next_line == False
			):
				if (
					len(list_) > 2 or
					len(list_) == 2
				):
					separator_text = ""

					if and_text == True:
						separator_text = text_list["and"]

					if or_text == True:
						separator_text = text_list["or"]

					if (
						language != None and
						separator_text != ""
					):
						separator_text = separator_text[language]

					if separator_text != "":
						text += separator_text + " "

			if lower == True:
				item = item.lower()

			if quotes == True:
				item = '"' + item + '"'

			if (
				item_backup != list_[-1] and
				next_line == False
			):
				if len(list_) == 2:
					item += " "

				if len(list_) > 2:
					item += ", "

			if (
				item_backup != list_[-1] and
				next_line == True
			):
				item += "\n"

			if (
				item_backup == "" and
				next_line == True
			):
				item = "\n"

			text += item

		return text

	def From_Dictionary(self, dictionary, break_line = True, next_line = False):
		keys = list(dictionary.keys())
		values = list(dictionary.values())

		string = ""

		i = 0
		for value in values:
			key = keys[i]

			string += key + ": "

			if next_line == True:
				string = string[:-1] + "\n"

			string += str(value)

			if (
				key != keys[-1] and
				break_line == True
			):
				string += "\n"

				if next_line == True:
					string += "\n"

			i += 1

		return string

	def Has_Duplicates(self, item_list):
		return len(item_list) != len(set(item_list))

	def Get_Clipboard(self): 
		# Import the "win32clipboard" module
		import win32clipboard

		# Open the clipboard
		win32clipboard.OpenClipboard()

		# Get the clipboard data
		data = win32clipboard.GetClipboardData()

		# Close the clipboard
		win32clipboard.CloseClipboard()

		# Return the data
		return data
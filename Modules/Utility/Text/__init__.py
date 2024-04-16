# Text.py

import os

class Text():
	def __init__(self):
		# Define module folders
		from Utility.Define_Folders import Define_Folders as Define_Folders

		self.switches = {
			"verbose": True
		}

		Define_Folders(self)

		from Utility.JSON import JSON as JSON

		self.JSON = JSON()

		# Define the "Language" class as the same class inside the "JSON" class
		self.Language = self.JSON.Language

		self.Define_Texts()

	def Verbose(self, text, item, verbose = True):
		if (
			self.switches["verbose"] == True and
			verbose == True
		):
			import inspect

			print()
			print(self.module["name"] + "." + inspect.stack()[1][3] + "():")
			print("\t" + text + ":")
			print("\t" + item)

	def Define_Texts(self):
		self.texts = self.JSON.To_Python(self.folders["apps"]["module_files"]["utility"][self.module["key"]]["texts"])

		self.language_texts = self.Language.Item(self.texts)

	def Add_Leading_Zeroes(self, number):
		if int(number) <= 9:
			number = str("0" + str(number))

		return number

	def Remove_Leading_Zeroes(self, number):
		if int(number) <= 9 and "0" in str(number):
			number = str(number)[1:]

		return number

	def By_Number(self, number, singular, plural):
		if type(number) == list:
			number = len(number)

		if int(number) <= 1:
			text = singular

		if int(number) >= 2:
			text = plural

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
		if type(text) == list:
			text = self.From_List(text, break_line = True)

		if type(text) == dict:
			text = self.From_Dictionary(text)

		import pyperclip

		pyperclip.copy(text)

		self.Verbose(self.language_texts["copied_text"], "[" + text + "]", verbose = verbose)

	def Old_From_List(self, list_, break_line = True, separator = "", and_text = True):
		string = ""

		i = 0
		for item in list_:
			string += item

			if i != len(list_) - 1:
				if separator != "":
					string += separator

				if break_line == True:
					string += "\n"

			if (
				i == len(list_) - 2 and
				and_text == True
			):
				string += self.Language.language_texts["and"] + " "

			i += 1

		return string

	def From_List(self, list_, language = None, lower = False, break_line = False, and_text = True, or_text = False, quotes = False):
		text = ""

		text_list = self.Language.language_texts

		if language != None:
			text_list = self.Language.texts

		for item in list_:
			item_backup = item

			if (
				item_backup == list_[-1] and
				break_line == False
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

			text += item

			if (
				item_backup != list_[-1] and
				break_line == False
			):
				if len(list_) == 2:
					text += " "

				if len(list_) > 2:
					text += ", "

			if (
				item_backup != list_[-1] and
				break_line == True
			):
				text += "\n"

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

			if key != keys[-1] and break_line == True:
				string += "\n"

				if next_line == True:
					string += "\n"

			i += 1

		return string

	def Get_Clipboard(self): 
		import win32clipboard

		win32clipboard.OpenClipboard()
		data = win32clipboard.GetClipboardData()
		win32clipboard.CloseClipboard()

		return data

	def Open_Link(self, link):
		import webbrowser

		self.Verbose(self.language_texts["opening, title()"], link, verbose = True)

		webbrowser.open(link)
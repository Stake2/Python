# Text.py

import os
import pathlib
import pyperclip
import webbrowser
import win32clipboard

class Text():
	def __init__(self):
		# Get modules dictionary
		self.modules = self.Modules.Set(self, ["JSON", "Language"])

		self.switches["global"].update({
			"verbose": True
		})

		self.Define_Folders(self)

		self.Define_Texts()

	def Verbose(self, text, item, verbose = True):
		if self.switches["global"]["verbose"] == True and verbose == True:
			import inspect

			print()
			print(self.module["name"] + "." + inspect.stack()[1][3] + "():")
			print("\t" + text + ":")
			print("\t" + item)

	def Define_Texts(self):
		self.texts = self.JSON.To_Python(self.folders["apps"]["module_files"]["utility"][self.module["key"]]["texts"])

		self.language_texts = self.Language.Item(self.texts)

	def Add_Leading_Zeros(self, number):
		if int(number) <= 9:
			number = str("0" + str(number))

		return number

	def Remove_Leading_Zeros(self, number):
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
			text = self.From_List(text)

		if type(text) == dict:
			text = self.From_Dictionary(text)

		pyperclip.copy(text)

		self.Verbose(self.language_texts["copied_text"], "[" + text + "]", verbose = verbose)

	def From_List(self, list_, break_line = True, separator = ""):
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
		win32clipboard.OpenClipboard()
		data = win32clipboard.GetClipboardData()
		win32clipboard.CloseClipboard()

		return data

	def Open_Link(self, link):
		webbrowser.open(link)
# System.py

import os

class System():
	def __init__(self):
		# Define module folders
		from Utility.Define_Folders import Define_Folders as Define_Folders

		from Utility.Global_Switches import Global_Switches as Global_Switches

		# Global Switches dictionary
		self.switches = Global_Switches().switches["Global"]

		Define_Folders(self)

		from Utility.JSON import JSON as JSON

		self.JSON = JSON()

		self.Define_Texts()

	def Define_Texts(self):
		self.texts = self.JSON.To_Python(self.folders["apps"]["module_files"]["utility"][self.module["key"]]["texts"])

		self.language_texts = self.JSON.Language.Item(self.texts)

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

	def Sanitize(self, path, restricted_characters = False):
		if restricted_characters == False:
			path = os.path.normpath(path).replace("\\", "/")

		if restricted_characters == True:
			self.restricted_characters_list = [":", "?", '"', "\\", "/", "|", "*", "<", ">"]

			for character in self.restricted_characters_list:
				if character in path:
					path = path.replace(character, "")

		return path

	def Open(self, item, open = False):
		if "https" not in item:
			item = self.Sanitize(item)

		self.Verbose(self.language_texts["opening, title()"], item, verbose = True)

		if (
			self.switches["testing"] == False or
			open == True
		):
			os.startfile(item)

	def Close(self, program):
		import psutil

		for process in (process for process in psutil.process_iter() if program.split("\\")[program.count("\\")] in process.name()):
			process.kill()

	def Open_Link(self, link):
		import webbrowser

		webbrowser.open(link)
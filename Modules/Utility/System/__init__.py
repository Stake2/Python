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
		import inspect

		verbose_text = "\n" + \
		self.module["name"] + "." + inspect.stack()[1][3] + "():" + "\n" + \
		"\t" + text + ":" + "\n" + \
		"\t" + item

		if (
			self.switches["verbose"] == True or
			verbose == True
		):
			print(verbose_text)

		return verbose_text

	def Sanitize(self, path, restricted_characters = False):
		if restricted_characters == False:
			path = os.path.normpath(path).replace("\\", "/")

			if (
				os.path.splitext(path)[-1] == "" and
				"/" not in path[-1]
			):
				path += "/"

		if restricted_characters == True:
			self.restricted_characters_list = [":", "?", '"', "\\", "/", "|", "*", "<", ">"]

			for character in self.restricted_characters_list:
				if character in path:
					path = path.replace(character, "")

		return path

	def Open(self, item, open = False, verbose = True):
		if (
			"http" not in item and
			"https" not in item
		):
			item = self.Sanitize(item)

		verbose_text = self.Verbose(self.language_texts["opening, title()"], item, verbose = verbose)

		if (
			self.switches["testing"] == False or
			open == True
		):
			os.startfile(item)

		return verbose_text

	def Close(self, program):
		import psutil

		for process in (process for process in psutil.process_iter() if program.split("\\")[program.count("\\")] in process.name()):
			process.kill()

	def Open_Link(self, link):
		import webbrowser

		self.Verbose(self.language_texts["opening, title()"], link, verbose = True)

		webbrowser.open(link)

	def Variable_Name(self, variable):
		import inspect

		callers_local_vars = inspect.currentframe().f_back.f_locals.items()

		variable_name = [variable_name for variable_name, variable_value in callers_local_vars if variable_value is variable]

		print()
		print("-----")
		print()
		print("Name:")
		print(variable_name)
		print()
		print("Type:")
		print(type(variable))
		print()
		print("-----")

		return variable_name
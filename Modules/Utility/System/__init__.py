# System.py

import os

class System():
	def __init__(self):
		# Import the classes
		self.Import_Classes()

		# Define the folders of the module
		self.Define_Folders(object = self)

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

		# Define the "Language" class as the same class inside the "JSON" class
		self.Language = self.JSON.Language

	def Define_Switches(self):
		# Get the "Switches" dictionary from the "Global_Switches" module
		self.switches = self.Global_Switches.switches["Global"]

	def Define_Texts(self):
		# Define the "Texts" dictionary
		self.texts = self.JSON.To_Python(self.module["Files"]["Texts"])

		# Define the "Language texts" dictionary
		self.language_texts = self.Language.Item(self.texts)

	def Verbose(self, text, item, verbose = True):
		import inspect

		verbose_text = "\n" + \
		self.module["Name"] + "." + inspect.stack()[1][3] + "():" + "\n" + \
		"\t" + text + ":" + "\n" + \
		"\t" + item

		if (
			self.switches["Verbose"] == True or
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
			self.switches["Testing"] == False or
			open == True
		):
			os.startfile(item)

		return verbose_text

	def Close(self, program):
		import psutil

		for process in (process for process in psutil.process_iter() if program.split("\\")[program.count("\\")] in process.name()):
			if self.switches["Testing"] == False:
				process.kill()

	def Open_Link(self, link, verbose = True):
		import webbrowser

		self.Verbose(self.language_texts["opening, title()"], link, verbose = verbose)

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
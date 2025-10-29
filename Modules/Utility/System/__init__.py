# System.py

import os
import win32com.client
import subprocess
import sys

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

		# ---------- #

		# Define the list of modules to be imported
		modules = [
			"Define_Folders",
			"Global_Switches",
			"JSON",
			"File"
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

		# Import the "system" dictionary from the "Language" class
		self.system = self.Language.system

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
		# Import the validators module
		import validators

		# If the item is not a link
		if validators.url(item) == False:
			# Sanitize the item
			item = self.Sanitize(item)

		# Show the verbose text about opening the item
		verbose_text = self.Verbose(self.language_texts["opening, title()"], item, verbose = verbose)

		# If the "Testing" switch is False
		# Or the "open" parameter is True
		if (
			self.switches["Testing"] == False or
			open == True
		):
			# Start the item
			os.startfile(item)

		# Return the verbose text
		return verbose_text

	def Open_Link(self, link, browser = "", verbose = True):
		# If the "browser" parameter is empty
		if browser == "":
			# Then define it as "Mozilla Firefox"
			browser = "Mozilla Firefox"

		# Get the browser dictionary from the system "Browsers" dictionary
		browser = self.system["Browsers"][browser]

		# Show the verbose text about opening the link
		verbose_text = self.Verbose(self.language_texts["opening, title()"], link, verbose = verbose)

		# Open the link using the selected browser
		subprocess.Popen([browser["File"], link])

		# Return the verbose text
		return verbose_text

	def Close(self, program):
		import psutil

		for process in (process for process in psutil.process_iter() if program.split("\\")[program.count("\\")] in process.name()):
			if self.switches["Testing"] == False:
				process.kill()

	def Define_Shortcut(self, dictionary):
		# Initiate the shell
		shell = win32com.client.Dispatch("wscript.shell")

		# Define the shortcut dictionary
		shortcut = {
			"Name": "",
			"Folder": "",
			"File": "",
			"Extension": "",
			"Target": ""
		}

		# Iterate through the keys inside the shortcut dictionary
		for key in shortcut:
			# If the key is inside the parameter dictionary
			if key in dictionary:
				# Define the key inside the shortcut dictionary as the one in the parameter one
				shortcut[key] = dictionary[key]

		# If the "Target" key is in the parameter dictionary
		if "Target" in dictionary:
			# If the "://" text is not in the shortcut target
			if "://" not in dictionary["Target"]:
				# Sanitize the target path
				shortcut["Target"] = self.Sanitize(shortcut["Target"])

				# Define the extension as "lnk" (link)
				shortcut["Extension"] = "lnk"

			else:
				# Define the extension as "url"
				shortcut["Extension"] = "url"

			# If the "Name" key is an empty string
			if shortcut["Name"] == "":
				# Get the name of the file path
				shortcut["Name"] = self.File.Name(shortcut["Target"])

			# If the "Folder" key is not present in the parameter dictionary
			if "Folder" not in dictionary:
				shortcut["Folder"] = self.File.Folder(shortcut["Target"])

		# If the target is not present
		else:
			# Create the shortcut with the file path
			shortcut_file = shell.CreateShortCut(shortcut["File"])

			# Get the name of the file path
			shortcut["Name"] = self.File.Name(shortcut["File"])

			# Get the target path from the already existing shortcut
			shortcut["Target"] = self.Sanitize(shortcut_file.TargetPath)

			# Get the extension from the file path
			shortcut["Extension"] = "." + dictionary["File"].split(".")[-1]

			# Define the folder of the shortcut
			shortcut["Folder"] = self.File.Folder(shortcut["File"])

		# Return the shortcut dictionary
		return shortcut

	def Create_Shortcut(self, dictionary):
		# Define the shortcut dictionary
		shortcut = self.Define_Shortcut(dictionary)

		# Update the "File" key
		shortcut["File"] = shortcut["Folder"] + shortcut["Name"] + "." + shortcut["Extension"]

		# Initiate the shell
		shell = win32com.client.Dispatch("wscript.shell")

		# Create the shortcut with the file path
		shortcut_file = shell.CreateShortCut(shortcut["File"])

		# Define the target path
		shortcut_file.TargetPath = dictionary["Target"]

		# Save the shortcut
		shortcut_file.Save()

		# Return the shortcut dictionary
		return shortcut

	def Get_Shortcut(self, shortcut):
		# Define the shortcut dictionary
		shortcut = self.Define_Shortcut(shortcut)

		# Return the shortcut dictionary
		return shortcut

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
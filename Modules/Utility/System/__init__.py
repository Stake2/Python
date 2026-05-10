# System.py

import os
import win32com.client
import subprocess
import time

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
			"Folder",
			"File",
			"JSON",
			"Text"
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

			# Add the sub-class to the current class
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

	def Verbose(self, text, item = None, verbose = None, first_space = True, item_tab = "\t"):
		# If the "Verbose" switch is True
		# And the verbose parameter is None
		# Or the verbose parameter is True
		if (
			self.switches["Verbose"] == True and
			verbose == None or
			verbose == True
		):
			import inspect

			# Get the name of the method which ran this method (the "Verbose" one)
			runner_method_name = inspect.stack()[1][3]

			# If the "first space" parameter is True
			if first_space == True:
				# Show the first space separator
				print()

			# Show the module name (Text) and the method which ran this method (the "Verbose" one)
			print(self.module["Name"] + "." + runner_method_name + "():")

			# If the tab is not in the text, add it
			if "\t" not in text[0]:
				text = "\t" + text

			# Show the verbose text
			print(text + ":")

			# If the item is not None, show it
			if item != None:
				# Show the verbose item with the item tab
				print(item_tab + item)

	def Open(self, item, open = False, commands = [], verbose = True, first_space = True):
		# Import the validators module
		import validators

		# Define the text key as "link"
		text_key = "link"

		# Define the gender initially as masculine
		gender = "masculine"

		# Define the verbose version of the item
		verbose_item = item

		# If the item is not a link
		if bool(validators.url(item)) == False:
			# Sanitize the item as a file
			item = self.File.Sanitize(item)

			# If the item is a folder
			if self.Folder.Exists(item) == True:
				# Sanitize the item as a folder (to add the slash at the end)
				item = self.Folder.Sanitize(item)

				# Define the text key as "folder"
				text_key = "folder"

				# Change the gender to be feminine
				gender = "feminine"

			# If the item is a file
			if self.File.Exists(item) == True:
				# Define the text key as "file"
				text_key = "file"

				# Get the file extension without the dot
				extension = self.File.Extension(item, remove_dot = True)

				# If the file extension is "exe"
				if extension == "exe":
					# Define the item text key as "program"
					text_key = "program"

				# If the file extension is "url"
				if extension == "url":
					# Define the item text key as "link"
					text_key = "link"

				# If the file extension is "lnk"
				if extension == "lnk":
					# Define the item text key as "shortcut"
					text_key = "shortcut"

		# Define the verbose text based on the gender
		verbose_text = self.language_texts["opening_this_{}" + ", " + gender]

		# Get the item text using the text key
		item_text = self.Language.language_texts[text_key]

		# Format the verbose text with the item text
		verbose_text = verbose_text.format(item_text)

		# If the "commands" parameter is not an empty string
		if commands != []:
			# Add a colon, a line break, a tab, and the item to the verbose text
			verbose_text += ":" + "\n" + "\t" + item

			# Add two line breaks
			verbose_text += "\n\n"

			# Add a tab and the "With these commands" text in the user language
			verbose_text += "\t" + self.Language.language_texts["with_these_commands"]

			# Create the commands string
			commands_string = " ".join(commands)

			# Change the verbose item to be the commands string embraced in brackets
			verbose_item = "[" + commands_string + "]"

		# Show the verbose text about opening the item
		verbose_text = self.Verbose(verbose_text, verbose_item, verbose = verbose, first_space = first_space)

		# If the "Testing" switch is False
		# Or the "open" parameter is True
		if (
			self.switches["Testing"] == False or
			open == True
		):
			# If the "commands" parameter is an empty string
			if commands == []:
				# Start the item using the "os" class and its "startfile" method
				os.startfile(item)

			# If the "commands" parameter is not an empty string
			if commands != []:
				# Open the item using the "subprocess" class and its "Popen" method
				# And pass the item and the list of commands to the method
				subprocess.Popen([item] + commands)

		# Return the verbose text
		return verbose_text

	def Open_Link(self, link, browser = "", verbose = True):
		# If the "browser" parameter is empty
		if browser == "":
			# Then define it as "Mozilla Firefox"
			browser = "Mozilla Firefox"

		# Get the browser dictionary from the system "Browsers" dictionary
		browser = self.system["Browsers"][browser]

		# Define the verbose text as "Opening this link" and the link
		verbose_text = "\t" + self.language_texts["opening_this_link"] + ":" + "\n" + \
		"\t" + link

		# Add the "Using this browser" text
		verbose_text += "\n\n" + \
		"\t" + self.language_texts["using_this_browser"]

		# Show the verbose text with the browser name
		verbose_text = self.Verbose(verbose_text, browser["Name"], verbose = verbose)

		# If the "Testing" switch is False
		if self.switches["Testing"] == False:
			# Open the link using the selected browser
			subprocess.Popen([browser["File"], link])

		# Return the verbose text
		return verbose_text

	def Close(self, programs_to_close, close = None, verbose = True, first_space = True):
		import psutil

		# Define the local list of attributes to get
		attributes = [
			"name"
		]

		# If the list of programs to close is a string
		if type(programs_to_close) == str:
			# Define it as a list containing only the string
			programs_to_close = [
				programs_to_close
			]

		# Define a local list of program names
		program_names = []

		# Iterate through the list of programs to close and their numbers
		for program_number, program in enumerate(programs_to_close):
			# Add ".exe" to the end of the program
			program += ".exe"

			# Update the program in the list
			programs_to_close[program_number] = program

			# Add the program to the list of program names
			program_names.append(program)

		# Define the verbose text as "Closing this program"
		verbose_text = self.language_texts["closing_this_program"]

		# Define the program text as the first program name
		program_text = program_names[0]

		# Define the item tab as a tab
		item_tab = "\t"

		# If the number of programs to close is greater than one
		if len(programs_to_close) > 1:
			# Update the verbose text to be "Closing these programs"
			verbose_text = self.language_texts["closing_these_programs"]

			# Update the program text to be the list of program names converted into a text, with the tab prefix
			program_text = self.Text.From_List(program_names, prefix = "\t")

			# Do not add a tab to the item in the "Verbose" method
			item_tab = ""

		# Define a local "found program" switch initially as False
		found_program = False

		# Iterate through the list of processes
		for process in psutil.process_iter(attrs = attributes):
			# Create a shortcut to the process name
			process_name = process.info["name"]

			# If the process name is inside the list of programs to close
			if process_name in programs_to_close:
				# If the number of programs to close is one
				# Or it greater than one
				# And the local "found program" switch is False
				if (
					len(programs_to_close) == 1 or
					len(programs_to_close) > 1 and
					found_program == False
				):
					# Show the verbose text about closing the program(s)
					verbose_text = self.Verbose(verbose_text, program_text, verbose = verbose, first_space = first_space, item_tab = item_tab)

				# If the "Testing" switch is False
				# And the close parameter is None
				# Or the close parameter is True
				if (
					self.switches["Testing"] == False and
					close == None or
					close == True
				):
					# Terminate the process
					process.terminate()

				# Change the local "found program" switch to True
				found_program = True

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
				# Define the key inside the shortcut dictionary as the one in the parameter dictionary
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
				# Define it as the target file name
				shortcut["Name"] = self.File.Name(shortcut["Target"])

			# If the "Folder" key is not present in the parameter dictionary
			if "Folder" not in dictionary:
				# Define it as the folder of the target file
				shortcut["Folder"] = self.File.Folder(shortcut["Target"])

		# If the "Target" key is not present
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
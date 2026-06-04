# Global_Switches.py

# Import some useful modules
import os
import json

# Define the main "Global_Switches" class
class Global_Switches():
	def __init__(self):
		# Define the variables of the class
		self.Define_Variables()

		# Define the "Switches" dictionary
		self.Define_Switches()

	def Define_Variables(self):
		import importlib

		# Define the classes to be imported
		classes = [
			"Modules"
		]

		# Iterate through the list of classes to import
		for class_title in classes:
			# Import the module of the class
			module = importlib.import_module("." + class_title, "Utility")

			# Get the class object inside the module
			class_object = getattr(module, class_title)

			# Add the class object to the root class
			setattr(self, class_title, class_object)

		# ---------- #

		# Define the module dictionary and the module folders and files
		self.Modules(class_object = self, create_texts = False, utility_mode = True)

	def Define_Switches(self):
		# Define and create the "Switches.json" file
		self.module["Files"]["Switches"] = self.module["Folders"]["Files"]["root"] + "Switches.json"
		self.File_Create(self.module["Files"]["Switches"])

		# Define the root "switches" dictionary
		self.switches = {
			"Reset": {
				"Testing": False,
				"Verbose": False,
				"Show user information": False,
				"Has active switches": False
			},
			"Global": {},
			"File": self.module["Files"]["Switches"]
		}

		# If the "Switches.json" file is empty
		if self.File_Contents(self.switches["File"])["Lines"] == []:
			# Write the "Reset" switches dictionary to it
			self.Reset()

		# Get the "Global" switches dictionary
		self.switches["Global"] = self.JSON_To_Python(self.switches["File"])

		# Update it with the "File" dictionary
		self.switches["Global"].update({
			"File": {
				"Create": True,
				"Edit": True
			}
		})

		# Define the "Has active switches" switch as False
		self.switches["Global"]["Has active switches"] = False

		# Iterate through the switches inside the "Global" dictionary
		for switch in self.switches["Global"]:
			# If the switch is in the "Reset" switches
			# And is not equal to the reset switch (False)
			if (
				switch in self.switches["Reset"] and
				switch != self.switches["Reset"][switch]
			):
				# Define the "Has active switches" switch as True
				self.switches["Global"]["Has active switches"] = True

	def Sanitize(self, path):
		# Normalize the path and replace backslashes with forward slashes
		path = os.path.normpath(path).replace("\\", "/")

		# Return the path
		return path

	def File_Exists(self, file):
		# Sanitize the file path
		file = self.Sanitize(file)

		# Checks if the file exists and returns True if it does or False if it does not
		return os.path.isfile(file)

	def File_Open(self, file, mode = "r", encoding = "UTF8"):
		# Open the file with the mode and encoding
		return open(file, mode, encoding = encoding)

	def File_Create(self, file):
		# Sanitize the file path
		file = self.Sanitize(file)

		# If the file does not exist
		if self.File_Exists(file) == False:
			# Open the file handle in write mode to create it
			create = self.File_Open(file, "w")

			# Close the file handle
			create.close()

	def File_Contents(self, file):
		# Sanitize the file path
		file = self.Sanitize(file)

		# Define the contents dictionary
		contents = {
			"Lines": [],
			"String": ""
		}

		# If the file exists
		if self.File_Exists(file) == True:
			# Open the file handle in read mode (the default mode)
			file_handle = self.File_Open(file)

			# Iterate through the lines inside the file
			for line in file_handle.readlines():
				# Remove the line break from the line
				line = line.replace("\n", "")

				# Add the line to the list of lines
				contents["Lines"].append(line)

			# Reset cursor to the beginning of the file before getting the file string
			file_handle.seek(0)

			# Read the file and get its string
			contents["String"] = file_handle.read()

		# Return the contents dictionary
		return contents

	def JSON_To_Python(self, file):
		# Sanitize the file
		file = self.Sanitize(file)

		# Get the JSON dictionary
		dictionary = json.load(open(file, encoding = "utf8"))

		# Return the JSON dictionary
		return dictionary

	def JSON_From_Python(self, items):
		from copy import deepcopy

		# Make a copy of the items
		items = deepcopy(items)

		# Return the JSON version of the items
		return json.dumps(items, indent = 4, ensure_ascii = False)

	def JSON_Edit(self, file, text):
		# Sanitize the file path
		file = self.Sanitize(file)

		# Get the contents of the file
		contents = self.File_Contents(file)

		# Transform the text into the JSON format
		text = self.JSON_From_Python(text)

		# If the file exists
		# And the file text string is not equal to the parameter text
		if (
			self.File_Exists(file) == True and
			contents["String"] != text
		):
			# Open the file handle in write mode
			edit = self.File_Open(file, "w")

			# Write the text into the file
			edit.write(text)

			# Close the file handle
			edit.close()

	def Reset(self):
		# Reset the switches to the "Reset" switches dictionary
		self.JSON_Edit(self.switches["File"], self.switches["Reset"])

	def Switch(self, switches):
		# Get the reset switch keys
		reset_switch_keys = list(self.switches["Reset"].keys())

		# Iterate through the switches in the "switches" parameter
		for switch in switches.copy():
			# If the switch is not in the "reset switch keys" list
			if switch not in reset_switch_keys:
				# Remove the unneeded switch
				switches.pop(switch)

		# Switch the switches to the switches in the "switches" parameter
		self.JSON_Edit(self.switches["File"], switches)
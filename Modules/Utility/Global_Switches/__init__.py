# Global_Switches.py

import os

class Global_Switches():
	def __init__(self):
		# Import the classes
		self.Import_Classes()

		# Define the folders of the module
		self.Define_Folders(object = self, files = ["Switches"])

		# Define the "Switches" dictionary
		self.Define_Switches()

	def Import_Classes(self):
		import importlib

		# Define the list of modules to be imported
		modules = [
			"Define_Folders"
		]

		# Iterate through the list of modules
		for module_title in modules:
			# Import the module
			module = importlib.import_module("." + module_title, "Utility")

			# Get the sub-class
			sub_class = getattr(module, module_title)

			# Add the sub-class to the current module
			setattr(self, module_title, sub_class)

	def Define_Switches(self):
		# Define the "Switches" dictionary
		self.switches = {
			"Reset": {
				"Testing": False,
				"Verbose": False,
				"User information": False,
				"Has active switches": False
			},
			"Global": {},
			"File": self.module["Files"]["Switches"]
		}

		# Write the "Reset" switches dictionary into the "Switches.json" file if it is empty
		if self.Contents(self.switches["File"])["Lines"] == []:
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
		path = os.path.normpath(path).replace("\\", "/")

		return path

	def Exist(self, file):
		file = self.Sanitize(file)

		if os.path.isfile(file) == True:
			return True

		if os.path.isfile(file) == False:
			return False

	def JSON_To_Python(self, file):
		import json

		# Sanitize the file
		file = self.Sanitize(file)

		# Get the JSON dictionary
		dictionary = json.load(open(file, encoding = "utf8"))

		return dictionary

	def JSON_From_Python(self, items):
		# Import the needed modules
		import json
		from copy import deepcopy

		# Make a copy of the items
		items = deepcopy(items)

		# Return the JSON version of the items
		return json.dumps(items, indent = 4, ensure_ascii = False)

	def Contents(self, file):
		# Sanitize the file
		file = self.Sanitize(file)

		# Create the "Contents" dictionary
		contents = {
			"Lines": []
		}

		# If the file exists
		if self.Exist(file) == True:
			# Iterate through the lines in the file
			for line in open(file, "r", encoding = "utf8").readlines():
				# Replace the line breaks in the line
				line = line.replace("\n", "")

				# Add the line to the "Lines" key
				contents["Lines"].append(line)

		# Return the "Contents" dictionary
		return contents

	def Edit(self, file, text):
		# Sanitize the file
		file = self.Sanitize(file)

		# Transform the text into a JSON dictionary
		text = self.JSON_From_Python(text)

		# If the file exists
		if self.Exist(file) == True:
			# Edit the file with the text
			edit = open(file, "w", encoding = "UTF8")
			edit.write(text)
			edit.close()

	def Reset(self):
		# Reset the switches to the "Reset" switches dictionary
		self.Edit(self.switches["File"], self.switches["Reset"])

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
		self.Edit(self.switches["File"], switches)
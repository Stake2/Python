# Global_Switches.py

import os

class Global_Switches():
	def __init__(self):
		# Global Switches dictionary
		self.switches = {}

		# Define module folders
		from Utility.Define_Folders import Define_Folders as Define_Folders

		Define_Folders(self, ["Switches"])

		self.switches = {
			"Reset": {
				"testing": False,
				"verbose": False,
				"user_information": False,
				"Has active switches": False
			},
			"Global": {},
			"File": self.folders["apps"]["module_files"]["utility"][self.module["key"]]["switches"]
		}

		# Write into the "Switches.json" file if it is empty
		if self.Contents(self.switches["File"])["lines"] == []:
			self.Reset()

		self.switches["Global"] = self.JSON_To_Python(self.switches["File"])

		self.switches["Global"].update({
			"file": {
				"create": True,
				"edit": True
			}
		})

		self.switches["Global"]["Has active switches"] = False

		for switch in self.switches["Global"]:
			if (
				switch in self.switches["Reset"] and
				switch != self.switches["Reset"][switch]
			):
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

		file = self.Sanitize(file)

		dictionary = json.load(open(file, encoding = "utf8"))

		return dictionary

	def JSON_From_Python(self, items):
		import json
		from copy import deepcopy

		items = deepcopy(items)

		return json.dumps(items, indent = 4, ensure_ascii = False)

	def Contents(self, file):
		file = self.Sanitize(file)

		contents = {
			"lines": [],
			"lines_none": [None],
			"string": "",
			"size": 0,
			"length": 0
		}

		if self.Exist(file) == True:
			contents["string"] = open(file, "r", encoding = "utf8").read()
			contents["size"] += os.path.getsize(file)

			for line in open(file, "r", encoding = "utf8").readlines():
				line = line.replace("\n", "")

				contents["lines"].append(line)
				contents["lines_none"].append(line)

			contents["length"] = len(contents["lines"])

		return contents

	def Edit(self, file, text):
		file = self.Sanitize(file)

		text = self.JSON_From_Python(text)

		if self.Exist(file) == True:
			edit = open(file, "w", encoding = "UTF8")
			edit.write(text)
			edit.close()

	def Reset(self):
		self.Edit(self.switches["File"], self.switches["Reset"])

	def Switch(self, switches):
		switch_keys = list(self.switches["Reset"].keys())

		for switch in switches.copy():
			if switch not in switch_keys:
				switches.pop(switch)

		self.Edit(self.switches["File"], switches)
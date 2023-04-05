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
			"reset": {
				"testing": False,
				"verbose": False,
				"user_information": False
			},
			"global": {},
			"file": self.folders["apps"]["module_files"]["utility"][self.module["key"]]["switches"]
		}

		# Write into "Switches.json" file if it is empty
		if self.Contents(self.switches["file"])["lines"] == []:
			self.Reset()

		self.switches["global"] = self.JSON_To_Python(self.switches["file"])

		self.switches["global"].update({
			"file": {
				"create": True,
				"edit": True
			}
		})

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
			"length": 0,
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
		self.Edit(self.switches["file"], self.switches["reset"])

	def Switch(self, switches):

		for switch in switches.copy():
			if switch not in list(self.switches["reset"].keys()):
				switches.pop(switch)

		self.Edit(self.switches["file"], switches)
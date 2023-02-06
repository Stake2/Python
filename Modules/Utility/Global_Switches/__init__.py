# Global_Switches.py

import os
import pathlib
import platform
import re
import json
from copy import deepcopy

class Global_Switches():
	def __init__(self):
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

		self.switches["global"] = self.JSON_To_Python(self.switches["file"])

		self.switches["global"].update({
			"file": {
				"create": True,
				"edit": True
			}
		})

		self.export = [
			self.switches
		]

	def Sanitize(self, path):
		path = os.path.normpath(path).replace("\\", "/")

		return path

	def JSON_To_Python(self, file):
		file = self.Sanitize(file)

		dictionary = json.load(open(file, encoding = "utf8"))

		return dictionary

	def JSON_From_Python(self, items):
		items = deepcopy(items)

		return json.dumps(items, indent = 4, ensure_ascii = False)

	def Edit(self, file, text):
		file = self.Sanitize(file)

		text = self.JSON_From_Python(text)

		if os.path.isfile(file) == True:
			edit = open(file, "w", encoding = "UTF8")
			edit.write(text)
			edit.close()

	def Reset(self):
		self.Edit(self.switches["file"], self.switches["reset"])

	def Switch(self, switches):
		self.Edit(self.switches["file"], switches)
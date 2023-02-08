# Modules.py

import os
import importlib

class Modules(object):
	def __init__(self):
		# Define module folders
		from Utility.Define_Folders import Define_Folders as Define_Folders

		Define_Folders(self)

		self.Get()

	def Get(self):
		self.modules = self.JSON_To_Python(self.folders["apps"]["modules"]["modules"])

		for key in ["utility", "usage"]:
			self.modules[key]["list"] = sorted(self.modules[key]["list"], key=str.lower)

		self.Edit(self.folders["apps"]["modules"]["modules"], self.modules)

		for key in ["utility", "usage"]:
			for title in self.modules[key]["list"]:
				if title != "Modules":
					if key == "utility":
						tuple_ = "." + title, key.title()

					if key == "usage":
						tuple_ = title,

					self.modules[key][title] = {
						"title": title,
						"key": title.lower(),
						"list": [title.lower()],
						"text_key": "executes_the_{}_module",
						"module": importlib.import_module(*tuple_)
					}

					if key == "usage":
						try:
							self.modules[key][title]["sub_module"] = importlib.import_module("." + title, title)

						except ModuleNotFoundError:
							pass

	def Sanitize(self, path):
		path = os.path.normpath(path).replace("\\", "/")

		return path

	def Edit(self, file, text):
		file = self.Sanitize(file)

		text = self.JSON_From_Python(text)

		if os.path.isfile(file) == True:
			edit = open(file, "w", encoding = "UTF8")
			edit.write(text)
			edit.close()

	def JSON_From_Python(self, items):
		import json

		from copy import deepcopy

		items = deepcopy(items)

		return json.dumps(items, indent = 4, ensure_ascii = False)

	def JSON_To_Python(self, file):
		import json

		dictionary = json.load(open(file, encoding = "utf8"))

		return dictionary
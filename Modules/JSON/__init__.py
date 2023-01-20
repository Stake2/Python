# JSON.py

from Global_Switches import Global_Switches as Global_Switches

import os
import locale
import re
import pathlib
import json
import platform

class JSON():
	def __init__(self, parameter_switches = None, show_global_switches = False):
		# Global Switches dictionary
		self.global_switches = Global_Switches().global_switches

		self.global_switches.update({
			"file": {
				"create": True,
				"edit": True
			}
		})

		if parameter_switches != None:
			self.global_switches.update(parameter_switches)

	def Sanitize(self, path):
		path = os.path.normpath(path).replace("\\", "/")

		if "/" not in path[-1] and os.path.splitext(path)[-1] == "":
			path += "/"

		return path

	def Create(self, item = None, text = None):
		if item == None:
			item = self.Type(text)

		item = self.Sanitize(item)

		if os.path.splitext(item)[-1] == "":
			if self.global_switches["folder"]["create"] == True and os.path.isdir(item) == False:
				os.mkdir(item)

		if os.path.splitext(item)[-1] != "":
			if self.global_switches["file"]["create"] == True and os.path.isfile(item) == False:
				create = open(item, "w", encoding = "utf8")
				create.close()

		return item

	def Edit(self, file, text):
		file = self.Sanitize(file)

		text = self.From_Python(text)

		if self.global_switches["file"]["edit"] == True and os.path.isfile(file) == True:
			edit = open(file, "w", encoding = "UTF8")
			edit.write(text)
			edit.close()

	def From_Python(self, item):
		return json.dumps(item, indent = 4, ensure_ascii = False)

	def To_Python(self, file):
		file = self.Sanitize(file)

		dictionary = json.load(open(file, encoding = "utf8"))

		return dictionary

	def Show(self, json):
		print(self.From_Python(json))
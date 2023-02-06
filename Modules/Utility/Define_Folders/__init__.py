# Define_Folders.py

import os
import pathlib

class Define_Folders():
	def __init__(self, object = None, folder_names = []):
		if object != None:
			name = type(object).__name__

			self.module = {
				"name": name,
				"key": name.lower().replace(" ", "_")
			}

			self.folders = {
				"hard_drive_letter": os.path.normpath(pathlib.Path.home().drive) + "/",
			}

			self.folders["apps"] = {
				"root": self.folders["hard_drive_letter"] + "Apps/"
			}

			self.folders["apps"]["module_files"] = {
				"root": self.folders["apps"]["root"] + "Module Files/"
			}

			self.folders["apps"]["module_files"]["utility"] = {
				"root": self.folders["apps"]["module_files"]["root"] + "Utility/"
			}

			self.folders["apps"]["module_files"]["utility"][self.module["key"]] = {
				"root": self.folders["apps"]["module_files"]["utility"]["root"] + self.module["name"] + "/"
			}

			folder = self.folders["apps"]["module_files"]["utility"][self.module["key"]]["root"]

			self.folders["apps"]["module_files"]["utility"][self.module["key"]]["texts"] = folder + "Texts.json"

			self.folders["apps"]["modules"] = {
				"root": self.folders["apps"]["root"] + "Modules/"
			}

			self.folders["apps"]["modules"]["modules"] = self.folders["apps"]["modules"]["root"] + "Modules.json"

			folder_names.append("Texts")

			for item in folder_names:
				key = item.lower().replace(" ", "_")

				self.folders["apps"]["module_files"]["utility"][self.module["key"]][key] = folder + item + ".json"

			for key in ["module", "folders"]:
				value = getattr(self, key)

				setattr(object, key, value)
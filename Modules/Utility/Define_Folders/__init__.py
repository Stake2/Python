# Define_Folders.py

class Define_Folders():
	def __init__(self, object_to_define = None, folder_names = []):
		if object_to_define != None:
			import os
			import pathlib

			name = type(object_to_define).__name__

			if "." in object_to_define.__module__:
				if object_to_define.__module__.split(".")[0] == "Utility":
					name = object_to_define.__module__.split(".")[1]

				else:
					name = object_to_define.__module__.split(".")[0]

			if name == "Run":
				name = object_to_define.__module__.split(".")[0]

			self.module = {
				"name": name,
				"key": name.lower().replace(" ", "_")
			}

			if hasattr(object_to_define, "folders") == False:
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

				self.folders["apps"]["modules"] = {
					"root": self.folders["apps"]["root"] + "Modules/"
				}

			if hasattr(object_to_define, "folders") == True:
				self.folders = getattr(object_to_define, "folders")

			self.folders["apps"]["module_files"]["utility"][self.module["key"]] = {
				"root": self.folders["apps"]["module_files"]["utility"]["root"] + self.module["name"] + "/"
			}

			folder_key = ""

			if os.path.isdir(self.folders["apps"]["module_files"]["utility"][self.module["key"]]["root"]) == True:
				folder_key = "utility"

				self.folders["apps"]["modules"][folder_key] = {
					"root": self.folders["apps"]["modules"]["root"] + folder_key.title() + "/"
				}

				self.folders["apps"]["modules"][folder_key][self.module["key"]] = {
					"root": self.folders["apps"]["modules"][folder_key]["root"] + self.module["name"] + "/"
				}

				self.folders["apps"]["module_files"][folder_key][self.module["key"]] = {
					"root": self.folders["apps"]["module_files"][folder_key]["root"] + self.module["name"] + "/"
				}

				folder = self.folders["apps"]["module_files"][folder_key][self.module["key"]]["root"]

			else:
				self.folders["apps"]["module_files"].pop("utility")

				self.folders["apps"]["modules"][self.module["key"]] = {
					"root": self.folders["apps"]["modules"]["root"] + self.module["name"] + "/"
				}

				self.folders["apps"]["module_files"][self.module["key"]] = {
					"root": self.folders["apps"]["module_files"]["root"] + self.module["name"] + "/"
				}

			self.folders["apps"]["modules"]["modules"] = self.folders["apps"]["modules"]["root"] + "Modules.json"

			folder_names.append("Texts")

			for item in folder_names:
				key = item.lower().replace(" ", "_")

				if self.module["key"] in self.folders["apps"]["module_files"]:
					folder = self.folders["apps"]["module_files"][self.module["key"]]

				else:
					folder = self.folders["apps"]["module_files"][folder_key][self.module["key"]]

				folder[key] = folder["root"] + item + ".json"

			for key in ["module", "folders"]:
				value = getattr(self, key)

				setattr(object_to_define, key, value)
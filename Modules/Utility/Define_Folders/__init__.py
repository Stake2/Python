# Define_Folders.py

import os
import pathlib

class Define_Folders():
	def __init__(self, object = None, files = []):
		# Define the "Folders" dictionary
		self.Define_Folders()

		# Define the "object" and "files" parameters inside this class
		self.object = object

		# Define the files list with the "Texts" item,
		# And also add the values of the "files" parameter, if it is not an empty list
		self.files = [
			"Texts",
			*files
		]

		# Define the "Module" dictionary
		self.Define_Module()

	def Define_Folders(self):
		# Define the hard drive letter
		self.hard_drive_letter = os.path.normpath(pathlib.Path.home().drive) + "/"

		# Define the "Folders" dictionary
		self.folders = {
			"root": self.hard_drive_letter
		}

		# Define the "Apps" folder
		self.folders["Apps"] = {
			"root": self.folders["root"] + "Apps/"
		}

		# Define its sub-folders
		folders = [
			"Module files",
			"Modules"
		]

		# Iterate through the list of folders
		for folder in folders:
			# Define the folder dictionary
			self.folders["Apps"][folder] = {
				"root": self.folders["Apps"]["root"] + folder + "/"
			}

		# Define the "Utility" folders
		for folder in ["Modules", "Module files"]:
			self.folders["Apps"][folder]["Utility"] = {
				"root": self.folders["Apps"][folder]["root"] + "Utility/"
			}

		# Define the "Modules.json" file
		self.folders["Apps"]["Modules"]["Modules"] = self.folders["Apps"]["Modules"]["root"] + "Modules.json"

	def Define_Module(self):
		# Define the "Module" dictionary
		self.module = {
			"Name": type(self.object).__name__,
			"Module": self.object.__module__,
			"Utility": False,
			"Folders": {},
			"Files": {}
		}

		# If there is a dot in the name of the module
		if "." in self.module["Module"]:
			# If the first item of the module name is "Utility"
			if self.module["Module"].split(".")[0] == "Utility":
				# Split it to get only the class module, not its root module
				# For example: Remove "Utility." from "Utility.Define_Folders"
				# Result: "Define_Folders"
				self.module["Name"] = self.module["Module"].split(".")[1]

				# Define the "Utility" state as True
				self.module["Utility"] = True

			# Else, just split the module name and get the first name, which is the root module name
			# There might be a sub-module on the module name
			# For example: "Module.Sub_Module"
			# Result: "Module"
			else:
				self.module["Name"] = self.module["Module"].split(".")[0]

		# Define the module folders
		for key in ["Modules", "Module files"]:
			# Define the root folder
			root_folder = self.folders["Apps"][key]

			# If the module is an utility module
			if self.module["Utility"] == True:
				root_folder = root_folder["Utility"]

			# Define the module folder
			self.module["Folders"][key] = {
				"root": root_folder["root"] + self.module["Name"] + "/"
			}

		# Iterate through the files of the module
		for file in self.files:
			self.module["Files"][file] = self.module["Folders"]["Module files"]["root"] + file + ".json"

		# Define the "Module" dictionary inside the object
		setattr(self.object, "module", self.module)
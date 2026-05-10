# Define_Folders.py

import os
import pathlib

class Define_Folders():
	def __init__(self, object = None, files = [], create_texts = True):
		# Define the "Folders" dictionary
		self.Define_Folders()

		# Define the "object" parameter inside this class
		self.object = object

		# Define the root files list as an empty list
		self.files = []

		# If the "create texts" parameter is True
		if create_texts == True:
			# Add the "Texts" item to the files list
			self.files.append("Texts")

		# Extend the files list with the "files" parameter
		self.files.extend(files)

		# Define the "Module" dictionary
		self.Define_Module()

	def Define_Folders(self):
		# Define the hard drive letter
		self.hard_drive_letter = os.path.normpath(pathlib.Path.home().drive) + "/"

		# Define the "Folders" dictionary
		self.folders = {
			"root": self.hard_drive_letter
		}

		# Define the "Python" folder
		self.folders["Python"] = {
			"root": self.folders["root"] + "Python/"
		}

		# Define a list of folder names
		folder_names = [
			"Modules",
			"Files"
		]

		# Define the root "Python" folders
		for folder_name in folder_names:
			# Define the folder dictionary
			self.folders["Python"][folder_name] = {
				"root": self.folders["Python"]["root"] + folder_name + "/"
			}

		# Define the "Utility" folders
		for folder_name in folder_names:
			self.folders["Python"][folder_name]["Utility"] = {
				"root": self.folders["Python"][folder_name]["root"] + "Utility/"
			}

		# Define the "Modules.json" file
		self.folders["Python"]["Modules"]["Modules"] = self.folders["Python"]["Modules"]["root"] + "Modules.json"

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

		# If the module is "__main__"
		if self.module["Module"] == "__main__":
			# Change the module to be the module name
			self.module["Module"] = self.module["Name"]

		# Define a list of folder names
		folder_names = [
			"Modules",
			"Files",
		]

		# Iterate through that list
		for key in folder_names:
			# Define the root folder
			root_folder = self.folders["Python"][key]

			# If the module is an utility module
			if self.module["Utility"] == True:
				root_folder = root_folder["Utility"]

			# Define the module folder
			self.module["Folders"][key] = {
				"root": root_folder["root"] + self.module["Name"] + "/"
			}

		# Iterate through the files of the module
		for file in self.files:
			# Define the current module JSON file inside the module "Files" dictionary
			self.module["Files"][file] = self.module["Folders"]["Files"]["root"] + file + ".json"

		# Define the "Module" dictionary inside the object
		setattr(self.object, "module", self.module)
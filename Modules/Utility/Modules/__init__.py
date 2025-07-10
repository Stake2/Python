# Modules.py

import os
import importlib
from copy import deepcopy

class Modules():
	def __init__(self, object, select_class = False):
		# Import the classes
		self.Import_Classes()

		# Define the object parameter inside this class
		self.object = object

		# Define the states dictionary
		self.states = {
			"Select class": select_class
		}

		# Define the module
		self.Define_Module()

		# Define the classes
		self.Define_Classes()

		# If the "Select class" state is True
		if (
			self.states["Select class"] == True and
			hasattr(self, "do_not_select_class") == False
		):
			self.Select_Class()

	def Import_Classes(self):
		# Define the list of modules to be imported
		modules = [
			"Folder",
			"File"
		]

		# Iterate through the list of modules
		for module_title in modules:
			# Import the module
			module = importlib.import_module("." + module_title, "Utility")

			# Get the sub-class
			sub_class = getattr(module, module_title)

			# Add the sub-class to the current module
			setattr(self, module_title, sub_class())

		# Import the "folders" dictionary from the "Folder" class
		self.folders = self.Folder.folders

	def Define_Module(self):
		import inspect

		# ---------- #

		# Import some utility modules
		modules = [
			"Input",
			"JSON"
		]

		# Iterate through the list of modules
		for module_title in modules:
			# Import the module
			module = importlib.import_module("." + module_title, "Utility")

			# Get the sub-class
			sub_class = getattr(module, module_title)

			# Add the sub-class to the current module
			setattr(self, module_title, sub_class())

		# ---------- #

		# Define the "Language" class as the same class inside the "JSON" class
		self.Language = self.JSON.Language

		# Get the file of the class	
		file = inspect.getfile(self.object.__class__)

		# Define the module dictionary
		self.module = {
			"Module": self.object.__module__,
			"Sub-module": "",
			"Folders": {
				"root": self.folders["Apps"]["Modules"]["root"] + self.object.__module__ + "/"
			},
			"Files": {},
			"Descriptions": {}
		}

		# Define the sub-module
		if "." in self.module["Module"]:
			self.module["Sub-module"] = self.module["Module"].split(".")[-1]
			self.module["Module"] = self.module["Module"].split(".")[0]

		else:
			# Remove the "Sub-module" key
			self.module.pop("Sub-module")

		# Define the root folder
		self.module["Folders"] = {
			"root": self.folders["Apps"]["Modules"]["root"] + self.module["Module"] + "/"
		}

		folder = self.module["Folders"]["root"]

		# Define the texts folder
		self.module["Folders"]["Texts"] = {
			"root": self.folders["Apps"]["Module files"]["root"] + self.module["Module"] + "/"
		}

		# Define the sub-module folder if it exists
		if "Sub-module" in self.module:
			# Define the folder
			self.module["Folders"][self.module["Sub-module"]] = {
				"root": self.module["Folders"]["root"] + self.module["Sub-module"] + "/"
			}

			# Update the local folder
			folder = self.module["Folders"][self.module["Sub-module"]]["root"]

		# Define the descriptions file
		self.module["Files"]["Descriptions"] = folder + "Descriptions.json"

		# Get the class descriptions
		self.module["Descriptions"] = self.JSON.To_Python(self.module["Files"]["Descriptions"])

		# Define and create the "Module.json" file
		self.module["Files"]["Module"] = folder + "Module.json"
		self.File.Create(self.module["Files"]["Module"])

		# Define the user language version of the show text
		self.module["Descriptions"]["Show text"] = self.Language.Item(self.module["Descriptions"]["Show text"])

	def Define_Classes(self):
		# Define the "Classes" dictionary
		self.classes = {
			"Dictionary": {},
			"Descriptions": []
		}

		# Define the list of keys to remove
		remove_list = [
			"Show text",
			"Remove list"
		]

		# Iterate through the descriptions dictionary
		for key, descriptions in self.module["Descriptions"].items():
			# If the key is not in the remove list
			if key not in remove_list:
				# If the "Remove list" is not present in the module descriptions dictionary
				# Or it is and the key is not in the remove list
				if (
					"Remove list" not in self.module["Descriptions"] or
					"Remove list" in self.module["Descriptions"] and
					key not in self.module["Descriptions"]["Remove list"]
				):
					# Import the module
					module = importlib.import_module("." + key, self.object.__module__)

					# If the module contains the key
					if hasattr(module, key) == True:
						# Get the class object
						object = getattr(module, key)

					else:
						# Get the "Run" class
						object = getattr(module, "Run")

					# Create the class dictionary and add it to the "Classes" dictionary, with the class descriptions
					self.classes["Dictionary"][key] = {
						"Descriptions": descriptions,
						"Description": self.Language.Item(descriptions),
						"Object": object
					}

		# Fill the list of class descriptions
		for class_ in self.classes["Dictionary"].values():
			self.classes["Descriptions"].append(class_["Description"])

		# Add the "Classes" dictionary to the "Module" dictionary
		self.module["Classes"] = self.classes

		# ---------- #

		# Make a local copy of the "Module" dictionary
		local_dictionary = deepcopy(self.module)

		for key, class_ in local_dictionary["Classes"]["Dictionary"].items():
			# Stringy the class object
			class_["Object"] = str(class_["Object"])

		# Update the "Module.json" file with the updated local "Module" dictionary
		self.JSON.Edit(self.module["Files"]["Module"], local_dictionary)

	def Select_Class(self, return_class = False):
		# Define the parameters dictionary for the "Input.Select" method
		parameters = {
			"options": list(self.classes["Dictionary"].values()),
			"language_options": self.classes["Descriptions"],
			"show_text": self.module["Descriptions"]["Show text"],
			"select_text": self.Language.language_texts["select_one_class_to_execute"]
		}

		# Ask the user to select a class
		self.module["Selected class"] = self.Input.Select(**parameters)["option"]

		# Define the "Modules" variable inside the class object
		setattr(self.module["Selected class"]["Object"], "Modules", Modules)

		# Define the "module" variable inside the class object
		setattr(self.module["Selected class"]["Object"], "module", self.module)

		# If the "return_class" parameter is False
		if return_class == False:
			# Run the object of the class
			self.module["Selected class"]["Object"]()

		else:
			return self.module["Selected class"]
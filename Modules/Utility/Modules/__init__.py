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

		# Define the "States" dictionary
		self.states = {
			"Select class": select_class
		}

		# Define the module
		self.Define_Module()

		# Define the classes
		self.Define_Classes()

		# If the "Select class" state is True
		if self.states["Select class"] == True:
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

		# Define the local folders dictionary as the Folder folders dictionary
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
			"Folders": {
				"root": self.folders["Apps"]["Modules"]["root"] + self.object.__module__ + "/"
			},
			"Files": {},
			"Descriptions": {}
		}

		# Define the descriptions file
		self.module["Files"]["Descriptions"] = self.Language.Current_Folder(file) + "Descriptions.json"

		# Get the class descriptions
		self.module["Descriptions"] = self.JSON.To_Python(self.module["Files"]["Descriptions"])

		# Define and create the "Module.json" file
		self.module["Files"]["Module"] = self.module["Folders"]["root"] + "Module.json"
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
					# Get the class object
					module = importlib.import_module("." + key, self.object.__module__)
					object = getattr(module, key)

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

		# If the "return_class" parameter is False
		if return_class == False:
			# Run the object of the class
			self.module["Selected class"]["Object"]()

		else:
			return self.module["Selected class"]
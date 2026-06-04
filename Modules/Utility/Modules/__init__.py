# Modules.py

# Import some useful modules
import importlib
import os
from copy import deepcopy

# Define the main "Modules" class
class Modules():
	def __init__(self, class_object, module_files = [], create_texts = True, define_classes = True, select_class = False, return_class = False, utility_mode = False):
		# Define the states dictionary
		self.states = {
			"Utility mode": utility_mode,
			"Define classes": define_classes,
			"Select class": select_class,
			"Return class": return_class
		}

		# Import some utility classes
		self.Import_Utility_Classes()

		# Define the dictionaries of the "Modules" class
		self.Define_Dictionaries()

		# Define the module, passing it some parameters
		self.Define_Module(class_object, module_files, create_texts)

		# If the module type is "Usage"
		if self.module["Type"] == "Usage":
			# If the "Define classes" state is True
			if self.states["Define classes"] == True:
				# Define the classes, passing it the class object
				self.Define_Classes(class_object)

			# If the "Select class" state is True
			# And the "do_not_select_class" variable is not present inside the current (self) class object
			if (
				self.states["Select class"] == True and
				hasattr(self, "do_not_select_class") == False
			):
				# Run the "Select_Class" method to select a class
				self.Select_Class(return_class = return_class)

	def Import_Utility_Classes(self):
		# If the "Utility mode" state is False
		if self.states["Utility mode"] == False:
			# Define the list of utility modules to be imported
			classes = [
				"Folder",
				"JSON",
				"Input"
			]

			# Iterate through the list of classes to import
			for class_title in classes:
				# Import the module of the class
				module = importlib.import_module("." + class_title, "Utility")

				# Get the class object inside the module
				class_object = getattr(module, class_title)

				# Add the class object to the root class
				setattr(self, class_title, class_object())

			# Import the "folders" dictionary from the "Folder" class
			self.folders = self.Folder.folders

			# ---------- #

			# Define the "Language" class as the same class inside the "JSON" class
			self.Language = self.JSON.Language

			# Import the "language" dictionary from the "Language" class
			self.language = self.Language.language

		# ---------- #

		# If the "Utility mode" state is True
		if self.states["Utility mode"] == True:
			import pathlib

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

	def Sanitize(self, path):
		# Normalize the path and replace backslashes with forward slashes
		path = os.path.normpath(path).replace("\\", "/")

		# Return the path
		return path

	def Folder_Exists(self, folder):
		# Sanitize the folder path
		folder = self.Sanitize(folder)

		# Checks if the folder exists and returns True if it does or False if it does not
		return os.path.isdir(folder)

	def File_Exists(self, file):
		# Sanitize the file path
		file = self.Sanitize(file)

		# Checks if the file exists and returns True if it does or False if it does not
		return os.path.isfile(file)

	def File_Open(self, file, mode = "r", encoding = "UTF8"):
		# Open the file with the mode and encoding
		return open(file, mode, encoding = encoding)

	def File_Create(self, file):
		# Sanitize the file path
		file = self.Sanitize(file)

		# If the file does not exist
		if self.File_Exists(file) == False:
			# Open the file handle in write mode to create it
			create = self.File_Open(file, "w")

			# Close the file handle
			create.close()

	def Define_Dictionaries(self):
		# Define a dictionary of class modes
		self.class_modes = {
			"Numbers": {
				"Total": 2
			},
			"List": [
				"Descriptions",
				"Classes"
			],
			"Dictionary": {
				"Descriptions": {
					"Module descriptions key": "Show text",
					"File key": "Descriptions file"
				},
				"Classes": {
					"Module descriptions key": "Module descriptions"
				}
			}
		}

	def Define_Module(self, class_object, module_files, create_texts):
		# Create a shortcut to the module name
		module_name = class_object.__module__

		# If the module name is "__main__"
		if module_name == "__main__":
			# Get the module name by the class object name
			module_name = type(class_object).__name__

		# Define the module dictionary
		self.module = {
			# Define the module name
			"Module": module_name,

			# Define the module type
			"Type": "Usage",

			# Define the folder and file dictionaries
			"Folders": {},
			"Files": {}
		}

		# If a dot is inside the module name
		if "." in self.module["Module"]:
			# Split the module name by the dot
			split = self.module["Module"].split(".")

			# Define the module name as the name before the dot
			self.module["Module"] = split[0]

			# If the name before the dot is "Utility"
			if split[0] == "Utility":
				# Define the module name as the sub-module name
				self.module["Module"] = split[1]

				# Change the module type to "Utility"
				self.module["Type"] = "Utility"

		# If the module type is "Usage"
		if self.module["Type"] == "Usage":
			# Create the module descriptions, class mode, and classes dictionaries
			self.module.update({
				"Descriptions": {},
				"Class mode": {},
				"Classes": {}
			})

		# Define the modules and files folders
		modules_folder = self.folders["Python"]["Modules"]
		files_folder = self.folders["Python"]["Files"]

		# If the module type is "Utility"
		if self.module["Type"] == "Utility":
			# Change the folders to the "Utility" folders
			modules_folder = modules_folder["Utility"]
			files_folder = files_folder["Utility"]

		# Define the root folder of the module
		self.module["Folders"] = {
			"root": modules_folder["root"] + self.module["Module"] + "/"
		}

		# Define the "Files" folder
		self.module["Folders"]["Files"] = {
			"root": files_folder["root"] + self.module["Module"] + "/"
		}

		# Create a shortcut to the root folder
		root_folder = self.module["Folders"]["root"]

		# If the module type is "Usage"
		if self.module["Type"] == "Usage":
			# If the root folder exists
			if self.Folder_Exists(root_folder) == True:
				# Define and create the module "Module.json" file
				self.module["Files"]["Module"] = root_folder + "Module.json"
				self.File_Create(self.module["Files"]["Module"])

			# Iterate through the list of class mode keys and dictionaries
			for key, class_mode in self.class_modes["Dictionary"].items():
				# Add the name of the class mode to its dictionary as the first key
				class_mode = {
					"Name": key,
					**class_mode
				}

				# Update the root class mode dictionary
				self.class_modes["Dictionary"][key] = class_mode

				# Define the local class mode JSON file with the class mode key as a filename
				file = root_folder + key + ".json"

				# If the class mode file exists
				if self.File_Exists(file) == True:
					# Define it inside the module "Files" dictionary
					self.module["Files"][key] = file

					# Define the file key initially as the class mode key
					file_key = key

					# If the class mode has a custom file key
					if "File key" in class_mode:
						# Use the custom file key
						file_key = class_mode["File key"]

					# Get the JSON dictionary from the class mode file and store it in the file key inside the module dictionary
					self.module[file_key] = self.JSON.To_Python(file)

					# Create a shortcut to the module descriptions key
					module_descriptions_key = class_mode["Module descriptions key"]

					# Define the module "Descriptions" dictionary based on the module descriptions key
					self.module["Descriptions"] = self.module[file_key][module_descriptions_key]

					# Define the root "Class mode" dictionary of the module as the local class mode dictionary
					self.module["Class mode"] = class_mode

		# ---------- #

		# If the module files is a string
		if type(module_files) == str:
			# Transform it into a list with the string as the only item
			module_files = [
				module_files
			]

		# If the "create texts" parameter is True
		if create_texts == True:
			# Add the "Texts" file at the top of the list
			module_files = [
				"Texts",
				*module_files
			]

		# Create a shortcut to the "Files" folder
		files_folder = self.module["Folders"]["Files"]["root"]

		# Iterate through the list of file names
		for file_name in module_files:
			# Define and create the module JSON file
			self.module["Files"][file_name] = files_folder + file_name + ".json"
			self.File_Create(self.module["Files"][file_name])

		# ---------- #

		# Define a dictionary of attributes to add to the selected class object
		attributes = {
			"Modules": Modules,
			"module": self.module,
			"folders": self.folders
		}

		# Iterate through the attribute names and values
		for name, attribute in attributes.items():
			# Add the attribute to the selected class object
			setattr(class_object, name, attribute)

	def Define_Classes(self, class_object):
		# Define a local classes dictionary to store information about the classes of the module
		classes = {
			"Numbers": {
				"Total": 0
			},
			"List": [],
			"Dictionary": {}
		}

		# ----- #

		# Create a shortcut to the class mode name
		class_mode = self.module["Class mode"]["Name"]

		# If the class mode name is "Classes"
		if class_mode == "Classes":
			# Update the local classes "Dictionary" with the root one
			classes["Dictionary"] = self.module["Classes"]["Dictionary"]

			# Create a shortcut to the module descriptions key
			module_descriptions_key = self.module["Class mode"]["Module descriptions key"]

			# Import the module descriptions key to the local classes dictionary
			classes[module_descriptions_key] = self.module["Classes"][module_descriptions_key]

		# ----- #

		# If the class mode name is "Descriptions"
		# (This is a temporary compatibility layer for the old way of defining class descriptions
		# Which is by using the old "Descriptions.json" file)
		if class_mode == "Descriptions":
			# Define the list of keys to remove
			remove_list = [
				"Show text",
				"Remove list",
				"List of classes"
			]

			# Iterate through the list of keys to remove
			for key in remove_list:
				# If that key exists inside the "Descriptions file" dictionary
				if key in self.module["Descriptions file"]:
					# Import that key to the local classes dictionary
					classes[key] = self.module["Descriptions file"][key]

			# If there is a "Remove list" inside the module "Descriptions file" dictionary
			if "Remove list" in self.module["Descriptions file"]:
				# Extend the local remove list with the one inside the "Descriptions" dictionary
				remove_list.extend(self.module["Descriptions file"]["Remove list"])

			# Iterate through the list of description keys and values
			for key, descriptions in self.module["Descriptions file"].items():
				# If the key is not in the list of keys to remove
				if key not in remove_list:
					# Create the local class dictionary
					dictionary = {
						"Name": key,
						"Descriptions": descriptions,
						"Object": {}
					}

					# Add the local class dictionary to the root class "Dictionary"
					classes["Dictionary"][key] = dictionary

			# Define the root "Classes" dictionary as the local one
			self.module["Classes"] = classes

		# ----- #

		# Iterate through the dictionary of class keys and dictionaries
		for key, dictionary in self.module["Classes"]["Dictionary"].items():
			# Add the class to the list of classes
			classes["List"].append(key)

			# If the class mode name is "Classes"
			if class_mode == "Classes":
				# Add the name of the class to its dictionary as the first key
				dictionary = {
					"Name": key,
					**dictionary
				}

			# Import the module of the class
			class_module = importlib.import_module("." + key, self.module["Module"])

			# If the module contains the class
			if hasattr(class_module, key) == True:
				# Define the class object as the class inside the class module
				object = getattr(class_module, key)

			# Else, define the class object as the "Run" class inside the class module
			# Which must be the class that is present inside that module
			else:
				object = getattr(class_module, "Run")

			# Update the class "Object" key to be the actual class object
			dictionary["Object"] = object

			# Add the local class dictionary to the root classes "Dictionary" with the class key
			classes["Dictionary"][key] = dictionary

		# Update the total number of classes
		classes["Numbers"]["Total"] = len(classes["List"])

		# ----- #

		# Update the root "Classes" dictionary to be the local one
		self.module["Classes"] = classes

		# ---------- #

		# Make a local copy of the module dictionary
		local_dictionary = deepcopy(self.module)

		# Iterate through the list of class dictionaries
		for dictionary in local_dictionary["Classes"]["Dictionary"].values():
			# Stringfy the class object to make it JSON compatible
			dictionary["Object"] = str(dictionary["Object"])

		# If the class mode name is "Classes"
		if class_mode == "Classes":
			# Remove the module descriptions dictionary from the "Classes" dictionary
			local_dictionary["Classes"].pop(module_descriptions_key)

		# If the class mode name is "Descriptions"
		if class_mode == "Descriptions":
			# Iterate through the list of keys to remove
			for key in remove_list:
				# If that key exists inside the "Classes" dictionary
				if key in local_dictionary["Classes"]:
					# Remove it
					local_dictionary["Classes"].pop(key)

			# Remove the "Descriptions file" key
			local_dictionary.pop("Descriptions file")

		# If the "Module" file is present inside the module "Files" dictionary
		if "Module" in self.module["Files"]:
			# Update the "Module.json" file with the updated local module dictionary
			self.JSON.Edit(self.module["Files"]["Module"], local_dictionary)

		# ---------- #

		# If the class mode name is "Classes"
		if class_mode == "Classes":
			# Make a local copy of the "Classes" dictionary
			local_dictionary = deepcopy(self.module["Classes"])

			# Iterate through the list of class dictionaries
			for dictionary in local_dictionary["Dictionary"].values():
				# Stringfy the class object to make it JSON compatible
				dictionary["Object"] = str(dictionary["Object"])

			# Create a backup of the module descriptions dictionary
			module_descriptions = local_dictionary[module_descriptions_key]

			# Remove the key
			local_dictionary.pop(module_descriptions_key)

			# Add it again to make it stay at the end
			local_dictionary[module_descriptions_key] = module_descriptions

			# Update the "Classes.json" file with the updated local "Classes" dictionary
			self.JSON.Edit(self.module["Files"]["Classes"], local_dictionary)

		# ---------- #

		# Define a dictionary of attributes to add to the selected class object
		attributes = {
			"Modules": Modules,
			"module": self.module,
			"folders": self.folders
		}

		# Iterate through the attribute names and values
		for name, attribute in attributes.items():
			# Add the attribute to the selected class object
			setattr(class_object, name, attribute)

	def Select_Class(self, return_class = False):
		# Create a shortcut to the root "Classes" dictionary for faster typing
		classes = self.module["Classes"]

		# Define the "Selected" class dictionary
		classes["Selected"] = {
			"Class": {},
			"Automatically selected": False
		}

		# If there is only one class
		if classes["Numbers"]["Total"] == 1:
			# Then define the selected class as the only one
			classes["Selected"]["Class"] = list(classes["Dictionary"].values())[0]

			# Define the "Automatically selected class" switch inside the class object as True
			setattr(classes["Selected"]["Class"]["Object"], "automatically_selected_class", True)

			# Switch the "Automatically selected" class switch to True
			classes["Selected"]["Automatically selected"] = True

		# If the "Automatically selected" switch is False
		if classes["Selected"]["Automatically selected"] == False:
			# Define the parameters dictionary to use on the "Input.Select" class method
			parameters = {
				# The list of classes
				"options": [],

				# The list of class descriptions in the user language
				"language_options": [],

				# The module description in the user language
				"show_text": self.module["Descriptions"][self.language["Small"]],

				# The text to show to the user to ask them to select a class
				"select_text": self.Language.language_texts["select_one_class_to_execute"]
			}

			# Iterate through the dictionary of class dictionaries
			for dictionary in self.module["Classes"]["Dictionary"].values():
				# Add the class dictionary to the list of options
				parameters["options"].append(dictionary)

				# Add the class description in the user language to the list of language options
				parameters["language_options"].append(dictionary["Descriptions"][self.language["Small"]])

			# Ask the user to select a class from the list of classes
			# And then define the selected class inside the "Selected" class dictionary
			classes["Selected"]["Class"] = self.Input.Select(**parameters)["Option"]["Original"]

		# Define the "Selected" key as the selected class for clarity
		classes["Selected"] = classes["Selected"]["Class"]

		# Define a dictionary of attributes to add to the selected class object
		attributes = {
			"Modules": Modules,
			"module": self.module
		}

		# Create a shortcut to the selected class object for clarity
		class_object = classes["Selected"]["Object"]

		# Iterate through the attribute names and values
		for name, attribute in attributes.items():
			# Add the attribute to the selected class object
			setattr(class_object, name, attribute)

		# If the "Return class" state is False
		if self.states["Return class"] == False:
			# Run the object of the selected class
			class_object()

		# If the "Return class" state is True
		if self.states["Return class"] == True:
			# Return the selected class dictionary
			return classes["Selected"]
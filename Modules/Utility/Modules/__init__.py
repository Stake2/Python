# Modules.py

# Import some useful modules
import importlib
from copy import deepcopy

class Modules():
	def __init__(self, object, select_class = False, return_class = False):
		# Import some utility classes
		self.Import_Utility_Classes()

		# Define the object parameter inside this class
		self.object = object

		# Define the states dictionary
		self.states = {
			"Select class": select_class
		}

		# Define the dictionaries of the "Modules" class
		self.Define_Dictionaries()

		# Define the module
		self.Define_Module()

		# Define the classes
		self.Define_Classes()

		# If the "Select class" state is True
		# And the "do_not_select_class" variable is not present inside the current (self) class object
		if (
			self.states["Select class"] == True and
			hasattr(self, "do_not_select_class") == False
		):
			# Run the "Select_Class" method to select a class
			self.Select_Class(return_class = return_class)

	def Import_Utility_Classes(self):
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

			# Add the sub-class to the current class
			setattr(self, module_title, sub_class())

		# Import the "folders" dictionary from the "Folder" class
		self.folders = self.Folder.folders

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
					"Module description key": "Show text",
					"File key": "Descriptions file"
				},
				"Classes": {
					"Module description key": "Module description"
				}
			}
		}

	def Define_Module(self):
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

			# Add the sub-class to the current class
			setattr(self, module_title, sub_class())

		# ---------- #

		# Define the "Language" class as the same class inside the "JSON" class
		self.Language = self.JSON.Language

		# Import the "language" dictionary from the "Language" class
		self.language = self.Language.language

		# ---------- #

		# Define the module dictionary
		self.module = {
			"Module": self.object.__module__,
			"Sub-module": "",
			"Folders": {
				"root": self.folders["Python"]["Modules"]["root"] + self.object.__module__ + "/"
			},
			"Files": {},
			"Descriptions": {},
			"Class mode": {},
			"Classes": {}
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
			"root": self.folders["Python"]["Modules"]["root"] + self.module["Module"] + "/"
		}

		# Create a shortcut to the root folder
		folder = self.module["Folders"]["root"]

		# Define the "Files" folder
		self.module["Folders"]["Files"] = {
			"root": self.folders["Python"]["Files"]["root"] + self.module["Module"] + "/"
		}

		# Define the sub-module folder if it exists
		if "Sub-module" in self.module:
			# Define the folder
			self.module["Folders"][self.module["Sub-module"]] = {
				"root": self.module["Folders"]["root"] + self.module["Sub-module"] + "/"
			}

			# Update the local folder
			folder = self.module["Folders"][self.module["Sub-module"]]["root"]

		# Define and create the "Module.json" file
		self.module["Files"]["Module"] = folder + "Module.json"
		self.File.Create(self.module["Files"]["Module"])

		# Iterate through the list of class mode keys and dictionaries
		for key, class_mode in self.class_modes["Dictionary"].items():
			# Add the name of the class mode to its dictionary
			class_mode = {
				"Name": key,
				**class_mode
			}

			# Update the root class mode dictionary
			self.class_modes["Dictionary"][key] = class_mode

			# Define the local file
			file = folder + key + ".json"

			# If the file exists
			if self.File.Exists(file) == True:
				# Define it inside the "Files" dictionary
				self.module["Files"][key] = file

				# Define the file key initially as the key
				file_key = key

				# If the class mode is "Descriptions"
				if key == "Descriptions":
					# Change the file key to the correct one
					file_key = class_mode["File key"]

				# Get the JSON dictionary from the file and store it in the file key
				self.module[file_key] = self.JSON.To_Python(file)

				# Create a shortcut to the module description key
				module_description_key = class_mode["Module description key"]

				# Define the module descriptions dictionary based on the module description key
				self.module["Descriptions"] = self.module[file_key][module_description_key]

				# Add the class mode dictionary to the module dictionary
				self.module["Class mode"] = class_mode

	def Define_Classes(self):
		# Define a local classes dictionary
		classes = {
			"Numbers": {
				"Total": 0
			},
			"List": [],
			"Dictionary": {}
		}

		# ----- #

		# If the class mode is "Classes"
		if self.module["Class mode"]["Name"] == "Classes":
			# Update the local "Dictionary" with the root one
			classes["Dictionary"] = self.module["Classes"]["Dictionary"]

			# Create a shortcut to the module description key
			module_description_key = self.module["Class mode"]["Module description key"]

			# Import the module description key to the local classes dictionary
			classes[module_description_key] = self.module["Classes"][module_description_key]

		# ----- #

		# If the class mode is "Descriptions"
		# (This is a compatibility layer for the old way of defining class descriptions, which is by using the old "Descriptions.json" file)
		if self.module["Class mode"]["Name"] == "Descriptions":
			# Define a local classes dictionary
			classes = {
				"Numbers": {
					"Total": 0
				},
				"List": [],
				"Dictionary": {}
			}

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

			# If there is a "Remove list" inside the module "Descriptions" dictionary
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

		# Create the list of class "Descriptions" in the user language
		classes["Descriptions"] = []

		# Iterate through the dictionary of class keys and dictionaries
		for key, dictionary in self.module["Classes"]["Dictionary"].items():
			# Add the class to the list of classes
			classes["List"].append(key)

			# If the class mode is "Classes"
			if self.module["Class mode"]["Name"] == "Classes":
				# Update the class dictionary to add its name
				dictionary = {
					"Name": key,
					**dictionary
				}

			# Import the module of the class
			class_module = importlib.import_module("." + key, self.module["Module"])

			# If the module contains the class
			if hasattr(class_module, key) == True:
				# Define the object as the class inside the class module
				object = getattr(class_module, key)

			else:
				# Define the object as the "Run" class inside the class module
				object = getattr(class_module, "Run")

			# Update the "Object" key to be the actual object
			dictionary["Object"] = object

			# Add the class description in the user language to the list of class descriptions
			classes["Descriptions"].append(dictionary["Descriptions"][self.language["Small"]])

			# Update the root class dictionary
			classes["Dictionary"][key] = dictionary

		# Update the number of classes
		classes["Numbers"]["Total"] = len(classes["List"])

		# ----- #

		# Update the root "Classes" dictionary with the local one
		self.module["Classes"] = classes

		# ---------- #

		# Make a local copy of the "Module" dictionary
		local_dictionary = deepcopy(self.module)

		# Iterate through the list of class dictionaries
		for dictionary in local_dictionary["Classes"]["Dictionary"].values():
			# Stringfy the class object to make it JSON compatible
			dictionary["Object"] = str(dictionary["Object"])

		# If the class mode is "Classes"
		if self.module["Class mode"]["Name"] == "Classes":
			# Remove the module description from the "Classes" dictionary
			local_dictionary["Classes"].pop(module_description_key)

		# Update the "Module.json" file with the updated local "Module" dictionary
		self.JSON.Edit(self.module["Files"]["Module"], local_dictionary)

		# ---------- #

		# If the class mode is "Classes"
		if self.module["Class mode"]["Name"] == "Classes":
			# Make a local copy of the "Classes" dictionary
			local_dictionary = deepcopy(self.module["Classes"])

			# Iterate through the list of class dictionaries
			for dictionary in local_dictionary["Dictionary"].values():
				# Stringfy the class object to make it JSON compatible
				dictionary["Object"] = str(dictionary["Object"])

			# Create a backup of the module description dictionary
			description = local_dictionary[module_description_key]

			# Remove the key
			local_dictionary.pop(module_description_key)

			# Add it again
			local_dictionary[module_description_key] = description

			# Update the "Classes.json" file with the updated local "Classes" dictionary
			self.JSON.Edit(self.module["Files"]["Classes"], local_dictionary)

		# ---------- #

		# Define the "Modules" variable inside the class object
		setattr(self.object, "Modules", Modules)

		# Define the "module" variable inside the class object
		setattr(self.object, "module", self.module)

	def Select_Class(self, return_class = False):
		# Create a shortcut to the "Classes" dictionary for faster typing
		classes = self.module["Classes"]

		# Define the "Selected" class dictionary
		classes["Selected"] = {
			"Class": {},
			"Automatically selected": False,
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
			# Define the parameters dictionary to use on the "Input.Select" method
			parameters = {
				# The list of class names
				"options": classes["List"],

				# The list of class descriptions in the user language
				"language_options": classes["Descriptions"],

				# The module description in the user language
				"show_text": self.module["Descriptions"][self.language["Small"]],

				# The text to show to the user to ask them to select a class
				"select_text": self.Language.language_texts["select_one_class_to_execute"]
			}

			# Ask the user to select a class from the list of classes
			# And then define theselected class inside the "Selected" class dictionary
			classes["Selected"]["Class"] = self.Input.Select(**parameters)["Option"]["Original"]

		# Define the "Select" key as the selected class for faster typing
		classes["Selected"] = classes["Selected"]["Class"]

		# Add the "Modules" class to the class object
		setattr(classes["Selected"]["Object"], "Modules", Modules)

		# Add the "module" dictionary to the class object
		setattr(classes["Selected"]["Object"], "module", self.module)

		# If the "return_class" parameter is False
		if return_class == False:
			# Run the object of the class
			classes["Selected"]["Object"]()

		else:
			# Return the class dictionary
			return classes["Selected"]
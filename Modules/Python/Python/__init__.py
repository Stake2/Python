# Python.py

# Import some useful modules
import importlib

# Define the main "Python" class
class Python(object):
	def __init__(self):
		# Define the variables of the class
		self.Define_Variables()

		# Define the "Python" dictionary
		self.Define_Python_Dictionary()

		# Update the "Modules.json" file
		self.Update_Modules_File()

	def Define_Variables(self):
		# Import the "JSON" class
		from Utility.JSON import JSON as JSON

		# Instance it and add it to the current class
		self.JSON = JSON()

		# Import the "folders" dictionary from the "JSON" class
		self.folders = self.JSON.folders

		# ---------- #

		# Get the dictionary of Python modules
		self.modules = self.JSON.To_Python(self.folders["Python"]["Modules"]["Modules"])

		# Define a list of utility classes to not import
		do_not_import = [
			"API",
			"System"
		]

		# Iterate through the list of utility classes
		for class_title in self.modules["Utility"]["List"]:
			# If the class is not already inside the self class (Python)
			# And the class title is not inside the list of utility classes to not import
			if (
				hasattr(self, class_title) == False and
				class_title not in do_not_import
			):
				# Import the module of the class
				module = importlib.import_module("." + class_title, "Utility")

				# Get the class object inside the module
				class_object = getattr(module, class_title)

				# If the class title is not "Modules"
				if class_title != "Modules":
					# Run the class object to define its attributes
					class_object = class_object()

				# Add the class object to the root class
				setattr(self, class_title, class_object)

		# ---------- #

		# Define the module dictionary and the module folders and files
		self.Modules(class_object = self)

		# ---------- #

		# Import the switches dictionary from the "Global Switches" class
		self.switches = self.Global_Switches.switches["Global"]

		# ---------- #

		# Define the "Language" class as the same class inside the "JSON" class
		self.Language = self.JSON.Language

		# Import some attributes from the "Language" class

		# Import the "languages" dictionary
		self.languages = self.Language.languages

		# Import the "language" dictionary
		self.language = self.Language.language

		# Import the "separators" dictionary
		self.separators = self.Language.separators

		# ---------- #

		# Import the "folders" dictionary from the "Folder" class
		self.folders = self.Folder.folders

		# ---------- #

		# Get the current date from the "Date" class
		self.date = self.Date.date

		# ---------- #

		# Define the "Texts" dictionary
		self.texts = self.JSON.To_Python(self.module["Files"]["Texts"])

		# Define the "Language texts" dictionary
		self.language_texts = self.Language.Item(self.texts)

	def Define_Python_Dictionary(self):
		# Define the root "Python" dictionary
		self.python = {
			"Folders": {
				"root": self.folders["Python"]["root"]
			},
			"Files": {
				"Python": {}
			}
		}

		# Define a list of folder names
		folder_names = [
			"Modules",
			"Files",
		]

		# Iterate through that list
		for folder_name in folder_names:
			# Define and create the folder
			self.python["Folders"][folder_name] = {
				"root": self.python["Folders"]["root"] + folder_name + "/"
			}

			self.Folder.Create(self.python["Folders"][folder_name]["root"])

			# Define and create the "Utility" folder
			self.python["Folders"][folder_name]["Utility"] = {
				"root": self.python["Folders"][folder_name]["root"] + "Utility/"
			}

			self.Folder.Create(self.python["Folders"][folder_name]["Utility"]["root"])

		# Define the "Modules.json" file
		self.python["Files"]["Modules"] = self.python["Folders"]["Modules"]["root"] + "Modules.json"
		self.File.Create(self.python["Files"]["Modules"])

		# Define the "Python" files folder
		self.python["Folders"]["Files"]["Python"] = {
			"root": self.python["Folders"]["Files"]["root"] + "Python/"
		}

		# Define the "Code templates" folder
		self.python["Folders"]["Files"]["Python"]["Code templates"] = {
			"root": self.python["Folders"]["Files"]["Python"]["root"] + "Code templates/"
		}

		# ---------- #

		# Get the "Modules" dictionary
		self.python["Modules"] = {
			"Types": {
				"List": [
					"Utility",
					"Usage"
				],
				"Dictionary": {}
			},
			"File": self.python["Files"]["Modules"],
			"Dictionary": self.JSON.To_Python(self.python["Files"]["Modules"])
		}

		# Iterate through the module types list
		for module_type in self.python["Modules"]["Types"]["List"]:
			# Create the module type dictionary
			module_type = {
				"Name": module_type,
				"Folders": {}
			}

			# Iterate through the list of folder names
			for key in folder_names:
				# Define the root folder
				folder = self.python["Folders"][key]["root"]

				# If the module type is "Utility"
				if module_type["Name"] == "Utility":
					folder = self.python["Folders"][key]["Utility"]["root"]

				# Add the folder to the "Folders" dictionary
				module_type["Folders"][key] = {
					"root": folder
				}

			# Add the module type dictionary to the root dictionary
			self.python["Modules"]["Types"]["Dictionary"][module_type["Name"]] = module_type

		# Create a shortcut to the "Modules" dictionary
		self.modules = self.python["Modules"]["Dictionary"]

		# ---------- #

		# Define the list of code templates
		code_templates = [
			"Root",
			"Main class",
			"Sub-class"
		]

		# Define the root folder
		folder = self.python["Folders"]["Files"]["Python"]["Code templates"]["root"]

		# Define a file for each code template
		for template in code_templates:
			# Define and create the file
			file = folder + template + ".txt"
			self.File.Create(file)

			# Add it to the "Templates" dictionary
			self.python["Templates"][template] = self.File.Contents(file)["string"]

	def Update_Modules_File(self):
		# Iterate through the module types list
		for module_type in self.python["Modules"]["Types"]["Dictionary"].values():
			# Get the module folders
			folders = self.Folder.Contents(module_type["Folders"]["Modules"]["root"])["folder"]["names"]

			# If the module is "Usage"
			if module_type["Name"] == "Usage":
				# Remove the "Utility" folder from the list
				folders.remove("Utility")

			# Update the list of modules for the current module type
			self.python["Modules"]["Dictionary"][module_type["Name"]]["List"] = folders

		# Update the "Modules.json" file with the updated modules list
		self.JSON.Edit(self.python["Modules"]["File"], self.python["Modules"]["Dictionary"])
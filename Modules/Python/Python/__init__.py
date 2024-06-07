# Python.py

# Import the "importlib" module
import importlib

class Python(object):
	def __init__(self):
		# Import the classes
		self.Import_Classes()

		# Define the folders of the module
		self.folders = self.Define_Folders(object = self).folders

		# Module related methods
		self.Define_Basic_Variables()
		self.Define_Texts()

		# Class methods

		# Define the "Python" dictionary
		self.Define_Python_Dictionary()

		# Update the "Modules.json" file
		self.Update_Modules_File()

	def Import_Classes(self):
		# Define the list of modules to be imported
		modules = [
			"Define_Folders",
			"JSON"
		]

		# Iterate through the list of modules
		for module_title in modules:
			# Import the module
			module = importlib.import_module("." + module_title, "Utility")

			# Get the sub-class
			sub_class = getattr(module, module_title)

			# If the module title is not "Define_Folders"
			if module_title != "Define_Folders":
				# Run the sub-class to define its variable
				sub_class = sub_class()

			# Add the sub-class to the current module
			setattr(self, module_title, sub_class)

		# Define the "Language" class as the same class inside the "JSON" class
		self.Language = self.JSON.Language

	def Define_Basic_Variables(self):
		# Get the modules list
		self.modules = self.JSON.To_Python(self.folders["Apps"]["Modules"]["Modules"])

		# Create a list of the modules that will not be imported
		remove_list = [
			"Define_Folders",
			"Modules",
			"Language",
			"JSON"
		]

		# Iterate through the Utility modules
		for module_title in self.modules["Utility"]["List"]:
			# If the module title is not inside the remove list
			if module_title not in remove_list:
				# Import the module
				module = importlib.import_module("." + module_title, "Utility")

				# Get the sub-class
				sub_class = getattr(module, module_title)

				# Add the sub-class to the current module
				setattr(self, module_title, sub_class())

		# Get the switches dictionary from the "Global Switches" module
		self.switches = self.Global_Switches.switches["Global"]

		# Get the Languages dictionary
		self.languages = self.Language.languages

		# Get the user language and full user language
		self.user_language = self.Language.user_language
		self.full_user_language = self.Language.full_user_language

		# Define the local folders dictionary as the Folder folders dictionary
		self.folders = self.Folder.folders

		# Get the Sanitize method of the File class
		self.Sanitize = self.File.Sanitize

		# Get the current date from the Date module
		self.date = self.Date.date

	def Define_Texts(self):
		# Define the "Texts" dictionary
		self.texts = self.JSON.To_Python(self.module["Files"]["Texts"])

		# Define the "Language texts" dictionary
		self.language_texts = self.Language.Item(self.texts)

		# Define the "Separators" dictionary
		self.separators = {}

		# Create separators from one to ten characters
		for number in range(1, 11):
			# Define the empty string
			string = ""

			# Add separators to it
			while len(string) != number:
				string += "-"

			# Add the string to the Separators dictionary
			self.separators[str(number)] = string

	def Define_Python_Dictionary(self):
		# Define the root "Python" dictionary
		self.python = {
			"Folders": {
				"root": self.folders["Apps"]["root"]
			},
			"Files": {
				"Python": {}
			}
		}

		# Define the sub-folders folder
		folders = [
			"Modules",
			"Module files",
		]

		for folder in folders:
			# Define and create the folder
			self.python["Folders"][folder] = {
				"root": self.python["Folders"]["root"] + folder + "/"
			}

			self.Folder.Create(self.python["Folders"][folder]["root"])

			# Define and create the "Utility" folder
			self.python["Folders"][folder]["Utility"] = {
				"root": self.python["Folders"][folder]["root"] + "Utility/"
			}

			self.Folder.Create(self.python["Folders"][folder]["Utility"]["root"])

		# Define the modules file
		self.python["Files"]["Modules"] = self.python["Folders"]["Modules"]["root"] + "Modules.json"
		self.File.Create(self.python["Files"]["Modules"])

		# Define the "Python" module files folder
		self.python["Folders"]["Module files"]["Python"] = {
			"root": self.python["Folders"]["Module files"]["root"] + "Python/"
		}

		# Define the "Code templates" folder
		self.python["Folders"]["Module files"]["Python"]["Code templates"] = {
			"root": self.python["Folders"]["Module files"]["Python"]["root"] + "Code templates/"
		}

		# ---------- #

		# Define the files of the "Module files" folder
		files = [
			"Last module",
			"Task number"
		]

		# Iterate through the list of files
		for file in files:
			# Define and create the file
			self.python["Files"][file] = self.python["Folders"]["Module files"]["Python"]["root"] + file + ".txt"
			self.File.Create(self.python["Files"][file])

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

			# Define the folders of the module type
			for key in ["Modules", "Module files"]:
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

		# Define a shortcut for the "Modules" dictionary
		self.modules = self.python["Modules"]["Dictionary"]

		# ---------- #

		# Define the "Templates" dictionary
		self.python["Templates"] = {
			"Task": """				<key name="Task[Number]" modified="2022-02-08 14:24:07" build="210912">
					<value name="Name" type="string" data="{[Module_Name]}"/>
					<value name="Flags" type="dword" data="00000004"/>
					<value name="Hotkey" type="dword" data="00000000"/>
					<value name="GuiArgs" type="string" data=""/>
					<value name="Active" type="long" data="0"/>
					<value name="Count" type="long" data="1"/>
					<value name="Cmd1" type="string" data="[module_execution_line]"/>
				</key>""",
			"Bat": 'cd "C:\Program Files\ConEmu"' + "\n" + 'start ConEmu.exe -Dir "C:\Apps" -Title "[Name]" -FontSize 12 -run {[Module]}'
		}

		# Define the list of code templates
		code_templates = [
			"Root",
			"Main class",
			"Sub-class"
		]

		# Define the root folder
		folder = self.python["Folders"]["Module files"]["Python"]["Code templates"]["root"]

		# Define a file for each code template
		for template in code_templates:
			# Define and create the file
			file = folder + template + ".txt"
			self.File.Create(file)

			# Add it to the "Templates" dictionary
			self.python["Templates"][template] = self.File.Contents(file)["string"]

		# ---------- #

		# Define the "ConEmu.xml" file
		self.python["Files"]["ConEmu"] = self.folders["User"]["AppData"]["Roaming"]["root"] + "ConEmu.xml"

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
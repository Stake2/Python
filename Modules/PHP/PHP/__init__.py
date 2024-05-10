# PHP.py

class PHP(object):
	def __init__(self):
		# Define the module folders
		from Utility.Define_Folders import Define_Folders as Define_Folders

		Define_Folders(self)

		# Module related methods
		self.Define_Basic_Variables()
		self.Define_Texts()

		# Define the dictionaries
		self.Define_Dictionaries()

		# Define the server
		self.Define_Server()

	def Define_Basic_Variables(self):
		from copy import deepcopy

		# Import the JSON module
		from Utility.JSON import JSON as JSON

		self.JSON = JSON()

		# Define the "Language" class as the same class inside the "JSON" class
		self.Language = self.JSON.Language

		# Get the modules list
		self.modules = self.JSON.To_Python(self.folders["apps"]["modules"]["modules"])

		import importlib

		# Create a list of the modules that will not be imported
		remove_list = [
			"Define_Folders",
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

				# Add the sub-clas to the current module
				setattr(self, module_title, sub_class())

		# Make a backup of the module folders
		self.module_folders = {}

		for item in ["modules", "module_files"]:
			self.module_folders[item] = deepcopy(self.folders["apps"][item][self.module["key"]])

		# Define the local folders dictionary as the Folder folders dictionary
		self.folders = self.Folder.folders

		# Restore the backup of the module folders
		for item in ["modules", "module_files"]:
			self.folders["apps"][item][self.module["key"]] = self.module_folders[item]

		# Get the switches dictionary from the "Global Switches" module
		self.switches = self.Global_Switches.switches["Global"]

		# Get the Languages dictionary
		self.languages = self.JSON.Language.languages

		# Get the user language and full user language
		self.user_language = self.JSON.Language.user_language
		self.full_user_language = self.JSON.Language.full_user_language

		# Get the Sanitize method of the File class
		self.Sanitize = self.File.Sanitize

		# Get the current date from the Date module
		self.date = self.Date.date

	def Define_Texts(self):
		# Define the "Texts" dictionary
		self.texts = self.JSON.To_Python(self.folders["apps"]["module_files"][self.module["key"]]["texts"])

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

	def Define_Dictionaries(self):
		# Read the "Websites.json" file to get the "Websites" dictionary
		self.websites = self.JSON.To_Python(self.folders["Mega"]["PHP"]["JSON"]["Websites"])

		# Read the "URL.json" file to get the "URL" dictionary
		self.url = self.JSON.To_Python(self.folders["Mega"]["PHP"]["JSON"]["URL"])

		# Read the "Colors.json" file to get the "Colors" dictionary
		self.colors = self.JSON.To_Python(self.folders["Mega"]["PHP"]["JSON"]["Colors"])

	def Define_Server(self):
		# Define the "Server" dictionary
		self.server = {
			"Name": "XAMPP",
			"Server": self.folders["XAMPP"]["XAMPP Control"],
			"Programs": [
				"xampp-control",
				"httpd",
				"mysql"
			]
		}

	def Manage_Server(self, open = False, close = False, show_text = True):
		# Get the class name
		class_name = type(self).__name__

		# Define the separator as the five dash space separator
		separator = self.separators["5"]

		# If the class name is not "Update_Websites"
		if class_name != "Update_Websites":
			# Define the separator as the one dash space separator
			separator = self.separators["1"]

		# If the "open" parameter is True
		if open == True:
			# Define the text as "opening"
			text = self.language_texts["opening_the_server"]

		# If the "close" parameter is True
		if close == True:
			# Define the text as "closing"
			text = self.language_texts["closing_the_server"]

		# Add the server name to the text
		text += ' "' + self.server["Name"] + '"'

		# If the "show text" parameter is True
		if show_text == True:
			# Show the text
			print()
			print(separator)
			print()
			print(text + "...")

		# If the "open" parameter is True
		if open == True:
			# Open the server
			self.System.Open(self.server["Server"], verbose = False)

			if self.switches["testing"] == False:
				# Wait for three seconds
				self.Date.Sleep(3)

		# If the "close" parameter is True
		if close == True:
			# Close the programs of the server
			for program in self.server["Programs"]:
				self.System.Close(program)
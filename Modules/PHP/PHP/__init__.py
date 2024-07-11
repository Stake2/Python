# PHP.py

# Import the "importlib" module
import importlib

class PHP(object):
	def __init__(self):
		# Import the classes
		self.Import_Classes()

		# Define the folders of the module
		self.folders = self.Define_Folders(object = self).folders

		# Module related methods
		self.Define_Basic_Variables()
		self.Define_Texts()

		# Class methods

		# Define the dictionaries
		self.Define_Dictionaries()

		# Define the server
		self.Define_Server()

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

		# Define the local "folders" dictionary as the dictionary inside the "Folder" class
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

	def Manage_Server(self, open = False, close = False, show_text = True, separator_number = None):
		# Get the class name
		class_name = type(self).__name__

		# Define the default separator number
		if separator_number == None:
			separator_number = 5

			# If the class name is not "Update_Websites"
			if class_name != "Update_Websites":
				# Define the separator number as one
				separator_number = 1

		# Define the separator with the separator number
		separator = self.separators[str(separator_number)]

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

			if self.switches["Testing"] == False:
				# Wait for three seconds
				self.Date.Sleep(3)

		# If the "close" parameter is True
		if close == True:
			# Close the programs of the server
			for program in self.server["Programs"]:
				self.System.Close(program)
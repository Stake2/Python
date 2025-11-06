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
		# Get the dictionary of modules
		self.modules = self.JSON.To_Python(self.folders["Apps"]["Modules"]["Modules"])

		# Create a list of the modules that will not be imported
		remove_list = [
			"Define_Folders",
			"Modules",
			"Language",
			"JSON"
		]

		# Iterate through the list of utility modules
		for module_title in self.modules["Utility"]["List"]:
			# If the module title is not inside the remove list
			if module_title not in remove_list:
				# Import the module
				module = importlib.import_module("." + module_title, "Utility")

				# Get the sub-class of the module
				sub_class = getattr(module, module_title)

				# Add the sub-class to the current class
				setattr(self, module_title, sub_class())

		# Get the switches dictionary from the "Global Switches" class
		self.switches = self.Global_Switches.switches["Global"]

		# ---------- #

		# Import some variables from the "Language" class

		# Import the "languages" dictionary
		self.languages = self.Language.languages

		# Import the "system" dictionary
		self.system = self.Language.system

		# Import the "language" dictionary
		self.language = self.Language.language

		# ---------- #

		# Import the "folders" dictionary from the "Folder" class
		self.folders = self.Folder.folders

		# ---------- #

		# Import the "Sanitize" method from the "File" class
		self.Sanitize = self.File.Sanitize

		# ---------- #

		# Get the current date from the "Date" class
		self.date = self.Date.date

		# Get the current year
		self.current_year = self.date["Units"]["Year"]

	def Define_Texts(self):
		# Define the "Texts" dictionary
		self.texts = self.JSON.To_Python(self.module["Files"]["Texts"])

		# Define the "Language texts" dictionary
		self.language_texts = self.Language.Item(self.texts)

		# Define the "separators" dictionary
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
		# Define the initial website dictionary
		self.website = {
			"URL format": "https://{}.{}/",
			"Domain": "",
			"Sub-domain": "",
			"URL": ""
		}

		# Define a shortcut to the website file
		website_file = self.folders["Mega"]["Websites"]["Website"]

		# If the websites "Website.json" file exists
		if self.File.Exists(website_file) == True:
			# Read the JSON file
			dictionary = self.JSON.To_Python(website_file)

			# Import the "Domain" and "Sub-domain" keys
			for key in ["Domain", "Sub-domain"]:
				self.website[key] = dictionary[key]

		# Define the website URL by formatting the URl format with the sub-domain and domain
		self.website["URL"] = self.website["URL format"].format(self.website["Sub-domain"], self.website["Domain"])

		# Update the "Website.json" file to add the "URL format" and "URL" keys
		self.JSON.Edit(website_file, self.website)

		# ---------- #

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
		# Get the method name which ran this method
		method_name = type(self).__name__

		# Define the default separator number if it is None
		if separator_number == None:
			# Define it as five
			separator_number = 5

			# If the method name is not "Update_Websites"
			if method_name != "Update_Websites":
				# Define the separator number as one
				separator_number = 1

		# Get the separator with the separator number
		separator = self.separators[str(separator_number)]

		# If the "open" parameter is True
		if open == True:
			# Define the text key as "opening"
			text_key = "opening"

		# If the "close" parameter is True
		if close == True:
			# Define the text key as "closing"
			text_key = "closing"

		# Define the correct text based on the "open" and "close" parameters
		text = self.language_texts[text_key + "_the_server"]

		# Add the server name to the [open/close] text
		text += ' "' + self.server["Name"] + '"'

		# If the "show text" parameter is True
		if show_text == True:
			# Show the separator and the text
			print()
			print(separator)
			print()
			print(text + "...")

		# If the "open" parameter is True
		if open == True:
			# Open the server
			self.System.Open(self.server["Server"], verbose = False)

			# If the "Testing" switch is False
			if self.switches["Testing"] == False:
				# Wait for three seconds
				self.Date.Sleep(3)

		# If the "close" parameter is True
		if close == True:
			# Close the programs of the server
			for program in self.server["Programs"]:
				self.System.Close(program)
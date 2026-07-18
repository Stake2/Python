# PHP.py

# Import some useful modules
import importlib

# Define the main "PHP" class
class PHP(object):
	def __init__(self):
		# Define the variables of the class
		self.Define_Variables()

		# Define the dictionaries
		self.Define_Dictionaries()

		# Define the server
		self.Define_Server()

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
			"Text"
		]

		# Iterate through the list of utility classes
		for class_title in self.modules["Utility"]["List"]:
			# If the class is not already inside the self class (PHP)
			if hasattr(self, class_title) == False:
				# If the class title is not inside the list of utility classes to not import
				# And it is is not inside the list of optional classes
				if (
					class_title not in do_not_import and
					class_title not in self.modules["Utility"]["Optional"]
				)
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

		# Create a shortcut to the current year number
		self.current_year = self.date["Units"]["Year"]

		# ---------- #

		# Define the "Texts" dictionary
		self.texts = self.JSON.To_Python(self.module["Files"]["Texts"])

		# Define the "Language texts" dictionary
		self.language_texts = self.Language.Item(self.texts)

	def Define_Dictionaries(self):
		# Define the initial website dictionary
		self.website = {
			"URL format": "https://{}.{}/",
			"Domain": "",
			"Sub-domain": "",
			"URL": ""
		}

		# Create a shortcut to the "Website.json" file
		website_file = self.folders["Websites"]["Website"]

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
		self.websites = self.JSON.To_Python(self.folders["PHP"]["JSON"]["Websites"])

		# Read the "URL.json" file to get the "URL" dictionary
		self.url = self.JSON.To_Python(self.folders["PHP"]["JSON"]["URL"])

		# Read the "Colors.json" file to get the "Colors" dictionary
		self.colors = self.JSON.To_Python(self.folders["PHP"]["JSON"]["Colors"])

	def Define_Server(self):
		# Define the "Server" dictionary
		self.server = {
			"Name": "XAMPP",
			"Server": self.folders["XAMPP"]["XAMPP Control"],
			"Programs": [
				"xampp-control",
				"httpd",
				"mysqld"
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

		# If the separator number is not zero and not None
		if separator_number not in [0, None]:
			# Get the separator text with the separator number
			separator = self.separators[str(separator_number)]

		# If the "open" parameter is True
		if open == True:
			# Define the text key as "opening"
			text_key = "opening"

		# If the "close" parameter is True
		if close == True:
			# Define the text key as "closing"
			text_key = "closing"

		# Define the correct text based on the defined text key
		# ("Opening" or "Closing" + " the server")
		text = self.language_texts[text_key + "_the_server"]

		# Add the server name to the [open/close] text
		text += ' "' + self.server["Name"] + '"'

		# If the "show text" parameter is True
		if show_text == True:
			# If the separator number is not zero
			if separator_number != 0:
				# Show the separator
				print()
				print(separator)

			# Show the text
			print()
			print(text + "...")

		# If the "open" parameter is True
		if open == True:
			# Open the server
			self.System.Open(self.server["Server"])

			# If the "Testing" switch is False
			if self.switches["Testing"] == False:
				# Wait for three seconds
				self.Date.Sleep(3)

		# If the "close" parameter is True
		if close == True:
			# Close the programs of the server
			self.System.Close(self.server["Programs"])
# Language.py

# Import some useful modules
import os
import pathlib
import re
import json
import pytz
import datetime
import locale as locale_module
from encodings.aliases import aliases as encoding_aliases
from copy import deepcopy

class Language():
	def __init__(self):
		# Import the classes
		self.Import_Classes()

		# Define the folders of the module
		self.folders = self.Define_Folders(object = self, files = ["Languages"]).folders

		# Define the "Switches" dictionary
		self.Define_Switches()

		# Define the lists and dictionaries of the module
		self.Define_Lists_And_Dictionaries()

		# Define the languages
		self.Define_Languages()

		# Create the mapping dictionary
		self.Create_Mapping_Dictionary()

		# Create the locale dictionary
		self.Create_Locale_Dictionary()

		# Get information about the system
		self.Get_System_Information()

		# Define the browsers dictionary
		self.Define_Browsers()

		# Define the texts of the module
		self.Define_Texts()

		# Define the language texts
		self.Define_Language_Texts()

		# Process the user settings
		self.Process_Settings()

	def Import_Classes(self):
		import importlib

		# Define the list of modules to be imported
		modules = [
			"Define_Folders",
			"Global_Switches"
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

	def Define_Switches(self):
		# Get the "Switches" dictionary from the "Global_Switches" module
		self.switches = self.Global_Switches.switches["Global"]

		# Update the "Switches" dictionary, adding the "Folder" and "File" dictionaries
		self.switches.update({
			"Folder": {
				"Create": True,
			},
			"File": {
				"Create": True,
				"Edit": True
			}
		})

		# If the "Testing" switch is True
		if self.switches["Testing"] == True:
			# Iterate through the switch keys
			for item in ["Folder", "File"]:
				# Iterate through the switches inside the "Switches" dictionary
				for switch in self.switches[item]:
					# Define them as False
					self.switches[item][switch] = False

	def Sanitize(self, path):
		# Replace double backwards slashes with one forward slash
		path = os.path.normpath(path).replace("\\", "/")

		# If there is no forward slash in the path
		# And the last character returned by the "splittext" method is an empty string
		if (
			"/" not in path[-1] and
			os.path.splitext(path)[-1] == ""
		):
			# Add a forward slash to the end of the path
			path += "/"

		# Return the path
		return path

	def Verbose(self, text, item, verbose = None):
		# If the "Verbose" switch is True
		# And the verbose parameter is None
		# Or the verbose parameter is True
		if (
			self.switches["Verbose"] == True and
			verbose == None or
			verbose == True
		):
			import inspect

			# Get the name of the method which ran this method (the "Verbose" one)
			runner_method_name = inspect.stack()[1][3]

			# Show the module name (Language) and the method which ran this method (the "Verbose" one)
			print()
			print(self.module["Name"] + "." + runner_method_name + "():")

			# Show the verbose text
			print("\t" + text + ":")

			# Show the verbose item
			print("\t" + item)

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

	def File_Create(self, file):
		# Sanitize the file path
		file = self.Sanitize(file)

		# If the file already exists, return False
		if self.File_Exists(file) == True:
			return False

		# If the file does not exist
		# And the "Create" file switch is True
		if (
			self.File_Exists(file) == False and
			self.switches["File"]["Create"] == True
		):
			# Open the file handle in write mode to create it
			create = self.File_Open(file, "w")

			# Close the file handle
			create.close()

			# Show the verbose text saying that the file was created
			self.Verbose(self.language_texts["file, title()"] + " " + self.language_texts["created, masculine"], file)

			return True

		# If the "Create" file switch is False
		if self.switches["File"]["Create"] == False:
			# Define the verbose text to tell the user that the file was not created due to the lack of permissions
			verbose_text = self.language_texts["it_was_not_possible_to_{}_the_file_permission_not_granted"].format(self.language_texts["create"]) + "." + "\n\n\t" + self.language_texts["file, title()"]

			# Show the verbose text
			self.Verbose(verbose_text, file)

			return False

	def File_Open(self, file, mode = "r", encoding = "UTF8"):
		# Open the file with the mode and encoding
		return open(file, mode, encoding = encoding)

	def File_Contents(self, file):
		# Sanitize the file path
		file = self.Sanitize(file)

		# Define the contents dictionary
		contents = {
			"Lines": [],
			"String": "",
			"Size": 0,
			"Length": 0
		}

		# If the file exists
		if self.File_Exists(file) == True:
			# Open the file handle in read mode (the default mode)
			file_handle = self.File_Open(file)

			# Iterate through the lines inside the file
			for line in file_handle.readlines():
				# Remove the line break from the line
				line = line.replace("\n", "")

				# Add the line to the list of lines
				contents["Lines"].append(line)

			# Reset cursor to the beginning of the file before getting the file string
			file_handle.seek(0)

			# Read the file and get its string
			contents["String"] = file_handle.read()

			# Close the file handle
			file_handle.close()

			# Get the size of the file
			contents["Size"] = os.path.getsize(file)

			# Get the length of the file
			contents["Length"] = len(contents["Lines"])

		# If the file does not exist
		if self.File_Exists(file) == False:
			# Show the verbose text saying that the file does not exist
			self.Verbose(self.language_texts["this_file_does_not_exists"], file)

		# Return the contents dictionary
		return contents

	def File_Edit(self, file, text, mode = "w", next_line = True, verbose = None, full_verbose = False):
		# Sanitize the file path
		file = self.Sanitize(file)

		# Get the contents of the file
		contents = self.File_Contents(file)

		# Define a shortcut to the file length
		length = contents["Length"]

		# Define the line break as an empty string
		line_break = ""

		# If the "next line" parameter is True
		# And the file length is not zero
		# And the mode is "a" (append)
		if (
			next_line == True and
			length != 0 and
			mode == "a"
		):
			# Define the line break as the new line caracter
			line_break = "\n"

		# Define the verbose text for the file as the file and the text
		verbose_text = file + "\n" + \
		"\n" + \
		"\t" + text

		# Add the line break to the text
		text = line_break + text
		
		# If the file exists
		if self.File_Exists(file) == True:
			# If the file "Edit" switch is True
			# And the file text string is not equal to the parameter text
			if (
				self.switches["File"]["Edit"] == True and
				contents["string"] != text
			):
				# Open the file handle
				edit = self.File_Open(file, mode)

				# Write the text into the file
				edit.write(text)

				# Close the file handle
				edit.close()

				# Show the file
				self.Verbose("File edited", verbose_text, verbose = verbose)

			# If the file "Edit" switch is True, return True
			if self.switches["File"]["Edit"] == True:
				return True

			# If the file "Edit" switch is False, return False
			if self.switches["File"]["Edit"] == False:
				return False

		# If the file does not exist
		if self.File_Exists(file) == False:
			# Show the file and return False
			self.Verbose("The file does not exist", file)

			return False

	def JSON_Edit(self, file, text, next_line = True, verbose = None, full_verbose = False, edit = False):
		# Sanitize the file path
		file = self.Sanitize(file)

		# Get the contents of the file
		contents = self.File_Contents(file)

		# Transform the text into the JSON format
		text = self.JSON_From_Python(text)

		# Define the verbose text for the file as the file and the text
		verbose_text = file + "\n" + \
		"\n" + \
		"Text:" + "\n" + \
		"[" + text + "]"

		# If the file exists
		if self.File_Exists(file) == True:
			# If the file "Edit" switch is True
			# Or the edit parameter is True
			if (
				self.switches["File"]["Edit"] == True or
				edit == True
			):
				# If the file text string is not equal to the parameter text
				if contents["String"] != text:
					# Open the file handle in write mode
					edit = self.File_Open(file, "w")

					# Write the text into the file
					edit.write(text)

					# Close the file handle
					edit.close()

					# Show the file
					self.Verbose("File edited", verbose_text, verbose = verbose)

			# If the file "Edit" switch is True
			# And the "edit" parameter is True
			if (
				self.switches["File"]["Edit"] == True or
				edit == True
			):
				return True

			# If the file "Edit" switch is False
			# And the "edit" parameter is False
			if (
				self.switches["File"]["Edit"] == False and
				edit == False
			):
				return False

		# If the file does not exist
		if self.File_Exists(file) == False:
			# Show the file return False
			self.Verbose("The file does not exist", file, verbose = verbose)

			return False

	def JSON_Dumps(self, items):
		# Dump the items
		items = json.dumps(items, indent = "\t", ensure_ascii = False)

		# Return the items
		return items

	def JSON_From_Python(self, items):
		# Import some useful modules
		import types

		# If the items parameter is a dictionary
		if type(items) == dict:
			# Convert it into a dictionary using the "dict" function
			items = dict(items)

			# Iterate through the keys and values of the items dictionary
			for key, value in items.items():
				# If the type name of the value is either "Credentials" or "Resource"
				# Or it is not a number, a dictionary, or a list
				if (
					type(value).__name__ in ["Credentials", "Resource"] or
					type(value) not in [int, dict, list]
				):
					# Convert it to a string
					items[key] = str(value)

		# Make a copy of the items parameter
		items_copy = deepcopy(items)

		# If the items parameter is a dictionary
		if type(items_copy) == dict:
			# Iterate through its keys and values
			for key, value in items_copy.items():
				# If the value is not a string, number, list, dictionary, boolean, or None
				if type(value) not in [str, int, list, dict, bool, None]:
					# Convert it into a string
					value = str(value)

				# Update the value inside the root dictionary
				items_copy[key] = value

				# If the value is a dictionary
				if type(value) == dict:
					# Iterate through its sub-keys and sub-values
					for sub_key, sub_value in value.items():
						# If the sub-value is not a string, number, list, dictionary, boolean, or None
						if type(sub_value) not in [str, int, list, dict, bool, None]:
							# Convert it into a string
							sub_value = str(sub_value)

						# Update the sub-value inside the root dictionary
						value[sub_key] = sub_value

						# If the sub-value is a dictionary
						if type(sub_value) == dict:
							# Iterate through its sub-sub-keys and sub-sub-values
							for sub_sub_key, sub_sub_value in sub_value.items():
								# If the sub-sub-value is not a string, number, list, dictionary, boolean, or None
								if type(sub_sub_value) not in [str, int, list, dict, bool, None]:
									# Convert it into a string
									sub_sub_value = str(sub_sub_value)

								# Update the sub-sub-value inside the root dictionary
								sub_value[sub_sub_key] = sub_sub_value

						# Update the sub-value inside the root dictionary
						value[sub_key] = sub_value

				# Update the value inside the root dictionary
				items_copy[key] = value

		# If the items parameter is a list
		if type(items_copy) == list:
			# Iterate through the items in the list
			i = 0
			for item in items_copy:
				# Convert it into a date string
				item = str(item)

				# Update the item in the root list
				items_copy[i] = item

				# Add one to the "i" number
				i += 1

		# If the items parameter is a string
		if type(items_copy) == str:
			# Convert it into a Python object
			items_copy = self.JSON_To_Python(items_copy)

		# Dump the items
		items_copy = self.JSON_Dumps(items_copy)

		# Return the items dictionary
		return items_copy

	def JSON_To_Python(self, item):
		# If the item is a file
		if self.File_Exists(item) == True:
			# Sanitize the file path
			item = self.Sanitize(item)

			# Convert the file text into a Python dictionary
			dictionary = json.load(open(item, encoding = "utf8"))

		# If the item is not a file
		if self.File_Exists(item) == False:
			# Convert the JSON dictionary into a Python dictionary
			dictionary = json.loads(item)

		# Return the Python dictionary
		return dictionary

	def JSON_Show(self, json, return_text = False):
		# Convert the JSON from Python to JSON text
		json = self.JSON_From_Python(json)

		# If the "return text" parameter is False, show the text
		if return_text == False:
			print(json)

		# If it is True, return the text
		if return_text == True:
			return json

	def Define_Lists_And_Dictionaries(self):
		self.dictionary_separators = [
			"=",
			" = ",
			":",
			": "
		]

		self.setting_names = {
			"language": {
				"key": "language",
				"name": {
					"en": "language",
					"pt": "idioma"
				},
				"list": [
					"language",
					"Language",
					"idioma",
					"Idioma",
					"linguagem",
					"Linguagem"
				]
			},
			"text_language": {
				"key": "text_language",
				"name": {
					"en": "text_language",
					"pt": "idioma_de_texto"
				},
				"list": [
					"text language",
					"Text language",
					"idioma de texto",
					"Idioma de texto"
				]
			}
		}

	def Define_Languages(self):
		# Get the root languages dictionary
		self.languages = self.JSON_To_Python(self.module["Files"]["Languages"])

		# Make a local copy of the small languages list
		small_languages = deepcopy(self.languages["Small"])

		# Iterate through the list of small languages
		for small_language in self.languages["Small"]:
			# If the language is not in the "Supported" languages list
			if small_language not in self.languages["Supported"]:
				# Remove it from the "Small" list
				self.languages["Small"].remove(small_language)

		# Reset the languages "Dictionary" to be empty
		self.languages["Dictionary"] = {}

		# Iterate through the list of small languages
		for small_language in self.languages["Small"]:
			# Get the full language
			full_language = self.languages["Full"][small_language]

			# Get the list of translated languages
			translated_languages = self.languages["Translated"][small_language]

			# Iterate through them
			for translated_language in deepcopy(translated_languages):
				# If the language is not in the "Supported" languages list
				if translated_language not in self.languages["Supported"]:
					# Remove it from the translated languages dictionary
					translated_languages.pop(translated_language)

			# Define the language dictionary
			dictionary = {
				"Small": small_language,
				"Full": full_language,
				"Translated": translated_languages
			}

			# Define the language dictionary inside the languages "Dictionary" using the small language as a key
			self.languages["Dictionary"][small_language] = dictionary

		# Make a local copy of the languages dictionary
		languages_copy = deepcopy(self.languages)

		# Define the list of small languages of the local copy as the backup list
		languages_copy["Small"] = small_languages 

		# Update the "Languages.json" file with the updated local copy of the languages dictionary
		self.JSON_Edit(self.module["Files"]["Languages"], languages_copy, edit = True, verbose = False)

		# Define the countries dictionary
		self.countries = self.languages["Countries"]

	def Create_Mapping_Dictionary(self):
		# Define the default mapping dictionary
		self.mapping = {
			"Locales": {},
			"Encodings": {}
		}

		# Invert the keys and values of the "locale alias" dictionary
		for alias, locale_name in locale_module.locale_alias.items():
			# Remove the encoding from the locale name
			locale_name = locale_name.split(".")[0]

			# If the locale list is not present inside the "Locales" dictionary
			if locale_name not in self.mapping["Locales"]:
				# Create it
				self.mapping["Locales"][locale_name] = []

			# Add the alias to the list of aliases
			self.mapping["Locales"][locale_name].append(alias)

			# If the locale name is not inside the list of aliases
			if locale_name not in self.mapping["Locales"][locale_name]:
				# Add the locale name to the list of aliases
				self.mapping["Locales"][locale_name].append(locale_name)

		# Invert the keys and values of the "encoding aliases" dictionary
		for alias, encoding in encoding_aliases.items():
			# If the encoding list is not present inside the "Encodings" dictionary
			if encoding not in self.mapping["Encodings"]:
				# Create it
				self.mapping["Encodings"][encoding] = []

			# Add the alias to the list of aliases
			self.mapping["Encodings"][encoding].append(alias)

			# If the encoding is not inside the list of aliases
			if encoding not in self.mapping["Encodings"][encoding]:
				# Add the encoding to the list of aliases
				self.mapping["Encodings"][encoding].append(encoding)

	def Create_Locale_Dictionary(self):
		# Define the default locale dictionary
		self.locale = {
			"Locale": {
				"Original": locale_module.getdefaultlocale(),
				"Mapped": "",
				"Locale": "",
				"List": [],
				"Information": {}
			},
			"Encoding": {
				"Original": "",
				"Mapped": "",
				"List": []
			},
			"Module": locale_module
		}

		# Updated the mapped lists of locales and encodings based on the original locale
		self.Updated_Mapped_Lists(self.locale["Locale"]["Original"])

		# Define the original encoding
		self.locale["Encoding"]["Original"] = self.locale["Locale"]["Original"][1]

		# Set the locale using the mapped locale

		# Iterate through the list of locales
		for locale in self.locale["Locale"]["List"]:
			# Iterate through the list of encodings
			for encoding in self.locale["Encoding"]["List"]:
				# Map the two
				mapped = locale + "." + encoding

				# Try to set the locale
				try:
					locale_module.setlocale(locale_module.LC_ALL, mapped)

					# ----- #

					# Update the full locale (locale + encoding)
					self.locale["Locale"]["Mapped"] = mapped

					# ----- #

					# Update the mapped encoding
					self.locale["Encoding"]["Mapped"] = encoding

					# ----- #

					# Update the locale
					self.locale["Locale"]["Locale"] = locale

				except locale_module.Error as e:
					pass

		# Update the locale information
		self.locale["Locale"]["Information"] = locale_module.localeconv()

		# Update the "Module" key
		self.locale["Module"] = locale_module

	def Updated_Mapped_Lists(self, locale):
		# Get the list of locales
		locales = self.mapping["Locales"][locale[0]]

		# Fill the locales list
		self.locale["Locale"]["List"] = locales

		# ----- #

		# Get the list of encodings
		encodings = self.mapping["Encodings"][locale[1]]

		# Fill the encodings list
		self.locale["Encoding"]["List"] = encodings

	def Get_System_Information(self):
		# Import some useful modules
		import platform
		import ctypes
		from tzlocal import get_localzone

		# ---------- #

		# Define the "system" dictionary
		self.system = {
			"Name": platform.system(), # The name of the system
			"Architecture": "",
			"Type": "",
			"Resolution": {},
			"Browsers": {}
		}

		# Get the local architecture tuple
		architecture = platform.architecture()

		# Define a bitness map
		bitness_map = {
			"32bit": "32 bits",
			"64bit": "64 bits"
		}

		# Define the system "Architecture"
		self.system["Architecture"] = bitness_map[architecture[0]]

		# Define the system type
		self.system["Type"] = architecture[1]

		# Get the "user32" class
		user32 = ctypes.windll.user32

		# Add the width
		self.system["Resolution"]["Width"] = str(user32.GetSystemMetrics(0))

		# Add the height
		self.system["Resolution"]["Height"] = str(user32.GetSystemMetrics(1))

		# Join the two dimensions
		self.system["Resolution"]["Dimensions"] = self.system["Resolution"]["Width"] + "x" + self.system["Resolution"]["Height"]

		# ---------- #

		# Define the "user" dictionary
		self.user = {
			# Get the user name, folder, and timezone
			"Name": str(pathlib.Path.home().name), 
			"Folder": self.Sanitize(str(pathlib.Path.home())),
			"Timezone": get_localzone(),

			# Get the user (system) locale
			"Locale": self.locale,

			# Define the empty user "Language" dictionary
			"Language": {},

			# Define the user "Country" dictionary
			"Country": {}
		}

		# ---------- #

		# Define a shortcut to the user timezone
		user_timezone = str(self.user["Timezone"])

		# Define a default date
		date = datetime.datetime.now()

		# Remove the microsecond from the date object
		date = date.replace(microsecond = 0)

		# Define the date object in the user timezone
		user_timezone_date = date.astimezone(self.user["Timezone"])

		# Update the user "Timezone" dictionary
		self.user["Timezone"] = {
			"String": user_timezone,
			"Name": user_timezone_date.strftime("%Z"),
			"UTC offset": user_timezone_date.strftime("%z"),
			"Timezone information": pytz.timezone(user_timezone)
		}

		# ---------- #

		# Define a shortcut to the user locale
		locale_shortcut = self.user["Locale"]["Locale"]["Original"]

		# Define the small language
		small_language = locale_shortcut[0].split("_")[0]

		# Define the user "Language" dictionary with the small language as a key
		self.user["Language"] = self.languages["Dictionary"][small_language]

		# Define the language with country
		self.user["Language"]["With country"] = locale_shortcut[0]

		# Get the country
		country = self.user["Language"]["With country"].split("_")[1]

		# Define the country code
		self.user["Country"]["Code"] = country

		# Get the country name
		country_name = self.languages["Countries"][country]

		# Define the country name
		self.user["Country"]["Name"] = country_name

		# ---------- #

		# Define a shortcut to a copy of the user "Language" dictionary
		self.language = deepcopy(self.user["Language"])

		# Remove the "With country" key
		self.language.pop("With country")

	def Define_Architecture_Folder(self, browser_folder, architecture = ""):
		# If the "architecture" parameter is empty
		if architecture == "":
			# Define it as the system architecture
			architecture = self.system["Architecture"]

		# Get the hard drive letter
		hard_drive_letter = os.path.normpath(pathlib.Path.home().drive) + "/"

		# Define the architecture folders
		program_files_32_bits = "Program Files (x86)/"
		program_files_64_bits = "Program Files/"

		# If the architecture is "32 bits"
		if architecture == "32 bits":
			# Define the root folder as the 32 bits one
			root_folder = hard_drive_letter + program_files_32_bits

		# If the architecture is "64 bits"
		if architecture == "64 bits":
			# Define the root folder as the 64 bits one
			root_folder = hard_drive_letter + program_files_64_bits

		# Add the browser folder to the root folder
		root_folder += browser_folder

		# Return the root folder
		return root_folder

	def Define_Browsers(self):
		# Define a dictionary of browsers
		self.browsers = {
			"Numbers": {
				"Total": 0
			},
			"List": [
				"Mozilla Firefox",
				"Microsoft Edge",
				"Google Chrome"
			],
			"Dictionary": {},
			"Data": {
				"Mozilla Firefox": {
					"Windows": "Mozilla Firefox/",
					"Linux": "firefox",
					"Darwin": "Firefox.app",
					"Darwin name": "firefox"
				},
				"Microsoft Edge": {
					"Windows": "Microsoft/Edge/Application/",
					"Linux": "microsoft-edge",
					"Darwin": "Microsoft Edge.app", # /Contents/MacOS/Microsoft Edge
					"Executable name": "msedge"
				},
				"Google Chrome": {
					"Windows": "Google/Chrome/Application/",
					"Linux": "google-chrome",
					"Darwin": "Google Chrome.app" # /Contents/MacOS/Google Chrome
				}
			}
		}

		# Iterate through the list of browsers
		for browser in self.browsers["List"]:
			# Define the browser dictionary
			browser = {
				"Name": browser,
				"Company": browser.split(" ")[0],
				"Data": self.browsers["Data"][browser],
				"Folders": {
					"root": ""
				},
				"File": ""
			}

			# If the system is "Windows"
			if self.system["Name"] == "Windows":
				# Get the browser folder from the browser "Data" dictionary
				browser_folder = browser["Data"]["Windows"]

				# Define the root as the local root folder and the browser folder
				browser["Folders"]["root"] = self.Define_Architecture_Folder(browser_folder)

				# Define the local executable name as the sub-browser name
				executable_name = browser["Name"].split(" ")[1].lower()

				# If the "Executable name" key is inside the browser "Data" dictionary
				if "Executable name" in browser["Data"]:
					# Define it as the local executable name
					executable_name = browser["Data"]["Executable name"]

				# Define the browser file as the root browser folder plus the executable name and the ".exe" extension
				browser["File"] = browser["Folders"]["root"] + executable_name + ".exe"

				# If the file does not exist
				if self.File_Exists(browser["File"]) == False:
					# If the system architecture is "32 bits"
					if self.system["Architecture"] == "32 bits":
						# Define the root folder based on the "64 bits" architecture
						browser["Folders"]["root"] = self.Define_Architecture_Folder(browser_folder, "64 bits")

					# If the system architecture is "64 bits"
					if self.system["Architecture"] == "64 bits":
						# Define the "Program Files" folder based on the "32 bits" architecture
						browser["Folders"]["root"] = self.Define_Architecture_Folder(browser_folder, "32 bits")

					# Define the browser file as the root browser folder plus the executable name and the ".exe" extension
					browser["File"] = browser["Folders"]["root"] + executable_name + ".exe"

			# If the system is "Linux"
			if self.system["Name"] == "Linux":
				# Define the root folder as the default one for Linux applications plus the browser Linux folder
				browser["Folders"]["root"] = "/usr/bin/" + browser["Data"]["Linux"]

				# Define the browser file as the root browser folder (which is also the application)
				browser["File"] = browser["Folders"]["root"]

			# If the system is "Darwin" (macOS)
			if self.system["Name"] == "Darwin":
				# Define the root folder as the default one for macOS applications
				browser["Folders"]["root"] = "/Applications"

				# Define the Darwin name for the browser as the full browser name
				darwin_name = browser["Name"]

				# If the "Darwin name" key is inside the browser "Data" dictionary
				if "Darwin name" in browser["Data"]:
					# Use it as the Darwin name
					darwin_name = browser["Data"]["Darwin name"]

				# Define the browser file as the root browser folder plus the data folder for macOS plus "/Contents/MacOS/" plus the defined Darwin name
				browser["File"] = browser["Folders"]["root"] + browser["Data"]["Darwin"] + "/Contents/MacOS/" + darwin_name

			# If the browser executable file exists (if the browser is installed)
			if self.File_Exists(browser["File"]) == True:
				# Add it to the "Browsers" dictionary of the "system" dictionary
				self.system["Browsers"][browser["Name"]] = browser

			# Define the browser inside the browsers "Dictionary" key
			self.browsers["Dictionary"][browser["Name"]] = browser

		# Remove the "Data" key
		self.browsers.pop("Data")

		# Update the number of browsers with the length of the list of browsers
		self.browsers["Numbers"]["Total"] = len(self.browsers["List"])

	def Show_User_Information(self):
		# Show the class and method names and the "Showing user information" text
		print(self.language_texts["language_class"] + ", " + self.language_texts["show_user_information_method"] + ":")
		print("\t" + self.language_texts["showing_user_information"] + "...")
		print()

		# Define a quotes template
		quotes = '"{}"'

		# ---------- #

		# Show the user name
		print(self.language_texts["username, title(), type: self"] + ":")
		print("\t" + self.user["Name"])
		print()

		# Show the user folder
		print(self.language_texts["user_folder"] + ":")
		print("\t" + self.user["Folder"])
		print()

		# ---------- #

		# Show the user timezone
		print(self.language_texts["user_timezone"] + ":")

		# Show the timezone string
		print("\t" + self.language_texts["text, title()"] + ":")
		print("\t" + quotes.format(self.user["Timezone"]["String"]))
		print()

		# Show the timezone name
		print("\t" + self.language_texts["name, title()"] + ":")
		print("\t" + quotes.format(self.user["Timezone"]["Name"]))
		print()

		# Show the UTC offset
		print("\t" + self.language_texts["difference_from_utc"] + ":")

		utc_offset = self.user["Timezone"]["UTC offset"]

		if "-" in utc_offset:
			utc_offset = "UTC" + utc_offset

		print("\t" + utc_offset)
		print()

		# Show the timezone information
		print("\t" + self.language_texts["timezone_information"] + ":")
		print("\t" + str([self.user["Timezone"]["Timezone information"]]))
		print()

		# ---------- #

		# Show the user language information
		print(self.language_texts["user_language"] + ":")

		# Show the small language
		print("\t" + self.language_texts["small, title()"] + ":")
		print("\t" + quotes.format(self.language["Small"]))
		print()

		# Show the language with country
		print("\t" + self.language_texts["with_country"] + ":")
		print("\t" + quotes.format(self.user["Language"]["With country"]))
		print()

		# Show the full language
		print("\t" + self.language_texts["full, title()"] + ":")
		print("\t" + quotes.format(self.language["Full"]))
		print()

		# Show the full language translated
		print("\t" + self.language_texts["full_translated"] + ":")

		# Iterate through the language keys and dictionaries
		for small_language, language in self.languages["Dictionary"].items():
			# If the small language is not the user language
			if small_language != self.language["Small"]:
				# Get the current language translated to the user language
				translated_language = language["Translated"][self.language["Small"]]

				# Get the user language translated to the current language
				# (First the user language then the current language)
				translated_user_language = self.language["Translated"][small_language]

				# Show the current language translated to the user language
				print("\t\t" + translated_language + ":")

				# Show the user language but translated to the current language
				print("\t\t" + quotes.format(translated_user_language))
				print()

		# ---------- #

		# Show the user country code
		print(self.language_texts["country_code"] + ":")
		print("\t" + quotes.format(self.user["Country"]["Code"]))
		print()

		# Show the user country name
		print(self.language_texts["country_name"] + ":")
		print("\t" + quotes.format(self.user["Country"]["Name"][self.language["Small"]]))
		print()

		# ---------- #

		# Show the "System information" text
		print(self.language_texts["system_information"] + ":")

		# Show the system name
		print("\t" + self.language_texts["name, title()"] + ":")
		print("\t" + quotes.format(self.system["Name"]))
		print()

		# Show the system architecture
		print("\t" + self.language_texts["architecture, title()"] + ":")
		print("\t" + quotes.format(self.system["Architecture"]))
		print()

		# Show the system resolution
		print("\t" + self.language_texts["resolution, title()"] + ":")

		# Iterate through the list of sizes
		for key in ["Width", "Height", "Dimensions"]:
			# Define a text key
			text_key = key

			# If the size is "Dimensions"
			if key == "Dimensions":
				# Update the text key to "full"
				text_key = "Full"

			# Get the text for the size
			text = self.language_texts[text_key.lower() + ", title()"]

			# Get the size
			size = self.system["Resolution"][key]

			# If the size is not "Dimensions"
			if key != "Dimensions":
				# Add "px" to the size
				size += "px"

			# Show the text and the size
			print("\t\t" + text + ":")
			print("\t\t" + size)

			# If the key is not the last one
			if key != "Dimensions":
				# Show a space separator
				print()

		# If the "Browsers" dictionary is not empty
		if self.system["Browsers"] != {}:
			# Show a space separator
			print()

			# Show the installed browsers
			print("\t" + self.language_texts["installed_browsers"] + ":")

			# Iterate through the list of available browsers
			for browser in self.browsers["List"]:
				# If the browser is installed
				if browser in self.system["Browsers"]:
					# Show the browser name
					print("\t" + quotes.format(browser))

			# Show a space separator
			print()

	def Current_Folder(self, file = None):
		# If the file parameter is None, define the file as "__file__"
		if file == None:
			file = __file__

		# Get the folder from the module file
		folder = self.Sanitize(os.path.dirname(file))

		# Return the folder
		return folder

	def Select(self, options, language_options = None, show_text = None, select_text = None, function = False, first_space = True):
		if show_text == None:
			show_text = self.language_texts["options, title()"] + ": "

		if select_text == None:
			select_text = self.language_texts["select_an_item_from_the_list"] + ": "

		if first_space == True:
			print()

		print(show_text)

		list_ = options.copy()

		if language_options != None:
			list_ += language_options.copy()

		numbers = []

		i = 0
		for option in options:
			if language_options != None:
				option = language_options[i]

				if type(option) == str:
					list_.append(option.lower())
					list_.append(option[0].lower())

			print("[" + str(i + 1) + "]" + " - " + option)

			numbers.append(i)
			numbers.append(str(i))

			i += 1

		letters = []

		for option in options:
			if type(option) == str:
				letters.append(option[0].lower())

		list_ += letters
		list_ += numbers

		print()

		option = ""

		while option in ["", " "]:
			option = input(select_text)

		found_option = False

		try:
			option = int(option)
			option_number = option - 1

			try:
				option = options[option_number]
				found_option = True

			except IndexError:
				option = 1000

				while option not in list_:
					try:
						option = int(input(select_text))

					except ValueError:
						option = str(option)

				option_number = option - 1
				option = options[option_number]
				found_option = True

		except ValueError:
			option = str(option)

			while option not in list_:
				option = input(select_text)

				try:
					option = int(option)
					option_number = option - 1

				except ValueError:
					option = str(option)

		possible_options = [option]

		if type(option) == str and found_option == False:
			possible_options.extend([
				str(option),
				str(option.lower()),
				str(option.title()),
				str(option.capitalize()),
				str(option.lower().title()),
				str(option.title()),
				str(option.capitalize())
			])

		i = 0
		for possible_option in possible_options:
			if type(possible_option) == str and found_option == False:
				if language_options != None:
					for option_ in language_options:
						if re.findall(possible_option, option_, re.IGNORECASE) != []:
							option = option_

							found_option = True

				if language_options == None:
					for option_ in options:
						if re.findall(possible_option, option_, re.IGNORECASE) != []:
							option = option_

							found_option = True
			i += 1

		if type(option) == str:
			i = 0
			for option_ in options:
				if option == option_:
					option_number = i

				i += 1

		dictionary = {
			"option": option,
			"language_option": option,
			"number": option_number,
		}

		if language_options != None:
			dictionary["language_option"] = language_options[dictionary["number"]]

		if found_option == True:
			print()
			print(self.language_texts["you_selected_this_option"] + ":")

			if language_options != None and str(option) != dictionary["language_option"]:
				print("\t" + dictionary["language_option"])
				print("\t" + str(option))

			if language_options == None or str(option) == dictionary["language_option"]:
				print(str(option))

			if function == True and type(option) in [function, type]:
				option()

		return dictionary

	def Define_Yes_Or_No(self, response):
		if response in ["Yes", self.language_texts["yes, title()"]]:
			return True

		if response in ["No", self.language_texts["no, title()"]]:
			return False

	def Yes_Or_No(self, question, convert_to_text = False, first_space = True):
		options = [
			self.language_texts["yes, title()"],
			self.language_texts["no, title()"],
		]

		if type(question) == dict:
			question = self.Item(question)

		option = self.Select(options, show_text = question + "?", select_text = self.language_texts["select_{}_or_{}_(number_or_word)"] + ": ", first_space = first_space)["option"]

		option = self.Define_Yes_Or_No(option)

		if convert_to_text == True:
			if option == True:
				option = self.language_texts["yes, title()"]

			if option == False:
				option = self.language_texts["no, title()"]

		return option

	def Type(self, text = None, accept_enter = True, next_line = False, first_space = True):
		if text == None:
			text = self.language_texts["type_or_paste_the_text"] + ": "

		if type(text) == dict:
			text = self.Item(text) + ": "

		if first_space == True:
			print()

		typed = ""

		if next_line == False:
			if accept_enter == True:
				typed = input(text)

			if accept_enter == False:
				while typed == "":
					typed = input(text)

		if next_line == True:
			print(text)

			if accept_enter == True:
				typed = input()

			if accept_enter == False:
				while typed == "":
					typed = input()

		return typed

	def Item(self, texts, user_language = None):
		if user_language == None:
			user_language = self.language["Small"]

		if user_language in texts:
			return texts[user_language]

		if user_language not in texts:
			language_texts = {}

			list_ = []

			for key in texts:
				language_texts[key] = texts[key]

				if type(language_texts[key]) == dict and user_language in language_texts[key]:
					if "masculine" in language_texts[key][user_language] or "feminine" in language_texts[key][user_language]:
						list_.append(True)

			add_gender_texts = False

			if len(list_) != 0:
				add_gender_texts = True

			del list_

			for key in texts:
				language_texts[key] = texts[key]

				if type(texts[key]) == dict and user_language in texts[key]:
					language_texts[key] = texts[key][user_language]

				language_texts[key + ", masculine"] = language_texts[key]
				language_texts[key + ", feminine"] = language_texts[key]

				if add_gender_texts == True and type(language_texts[key]) == dict:
					if "masculine" in language_texts[key]:
						language_texts[key + ", masculine"] = language_texts[key]["masculine"]

					if "feminine" in language_texts[key]:
						language_texts[key + ", feminine"] = language_texts[key]["feminine"]

					if "masculine" in language_texts[key]:
						language_texts[key] = language_texts[key]["masculine"]

			return language_texts

	def Define_Texts(self):
		# Define the "Texts" dictionary
		self.texts = self.JSON_To_Python(self.module["Files"]["Texts"])

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

	def Define_Language_Texts(self):
		# Get the language texts dictionary
		self.language_texts = self.Item(self.texts)

		for language_type in self.languages["Types"]:
			language_type = language_type.lower().replace(" ", "_")

			self.language_texts["your_" + language_type + "_is"] = self.language_texts["your_{}_is"].format(self.Item(self.texts[language_type]))

		self.settings_file = self.folders["Apps"]["root"] + self.language_texts["settings"].capitalize() + ".json"

		if self.File_Exists(self.settings_file) == False:
			self.Create(self.settings_file)
			self.JSON_Edit(self.settings_file, {})

	def Process_Settings(self):
		# Define the default root settings dictionary
		self.settings = {}

		# If the settings file exists
		if self.File_Exists(self.settings_file) == True:
			# Read the "Settings.json" file to get the settings dictionary
			settings = self.JSON_To_Python(self.settings_file)

			# Iterate through the setting names inside the "setting names" list
			for setting_name in self.setting_names:
				possible_setting_names = self.setting_names[setting_name]["list"]

				for possible_setting_name in possible_setting_names:
					if possible_setting_name in settings:
						setting = settings[possible_setting_name]

						# If the setting name is "Language"
						if setting_name == "Language":
							# Get the locale based on the setting
							locale_shortcut = setting

							# Define the "Language" dictionary keys
							self.system["Language"]["Small"] = locale_shortcut[0].split("_")[0]
							self.system["Language"]["With country"] = locale_shortcut[0]
							self.system["Language"]["Full"] = self.languages["Full"][self.system["Language"]["Small"]]

						self.settings[setting_name.replace("_", " ").capitalize()] = setting

						key = self.setting_names[setting_name]["name"][self.language["Small"]].replace("_", " ").capitalize()

						self.settings[key] = setting

			self.Define_Language_Texts()

			# Update the "Settings.json" file with the new settings dictionary
			self.JSON_Edit(self.settings_file, self.settings)

			# ----- #

			# Create 
			settings = {
				"Language": self.settings["Language"]
			}

			self.global_settings_file = self.folders["Apps"]["root"] + "Settings.json"

			self.File_Create(self.global_settings_file)
			self.JSON_Edit(self.global_settings_file, settings)

		# If the settings file does not exist
		if self.File_Exists(self.settings_file) == False:
			texts = {
				"en": "Default settings file not found, do you want to select settings",
				"pt": "Arquivo padrão de configurações não encontrado, você quer selecionar configurações",
			}

			option = self.Yes_Or_No(texts)

			if option == True:
				self.Create_Settings()

	def Create_Settings(self):
		# Create the folder
		folder = self.Create(None, self.texts["type_or_paste_the_folder_where_you_want_to_create_the_settings_file"])

		settings_file = folder + self.language_texts["settings"].title() + ".txt"

		# Create file
		self.Create(settings_file)

		# Ask for each setting
		for setting_name in self.setting_names:
			setting_information = self.setting_names[setting_name]

			language_setting_name = setting_information["name"][self.app_settings["Language"]]

			option = self.Select(self.languages["Small"], show_text = self.language_texts["languages"].title() + ":", select_text = self.language_texts["select_one_{}_(number_or_word), masculine"].format(language_setting_name) + ": ")

			self.File_Edit(settings_file, setting_name.title() + ": " + option, "a")

		self.Read_Settings_File()

	def Copy(self, text):
		import pyperclip

		pyperclip.copy(text)

		self.Verbose(self.language_texts["copied_text"], text)

	def Create_Language_Text(self):
		template = '''"[key]": {
		[input]
	},'''

		empty_json = self.Yes_Or_No(self.language_texts["is_the_json_file_empty"])

		if empty_json == False:
			template = template.replace('"[key]', ',\n\t"[key]')
			template = template.replace('},', "}")

		if empty_json == True:
			template = "{\n\t" + template + "\n}"

		text = template

		# Iterate through the language keys and dictionaries
		for small_language, language in self.languages["Dictionary"].items():
			# Get the current language translated to the user language
			translated_language = language["Translated"][self.language["Small"]]

			typed = self.Type(self.language_texts["type_the_text_in_{}"].format(translated_language) + ": ", accept_enter = False, next_line = True)

			if small_language == "en":
				key = typed.lower().replace(" ", "_")

				for item in [":", '"', "'", "\n", "."]:
					key = key.replace(item, "")

				if " " not in typed and typed[0].isupper() == True:
					key += ", title()"

				text = text.replace("[key]", key)

			typed = typed.replace('"', '\\"')

			language_text = '"' + small_language + '": "' + typed + '"'

			if small_language != self.languages["Small"][-1]:
				language_text += "," + "\n\t\t[input]"

			text = text.replace("[input]", language_text)

		self.Copy(text)

		return text

	def Text_From_List(self, list_, next_line = True, separator = ""):
		string = ""

		i = 0
		for item in list_:
			string += item

			if i != len(list_) - 1:
				if separator != "":
					string += separator

				if next_line == True:
					string += "\n"

			i += 1

		return string

	# Make the text difference between the text inside the file and the text to be written
	def Text_Difference(self, file_text, text_lines_to_write, filters = {}):
		# Get the lines list if the file text is a dictionary
		if type(file_text) == dict:
			file_text = file_text["Lines"]

		# Get the lines list if the file text is a string
		if type(text_lines_to_write) == str:
			text_lines_to_write = text_lines_to_write.splitlines()

		settings = filters

		# Define the difference dictionary
		dictionary = {
			"Difference": {
				"Lines": [],
				"Text": ""
			},
			"Additions": 0,
			"Changes": 0,
			"Deletions": 0
		}

		# Get the length of the lines to write and the number of lines inside the file
		text_lines_number = len(text_lines_to_write)
		file_lines_number = len(file_text)

		difference_number = abs(text_lines_number - file_lines_number)

		# Define the line text and template
		line_text = self.language_texts["line, title()"]

		tab = "\t\t"

		template = tab + "{} " + line_text + " {}: [{}"

		added_space = False

		# Define the default settings dictionary
		self.default_settings = {
			"Filters": {
				"Deletions mode": False,
				"Full text": False
			},
			"Separators": True
		}

		# Check the settings dictionary
		for key, default in self.default_settings.items():
			if key not in settings:
				settings[key] = default

		i = 0
		line_number = 0
		for line in text_lines_to_write:
			add = False

			# If the "Separators" filter is on
			# And the "i" number is zero
			if (
				settings["Separators"] == True and
				i == 0
			):
				# Add a text to start the changes text
				dictionary["Difference"]["Lines"].append("")
				dictionary["Difference"]["Lines"].append(tab + "-----")
				dictionary["Difference"]["Lines"].append("")
				dictionary["Difference"]["Lines"].append(tab + self.language_texts["changes"].title() + ":")
				dictionary["Difference"]["Lines"].append("")
				dictionary["Difference"]["Lines"].append(tab + "---")

			# If the number of file lines is greater than or equal to number of text lines
			# Or the number of file lines is lesser than the number of text lines
			if (
				len(file_text) >= len(text_lines_to_write) or
				len(file_text) < len(text_lines_to_write)
			):
				# If the number of file lines is greater than or equal to number of text lines
				if len(file_text) >= len(text_lines_to_write):
					# If the "Full text" filter is off
					if settings["Filters"]["Full text"] == False:
						# If the current file line is not the same as the current text line
						# Or the line is not inside the file lines list
						if (
							file_text[i] != text_lines_to_write[i] or
							line not in file_text
						):
							# Add the line to the text difference list
							add = True

					# If the "Full text" filter is on
					# And the current file line is not the same as the current text line
					if (
						settings["Filters"]["Full text"] == True and
						file_text[i] != text_lines_to_write[i]
					):
						# Add the line to the text difference list
						add = True

					# If the line is empty
					if line == "":
						# Add the line to the text difference list
						add = True

				# If the number of file lines is lesser than the number of text lines
				if len(file_text) < len(text_lines_to_write):
					# If the current line is empty
					# Or the "i" number plus one is greater than or equal to the number of file text lines
					if (
						line == "" or
						(i + 1) >= len(file_text)
					):
						# Add the line to the text difference list
						add = True

					# If the "Full text" filter is off
					# And the line is not inside the file lines list
					if (
						settings["Filters"]["Full text"] == False and
						line not in file_text
					):
						# Add the line to the text difference list
						add = True

					# If the "Full text" filter is on
					# And the "i" number plus one is lesser than or equal to the number of file text lines
					if (
						settings["Filters"]["Full text"] == True and
						(i + 1) <= len(file_text)
					):
						# Add the line to the text difference list
						add = True

				# Add the line to the text difference list
				if add == True:
					# Create the number text
					number_text = str(i + 1)

					# If the number of lines to write are lesser than the number of lines inside the file
					if len(text_lines_to_write) < len(file_text):
						# Add one to the number of lines inside the file
						file_lines_number += 1

						# Change the number text to the number of lines inside the file
						number_text = str(file_lines_number)

					# While the length of the number text is lesser than the number of lines to write
					while len(number_text) < len(str(text_lines_number)):
						# Add spaces to the number text
						number_text = " " + number_text

					previous_line = dictionary["Difference"]["Lines"][-1]

					if previous_line == "":
						previous_line = dictionary["Difference"]["Lines"][-2]

					self.testing = False

					if self.testing == True:
						print()
						print("-----")
						print()
						print("[" + str(i - 1))
						print("[" + str(i))
						print("[" + str(i + 1))
						print("[" + str(line_number))
						print("[" + str(int(number_text) - 1))
						print()
						print(" - [" + previous_line)

					# If the "i" number is not in the previous line
					# And the "number_text" number is not in the previous line
					if (
						str(i) not in previous_line and
						str(int(number_text) - 1) not in previous_line
					):
						# Add a space to separate the change lines
						dictionary["Difference"]["Lines"].append("")

					# If the "Deletions mode" filter is on
					# And the "i" number plus one is lesser than or equal to the number of lines inside the file
					if (
						settings["Filters"]["Deletions mode"] == True and
						(i + 1) <= len(file_text)
					):
						# If the "i" number plus one is equal to the number of lines inside the file
						if (i + 1) == len(file_text) and len(text_lines_to_write) >= len(file_text):
							# Remove one from the line number
							line_number -= 1

						file_line = file_text[line_number]

						# Make the old line text with the "-" (minus) symbol
						old_line = template.format("-", number_text, file_line)

						# Add the old line text to the text difference list
						dictionary["Difference"]["Lines"].append(old_line)

						# Add to the deletions number
						dictionary["Deletions"] += 1

					symbol = "+"

					# If the "i" number plus one is lesser than or equal to the number of lines inside the file
					if (i + 1) <= len(file_text):
						# If the "Deletions mode" filter is off
						if settings["Filters"]["Deletions mode"] == False:
							symbol = "~"

						# Add to the changes number
						dictionary["Changes"] += 1

					# Make the new line text with the "+" (plus) symbol
					new_line = template.format(symbol, number_text, line)

					if self.testing == True:
						print(" - [" + new_line)
						input()

					# Add the new line text to the text difference list
					dictionary["Difference"]["Lines"].append(new_line)

					# If the "Deletions mode" filter is on
					# And the "i" number plus one is lesser than or equal to the number of lines inside the file
					# And the previous line is not a space
					if (
						settings["Filters"]["Deletions mode"] == True and
						(i + 1) <= len(file_text) and
						dictionary["Difference"]["Lines"][-1] != ""
					):
						# Add a space to separate the change lines
						dictionary["Difference"]["Lines"].append("")

					# If the "i" number plus one is lesser than or equal to the number of lines inside the file
					# And the number of lines to write is greater than or equal to the number of lines inside the file
					if (
						(i + 1) <= len(file_text) and
						len(text_lines_to_write) >= len(file_text)
					):
						# Add to the additions number
						dictionary["Additions"] += 1

			# If the "Separators" filter is on
			# And the "added_space" is False
			# And the "i" number plus one is lesser than or equal to the number of lines inside the file
			# And the "Additions" number is not zero
			if (
				settings["Separators"] == True and
				added_space == False and
				(i + 1) == len(file_text) and
				dictionary["Additions"] != 0
			):
				# Add a text to separate the lines

				# If the "Deletions mode" filter is off
				if settings["Filters"]["Deletions mode"] == False:
					dictionary["Difference"]["Lines"].append("")

				dictionary["Difference"]["Lines"].append(tab + "-----")
				dictionary["Difference"]["Lines"].append("")
				dictionary["Difference"]["Lines"].append(tab + self.language_texts["additions"].title() + ":")
				dictionary["Difference"]["Lines"].append("")
				dictionary["Difference"]["Lines"].append(tab + "---")

				added_space = True

			i += 1
			line_number += 1

		# Make the number of additions and deletions text
		numbers = []

		# Define the text template
		text_template = ""

		# Add the "changes" number and text if the changes are not zero
		if dictionary["Additions"] != 0:
			numbers.append(dictionary["Additions"])

			# Get the singular or plural text
			text = self.language_texts["addition"]

			if dictionary["Additions"] > 1:
				text = self.language_texts["additions"]

			# Add the " and {} additions" text
			text_template += "[{} " + text + "]"

		# Add the "changes" number and text if the changes are not zero
		if dictionary["Changes"] != 0:
			numbers.append(dictionary["Changes"])

			# Remove the "]" character of the text template
			if text_template != "" and "]" in text_template[-1]:
				text_template = text_template[:-1]

			# Get the singular or plural text
			text = self.language_texts["change"]

			if dictionary["Changes"] > 1:
				text = self.language_texts["changes"]

			# If the additions are not zero
			# Add the " and " text
			if dictionary["Additions"] != 0:
				text_template += " " + self.language_texts["and"] + " "

			# Else, add the "[" text
			# (Difference has only changes)
			else:
				text_template += "["

			# Add the " and {} changes" text
			text_template += "{} " + text

			# Re-add the "]" character
			text_template += "]"

		# Add the "deletions" number and text if the deletions are not zero
		if dictionary["Deletions"] != 0:
			numbers.append(dictionary["Deletions"])

			# Remove the "]" character of the text template
			if text_template != "" and "]" in text_template[-1]:
				text_template = text_template[:-1]

			# If the changes are not zero
			# Replace the " and " text with the ", " (comma and space) text
			if dictionary["Changes"] != 0:
				text_template = text_template.replace(" " + self.language_texts["and"] + " ", ", ")

			# Get the singular or plural text
			text = self.language_texts["deletion"]

			if dictionary["Deletions"] > 1:
				text = self.language_texts["deletions"]

			# If the changes are not zero
			# Add the ", and " text
			if dictionary["Changes"] != 0:
				text_template += ", " + self.language_texts["and"] + " "

			# Else, add the "[" text
			# (Difference has only deletions)
			else:
				text_template += "["

			# Add the " and {} deletions" text
			text_template += "{} " + text

			# Re-add the "]" character
			text_template += "]"

		# Format the text template
		if numbers != []:
			text = "\t\t" + text_template.format(*numbers)

			# Add a space and the template to the lines of text difference
			if dictionary["Difference"]["Lines"] != [] and dictionary["Difference"]["Lines"][-1] != "":
				dictionary["Difference"]["Lines"].append("")

			dictionary["Difference"]["Lines"].append(text)

		# Transform the lines list into a string
		dictionary["Difference"]["Text"] = self.Text_From_List(dictionary["Difference"]["Lines"])

		return dictionary["Difference"]["Text"]

	def Check_Text_Difference(self, file_text, text_lines_to_write, settings = {}, full_verbose = False):
		# Define the maximum number of lines of when to not use the text difference
		# Any changes that exceed this limit activate the full verbose mode
		maximum_lines = 20

		# Define the "make text difference" switch as True by default
		make_text_difference = True

		# If the "full verbose" parameter is True
		if full_verbose == True:
			# Change the "make text difference" switch to False
			make_text_difference = False

		# Define the default verbose text for the non-verbose mode
		verbose_text = self.language_texts["text, title()"] + ":\n[" + \
		text_lines_to_write + \
		"]"

		# If the verbose mode is activated
		# And the "make text difference" switch is True
		# And the number of lines of the text file is greater than the maximum number of lines to show
		# And the file is not empty
		# Show only the text difference, not the full text to write
		if (
			self.switches["Verbose"] == True and
			make_text_difference == True and
			len(file_text["Lines"]) > maximum_lines and
			file_text["Lines"] != []
		):
			# Make the text difference between the text inside the file and the text to be written
			text_difference = self.Text_Difference(file_text, text_lines_to_write, settings)

			# Update the verbose text to add the text difference
			verbose_text = self.language_texts["text_difference"] + ":\n" + \
			"\t[\n" + \
			text_difference + \
			"\n\t]"

		# Return the verbose text
		return verbose_text
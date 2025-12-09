# Christmas.py

# Import some useful modules
import importlib

class Christmas():
	def __init__(self):
		# Import some utility classes
		self.Import_Utility_Classes()

		# Define the folders of the module
		self.folders = self.Define_Folders(object = self).folders

		# Define basic variables for the class
		self.Define_Basic_Variables()

		# Define the text dictionaries of the class
		self.Define_Texts()

		# Import some usage classes
		self.Import_Usage_Classes()

		# Define the dictionaries of the class
		self.Define_Dictionaries()

	def Import_Utility_Classes(self):
		# Define the classes to be imported
		classes = [
			"Define_Folders",
			"JSON"
		]

		# Iterate through the list of classes
		for class_title in classes:
			# If the class is not already inside this class (Christmas)
			# Or the class is "Define_Folders"
			if (
				hasattr(self, class_title) == False or
				class_title == "Define_Folders"
			):
				# Import the module
				module = importlib.import_module("." + class_title, "Utility")

				# Get the sub-class
				sub_class = getattr(module, class_title)

				# If the module title is not "Define_Folders"
				if class_title != "Define_Folders":
					# Run the sub-class to define its variable
					sub_class = sub_class()

				# Add the sub-class to the current class
				setattr(self, class_title, sub_class)

		# ---------- #

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
			# And the class is not already inside this class ("Christmas")
			if (
				module_title not in remove_list and
				hasattr(self, module_title) == False
			):
				# Import the module
				module = importlib.import_module("." + module_title, "Utility")

				# Get the sub-class of the module
				sub_class = getattr(module, module_title)

				# Add the sub-class to the current class
				setattr(self, module_title, sub_class())

		# ---------- #

		# Get the switches dictionary from the "Global Switches" class
		self.switches = self.Global_Switches.switches["Global"]

		# ---------- #

		# Import some variables from the "Language" class

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

		# Import the "Sanitize" method from the "File" class
		self.Sanitize = self.File.Sanitize

		# ---------- #

		# Get the current date from the "Date" class
		self.date = self.Date.date

	def Define_Texts(self):
		# Define the "separators" dictionary
		self.separators = {}

		# Create separators from one to ten characters
		for number in range(1, 11):
			# Define the empty string
			string = ""

			# Add separators to it
			while len(string) != number:
				string += "-"

			# Add the string to the separators dictionary
			self.separators[str(number)] = string

		# Define the "Texts" dictionary
		self.texts = self.JSON.To_Python(self.module["Files"]["Texts"])

		# Define the "Language texts" dictionary
		self.language_texts = self.Language.Item(self.texts)

	def Import_Usage_Classes(self):
		# Define a local dictionary of classes
		classes = {
			"List": [
				"Years",
				"Social_Networks"
			],
			"Dictionary": {
				"Social_Networks": {
					"Sub-classes to import": {
						"List": [
							"Open_Social_Network"
						]
					}
				}
			},
			"Do not run": []
		}

		# Iterate through the list of classes
		for class_title in classes["List"]:
			# Define the class dictionary
			class_dictionary = {
				"Title": class_title,
				"Module": "",
				"Object": ""
			}

			# If the class title is inside the dictionary of classes
			if class_title in classes["Dictionary"]:
				# Get the "Sub-classes to import" dictionary from it
				class_dictionary["Sub-classes to import"] = classes["Dictionary"][class_title]["Sub-classes to import"]

			# Import the module
			class_dictionary["Module"] = importlib.import_module("." + class_title, class_title)

			# Get the class object
			class_dictionary["Object"] = getattr(class_dictionary["Module"], class_title)

			# If the class title is not inside the list of classes to not run
			if class_title not in classes["Do not run"]:
				# Run the class to define its variables
				class_dictionary["Object"] = class_dictionary["Object"]()

			# If the "Sub-classes to import" key is present
			if "Sub-classes to import" in class_dictionary:
				# Create the "Sub-classes" dictionary
				class_dictionary["Sub-classes"] = {}

				# Create a shortcut to the sub-classes dictionary
				sub_classes = class_dictionary["Sub-classes to import"]

				# Define a sub-class number
				sub_class_number = 0

				# Iterate through the list of sub-classes
				for sub_class_title in sub_classes["List"]:
					# Create the sub-class dictionary
					sub_class_dictionary = {
						"Title": sub_class_title,
						"Module": "",
						"Object": ""
					}

					# Import the sub-module
					sub_class_dictionary["Module"] = importlib.import_module("." + sub_class_title, class_title)

					# Get the sub-class
					sub_class_dictionary["Object"] = getattr(sub_class_dictionary["Module"], sub_class_title)

					# If the "Titles" list is present
					if "Titles" in sub_classes:
						# Change the sub-class title to the one in the list of sub-class titles
						sub_class_title = sub_classes["Titles"][sub_class_number]

					# Add the sub-class dictionary to the root sub-classes dictionary
					class_dictionary["Sub-classes"][sub_class_title] = sub_class_dictionary

					# Add the sub-class to the root class
					setattr(class_dictionary["Object"], sub_class_title, sub_class_dictionary["Object"])

					# Add one to the sub-class number
					sub_class_number += 1

				# Remove the "Sub-classes to import" dictionary
				class_dictionary.pop("Sub-classes to import")

			# Add the class dictionary to the root classes dictionary
			classes["Dictionary"][class_title] = class_dictionary

			# Add the class to the current class
			setattr(self, class_title, class_dictionary["Object"])

		# Sort the dictionary of classes with the order of the list of classes
		classes["Dictionary"] = self.JSON.Sort_Item_List(classes["Dictionary"], order = classes["List"])

		# ---------- #

		# Get the "Current year" dictionary from the "Years" class
		self.current_year = self.Years.years["Current year"]

	def Define_Dictionaries(self):
		# Define the root "Christmas" dictionary
		self.christmas = {}

		# ---------- #

		# Define the date string as 25 of December of the current year
		date_string = "25/12/" + str(self.date["Units"]["Year"])

		# Define the Christmas "Date" dictionary
		self.christmas["Date"] = self.Date.From_String(date_string, format = "%d/%m/%Y")

		# Define the "States" dictionary
		self.christmas["States"] = {
			"Today is Christmas": False
		}

		# Check if today is Christmas to update the "States" dictionary
		self.Today_Is_Christmas()

		# ---------- #

		# Define the "Folders" dictionary
		self.christmas["Folders"] = {
			"Year": {},
			"Texts": self.Years.years["Texts"]["Folders"]["Christmas"]
		}

		# Create a shortcut to the Christmas image folder
		christmas_folder = self.current_year["Folders"]["Image"]["Christmas"]

		# Iterate through the defined list of folder keys
		for key in ["Screenshots", "Pictures"]:
			# Get the folder
			folder = christmas_folder[key]["root"]

			# Add it to the "Year" folders dictionary
			self.christmas["Folders"]["Year"][key] = {
				"root": folder
			}

		# ---------- #

		# Define the "Files" dictionary
		self.christmas["Files"] = {
			"Merry Christmas": {
				"Texts": "",
				"Social networks": {}
			},
			"Planning": "",
			"Objects": ""
		}

		# ----- #

		# Define the merry Christmas "Texts" key as the Christmas texts file
		self.christmas["Files"]["Merry Christmas"]["Texts"] = self.current_year["Folders"]["Christmas"]["Merry Christmas"]["Texts"]

		# ----- #

		# Define the root "social networks" dictionary
		self.social_networks = {
			"Numbers": {
				"Total": 0,
				"Iteration": 1
			},
			"List": [],
			"Custom links": {
				"Twitter": "https://twitter.com/compose/tweet/unsent/scheduled",
				"Wattpad": self.Social_Networks.social_networks["Dictionary"]["Wattpad"]["Profile"]["Links"]["Conversations"]
			},
			"States": {
				"First separator": False
			},
			"Spaces": {
				"First": False
			},
			"Input text": ""
		}

		# Define a local list of social networks
		social_networks = [
			"Discord",
			"Instagram {} Facebook",
			"Twitter",
			"Bluesky {} Threads",
			"Wattpad",
			"WhatsApp"
		]

		# Iterate through the local list of social networks
		for key in social_networks:
			# If the "{}" format string is present inside the key
			if "{}" in key:
				# Format the key with the "and" text
				key = key.format("and")

			# Get the Christmas texts file for the social network from the texts "Merry Christmas" dictionary
			texts_file = self.christmas["Folders"]["Texts"]["Merry Christmas"]["Social networks"][key]

			# Define the texts file inside the merry Christmas "Social networks" dictionary
			self.christmas["Files"]["Merry Christmas"]["Social networks"][key] = texts_file

		# ----- #

		# Iterate through the list of defined keys
		for key in ["Planning", "Objects"]:
			# Get the text file for the key from the texts "Planning" dictionary
			text_file = self.christmas["Folders"]["Texts"]["Planning"]

			# If the key is "Planning"
			if key == "Planning":
				# Get the text file in the user language
				text_file = text_file[self.language["Small"]]

			# Else, use the key
			else:
				text_file = text_file[key]

			# Define the text file inside the "Files" dictionary
			self.christmas["Files"][key] = text_file

		# ---------- #

		# Define the "Theme" key as the "Christmas.lnk" key which links to the theme file
		self.christmas["Theme"] = self.folders["Image"]["Christmas"]["Theme"]["Christmas.lnk"]

		# ---------- #

		# Define the "Music players" dictionary
		self.christmas["Music players"] = {
			"Foobar2000": {
				"Name": "Foobar2000",
				"Link": self.folders["Program Files (x86)"]["Foobar2000"]["Foobar2000"]
			}
		}

		# Define a "Music player" dictionary by choosing one of the music players inside the "Music players" dictionary
		dictionary = self.christmas["Music players"]

		self.christmas["Music player"] = dictionary["Foobar2000"]

		# ---------- #

		# Define the "Methods" dictionary
		self.christmas["Methods"] = {
			"List": [
				"Open_Christmas_Theme",
				"Open_Folder",
				"Open_Music_Player",
				"Open_Social_Networks",
				"Create_Discord_Status",
				"Open_File",
				"Open_Module"
			],
			"Dictionary": {},
			"Do not ask for input": [
				"Open_Module",
				"Open_Social_Networks"
			]
		}

		# Iterate through the list of method titles
		for method_title in self.christmas["Methods"]["List"]:
			# Get the method
			method = getattr(self, method_title)

			# Add it to the methods "Dictionary"
			self.christmas["Methods"]["Dictionary"][method_title] = method

	def Today_Is_Christmas(self, date_parameter = None):
		# Define the date as the date parameter
		date = date_parameter

		# If the date parameter is None
		if date_parameter == None:
			# Define the local date as the root one
			date = self.date

		# Define the local "today is Christmas" state as False
		today_is_christmas = False

		# If today is 24 or 25 of December
		# The day 24 is also fine to start Christmas (probably close to midnight of day 25)
		if (
			date["Units"]["Day"] in [24, 25] and # Day is either 24 or 25
			date["Units"]["Month"] == self.christmas["Date"]["Units"]["Month"] # Month is 12
		):
			# Change the local "today is Christmas" state to True
			today_is_christmas = True

		# If the date parameter is None
		if date_parameter == None:
			# Change the root "Today is Christmas" state to the local one
			self.christmas["States"]["Today is Christmas"] = today_is_christmas

		# Return the local state
		return today_is_christmas

	def Open_Christmas_Theme(self):
		# Create a shortcut to the text about defining the Christmas theme for the computer
		text = self.language_texts["using_the_christmas_theme_for_the_computer"]

		# Show the text
		print(text + "...")

		# Open the Christmas theme to use it on the computer
		self.System.Open(self.christmas["Theme"])

	def Open_Folder(self, folder_name):
		# Get the text key for the folder name
		text_key = folder_name.lower() + ", title()"

		# Get the text for the folder
		folder_text = self.Language.language_texts[text_key].lower()

		# Create a shortcut to the text template about opening the folder for the current year
		text_template = self.language_texts["opening_the_{}_folder_for_the_current_year"]

		# Format the text template with the folder text
		text = text_template.format(folder_text)

		# Show the text
		print(text + "...")

		# Get the folder
		folder = self.christmas["Folders"]["Year"][folder_name]["root"]

		# Open it
		self.System.Open(folder)

	def Open_Music_Player(self):
		# Create a shortcut to the text template about opening the music player for the user to listen to the playlist of Christmas songs
		text_template = self.language_texts["opening_the_{}_music_player_for_you_to_listen_to_the_playlist_of_christmas_songs"]

		# Format the text template with the name of the music player
		text = text_template.format(self.christmas["Music player"]["Name"])

		# Show the text
		print(text + "...")

		# Open the music player program so the user can listen to the soundtrack of the story
		self.System.Open(self.christmas["Music player"]["Link"], verbose = False)

		# If the "Testing" switch is False
		if self.switches["Testing"] == False:
			# Wait for one second
			self.Date.Sleep(1)

	def Open_Social_Networks(self, social_networks):
		# Define a local "skip" switch initially as False
		skip = False

		# If the "social networks" parameter is "Twitter"
		if social_networks == "Twitter":
			# Define the list of social networks as only Twitter
			self.social_networks["List"] = [
				"Twitter"
			]

			# Define the input text to be about when the user finishes scheduling the tweets
			self.social_networks["Input text"] = self.language_texts["press_enter_when_you_finish_scheduling_the_tweets_of_the, type: long"]

		# If the "social networks" parameter not "Twitter"
		if social_networks != "Twitter":
			# Reset the list of social networks to be empty
			self.social_networks["List"] = []

			# If the social networks parameter is a string
			if type(social_networks) == str:
				# Add it to the list of social networks
				self.social_networks["List"].append(social_networks)

			# If the social networks parameter is a list
			if type(social_networks) == list:
				# Extend the list of social networks with it
				self.social_networks["List"].extend(social_networks)

			# Update the number of social networks
			self.social_networks["Numbers"]["Total"] = len(self.social_networks["List"])

		# Create a local copy of the list of social networks
		social_networks_copy = self.social_networks["List"].copy()

		# Iterate through the local list of social networks
		for social_network_number, social_network in enumerate(social_networks_copy, start = 1):
			# Update the "Iteration" number
			self.social_networks["Numbers"]["Iteration"] = social_network_number

			# Update the list of social networks to be the local current social network
			self.social_networks["List"] = [
				social_network
			]

			# If the "social networks" parameter is not "Twitter"
			if social_networks != "Twitter":
				# Create a shortcut to the text template to ask the user to press Enter when they finish posting the "Merry Christmas" text on the social network
				text_template = self.language_texts["press_enter_when_you_finish_posting_the_merry_christmas, type: long"]

				# Format the text template with the social network name
				text = text_template.format(social_network)

				# Update the input text
				self.social_networks["Input text"] = text

				# If the "social networks" parameter is not "Wattpad"
				if social_networks != "Wattpad":
					# Change the "First separator" state to True
					self.social_networks["States"]["First separator"] = True

			# If the "social networks" parameter is "Wattpad"
			if social_networks == "Wattpad":
				# Show the first space
				self.social_networks["Spaces"]["First"] = True

			# Open the social network using the "Open_Social_Network" sub-class of the "Social_Networks" class
			self.Social_Networks.Open_Social_Network(self.social_networks)

	def Create_Discord_Status(self):
		# Define the status as the "Merry Christmas" in the user language plus the current year, and the Christmas tree and present emojis
		status = self.Language.language_texts["merry_christmas"] + "! {} 🎄🎁".format(self.current_year["Number"])

		# Copy the status to the user clipboard
		self.Text.Copy(status, first_space = False)

	def Open_File(self, file_name):
		# Define a local list of file names as the file name parameter
		file_names = file_name

		# If the file name is a string
		if type(file_name) == str:
			# Define the list of file names as a list with the only file name
			file_names = [
				file_name
			]

		# Iterate through the list of file names
		for file_name in file_names:
			# If the file name is "Texts"
			if file_name == "Texts":
				# Define the file as the merry Christmas "Texts" file
				file = self.christmas["Files"]["Merry Christmas"]["Texts"]

			# Else, get the file from the merry Christmas "Social networks" dictionary
			else:
				file = self.christmas["Files"]["Merry Christmas"]["Social networks"][file_name]

			# Define the first space initially as off
			first_space = False

			# If the file name is not the first one
			if file_name != file_names[0]:
				# Change the first space to on
				first_space = True

			# Open the file
			self.System.Open(file, first_space = first_space)

	def Open_Module(self, module_title):
		# Get the list of files from the apps "Shortcuts" folder
		files = self.Folder.Contents(self.folders["Apps"]["Shortcuts"]["White"]["root"])["file"]["list"]

		# Iterate through the list of files
		for file in files:
			# Try to find the "Apps.lnk" shortcut inside the file
			if "Apps.lnk" in file:
				# If found, define the "apps" variable as the current file
				apps = file

		# Open the "Apps.lnk" shortcut
		self.System.Open(apps, verbose = False)

		# Create a shortcut to the "Planning" folder of the "Christmas" folder of the current year
		planning_folder = self.current_year["Folders"]["Christmas"]["Planning"]

		# Iterate through the list of item types
		for item_type in ["Watch", "Eat"]:
			# Define the text key for the file
			text_key = item_type.lower() + ", title()"

			# Get the text for the file in the user language
			text = self.Language.language_texts[text_key]

			# Show the text in the user language
			print(text + ":")

			# Get the text_file
			text_file = planning_folder[item_type]

			# Open the text file
			self.System.Open(text_file, verbose = False)

			# Get the lines of the text files
			lines = self.File.Contents(text_file)["Lines"]

			# Define the tab as one tab
			tab = "\t"

			# If the lines of the file is an empty list
			if lines == []:
				# Show the "[Nothing]" text with the tab
				print(tab + "[" + self.Language.language_texts["nothing, title()"] + "]")

			# Iterate through the list of lines
			i = 1
			for line in lines:
				# Show the tab, the line number, and the line
				print(tab + str(i) + ". " + line)

				# Add one to the "i" number
				i += 1

			# If the item type is not "Eat"
			if item_type != "Eat":
				# Show a space separator at the end
				print()

		# Define the input text to be about when the user finishes watching all of the Christmas episodes
		input_text = self.language_texts["press_enter_when_you_finish_watching_all_of_the_christmas_episodes"]

		# Use it to ask the user to press Enter when they finish watching
		self.Input.Type(input_text)
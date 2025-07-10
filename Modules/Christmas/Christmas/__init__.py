# Christmas.py

# Import the "importlib" module
import importlib

import Utility

class Christmas():
	def __init__(self):
		# Import the classes
		self.Import_Classes()

		# Define the folders of the module
		self.folders = Utility.Define_Folders(object = self).folders

		# Module related methods
		self.Define_Basic_Variables()
		self.Define_Texts()

		# Import some usage classes
		self.Import_Usage_Classes()

		# Folders, lists, and dictionaries methods
		self.Define_Folders()
		self.Define_Lists_And_Dictionaries()

		# Class methods
		self.Today_Is_Christmas()

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
				# Add the sub-class to the current module
				setattr(self, module_title, sub_class())

			# If the module title is "Define_Folders"
			if module_title == "Define_Folders":
				# Add the sub-class to the "Utility" module
				setattr(Utility, "Define_Folders", sub_class)

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

			# Add the string to the Separators dictionary
			self.separators[str(number)] = string

		# Define the "Texts" dictionary
		self.texts = self.JSON.To_Python(self.module["Files"]["Texts"])

		# Define the "Language texts" dictionary
		self.language_texts = self.Language.Item(self.texts)

	def Import_Usage_Classes(self):
		# Define the classes to be imported
		classes = [
			"Social_Networks",
			"Social_Networks.Open_Social_Network",
			"Years"
		]

		do_not_run = [
			"Open_Social_Network"
		]

		# Import them
		for title in classes:
			module_title = title

			if "." in module_title:
				module_title = module_title.split(".")[0]

				title = title.split(".")[1]

			# Import the module
			module = importlib.import_module("." + title, module_title)

			# Get the sub-class
			sub_class = getattr(module, title)

			if title not in do_not_run:
				sub_class = sub_class()

			# Add the sub-class to the current module
			setattr(self, title, sub_class)

	def Define_Folders(self):
		self.current_year = self.Years.years["Current year"]

		self.year_texts = self.Years.years["Texts"]

	def Define_Lists_And_Dictionaries(self):
		# Define the root "Social Networks" dictionary
		self.social_networks = {
			"Numbers": {
				"Total": 0,
				"Iteration": 1
			},
			"List": [],
			"Custom links": {
				"Twitter": "https://twitter.com/compose/tweet/unsent/scheduled"
			},
			"States": {
				"First separator": False
			}
		}

		# Define the root "Christmas" dictionary
		self.christmas = {
			"States": {
				"Today is Christmas": False
			},
			"Date": self.Date.From_String("25/12/" + str(self.date["Units"]["Year"])),
			"Folders": {
				"Year screenshots": self.current_year["Folders"]["Image"]["Christmas"]["Screenshots"]["root"],
				"Year pictures": self.current_year["Folders"]["Image"]["Christmas"]["Pictures"]["root"],
			},
			"Files": {
				"Christmas theme": self.folders["Image"]["Christmas"]["Theme"]["root"] + self.Language.language_texts["christmas, title()"] + ".lnk",
				"Texts": self.current_year["Folders"]["Christmas"]["Merry Christmas"]["Texts"]
			},
			"Programs": {
				"Foobar2000": self.folders["Program Files (x86)"]["Foobar2000"]["Foobar2000"]
			},
			"Social Network links": {
				"YouTube": "https://www.youtube.com/@Stake2_/",
				"DeviantArt": "https://www.deviantart.com/stake2"
			}
		}

		# Define a local list of Social Networks
		social_networks = [
			"Discord",
			"Instagram {} Facebook".format(self.Language.language_texts["and"]),
			"Twitter",
			"Bluesky {} Threads".format(self.Language.language_texts["and"]),
			"Wattpad",
			"WhatsApp"
		]

		# Iterate through the local Social Networks list
		for key in social_networks:
			# Define the file of the Social Network inside the "Files" dictionary of the "Christmas" dictionary
			self.christmas["Files"][key] = self.year_texts["Folders"]["Christmas"]["Merry Christmas"]["Social Networks"][key]

		self.christmas["Functions"] = {
			"Open_Folder": {
				"Values": self.christmas["Folders"]
			},
			"Open_File": {
				"Values": self.christmas["Files"]
			},
			"Open_Program": {
				"Values": self.christmas["Programs"]
			},
			"Open_Module": {
				"Function": self.Open_Module,
				"Ask for input": False
			},
			"Open_Social_Network": {
				"Function": self.Open_Social_Networks,
				"Ask for input": False
			},
			"Discord_Status": {
				"Function": self.Discord_Status
			}
		}

	def Today_Is_Christmas(self):
		if (
			self.date["Units"]["Day"] == self.christmas["Date"]["Units"]["Day"] and
			self.date["Units"]["Month"] == self.christmas["Date"]["Units"]["Month"]
		):
			self.christmas["States"]["Today is Christmas"] = True

		return self.christmas["States"]["Today is Christmas"]

	def Open(self, item):
		# If the item is a string (folder, file, or program)
		if type(item) == str:
			self.System.Open(item, verbose = False)

		# If the item is a dictionary (list of folders, files, or programs)
		if type(item) == dict:
			key = item["Key"]
			items = item["List"]

			for item in items:
				if key == "Instagram, Facebook":
					key = "Instagram {} Facebook".format(self.Language.language_texts["and"])

				item = self.christmas[key][item]

				self.System.Open(item, verbose = False)

	def Open_Module(self, module):
		self.press_enter_text = self.Language.language_texts["press_enter_when_you"] + " {}"

		texts = {
			"Watch_History": self.language_texts["press_enter_when_you_finish_watching_all_of_the_christmas_episodes"],
			"GamePlayer": self.language_texts["press_enter_when_you_finish_spending_time_with_monika_on_the_game"] + ' "Monika After Story"',
		}

		if module != "GamePlayer":
			files = self.Folder.Contents(self.folders["Apps"]["Shortcuts"]["White"]["root"])["file"]["list"]

			for file in files:
				if "Apps.lnk" in file:
					apps = file

			self.System.Open(apps, verbose = False)

		if module == "Watch_History":
			text_files = {
				"Watch": self.current_year["Folders"]["Christmas"]["Planning"]["Watch"],
				"Eat": self.current_year["Folders"]["Christmas"]["Planning"]["Eat"]
			}

			for key in text_files:
				# Get the file
				file = text_files[key]

				# Open it
				self.System.Open(file, verbose = False)

				# Get the file lines
				lines = self.File.Contents(file)["lines"]

				# Define the file information text
				text = self.Language.language_texts[key.lower() + ", title()"].lower()

				print()
				print(self.Language.language_texts["to, title()"] + " " + text + ":")

				tab = "\t"

				if lines == []:
					print(tab + "[" + self.Language.language_texts["nothing, title()"] + "]")

				i = 1
				for line in lines:
					print(tab + str(i) + ". " + line)

					i += 1

		self.Input.Type(texts[module])

	def Open_Social_Networks(self, parameter):
		# If the parameter is "Twitter"
		if parameter == "Twitter":
			# Define the list of social networks as only the Twitter one
			self.social_networks["List"] = [
				"Twitter"
			]

		# Define the default skip value as False
		skip = False

		# If the parameter is "All"
		if parameter == "All":
			# Define the input text
			input_text = self.language_texts["do_you_want_to_skip_changing_the_profile_pictures"]

			# Ask if the user wants to skip the changing the profile pictures
			skip = self.Input.Yes_Or_No(input_text)

			# Make a copy of the root list of social networks and sort it with the ascending lowercase key
			self.social_networks["List"] = sorted(self.Social_Networks.social_networks["List"], key = str.lower)

			# Make a list of social networks to remove
			to_remove = [
				"Derpibooru",
				"Habitica",
				#"Steam"
			]

			# Remove them
			for item in to_remove:
				self.social_networks["List"].remove(item)

			# Update the number of social networks
			self.social_networks["Numbers"]["Total"] = len(self.social_networks["List"])

			# If the skip variable is False
			if skip == False:
				# Show a space
				print()

		# If the parameter is "Twitter"
		# Or the parameter is "All"
		# And the skip variable is False
		if (
			parameter == "Twitter" or
			parameter == "All" and
			skip == False
		):
			# Define the "i" variable and run the for each loop
			i = 1
			for social_network in self.social_networks["List"].copy():
				# If the parameter is "All"
				if parameter == "All":
					# Get the total number of social networks
					# And store it in a short variable for easier typing
					total_number = self.social_networks["Numbers"]["Total"]

					# Make the number text
					text = str(i) + "/" + str(total_number)

					# If the social network is not the first one
					if social_network != self.social_networks["List"][0]:
						# Show a three dash space separator
						print(self.separators["3"])
						print()

					# Show the "Social Networks" and the "[Current number]/[Total number]" texts
					print(self.Language.language_texts["social_networks"] + ":")
					print("\t" + text)
					print()

					# Show the "Social Network" text and the Social Network name
					print(self.Language.language_texts["social_network"] + ":")
					print("\t" + social_network)

				# Update the list of social networks to be the local current social network
				self.social_networks["List"] = [
					social_network
				]

				# Open the social network
				self.Open_Social_Network(self.social_networks)

				# Define the input text to be about the scheduled tweets about the screenshot and picture of the computer
				text = self.language_texts["press_enter_when_you_finish_scheduling_the_tweets_of_the_screenshot_and_picture_of_the_decorated_computer"]

				# If the parameter is "All"
				if parameter == "All":
					# Define the input text to be about changing the profile picture of the local current social network
					text = self.language_texts["press_enter_when_you_finish_changing_the_profile_picture_of"] + ' "' + social_network + '"'

				# Ask for user input before continuing
				self.Input.Type(text)

				# If the parameter is "All"
				if parameter == "All":
					# Show a space separator
					print()

					# Add one to the "i" variable
					i += 1

	def Discord_Status(self):
		# Define the status
		status = self.Language.language_texts["merry_christmas"] + "! {} 🎄🎁".format(self.current_year["Number"])

		# Copy the status
		self.Text.Copy(status)
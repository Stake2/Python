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

		# Import the usage classes
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
		# Define the "Language" class as the same class inside the "JSON" class
		self.Language = self.JSON.Language

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
			"Instagram, Facebook",
			"Twitter",
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
				item = self.christmas[key][item]

				self.System.Open(item, verbose = False)

	def Open_Social_Networks(self, parameter):
		if parameter == "Twitter":
			self.social_networks["List"] = [
				"Twitter"
			]

		if parameter == "All":
			self.social_networks["List"] = sorted(self.Social_Networks.social_networks["List"], key = str.lower)
			self.social_networks["List"].remove("Twitter")
			self.social_networks["List"].remove("Habitica")

			self.social_networks["Numbers"]["Total"] = len(self.social_networks["List"]) + 2

			print()

		i = 1
		for social_network in self.social_networks["List"]:
			if parameter == "All":
				# Get the total numbers
				# And store it in a short variable for easier typing
				total_number = self.social_networks["Numbers"]["Total"]

				# Make the number text
				text = str(i) + "/" + str(total_number)

				if social_network != self.social_networks["List"][0]:
					print("---")
					print()

				# Show the "Social Networks" and the "[Current number]/[Total number]" texts
				print(self.Language.language_texts["social_networks"] + ":")
				print("\t" + text)
				print()

				# Show the "Social Network" text and the Social Network name
				print(self.Language.language_texts["social_network"] + ":")
				print("\t" + social_network)

			self.social_networks["List"] = [
				social_network
			]

			self.Open_Social_Network(self.social_networks)

			text = self.language_texts["press_enter_when_you_finish_adding_the_screenshots_to_the_scheduled_tweet"]

			if parameter == "All":
				text = self.language_texts["press_enter_when_you_finish_changing_the_profile_picture_of"] + ' "' + social_network + '"'

			self.Input.Type(text)

			if parameter == "All":
				print()

				i += 1

		if parameter == "All":
			social_networks = [
				"YouTube",
				"DeviantArt"
			]

			print("---")
			print()

			for social_network in social_networks:
				link = self.christmas["Social Network links"][social_network]

				# Get the total numbers
				# And store it in a short variable for easier typing
				total_number = self.social_networks["Numbers"]["Total"]

				# Make the number text
				text = str(i) + "/" + str(total_number)

				if social_network != social_networks[0]:
					print("---")
					print()

				# Show the "Social Networks" and the "[Current number]/[Total number]" texts
				print(self.Language.language_texts["social_networks"] + ":")
				print("\t" + text)
				print()

				# Show the "Social Network" text and the Social Network name
				print(self.Language.language_texts["social_network"] + ":")
				print("\t" + social_network)

				# Define the text template
				template = self.Social_Networks.language_texts["opening_the_social_network_{}_on_its_{}_page_with_this_link"]

				# Define the text template items
				items = [
					social_network,
					self.Language.language_texts["profile, title()"]
				]

				# Format the text template with the items
				text = template.format(*items)

				print()
				print(text + ":")
				print("\t" + link)

				if self.switches["Testing"] == False:
					self.System.Open(link)

				text = self.language_texts["press_enter_when_you_finish_changing_the_profile_picture_of"] + ' "' + social_network + '"'

				self.Input.Type(text)

				if social_network != social_networks[-1]:
					print()

				i += 1

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
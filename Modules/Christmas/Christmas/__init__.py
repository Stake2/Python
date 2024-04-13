# Christmas.py

# Import the "importlib" module
import importlib

class Christmas():
	def __init__(self):
		# Define the module folders
		from Utility.Define_Folders import Define_Folders as Define_Folders

		Define_Folders(self)

		# Module related methods
		self.Define_Basic_Variables()
		self.Define_Texts()

		# Import classes method
		self.Import_Classes()

		# Folders, lists, and dictionaries methods
		self.Define_Folders()
		self.Define_Lists_And_Dictionaries()

		# Class methods
		self.Today_Is_Christmas()

	def Define_Basic_Variables(self):
		from copy import deepcopy

		# Import the JSON module
		from Utility.JSON import JSON as JSON

		self.JSON = JSON()

		# Define the "Language" class as the same class inside the "JSON" class
		self.Language = self.JSON.Language

		# Get the modules list
		self.modules = self.JSON.To_Python(self.folders["apps"]["modules"]["modules"])

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

				# Add the sub-class to the current module
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
		self.large_bar = "-----"
		self.dash_space = "-"

		self.texts = self.JSON.To_Python(self.folders["apps"]["module_files"][self.module["key"]]["texts"])

		self.language_texts = self.JSON.Language.Item(self.texts)

	def Import_Classes(self):
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
				"Christmas theme": self.folders["Image"]["Christmas"]["Theme"]["root"] + self.JSON.Language.language_texts["christmas, title()"] + ".lnk",
				"Texts": self.current_year["Folders"]["Christmas"]["Merry Christmas"]["Texts"]
			},
			"Programs": {
				"Foobar2000": self.folders["Program Files (x86)"]["Foobar2000"]["root"] + "foobar2000.exe"
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
				print(self.JSON.Language.language_texts["social_networks"] + ":")
				print("\t" + text)
				print()

				# Show the "Social Network" text and the Social Network name
				print(self.JSON.Language.language_texts["social_network"] + ":")
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
				print(self.JSON.Language.language_texts["social_networks"] + ":")
				print("\t" + text)
				print()

				# Show the "Social Network" text and the Social Network name
				print(self.JSON.Language.language_texts["social_network"] + ":")
				print("\t" + social_network)

				# Define the text template
				template = self.Social_Networks.language_texts["opening_the_social_network_{}_on_its_{}_page_with_this_link"]

				# Define the text template items
				items = [
					social_network,
					self.JSON.Language.language_texts["profile, title()"]
				]

				# Format the text template with the items
				text = template.format(*items)

				print()
				print(text + ":")
				print("\t" + link)

				if self.switches["testing"] == False:
					self.System.Open(link)

				text = self.language_texts["press_enter_when_you_finish_changing_the_profile_picture_of"] + ' "' + social_network + '"'

				self.Input.Type(text)

				if social_network != social_networks[-1]:
					print()

				i += 1

	def Open_Module(self, module):
		self.press_enter_text = self.JSON.Language.language_texts["press_enter_when_you"] + " {}"

		texts = {
			"Watch_History": self.language_texts["press_enter_when_you_finish_watching_all_of_the_christmas_episodes"],
			"GamePlayer": self.language_texts["press_enter_when_you_finish_spending_time_with_monika_on_the_game"] + ' "Monika After Story"',
		}

		if module != "GamePlayer":
			files = self.Folder.Contents(self.folders["Apps"]["Shortcuts"]["White"])["file"]["list"]

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
				text = self.JSON.Language.language_texts[key.lower() + ", title()"].lower()

				print()
				print(self.JSON.Language.language_texts["to, title()"] + " " + text + ":")

				tab = "\t"

				if lines == []:
					print(tab + "[" + self.JSON.Language.language_texts["nothing, title()"] + "]")

				i = 1
				for line in lines:
					print(tab + str(i) + ". " + line)

					i += 1

		self.Input.Type(texts[module])
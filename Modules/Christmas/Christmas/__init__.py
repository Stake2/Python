# Christmas.py

# Import some useful modules
import importlib
from copy import deepcopy

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

		# Define the Christmas "Texts" dictionary
		self.Define_Christmas_Texts()

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

		# Sort the dictionary of classes with the order being the list of classes
		classes["Dictionary"] = self.JSON.Sort_Item_List(classes["Dictionary"], order = classes["List"])

		# ---------- #

		# Get the "Current year" dictionary from the "Years" class
		self.current_year = self.Years.years["Current year"]

	def Define_Dictionaries(self):
		# Define the root "Christmas" dictionary
		self.christmas = {
			"Dates": {}
		}

		# ---------- #

		# Define a local list of days
		days = [
			"24",
			"25"
		]

		# Iterate through the list of days
		for day in days:
			# Define the date string as [Day] of December of the [Current year]
			date_string = day + "/12/" + str(self.date["Units"]["Year"])

			# Define the date key as "[Day] of December"
			date_key = day + " of December"

			# Define the "[Day] of December" date dictionary using the defined date string
			self.christmas["Dates"][date_key] = self.Date.From_String(date_string, format = "%d/%m/%Y")

		# Define the "States" dictionary
		self.christmas["States"] = {
			"Today is Christmas": False
		}

		# Check if today is Christmas to update the "Today is Christmas" state
		self.christmas["States"]["Today is Christmas"] = self.Today_Is_Day()

		# ---------- #

		# Define the "Folders" dictionary
		self.christmas["Folders"] = {
			"Year": {},
			"Texts": self.Years.years["Texts"]["Folders"]["Christmas"]
		}

		# Create a shortcut to the Christmas image folder
		christmas_folder = self.current_year["Folders"]["Image"]["Christmas"]

		# Iterate through the defined list of folder keys
		for key in ["root", "Screenshots", "Pictures"]:
			# Add the folder to the Christmas "Year" folders dictionary
			self.christmas["Folders"]["Year"][key] = christmas_folder[key]

		# ---------- #

		# Define a shortcut to the root year texts "Christmas" dictionary
		year_texts = self.Years.years["Texts"]["Files"]["Christmas"]

		# Define the "Files" dictionary
		self.christmas["Files"] = {
			"Merry Christmas": {}
		}

		# ----- #

		# Define the merry Christmas "Texts" key as the Christmas texts file
		self.christmas["Files"]["Merry Christmas"]["Texts"] = self.current_year["Files"]["Christmas"]["Merry Christmas"]["Texts"]

		# Define a list of files to import from the "Merry Christmas" dictionary of the year "Texts" files dictionary
		to_import = [
			"Social networks",
			"Friends"
		]

		# Iterate through the list of files to import
		for file in to_import:
			# If the file is "Social networks"
			if file == "Social networks":
				# Define the local files dictionary as the year texts "Files" dictionary
				files = year_texts

			# If the file is "Friends"
			if file == "Friends":
				# Define the local files dictionary as the "Christmas" files dictionary of the current year
				files = self.current_year["Files"]["Christmas"]

			# Define the file inside the defind local "Merry Christmas" files dictionary
			self.christmas["Files"]["Merry Christmas"][file] = files["Merry Christmas"][file]

		# ----- #

		# Define a list of files to import from the root "Christmas" dictionary of the year "Texts" files dictionary
		to_import = [
			"Steps",
			"Profile pictures to change",
			"Watch",
			"Eat"
		]

		# Iterate through the list of files to import
		for file in to_import:
			# If the file is not inside the defined list
			if file not in ["Watch", "Eat"]:
				# Define the local files dictionary as the year texts "Files" dictionary
				files = year_texts

			# If the file is inside the defined list
			if file in ["Watch", "Eat"]:
				# Define the local files dictionary as the "Christmas" files dictionary of the current year
				files = self.current_year["Files"]["Christmas"]

			# Define the file inside the defined local "Christmas" files dictionary
			self.christmas["Files"][file] = files[file]

		# ----- #

		# Define the root "social networks" dictionary
		self.social_networks = {
			"Numbers": {
				"Total": 0,
				"Iteration": 1
			},
			"List": [],
			"Custom links": {
				"Wattpad": self.Social_Networks.social_networks["Dictionary"]["Wattpad"]["Profile"]["Links"]["Conversations"]
			},
			"States": {
				"First separator": False
			},
			"Spaces": {
				"First": True
			},
			"Input text": ""
		}

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

		# ---------- #

		# Define the "Methods" dictionary
		self.christmas["Methods"] = {
			"List": [
				"Copy_Christmas_Text",
				"Open_Social_Networks",
				"Change_Profile_Pictures",
				"Wish_Merry_Christmas_To_Friends",
				"Open_Christmas_Theme",
				"Open_Folder",
				"Open_Music_Player",
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

	def Define_Christmas_Texts(self):
		# Create a shortcut to the Christmas "Texts" file
		texts_file = self.christmas["Files"]["Merry Christmas"]["Texts"]

		# Get the contents of the file
		contents = self.File.Contents(texts_file)

		# Read the Merry Christmas "Texts" file to get the "Texts" file dictionary
		self.christmas["Texts"] = self.File.Dictionary_2(texts_file, convert_lists_into_texts = True)

		# Define a dictionary of text keys to replace
		text_keys = {
			"General": "general, title()",
			"General with hashtags": "general_with_hashtags",
			"User language": self.language["Full"],
			"User language with hashtags": "[language]_with_hashtags",
			"For friends": "for_friends"
		}

		# Iterate through the list of text key to use and to replace
		for to_use, to_replace in text_keys.items():
			# If the to use key is not "User language"
			if to_use != "User language":
				# Get the text to replace
				to_replace = self.Language.language_texts[to_replace]

			# Replace the text key in the root "Texts" dictionary with the to use key
			self.christmas["Texts"][to_use] = self.christmas["Texts"][to_replace]

			# Remove the to replace key
			self.christmas["Texts"].pop(to_replace)

		# Define the "For friends" key as the last three lines of the file
		self.christmas["Texts"]["For friends"] = self.Text.From_List(contents["Lines"][-3:])

	def Today_Is_Day(self, days = [25], today = None):
		# Define the local date as the "today" parameter
		date = today

		# If the "today" parameter is None
		if today == None:
			# Define the local date as the root one
			date = self.date

		# Define the local "today is day" state as False
		today_is_day = False

		# If the current day is inside the local list of days
		# And the current month is the Christmas month (12 - December)
		if (
			date["Units"]["Day"] in days and
			date["Units"]["Month"] == self.christmas["Dates"]["25 of December"]["Units"]["Month"]
		):
			# Change the local "today is day" state to True
			today_is_day = True

		# Return the local state
		return today_is_day

	def Current_Month_Is_December(self, today):
		# Define the local date as the "today" parameter
		date = today

		# If the "today" parameter is None
		if today == None:
			# Define the local date as the root one
			date = self.date

		# Define the local "current month is December" state as False
		current_month_is_december = False

		# If the current month is the Christmas month (12 - December)
		if date["Units"]["Month"] == self.christmas["Dates"]["25 of December"]["Units"]["Month"]:
			# Change the local "current month is December" state to True
			current_month_is_december = True

		# Return the local state
		return current_month_is_december

	def Copy_Christmas_Text(self, key):
		# Copy the Christmas text
		self.Text.Copy(self.christmas["Texts"][key], first_space = False)

	def Open_Social_Networks(self, social_networks):
		# Define a list of keys to import
		to_import = [
			"List",
			"Do not open",
			"Input texts"
		]

		# Iterate through the list
		for key in to_import:
			# If the key is inside the parameter dictionary
			if key in social_networks:
				# Import it to the root dictionary
				self.social_networks[key] = social_networks[key]

			# Else, if the key is present in the root dictionary
			elif key in self.social_networks:
				# Remove it
				self.social_networks.pop(key)

		# Update the total number of social networks
		self.social_networks["Numbers"]["Total"] = len(self.social_networks["List"])

		# Iterate through the social network numbers and names inside the list of social networks
		for social_network_number, social_network_name in enumerate(self.social_networks["List"], start = 1):
			# Update the "Iteration" number to be the current one
			self.social_networks["Numbers"]["Iteration"] = social_network_number

			# Update the list of social networks to be the local current social network
			self.social_networks["List"] = [
				social_network_name
			]

			# Make a copy of the root social networks dictionary
			social_networks_copy = deepcopy(self.social_networks)

			# If the "Custom links" key is inside the parameter dictionary
			if "Custom links" in social_networks:
				# Iterate through the custom link names and links
				for name, custom_link in social_networks["Custom links"].items():
					# Import the link
					social_networks_copy["Custom links"][name] = social_networks["Custom links"][name]

			# If the "Input text" key is inside the parameter dictionary
			if "Input text" in social_networks:
				# Define the local input text as the root "Input text" key
				input_text = social_networks["Input text"]

				# If the user language is inside the input text
				if self.language["Small"] in input_text:
					# Get the input text in the user language
					input_text = input_text[self.language["Small"]]

				# Update the "Input text" key of the local copy dictionary
				social_networks_copy["Input text"] = input_text

			# Define the "First separator" initially as False
			social_networks_copy["States"]["First separator"] = False

			# If the number of social networks is more than one
			if self.social_networks["Numbers"]["Total"] > 1:
				# Change the "First separator" to True
				social_networks_copy["States"]["First separator"] = True

			# Open the social network using the "Open_Social_Network" sub-class of the "Social_Networks" class
			self.Social_Networks.Open_Social_Network(social_networks_copy)

		# If the "Last separator" key is inside the parameter dictionary
		if "Last separator" in social_networks:
			# Show a five dash space separator
			print()
			print(self.separators["5"])

	def Change_Profile_Pictures(self):
		# Create a shortcut to the Christmas "Profile pictures to change" file
		file = self.christmas["Files"]["Profile pictures to change"]

		# Read the "Profile pictures to change" file to get the file dictionary
		self.christmas["Profile pictures to change"] = self.File.Dictionary_2(file)

		# ---------- #

		# Define the "Digital identities" dictionary
		self.christmas["Digital identities"] = {
			"Numbers": {
				"Total": 0
			},
			"List": [
				"Stake2",
				"Funkysnipa Cat",
				"Sunset Shimmer and Stake2"
			],
			"Dictionary": {
				"Stake2": {
					"List": [
						"Stake2"
					],
					"Genders": [
						"masculine"
					],
					"Social networks": [],
					"Folder": "",
					"Use profile folder": True
				},
				"Funkysnipa Cat": {
					"List": [
						"Funkysnipa Cat"
					],
					"Genders": [
						"masculine"
					],
					"Social networks": [],
					"Folder": "",
					"Use profile folder": True
				},
				"Sunset Shimmer and Stake2": {
					"List": [
						"Sunset Shimmer",
						"Stake2"
					],
					"Genders": [
						"feminine",
						"masculine"
					],
					"Social networks": [],
					"Folder": "",
					"Use profile folder": False
				}
			}
		}

		# Update the total number of digital identities
		self.christmas["Digital identities"]["Numbers"]["Total"] = len(self.christmas["Digital identities"]["List"])

		# ---------- #

		# Define the text key to get the "Christmas version {}" text template
		text_key = "christmas_version_{}"

		# Get the Christmas version text template
		christmas_version_text_template = self.Language.language_texts[text_key]

		# ---------- #

		# Create a shortcut to the "Digital identities" image folders
		digital_identities_folder = self.folders["Image"]["Social networks"]["Digital identities"]["root"]

		# Make a local copy of the "Digital identities" dictionary
		digital_identities = deepcopy(self.christmas["Digital identities"])

		# Get a list of identity keys
		keys = list(digital_identities["Dictionary"].keys())

		# Define a local digital identity
		digital_identity_number = 1

		# Create a shortcut to the total number of digital identities
		total_digital_identities_number = self.christmas["Digital identities"]["Numbers"]["Total"]

		# Iterate through the dictionary of digital identities
		for identity, dictionary in digital_identities["Dictionary"].items():
			# Define the identity name dictionary
			identity_name = {}

			# Iterate through the defined list
			for key in ["English", "Language", "Language with prefix", "Language with prefix and quotes"]:
				# Define the dictionary of parameters to use in the "From_List" method of the "Text" utility class
				parameters = {
					"items": dictionary["List"],
					"genders": dictionary["Genders"],
					"language": self.language["Small"],
					"next_line": False
				}

				# If the "with prefix" text is not inside the key
				if "with prefix" not in key:
					# Remove the "genders" key
					parameters.pop("genders")

				# If the key is "English"
				if key == "English":
					# Change the "language" key to English
					parameters["language"] = "en"

				# If the "and quotes" text is inside the key
				if "and quotes" in key:
					# Add the "quotes" key as True
					parameters["quotes"] = True

				# Create the identity name using the dictionary of parameters and define it inside the identity name dictionary
				identity_name[key] = self.Text.From_List(**parameters)

			# Add the language identity name and identity names dictionary to the start of the dictionary
			dictionary = {
				"Name": identity_name["Language"],
				"Names": identity_name,
				**dictionary
			}

			# ---------- #

			# If the identity is not the first one
			if identity != keys[0]:
				# Show a space separator
				print()

			# Define the number of separators as five
			separators = "5"

			# If the identity is not the first one
			if identity != keys[0]:
				# Change the number of separators to three
				separators = "3"

			# Show the defined number of dash space separators
			print(self.separators[separators])
			print()

			# Show the current and total digital identity numbers
			print(self.Language.language_texts["number_of_the_digital_identity"] + ":")
			print("\t" + "[" + str(digital_identity_number) + "/" + str(total_digital_identities_number) + "]")
			print()

			# Show the digital identity
			print(self.Language.language_texts["digital_identity"] + ":")
			print("\t" + identity_name["Language"])
			print()

			# ---------- #

			# Format the Christmas version text template with the digital identity name with prefix and define it as the key
			key = christmas_version_text_template.format(identity_name["Language with prefix"])

			# Get the folder of the digital identity using its name
			folder = digital_identities_folder + identity_name["Language"] + "/"

			# If the "Use profile folder" switch is True
			if dictionary["Use profile folder"] == True:
				# Add the "Profile" folder to the folder
				folder += self.Language.language_texts["profile, title()"] + "/"

			# Add the identity folder to the dictionary
			dictionary["Folder"] = folder

			# Show the "Christmas step action" text in the user language
			print(self.Language.language_texts["christmas_step_action"] + ":")

			# Define the text template as "Opening the image folder of the Digital Identity "{}""
			text_template = self.language_texts["opening_the_image_folder_of_the_digital_identity_{}"]

			# Format the template with the language identity name
			text = text_template.format(identity_name["Language"])

			# Show the text
			print("\t" + text + "...")

			# Open the identity folder
			self.System.Open(dictionary["Folder"])

			# If the identity is the first one
			if identity == keys[0]:
				# Show a space separator
				print()

			# ---------- #

			# Get the list of social networks of the digital identity and add it to the dictionary
			dictionary["Social networks"] = self.christmas["Profile pictures to change"][key]

			# Define the input text as "Press Enter when you finish changing your profile picture [identity_name] on {social_network} to their Christmas version"
			input_text = self.language_texts["press_enter_when_you_finish_changing_your_profile_picture_[identity_name], type: long"]

			# Replace the "[identity_name]" with the language identity name with prefix and quotes around the name
			input_text = input_text.replace("[identity_name]", identity_name["Language with prefix and quotes"])

			# Define a local dictionary of social networks
			social_networks = {
				# Define the list of social networks to open
				"List": dictionary["Social networks"],

				# Define the empty "Custom links" dictionary
				"Custom links": {},

				# Import the local input text
				"Input text": input_text
			}

			# Define a list of social networks to update
			to_update = [
				"Instagram",
				"Spirit Fanfics",
				"Steam",
				"Twitter",
				"Wattpad",
				"YouTube"
			]

			# Iterate through the list of social network names
			for social_network_name in to_update:
				# If the social network is inside the list of social networks
				if social_network_name in social_networks["List"]:
					# Create a shortcut to the root link
					link = self.Social_Networks.social_networks["Dictionary"][social_network_name]["Profile"]["Links"]["Profile"]

					# If the current social network is inside the defined list
					if social_network_name in ["Twitter", "Instagram", "Spirit Fanfics"]:
						# Update the link to be the root link of the social network
						link = self.Social_Networks.social_networks["Dictionary"][social_network_name]["Information"]["Link"]

					# If the current social network is "Twitter"
					if social_network_name == "Twitter":
						# Add the "settings profile" part
						link += "settings/profile"

					# If the current social network is "Instagram"
					if social_network_name == "Instagram":
						# Add the "edit profile picture" part
						link += "accounts/edit/"

					# If the current social network is "Spirit Fanfics"
					if social_network_name == "Spirit Fanfics":
						# Add the "edit avatar" part
						link += "editar/avatar"

					# If the current social network is "Steam"
					if social_network_name == "Steam":
						# Add the "edit avatar" part
						link += "/edit/avatar"

					# If the current social network is "YouTube"
					if social_network_name == "YouTube":
						# Replace "www" with "studio" in the link
						link = link.replace("www", "studio")

						# Add the "edit profile picture" part
						link += "/editing/profile"

					# Update the root link
					social_networks["Custom links"][social_network_name] = link

			# If the identity is not the first one
			if identity != keys[0]:
				# Show a space separator
				print()

			# Open the list of social networks
			self.Open_Social_Networks(social_networks)

			# ---------- #

			# Update the root dictionary with the local one using the English identity as a key
			self.christmas["Digital identities"]["Dictionary"][identity_name["English"]] = dictionary

			# ---------- #

			# Add one to the digital identity number
			digital_identity_number += 1

	def Wish_Merry_Christmas_To_Friends(self):
		# Copy the Christmas text for friends
		self.Text.Copy(self.christmas["Texts"]["For friends"], first_space = False)

		# Show a space separator
		print()

		# Open the "Friends" file which is inside the "Merry Christmas" folder
		self.Open_File("Friends")

	def Open_Christmas_Theme(self):
		# Show the "Christmas step action" text in the user language
		print(self.Language.language_texts["christmas_step_action"] + ":")

		# Create a shortcut to the text about defining the Christmas theme for the computer
		text = self.language_texts["applying_the_christmas_theme_on_the_computer"]

		# Show the text with a tab and three periods
		print("\t" + text + "...")

		# Open the Christmas theme to use it on the computer
		self.System.Open(self.christmas["Theme"])

	def Open_Folder(self, folder_name):
		# Show the "Christmas step action" text in the user language
		print(self.Language.language_texts["christmas_step_action"] + ":")

		# Get the text key for the folder name
		text_key = folder_name.lower() + ", title()"

		# Get the text for the folder
		folder_text = self.Language.language_texts[text_key].lower()

		# Create a shortcut to the text template about opening the folder for the current year
		text_template = self.language_texts["opening_the_christmas_{}_folder_for_{}"]

		# If the user language is not English
		# And the folder name is "root"
		if (
			self.language["Small"] != "en" and
			folder_name == "root"
		):
			# Change the text template
			text_template = self.language_texts["opening_the_{}_christmas_folder_of_{}"]

		# Format the text template with the folder text and the current year number
		text = text_template.format(folder_text, self.current_year["Number"])

		# Show the text with a tab
		print("\t" + text + "...")

		# Get the folder
		folder = self.christmas["Folders"]["Year"][folder_name]

		# If the "root" key is present
		if "root" in folder:
			# Define the folder as the value in the "root" key
			folder = folder["root"]

		# Open it
		self.System.Open(folder)

	def Open_Music_Player(self, music_player):
		# Show the "Christmas step action" text in the user language
		print(self.Language.language_texts["christmas_step_action"] + ":")

		# Updates the "Music player" dictionary with the value corresponding to the specified "music player" parameter
		self.christmas["Music player"] = self.christmas["Music players"][music_player]

		# Create a shortcut to the text template about opening the music player for the user to listen to the playlist of Christmas songs
		text_template = self.language_texts["opening_the_{}_music_player_for_you_to_listen_to_the_playlist_of_christmas_songs"]

		# Format the text template with the name of the music player
		text = text_template.format(self.christmas["Music player"]["Name"])

		# Show the text with a tab
		print("\t" + text + "...")

		# Open the music player program so the user can listen to the soundtrack of the story
		self.System.Open(self.christmas["Music player"]["Link"], verbose = False)

		# If the "Testing" switch is False
		if self.switches["Testing"] == False:
			# Wait for one second
			self.Date.Sleep(1)

	def Create_Discord_Status(self):
		# Define the status as the "Merry Christmas! :3" in the user language plus the current year, and the Christmas tree and present emojis
		status = self.Language.language_texts["merry_christmas"] + "! :3 🎄🎁 ({})".format(self.current_year["Number"])

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
			# If the file name is inside the "Merry Christmas" dictionary
			if file_name in self.christmas["Files"]["Merry Christmas"]:
				# Define the file as the file inside that dictionary
				file = self.christmas["Files"]["Merry Christmas"][file_name]

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
		files = self.Folder.Contents(self.folders["Apps"]["Shortcuts"]["White"]["root"])["File"]["List"]

		# Iterate through the list of files
		for file in files:
			# Try to find the "Apps.lnk" shortcut inside the file
			if "Apps.lnk" in file:
				# If found, define the "apps" variable as the current file
				apps = file

		# Open the "Apps.lnk" shortcut
		self.System.Open(apps, verbose = False)

		# Define the local list of item types
		item_types = [
			"Watch",
			"Eat"
		]

		# Iterate through the local list of item types
		for item_type in item_types:
			# Define the text key for the file as "things_to_" plus the item type in lowercase
			text_key = "things_to_" + item_type.lower()

			# Get the text for the file in the user language
			text = self.language_texts[text_key]

			# Show the text in the user language
			print(text + ":")

			# Get the text file
			text_file = self.christmas["Files"][item_type]

			# Open the text file
			self.System.Open(text_file, verbose = False)

			# Get the lines of the text file
			lines = self.File.Contents(text_file)["Lines"]

			# Define the tab as one tab
			tab = "\t"

			# If the lines of the file is an empty list
			if lines == []:
				# Show the "[Nothing]" text with the tab
				print(tab + "[" + self.Language.language_texts["nothing, title()"] + "]")

			# Iterate through the line numbers and lines inside the list of lines
			for line_number, line in enumerate(lines, start = 1):
				# Show the tab, the line number, and the line
				print(tab + str(line_number) + ". " + line)

			# If the item type is not the last one
			if item_type != item_types[-1]:
				# Show a space separator at the end
				print()

		# Define the input text to be about when the user finishes watching all of the Christmas-special episodes
		input_text = self.language_texts["press_enter_when_you_finish_watching_all_of_the_christmas_special_episodes"]

		# Use it to ask the user to press Enter when they finish watching
		self.Input.Type(input_text)
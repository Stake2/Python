# Years.py

# Import some useful modules
import importlib
from copy import deepcopy

class Years(object):
	def __init__(self, select_year = False):
		# Import some utility classes
		self.Import_Utility_Classes()

		# Define the folders of the module
		self.folders = self.Define_Folders(object = self).folders

		# Define basic variables for the class
		self.Define_Basic_Variables()

		# Define the text dictionaries of the class
		self.Define_Texts()

		# Define the folders and files of the class
		self.Define_Folders_And_Files()

		# Define the dictionaries of the class
		self.Define_Dictionaries()

		# Define the "Folder items" dictionary
		self.Define_Folder_Items_Dictionary()

		# Define the "Social networks" dictionary
		self.Define_Social_Networks()

		# Define the "Format strings" dictionary
		self.Define_Format_Strings()

		# Define the root "Years" dictionary
		self.Define_Years_Dictionary()

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

		# Define the current year number
		self.current_year_number = str(self.date["Units"]["Year"])

	def Define_Texts(self):
		# Define the "Texts" dictionary
		self.texts = self.JSON.To_Python(self.module["Files"]["Texts"])

		# Define the "Language texts" dictionary
		self.language_texts = self.Language.Item(self.texts)

		# ---------- #

		# Define the "separators" dictionary
		self.separators = {}

		# Create separators from one to twenty characters
		for number in range(1, 21):
			# Define the empty string
			string = ""

			# Add dash separators to it
			while len(string) != number:
				string += "-"

			# Add the separator to the separators dictionary
			self.separators[str(number)] = string

		# Create a copy of the original separators dictionary
		separators_copy = deepcopy(self.separators)

		# Get the keys
		keys = list(separators_copy.keys())

		# Iterate through the separators and enumerate them
		for number, key in enumerate(keys.copy()):
			# Replace the dashes with underscores
			separator = separators_copy[key].replace("-", "_")

			# Update the separator inside the root list
			separators_copy[key] = separator

		# Add the underscore separators to the original separators dictionary
		self.separators["Underlines"] = separators_copy

	def Define_Folders_And_Files(self):
		# Define the root "Years" dictionary with its "Text" and "Image" folders dictionary
		self.years = {
			"Folders": {
				"Text": {
					"root": self.folders["Notepad"]["Years"]["root"]
				},
				"Image": {
					"root": self.folders["Image"]["Years"]["root"]
				}
			}
		}

		# ---------- #

		# Define and create the year "Texts" text folder
		self.years["Folders"]["Text"]["Texts"] = {
			"root": self.years["Folders"]["Text"]["root"] + self.Language.language_texts["texts, title()"] + "/"
		}

		self.Folder.Create(self.years["Folders"]["Text"]["Texts"]["root"])

		# Define and create the "Years.json" file
		self.years["Folders"]["Text"]["Years"] = self.years["Folders"]["Text"]["root"] + "Years.json"
		self.File.Create(self.years["Folders"]["Text"]["Years"])

		# Define and create the "Years list.txt" file
		self.years["Folders"]["Text"]["Years list"] = self.years["Folders"]["Text"]["root"] + self.Date.language_texts["years_list"] + ".txt"
		self.File.Create(self.years["Folders"]["Text"]["Years list"])

		# ---------- #

		# Define and create the year "Images" image folder
		self.years["Folders"]["Image"]["Images"] = {
			"root": self.years["Folders"]["Image"]["root"] + self.Language.language_texts["images, title()"] + "/"
		}

		self.Folder.Create(self.years["Folders"]["Image"]["Images"]["root"])

	def Define_Dictionaries(self):
		# Define the root "Summary" dictionary with the "Websites" dictionary of websites to post the year summary on
		self.years["Summary"] = {
			"Websites": {
				"Numbers": {
					"Total": 0
				},
				"List": [
					"WriteAs",
					"Fandom Stake2"
				],
				"Dictionary": {}
			}
		}

		# Add the "WriteAs" website
		self.years["Summary"]["Websites"]["Dictionary"]["WriteAs"] = {
			"Name": "WriteAs",
			"Links": {}
		}

		# Iterate through the list of small languages
		for language in self.languages["Small"]:
			# Define the link
			link = "https://write.as/stake2/" + self.texts["summary_of_my_year_of_{current_year}, type: link"][language]

			# Add it to the links dictionary
			self.years["Summary"]["Websites"]["Dictionary"]["WriteAs"]["Links"][language] = link

		# Add the "Fandom" website
		self.years["Summary"]["Websites"]["Dictionary"]["Fandom Stake2"] = {
			"Name": "Fandom Stake2",
			"Links": {
				"pt": "https://the-stake2.fandom.com/pt-br/wiki/{current_year}#Resumo_do_Ano",
				"en": "https://stake2.fandom.com/wiki/{current_year}#Year_Summary"
			}
		}

		# Update the total number of websites
		self.years["Summary"]["Websites"]["Numbers"]["Total"] = len(list(self.years["Summary"]["Websites"]["Dictionary"].keys()))

	def Define_Social_Networks(self):
		# Define the root "Social networks" dictionary
		self.social_networks = {
			"Numbers": {
				"Total": 0
			},
			"List": [
				"Merry Christmas",
				"Summary",
				"New Year"
			],
			"Dictionary": {
				"Merry Christmas": {
					"Name": {},
					"Numbers": {
						"Total": 0
					},
					"List": [
						"Twitter",
						"Bluesky {} Threads",
						"WhatsApp",
						"Instagram {} Facebook",
						"Discord",
						"Wattpad"
					],
					"Dictionary": {}
				},
				"Summary": {
					"Name": {},
					"Numbers": {
						"Total": 0
					},
					"List": [
						"Twitter, Bluesky, {} Threads",
						"WhatsApp",
						"Instagram {} Facebook",
						"Discord"
					],
					"Dictionary": {}
				}
			}
		}

		# Update the total number of social network lists
		self.social_networks["Numbers"]["Total"] = len(self.social_networks["List"])

		# Iterate through the list names and dictionaries isnide the root social networks "Dictionary"
		for list_name, dictionary in deepcopy(self.social_networks["Dictionary"]).items():
			# Update the total number of social networks
			dictionary["Numbers"]["Total"] = len(dictionary["List"])

			# If the "Name" dictionary is empty
			if dictionary["Name"] == {}:
				# Create the text key by converting the list name into lowercase and replacing spaces with underscores
				text_key = list_name.lower().replace(" ", "_")

				# If the underscore character is not inside the text key
				if "_" not in text_key:
					# Add the ", title()" text
					text_key += ", title()"

				# Define the name as the text dictionary inside the text key
				name = self.Language.texts[text_key]

				# Update the root "Name" dictionary
				dictionary["Name"] = name

			# Define a local social network number
			social_network_number = 0

			# Iterate through the list of social network names
			for social_network_name in dictionary["List"].copy():
				# Create the local social network dictionary
				social_network = {
					"Name": {}
				}

				# Iterate through the list of small languages
				for language in self.languages["Small"]:
					# Define the language social network name as the root name
					language_social_network_name = social_network_name

					# If the "{}" format string is inside the language social network name
					if "{}" in language_social_network_name:
						# Format it with the "and" text in the current language
						language_social_network_name = language_social_network_name.format(self.Language.texts["and"][language])

					# Add the language social network name to the social network "Name" dictionary in the current language
					social_network["Name"][language] = language_social_network_name

				# Update the social network name to be the one with the "and" text in English
				social_network_name = social_network_name.format(self.Language.texts["and"]["en"])

				# Also update the social network name in the list
				dictionary["List"][social_network_number] = social_network_name

				# Add the social network to the social networks "Dictionary" of the current list
				dictionary["Dictionary"][social_network_name] = social_network

				# Add one to the local social network number
				social_network_number += 1

			# Update the root dictionary with the local one
			self.social_networks["Dictionary"][list_name] = dictionary

		# Define the "New Year" dictionary as the "Merry Christmas" dictionary because their list of social networks are the same
		self.social_networks["Dictionary"]["New Year"] = self.social_networks["Dictionary"]["Merry Christmas"]

		# Update the root "Name" dictionary to be the "New Year" text dictionary
		self.social_networks["Dictionary"]["New Year"]["Name"] = self.Language.texts["new_year"]

	def Define_Years_Dictionary(self):
		# Define the root "Years" dictionary
		self.years = {
			**self.years,
			"Author": "Izaque (Stake2, Funkysnipa Cat)",
			"Numbers": {
				"Total": 0
			},
			"List": [],
			"Dictionary": {},
			"Current year": {},
			"States": {
				"Current year folder exists": True
			}
		}

		# ---------- #

		# Define the date string as "1 of December" and format it with the year
		date_string = "01/12/{}".format(self.date["Units"]["Year"])

		# Create the date dictionary from the date string
		# And add it to the "December" key of the root "Summary" dictionary
		self.years["Summary"]["December"] = self.Date.From_String(date_string, format = "%d/%m/%Y")

		# Add the number of month days in December
		self.years["Summary"]["Month days"] = self.years["Summary"]["December"]["Timezone"]["DateTime"]["Units"]["Month days"]

		# Add the year
		self.years["Summary"]["Year"] = self.date["Units"]["Year"]

		# Create a shortcut to the month days and year
		month_days_and_year = (self.years["Summary"]["Month days"], self.years["Summary"]["Year"])

		# Define the date string as the last day of December and format it with the month days and year
		date_string = "{}/12/{}".format(*month_days_and_year)

		# Create the date dictionary from the date string and format and add it to the "Date" key
		self.years["Summary"]["Date"] = self.Date.From_String(date_string, format = "%d/%m/%Y")

		# ---------- #

		# Get the list of years (from 2018 to the current year)
		self.years["List"] = self.Date.Create_Years_List(function = str)

		# Update the total number of years
		self.years["Numbers"]["Total"] = len(self.years["List"])

		# Define the current year folder
		current_year_folder = self.years["Folders"]["Text"]["root"] + str(self.date["Units"]["Year"]) + "/"

		# If the current year folder does not exist
		if self.Folder.Exists(current_year_folder) == False:
			# Define the "Current year folder exists" as False
			self.years["States"]["Current year folder exists"] = False

		# Convert the list of years into a text
		text_to_write = self.Text.From_List(self.years["List"])

		# Write the list of years into the "Year list.txt" file
		self.File.Edit(self.years["Folders"]["Text"]["Years list"], text_to_write, "w")

		# ---------- #

		# Iterate through the list of year numbers
		for year_number in self.years["List"]:
			# Create the local year dictionary with its keys
			year = {
				"Number": year_number,
				"Folders": {},
				"Files": {},
				"Information": {},
				"Statistics": {}
			}

			# Iterate through the list of folder types
			for folder_type in ["Text", "Image"]:
				# Iterate through the defined list of item types
				for item_type in ["Folders", "Files"]:
					# If the folder type is not image
					# Or it is
					# And the item type is not "Files"
					if (
						folder_type != "Image" or
						folder_type == "Image" and
						item_type != "Files"
					):
						# Create the empty folder type dictionary inside the item type dictionary
						# Example: item_type: "Folders", folder_type: "Text"
						year[item_type][folder_type] = {}

				# Create the local year folders dictionary of the folder type
				year["Folders"][folder_type] = {
					"root": self.years["Folders"][folder_type]["root"] + year_number + "/"
				}

				# Create the root year folder
				self.Folder.Create(year["Folders"][folder_type]["root"])

				# ----- #

				# If the folder type is "Text"
				if folder_type == "Text":
					# Create the text folders of the year and get back the updated year dictionary
					year = self.Create_Text_Folders(year)

				# ----- #

				# If the folder type is "Image"
				if folder_type == "Image":
					# Create the image folders of the year and get back the updated year dictionary
					year = self.Create_Image_Folders(year)

			# Iterate through the text folders inside the "Text" folders dictionary
			for key, folder in year["Folders"]["Text"].items():
				# If the key is not "root"
				if key != "root":
					# Add the folder key and value to the root dictionary
					year["Folders"][key] = folder

			# If the "Text" key is inside the year "Files" dictionary
			if "Text" in year["Files"]:
				# Add the keys of the "Text" files dictionary to the root year "Files" dictionary
				year["Files"].update(year["Files"]["Text"])

			# Add the local year dictionary to the root years "Dictionary"
			self.years["Dictionary"][year_number] = year

		# Define the "Current year" key as the current year dictionary which is inside the root "Years" dictionary
		self.years["Current year"] = self.years["Dictionary"][self.current_year_number]

		# ---------- #

		# Define the root "Texts" dictionary
		texts = {
			"Number": "Texts",
			"Folders": {
				"Text": {
					"root": self.years["Folders"]["Text"]["Texts"]["root"]
				}
			},
			"Files": {
				"Text": {}
			}
		}

		# Create the root "Texts" text folder
		self.Folder.Create(texts["Folders"]["Text"]["root"])

		# Create the text folders of the "Texts" folder and get back the updated texts dictionary
		texts = self.Create_Text_Folders(texts)

		# Iterate through the text folders inside the "Text" folders dictionary
		for key, folder in texts["Folders"]["Text"].items():
			# If the key is not "root"
			if key != "root":
				# Add the folder key and value to the root dictionary
				texts["Folders"][key] = folder

		# If the "Text" key is inside the texts "Files" dictionary
		if "Text" in texts["Files"]:
			# Add the keys of the "Text" files dictionary to the root texts "Files" dictionary
			texts["Files"].update(texts["Files"]["Text"])

		# Define the root "Texts" dictionary as the local one
		self.years["Texts"] = texts

		# ---------- #

		# Create the local "Images" dictionary
		images = {
			"Number": "Image",
			"Folders": {
				"root": self.years["Folders"]["Image"]["root"] + self.Language.language_texts["images, title()"] + "/"
			},
			"Files": {}
		}

		# Create the image folders and files of the "Images" folder
		images = self.Create_Image_Folders(images)

		# Define the "Images" dictionary as the local "Images" dictionary
		self.years["Folders"]["Image"]["Images"] = images

		# ---------- #

		# Make a local copy of the root "Years" dictionary
		dictionary = deepcopy(self.years)

		# Define the keys to remove
		to_remove = [
			"Folders",
			"Summary",
			"Folder items",
			"Author",
			"States",
			"Format strings"
		]

		# Remove the keys
		for key in to_remove:
			dictionary.pop(key)

		# Define a list of item types to iterate through
		item_types = [
			"Folders",
			"Files"
		]

		# Define a list of keys to add at the end of the dictionary
		add_to_end = [
			"Image"
		]

		# Iterate through the year numbers and dictionaries inside the root "Years" dictionary
		for year_number, year in self.years["Dictionary"].items():
			# Create a copy of the year dictionary
			year = deepcopy(year)

			# Iterate through the defined list of item types
			for item_type in item_types:
				# Remove the "Text" key of the item type dictionary inside the year dictionary
				year[item_type].pop("Text")

			# Add the keys above to the end of the year "Folders" dictionary
			year["Folders"] = self.JSON.Add_To_End_Of_Dictionary(year["Folders"], to_add = add_to_end)

			# Update the year dictionary inside the local "Years" dictionary
			dictionary["Dictionary"][year_number] = year

		# Add the keys above to the end of the year "Folders" dictionary
		dictionary["Current year"]["Folders"] = self.JSON.Add_To_End_Of_Dictionary(dictionary["Current year"]["Folders"], to_add = add_to_end)

		# Iterate through the defined list of item types
		for item_type in item_types:
			# Remove the "Text" key of the item type dictionary inside the "Current year" dictionary
			dictionary["Current year"][item_type].pop("Text")

			# Remove the "Text" key of the item type dictionary inside the "Texts" dictionary
			dictionary["Texts"][item_type].pop("Text")

		# Write the local updated "Years" dictionary to the "Years.json" file
		self.JSON.Edit(self.years["Folders"]["Text"]["Years"], dictionary)

	def Define_Folder_Items_Dictionary(self):
		# Define the root "Folder items" dictionary
		self.years["Folder items"] = {
			"Numbers": {
				"Total": 0
			},
			"List": [
				"Root",
				"Language",
				"Christmas",
				"New Year",
				"Texts"
			],
			"Dictionary": {
				"Root": {
					"Folders": [
						"Language",
						"Christmas",
						"Summary",
						"New Year"
					],
					"Files": [
						"Created in",
						"Edited in"
					]
				},
				"Language": {
					"Folders": [
						"Completed tasks",
						"Firsts of the year",
						"Gaming sessions",
						"Watched media"
					],
					"Files": [
						"Welcome",
						"Summary",
						"This Year I",
						"This Year I (post)",
						"This Year I (personal version)",
						"Goodbye",
						"Yearly statistics",
						"FutureMe"
					],
					"User language files": [
						"Yearly statistics",
						"FutureMe"
					]
				},
				"Christmas": {
					"Folders": {
						"Merry Christmas": {
							"Files": [
								"Texts",
								"Friends"
							]
						}
					},
					"Files": [
						"Watch",
						"Eat"
					]
				},
				"New Year": {
					"Folders": [
						"Social networks"
					],
					"Files": [
						"Texts"
					]
				},
				"Texts": {
					"Folders": {
						"Christmas": {
							"Folders": {
								"Merry Christmas": {
									"Folders": [
										"Social networks"
									]
								}
							},
							"Files": {
								"Steps": {
									"JSON": True
								},
								"Profile pictures to change": {}
							}
						}
					}
				}
			}
		}

		# Update the total number of folder item dictionaries
		self.years["Folder items"]["Numbers"]["Total"] = len(self.years["Folder items"]["List"])

		# Iterate through the folder item keys and dictionaries inside the root folder items "Dictionary"
		# 
		# Folder item keys: [Root, Language, Christmas, New Year, Texts]
		for folder_item, folder_item_dictionary in self.years["Folder items"]["Dictionary"].items():
			# Iterate through the item type keys and dictionaries inside the folder item dictionary
			# 
			# Item types: ["Folders", "Files", and sometimes "User language files"]
			for item_type, item_type_dicitionary in folder_item_dictionary.items():
				# If the item type dictionary is a list
				if type(item_type_dicitionary) == list:
					# Create a dictionary of empty dictionaries using the list of item types as keys
					item_type_dicitionary = {key: {} for key in item_type_dicitionary}

				# Iterate through the item names and dictionaries inside the item type dictionary
				# 
				# Item names list example: [Christmas, Summary, New Year, Language]
				for item_name, item_dictionary in item_type_dicitionary.items():
					# If the item dictionary is not empty
					if item_dictionary != {}:
						# Iterate through the sub-item type keys and dictionaries inside the item dictionary
						# 
						# Sub-item type list example: [Folders, Files]
						for sub_item_type, sub_item_type_dictionary in item_dictionary.items():
							# If the sub-item type dictionary is a list
							if type(sub_item_type_dictionary) == list:
								# Create a dictionary of empty dictionaries using the list of sub-item types as keys
								sub_item_type_dictionary = {key: {} for key in sub_item_type_dictionary}

							# Iterate through the sub-item names and dictionaries inside the sub-item type dictionary
							# 
							# Sub-item names list examples: [Watch, Eat], [Texts]
							for sub_item_name, sub_item_dictionary in sub_item_type_dictionary.items():
								# Define the folder sub-item name and get the sub-item dictionary back
								sub_item_dictionary = self.Define_Folder_Item_Name(sub_item_type, sub_item_name, sub_item_dictionary)

								# Iterate through the sub-sub-item type keys and dictionaries inside the item dictionary
								# 
								# Sub-sub-item type list example: [Folders, Files]
								for sub_sub_item_type, sub_sub_item_type_dictionary in sub_item_dictionary.items():
									# If the sub-sub-item type dictionary is not a boolean
									if type(sub_sub_item_type_dictionary) != bool:
										# If the sub-sub-item type dictionary is a list
										if type(sub_sub_item_type_dictionary) == list:
											# Create a dictionary of empty dictionaries using the list of sub-sub-item types as keys
											sub_sub_item_type_dictionary = {key: {} for key in sub_sub_item_type_dictionary}

										# If the sub-sub-item type is inside the defined list
										if sub_sub_item_type in ["Folders", "Files"]:
											# Iterate through the sub-sub-item names and dictionaries inside the sub-sub-item type dictionary
											# 
											# Sub-sub-item names list examples: [Social networks], [Texts], [Steps]
											for sub_sub_item_name, sub_sub_item_dictionary in sub_sub_item_type_dictionary.items():
												# Get the sub-sub-item dictionary
												sub_sub_item_dictionary = sub_sub_item_type_dictionary[sub_sub_item_name]

												# If the sub-sub-item dictionary is a list
												if type(sub_sub_item_dictionary) == list:
													# Create a dictionary of empty dictionaries using the list of sub-sub-items as keys
													sub_sub_item_dictionary = {key: {} for key in sub_sub_item_dictionary}

												# Define the folder sub-sub-item name and get the sub-sub-item dictionary back
												sub_sub_item_dictionary = self.Define_Folder_Item_Name(sub_sub_item_type, sub_sub_item_name, sub_sub_item_dictionary)

												# Update the root sub-item dictionary with the local one
												sub_sub_item_type_dictionary[sub_sub_item_name] = sub_sub_item_dictionary

									# Update the root sub-item dictionary with the local one
									sub_item_dictionary[sub_sub_item_type] = sub_sub_item_type_dictionary

								# Update the root sub-item dictionary with the local one
								sub_item_type_dictionary[sub_item_name] = sub_item_dictionary

							# Update the root sub-item type dictionary with the local one
							item_dictionary[sub_item_type] = sub_item_type_dictionary

					# Define the folder item name and get the item dictionary back
					item_dictionary = self.Define_Folder_Item_Name(item_type, item_name, item_dictionary)

					# Update the root item dictionary with the local one
					item_type_dicitionary[item_name] = item_dictionary

				# Update the root item type dictionary with the local one
				folder_item_dictionary[item_type] = item_type_dicitionary

			# Update the root folder item dictionary with the local one
			self.years["Folder items"]["Dictionary"][folder_item] = folder_item_dictionary

	def Define_Folder_Item_Name(self, item_type, item_name, item_dictionary):
		# Create the "Name" dictionary at the top of the item dictionary
		item_dictionary = {
			"Name": {},
			**item_dictionary
		}

		# Define the local list of small languages
		languages = self.languages["Small"]

		# If the item type is "User language files"
		if item_type == "User language files":
			# Define the local list of small languages to contain only the user language
			languages = [
				self.language["Small"]
			]

		# Iterate through the local list of small languages
		for language in languages:
			# If the item name is not "Language"
			if item_name != "Language":
				# Create the text key by converting the item name into lowercase and replacing spaces with underscores
				text_key = item_name.lower().replace(" ", "_")

				# Remove the parentheses from the text key
				text_key = text_key.replace("(", "")
				text_key = text_key.replace(")", "")

				# If the underscore character is not inside the text key
				if "_" not in text_key:
					# Add the ", title()" text
					text_key += ", title()"

				# Define the text as the item name
				text = item_name

				# If the text key is inside the language texts dictionary of the "Language" utility class
				if text_key in self.Language.texts:
					# Define the text as the text inside that dictionary and in the current language key
					text = self.Language.texts[text_key][language]

			# If the item name is "Language"
			if item_name == "Language":
				# Define the text as the full language
				text = self.languages["Full"][language]

			# Define the item name inside the "Name" dictionary as the text in the current language
			item_dictionary["Name"][language] = text

		# Return the item dictionary
		return item_dictionary

	def Create_Folder_Item(self, dictionary):
		# Create a shortcut to the key
		key = dictionary["Key"]

		# If the item type is "Folders"
		if dictionary["Item type"] == "Folders":
			# Define the folder with the folder name being the item name in the current language
			dictionary["Folders"][key] = {
				"root": dictionary["Folders"]["root"] + dictionary["Language item name"] + "/"
			}

			# Define the item as the root folder
			item = dictionary["Folders"][key]["root"]

			# Define the class to use as the "Folder" utility class
			Class = self.Folder

		# If the item type is "Files"
		if dictionary["Item type"] == "Files":
			# Define the file extension initially as "txt"
			file_extension = "txt"

			# If the "JSON" key is inside the dictionary and it is True
			if (
				"JSON" in dictionary and
				dictionary["JSON"] == True
			):
				# Change the file extension to "json"
				file_extension = "json"

			# Define the file with the file name being the item name in the current language and the file extension being the defined extension
			dictionary["Files"][key] = dictionary["Folders"]["root"] + dictionary["Language item name"] + "." + file_extension

			# Define the item as the file
			item = dictionary["Files"][key]

			# Define the class to use as the "File" utility class
			Class = self.File

		# Create the item using the "Create" method of the defined class
		Class.Create(item)

	def Create_Text_Folders(self, year):
		# Define the local folder items dictionary as the "Root" folder item dictionary
		folder_item_dictionary = self.years["Folder items"]["Dictionary"]["Root"]

		# Iterate through the item type keys and dictionaries inside the "Root" folder item dictionary
		# 
		# Item types: [Folders, Files]
		for item_type, item_type_dicitionary in folder_item_dictionary.items():
			# Iterate through the item names and dictionaries inside the item type dictionary
			# 
			# Item names (folders): [Christmas, Summary, New Year, Language]
			# Item names (files): [Created in, Edited in]
			for item_name, item_dictionary in item_type_dicitionary.items():
				# Define the local list of small languages as a list containing only the user language
				languages = [
					self.language["Small"]
				]

				# If the item name is "Language"
				if item_name == "Language":
					# Define the local list of small languages as the root one
					languages = self.languages["Small"]

				# Iterate through the local list of small languages
				for language in languages:
					# Define the language item name as the item name in the current language
					language_item_name = item_dictionary["Name"][language]

					# Define the key as the item name
					key = item_name

					# If the item name is "Language"
					if item_name == "Language":
						# Change the key to be the current language
						key = language

					# Define the dictionary to use in the "Create_Folder_Item" method
					dictionary = {
						"Item type": item_type,
						"Key": key,
						"Language item name": language_item_name,
						"Folders": year["Folders"]["Text"],
						"Files": year["Files"]["Text"]
					}

					# Create the folder item
					self.Create_Folder_Item(dictionary)

		# ---------- #

		# Define the local folder items dictionary as the "Language" folder item dictionary
		folder_item_dictionary = self.years["Folder items"]["Dictionary"]["Language"]

		# List the item types
		item_types = list(folder_item_dictionary.keys())

		# Remove the "User language files" item type
		item_types.remove("User language files")

		# Iterate through the list of item types inside the "Language" folder item dictionary
		# 
		# Item types: [Folders, Files]
		for item_type in item_types:
			# Get the item type dictionary
			item_type_dicitionary = folder_item_dictionary[item_type]

			# Iterate through the item names and dictionaries inside the item type dictionary
			# 
			# Item names (folders): [Completed tasks, Firsts of the year, Gaming sessions, Watched media]
			# Item names (files): [Welcome, Summary, This Year I, This Year I (post), This Year I (personal version), Goodbye]
			for item_name, item_dictionary in item_type_dicitionary.items():
				# Define the local list of languages as the list of keys inside the item "Name" dictionary
				languages = list(item_dictionary["Name"].keys())

				# Iterate through the local list of small languages
				for language in languages:
					# Define the language item name as the item name in the current language
					language_item_name = item_dictionary["Name"][language]

					# If the current language dictionary is not inside the files "Text" dictionary
					if language not in year["Files"]["Text"]:
						# Create the empty language dictionary
						year["Files"]["Text"][language] = {}

					# If the item name is not inside the "User language files" list
					# Or it is
					# And the current language is the user language
					# (This is to create the file only in the folder of the user language)
					if (
						item_name not in folder_item_dictionary["User language files"] or
						item_name in folder_item_dictionary["User language files"] and
						language == self.language["Small"]
					):
						# Define the dictionary to use in the "Create_Folder_Item" method
						dictionary = {
							"Item type": item_type,
							"Key": item_name,
							"Language item name": language_item_name,
							"Folders": year["Folders"]["Text"][language],
							"Files": year["Files"]["Text"][language]
						}

						# Create the folder item
						self.Create_Folder_Item(dictionary)

		# ---------- #

		# Define the local folder items dictionary as the "Christmas" folder item dictionary
		folder_item_dictionary = self.years["Folder items"]["Dictionary"]["Christmas"]

		# List the item types
		item_types = list(folder_item_dictionary.keys())

		# If the "Christmas" dictionary is not inside the files "Text" dictionary
		if "Christmas" not in year["Files"]["Text"]:
			# Create the empty "Christmas" dictionary
			year["Files"]["Text"]["Christmas"] = {}

		# Iterate through the item type keys and dictionaries inside the "Christmas" folder item dictionary
		# 
		# Item types: [Folders, Files]
		for item_type, item_type_dicitionary in folder_item_dictionary.items():
			# Iterate through the item names and dictionaries inside the item type dictionary
			# 
			# Item names (folders): [Merry Christmas]
			# Item names (files): [Watch, Eat]
			for item_name, item_dictionary in item_type_dicitionary.items():
				# Define the language item name as the item name in the user language
				language_item_name = item_dictionary["Name"][self.language["Small"]]

				# Define the dictionary to use in the "Create_Folder_Item" method
				dictionary = {
					"Item type": item_type,
					"Key": item_name,
					"Language item name": language_item_name,
					"Folders": year["Folders"]["Text"]["Christmas"],
					"Files": year["Files"]["Text"]["Christmas"]
				}

				# Create the folder item
				self.Create_Folder_Item(dictionary)

				# Iterate through the sub-item type keys and dictionaries inside the item dictionary
				# 
				# Sub-item type list example: [Folders, Files]
				for sub_item_type, sub_item_type_dictionary in item_dictionary.items():
					# If the sub-item type is inside the root list of item types
					# Item types: [Folders, Files]
					if sub_item_type in item_types:
						# If the [item name] dictionary is not inside the files Christmas "Text" dictionary
						if item_name not in year["Files"]["Text"]["Christmas"]:
							# Create the empty "[item name]" dictionary
							year["Files"]["Text"]["Christmas"][item_name] = {}

						# Iterate through the sub-item names and dictionaries inside the sub-item type dictionary
						# 
						# Sub-item names list examples: [Texts]
						for sub_item_name, sub_item_dictionary in sub_item_type_dictionary.items():
							# Define the language sub-item name as the sub-item name in the user language
							language_sub_item_name = sub_item_dictionary["Name"][self.language["Small"]]

							# Define the dictionary to use in the "Create_Folder_Item" method
							dictionary = {
								"Item type": sub_item_type,
								"Key": sub_item_name,
								"Language item name": language_sub_item_name,
								"Folders": year["Folders"]["Text"]["Christmas"][item_name],
								"Files": year["Files"]["Text"]["Christmas"][item_name]
							}

							# Create the folder item
							self.Create_Folder_Item(dictionary)

		# ---------- #

		# Iterate through the social network names and dictionaries inside the "Summary" social networks dictionary
		for social_network_name, social_network in self.social_networks["Dictionary"]["Summary"]["Dictionary"].items():
			# If the "Summary" dictionary is not inside the files "Text" dictionary
			if "Summary" not in year["Files"]["Text"]:
				# Create the empty "Summary" dictionary
				year["Files"]["Text"]["Summary"] = {}

			# Define the language item name as the social network name in the user language
			language_item_name = social_network["Name"][self.language["Small"]]

			# Define the dictionary to use in the "Create_Folder_Item" method
			dictionary = {
				"Item type": "Files",
				"Key": social_network_name,
				"Language item name": language_item_name,
				"Folders": year["Folders"]["Text"]["Summary"],
				"Files": year["Files"]["Text"]["Summary"]
			}

			# Create the folder item
			self.Create_Folder_Item(dictionary)

		# ---------- #

		# Define the local folder items dictionary as the "New Year" folder item dictionary
		folder_item_dictionary = self.years["Folder items"]["Dictionary"]["New Year"]

		# List the item types
		item_types = list(folder_item_dictionary.keys())

		# If the "New Year" dictionary is not inside the files "Text" dictionary
		if "New Year" not in year["Files"]["Text"]:
			# Create the empty "New Year" dictionary
			year["Files"]["Text"]["New Year"] = {}

		# Iterate through the item type keys and dictionaries inside the "New Year" folder item dictionary
		# 
		# Item types: [Folders, Files]
		for item_type, item_type_dicitionary in folder_item_dictionary.items():
			# Iterate through the item names and dictionaries inside the item type dictionary
			# 
			# Item names (folders): [Social networks]
			# Item names (files): [Texts]
			for item_name, item_dictionary in item_type_dicitionary.items():
				# Define the language item name as the item name in the user language
				language_item_name = item_dictionary["Name"][self.language["Small"]]

				# Define the dictionary to use in the "Create_Folder_Item" method
				dictionary = {
					"Item type": item_type,
					"Key": item_name,
					"Language item name": language_item_name,
					"Folders": year["Folders"]["Text"]["New Year"],
					"Files": year["Files"]["Text"]["New Year"]
				}

				# Create the folder item
				self.Create_Folder_Item(dictionary)

				# If the [item name] dictionary is not inside the files New Year "Text" dictionary
				if item_name not in year["Files"]["Text"]["New Year"]:
					# Create the empty "[item name]" dictionary
					year["Files"]["Text"]["New Year"][item_name] = {}

		# Iterate through the social network names and dictionaries inside the "New Year" social networks dictionary
		for social_network_name, social_network in self.social_networks["Dictionary"]["New Year"]["Dictionary"].items():
			# Define the language item name as the social network name in the user language
			language_item_name = social_network["Name"][self.language["Small"]]

			# Define the dictionary to use in the "Create_Folder_Item" method
			dictionary = {
				"Item type": "Files",
				"Key": social_network_name,
				"Language item name": language_item_name,
				"Folders": year["Folders"]["Text"]["New Year"]["Social networks"],
				"Files": year["Files"]["Text"]["New Year"]["Social networks"]
			}

			# Create the folder item
			self.Create_Folder_Item(dictionary)

		# ---------- #

		# If the year "Number" is "Texts"
		if year["Number"] == "Texts":
			# Define the local folder items dictionary as the "Christmas" folder item dictionary inside the "Texts" folder item dictionary
			folder_item_dictionary = self.years["Folder items"]["Dictionary"]["Texts"]["Folders"]["Christmas"]

			# List the item types
			item_types = list(folder_item_dictionary.keys())

			# Remove the "Name" item type
			item_types.remove("Name")

			# Iterate through the item types inside the defined folder item dictionary
			# 
			# Item types: [Folders, Files]
			for item_type in item_types:
				# Get the item type dictionary
				item_type_dicitionary = folder_item_dictionary[item_type]

				# Iterate through the item names and dictionaries inside the item type dictionary
				# 
				# Item names (folders): [Social networks]
				# Item names (files): [Texts]
				for item_name, item_dictionary in item_type_dicitionary.items():
					# Define the language item name as the item name in the user language
					language_item_name = item_dictionary["Name"][self.language["Small"]]

					# Define the "json" variable as False
					json = False

					# If the "JSON" key is inside the item dictionary
					# And it is True
					if (
						"JSON" in item_dictionary and
						item_dictionary["JSON"] == True
					):
						# Update the "json" variable to True
						json = True

						# Update the language item name to be the item name
						language_item_name = item_name

					# Define the dictionary to use in the "Create_Folder_Item" method
					dictionary = {
						"Item type": item_type,
						"Key": item_name,
						"Language item name": language_item_name,
						"Folders": year["Folders"]["Text"]["Christmas"],
						"Files": year["Files"]["Text"]["Christmas"],
						"JSON": json
					}

					# Create the folder item
					self.Create_Folder_Item(dictionary)

					# Iterate through the sub-item type keys and dictionaries inside the item dictionary
					# 
					# Sub-item type list: [Folders]
					for sub_item_type, sub_item_type_dictionary in item_dictionary.items():
						# If the sub-item type is inside the root list of item types
						# Item types: [Folders, Files]
						if sub_item_type in item_types:
							# If the [item name] dictionary is not inside the files Christmas "Text" dictionary
							if item_name not in year["Files"]["Text"]["Christmas"]:
								# Create the empty "[item name]" dictionary
								year["Files"]["Text"]["Christmas"][item_name] = {}

							# Iterate through the sub-item names and dictionaries inside the sub-item type dictionary
							# 
							# Sub-item names list examples: [Texts]
							for sub_item_name, sub_item_dictionary in sub_item_type_dictionary.items():
								# If the [sub-item name] dictionary is not inside the files Christmas [item name] "Text" dictionary
								if sub_item_name not in year["Files"]["Text"]["Christmas"][item_name]:
									# Create the empty "[item name]" dictionary
									year["Files"]["Text"]["Christmas"][item_name][sub_item_name] = {}

								# Define the language sub-item name as the sub-item name in the user language
								language_sub_item_name = sub_item_dictionary["Name"][self.language["Small"]]

								# Define the dictionary to use in the "Create_Folder_Item" method
								dictionary = {
									"Item type": sub_item_type,
									"Key": sub_item_name,
									"Language item name": language_sub_item_name,
									"Folders": year["Folders"]["Text"]["Christmas"][item_name],
									"Files": year["Files"]["Text"]["Christmas"][item_name]
								}

								# Create the folder item
								self.Create_Folder_Item(dictionary)

			# ---------- #

			# Iterate through the social network names and dictionaries inside the "Merry Christmas" social networks dictionary
			for social_network_name, social_network in self.social_networks["Dictionary"]["Merry Christmas"]["Dictionary"].items():
				# Define the language item name as the social network name in the user language
				language_item_name = social_network["Name"][self.language["Small"]]

				# Define the dictionary to use in the "Create_Folder_Item" method
				dictionary = {
					"Item type": "Files",
					"Key": social_network_name,
					"Language item name": language_item_name,
					"Folders": year["Folders"]["Text"]["Christmas"]["Merry Christmas"]["Social networks"],
					"Files": year["Files"]["Text"]["Christmas"]["Merry Christmas"]["Social networks"]
				}

				# Create the folder item
				self.Create_Folder_Item(dictionary)

			# Add the "Social networks" key to the start of the "Merry Christmas" dictionary
			year["Files"]["Text"]["Christmas"]["Merry Christmas"] = {
				"Social networks": year["Files"]["Text"]["Christmas"]["Merry Christmas"]["Social networks"],
				**year["Files"]["Text"]["Christmas"]["Merry Christmas"]
			}

		# ---------- #

		# Define a list of keys to add at the end of the dictionary
		keys = [
			"Created in",
			"Edited in"
		]

		# Add the keys above to the end of the year files "Text" dictionary
		year["Files"]["Text"] = self.JSON.Add_To_End_Of_Dictionary(year["Files"]["Text"], to_add = keys)

		# ---------- #

		# Return the local year dictionary
		return year

	def Create_Image_Folders(self, year):
		# Define the dictionary of image folder names
		folder_names = {
			"Christmas": "",
			"Memories": "",
			"Story": "Key",
			"Summary": "",
			"New Year": ""
		}

		# Define the local folders dictionary as the root year folders dictionary
		folders = year["Folders"]

		# If the "Image" key is inside the local folders dictionary
		if "Image" in folders:
			# Change the local folders dictionary to that dictionary
			folders = folders["Image"]

		# Iterate through the folder keys and names
		for key, folder_name in folder_names.items():
			# If the folder name is empty
			if folder_name == "":
				# Create the text key by converting the key into lowercase and replacing spaces with underscores
				text_key = key.lower().replace(" ", "_")

				# If the underscore character is not inside the text key
				if "_" not in text_key:
					# Add the ", title()" text
					text_key += ", title()"

				# Get the folder name in the user language
				folder_name = self.Language.language_texts[text_key]

			# If the folder name is "Key"
			if folder_name == "Key":
				# Then use the key as the folder name
				folder_name = key

			# Define the folder inside the local folders dictionary
			folders[key] = {
				"root": folders["root"] + folder_name + "/"
			}

			# Create the folder
			self.Folder.Create(folders[key]["root"])

		# Define the "Dates.txt" file inside the "Memories" folder
		folders["Memories"]["Dates"] = folders["Memories"]["root"] + "Dates.txt"

		# Create the file
		self.File.Create(folders["Memories"]["Dates"])

		# ---------- #

		# Define the "Christmas" image folders

		# Define the list of image folder names
		folder_names = [
			"Screenshots",
			"Pictures"
		]

		# Iterate through the list of folder names
		for folder_name in folder_names:
			# Define the key as the folder name
			key = folder_name

			# Create the text key by converting the key into lowercase and replacing spaces with underscores
			text_key = key.lower().replace(" ", "_")

			# If the underscore character is not inside the text key
			if "_" not in text_key:
				# Add the ", title()" text
				text_key += ", title()"

			# Get the folder name in the user language
			folder_name = self.Language.language_texts[text_key]

			# Define the folder inside the local "Christmas" folders dictionary
			folders["Christmas"][key] = {
				"root": folders["Christmas"]["root"] + folder_name + "/"
			}

			# Create the folder
			self.Folder.Create(folders["Christmas"][key]["root"])

		# Return the year dictionary
		return year

	def Select_Year(self, years = None, select_text = None):
		# If the years parameter is None
		if years == None:
			# Define the local years as the root list of years
			years = self.years["List"]

		# Define the show text as the "Years" text in the user language
		show_text = self.Date.language_texts["years, title()"]

		# If the "select text" parameter is None
		if select_text == None:
			# Define the select text as the "Select a year" text in the user language
			select_text = self.language_texts["select_a_year"]

		# Ask the user to select a year from the list of years
		year = self.Input.Select(years, show_text = show_text, select_text = select_text)["Option"]["Original"]

		# Get the year dictionary 
		self.year = self.years["Dictionary"][year]

		# Return it
		return self.year

	def Define_Format_Strings(self):
		# Define the root "Format strings" dictionary with the format strings and their values
		self.years["Format strings"] = {
			"Current year": {
				# The list of texts to replace with the current year number
				"List": [
					"{current_year}",
					"[" + self.Language.language_texts["current_year"] + "]"
				],
		
				# The year number
				"Value": str(self.date["Units"]["Year"])
			},
			"Next year": {
				# The list of texts to replace with the next year number
				"List": [
					"{next_year}",
					"[" + self.Language.language_texts["next_year"] + "]"
				],

				# The next year number
				"Value": str(self.date["Units"]["Year"] + 1)
			}
		}

	def Replace_Year_Format_Strings(self, text):
		# Iterate through the string dictionaries inside the root "Format strings" dictionary
		# 
		# Current year: "{current_year}", "[Current year]"
		# Next year: "{next_year}", "[Next year]"
		for strings in self.years["Format strings"].values():
			# Iterate through the list of strings to search for
			for string in strings["List"]:
				# If the string is inside the text
				if string in text:
					# Replace the string with the value on the text
					# Example: "{current_year}" and "[Current year]" would both become "2025"
					text = text.replace(string, strings["Value"])

		# Return the text
		return text
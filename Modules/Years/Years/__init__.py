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

		# Define the "Folder item names" dictionary
		self.Define_Folder_Item_Names_Dictionary()

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
			# Replace the dashes with underlines
			separator = separators_copy[key].replace("-", "_")

			# Update the separator inside the root list
			separators_copy[key] = separator

		# Add the underline separators to the original separators dictionary
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

		# Update the number of websites
		self.years["Summary"]["Websites"]["Numbers"]["Total"] = len(list(self.years["Summary"]["Websites"]["Dictionary"].keys()))

	def Define_Folder_Item_Names_Dictionary(self):
		# Define the root "Folder item names" dictionary
		self.years["Folder item names"] = {
			"Root": {
				"Folders": [
					"Christmas",
					"Summary",
					"New Year"
					# Language folders
				],
				"Files": [
					"Created in",
					"Edited in"
				]
			},
			"Language": {
				"Folders": [
					"Completed tasks",
					"Firsts of the Year",
					"Gaming sessions",
					"Watched media"
				],
				"Files": [
					"Welcome",
					"Summary",
					"This Year I",
					"This Year I (post)",
					"This Year I (personal version)",
					"Goodbye"
				],
				"User language files": [
					"Yearly statistics",
					"FutureMe"
				]
			},
			"Christmas": {
				"Folders": [
					"Planning",
					"Merry Christmas"
				],
				"Files": [
					"Texts"
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
			"Additional items": {
				"Christmas": {
					"Planning": {
						"Files": [
							"Watch",
							"Eat"
						]
					},
					"Merry Christmas": {
						"Files": [
							"Texts"
						]
					}
				}
			},
			"Texts": {
				"Christmas": {
					"Planning": {
						"Files": [
							"Objects"
							# Full language files
						],
						"JSON": [
							"Objects"
						]
					},
					"Merry Christmas": {
						"Folders": [
							"Social networks"
						],
						"Files": [
							"Texts"
						]
					}
				},
				"New Year": {
					"Files": [
						"Planning",
						"Texts"
					]
				}
			},
			"Social networks": {
				"New Year": [
					
				]
			}
		}

		# Define the list of keys to use as the list of keys of the "folder item names" dictionary
		keys = list(self.years["Folder item names"].keys())

		# Define the keys to remove
		to_remove = [
			"Additional items",
			"Texts",
			"Social networks"
		]

		# Remove the keys
		for key in to_remove:
			keys.remove(key)

		# Iterate through the list of keys
		# keys = ["Root", "Language", "Christmas", "New Year"]
		for folder_key in keys:
			# Get the item types list
			item_types = self.years["Folder item names"][folder_key]

			# Iterate through the list of item types
			# item_types = ["Folders", "Files"]
			for item_type in item_types:
				# Transform the names list into a dictionary
				dictionary = {
					"List": item_types[item_type],
					"Dictionary": {}
				}

				# Iterate through the items inside the list
				for item_name in dictionary["List"]:
					# Define the item as a dictionary inside the local dictionary
					dictionary["Dictionary"][item_name] = {}

					# Define the list of small languages
					languages = self.languages["Small"]

					# If the item type is "User language files"
					if item_type == "User language files":
						# Define the list of small languages as just the user language
						languages = [
							self.language["Small"]
						]

					# Iterate through the list of small languages
					for language in languages:
						# Replace spaces with underscores and lowercase the item name to make the text key
						text_key = item_name.lower().replace(" ", "_")

						# Remove the parenthesis from the text key
						text_key = text_key.replace("(", "")
						text_key = text_key.replace(")", "")

						# If the underline is not inside the text key
						if "_" not in text_key:
							# Add the ", title()" text
							text_key += ", title()"

						# If the text key is inside the language texts dictionary of the "Language" class
						if text_key in self.Language.texts:
							# Define the text
							text = self.Language.texts[text_key][language]

						# Else, use the own item name
						else:
							text = item_name

						# Define the folder or file name in the current language as the text
						dictionary["Dictionary"][item_name][language] = text

				# Update the root folder item names dictionary to add the local dictionary
				self.years["Folder item names"][folder_key][item_type] = dictionary

		# Iterate through the "Additional items" dictionary
		# Example:
		# folder: "Christmas"
		for key, folder in self.years["Folder item names"]["Additional items"].items():
			# Example:
			# sub_folder: "Planning"
			for sub_folder in folder:
				# Transform the names list into a dictionary
				dictionary = {
					"List": folder[sub_folder]["Files"],
					"Dictionary": {}
				}

				# Iterate through the items inside the list
				for item_name in dictionary["List"]:
					# Define the item as a dictionary inside the local dictionary
					dictionary["Dictionary"][item_name] = {}

					# Iterate through the list of small languages
					for language in self.languages["Small"]:
						# Replace spaces with underscores and lowercase the item name to make the text key
						text_key = item_name.lower().replace(" ", "_")

						# If the underline is not inside the text key
						if "_" not in text_key:
							# Add the ", title()" text
							text_key += ", title()"

						# Define the folder or file name in the current language as the text
						dictionary["Dictionary"][item_name][language] = self.Language.texts[text_key][language]

				# Example:
				# key: "Christmas", sub_folder: "Planning"
				self.years["Folder item names"]["Additional items"][key][sub_folder]["Files"] = dictionary

		# Iterate through the "Texts" dictionary
		# Example:
		# folder: "Christmas"
		for key, items in self.years["Folder item names"]["Texts"].items():
			# If the key is "Christmas"
			if key == "Christmas":
				# Define the list of sub-folders as the copy of the items dictionary
				sub_folders = items.copy()

				# Example:
				# sub_folder: "Planning"
				for sub_folder, item_types in sub_folders.items():
					# Iterate through the list of item types
					# item_types = ["Folders", "Files"]
					for item_type in item_types:
						# Define the items as the item type of the sub-folders
						# Example:
						# sub_folder: "Planning", item_type: "Folders"
						items = sub_folders[sub_folder][item_type]

						# Transform the names list into a dictionary
						dictionary = {
							"List": items,
							"Dictionary": {}
						}

						# Iterate through the item names in the list
						# Example:
						# item_name: "Objects"
						for item_name in dictionary["List"].copy():
							# Define the empty item name dictionary
							dictionary["Dictionary"][item_name] = {}

							# Iterate through list of small languages
							for language in self.languages["Small"]:
								# Get the text key by converting the item name into lowercase and replace spaces with underlines
								text_key = item_name.lower().replace(" ", "_")

								# If the underline is not inside the text key
								if "_" not in text_key:
									# Add the ", title()" text
									text_key += ", title()"

								# Define the item name in the current language as the text in the current language
								dictionary["Dictionary"][item_name][language] = self.Language.texts[text_key][language]

							# Define the local folder dictionary
							# Example:
							# key: "Christmas", sub_folder: "Planning"
							folder_dictionary = self.years["Folder item names"]["Texts"][key][sub_folder]

							# Define the item type key as the local dictionary
							# Example:
							# item_type: "Files"
							folder_dictionary[item_type] = dictionary

			# If the key is "New Year"
			if key == "New Year":
				# Iterate through the list of item types
				# item_types = ["Folders", "Files"]
				for item_type, sub_items in items.items():
					# Transform the items list into a dictionary
					dictionary = {
						"List": sub_items,
						"Dictionary": {}
					}

					# Iterate through the item names in the list
					# Example:
					# item_name: "Objects"
					for item_name in dictionary["List"].copy():
						# Define the empty dictionary
						dictionary["Dictionary"][item_name] = {}

						# Iterate through list of small languages
						for language in self.languages["Small"]:
							# Get the text key by converting the item name into lowercase and replace spaces with underlines
							text_key = item_name.lower().replace(" ", "_")

							# If the underline is not inside the text key
							if "_" not in text_key:
								# Add the ", title()" text
								text_key += ", title()"

							# Define the item name in the current language as the text in the current language
							dictionary["Dictionary"][item_name][language] = self.Language.texts[text_key][language]

						# Define the local folder dictionary
						# Example:
						# key: "New Year"
						folder_dictionary = self.years["Folder item names"]["Texts"][key]

						# Define the item type key as the local dictionary
						# Example:
						# item_type: "Files"
						folder_dictionary[item_type] = dictionary

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
				# Define the root folder
				folder = self.years["Folders"][folder_type]["root"] + year_number + "/"

				# Create the local folders dictionary
				folders = {
					"root": folder
				}

				# Create the root year folder
				self.Folder.Create(folders["root"])

				# ----- #

				# Define the folder type inside the "Files" dictionary
				year["Files"][folder_type] = {}

				# If the folder type is "Text"
				# Then create the year text folders and files
				if folder_type == "Text":
					# Define the local data dictionary
					# With the year number, the folders dictionary, the year dictionary, and the folder type as the current one in the loop
					data = {
						"Year": year_number,
						"Folders": folders,
						"Dictionary": year,
						"Folder type": folder_type
					}

					# Create the folders of the year
					data = self.Create_Year_Folders(data)

					# Update the root year "Folders" dictionary with the one inside the data dictionary
					folders = data["Folders"]

					# Update the local year dictionary with the one inside the data dictionary
					year = data["Dictionary"]

				# ----- #

				# If the folder type is "Image"
				# Then create the year image folders and files
				if folder_type == "Image":
					# Create image folders of the year "Images" folder
					folders = self.Create_Image_Folders(folders)

					# --- #

					# Define the "Christmas" image folders

					# Define the image folder names dictionary
					folder_names = {
						"Screenshots": "",
						"Pictures": ""
					}

					# Iterate through the folder names
					for key, folder_name in folder_names.items():
						# If the folder name is empty
						if folder_name == "":
							# Replace spaces with underscores and lowercase the key to make the text key
							text_key = key.lower().replace(" ", "_")

							# If the underline is not inside the text key
							if "_" not in text_key:
								# Add the ", title()" text
								text_key += ", title()"

							# Get the folder name
							folder_name = self.Language.language_texts[text_key]

						# Define the folder inside the local folders dictionary
						folders["Christmas"][key] = {
							"root": folders["Christmas"]["root"] + folder_name + "/"
						}

						# Create the folder
						self.Folder.Create(folders["Christmas"][key]["root"])

					# Define the "Dates.txt" file inside the "Memories" folder
					year["Files"][folder_type]["Memories"] = {
						"Dates": folders["Memories"]["root"] + "Dates.txt"
					}

					self.File.Create(year["Files"][folder_type]["Memories"]["Dates"])

				# Add the local folders dictionary to the local year dictionary
				year["Folders"][folder_type] = folders

			# Add the keys of the "Text" folders dictionary to the root year "Folders" dictionary
			year["Folders"].update(year["Folders"]["Text"])

			# If the "Text" key is inside the year "Files" dictionary
			if "Text" in year["Files"]:
				# Add the keys of the "Text" files dictionary to the root year "Files" dictionary
				year["Files"].update(year["Files"]["Text"])

			# Add the local year dictionary to the root years "Dictionary"
			self.years["Dictionary"][year_number] = year

		# Define the "Current year" key as the current year dictionary which is inside the root "Years" dictionary
		self.years["Current year"] = self.years["Dictionary"][self.current_year_number]

		# Update the total number of years
		self.years["Numbers"]["Total"] = len(self.years["List"])

		# ---------- #

		# Define the root "Texts" dictionary
		texts = {
			"Name": "Texts",
			"Folders": {
				"Text": {}
			},
			"Files": {
				"Text": {}
			}
		}

		# Create the local "Texts" folders dictionary
		folders = {
			"root": self.years["Folders"]["Text"]["Texts"]["root"]
		}

		self.Folder.Create(folders["root"])

		# Define the local data dictionary
		# With the year as 2018, the folders dictionary, the "Texts" dictionary, and the folder type as "Text"
		data = {
			"Year": "2018",
			"Folders": folders,
			"Dictionary": texts,
			"Folder type": "Text"
		}

		# Define the folders of the "Texts" dictionary
		data = self.Create_Year_Folders(data)

		# Update the root texts "Folders" dictionary with the one inside the data dictionary
		texts["Folders"] = data["Folders"]

		# Update the root texts "Files" dictionary with the one inside the data dictionary
		texts["Files"] = data["Dictionary"]["Files"]["Text"]

		# Define the root "Texts" dictionary as the local one
		self.years["Texts"] = texts

		# ---------- #

		# Create the local "Images" folders dictionary
		folders = {
			"root": self.years["Folders"]["Image"]["root"] + self.Language.language_texts["images, title()"] + "/"
		}

		# Create image folders of the "Images" folder
		folders = self.Create_Image_Folders(folders)

		# Define the "Images" folders dictionary as the local images folders dictionary
		self.years["Folders"]["Image"]["Images"] = folders

		# ---------- #

		# Make a local copy of the root "Years" dictionary
		dictionary = deepcopy(self.years)

		# Define the keys to remove
		to_remove = [
			"Folders",
			"Summary",
			"Folder item names",
			"Author",
			"States"
		]

		# Remove the keys
		for key in to_remove:
			dictionary.pop(key)

		# Iterate through the year numbers and dictionaries inside the root "Years" dictionary
		for year_number, year in self.years["Dictionary"].items():
			# Create a copy of the year dictionary
			year = deepcopy(year)

			# Remove the "Folders" key
			year.pop("Folders")

			# If the "Text" key is inside the year "Files" dictionary
			if "Text" in year["Files"]:
				# Remove the "Text" key
				year["Files"].pop("Text")

			# Update the year dictionary inside the local "Years" dictionary
			dictionary["Dictionary"][year_number] = year

		# Remove the "Folders" key of the "Current year" dictionary
		dictionary["Current year"].pop("Folders")

		# Remove the "Text" key of the current year "Files" dictionary
		dictionary["Current year"]["Files"].pop("Text")

		# Remove the "Folders" keys of the "Texts" dictionary
		dictionary["Texts"].pop("Folders")

		# Write the local updated "Years" dictionary to the "Years.json" file
		self.JSON.Edit(self.years["Folders"]["Text"]["Years"], dictionary)

	def Create_Year_Folders(self, data):
		# Define the folder type key inside the "Files" dictionary
		data["Dictionary"]["Files"][data["Folder type"]] = {}

		# Define the folder keys with the keys inside the defined list
		for item in ["Christmas", "New Year"]:
			data["Dictionary"]["Files"][data["Folder type"]][item] = {}

		# Iterate through list of small languages to define the language folder keys
		for language in self.languages["Small"]:
			data["Dictionary"]["Files"][data["Folder type"]][language] = {}

		# Create the language text folders

		# Iterate through the language keys and dictionaries
		for small_language, language in self.languages["Dictionary"].items():
			# Define the folder with the full language
			data["Folders"][small_language] = {
				"root": data["Folders"]["root"] + language["Full"] + "/"
			}

			# Create it
			self.Folder.Create(data["Folders"][small_language]["root"])

		# Create the root text folders and files
		for item_type in ["Folders", "Files", "User language files"]:
			# folders = ["Christmas", "Summary", "New Year"]
			# files = ["Created in", "Edited in"]

			# If the current item type is inside the dictionary of root names
			if item_type in self.years["Folder item names"]["Root"]:
				for key, folder_item in self.years["Folder item names"]["Root"][item_type]["Dictionary"].items():
					# Define the folder
					data["Folders"][key] = {
						"root": data["Folders"]["root"] + folder_item[self.language["Small"]] + "/"
					}

					# Define the folder item as the root folder
					item = data["Folders"][key]["root"]

					# Define the class as "self.Folder"
					Class = self.Folder

					if item_type in ["Files", "User language files"]:
						# Define the file
						data["Folders"][key] = data["Folders"]["root"] + folder_item[self.language["Small"]] + ".txt"

						# Define the class as "self.File"
						Class = self.File

						# Define the folder item as the file
						item = data["Folders"][key]

					# Create it
					Class.Create(item)

					if item_type in ["Files", "User language files"]:
						# Add it to the "Files" dictionary
						data["Dictionary"]["Files"][data["Folder type"]][key] = data["Folders"][key]

			# folders = ["Done tasks", "Firsts of the Year", "Gaming sessions", "Watched media"]
			# files = ["Welcome", "This Year I", "This Year I (post)", "This Year I (personal version)", "Summary", "Goodbye"]
			# user_language_files = ["Yearly statistics", "FutureMe"]
			keys = list(self.years["Folder item names"]["Language"][item_type]["Dictionary"].keys())

			# If the "Name" is inside the data dictionary
			# And the dictionary name is "Texts"
			# And the item type is inside the list of ["Files", "User language files"]
			# files = ["This Year I (post)"]
			if (
				"Name" in data["Dictionary"] and
				data["Dictionary"]["Name"] == "Texts" and
				item_type == "Files"
			):
				# Define the list of keys as only the "This Year I (post)" key
				keys = [
					"This Year I (post)"
				]

			# Iterate through list of small languages
			for language in self.languages["Small"]:
				data["Dictionary"]["Files"][data["Folder type"]][language]

				# Create the language folder text folders
				for key in keys:
					# Get the folder item in the language dictionary of the current item type
					folder_item = self.years["Folder item names"]["Language"][item_type]["Dictionary"][key]

					# If the language key exists inside the data local dictionary
					# And also inside the folder item dictionary
					if (
						language in data["Folders"] and
						language in folder_item
					):
						# Define the folder
						data["Folders"][language][key] = {
							"root": data["Folders"][language]["root"] + folder_item[language] + "/"
						}

						# Define the folder item as the root folder
						item = data["Folders"][language][key]["root"]

						if item_type in ["Files", "User language files"]:
							# Define the file
							data["Folders"][language][key] = data["Folders"][language]["root"] + folder_item[language] + ".txt"

							# Define the class as "self.File"
							Class = self.File

							# Define the folder item as the file
							item = data["Folders"][language][key]

						# Create it
						Class.Create(item)

						if item_type in ["Files", "User language files"]:
							# Add it to the "Files" dictionary
							data["Dictionary"]["Files"][data["Folder type"]][language][key] = data["Folders"][language][key]

		# ---------- #

		# Create the "Christmas" folders

		# Iterate through the "Christmas" files dictionary
		# keys = ["Planning", "Merry Christmas"]
		for key, folder in self.years["Folder item names"]["Christmas"]["Folders"]["Dictionary"].items():
			data["Folders"]["Christmas"][key] = {
				"root": data["Folders"]["Christmas"]["root"] + folder[self.language["Small"]] + "/"
			}

			self.Folder.Create(data["Folders"]["Christmas"][key]["root"])

			data["Dictionary"]["Files"][data["Folder type"]]["Christmas"][key] = {}

		# ---------- #

		# If the year is not the current year
		# Or it is the current year
		# And its year folder exists
		if (
			data["Year"] != self.current_year_number or
			data["Year"] == self.current_year_number and
			self.years["States"]["Current year folder exists"] == True
		):
			# Define the local Christmas "Merry Christmas" folder and dictionary
			folder = data["Folders"]["Christmas"]["Merry Christmas"]

			dictionary = deepcopy(self.years["Folder item names"]["Christmas"]["Files"]["Dictionary"])

			# Iterate through the "Merry Christmas" files dictionary
			# keys = ["Texts"]
			for key, file in dictionary.items():
				# Define the file
				folder[key] = folder["root"] + file[self.language["Small"]] + ".txt"

				# Create it
				self.File.Create(folder[key])

				# And add it to the "Files" dictionary
				data["Dictionary"]["Files"][data["Folder type"]]["Christmas"]["Merry Christmas"][key] = folder[key]

		# ---------- #

		# Define the list of files to create
		social_networks_list = [
			"Discord",
			"Instagram {} Facebook",
			"Twitter",
			"Bluesky {} Threads",
			"Wattpad",
			"WhatsApp"
		]

		# If the "Name" is inside the data dictionary
		# And the dictionary name is "Texts"
		if (
			"Name" in data["Dictionary"] and
			data["Dictionary"]["Name"] == "Texts"
		):
			# Define the local Christmas "Planning" folder and dictionary
			folder = data["Folders"]["Christmas"]["Planning"]

			dictionary = self.years["Folder item names"]["Texts"]["Christmas"]["Planning"]

			# Create the Christmas "Planning" files
			# Iterate through the files dictionary
			# keys = ["Objects", self.languages["Full"].values()]
			for key, file in dictionary["Files"]["Dictionary"].items():
				# Define the root folder
				folder[key] = folder["root"]

				# Define the file name and extension
				# (Language file name and "txt")
				file_name = file[self.language["Small"]]

				extension = "txt"

				# If the file is a JSON file
				if key in dictionary["JSON"]["List"]:
					# Update the file name to the English file name
					file_name = file["en"]

					# And define the extension as "JSON"
					extension = "json"

				# Add the file name and extension to the file dictionary
				folder[key] += file_name + "." + extension

				# Create the file
				self.File.Create(folder[key])

				# And add it to the "Files" dictionary
				data["Dictionary"]["Files"][data["Folder type"]]["Christmas"]["Planning"][key] = folder[key]

			# ---------- #

			# Define the local Christmas "Merry Christmas" folder and dictionary
			folder = data["Folders"]["Christmas"]["Merry Christmas"]

			dictionary = self.years["Folder item names"]["Texts"]["Christmas"]["Merry Christmas"]

			# Create the Christmas "Merry Christmas" folders
			# Iterate through the folders dictionary
			# keys = ["Social networks"]
			for key, folder_name in dictionary["Folders"]["Dictionary"].items():
				# Define the root folder
				folder[key] = {
					"root": folder["root"] + folder_name[self.language["Small"]] + "/"
				}

				# Create the folder
				self.Folder.Create(folder[key]["root"])

			# Create the Christmas "Merry Christmas" social networks files
			for file_name in social_networks_list:
				# Define the file key as the file name
				key = file_name

				# If the "{}" format string is present inside the key
				if "{}" in key:
					# Format the key with the "and" text
					key = key.format("and")

					# Format the file name with the "and" text in the user language
					file_name = file_name.format(self.Language.language_texts["and"])

				# Define the file
				folder["Social networks"][key] = folder["Social networks"]["root"] + file_name + ".txt"

				# Create the file
				self.File.Create(folder["Social networks"][key])

		# ---------- #

		# Define the local "New Year" folder and dictionary
		folder = data["Folders"]["New Year"]

		dictionary = self.years["Folder item names"]["New Year"]

		# Create the New Year "Social networks" file
		# Iterate through the files dictionary
		for key, folder_name in dictionary["Folders"]["Dictionary"].items():
			# Define the root folder
			folder[key] = {
				"root": folder["root"] + folder_name[self.language["Small"]] + "/"
			}

			# Create it
			self.Folder.Create(folder[key]["root"])

			# And add it to the "Files" dictionary
			data["Dictionary"]["Files"][data["Folder type"]]["New Year"][key] = {}

			# Define and create the social network files
			for social_network_name in social_networks_list:
				# Define the sub key as the social network name
				sub_key = social_network_name

				# If the "{}" format string is present inside the sub-key
				if "{}" in sub_key:
					# Format the sub-key with the "and" text
					sub_key = sub_key.format("and")

					# Format the social network name with the "and" text in the user language
					social_network_name = social_network_name.format(self.Language.language_texts["and"])

				# Define the file with the root folder and the social network name
				folder[key][sub_key] = folder[key]["root"] + social_network_name + ".txt"

				# Create it
				self.File.Create(folder[key][sub_key])

				# And add it to the Files "Social networks" dictionary
				data["Dictionary"]["Files"][data["Folder type"]]["New Year"][key][sub_key] = folder[key][sub_key]

		# Create the New Year "Texts" file
		# Iterate through the files dictionary
		for key, file in dictionary["Files"]["Dictionary"].items():
			# Define the file
			folder[key] = folder["root"] + file[self.language["Small"]] + ".txt"

			# Create it
			self.File.Create(folder[key])

			# And add it to the "Files" dictionary
			data["Dictionary"]["Files"][data["Folder type"]]["New Year"][key] = folder[key]

		# ---------- #

		# If the year is not the current year
		# Or it is the current year
		# And its year folder exists
		if (
			data["Year"] != self.current_year_number or
			data["Year"] == self.current_year_number and
			self.years["States"]["Current year folder exists"] == True
		):
			# Create the "Christmas" additional items
			for folder_key in self.years["Folder item names"]["Additional items"]["Christmas"]:
				# Get the list of files to create
				# Example:
				# folder_key: "Planning"
				files = self.years["Folder item names"]["Additional items"]["Christmas"][folder_key]["Files"]

				# Define the folder dictionary
				folder = data["Folders"]["Christmas"][folder_key]

				# Define the keys list
				keys = list(files["Dictionary"].keys())

				# If the "Name" is inside the data dictionary
				# And the dictionary name is "Texts"
				if (
					"Name" in data["Dictionary"] and
					data["Dictionary"]["Name"] == "Texts"
				):
					# Remove the "Watch" and "Eat" from the list of keys if they exist
					for key in ["Watch", "Eat"]:
						if key in keys:
							keys.remove(key)

				# Iterate through the keys list
				for key in keys:
					# Get the file dictionary
					file = files["Dictionary"][key]

					# Define the file
					folder[key] = folder["root"] + file[self.language["Small"]] + ".txt"

					# Create it
					self.File.Create(folder[key])

					# And add it to the "Files" dictionary
					data["Dictionary"]["Files"][data["Folder type"]]["Christmas"][folder_key][key] = folder[key]

			# Create the "Christmas" language files for the "Texts" folder

			# If the "Name" is inside the data dictionary
			# And the dictionary name is "Texts"
			if (
				"Name" in data["Dictionary"] and
				data["Dictionary"]["Name"] == "Texts"
			):
				# Define the local folder dictionary to use
				folder = data["Folders"]["Christmas"]["Planning"]

				# Iterate through the language keys and dictionaries
				for small_language, language in self.languages["Dictionary"].items():
					# Create a shortcut to the full language
					full_language = language["Full"]

					# Define the file
					folder[small_language] = folder["root"] + full_language + ".txt"

					# Create it
					self.File.Create(folder[small_language])

					# And add it to the Christmas "Planning" text files dictionary
					data["Dictionary"]["Files"]["Text"]["Christmas"]["Planning"][small_language] = folder[small_language]

			# ---------- #

			# Create the "New Year" files
			# keys = ["Texts"]
			folder = data["Folders"]["New Year"]

			# Iterate through the files dictionary
			for key, file in self.years["Folder item names"]["New Year"]["Files"]["Dictionary"].items():
				folder[key] = folder["root"] + file[self.language["Small"]] + ".txt"

				self.File.Create(folder[key])

				# And add it to the "Files" dictionary
				data["Dictionary"]["Files"][data["Folder type"]]["New Year"][key] = folder[key]

		# Return the local data dictionary
		return data

	def Create_Image_Folders(self, folders):
		# Define the image folder names dictionary
		folder_names = {
			"Christmas": "",
			"Memories": "",
			"Story": "Key",
			"Summary": "",
			"New Year": ""
		}

		# Iterate through the folder keys and names
		for key, folder_name in folder_names.items():
			# If the folder name is empty
			if folder_name == "":
				# Replace spaces with underscores and lowercase the key to make the text key
				text_key = key.lower().replace(" ", "_")

				# If the underline is not inside the text key
				if "_" not in text_key:
					# Add the ", title()" text
					text_key += ", title()"

				# Get the folder name
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

		# Return the local folders dictionary
		return folders

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
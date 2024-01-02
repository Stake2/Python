# Years.py

class Years(object):
	def __init__(self, select_year = False, create_current_year = True):
		# Define the module folders
		from Utility.Define_Folders import Define_Folders as Define_Folders

		Define_Folders(self)

		# Module related methods
		self.Define_Basic_Variables()
		self.Define_Texts()

		self.create_current_year = create_current_year

		# Folders, lists, and dictionaries methods
		self.Define_Folders_And_Files()

		# Class methods
		self.Define_Folder_Item_Names_Dictionary()
		self.Define_Years_Dictionary()

	def Define_Basic_Variables(self):
		from copy import deepcopy

		# Import the JSON module
		from Utility.JSON import JSON as JSON

		self.JSON = JSON()

		# Get the modules list
		self.modules = self.JSON.To_Python(self.folders["apps"]["modules"]["modules"])

		# Import the "importlib" module
		import importlib

		# Create a list of the modules that will not be imported
		remove_list = [
			"Define_Folders",
			"JSON",
			"Language"
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

	def Define_Folders_And_Files(self):
		# Define the "Years" folder dictionary
		self.folders["Years"] = {
			"Text": {
				"root": self.folders["Notepad"]["Years"]["root"]
			},
			"Image": {
				"root": self.folders["Image"]["Years"]["root"]
			}
		}

		# ---------- #

		# Year "Texts" text folder
		self.folders["Years"]["Text"]["Texts"] = {
			"root": self.folders["Years"]["Text"]["root"] + self.JSON.Language.language_texts["texts, title()"] + "/"
		}

		# "Years.json" file
		self.folders["Years"]["Text"]["Years"] = self.folders["Years"]["Text"]["root"] + "Years.json"
		self.File.Create(self.folders["Years"]["Text"]["Years"])

		# "Years list.txt" file
		self.folders["Years"]["Text"]["Years list"] = self.folders["Years"]["Text"]["root"] + self.Date.language_texts["years_list"] + ".txt"
		self.File.Create(self.folders["Years"]["Text"]["Years list"])

		# ---------- #

		# Year "Images" image folder
		self.folders["Years"]["Image"]["Images"] = {
			"root": self.folders["Years"]["Image"]["root"] + self.JSON.Language.language_texts["images, title()"] + "/"
		}

	def Define_Folder_Item_Names_Dictionary(self):
		# Define the default folder item "Names" dictionary
		self.folder_item_names = {
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
					"Done tasks",
					"Firsts of the Year",
					"Game sessions",
					"Watched media"
				],
				"Files": [
					"Welcome",
					"Summary",
					"This Year I",
					"This Year I (post)",
					"Goodbye"
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
					"Social Networks"
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
							"Social Networks"
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
			}
		}

		# Define the list of keys to use and remove not used keys
		keys = list(self.folder_item_names.keys())
		keys.remove("Additional items")
		keys.remove("Texts")

		# Iterate through the folder item names dictionaries
		# keys = ["Root", "Language", "Christmas", "New Year"]
		for folder_key in keys:
			# Get the item types list
			item_types = self.folder_item_names[folder_key]

			# Iterate through the item types list
			# item_types = ["Folders", "Files"]
			for item_type in item_types:
				# Transform the names list into a dictionary
				dict_ = {
					"List": item_types[item_type],
					"Dictionary": {}
				}

				for item_name in dict_["List"]:
					dict_["Dictionary"][item_name] = {}

					for language in self.languages["small"]:
						text_key = item_name.lower().replace(" ", "_")

						text_key = text_key.replace("(", "")
						text_key = text_key.replace(")", "")

						if "_" not in text_key:
							text_key += ", title()"

						dict_["Dictionary"][item_name][language] = self.JSON.Language.texts[text_key][language]

				self.folder_item_names[folder_key][item_type] = dict_

		# Iterate through the "Additional items" dictionary
		# Example:
		# folder: "Christmas"
		for key, folder in self.folder_item_names["Additional items"].items():
			# Example:
			# sub_folder: "Planning"
			for sub_folder in folder:
				# Transform the names list into a dictionary
				dict_ = {
					"List": folder[sub_folder]["Files"],
					"Dictionary": {}
				}

				for item_name in dict_["List"]:
					dict_["Dictionary"][item_name] = {}

					for language in self.languages["small"]:
						text_key = item_name.lower().replace(" ", "_")

						if "_" not in text_key:
							text_key += ", title()"

						dict_["Dictionary"][item_name][language] = self.JSON.Language.texts[text_key][language]

				# Example:
				# key: "Christmas", sub_folder: "Planning"
				self.folder_item_names["Additional items"][key][sub_folder]["Files"] = dict_

		# Iterate through the "Texts" dictionary
		# Example:
		# folder: "Christmas"
		for key, items in self.folder_item_names["Texts"].items():
			if key == "Christmas":
				sub_folders = items.copy()

				# Example:
				# sub_folder: "Planning"
				for sub_folder, item_types in sub_folders.items():
					# Iterate through the item types list
					# item_types = ["Folders", "Files"]
					for item_type in item_types:
						items = sub_folders[sub_folder][item_type]

						# Transform the names list into a dictionary
						dict_ = {
							"List": items,
							"Dictionary": {}
						}

						# Example:
						# item_name: "Objects"
						for item_name in dict_["List"].copy():
							# Define the empty dictionary
							dict_["Dictionary"][item_name] = {}

							# Iterate through the small languages list
							for language in self.languages["small"]:
								text_key = item_name.lower().replace(" ", "_")

								if "_" not in text_key:
									text_key += ", title()"

								dict_["Dictionary"][item_name][language] = self.JSON.Language.texts[text_key][language]

							# Define the local dictionary
							# Example:
							# key: "Christmas", sub_folder: "Planning", item_type: "Folders"
							folder_dictionary = self.folder_item_names["Texts"][key][sub_folder]

							# Example:
							# item_type: "Files"
							folder_dictionary[item_type] = dict_

			if key == "New Year":
				# Iterate through the item types list
				# item_types = ["Folders", "Files"]
				for item_type, items in items.items():
					# Transform the names list into a dictionary
					dict_ = {
						"List": items,
						"Dictionary": {}
					}

					# Example:
					# item_name: "Objects"
					for item_name in dict_["List"].copy():
						# Define the empty dictionary
						dict_["Dictionary"][item_name] = {}

						# Iterate through the small languages list
						for language in self.languages["small"]:
							text_key = item_name.lower().replace(" ", "_")

							if "_" not in text_key:
								text_key += ", title()"

							dict_["Dictionary"][item_name][language] = self.JSON.Language.texts[text_key][language]

						# Define the local dictionary
						# Example:
						# key: "New Year", item_type: "Files"
						folder_dictionary = self.folder_item_names["Texts"][key]

						# Example:
						# item_type: "Files"
						folder_dictionary[item_type] = dict_

	def Define_Years_Dictionary(self):
		# Define the root "Years" dictionary
		self.years = {
			"Numbers": {
				"Total": 0
			},
			"List": [],
			"Dictionary": {},
			"Author": "Izaque (Stake2, Funkysnipa Cat)",
			"Summary": {},
			"Current year": {},
			"Names": {
				"Folder": {},
				"File": {}
			},
			"States": {
				"Current year folder exists": True
			}
		}

		# ---------- #

		# Create a local dictionary with the "December key"
		dictionary = {
			"December": self.Date.From_String("01/12/{}".format(self.date["Units"]["Year"]))
		}

		# Get the number of days in December
		dictionary["Month days"] = dictionary["December"]["Timezone"]["DateTime"]["Units"]["Month days"]

		# Define the Year
		dictionary["Year"] = self.date["Units"]["Year"]

		# Get the last day of the month, with the month and year
		dictionary["Date"] = self.Date.From_String("{}/12/{}".format(dictionary["Month days"], dictionary["Year"]))

		# Define the root "Summary" dictionary inside the "Years" dictionary as the local dictionary
		self.years["Summary"] = dictionary

		# Define the "Names" key as the updated "Names" dictionary
		self.years["Names"] = self.folder_item_names

		# ---------- #

		# Get the list of years
		self.years["List"] = self.Date.Create_Years_List(function = str)

		# Define the current year folder
		current_year = str(self.date["Units"]["Year"])

		current_year_folder = self.folders["Years"]["Text"]["root"] + current_year + "/"

		self.current_year_number = current_year

		# If the current year folder does not exist
		if self.Folder.Exist(current_year_folder) == False:
			# Define the "Current year folder exists" as False
			self.years["States"]["Current year folder exists"] = False

		# Write the Years list to the "Year list.txt" file
		text_to_write = self.Text.From_List(self.years["List"])

		self.File.Edit(self.folders["Years"]["Text"]["Years list"], text_to_write, "w")

		# ---------- #

		# Iterate through the Years list
		for year in self.years["List"]:
			# Create the local "Year" dictionary
			dictionary = {
				"Number": year,
				"Name": year,
				"Folders": {},
				"Files": {},
				"Information": {}
			}

			# Iterate through the folder type list
			for folder_type in ["Text", "Image"]:
				# Define the root folder
				folder = self.folders["Years"][folder_type]["root"] + year + "/"

				# Create the folders dictionary
				local_dictionary = {
					"root": folder
				}

				self.Folder.Create(local_dictionary["root"])

				# Define the folder type inside the "Files" dictionary
				dictionary["Files"][folder_type] = {}

				# Create the year text folders and files

				# If the folder type is "Text"
				if folder_type == "Text":
					# Define the local "Data" dictionary
					# With the local dictionary, root dictionary, and the folder type ("Text" or "Image")
					data = {
						"Year": year,
						"Local": local_dictionary,
						"Dictionary": dictionary,
						"Folder type": folder_type
					}

					# Define the Year folders
					data = self.Define_Year_Folders(data)

					# Update the local and root dictionary
					local_dictionary = data["Local"]

					dictionary = data["Dictionary"]

				# Create the year image folders
				if folder_type == "Image":
					# Define the image folder names dictionary
					folder_names = {
						"Christmas": self.JSON.Language.language_texts["christmas, title()"],
						"Memories": self.JSON.Language.language_texts["memories, title()"],
						"Story": "",
						"Summary": self.JSON.Language.language_texts["summary, title()"],
						"New Year": self.JSON.Language.language_texts["new_year"]
					}

					# Iterate through the folder names
					for key, folder in folder_names.items():
						# Define the folder name as the key if it is empty
						if folder == "":
							folder = key

						# Define the folder
						local_dictionary[key] = {
							"root": local_dictionary["root"] + folder + "/"
						}

						# Create it
						self.Folder.Create(local_dictionary[key]["root"])

					# Define the "Christmas" image folders

					# Define the image folder names dictionary
					folder_names = {
						"Screenshots": self.JSON.Language.language_texts["screenshots, title()"],
						"Pictures": self.JSON.Language.language_texts["pictures, title()"]
					}

					# Iterate through the folder names
					for key, folder in folder_names.items():
						# Define the folder
						local_dictionary["Christmas"][key] = {
							"root": local_dictionary["Christmas"]["root"] + folder + "/"
						}

						# Create it
						self.Folder.Create(local_dictionary["Christmas"][key]["root"])

				# Define the folders dictionary as the local folders dictionary
				dictionary["Folders"][folder_type] = local_dictionary

			# Add the keys of the "Text" folders dictionary to the root folders dictionary
			dictionary["Folders"].update(dictionary["Folders"]["Text"])

			if "Text" in dictionary["Files"]:
				# Add the keys of the "Text" files dictionary to the root files dictionary
				dictionary["Files"].update(dictionary["Files"]["Text"])

			# Define the "Year" dictionary as the local "Year" dictionary
			self.years["Dictionary"][year] = dictionary

		# Define the "Current year" key as the Year dictionary inside the Years dictionary
		self.years["Current year"] = self.years["Dictionary"][current_year]

		# Get the number of years
		self.years["Numbers"]["Total"] = len(self.years["List"])

		# ---------- #

		# Define the "Texts" dictionary
		dictionary = {
			"Name": "Texts",
			"Folders": {
				"Text": {}
			},
			"Files": {
				"Text": {}
			}
		}

		# Create the local folders dictionary
		local_dictionary = {
			"root": self.folders["Years"]["Text"]["Texts"]["root"]
		}

		self.Folder.Create(local_dictionary["root"])

		# Define the local "Data" dictionary
		# With the local dictionary, root dictionary, and the folder type ("Text" or "Image")
		data = {
			"Year": "2018",
			"Local": local_dictionary,
			"Dictionary": dictionary,
			"Folder type": "Text"
		}

		# Define the "Texts" folders
		data = self.Define_Year_Folders(data)

		# Get the local folders dictionary
		dictionary["Folders"] = data["Local"]

		# Get the local files dictionary
		dictionary["Files"] = data["Dictionary"]["Files"]["Text"]

		# Define the "Texts" dictionary as the local "Texts" dictionary
		self.years["Texts"] = dictionary

		# ---------- #

		# Define the image folder names dictionary
		folder_names = {
			"Christmas": self.JSON.Language.language_texts["christmas, title()"],
			"Memories": self.JSON.Language.language_texts["memories, title()"],
			"Summary": self.JSON.Language.language_texts["summary, title()"],
			"New Year": self.JSON.Language.language_texts["new_year"],
			"Story": ""
		}

		# Define the local "Images" dictionary
		local_dictionary = {
			"root": self.folders["Years"]["Image"]["root"] + self.JSON.Language.language_texts["images, title()"] + "/"
		}

		# Iterate through the folder names
		for key, folder in folder_names.items():
			# Define the folder name as the key if it is empty
			if folder == "":
				folder = key

			# Define the folder
			local_dictionary[key] = {
				"root": local_dictionary["root"] + folder + "/"
			}

			# Create it
			self.Folder.Create(local_dictionary[key]["root"])

		# Define the "Images" folder dictionary as the local "Images" dictionary
		self.folders["Years"]["Image"]["Images"] = local_dictionary

		# ---------- #

		# Make a local copy of the Years dictionary
		from copy import deepcopy

		local_dictionary = deepcopy(self.years)

		# Define the root keys to remove
		to_remove = [
			"Author",
			"Summary",
			"Names",
			"States"
		]

		# Iterate through the "root keys to remove" list and remove the keys
		for key in to_remove:
			local_dictionary.pop(key)

		# Iterate through the years list
		for year in self.years["List"]:
			# Define the year dictionary variable for easier typing
			year_dictionary = local_dictionary["Dictionary"][year]

			# Remove the unused keys of the Year dictionary
			for key in ["Name", "Folders"]:
				year_dictionary.pop(key)

			if "Text" in year_dictionary["Files"]:
				# Remove the "Text" keys of the "Files" dictionary of the Year dictionary
				year_dictionary["Files"].pop("Text")

		# Remove the "Folders" keys of the "Texts" dictionary
		local_dictionary["Texts"].pop("Folders")

		# Write the local updated "Years" dictionary to the "Years.json" file
		self.JSON.Edit(self.folders["Years"]["Text"]["Years"], local_dictionary)

	def Define_Year_Folders(self, data):
		from copy import deepcopy

		# Define the folder type key inside the "Files" dictionary
		data["Dictionary"]["Files"][data["Folder type"]] = {}

		# Define the folder keys
		for item in ["Christmas", "New Year"]:
			data["Dictionary"]["Files"][data["Folder type"]][item] = {}

		# Define the language folder keys
		# Iterate through the small languages list
		for language in self.languages["small"]:
			data["Dictionary"]["Files"][data["Folder type"]][language] = {}

		# Create the language text folders
		# Iterate through the small languages list
		for language in self.languages["small"]:
			# Get the full language
			full_language = self.languages["full"][language]

			# Define the folder
			data["Local"][language] = {
				"root": data["Local"]["root"] + full_language + "/"
			}

			# Create it
			self.Folder.Create(data["Local"][language]["root"])

		# Create the root text folders and files
		for item_type in ["Folders", "Files"]:
			# folders = ["Christmas", "Summary", "New Year"]
			# files = ["Created in", "Edited in"]
			for key, folder_item in self.years["Names"]["Root"][item_type]["Dictionary"].items():
				# Define the folder
				data["Local"][key] = {
					"root": data["Local"]["root"] + folder_item[self.user_language] + "/"
				}

				# Define the folder item as the root folder
				item = data["Local"][key]["root"]

				# Define the class as "self.Folder"
				Class = self.Folder

				if item_type == "Files":
					# Define the file
					data["Local"][key] = data["Local"]["root"] + folder_item[self.user_language] + ".txt"

					# Define the class as "self.File"
					Class = self.File

					# Define the folder item as the file
					item = data["Local"][key]

				# Create it
				Class.Create(item)

				if item_type == "Files":
					# Add it to the "Files" dictionary
					data["Dictionary"]["Files"][data["Folder type"]][key] = data["Local"][key]

			# folders = ["Done tasks", "Firsts of the Year", "Game Sessions", "Watched media"]
			# files = ["Summary", "This Year I"]
			keys = list(self.years["Names"]["Language"][item_type]["Dictionary"].keys())

			# If the "Name" is inside the data dictionary
			# And the dictionary name is "Texts"
			# And the item type is "Files"
			# files = ["This Year I (post)"]
			if (
				"Name" in data["Dictionary"] and
				data["Dictionary"]["Name"] == "Texts" and
				item_type == "Files"
			):
				keys = [
					"This Year I (post)"
				]

			# Iterate through the small languages list
			for language in self.languages["small"]:
				data["Dictionary"]["Files"][data["Folder type"]][language]

				# Create the language folder text folders
				for key in keys:
					folder_item = self.years["Names"]["Language"][item_type]["Dictionary"][key]

					# Define the folder
					data["Local"][language][key] = {
						"root": data["Local"][language]["root"] + folder_item[language] + "/"
					}

					# Define the folder item as the root folder
					item = data["Local"][language][key]["root"]

					if item_type == "Files":
						# Define the file
						data["Local"][language][key] = data["Local"][language]["root"] + folder_item[language] + ".txt"

						# Define the class as "self.File"
						Class = self.File

						# Define the folder item as the file
						item = data["Local"][language][key]

					# Create it
					Class.Create(item)

					if item_type == "Files":
						# Add it to the "Files" dictionary
						data["Dictionary"]["Files"][data["Folder type"]][language][key] = data["Local"][language][key]

		# ---------- #

		# Create the "Christmas" folders

		# Iterate through the "Christmas" files dictionary
		# keys = ["Planning", "Merry Christmas"]
		for key, folder in self.years["Names"]["Christmas"]["Folders"]["Dictionary"].items():
			data["Local"]["Christmas"][key] = {
				"root": data["Local"]["Christmas"]["root"] + folder[self.user_language] + "/"
			}

			self.Folder.Create(data["Local"]["Christmas"][key]["root"])

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
			folder = data["Local"]["Christmas"]["Merry Christmas"]

			dictionary = deepcopy(self.years["Names"]["Christmas"]["Files"]["Dictionary"])

			# Iterate through the "Merry Christmas" files dictionary
			# keys = ["Texts"]
			for key, file in dictionary.items():
				# Define the file
				folder[key] = folder["root"] + file[self.user_language] + ".txt"

				# Create it
				self.File.Create(folder[key])

				# And add it to the "Files" dictionary
				data["Dictionary"]["Files"][data["Folder type"]]["Christmas"]["Merry Christmas"][key] = folder[key]

		# ---------- #

		# Define the list of files to create
		social_networks_list = [
			"Discord",
			"Instagram, Facebook",
			"Twitter",
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
			folder = data["Local"]["Christmas"]["Planning"]

			dictionary = self.years["Names"]["Texts"]["Christmas"]["Planning"]

			# Create the Christmas "Planning" files
			# Iterate through the files dictionary
			# keys = ["Objects", self.languages["full"].values()]
			for key, file in dictionary["Files"]["Dictionary"].items():
				# Define the root folder
				folder[key] = folder["root"]

				# Define the file name and extension
				# (Langauge file name and "txt")
				file_name = file[self.user_language]

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
			folder = data["Local"]["Christmas"]["Merry Christmas"]

			dictionary = self.years["Names"]["Texts"]["Christmas"]["Merry Christmas"]

			# Create the Christmas "Merry Christmas" folders
			# Iterate through the folders dictionary
			# keys = ["Social Networks"]
			for key, folder_name in dictionary["Folders"]["Dictionary"].items():
				# Define the root folder
				folder[key] = {
					"root": folder["root"] + folder_name[self.user_language] + "/"
				}

				# Create the folder
				self.Folder.Create(folder[key]["root"])

			# Create the Christmas "Merry Christmas" social networks files
			for file_name in social_networks_list:
				# Define the file
				folder["Social Networks"][file_name] = folder["Social Networks"]["root"] + file_name + ".txt"

				# Create the file
				self.File.Create(folder["Social Networks"][file_name])

		# ---------- #

		# Define the local "New Year" folder and dictionary
		folder = data["Local"]["New Year"]

		dictionary = self.years["Names"]["New Year"]

		# Remove the "Wattpad" social network from the list of Social Networks
		social_networks_list.remove("Wattpad")

		# Create the New Year "Social Networks" file
		# Iterate through the files dictionary
		for key, folder_name in dictionary["Folders"]["Dictionary"].items():
			# Define the root folder
			folder[key] = {
				"root": folder["root"] + folder_name[self.user_language] + "/"
			}

			# Create it
			self.Folder.Create(folder[key]["root"])

			# And add it to the "Files" dictionary
			data["Dictionary"]["Files"][data["Folder type"]]["New Year"][key] = {}

			# Define and create the social network files
			for social_network in social_networks_list:
				# Define the file
				folder[key][social_network] = folder[key]["root"] + social_network + ".txt"

				# Create it
				self.File.Create(folder[key][social_network])

				# And add it to the Files "Social Networks" dictionary
				data["Dictionary"]["Files"][data["Folder type"]]["New Year"][key][social_network] = folder[key][social_network]

		# Create the New Year "Texts" file
		# Iterate through the files dictionary
		for key, file in dictionary["Files"]["Dictionary"].items():
			# Define the file
			folder[key] = folder["root"] + file[self.user_language] + ".txt"

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
			for folder_key in self.years["Names"]["Additional items"]["Christmas"]:
				# Get the list of files to create
				# Example:
				# folder_key: "Planning"
				files = self.years["Names"]["Additional items"]["Christmas"][folder_key]["Files"]

				# Define the folder dictionary
				folder = data["Local"]["Christmas"][folder_key]

				# Define the keys list
				keys = list(files["Dictionary"].keys())

				# If the "Name" is inside the data dictionary
				# And the dictionary name is "Texts"
				if (
					"Name" in data["Dictionary"] and
					data["Dictionary"]["Name"] == "Texts"
				):
					# Remove the "Watch" and "Eat" from the keys list
					for key in ["Watch", "Eat"]:
						if key in keys:
							keys.remove(key)

				# Iterate through the keys list
				for key in keys:
					# Get the file dictionary
					file = files["Dictionary"][key]

					# Define the file
					folder[key] = folder["root"] + file[self.user_language] + ".txt"

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
				folder = data["Local"]["Christmas"]["Planning"]

				# Iterate through the small languages list
				for language in self.languages["small"]:
					# Get the full language
					full_language = self.languages["full"][language]

					# Define the file
					folder[language] = folder["root"] + full_language + ".txt"

					# Create it
					self.File.Create(folder[language])

					# And add it to the "Files" dictionary
					data["Dictionary"]["Files"]["Text"]["Christmas"]["Planning"][language] = folder[language]

			# ---------- #

			# Create the "New Year" files
			# keys = ["Texts"]
			folder = data["Local"]["New Year"]

			# Iterate through the files dictionary
			for key, file in self.years["Names"]["New Year"]["Files"]["Dictionary"].items():
				folder[key] = folder["root"] + file[self.user_language] + ".txt"

				self.File.Create(folder[key])

				# And add it to the "Files" dictionary
				data["Dictionary"]["Files"][data["Folder type"]]["New Year"][key] = folder[key]

		return data

	def Select_Year(self, years = None, select_text = None):
		if years == None:
			years = self.years["List"]

		show_text = self.Date.language_texts["years, title()"]

		if select_text == None:
			select_text = self.language_texts["select_a_year"]

		option = self.Input.Select(years, show_text = show_text, select_text = select_text)["option"]

		self.year = self.years["Dictionary"][option]

		return self.year
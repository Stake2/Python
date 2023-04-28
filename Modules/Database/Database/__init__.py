# Database.py

class Database(object):
	def __init__(self):
		self.Define_Basic_Variables()

		# Define module folders
		from Utility.Define_Folders import Define_Folders as Define_Folders

		Define_Folders(self)

		self.Define_Texts()

		# Import the Years class
		from Years.Years import Years as Years
		self.Years = Years()

		# Import the Christmas class
		from Christmas.Christmas import Christmas as Christmas

		self.Christmas = Christmas()
		self.Today_Is_Christmas = self.Christmas.Today_Is_Christmas()

		self.Define_Folders_And_Files()

		self.Define_Types()
		self.Define_Registry_Format()

	def Define_Basic_Variables(self):
		from Utility.Global_Switches import Global_Switches as Global_Switches

		from Utility.File import File as File
		from Utility.Folder import Folder as Folder
		from Utility.Date import Date as Date
		from Utility.Input import Input as Input
		from Utility.JSON import JSON as JSON
		from Utility.Text import Text as Text

		self.switches = Global_Switches().switches["global"]

		self.File = File()
		self.Folder = Folder()
		self.Date = Date()
		self.Input = Input()
		self.JSON = JSON()
		self.Text = Text()

		self.languages = self.JSON.Language.languages

		self.user_language = self.JSON.Language.user_language
		self.full_user_language = self.JSON.Language.full_user_language

		self.Sanitize = self.File.Sanitize

		self.folders = self.Folder.folders

		self.date = self.Date.date

	def Define_Texts(self):
		self.texts = self.JSON.To_Python(self.folders["apps"]["module_files"][self.module["key"]]["texts"])

		self.language_texts = self.JSON.Language.Item(self.texts)

		self.large_bar = "-----"
		self.dash_space = "-"

	def Define_Folders_And_Files(self):
		self.current_year = self.Years.current_year

		# Folders dictionary
		self.folders = self.Folder.Contents(self.folders["notepad"]["networks"]["database_network"]["root"], lower_key = True)["dictionary"]

		# Define the current year folder for easier typing
		self.folders["history"]["current_year"] = self.folders["history"][str(self.date["Units"]["Year"])]

	def Define_Types(self):
		self.types = self.JSON.To_Python(self.folders["data"]["types"])

		self.types.update({
			"Genders": self.JSON.Language.texts["genders, type: dict"],
			"Gender items": self.JSON.Language.texts["gender_items"],
			"Data list": {
				"Number": 0,
				"Numbers": {}
			}
		})

		# Reset the data number to 0
		if self.types["Data list"]["Number"] != 0:
			self.types["Data list"]["Number"] = 0

		# Read the root "Info.json" file
		if self.File.Contents(self.folders["information"]["info"])["lines"] != []:
			info_dictionary = self.JSON.To_Python(self.folders["information"]["info"])

		# If the root "Info.json" file is empty, add a default JSON dictionary inside it
		if self.File.Contents(self.folders["information"]["info"])["lines"] == []:
			info_dictionary = {
				"Types": self.game_types["Plural"],
				"Number": 0,
				"Numbers": {}
			}

		# Iterate through English plural types list
		i = 0
		for plural_type in self.types["Plural"]["en"]:
			key = plural_type.lower().replace(" ", "_")

			language_type = self.types["Plural"][self.user_language][i]

			# Create type dictionary
			self.types[plural_type] = {
				"Singular": {},
				"Plural": {},
				"Folders": {},
				"Status": [
					self.texts["plan_to_experience, title()"]["en"],
					self.texts["experiencing, title()"]["en"],
					self.texts["re_experiencing, title()"]["en"],
					self.JSON.Language.texts["on_hold, title()"]["en"]
				],
				"Items": {},
				"Texts": {},
				"Data number": 0,
				"Data list": []
			}

			# Define the singular and plural types
			for language in self.languages["small"]:
				for item in ["Singular", "Plural"]:
					self.types[plural_type][item][language] = self.types[item][language][i]

			# Create type folders
			for root_folder in ["Information", "History"]:
				root_key = root_folder.lower().replace(" ", "_")

				# "Data Information" folder
				if root_folder == "Information":
					self.folders[root_key][key] = {
						"root": self.folders[root_key]["root"] + language_type + "/"
					}

					self.Folder.Create(self.folders[root_key][key]["root"])

				# "History Per Type" folder
				if root_folder == "History":
					self.folders[root_key]["current_year"]["per_type"][key] = {
						"root": self.folders[root_key]["current_year"]["per_type"]["root"] + plural_type + "/"
					}

					self.Folder.Create(self.folders[root_key]["current_year"]["per_type"][key]["root"])

					# Create "Entries.json" file
					self.folders[root_key]["current_year"]["per_type"][key]["entries"] = self.folders[root_key]["current_year"]["per_type"][key]["root"] + "Entries.json"
					self.File.Create(self.folders[root_key]["current_year"]["per_type"][key]["entries"])

					# Create "Entry list.txt" file
					self.folders[root_key]["current_year"]["per_type"][key]["entry_list"] = self.folders[root_key]["current_year"]["per_type"][key]["root"] + "Entry list.txt"
					self.File.Create(self.folders[root_key]["current_year"]["per_type"][key]["entry_list"])

					# Create "Files" folder 
					self.folders[root_key]["current_year"]["per_type"][key]["files"] = {
						"root": self.folders[root_key]["current_year"]["per_type"][key]["root"] + "Files/"
					}

					self.Folder.Create(self.folders[root_key]["current_year"]["per_type"][key]["files"]["root"])

			# Define type folders and files
			self.types[plural_type]["Folders"] = {
				"information": self.folders["information"][key],
				"per_type": self.folders["history"]["current_year"]["per_type"][key]
			}

			# Define the "Info.json" file
			self.types[plural_type]["Folders"]["information"]["info"] = self.types[plural_type]["Folders"]["information"]["root"] + "Info.json"
			self.File.Create(self.types[plural_type]["Folders"]["information"]["info"])

			# Read the "Info.json" file
			if self.File.Contents(self.types[plural_type]["Folders"]["information"]["info"])["lines"] != []:
				self.types[plural_type]["JSON"] = self.JSON.To_Python(self.types[plural_type]["Folders"]["information"]["info"])

			# If the "Info.json" file is empty, add a default JSON dictionary inside it
			if self.File.Contents(self.types[plural_type]["Folders"]["information"]["info"])["lines"] == []:
				# Define the default JSON dictionary
				self.types[plural_type]["JSON"] = {
					"Number": 0,
					"Titles": [],
					"Status": {}
				}

				# Create an empty list for each status
				for english_status in self.texts["statuses, type: list"]["en"]:
					self.types[plural_type]["JSON"]["Status"][english_status] = []

			# Update the number of data inside the json dictionary
			self.types[plural_type]["JSON"]["Number"] = len(self.types[plural_type]["JSON"]["Titles"])

			# Edit the "Info.json" file with the new dictionary
			self.JSON.Edit(self.types[plural_type]["Folders"]["information"]["info"], self.types[plural_type]["JSON"])

			# Check the status of the data list
			# Add the data inside the correct status list if it is not there already
			# Remove the data from the wrong status list if it is there
			self.types[plural_type] = self.Check_Status(self.types[plural_type])

			# Add the data number to the data number inside the data list
			self.types["Data list"]["Number"] += self.types[plural_type]["JSON"]["Number"]

			# Add the data number to the data type data numbers
			self.types["Data list"]["Numbers"][plural_type] = self.types[plural_type]["JSON"]["Number"]

			# Add the data number to the root data number
			info_dictionary["Numbers"][plural_type] = self.types[plural_type]["JSON"]["Number"]

			# Get the data list with "Experiencing" and "Re-experiencing" statuses
			self.types[plural_type]["Data list"] = self.Get_Data_List(self.types[plural_type])

			# Define the data number of the data type
			self.types[plural_type]["Data number"] = len(self.types[plural_type]["Data list"])

			add_status = True

			# Add status to the "data list option" list if add_status is True
			if add_status == True:
				self.types[plural_type]["Data list (option)"] = self.types[plural_type]["Data list"].copy()

				d = 0
				for data in self.types[plural_type]["Data list"]:
					for status in self.types[plural_type]["Status"]:
						if data in self.types[plural_type]["JSON"]["Status"][status]:
							language_status = self.Get_Language_Status(status)

					items = [
						self.types[plural_type]["Data list (option)"][d],
						language_status
					]

					self.types[plural_type]["Data list (option)"][d] = "{} - ({})".format(*items)

					d += 1

				if self.types[plural_type]["Data list (option)"] == []:
					self.types[plural_type].pop("Data list (option)")

			# Remove the "JSON" key
			self.types[plural_type].pop("JSON")

			# Define the entry item
			for language in self.languages["small"]:
				self.types[plural_type]["Items"][language] = self.types["items, type: dict"][plural_type][language]

			# Add the data list length numbers to the data types list to show on select data type
			for text_type in ["Singular", "Plural"]:
				self.types[plural_type][text_type]["Show"] = self.types[plural_type][text_type][self.user_language] + " (" + str(len(self.types[plural_type]["Data list"])) + ")"

			# Update the "Show" text
			self.types[plural_type]["Texts"]["Show"] = self.Text.By_Number(self.types[plural_type]["Data list"], self.types[plural_type]["Singular"]["Show"], self.types[plural_type]["Plural"]["Show"])

			i += 1

		# Write the types dictionary into the "Types.json" file
		self.JSON.Edit(self.folders["data"]["types"], self.types)

		# Update the data list inside the root "Info.json" dictionary
		info_dictionary.update(self.types["Data list"])

		# Update the root "Info.json" file
		self.JSON.Edit(self.folders["information"]["info"], info_dictionary)

	def Define_Registry_Format(self):
		from copy import deepcopy

		# Define the default Entries dictionary template
		self.template = {
			"Numbers": {
				"Total": 0
			},
			"Entries": [],
			"Dictionary": {}
		}

		self.dictionaries = {
			"History": {
				"Numbers": {
					"Years": 0,
					"Entries": 0
				},
				"Years": []
			},
			"Registered": deepcopy(self.template),
			"Entries": deepcopy(self.template),
			"Entry type": {}
		}

		if self.File.Contents(self.folders["history"]["history"])["lines"] != [] and self.JSON.To_Python(self.folders["history"]["history"])["Years"] != []:
			# Get the History dictionary from file
			self.dictionaries["History"] = self.JSON.To_Python(self.folders["history"]["history"])

		# If the current year is not inside the "History" years list, add it to the list
		if self.current_year["Number"] not in self.dictionaries["History"]["Years"]:
			self.dictionaries["History"]["Years"].append(self.current_year["Number"])

		# Update the number of years with the length of the years list
		self.dictionaries["History"]["Numbers"]["Years"] = len(self.dictionaries["History"]["Years"])

		entries = 0

		# Update the number of entries of all years
		for year in range(self.date["Units"]["Year"], self.date["Units"]["Year"] + 1):
			year = str(year)

			# Get the year folder and the entries file
			year_folder = self.folders["history"]["root"] + year + "/"
			entries_file = year_folder + "Entries.json"

			# If the file exists and it is not empty
			if self.File.Exist(entries_file) == True and self.File.Contents(entries_file)["lines"] != []:
				# Add the number of lines of the file to the local number of entries
				entries += self.JSON.To_Python(entries_file)["Numbers"]["Total"]

			# Add the year to the Years list if it is not inside it
			if year not in self.dictionaries["History"]["Years"]:
				self.dictionaries["History"]["Years"].append(year)

		# Sort the Years list
		self.dictionaries["History"]["Years"] = sorted(self.dictionaries["History"]["Years"], key = str.lower)

		# Define the number of Entries of all years as the local number of entries
		self.dictionaries["History"]["Numbers"]["Entries"] = entries

		# Update the "History.json" file with the new History dictionary
		self.JSON.Edit(self.folders["history"]["history"], self.dictionaries["History"])

		# Create the "Per Type" key inside the "Numbers" dictionary of the "Entries" dictionary
		self.dictionaries["Entries"]["Numbers"]["Per Type"] = {}

		# If the "Entries.json" is not empty and has entries, get the Entries dictionary from it
		if self.File.Contents(self.folders["history"]["current_year"]["entries"])["lines"] != [] and self.JSON.To_Python(self.folders["history"]["current_year"]["entries"])["Entries"] != []:
			self.dictionaries["Entries"] = self.JSON.To_Python(self.folders["history"]["current_year"]["entries"])

		# Iterate through the English types list
		for plural_type in self.types["Plural"]["en"]:
			key = plural_type.lower().replace(" ", "_")

			# Define default type dictionary
			self.dictionaries["Entry type"][plural_type] = deepcopy(self.template)

			# If the type "Entries.json" is not empty, get the type Entries dictionary from it
			if self.File.Contents(self.folders["history"]["current_year"]["per_type"][key]["entries"])["lines"] != [] and self.JSON.To_Python(self.folders["history"]["current_year"]["per_type"][key]["entries"])["Entries"] != []:
				self.dictionaries["Entry type"][plural_type] = self.JSON.To_Python(self.folders["history"]["current_year"]["per_type"][key]["entries"])

			# Add the plural type number to the root numbers per type if it does not exist in there
			if plural_type not in self.dictionaries["Entries"]["Numbers"]["Per Type"]:
				self.dictionaries["Entries"]["Numbers"]["Per Type"][plural_type] = 0

			# Else, define the root total number per type as the number inside the Entries dictionary per type
			if plural_type in self.dictionaries["Entries"]["Numbers"]["Per Type"]:
				self.dictionaries["Entries"]["Numbers"]["Per Type"][plural_type] = self.dictionaries["Entry type"][plural_type]["Numbers"]["Total"]

			# Update the per type "Entries.json" file with the updated per type Entries dictionary
			self.JSON.Edit(self.folders["history"]["current_year"]["per_type"][key]["entries"], self.dictionaries["Entry type"][plural_type])

		# Update the "Entries.json" file with the updated Entries dictionary
		self.JSON.Edit(self.folders["history"]["current_year"]["entries"], self.dictionaries["Entries"])

	def Get_Data_List(self, dictionary, status = None):
		'''

		Returns a data list of a specific data type that contains a data status

			Parameters:
				dictionary (dict): a data_type dictionary containing the data type folders
				status (str or list): a status string or list used to get the data that has that status

			Returns:
				data_list (list): The data list that contains the data that has the passed status string or list

		'''

		# Get the status list from the data type dictionary
		status_list = dictionary["Status"].copy()

		# If the status parameter is not None, use it as the status
		if status != None:
			status_list = status

		# If the type of the status list is string, make it a list of only the string
		if type(status_list) == str:
			status_list = [status_list]

		# Get the data type "Info.json" file and read it
		dictionary["JSON"] = self.JSON.To_Python(dictionary["Folders"]["information"]["info"])

		# Define the empty data list
		data_list = []

		# Add the data of each status to the data list
		for status in status_list:
			if type(status) == dict:
				status = status["en"]

			data_list.extend(dictionary["JSON"]["Status"][status])

		# Sort the data list
		data_list = sorted(data_list, key = str.lower)

		return data_list

	def Select_Type(self, options = None):
		dictionary = {
			"Texts": {
				"Show": self.language_texts["data_types"],
				"Select": self.language_texts["select_one_data_type_to_experience"]
			},
			"List": {
				"en": self.types["Plural"]["en"].copy(),
				self.user_language: self.types["Plural"][self.user_language].copy()
			},
			"Status": [
				self.texts["plan_to_experience, title()"]["en"],
				self.texts["experiencing, title()"]["en"],
				self.texts["re_experiencing, title()"]["en"],
				self.JSON.Language.texts["on_hold, title()"]["en"]
			]
		}

		if options != None:
			dictionary = self.Define_Options(dictionary, options)

		# Get the data type data numbers
		numbers = self.JSON.To_Python(self.folders["information"]["info"])["Numbers"]

		# Add the number of data inside each data type text
		i = 0
		for plural_type in self.types["Plural"]["en"]:
			if plural_type in dictionary["List"]["en"]:
				for language in self.languages["small"]:
					dictionary["List"][language][i] = dictionary["List"][language][i] + " (" + str(numbers[plural_type]) + ")"

				i += 1

		# Select the data type
		if "option" not in dictionary and "number" not in dictionary:
			dictionary["option"] = self.Input.Select(dictionary["List"]["en"], dictionary["List"][self.user_language], show_text = dictionary["Texts"]["Show"], select_text = dictionary["Texts"]["Select"])["option"]
			dictionary["option"] = dictionary["option"].split(" (")[0]

		if "number" in dictionary:
			dictionary["option"] = dictionary["List"]["en"][dictionary["number"]]

		# Get the selected data type dictionary from the data types dictionary
		dictionary.update(self.types[dictionary["option"]])

		# Get the status from the options dictionary
		if "Status" in options:
			dictionary["Status"] = options["Status"]

		# Get the data list using the correct status
		dictionary["Data list"] = self.Get_Data_List(dictionary, dictionary["Status"])

		# Add the data list length numbers to the data types list to show on the select data
		for language in self.languages["small"]:
			for text_type in ["Singular", "Plural"]:
				dictionary[text_type]["Show"] = dictionary[text_type][self.user_language] + " (" + str(len(dictionary["Data list"])) + ")"

		# Update the "Show" text
		dictionary["Texts"]["Show"] = self.Text.By_Number(dictionary["Data list"], dictionary["Singular"]["Show"], dictionary["Plural"]["Show"])

		return dictionary

	def Select_Data(self, options = None):
		from copy import deepcopy

		dictionary = {}

		if options != None:
			dictionary = self.Define_Options(dictionary, options)

		data = dictionary["Data"]

		dictionary["Texts"] = dictionary["Type"]["Texts"]

		# Define the select text
		text = dictionary["Type"]["Singular"][self.user_language]

		if "Select" in dictionary["Type"]["Singular"]:
			text = dictionary["Type"]["Singular"]["Select"]

		dictionary["Texts"]["Select"] = self.language_texts["select_one_data_to_experience"]

		# Select the data
		if "Title" not in data:
			language_options = dictionary["Type"]["Data list"]

			if "Data list (option)" in dictionary["Type"]:
				language_options = dictionary["Type"]["Data list (option)"]

			data.update({
				"Title": self.Input.Select(dictionary["Type"]["Data list"], language_options = language_options, show_text = dictionary["Texts"]["Show"], select_text = dictionary["Texts"]["Select"])["option"]
			})

		# Define the data information folder
		data["folders"] = {
			"root": dictionary["Type"]["Folders"]["information"]["root"] + self.Sanitize_Title(data["Title"]) + "/"
		}

		# Create the folders
		for key in data["folders"]:
			folder = data["folders"][key]

			if "root" in folder:
				folder = folder["root"]

			self.Folder.Create(folder)

		file_names = [
			"Details",
			"Dates"
		]

		data["Information"] = {
			"File name": "Data",
			"Key": ""
		}

		file_names.append(data["Information"]["File name"] + ".json")

		data["Information"]["Key"] = data["Information"]["File name"].lower().replace(" ", "_")

		# Define the data text files
		for file_name in file_names:
			key = file_name.lower().replace(" ", "_").replace(".json", "")

			if key == "details":
				texts_list = self.JSON.Language.language_texts

			if key == "dates":
				texts_list = self.Date.language_texts

			if ".json" not in file_name:
				file_name = texts_list[key + ", title()"] + ".txt"

			data["folders"][key] = data["folders"]["root"] + file_name
			self.File.Create(data["folders"][key])

		if self.File.Contents(data["folders"][data["Information"]["Key"]])["lines"] != []:
			data["Information"]["Dictionary"] = self.JSON.To_Python(data["folders"][data["Information"]["Key"]])

		# Create the "Registered" folder
		data["folders"]["registered"] = {
			"root": data["folders"]["root"] + self.language_texts["registered, title()"] + "/"
		}

		self.Folder.Create(data["folders"]["registered"]["root"])

		# Create the "Entries.json" file inside the "Registered" folder
		data["folders"]["registered"]["entries"] = data["folders"]["registered"]["root"] + "Entries.json"
		self.File.Create(data["folders"]["registered"]["entries"])

		# Create the "Entry list.txt" file inside the "Registered" folder
		data["folders"]["registered"]["entry_list"] = data["folders"]["registered"]["root"] + "Entry list.txt"
		self.File.Create(data["folders"]["registered"]["entry_list"])

		# Create the "Files" folder file inside the "Registered" folder
		data["folders"]["registered"]["files"] = {
			"root": data["folders"]["registered"]["root"] + self.File.language_texts["files, title()"] + "/"
		}

		self.Folder.Create(data["folders"]["registered"]["files"]["root"])

		# Define the "Registered" dictionary as the template
		self.dictionaries["Registered"] = deepcopy(self.template)

		# Get the "Registered" dictionary from file if the dictionary is not empty and has entries
		if self.File.Contents(data["folders"]["registered"]["entries"])["lines"] != [] and self.JSON.To_Python(data["folders"]["registered"]["entries"])["Entries"] != []:
			self.dictionaries["Registered"] = self.JSON.To_Python(data["folders"]["registered"]["entries"])

		# Update the number of entries with the length of the entries list
		self.dictionaries["Registered"]["Numbers"]["Total"] = len(self.dictionaries["Registered"]["Entries"])

		# Define the "Registered" dictionary inside the data dictionary
		data["Registered"] = deepcopy(self.dictionaries["Registered"])

		# Write the default or file dictionary into the "Registered.json" file
		self.JSON.Edit(data["folders"]["registered"]["entries"], self.dictionaries["Registered"])

		# Define the data details
		data["details"] = self.File.Dictionary(data["folders"]["details"])

		# Define the default data language as the user language
		data["Language"] = self.full_user_language

		# Change user language to original data language if the key exists inside the data details
		if self.JSON.Language.language_texts["original_language"] in data["details"]:
			data["Language"] = data["details"][self.JSON.Language.language_texts["original_language"]]

		if data["Language"] in list(self.languages["full"].values()):
			# Iterate through full languages list to find small language from the full language
			for small_language in self.languages["full"]:
				full_language = self.languages["full"][small_language]

				if full_language == data["Language"]:
					data["Language"] = small_language

		# Define data states dictionary
		states = {
			"Remote": False,
			"Local": False,
			"Re-experiencing": False,
			"Christmas": False,
			"Completed data": False,
			"First entry in year": False,
			"First type entry in year": False,
			"Finished experiencing": False
		}

		if "States" in data:
			data["States"].update(states)

		elif "States" not in data:
			data["States"] = states

		if self.Today_Is_Christmas == True:
			data["States"]["Christmas"] = True

		origin_types = [
			"Local",
			"Remote"
		]

		# Define the origin type state
		for key in origin_types:
			if self.JSON.Language.language_texts["origin_type"] in data["details"]:
				if data["details"][self.JSON.Language.language_texts["origin_type"]] == self.language_texts[key.lower() + ", title()"]:
					data["States"][key] = True

		data["States"]["Remote"] = False

		if self.JSON.Language.language_texts["origin_type"] not in data["details"]:
			data["States"]["Remote"] = True

			data["details"][self.JSON.Language.language_texts["origin_type"]] = self.JSON.Language.language_texts["remote, title()"]

		# Define Re-experiencing state for Re-experiencing status
		if self.JSON.Language.language_texts["status, title()"] in data["details"] and data["details"][self.JSON.Language.language_texts["status, title()"]] == self.language_texts["re_experiencing, title()"]:
			data["States"]["Re-experiencing"] = True

		if self.dictionaries["Entries"]["Numbers"]["Total"] == 0:
			data["States"]["First entry in year"] = True

		if self.dictionaries["Entry type"][dictionary["Type"]["Plural"]["en"]]["Numbers"]["Total"] == 0:
			data["States"]["First type entry in year"] = True

		dictionary = self.Define_Data_Titles(dictionary)

		return dictionary

	def Select_Data_Type_And_Data(self, options = None):
		dictionary = {
			"Type": {
				"Select": True,
				"Status": [
					self.texts["plan_to_experience, title()"]["en"],
					self.texts["experiencing, title()"]["en"],
					self.texts["re_experiencing, title()"]["en"],
					self.JSON.Language.texts["on_hold, title()"]["en"]
				]
			},
			"Data": {
				"Select": True,
				"List": {}
			}
		}

		if options != None:
			dictionary = self.Define_Options(dictionary, options)

		if dictionary["Type"]["Select"] == True:
			dictionary["Type"] = self.Select_Type(dictionary["Type"])

		if dictionary["Data"]["Select"] == True:
			dictionary["Data"] = self.Select_Data(dictionary)["Data"]

		return dictionary

	def Define_States_Dictionary(self, dictionary):
		states_dictionary = {
			"States": {},
			"Texts": {}
		}

		# Define the keys for the states
		keys = [
			"Re-experiencing",
			"Christmas",
			"Completed data",
			"First entry in year",
			"First type entry in year"
		]

		state_texts = {
			"Re-experiencing": "Re-experienced",
			"Completed data": "Completed the data"
		}

		# Iterate through the states keys
		for key in keys:
			# If the state is True
			if dictionary["Data"]["States"][key] == True:
				# If the key has a different state text, get it
				if key in state_texts:
					key = state_texts[key]

				state = True

				# Define the state dictionary
				states_dictionary["States"][key] = state

				# Define the state texts of the current state dictionary
				states_dictionary["Texts"][key] = {}

				for language in self.languages["small"]:
					text = ""

					if key != "First type entry in year":
						text_key = key.lower().replace(" ", "_")

						if text_key in self.JSON.Language.texts:
							text = self.JSON.Language.texts[text_key][language]

						else:
							text = self.texts[text_key][language]

					if key == "First type entry in year":
						entry_item = dictionary["Type"]["Items"][language].lower()

						text = self.JSON.Language.texts["first_{}_in_year"][language].format(entry_item)

					states_dictionary["Texts"][key][language] = text

		return states_dictionary

	def Define_Options(self, dictionary, options):
		for key in options:
			if type(options[key]) == dict:
				if key in dictionary and dictionary[key] != {}:
					for sub_key in dictionary[key]:
						if sub_key in options[key]:
							dictionary[key][sub_key] = options[key][sub_key]

					for sub_key in options[key]:
						if sub_key not in dictionary[key]:
							dictionary[key][sub_key] = options[key][sub_key]

				if key not in dictionary or dictionary[key] == {}:
					dictionary[key] = options[key]

			if type(options[key]) in [str, list]:
				dictionary[key] = options[key]

		return dictionary

	def Define_Data_Titles(self, dictionary):
		data = dictionary["Data"]

		if self.File.Exist(data["folders"]["details"]) == True:
			data["details"] = self.File.Dictionary(data["folders"]["details"])

			# Define titles key
			data["Titles"] = {
				"Original": data["details"][self.JSON.Language.language_texts["title, title()"]],
				"Sanitized": data["details"][self.JSON.Language.language_texts["title, title()"]],
			}

			data["Titles"]["Language"] = data["Titles"]["Original"]

			# If the "romanized_name" key exists inside the data details, define the romanized name and ja name
			if self.JSON.Language.language_texts["romanized_name"] in data["details"]:
				if self.JSON.Language.language_texts["romanized_name"] in data["details"]:
					data["Titles"]["Romanized"] = data["details"][self.JSON.Language.language_texts["romanized_name"]]
					data["Titles"]["Language"] = data["Titles"]["Romanized"]

				if "Romanized" in data["Titles"]:
					data["Titles"]["Sanitized"] = data["Titles"]["Romanized"]

				data["Titles"]["ja"] = data["details"][self.JSON.Language.language_texts["title, title()"]]

			if " (" in data["Titles"]["Original"] and " (" not in data["Titles"]["Language"]:
				data["Titles"]["Language"] = data["Titles"]["Language"] + " (" + data["Titles"]["Original"].split(" (")[-1]

				if self.user_language in data["Titles"]:
					data["Titles"][self.user_language] = data["Titles"][self.user_language] + " (" + data["Titles"]["Original"].split(" (")[-1]

			# Define data titles per language
			for language in self.languages["small"]:
				language_name = self.JSON.Language.texts["language_name"][language][self.user_language]

				for key in data["details"]:
					if language_name == key:
						data["Titles"][language] = data["details"][language_name]

			data["Titles"]["Language"] = data["Titles"]["Original"]

			if self.user_language in data["Titles"]:
				data["Titles"]["Language"] = data["Titles"][self.user_language]

			if self.user_language not in data["Titles"] and "Romanized" in data["Titles"]:
				data["Titles"]["Language"] = data["Titles"]["Romanized"]

			# Sanitize data title
			data["Titles"]["Sanitized"] = self.Sanitize_Title(data["Titles"]["Sanitized"])

		return dictionary

	def Sanitize_Title(self, title):
		if len(title) > 1 and title[0] + title[1] == ": ":
			title = title[2:]

		if ". " in title:
			title = title.replace(". ", " ")

		elif "." in title:
			title = title.replace(".", "")

		title = self.Sanitize(title, restricted_characters = True)

		return title

	def Get_Language_Status(self, status):
		return_english = False

		if status in self.texts["statuses, type: list"][self.user_language]:
			return_english = True

		w = 0
		for english_status in self.texts["statuses, type: list"]["en"]:
			# Return the user language status
			if return_english == False and english_status == status:
				status_to_return = self.texts["statuses, type: list"][self.user_language][w]

			# Return the English status
			if return_english == True and status == self.texts["statuses, type: list"][self.user_language][w]:
				status_to_return = english_status

			w += 1

		return status_to_return

	def Change_Status(self, dictionary, status = ""):
		if status == "":
			status = self.language_texts["registered, title()"]

		# Update the status key in the data details
		dictionary["Data"]["details"][self.JSON.Language.language_texts["status, title()"]] = status

		# Update the data details file
		self.File.Edit(dictionary["Data"]["folders"]["details"], self.Text.From_Dictionary(dictionary["Data"]["details"]), "w")

		self.Check_Status(dictionary)

	def Check_Status(self, dictionary):
		data_type = dictionary

		if "Type" in dictionary and "JSON" in dictionary["Type"]:
			data_type = dictionary["Type"]

			self.language_status = dictionary["Data"]["details"][self.JSON.Language.language_texts["status, title()"]]

			# Get the English status from the language status of the data details
			status = self.Get_Language_Status(self.language_status)

		dictionary["JSON"] = self.JSON.To_Python(data_type["Folders"]["information"]["info"])

		# Update the number of data
		dictionary["JSON"]["Number"] = len(dictionary["JSON"]["Titles"])

		# Sort the titles list
		dictionary["JSON"]["Titles"] = sorted(dictionary["JSON"]["Titles"], key = str.lower)

		titles = []

		if "Type" in dictionary and "JSON" not in dictionary["Type"]:
			titles.extend(dictionary["JSON"]["Titles"])

		if "Type" in dictionary and "JSON" in dictionary["Type"]:
			titles.append(dictionary["Data"]["Title"])

		# Iterate through the statuses list
		for experiencing_status in self.texts["statuses, type: list"]["en"]:
			for data_title in titles:
				if "Type" in dictionary and "JSON" not in dictionary["Type"]:
					folder = data_type["Folders"]["information"]["root"] + self.Sanitize_Title(data_title) + "/"
					details_file = folder + self.JSON.Language.language_texts["details, title()"] + ".txt"
					details = self.File.Dictionary(details_file)

					self.language_status = details[self.JSON.Language.language_texts["status, title()"]]

					# Get the English status from the language status of the data details
					status = self.Get_Language_Status(self.language_status)

				# If the data status is equal to the experiencing status
				# And the data is not in the correct status list, add it to the list
				if status == experiencing_status and data_title not in dictionary["JSON"]["Status"][experiencing_status]:
					dictionary["JSON"]["Status"][experiencing_status].append(data_title)

				# If the data status is not equal to the experiencing status
				# And the data is in the wrong experiencing status list, remove it from the list
				if status != experiencing_status and data_title in dictionary["JSON"]["Status"][experiencing_status]:
					dictionary["JSON"]["Status"][experiencing_status].remove(data_title)

			# Sort the data list
			dictionary["JSON"]["Status"][experiencing_status] = sorted(dictionary["JSON"]["Status"][experiencing_status], key = str.lower)

		# Update the data type "Info.json" file
		self.JSON.Edit(data_type["Folders"]["information"]["info"], dictionary["JSON"])

		return dictionary

	def Show_Information(self, dictionary):
		data = dictionary["Data"]

		print()
		print(self.large_bar)
		print()

		print(self.JSON.Language.language_texts["entry, title()"] + ":")

		key = "Original"

		if "Romanized" in self.data["Titles"]:
			key = "Romanized"

		print("\t" + self.data["Titles"][key])

		for language in self.languages["small"]:
			if language in self.data["Titles"]:
				translated_language = self.languages["full_translated"][language][self.user_language]

				print("\t" + translated_language + ":")
				print("\t" + self.data["Titles"][language])

		print()

		print(self.JSON.Language.language_texts["type, title()"] + ":")

		types = []

		for language in self.languages["small"]:
			text = "\t" + dictionary["Type"]["Plural"][language]

			if text not in types:
				types.append(text)

		for item in types:
			print(item)

		if "Entry" in dictionary:
			print()
			print(self.JSON.Language.language_texts["when, title()"] + ":")
			print("\t" + dictionary["Entry"]["Dates"]["Timezone"])

			# If there are states, show them
			if "States" in self.dictionary and self.dictionary["States"]["States"] != {}:
				print()
				print(self.JSON.Language.language_texts["states, title()"] + ":")

				for key in self.dictionary["States"]["Texts"]:
					print("\t" + self.dictionary["States"]["Texts"][key][self.user_language])

			# If the user finished experiencing, ask for input before ending execution
			print()
			print(self.large_bar)

			self.Input.Type(self.JSON.Language.language_texts["press_enter_when_you_finish_reading_the_info_summary"])

if __name__ == "__main__":
	Database()
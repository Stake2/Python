# GamePlayer.py

class GamePlayer(object):
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
		# If there is no current year variable inside the self object, get the current year variable from the "Years" module
		if hasattr(self, "current_year") == False:
			self.current_year = self.Years.current_year

		# List the contents of the root folder of the "Game Network"
		if self.folders == self.Folder.folders:
			self.folders = self.Folder.Contents(self.folders["notepad"]["networks"]["game_network"]["root"], lower_key = True)["dictionary"]

		# Define the current year folder for easier typing
		self.folders["play_history"]["current_year"] = self.folders["play_history"][self.current_year["Number"]]

	def Define_Types(self):
		self.game_types = self.JSON.To_Python(self.folders["game"]["types"])

		self.game_types.update({
			"Singular": self.game_types["Singular"],
			"Plural": self.game_types["Plural"],
			"Genders": self.JSON.Language.texts["genders, type: dict"],
			"Gender items": self.JSON.Language.texts["gender_items"],
			"Game list": {
				"Number": 0,
				"Numbers": {}
			}
		})

		# Reset the game number to 0
		if self.game_types["Game list"]["Number"] != 0:
			self.game_types["Game list"]["Number"] = 0

		# Read the root "Info.json" file
		if self.File.Contents(self.folders["information"]["info"])["lines"] != []:
			info_dictionary = self.JSON.To_Python(self.folders["information"]["info"])

		# If the root "Info.json" file is empty, add a default JSON dictionary inside it
		if self.File.Contents(self.folders["information"]["info"])["lines"] == []:
			info_dictionary = {
				"Types": self.game_types["Types"],
				"Number": 0,
				"Numbers": {}
			}

		# Iterate through the English plural types list
		i = 0
		for game_type in self.game_types["Types"]["en"]:
			key = game_type.lower().replace(" ", "_")

			language_type = self.game_types["Types"][self.user_language][i]

			# Create game type dictionary
			self.game_types[game_type] = {
				"Type": {},
				"Folders": {},
				"Status": [
					self.texts["plan_to_play, title()"]["en"],
					self.texts["playing, title()"]["en"],
					self.texts["re_playing, title()"]["en"],
					self.JSON.Language.texts["on_hold, title()"]["en"]
				],
				"Game number": 0,
				"Game list": []
			}

			# Define the game types per language
			for language in self.languages["small"]:
				self.game_types[game_type]["Type"][language] = self.game_types["Types"][language][i]

			# Create type folders
			for root_folder in ["Information", "Play History"]:
				root_key = root_folder.lower().replace(" ", "_")

				# "Game Information" folder
				if root_folder == "Information":
					self.folders[root_key][key] = {
						"root": self.folders[root_key]["root"] + language_type + "/"
					}

					self.Folder.Create(self.folders[root_key][key]["root"])

				# "Play History Per Game Type" folder
				if root_folder == "Play History":
					self.folders[root_key]["current_year"]["per_game_type"][key] = {
						"root": self.folders[root_key]["current_year"]["per_game_type"]["root"] + game_type + "/"
					}

					self.Folder.Create(self.folders[root_key]["current_year"]["per_game_type"][key]["root"])

					# Create "Sessions.json" file
					self.folders[root_key]["current_year"]["per_game_type"][key]["sessions"] = self.folders[root_key]["current_year"]["per_game_type"][key]["root"] + "Sessions.json"
					self.File.Create(self.folders[root_key]["current_year"]["per_game_type"][key]["sessions"])

					# Create "Entry list.txt" file
					self.folders[root_key]["current_year"]["per_game_type"][key]["entry_list"] = self.folders[root_key]["current_year"]["per_game_type"][key]["root"] + "Entry list.txt"
					self.File.Create(self.folders[root_key]["current_year"]["per_game_type"][key]["entry_list"])

					# Create "Files" folder 
					self.folders[root_key]["current_year"]["per_game_type"][key]["files"] = {
						"root": self.folders[root_key]["current_year"]["per_game_type"][key]["root"] + "Files/"
					}

					self.Folder.Create(self.folders[root_key]["current_year"]["per_game_type"][key]["files"]["root"])

			# Define game type folders and files
			self.game_types[game_type]["Folders"] = {
				"information": self.folders["information"][key],
				"per_game_type": self.folders["play_history"]["current_year"]["per_game_type"][key]
			}

			# Define the "Info.json" file
			self.game_types[game_type]["Folders"]["information"]["info"] = self.game_types[game_type]["Folders"]["information"]["root"] + "Info.json"
			self.File.Create(self.game_types[game_type]["Folders"]["information"]["info"])

			# Read the "Info.json" file
			if self.File.Contents(self.game_types[game_type]["Folders"]["information"]["info"])["lines"] != []:
				self.game_types[game_type]["JSON"] = self.JSON.To_Python(self.game_types[game_type]["Folders"]["information"]["info"])

			# If the "Info.json" file is empty, add a default JSON dictionary inside it
			if self.File.Contents(self.game_types[game_type]["Folders"]["information"]["info"])["lines"] == []:
				# Define the default JSON dictionary
				self.game_types[game_type]["JSON"] = {
					"Number": 0,
					"Titles": [],
					"Status": {}
				}

				# Create an empty list for each status
				for english_status in self.texts["statuses, type: list"]["en"]:
					self.game_types[game_type]["json"]["Status"][english_status] = []

			# Update the number of games inside the json dictionary
			self.game_types[game_type]["JSON"]["Number"] = len(self.game_types[game_type]["JSON"]["Titles"])

			# Edit the "Info.json" file with the new dictionary
			self.JSON.Edit(self.game_types[game_type]["Folders"]["information"]["info"], self.game_types[game_type]["JSON"])

			# Add the game number to the game number
			self.game_types["Game list"]["Number"] += self.game_types[game_type]["JSON"]["Number"]

			# Add the game number to the root game number
			info_dictionary["Numbers"][game_type] = self.game_types[game_type]["JSON"]["Number"]

			# Add the media number to the media type media numbers
			self.game_types["Game list"]["Numbers"][game_type] = self.game_types[game_type]["JSON"]["Number"]

			# Get the game list with "Playing" and "Re-playing" statuses
			self.game_types[game_type]["Game list"] = self.Get_Game_List(self.game_types[game_type])

			# Define the game number of the game type
			self.game_types[game_type]["Game number"] = len(self.game_types[game_type]["Game list"])

			add_status = True

			# Add status to the "game list option" list if add_status is True
			if add_status == True:
				self.game_types[game_type]["Game list (option)"] = self.game_types[game_type]["Game list"].copy()

				d = 0
				for game in self.game_types[game_type]["Game list"]:
					for status in self.game_types[game_type]["Status"]:
						if game in self.game_types[game_type]["JSON"]["Status"][status]:
							language_status = self.Get_Language_Status(status)

					items = [
						self.game_types[game_type]["Game list (option)"][d],
						language_status
					]

					self.game_types[game_type]["Game list (option)"][d] = "{} - ({})".format(*items)

					d += 1

			# Remove the "JSON" key
			self.game_types[game_type].pop("JSON")

			# Add the game list length numbers to the game types list to show on select game type
			for language in self.languages["small"]:
				for text_type in ["Singular", "Plural"]:
					self.game_types[game_type][text_type]["Show"] = self.types[game_type][text_type][self.user_language] + " (" + str(len(self.game_types[game_type]["Game list"])) + ")"

			# Update the "Show" text
			self.game_types[game_type]["Texts"]["Show"] = self.Text.By_Number(self.game_types[game_type]["Game list"], self.game_types[game_type]["Singular"]["Show"], self.game_types[game_type]["Plural"]["Show"])

			i += 1

		# Write the game types dictionary into the "Types.json" file
		self.JSON.Edit(self.folders["game"]["types"], self.game_types)

		# Update the game list inside the root "Info.json" dictionary
		info_dictionary.update(self.game_types["Game list"])

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
					"Sessions": 0
				},
				"Years": []
			},
			"Sessions": deepcopy(self.template),
			"Session": {},
			"Game Type": {}
		}

		if self.File.Contents(self.folders["play_history"]["history"])["lines"] != [] and self.JSON.To_Python(self.folders["play_history"]["history"])["Years"] != []:
			# Get the History dictionary from file
			self.dictionaries["History"] = self.JSON.To_Python(self.folders["play_history"]["history"])

		# If the current year is not inside the "History" years list, add it to the list
		if self.current_year["Number"] not in self.dictionaries["History"]["Years"]:
			self.dictionaries["History"]["Years"].append(self.current_year["Number"])

		# Update the number of years with the length of the years list
		self.dictionaries["History"]["Numbers"]["Years"] = len(self.dictionaries["History"]["Years"])

		sessions = 0

		# Update the number of sessions of all years
		for year in range(self.date["year"], self.date["year"] + 1):
			year = str(year)

			# Get the year folder and the entries file
			year_folder = self.folders["play_history"]["root"] + year + "/"
			entries_file = year_folder + "Sessions.json"

			# If the file exists and it is not empty
			if self.File.Exist(entries_file) == True and self.File.Contents(entries_file)["lines"] != []:
				# Add the number of lines of the file to the local number of entries
				sessions += self.JSON.To_Python(entries_file)["Numbers"]["Total"]

			# Add the year to the Years list if it is not inside it
			if year not in self.dictionaries["History"]["Years"]:
				self.dictionaries["History"]["Years"].append(year)

		# Sort the Years list
		self.dictionaries["History"]["Years"] = sorted(self.dictionaries["History"]["Years"], key = str.lower)

		# Define the number of Entries of all years as the local number of entries
		self.dictionaries["History"]["Numbers"]["Sessions"] = sessions

		# Update the "History.json" file with the new History dictionary
		self.JSON.Edit(self.folders["play_history"]["history"], self.dictionaries["History"])

		# If the "Sessions.json" is not empty and has entries, get the Sessions dictionary from it
		if self.File.Contents(self.folders["play_history"]["current_year"]["sessions"])["lines"] != [] and self.JSON.To_Python(self.folders["play_history"]["current_year"]["sessions"])["Entries"] != []:
			self.dictionaries["Sessions"] = self.JSON.To_Python(self.folders["play_history"]["current_year"]["sessions"])

		# Iterate through the English game types list
		for plural_game_type in self.game_types["Types"]["en"]:
			key = plural_game_type.lower().replace(" ", "_")

			# Define default type dictionary
			self.dictionaries["Game Type"][plural_game_type] = deepcopy(self.template)

			# If the game type "Sessions.json" is not empty, get the game type Sessions dictionary from it
			if self.File.Contents(self.folders["play_history"]["current_year"]["per_game_type"][key]["sessions"])["lines"] != [] and self.JSON.To_Python(self.folders["play_history"]["current_year"]["per_game_type"][key]["sessions"])["Entries"] != []:
				self.dictionaries["Game Type"][plural_game_type] = self.JSON.To_Python(self.folders["play_history"]["current_year"]["per_game_type"][key]["sessions"])

			# Add the plural game type number to the root numbers if it does not exist in there
			if plural_game_type not in self.dictionaries["Sessions"]["Numbers"]:
				self.dictionaries["Sessions"]["Numbers"][plural_game_type] = 0

			# Else, define the root total number per game type as the number inside the Sessions dictionary per game type
			if plural_game_type in self.dictionaries["Sessions"]["Numbers"]:
				self.dictionaries["Sessions"]["Numbers"][plural_game_type] = self.dictionaries["Game Type"][plural_game_type]["Numbers"]["Total"]

			# Update the per game type "Sessions.json" file with the updated per game type Sessions dictionary
			self.JSON.Edit(self.folders["play_history"]["current_year"]["per_game_type"][key]["sessions"], self.dictionaries["Game Type"][plural_game_type])

		# Update the "Sessions.json" file with the updated Sessions dictionary
		self.JSON.Edit(self.folders["play_history"]["current_year"]["sessions"], self.dictionaries["Sessions"])

	def Get_Game_List(self, dictionary, status = None):
		'''

		Returns a game list of a specific game type that contains a game status

			Parameters:
				dictionary (dict): a game_type dictionary containing the game type folders
				status (str or list): a status string or list used to get the game that has that status

			Returns:
				game_list (list): The game list that contains the game that has the passed status string or list

		'''

		# Get the status list from the game type dictionary
		status_list = dictionary["Status"].copy()

		# If the status parameter is not None, use it as the status
		if status != None:
			status_list = status

		# If the type of the status list is string, make it a list of only the string
		if type(status_list) == str:
			status_list = [status_list]

		# Get the game type "Info.json" file and read it
		dictionary["JSON"] = self.JSON.To_Python(dictionary["Folders"]["information"]["info"])

		# Define the empty game list
		game_list = []

		# Add the game of each status to the game list
		for status in status_list:
			if type(status) == dict:
				status = status["en"]

			game_list.extend(dictionary["JSON"]["Status"][status])

		# Sort the game list
		game_list = sorted(game_list, key = str.lower)

		return game_list

	def Select_Game_Type(self, options = None):
		dictionary = {
			"Texts": {
				"Show": self.language_texts["game_categories"],
				"Select": self.language_texts["select_one_game_category_to_play"]
			},
			"List": {
				"en": self.game_types["Plural"]["en"].copy(),
				self.user_language: self.game_types["Plural"][self.user_language].copy()
			},
			"Status": [
				self.texts["plan_to_play, title()"]["en"],
				self.texts["playing, title()"]["en"],
				self.texts["re_playing, title()"]["en"],
				self.JSON.Language.texts["on_hold, title()"]["en"]
			]
		}

		if options != None:
			dictionary = self.Define_Options(dictionary, options)

		# Get the game type game numbers
		numbers = self.JSON.To_Python(self.folders["information"]["info"])["Numbers"]

		# Add the number of game inside each game type text
		i = 0
		for plural_type in self.types["Plural"]["en"]:
			if plural_type in dictionary["List"]["en"]:
				for language in self.languages["small"]:
					dictionary["List"][language][i] = dictionary["List"][language][i] + " (" + str(numbers[plural_type]) + ")"

				i += 1

		# Select the game type
		if "option" not in dictionary and "number" not in dictionary:
			dictionary["option"] = self.Input.Select(dictionary["List"]["en"], dictionary["List"][self.user_language], show_text = dictionary["Texts"]["Show"], select_text = dictionary["Texts"]["Select"])["option"]
			dictionary["option"] = dictionary["option"].split(" (")[0]

		if "number" in dictionary:
			dictionary["option"] = dictionary["List"]["en"][dictionary["number"]]

		# Get the selected game type dictionary from the game types dictionary
		dictionary.update(self.game_types[dictionary["option"]])

		# Get the status from the options dictionary
		if "Status" in options:
			dictionary["Status"] = options["Status"]

		# Get the game list using the correct status
		dictionary["Game list"] = self.Get_Game_List(dictionary, dictionary["Status"])

		# Add the game list length numbers to the game types list to show on the select game
		for language in self.languages["small"]:
			for text_type in ["Singular", "Plural"]:
				dictionary[text_type]["Show"] = dictionary[text_type][self.user_language] + " (" + str(len(dictionary["Game list"])) + ")"

		# Update the "Show" text
		dictionary["Texts"]["Show"] = self.Text.By_Number(dictionary["Game list"], dictionary["Singular"]["Show"], dictionary["Plural"]["Show"])

		return dictionary

	def Select_Game(self, options = None):
		dictionary = {}

		if options != None:
			dictionary = self.Define_Options(dictionary, options)

		game = dictionary["Data"]

		dictionary["Texts"] = dictionary["Type"]["Texts"]

		# Define the select text
		text = dictionary["Type"]["Singular"][self.user_language]

		if "Select" in dictionary["Type"]["Singular"]:
			text = dictionary["Type"]["Singular"]["Select"]

		dictionary["Texts"]["Select"] = self.language_texts["select_one_data_to_experience"]

		# Select the game
		if "Title" not in game:
			language_options = dictionary["Type"]["Data list"]

			if "Data list (option)" in dictionary["Type"]:
				language_options = dictionary["Type"]["Data list (option)"]

			game.update({
				"Title": self.Input.Select(dictionary["Type"]["Data list"], language_options = language_options, show_text = dictionary["Texts"]["Show"], select_text = dictionary["Texts"]["Select"])["option"]
			})

		# Define the game information folder
		game["folders"] = {
			"root": dictionary["Type"]["Folders"]["information"]["root"] + self.Sanitize(game["Title"], restricted_characters = True) + "/"
		}

		# Create the folders
		for key in game["folders"]:
			folder = game["folders"][key]

			if "root" in folder:
				folder = folder["root"]

			self.Folder.Create(folder)

		file_names = [
			"Details",
			"Dates"
		]

		game["Information"] = {
			"File name": "Data",
			"Key": ""
		}

		file_names.append(game["Information"]["File name"] + ".json")

		game["Information"]["Key"] = game["Information"]["File name"].lower().replace(" ", "_")

		# Define the game text files
		for file_name in file_names:
			key = file_name.lower().replace(" ", "_").replace(".json", "")

			if key == "details":
				texts_list = self.JSON.Language.language_texts

			if key == "dates":
				texts_list = self.Date.language_texts

			if ".json" not in file_name:
				file_name = texts_list[key + ", title()"] + ".txt"

			game["folders"][key] = game["folders"]["root"] + file_name
			self.File.Create(game["folders"][key])

		if self.File.Contents(game["folders"][game["Information"]["Key"]])["lines"] != []:
			game["Information"]["Dictionary"] = self.JSON.To_Python(game["folders"][game["Information"]["Key"]])

		# Define the game details
		game["details"] = self.File.Dictionary(game["folders"]["details"])

		# Define the default game language as the user language
		game["Language"] = self.full_user_language

		# Change user language to original game language if the key exists inside the game details
		if self.JSON.Language.language_texts["original_language"] in game["details"]:
			game["Language"] = game["details"][self.JSON.Language.language_texts["original_language"]]

		if game["Language"] in list(self.languages["full"].values()):
			# Iterate through full languages list to find small language from the full language
			for small_language in self.languages["full"]:
				full_language = self.languages["full"][small_language]

				if full_language == game["Language"]:
					game["Language"] = small_language

		# Define game states dictionary
		states = {
			"Remote": False,
			"Local": False,
			"Re-experiencing": False,
			"Christmas": False,
			"Completed game": False,
			"First game session in year": False,
			"First game type session in year": False,
			"Finished experiencing": False
		}

		if "States" in game:
			game["States"].update(states)

		elif "States" not in game:
			game["States"] = states

		if self.Today_Is_Christmas == True:
			game["States"]["Christmas"] = True

		origin_types = [
			"Local",
			"Remote"
		]

		# Define the origin type state
		for key in origin_types:
			if self.JSON.Language.language_texts["origin_type"] in game["details"]:
				if game["details"][self.JSON.Language.language_texts["origin_type"]] == self.language_texts[key.lower() + ", title()"]:
					game["States"][key] = True

		game["States"]["Remote"] = False

		if self.JSON.Language.language_texts["origin_type"] not in game["details"]:
			game["States"]["Remote"] = True

			game["details"][self.JSON.Language.language_texts["origin_type"]] = self.JSON.Language.language_texts["remote, title()"]

		# Define Re-experiencing state for Re-experiencing status
		if self.JSON.Language.language_texts["status, title()"] in game["details"] and game["details"][self.JSON.Language.language_texts["status, title()"]] == self.language_texts["re_experiencing, title()"]:
			game["States"]["Re-experiencing"] = True

		dictionary = self.Define_Game_Titles(dictionary)

		return dictionary

	def Select_Game_Type_And_Game(self, options = None):
		dictionary = {
			"Type": {
				"Select": True,
				"Status": [
					self.texts["plan_to_play, title()"]["en"],
					self.texts["playing, title()"]["en"],
					self.texts["re_playing, title()"]["en"],
					self.JSON.Language.texts["on_hold, title()"]["en"]
				]
			},
			"Game": {
				"Select": True,
				"List": {}
			}
		}

		if options != None:
			dictionary = self.Define_Options(dictionary, options)

		if dictionary["Type"]["Select"] == True:
			dictionary["Type"] = self.Select_Game_Type(dictionary["Type"])

		if dictionary["Game"]["Select"] == True:
			dictionary["Game"] = self.Select_Game(dictionary)["Game"]

		return dictionary

	def Define_States_Dictionary(self, dictionary):
		states_dictionary = {
			"States": {},
			"Texts": {}
		}

		# Define the keys for the states
		keys = [
			"First session in year",
			"First game type session in year"
		]

		# Iterate through the states keys
		for key in keys:
			# If the state is True
			if dictionary["States"][key] == True:
				state = True

				# Define the state dictionary
				states_dictionary["States"][key] = state

				# Define the state texts of the current state dictionary
				states_dictionary["Texts"][key] = {}

				for language in self.languages["small"]:
					text = ""

					if key != "First game type session in year":
						text_key = key.lower().replace(" ", "_")

						if text_key in self.JSON.Language.texts:
							text = self.JSON.Language.texts[text_key][language]

						else:
							text = self.texts[text_key][language]

					if key == "First game type session in year":
						entry_item = dictionary["Type"]["Type"][language].lower()

						text = self.JSON.Language.texts["first_game_session_of_{}_category_in_year"][language].format(entry_item)

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

	def Define_Game_Titles(self, dictionary):
		game = dictionary["Data"]

		if self.File.Exist(game["folders"]["details"]) == True:
			game["details"] = self.File.Dictionary(game["folders"]["details"])

			# Define titles key
			game["Titles"] = {
				"Original": game["details"][self.JSON.Language.language_texts["title, title()"]],
				"Sanitized": game["details"][self.JSON.Language.language_texts["title, title()"]],
			}

			game["Titles"]["Language"] = game["Titles"]["Original"]

			# If the "romanized_name" key exists inside the game details, define the romanized name and ja name
			if self.JSON.Language.language_texts["romanized_name"] in game["details"]:
				if self.JSON.Language.language_texts["romanized_name"] in game["details"]:
					game["Titles"]["Romanized"] = game["details"][self.JSON.Language.language_texts["romanized_name"]]
					game["Titles"]["Language"] = game["Titles"]["Romanized"]

				if "Romanized" in game["Titles"]:
					game["Titles"]["Sanitized"] = game["Titles"]["Romanized"]

				game["Titles"]["ja"] = game["details"][self.JSON.Language.language_texts["title, title()"]]

			if " (" in game["Titles"]["Original"] and " (" not in game["Titles"]["Language"]:
				game["Titles"]["Language"] = game["Titles"]["Language"] + " (" + game["Titles"]["Original"].split(" (")[-1]

				if self.user_language in game["Titles"]:
					game["Titles"][self.user_language] = game["Titles"][self.user_language] + " (" + game["Titles"]["Original"].split(" (")[-1]

			# Define game titles per language
			for language in self.languages["small"]:
				language_name = self.JSON.Language.texts["language_name"][language][self.user_language]

				for key in game["details"]:
					if language_name == key:
						game["Titles"][language] = game["details"][language_name]

			game["Titles"]["Language"] = game["Titles"]["Original"]

			if self.user_language in game["Titles"]:
				game["Titles"]["Language"] = game["Titles"][self.user_language]

			if self.user_language not in game["Titles"] and "Romanized" in game["Titles"]:
				game["Titles"]["Language"] = game["Titles"]["Romanized"]

			# Sanitize game title
			game["Titles"]["Sanitized"] = self.Sanitize(game["Titles"]["Sanitized"], restricted_characters = True)

		return dictionary

	def Show_Information(self):
		print()
		print(self.large_bar)
		print()

		print(self.language_texts["game, title()"] + ":")

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

		for plural_type in self.dictionary["Type"]["Plural"].values():
			if "(" not in plural_type:
				print("\t" + plural_type)

		print()

		print(self.JSON.Language.language_texts["when, title()"] + ":")
		print(self.dictionaries["Entry"]["Times"]["Timezone"])
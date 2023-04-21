# GamePlayer.py

class GamePlayer(object):
	def __init__(self):
		self.Define_Basic_Variables()

		# Define module folders
		from Utility.Define_Folders import Define_Folders as Define_Folders

		Define_Folders(self)

		self.Define_Texts()

		# Import Years class
		from Years.Years import Years as Years
		self.Years = Years()

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
		self.game_types = self.JSON.To_Python(self.folders["data"]["types"])

		self.game_types.update({
			"game_list": {
				"Number": 0,
				"Numbers": {}
			}
		})

		# Reset the game number to 0
		if self.game_types["game_list"]["Number"] != 0:
			self.game_types["game_list"]["Number"] = 0

		# Read the root "Info.json" file
		if self.File.Contents(self.folders["information"]["info"])["lines"] != []:
			info_dictionary = self.JSON.To_Python(self.folders["information"]["info"])

		# If the root "Info.json" file is empty, add a default JSON dictionary inside it
		if self.File.Contents(self.folders["information"]["info"])["lines"] == []:
			info_dictionary = {
				"types": self.game_types["types"],
				"Number": 0,
				"Numbers": {}
			}

		# Iterate through English plural types list
		i = 0
		for game_type in self.game_types["types"]["en"]:
			key = game_type.lower().replace(" ", "_")

			language_type = self.game_types["types"][self.user_language][i]

			# Create game type dictionary
			self.game_types[game_type] = {
				"type": {},
				"folders": {},
				"status": [
					self.texts["playing, title()"]["en"],
					self.texts["re_playing, title()"]["en"]
				]
			}

			# Define types per language
			for language in self.languages["small"]:
				self.game_types[game_type]["type"][language] = self.game_types["types"][language][i]

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
			self.game_types[game_type]["folders"] = {
				"information": self.folders["information"][key],
				"per_game_type": self.folders["play_history"]["current_year"]["per_game_type"][key]
			}

			# Define the "Info.json" file
			self.game_types[game_type]["folders"]["information"]["info"] = self.game_types[game_type]["folders"]["information"]["root"] + "Info.json"
			self.File.Create(self.game_types[game_type]["folders"]["information"]["info"])

			# Read the "Info.json" file
			if self.File.Contents(self.game_types[game_type]["folders"]["information"]["info"])["lines"] != []:
				self.game_types[game_type]["json"] = self.JSON.To_Python(self.game_types[game_type]["folders"]["information"]["info"])

			# If the "Info.json" file is empty, add a default JSON dictionary inside it
			if self.File.Contents(self.game_types[game_type]["folders"]["information"]["info"])["lines"] == []:
				# Define the default JSON dictionary
				self.game_types[game_type]["json"] = {
					"Number": 0,
					"Titles": [],
					"Status": {}
				}

				# Create an empty list for each status
				for english_status in self.texts["statuses, type: list"]["en"]:
					self.game_types[game_type]["json"]["Status"][english_status] = []

			# Update the number of games inside the json dictionary
			self.game_types[game_type]["json"]["Number"] = len(self.game_types[game_type]["json"]["Titles"])

			# Edit the "Info.json" file with the new dictionary
			self.JSON.Edit(self.game_types[game_type]["folders"]["information"]["info"], self.game_types[game_type]["json"])

			# Add the game number to the game number
			self.game_types["game_list"]["Number"] += self.game_types[game_type]["json"]["Number"]

			# Add the game number to the root game number
			info_dictionary["Numbers"][game_type] = self.game_types[game_type]["json"]["Number"]

			# Add the media number to the media type media numbers
			self.game_types["game_list"]["Numbers"][game_type] = self.game_types[game_type]["json"]["Number"]

			# Get the game list with "Playing" and "Re-playing" statuses
			self.game_types[game_type]["game_list"] = self.Get_Game_List(self.game_types[game_type])

			# Remove the "json" key
			self.game_types[game_type].pop("json")

			i += 1

		# Write the game types dictionary into the "Types.json" file
		self.JSON.Edit(self.folders["data"]["types"], self.game_types)

		# Update the game list inside the root "Info.json" dictionary
		info_dictionary.update(self.game_types["game_list"])

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
		for plural_game_type in self.game_types["types"]["en"]:
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
		status_list = dictionary["status"].copy()

		# If the status parameter is not None, use it as the status
		if status != None:
			status_list = status

		# If the type of the status list is string, make it a list of only the string
		if type(status_list) == str:
			status_list = [status_list]

		# Get the game type "Info.json" file and read it
		dictionary["json"] = self.JSON.To_Python(dictionary["folders"]["information"]["info"])

		# Define the empty game list
		game_list = []

		# Add the game of each status to the game list
		for status in status_list:
			if type(status) == dict:
				status = status["en"]

			game_list.extend(dictionary["json"]["Status"][status])

		# Sort the game list
		game_list = sorted(game_list, key = str.lower)

		return game_list

	def Show_Game_Information(self, game_dictionary):
		print()
		print("-----")
		print()

		print(game_dictionary["show_text"] + ":")
		print(game_dictionary["game"]["name"])
		print()

		print(self.language_texts["game_folder"] + ":")
		print(game_dictionary["game"]["category"]["folder"])
		print()

		print(self.language_texts["game_file"] + ":")
		print(game_dictionary["game"]["file"])
		print()

		print(self.language_texts["game_category"] + ":")
		print(game_dictionary["game"]["category"]["names"][self.user_language])
		print()

		if "texts" in game_dictionary:
			print(self.language_texts["when_finished_playing"] + ":")
			print(game_dictionary["texts"]["Times"])
			print()

			print(self.language_texts["for_how_much_time"] + ":")
			print(game_dictionary["texts"]["Time spent"])
			print()

			print(game_dictionary["diary_slim_text"])
			print()

		print(self.large_bar)

		if "texts" in game_dictionary:
			self.Input.Type(self.JSON.Language.language_texts["press_enter_when_you_finish_reading_the_info_summary"])
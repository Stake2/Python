# Watch History.py

# Main class Watch_History that provides variables to the classes that implement it
class Watch_History(object):
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
		self.Define_Lists_And_Dictionaries()
		self.Define_Types()
		self.Define_Registry_Format()

	def Define_Basic_Variables(self):
		from Utility.Global_Switches import Global_Switches as Global_Switches

		from Utility.API import API as API
		from Utility.File import File as File
		from Utility.Folder import Folder as Folder
		from Utility.Date import Date as Date
		from Utility.Input import Input as Input
		from Utility.JSON import JSON as JSON
		from Utility.Text import Text as Text

		self.Global_Switches = Global_Switches()

		self.switches = self.Global_Switches.switches["global"]

		self.API = API()
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

		# List the contents of the root folder of the "Audiovisual Media Network"
		if self.folders == self.Folder.folders:
			self.folders = self.Folder.Contents(self.folders["notepad"]["networks"]["audiovisual_media_network"]["root"], lower_key = True)["dictionary"]

		# Audiovisual Media Network root files
		self.folders["audiovisual_media_network"]["watch_list"] = self.folders["audiovisual_media_network"]["root"] + "Watch List.txt"

		# Define the current year folder for easier typing
		self.folders["watch_history"]["current_year"] = self.folders["watch_history"][self.current_year["Number"]]

	def Define_Lists_And_Dictionaries(self):
		# Lists
		self.alternative_episode_types = [
			"OVA",
			"ONA",
			"Special",
			"Especial",
			"Shorts",
			"Curtas"
		]

		# Dictionaries
		self.remote_origins = {
			"Animes Vision": "https://animes.vision/",
			"YouTube": "https://www.youtube.com/"
		}

		self.secondary_types = {
			"Singular": {
				"Keys": [
					"season",
					"serie",
					"pilot",
					"special",
					"movie",
					"short",
					"music",
					"OVA",
					"ONA"
				]
			},
			"Plural": {
				"Keys": [
					"seasons",
					"series",
					"pilot",
					"specials",
					"movies",
					"shorts",
					"musics",
					"OVAs",
					"ONAs"
				]
			}
		}

		for item_type in ["Singular", "Plural"]:
			for language in self.languages["small"]:
				if language not in self.secondary_types[item_type]:
					self.secondary_types[item_type][language] = []

				for text_key in self.secondary_types[item_type]["Keys"]:
					# If the text key is inside the "texts" dictionary of the Language class, use it as the list
					if text_key in self.JSON.Language.texts:
						texts_list = self.JSON.Language.texts

					# If the text key is inside the "texts" dictionary of "Watch_History"
					if text_key in self.texts:
						texts_list = self.texts

					elif text_key + ", title()" in self.texts:
						texts_list = self.texts
						text_key = text_key + ", title()"

					if text_key in texts_list:
						self.secondary_types[item_type][language].append(texts_list[text_key][language].title())

					else:
						self.secondary_types[item_type][language].append(text_key)

	def Define_Types(self):
		self.media_types = self.JSON.To_Python(self.folders["data"]["types"])

		self.media_types.update({
			"Genders": self.JSON.Language.texts["genders, type: dict"],
			"Gender items": self.JSON.Language.texts["gender_items"],
			"Media list": {
				"Number": 0,
				"Numbers": {}
			}
		})

		# Read the root "Info.json" file
		if self.File.Contents(self.folders["media_info"]["info"])["lines"] != []:
			info_dictionary = self.JSON.To_Python(self.folders["media_info"]["info"])

		# If the root "Info.json" file is empty, add a default JSON dictionary inside it
		if self.File.Contents(self.folders["media_info"]["info"])["lines"] == []:
			info_dictionary = {
				"media_types": self.media_types["Plural"],
				"Number": 0,
				"Numbers": {}
			}

		# Iterate through the English plural media types list
		i = 0
		for plural_media_type in self.media_types["Plural"]["en"]:
			language_media_type = self.media_types["Plural"][self.user_language][i]

			# Create media type dictionary
			self.media_types[plural_media_type] = {
				"Singular": {},
				"Plural": {},
				"Genders": {},
				"Folders": {},
				"Subfolders": {},
				"Status": [
					self.texts["plan_to_watch, title()"]["en"],
					self.texts["watching, title()"]["en"],
					self.texts["re_watching, title()"]["en"],
					self.JSON.Language.texts["on_hold, title()"]["en"]
				],
				"Texts": {},
				"Media number": 0,
				"Media list": []
			}

			# Define the singular and plural media types
			for language in self.languages["small"]:
				for text_type in ["Singular", "Plural"]:
					self.media_types[plural_media_type][text_type][language] = self.media_types[text_type][language][i]

			# Define the select text for "Videos" media type
			if self.media_types[plural_media_type]["Plural"]["en"] == self.texts["videos, title()"]["en"]:
				self.media_types[plural_media_type]["Singular"]["select"] = self.JSON.Language.language_texts["channel, title()"]
				self.media_types[plural_media_type]["Plural"]["select"] = self.JSON.Language.language_texts["channels, title()"]

			# Define the genders
			gender = "masculine"

			if plural_media_type == self.texts["series, title()"]["en"]:
				gender = "feminine"

			for language in self.languages["small"]:
				self.media_types[plural_media_type]["Genders"][language] = self.media_types["Genders"][language][gender]

			# Create media type folders
			for root_folder in ["Media Info", "Watch History"]:
				root_key = root_folder.lower().replace(" ", "_")
				key = plural_media_type.lower().replace(" ", "_")

				# "Media Info" folder
				if root_folder == "Media Info":
					self.folders[root_key][key] = {
						"root": self.folders[root_key]["root"] + language_media_type + "/"
					}

					self.Folder.Create(self.folders[root_key][key]["root"])

				# "Watch History Per Media Type" folder
				if root_folder == "Watch History":
					self.folders[root_key]["current_year"]["per_media_type"][key] = {
						"root": self.folders[root_key]["current_year"]["per_media_type"]["root"] + plural_media_type + "/"
					}

					self.Folder.Create(self.folders[root_key]["current_year"]["per_media_type"][key]["root"])

					# Create "Entries.json" file
					self.folders[root_key]["current_year"]["per_media_type"][key]["entries"] = self.folders[root_key]["current_year"]["per_media_type"][key]["root"] + "Entries.json"
					self.File.Create(self.folders[root_key]["current_year"]["per_media_type"][key]["entries"])

					# Create "Entry list.txt" file
					self.folders[root_key]["current_year"]["per_media_type"][key]["entry_list"] = self.folders[root_key]["current_year"]["per_media_type"][key]["root"] + "Entry list.txt"
					self.File.Create(self.folders[root_key]["current_year"]["per_media_type"][key]["entry_list"])

					# Create "Files" folder
					self.folders[root_key]["current_year"]["per_media_type"][key]["files"] = {
						"root": self.folders[root_key]["current_year"]["per_media_type"][key]["root"] + "Files/"
					}

					self.Folder.Create(self.folders[root_key]["current_year"]["per_media_type"][key]["files"]["root"])

			# Define media type folders and files
			key = self.media_types[plural_media_type]["Plural"]["en"].lower().replace(" ", "_")

			self.media_types[plural_media_type]["Folders"] = {
				"media_info": self.folders["media_info"][key],
				"per_media_type": self.folders["watch_history"]["current_year"]["per_media_type"][key]
			}

			# Define the "Info.json" file
			self.media_types[plural_media_type]["Folders"]["media_info"]["info"] = self.media_types[plural_media_type]["Folders"]["media_info"]["root"] + "Info.json"
			self.File.Create(self.media_types[plural_media_type]["Folders"]["media_info"]["info"])

			# Define media type subfolders
			text = self.media_types[plural_media_type]["Singular"][self.user_language]

			if plural_media_type != self.texts["movies, title()"]["en"]:
				text = "season"

			if plural_media_type == self.texts["videos, title()"]["en"]:
				text = "serie"

			for text_type in ["Singular", "Plural"]:
				if text_type == "Plural":
					text += "s"

				self.media_types[plural_media_type]["Subfolders"][text_type] = text.capitalize()

				if text + ", title()" in self.language_texts:
					self.media_types[plural_media_type]["Subfolders"][text_type] = self.language_texts[text + ", title()"]

			# Define current "season/series" folder
			text = self.media_types[plural_media_type]["Subfolders"]["Singular"]

			if "{" not in self.JSON.Language.language_texts["current_{}"][0]:
				text = text.lower()

			self.media_types[plural_media_type]["Subfolders"]["Current"] = self.JSON.Language.language_texts["current_{}"].format(text)

			# Read the "Info.json" file
			if self.File.Contents(self.media_types[plural_media_type]["Folders"]["media_info"]["info"])["lines"] != []:
				self.media_types[plural_media_type]["JSON"] = self.JSON.To_Python(self.media_types[plural_media_type]["Folders"]["media_info"]["info"])

			# If the "Info.json" file is empty, add a default JSON dictionary inside it
			if self.File.Contents(self.media_types[plural_media_type]["Folders"]["media_info"]["info"])["lines"] == []:
				# Define the default JSON dictionary
				self.media_types[plural_media_type]["JSON"] = {
					"Number": 0,
					"Titles": [],
					"Status": {}
				}

				# Create an empty list for each status
				for english_status in self.texts["statuses, type: list"]["en"]:
					self.media_types[plural_media_type]["JSON"]["Status"][english_status] = []

			# Update the number of media inside the JSON dictionary
			self.media_types[plural_media_type]["JSON"]["Number"] = len(self.media_types[plural_media_type]["JSON"]["Titles"])

			# Sort the media titles list
			self.media_types[plural_media_type]["JSON"]["Titles"] = sorted(self.media_types[plural_media_type]["JSON"]["Titles"], key = str.lower)

			# Sort the status lists
			for english_status in self.texts["statuses, type: list"]["en"]:
				self.media_types[plural_media_type]["JSON"]["Status"][english_status] = sorted(self.media_types[plural_media_type]["JSON"]["Status"][english_status], key = str.lower)

			# Edit the "Info.json" file with the new dictionary
			self.JSON.Edit(self.media_types[plural_media_type]["Folders"]["media_info"]["info"], self.media_types[plural_media_type]["JSON"])

			# Check the "watching status" of the media list
			# Add the media inside the correct "watching status" list if it is not there already
			# Remove the media from the wrong "watching status" list if it is there
			self.media_types[plural_media_type] = self.Check_Status(self.media_types[plural_media_type])

			# Add the media number to the media number inside the media list
			self.media_types["Media list"]["Number"] += self.media_types[plural_media_type]["JSON"]["Number"]

			# Add the media number to the media type media numbers
			self.media_types["Media list"]["Numbers"][plural_media_type] = self.media_types[plural_media_type]["JSON"]["Number"]

			# Add the media number to the root media number
			info_dictionary["Numbers"][plural_media_type] = self.media_types[plural_media_type]["JSON"]["Number"]

			# Get the media list with "Watching" and "Re-watching" statuses
			self.media_types[plural_media_type]["Media list"] = self.Get_Media_List(self.media_types[plural_media_type])

			# Define the media number of the media type
			self.media_types[plural_media_type]["Media number"] = len(self.media_types[plural_media_type]["Media list"])

			self.add_status = True

			# Add status to the "media list option" list if add_status is True
			if self.add_status == True:
				self.media_types[plural_media_type]["Media list (option)"] = self.media_types[plural_media_type]["Media list"].copy()

				m = 0
				for media in self.media_types[plural_media_type]["Media list"]:
					for status in self.media_types[plural_media_type]["Status"]:
						if media in self.media_types[plural_media_type]["JSON"]["Status"][status]:
							language_status = self.Get_Language_Status(status)

					items = [
						self.media_types[plural_media_type]["Media list (option)"][m],
						language_status
					]

					self.media_types[plural_media_type]["Media list (option)"][m] = "{} - ({})".format(*items)

					m += 1

				if self.media_types[plural_media_type]["Media list (option)"] == []:
					self.media_types[plural_media_type].pop("Media list (option)")

			# Remove the "JSON" key
			self.media_types[plural_media_type].pop("JSON")

			# Add the media list length numbers to the media types list to show on the select media type
			for text_type in ["Singular", "Plural"]:
				self.media_types[plural_media_type][text_type]["Show"] = self.media_types[plural_media_type][text_type][self.user_language] + " (" + str(len(self.media_types[plural_media_type]["Media list"])) + ")"

			# Update the "Show" text
			self.media_types[plural_media_type]["Texts"]["Show"] = self.Text.By_Number(self.media_types[plural_media_type]["Media list"], self.media_types[plural_media_type]["Singular"]["Show"], self.media_types[plural_media_type]["Plural"]["Show"])

			i += 1

		if self.current_year["Number"] == str(self.date["Units"]["Year"]):
			# Write the media types dictionary into the "Media Types.json" file
			self.JSON.Edit(self.folders["data"]["types"], self.media_types)

		# Update the media list inside the root "Info.json" dictionary
		info_dictionary.update(self.media_types["Media list"])

		# Update the root "Info.json" file
		self.JSON.Edit(self.folders["media_info"]["info"], info_dictionary)

	def Define_Registry_Format(self):
		from copy import deepcopy
		import collections

		# Define the default Entries dictionary template
		self.template = {
			"Numbers": {
				"Total": 0,
				"Comments": 0
			},
			"Entries": [],
			"Dictionary": {}
		}

		self.dictionaries = {
			"History": {
				"Numbers": {
					"Years": 0,
					"Entries": 0,
					"Comments": 0
				},
				"Years": []
			},
			"Entries": deepcopy(self.template),
			"Media type": {},
			"Watched": deepcopy(self.template),
			"Root comments": {
				"Numbers": {
					"Total": 0,
					"No time": 0,
					"Years": {},
					"Type": {}
				}
			},
			"Comments": deepcopy(self.template)
		}

		if self.File.Contents(self.folders["watch_history"]["history"])["lines"] != [] and self.JSON.To_Python(self.folders["watch_history"]["history"])["Years"] != []:
			# Get the History dictionary from file
			self.dictionaries["History"] = self.JSON.To_Python(self.folders["watch_history"]["history"])

		# If the current year is not inside the "History" years list, add it to the list
		if self.current_year["Number"] not in self.dictionaries["History"]["Years"]:
			self.dictionaries["History"]["Years"].append(self.current_year["Number"])

		# Update the number of years with the length of the years list
		self.dictionaries["History"]["Numbers"]["Years"] = len(self.dictionaries["History"]["Years"])

		entries = 0

		# Update the number of entries of all years
		for year in range(2018, self.date["Units"]["Year"] + 1):
			year = str(year)

			# Get the year folder and the entries file
			year_folder = self.folders["watch_history"]["root"] + year + "/"
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

		# Define the total number of comments as the number gotten from the root comments file
		self.dictionaries["History"]["Numbers"]["Comments"] = self.JSON.To_Python(self.folders["comments"]["comments"])["Numbers"]["Total"]

		# Update the "History.json" file with the new History dictionary
		self.JSON.Edit(self.folders["watch_history"]["history"], self.dictionaries["History"])

		# Create the "Per Media Type" key inside the "Numbers" dictionary of the "Entries" dictionary
		self.dictionaries["Entries"]["Numbers"]["Per Media Type"] = {}

		# If the "Entries.json" is not empty and has entries, get the Entries dictionary from it
		if self.File.Contents(self.folders["watch_history"]["current_year"]["entries"])["lines"] != [] and self.JSON.To_Python(self.folders["watch_history"]["current_year"]["entries"])["Entries"] != []:
			self.dictionaries["Entries"] = self.JSON.To_Python(self.folders["watch_history"]["current_year"]["entries"])

		if self.File.Contents(self.folders["comments"]["comments"])["lines"] != [] and self.JSON.To_Python(self.folders["comments"]["comments"])["Numbers"]["Total"] != 0:
			# Get Comments dictionary from file
			self.dictionaries["Root comments"] = self.JSON.To_Python(self.folders["comments"]["comments"])

		# If current year is not inside the "year comment numbers" dictionary, add it to the dictionary as zero
		if self.current_year["Number"] not in self.dictionaries["Root comments"]["Numbers"]["Years"]:
			self.dictionaries["Root comments"]["Numbers"]["Years"][self.current_year["Number"]] = 0

		# Sort years list
		self.dictionaries["Root comments"]["Numbers"]["Years"] = dict(collections.OrderedDict(sorted(self.dictionaries["Root comments"]["Numbers"]["Years"].items())))

		# Update the current year comments number with the number from the comments dictionary
		self.dictionaries["Entries"]["Numbers"]["Comments"] = self.dictionaries["Root comments"]["Numbers"]["Years"][self.current_year["Number"]]

		# Iterate through the English media types list
		for plural_media_type in self.media_types["Plural"]["en"]:
			key = plural_media_type.lower().replace(" ", "_")

			# Define default media type dictionary
			self.dictionaries["Media type"][plural_media_type] = deepcopy(self.template)

			# If the media type "Entries.json" is not empty, get the media type Entries dictionary from it
			if self.File.Contents(self.folders["watch_history"]["current_year"]["per_media_type"][key]["entries"])["lines"] != [] and self.JSON.To_Python(self.folders["watch_history"]["current_year"]["per_media_type"][key]["entries"])["Entries"] != []:
				self.dictionaries["Media type"][plural_media_type] = self.JSON.To_Python(self.folders["watch_history"]["current_year"]["per_media_type"][key]["entries"])

			if self.current_year["Number"] not in self.dictionaries["Root comments"]["Numbers"]["Type"][plural_media_type]["Years"]:
				self.dictionaries["Root comments"]["Numbers"]["Type"][plural_media_type]["Years"][self.current_year["Number"]] = 0

			# Get media type comment number per year
			self.dictionaries["Media type"][plural_media_type]["Numbers"]["Comments"] = self.dictionaries["Root comments"]["Numbers"]["Type"][plural_media_type]["Years"][self.current_year["Number"]]

			self.JSON.Edit(self.folders["watch_history"]["current_year"]["per_media_type"][key]["entries"], self.dictionaries["Media type"][plural_media_type])

			if plural_media_type not in self.dictionaries["Root comments"]["Numbers"]["Type"]:
				self.dictionaries["Root comments"]["Numbers"]["Type"][plural_media_type] = {
					"Total": 0,
					"Years": {}
				}

			# If the current year is not inside the media type year comment number dictionary, add it
			if self.current_year["Number"] not in self.dictionaries["Root comments"]["Numbers"]["Type"][plural_media_type]["Years"]:
				self.dictionaries["Root comments"]["Numbers"]["Type"][plural_media_type]["Years"][self.date["Units"]["Year"]] = 0

			# Sort media type years list
			self.dictionaries["Root comments"]["Numbers"]["Type"][plural_media_type]["Years"] = dict(collections.OrderedDict(sorted(self.dictionaries["Root comments"]["Numbers"]["Type"][plural_media_type]["Years"].items())))

			# Add the plural media type number to the root numbers per media type if it does not exist in there
			if plural_media_type not in self.dictionaries["Entries"]["Numbers"]["Per Media Type"]:
				self.dictionaries["Entries"]["Numbers"]["Per Media Type"][plural_media_type] = 0

			# Else, define the root total number per media type as the number inside the Entries dictionary per media type
			if plural_media_type in self.dictionaries["Entries"]["Numbers"]["Per Media Type"]:
				self.dictionaries["Entries"]["Numbers"]["Per Media Type"][plural_media_type] = self.dictionaries["Media type"][plural_media_type]["Numbers"]["Total"]

		# Update the "Entries.json" file with the updated Entries dictionary
		self.JSON.Edit(self.folders["watch_history"]["current_year"]["entries"], self.dictionaries["Entries"])

		# Update "Comments.json" file with the updated Comments dictionary
		self.JSON.Edit(self.folders["comments"]["comments"], self.dictionaries["Root comments"])

	def Get_Media_List(self, dictionary, status = None):
		'''

		Returns a media list of a specific media type that contains a media status

			Parameters:
				dictionary (dict): a media_type dictionary containing the media type folders
				status (str or list): a status string or list used to get the media that has that status

			Returns:
				media_list (list): The media list that contains the media that has the passed status string or list

		'''

		# Get the status list from the media type dictionary
		status_list = dictionary["Status"].copy()

		# If the status parameter is not None, use it as the status
		if status != None:
			status_list = status

		# If the type of the status list is string, make it a list of only the string
		if type(status_list) == str:
			status_list = [
				status_list
			]

		# Get the media type "Info.json" file and read it
		dictionary["JSON"] = self.JSON.To_Python(dictionary["Folders"]["media_info"]["info"])

		# Define the empty media list
		media_list = []

		# Add the media of each watching status to the media list
		for status in status_list:
			if type(status) == dict:
				status = status["en"]

			media_list.extend(dictionary["JSON"]["Status"][status])

		# Sort the media list
		media_list = sorted(media_list, key = str.lower)

		return media_list

	def Select_Media_Type(self, options = None):
		dictionary = {
			"Texts": {
				"Show": self.language_texts["media_types"],
				"Select": self.language_texts["select_one_media_type_to_watch"]
			},
			"List": {
				"en": self.media_types["Plural"]["en"].copy(),
				self.user_language: self.media_types["Plural"][self.user_language].copy()
			},
			"Status": [
				self.texts["watching, title()"]["en"],
				self.texts["re_watching, title()"]["en"]
			]
		}

		if options != None:
			dictionary = self.Define_Options(dictionary, options)

		# Get the media type media numbers
		numbers = self.JSON.To_Python(self.folders["media_info"]["info"])["Numbers"]

		# Add the number of media inside each media type text
		i = 0
		for plural_media_type in self.media_types["Plural"]["en"]:
			if plural_media_type in dictionary["List"]["en"]:
				for language in self.languages["small"]:
					dictionary["List"][language][i] = dictionary["List"][language][i] + " (" + str(numbers[plural_media_type]) + ")"

				i += 1

		# Select the media type
		if "option" not in dictionary and "number" not in dictionary:
			dictionary["option"] = self.Input.Select(dictionary["List"]["en"], dictionary["List"][self.user_language], show_text = dictionary["Texts"]["Show"], select_text = dictionary["Texts"]["Select"])["option"]
			dictionary["option"] = dictionary["option"].split(" (")[0]

		if "number" in dictionary:
			dictionary["option"] = dictionary["List"]["en"][dictionary["number"]]

		# Get the selected media type dictionary from the media types dictionary
		dictionary.update(self.media_types[dictionary["option"]])

		# Get the status from the options dictionary
		if options != None and "Status" in options:
			dictionary["Status"] = options["Status"]

		# Get the media list using the correct status
		dictionary["Media list"] = self.Get_Media_List(dictionary, dictionary["Status"])

		# Add status to the "media list option" list if add_status is True
		if self.add_status == True:
			dictionary["Media list (option)"] = dictionary["Media list"].copy()

			m = 0
			for media in dictionary["Media list"]:
				for status in dictionary["Status"]:
					if media in dictionary["JSON"]["Status"][status]:
						language_status = self.Get_Language_Status(status)

				items = [
					dictionary["Media list (option)"][m],
					language_status
				]

				dictionary["Media list (option)"][m] = "{} - ({})".format(*items)

				m += 1

			if dictionary["Media list (option)"] == []:
				dictionary.pop("Media list (option)")

		# Add the media list length numbers to the media types list to show on the select media
		for language in self.languages["small"]:
			for text_type in ["Singular", "Plural"]:
				dictionary[text_type]["Show"] = dictionary[text_type][self.user_language] + " (" + str(len(dictionary["Media list"])) + ")"

		# Update the "Show" text
		dictionary["Texts"]["Show"] = self.Text.By_Number(dictionary["Media list"], dictionary["Singular"]["Show"], dictionary["Plural"]["Show"])

		return dictionary

	def Select_Media(self, options = None, item = False, watch = False, select_media_item = False):
		self.item = item

		dictionary = {}

		if options != None:
			dictionary = self.Define_Options(dictionary, options)

		media = dictionary["Media"]

		if self.item == True:
			media = dictionary["Media"]["Item"]

		dictionary["Texts"] = dictionary["Media type"]["Texts"]

		# Define the select text
		text = dictionary["Media type"]["Singular"][self.user_language]

		if "Select" in dictionary["Media type"]["Singular"]:
			text = dictionary["Media type"]["Singular"]["Select"]

		dictionary["Texts"]["Select"] = self.language_texts["select_{}_to_watch"].format(dictionary["Media type"]["Genders"][self.user_language]["a"] + " " + text)

		# Select the media
		if "Title" not in media:
			language_options = dictionary["Media type"]["Media list"]

			print(len(language_options))

			if "Media list (option)" in dictionary["Media type"]:
				language_options = dictionary["Media type"]["Media list (option)"]

			print(len(language_options))

			media.update({
				"Title": self.Input.Select(dictionary["Media type"]["Media list"], language_options = language_options, show_text = dictionary["Texts"]["Show"], select_text = dictionary["Texts"]["Select"])["option"]
			})

		sanitized_title = self.Sanitize_Title(media["Title"])

		if media["Title"] != "[" + self.JSON.Language.language_texts["finish_selection"] + "]":
			# Define media info and local media folder
			if "folders" in media:
				if "root" not in media["folders"]:
					media["folders"].update({
						"root": dictionary["Media type"]["Folders"]["media_info"]["root"] + self.Sanitize(sanitized_title, restricted_characters = True) + "/"
					})

				media["folders"].update({
					"media": {
						"root": dictionary["Media"]["folders"]["media"]["root"]
					}
				})

				if sanitized_title + "/" not in media["folders"]["media"]["root"]:
					media["folders"]["media"]["root"] += self.Sanitize(sanitized_title, restricted_characters = True) + "/"

				# Create the folders
				for key in media["folders"]:
					folder = media["folders"][key]

					if "root" in folder:
						folder = folder["root"]

					self.Folder.Create(folder)

			if "folders" not in media:
				media["folders"] = {
					"root": dictionary["Media type"]["Folders"]["media_info"]["root"] + self.Sanitize(sanitized_title, restricted_characters = True) + "/",
					"media": {
						"root": self.Folder.folders["root"]["media"]["root"] + self.Sanitize_Title(sanitized_title) + "/"
					}
				}

				# Create the folders
				for key in media["folders"]:
					folder = media["folders"][key]

					if "root" in folder:
						folder = folder["root"]

					self.Folder.Create(folder)

			file_names = [
				"Details",
				"Dates"
			]

			media["Information"] = {
				"File name": "",
				"Key": ""
			}

			# Define "[Singular media type].json" or "Season.json" file (media information file) for non-video media
			if dictionary["Media type"]["Plural"]["en"] != self.texts["videos, title()"]["en"]:
				media["Information"]["File name"] = dictionary["Media type"]["Singular"]["en"]

				if self.item == True and media["Title"] != dictionary["Media"]["Title"] and dictionary["Media type"]["Plural"]["en"] != self.texts["movies, title()"]["en"]:
					media["Information"]["File name"] = "Season"

				file_names.append(media["Information"]["File name"] + ".json")

			# Define "Channel.json" or "Playlist.json" file for video media
			if dictionary["Media type"]["Plural"]["en"] == self.texts["videos, title()"]["en"]:
				media["Information"]["File name"] = "Channel"

				if self.item == True:
					media["Information"]["File name"] = "Playlist"

				file_names.append(media["Information"]["File name"] + ".json")

			media["Information"]["Key"] = media["Information"]["File name"].lower().replace(" ", "_")

			# Define the media text files
			for file_name in file_names:
				key = file_name.lower().replace(" ", "_").replace(".json", "")

				if key == "details":
					texts_list = self.JSON.Language.language_texts

				if key == "dates":
					texts_list = self.Date.language_texts

				if ".json" not in file_name:
					file_name = texts_list[key + ", title()"] + ".txt"

				media["folders"][key] = media["folders"]["root"] + file_name
				self.File.Create(media["folders"][key])

			if self.File.Contents(media["folders"][media["Information"]["Key"]])["lines"] != []:
				media["Information"]["Dictionary"] = self.JSON.To_Python(media["folders"][media["Information"]["Key"]])

			# Define the media details
			media["Details"] = self.File.Dictionary(media["folders"]["details"])

			if self.item == False:
				# Define the default media language as the user language
				media["Language"] = self.full_user_language

				# Define the media language as "日本語" (Nihongo, Japanese) for anime media
				if dictionary["Media type"]["Plural"]["en"] == self.texts["animes, title()"]["en"]:
					media["Language"] = "日本語"

				# Define the default media language as the user language for video media
				if dictionary["Media type"]["Plural"]["en"] == self.texts["videos, title()"]["en"]:
					media["Language"] = self.full_user_language

				# Change user language to original media language if the key exists inside the media details
				if self.JSON.Language.language_texts["original_language"] in media["Details"]:
					media["Language"] = media["Details"][self.JSON.Language.language_texts["original_language"]]

				if media["Language"] in list(self.languages["full"].values()):
					# Iterate through full languages list to find small language from the full language
					for small_language in self.languages["full"]:
						full_language = self.languages["full"][small_language]

						if full_language == media["Language"]:
							media["Language"] = small_language

				# Define media states dictionary
				states = {
					"Remote": False,
					"Local": False,
					"Video": False,
					"Series media": True,
					"Episodic": False,
					"Single unit": False,
					"Replace title": False,
					"Media item list": False,
					"Dubbing": {
						"Has dubbing": False,
						"Dubbed to the media title": False,
						"Watch dubbed": False
					},
					"Re-watching": False,
					"Christmas": False,
					"Commented": False,
					"Completed media": False,
					"Completed media item": False,
					"First entry in year": False,
					"First media type entry in year": False,
					"Finished watching": False
				}

				if "States" in media:
					media["States"].update(states)

				elif "States" not in media:
					media["States"] = states

				if self.Today_Is_Christmas == True:
					media["States"]["Christmas"] = True

				origin_types = [
					"Local",
					"Remote"
				]

				# Define the origin type state
				for key in origin_types:
					if self.JSON.Language.language_texts["origin_type"] in media["Details"]:
						if media["Details"][self.JSON.Language.language_texts["origin_type"]] == self.JSON.Language.language_texts[key.lower() + ", title()"]:
							media["States"][key] = True

				media["States"]["Remote"] = False

				if self.JSON.Language.language_texts["origin_type"] not in media["Details"]:
					media["States"]["Remote"] = True

					media["Details"][self.JSON.Language.language_texts["origin_type"]] = self.JSON.Language.language_texts["remote, title()"]

				# Define video state for videos
				if dictionary["Media type"]["Plural"]["en"] == self.texts["videos, title()"]["en"]:
					media["States"]["Video"] = True
					media["States"]["Episodic"] = False

				if self.JSON.Language.language_texts["episodic, title()"] in media["Details"]:
					media["States"]["Episodic"] = self.Input.Define_Yes_Or_No(media["Details"][self.JSON.Language.language_texts["episodic, title()"]])

				# Define single unit state
				if self.language_texts["single_unit"] in media["Details"]:
					media["States"]["Single unit"] = self.Input.Define_Yes_Or_No(media["Details"][self.language_texts["single_unit"]])

				# Define non-series media state for movies
				if dictionary["Media type"]["Plural"]["en"] == self.texts["movies, title()"]["en"]:
					media["States"]["Series media"] = False

				if media["States"]["Video"] == True:
					dictionary["Media"]["folders"]["channel"] = dictionary["Media"]["folders"]["root"] + "Channel.json"
					self.File.Create(dictionary["Media"]["folders"]["channel"])

					if self.File.Contents(dictionary["Media"]["folders"]["channel"])["lines"] == []:
						# Get channel information
						dictionary["Media"]["Channel"] = self.Get_YouTube_Information("channel", dictionary["Media"]["Details"]["ID"])

						# Define channel date
						channel_date = self.Date.From_String(dictionary["Media"]["Channel"]["Date"])

						# Update "Date" key of media details
						dictionary["Media"]["Details"][self.Date.language_texts["start_date"]] = channel_date["Formats"]["HH:MM DD/MM/YYYY"]

						# Update "Year" key of media details
						dictionary["Media"]["Details"][self.Date.language_texts["year, title()"]] = channel_date["Units"]["Year"]

						# Update media details dictionary
						self.File.Edit(dictionary["Media"]["folders"]["details"], self.Text.From_Dictionary(dictionary["Media"]["Details"]), "w")

						# Update "Channel.json" file
						self.JSON.Edit(dictionary["Media"]["folders"]["channel"], dictionary["Media"]["Channel"])

					else:
						# Get channel information
						dictionary["Media"]["Channel"] = self.JSON.To_Python(dictionary["Media"]["folders"]["channel"])

				# Define remote origin for animes or videos media type
				if self.JSON.Language.language_texts["remote_origin"] not in dictionary["Media"]["Details"]:
					remote_origin = "None"

					if dictionary["Media type"]["Plural"]["en"] == self.texts["animes, title()"]["en"]:
						remote_origin = "Animes Vision"

					if dictionary["Media type"]["Plural"]["en"] == self.texts["videos, title()"]["en"]:
						remote_origin = "YouTube"

					if remote_origin != "None":
						dictionary["Media"]["Details"][self.JSON.Language.language_texts["remote_origin"]] = remote_origin

				# Define Re-watching state for Re-watching status
				if self.JSON.Language.language_texts["status, title()"] in media["Details"] and media["Details"][self.JSON.Language.language_texts["status, title()"]] == self.language_texts["re_watching, title()"]:
					media["States"]["Re-watching"] = True

				media["Episode"] = {
					"Title": "",
					"Titles": {},
					"Sanitized": "",
					"Number": 1,
					"Number text": "1",
					"Separator": ""
				}

				if media["States"]["Remote"] == True or self.JSON.Language.language_texts["remote_origin"] in media["Details"]:
					media["Episode"]["Remote"] = {
						"Title": "",
						"Link": "",
						"Code": ""
					}

				media["Episodes"] = {
					"Number": 0
				}

			dictionary = self.Define_Media_Titles(dictionary, self.item)

			if self.item == False:
				dictionary = self.Define_Media_Item(dictionary, watch = watch, select_media_item = select_media_item)

		return dictionary

	def Define_Media_Item(self, dictionary, watch = False, media_item = None, select_media_item = False):
		from copy import deepcopy

		# Get the class that called the function
		import inspect

		self.caller = inspect.stack()[3][1].split("\\")[-2]

		# If the media is series media
		if dictionary["Media"]["States"]["Series media"] == True:
			# Define the media items dictionary with the folders and number keys
			dictionary["Media"]["Items"] = {
				"folders": {
					"root": dictionary["Media"]["folders"]["root"] + dictionary["Media type"]["Subfolders"]["Plural"] + "/"
				},
				"Number": 1
			}

			# If the media items folder exists
			if self.Folder.Exist(dictionary["Media"]["Items"]["folders"]["root"]) == True or dictionary["Media"]["States"]["Media item list"] == True:
				# The media has a media items list
				dictionary["Media"]["States"]["Media item list"] = True

				# Iterate through item type keys
				for name in ["List", "Current"]:
					key = name

					if name == "List":
						key = "Plural"

					# Define the item type text file
					dictionary["Media"]["Items"]["folders"][name.lower()] = dictionary["Media"]["Items"]["folders"]["root"] + dictionary["Media type"]["Subfolders"][key] + ".txt"
					self.File.Create(dictionary["Media"]["Items"]["folders"][name.lower()])

					# Get the contents of the text file
					dictionary["Media"]["Items"][name] = self.File.Contents(dictionary["Media"]["Items"]["folders"][name.lower()])["lines"]

					# If the contents is not empty and the item type is "current"
					if dictionary["Media"]["Items"][name] != [] and name == "Current":
						# Define the contents as the first line of the text file
						dictionary["Media"]["Items"][name] = dictionary["Media"]["Items"][name][0]

					# If the item type is "list"
					if name == "List":
						# Define the items number as the number of lines of the text file
						dictionary["Media"]["Items"]["Number"] = len(dictionary["Media"]["Items"]["List"])

				# Define media item folders
				for name in dictionary["Media"]["Items"]["List"]:
					name = self.Sanitize_Title(name)

					dictionary["Media"]["Items"]["folders"][name] = dictionary["Media"]["Items"]["folders"]["root"] + name + "/"
					self.Folder.Create(dictionary["Media"]["Items"]["folders"][name])

				# Define current media item
				title = dictionary["Media"]["Items"]["Current"]

				show_text = self.Text.Capitalize(dictionary["Media type"]["Subfolders"]["Plural"])
				select_text = self.language_texts["select_a_season"]

				items_list = dictionary["Media"]["Items"]["List"].copy()

				# Define show and select text for video media
				if dictionary["Media"]["States"]["Video"] == True:
					show_text = self.Text.Capitalize(self.language_texts["video_series"])
					select_text = self.language_texts["select_a_youtube_video_series"]

				# Iterate through media items list
				for media_list_item in dictionary["Media"]["Items"]["List"].copy():
					folders = {
						"root": dictionary["Media"]["Items"]["folders"]["root"] + self.Sanitize_Title(media_list_item) + "/"
					}

					# Define details file
					folders["details"] = folders["root"] + self.JSON.Language.language_texts["details, title()"] + ".txt"

					# Read details file
					details = self.File.Dictionary(folders["details"])

					# If the media item is a single unit media item and the "Type" key is inside the details
					if self.JSON.Language.language_texts["type, title()"] in details:
						# Define the empty secondary types list
						if "Secondary types" not in dictionary["Media"]["Items"]:
							dictionary["Media"]["Items"]["Secondary types"] = {}

						for item_type in ["Singular", "Plural"]:
							if item_type not in dictionary["Media"]["Items"]["Secondary types"]:
								dictionary["Media"]["Items"]["Secondary types"][item_type] = {}

							for language in self.languages["small"]:
								if language not in dictionary["Media"]["Items"]["Secondary types"][item_type]:
									dictionary["Media"]["Items"]["Secondary types"][item_type][language] = []

						# Iterate through the secondary type keys list
						i = 0
						for secondary_type in self.secondary_types["Singular"][self.user_language]:
							# If the type inside the media item details is equal to the singular type
							if details[self.JSON.Language.language_texts["type, title()"]] == secondary_type:
								for item_type in ["Singular", "Plural"]:
									for language in self.languages["small"]:
										secondary_type = self.secondary_types[item_type][language][i]

										if secondary_type not in dictionary["Media"]["Items"]["Secondary types"][item_type][language]:
											# Add the item type to the secondary types list
											dictionary["Media"]["Items"]["Secondary types"][item_type][language].append(secondary_type)

							i += 1

					# If the "Status" key is present inside the details dictionary and the status is "Completed", remove the media item from the media items list
					if self.JSON.Language.language_texts["status, title()"] in details and details[self.JSON.Language.language_texts["status, title()"]] == self.JSON.Language.language_texts["completed, title()"]:
						items_list.remove(media_list_item)

					if self.caller == "Fill_Media_Files" and self.language_texts["single_unit"] not in details and dictionary["Media"]["States"]["Video"] == False:
						# Define titles folder
						folders["titles"] = {
							"root": folders["root"] + self.JSON.Language.language_texts["titles, title()"] + "/"
						}

						# Define titles files
						for language in self.languages["small"]:
							full_language = self.languages["full"][language]

							folders["titles"][language] = folders["titles"]["root"] + full_language + ".txt"

						# Remove media item from the media items list if its titles file is filled (for "Fill_Media_Files")
						if self.File.Contents(folders["titles"]["en"])["length"] > 0:
							items_list.remove(media_list_item)

					if self.language_texts["single_unit"] in details and media_list_item in items_list:
						items_list.remove(media_list_item)

				if dictionary["Media"]["States"]["Video"] == True or select_media_item == True:
					if watch == True and len(dictionary["Media"]["Items"]["List"]) != 1:
						title = self.Input.Select(items_list, show_text = show_text, select_text = select_text)["option"]

				if media_item != None:
					title = media_item

				if watch == True and len(dictionary["Media"]["Items"]["List"]) == 1:
					print()
					print("---")
					print()
					print(self.Text.Capitalize(dictionary["Media type"]["Subfolders"]["Current"]) + ":")
					print(title)

				sanitized_title = self.Sanitize_Title(title)

				# Define media item dictionary with titles and folder
				dictionary["Media"]["Item"] = {
					"Title": title,
					"Titles": {},
					"Sanitized": sanitized_title,
					"folders": {
						"root": dictionary["Media"]["Items"]["folders"]["root"] + sanitized_title + "/"
					},
					"Number": 0
				}

				dictionary["Media"]["Episodes"]["Number"] = 0

				i = 0
				for name in dictionary["Media"]["Items"]["List"]:
					if dictionary["Media"]["Item"]["Title"] == name:
						dictionary["Media"]["Item"]["Number"] = i

					# Get media item details file
					folder = dictionary["Media"]["Items"]["folders"]["root"] + self.Sanitize_Title(name) + "/"
					details_file = folder + self.JSON.Language.language_texts["details, title()"] + ".txt"
					details = self.File.Dictionary(details_file)

					# If the item is not a single unit, add its episode number to the root episode number
					if self.language_texts["single_unit"] not in details:
						titles_folder = folder + self.JSON.Language.language_texts["titles, title()"] + "/"
						titles_file = titles_folder + self.languages["full"]["en"] + ".txt"

						dictionary["Media"]["Episodes"]["Number"] += self.File.Contents(titles_file)["length"]

					i += 1

				# Add the episode number after the "Final date" or "Start date" key or update it
				key_value = {
					"key": self.language_texts["episodes, title()"],
					"value": dictionary["Media"]["Episodes"]["Number"]
				}

				after_key = self.Date.language_texts["end_date"]

				if after_key not in dictionary["Media"]["Details"]:
					after_key = self.Date.language_texts["start_date"]

				if after_key not in dictionary["Media"]["Details"]:
					after_key = self.JSON.Language.language_texts["romanized_title"]

				if after_key not in dictionary["Media"]["Details"]:
					after_key = self.JSON.Language.language_texts["title, title()"]

				if self.JSON.Language.language_texts["id, upper()"] in dictionary["Media"]["Details"]:
					after_key = self.JSON.Language.language_texts["id, upper()"]

				dictionary["Media"]["Details"] = self.JSON.Add_Key_After_Key(dictionary["Media"]["Details"], key_value, after_key = after_key)

				# Define the key to the plural media items text
				key = dictionary["Media type"]["Subfolders"]["Plural"]

				# If the media has secondary types, define the correct key
				if "Secondary types" in dictionary["Media"]["Items"]:
					key = ""

					secondary_types = [
						dictionary["Media type"]["Subfolders"]["Plural"]
					]

					for plural_type in dictionary["Media"]["Items"]["Secondary types"]["Plural"][self.user_language]:
						if "OVA" not in plural_type and "ONA" not in plural_type:
							plural_type = plural_type.lower()

						secondary_types.append(plural_type)

					key += self.Text.List_To_Text(secondary_types)

				# Add the media subfolders plural text before the "Episodes" key or update it
				key_value = {
					"key": key,
					"value": dictionary["Media"]["Items"]["Number"]
				}

				after_key = self.language_texts["episodes, title()"]

				dictionary["Media"]["Details"] = self.JSON.Add_Key_After_Key(dictionary["Media"]["Details"], key_value, after_key = after_key, number_to_add = 0)

				# If the media has secondary types and the items list plural text key is inside the details
				if "Secondary types" in dictionary["Media"]["Items"] and dictionary["Media type"]["Subfolders"]["Plural"] in dictionary["Media"]["Details"]:
					# Remove the key
					dictionary["Media"]["Details"].pop(dictionary["Media type"]["Subfolders"]["Plural"])

				dict_ = deepcopy(dictionary["Media"]["Details"])

				if self.JSON.Language.language_texts["remote_origin"] in dict_:
					if dict_[self.JSON.Language.language_texts["remote_origin"]] == "Animes Vision":
						dict_.pop(self.JSON.Language.language_texts["remote_origin"])

					elif dict_[self.JSON.Language.language_texts["remote_origin"]] == "YouTube":
						dict_.pop(self.JSON.Language.language_texts["remote_origin"])

				# Update the media details file
				self.File.Edit(dictionary["Media"]["folders"]["details"], self.Text.From_Dictionary(dict_), "w")

				dictionary = self.Select_Media(dictionary, item = True)

				dictionary["Media"]["States"]["Single unit"] = False

				# Define the single unit state
				if self.language_texts["single_unit"] in dictionary["Media"]["Item"]["Details"]:
					dictionary["Media"]["States"]["Single unit"] = self.Input.Define_Yes_Or_No(dictionary["Media"]["Item"]["Details"][self.language_texts["single_unit"]])

				if dictionary["Media"]["States"]["Single unit"] == True:
					dictionary["Media"]["Item"]["folders"]["media"]["root"] = dictionary["Media"]["folders"]["media"]["root"]

			# If the folder of media items does not exist, define that the media has no media item list
			# And add the root media to the media items list
			if self.Folder.Exist(dictionary["Media"]["Items"]["folders"]["root"]) == False:
				dictionary["Media"]["States"]["Media item list"] = False

				dictionary["Media"]["Items"]["List"] = [
					dictionary["Media"]["Title"]
				]

		# Define media item as the media for media that has no media item list
		if dictionary["Media"]["States"]["Series media"] == False or dictionary["Media"]["States"]["Media item list"] == False:
			dictionary["Media"]["Item"] = dictionary["Media"].copy()

		# Create the "Watched" folder
		dictionary["Media"]["Item"]["folders"]["watched"] = {
			"root": dictionary["Media"]["Item"]["folders"]["root"] + self.language_texts["watched, title()"] + "/"
		}

		self.Folder.Create(dictionary["Media"]["Item"]["folders"]["watched"]["root"])

		# Create the "Watched" files
		files = [
			"Entries.json",
			"Entry list.txt"
		]

		for file in files:
			key = file.lower().split(".")[0].replace(" ", "_")

			dictionary["Media"]["Item"]["folders"]["watched"][key] = dictionary["Media"]["Item"]["folders"]["watched"]["root"] + file
			self.File.Create(dictionary["Media"]["Item"]["folders"]["watched"][key])

		# Create "Files" folder file inside "Watched" folder
		dictionary["Media"]["Item"]["folders"]["watched"]["files"] = {
			"root": dictionary["Media"]["Item"]["folders"]["watched"]["root"] + self.File.language_texts["files, title()"] + "/"
		}

		self.Folder.Create(dictionary["Media"]["Item"]["folders"]["watched"]["files"]["root"])

		# Define the "Watched" dictionary as the template
		self.dictionaries["Watched"] = deepcopy(self.template)

		# Get the "Watched" dictionary from file if the dictionary is not empty and has entries
		if self.File.Contents(dictionary["Media"]["Item"]["folders"]["watched"]["entries"])["lines"] != [] and self.JSON.To_Python(dictionary["Media"]["Item"]["folders"]["watched"]["entries"])["Entries"] != []:
			self.dictionaries["Watched"] = self.JSON.To_Python(dictionary["Media"]["Item"]["folders"]["watched"]["entries"])

		# Update the number of entries with the length of the entries list
		self.dictionaries["Watched"]["Numbers"]["Total"] = len(self.dictionaries["Watched"]["Entries"])

		# Create "Comments" folder
		dictionary["Media"]["Item"]["folders"]["comments"] = {
			"root": dictionary["Media"]["Item"]["folders"]["root"] + self.JSON.Language.language_texts["comments, title()"] + "/"
		}

		self.Folder.Create(dictionary["Media"]["Item"]["folders"]["comments"]["root"])

		# Define media comments folder comments file
		dictionary["Media"]["Item"]["folders"]["comments"]["comments"] = dictionary["Media"]["Item"]["folders"]["comments"]["root"] + self.JSON.Language.texts["comments, title()"]["en"] + ".json"
		self.File.Create(dictionary["Media"]["Item"]["folders"]["comments"]["comments"])

		# Define media item folders
		if dictionary["Media"]["States"]["Series media"] == True and dictionary["Media"]["States"]["Single unit"] == False:
			dictionary["Media"]["Item"]["folders"]["titles"] = {
				"root": dictionary["Media"]["Item"]["folders"]["root"] + self.JSON.Language.language_texts["titles, title()"] + "/",
			}

			self.Folder.Create(dictionary["Media"]["Item"]["folders"]["titles"]["root"])

			for language in self.languages["small"]:
				full_language = self.languages["full"][language]

				# Define episode titles file
				dictionary["Media"]["Item"]["folders"]["titles"][language] = dictionary["Media"]["Item"]["folders"]["titles"]["root"] + full_language + ".txt"
				self.File.Create(dictionary["Media"]["Item"]["folders"]["titles"][language])

			if dictionary["Media"]["States"]["Video"] == True:
				# Define ids file
				dictionary["Media"]["Item"]["folders"]["titles"]["ids"] = dictionary["Media"]["Item"]["folders"]["titles"]["root"] + self.JSON.Language.language_texts["ids, title()"] + ".txt"
				self.File.Create(dictionary["Media"]["Item"]["folders"]["titles"]["ids"])

			# Update "Playlist.json" file for video media type
			if dictionary["Media"]["States"]["Video"] == True and dictionary["Media"]["States"]["Media item list"] == True:
				# Get ID (origin location) from link
				if self.JSON.Language.language_texts["origin_location"] in dictionary["Media"]["Item"]["Details"] and dictionary["Media"]["Item"]["Details"][self.JSON.Language.language_texts["origin_location"]] == "?":
					dictionary["Media"]["Item"]["Details"][self.JSON.Language.language_texts["origin_location"]] = dictionary["Media"]["Item"]["Details"][self.JSON.Language.language_texts["link, title()"]].split("list=")[-1]

				dictionary["Media"]["Item"]["folders"]["playlist"] = dictionary["Media"]["Item"]["folders"]["root"] + "Playlist.json"
				self.File.Create(dictionary["Media"]["Item"]["folders"]["playlist"])

				if self.File.Contents(dictionary["Media"]["Item"]["folders"]["playlist"])["lines"] == [] and dictionary["Media"]["Item"]["Details"][self.JSON.Language.language_texts["origin_location"]] != "?":
					# Get playlist information
					dictionary["Media"]["Item"]["Playlist"] = self.Get_YouTube_Information("playlist", dictionary["Media"]["Item"]["Details"][self.JSON.Language.language_texts["origin_location"]])

					# Define playlist date variable
					dictionary["Media"]["Item"]["Playlist"]["Date"] = self.Date.From_String(dictionary["Media"]["Item"]["Playlist"]["Date"])

					playlist_date = dictionary["Media"]["Item"]["Playlist"]["Date"]

					# Get the first video date
					if self.File.Contents(dictionary["Media"]["Item"]["folders"]["titles"]["root"] + self.JSON.Language.language_texts["ids, title()"] + ".txt")["lines"] != []:
						video_id = self.File.Contents(dictionary["Media"]["Item"]["folders"]["titles"]["root"] + self.JSON.Language.language_texts["ids, title()"] + ".txt")["lines"][0]
						video_date = self.Date.From_String(self.Get_YouTube_Information("video", video_id)["Date"])

						# If the first video date is older than playlist creation date
						# Define the playlist time as the video date
						if video_date["Object"] < playlist_date["Object"]:
							dictionary["Media"]["Item"]["Playlist"]["Date"] = video_date["UTC"]["DateTime"]["Formats"]["YYYY-MM-DDTHH:MM:SSZ"]

						# Update "Date" key of media item details
						dictionary["Media"]["Item"]["Details"][self.Date.language_texts["start_date"]] = channel_date["Formats"]["HH:MM DD/MM/YYYY"]

						# Update "Year" key of media item details
						dictionary["Media"]["Item"]["Details"][self.Date.language_texts["year, title()"]] = dictionary["Media"]["Item"]["Playlist"]["Date"]["Units"]["Year"]

						# Update media item details dictionary
						self.File.Edit(dictionary["Media"]["Item"]["folders"]["details"], self.Text.From_Dictionary(dictionary["Media"]["Item"]["Details"]), "w")

					dictionary["Media"]["Item"]["Playlist"]["Date"] = playlist_date["UTC"]["DateTime"]["Formats"]["YYYY-MM-DDTHH:MM:SSZ"]

					# Update "Playlist.json" file
					self.JSON.Edit(dictionary["Media"]["Item"]["folders"]["playlist"], dictionary["Media"]["Item"]["Playlist"])

				if self.File.Contents(dictionary["Media"]["Item"]["folders"]["playlist"])["lines"] != [] and dictionary["Media"]["Item"]["Details"][self.JSON.Language.language_texts["origin_location"]] != "?":
					# Get playlist from JSON file
					dictionary["Media"]["Item"]["Playlist"] = self.JSON.To_Python(dictionary["Media"]["Item"]["folders"]["playlist"])

		folder = dictionary["Media"]["Item"]["folders"]["comments"]

		# Define the comments dictionary as the template
		self.dictionaries["Comments"] = deepcopy(self.template)

		# If the "Comments" key is inside the numbers dictionary, remove it
		if "Comments" in self.dictionaries["Comments"]["Numbers"]:
			self.dictionaries["Comments"]["Numbers"].pop("Comments")

		# If the comments file is empty or has no entries
		if self.File.Contents(folder["comments"])["lines"] == [] or self.JSON.To_Python(folder["comments"])["Entries"] == []:
			# If the media type is video
			if dictionary["Media"]["States"]["Video"] == True:
				# Define default video dictionary with "channel" and "playlist" keys
				self.dictionaries["Comments"] = {
					"Numbers": {
						"Total": 0
					},
					"Channel": {},
					"Playlist": {},
					"Entries": [],
					"Dictionary": {}
				}

				# If the media has no media item list, remove "Playlist" key from dictionary
				if dictionary["Media"]["States"]["Media item list"] == False:
					self.dictionaries["Comments"].pop("Playlist")

			file_dictionary = self.dictionaries["Comments"]

		# If the comments file is not empty and has entries, get comments dictionary from file
		if self.File.Contents(folder["comments"])["lines"] != [] and self.JSON.To_Python(folder["comments"])["Entries"] != []:
			file_dictionary = self.JSON.To_Python(folder["comments"])

			comments_dictionary = {
				"Numbers": {
					"Total": ""
				}
			}

			# Get total comments number
			if "Numbers" in file_dictionary:
				comments_dictionary["Numbers"]["Total"] = file_dictionary["Numbers"]["Total"]

			# Add the channel and playlist dictionaries to the comments dictionary
			if dictionary["Media"]["States"]["Video"] == True:
				comments_dictionary["Channel"] = file_dictionary["Channel"]

				# If the media has media item list, add the "Playlist" key to the dictionary
				if dictionary["Media"]["States"]["Media item list"] == True:
					comments_dictionary["Playlist"] = file_dictionary["Playlist"]

			# Update the dictionary with the entries and dictionary
			comments_dictionary.update({
				"Entries": file_dictionary["Entries"],
				"Dictionary": file_dictionary["Dictionary"]
			})

			# Define the media comments dictionary as the dictionary gotten from the file
			self.dictionaries["Comments"] = comments_dictionary

		if dictionary["Media"]["States"]["Video"] == True:
			# If the channel inside the comments dictionary file is not empty, define it as the dictionary channel
			if file_dictionary["Channel"] != {}:
				self.dictionaries["Comments"]["Channel"] = file_dictionary["Channel"]

			# If the channel inside the comments dictionary is empty, define it as the channel gotten from the "Channel.json" file
			if self.dictionaries["Comments"]["Channel"] == {}:
				self.dictionaries["Comments"]["Channel"] = dictionary["Media"]["Channel"]

			# If the playlist exists inside the dictionary
			if "Playlist" in self.dictionaries["Comments"]:
				# And the playlist inside the comments dictionary file is not empty, define it as the dictionary playlist
				if file_dictionary["Playlist"] != {}:
					self.dictionaries["Comments"]["Playlist"] = file_dictionary["Playlist"]

				# If the playlist inside the comments dictionary file is empty, define it as the playlist gotten from the "Playlist.json" file
				if file_dictionary["Playlist"] == {}:
					self.dictionaries["Comments"]["Playlist"] = dictionary["Media"]["Item"]["Playlist"]

		# Update the total comments number with the length of the entries list
		self.dictionaries["Comments"]["Numbers"]["Total"] = len(self.dictionaries["Comments"]["Entries"])

		# Define "Comments" dictionary inside the media item dictionary
		dictionary["Media"]["Item"]["Comments"] = deepcopy(self.dictionaries["Comments"])

		# Update "Comments.json" file
		self.JSON.Edit(folder["comments"], self.dictionaries["Comments"])

		# Get the total comment number from the comments dictionary
		self.dictionaries["Watched"]["Numbers"]["Comments"] = self.dictionaries["Comments"]["Numbers"]["Total"]

		# Define the "Watched" dictionary inside the media item dictionary
		dictionary["Media"]["Item"]["Watched"] = deepcopy(self.dictionaries["Watched"])

		# Write the default or file dictionary into the "Watched.json" file
		self.JSON.Edit(dictionary["Media"]["Item"]["folders"]["watched"]["entries"], self.dictionaries["Watched"])

		# Define the media item files
		dictionary["Media"]["Item"]["folders"]["dates"] = dictionary["Media"]["Item"]["folders"]["root"] + self.Date.language_texts["dates, title()"] + ".txt"
		self.File.Create(dictionary["Media"]["Item"]["folders"]["dates"])

		# Define the episodes dictionary
		if dictionary["Media"]["States"]["Series media"] == True:
			dictionary["Media"]["Item"]["Episodes"] = {
				"Number": 0,
				"Titles": {
					"Files": {}
				}
			}

			# Define episode number name as "EP"
			dictionary["Media"]["Episode"].update({
				"Separator": "EP"
			})

			# Or custom episode number name
			if self.language_texts["episode_number_name"] in dictionary["Media"]["Details"]:
				dictionary["Media"]["Episode"]["Separator"] = dictionary["Media"]["Details"][self.language_texts["episode_number_name"]]

			if self.language_texts["episode_number_name"] in dictionary["Media"]["Item"]["Details"]:
				dictionary["Media"]["Episode"]["Separator"] = dictionary["Media"]["Item"]["Details"][self.language_texts["episode_number_name"]]

			if dictionary["Media"]["States"]["Video"] == True:
				dictionary["Media"]["Episode"]["Separator"] = ""

			if dictionary["Media"]["States"]["Video"] == True:
				dictionary["Media"]["Item"]["Episodes"]["Titles"]["Files"]["IDs"] = dictionary["Media"]["Item"]["folders"]["titles"]["ids"]
				dictionary["Media"]["Item"]["Episodes"]["Titles"]["IDs"] = self.File.Contents(dictionary["Media"]["Item"]["Episodes"]["Titles"]["Files"]["IDs"])["lines"]

			# Define episode titles files and lists
			for language in self.languages["small"]:
				full_language = self.languages["full"][language]

				if dictionary["Media"]["States"]["Single unit"] == False:
					# Define episode titles on titles dictionary file
					dictionary["Media"]["Item"]["Episodes"]["Titles"]["Files"][language] = dictionary["Media"]["Item"]["folders"]["titles"][language]

					# Get language episode titles from file
					dictionary["Media"]["Item"]["Episodes"]["Titles"][language] = self.File.Contents(dictionary["Media"]["Item"]["Episodes"]["Titles"]["Files"][language])["lines"]

				# Iterate through episode titles
				if dictionary["Media"]["Episode"]["Separator"] != "" and dictionary["Media"]["States"]["Single unit"] == False:
					import re

					i = 1
					for episode_title in dictionary["Media"]["Item"]["Episodes"]["Titles"][language]:
						number = str(self.Text.Add_Leading_Zeroes(i))

						separator = dictionary["Media"]["Episode"]["Separator"]

						if separator == "EP" and self.JSON.Language.language_texts["episodic, title()"] not in dictionary["Media"]["Details"]:
							dictionary["Media"]["States"]["Episodic"] = True

						for alternative_episode_type in self.alternative_episode_types:
							if re.search(alternative_episode_type + " [0-9]{1,2}", episode_title) != None:
								separator = ""

								if self.JSON.Language.language_texts["episodic, title()"] not in dictionary["Media"]["Details"]:
									dictionary["Media"]["States"]["Episodic"] = True

						if self.JSON.Language.language_texts["type, title()"] in dictionary["Media"]["Item"]["Details"]:
							separator = ""

						# Add episode number name to local episode title
						episode_title = separator + number + " " + episode_title

						# Add episode number name to episode titles if the separator is not empty and the number name is not present
						if separator != "" and number not in dictionary["Media"]["Item"]["Episodes"]["Titles"][language][i - 1]:
							dictionary["Media"]["Item"]["Episodes"]["Titles"][language][i - 1] = episode_title

						i += 1

			if dictionary["Media"]["States"]["Single unit"] == True:
				dictionary["Media"]["Episode"]["Title"] = dictionary["Media"]["Item"]["Title"]
				dictionary["Media"]["Episode"]["Titles"] = dictionary["Media"]["Item"]["Titles"]

				for language in self.languages["small"]:
					if language not in dictionary["Media"]["Episode"]["Titles"]:
						dictionary["Media"]["Episode"]["Titles"][language] = self.Get_Media_Title(dictionary, item = True)

			if dictionary["Media"]["States"]["Single unit"] == False:
				# Add the episode number to the episode "Number" key
				dictionary["Media"]["Item"]["Episodes"]["Number"] = len(dictionary["Media"]["Item"]["Episodes"]["Titles"]["en"])

			# Add the episode number after the "Status" key
			key_value = {
				"key": self.language_texts["episodes, title()"],
				"value": dictionary["Media"]["Item"]["Episodes"]["Number"]
			}

			after_key = self.Date.language_texts["end_date"]

			if after_key not in dictionary["Media"]["Details"]:
				after_key = self.Date.language_texts["start_date"]

			if after_key not in dictionary["Media"]["Details"]:
				after_key = self.JSON.Language.language_texts["romanized_title"]

			if after_key not in dictionary["Media"]["Details"]:
				after_key = self.JSON.Language.language_texts["title, title()"]

			if self.JSON.Language.language_texts["id, upper()"] in dictionary["Media"]["Details"]:
				after_key = self.JSON.Language.language_texts["id, upper()"]

			dictionary["Media"]["Item"]["Details"] = self.JSON.Add_Key_After_Key(dictionary["Media"]["Item"]["Details"], key_value, after_key = after_key)

			# Update media item details file
			self.File.Edit(dictionary["Media"]["Item"]["folders"]["details"], self.Text.From_Dictionary(dictionary["Media"]["Item"]["Details"]), "w")

		if self.dictionaries["Entries"]["Numbers"]["Total"] == 0:
			dictionary["Media"]["States"]["First entry in year"] = True

		if self.dictionaries["Media type"][dictionary["Media type"]["Plural"]["en"]]["Numbers"]["Total"] == 0:
			dictionary["Media"]["States"]["First media type entry in year"] = True

		# Define media texts to be used in the "Show_Media_Information" root method
		dictionary["Media"]["texts"] = {
			"genders": dictionary["Media type"]["Genders"]
		}

		# Define the container, item, and unit texts as the media type (for movies)
		for item_type in ["container", "item", "unit"]:
			dictionary["Media"]["texts"][item_type] = dictionary["Media type"]["Singular"].copy()

		dictionary["Media"]["Item"]["Type"] = {}

		# Define the item type
		if self.JSON.Language.language_texts["type, title()"] in dictionary["Media"]["Item"]["Details"]:
			dictionary["Media"]["Item"]["Type"] = dictionary["Media"]["Item"]["Details"][self.JSON.Language.language_texts["type, title()"]]

		# Define the container, item, and unit for series media
		if dictionary["Media"]["States"]["Series media"] == True:
			# Define the unit text as the "episode" text per language
			dictionary["Media"]["texts"]["unit"] = {}

			for language in self.languages["small"]:
				dictionary["Media"]["texts"]["unit"][language] = self.texts["episode"][language]

			if dictionary["Media"]["States"]["Media item list"] == True and dictionary["Media"]["Item"]["Title"] != dictionary["Media"]["Title"]:
				dictionary["Media"]["texts"]["item"] = {}

			if dictionary["Media"]["Item"]["Type"] == {}:
				dictionary["Media"]["Item"]["Type"] = dictionary["Media"]["texts"]["item"]

			if dictionary["Media"]["Item"]["Type"] != {}:
				dict_ = {}

				i = 0
				for singular_type in self.secondary_types["Singular"][self.user_language]:
					if dictionary["Media"]["Item"]["Type"] == singular_type:
						for language in self.languages["small"]:
							singular_type = self.secondary_types["Singular"][language][i]

							dictionary["Media"]["texts"]["item"][language] = singular_type
							dictionary["Media"]["texts"]["unit"][language] = singular_type
							dict_[language] = singular_type

					i += 1

				dictionary["Media"]["Item"]["Type"] = dict_

			# Define the item text as the "season" text for media that have a media item list
			if dictionary["Media"]["States"]["Media item list"] == True and dictionary["Media"]["Item"]["Title"] != dictionary["Media"]["Title"] and dictionary["Media"]["texts"]["item"] == {}:
				for language in self.languages["small"]:
					dictionary["Media"]["texts"]["item"][language] = self.texts["season, title()"][language].lower()

					if dictionary["Media"]["States"]["Single unit"] == True:
						dictionary["Media"]["texts"]["item"][language] = self.texts["episode"][language]

			# Define the container, item, and unit texts for video series media
			if dictionary["Media"]["States"]["Video"] == True:
				for language in self.languages["small"]:
					dictionary["Media"]["texts"]["container"][language] = self.texts["youtube_channel"][language]
					dictionary["Media"]["texts"]["item"][language] = self.texts["video_serie"][language]
					dictionary["Media"]["texts"]["unit"][language] = self.texts["video"][language]

			if dictionary["Media"]["Item"]["Type"] == {}:
				dictionary["Media"]["Item"]["Type"] = dictionary["Media"]["texts"]["item"]

		dict_ = deepcopy(dictionary["Media"]["texts"])

		# Define media texts by item and gender
		for text_type in ["the", "this", "of"]:
			for key in dict_:
				if key != "genders":
					if text_type + "_" + key not in dictionary["Media"]["texts"]:
						dictionary["Media"]["texts"][text_type + "_" + key] = {}

					for language in self.languages["small"]:
						if dictionary["Media"]["texts"][key][language] not in [self.texts["season, title()"][language].lower(), self.texts["video_serie"][language]]:
							item_text = dictionary["Media type"]["Genders"][language][text_type]

						if dictionary["Media"]["texts"][key][language] in [self.texts["season, title()"][language].lower(), self.texts["video_serie"][language]]:
							for gender_key in dict_["genders"][language]:

								gender = dict_["genders"][language][gender_key]

								if text_type == gender_key:
									item_text = self.media_types["Genders"][language]["feminine"][gender_key]

						text = dictionary["Media"]["texts"][key][language].lower()

						if "youtube" in text:
							text = text.replace("youtube", "YouTube")

						dictionary["Media"]["texts"][text_type + "_" + key][language] = item_text + " " + text

		# Add "Christmas special" text to unit text
		if dictionary["Media"]["States"]["Video"] == False and self.Today_Is_Christmas == True:
			dict_ = {}

			for language in self.languages["small"]:
				dict_[language] = self.texts["christmas_special_{}"][language].format(dictionary["Media"]["texts"]["unit"][language])

			dictionary["Media"]["texts"]["unit"] = dict_

		dictionary["Media"]["States"]["Replace title"] = False

		if self.language_texts["replace_title"] in dictionary["Media"]["Item"]["Details"]:
			dictionary["Media"]["States"]["Replace title"] = True

		return dictionary

	def Select_Media_Type_And_Media(self, options = None, watch = False, select_media_item = False):
		dictionary = {
			"Media type": {
				"Select": True,
				"Status": [
					self.texts["plan_to_watch, title()"]["en"],
					self.texts["watching, title()"]["en"],
					self.texts["re_watching, title()"]["en"],
					self.JSON.Language.texts["on_hold, title()"]["en"]
				]
			},
			"Media": {
				"Select": True,
				"List": {}
			}
		}

		if options != None:
			dictionary = self.Define_Options(dictionary, options)

		if dictionary["Media type"]["Select"] == True:
			dictionary["Media type"] = self.Select_Media_Type(dictionary["Media type"])

		if dictionary["Media"]["Select"] == True:
			dictionary["Media"] = self.Select_Media(dictionary, watch = watch, select_media_item = select_media_item)["Media"]

		return dictionary

	def Define_States_Dictionary(self, dictionary):
		states_dictionary = {
			"States": {},
			"Texts": {}
		}

		# Define the keys for the states
		keys = [
			"Completed media",
			"Completed media item",
			"Watch dubbed",
			"Re-watching",
			"Christmas",
			"Commented",
			"First entry in year",
			"First media type entry in year"
		]

		state_texts = {
			"Watch dubbed": "Watched dubbed",
			"Re-watching": "Re-watched",
			"Completed media": "Completed media",
			"Completed media item": "Completed media item"
		}

		# Iterate through states keys
		for key in keys:
			# If the state is true
			if (
				key in dictionary["Media"]["States"] and dictionary["Media"]["States"][key] == True or
				key in dictionary["Media"]["States"]["Dubbing"] and dictionary["Media"]["States"]["Dubbing"][key] == True
			):
				# If the key has a different state text, get it
				if key in state_texts:
					key = state_texts[key]

				# Define the state as true
				state = True

				# If the key is the "Re-watched" key, get its state dictionary
				if key == "Re-watched":
					state = {
						"Times": dictionary["Media"]["Episode"]["re_watched"]["times"]
					}

				# Define the state dictionary
				states_dictionary["States"][key] = state

				# Define the state texts of the current state dictionary
				states_dictionary["Texts"][key] = {}

				for language in self.languages["small"]:
					text = ""

					if key != "Re-watched":
						# Make text key
						text_key = key.lower().replace(" ", "_")

						# If a underscore does not exist inside the text key, the text key is a word, then add the ", title()" text
						if "_" not in text_key:
							text_key += ", title()"

						# If the text key is inside the texts dictionary of Watch_History, get the language text from it
						if text_key in self.texts:
							language_text = self.texts[text_key][language]

						# If the text key is inside the texts dictionary of the Language class, get the language text from it
						if text_key in self.JSON.Language.texts:
							language_text = self.JSON.Language.texts[text_key][language]

						# Define the unit text
						unit = dictionary["Media"]["texts"]["unit"][language].lower()

						# Define the unit text for series media as the unit text plus the neutral "of" text, plus the lowercase container text
						if dictionary["Media"]["States"]["Series media"] == True:
							unit = dictionary["Media"]["texts"]["unit"][language] + " " + self.JSON.Language.texts["of, neutral"][language] + " " + dictionary["Media"]["texts"]["container"][language].lower()

						# Define the language text as the "first_{}_in_year" formatted with the media unit text
						if key == "First media type entry in year":
							language_text = self.JSON.Language.texts["first_{}_in_year"][language].format(unit.lower())

						# If the media is completed
						if key == "Completed media":
							# Define the "the text" as the "the" text and the container
							the_text = dictionary["Media"]["texts"]["genders"][language]["the"] + " " + dictionary["Media"]["texts"]["container"][language].lower()

						# If the media item is completed
						if key == "Completed media item":
							# Define the "the text" as the "the" text plus the item text, plus the gender "of" text, plus the container text
							the_text = self.media_types["Genders"][language]["feminine"]["the"] + " " + dictionary["Media"]["texts"]["item"][language].lower() + " " + dictionary["Media"]["texts"]["genders"][language]["of"] + " " + dictionary["Media"]["texts"]["container"][language].lower()

							if dictionary["Media"]["Item"]["Title"] == dictionary["Media"]["Title"]:
								if dictionary["Media type"]["Plural"]["en"] != self.texts["videos, title()"]["en"]:
									the_text = the_text.replace(dictionary["Media"]["texts"]["item"][language], self.texts["season, title()"][language].lower())

								if dictionary["Media type"]["Plural"]["en"] == self.texts["videos, title()"]["en"]:
									the_text = the_text.replace(dictionary["Media"]["texts"]["item"][language], self.texts["series"][language])

							if dictionary["Media"]["States"]["Single unit"] == True:
								the_text = the_text.replace(self.media_types["Genders"][language]["feminine"]["the"] + " ", self.media_types["Genders"][language]["masculine"]["the"] + " ")

						# If the media or media item is completed, add the "the text" defined above to the "completed, past_perfect" text
						if key in ["Completed media", "Completed media item"]:
							language_text = self.JSON.Language.texts["completed, past_perfect, title()"][language] + " " + the_text

						# If the "youtube" text is inside the language text, correct its case
						if "youtube" in language_text:
							language_text = language_text.replace("youtube", "YouTube")

						# Add the language text to the text variable
						text += language_text

					if key == "Re-watched":
						# If the state is "Re-watched", add the Re-watched text plus the Re-watched times to the text
						text += dictionary["Media"]["Episode"]["re_watched"]["re_watched_text"][language] + " (" + str(dictionary["Media"]["Episode"]["re_watched"]["times"]) + "x)"

					# Define the state text per language
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

	def Remove_Media_Type(self, to_remove):
		from copy import deepcopy

		if type(to_remove) == str:
			to_remove = [
				to_remove
			]

		media_types = deepcopy(self.media_types)

		for text in to_remove:
			if text in media_types:
				media_types.pop(text)

		dictionary = {
			"To remove": to_remove,
			"Media types": media_types,
			"List": {}
		}

		# Iterate through English plural media types list
		for plural_media_type in self.media_types["Plural"]["en"]:
			# If the plural media type is inside the local media types dictionary
			if plural_media_type in dictionary["Media types"]:
				# Get the media type dictionary
				media_type = dictionary["Media types"][plural_media_type]

				# Iterate through small languages list
				for language in self.languages["small"]:
					# Create empty language list if it does not exist
					if language not in dictionary["List"]:
						dictionary["List"][language] = []

					# Add to the plural media types list
					dictionary["List"][language].append(media_type["Plural"][language])

		return dictionary["List"]

	def Define_Media_Titles(self, dictionary, item = False):
		media = dictionary["Media"]

		if item == True:
			media = dictionary["Media"]["Item"]

		if self.File.Exist(media["folders"]["details"]) == True:
			media["Details"] = self.File.Dictionary(media["folders"]["details"])

			if self.JSON.Language.language_texts["original_title"] not in media["Details"]:
				text = self.JSON.Language.language_texts["original_title"] + ": {}" + "\n" + self.JSON.Language.language_texts["episode, title()"] + ": None"
				text = text.format(media["folders"]["details"].split("/")[-2])
				self.File.Edit(media["folders"]["details"], text, "w")

				media["Details"] = self.File.Dictionary(media["folders"]["details"])

			# Define titles key
			media["Titles"] = {
				"Original": media["Details"][self.JSON.Language.language_texts["original_title"]],
				"Sanitized": media["Details"][self.JSON.Language.language_texts["original_title"]],
			}

			media["Titles"]["Language"] = media["Titles"]["Original"]

			# If media type is "Animes" or the "romanized_title" key exists inside the media details, define the romanized name and ja name
			if dictionary["Media type"]["Plural"]["en"] == self.texts["animes, title()"]["en"] or self.JSON.Language.language_texts["romanized_title"] in media["Details"]:
				if self.JSON.Language.language_texts["romanized_title"] in media["Details"]:
					media["Titles"]["Romanized"] = media["Details"][self.JSON.Language.language_texts["romanized_title"]]
					media["Titles"]["Language"] = media["Titles"]["Romanized"]

				if "Romanized" in media["Titles"]:
					media["Titles"]["Sanitized"] = media["Titles"]["Romanized"]

				media["Titles"]["ja"] = media["Details"][self.JSON.Language.language_texts["original_title"]]

			if " (" in media["Titles"]["Original"] and " (" not in media["Titles"]["Language"]:
				media["Titles"]["Language"] = media["Titles"]["Language"] + " (" + media["Titles"]["Original"].split(" (")[-1]

				if self.user_language in media["Titles"]:
					media["Titles"][self.user_language] = media["Titles"][self.user_language] + " (" + media["Titles"]["Original"].split(" (")[-1]

			# Define media titles per language
			for language in self.languages["small"]:
				key = self.JSON.Language.texts["title_in_language"][language][self.user_language]

				if key in media["Details"]:
					media["Titles"][language] = media["Details"][key]

			media["Titles"]["Language"] = media["Titles"]["Original"]

			if self.user_language in media["Titles"]:
				media["Titles"]["Language"] = media["Titles"][self.user_language]

			if self.user_language not in media["Titles"] and "Romanized" in media["Titles"]:
				media["Titles"]["Language"] = media["Titles"]["Romanized"]

			# Sanitize media title
			media["Titles"]["Sanitized"] = self.Sanitize_Title(media["Titles"]["Sanitized"])

		return dictionary

	def Get_Media_Title(self, dictionary, language = None, item = False, episode = False):
		titles = dictionary["Media"]["Titles"]

		if item == True:
			titles = dictionary["Media"]["Item"]["Titles"]

		if episode == True:
			titles = dictionary["Media"]["Episode"]["Titles"]

		if language not in titles:
			title = titles["Original"]

			if "Romanized" in titles:
				title = titles["Romanized"]

		if language in titles:
			title = titles[language]

		return title

	def Sanitize_Title(self, title):
		if len(title) > 1 and title[0] + title[1] == ": ":
			title = title[2:]

		if ". " in title:
			title = title.replace(". ", " ")

		elif "." in title:
			title = title.replace(".", "")

		title = self.Sanitize(title, restricted_characters = True)

		return title

	def Show_Media_Title(self, dict_, media_item = False):
		self.media_item = media_item

		media = dict_["Media"]

		if self.media_item == True:
			media = dict_["Media"]["Item"]

		if media["Titles"]["Language"] == media["Titles"]["Original"]:
			print("\t" + media["Titles"]["Original"])

			if dict_["Media"]["States"]["Video"] == True and self.media_item == False and dict_["Media"]["Item"]["Title"] != media["Titles"]["Original"]:				
				print()
				print(self.Text.Capitalize(dict_["Media"]["texts"]["item"][self.user_language]) + ":")
				print("\t" + dict_["Media"]["Item"]["Title"])

		if media["Titles"]["Language"] != media["Titles"]["Original"]:
			print("\t" + media["Titles"]["Original"])
			print("\t" + media["Titles"]["Language"])

			for language in self.languages["small"]:
				language_name = self.JSON.Language.texts["title_in_language"][language][self.user_language]

				if language in media["Titles"] and media["Titles"][language] != media["Titles"]["Original"] and media["Titles"][language] != media["Titles"]["Language"]:
					print("\t" + media["Titles"][language])

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
			status = self.JSON.Language.language_texts["completed, title()"]

		# Update the status key in the media details
		dictionary["Media"]["Details"][self.JSON.Language.language_texts["status, title()"]] = status

		# Update the media details file
		self.File.Edit(dictionary["Media"]["folders"]["details"], self.Text.From_Dictionary(dictionary["Media"]["Details"]), "w")

		self.Check_Status(dictionary)

	def Check_Status(self, dictionary):
		media_type = dictionary

		if "Media type" in dictionary:
			media_type = dictionary["Media type"]

			self.language_status = dictionary["Media"]["Details"][self.JSON.Language.language_texts["status, title()"]]

			# Get the English watching status from the language status of the media details
			status = self.Get_Language_Status(self.language_status)

		dictionary["JSON"] = self.JSON.To_Python(media_type["Folders"]["media_info"]["info"])

		# Update the number of media
		dictionary["JSON"]["Number"] = len(dictionary["JSON"]["Titles"])

		# Sort the titles list
		dictionary["JSON"]["Titles"] = sorted(dictionary["JSON"]["Titles"], key = str.lower)

		titles = []

		if "Media type" not in dictionary:
			titles.extend(dictionary["JSON"]["Titles"])

		if "Media type" in dictionary:
			titles.append(dictionary["Media"]["Title"])

		# Iterate through the watching statuses list
		for self.watching_status in self.texts["statuses, type: list"]["en"]:
			for media_title in titles:
				if "Media type" not in dictionary:
					folder = media_type["Folders"]["media_info"]["root"] + self.Sanitize_Title(media_title) + "/"
					details_file = folder + self.JSON.Language.language_texts["details, title()"] + ".txt"
					details = self.File.Dictionary(details_file)

					self.language_status = details[self.JSON.Language.language_texts["status, title()"]]

					# Get the English watching status from the language status of the media details
					status = self.Get_Language_Status(self.language_status)

				# If the media status is equal to the watching status
				# And the media is not in the correct watching status list, add it to the list
				if status == self.watching_status and media_title not in dictionary["JSON"]["Status"][self.watching_status]:
					dictionary["JSON"]["Status"][self.watching_status].append(media_title)

				# If the media status is not equal to the watching status
				# And the media is in the wrong watching status list, remove it from the list
				if status != self.watching_status and media_title in dictionary["JSON"]["Status"][self.watching_status]:
					dictionary["JSON"]["Status"][self.watching_status].remove(media_title)

			# Sort media list
			dictionary["JSON"]["Status"][self.watching_status] = sorted(dictionary["JSON"]["Status"][self.watching_status], key = str.lower)

		# Update the media type "Info.json" file
		self.JSON.Edit(media_type["Folders"]["media_info"]["info"], dictionary["JSON"])

		return dictionary

	def Get_YouTube_Information(self, name, link = None, remove_unused_keys = True):
		ids = {
			"video": "v",
			"playlist": "list",
			"playlistItem": "list",
			"comment": "lc"
		}

		if type(name) == dict:
			for key in ["id", "link"]:
				if key in name:
					link = name[key]

			name = name["item"]

		id = link

		if "youtube" in link:
			from urllib.parse import urlparse, parse_qs

			link = urlparse(link)
			query = link.query
			parameters = parse_qs(query)
			id = parameters[ids[name]][0]

		youtube = {
			"item": name,
			"id": id
		}

		if "s" not in youtube["item"][-1]:
			youtube["item"] += "s"

		dict_ = self.API.Call("YouTube", youtube)["Dictionary"]

		if youtube["id"] in dict_:
			dict_ = dict_[youtube["id"]]

		if youtube["item"] == "playlistItems":
			dict_ = dict_["Videos"]

			if remove_unused_keys == True:
				for id in dict_:
					video = dict_[id]

					if "Images" in video:
						video.pop("Images")

					if "Language" in video:
						video.pop("Language")

		return dict_

	def Show_Media_Information(self, dictionary):
		# Show opening this media text
		header_text = dictionary["Media type"]["Singular"][self.user_language] + ":"

		if "header_text" in dictionary and "header_text" not in ["", None]:
			header_text = dictionary["header_text"]

		print()
		print(self.large_bar)

		# Show congratulations text if the user finished the media
		if dictionary["Media"]["States"]["Re-watching"] == False and dictionary["Media"]["States"]["Completed media"] == True:
			print()
			print(self.JSON.Language.language_texts["congratulations"] + "! :3")

		print()
		print(header_text)

		# Show the title of the media
		self.Show_Media_Title(dictionary)

		print()

		# Show finished watching media texts and times
		if dictionary["Media"]["States"]["Re-watching"] == False and dictionary["Media"]["States"]["Completed media"] == True:
			print(self.language_texts["new_watching_status"] + ":")
			print("\t" + dictionary["Media"]["Details"][self.JSON.Language.language_texts["status, title()"]])
			print()

			if "finished_watching_text" in dictionary["Media"] and dictionary["Media"]["Finished watching text"] != "":
				print(dictionary["Media"]["Finished watching text"])
				print()

		# Show media episode if the media is series media (not a movie)
		if dictionary["Media"]["States"]["Series media"] == True:
			if dictionary["Media"]["States"]["Media item list"] == True:
				if (
					dictionary["Media"]["States"]["Video"] == False and dictionary["Media"]["Item"]["Title"] != dictionary["Media"]["Items"]["List"][0] or
					dictionary["Media"]["States"]["Video"] == True
				):
					dictionary["Media type"]["Genders"][self.user_language]["of_the"] = self.media_types["Genders"][self.user_language]["feminine"]["of_the"]

			media_episode_text = "{} {}".format(self.Text.Capitalize(dictionary["Media"]["texts"]["unit"][self.user_language]), dictionary["Media type"]["Genders"][self.user_language]["of_the"]) + " "

			if dictionary["Media"]["Item"]["Type"][self.user_language] in [self.language_texts["season, title()"].lower(), self.language_texts["serie"]]:
				if dictionary["Media"]["States"]["Media item list"] == False or dictionary["Media"]["Item"]["Title"] == dictionary["Media"]["Items"]["List"][0]:
					media_episode_text = media_episode_text.replace(dictionary["Media type"]["Genders"][self.user_language]["of_the"], dictionary["Media"]["texts"]["container_text"]["of_the"])

				if dictionary["Media"]["States"]["Media item list"] == True and dictionary["Media"]["Item"]["Title"] != dictionary["Media"]["Items"]["List"][0]:
					text = dictionary["Media"]["texts"]["item"][self.user_language]

					if dictionary["Media"]["States"]["Video"] == False:
						text = text.lower()

					if text not in media_episode_text:
						media_episode_text += text

			if dictionary["Media"]["Item"]["Type"][self.user_language] not in [self.language_texts["season, title()"].lower(), self.language_texts["serie"]]:
				media_episode_text = media_episode_text.replace(dictionary["Media type"]["Genders"][self.user_language]["of_the"], dictionary["Media"]["texts"]["container_text"]["of_the"])

			if " " in media_episode_text[-1]:
				media_episode_text = media_episode_text[:-1]

			title = dictionary["Media"]["Episode"]["Title"]

			if dictionary["Media"]["Language"] != self.user_language:
				title = dictionary["Media"]["Episode"]["Titles"][self.user_language]

			if dictionary["Media"]["States"]["Re-watching"] == True:
				title += dictionary["Media"]["Episode"]["re_watched"]["text"]

			print(media_episode_text + ":")
			print("\t" + title)
			print()

			text = self.JSON.Language.language_texts["with_{}_title"]

			if dictionary["Media"]["States"]["Video"] == True:
				text = self.JSON.Language.language_texts["with"] + " {}"

			text_to_show = self.Text.Capitalize(dictionary["Media"]["texts"]["unit"][self.user_language]) + " " + text.format(dictionary["Media"]["texts"]["container_text"]["the"])

			# Show media episode (episode with media item) if the media has a media item list
			if (
				dictionary["Media"]["States"]["Media item list"] == True and
				dictionary["Media"]["States"]["Video"] == False and
				dictionary["Media"]["Item"]["Title"] != dictionary["Media"]["Title"] and
				self.language_texts["single_unit"] not in dictionary["Media"]["Item"]["Details"] and
				dictionary["Media"]["States"]["Replace title"] == False
			):
				media_episode_text = self.Text.Capitalize(dictionary["Media"]["texts"]["unit"][self.user_language]) + " " + self.language_texts["with_{}"].format(dictionary["Media"]["texts"]["item"][self.user_language])

				print(media_episode_text + ":")

				title = dictionary["Media"]["Episode"]["with_item"][self.user_language]

				if dictionary["Media"]["States"]["Re-watching"] == True:
					title += dictionary["Media"]["Episode"]["re_watched"]["text"]

				print("\t" + title)
				print()

				text_to_show += " " + self.JSON.Language.language_texts["and"] + " " + dictionary["Media"]["texts"]["item"][self.user_language]

				key = "with_title_and_item"

			# Show only media title with episode if the media has no media item list
			if (
				dictionary["Media"]["States"]["Media item list"] == False or
				dictionary["Media"]["States"]["Video"] == True or
				dictionary["Media"]["Item"]["Title"] == dictionary["Media"]["Title"] or
				self.language_texts["single_unit"] in dictionary["Media"]["Item"]["Details"] or
				dictionary["Media"]["States"]["Replace title"] == True
			):
				key = "with_title"

			title = dictionary["Media"]["Episode"][key][self.user_language]

			if dictionary["Media"]["States"]["Re-watching"] == True:
				title += dictionary["Media"]["Episode"]["re_watched"]["text"]

			if dictionary["Media"]["States"]["Replace title"] == False:
				print(text_to_show + ":")
				print("\t" + title)
				print()

		# Show media type
		print(self.language_texts["media_type"] + ":")
		print("\t" + dictionary["Media type"]["Plural"][self.user_language])

		if dictionary["Media"]["States"]["Re-watching"] == False and dictionary["Media"]["States"]["Completed media item"] == True:
			print()
			print("-")
			print()
			print(self.JSON.Language.language_texts["congratulations"] + "! :3")
			print()

			text_to_show = self.language_texts["you_finished_watching"] + " " + dictionary["Media"]["texts"]["this_item"][self.user_language] + " " + dictionary["Media"]["texts"]["container_text"]["of_the"] + ' "' + dictionary["Media"]["Titles"]["Language"] + '"'

			if dictionary["Media"]["States"]["Media item list"] == True and dictionary["Media"]["Item"]["Title"] == dictionary["Media"]["Title"]:
				text_to_show = self.language_texts["you_finished_watching"] + " " + dictionary["Media"]["texts"]["this_container"][self.user_language]

			print(text_to_show + ":")

			self.Show_Media_Title(dictionary, media_item = True)

			if dictionary["Media"]["States"]["Completed media"] == False and dictionary["Media"]["States"]["Video"] == False:
				item_type = dictionary["Media"]["Item"]["Next"]["Type"][self.user_language]

				text = self.language_texts["next_{}_to_watch, feminine"]

				if item_type not in [self.texts["season, title()"][self.user_language].lower(), self.texts["series"][self.user_language]]:
					text = self.language_texts["next_{}_to_watch, masculine"]

				print()
				print(text.format(item_type.lower()) + ": ")

				dict_ = { 
					"Media": {
						"Item": {
							"Titles": dictionary["Media"]["Item"]["Next"]["Titles"]
						},
						"States": dictionary["Media"]["States"],
						"texts": dictionary["Media"]["texts"]
					}
				}

				self.Show_Media_Title(dict_, media_item = True)

		if "unit" in dictionary["Media"]["Episode"]:
			# Show media unit text and episode unit
			print()
			print(self.language_texts["media_unit"] + ":")
			print("\t" + dictionary["Media"]["Episode"]["unit"])

		if "Entry" in dictionary and "Dates" in dictionary["Entry"]:
			text = self.language_texts["when_i_finished_watching"] + " " + dictionary["Media"]["texts"]["the_unit"][self.user_language]

			# Replaced "watching" with "re-watching" text
			if dictionary["Media"]["States"]["Re-watching"] == True:
				text = text.replace(self.language_texts["watching, infinitive"], self.language_texts["re_watching, infinitive"] + " " + dictionary["Media"]["Episode"]["re_watched"]["time_text"][self.user_language])

			print()
			print(text + ":")
			print("\t" + dictionary["Entry"]["Dates"]["Timezone"])

		if (
			"finished_watching_text" in dictionary["Media"]["Item"] and dictionary["Media"]["Item"]["Finished watching text"] != "" or

			dictionary["Media"]["States"]["Finished watching"] == True and
			dictionary["Media"]["States"]["First entry in year"] == True or

			dictionary["Media"]["States"]["Finished watching"] == True and
			dictionary["Media"]["States"]["First media type entry in year"] == True or

			"ID" in dictionary["Media"]["Episode"] or
			"Next" in dictionary["Media"]["Episode"]
		):
			print()

		# Show ID of episode if there is one
		if "ID" in dictionary["Media"]["Episode"]:
			print(self.JSON.Language.language_texts["id, upper()"] + ":")
			print("\t" + dictionary["Media"]["Episode"]["ID"])

			# If the "Remote" key is inside the "Episode" dictionary
			if "Remote" in dictionary["Media"]["Episode"]:
				# Show the remote origin title
				if "Title" in dictionary["Media"]["Episode"]["Remote"]:
					print()
					print(self.JSON.Language.language_texts["remote_origin"] + ":")
					print("\t" + dictionary["Media"]["Episode"]["Remote"]["Title"])

				# Show the remote origin link
				if "Link" in dictionary["Media"]["Episode"]["Remote"]:
					print()
					print(self.JSON.Language.language_texts["link, title()"] + ":")
					print("\t" + dictionary["Media"]["Episode"]["Remote"]["Link"])

			if (
				"Next" in dictionary["Media"]["Episode"] or
				dictionary["Media"]["States"]["Re-watching"] == False and dictionary["Media"]["States"]["Completed media item"] == True and "finished_watching_text" in dictionary["Media"]["Item"]
			):
				print()

		# Show next episode to watch if it is present in the "episode" dictionary
		if "Next" in dictionary["Media"]["Episode"]:
			text = self.language_texts["next_{}_to_watch, masculine"]

			if dictionary["Media"]["States"]["Re-watching"] == True:
				text = text.replace(self.language_texts["watch"], self.language_texts["re_watch"])

			print(text.format(dictionary["Media"]["texts"]["unit"][self.user_language]) + ": ")
			print("\t" + dictionary["Media"]["Episode"]["Next"])

			if (
				"finished_watching_text" in dictionary["Media"]["Item"] and dictionary["Media"]["Item"]["Finished watching text"] != "" or

				dictionary["Media"]["States"]["Finished watching"] == True and
				dictionary["Media"]["States"]["First entry in year"] == True or

				dictionary["Media"]["States"]["Finished watching"] == True and
				dictionary["Media"]["States"]["First media type entry in year"] == True
			):
				print()

		# Show the finished watching media (started and finished watching dates) text when the user completed a media item
		if (
			dictionary["Media"]["States"]["Re-watching"] == False and
			dictionary["Media"]["States"]["Completed media item"] == True and
			dictionary["Media"]["States"]["Single unit"] == False and 
			"finished_watching_text" in dictionary["Media"]["Item"] and
			dictionary["Media"]["Item"]["Finished watching text"] != ""
		):
			print(dictionary["Media"]["Item"]["Finished watching text"])

			if dictionary["Media"]["States"]["Finished watching"] == True:
				print()

		if dictionary["Media"]["States"]["Finished watching"] == True:
			# If there are states, show them
			if "States" in self.dictionary and self.dictionary["States"]["States"] != {}:
				if "ID" in dictionary["Media"]["Episode"]:
					print()

				print(self.JSON.Language.language_texts["states, title()"] + ":")

				for key in self.dictionary["States"]["Texts"]:
					print("\t" + self.dictionary["States"]["Texts"][key][self.user_language])

			if "ID" in dictionary["Media"]["Episode"] or "States" in self.dictionary and self.dictionary["States"]["States"] != {}:
				if dictionary["Media"]["States"]["First entry in year"] == True or dictionary["Media"]["States"]["First media type entry in year"] == True:
					print()

			# Show the "first watched media in year" text if this is the first media that the user watched in the year
			if dictionary["Media"]["States"]["First entry in year"] == True:
				container = dictionary["Media"]["texts"]["container"][self.user_language]

				if dictionary["Media"]["States"]["Video"] == False:
					container = container.lower()

				items = [
					self.media_types["Genders"][self.user_language]["feminine"]["this"].title(),
					self.media_types["Genders"][self.user_language]["feminine"]["the"] + " " + self.media_types["Genders"][self.user_language]["feminine"]["first"] + " "+ self.JSON.Language.language_texts["media"]
				]

				items.append(self.JSON.Language.language_texts["genders, type: dict, masculine"]["in"] + " " + self.current_year["Number"])

				print(self.language_texts["{}_is_{}_that_you_watched_{}"].format(*items) + ".")

				if dictionary["Media"]["States"]["First media type entry in year"] == True:
					print()

			# Show the "first media type media watched in year" text if this is the first media that the user watched in the year, per media type
			if dictionary["Media"]["States"]["First media type entry in year"] == True:
				container = dictionary["Media"]["texts"]["container"][self.user_language]

				if dictionary["Media"]["States"]["Video"] == False:
					container = container.lower()

				if dictionary["Media"]["States"]["Series media"] == True:
					container = dictionary["Media"]["texts"]["unit"][self.user_language] + " " + self.JSON.Language.language_texts["of, neutral"] + " " + container

				if dictionary["Media"]["States"]["First entry in year"] == False:
					if dictionary["Media"]["States"]["Video"] == False:
						container = container.lower()

					items = [
						dictionary["Media type"]["Genders"][self.user_language]["this"].title(),
						dictionary["Media type"]["Genders"][self.user_language]["the"] + " " + dictionary["Media type"]["Genders"][self.user_language]["first"] + " " + container
					]

					items.append(self.JSON.Language.language_texts["genders, type: dict, masculine"]["in"] + " " + self.current_year["Number"])

					text = self.language_texts["{}_is_{}_that_you_watched_{}"].format(*items)

				if dictionary["Media"]["States"]["First entry in year"] == True:
					text = self.JSON.Language.language_texts["and_also"].capitalize() + " " + dictionary["Media type"]["Genders"][self.user_language]["the"] + " " + dictionary["Media type"]["Genders"][self.user_language]["first"] + " " + container

				print(text + ".")

			# If the user finished watching, ask for input before ending execution
			print()
			print(self.large_bar)

			self.Input.Type(self.JSON.Language.language_texts["press_enter_when_you_finish_reading_the_info_summary"])
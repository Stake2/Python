# Watch History.py

# Import the "importlib" module
import importlib

from copy import deepcopy

# Main class Watch_History that provides variables to the classes that implement it
class Watch_History(object):
	def __init__(self):
		# Import the classes
		self.Import_Classes()

		# Define the folders of the module
		self.folders = self.Define_Folders(object = self).folders

		# Module related methods
		self.Define_Basic_Variables()
		self.Define_Texts()

		# Import the usage classes
		self.Import_Usage_Classes()

		# Folders, files, lists, and dictionaries methods
		self.Define_Folders_And_Files()
		self.Define_Lists_And_Dictionaries()

		# Class methods
		self.Define_Types()
		self.Define_Registry_Format()

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
				# Run the sub-class to define its variable
				sub_class = sub_class()

			# Add the sub-class to the current module
			setattr(self, module_title, sub_class)

		# Define the "Language" class as the same class inside the "JSON" class
		self.Language = self.JSON.Language

	def Define_Basic_Variables(self):
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
		# Define the "Texts" dictionary
		self.texts = self.JSON.To_Python(self.module["Files"]["Texts"])

		# Define the "Language texts" dictionary
		self.language_texts = self.Language.Item(self.texts)

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

	def Import_Usage_Classes(self):
		# Define the classes to be imported
		classes = [
			"Years",
			"Christmas"
		]

		# Import them
		for title in classes:
			# Import the module
			module = importlib.import_module("." + title, title)

			# Get the sub-class
			sub_class = getattr(module, title)

			# Add the sub-class to the current module
			setattr(self, title, sub_class())

		self.Today_Is_Christmas = self.Christmas.Today_Is_Christmas()

	def Define_Folders_And_Files(self):
		# If there is no current year variable inside the self object, get the current year variable from the "Years" module
		if hasattr(self, "current_year") == False:
			self.current_year = self.Years.years["Current year"]

		# Replace the "self.folders" folder dictionary with the "Audiovisual Media" network folder dictionary
		self.folders = self.folders["Notepad"]["Data Networks"]["Audiovisual Media"]

		# Audiovisual Media Network root files
		self.folders["Watch list"] = self.folders["root"] + "Watch list.txt"

		# Define the current year folder for easier typing
		self.folders["Watch History"]["Current year"] = self.folders["Watch History"][self.current_year["Number"]]

		# Define the "History" dictionary
		self.history = {
			"Key": "Entries",
			"Numbers": {
				"Watched things": "",
				"Media comments": "Comments"
			},
			"Per type": True,
			"Folder": self.Folder.folders["Notepad"]["Data Networks"]["Audiovisual Media"]["Watch History"]["root"]
		}

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

		# Dictionary of remove origins
		self.remote_origins = {
			"Animes Vision": "https://animes.vision/",
			"YouTube": "https://www.youtube.com/"
		}

		# Define the secondary type keys in singular and plural mode
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

		# Define the secondary type texts per language
		for item_type in ["Singular", "Plural"]:
			for language in self.languages["small"]:
				if language not in self.secondary_types[item_type]:
					self.secondary_types[item_type][language] = []

				for text_key in self.secondary_types[item_type]["Keys"]:
					# If the text key is inside the "texts" dictionary of the Language class, use it as the list
					if text_key in self.Language.texts:
						texts_list = self.Language.texts

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

		# Define the default media states dictionary
		self.states = {
			"Remote": False,
			"Local": False,
			"Video": False,
			"Series media": True,
			"Episodic": False,
			"Single unit": False,
			"Replace title": False,
			"Media item list": False,
			"Media item is media": False,
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

	def Define_Types(self):
		# Get the media types dictionary from the "Types.json" file
		self.media_types = self.JSON.To_Python(self.folders["Data"]["Types"])

		# Update the dictionary with more keys
		self.media_types.update({
			"Genders": self.Language.texts["genders, type: dict"],
			"Gender items": self.Language.texts["gender_items"],
			"Media list": {
				"Number": 0,
				"Numbers": {}
			}
		})

		# Read the root "Information.json" file if it is not empty
		if self.File.Contents(self.folders["Media information"]["Information"])["lines"] != []:
			# Get the media information dictionary from it
			info_dictionary = self.JSON.To_Python(self.folders["Media information"]["Information"])

		# If the root "Information.json" file is empty, add a default JSON dictionary inside it
		if self.File.Contents(self.folders["Media information"]["Information"])["lines"] == []:
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
				"Gender": "",
				"Genders": {},
				"Folders": {},
				"Subfolders": {},
				"Status": [
					self.texts["plan_to_watch, title()"]["en"],
					self.texts["watching, title()"]["en"],
					self.texts["re_watching, title()"]["en"],
					self.Language.texts["on_hold, title()"]["en"]
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
				self.media_types[plural_media_type]["Singular"]["select"] = self.Language.language_texts["channel, title()"]
				self.media_types[plural_media_type]["Plural"]["select"] = self.Language.language_texts["channels, title()"]

			# Define the genders
			gender = "masculine"

			if plural_media_type == self.texts["series, title()"]["en"]:
				gender = "feminine"

			self.media_types[plural_media_type]["Gender"] = gender

			for language in self.languages["small"]:
				self.media_types[plural_media_type]["Genders"][language] = deepcopy(self.media_types["Genders"][language][gender])

			# Create media type folders
			for root_folder in ["Media information", "Watch History", "Media"]:
				media_type_key = plural_media_type.lower().replace(" ", "_")

				# "Media information" folder
				if root_folder == "Media information":
					self.folders[root_folder][media_type_key] = {
						"root": self.folders[root_folder]["root"] + language_media_type + "/"
					}

					self.Folder.Create(self.folders[root_folder][media_type_key]["root"])

				# "Watch History" "Per Media Type" folder
				if root_folder == "Watch History":
					# Iterate through the years list from "2018" to the current year
					for year in self.Date.Create_Years_List(function = str):
						# Create the "Per Media Type" media type dictionary
						self.folders[root_folder][year]["Per Media Type"][media_type_key] = {
							"root": self.folders[root_folder][year]["Per Media Type"]["root"] + plural_media_type + "/"
						}

						# Create the root "Per Media Type" media type folder
						self.Folder.Create(self.folders[root_folder][year]["Per Media Type"][media_type_key]["root"])

						# Create the "Entries.json" file
						self.folders[root_folder][year]["Per Media Type"][media_type_key]["Entries"] = self.folders[root_folder][year]["Per Media Type"][media_type_key]["root"] + "Entries.json"
						self.File.Create(self.folders[root_folder][year]["Per Media Type"][media_type_key]["Entries"])

						# Create the "Entry list.txt" file
						self.folders[root_folder][year]["Per Media Type"][media_type_key]["Entry list"] = self.folders[root_folder][year]["Per Media Type"][media_type_key]["root"] + "Entry list.txt"
						self.File.Create(self.folders[root_folder][year]["Per Media Type"][media_type_key]["Entry list"])

						# Create the "Files" folder
						self.folders[root_folder][year]["Per Media Type"][media_type_key]["Files"] = {
							"root": self.folders[root_folder][year]["Per Media Type"][media_type_key]["root"] + "Files/"
						}

						self.Folder.Create(self.folders[root_folder][year]["Per Media Type"][media_type_key]["Files"]["root"])

					# Define the "current_year" as the current year folder
					self.folders[root_folder]["current_year"] = self.folders[root_folder][str(self.date["Units"]["Year"])]

				# "Media" folder
				if root_folder == "Media":
					if root_folder not in self.folders:
						self.folders[root_folder] = {}

					self.folders[root_folder][media_type_key] = {
						"root": self.Folder.folders[root_folder]["root"] + language_media_type + "/"
					}

					self.Folder.Create(self.folders[root_folder][media_type_key]["root"])

			# Define the media type folders and files
			key = self.media_types[plural_media_type]["Plural"]["en"].lower().replace(" ", "_")

			self.media_types[plural_media_type]["Folders"] = {
				"Media information": self.folders["Media information"][key],
				"Per Media Type": self.folders["Watch History"]["Current year"]["Per Media Type"][key],
				"Media": self.folders["Media"][key]
			}

			# Define the "Information.json" file
			self.media_types[plural_media_type]["Folders"]["Media information"]["Information"] = self.media_types[plural_media_type]["Folders"]["Media information"]["root"] + "Information.json"
			self.File.Create(self.media_types[plural_media_type]["Folders"]["Media information"]["Information"])

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

			if "{" not in self.Language.language_texts["current_{}"][0]:
				text = text.lower()

			self.media_types[plural_media_type]["Subfolders"]["Current"] = self.Language.language_texts["current_{}"].format(text)

			# Read the "Information.json" file
			if self.File.Contents(self.media_types[plural_media_type]["Folders"]["Media information"]["Information"])["lines"] != []:
				self.media_types[plural_media_type]["JSON"] = self.JSON.To_Python(self.media_types[plural_media_type]["Folders"]["Media information"]["Information"])

			# If the "Information.json" file is empty, add a default JSON dictionary inside it
			if self.File.Contents(self.media_types[plural_media_type]["Folders"]["Media information"]["Information"])["lines"] == []:
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

			# Edit the "Information.json" file with the updated "Information" dictionary
			self.JSON.Edit(self.media_types[plural_media_type]["Folders"]["Media information"]["Information"], self.media_types[plural_media_type]["JSON"])

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
			self.JSON.Edit(self.folders["Data"]["Types"], self.media_types)

		# Update the media list inside the root "Information.json" dictionary
		info_dictionary.update(self.media_types["Media list"])

		# Update the root "Information.json" file
		self.JSON.Edit(self.folders["Media information"]["Information"], info_dictionary)

		# Add the entry types to the History dictionary
		self.history["Types"] = self.media_types

		# Define the types folder
		self.history["Types folder"] = "Per Media Type"

	def Define_Registry_Format(self):
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

		if (
			self.File.Contents(self.folders["Watch History"]["History"])["lines"] != [] and
			self.JSON.To_Python(self.folders["Watch History"]["History"])["Years"] != []
		):
			# Get the History dictionary from the file
			self.dictionaries["History"] = self.JSON.To_Python(self.folders["Watch History"]["History"])

		# If the current year is not inside the "History" years list, add it to the list
		if self.current_year["Number"] not in self.dictionaries["History"]["Years"]:
			self.dictionaries["History"]["Years"].append(self.current_year["Number"])

		entries = 0

		# Update the number of entries of all years
		for year in self.Date.Create_Years_List(function = str):
			# Get the year folder and the entries file
			year_folder = self.folders["Watch History"]["root"] + year + "/"
			entries_file = year_folder + "Entries.json"

			# If the file exists and it is not empty
			if (
				self.File.Exist(entries_file) == True and
				self.File.Contents(entries_file)["lines"] != []
			):
				# Add the total number to the local number of entries
				entries += self.JSON.To_Python(entries_file)["Numbers"]["Total"]

			# Add the year to the Years list if it is not inside it
			if year not in self.dictionaries["History"]["Years"]:
				self.dictionaries["History"]["Years"].append(year)

		# Sort the Years list
		self.dictionaries["History"]["Years"] = sorted(self.dictionaries["History"]["Years"], key = str.lower)

		# Update the number of years with the length of the years list
		self.dictionaries["History"]["Numbers"]["Years"] = len(self.dictionaries["History"]["Years"])

		# Define the number of Entries of all years as the local number of entries
		self.dictionaries["History"]["Numbers"]["Entries"] = entries

		# Define the total number of comments as the number gotten from the root comments file
		self.dictionaries["History"]["Numbers"]["Comments"] = self.JSON.To_Python(self.folders["Comments"]["Comments"])["Numbers"]["Total"]

		# Update the "History.json" file with the updated "History" dictionary
		self.JSON.Edit(self.folders["Watch History"]["History"], self.dictionaries["History"])

		# Create the "Per Media Type" key inside the "Numbers" dictionary of the "Entries" dictionary
		self.dictionaries["Entries"]["Numbers"]["Per Media Type"] = {}

		# If the "Entries.json" is not empty and has entries, get the Entries dictionary from it
		if (
			self.File.Contents(self.folders["Watch History"]["Current year"]["Entries"])["lines"] != [] and
			self.JSON.To_Python(self.folders["Watch History"]["Current year"]["Entries"])["Entries"] != []
		):
			self.dictionaries["Entries"] = self.JSON.To_Python(self.folders["Watch History"]["Current year"]["Entries"])

		if (
			self.File.Contents(self.folders["Comments"]["Comments"])["lines"] != [] and
			self.JSON.To_Python(self.folders["Comments"]["Comments"])["Numbers"]["Total"] != 0
		):
			# Get Comments dictionary from file
			self.dictionaries["Root comments"] = self.JSON.To_Python(self.folders["Comments"]["Comments"])

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
			if (
				self.File.Contents(self.folders["Watch History"]["Current year"]["Per Media Type"][key]["Entries"])["lines"] != [] and
				self.JSON.To_Python(self.folders["Watch History"]["Current year"]["Per Media Type"][key]["Entries"])["Entries"] != []
			):
				self.dictionaries["Media type"][plural_media_type] = self.JSON.To_Python(self.folders["Watch History"]["Current year"]["Per Media Type"][key]["Entries"])

			if self.current_year["Number"] not in self.dictionaries["Root comments"]["Numbers"]["Type"][plural_media_type]["Years"]:
				self.dictionaries["Root comments"]["Numbers"]["Type"][plural_media_type]["Years"][self.current_year["Number"]] = 0

			# Get media type comment number per year
			self.dictionaries["Media type"][plural_media_type]["Numbers"]["Comments"] = self.dictionaries["Root comments"]["Numbers"]["Type"][plural_media_type]["Years"][self.current_year["Number"]]

			self.JSON.Edit(self.folders["Watch History"]["Current year"]["Per Media Type"][key]["Entries"], self.dictionaries["Media type"][plural_media_type])

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

		# Update the "Entries.json" file with the updated "Entries" dictionary
		self.JSON.Edit(self.folders["Watch History"]["Current year"]["Entries"], self.dictionaries["Entries"])

		# Update "Comments.json" file with the updated "Comments" dictionary
		self.JSON.Edit(self.folders["Comments"]["Comments"], self.dictionaries["Root comments"])

	def Create_Statistics(self, years_list):
		# Define a local dictionary of statistics
		statistics = {
			"Module": "Watch_History",
			"Statistic key": "Watched media",
			"Text key": "watched_media, type: plural",
			"Text": {},
			"List": [],
			"Years": {}
		}

		# Create a root dictionary of media
		self.media = {
			"List": [],
			"Dictionary": {}
		}

		# Create a root dictionary of media type entries
		self.media_type_entries = {
		
		}

		# ---------- #

		# Fill the "Years" dictionary

		# Iterate through the list of years from 2020 to the current year
		for year_number in years_list:
			# Create the year dictionary
			year = {
				"Key": year_number,
				"Total": 0,
				"Numbers": {},
				"Months": {}
			}

			# Get the year folder
			year_folder = self.folders["Watch History"]["root"] + year_number + "/"

			# Get the per media type folder
			per_media_type_folder = year_folder + "Per Media Type/"

			# Iterate through the English plural media types list
			for plural_media_type in self.media_types["Plural"]["en"]:
				# Get the media type folder
				media_type_folder = per_media_type_folder + plural_media_type + "/"

				# Get the entries file
				entries_file = media_type_folder + "Entries.json"

				# Read the "Entries.json" file, getting the "Entries" dictionary and adding it into the year dictionary
				year["Entries"] = self.JSON.To_Python(entries_file)

				# Iterate through the dictionary of entries, updating the "Numbers" dictionary of the year dictionary
				year = self.Iterate_Through_Entries(year)

				# ---------- #

				# Fill the "Months" dictionary
				for month in range(1, 13):
					# Add leading zeroes to the month number
					month_number = str(self.Text.Add_Leading_Zeroes(month))

					# Create the month dictionary
					month = {
						"Key": month_number,
						"Total": 0,
						"Numbers": {}
					}

					# If the month number is already inside the "Months" dictionary
					if month_number in year["Months"]:
						# Get the month dictionary from it
						month = year["Months"][month_number]

					# Define the "has month" switch
					has_month = False

					# Iterate through the entries dictionary
					for entry in year["Entries"]["Dictionary"].values():
						# Split the entry date
						split = entry["Entry"].split("/")

						# If the first item inside the split list is not the entry itself (the entry date has a month)
						if split[0] != entry["Entry"]:
							# Define the local month number as the month number
							local_month_number = split[1]

							# If the local month number is equal to the root month number
							if local_month_number == month_number:
								# Define the media dictionary (media or media item), and add the media watched numbers
								month = self.Define_Media_Dictionary(month, entry)[0]

								# Add one to the month total entries number
								month["Total"] += 1

							# Define the "has month" switch as True
							has_month = True

					# If the "has month" switch is True
					if has_month == True:
						# Add the month dictionary to the "Months" dictionary of the year dictionary
						year["Months"][month_number] = month

				# Iterate through the media inside the "Numbers" dictionary
				for media_title, media in deepcopy(year["Numbers"]).items():
					# If the media key is a dictionary
					if isinstance(media, dict):
						# List the keys inside the media dictionary
						keys = list(media.keys())

						# If the number of keys is equal to two
						# And the value of the keys is equal
						if (
							len(keys) == 2 and
							media["Total"] == list(media["Dictionary"].values())[0]
						):
							# Get the full media title from the root media dictionary
							title = self.media["Dictionary"][media_title]

							# Add the new key at the position of the original key
							# Parameters: numbers, original key, new key, new value
							year["Numbers"] = self.Add_To_Index(year["Numbers"], media_title, title, media["Total"])

				# Iterate through the list of months from 1 to 12
				for month in range(1, 13):
					# Add leading zeroes to the month number
					month_number = str(self.Text.Add_Leading_Zeroes(month))

					# If the month number is already inside the "Months" dictionary
					if month_number in year["Months"]:
						# Get the month dictionary from it
						month = year["Months"][month_number]

						# Iterate through the media inside the "Numbers" dictionary
						for media_title, media in deepcopy(month["Numbers"]).items():
							# If the media key is a dictionary
							if isinstance(media, dict):
								# List the keys inside the media dictionary
								keys = list(media.keys())

								# If the number of keys is equal to two
								# And the value of the keys is equal
								if (
									len(keys) == 2 and
									media["Total"] == list(media["Dictionary"].values())[0]
								):
									# Get the full media title from the root media dictionary
									title = self.media["Dictionary"][media_title]

									# Add the new key at the position of the original key
									# Parameters: numbers, original key, new key, new value
									month["Numbers"] = self.Add_To_Index(month["Numbers"], media_title, title, media["Total"])

			# ---------- #

			# Remove the "Entries" key
			year.pop("Entries")

			# Add the year dictionary to the "Years" dictionary
			statistics["Years"][year_number] = year

		# Iterate through the dictionary of years
		for year in statistics["Years"].values():
			# Iterate through the month keys and month dictionaries inside the year "Months" dictionary
			for month_key, month in deepcopy(year["Months"]).items():
				# If the number of total entries of the month is zero
				if month["Total"] == 0:
					# Remove the month from the dictionary of months
					year["Months"].pop(month_key)

		# Sort the list of media in alphabetical order
		self.media["List"] = sorted(self.media["List"], key = str.lower)

		# Define the list of statistics as the list of media
		statistics["List"] = self.media["List"]

		# Return the statistics dictionary
		return statistics

	def Add_To_Index(self, numbers, original_key, new_key, new_value):
		# List the keys
		keys = list(numbers.keys())

		# Get the index
		index = keys.index(original_key)

		# Remove the original key
		numbers.pop(original_key)

		# Define a new local dictionary
		new_numbers = {}

		# Iterate through the indexes and keys of the list of keys
		for i, key in enumerate(keys):
			# If the "i" variable is the index we are looking for
			if i == index:
				# Add the new key 
				new_numbers[new_key] = new_value

			else:
				# Add the original key
				new_numbers[key] = numbers[key]

		# Return the new numbers dictionary
		return new_numbers

	def Define_Media_Dictionary(self, dictionary, entry):
		# Define the key to get the media title
		key = "Original"

		if "Romanized" in entry["Media"]:
			key = "Romanized"

		# Get the media title
		media_title = entry["Media"][key]

		# Add the game title to the root media dictionary
		if media_title not in self.media["List"]:
			self.media["List"].append(media_title)

		# If there is a media item inside the entry dictionary
		if "Item" in entry:
			# If the media title is not inside the "Numbers" dictionary
			if media_title not in dictionary["Numbers"]:
				# Define the root media dictionary
				dictionary["Numbers"][media_title] = {
					"Total": 0,
					"Dictionary": {}
				}

			# Else, if the media title key inside the "Numbers" dictionary is a number
			elif isinstance(dictionary["Numbers"][media_title], int):
				# Get the original number of times watched
				watched_number = dictionary["Numbers"][media_title]

				# Define the root media dictionary
				dictionary["Numbers"][media_title] = {
					"Total": watched_number,
					"Dictionary": {
						media_title: watched_number
					}
				}

			# Update the media variable
			media = dictionary["Numbers"][media_title]

			# Define the key to get the media item title
			key = "Original"

			if "Romanized" in entry["Item"]:
				key = "Romanized"

			# Get the media item title
			media_item_title = entry["Item"][key]

			# Make a backup of the full media title (media and media item titles joined together)
			self.media["Dictionary"][media_title] = media_title

			# If the media title is already inside the media item title
			if media_title in media_item_title:
				self.media["Dictionary"][media_title] = self.media["Dictionary"][media_title].replace(media_title, "")

			# Else, if the ": " string is not the first two characters of the media item
			elif media_item_title[0] + media_item_title[1] != ": ":
				# Add a space to the backup of the full media title
				self.media["Dictionary"][media_title] += " "

			# Add the media item title to the backup of the full media title
			self.media["Dictionary"][media_title] += media_item_title

			# Add the full media title to the root media dictionary
			if self.media["Dictionary"][media_title] not in self.media["List"]:
				self.media["List"].append(self.media["Dictionary"][media_title])

			# If the ": " string is inside the media item title, remove it
			if ": " in media_item_title:
				media_item_title = media_item_title.replace(": ", "")

			# Add the media item key to the media dictionary if it is not already present
			if media_item_title not in media["Dictionary"]:
				media["Dictionary"][media_item_title] = 0

			# Add one to the number of times the media item was played
			media["Dictionary"][media_item_title] += 1

		# Define the media inside the "Numbers" dictionary as zero if it is not there already
		if media_title not in dictionary["Numbers"]:
			dictionary["Numbers"][media_title] = 0

		# Define a shortcut for the media variable
		media = dictionary["Numbers"][media_title]

		# If the media variable is an integer
		if isinstance(media, int):
			# Add one to the number of times the media was watched
			dictionary["Numbers"][media_title] += 1

		else:
			# Add one to the number of times the media was watched in the "Total" key
			media["Total"] += 1

		# ---------- #

		return dictionary, media_title

	def Iterate_Through_Entries(self, dictionary, month = True):
		# Iterate through the entries dictionary
		for entry in dictionary["Entries"]["Dictionary"].values():
			# Define the media dictionary (media or media item), and add the media watched numbers
			dictionary, media_title = self.Define_Media_Dictionary(dictionary, entry)

			# Add one to the total number of media watched in the year or month
			dictionary["Total"] += 1

		return dictionary

	def Update_Statistics(self, media_titles, media_type):
		# Import the "Diary_Slim" module
		from Diary_Slim.Diary_Slim import Diary_Slim as Diary_Slim

		# Define the "Diary_Slim" class inside this class
		self.Diary_Slim = Diary_Slim()

		# Get the "diary_slim" dictionary from the class above
		self.diary_slim = self.Diary_Slim.diary_slim

		# ---------- #

		# Define a local dictionary of statistics
		statistics = {
			"Module": "Watch_History",
			"Statistic key": "Watched media",
			"Year": {},
			"Month": {},
			"Text": "",
			"Dictionary": {
				"Numbers": {
					"Year": {
						"Old": 0,
						"New": 1
					},
					"Month": {
						"Old": 0,
						"New": 1
					}
				},
				"Text": ""
			}
		}

		# Define a shortcut for the statistic key
		statistic_key = statistics["Statistic key"]

		# ---------- #

		# Iterate through the list of keys
		for key in ["Year", "Month"]:
			# Define the default dictionary as the year dictionary
			dictionary = self.diary_slim["Current year"]

			# If the key is "Month"
			if key == "Month":
				# Define the default dictionary as the month dictionary
				dictionary = self.diary_slim["Current year"]["Month"]

			# Get the year statistics for the "Stories" module
			statistics[key] = dictionary["Statistics"][statistic_key]

			# If the story title is not inside the dictionary of stories
			if media_titles["Original"] not in statistics[key]["Dictionary"]:
				# Create the story statistics dictionary
				statistics[key]["Dictionary"][media_titles["Original"]] = 0

			# Add one to the total number of statistics
			statistics[key]["Total"] += 1

			# Define the old number as the current number
			statistics["Dictionary"]["Numbers"][key]["Old"] = statistics[key]["Dictionary"][media_titles["Original"]]

			# Update the number of times watched played in the defined media dictionary
			statistics[key]["Dictionary"][media_titles["Original"]] += 1

			# Define the new number as the current number (with the added number)
			statistics["Dictionary"]["Numbers"][key]["New"] = statistics[key]["Dictionary"][media_titles["Original"]]

		# Define the statistic text, formatting the template with the language media title
		statistics["Dictionary"]["Text"] = self.language_texts["times_that_i_watched_{}_{}"].format(media_type, media_titles["Language"])

		# ---------- #

		# Update the external statistics of the current year using the "Update_External_Statistics" root method of the "Diary_Slim" class
		# And return the statistics text
		return self.Diary_Slim.Update_External_Statistics(statistic_key, statistics)

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

		# Get the media type "Information.json" file and read it
		dictionary["JSON"] = self.JSON.To_Python(dictionary["Folders"]["Media information"]["Information"])

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

		# If the option or number keys are present, define them
		for key in ["option", "number"]:
			if key in options:
				dictionary[key] = options[key]

		# Get the media type media numbers
		numbers = self.JSON.To_Python(self.folders["Media information"]["Information"])["Numbers"]

		# Add the number of media inside each media type text
		i = 0
		for plural_media_type in self.media_types["Plural"]["en"]:
			if plural_media_type in dictionary["List"]["en"]:
				for language in self.languages["small"]:
					dictionary["List"][language][i] = dictionary["List"][language][i] + " (" + str(numbers[plural_media_type]) + ")"

				i += 1

		# Select the media type
		if (
			"option" not in dictionary and
			"number" not in dictionary
		):
			dictionary["option"] = self.Input.Select(dictionary["List"]["en"], dictionary["List"][self.user_language], show_text = dictionary["Texts"]["Show"], select_text = dictionary["Texts"]["Select"])["option"]

		if "number" in dictionary:
			dictionary["option"] = dictionary["List"]["en"][dictionary["number"]]

		dictionary["option"] = dictionary["option"].split(" (")[0]

		# Get the selected media type dictionary from the media types dictionary
		dictionary.update(self.media_types[dictionary["option"]])

		# Get the status from the options dictionary
		if (
			options != None and
			"Status" in options
		):
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

		dictionary["Texts"]["Select"] = self.language_texts["select_{}_to_watch"].format(dictionary["Media type"]["Genders"][self.user_language]["a"] + " " + text.lower())

		# Select the media
		if "Title" not in media:
			language_options = dictionary["Media type"]["Media list"]

			if "Media list (option)" in dictionary["Media type"]:
				language_options = dictionary["Media type"]["Media list (option)"]

			media.update({
				"Title": self.Input.Select(dictionary["Media type"]["Media list"], language_options = language_options, show_text = dictionary["Texts"]["Show"], select_text = dictionary["Texts"]["Select"])["option"]
			})

		sanitized_title = self.Sanitize_Title(media["Title"])

		if media["Title"] != "[" + self.Language.language_texts["finish_selection"] + "]":
			# Define the media information and local media folder
			if "Folders" in media:
				if "root" not in media["Folders"]:
					media["Folders"].update({
						"root": dictionary["Media type"]["Folders"]["Media information"]["root"] + self.Sanitize(sanitized_title, restricted_characters = True) + "/"
					})

				media["Folders"].update({
					"Media": {
						"root": dictionary["Media type"]["Folders"]["Media"]["root"] + dictionary["Media"]["Titles"]["Sanitized"] + "/"
					}
				})

				if sanitized_title + "/" not in media["Folders"]["Media"]["root"]:
					media["Folders"]["Media"]["root"] += self.Sanitize(sanitized_title, restricted_characters = True) + "/"

			if "Folders" not in media:
				media["Folders"] = {
					"root": dictionary["Media type"]["Folders"]["Media information"]["root"] + self.Sanitize(sanitized_title, restricted_characters = True) + "/",
					"Media": {
						"root": dictionary["Media type"]["Folders"]["Media"]["root"] + self.Sanitize_Title(sanitized_title) + "/"
					}
				}

			# Create the root media folder
			self.Folder.Create(media["Folders"]["Media"]["root"])

			# If the item is the media, not a media item
			if (
				self.item == False and
				"States" in media and
				"Media item list" in media["States"] and
				media["States"]["Media item list"] == False or
				self.item == True
			):
				# Define the list of media folders to create
				folders = [
					"Pictures",
					"Covers"
				]

				# If the item variable is True, that means it is a media item
				if self.item == True:
					# Remove the "Covers" folder
					folders.remove("Covers")

				# Define the language texts dictionary variable for easier typing
				language_texts = self.Language.language_texts

				# Define the dictionary variable for easier typing
				folders_dictionary = media["Folders"]["Media"]

				for name in folders:
					# Define the folder name variable
					folder_name = name

					# Define the text key for the name of the folder
					text_key = name.lower().replace(" ", "_")

					if "_" not in text_key:
						text_key += ", title()"

					# If the key is present inside the language texts dictionary
					if text_key in language_texts:
						# Define the folder name variable as the folder name in the user language
						folder_name = language_texts[text_key]

					# Define the folder inside the dictionary
					folders_dictionary[name] = {
						"root": folders_dictionary["root"] + folder_name + "/"
					}

					# Create the folder
					self.Folder.Create(folders_dictionary[name]["root"])

			# Define the list of restricted files that are not a folder
			restricted_files = [
				"details",
				"dates",
				"channel",
				"playlist",
				"season",
				"anime",
				"cartoon",
				"series",
				"movie"
			]

			# Create the folders
			for key in media["Folders"]:
				if key not in restricted_files:
					folder = media["Folders"][key]

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

				if (
					self.item == True and
					media["Title"] != dictionary["Media"]["Title"] and
					dictionary["Media type"]["Plural"]["en"] != self.texts["movies, title()"]["en"]
				):
					media["Information"]["File name"] = "Season"

				file_names.append(media["Information"]["File name"] + ".json")

			# Define the "Channel.json" or "Playlist.json" file for video media
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
					texts_list = self.Language.language_texts

				if key == "dates":
					texts_list = self.Date.language_texts

				if ".json" not in file_name:
					file_name = texts_list[key + ", title()"] + ".txt"

				media["Folders"][key] = media["Folders"]["root"] + file_name
				self.File.Create(media["Folders"][key])

			if self.File.Contents(media["Folders"][media["Information"]["Key"]])["lines"] != []:
				media["Information"]["Dictionary"] = self.JSON.To_Python(media["Folders"][media["Information"]["Key"]])

			# Define the media details
			media["Details"] = self.File.Dictionary(media["Folders"]["details"])

			# If the "Item" variable is True
			if self.item == True:
				# Define the default "Last season" state
				media["Last season"] = False

				# If the key is inside the details dictionary
				if self.language_texts["last_season"] in media["Details"]:
					# Define it as True or False
					media["Last season"] = self.Input.Define_Yes_Or_No(media["Details"][self.language_texts["last_season"]])

			# If the "Item" variable is False
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
				if self.Language.language_texts["original_language"] in media["Details"]:
					media["Language"] = media["Details"][self.Language.language_texts["original_language"]]

				if media["Language"] in list(self.languages["full"].values()):
					# Iterate through the full languages list to find the small language from the full language
					for small_language in self.languages["full"]:
						full_language = self.languages["full"][small_language]

						if full_language == media["Language"]:
							media["Full language"] = full_language
							media["Language"] = small_language

				states = deepcopy(self.states)

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
					if (
						self.Language.language_texts["origin_type"] in media["Details"] and
						media["Details"][self.Language.language_texts["origin_type"]] == self.Language.language_texts[key.lower() + ", title()"]
					):
						media["States"][key] = True

				media["States"]["Remote"] = False

				if self.Language.language_texts["origin_type"] not in media["Details"]:
					media["States"]["Remote"] = True

					media["Details"][self.Language.language_texts["origin_type"]] = self.Language.language_texts["remote, title()"]

				# Define video state for videos
				if dictionary["Media type"]["Plural"]["en"] == self.texts["videos, title()"]["en"]:
					media["States"]["Video"] = True
					media["States"]["Episodic"] = False

				if self.Language.language_texts["episodic, title()"] in media["Details"]:
					media["States"]["Episodic"] = self.Input.Define_Yes_Or_No(media["Details"][self.Language.language_texts["episodic, title()"]])

				# Define the single unit state
				if self.language_texts["single_unit"] in media["Details"]:
					media["States"]["Single unit"] = self.Input.Define_Yes_Or_No(media["Details"][self.language_texts["single_unit"]])

				# Define non-series media state for movies
				if dictionary["Media type"]["Plural"]["en"] == self.texts["movies, title()"]["en"]:
					media["States"]["Series media"] = False

				if media["States"]["Video"] == True:
					dictionary["Media"]["Folders"]["channel"] = dictionary["Media"]["Folders"]["root"] + "Channel.json"
					self.File.Create(dictionary["Media"]["Folders"]["channel"])

					if self.File.Contents(dictionary["Media"]["Folders"]["channel"])["lines"] == []:
						# Get channel information
						dictionary["Media"]["Channel"] = self.Get_YouTube_Information("channel", dictionary["Media"]["Details"]["ID"])

						if "Localized" in dictionary["Media"]["Channel"]:
							dictionary["Media"]["Channel"].pop("Localized")

						# Define channel date
						channel_date = self.Date.From_String(dictionary["Media"]["Channel"]["Date"])

						# Update "Date" key of media details
						dictionary["Media"]["Details"][self.Date.language_texts["start_date"]] = channel_date["Formats"]["HH:MM DD/MM/YYYY"]

						# Update "Year" key of media details
						dictionary["Media"]["Details"][self.Date.language_texts["year, title()"]] = channel_date["Units"]["Year"]

						# Update media details dictionary
						self.File.Edit(dictionary["Media"]["Folders"]["details"], self.Text.From_Dictionary(dictionary["Media"]["Details"]), "w")

						# Update "Channel.json" file
						self.JSON.Edit(dictionary["Media"]["Folders"]["channel"], dictionary["Media"]["Channel"])

					else:
						# Get channel information
						dictionary["Media"]["Channel"] = self.JSON.To_Python(dictionary["Media"]["Folders"]["channel"])

				# Define remote origin for animes or videos media type
				if self.Language.language_texts["remote_origin"] not in dictionary["Media"]["Details"]:
					remote_origin = "None"

					if dictionary["Media type"]["Plural"]["en"] == self.texts["animes, title()"]["en"]:
						remote_origin = "Animes Vision"

					if dictionary["Media type"]["Plural"]["en"] == self.texts["videos, title()"]["en"]:
						remote_origin = "YouTube"

					if remote_origin != "None":
						dictionary["Media"]["Details"][self.Language.language_texts["remote_origin"]] = remote_origin

				# Define Re-watching state for Re-watching status
				if (
					self.Language.language_texts["status, title()"] in media["Details"] and
					media["Details"][self.Language.language_texts["status, title()"]] == self.language_texts["re_watching, title()"]
				):
					media["States"]["Re-watching"] = True

				media["Episode"] = {
					"Title": "",
					"Titles": {},
					"Sanitized": "",
					"Number": 1,
					"Number text": "1",
					"Separator": ""
				}

				if (
					media["States"]["Remote"] == True or
					self.Language.language_texts["remote_origin"] in media["Details"]
				):
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
		# Get the class that called the function
		import inspect

		self.caller = inspect.stack()[3][1].split("\\")[-2]

		# If the media is series media
		if dictionary["Media"]["States"]["Series media"] == True:
			# Define the media items dictionary with the folders and number keys
			dictionary["Media"]["Items"] = {
				"Folders": {
					"root": dictionary["Media"]["Folders"]["root"] + dictionary["Media type"]["Subfolders"]["Plural"] + "/"
				},
				"Number": 1,
				"Current": "",
				"List": []
			}

			# If the media items folder exists
			if (
				self.Folder.Exist(dictionary["Media"]["Items"]["Folders"]["root"]) == True or
				dictionary["Media"]["States"]["Media item list"] == True
			):
				# The media has a media items list
				dictionary["Media"]["States"]["Media item list"] = True

				# Iterate through item type keys
				for name in ["List", "Current"]:
					key = name

					if name == "List":
						key = "Plural"

					# Define the item type text file
					dictionary["Media"]["Items"]["Folders"][name.lower()] = dictionary["Media"]["Items"]["Folders"]["root"] + dictionary["Media type"]["Subfolders"][key] + ".txt"

					# Create the file
					self.File.Create(dictionary["Media"]["Items"]["Folders"][name.lower()])

					# Get the contents of the text file
					dictionary["Media"]["Items"][name] = self.File.Contents(dictionary["Media"]["Items"]["Folders"][name.lower()])["lines"]

					# If the name is "Current" and the file contents are not empty
					if (
						name == "Current" and
						dictionary["Media"]["Items"][name] != []
					):
						# Define the contents as the first line of the text file
						dictionary["Media"]["Items"][name] = dictionary["Media"]["Items"][name][0]

					# If the item type is "List"
					if name == "List":
						# Define the items number as the number of lines of the text file
						dictionary["Media"]["Items"]["Number"] = len(dictionary["Media"]["Items"]["List"])

				# Define media item folders
				for name in dictionary["Media"]["Items"]["List"]:
					name = self.Sanitize_Title(name)

					dictionary["Media"]["Items"]["Folders"][name] = dictionary["Media"]["Items"]["Folders"]["root"] + name + "/"
					self.Folder.Create(dictionary["Media"]["Items"]["Folders"][name])

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
						"root": dictionary["Media"]["Items"]["Folders"]["root"] + self.Sanitize_Title(media_list_item) + "/"
					}

					# Define details file
					folders["details"] = folders["root"] + self.Language.language_texts["details, title()"] + ".txt"

					# Read details file
					details = self.File.Dictionary(folders["details"])

					# If the media item is a single unit media item and the "Type" key is inside the details
					if self.Language.language_texts["type, title()"] in details:
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
							if details[self.Language.language_texts["type, title()"]] == secondary_type:
								for item_type in ["Singular", "Plural"]:
									for language in self.languages["small"]:
										secondary_type = self.secondary_types[item_type][language][i]

										if secondary_type not in dictionary["Media"]["Items"]["Secondary types"][item_type][language]:
											# Add the item type to the secondary types list
											dictionary["Media"]["Items"]["Secondary types"][item_type][language].append(secondary_type)

							i += 1

					# If the "Status" key is present inside the details dictionary and the status is "Completed", remove the media item from the media items list
					if (
						self.Language.language_texts["status, title()"] in details and
						details[self.Language.language_texts["status, title()"]] == self.Language.language_texts["completed, title()"]
					):
						items_list.remove(media_list_item)

					if (
						self.caller == "Fill_Media_Files" and
						self.language_texts["single_unit"] not in details and
						dictionary["Media"]["States"]["Video"] == False
					):
						# Define titles folder
						folders["titles"] = {
							"root": folders["root"] + self.Language.language_texts["titles, title()"] + "/"
						}

						# Define titles files
						for language in self.languages["small"]:
							full_language = self.languages["full"][language]

							folders["titles"][language] = folders["titles"]["root"] + full_language + ".txt"

						# Remove media item from the media items list if its titles file is filled (for "Fill_Media_Files")
						if self.File.Contents(folders["titles"]["en"])["length"] > 0:
							items_list.remove(media_list_item)

					if (
						self.language_texts["single_unit"] in details and
						media_list_item in items_list
					):
						items_list.remove(media_list_item)

				if (
					dictionary["Media"]["States"]["Video"] == True or
					select_media_item == True
				):
					if (
						watch == True and
						len(items_list) != 1
					):
						title = self.Input.Select(items_list, show_text = show_text, select_text = select_text)["option"]

				if media_item != None:
					title = media_item

				#if (
				#	watch == False and
				#	len(items_list) == 1 and
				#	"Fill media files" not in dictionary and
				#	"Watch list of media" not in dictionary
				#):
				#	print()
				#	print("---")
				#	print()
				#	print(self.Text.Capitalize(dictionary["Media type"]["Subfolders"]["Current"]) + ":")
				#	print(title)

				sanitized_title = self.Sanitize_Title(title)

				# Define media item dictionary with titles and folder
				dictionary["Media"]["Item"] = {
					"Title": title,
					"Titles": {},
					"With media title": {},
					"Sanitized": sanitized_title,
					"Folders": {
						"root": dictionary["Media"]["Items"]["Folders"]["root"] + sanitized_title + "/"
					},
					"Number": 0
				}

				dictionary["Media"]["Episodes"]["Number"] = 0

				i = 0
				for name in dictionary["Media"]["Items"]["List"]:
					if dictionary["Media"]["Item"]["Title"] == name:
						dictionary["Media"]["Item"]["Number"] = i

					# Get media item details file
					folder = dictionary["Media"]["Items"]["Folders"]["root"] + self.Sanitize_Title(name) + "/"
					details_file = folder + self.Language.language_texts["details, title()"] + ".txt"
					details = self.File.Dictionary(details_file)

					# If the item is not a single unit, add its episode number to the root episode number
					if self.language_texts["single_unit"] not in details:
						titles_folder = folder + self.Language.language_texts["titles, title()"] + "/"
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
					after_key = self.Language.language_texts["romanized_title"]

				if after_key not in dictionary["Media"]["Details"]:
					after_key = self.Language.language_texts["title, title()"]

				if self.Language.language_texts["id, upper()"] in dictionary["Media"]["Details"]:
					after_key = self.Language.language_texts["id, upper()"]

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
						if (
							"OVA" not in plural_type and
							"ONA" not in plural_type
						):
							plural_type = plural_type.lower()

						secondary_types.append(plural_type)

					key += self.Text.From_List(secondary_types)

				# Add the media subfolders plural text before the "Episodes" key or update it
				key_value = {
					"key": key,
					"value": dictionary["Media"]["Items"]["Number"]
				}

				after_key = self.language_texts["episodes, title()"]

				dictionary["Media"]["Details"] = self.JSON.Add_Key_After_Key(dictionary["Media"]["Details"], key_value, after_key = after_key, number_to_add = 0)

				# If the media has secondary types and the items list plural text key is inside the details
				if (
					"Secondary types" in dictionary["Media"]["Items"] and
					dictionary["Media type"]["Subfolders"]["Plural"] in dictionary["Media"]["Details"]
				):
					# Remove the key
					dictionary["Media"]["Details"].pop(dictionary["Media type"]["Subfolders"]["Plural"])

				dict_ = deepcopy(dictionary["Media"]["Details"])

				if self.Language.language_texts["remote_origin"] in dict_:
					if dict_[self.Language.language_texts["remote_origin"]] == "Animes Vision":
						dict_.pop(self.Language.language_texts["remote_origin"])

					elif dict_[self.Language.language_texts["remote_origin"]] == "YouTube":
						dict_.pop(self.Language.language_texts["remote_origin"])

				# Update the media details file
				self.File.Edit(dictionary["Media"]["Folders"]["details"], self.Text.From_Dictionary(dict_), "w")

				# ------------------------------ #

				# Run the "Select_Media" method to define the variables

				# Select the media item to define its variables
				dictionary = self.Select_Media(dictionary, item = True)

				# ------------------------------ #

				# Fill the "With media title" dictionary

				# Iterate through the list of small languages
				for language in self.languages["small"]:
					# Get the media title in the current language
					media_title = self.Get_Media_Title(dictionary, language = language)

					# Define the local empty title
					title = ""

					# Get the correct media item title in the current language
					item_title = self.Get_Media_Title(dictionary, language = language, item = True)

					# Define the separator
					separator = " "

					# If the item title has a colon and a space at the start
					if item_title[0] + item_title[1] == ": ":
						# Define the separator as an empty string
						separator = ""

					# Add the original media title if it is not present in the item title
					if media_title not in item_title:
						title += media_title + separator

					# Add the item title to the local title
					title += item_title

					# Define the root language title as the local title
					dictionary["Media"]["Item"]["With media title"][language] = title

				# ------------------------------ #

				# Define the single unit state as False
				dictionary["Media"]["States"]["Single unit"] = False

				# Define the single unit state
				if self.language_texts["single_unit"] in dictionary["Media"]["Item"]["Details"]:
					dictionary["Media"]["States"]["Single unit"] = self.Input.Define_Yes_Or_No(dictionary["Media"]["Item"]["Details"][self.language_texts["single_unit"]])

				if dictionary["Media"]["States"]["Single unit"] == True:
					dictionary["Media"]["Item"]["Folders"]["Media"]["root"] = dictionary["Media"]["Folders"]["Media"]["root"]

				# Reset the "Media item is media" state to its default value
				dictionary["Media"]["States"]["Media item is media"] = False

				# Define if the media item is the media
				if (
					dictionary["Media"]["Item"]["Title"] == dictionary["Media"]["Title"] or
					"Romanized" in dictionary["Media"]["Item"]["Titles"] and
					dictionary["Media"]["Item"]["Titles"]["Romanized"] == dictionary["Media"]["Titles"]["Romanized"]
				):
					dictionary["Media"]["States"]["Media item is media"] = True

			# If the folder of media items does not exist, define that the media has no media item list
			# And add the root media to the media items list
			if (
				self.Folder.Exist(dictionary["Media"]["Items"]["Folders"]["root"]) == False and
				dictionary["Media"]["States"]["Media item list"] == False
			):
				#dictionary["Media"]["States"]["Media item list"] = False

				dictionary["Media"]["Items"]["List"] = [
					dictionary["Media"]["Title"]
				]

				dictionary["Media"]["States"]["Media item is media"] = True

		# Define media item as the media for media that has no media item list
		if (
			dictionary["Media"]["States"]["Series media"] == False or
			dictionary["Media"]["States"]["Media item list"] == False
		):
			dictionary["Media"]["Item"] = dictionary["Media"].copy()

		# Create the "Watched" folder
		dictionary["Media"]["Item"]["Folders"]["Watched"] = {
			"root": dictionary["Media"]["Item"]["Folders"]["root"] + self.language_texts["watched, title()"] + "/"
		}

		self.Folder.Create(dictionary["Media"]["Item"]["Folders"]["Watched"]["root"])

		# Create the "Watched" files
		files = [
			"Entries.json",
			"Entry list.txt"
		]

		for file in files:
			key = file.lower().split(".")[0].replace(" ", "_")

			dictionary["Media"]["Item"]["Folders"]["Watched"][key] = dictionary["Media"]["Item"]["Folders"]["Watched"]["root"] + file
			self.File.Create(dictionary["Media"]["Item"]["Folders"]["Watched"][key])

		# Create "Files" folder file inside "Watched" folder
		dictionary["Media"]["Item"]["Folders"]["Watched"]["files"] = {
			"root": dictionary["Media"]["Item"]["Folders"]["Watched"]["root"] + self.File.language_texts["files, title()"] + "/"
		}

		self.Folder.Create(dictionary["Media"]["Item"]["Folders"]["Watched"]["files"]["root"])

		# Define the "Watched" dictionary as the template
		self.dictionaries["Watched"] = deepcopy(self.template)

		# Get the "Watched" dictionary from file if the dictionary is not empty and has entries
		if (
			self.File.Contents(dictionary["Media"]["Item"]["Folders"]["Watched"]["entries"])["lines"] != [] and
			self.JSON.To_Python(dictionary["Media"]["Item"]["Folders"]["Watched"]["entries"])["Entries"] != []
		):
			self.dictionaries["Watched"] = self.JSON.To_Python(dictionary["Media"]["Item"]["Folders"]["Watched"]["entries"])

		# Update the number of entries with the length of the entries list
		self.dictionaries["Watched"]["Numbers"]["Total"] = len(self.dictionaries["Watched"]["Entries"])

		# Create the "Comments" folder
		dictionary["Media"]["Item"]["Folders"]["comments"] = {
			"root": dictionary["Media"]["Item"]["Folders"]["root"] + self.Language.language_texts["comments, title()"] + "/"
		}

		self.Folder.Create(dictionary["Media"]["Item"]["Folders"]["comments"]["root"])

		# Create the "Files" folder inside the "Comments" folder
		dictionary["Media"]["Item"]["Folders"]["comments"]["files"] = {
			"root": dictionary["Media"]["Item"]["Folders"]["comments"]["root"] + self.File.language_texts["files, title()"] + "/"
		}

		self.Folder.Create(dictionary["Media"]["Item"]["Folders"]["comments"]["files"]["root"])

		# Define media comments folder comments file
		dictionary["Media"]["Item"]["Folders"]["comments"]["comments"] = dictionary["Media"]["Item"]["Folders"]["comments"]["root"] + self.Language.texts["comments, title()"]["en"] + ".json"
		self.File.Create(dictionary["Media"]["Item"]["Folders"]["comments"]["comments"])

		# Define media item folders
		if (
			dictionary["Media"]["States"]["Series media"] == True and
			dictionary["Media"]["States"]["Single unit"] == False
		):
			dictionary["Media"]["Item"]["Folders"]["titles"] = {
				"root": dictionary["Media"]["Item"]["Folders"]["root"] + self.Language.language_texts["titles, title()"] + "/",
			}

			self.Folder.Create(dictionary["Media"]["Item"]["Folders"]["titles"]["root"])

			for language in self.languages["small"]:
				full_language = self.languages["full"][language]

				# Define the episode titles file
				dictionary["Media"]["Item"]["Folders"]["titles"][language] = dictionary["Media"]["Item"]["Folders"]["titles"]["root"] + full_language + ".txt"
				self.File.Create(dictionary["Media"]["Item"]["Folders"]["titles"][language])

			if dictionary["Media"]["States"]["Video"] == True:
				# Define ids file
				dictionary["Media"]["Item"]["Folders"]["titles"]["ids"] = dictionary["Media"]["Item"]["Folders"]["titles"]["root"] + self.Language.language_texts["ids, title()"] + ".txt"
				self.File.Create(dictionary["Media"]["Item"]["Folders"]["titles"]["ids"])

			# Update the "Playlist.json" file for the video media type
			if (
				dictionary["Media"]["States"]["Video"] == True and
				dictionary["Media"]["States"]["Media item list"] == True
			):
				# Get ID (origin location) from link
				if (
					self.Language.language_texts["origin_location"] in dictionary["Media"]["Item"]["Details"] and
					dictionary["Media"]["Item"]["Details"][self.Language.language_texts["origin_location"]] == "?"
				):
					dictionary["Media"]["Item"]["Details"][self.Language.language_texts["origin_location"]] = dictionary["Media"]["Item"]["Details"][self.Language.language_texts["link, title()"]].split("list=")[-1]

				dictionary["Media"]["Item"]["Folders"]["playlist"] = dictionary["Media"]["Item"]["Folders"]["root"] + "Playlist.json"
				self.File.Create(dictionary["Media"]["Item"]["Folders"]["playlist"])

				if (
					self.File.Contents(dictionary["Media"]["Item"]["Folders"]["playlist"])["lines"] == [] and
					dictionary["Media"]["Item"]["Details"][self.Language.language_texts["origin_location"]] != "?"
				):
					# Get the playlist information
					dictionary["Media"]["Item"]["Playlist"] = self.Get_YouTube_Information("playlist", dictionary["Media"]["Item"]["Details"][self.Language.language_texts["origin_location"]])

					if "Date" in dictionary["Media"]["Item"]["Playlist"]:
						# Define the playlist date variable
						dictionary["Media"]["Item"]["Playlist"]["Date"] = self.Date.From_String(dictionary["Media"]["Item"]["Playlist"]["Date"])

						# Get the playlist date
						playlist_date = dictionary["Media"]["Item"]["Playlist"]["Date"]

						# Define the IDs file
						ids_file = dictionary["Media"]["Item"]["Folders"]["titles"]["root"] + self.Language.language_texts["ids, title()"] + ".txt"

						# Get the list of video IDs
						ids_list = self.File.Contents(ids_file)["lines"]

						# If the list of IDs is not empty
						if ids_list != []:
							# Get the first video ID
							first_video_id = ids_list[0]

							# Get the first video date
							first_video_date = self.Date.From_String(self.Get_YouTube_Information("video", first_video_id)["Date"])

							# If the first video date is older than playlist creation date
							# Define the playlist time as the video date
							if first_video_date["Object"] < playlist_date["Object"]:
								dictionary["Media"]["Item"]["Playlist"]["Date"] = first_video_date

							# If the first video date is newer than playlist creation date
							# Define the playlist time as the playlist date
							if first_video_date["Object"] > playlist_date["Object"]:
								dictionary["Media"]["Item"]["Playlist"]["Date"] = playlist_date

							# Update the "Start date" key of the media item details
							dictionary["Media"]["Item"]["Details"][self.Date.language_texts["start_date"]] = playlist_date["Formats"]["HH:MM DD/MM/YYYY"]

							# Get the last video ID
							last_video_id = ids_list[-1]

							# Get the last video date
							last_video_date = self.Date.From_String(self.Get_YouTube_Information("video", last_video_id)["Date"])

							# Update the "End date" key of the media item details
							dictionary["Media"]["Item"]["Details"][self.Date.language_texts["end_date"]] = last_video_date["Formats"]["HH:MM DD/MM/YYYY"]

							# Update "Year" key of media item details
							dictionary["Media"]["Item"]["Details"][self.Date.language_texts["year, title()"]] = dictionary["Media"]["Item"]["Playlist"]["Date"]["Units"]["Year"]

							# Update media item details dictionary
							self.File.Edit(dictionary["Media"]["Item"]["Folders"]["details"], self.Text.From_Dictionary(dictionary["Media"]["Item"]["Details"]), "w")

						# Update the playlist date back to the correct (ISO) format
						dictionary["Media"]["Item"]["Playlist"]["Date"] = playlist_date["UTC"]["DateTime"]["Formats"]["YYYY-MM-DDTHH:MM:SSZ"]

					# Update the "Playlist.json" file
					self.JSON.Edit(dictionary["Media"]["Item"]["Folders"]["playlist"], dictionary["Media"]["Item"]["Playlist"])

				if (
					self.File.Contents(dictionary["Media"]["Item"]["Folders"]["playlist"])["lines"] != [] and
					dictionary["Media"]["Item"]["Details"][self.Language.language_texts["origin_location"]] != "?"
				):
					# Get playlist from JSON file
					dictionary["Media"]["Item"]["Playlist"] = self.JSON.To_Python(dictionary["Media"]["Item"]["Folders"]["playlist"])

		folder = dictionary["Media"]["Item"]["Folders"]["comments"]

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
		if (
			self.File.Contents(folder["comments"])["lines"] != [] and
			self.JSON.To_Python(folder["comments"])["Entries"] != []
		):
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
		self.JSON.Edit(dictionary["Media"]["Item"]["Folders"]["Watched"]["entries"], self.dictionaries["Watched"])

		# Define the media item files
		dictionary["Media"]["Item"]["Folders"]["dates"] = dictionary["Media"]["Item"]["Folders"]["root"] + self.Date.language_texts["dates, title()"] + ".txt"
		self.File.Create(dictionary["Media"]["Item"]["Folders"]["dates"])

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
				dictionary["Media"]["Item"]["Episodes"]["Titles"]["Files"]["IDs"] = dictionary["Media"]["Item"]["Folders"]["titles"]["ids"]
				dictionary["Media"]["Item"]["Episodes"]["Titles"]["IDs"] = self.File.Contents(dictionary["Media"]["Item"]["Episodes"]["Titles"]["Files"]["IDs"])["lines"]

			# Define episode titles files and lists
			for language in self.languages["small"]:
				full_language = self.languages["full"][language]

				if dictionary["Media"]["States"]["Single unit"] == False:
					# Define episode titles on titles dictionary file
					dictionary["Media"]["Item"]["Episodes"]["Titles"]["Files"][language] = dictionary["Media"]["Item"]["Folders"]["titles"][language]

					# Get language episode titles from file
					dictionary["Media"]["Item"]["Episodes"]["Titles"][language] = self.File.Contents(dictionary["Media"]["Item"]["Episodes"]["Titles"]["Files"][language])["lines"]

				# Iterate through the episode titles list
				if (
					dictionary["Media"]["Episode"]["Separator"] != "" and
					dictionary["Media"]["States"]["Single unit"] == False
				):
					import re

					i = 1
					for episode_title in dictionary["Media"]["Item"]["Episodes"]["Titles"][language]:
						number = str(self.Text.Add_Leading_Zeroes(i))

						separator = dictionary["Media"]["Episode"]["Separator"]

						if (
							separator == "EP" and
							self.Language.language_texts["episodic, title()"] not in dictionary["Media"]["Details"]
						):
							dictionary["Media"]["States"]["Episodic"] = True

						for alternative_episode_type in self.alternative_episode_types:
							if re.search(alternative_episode_type + " [0-9]{1,2}", episode_title) != None:
								separator = ""

								if self.Language.language_texts["episodic, title()"] not in dictionary["Media"]["Details"]:
									dictionary["Media"]["States"]["Episodic"] = True

						if self.Language.language_texts["type, title()"] in dictionary["Media"]["Item"]["Details"]:
							separator = ""

						# Add episode number name to local episode title
						episode_title = separator + number + " " + episode_title

						# Add episode number name to episode titles if the separator is not empty and the number name is not present
						if (
							separator != "" and
							number not in dictionary["Media"]["Item"]["Episodes"]["Titles"][language][i - 1]
						):
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

			if after_key not in dictionary["Media"]["Item"]["Details"]:
				after_key = self.Date.language_texts["start_date"]

			if after_key not in dictionary["Media"]["Item"]["Details"]:
				after_key = self.Language.language_texts["romanized_title"]

			if after_key not in dictionary["Media"]["Item"]["Details"]:
				after_key = self.Language.language_texts["title, title()"]

			if self.Language.language_texts["id, upper()"] in dictionary["Media"]["Item"]["Details"]:
				after_key = self.Language.language_texts["id, upper()"]

			if self.language_texts["single_unit"] not in dictionary["Media"]["Item"]["Details"]:
				dictionary["Media"]["Item"]["Details"] = self.JSON.Add_Key_After_Key(dictionary["Media"]["Item"]["Details"], key_value, after_key = after_key)

			# Update media item details file
			self.File.Edit(dictionary["Media"]["Item"]["Folders"]["details"], self.Text.From_Dictionary(dictionary["Media"]["Item"]["Details"]), "w")

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
		if self.Language.language_texts["type, title()"] in dictionary["Media"]["Item"]["Details"]:
			dictionary["Media"]["Item"]["Type"] = dictionary["Media"]["Item"]["Details"][self.Language.language_texts["type, title()"]]

		# Define the container, item, and unit for series media
		if dictionary["Media"]["States"]["Series media"] == True:
			# Define the unit text as the "episode" text per language
			dictionary["Media"]["texts"]["unit"] = {}

			for language in self.languages["small"]:
				dictionary["Media"]["texts"]["unit"][language] = self.texts["episode"][language]

			if (
				dictionary["Media"]["States"]["Media item list"] == True and
				dictionary["Media"]["Item"]["Title"] != dictionary["Media"]["Title"]
			):
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
							#dictionary["Media"]["texts"]["unit"][language] = singular_type
							dict_[language] = singular_type

					i += 1

				dictionary["Media"]["Item"]["Type"] = dict_

			# Define the item text as the "season" text for media that have a media item list
			if (
				dictionary["Media"]["States"]["Media item list"] == True and
				dictionary["Media"]["Item"]["Title"] != dictionary["Media"]["Title"] and
				dictionary["Media"]["texts"]["item"] == {}
			):
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

						if dictionary["Media"]["texts"][key][language] == self.texts["episode"][language]:
							for gender_key in dict_["genders"][language]:
								gender = dict_["genders"][language][gender_key]

								if text_type == gender_key:
									item_text = self.media_types["Genders"][language]["masculine"][gender_key]

						text = dictionary["Media"]["texts"][key][language].lower()

						if "youtube" in text:
							text = text.replace("youtube", "YouTube")

						dictionary["Media"]["texts"][text_type + "_" + key][language] = item_text + " " + text

		# Add the "Christmas special" text to the unit text
		if (
			dictionary["Media"]["States"]["Video"] == False and
			self.Today_Is_Christmas == True
		):
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
					self.Language.texts["on_hold, title()"]["en"],
					self.texts["watching, title()"]["en"],
					self.texts["re_watching, title()"]["en"]
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

		# Iterate through the states keys
		for key in keys:
			# If the state is true
			if (
				key in dictionary["Media"]["States"] and
				dictionary["Media"]["States"][key] == True or
				key in dictionary["Media"]["States"]["Dubbing"] and
				dictionary["Media"]["States"]["Dubbing"][key] == True
			):
				# If the key has a different state text, get it
				if key in state_texts:
					key = state_texts[key]

				# Define the state as true
				state = True

				# If the key is the "Re-watched" key, get its state dictionary
				if key == "Re-watched":
					state = {
						"Times": dictionary["Media"]["Episode"]["Re-watched"]["Times"]
					}

				# Define the state dictionary
				states_dictionary["States"][key] = state

				# Define the state texts of the current state dictionary
				states_dictionary["Texts"][key] = {}

				for language in self.languages["small"]:
					text = ""

					if key != "Re-watched":
						# Define the text key
						text_key = key.lower().replace(" ", "_")

						# If a underscore does not exist inside the text key, the text key is a word, then add the ", title()" text
						if "_" not in text_key:
							text_key += ", title()"

						# If the text key is inside the texts dictionary of Watch_History, get the language text from it
						if text_key in self.texts:
							language_text = self.texts[text_key][language]

						# If the text key is inside the texts dictionary of the Language class, get the language text from it
						if text_key in self.Language.texts:
							language_text = self.Language.texts[text_key][language]

						# Define the unit text
						unit = dictionary["Media"]["texts"]["unit"][language].lower()

						# Define the unit text for series media as the unit text plus the neutral "of" text, plus the lowercased container text
						if dictionary["Media"]["States"]["Series media"] == True:
							unit = dictionary["Media"]["texts"]["unit"][language] + " " + self.Language.texts["of, neutral"][language] + " " + dictionary["Media"]["texts"]["container"][language].lower()

						# Define the language text as the "first_{}_in_year" formatted with the media unit text
						if key == "First media type entry in year":
							language_text = self.Language.texts["first_{}_in_year"][language].format(unit.lower())

						# If the media is completed
						if key == "Completed media":
							# Define the "the text" as the "the" text and the container
							the_text = dictionary["Media"]["texts"]["genders"][language]["the"] + " " + dictionary["Media"]["texts"]["container"][language].lower()

						# If the media item is completed
						if key == "Completed media item":
							# Define the item and container texts
							item_text = dictionary["Media"]["texts"]["item"][language].lower()
							container_text = dictionary["Media"]["texts"]["container"][language].lower()

							# Define the list of items to use to format the template
							items = [
								item_text,
								container_text
							]

							# Define the default template as the feminine "the {} of {}" text
							template = self.media_types["Genders"][language]["feminine"]["the"] + " {} " + dictionary["Media"]["texts"]["genders"][language]["of"] + " {}"

							# If the media has a media item list and the media item is the media
							# And the media is not completed
							# And the "Last season" key of the media item dictionary is True
							if (
								dictionary["Media"]["States"]["Media item is media"] == True and
								dictionary["Media"]["States"]["Completed media"] == False and
								dictionary["Media"]["Item"]["Last season"] == True
							):
								# Define the template as the masculine "the {}" text
								template = self.media_types["Genders"][language]["masculine"]["the"] + " {}"

								# Define the item text as the media item type text
								item_text = dictionary["Media"]["Item"]["Type"][language]

								# Remove the container text from the list of items
								items.pop(1)

							# If this is not the last season of the media
							if dictionary["Media"]["Item"]["Last season"] == False:
								# Define the item text as "season" in the current language
								items[0] = self.texts["season, title()"][language].lower()

							# If the media is a video channel
							if dictionary["Media type"]["Plural"]["en"] == self.texts["videos, title()"]["en"]:
								# Define the item text as "series" in the current language
								items[0] = self.texts["series"][language].lower()

							# If the media item is a single unit one
							if dictionary["Media"]["States"]["Single unit"] == True:
								# Define the item text as the item type text in the current language
								items[0] = dictionary["Media"]["Item"]["Type"][language].lower()

							# If the media unit is a single unit one
							if dictionary["Media"]["States"]["Single unit"] == True:
								# Replace the "the" word in the feminine gender with the masculine gender
								template = template.replace(self.media_types["Genders"][language]["feminine"]["the"] + " ", self.media_types["Genders"][language]["masculine"]["the"] + " ")

							# Format the "the text" with the list of items
							the_text = template.format(*items)

						# If the media or media item is completed, add the "the text" defined above to the "completed, past_perfect" text
						if key in ["Completed media", "Completed media item"]:
							language_text = self.Language.texts["completed, past_perfect, title()"][language] + " " + the_text

						# If the "youtube" text is inside the language text, correct its case
						if "youtube" in language_text:
							language_text = language_text.replace("youtube", "YouTube")

						# Add the language text to the text variable
						text += language_text

					if key == "Re-watched":
						# If the state is "Re-watched", add the Re-watched text plus the Re-watched times to the text
						text += dictionary["Media"]["Episode"]["Re-watched"]["Texts"]["Number name"][language] + " (" + str(dictionary["Media"]["Episode"]["Re-watched"]["Times"]) + "x)"

					# Define the state text per language
					states_dictionary["Texts"][key][language] = text

		return states_dictionary

	def Define_Options(self, dictionary, options):
		for key in options:
			if type(options[key]) == dict:
				if (
					key in dictionary and
					dictionary[key] != {}
				):
					for sub_key in dictionary[key]:
						if sub_key in options[key]:
							dictionary[key][sub_key] = options[key][sub_key]

					for sub_key in options[key]:
						if sub_key not in dictionary[key]:
							dictionary[key][sub_key] = options[key][sub_key]

				if (
					key not in dictionary or
					dictionary[key] == {}
				):
					dictionary[key] = options[key]

			if type(options[key]) in [str, list]:
				dictionary[key] = options[key]

		return dictionary

	def Remove_Media_Type(self, to_remove):
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

		# Iterate through the English plural media types list
		for plural_media_type in self.media_types["Plural"]["en"]:
			# If the plural media type is inside the local media types dictionary
			if plural_media_type in dictionary["Media types"]:
				# Get the media type dictionary
				media_type = dictionary["Media types"][plural_media_type]

				# Iterate through the small languages list
				for language in self.languages["small"]:
					# Create the empty language list if it does not exist
					if language not in dictionary["List"]:
						dictionary["List"][language] = []

					# Add to the plural media types list
					dictionary["List"][language].append(media_type["Plural"][language])

		return dictionary["List"]

	def Define_Media_Titles(self, dictionary, item = False):
		media = dictionary["Media"]

		if item == True:
			media = dictionary["Media"]["Item"]

		if self.File.Exist(media["Folders"]["details"]) == True:
			media["Details"] = self.File.Dictionary(media["Folders"]["details"])

			if self.Language.language_texts["original_title"] not in media["Details"]:
				text = self.Language.language_texts["original_title"] + ": {}" + "\n" + self.Language.language_texts["episode, title()"] + ": None"
				text = text.format(media["Folders"]["details"].split("/")[-2])
				self.File.Edit(media["Folders"]["details"], text, "w")

				media["Details"] = self.File.Dictionary(media["Folders"]["details"])

			# Define the titles key
			media["Titles"] = {
				"Original": media["Details"][self.Language.language_texts["original_title"]],
				"Sanitized": media["Details"][self.Language.language_texts["original_title"]],
			}

			media["Titles"]["Language"] = media["Titles"]["Original"]

			# If media type is "Animes" or the "romanized_title" key exists inside the media details, define the romanized name and ja name
			if (
				dictionary["Media type"]["Plural"]["en"] == self.texts["animes, title()"]["en"] or
				self.Language.language_texts["romanized_title"] in media["Details"]
			):
				if self.Language.language_texts["romanized_title"] in media["Details"]:
					media["Titles"]["Romanized"] = media["Details"][self.Language.language_texts["romanized_title"]]
					media["Titles"]["Language"] = media["Titles"]["Romanized"]

				if "Romanized" in media["Titles"]:
					media["Titles"]["Sanitized"] = media["Titles"]["Romanized"]

				media["Titles"]["ja"] = media["Details"][self.Language.language_texts["original_title"]]

			if (
				" (" in media["Titles"]["Original"] and
				" (" not in media["Titles"]["Language"]
			):
				media["Titles"]["Language"] = media["Titles"]["Language"] + " (" + media["Titles"]["Original"].split(" (")[-1]

				if self.user_language in media["Titles"]:
					media["Titles"][self.user_language] = media["Titles"][self.user_language] + " (" + media["Titles"]["Original"].split(" (")[-1]

			# Define the media titles per language
			for language in self.languages["small"]:
				key = self.Language.texts["title_in_language"][language][self.user_language]

				if key in media["Details"]:
					media["Titles"][language] = media["Details"][key]

			media["Titles"]["Language"] = media["Titles"]["Original"]

			if self.user_language in media["Titles"]:
				media["Titles"]["Language"] = media["Titles"][self.user_language]

			if (
				self.user_language not in media["Titles"] and
				"Romanized" in media["Titles"]
			):
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

		if language in titles:
			title = titles[language]

		if "Romanized" in titles:
			title = titles["Romanized"]

		return title

	def Sanitize_Title(self, title, remove_dot = True):
		# If the length of the title is greater than one
		# And the first two characters of the title are a space and a colon
		if (
			len(title) > 1 and
			title[0] + title[1] == ": "
		):
			# Remove them
			title = title[2:]

		if ". " in title:
			title = title.replace(". ", " ")

		elif "." in title:
			if remove_dot == True:
				title = title.replace(".", "")

		title = self.Sanitize(title, restricted_characters = True)

		return title

	def Show_Media_Title(self, root_dictionary, is_media_item = False, include_media_title = False):
		# Define a shortcut for the media dictionary
		media = root_dictionary["Media"]

		# If the "Is media item" parameter is True
		if is_media_item == True:
			# Define the shortcut for the media dictionary as one for the media item dictionary
			media = root_dictionary["Media"]["Item"]

		# Make a list of titles to show
		to_show = []

		# If the language title is the same as the original title, add it to the list
		if media["Titles"]["Language"] == media["Titles"]["Original"]:
			to_show.append(media["Titles"]["Original"])

		# If the language title is not the same as the original title
		else:
			# Add the original and language titles to the list
			to_show.append(media["Titles"]["Original"])
			to_show.append(media["Titles"]["Language"])

			# Iterate through the list of small languages
			for language in self.languages["small"]:
				# If the language is inside the dictionary of titles
				# And the media title in that language differs from the original title
				# And it is also different from the language title
				if (
					language in media["Titles"] and
					media["Titles"][language] != media["Titles"]["Original"] and
					media["Titles"][language] != media["Titles"]["Language"]
				):
					# Add the title in the specified language to the list
					to_show.append(media["Titles"][language])

					# Otherwise, there is no need to display this language title, as it has already been shown before

		# Iterate through the list of titles to show
		for title in to_show:
			# If the length of the title is greater than one
			# And the first two characters of the title are a space and a colon
			if (
				len(title) > 1 and
				title[0] + title[1] == ": "
			):
				# Remove them
				title = title[2:]

			# Show the title
			print("\t" + title)

		# If the "Include media title" parameter is True
		if include_media_title == True:
			# Show the item text
			print()
			print(self.Language.language_texts["item, title()"] + ":")

			# Display the "With media title" version of the media item title, in the user's language
			print("\t" + root_dictionary["Media"]["Item"]["With media title"][self.user_language])

	def Get_Language_Status(self, status):
		return_english = False

		if status in self.texts["statuses, type: list"][self.user_language]:
			return_english = True

		w = 0
		for english_status in self.texts["statuses, type: list"]["en"]:
			# Return the user language status
			if (
				return_english == False and
				english_status == status
			):
				status_to_return = self.texts["statuses, type: list"][self.user_language][w]

			# Return the English status
			if (
				return_english == True and
				status == self.texts["statuses, type: list"][self.user_language][w]
			):
				status_to_return = english_status

			w += 1

		return status_to_return

	def Change_Status(self, dictionary, status = ""):
		if status == "":
			status = self.Language.language_texts["completed, title()"]

		# Update the status key in the media details
		dictionary["Media"]["Details"][self.Language.language_texts["status, title()"]] = status

		# Update the media details file
		self.File.Edit(dictionary["Media"]["Folders"]["details"], self.Text.From_Dictionary(dictionary["Media"]["Details"]), "w")

		self.Check_Status(dictionary)

		return dictionary["Media"]["Details"]

	def Check_Status(self, dictionary):
		media_type = dictionary

		if "Media type" in dictionary:
			media_type = dictionary["Media type"]

			self.language_status = dictionary["Media"]["Details"][self.Language.language_texts["status, title()"]]

			# Get the English watching status from the language status of the media details
			status = self.Get_Language_Status(self.language_status)

		dictionary["JSON"] = self.JSON.To_Python(media_type["Folders"]["Media information"]["Information"])

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
					folder = media_type["Folders"]["Media information"]["root"] + self.Sanitize_Title(media_title) + "/"
					details_file = folder + self.Language.language_texts["details, title()"] + ".txt"
					details = self.File.Dictionary(details_file)

					self.language_status = details[self.Language.language_texts["status, title()"]]

					# Get the English watching status from the language status of the media details
					status = self.Get_Language_Status(self.language_status)

				# If the media status is equal to the watching status
				# And the media is not in the correct watching status list, add it to the list
				if (
					status == self.watching_status and
					media_title not in dictionary["JSON"]["Status"][self.watching_status]
				):
					dictionary["JSON"]["Status"][self.watching_status].append(media_title)

				# If the media status is not equal to the watching status
				# And the media is in the wrong watching status list, remove it from the list
				if (
					status != self.watching_status and
					media_title in dictionary["JSON"]["Status"][self.watching_status]
				):
					dictionary["JSON"]["Status"][self.watching_status].remove(media_title)

			# Sort media list
			dictionary["JSON"]["Status"][self.watching_status] = sorted(dictionary["JSON"]["Status"][self.watching_status], key = str.lower)

		# Update the media type "Information.json" file
		self.JSON.Edit(media_type["Folders"]["Media information"]["Information"], dictionary["JSON"])

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

	def Create_Playlist(self, dictionary):
		# To-Do: Make method
		# Creates a playlist of media units (episodes, videos) for the specified media
		print()

		media = dictionary["Media"]

		titles = media["Item"]["Episodes"]["Titles"]

		folder = media["Item"]["Folders"]["Media"]["root"]

		for title in titles:
			file_name = title

			for extension in self.dictionary["File extensions"]:
				file = folder + file_name + execution

	def Define_Title(self, title, language = None):
		if language == None:
			language = self.user_language

		keys = [
			"Original",
			language,
			"Romanized"
		]

		for title_key in keys:
			if title_key in title:
				key = title_key

		title = title[key]

		return title

	def Define_Year_Summary_Data(self, entry, language):
		import re

		# Get the entry Media
		item = self.Define_Title(entry["Media"], language)

		# Add the ": " separator if the entry is a video
		if entry["Type"] == "Videos":
			item += ": "

		# If the entry type is not "Videos"
		else:
			# Only add a space if there is an item or episode
			if (
				"Item" in entry or
				"Episode" in entry
			):
				item += " "

		# Add the item if it exists
		if "Item" in entry:
			item_title = self.Define_Title(entry["Item"], language)

			# Add the item title if it is not already present in the item text
			# And if the media type is not "Videos"
			if (
				item_title not in item and
				entry["Type"] != "Videos"
			):
				item_separator = ""
				episode_separator = " "

				# If the "S[Any number two times]" text is found on the item title
				if re.findall(r"S[0-9]{2}", item_title) != []:
					# Define the episode separator as empty
					episode_separator = ""

				# If the "S[Any number two times]" text is not found on the item title
				if re.findall(r"S[0-9]{2}", item_title) == []:
					# Define the item separator as a dash and space
					item_separator = "- "

				add = True

				# If the "Episode" key is present in the Entry dictionary
				if "Episode" in entry:
					# Get the episode title
					episode_title = self.Define_Title(entry["Episode"]["Titles"], language)

					# If the item title is inside the episode title
					if item_title in episode_title:
						# Then do not add the item title
						add = False

				# Add the item title if the "add" variable is True
				if add == True:
					# Add the item separator
					item += item_separator

					# Add the item title
					item += item_title

					# Only add the episode separator if there is an episode
					if "Episode" in entry:
						item += episode_separator

		# Add the episode if it exists
		if "Episode" in entry:
			# Add a space if the entry does not have a "Item" key
			# And if a space is not the last character in the item string
			if (
				"Item" not in entry and
				item[-1] != " "
			):
				item += " "

			episode_title = self.Define_Title(entry["Episode"]["Titles"], language)

			item += episode_title

		# Add the re-watched text if it exists
		if (
			"States" in entry and
			"Re-watched" in entry["States"]
		):
			text = " (" + self.texts["re_watched, capitalize()"][language] + " "

			text += str(entry["States"]["Re-watched"]["Times"]) + "x"

			text += ")"

			item += text

		# Add the entry date
		date = self.Date.From_String(entry["Date"])["Timezone"]["DateTime"]["Formats"]["HH:MM DD/MM/YYYY"]

		item += " (" + date + ")"

		return item

	def Show_Media_Information(self, dictionary):
		# Define a local version of the media dictionary for easier typing
		media = dictionary["Media"]

		# Define the singular media type variable for easier typing
		singular_media_type = dictionary["Media type"]["Singular"][self.user_language]

		# Define the header text
		header_text = singular_media_type + ":"

		# If the "Header text" key is inside the dictionary
		# And the key is not empty or None
		if (
			"Header text" in dictionary and
			"Header text" not in ["", None]
		):
			header_text = dictionary["Header text"]

		# Show a five dash space separator
		print()
		print(self.separators["5"])

		# Show the "Congratulations! :3" text in the user language if the user finished the media
		if (
			media["States"]["Re-watching"] == False and
			media["States"]["Completed media"] == True
		):
			print()
			print(self.Language.language_texts["congratulations"] + "! :3")

		# Show the header text
		print()
		print(header_text)

		# Show the title of the media
		self.Show_Media_Title(dictionary)

		# If the header text is not equal to the singular media type in the user language
		if header_text != singular_media_type + ":":
			# Show the plural media type in the user language
			print()
			print(self.language_texts["media_type"] + ":")
			print("\t" + dictionary["Media type"]["Plural"][self.user_language])

		# If the "Status change" key is inside the media dictionary
		if "Status change" in media:
			# Show the old status
			print()
			print(self.Language.language_texts["old_status"] + ":")
			print("\t" + media["Status change"]["Old"])

			# Show the new status
			print()
			print(self.Language.language_texts["new_status"] + ":")
			print("\t" + media["Status change"]["New"])

		# If the user is not re-watching the media
		# And the user completed the media
		if (
			media["States"]["Re-watching"] == False and
			media["States"]["Completed media"] == True
		):
			# Show the "New watching staus" text in the user language
			print()
			print(self.language_texts["new_watching_status"] + ":")
			
			# Show the new watching status in the user language
			print("\t" + media["Details"][self.Language.language_texts["status, title()"]])

			# If the "Finished watching text" key is inside the media dictionary
			# And the text is not empty
			if (
				"Finished watching text" in media and
				media["Finished watching text"] != ""
			):
				# Get the finished watching text for easier typing
				text = media["Finished watching text"]

				# Replace the ":\n" texts to add tabs
				text = text.replace(":\n", ":\n\t")

				# Show the finished watching text
				print()
				print(text)

		# Show the media episode title if the media is series media (not a movie)
		if media["States"]["Series media"] == True:
			# If the media item is not the media (not the same title as the media)
			if media["States"]["Media item is media"] == False:
				# Define the "of the" text as the "of the" text in the feminine gender
				dictionary["Media type"]["Genders"][self.user_language]["of_the"] = self.media_types["Genders"][self.user_language]["feminine"]["of_the"]

				# Show the "season"/"series" text
				print()
				print(self.Text.Capitalize(media["texts"]["item"][self.user_language]) + ":")

				# Show the title of the media
				self.Show_Media_Title(dictionary, is_media_item = True)

			# Define the unit text variable for easier typing
			unit_text = self.Text.Capitalize(media["texts"]["unit"][self.user_language])

			# If the media item is a single unit one
			if media["States"]["Single unit"] == True:
				# Define the unit text as the media item type text
				unit_text = media["Item"]["Type"][self.user_language]

			# Define the media episode text as the unit text plus the " {}" format text
			media_episode_text = unit_text + " {}"

			# Define the local "of the" text for easier typing
			of_the_text = dictionary["Media type"]["Genders"][self.user_language]["of_the"]

			# Define the list of "series types" texts
			series_types = [
				self.language_texts["season, title()"],
				self.language_texts["season, title()"].lower(),
				self.language_texts["serie, title()"],
				self.language_texts["serie, title()"].lower(),
				self.language_texts["video_serie"],
				self.language_texts["video_series"]
			]

			# If the media item is not a single unit one
			if media["States"]["Single unit"] == False:
				# If the media item type is inside that list
				if media["Item"]["Type"][self.user_language] in series_types:
					# If the media has no media item list
					# Or the media item is the media
					if (
						media["States"]["Media item list"] == False or
						media["States"]["Media item is media"] == True
					):
						# Define the "of the" text as the container "of the" text
						of_the_text = media["texts"]["container_text"]["of_the"]

					# If the media has a media item list
					# And the media item is not the media
					if (
						media["States"]["Media item list"] == True and
						media["States"]["Media item is media"] == False
					):
						# Define the text as the media item text in the user language
						text = media["texts"]["item"][self.user_language]

						# If the media is a video channel, make the text lowercase
						if media["States"]["Video"] == False:
							text = text.lower()

						# If the text with a space on the beginning is not inside the media episode text, add it
						if " " + text not in media_episode_text:
							media_episode_text += " " + text

				# If the media item type is not inside the list of series types
				if media["Item"]["Type"][self.user_language] not in series_types:
					# Define the "of the" text as the masculine "of the" text with the item type of the media item in the user language
					# 
					# Example:
					# "of the anime"
					of_the_text = self.media_types["Genders"][self.user_language]["masculine"]["of_the"] + " " + media["Item"]["Type"][self.user_language].lower()

			# If the media item is a single unit one
			if media["States"]["Single unit"] == True:
				# Define the "of the" text as the container "of the" text
				# 
				# Example:
				# "of the anime"
				of_the_text = media["texts"]["container_text"]["of_the"]

			# Format the media episode text with the defined "of the" text
			media_episode_text = media_episode_text.format(of_the_text)

			# Define the episode title as the episode title
			# (May or may not be in the user language)
			title = media["Episode"]["Title"]

			# If the language of the media is not the user language
			if media["Language"] != self.user_language:
				# Define the episode title as the episode title in the user language
				title = media["Episode"]["Titles"][self.user_language]

			# If the user is re-watching the media
			if media["States"]["Re-watching"] == True:
				# Add the re-watched text to the episode title
				title += media["Episode"]["Re-watched"]["Texts"]["Number"][self.user_language]

			# If the length of the title is greater than one
			# And the first two characters of the title are a space and a colon
			if (
				len(title) > 1 and
				title[0] + title[1] == ": "
			):
				# Remove them
				title = title[2:]

			# Show the media episode text and the epsiode title
			print()
			print(media_episode_text + ":")
			print("\t" + title)

			# Define the text template for the "with {[the container text]} title"
			template = self.Language.language_texts["with_{}_title"]

			# If the media is a video channel
			if media["States"]["Video"] == True:
				# Define the text template as "With {[the container text]}"
				template = self.Language.language_texts["with"] + " {}"

			# Define the default text to show
			text_to_show = ""

			# If the media item is not a single unit one
			if media["States"]["Single unit"] == False:
				# Add the unit text in the user language
				# 
				# Example:
				# Episode
				text_to_show += self.Text.Capitalize(media["texts"]["unit"][self.user_language])

			# If the media item is a single unit one
			else:
				# Add the item type of the media item in the user language
				# 
				# Example:
				# Special
				text_to_show += media["Item"]["Type"][self.user_language].lower()

			# Format the text template with the "the" container text of the media and add the text to show
			# 
			# Example:
			# Episode of the anime
			text_to_show = self.Text.Capitalize(text_to_show) + " " + template.format(media["texts"]["container_text"]["the"])

			# If the media has a media item list
			# And the media item is not the media
			# And the media is not a video channel
			# And the media item is not a single unit one
			# And the "Replace title" state is False
			if (
				media["States"]["Media item list"] == True and
				media["States"]["Media item is media"] == False and
				media["States"]["Video"] == False and
				self.language_texts["single_unit"] not in media["Item"]["Details"] and
				media["States"]["Replace title"] == False
			):
				# Define the media episode text as the media unit text with the "with_{}" formatted with the media item text
				media_episode_text = self.Text.Capitalize(media["texts"]["unit"][self.user_language]) + " " + self.Language.language_texts["with_{}"].format(media["texts"]["item"][self.user_language])

				# Show the media episode text with the media item text (item type)
				# 
				# Example:
				# "Episode with season:"
				print()
				print(media_episode_text + ":")

				# Define the media episode title with the media item text in the user language
				title = media["Episode"]["with_item"][self.user_language]

				# If the user is re-watching the media
				if media["States"]["Re-watching"] == True:
					# Add the re-watched text to the episode title
					title += media["Episode"]["Re-watched"]["Texts"]["Number"][self.user_language]

				# If the length of the title is greater than one
				# And the first two characters of the title are a space and a colon
				if (
					len(title) > 1 and
					title[0] + title[1] == ": "
				):
					# Remove them
					title = title[2:]

				# Show media episode title with the media item text in the user language
				print("\t" + title)

				# Add the " and [media item text]" to the text to show
				# 
				# Example:
				# "Episode with of the anime and season:"
				text_to_show += " " + self.Language.language_texts["and"] + " " + media["texts"]["item"][self.user_language]

				# Define the key as "with_title_and_item" to show the media title, media item title, and the episode title
				key = "with_title_and_item"

			# If the media has no media item list
			# Or the media item is the media
			# Or the media is a video channel
			# Or the media item is a single unit
			# Or the "Replace title" state is True
			if (
				media["States"]["Media item list"] == False or
				media["States"]["Media item is media"] == True or
				media["States"]["Video"] == True or
				self.language_texts["single_unit"] in media["Item"]["Details"] or
				media["States"]["Replace title"] == True
			):
				# Define the key as "with_title" to show only the media title and episode title
				key = "with_title"

			# Define the media episode title as the episode title with the correct key, in the user language
			title = media["Episode"][key][self.user_language]

			# If the user is re-watching the media
			if media["States"]["Re-watching"] == True:
				# Add the re-watched text to the episode title
				title += media["Episode"]["Re-watched"]["Texts"]["Number"][self.user_language]

			# If the length of the title is greater than one
			# And the first two characters of the title are a space and a colon
			if (
				len(title) > 1 and
				title[0] + title[1] == ": "
			):
				# Remove them
				title = title[2:]

			# If the "Replace title" state is False
			if media["States"]["Replace title"] == False:
				# Show the text to show and the defined title
				# 
				# Examples:
				# "Episode of the anime:"
				# "Episode of the anime and season:"
				print()
				print(text_to_show + ":")
				print("\t" + title)

		# If the "Entry" key is inside the dictionary
		# And the "Dates" key is inside the entry dictionary
		if (
			"Entry" in dictionary and
			"Dates" in dictionary["Entry"]
		):
			# Define the text as "When I finished watching [the unit]"
			# 
			# Example:
			# "When I finished watching the anime"
			text = self.language_texts["when_i_finished_watching"] + " " + media["texts"]["the_unit"][self.user_language]

			# Replaced the "watching" text with "re-watching"
			if media["States"]["Re-watching"] == True:
				text = text.replace(self.language_texts["watching, infinitive"], self.language_texts["re_watching, infinitive"] + " " + self.media["Episode"]["Re-watched"]["Texts"]["Times"][self.user_language])

			# Show the text with the entry date (watched date) in the user timezone
			print()
			print(text + ":")
			print("\t" + dictionary["Entry"]["Dates"]["Timezone"])

		# If the "Unit" key is inside the "Epsiode" dictionary
		if "unit" in media["Episode"]:
			# Show the media unit text and the episode unit
			print()
			print(self.language_texts["media_unit"] + ":")
			print("\t" + media["Episode"]["unit"])

		# If the user is not re-watching the media
		# And the user completed teh media item
		if (
			media["States"]["Re-watching"] == False and
			media["States"]["Completed media item"] == True
		):
			# Show a separator
			print()
			print("-")
			print()

			# Show the "Congratulations! :3" text
			print(self.Language.language_texts["congratulations"] + "! :3")
			print()

			# Define the text to show as:
			# 'You finished watching [this item] [media container the text] "[media title in the user language]"'
			# 
			# Example:
			# 'You finished watching this season of the anime "Sword Art Online"'
			text_to_show = self.language_texts["you_finished_watching"] + " " + media["texts"]["this_item"][self.user_language] + " " + media["texts"]["container_text"]["of_the"] + ' "' + media["Titles"]["Language"] + '"'

			# If the media has a media item list
			# And the media item is the media (same title as the root media)
			if (
				media["States"]["Media item list"] == True and
				media["States"]["Media item is media"] == True
			):
				# Define the text to show as:
				# "You finished watching [this container]"
				# 
				# Example:
				# "You finished watching this anime"
				text_to_show = self.language_texts["you_finished_watching"] + " " + media["texts"]["this_container"][self.user_language]

			# Show the text to show with a comma
			print(text_to_show + ":")

			# Show the media item title
			self.Show_Media_Title(dictionary, is_media_item = True)

			# If the media item is not a single unit
			# And the "Finished watching text" key is inside the media item dictionary
			# And the text is not empty
			if (
				media["States"]["Single unit"] == False and
				"Finished watching text" in media["Item"] and
				media["Item"]["Finished watching text"] != ""
			):
				# Get the finished watching text for easier typing
				text = media["Item"]["Finished watching text"]

				# Replace the ":\n" texts to add tabs
				text = text.replace(":\n", ":\n\t")

				# Show the finished watching text
				print()
				print(text)

			# If the user did not completed the media
			# And the media is not a video channel
			if (
				media["States"]["Completed media"] == False and
				media["States"]["Video"] == False
			):
				# Define the type of the next media item
				item_type = media["Item"]["Next"]["Type"][self.user_language]

				# Define the local text as the "Next {} to watch" text in the feminine version
				text = self.language_texts["next_{}_to_watch, feminine"]

				# Define the list of season and series item types
				series_types = [
					self.texts["season, title()"][self.user_language].lower(),
					self.texts["series"][self.user_language]
				]

				# If the item type is not inside that list, define the text as its masculine version
				if item_type not in series_types:
					text = self.language_texts["next_{}_to_watch, masculine"]

				# Show an empty line and the text
				print()
				print(text.format(item_type.lower()) + ":")

				# Define a dictionary with the next media item titles, states, and text
				dict_ = { 
					"Media": {
						"Item": {
							"Titles": media["Item"]["Next"]["Titles"]
						},
						"States": media["States"],
						"texts": media["texts"]
					}
				}

				# Show the next media item title
				self.Show_Media_Title(dict_, is_media_item = True)

		# If the "ID" key is inside the "Episode" dictionary
		if "ID" in media["Episode"]:
			# Show the "ID" text and the epsiode ID
			print()
			print(self.Language.language_texts["id, upper()"] + ":")
			print("\t" + media["Episode"]["ID"])

			# If the "Remote" key is inside the "Episode" dictionary
			if "Remote" in media["Episode"]:
				# If the "Title" key is inside the remote dictionary, show the title of the remote origin
				if "Title" in media["Episode"]["Remote"]:
					print()
					print(self.Language.language_texts["remote_origin"] + ":")
					print("\t" + media["Episode"]["Remote"]["Title"])

				# If the "Link" key is inside the remote dictionary, show it
				if "Link" in media["Episode"]["Remote"]:
					print()
					print(self.Language.language_texts["link, title()"] + ":")
					print("\t" + media["Episode"]["Remote"]["Link"])

		# If the "Next" key is inside the "Episode" dictionary
		if "Next" in media["Episode"]:
			# Define the local text as the "Next {media unit} to watch" text in the masculine gender
			text = self.language_texts["next_{}_to_watch, masculine"]

			# If the user is re-watching the media, replace the "watch" text with "re-watch"
			if media["States"]["Re-watching"] == True:
				text = text.replace(self.language_texts["watch"], self.language_texts["re_watch"])

			# Show the media unit text and the next episode to watch
			print()
			print(text.format(media["texts"]["unit"][self.user_language]) + ": ")
			print("\t" + media["Episode"]["Next"])

		# If the user finished watching the episode
		if media["States"]["Finished watching"] == True:
			# If there are states, show them
			if (
				"States" in self.dictionary and
				self.dictionary["States"]["States"] != {}
			):
				# Show the states text
				print()
				print(self.Language.language_texts["states, title()"] + ":")

				# Show the states
				for key in self.dictionary["States"]["Texts"]:
					print("\t" + self.dictionary["States"]["Texts"][key][self.user_language])

			# If this is the first media the user watches in the year
			if media["States"]["First entry in year"] == True:
				# Define the container text for easier typing
				container = media["texts"]["container"][self.user_language]

				# If the media is a video channel, make the container lowercase
				if media["States"]["Video"] == False:
					container = container.lower()

				# Define the list of items to use to format the text
				items = [
					self.media_types["Genders"][self.user_language]["feminine"]["this"].title(),
					self.media_types["Genders"][self.user_language]["feminine"]["the"] + " " + self.media_types["Genders"][self.user_language]["feminine"]["first"] + " " + self.Language.language_texts["media, title()"].lower()
				]

				# Add the "in" text in the masculine gender and the current year number
				items.append(self.Language.language_texts["genders, type: dict, masculine"]["in"] + " " + self.current_year["Number"])

				# Define the template
				template = self.language_texts["{}_is_{}_that_you_watched_{}"]

				# Format the template with the list of items
				text = template.format(*items)

				# Show the text telling the user that this is the first media they watched in the year
				# 
				# Example:
				# "This is the first media that you watched in 2024."
				print()
				print(text + ".")

			# If this is the first media type the user watches in the year (first anime, cartoon, series, movie, or video)
			if media["States"]["First media type entry in year"] == True:
				# Define the container text for easier typing
				container = media["texts"]["container"][self.user_language]

				# If the media is a video channel, make the container lowercase
				if media["States"]["Video"] == False:
					container = container.lower()

				# If the media is a series media
				if media["States"]["Series media"] == True:
					# Define the container text as the "[unit] of [container]"
					# 
					# Example:
					# "Episode of anime"
					container = media["texts"]["unit"][self.user_language] + " " + self.Language.language_texts["of, neutral"] + " " + container

				# If this is not the first media the user watches in the year
				if media["States"]["First entry in year"] == False:
					# If the media is a video channel, make the container lowercase
					if media["States"]["Video"] == False:
						container = container.lower()

					# Define a shortcut for the words dictionary
					words = dictionary["Media type"]["Genders"][self.user_language]

					# Define the list of items to use to format the text
					items = [
						words["this"].title(),
						words["the"] + " " + words["first"] + " " + container
					]

					# Re-define the words shortcut
					words = self.Language.language_texts["genders, type: dict, masculine"]

					# If the media unit is "episode"
					if media["texts"]["unit"]["en"] == "episode":
						# Re-define the list of items to be in the masculine gender
						items = [
							words["this"].title(),
							words["the"] + " " + words["first"] + " " + container
						]

					# Add the "in" text in the masculine gender and the current year number
					items.append(words["in"] + " " + self.current_year["Number"])

					# Define the template
					template = self.language_texts["{}_is_{}_that_you_watched_{}"]

					# Format the template with the list of items
					text = template.format(*items)

				# If this is not the first media the user watches in the year
				if media["States"]["First entry in year"] == True:
					# Define the text as "And also [the first container]"
					# 
					# Examples:
					# "And also the first anime"
					# "And also the first cartoon"
					text = self.Language.language_texts["and_also"].capitalize() + " " + dictionary["Media type"]["Genders"][self.user_language]["the"] + " " + dictionary["Media type"]["Genders"][self.user_language]["first"] + " " + container

				# Show the text telling the user that this is the first media type they watched in the year
				# 
				# Examples:
				# "This is the first anime that you watched in 2024."
				# "This is the first cartoon that you watched in 2025."
				print()
				print(text + ".")

		# If the "Statistics text" key is present
		if "Statistics text" in self.dictionary:
			# Show the statistics text
			print(self.dictionary["Statistics text"])
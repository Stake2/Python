# Watch History.py

# Import the "importlib" module
import importlib

# Import the "deepcopy" module from the "copy" module
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

		# Import some usage classes
		self.Import_Usage_Classes()

		# Folders, files, lists, and dictionaries methods
		self.Define_Folders_And_Files()
		self.Define_Lists_And_Dictionaries()

		# Define the media types dictionary
		self.Define_Media_Types()

		# Define the format of the registry
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
			if module_title not in remove_list:
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
		# Define the "Texts" dictionary
		self.texts = self.JSON.To_Python(self.module["Files"]["Texts"])

		# Define the "Language texts" dictionary
		self.language_texts = self.Language.Item(self.texts)

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

		# Iterate through the list of small languages
		for language in self.languages["Small"]:
			# Define a shortcut for the folder
			folder = self.current_year["Folders"][language]

			# Get the "Watched media" text in the current language to be the folder name
			folder_name = self.Language.texts["watched_media"][language]

			# Define the watched media folder
			folder["Watched media"] = {
				"root": folder["root"] + folder_name + "/"
			}

			# Create the folder
			self.Folder.Create(folder["Watched media"]["root"])

			# Update the folder shortcut
			folder = self.current_year["Folders"][language]["Firsts of the Year"]

			# Define the sub-folder name
			sub_folder_name = self.Language.texts["media, title()"][language]

			# Define the sub-folder dictionary
			folder["Media"] = {
				"root": folder["root"] + sub_folder_name + "/"
			}

			self.Folder.Create(folder["Media"]["root"])

		# ---------- #

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
			"By type": True,
			"Folder": self.Folder.folders["Notepad"]["Data Networks"]["Audiovisual Media"]["Watch History"]["root"]
		}

	def Define_Lists_And_Dictionaries(self):
		# Define the list of alternative episode types
		self.alternative_episode_types = [
			"OVA",
			"ONA",
			"Special",
			"Especial",
			"Shorts",
			"Curtas"
		]

		# Define the dictionary of remote origins
		self.remote_origins = {
			"Animes Vision": {
				"Link": "https://animes.vision/"
			},
			"YouTube": {
				"Link": "https://www.youtube.com/",
				"Link templates": {
					"Video": "https://www.youtube.com/watch?v={Video}",
					"Video and comment": "https://www.youtube.com/watch?v={Video}&lc={Comment}",
					"Video and playlist": "https://www.youtube.com/watch?v={Video}&list={Playlist}",
				}
			}
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

		# Define the secondary type texts by language
		for item_type in ["Singular", "Plural"]:
			for language in self.languages["Small"]:
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
		self.media_states = {
			"Remote": False,
			"Local": False,
			"Video": False,
			"Series media": True,
			"Episodic": False,
			"Single unit": False,
			"Replace title": False,
			"Has a list of media items": False,
			"The media item is the root media": False,
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

	def Define_Media_Types(self):
		# Get the media types dictionary from the "Types.json" file
		self.media_types = self.JSON.To_Python(self.folders["Data"]["Types"])

		# Add or update the "Genders" key to the media types dictionary
		self.media_types["Genders"] = self.Language.texts["genders, type: dictionary"]

		# ---------- #

		# Define a shortcut to the root "Information.json" file
		root_information_file = self.folders["Media information"]["Information"]

		# Read the file contents
		contents = self.File.Contents(root_information_file)

		# Define a default root information dictionary
		root_information = {
			"Media types": {
				"Numbers": {
					"Total": len(self.media_types["Plural"]["en"]),
				},
				"List": self.media_types["Plural"]["en"]
			},
			"Media numbers": {
				"Total": 0,
				"By media type": {}
			}
		}

		# ---------- #

		# Iterate through the English plural media types list
		media_type_number = 0
		for plural_media_type in self.media_types["Plural"]["en"]:
			# Get the language media type
			language_media_type = self.media_types["Plural"][self.language["Small"]][media_type_number]

			# Create the local media type dictionary
			media_type = {
				"Singular": {},
				"Plural": {},
				"Gender": "",
				"Genders": {},
				"Folders": {},
				"Subfolders": {},
				"Statuses": [
					self.texts["watching, title()"]["en"],
					self.texts["re_watching, title()"]["en"]
				],
				"Texts": {},
				"Medias": {
					"Numbers": {
						"Total": 0
					},
					"List": [],
					"List (with statuses)": []
				}
			}

			# ----- #

			# Define the singular and plural media types
			for language in self.languages["Small"]:
				for text_type in ["Singular", "Plural"]:
					media_type[text_type][language] = self.media_types[text_type][language][media_type_number]

			# ----- #

			# If the media type is "Videos"
			if plural_media_type == self.texts["videos, title()"]["en"]:
				# Update the select texts to be "Channel" and "Channels"
				media_type["Singular"]["select"] = self.Language.language_texts["channel, title()"]
				media_type["Plural"]["select"] = self.Language.language_texts["channels, title()"]

			# ----- #

			# Define the gender of the media type as masculine by default
			gender = "masculine"

			# For the "Series" media type, define it as feminine
			if plural_media_type == self.texts["series, title()"]["en"]:
				gender = "feminine"

			# Update the "Gender" key with the local defined gender
			media_type["Gender"] = gender

			# Define the "Genders" dictionary for each language
			for language in self.languages["Small"]:
				media_type["Genders"][language] = deepcopy(self.media_types["Genders"][language][gender])

			# ----- #

			# Define and create the media type folders
			for root_folder in ["Media information", "Watch History", "Media"]:
				media_type_key = plural_media_type.lower().replace(" ", "_")

				# Define and create the "Media information" folder
				if root_folder == "Media information":
					self.folders[root_folder][media_type_key] = {
						"root": self.folders[root_folder]["root"] + language_media_type + "/"
					}

					self.Folder.Create(self.folders[root_folder][media_type_key]["root"])

				# Define and create the Watch History "By media type" folder
				if root_folder == "Watch History":
					# Create a list of years from 2018 to the current year
					years_list = self.Date.Create_Years_List()

					# Iterate through the lst of years
					for year in years_list:
						# Create the "By media type" media type dictionary
						self.folders[root_folder][year]["By media type"][media_type_key] = {
							"root": self.folders[root_folder][year]["By media type"]["root"] + plural_media_type + "/"
						}

						# Create the root "By media type" media type folder
						self.Folder.Create(self.folders[root_folder][year]["By media type"][media_type_key]["root"])

						# Create the "Entries.json" file
						self.folders[root_folder][year]["By media type"][media_type_key]["Entries"] = self.folders[root_folder][year]["By media type"][media_type_key]["root"] + "Entries.json"
						self.File.Create(self.folders[root_folder][year]["By media type"][media_type_key]["Entries"])

						# Create the "Entry list.txt" file
						self.folders[root_folder][year]["By media type"][media_type_key]["Entry list"] = self.folders[root_folder][year]["By media type"][media_type_key]["root"] + "Entry list.txt"
						self.File.Create(self.folders[root_folder][year]["By media type"][media_type_key]["Entry list"])

						# Create the "Files" folder
						self.folders[root_folder][year]["By media type"][media_type_key]["Files"] = {
							"root": self.folders[root_folder][year]["By media type"][media_type_key]["root"] + "Files/"
						}

						self.Folder.Create(self.folders[root_folder][year]["By media type"][media_type_key]["Files"]["root"])

					# Define the "Current year" as the current year folder
					self.folders[root_folder]["Current year"] = self.folders[root_folder][str(self.date["Units"]["Year"])]

				# Define and create the local "Media" folder
				if root_folder == "Media":
					if root_folder not in self.folders:
						self.folders[root_folder] = {}

					self.folders[root_folder][media_type_key] = {
						"root": self.Folder.folders[root_folder]["root"] + language_media_type + "/"
					}

					self.Folder.Create(self.folders[root_folder][media_type_key]["root"])

			# Define the media type folders and files
			key = media_type["Plural"]["en"].lower().replace(" ", "_")

			media_type["Folders"] = {
				"Media information": self.folders["Media information"][key],
				"By media type": self.folders["Watch History"]["Current year"]["By media type"][key],
				"Media": self.folders["Media"][key]
			}

			# ----- #

			# Define the "Information.json" file
			media_type["Folders"]["Media information"]["Information"] = media_type["Folders"]["Media information"]["root"] + "Information.json"
			self.File.Create(media_type["Folders"]["Media information"]["Information"])

			# Define the media type sub-folders
			text = media_type["Singular"][self.language["Small"]]

			if plural_media_type != self.texts["movies, title()"]["en"]:
				text = "season"

			if plural_media_type == self.texts["videos, title()"]["en"]:
				text = "serie"

			for text_type in ["Singular", "Plural"]:
				if text_type == "Plural":
					text += "s"

				media_type["Subfolders"][text_type] = text.capitalize()

				if text + ", title()" in self.language_texts:
					media_type["Subfolders"][text_type] = self.language_texts[text + ", title()"]

			# Define current "season/series" folder
			text = media_type["Subfolders"]["Singular"]

			if "{" not in self.Language.language_texts["current_{}"][0]:
				text = text.lower()

			media_type["Subfolders"]["Current"] = self.Language.language_texts["current_{}"].format(text)

			# ----- #

			# Define a shortcut to the "Information.json" file
			media_type_information_file = media_type["Folders"]["Media information"]["Information"]

			# Get the contents of the file
			contents = self.File.Contents(media_type_information_file)

			# If the "Information.json" file is not empty, get the media type information dictionary from it
			if contents["Lines"] != []:
				media_type_information = self.JSON.To_Python(media_type_information_file)

			# If the "Information.json" file is empty
			if contents["Lines"] == []:
				# Define the default media type dictionary
				media_type_information = {
					"Numbers": {
						"Total": 0
					},
					"Media titles": [],
					"Statuses": {}
				}

				# Create an empty list for each English status
				for english_status in self.texts["statuses, type: list"]["en"]:
					media_type_information["Statuses"][english_status] = []

			# Sort the dictionary of statuses
			media_type_information["Statuses"] = self.Sort_Statuses(media_type_information["Statuses"])

			# Update the number of medias inside the media type dictionary with the number of medias in the "Media titles" list
			media_type_information["Numbers"]["Total"] = len(media_type_information["Media titles"])

			# Sort the list of media titles
			media_type_information["Media titles"] = sorted(media_type_information["Media titles"], key = str.lower)

			# Sort the list of media inside each watching status in the correct order
			for english_status in self.texts["statuses, type: list"]["en"]:
				media_type_information["Statuses"][english_status] = sorted(media_type_information["Statuses"][english_status], key = str.lower)

			# Edit the "Information.json" file with the updated media type information dictionary
			self.JSON.Edit(media_type_information_file, media_type_information)

			# Update the "JSON" key of the media type dictionary with the media type information dictionary
			media_type["JSON"] = media_type_information

			# ----- #

			# Add the media number of the current media type to the root "Media numbers" dictionary
			root_information["Media numbers"]["Total"] += media_type_information["Numbers"]["Total"]

			# Add the media number of the current media type to the root media numbers "By media type" dictionary
			root_information["Media numbers"]["By media type"][plural_media_type] = media_type_information["Numbers"]["Total"]

			# ----- #

			# Check the watching status of the list of media
			# Add the medias inside the correct watching status list if they are not there already
			# And remove the medias from the wrong watching status list if they are there
			media_type = self.Check_Status(media_type)

			# Get the list of media with the default list of watching statuses:
			# Plan to watch, watching, re-watching, and on hold
			media_type["Medias"]["List"] = self.Get_Media_List(media_type)

			# Update the number of medias
			media_type["Medias"]["Numbers"]["Total"] = len(media_type["Medias"]["List"])

			# Define the "add status" switch as True by default
			self.add_status = True

			# If the "add status" switch is True
			if self.add_status == True:
				# Call the method to add status to the list of media and update the dictionary
				media_type = self.Add_Status_To_Media_List(media_type)

			# ----- #

			# Get the number of medias
			media_number = str(len(media_type["Medias"]["List"]))

			# Update the singular and plural "Show" texts to update the number of medias
			for grammatical_number in ["Singular", "Plural"]:
				# Get the media type text for the current grammatical number and the user language
				text = media_type[grammatical_number][self.language["Small"]]

				# Add the media type text and the media number to update the "Show" text in the current grammatical number
				media_type[grammatical_number]["Show"] = text + " (" + media_number + ")"

			# ----- #

			# Update the media type "Show" text to be the singular or plural based on the number of medias
			# Parameters: number, singular text, plural text
			media_type["Texts"]["Show"] = self.Text.By_Number(media_type["Medias"]["List"], media_type["Singular"]["Show"], media_type["Plural"]["Show"])

			# If the media type is "Videos"
			if plural_media_type == self.texts["videos, title()"]["en"]:
				# Update the media type "Select" text to be:
				# "Select a YouTube channel to watch"
				media_type["Texts"]["Select"] = self.language_texts["select_{}_to_watch"].format(media_type["Genders"][self.language["Small"]]["a"] + " " + self.language_texts["youtube_channel"])

			# ----- #

			# Add the local media type dictionary to the root media types dictionary
			self.media_types[plural_media_type] = media_type

			# ----- #

			# Add one to the local media type number
			media_type_number += 1

		# Write the media types dictionary into the "Types.json" file
		self.JSON.Edit(self.folders["Data"]["Types"], self.media_types)

		# Update the root "Information.json" file with the updated root information dictionary
		self.JSON.Edit(self.folders["Media information"]["Information"], root_information)

		# ---------- #

		# These keys of the history dictionary are to be used on Python modules that collect history information of database-registering modules
		# Such as the "Years" module and its "Create_Year_Summary" sub-class

		# Add the media types dictionary to the history dictionary
		self.history["Types"] = self.media_types

		# Define the types folder
		self.history["Types folder"] = "By media type"

	def Sort_Statuses(self, statuses):
		# Define the list of statuses to use to sort the statuses
		order = [
			self.texts["plan_to_watch, title()"]["en"],
			self.texts["watching, title()"]["en"],
			self.texts["re_watching, title()"]["en"],
			self.Language.texts["on_hold, title()"]["en"],
			self.Language.texts["completed, title()"]["en"]
		]

		# Sort the statuses using the "Sort_Item_List" method of the "JSON" utility class
		statuses = self.JSON.Sort_Item_List(statuses, order)

		# Return the statuses
		return statuses

	def Define_Registry_Format(self):
		import collections

		# Define the default entries dictionary template
		self.template_dictionary = {
			"Numbers": {
				"Total": 0,
				"Comments": 0
			},
			"Entries": [],
			"Dictionary": {}
		}

		# Define the dictionary of dictionaries
		self.dictionaries = {
			"History": {
				"Numbers": {
					"Years": 0,
					"Entries": 0,
					"Comments": 0
				},
				"Years": []
			},
			"Entries": deepcopy(self.template_dictionary),
			"Media type": {},
			"Watched": deepcopy(self.template_dictionary),
			"Root comments": {
				"Numbers": {
					"Total": 0,
					"No time": 0,
					"Years": {},
					"Type": {}
				}
			},
			"Comments": {
				"Numbers": {
					"Total": 0
				},
				"Entries": [],
				"Dictionary": {}
			},
			"Comments (videos)": {
				"Numbers": {
					"Total": 0
				},
				"Channel": {},
				"Playlist": {},
				"Entries": [],
				"Dictionary": {}
			}
			
		}

		# If the file is not empty and the list of years is not empty
		if (
			self.File.Contents(self.folders["Watch History"]["History"])["lines"] != [] and
			self.JSON.To_Python(self.folders["Watch History"]["History"])["Years"] != []
		):
			# Get the "History" dictionary from the file
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
				self.File.Exists(entries_file) == True and
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

		# Create the "By media type" key inside the "Numbers" dictionary of the "Entries" dictionary
		self.dictionaries["Entries"]["Numbers"]["By media type"] = {}

		# If the "Entries.json" is not empty and has entries, get the entries dictionary from it
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

		# Sort the dictionary of year comment numbers based on its keys
		self.dictionaries["Root comments"]["Numbers"]["Years"] = dict(collections.OrderedDict(sorted(self.dictionaries["Root comments"]["Numbers"]["Years"].items())))

		# Update the current year comments number with the number from the comments dictionary
		self.dictionaries["Entries"]["Numbers"]["Comments"] = self.dictionaries["Root comments"]["Numbers"]["Years"][self.current_year["Number"]]

		# Iterate through the English media types list
		for plural_media_type in self.media_types["Plural"]["en"]:
			key = plural_media_type.lower().replace(" ", "_")

			# Define default media type dictionary
			self.dictionaries["Media type"][plural_media_type] = deepcopy(self.template_dictionary)

			# If the media type "Entries.json" is not empty, get the media type entries dictionary from it
			if (
				self.File.Contents(self.folders["Watch History"]["Current year"]["By media type"][key]["Entries"])["lines"] != [] and
				self.JSON.To_Python(self.folders["Watch History"]["Current year"]["By media type"][key]["Entries"])["Entries"] != []
			):
				self.dictionaries["Media type"][plural_media_type] = self.JSON.To_Python(self.folders["Watch History"]["Current year"]["By media type"][key]["Entries"])

			if self.current_year["Number"] not in self.dictionaries["Root comments"]["Numbers"]["Type"][plural_media_type]["Years"]:
				self.dictionaries["Root comments"]["Numbers"]["Type"][plural_media_type]["Years"][self.current_year["Number"]] = 0

			# Get media type comment number by year
			self.dictionaries["Media type"][plural_media_type]["Numbers"]["Comments"] = self.dictionaries["Root comments"]["Numbers"]["Type"][plural_media_type]["Years"][self.current_year["Number"]]

			self.JSON.Edit(self.folders["Watch History"]["Current year"]["By media type"][key]["Entries"], self.dictionaries["Media type"][plural_media_type])

			if plural_media_type not in self.dictionaries["Root comments"]["Numbers"]["Type"]:
				self.dictionaries["Root comments"]["Numbers"]["Type"][plural_media_type] = {
					"Total": 0,
					"Years": {}
				}

			# If the current year is not inside the media type year comment number dictionary, add it
			if self.current_year["Number"] not in self.dictionaries["Root comments"]["Numbers"]["Type"][plural_media_type]["Years"]:
				self.dictionaries["Root comments"]["Numbers"]["Type"][plural_media_type]["Years"][self.date["Units"]["Year"]] = 0

			# Sort the dictionary of comment numbers by media type and by year based on its keys
			self.dictionaries["Root comments"]["Numbers"]["Type"][plural_media_type]["Years"] = dict(collections.OrderedDict(sorted(self.dictionaries["Root comments"]["Numbers"]["Type"][plural_media_type]["Years"].items())))

			# Add the plural media type number to the root numbers by media type if it does not exist in there
			if plural_media_type not in self.dictionaries["Entries"]["Numbers"]["By media type"]:
				self.dictionaries["Entries"]["Numbers"]["By media type"][plural_media_type] = 0

			# Else, define the root total number by media type as the number inside the entries dictionary by media type
			if plural_media_type in self.dictionaries["Entries"]["Numbers"]["By media type"]:
				self.dictionaries["Entries"]["Numbers"]["By media type"][plural_media_type] = self.dictionaries["Media type"][plural_media_type]["Numbers"]["Total"]

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
			"Media types": [],
			"List": [],
			"Years": {}
		}

		# Create a root dictionary of media
		self.media = {
			"List": [],
			"Dictionary": {}
		}

		# ---------- #

		# Create the "statistic media types" dictionary
		media_types = self.Create_Statistic_Media_Types_Dictionary()

		# Add the list of media types to the "Media types" key
		statistics["Media types"] = media_types["Lists"]

		# ---------- #

		# Fill the "Years" dictionary

		# Iterate through the list of years from 2020 to the current year
		for year_number in years_list:
			# Create the year dictionary
			year = {
				"Key": year_number,
				"Total": 0,
				"Numbers": deepcopy(media_types),
				"Months": {}
			}

			# Get the year folder
			year_folder = self.folders["Watch History"]["root"] + year_number + "/"

			# Get the by media type folder
			by_media_type_folder = year_folder + "By Media Type/"

			# Iterate through the English plural media types list
			for plural_media_type in self.media_types["Plural"]["en"]:
				# Get the media type folder
				media_type_folder = by_media_type_folder + plural_media_type + "/"

				# Get the entries file
				entries_file = media_type_folder + "Entries.json"

				# Read the "Entries.json" file, getting the "Entries" dictionary and adding it into the year dictionary
				year["Entries"] = self.JSON.To_Python(entries_file)

				# Iterate through the dictionary of entries, updating the "Numbers" dictionary of the year dictionary
				year = self.Iterate_Through_Entries(year, plural_media_type)

				# ---------- #

				# Correct the translation dictionary of the year dictionary
				year = self.Correct_Translation_Dictionary(year)

				# ---------- #

				# Fill the "Months" dictionary
				for month in range(1, 13):
					# Add leading zeroes to the month number
					month_number = str(self.Text.Add_Leading_Zeroes(month))

					# Create the month dictionary
					month = {
						"Key": month_number,
						"Year": year_number,
						"Total": 0,
						"Numbers": deepcopy(media_types),
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
								month = self.Define_Media_Dictionary(month, plural_media_type, entry)[0]

								# Correct the translation dictionary of the month dictionary
								month = self.Correct_Translation_Dictionary(month)

								# Add one to the month total entries number
								month["Total"] += 1

							# Define the "has month" switch as True
							has_month = True

					# If the "has month" switch is True
					if has_month == True:
						# Add the month dictionary to the "Months" dictionary of the year dictionary
						year["Months"][month_number] = month

				# Iterate through the media inside the "Numbers" dictionary
				for media_title, media in deepcopy(year["Numbers"]["Dictionary"][plural_media_type]["Dictionary"]).items():
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
							year["Numbers"]["Dictionary"][plural_media_type]["Dictionary"] = self.Add_To_Index(year["Numbers"]["Dictionary"][plural_media_type]["Dictionary"], media_title, title, media["Total"])

				# Iterate through the list of months from 1 to 12
				for month in range(1, 13):
					# Add leading zeroes to the month number
					month_number = str(self.Text.Add_Leading_Zeroes(month))

					# If the month number is already inside the "Months" dictionary
					if month_number in year["Months"]:
						# Get the month dictionary from it
						month = year["Months"][month_number]

						# Iterate through the media inside the "Numbers" dictionary
						for media_title, media in deepcopy(month["Numbers"]["Dictionary"][plural_media_type]["Dictionary"]).items():
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
									month["Numbers"]["Dictionary"][plural_media_type]["Dictionary"] = self.Add_To_Index(month["Numbers"]["Dictionary"][plural_media_type]["Dictionary"], media_title, title, media["Total"])

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

	def Create_Statistic_Media_Types_Dictionary(self):
		# Create a dictionary of media types with the list and dictionary
		# (And also define the statistics as "By type")
		media_types = {
			"Lists": self.media_types["Plural"],
			"Dictionary": {},
			"Translation dictionary": {},
			"Per type statistic": True
		}

		# Iterate through the English plural media types list
		for plural_media_type in self.media_types["Plural"]["en"]:
			# Create the media type dictionary
			media_type = {
				"Total": 0,
				"Dictionary": {}
			}

			# Add it to the media types dictionary
			media_types["Dictionary"][plural_media_type] = media_type

		# Define the statistic media types dictionary as a variable in the root class
		self.statistic_media_types = media_types

		# Return the dictionary
		return self.statistic_media_types

	def Correct_Translation_Dictionary(self, dictionary):
		# Define the translation dictionary as the "dictionary" parameter
		translation_dictionary = dictionary

		# If the "Numbers" key exists inside that parameter
		if "Numbers" in dictionary:
			# Define the translation dictionary as the "Translation dictionary" key inside the "Numbers" dictionary
			translation_dictionary = dictionary["Numbers"]["Translation dictionary"]

		# Get the list of media keys
		media_keys = list(translation_dictionary.keys())

		# Iterate through the media types inside the translation dictionary
		for media_title in media_keys:
			# Get the media dictionary
			media_dictionary = translation_dictionary[media_title]

			# Get the keys of the dictionary
			keys = list(media_dictionary.keys())

			# If the media title key is present inside the media dictionary
			if media_title in media_dictionary:
				# Get the root media keys
				root_media_keys = list(media_dictionary[media_title].keys())

				# Define the "remove dictionary" switch as True initially
				remove_dictionary = True

				# If the keys are just the media title
				# And its only key is not the original one
				if (
					len(keys) == 1 and
					root_media_keys != ["Original"]
				):
					# Define the "remove dictionary" switch as False
					remove_dictionary = False

				# If the keys are not just the media title
				if len(keys) > 1:
					# Iterate through the list of media items
					for media_item in keys:
						# List the keys of the media item dictionary
						item_keys = list(media_dictionary[media_item].keys())

						# If the item does not contain only the original key
						if item_keys != ["Original"]:
							# Define the "remove dictionary" switch as False
							remove_dictionary = False

						# If the item contains only the original key
						if item_keys == ["Original"]:
							# Remove the media title key
							media_dictionary.pop(media_item)

				# If all media items only contain the original key, then remove the media dictionary
				if remove_dictionary == True:
					translation_dictionary.pop(media_title)

		# Iterate through the media types inside the translation dictionary
		for media_title in media_keys:
			# If the media title key is present inside the translation dictionary
			if media_title in translation_dictionary:
				# Get the media dictionary
				media_dictionary = translation_dictionary[media_title]

				# Get the keys of the dictionary
				keys = list(media_dictionary.keys())

				# If the only key present inside the list above is the media title
				if keys == [media_title]:
					# Get the root media keys
					root_media_keys = list(media_dictionary[media_title].keys())

					# If the media title dictionary does not only contain the original key
					if root_media_keys != ["Original"]:
						# Replace the root media dictionary by its respective inner dictionary
						translation_dictionary[media_title] = media_dictionary[media_title]

						# Get the local media dictionary variable again
						media_dictionary = translation_dictionary[media_title]

		# Return the date dictionary
		return dictionary

	def Define_Media_Dictionary(self, dictionary, media_type, entry):
		# Define the key to get the media title
		key = "Original"

		if "Romanized" in entry["Media"]:
			key = "Romanized"

		# Get the media title
		media_title = entry["Media"][key]

		# Add the media title to the root media dictionary
		if media_title not in self.media["List"]:
			self.media["List"].append(media_title)

		# Get the media type dictionary
		media_type_dictionary = dictionary["Numbers"]["Dictionary"][media_type]

		# ---------- #

		# Add the media title to the "Translation dictionary" key
		if media_title not in dictionary["Numbers"]["Translation dictionary"]:
			# Create a local titles dictionary
			titles = {
				"Original": media_title
			}

			# Iterate through the list of small languages
			for language in self.languages["Small"]:
				# Add the current language media title if it exists
				if language in entry["Media"]:
					titles[language] = entry["Media"][language]

			# Add the language media title if it exists
			if "Language" in entry["Media"]:
				titles["Language"] = entry["Media"]["Language"]

			# Create the media translation dictionary with the local titles dictionary
			dictionary["Numbers"]["Translation dictionary"][media_title] = {
				media_title: titles
			}

		# ---------- #

		# If there is a media item inside the entry dictionary
		if "Item" in entry:
			# If the media title is not inside the "Numbers" dictionary
			if media_title not in media_type_dictionary["Dictionary"]:
				# Define the root media dictionary inside the media type dictionary
				media_type_dictionary["Dictionary"][media_title] = {
					"Total": 0,
					"Dictionary": {}
				}

			# Else, if the media title key inside the "Numbers" dictionary is a number
			elif isinstance(media_type_dictionary["Dictionary"][media_title], int):
				# Get the original number of times watched
				watched_number = media_type_dictionary["Dictionary"][media_title]

				# Define the root media dictionary
				media_type_dictionary["Dictionary"][media_title] = {
					"Total": watched_number,
					"Dictionary": {
						media_title: watched_number
					}
				}

			# Update the media variable
			media = media_type_dictionary["Dictionary"][media_title]

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

			# ---------- #

			# Create a local titles dictionary for the media item
			titles = {
				"Original": media_item_title
			}

			# Iterate through the list of small languages
			for language in self.languages["Small"]:
				# Add the current language media title if it exists
				if language in entry["Item"]:
					titles[language] = entry["Item"][language]

			# Add the language media title if it exists
			if "Language" in entry["Item"]:
				titles["Language"] = entry["Item"]["Language"]

			# If the media item dictionary is not already present
			if media_item_title not in dictionary["Numbers"]["Translation dictionary"][media_title]:
				# Create the media item translation dictionary with the local titles dictionary
				dictionary["Numbers"]["Translation dictionary"][media_title][media_item_title] = titles

			# ---------- #

			# Add the media item key to the media dictionary if it is not already present
			if media_item_title not in media["Dictionary"]:
				media["Dictionary"][media_item_title] = 0

			# Add one to the number of times the media item was played
			media["Dictionary"][media_item_title] += 1

		# Define the media inside the "Numbers" dictionary as zero if it is not there already
		if media_title not in media_type_dictionary["Dictionary"]:
			media_type_dictionary["Dictionary"][media_title] = 0

		# Define a shortcut for the media variable
		media = media_type_dictionary["Dictionary"][media_title]

		# If the media variable is an integer
		if isinstance(media, int):
			# Add one to the number of times the media was watched
			media_type_dictionary["Dictionary"][media_title] += 1

		else:
			# Add one to the number of times the media was watched in the "Total" key
			media["Total"] += 1

		# Add one to the number of times the media type was watched
		media_type_dictionary["Total"] += 1

		# ---------- #

		# Return the dictionary and the media title inside a tuple
		return dictionary, media_title

	def Iterate_Through_Entries(self, dictionary, media_type):
		# Iterate through the entries dictionary
		for entry in dictionary["Entries"]["Dictionary"].values():
			# Define the media dictionary (media or media item), and add the media watched numbers
			dictionary, media_title = self.Define_Media_Dictionary(dictionary, media_type, entry)

			# Add one to the total number of media watched in the year or month
			dictionary["Total"] += 1

		return dictionary

	def Add_To_Index(self, dictionary, original_key, new_key, new_value):
		# List the keys of the dictionary
		keys = list(dictionary.keys())

		# Checks if the original key exists inside the dictionary
		if original_key not in keys:
			# Returns the original dictionary if not
			return dictionary

		# Get the index of the original key
		index = keys.index(original_key)

		# Define a new local dictionary
		new_dictionary = {}

		# Iterate through the indexes and keys of the list of keys
		for i, key in enumerate(keys):
			# If the "i" variable is the index we are looking for
			if i == index:
				# Replace the original key with the new key
				new_dictionary[new_key] = new_value

			else:
				# Add the original key that existed before
				new_dictionary[key] = dictionary[key]

		# Return the new dictionary
		return new_dictionary

	def Update_Statistics(self, root_dictionary, media, media_type):
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
			"External statistic": True,
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

		# Define the key to get the media title
		title_key = "Original"

		if "Romanized" in media["Titles"]:
			title_key = "Romanized"

		# Define a shortcut for the media title
		media_title = media["Titles"][title_key]

		# ---------- #

		# Get the current month statistics dictionary
		current_month_statistics = self.diary_slim["Current year"]["Month"]["Statistics"]

		# If statistics dictionary is empty
		if current_month_statistics == {}:
			# Run the "Diary_Slim" class again so it can define the statistics of the current month
			self.Diary_Slim = Diary_Slim()

			# Get the "diary_slim" dictionary from the class above
			self.diary_slim = self.Diary_Slim.diary_slim

		# ---------- #

		# Create the "statistic media types" dictionary
		self.Create_Statistic_Media_Types_Dictionary()

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

			# Add one to the total number of statistics
			statistics[key]["Total"] += 1

			# If the "Dictionary" key is not inside the "Watched Media" dictionary
			if "Dictionary" not in statistics[key]["Dictionary"]:
				# Define the key as a copy of the "statistic media types" default dictionary
				statistics[key]["Dictionary"] = deepcopy(self.statistic_media_types)
				

			# Get the media type dictionary
			media_type_dictionary = statistics[key]["Dictionary"]["Dictionary"][media_type["Plural"]]

			# Add one to the total number of the media type
			media_type_dictionary["Total"] += 1

			# ---------- #

			# If the media title is not inside the translation dictionary
			if media_title not in statistics[key]["Dictionary"]["Translation dictionary"]:
				# Get the media titles
				titles = root_dictionary["Media"]["Titles"]

				# Define the key to get the media title
				title_key = "Original"

				if "Romanized" in titles:
					title_key = "Romanized"

				# Create a local titles dictionary for the media
				titles = {
					"Original": titles[title_key]
				}

				# Iterate through the list of small languages
				for language in self.languages["Small"]:
					# Add the current language media title if it exists
					if language in titles:
						titles[language] = titles[language]

				# Add the language media title if it exists
				if "Language" in titles:
					titles["Language"] = titles["Language"]

				# Iterate through them
				for title_key, title in titles.items():
					# If the length of the title is greater than one
					# And the first two characters of the title are a space and a colon
					if (
						len(title) > 1 and
						title[0] + title[1] == ": "
					):
						# Remove them
						title = title[2:]

					# Update the root tile key
					titles[title_key] = title

				# Add the media title key to the translation dictionary
				statistics[key]["Dictionary"]["Translation dictionary"][media_title] = {
					media_title: titles
				}

			# Get the media dictionary
			media_dictionary = statistics[key]["Dictionary"]["Translation dictionary"][media_title]

			# ---------- #

			# If the "Item" key is inside the media titles dictionary
			if "Item" in media["Titles"]:
				# Define the key to get the media and media item titles
				title_key = "Original"
				item_key = "Original"

				# Define the keys as the "Romanized" key if it exists
				if "Romanized" in media["Titles"]:
					title_key = "Romanized"

				if "Romanized" in media["Titles"]["Item"]:
					item_key = "Romanized"

			# ---------- #

			# If the "Item" key is inside the media titles dictionary
			# And the media item title is not the same as the media title
			if (
				"Item" in media["Titles"] and
				media["Titles"]["Item"][item_key] != media["Titles"][title_key]
			):
				# Get the item title
				item_title = media["Titles"]["Item"]["Original (no media title)"]

				# Get the item dictionary from it
				item = media["Items"]["Dictionary"][item_title]

				# If the media item title key does not exist inside the media translation dictionary
				if item_title not in media_dictionary:
					# Get the media item titles
					item_titles = item["Titles"]

					# Define the key to get the media title
					local_title_key = "Original"

					if "Romanized" in titles:
						local_title_key = "Romanized"

					# Create a local titles dictionary for the media item
					titles = {
						"Original": item_titles[local_title_key]
					}

					# Iterate through the list of small languages
					for language in self.languages["Small"]:
						# Add the current language media title if it exists
						if language in item_titles:
							titles[language] = item_titles[language]

					# Add the language media title if it exists
					# And it is not already present in the local titles dictionary
					if (
						"Language" in item_titles and
						item_titles["Language"] not in list(titles.values())
					):
						titles["Language"] = item_titles["Language"]

					# Iterate through them
					for local_title_key, title in titles.items():
						# If the length of the title is greater than one
						# And the first two characters of the title are a space and a colon
						if (
							len(title) > 1 and
							title[0] + title[1] == ": "
						):
							# Remove them
							title = title[2:]

						# Update the root tile key
						titles[local_title_key] = title

					# Add the media item key to the translation dictionary
					media_dictionary[item_title] = titles

			# Correct the translation dictionary
			statistics[key]["Dictionary"]["Translation dictionary"] = self.Correct_Translation_Dictionary(statistics[key]["Dictionary"]["Translation dictionary"])

			# ---------- #

			# If the "Items" key does not exist in the local media dictionary
			# Or the "Items" key exists in the local media dictionary
			# And the "Item" key is inside the media titles dictionary
			# And the media item title is the same as the media title
			if (
				"Items" not in media or
				"Items" in media and
				"Item" in media["Titles"] and
				media["Titles"]["Item"][item_key] == media["Titles"][title_key]
			):
				# If the media title is not inside the dictionary of medias of the media type
				if media_title not in media_type_dictionary["Dictionary"]:
					# Define the media statistic key as zero
					media_type_dictionary["Dictionary"][media_title] = 0

			# ---------- #

			# Define the "media item found in dictionary" switch as False
			media_item_found_in_dictionary = False

			# If the "Items" key exists in the local media dictionary
			if "Items" in media:
				# Make a list of media items to iterate through
				media_items = media["Items"]["List"]

				# Iterate through the list of items
				for item_title in media_items:
					# If the media item title key exists inside the items dictionary
					if item_title in media["Items"]["Dictionary"]:
						# Get the item dictionary from it
						item = media["Items"]["Dictionary"][item_title]

						# Define the key to get the number of times the media item was watched
						media_item_title = item["With media title"]["Original"]

						# If the media item title with the media title is inside the media type statistics dictionary
						# And the current media item title is the same as the title of the watched media item
						if (
							media_item_title in media_type_dictionary["Dictionary"] and
							item_title == media["Titles"]["Item"]["Original (no media title)"]
						):
							# Define the "media item found in dictionary" switch as True
							media_item_found_in_dictionary = True

			# ---------- #

			# Define the default media title key
			media_title_key = media_title

			# If the "Items" key exists in the local media dictionary
			# And the media item was found inside the statistics dictionary
			if (
				"Items" in media and
				media_item_found_in_dictionary == True
			):
				# Define the media title key as the media item title
				media_title_key = media["Titles"]["Item"][item_key]

			# ---------- #

			# If the "Items" key exists in the local media dictionary
			# And the "Item" key is inside the media titles dictionary
			# And the media item title is not the same as the media title
			# And the media item was not found inside the statistics dictionary
			if (
				"Items" in media and
				"Item" in media["Titles"] and
				media["Titles"]["Item"][item_key] != media["Titles"][title_key] and
				media_item_found_in_dictionary == False
			):
				# If the media title is inside the statistics dictionary of the module
				if media_title in media_type_dictionary["Dictionary"]:
					# If the media title key is a number
					if isinstance(media_type_dictionary["Dictionary"][media_title], int):
						# Create the media statistics dictionary
						media_type_dictionary["Dictionary"][media_title] = {
							"Total": media_type_dictionary["Dictionary"][media_title],
							"Dictionary": {}
						}

					# Add one to the total number of times the root media was watched
					media_type_dictionary["Dictionary"][media_title]["Total"] += 1

					# Make a list of media items to iterate through
					media_items = media["Items"]["List"]

					# Iterate through the list of items
					for local_item_title in media_items:
						# Define a local number a zero
						number = 0

						# If the item title is the media title
						# And the total number of watched times is not zero
						if (
							local_item_title == media_title and
							media_type_dictionary["Dictionary"][media_title]["Total"] != 0
						):
							# Define the local number as the total number of watched times
							number = media_type_dictionary["Dictionary"][media_title]["Total"]

						# If the length of the title is greater than one
						# And the first two characters of the title are a space and a colon
						if (
							len(local_item_title) > 1 and
							local_item_title[0] + local_item_title[1] == ": "
						):
							# Remove them
							local_item_title = local_item_title[2:]

						# Add the item title to the dictionary with the correct number (zero or the number of times the user watched the root media)
						media_type_dictionary["Dictionary"][media_title]["Dictionary"][local_item_title] = number

						# Define the default title as the media title
						title = media["Titles"]["Original"]

						# If the "Item" key is inside the media titles dictionary
						if "Item" in media["Titles"]:
							# Define the title as the media item title
							title = media["Titles"]["Item"]["Original (no media title)"]

						# If the item title is not the media title
						# And the current media item is the media item that was watched
						if (
							local_item_title != media_title and
							local_item_title == title
						):
							# Add one to the number of times the media item was watched
							media_type_dictionary["Dictionary"][media_title]["Dictionary"][local_item_title] += 1

				# If the media title is not inside the statistics dictionary of the module
				if media_title not in media_type_dictionary["Dictionary"]:
					# Make a list of media items to iterate through
					media_items = media["Items"]["List"]

					# Make a copy of the statistics dictionary
					statistics_copy = deepcopy(media_type_dictionary["Dictionary"])

					# Define the new key
					new_key = media_title

					# Iterate through the list of items
					for item_title in media_items:
						# Define the default media item title as the item title
						media_item_title = item_title

						# If the media item title key exists inside the items dictionary
						if item_title in media["Items"]["Dictionary"]:
							# Get the item dictionary from it
							item = media["Items"]["Dictionary"][item_title]

							# Define the key to get the media item title
							item_key = "Original"

							if "Romanized" in item["With media title"]:
								item_key = "Romanized"

							# Define the key to get the number of times the media item was watched
							media_item_title = item["With media title"][item_key]

						# Define a local number as zero
						number = 0

						# If the media item title (with the media title) is inside the copy of the statistics dictionary
						if media_item_title in statistics_copy:
							# Define the local number as the total number times the media item was watched
							number = statistics_copy[media_item_title]

						# Define the default title as the media title
						title = media["Titles"]["Original"]

						# If the "Item" key is inside the media titles dictionary
						if "Item" in media["Titles"]:
							# Define the title as the media item title
							title = media["Titles"]["Item"]["Original (no media title)"]

						# If the media title is not inside the statistics dictionary of the module
						if media_title not in media_type_dictionary["Dictionary"]:
							# Define the new value dictionary as the media statistics dictionary
							new_value = {
								"Total": number,
								"Dictionary": {}
							}

							# If the item title is the media title
							if item_title == media_title:
								# Add the media title to the media dictionary
								new_value["Dictionary"][item_title] = 0

							# Define the "has previous key" switch as False
							has_previous_key = False

							# Define the default original key as None
							original_key = None

							# Define the new key
							new_key = media_title

							# Iterate through the list of item titles
							for local_item in media["Items"]["Dictionary"].values():
								# Define the key to get the media item title
								item_key = "Original"

								if "Romanized" in local_item["With media title"]:
									item_key = "Romanized"

								# Define local media item title
								local_media_item_title = local_item["With media title"][item_key]

								# If the media item title (with the media title) is inside the statistics dictionary
								if local_media_item_title in media_type_dictionary["Dictionary"]:
									# Define the original key as the media item title
									original_key = local_media_item_title

									# Set the "has previous key" switch to True
									has_previous_key = True

							# If the "has previous key" switch is False
							# And the item title is not the media title
							# And the current media item is the root media or media item that was watched
							if (
								has_previous_key == False and
								item_title != media_title and
								item_title == title
							):
								# Define the new value as zero
								new_value = 0

								# Define the new key as the media item title
								new_key = media_item_title

								# Define the media title key as the media item title
								media_title_key = media_item_title

							# If the original key is not None (it was found)
							if (
								original_key != None and
								item_title == title
							):
								# Replaces the media item key with the root media key using the previous index
								media_type_dictionary["Dictionary"] = self.Add_To_Index(
									media_type_dictionary["Dictionary"], # The dictionary of statistics
									original_key, # The original media item title key
									new_key, # The new key that is the root media title
									new_value # The new value to replace the media item dictionary
								)

							# If the original key is None (it was not found)
							if (
								original_key == None and
								item_title == title
							):
								# Adds the the media dictionary to the end of the statistics dictionary
								media_type_dictionary["Dictionary"][new_key] = new_value

						# If the first two characters of the item title is a colon and a space
						# (Remove the colon and space from the item title so the media item title is more beautiful inside the dictionary)
						if item_title[0] + item_title[1] == ": ":
							# Remove the colon and space
							item_title = item_title[2:]

						# If the media key is not a number
						# And the "Dictionary" key is inside the media dictionary
						if (
							new_key in media_type_dictionary["Dictionary"] and
							isinstance(media_type_dictionary["Dictionary"][new_key], int) == False and
							"Dictionary" in media_type_dictionary["Dictionary"][new_key]
						):
							# Add the item title to the dictionary with the correct number (zero or the number of times the user watched the root media)
							media_type_dictionary["Dictionary"][new_key]["Dictionary"][item_title] = number

							# If the current media item is the root media or media item that was watched
							if item_title == title:
								# Add one to the number of times the media item was watched
								media_type_dictionary["Dictionary"][new_key]["Dictionary"][item_title] += 1

						# If the media item title is not the same as the media title
						# And the old media item title (with the media title) key is present inside the root media statistics dictionary
						if (
							item_title != media_title and
							media_item_title in statistics[key]["Dictionary"] and
							item_title != title
						):
							# Remove the key
							media_type_dictionary["Dictionary"].pop(media_item_title)

					# If the media key is not a number
					# And the "Dictionary" key is inside the media dictionary
					if (
						new_key in media_type_dictionary["Dictionary"] and
						isinstance(media_type_dictionary["Dictionary"][new_key], int) == False and
						"Dictionary" in media_type_dictionary["Dictionary"][new_key]
					):
						# Reset the total number to be zero
						media_type_dictionary["Dictionary"][new_key]["Total"] = 0

						# Iterate through the keys inside the root media dictionary
						for media_number in media_type_dictionary["Dictionary"][new_key]["Dictionary"].values():
							# Add the media number to the total number of times the root media was played
							media_type_dictionary["Dictionary"][new_key]["Total"] += media_number

			# ---------- #

			# Define the old number as the current number
			statistics["Dictionary"]["Numbers"][key]["Old"] = media_type_dictionary["Dictionary"][media_title_key]

			# If the old key is a dictionary
			if isinstance(statistics["Dictionary"]["Numbers"][key]["Old"], dict):
				# Get the number of the "Total" key
				statistics["Dictionary"]["Numbers"][key]["Old"] = statistics["Dictionary"]["Numbers"][key]["Old"]["Total"]

				# If the "Items" key does exist in the local media dictionary
				# And the "Item" key is inside the media titles dictionary
				# And the media item title is not the same as the media title
				if (
					"Items" in media and
					"Item" in media["Titles"] and
					media["Titles"]["Item"]["Original"] != media_title
				):
					input()
					# Define the title as the media item title
					title = media["Titles"]["Item"]["Original (no media title)"]

					# If the media key is not a number
					# And the "Dictionary" key is inside the media dictionary
					if (
						isinstance(media_type_dictionary["Dictionary"][media_title], int) == False and
						"Dictionary" in media_type_dictionary["Dictionary"][media_title]
					):
						# Remove one from the number of times the media item was watched
						statistics["Dictionary"]["Numbers"][key]["Old"] = media_type_dictionary["Dictionary"][media_title]["Dictionary"][title] - 1

					# If the media title key is a number
					if isinstance(media_type_dictionary["Dictionary"][media_title], int) == True:
						# Define the title as the media item title
						title = media["Titles"]["Item"]["Original"]
						print(title)

						# Remove one from the number of times the media item was watched
						statistics["Dictionary"]["Numbers"][key]["Old"] = media_type_dictionary["Dictionary"][title] - 1

			# ---------- #

			# If the media title key is a number
			if isinstance(media_type_dictionary["Dictionary"][media_title_key], int):
				# Update the number of times the media was watched
				media_type_dictionary["Dictionary"][media_title_key] += 1

			# ---------- #

			# Define the new number as the old number
			statistics["Dictionary"]["Numbers"][key]["New"] = statistics["Dictionary"]["Numbers"][key]["Old"]

			# If the "Items" key does exist in the local media dictionary
			# (If the "Items" key exists inside the media dictionary, we add 1 to the new number, because the old number has been decreased by one before, to be correct)
			if "Items" in media:
				# Add one to the new number
				statistics["Dictionary"]["Numbers"][key]["New"] += 1

		# Define the local media title as the media title in the user language
		media_title = '"' + media["Titles"]["Language"] + '"'

		# Define the parameter as the media type plus the media title
		parameter = media_type["The"] + " " + media_title

		# If the "Items" key exists in the local media dictionary
		# And the "Item" key is inside the media titles dictionary
		# And the media item title is not the same as the media title
		if (
			"Items" in media and
			"Item" in media["Titles"] and
			media["Titles"]["Item"][item_key] != media["Titles"][title_key]
		):
			# Get the gender of the media item
			gender = self.Define_Media_Item_Text(root_dictionary)[2]

			# Define a shortcut for the item type
			item_type = media["Item"]["Type"][self.language["Small"]].lower()

			# Get the item title in the user language
			item_title = self.Get_Media_Title(root_dictionary, language = self.language["Small"], item = True)

			# Define the text to add as the "the" text in the item gender, the item type and the media type "of the" text
			the_text = self.media_types["Genders"][self.language["Small"]][gender]["the"]
			of_the_text = media["Texts"]["Container texts"]["Of the"]

			text = the_text + " " + item_type + ' "{}"'.format(item_title) + " " + of_the_text

			# Define the local media title as the media title in the user language
			text = text + " " + media_title

			# Define the parameter as the defined text
			parameter = text

		# Define the statistic text, formatting the template with the parameter
		statistics["Text"] = self.language_texts["times_that_i_watched_{}"].format(parameter)

		# ---------- #

		# Update the external statistics of the current year using the "Update_External_Statistics" root method of the "Diary_Slim" class
		# And return the statistics text
		return self.Diary_Slim.Update_External_Statistics(statistic_key, statistics)

	def Get_Media_List(self, dictionary, statuses = None):
		'''
		Returns a list of media of a specific media type that contains a media status

			Parameters:
				dictionary (dict): a media type dictionary containing the media type keys
				statuses_list (str or list): a statuses string or list used to get the media that has the specific statuses

			Returns:
				media_list (list): The list of media that contains the medias that have the parameter statuses string or list
		'''

		# Get the list of statuses from the media type dictionary
		statuses_list = dictionary["Statuses"].copy()

		# If the statuses parameter is not None, use it as the statuses
		if statuses != None:
			statuses_list = statuses

		# If the type of the statuses is a string, make it a list of only the string
		if type(statuses_list) == str:
			statuses_list = [
				statuses_list
			]

		# Define a local list of media
		media_list = []

		# Iterate through each status in the list of statuses
		for status in statuses_list:
			# If the status is a dictionary
			if type(status) == dict:
				# Get the English status
				status = status["en"]

			# Add the list of media with that status to the local list of media
			media_list.extend(dictionary["JSON"]["Statuses"][status])

		# Sort the list of media
		media_list = sorted(media_list, key = str.lower)

		# Return the list of media
		return media_list

	def Select_Media_Type(self, options = None):
		dictionary = {
			"Texts": {
				"Show": self.language_texts["media_types"],
				"Select": self.language_texts["select_one_media_type_to_watch"]
			},
			"List": {
				"en": self.media_types["Plural"]["en"].copy(),
				self.language["Small"]: self.media_types["Plural"][self.language["Small"]].copy()
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

		# Get the root information dictionary from the root "Information.json" file
		root_information = self.JSON.To_Python(self.folders["Media information"]["Information"])

		# Get the media numbers dictionary
		media_numbers = root_information["Media numbers"]

		# Make a copy of the list of media types in English
		media_types = deepcopy(dictionary["List"]["en"])

		# Update each media type text to add the number of medias for each media type
		# To show texts with the number of medias such as:
		# Animes (40)
		# Videos (109)
		i = 0
		for plural_media_type in self.media_types["Plural"]["en"]:
			# If the plural media type is inside the list of media in English
			if plural_media_type in dictionary["List"]["en"]:
				# Iterate through the list of small languages
				for language in self.languages["Small"]:
					# Get the number of medias for the current media type
					media_number = media_numbers["By media type"][plural_media_type]

					# Add the number of medias to the "List" text for the current language
					dictionary["List"][language][i] = dictionary["List"][language][i] + " (" + str(media_number) + ")"

				# Add one to the "i" number
				i += 1

		# Ask the user to select the media type if the "option" and "number" keys are not present inside the dictionary
		if (
			"option" not in dictionary and
			"number" not in dictionary
		):
			# Define the list of options as the list of plural media types in English
			options = media_types

			# Define the list of language options as the list of media types in the user language
			language_options = dictionary["List"][self.language["Small"]]

			# Define the show and select texts as the texts inside the "Texts" dictionary
			show_text = dictionary["Texts"]["Show"]
			select_text = dictionary["Texts"]["Select"]

			dictionary["option"] = self.Input.Select(options = options, language_options = language_options, show_text = show_text, select_text = select_text)["option"]

		# If the "number" key is inside the dictionary
		if "number" in dictionary:
			# Use the number to select the media type
			dictionary["option"] = media_types[dictionary["number"]]

		# Get the selected media type dictionary from the root media types dictionary using the option as a key
		dictionary.update(self.media_types[dictionary["option"]])

		# Get the status from the options dictionary
		if (
			options != None and
			"Status" in options
		):
			dictionary["Status"] = options["Status"]

		# Get the list of media using the correct status
		dictionary["Media list"] = self.Get_Media_List(dictionary, dictionary["Status"])

		# Check if the status should be added to the list of media
		if self.add_status == True:
			# Call the method to add status to the list of media and update the dictionary
			dictionary = self.Add_Status_To_Media_List(dictionary)

		# Add the list of media length numbers to the media types list to show on the select media
		for language in self.languages["Small"]:
			for text_type in ["Singular", "Plural"]:
				dictionary[text_type]["Show"] = dictionary[text_type][self.language["Small"]] + " (" + str(len(dictionary["Media list"])) + ")"

		# Update the "Show" text
		dictionary["Texts"]["Show"] = self.Text.By_Number(dictionary["Media list"], dictionary["Singular"]["Show"], dictionary["Plural"]["Show"])

		return dictionary

	def Add_Status_To_Media_List(self, dictionary):
		# Make a copy of the original list of media
		dictionary["Medias"]["List (with statuses)"] = dictionary["Medias"]["List"].copy()

		# Define the media number as zero
		media_number = 0

		# Define a text template to be used to create a text containing the media and its language statuses
		template = "{} - ({})"

		# Iterate over each media in the list of media
		for media in dictionary["Medias"]["List"]:
			# Iterate over each status to find the corresponding language status for the media
			for status in dictionary["Statuses"]:
				# Check if the media is associated with the current status
				if media in dictionary["JSON"]["Statuses"][status]:
					# Get the language status for the current status
					language_status = self.Get_Language_Status(status)

			# Create a list of items to be used to format the text template
			items = [
				dictionary["Medias"]["List (with statuses)"][media_number], # The title of the current media
				language_status # The language status of the media
			]

			# Format the template add update the media text in the "List (with statuses)" list in the media number index
			dictionary["Medias"]["List (with statuses)"][media_number] = template.format(*items)

			# Add one to the media number
			media_number += 1

		# If the list of media (options version) is empty, remove it from the dictionary
		# (That means there are no medias for the current media type)
		if dictionary["Medias"]["List (with statuses)"] == []:
			dictionary["Medias"].pop("List (with statuses)")

		# Return the root dictionary
		return dictionary

	def Add_Additional_Options(self, dictionary, options, language_options, additional_options, to_remove = []):
		# Define the dictionary of questions to be added
		questions = {
			"Show plan to watch media": self.language_texts["show_plan_to_watch_media"],
			"Show non-watching media": self.language_texts["show_non_watching_media"]
		}

		# Define the dictionary to match status and questions
		status_dictionary = {
			"Show plan to watch media": [
				self.texts["plan_to_watch, title()"]["en"]
			],
			"Show non-watching media": [
				self.Language.texts["on_hold, title()"]["en"],
				self.Language.texts["completed, title()"]["en"]
			]
		}

		# Iterate over each additional option and list of statuses in the status dictionary
		for additional_option, status_list in status_dictionary.items():
			# Define a local list of media
			media_list = []

			# Iterate over each status in the status list
			for status in status_list:
				# Get the list of media of the current status
				status_media_list = dictionary["Media type"]["JSON"]["Statuses"][status]

				# If the list of media of the current status is not empty
				if status_media_list != []:
					# Extend the local list of media with the current status list of media
					media_list.extend(status_media_list)

			# If the local list of media is empty
			if media_list == []:
				# If the local list of media is empty add the additional option to the "to remove" list
				to_remove.append(additional_option)

		# If the "to remove" parameter is not an empty list
		if to_remove != []:
			# Iterate through the list and remove the items from the questions dictionary
			for item in to_remove:
				# Remove the brackets from the item
				item = item.replace("[", "").replace("]", "")

				# Remove the item
				questions.pop(item)

		# Iterate through the questions inside the dictionary
		for question, text in questions.items():
			# Format the question and question text with brackets
			question = f"[{question}]"
			text = f"[{text}]"

			# Add the question name to the list of options
			options.append(question)

			# Add the question text to the list of language options
			language_options.append(text)

			# Add the question name to the list of additional options
			additional_options.append(question)

		# Return the lists of options, language options, and additional options
		return options, language_options, additional_options

	def Update_Media_List(self, dictionary, options, language_options, additional_options_selected, status_type):
		# Define the list of statuses with the "watching" statuses
		statuses = [
			self.texts["watching, title()"]["en"],
			self.texts["re_watching, title()"]["en"]
		]

		# Update the list of statuses based on the provided status type

		# If the "plan to watch" text is present in the status type text
		# Or if there is any option in the "additional_options_selected" list that contains "plan to watch"
		if (
			"plan to watch" in status_type["Original"] or
			any("plan to watch" in option for option in additional_options_selected)
		):
			# If any of the above conditions are true, add the "Plan to watch" status to the list of statuses
			statuses.extend([
				self.texts["plan_to_watch, title()"]["en"]
			])

		# If the "non-watching" text is present in the status type text
		# Or if there is any option in the "additional_options_selected" list that contains "non-watching"
		if (
			"non-watching" in status_type["Original"] or
			any("non-watching" in option for option in additional_options_selected)
		):
			# If any of the above conditions are true, add the "On hold" and "Completed" statuses to the list of statuses
			statuses.extend([
				self.Language.texts["on_hold, title()"]["en"],
				self.Language.texts["completed, title()"]["en"]
			])

		# If the "To remove" key does not exist
		if "To remove" not in dictionary:
			dictionary["To remove"] = []

		# Add the selected option to the "To remove" list
		dictionary["To remove"].append(status_type["Original"])

		# Define a shortcut to the media type dictionary
		media_type = dictionary["Media type"]

		# Update the statuses list inside the "Media type" dictionary
		media_type["Statuses"] = statuses

		# Get the list of media using the new list of statuses
		options = self.Get_Media_List(media_type)

		# Define the list of language options to show to the user as the list of media
		language_options = options

		# Update the list of media inside the "Media type" dictionary
		media_type["Medias"]["List"] = options

		# Check if the status should be added to the list of media
		if self.add_status == True:
			# Call the method to add watching statuses to the list of media and update the dictionary
			media_type = self.Add_Status_To_Media_List(media_type)

			# Use the list of media with their respective watching statuses as the list of language options
			language_options = media_type["Medias"]["List (with statuses)"]

		# Get the number of medias
		media_number = str(len(media_type["Medias"]["List"]))

		# Update the singular and plural "Show" texts to update the number of medias
		for grammatical_number in ["Singular", "Plural"]:
			# Get the media type text for the current grammatical number and the user language
			text = media_type[grammatical_number][self.language["Small"]]

			# Add the media type text and the media number to update the "Show" text in the current grammatical number
			media_type[grammatical_number]["Show"] = text + " (" + media_number + ")"

		# Define the show text based on the number of medias in the list
		# Before adding the additional options
		show_text = self.Text.By_Number(media_type["Medias"]["List"], media_type["Singular"]["Show"], media_type["Plural"]["Show"])

		# Add additional options to the lists of options
		options, language_options, additional_options = self.Add_Additional_Options(dictionary, options, language_options, [], to_remove = dictionary["To remove"])

		# Return the lists of options, language options, and the show text
		return options, language_options, show_text

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
		text = dictionary["Media type"]["Singular"][self.language["Small"]]

		if "Select" in dictionary["Media type"]["Singular"]:
			text = dictionary["Media type"]["Singular"]["Select"]

		# Define the select text
		dictionary["Texts"]["Select"] = self.language_texts["select_{}_to_watch"].format(dictionary["Media type"]["Genders"][self.language["Small"]]["a"] + " " + text.lower())

		# Ask the user to select the media
		if "Title" not in media:
			# Define the list of options as the default list of media
			options = dictionary["Media type"]["Medias"]["List"]

			# Define the list of language options to show to the user as the default list of media
			language_options = dictionary["Media type"]["Medias"]["List"]

			# If a list of media with their respective statuses is inside the media type "Medias" dictionary, use it
			if "List (with statuses)" in dictionary["Media type"]["Medias"]:
				language_options = dictionary["Media type"]["Medias"]["List (with statuses)"]

			# Define the list of additional options
			additional_options = [
				"Additional option"
			]

			# Define the list of additional options selected
			additional_options_selected = []

			# If the "Add status option" is inside the "Media" dictionary
			if "Add status options" in dictionary["Media"]:
				# Update the lists of options, language options, and additional options using the method
				options, language_options, additional_options = self.Add_Additional_Options(dictionary, options, language_options, additional_options)

			# Define the option as "Additional option" by default, to run the while loop
			option = "Additional option"

			# Define the show and select texts
			show_text = dictionary["Texts"]["Show"]
			select_text = dictionary["Texts"]["Select"]

			# While the selected option is inside the list of additional options
			while option in additional_options:
				# Ask the user to select an option from the list of options
				selection = self.Input.Select(options, language_options = language_options, show_text = show_text, select_text = select_text)

				# Define the option as the original option
				option = selection["Option"]["Original"]

				# If the selected option is inside the list of additional options
				if option in additional_options:
					# Add the option to the list of additional options selected
					additional_options_selected.append(option)

					# Send the option to the "Update_Media_List" method to update the list of media
					options, language_options, show_text = self.Update_Media_List(dictionary, options, language_options, additional_options_selected, selection["Option"])

				# If the selected option is not inside the list of additional options
				elif option not in additional_options:
					# Then define it as the media title
					media["Title"] = option

		# Sanitize the media title
		sanitized_title = self.Sanitize_Title(media["Title"])

		if media["Title"] != "[" + self.Language.language_texts["finish_selection"] + "]":
			# Define the media information and local media folder
			if "Folders" in media:
				if "root" not in media["Folders"]:
					# Define a local folder to check if it exists
					folder = dictionary["Media type"]["Folders"]["Media information"]["root"] + self.Sanitize(sanitized_title, restricted_characters = True) + "/"

					media["Folders"].update({
						"root": folder
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
				"Has a list of media items" in media["States"] and
				media["States"]["Has a list of media items"] == False or
				self.item == True
			):
				# Define the list of media folders to create
				folders = [
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
				media["Language"] = self.language["Full"]

				# Define the media language as "日本語" (Nihongo, Japanese) for anime media
				if dictionary["Media type"]["Plural"]["en"] == self.texts["animes, title()"]["en"]:
					media["Language"] = "日本語"

				# Define the default media language as the user language for video media
				if dictionary["Media type"]["Plural"]["en"] == self.texts["videos, title()"]["en"]:
					media["Language"] = self.language["Full"]

				# Define a shortcut to the "Original language" text
				original_language_text = self.Language.language_texts["original_language"]

				# If the "Original language" key exists in the media "Details" dictionary
				if original_language_text in media["Details"]:
					# Define the media language as the original language
					media["Language"] = media["Details"][original_language_text]

				# Define a local list of full languages
				full_languages = list(self.languages["Full"].values())

				# If the media language is inside the local list of full languages
				if media["Language"] in full_languages:
					# Iterate through the language keys and dictionaries
					for small_language, language in self.languages["Dictionary"].items():
						# Define a shortcut to the full language
						full_language = language["Full"]

						# If the full current language is the same as the media language
						if full_language == media["Language"]:
							# Define the media full and small language as the current language
							media["Full language"] = full_language
							media["Language"] = small_language

				# Define the local media states dictionary as the root media states dictionary
				media_states = deepcopy(self.media_states)

				# If the "States" key is inside the media dictionary
				if "States" in media:
					# Update its keys with the keys of the local one
					media["States"].update(media_states)

				# Else if the key is not inside
				elif "States" not in media:
					# Define the root media states dictionary as the local one
					media["States"] = media_states

				# If today is Christmas (December, 25)
				if self.Today_Is_Christmas == True:
					# Define the "Christmas" state as True
					media["States"]["Christmas"] = True

				# Define the "Local" state as True
				media["States"]["Local"] = True

				# Define a local list of origin types
				origin_types = [
					"Local",
					"Remote"
				]

				# Define a shortcut for the "Origin type" key
				origin_type_key = self.Language.language_texts["origin_type"]

				# Define the "has origin type key" switch as False
				has_origin_type_key = False

				# If the "Origin type" key is inside the media "Details" dictionary
				if origin_type_key in media["Details"]:
					# Iterate through the keys inside that list
					for origin_type in origin_types:
						# Get the origin type text in the user language
						origin_type = self.Language.language_texts[origin_type.lower() + ", title()"]

						# If the "Origin type" key is the same as the current origin type
						if media["Details"][origin_type_key] == origin_type:
							# Change the origin type state to True
							media["States"][key] = True

							# Define the "has origin type key" switch as True
							has_origin_type_key = True

				# Define the media states for videos
				# (Video and episodic states)
				if dictionary["Media type"]["Plural"]["en"] == self.texts["videos, title()"]["en"]:
					media["States"]["Video"] = True
					media["States"]["Episodic"] = False

				if self.Language.language_texts["episodic, title()"] in media["Details"]:
					media["States"]["Episodic"] = self.Input.Define_Yes_Or_No(media["Details"][self.Language.language_texts["episodic, title()"]])

				# Define the single unit state
				if self.language_texts["single_unit"] in media["Details"]:
					media["States"]["Single unit"] = self.Input.Define_Yes_Or_No(media["Details"][self.language_texts["single_unit"]])

				# Define the "Series media" state as False for movies
				if dictionary["Media type"]["Plural"]["en"] == self.texts["movies, title()"]["en"]:
					media["States"]["Series media"] = False

				# If the media is a video channel
				if media["States"]["Video"] == True:
					# Define and create the "Channel.json" file
					dictionary["Media"]["Folders"]["channel"] = dictionary["Media"]["Folders"]["root"] + "Channel.json"
					self.File.Create(dictionary["Media"]["Folders"]["channel"])

					# Get the contents of the file
					contents = self.File.Contents(dictionary["Media"]["Folders"]["channel"])

					# If the "Channel.json" file is empty
					# Or the old "Date" key is inside it
					if (
						contents["lines"] == [] or
						'"Date":' in contents["string"]
					):
						# Get the channel information dictionary
						channel = self.Get_YouTube_Information("Channel", dictionary["Media"]["Details"]["ID"])

						# Get the channel date
						channel_date = self.Date.From_String(channel["Times"]["UTC"])

						# Update the "Start date" key of the media details
						dictionary["Media"]["Details"][self.Date.language_texts["start_date"]] = channel_date["Formats"]["HH:MM DD/MM/YYYY"]

						# Update the "Year" key of the media details
						dictionary["Media"]["Details"][self.Date.language_texts["year, title()"]] = channel_date["Units"]["Year"]

						# Update the media details dictionary
						self.File.Edit(dictionary["Media"]["Folders"]["details"], self.Text.From_Dictionary(dictionary["Media"]["Details"]), "w")

						# Add the "Channel creation times" after the "Times" key and remove the "Times" key
						key_value = {
							"Channel creation times": channel["Times"]
						}

						channel = self.JSON.Add_Key_After_Key(channel, key_value, after_key = "Times", remove_after_key = True)

						# Update the root "Channel" dictionary to be the local one
						dictionary["Media"]["Channel"] = channel

						# Update the "Dictionary" information key to be the "Channel" dictionary
						media["Information"]["Dictionary"] = channel

						# Update the "Channel.json" file with the updated "Channel" dictionary
						self.JSON.Edit(dictionary["Media"]["Folders"]["channel"], dictionary["Media"]["Channel"])

					# If there is a correct channel dictionary, get it from the "Channel.json" file
					else:
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

				# Define the default media "Episode" dictionary with its keys
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

		# If the media is a series media (not a movie)
		if dictionary["Media"]["States"]["Series media"] == True:
			# Define the media items dictionary with the folders and number keys
			dictionary["Media"]["Items"] = {
				"Folders": {
					"root": dictionary["Media"]["Folders"]["root"] + dictionary["Media type"]["Subfolders"]["Plural"] + "/"
				},
				"Number": 1,
				"Current": "",
				"List": [],
				"Dictionary": {}
			}

			# If the media items folder exists
			if (
				self.Folder.Exists(dictionary["Media"]["Items"]["Folders"]["root"]) == True or
				dictionary["Media"]["States"]["Has a list of media items"] == True
			):
				# The media has a media items list
				dictionary["Media"]["States"]["Has a list of media items"] = True

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

				# Define the media item folders
				for name in dictionary["Media"]["Items"]["List"]:
					# Get the media item name
					name = self.Sanitize_Title(name)

					# ---------- #

					# Define and create the media item folder
					dictionary["Media"]["Items"]["Folders"][name] = {
						"root": dictionary["Media"]["Items"]["Folders"]["root"] + name + "/"
					}

					self.Folder.Create(dictionary["Media"]["Items"]["Folders"][name]["root"])

					# ---------- #

					# Define the details file
					dictionary["Media"]["Items"]["Folders"][name]["details"] = dictionary["Media"]["Items"]["Folders"][name]["root"] + self.Language.language_texts["details, title()"] + ".txt"

					# ---------- #

					# Define the key to get the media title
					key = "Original"

					if "Romanized" in dictionary["Media"]["Titles"]:
						key = "Romanized"

					# Get the media title
					media_title = dictionary["Media"]["Titles"][key]

					# Get the media item title
					item_title = name

					# Define the default separator as a space
					separator = " "

					# If the media item title has two or more characters
					# And the media item title has a colon and a space at the start
					if (
						len(item_title) >= 2 and
						item_title[0] + item_title[1] == ": "
					):
						# Define the separator as an empty string
						separator = ""

					# Define the title variable as an empty string
					title = ""

					# Add the original media title if it is not present in the item title
					if media_title not in item_title:
						title += media_title + separator

					# Add the item title to the local title
					title += item_title

					# ---------- #

					# Make a copy of the root dictionary
					dictionary_copy = deepcopy(dictionary)

					# Add the current media item with its keys
					dictionary_copy["Media"]["Item"] = {
						"Folders": dictionary["Media"]["Items"]["Folders"][name]
					}

					# ---------- #

					# Get the media item titles
					titles = self.Define_Media_Titles(dictionary_copy, item = True)["Media"]["Item"]["Titles"]

					# Add the media item to the dictionary of media items, with its "Titles" dictionary and the "With media title" title
					dictionary["Media"]["Items"]["Dictionary"][name] = {
						"Titles": titles,
						"With media title": {
							"Original": title
						}
					}

				# Define current media item
				title = dictionary["Media"]["Items"]["Current"]

				show_text = self.Text.Capitalize(dictionary["Media type"]["Subfolders"]["Plural"])
				select_text = self.language_texts["select_a_season"]

				items_list = dictionary["Media"]["Items"]["List"].copy()

				# Define show and select text for video media
				if dictionary["Media"]["States"]["Video"] == True:
					show_text = self.Text.Capitalize(self.language_texts["video_series, capitalize()"])
					select_text = self.language_texts["select_a_youtube_video_series"]

				# Iterate through media items list
				for media_list_item in dictionary["Media"]["Items"]["List"].copy():
					folders = {
						"root": dictionary["Media"]["Items"]["Folders"]["root"] + self.Sanitize_Title(media_list_item) + "/"
					}

					# Define the details file
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

							for language in self.languages["Small"]:
								if language not in dictionary["Media"]["Items"]["Secondary types"][item_type]:
									dictionary["Media"]["Items"]["Secondary types"][item_type][language] = []

						# Iterate through the secondary type keys list
						i = 0
						for secondary_type in self.secondary_types["Singular"][self.language["Small"]]:
							# If the type inside the media item details is equal to the singular type
							if details[self.Language.language_texts["type, title()"]] == secondary_type:
								for item_type in ["Singular", "Plural"]:
									for language in self.languages["Small"]:
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
						# Define the "Titles" folder
						folders["Titles"] = {
							"root": folders["root"] + self.Language.language_texts["titles, title()"] + "/"
						}

						# Define the titles files

						# Iterate through the language keys and dictionaries
						for small_language, language in self.languages["Dictionary"].items():
							# Define a shortcut to the full language
							full_language = language["Full"]

							# Define the titles file
							folders["titles"][small_language] = folders["titles"]["root"] + full_language + ".txt"

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

				sanitized_title = self.Sanitize_Title(title)

				# Define the media item dictionary and its keys
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
						titles_file = titles_folder + self.languages["Full"]["en"] + ".txt"

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

					for plural_type in dictionary["Media"]["Items"]["Secondary types"]["Plural"][self.language["Small"]]:
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
				for language in self.languages["Small"]:
					# Get the media title in the current language
					media_title = self.Get_Media_Title(dictionary, language = language)

					# Define the local empty title
					title = ""

					# Get the correct media item title in the current language
					item_title = self.Get_Media_Title(dictionary, language = language, item = True)

					# Define the default separator as a space
					separator = " "

					# If the item title has two or more characters
					# And the item title has a colon and a space at the start
					if (
						len(item_title) >= 2 and
						item_title[0] + item_title[1] == ": "
					):
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

				# If the media item is a single unit one
				if dictionary["Media"]["States"]["Single unit"] == True:
					dictionary["Media"]["Item"]["Folders"]["Media"]["root"] = dictionary["Media"]["Folders"]["Media"]["root"]

				# Reset the "The media item is the root media" state to its default value
				dictionary["Media"]["States"]["The media item is the root media"] = False

				# Define if the media item is the root media
				if (
					dictionary["Media"]["Item"]["Title"] == dictionary["Media"]["Title"] or
					"Romanized" in dictionary["Media"]["Item"]["Titles"] and
					dictionary["Media"]["Item"]["Titles"]["Romanized"] == dictionary["Media"]["Titles"]["Romanized"]
				):
					dictionary["Media"]["States"]["The media item is the root media"] = True

			# If the folder of media items does not exist, define that the media has no media item list
			# And add the root media to the media items list
			if (
				self.Folder.Exists(dictionary["Media"]["Items"]["Folders"]["root"]) == False and
				dictionary["Media"]["States"]["Has a list of media items"] == False
			):
				dictionary["Media"]["Items"]["List"] = [
					dictionary["Media"]["Title"]
				]

				dictionary["Media"]["States"]["The media item is the root media"] = True

		# If the media is not series media (is a movie)
		# Or it is a series media (not a movie)
		# And it does not contain a media item list
		if (
			dictionary["Media"]["States"]["Series media"] == False or
			dictionary["Media"]["States"]["Has a list of media items"] == False
		):
			# Define the item dictionary as a copy of the root media dictionary
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
		self.dictionaries["Watched"] = deepcopy(self.template_dictionary)

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

		# If the media is a series media (not a movie)
		# And the media item is not a single unit
		if (
			dictionary["Media"]["States"]["Series media"] == True and
			dictionary["Media"]["States"]["Single unit"] == False
		):
			# Defile the "Titles" folder for the media item
			dictionary["Media"]["Item"]["Folders"]["Titles"] = {
				"root": dictionary["Media"]["Item"]["Folders"]["root"] + self.Language.language_texts["titles, title()"] + "/"
			}

			# Create it
			self.Folder.Create(dictionary["Media"]["Item"]["Folders"]["Titles"]["root"])

			# Define a shortcut to it
			titles_folder = dictionary["Media"]["Item"]["Folders"]["Titles"]

			# Iterate through the language keys and dictionaries
			for small_language, language in self.languages["Dictionary"].items():
				# Define a shortcut to the full language
				full_language = language["Full"]

				# Define and create the episode titles file for the current language
				titles_folder[small_language] = titles_folder["root"] + full_language + ".txt"
				self.File.Create(titles_folder[small_language])

			# If the media is a video channel
			if dictionary["Media"]["States"]["Video"] == True:
				# Iterate through the list of video file keys
				for file_key in ["IDs", "Dates"]:
					# Define a text key for the file
					text_key = file_key.lower().replace(" ", "_") + ", title()"

					# Get the file name for the file
					file_name = self.Language.language_texts[text_key]

					# Define and create the file
					titles_folder[file_key] = titles_folder["root"] + file_name + ".txt"
					self.File.Create(titles_folder[file_key])

				# If the media has a list of media items
				if dictionary["Media"]["States"]["Has a list of media items"] == True:
					# Define an initial playlist ID as an empty string
					playlist_id = ""

					# If the "Origin location" key is inside the media item details dictionary
					if self.Language.language_texts["origin_location"] in dictionary["Media"]["Item"]["Details"]:
						# Define a shortcut to the origin location key to made the code easier to look at
						origin_location_key = self.Language.language_texts["origin_location"]

						# Define a shortcut to the origin location
						origin_location = dictionary["Media"]["Item"]["Details"][origin_location_key]

						# Get the playlist link
						playlist_link = dictionary["Media"]["Item"]["Details"][self.Language.language_texts["link, title()"]]

						# If it is not a question mark and is not None
						if origin_location not in ["?", "None"]:
							# Get the playlist ID (origin location) of the playlist based on the playlist link
							playlist_id = playlist_link.split("list=")[-1]

							# Add the playlist ID to the media item details dictionary
							dictionary["Media"]["Item"]["Details"][origin_location_key] = playlist_id

					# Define and create the media item "Playlist.json" file
					dictionary["Media"]["Item"]["Folders"]["Playlist"] = dictionary["Media"]["Item"]["Folders"]["root"] + "Playlist.json"
					self.File.Create(dictionary["Media"]["Item"]["Folders"]["Playlist"])

					# Get the contents of the file
					contents = self.File.Contents(dictionary["Media"]["Item"]["Folders"]["Playlist"])

					# If the playlist ID is not empty
					# And (the file is empty
					# Or the old "Date" key is inside the file
					# Or the new "Playlist creation times" key is not inside the file)
					if (
						playlist_id != "" and
						(
							contents["Lines"] == [] or
							'"Date":' in contents["string"] or
							"Playlist creation times" not in contents["string"]
						)
					):
						# Get the playlist information using the "Get_YouTube_Information" method that uses the "API" utility method
						playlist = self.Get_YouTube_Information("Playlist", playlist_id)

						# If the "Channel" dictionary inside the playlist dictionary is not the same as the media channel
						if dictionary["Media"]["Channel"]["Channel"] != playlist["Channel"]:
							# Then update the playlist "Channel" dictionary with the media "Channel" dictionary
							playlist["Channel"] = dictionary["Media"]["Channel"]["Channel"]

						# Get the playlist date
						playlist_date = self.Date.From_String(playlist["Times"]["UTC"])

						# Get the "IDs.txt" file
						ids_file = titles_folder["root"] + self.Language.language_texts["ids, title()"] + ".txt"

						# Get the list of video IDs
						ids_list = self.File.Contents(ids_file)["lines"]

						# If the list of IDs is not empty
						if ids_list != []:
							# Get the first video ID
							first_video_id = ids_list[0]

							# Get the first video information using the "Get_YouTube_Information" method that uses the "API" utility method
							first_video = self.Get_YouTube_Information("Video", first_video_id)

							# Transform the first video date into a date dictionary
							first_video_date = self.Date.From_String(first_video["Times"]["UTC"])

							# If the date of the first video is older than the creation date of the playlist
							# Define a local date as the date of the first video
							if first_video_date["Object"] < playlist_date["Object"]:
								date = first_video_date

							# If the  date of the first video is newer than the creation date of the playlist
							# Define a local date as the date of the playlist
							if first_video_date["Object"] > playlist_date["Object"]:
								date = playlist_date

							# Update the "Start date" key of the media item details dictionary
							dictionary["Media"]["Item"]["Details"][self.Date.language_texts["start_date"]] = date["Formats"]["HH:MM DD/MM/YYYY"]

							# Get the last video ID
							last_video_id = ids_list[-1]

							# Get the last video information using the "Get_YouTube_Information" method that uses the "API" utility method
							last_video = self.Get_YouTube_Information("Video", last_video_id)

							# Transform the first video date into a date dictionary
							last_video_date = self.Date.From_String(last_video["Times"]["UTC"])

							# Update the "End date" key of the media item details and define it as the last video date
							# (The last video in the playlist is probably newer than the creation date of the playlist)
							dictionary["Media"]["Item"]["Details"][self.Date.language_texts["end_date"]] = last_video_date["Formats"]["HH:MM DD/MM/YYYY"]

							# Update the "Year" key of the media item details
							dictionary["Media"]["Item"]["Details"][self.Date.language_texts["year, title()"]] = date["Units"]["Year"]

							# Transform the media item details dictionary into a text
							media_item_details = self.Text.From_Dictionary(dictionary["Media"]["Item"]["Details"])

							# Update the media item details file with the updated media item details dictionary
							self.File.Edit(dictionary["Media"]["Item"]["Folders"]["details"], media_item_details, "w")

						# Add the "Playlist creation times" key after the "Times" key and remove the "Times" key
						key_value = {
							"Playlist creation times": playlist["Times"]
						}

						playlist = self.JSON.Add_Key_After_Key(playlist, key_value, after_key = "Times", remove_after_key = True)

						# Update the "Playlist.json" file with the updated playlist dictionary
						self.JSON.Edit(dictionary["Media"]["Item"]["Folders"]["Playlist"], playlist)

					# If there is a correct playlist dictionary, get it from the "Playlist.json" file
					else:
						playlist = self.JSON.To_Python(dictionary["Media"]["Item"]["Folders"]["Playlist"])

					# Update the root "Playlist" dictionary to be the local one
					dictionary["Media"]["Item"]["Playlist"] = playlist

					# Update the "Dictionary" information key to be the "Playlist" dictionary
					dictionary["Media"]["Item"]["Information"]["Dictionary"] = playlist

		# ---------- #

		# Define a shortcut to the comments folder
		folder = dictionary["Media"]["Item"]["Folders"]["comments"]

		# Define the local comments dictionary as the root "Comments" dictionary template
		comments = deepcopy(self.dictionaries["Comments"])

		# If the media is a video channel
		if dictionary["Media"]["States"]["Video"] == True:
			# Update the local comments dictionary to be the video version of the root "Comments" dictionary
			comments = deepcopy(self.dictionaries["Comments (videos)"])

			# If the media has no media item list, remove the "Playlist" key from the dictionary
			if dictionary["Media"]["States"]["Has a list of media items"] == False:
				comments.pop("Playlist")

		# If the "Comments.json" file is not empty
		if self.File.Contents(folder["comments"])["lines"] != []:
			# Define the local comments dictionary as the file dictionary
			comments = self.JSON.To_Python(folder["comments"])

		# If the media is a video channel
		if dictionary["Media"]["States"]["Video"] == True:
			# Update the "Channel" key with the most up-to-date dictionary
			comments["Channel"] = dictionary["Media"]["Channel"]

			# If the media has a list of media items
			if dictionary["Media"]["States"]["Has a list of media items"] == True:
				# Update the "Playlist" key with the most up-to-date dictionary
				comments["Playlist"] = dictionary["Media"]["Item"]["Playlist"]

		# Update the total number of comments with the length of the list of entries
		comments["Numbers"]["Total"] = len(comments["Entries"])

		# Define the "Comments" dictionary inside the media item dictionary
		dictionary["Media"]["Item"]["Comments"] = deepcopy(comments)

		# Update the "Comments.json" file with the updated "Comments" dictionary
		self.JSON.Edit(folder["comments"], comments)

		# Update the number of comments of the "Watched" dictionary with the number of comments in the comments dictionary
		self.dictionaries["Watched"]["Numbers"]["Comments"] = comments["Numbers"]["Total"]

		# ---------- #

		# Define the "Watched" dictionary inside the media item dictionary
		dictionary["Media"]["Item"]["Watched"] = deepcopy(self.dictionaries["Watched"])

		# Update the watched "Entries.json" file with the updated "Watched" dictionary
		self.JSON.Edit(dictionary["Media"]["Item"]["Folders"]["Watched"]["entries"], self.dictionaries["Watched"])

		# ---------- #

		# Define and create the media item "Dates.txt" file
		dictionary["Media"]["Item"]["Folders"]["dates"] = dictionary["Media"]["Item"]["Folders"]["root"] + self.Date.language_texts["dates, title()"] + ".txt"
		self.File.Create(dictionary["Media"]["Item"]["Folders"]["dates"])

		# If the media is a series media (not a movie)
		if dictionary["Media"]["States"]["Series media"] == True:
			# Define a shortcut to the "Titles" folder dictionary
			titles_folder = dictionary["Media"]["Item"]["Folders"]["Titles"]

			# Define the "Episodes" dictionary with the "Number" and "Titles" keys
			dictionary["Media"]["Item"]["Episodes"] = {
				"Number": 0,
				"Titles": {
					"Files": {}
				}
			}

			# Define the default episode separator as "EP"
			dictionary["Media"]["Episode"].update({
				"Separator": "EP"
			})

			# If there is a custom separator inside the media "Details" dictionary
			if self.language_texts["episode_number_name"] in dictionary["Media"]["Details"]:
				# Define it as the episode separator
				dictionary["Media"]["Episode"]["Separator"] = dictionary["Media"]["Details"][self.language_texts["episode_number_name"]]

			# If there is a custom separator inside the media media "Details" dictionary
			if self.language_texts["episode_number_name"] in dictionary["Media"]["Item"]["Details"]:
				# Define it as the episode separator
				dictionary["Media"]["Episode"]["Separator"] = dictionary["Media"]["Item"]["Details"][self.language_texts["episode_number_name"]]

			# If the media is a video channel
			if dictionary["Media"]["States"]["Video"] == True:
				# Define the episode separator as nothing
				dictionary["Media"]["Episode"]["Separator"] = ""

				# Iterate through the list of video file keys
				for file_key in ["IDs", "Dates"]:
					# Get the file
					file = titles_folder[file_key]

					# Define it inside the "Files" dictionary
					dictionary["Media"]["Item"]["Episodes"]["Titles"]["Files"][file_key] = file

					# Get the contents from the file and add them to the file key
					dictionary["Media"]["Item"]["Episodes"]["Titles"][file_key] = self.File.Contents(file)["Lines"]

			# Iterate through the language keys and dictionaries
			for small_language, language in self.languages["Dictionary"].items():
				# Define a shortcut to the full language
				full_language = language["Full"]

				# If the media item is not a single unit
				if dictionary["Media"]["States"]["Single unit"] == False:
					# Define the language episode titles file on the "Files" dictionary
					dictionary["Media"]["Item"]["Episodes"]["Titles"]["Files"][small_language] = dictionary["Media"]["Item"]["Folders"]["Titles"][small_language]

					# Get the language episode titles from the file and add them to the "Titles" key
					dictionary["Media"]["Item"]["Episodes"]["Titles"][small_language] = self.File.Contents(dictionary["Media"]["Item"]["Episodes"]["Titles"]["Files"][small_language])["lines"]

					# If the episode separator is not empty
					if dictionary["Media"]["Episode"]["Separator"] != "":
						# Import the Regexp module
						import re

						# Iterate through the list of episode titles in the current language
						i = 1
						for episode_title in dictionary["Media"]["Item"]["Episodes"]["Titles"][small_language]:
							# Get the episode number
							number = str(self.Text.Add_Leading_Zeroes(i))

							# Get the episode separator
							separator = dictionary["Media"]["Episode"]["Separator"]

							# If the separator is "EP"
							# And the "Episodic" key is present inside the media "Details" dictionary
							if (
								separator == "EP" and
								self.Language.language_texts["episodic, title()"] not in dictionary["Media"]["Details"]
							):
								# Define the media as an "Episodic" one
								# (Follows episode order)
								dictionary["Media"]["States"]["Episodic"] = True

							# Iterate through the alternative episode types in the list
							# alternative_episode_types = ["OVA", "ONA", "Special", "Especial", "Shorts", "Curtas"]
							for alternative_episode_type in self.alternative_episode_types:
								# If the episode type plus one or two numbers from zero to nine are inside the episode title
								if re.search(alternative_episode_type + " [0-9]{1,2}", episode_title) != None:
									# Define the episode separator as an empty string
									separator = ""

									# If the "Episodic" key not is inside the media "Details" dictionary
									if self.Language.language_texts["episodic, title()"] not in dictionary["Media"]["Details"]:
										# Define the media as an "Episodic" one
										# (Follows episode order)
										dictionary["Media"]["States"]["Episodic"] = True

							# If the "Type" key is inside the media item "Details" dictionary
							if self.Language.language_texts["type, title()"] in dictionary["Media"]["Item"]["Details"]:
								# Define the episode separator as an empty string
								separator = ""

							# Define the episode title as the episode separator plus the episode number, a space, and the episode title
							episode_title = separator + number + " " + episode_title

							# If the separator is not an empty string
							# And the episode number is not inside the episode title inside the titles list
							if (
								separator != "" and
								number not in dictionary["Media"]["Item"]["Episodes"]["Titles"][small_language][i - 1]
							):
								# Add it to the list with the correct (i) index
								dictionary["Media"]["Item"]["Episodes"]["Titles"][small_language][i - 1] = episode_title

							i += 1

			# If the media item is a single unit one
			if dictionary["Media"]["States"]["Single unit"] == True:
				# Define the "Title" and "Titles" keys for the "Episode" dictionary as the same keys in the media "Item" dictionary
				dictionary["Media"]["Episode"]["Title"] = dictionary["Media"]["Item"]["Title"]
				dictionary["Media"]["Episode"]["Titles"] = dictionary["Media"]["Item"]["Titles"]

				# Iterate through the list of small languages
				for language in self.languages["Small"]:
					# If the language is not inside the episode "Titles" dictionary
					if language not in dictionary["Media"]["Episode"]["Titles"]:
						# Get the media item title in the current language to use as the episode title
						dictionary["Media"]["Episode"]["Titles"][language] = self.Get_Media_Title(dictionary, language = language, item = True)

			# If the media item is not a single unit one
			if dictionary["Media"]["States"]["Single unit"] == False:
				# Update the number of episodes to be the number of episode titles in English
				dictionary["Media"]["Item"]["Episodes"]["Number"] = len(dictionary["Media"]["Item"]["Episodes"]["Titles"]["en"])

			# Add the "Episodes" key and episode number after the defined after key
			key_value = {
				"key": self.language_texts["episodes, title()"],
				"value": dictionary["Media"]["Item"]["Episodes"]["Number"]
			}

			# Define the after key as "End date" and try to find a key that exists inside the media item "Details" dictionary
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

		# If the total number of entries is zero, the watched media is the first one in the year
		if self.dictionaries["Entries"]["Numbers"]["Total"] == 0:
			dictionary["Media"]["States"]["First entry in year"] = True

		# If the total number of media type entries is zero, the watched media by media type is the first one in the year
		if self.dictionaries["Media type"][dictionary["Media type"]["Plural"]["en"]]["Numbers"]["Total"] == 0:
			dictionary["Media"]["States"]["First media type entry in year"] = True

		# Define media texts to be used in the "Show_Media_Information" root method
		dictionary["Media"]["Texts"] = {
			"genders": dictionary["Media type"]["Genders"]
		}

		# Define the container, item, and unit texts as the media type (for movies)
		for item_type in ["container", "item", "unit"]:
			dictionary["Media"]["Texts"][item_type] = dictionary["Media type"]["Singular"].copy()

		dictionary["Media"]["Item"]["Type"] = {}

		# Define the item type
		if self.Language.language_texts["type, title()"] in dictionary["Media"]["Item"]["Details"]:
			dictionary["Media"]["Item"]["Type"] = dictionary["Media"]["Item"]["Details"][self.Language.language_texts["type, title()"]]

		# If the media is not a series media (a movie)
		# And the "Type" dictionary of the "Item" dictionary is empty
		if (
			dictionary["Media"]["States"]["Series media"] == False and
			dictionary["Media"]["Item"]["Type"] == {}
		):
			# Define it as the "Item" text dictionary defined above
			dictionary["Media"]["Item"]["Type"] = dictionary["Media"]["Texts"]["item"]

		# If the media is a series media (not a movie)
		if dictionary["Media"]["States"]["Series media"] == True:
			# Define the unit text as the "episode" text by language
			dictionary["Media"]["Texts"]["unit"] = {}

			for language in self.languages["Small"]:
				dictionary["Media"]["Texts"]["unit"][language] = self.texts["episode"][language]

			# If the media has a list of media items
			# And the current media item is not the root media
			if (
				dictionary["Media"]["States"]["Has a list of media items"] == True and
				dictionary["Media"]["Item"]["Title"] != dictionary["Media"]["Title"]
			):
				# Add the "Item" dictionary to the dictionary of texts
				dictionary["Media"]["Texts"]["item"] = {}

			# If the "Type" dictionary of the "Item" dictionary is empty
			if dictionary["Media"]["Item"]["Type"] == {}:
				# Define it as the "Item" text dictionary defined above
				dictionary["Media"]["Item"]["Type"] = dictionary["Media"]["Texts"]["item"]

			# If the "Type" dictionary is not empty
			if dictionary["Media"]["Item"]["Type"] != {}:
				# Define a local empty dictionary
				dict_ = {}

				# Iterate through the list of singular secondary type in the user language
				i = 0
				for singular_type in self.secondary_types["Singular"][self.language["Small"]]:
					# If the media item type is the same as the current singular secondary type
					if dictionary["Media"]["Item"]["Type"] == singular_type:
						# Iterate through the list of small languages
						for language in self.languages["Small"]:
							# Get the singular secondary type in the current language
							singular_type = self.secondary_types["Singular"][language][i]

							# Define it inside the "Item" dictionary
							dictionary["Media"]["Texts"]["item"][language] = singular_type

							# Add the singular secondary type to the local dictionary in the language key
							dict_[language] = singular_type

					# Add one to the "i" number
					i += 1

				# Define the media item "Type" dictionary as the local dictionary created above
				dictionary["Media"]["Item"]["Type"] = dict_

			# Define the item text as the "season" text for media that have a media item list
			if (
				dictionary["Media"]["States"]["Has a list of media items"] == True and
				dictionary["Media"]["Item"]["Title"] != dictionary["Media"]["Title"] and
				dictionary["Media"]["Texts"]["item"] == {}
			):
				for language in self.languages["Small"]:
					dictionary["Media"]["Texts"]["item"][language] = self.texts["season, title()"][language].lower()

					# If the media item is a single unit one
					if dictionary["Media"]["States"]["Single unit"] == True:
						dictionary["Media"]["Texts"]["item"][language] = self.texts["episode"][language]

			# Define the container, item, and unit texts for video series media
			if dictionary["Media"]["States"]["Video"] == True:
				for language in self.languages["Small"]:
					dictionary["Media"]["Texts"]["container"][language] = self.texts["youtube_channel"][language]
					dictionary["Media"]["Texts"]["item"][language] = self.texts["video_series, type: singular"][language]
					dictionary["Media"]["Texts"]["unit"][language] = self.texts["video"][language]

			if dictionary["Media"]["Item"]["Type"] == {}:
				dictionary["Media"]["Item"]["Type"] = dictionary["Media"]["Texts"]["item"]

		dict_ = deepcopy(dictionary["Media"]["Texts"])

		# Define a shortcut to the season text
		season_text = self.texts["season, title()"][language].lower()

		# Define a shortcut to the video series text
		video_series_text = self.texts["video_series, type: singular"][language]

		# Define media texts by item and gender
		for text_type in ["the", "this", "of"]:
			for key in dict_:
				if key != "genders":
					if text_type + "_" + key not in dictionary["Media"]["Texts"]:
						dictionary["Media"]["Texts"][text_type + "_" + key] = {}

					for language in self.languages["Small"]:
						if dictionary["Media"]["Texts"][key][language] not in [season_text, video_series_text]:
							item_text = dictionary["Media type"]["Genders"][language][text_type]

						if dictionary["Media"]["Texts"][key][language] in [season_text, video_series_text]:
							for gender_key in dict_["genders"][language]:
								gender = dict_["genders"][language][gender_key]

								if text_type == gender_key:
									item_text = self.media_types["Genders"][language]["feminine"][gender_key]

						if dictionary["Media"]["Texts"][key][language] == self.texts["episode"][language]:
							for gender_key in dict_["genders"][language]:
								gender = dict_["genders"][language][gender_key]

								if text_type == gender_key:
									item_text = self.media_types["Genders"][language]["masculine"][gender_key]

						text = dictionary["Media"]["Texts"][key][language].lower()

						if "youtube" in text:
							text = text.replace("youtube", "YouTube")

						dictionary["Media"]["Texts"][text_type + "_" + key][language] = item_text + " " + text

		# Add the "Christmas special" text to the unit text
		if (
			dictionary["Media"]["States"]["Video"] == False and
			self.Today_Is_Christmas == True
		):
			dict_ = {}

			for language in self.languages["Small"]:
				dict_[language] = self.texts["christmas_special_{}"][language].format(dictionary["Media"]["Texts"]["unit"][language])

			dictionary["Media"]["Texts"]["unit"] = dict_

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
		# Define the initial states dictionary with the "States" and "Texts" keys
		states_dictionary = {
			"States": {},
			"Texts": {}
		}

		# Define a list of keys for the states
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

		# Define a list of alternative state texts based on the key
		state_texts = {
			"Watch dubbed": "Watched dubbed",
			"Re-watching": "Re-watched",
			"Completed media": "Completed media",
			"Completed media item": "Completed media item"
		}

		# Iterate through the list of state keys
		for key in keys:
			# If the state is inside the dictionary of media states
			# And it is True
			# Or it is inside the dictionary of media "Dubbing" states
			# And it is True
			if (
				key in dictionary["Media"]["States"] and
				dictionary["Media"]["States"][key] == True or
				key in dictionary["Media"]["States"]["Dubbing"] and
				dictionary["Media"]["States"]["Dubbing"][key] == True
			):
				# If the key has an alternative state text, get it
				if key in state_texts:
					key = state_texts[key]

				# Define the state as true
				state = True

				# If the key is the "Re-watched" key, define its state dictionary to add the "Times" key
				if key == "Re-watched":
					state = {
						"Times": dictionary["Media"]["Episode"]["Re-watching"]["Times"]
					}

				# Define the state dictionary inside the "States" dictionary
				states_dictionary["States"][key] = state

				# Define the state texts of the current state dictionary inside the "Texts" dictionary
				states_dictionary["Texts"][key] = {}

				# Iterate through the list of small languages
				for language in self.languages["Small"]:
					# Define rhe state text as empty by default
					text = ""

					# If the current state is not "Re-watched"
					if key != "Re-watched":
						# Define the text key
						text_key = key.lower().replace(" ", "_")

						# If a underscore does not exist inside the text key, the text key is a single word, then add the ", title()" text
						if "_" not in text_key:
							text_key += ", title()"

						# If the text key is inside the texts dictionary of the "Watch_History" class, get the language text from it
						if text_key in self.texts:
							language_text = self.texts[text_key][language]

						# If the text key is inside the texts dictionary of the "Language" class, get the language text from it
						if text_key in self.Language.texts:
							language_text = self.Language.texts[text_key][language]

						# Define the media unit text as the lowercase version of it
						unit = dictionary["Media"]["Texts"]["unit"][language].lower()

						# Define the unit text for series media as the unit text plus the neutral "of" text, plus the lowercased container text
						if dictionary["Media"]["States"]["Series media"] == True:
							# Get the neutral "of" text
							of_text = self.Language.texts["of, neutral"][language]

							# Get the container text
							container_text = dictionary["Media"]["Texts"]["container"][language].lower()

							# Define the unit text by joining the unit text, neutral "of" text, and lowercased container text
							unit = dictionary["Media"]["Texts"]["unit"][language] + " " + of_text + " " + container_text

						# Define the language text as the "first_{}_in_year" formatted with the media unit text, for the "First media type entry in year" state
						if key == "First media type entry in year":
							language_text = self.Language.texts["first_{}_in_year"][language].format(unit.lower())

						# If the current state is "Completed media" (the media was completed)
						if key == "Completed media":
							# Define the "the text" as the media "the" text and the media container
							the_text = dictionary["Media"]["Texts"]["genders"][language]["the"] + " " + dictionary["Media"]["Texts"]["container"][language].lower()

						# If the current state is "Completed media item" (the media item was completed)
						if key == "Completed media item":
							# Define the item and container texts
							item_text = dictionary["Media"]["Texts"]["item"][language].lower()
							container_text = dictionary["Media"]["Texts"]["container"][language].lower()

							# Define the list of items to use to format the template
							items = [
								item_text,
								container_text
							]

							# Define the default template as the feminine "the {} of {}" text
							template = self.media_types["Genders"][language]["feminine"]["the"] + " {} " + dictionary["Media"]["Texts"]["genders"][language]["of"] + " {}"

							# If the media has a list of media items and the media item is the root media
							# And the root media is not completed (it has more media items to be watched)
							# And the "Last season" key of the media item dictionary is True
							# (This key is True when the "Last season" text is present in the media item details dictionary)
							if (
								dictionary["Media"]["States"]["The media item is the root media"] == True and
								dictionary["Media"]["States"]["Completed media"] == False and
								dictionary["Media"]["Item"]["Last season"] == True
							):
								# Define the template as the masculine "the {}" text
								template = self.media_types["Genders"][language]["masculine"]["the"] + " {}"

								# Define the first item inside the list of items as the media type text (the container text)
								items[0] = container_text

								# Remove the container text from the list of items
								items.pop(1)

								# This will create texts such as:
								# "Completed the season of [anime/cartoon/series]"
								# "Completed the video series of [YouTube channel]"
								# But only if the "Last season" state is True
								# (Movies do not apply here because with them, the "Completed media item" state is never True since movies do not contain media items)

							# If this is not the last season of the media
							if dictionary["Media"]["Item"]["Last season"] == False:
								# Define the item text as "season" text in the current language
								items[0] = self.texts["season, title()"][language].lower()

							# If the media is a video channel
							if dictionary["Media type"]["Plural"]["en"] == "Videos":
								# Define the item text as "series" in the current language
								items[0] = self.texts["series"][language].lower()

							# If the media item is a single unit one
							if dictionary["Media"]["States"]["Single unit"] == True:
								# Define the item text as the item type text in the current language
								items[0] = dictionary["Media"]["Item"]["Type"][language].lower()

							# If the media unit is a single unit one
							if dictionary["Media"]["States"]["Single unit"] == True:
								# Replace the "the" word in the feminine gender with the masculine gender
								feminine_the = self.media_types["Genders"][language]["feminine"]["the"]
								masculine_the = self.media_types["Genders"][language]["masculine"]["the"]

								template = template.replace(feminine_the + " ", masculine_the + " ")

							# Format the "the text" with the list of items
							the_text = template.format(*items)

						# If the media or media item is completed, add the "the text" defined above to the "completed, past_perfect" text
						if key in ["Completed media", "Completed media item"]:
							language_text = self.Language.texts["completed, past_perfect, title()"][language] + " " + the_text

						# If the "youtube" text is inside the language text, correct its case
						if "youtube" in language_text:
							language_text = language_text.replace("youtube", "YouTube")

						# Add the language text to the state text variable
						text += language_text

					# If the current state is "Re-watched"
					if key == "Re-watched":
						# Add the "Re-watched" text plus the number of re-watched to the state text
						re_watching = dictionary["Media"]["Episode"]["Re-watching"]
						number_name = re_watching["Texts"]["Number name"][language]
						times = re_watching["Times"]

						text += number_name + " (" + str(times) + "x)"

					# Define the state text by language
					states_dictionary["Texts"][key][language] = text

		# Return the dictionary of states
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
				for language in self.languages["Small"]:
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

		if self.File.Exists(media["Folders"]["details"]) == True:
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

			# If media type is "Animes"
			# Or the "Romanized title" key exists inside the media details, define the romanized name and Japanese name
			if (
				dictionary["Media type"]["Plural"]["en"] == "Animes" or
				self.Language.language_texts["romanized_title"] in media["Details"]
			):
				if self.Language.language_texts["romanized_title"] in media["Details"]:
					media["Titles"]["Romanized"] = media["Details"][self.Language.language_texts["romanized_title"]]
					media["Titles"]["Language"] = media["Titles"]["Romanized"]

				if "Romanized" in media["Titles"]:
					media["Titles"]["Sanitized"] = media["Titles"]["Romanized"]

				# Define the Japanese title as the original media title
				media["Titles"]["ja"] = media["Details"][self.Language.language_texts["original_title"]]

			# Get the "Title in Japanese" text in the user language
			title_in_japanese = self.Language.texts["title_in_language"]["ja"][self.language["Small"]]

			# If the "Title in Japanese" text in the user language is inside the media details
			if title_in_japanese in media["Details"]:
				# Define the "ja" key as the Japanese media title
				media["Titles"]["ja"] = media["Details"][title_in_japanese]

			if (
				" (" in media["Titles"]["Original"] and
				" (" not in media["Titles"]["Language"]
			):
				media["Titles"]["Language"] = media["Titles"]["Language"] + " (" + media["Titles"]["Original"].split(" (")[-1]

				if self.language["Small"] in media["Titles"]:
					media["Titles"][self.language["Small"]] = media["Titles"][self.language["Small"]] + " (" + media["Titles"]["Original"].split(" (")[-1]

			# Define the media titles by language
			for language in self.languages["Small"]:
				key = self.Language.texts["title_in_language"][language][self.language["Small"]]

				if key in media["Details"]:
					media["Titles"][language] = media["Details"][key]

			media["Titles"]["Language"] = media["Titles"]["Original"]

			if self.language["Small"] in media["Titles"]:
				media["Titles"]["Language"] = media["Titles"][self.language["Small"]]

			if (
				self.language["Small"] not in media["Titles"] and
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
		if len(title) > 1:
			# If the first two characters of the title are a space and a colon
			# Or they are a dot and a space
			if (
				title[0] + title[1] == ": " or
				title[0] + title[1] == ". "
			):
				# Remove them
				title = title[2:]

		# If there are dots inside the title
		# And the "remove dot" parameter is True
		if (
			"." in title and
			remove_dot == True
		):
			# Remove the dots
			title = title.replace(".", "")

		# Remove restricted characters from the title
		title = self.File.Remove_Restricted_Characters(title)

		# Return the title
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
			for language in self.languages["Small"]:
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
			print("\t" + root_dictionary["Media"]["Item"]["With media title"][self.language["Small"]])

	def Get_Language_Status(self, status):
		# Define a switch to tell if the status should be return in English as False by default
		return_english = False

		# If the status is in the user language, then change the switch to True, to return the English version of the status
		if status in self.texts["statuses, type: list"][self.language["Small"]]:
			return_english = True

		# Iterate through the list of statuses in English
		status_number = 0
		for english_status in self.texts["statuses, type: list"]["en"]:
			# If the "return English" switch is False
			# And the English status is the same as the parameter status (it is also in English)
			if (
				return_english == False and
				english_status == status
			):
				# Define the status to return as the status in the user language
				status_to_return = self.texts["statuses, type: list"][self.language["Small"]][status_number]

			# If the "return English" switch is True
			# And the parameter status (it is in the user language) is the same as the current language status
			if (
				return_english == True and
				status == self.texts["statuses, type: list"][self.language["Small"]][status_number]
			):
				# Define the status to return as the status in English
				status_to_return = english_status

			# Add one to the status number
			status_number += 1

		# Return the status to return
		return status_to_return

	def Change_Status(self, dictionary, status = ""):
		# If the status is empty, then define it as "Completed"
		if status == "":
			status = self.Language.language_texts["completed, title()"]

		# Update the "Status" key in the media details dictionary
		dictionary["Media"]["Details"][self.Language.language_texts["status, title()"]] = status

		# Update the media details file
		self.File.Edit(dictionary["Media"]["Folders"]["details"], self.Text.From_Dictionary(dictionary["Media"]["Details"]), "w")

		# Move the media title to the list of media under the new status
		self.Check_Status(dictionary)

		# Return the media status dictionary
		return dictionary["Media"]["Details"]

	def Check_Status(self, dictionary):
		# Define the local media type dictionary as the parameter dictionary
		media_type = dictionary

		# If the "Media type" key is inside the parameter dictionary
		if "Media type" in dictionary:
			# Define the local media type dictionary as the "Media type" dictionary inside it
			media_type = dictionary["Media type"]

			# Get the language status for the media
			language_status = dictionary["Media"]["Details"][self.Language.language_texts["status, title()"]]

			# Get the English watching status from the language status of the media details
			status = self.Get_Language_Status(language_status)

		# Update the number of medias inside the media type dictionary with the number of medias in the "Media titles" list
		media_type["JSON"]["Numbers"]["Total"] = len(media_type["JSON"]["Media titles"])

		# Sort the list of media titles
		media_type["JSON"]["Media titles"] = sorted(media_type["JSON"]["Media titles"], key = str.lower)

		# Define an empty list of media titles
		media_titles = []

		# If the "Media type" dictionary is not inside the parameter dictionary
		if "Media type" not in dictionary:
			# Then the parameter dictionary is a media type dictionary
			# Add the list of media titles from inside the media type "JSON" dictionary
			media_titles.extend(media_type["JSON"]["Media titles"])

		# If the "Media type" dictionary is inside the parameter dictionary
		# Then that means that we also have a "Media" dictionary inside it
		if "Media type" in dictionary:
			# Add the media title to the list of media titles
			media_titles.append(dictionary["Media"]["Title"])

		# Define the media information folder

		# Iterate through the list of English watching statuses
		for watching_status in self.texts["statuses, type: list"]["en"]:
			# Iterate through the list of media titles
			for media_title in media_titles:
				# Get the media folder
				folder = media_type["Folders"]["Media information"]["root"] + self.Sanitize_Title(media_title) + "/"

				# Get the media "Details.txt" file
				details_file = folder + self.Language.language_texts["details, title()"] + ".txt"

				# Get the media details dictionary
				details = self.File.Dictionary(details_file)

				# Get the language watching status of the media
				language_status = details[self.Language.language_texts["status, title()"]]

				# Get the English watching status from the language status
				status = self.Get_Language_Status(language_status)

				# If the media status is equal to the current watching status
				# And the media is not in the correct watching status list, add it to the list
				if (
					status == watching_status and
					media_title not in media_type["JSON"]["Statuses"][watching_status]
				):
					media_type["JSON"]["Statuses"][watching_status].append(media_title)

				# If the media status is not equal to the current watching status
				# And the media is in the wrong watching status list, remove it from the list
				if (
					status != watching_status and
					media_title in media_type["JSON"]["Statuses"][watching_status]
				):
					media_type["JSON"]["Statuses"][watching_status].remove(media_title)

			# Sort the list of media
			media_type["JSON"]["Statuses"][watching_status] = sorted(media_type["JSON"]["Statuses"][watching_status], key = str.lower)

		# Update the media type "Information.json" file
		self.JSON.Edit(media_type["Folders"]["Media information"]["Information"], media_type["JSON"])

		# Return the dictionary
		return dictionary

	def Parse_Link(self, link, id_parameter):
		# Define the dictionary of ID parameters to find the correct ID
		id_parameters_map = {
			"Playlist": "list", # For playlists
			"Video": "v", # For videos
			"Comment": "lc" # For comments
		}

		# If the "youtube" text is inside the link
		if "youtube" in link:
			# Import some useful functions from the "urllib.parse" module
			from urllib.parse import urlparse, parse_qs

			# Parse the link
			parsed_link = urlparse(link)

			# Get the query part of the URL
			query_string = parsed_link.query

			# Parse the query string into a dictionary
			url_parameters = parse_qs(query_string)

			# Get the correct key to extract the ID based on the type
			id_key = id_parameters_map[id_parameter]

			# Get the ID value from the parsed parameters
			id = url_parameters[id_key][0]

			# Return the ID
			return id

		else:
			# Return the original link
			return link

	def Get_YouTube_Information(self, item, link = None):
		# Define a root dictionary
		dictionary = {
			"Item": "",
			"Link": ""
		}

		# If the type of the item parameter is a dictionary
		if type(item) == dict:
			# Iterate through the list of keys to find the correct ID
			for key in ["ID", "Link"]:
				# If it is found, add it to the "Link" key
				if key in item:
					dictionary["Link"] = item[key]

			# Define the item as the "Item" key
			dictionary["Item"] = item["Item"]

			# Define a shortcut to the item
			item = dictionary["Item"]

		else:
			# Define the item as the item parameter
			dictionary["Item"] = item

			# Define the link as the link parameter
			dictionary["Link"] = link

		# Define the ID parameter as the normal item
		id_parameter = item

		# If the item is "Playlist videos"
		if item == "Playlist videos":
			# The ID parameter is "Playlist"
			id_parameter = "Playlist"

		# Parse the link to get the ID
		id = self.Parse_Link(dictionary["Link"], id_parameter)

		# Define the request dictionary with the item and ID
		request = {
			"Item": item,
			"ID": id
		}

		# If the item is "Comment"
		if item == "Comment":
			# Parse the link to get the video ID
			video_id = self.Parse_Link(dictionary["Link"], "Video")
		
			# Add the video ID to the request dictionary
			request["Video ID"] = video_id

		# Call the "Call" method of the "API" class to get the information about the item
		information = self.API.Call("YouTube", request)["Request"]["Dictionary"]

		# If the ID is inside the information dictionary
		if id in information:
			# Define the information as it
			information = information[id]

		# Return the information dictionary
		return information

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

	def Define_Title(self, titles, language = None, add_language = True, add_romanized = True, remove_colon = False):
		# If the language parameter is None
		if language == None:
			# Use the user language
			language = self.language["Small"]

		# Define the list of keys to search for the title
		keys = [
			"Original",
			language,
			"Romanized"
		]

		# If the "add language" parameter is False
		if add_language == False:
			keys.remove(language)

		# If the "add romanized" parameter is False
		if add_romanized == False:
			keys.remove("Romanized")

		# Iterate through the list of keys
		for key in keys:
			# If the key is inside the dictionary of titles
			if key in titles:
				# Define the title key as the current key
				title_key = key

		# Get the title from the dictionary of titles using the defined title key
		title = titles[title_key]

		# If the number of characters in the title is more than one
		# And the first two characters of the title are a colon and a space
		# And the "remove colon" parameter is True
		if (
			len(title) > 1 and
			title[0] + title[1] == ": " and
			remove_colon == True
		):
			# Remove the colon and a space
			title = title[2:]

		# Return the title
		return title

	def Define_Year_Summary_Data(self, entry, language):
		# Import the "Regex" module
		import re

		# Define an entry text initially as the media title in the parameter language
		entry_text = self.Define_Title(entry["Media titles"], language)

		# Add the ": " separator to the entry text if the media type is a video and the media is a video channel
		if entry["Media type"] == "Videos":
			entry_text += ": "

		# If the media type is not "Videos"
		else:
			# Only add a space to the entry text if there is a media item or an episode in the entry dictionary
			if (
				"Media item titles" in entry or
				"Episode" in entry
			):
				entry_text += " "

		# If there is a media item in the entry dictionary
		if "Media item titles" in entry:
			# Get the media item title in the parameter language
			media_item_title = self.Define_Title(entry["Media item titles"], language)

			# Add the media item title if it is not already present in the item text
			# And if the media type is not "Videos"
			# The medias that are video channels ("Videos" media type) do not add the media item (video series) to the entry text
			if (
				media_item_title not in entry_text and
				entry["Media type"] != "Videos"
			):
				# Define the default media item and episode separators as an empty string and a space
				media_item_separator = ""
				episode_separator = " "

				# Check if the "S[Any number two times]" text is found in the media item title with regex
				result = re.findall(r"S[0-9]{2}", media_item_title)

				# If the text is found in the media item title (a non-empty result)
				if result != []:
					# Define the episode separator as an empty string
					episode_separator = ""

				# If the text is not found in the media item title (an empty result)
				if result == []:
					# Define the media item separator as a dash and space
					media_item_separator = "- "

				# Define a switch to tell if the media item title will be added or not (default as True)
				add_media_item_title = True

				# If the "Episode" key is present in the entry dictionary
				if "Episode" in entry:
					# Get the episode title in the parameter language
					episode_title = self.Define_Title(entry["Episode"]["Titles"], language)

					# If the media item title is inside the episode title
					if media_item_title in episode_title:
						# Then do not add the media item title
						add_media_item_title = False

				# Add the media item title if the "add media item title" switch is True
				if add_media_item_title == True:
					# Add the media item separator to the entry text
					entry_text += media_item_separator

					# Add the media item title
					entry_text += media_item_title

					# Only add the episode separator if there is an episode
					if "Episode" in entry:
						entry_text += episode_separator

		# Add the episode if it exists
		if "Episode" in entry:
			# Add a space to the entry text if there is no media item in the entry dictionary
			# And if the last character of the entry text is not already a space
			if (
				"Media item titles" not in entry and
				entry_text[-1] != " "
			):
				entry_text += " "

			# Get the episode title title in the parameter language
			episode_title = self.Define_Title(entry["Episode"]["Titles"], language)

			# Add it to the entry text
			entry_text += episode_title

		# If the "States" dictionary is in the entry dictionary
		# And the "Re-watched" state is inside it
		if (
			"States" in entry and
			"Re-watched" in entry["States"]
		):
			# Add the "(Re-watched " text in the parameter language
			text = " (" + self.texts["re_watched, capitalize()"][language] + " "

			# Add the number of re-watched times plus "x" (the ex letter)
			text += str(entry["States"]["Re-watched"]["Times"]) + "x"

			# Add the closing parenthesis
			text += ")"

			# Add the defined re-watched text to the entry text
			entry_text += text

		# Get the date from the entry dictionary
		# The date is already in the "HH:MM DD/MM/YYYY" format required by the class which is going to use this method (the "Years" class)
		date = entry["Times"]["Finished watching"]

		# Add the date around parenthesis to the entry text
		entry_text += " (" + date + ")"

		# Return the entry text to the class which is going to use this method (the "Years" class)
		return entry_text

	def Define_Media_Item_Text(self, dictionary, media_episode_text = None):
		# Define a local version of the media dictionary for easier typing
		media = dictionary["Media"]

		# Define the local "of the" text for easier typing
		of_the_text = dictionary["Media type"]["Genders"][self.language["Small"]]["of_the"]

		# Define the list of "series types" texts
		series_types = [
			self.language_texts["season, title()"],
			self.language_texts["season, title()"].lower(),
			self.language_texts["serie, title()"],
			self.language_texts["serie, title()"].lower(),
			self.language_texts["video_series, type: singular"],
			self.language_texts["video_series, capitalize()"]
		]

		# If the media item type is inside that list
		if media["Item"]["Type"][self.language["Small"]] in series_types:
			# If the media does not have a list of media items
			# Or the media item is the root media
			if (
				media["States"]["Has a list of media items"] == False or
				media["States"]["The media item is the root media"] == True
			):
				# Define the "of the" text as the selected container "of the" text
				# (Selected means it maybe a normal or dubbed "of the container" text
				# "of the anime" or "of the dubbed anime")
				of_the_text = media["Texts"]["Selected container texts"]["Of the"]

			# If the media has a list of media items
			# And the media item is not the root media
			if (
				media["States"]["Has a list of media items"] == True and
				media["States"]["The media item is the root media"] == False
			):
				# Define the text as the media item text in the user language
				text = media["Texts"]["item"][self.language["Small"]].lower()

				# If the media episode text parameter is not None
				# And the text with a space on the beginning is not inside the media episode text
				if (
					media_episode_text != None and
					" " + text not in media_episode_text
				):
					# Add the text to the media episode text
					# Text will be one of:
					# " season"
					# " serie"
					# " video series"
					media_episode_text += " " + text

			# Define the gender as feminine
			gender = "feminine"

		# If the media item type is not inside the list of series types
		if media["Item"]["Type"][self.language["Small"]] not in series_types:
			# Define the "of the" text as the masculine "of the" text with the item type of the media item in the user language
			# 
			# Example:
			# "of the anime"
			of_the_text = self.media_types["Genders"][self.language["Small"]]["masculine"]["of_the"] + " "

			# Define a shortcut to the item type
			item_type = media["Item"]["Type"][self.language["Small"]].lower()

			# If the item type is inside the list of singular media types of the user language
			if media["Item"]["Type"][self.language["Small"]] in self.media_types["Singular"][self.language["Small"]]:
				# Change it to the container inside the "Selected container texts" dictionary
				# (Selected means it maybe a normal or dubbed container text
				# "anime" or "dubbed anime")
				item_type = media["Texts"]["Selected container texts"]["Container"]

			# Add the item type to the "of the" text
			of_the_text += item_type

			# Define the gender as feminine
			gender = "masculine"

		# If the media item is a single unit one
		if media["States"]["Single unit"] == True:
			# Define the "of the" text as the container "of the" text
			# 
			# Examples:
			# "of the anime"
			# "of the dubbed anime"
			# 
			# (Selected means it maybe a normal or dubbed "of the container" text
			# "of the anime" or "of the dubbed anime")
			of_the_text = media["Texts"]["Selected container texts"]["Of the"]

		# Return a list with the used variables
		return [
			of_the_text,
			media_episode_text,
			gender
		]

	def Show_Media_Information(self, dictionary):
		# Define a local version of the media dictionary for easier typing
		media = dictionary["Media"]

		# Define the singular media type variable for easier typing
		singular_media_type = dictionary["Media type"]["Singular"][self.language["Small"]]

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
			print("\t" + dictionary["Media type"]["Plural"][self.language["Small"]])

		# If the "Status change" key is inside the media dictionary
		if "Status change" in media:
			# Show the "Old watching staus" text in the user language
			print()
			print(self.language_texts["old_watching_status"] + ":")
			
			# Show the old watching status in the user language
			print("\t" + media["Status change"]["Old"])

			# Show the "New watching staus" text in the user language
			print()
			print(self.language_texts["new_watching_status"] + ":")
			
			# Show the new watching status in the user language
			print("\t" + media["Status change"]["New"])

		# If the user is not re-watching the media
		# And the user completed the media
		if (
			media["States"]["Re-watching"] == False and
			media["States"]["Completed media"] == True
		):
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

				# Replace the personal pronoun "I" for the personal pronoun "you" to personalize the message for the user
				# Both for "started" and "finished"
				text = text.replace(self.Language.language_texts["when_i_started"], self.Language.language_texts["when_you_started"])
				text = text.replace(self.Language.language_texts["when_i_finished"], self.Language.language_texts["when_you_finished"])

				# Show the finished watching text
				print()
				print(text)

		# Show the media episode title if the media is a series media (not a movie)
		if media["States"]["Series media"] == True:
			# If the media item is not the media (not the same title as the media)
			if media["States"]["The media item is the root media"] == False:
				# Define the "of the" text as the "of the" text in the feminine gender
				dictionary["Media type"]["Genders"][self.language["Small"]]["of_the"] = self.media_types["Genders"][self.language["Small"]]["feminine"]["of_the"]

				# Show the "season"/"series" text
				print()
				print(self.Text.Capitalize(media["Texts"]["item"][self.language["Small"]]) + ":")

				# Show the title of the media
				self.Show_Media_Title(dictionary, is_media_item = True)

			# Define the unit text variable for easier typing
			unit_text = self.Text.Capitalize(media["Texts"]["unit"][self.language["Small"]])

			# If the media item is a single unit one
			if media["States"]["Single unit"] == True:
				# Define the unit text as the media item type text
				unit_text = media["Item"]["Type"][self.language["Small"]]

			# Define the media episode text as the unit text plus the " {}" format text
			media_episode_text = unit_text + " {}"

			# Define the "of the" text with the "Define_Media_Item_Text" method
			result = self.Define_Media_Item_Text(dictionary, media_episode_text)

			# Get the variables from it
			of_the_text = result[0]
			media_episode_text = result[1]

			# Format the media episode text with the defined "of the" text
			media_episode_text = media_episode_text.format(of_the_text)

			# Define the episode title as the episode title
			# (May or may not be in the user language)
			title = media["Episode"]["Title"]

			# If the language of the media is not the user language
			if media["Language"] != self.language["Small"]:
				# Define the episode title as the episode title in the user language
				title = media["Episode"]["Titles"][self.language["Small"]]

			# If the user is re-watching the media
			if media["States"]["Re-watching"] == True:
				# Add the re-watched text to the episode title
				title += media["Episode"]["Re-watching"]["Texts"]["Number"][self.language["Small"]]

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
				text_to_show += self.Text.Capitalize(media["Texts"]["unit"][self.language["Small"]])

			# If the media item is a single unit one
			else:
				# Add the item type of the media item in the user language
				# 
				# Example:
				# Special
				text_to_show += media["Item"]["Type"][self.language["Small"]].lower()

			# Format the text template with the "the" container text of the media and add the text to show
			# 
			# Examples:
			# Episode of the anime
			# Episode of the dubbed anime
			# 
			# (Selected means it maybe a normal or dubbed "the container" text
			# "the anime" or "the dubbed anime")
			text_to_show = self.Text.Capitalize(text_to_show) + " " + template.format(media["Texts"]["Selected container texts"]["The"])

			# If the media has a list of media items
			# And the media item is not the media
			# And the media is not a video channel
			# And the media item is not a single unit one
			# And the "Replace title" state is False
			if (
				media["States"]["Has a list of media items"] == True and
				media["States"]["The media item is the root media"] == False and
				media["States"]["Video"] == False and
				self.language_texts["single_unit"] not in media["Item"]["Details"] and
				media["States"]["Replace title"] == False
			):
				# Define a shortcut for the media item type text
				item_type_text = media["Texts"]["item"][self.language["Small"]]

				# If the media item type text is not inside the defined list
				if item_type_text not in ["OVA", "ONA"]:
					# Make it lowercase
					item_type_text = item_type_text.lower()

				# Define the media episode text as the media unit text with the "with_{}" formatted with the media item text
				media_episode_text = self.Text.Capitalize(media["Texts"]["unit"][self.language["Small"]]) + " " + self.Language.language_texts["with_{}"].format(item_type_text)

				# Show the media episode text with the media item text (item type)
				# 
				# Example:
				# "Episode with season:"
				print()
				print(media_episode_text + ":")

				# Define the media episode title with the media item text in the user language
				title = media["Episode"]["with_item"][self.language["Small"]]

				# If the user is re-watching the media
				if media["States"]["Re-watching"] == True:
					# Add the re-watching text to the episode title
					title += media["Episode"]["Re-watching"]["Texts"]["Number"][self.language["Small"]]

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
				text_to_show += " " + self.Language.language_texts["and"] + " " + item_type_text

				# Define the key as "with_title_and_item" to show the media title, media item title, and the episode title
				key = "with_title_and_item"

			# If the media has no media item list
			# Or the media item is the media
			# Or the media is a video channel
			# Or the media item is a single unit
			# Or the "Replace title" state is True
			if (
				media["States"]["Has a list of media items"] == False or
				media["States"]["The media item is the root media"] == True or
				media["States"]["Video"] == True or
				self.language_texts["single_unit"] in media["Item"]["Details"] or
				media["States"]["Replace title"] == True
			):
				# Define the key as "with_title" to show only the media title and episode title
				key = "with_title"

			# Define the media episode title as the episode title with the correct key, in the user language
			title = media["Episode"][key][self.language["Small"]]

			# If the user is re-watching the media
			if media["States"]["Re-watching"] == True:
				# Add the re-watched text to the episode title
				title += media["Episode"]["Re-watching"]["Texts"]["Number"][self.language["Small"]]

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

		# Check if the "Entry" and "Times" keys are in the dictionary
		if (
			"Entry" in dictionary and
			"Times" in dictionary["Entry"]
		):
			# Define a local (re)watching text
			watching_text = " " + media["Texts"]["Watching"][self.language["Small"]]

			# Define a local "the unit" text
			the_unit_text = " " + media["Texts"]["the_unit"][self.language["Small"]]

			# Iterate over the time types "started" and "finished"
			for time_key in ["started", "finished"]:
				# Construct the display text dynamically, e.g. "when_you_started" or "when_you_finished"
				text = self.Language.language_texts["when_you_" + time_key] + watching_text + the_unit_text

				# Format the dictionary key to match the stored time entries, e.g. "Started watching"
				time_key = time_key.capitalize() + " watching"

				# Print the composed text and the corresponding formatted time
				print()
				print(text + ":")
				print("\t" + dictionary["Entry"]["Times"][time_key]["Formats"]["HH:MM DD/MM/YYYY"])

			# Show the watching session duration text in the user language
			print()
			print(self.language_texts["watching_session_duration"] + ":")
			print("\t" + dictionary["Entry"]["Times"]["Watching session duration"]["Text"][self.language["Small"]])

		# If the "Unit" key is inside the "Epsiode" dictionary
		if "Unit" in media["Episode"]:
			# Show the media unit text and the episode unit
			print()
			print(self.language_texts["media_unit"] + ":")
			print("\t" + media["Episode"]["Unit"])

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
			# You finished watching [this item] [of the container text] "[media title in the user language]"
			# 
			# Example:
			# You finished watching this season of the anime "Sword Art Online"
			# 
			# (Selected means it maybe a normal or dubbed "of the container" text
			# "of the anime" or "of the dubbed anime")
			this_item_text = media["Texts"]["this_item"][self.language["Small"]]
			of_the_container_text = media["Texts"]["Selected container texts"]["Of the"]
			media_title = media["Titles"]["Language"]

			text_to_show = self.language_texts["you_finished_watching"] + " " + this_item_text + " " + of_the_container_text + ' "' + media_title + '"'

			# If the media has a list of media items
			# And the media item is the media (same title as the root media)
			if (
				media["States"]["Has a list of media items"] == True and
				media["States"]["The media item is the root media"] == True
			):
				# Define the text to show as:
				# "You finished watching [this container]"
				# 
				# Example:
				# "You finished watching this anime"
				text_to_show = self.language_texts["you_finished_watching"] + " " + media["Texts"]["this_container"][self.language["Small"]]

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

				# Replace the personal pronoun "I" for the personal pronoun "you" to personalize the message for the user
				# Both for "started" and "finished"
				text = text.replace(self.Language.language_texts["when_i_started"], self.Language.language_texts["when_you_started"])
				text = text.replace(self.Language.language_texts["when_i_finished"], self.Language.language_texts["when_you_finished"])

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
				item_type = media["Item"]["Next"]["Type"][self.language["Small"]]

				# Define the local text as the "Next {} to watch" text in the feminine version
				text = self.language_texts["next_{}_to_watch, feminine"]

				# Define the list of season and series item types
				series_types = [
					self.texts["season, title()"][self.language["Small"]].lower(),
					self.texts["series"][self.language["Small"]]
				]

				# If the item type is not inside that list, define the text as its masculine version
				if item_type not in series_types:
					text = self.language_texts["next_{}_to_watch, masculine"]

				# Show an empty line and the text
				print()
				print(text.format(item_type.lower()) + ":")

				# Define a dictionary with the next media item titles, states, and text
				media_dictionary = {
					"Media": {
						"Item": {
							"Titles": media["Item"]["Next"]["Titles"]
						}
					}
				}

				# Show the next media item title
				self.Show_Media_Title(media_dictionary, is_media_item = True)

		# If the "ID" key is inside the "Episode" dictionary
		if "ID" in media["Episode"]:
			# Show the "Remote origin" text and the remote origin
			print()
			print(self.Language.language_texts["remote_origin"] + ":")
			print("\t" + media["Episode"]["Remote"]["Title"])

			# Define a shortcut for the "Episode ID" and "Episode link" texts
			episode_id_text = self.language_texts["episode_id"]
			episode_link_text = self.language_texts["episode_link"]

			# If the media is a video channel
			if media["States"]["Video"] == True:
				# Define a shortcut for the "Episode" text by language (uppercase for English, lowercase for other languages)
				episode_text = self.Language.language_texts["episode, by language"]

				# Replace the "Episode" text with the "Video" text by language (uppercase for English, lowercase for other languages)
				# In both the local episode ID and episode link texts
				episode_id_text = episode_id_text.replace(episode_text, self.Language.language_texts["video, by language"])
				episode_link_text = episode_link_text.replace(episode_text, self.Language.language_texts["video, by language"])

			# Show the "ID" text and the epsiode ID
			print()
			print(episode_id_text + ":")
			print("\t" + media["Episode"]["ID"])

			# Show the "Episode link" text and the episode link
			print()
			print(episode_link_text + ":")
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
			print(text.format(media["Texts"]["unit"][self.language["Small"]]) + ": ")
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
					print("\t" + self.dictionary["States"]["Texts"][key][self.language["Small"]])

			# If this is the first media the user watches in the year
			if media["States"]["First entry in year"] == True:
				# Define the container text for easier typing
				container = media["Texts"]["container"][self.language["Small"]]

				# If the media is not a video channel, make the container lowercase
				if media["States"]["Video"] == False:
					container = container.lower()

				# Define the list of items to use to format the text
				items = [
					self.media_types["Genders"][self.language["Small"]]["feminine"]["this"].title(),
					self.media_types["Genders"][self.language["Small"]]["feminine"]["the"] + " " + self.media_types["Genders"][self.language["Small"]]["feminine"]["first"] + " " + self.Language.language_texts["media, title()"].lower()
				]

				# Add the "in" text in the masculine gender and the current year number
				items.append(self.Language.language_texts["genders, type: dictionary, masculine"]["in"] + " " + self.current_year["Number"])

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
				container = media["Texts"]["container"][self.language["Small"]]

				# If the media is a video channel, make the container lowercase
				if media["States"]["Video"] == False:
					container = container.lower()

				# If the media is a series media (not a movie)
				if media["States"]["Series media"] == True:
					# Define the container text as the "[unit] of [container]"
					# 
					# Example:
					# "Episode of anime"
					container = media["Texts"]["unit"][self.language["Small"]] + " " + self.Language.language_texts["of, neutral"] + " " + container

				# If this is not the first media the user watches in the year
				if media["States"]["First entry in year"] == False:
					# If the media is a video channel, make the container lowercase
					if media["States"]["Video"] == False:
						container = container.lower()

					# Define a shortcut for the words dictionary
					words = dictionary["Media type"]["Genders"][self.language["Small"]]

					# Define the list of items to use to format the text
					items = [
						words["this"].title(),
						words["the"] + " " + words["first"] + " " + container
					]

					# Re-define the words shortcut
					words = self.Language.language_texts["genders, type: dictionary, masculine"]

					# If the media unit is "episode"
					if media["Texts"]["unit"]["en"] == "episode":
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
					text = self.Language.language_texts["and_also"].capitalize() + " " + dictionary["Media type"]["Genders"][self.language["Small"]]["the"] + " " + dictionary["Media type"]["Genders"][self.language["Small"]]["first"] + " " + container

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
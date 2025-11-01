# Convert_History.py

# Import the root "Watch_History" class
from Watch_History.Watch_History import Watch_History as Watch_History

# Import the "importlib" module
import importlib

# Import the "deepcopy" module from the "copy" module
from copy import deepcopy

# Import the regex module
import re

class Convert_History(Watch_History):
	def __init__(self):
		# Import the root "Watch_History" class to import its variables and methods
		super().__init__()

		# Show a five dash space separator
		print()
		print(self.separators["5"])
		print()

		# Show the "Convert history" text in the user language
		print(self.Language.language_texts["convert_history"] + ":")

		# Create the states dictionary
		self.states = {
			"Verbose": {
				"JSON": True,
				"Text": True,
				"Full verbose": False
			},
			"Wait for input": False
		}

		# If the "Testing" switch is True
		if self.switches["Testing"] == True:
			# Change the "JSON" and "Text" states to False
			self.states["Verbose"]["JSON"] = False
			self.states["Verbose"]["Text"] = False

			# Define a local "skip input" switch
			skip_input = False

			# If the "skip input" switch is False
			if skip_input == False:
				# Change the "Wait for input" state to True
				self.states["Wait for input"] = True

		# Create the years dictionary
		self.Create_Years_Dictionary()

		# Create the medias dictionary
		self.Create_Medias_Dictionary()

		# Iterate through the year dictionary
		self.Iterate_Through_The_Year_Dictionary()

	def Create_Years_Dictionary(self):
		# Create a list of years starting from the starting year (the default is 2018) to the current year
		years_list = self.Date.Create_Years_List()

		# Create the years dictionary
		self.years = {
			"Numbers": {
				"Total": len(years_list) # The total number of years
			},
			"Settings": {}, # A dictionary for year settings
			"List": years_list, # The list of years
			"Dictionary": {} # The years dictionary
		}

		# Iterate through the list of years
		for year_number in self.years["List"]:
			# Define the year dictionary with its keys and values
			year = {
				"Number": str(year_number),
				"Folders": {
					"Watch History": {
						"root": "",
						"Entries": "",
						"Entry list": ""
					},
					"Watch History (by media type)": {
						"root": ""
					},
					"Year": {
						"Watched media": {},
						"Firsts of the Year": {}
					}
				},
				"Watch History": {
					"Entries": {
						"Original": {},
						"Updated": {
							"Numbers": {},
							"Entries": [],
							"Dictionary": {}
						}
					},
					"Entry list": {
						"Original": [],
						"Updated": []
					}
				},
				"Watch History (by media type)": {}
			}

			# ---------- #

			# Watch History folders and files

			# Define the "Watch History" root folder
			year["Folders"]["Watch History"]["root"] = self.folders["Watch History"]["root"] + str(year_number) + "/"

			# Define a shortcut to the Watch History folder
			watch_history_folders = year["Folders"]["Watch History"]

			# ----- #

			# Define the Watch History "Entries.json" file
			watch_history_folders["Entries"] = watch_history_folders["root"] + "Entries.json"

			# Get the JSON dictionary from the file
			dictionary = self.JSON.To_Python(watch_history_folders["Entries"])

			# Copy the "Numbers" dictionary of the "Original" dictionary to the "Updated" dictionary
			year["Watch History"]["Entries"]["Updated"]["Numbers"] = dictionary["Numbers"]

			# Define the original "Entries" dictionary as the JSON dictionary of the file
			year["Watch History"]["Entries"]["Original"] = dictionary

			# ----- #

			# Define the Watch History "Entry list.txt" file
			watch_history_folders["Entry list"] = watch_history_folders["root"] + "Entry list.txt"

			# Read the file to get the file lines
			lines = self.File.Contents(watch_history_folders["Entry list"])["Lines"]

			# Add the text lines to the "Original" key of the Watch History "Entry list" dictionary
			year["Watch History"]["Entry list"]["Original"] = lines

			# ----- #

			# Define the "By media type" root folder
			year["Folders"]["Watch History (by media type)"]["root"] = watch_history_folders["root"] + "By media type/"

			# Define a shortcut to the by media type folder
			by_media_type = year["Folders"]["Watch History (by media type)"]

			# ---------- #

			# Watch History (by media type) folders and files

			# Iterate through the English plural media types list
			for plural_media_type in self.media_types["Plural"]["en"]:
				# Get the root media type dictionary
				root_media_type = self.media_types[plural_media_type]

				# Define the media type dictionary
				media_type = {
					"Media type": root_media_type["Plural"],
					"Folders": {
						"root": by_media_type["root"] + plural_media_type + "/"
					}
				}

				# Define a shortcut to the media type folders
				media_type_folders = media_type["Folders"]

				# Define the media type dictionary inside the "Watch History (by media type)" key
				year["Watch History (by media type)"][plural_media_type] = {
					"Entries": {
						"Original": {},
						"Updated": {
							"Numbers": {},
							"Entries": [],
							"Dictionary": {}
						}
					},
					"Entry list": {
						"Original": [],
						"Updated": []
					}
				}

				# ----- #

				# Define the media type "Entries.json" file
				media_type_folders["Entries"] = media_type_folders["root"] + "Entries.json"

				# Get the JSON dictionary from the file
				dictionary = self.JSON.To_Python(media_type_folders["Entries"])

				# Copy the "Numbers" dictionary of the "Original" dictionary to the "Updated" dictionary
				year["Watch History (by media type)"][plural_media_type]["Entries"]["Updated"]["Numbers"] = dictionary["Numbers"]

				# Define the original media type "Entries" dictionary as the JSON dictionary of the file
				year["Watch History (by media type)"][plural_media_type]["Entries"]["Original"] = dictionary

				# ----- #

				# Define the media type "Entry list.txt" file
				media_type_folders["Entry list"] = media_type_folders["root"] + "Entry list.txt"

				# Read the file to get the file lines
				lines = self.File.Contents(media_type_folders["Entry list"])["Lines"]

				# Define the original media type "Entry list" list as the file lines
				year["Watch History (by media type)"][plural_media_type]["Entry list"]["Original"] = lines

				# ----- #

				# Define the "Files" folder
				media_type_folders["Files"] = {
					"root": media_type_folders["root"] + "Files/"
				}

				# Add the media type dictionary to the "Watch History (by media type)" dictionary
				year["Folders"]["Watch History (by media type)"][plural_media_type] = media_type

			# ---------- #

			# Year folders

			# Iterate through the list of folder types
			for folder_type in ["Watched media", "Firsts of the Year"]:
				# Get the folder dictionary of the folder type
				dictionary = year["Folders"]["Year"][folder_type]

				# Iterate through the list of small languages
				for language in self.languages["Small"]:
					# If the language folder key does not exist, create it
					if language not in dictionary:
						dictionary[language] = {}

					# Get the root year folders dictionary from the "Years" module
					year_folders = self.Years.years["Dictionary"][year_number]["Folders"]

					# Define a shortcut for the [folder type] folder
					folder = year_folders[language][folder_type]

					# If the folder type is "Watched media"
					if folder_type == "Watched media":
						# Iterate through the English plural media types list
						for plural_media_type in self.media_types["Plural"]["en"]:
							# Get the root media type dictionary
							root_media_type = self.media_types[plural_media_type]

							# Get the language media type for the current language
							language_media_type = root_media_type["Plural"][language]

							# Define the folder
							folder[plural_media_type] = {
								"root": folder["root"] + language_media_type + "/"
							}

					# If the folder type is "Firsts of the Year"
					if folder_type == "Firsts of the Year":
						# Define the sub-folder name as the "Media" text in the current language
						sub_folder_name = self.Language.texts["media, title()"][language]

						# Define the folder as the root "Firsts of the Year" plus the sub-folder
						folder = {
							"root": folder["root"] + sub_folder_name + "/"
						}

						# Create the folder
						self.Folder.Create(folder["root"])

					# Add the [folder type] folder to the local folder dictionary
					dictionary[language] = folder

			# ---------- #

			# Add the local year dictionary to the root years dictionary
			self.years["Dictionary"][year_number] = year

			# ---------- #

			# Create a "Year.json" file to store the year dictionary
			year_file = year["Folders"]["Watch History"]["root"] + "Year.json"
			self.File.Create(year_file)

			# Write the year dictionary into the "Year.json" file
			self.JSON.Edit(year_file, year, verbose = self.states["Verbose"]["JSON"])

	def Create_Medias_Dictionary(self):
		# Define the root medias dictionary
		self.medias = {
			"Numbers": {
				"Total": 0
			},
			"List": [],
			"Dictionary": {}
		}

	def Iterate_Through_The_Year_Dictionary(self):
		# Iterate through the Watch History entries to update the:
		# 
		# Root:
		# [X] - "Entries.json" file
		# [X] - "Entry list.txt" file
		# 
		# Media type:
		# [X] - "Entries.json" file
		# [X] - "Entry list.txt" file
		# [X] - Entry text files
		#
		# Year:
		# [X] - "Watched media" entry text files
		# [X] - "Firsts of the Year" entry text files

		# Iterate through the medias inside the root medias dictionary:
		# 
		# For medias with no media items, update the "Watched":
		# [X] - Root media "Entries.json" file
		# [X] - Root media "Entry list.txt" file
		# [X] - Root media entry text files
		# 
		# For medias with media items, update the "Watched":
		# [X] - Media item "Entries.json" file
		# [X] - Media item "Entry list.txt" file
		# [X] - Media item entry text files
		# (For all media items of the root media)

		# For the JSON files:
		# [X] - Fix the first entry in the "Entries" list of the "Entries.json" files, which is incorrect (usually the last entry)
		# And fill the "Dictionary" dictionary in the "Entries.json" files which is empty

		# For the entry text files:
		# 
		# [X] - Change the entry text to this order:
		# Watched media number:
		# [Watched media number]
		# 
		# Watched media number by media type:
		# [Watched media number by media type]
		# 
		# Media type:
		# [Media type]
		# 
		# Entry:
		# [Watched media number. Media type (Finished watching time)]
		#
		# Media titles:
		# [Media titles]
		# 
		# (
		# Media item titles:
		# [Item titles]
		# 
		# Episode titles:
		# [Episode titles]
		# )
		# 
		# When I finished watching:
		# [Finished watching time in the local timezone]
		# 
		# When I finished watching (UTC):
		# [Finished watching time in the UTC time]
		# 
		# (
		# States:
		# [State texts]
		# )
		# 
		# [X] - Adjust entry times in the user's timezone, accounting for the UTC offset during Brazilian Daylight Saving Time (DST):
		# DST started in Brazil at: 21:00 04/11/2018
		# And ended at: 21:00 17/02/2019
		# -
		# - Update the entry names (which contain the user's timezone entry times) in these places:
		# 
		# - Entry text files (to update the "Entry" and "When I finished watching" texts):
		# - Media type entry text files
		# - Year "Watched media" entry text files
		# - Year "Firsts of the Year" entry text files
		# - For medias with no media items, update the "Watched" root media entry text files
		# - For medias with media items, update the "Watched" media item entry text files (for all media items of the root media)
		# 
		# - "Entries.json" files (to update the entry name in the "Entries" list and "Dictionary" dictionary)
		# - Root "Entries.json" file
		# - Media type "Entries.json" file
		# - For medias with no media items, update the "Watched" root media "Entries.json" file
		# - For medias with media items, update the "Watched" media item "Entries.json" file (for all media items of the root media)
		# 
		# - "Entry list.txt" files (to update the entry name)
		# - Root "Entry list.txt" file
		# - Media type "Entry list.txt" file
		# - For medias with no media items, update the "Watched" root media "Entry list.txt" file
		# - For medias with media items, update the "Watched" media item "Entry list.txt" file (for all media items of the root media)
		# 
		# [X] - Fix incorrect singular or plural texts inside the entry text
		# 
		# [X] - Update the files using the "Update_Entry_Text" method
		# And also rename the files using the "Move" method of the "self.File" class

		# Todo:
		# Check all the checkboxes, then test the class

		# ---------- #

		# Define a custom settings dictionary (for the user to change)
		custom_settings = {
			"Skip": { # Define a skip dictionary for years where to skip the year, input, or entries
				"Year": [
					#"2018",
					#"2019",
					#"2020",
					#"2021",
					#"2022",
					#"2023",
					#"2024",
					#"2025"
				],
				"Input": [
					"2018",
					"2019",
					"2020",
					"2021",
					"2022",
					"2023",
					"2024",
					"2025"
				],
				"Entries": {
					"2018": 0,
					"2019": 0,
					"2020": 0,
					"2021": 0,
					"2022": 0,
					"2023": 0,
					"2024": 0,
					"2025": 0
				}
			}
		}

		# Iterate through the list of years
		for year_number in self.years["List"]:
			# Create the settings dictionary for the year
			settings = {
				"Year": str(year_number),
				"Skip": {
					"Year": False,
					"Input": False,
					"Entries": {
						"Number": 0
					}
				}
			}

			# If the year is inside the skip "Year" list of the custom settings dictionary
			if year_number in custom_settings["Skip"]["Year"]:
				# Change the skip "Year" setting to True (to skip the year)
				settings["Skip"]["Year"] = True

			# If the year is inside the skip "Input" list of the custom settings dictionary
			if year_number in custom_settings["Skip"]["Input"]:
				# Change the skip "Input" setting to True (to skip the pause between years)
				settings["Skip"]["Input"] = True

			# If the year key inside the skip "Entries" dictionary of the custom settings dictionary is not zero
			if custom_settings["Skip"]["Entries"][year_number] != 0:
				# Change the number of entries to skip as the number inside the "Entries" dictionary
				settings["Skip"]["Entries"]["Number"] = custom_settings["Skip"]["Entries"][year_number]

			# If the "Testing" switch is disabled
			if self.switches["Testing"] == False:
				# Change the skip "Year" setting to False (to not skip the year)
				settings["Skip"]["Year"] = False

				# Change the skip "Input" setting to True (to skip the pause between years)
				settings["Skip"]["Input"] = True

				# Define the number of entries to skip as zero
				settings["Skip"]["Entries"]["Number"] = 0

			# Add the year settings dictionary to the root "Settings" dictionary
			self.years["Settings"][year_number] = settings

		# ---------- #

		# Initialize the index of the current year, starting at one
		current_year_index = 1

		# Get a copy of the list of years
		years_list = self.years["List"].copy()

		# Iterate through the list of years
		for year_number in self.years["List"]:
			# Get the settings dictionary for the year
			year_settings = self.years["Settings"][year_number]

			# If the skip "Year" setting is True
			if year_settings["Skip"]["Year"] == True:
				# Remove the year from the local list of years
				years_list.remove(year_number)

		# Get the number of years
		number_of_years = str(len(years_list))

		# Get the last year
		last_year = years_list[-1]

		# Iterate through the local list of years
		for year_number in years_list:
			# Get the year dictionary
			year = self.years["Dictionary"][year_number]

			# ---------- #

			# Define the year information text
			year_information = f"""
			{self.separators["10"]}

			{self.Date.language_texts["number_of_the_year"]}:
			[{current_year_index}/{number_of_years}]

			{self.Date.language_texts["year"].title()}:
			[{year_number}/{last_year}]""".replace("\t", "")

			# ---------- #

			# Get the settings dictionary for the year
			year_settings = self.years["Settings"][year_number]

			# ---------- #

			# Define a shortcut to the Watch History folders dictinary
			watch_history_folders = year["Folders"]["Watch History"]

			# ----- #

			# Define a shortcut to the root "Entries.json" file of the current year
			entries_file = watch_history_folders["Entries"]

			# Define a shortcut the root original "Entries" dictionary of the current year
			entries = year["Watch History"]["Entries"]["Original"]

			# Define a shortcut the root updated "Entries" dictionary of the current year
			updated_entries = year["Watch History"]["Entries"]["Updated"]

			# ----- #

			# Define a shortcut to the root "Entry list.txt" file of the current year
			entry_list_file = watch_history_folders["Entry list"]

			# Define a shortcut the root original "Entry list" list of the current year
			entry_list = year["Watch History"]["Entry list"]["Original"]

			# Define a shortcut the root updated "Entry list" list of the current year
			updated_entry_list = year["Watch History"]["Entry list"]["Updated"]

			# ----- #

			# Define a local entry number as one
			entry_number = 1

			# Get the number of entries
			number_of_entries = str(len(entries["Entries"]))

			# Get the list of entry keys
			entry_keys = list(entries["Dictionary"].keys())

			# If the number of entries to skip inside the year settings dictionary is not zero
			if year_settings["Skip"]["Entries"]["Number"] != 0:
				# Define an entry number to count the entries
				e = 0

				# While the entry number is lesser than the number of entries to skip
				# And the number of keys inside the list of entry keys is not zero
				while (
					e < year_settings["Skip"]["Entries"]["Number"] and
					len(entry_keys) != 0
				):
					# Remove the first entry from the list of keys
					entry_keys.pop(0)

					# Add one to the entry number
					e += 1

				# Get the number number of entries
				new_number_of_entries = str(len(entry_keys))

			# Iterate through the entry names in the list of entry keys
			for entry_name in entry_keys:
				# Get the entry dictionary
				entry = entries["Dictionary"][entry_name]

				# Define the entry number to show
				entry_number_to_show = str(entry_number) + "/" + str(number_of_entries)

				# If the number of entries to skip inside the year settings dictionary is not zero
				if year_settings["Skip"]["Entries"]["Number"] != 0:
					# Update the entry number to show to add the correct entry number
					entry_number_to_show = str(entry["Watched media number"]) + "/" + str(number_of_entries)

				# Define an entry information text
				entry_information = year_information + "\n" + \
				f"""
				{self.Language.language_texts["number_of_the_entry"]}:
				[{entry_number_to_show}]"""

				# If the number of entries to skip inside the year settings dictionary is not zero
				if year_settings["Skip"]["Entries"]["Number"] != 0:
					# Add the number of the iteration
					entry_information = entry_information + f"""
					
					{self.Language.language_texts["number_of_the_iteration"]}:
					[{entry_number}/{new_number_of_entries}]"""

				# Add the entry name
				entry_information = (entry_information + f"""
				
				{self.Language.language_texts["entry_name"]}:
				[{entry_name}]""".replace("\t", "")).replace("\t", "")

				# ----- #

				# Get the media type of the entry
				plural_media_type = entry["Media type"]

				# Get the root media type dictionary
				root_media_type = self.media_types[plural_media_type]

				# Get the language media type for the user language
				language_media_type = root_media_type["Plural"][self.language["Small"]]

				# Add the media type to the entry information text
				entry_information += f"""
				
				{self.language_texts["media_type"]}:
				[{language_media_type}]""".replace("\t", "")

				# ----- #

				# Get the "Watch History (by media type)" dictionary of the current media type
				media_type_dictionary = year["Watch History (by media type)"][plural_media_type]

				# Define a shortcut the media type "Entries" dictionary of the current year
				media_type_entries = media_type_dictionary["Entries"]

				# Define a shortcut the media type "Entry list" dictionary of the current year
				media_type_entry_list = media_type_dictionary["Entry list"]

				# ----- #

				# Define a shortcut to the media type folders
				media_type_folders = year["Folders"]["Watch History (by media type)"][plural_media_type]["Folders"]

				# Get the media type "Media information" folder
				media_information_folder = root_media_type["Folders"]["Media information"]

				# ----- #

				# Define a shortcut to the media titles dictionary
				media_titles = entry["Media titles"]

				# Get the original media title
				media_title = self.Define_Title(media_titles, add_language = False)

				# Get the language media title
				language_media_title = self.Define_Title(media_titles)

				# If the media type is "Movies"
				# And the media title is not inside the list of movie titles
				if (
					plural_media_type == "Movies" and
					media_title not in root_media_type["JSON"]["Media titles"]
				):
					# Get the original title
					media_title = self.Define_Title(media_titles, add_language = False, add_romanized = False)

					# Get the original title
					language_media_title = self.Define_Title(media_titles, add_language = False, add_romanized = False)

				# Add the media title to the entry information text
				entry_information += f"""
				
				{self.language_texts["media_title"]}:
				[{language_media_title}]""".replace("\t", "")

				# ----- #

				# Define a template dictionary to use as a base to store the entries and entry lists
				template_dictionary = {
					"Entries": {
						"Original": {},
						"Updated": {
							"Numbers": {},
							"Entries": [],
							"Dictionary": {}
						}
					},
					"Entry list": {
						"Original": [],
						"Updated": []
					}
				}

				# If the media title is not in the media dictionary
				if media_title not in self.medias["List"]:
					# Define the media dictionary
					media = {
						"Title": media_title,
						"Titles": media_titles,
						"Root dictionary": {},
						"Folders": {
							"root": "",
							"Watched": {
								"root": "",
								"Entries": "",
								"Entry list": "",
								"Files": {
									"root": ""
								}
							},
							"Watched (media items)": {}
						},
						"Watched": {},
						"Watched (media items)": {}
					}

					# ----- #

					# Define the root media dictionary with the media type and the media
					media["Root dictionary"] = {
						"Media type": root_media_type,
						"Media": {
							"Title": media_title
						}
					}

					# Define the media item title as initially the media title
					media_item_title = media["Title"]

					# Select the media and define its variables, returning the media dictionary (without asking the user to select the media)
					media["Root dictionary"] = self.Select_Media(media["Root dictionary"])

					# Define a shortcut to the media dictionary
					root_media_dictionary = media["Root dictionary"]["Media"]

					# ----- #

					# Import the root folder
					media["Folders"]["root"] = root_media_dictionary["Folders"]["root"]

					# ----- #

					# If the media does not have a media item list
					if root_media_dictionary["States"]["Has a list of media items"] == False:
						# Define a shortcut to the root media "Watched" folder
						watched_folder = root_media_dictionary["Folders"]["Watched"]

						# Import the "Watched" folders and files
						media["Folders"]["Watched"]["root"] = watched_folder["root"]
						media["Folders"]["Watched"]["Entries"] = watched_folder["entries"]
						media["Folders"]["Watched"]["Entry list"] = watched_folder["entry_list"]
						media["Folders"]["Watched"]["Files"] = watched_folder["files"]

						# ----- #

						# Define the original "Watched" dictionary as a copy of the template dictionary
						media["Watched"] = deepcopy(template_dictionary)

						# Get the JSON dictionary from the watched "Entries.json" file
						dictionary = self.JSON.To_Python(media["Folders"]["Watched"]["Entries"])

						# Copy the "Numbers" dictionary of the "Original" dictionary to the "Updated" dictionary
						media["Watched"]["Entries"]["Updated"]["Numbers"] = dictionary["Numbers"]

						# Define the original watched "Entries" dictionary as the JSON dictionary of the file
						media["Watched"]["Entries"]["Original"] = dictionary

						# ----- #

						# Read the watched "Entry file.txt" file to get the file lines
						lines = self.File.Contents(media["Folders"]["Watched"]["Entry list"])["Lines"]

						# Add the text lines to the "Original" key of the watched "Entry list" dictionary
						media["Watched"]["Entry list"]["Original"] = lines

					# Add the media to the list of media
					self.medias["List"].append(media_title)

					# Update the number of medias in the list
					self.medias["Numbers"]["Total"] = len(self.medias["List"])

					# ----- #

					# Add the media dictionary to the dictionary of medias
					self.medias["Dictionary"][media_title] = media

				# ----- #

				# If the media title is in the list of media
				if media_title in self.medias["List"]:
					# Get the media dictionary
					media = self.medias["Dictionary"][media_title]

					# Define a shortcut to the media dictionary
					root_media_dictionary = media["Root dictionary"]["Media"]

				# If the media does not have a media item list
				if root_media_dictionary["States"]["Has a list of media items"] == False:
					# Define a shortcut to the titles
					titles = root_media_dictionary["Titles"]

					# Get the list of title keys for the media
					title_keys = list(titles.keys())

					# Define a list of keys to remove
					to_remove = [
						"Language",
						"Sanitized"
					]

					# Remove the keys
					for key in to_remove:
						if key in title_keys:
							title_keys.remove(key)

					# Iterate through the media titles inside the "Titles" list
					for title_key in title_keys:
						# Get the title
						title = titles[title_key]

						# If the title is not inside the "Media titles" dictionary as a key
						# And it is not inside the "Media titles" dictionary as a value
						if (
							title_key not in entry["Media titles"] and
							title not in list(entry["Media titles"].values())
						):
							# Add it
							entry["Media titles"][title_key] = title

				# ----- #

				# Define a "added a new media item title" switch as False by default
				added_a_new_media_item_title = False

				# If the "Media item titles" key is in the entry dictionary
				# Or the media has a media item list
				# And the "Media item titles" key is not in the entry dictionary
				# (That means the media item is the root media)
				if (
					"Media item titles" in entry or
					root_media_dictionary["States"]["Has a list of media items"] == True and
					"Media item titles" not in entry
				):
					# Define the titles key as "Media item titles"
					titles_key = "Media item titles"

					# If the media has a list of media items
					# And the "Media item titles" key is not in the entry dictionary
					if (
						root_media_dictionary["States"]["Has a list of media items"] == True and
						"Media item titles" not in entry
					):
						# Define the titles key as "Media titles"
						titles_key = "Media titles"

					# Get the media item title
					media_item_title = self.Define_Title(entry[titles_key], add_language = False)

					# Get the language media item title
					language_media_item_title = self.Define_Title(entry[titles_key])

					# Add the media item title to the entry information text
					entry_information += f"""
					
					{self.language_texts["media_item_title"]}:
					[{language_media_item_title}]""".replace("\t", "")

					# Define an empty new media item title
					new_media_item_title = ""

					# If the media item is not in the "Watched (media items)" dictionary
					if media_item_title not in media["Watched (media items)"]:
						# Update the root media dictionary to define the media item inside it
						media["Root dictionary"] = self.Define_Media_Item(media["Root dictionary"], media_item = media_item_title)

						# ----- #

						# Define a shortcut to the root media dictionary
						root_media_dictionary = media["Root dictionary"]["Media"]

						# Define a shortcut to the media item dictionary
						media_item = root_media_dictionary["Item"]

						# ----- #

						# Define a shortcut to the media item "Watched" folder
						watched_folder = media_item["Folders"]["Watched"]

						# Define the media item folders dictionary by copying the keys from the original dictionary and converting them to title case
						media["Folders"]["Watched (media items)"][media_item_title] = {
							"root": watched_folder["root"],
							"Entries": watched_folder["entries"],
							"Entry list": watched_folder["entry_list"],
							"Files": watched_folder["files"]
						}

						# ----- #

						# Define the media item "Watched" dictionary as a copy of the template dictionary
						media["Watched (media items)"][media_item_title] = deepcopy(template_dictionary)

						# Get the JSON dictionary from the watched media item "Entries.json" file
						dictionary = self.JSON.To_Python(media["Folders"]["Watched (media items)"][media_item_title]["Entries"])

						# Copy the "Numbers" dictionary of the "Original" dictionary to the "Updated" dictionary
						media["Watched (media items)"][media_item_title]["Entries"]["Updated"]["Numbers"] = dictionary["Numbers"]

						# Define the original watched "Entries" dictionary as the JSON dictionary of the file
						media["Watched (media items)"][media_item_title]["Entries"]["Original"] = dictionary

						# ----- #

						# Read the watched media item "Entry file.txt" file to get the file lines
						lines = self.File.Contents(media["Folders"]["Watched (media items)"][media_item_title]["Entry list"])["Lines"]

						# Add the text lines to the "Original" key of the watched "Entry list" dictionary
						media["Watched (media items)"][media_item_title]["Entry list"]["Original"] = lines

						# Define a shortcut to the titles
						titles = media_item["Titles"]

						# Get the list of title keys for the media item
						title_keys = list(titles.keys())

						# Define a list of keys to remove
						to_remove = [
							"Language",
							"ja",
							"Sanitized"
						]

						# Remove the keys
						for key in to_remove:
							if key in title_keys:
								title_keys.remove(key)

						# Iterate through the media titles inside the "Titles" list
						for title_key in title_keys:
							# Get the title
							title = titles[title_key]

							# If the title is not inside the [titles key] dictionary as a key
							# And it is not inside the [titles key] dictionary as a value
							if (
								title_key not in entry[titles_key] and
								title not in list(entry[titles_key].values())
							):
								# Add it
								entry[titles_key][title_key] = title

								# Define the new media item title as it
								new_media_item_title = title

								# Switch the "added a new media item title" switch to True
								added_a_new_media_item_title = True

						# Add the media dictionary to the media "Watched (media items)" dictionary
						media["Watched (media items)"][media_item_title]["Root dictionary"] = deepcopy(media["Root dictionary"])

					# If the media item is in the "Watched (media items)" dictionary
					if media_item_title in media["Watched (media items)"]:
						# Get the root dictionary
						root_dictionary = media["Watched (media items)"][media_item_title]["Root dictionary"]

						# Define a shortcut to the media dictionary
						root_media_dictionary = root_dictionary["Media"]

						# Define a shortcut to the media item dictionary
						media_item = root_media_dictionary["Item"]

						# Define a shortcut to the titles
						titles = media_item["Titles"]

						# Get the list of title keys for the media item
						title_keys = list(titles.keys())

						# Define a list of keys to remove
						to_remove = [
							"Language",
							"ja",
							"Sanitized"
						]

						# Remove the keys
						for key in to_remove:
							if key in title_keys:
								title_keys.remove(key)

						# Define the titles key as "Media item titles"
						titles_key = "Media item titles"

						# If the media has a list of media items
						# And the "Media item titles" key is not in the entry dictionary
						# (That means the media item is the root media)
						if (
							root_media_dictionary["States"]["Has a list of media items"] == True and
							"Media item titles" not in entry
						):
							# Define the titles key as "Media titles"
							titles_key = "Media titles"

						# Iterate through the media titles inside the "Titles" list
						for title_key in title_keys:
							# Get the title
							title = titles[title_key]

							# If the title is not inside the [titles key] dictionary as a key
							# And it is not inside the [titles key] dictionary as a value
							if (
								title_key not in entry[titles_key] and
								title not in list(entry[titles_key].values())
							):
								# Add it
								entry[titles_key][title_key] = title

								# Define the new media item title as it
								new_media_item_title = title

								# Switch the "added a new media item title" switch to True
								added_a_new_media_item_title = True

					# If the new media item title is not empty
					if new_media_item_title != "":
						# Add the new media item title to the entry information text
						entry_information += f"""
						
						{self.language_texts["new_media_item_title_added"]}:
						[{new_media_item_title}]""".replace("\t", "")

					# ----- #

					# Update the media dictionary in the dictionary of medias
					self.medias["Dictionary"][media_title] = media

				# ----- #

				# Get the watched media number
				watched_media_number = entry["Watched media number"]

				# ----- #

				# Get the finished watching time
				entry_time = entry["Times"]["Finished watching"]

				# Define the old entry time as a backup
				old_entry_time = entry["Entry"].split("(")[1].split(")")[0]

				# Get the UTC time
				utc_time = entry["Times"]["Finished watching (UTC)"]

				# Define a date dictionary based on the UTC time
				date = self.Date.From_String(utc_time)

				# Define a default new entry time as the original one by default
				new_entry_time = entry_time

				# If the original entry time is not just the year (four digits)
				if len(entry_time) != 4:
					# Get the new finished watching time (in the user timezone)
					new_entry_time = date["Timezone"]["DateTime"]["Formats"]["HH:MM DD/MM/YYYY"]

				# Update the "Finished watching" key with the new entry time
				entry["Times"]["Finished watching"] = new_entry_time

				# ----- #

				# Define a dictionary of entry names
				entry_names = {
					"Original": {
						"Normal": {},
						"Sanitized": {}
					},
					"Updated": {
						"Normal": {},
						"Sanitized": {}
					}
				}

				# Iterate through the list of entry name keys
				for key in entry_names:
					# Define a local shortcut to the original entry time
					local_entry_time = entry_time

					# If the key is "Updated"
					if key == "Updated":
						# Define the local entry time as the new entry time
						local_entry_time = new_entry_time

					# Define a local entry name template with the watched media number and the correct entry time
					template = str(watched_media_number) + ". {} (" + local_entry_time + ")"

					# Iterate through the list of small languages
					for language in self.languages["Small"]:
						# Create the normal entry name by formating the template with the plural media type in the current language
						entry_names[key]["Normal"][language] = template.format(root_media_type["Plural"][language])

						# Define the sanitized version of it
						entry_names[key]["Sanitized"][language] = entry_names[key]["Normal"][language].replace(":", ";").replace("/", "-")

				# ----- #

				# Iterate through the Watch History entries to update the:
				# 
				# Root:
				# - "Entries.json" file
				# - "Entry list.txt" file

				# ----- #

				# Define a shortcut to the updated entry name
				updated_entry_name = entry_names["Updated"]["Normal"]

				# Define an "updated entry time" switch as False by default
				updated_entry_time = False

				# If the "Entry" key is not the same as the updated entry name in English
				if entry["Entry"] != updated_entry_name["en"]:
					# Update the "Entry" key with the updated entry name
					entry["Entry"] = updated_entry_name["en"]

					# Then the entry time was updated, switch the "updated entry time" switch to True
					updated_entry_time = True

				# If the UTC time is not equal to the new entry time
				if utc_time != new_entry_time:
					# Add the UTC entry time to the entry information text
					entry_information += f"""
					
					{self.Language.language_texts["entry_time_in_utc"]}:
					[{utc_time}]""".replace("\t", "")

				# If the original finished watching time is not the same as the new one
				# Or the entry time was updated
				if (
					entry_time != new_entry_time or
					updated_entry_time == True
				):
					# Add the original, new, and UTC entry time to the entry information text
					entry_information += f"""
					
					{self.Language.language_texts["original_entry_time"]}:
					[{old_entry_time}]

					{self.Language.language_texts["new_entry_time"]}:
					[{new_entry_time}]""".replace("\t", "")

					# Then the entry time was updated, switch the "updated entry time" switch to True
					updated_entry_time = True

				# Else
				else:
					# Add entry time to the entry information text
					entry_information += f"""
					
					{self.Language.language_texts["entry_time"]}:
					[{entry_time}]""".replace("\t", "")

				# ----- #

				# Show the entry information text
				print(entry_information)

				# ----- #

				# Define a "added season ordinal number" switch as False by default
				added_season_ordinal_number = False

				# If the "Media item titles" key is in the entry dictionary
				# Or the media does has a media item list
				# And the "The media item is the root media" state is True
				# (That means the media item is the root media)
				if (
					"Media item titles" in entry or
					(
						root_media_dictionary["States"]["Has a list of media items"] == True and
						root_media_dictionary["States"]["The media item is the root media"] == True
					)
				):
					# Define the titles key as "Media item titles"
					titles_key = "Media item titles"

					# If the "The media item is the root media" state is True
					# (That means the media item is the root media)
					if root_media_dictionary["States"]["The media item is the root media"] == True:
						# Define the titles key as "Media titles"
						titles_key = "Media titles"

					# Search for the "First" to "Eleventh" season text in the media item title
					match = re.search(r"S(0[1-9]|1[0-1])", entry[titles_key]["Original"])

					# If it is found
					if match:
						# Get the season number
						season_number = int(match.group(1))

						# Get the ordinal number for the season in the Portuguese language
						ordinal_title = self.Date.texts["ordinal_numbers, type: list"]["pt"]["feminine"][season_number - 1]

						# Get the season text
						season_text = self.texts["season, title()"]["pt"]

						# If the "pt" key is not already inside the [titles key] dictionary
						if "pt" not in entry[titles_key]:
							# Add the season title in Portuguese to the [titles key] dictionary
							entry[titles_key]["pt"] = ordinal_title.title() + " " + season_text

							# Switch the "added season ordinal number" switch to True
							added_season_ordinal_number = True

					# Check for the "2nd" or "3rd" season text in the media item title
					match = re.search(r"(2nd|2nd Season|3rd|3rd Season)", entry[titles_key]["Original"])

					# If it is found
					if match:
						# Define a "add season" switch as False by default
						add_season = False

						# If the season text is inside the first match group
						if " Season" in match.group(0):
							# Switch the "add season" switch to True
							add_season = True

						# Check if the "2nd" text is found
						if match.group(0) == "2nd":
							season_number = 2

						# Check if the "3rd" text is found
						elif match.group(0) == "3rd":
							season_number = 3

						# Get the ordinal number for the season in the Portuguese language
						ordinal_title = self.Date.texts["ordinal_numbers, type: list"]["pt"]["feminine"][season_number - 1]

						# Define the season text as empty by default
						season_text = ""

						# If the "add season" switch is True
						if add_season == True:
							# Get the season text and add a space to the start
							season_text = " " + self.texts["season, title()"]["pt"]

						# If the "pt" key is not already inside the "Media item titles" dictionary
						if "pt" not in entry[titles_key]:
							# Add the season title in Portuguese to the "Media item titles" dictionary
							entry[titles_key]["pt"] = ordinal_title.title() + season_text

							# Switch the "added season ordinal number" switch to True
							added_season_ordinal_number = True

				# ----- #

				# [X] - Adjust entry times in the user's timezone, accounting for the UTC offset during Brazilian Daylight Saving Time (DST):
				# DST started in Brazil at: 21:00 04/11/2018
				# And ended at: 21:00 17/02/2019
				# 
				# Update the entry names (which contain the user's timezone entry times) in the:
				# Root "Entries.json" file (to update the entry name in the "Entries" list and "Dictionary" dictionary)

				# Add the updated entry name to the "Entries" list of the updated Watch History "Entries" dictionary
				updated_entries["Entries"].append(updated_entry_name["en"])

				# Add the entry dictionary to the "Dictionary" dictionary of the updated Watch History "Entries" dictionary
				updated_entries["Dictionary"][updated_entry_name["en"]] = entry

				# If the "Episode" key is inside the entry dictionary
				if "Episode" in entry:
					# Define a "titles are the same" switch as False by default
					titles_are_the_same = False

					# Define a dictionary of dictionaries to store the dictionaries
					dictionaries = {}

					# Get the list of titles
					titles = entry["Episode"]["Titles"]

					# If the English title is the same as the Portuguese time
					if titles["en"] == titles["pt"]:
						# Store the dictionary
						dictionaries["Watch History"] = entry

						# Switch the "titles are the same" switch to True
						titles_are_the_same = True

					# Define the media type "Watched" entry dictionary as an empty dictionary
					media_type_entry_dictionary = {}

					# Define a shortcut to the original dictionary
					original_dictionary = media_type_entries["Original"]["Dictionary"]

					# If the entry name key is inside the original "Entries" dictionary
					if entry_name in original_dictionary:
						# Get the media type entry dictionary
						media_type_entry_dictionary = original_dictionary[entry_name]

					# If the updated entry name key is inside the original "Entries" dictionary
					if updated_entry_name["en"] in original_dictionary:
						# Get the media type entry dictionary
						media_type_entry_dictionary = original_dictionary[updated_entry_name["en"]]

					# If the media type entry dictionary is not empty
					if media_type_entry_dictionary != {}:
						# Get the list of titles
						titles = media_type_entry_dictionary["Episode"]["Titles"]

						# If the English title is the same as the Portuguese time
						if titles["en"] == titles["pt"]:
							# Store the dictionary
							dictionaries["Watch History (by media type)"] = media_type_entry_dictionary

							# Switch the "titles are the same" switch to True
							titles_are_the_same = True

					# If the media does not have a media item list
					if root_media_dictionary["States"]["Has a list of media items"] == False:
						# Define the media item "Watched" entry dictionary as an empty dictionary
						watched_entry_dictionary = {}

						# Define a shortcut to the original dictionary
						original_dictionary = media["Watched"]["Entries"]["Original"]["Dictionary"]

						# If the entry name key is inside the original "Entries" dictionary
						if entry_name in original_dictionary:
							# Get the media item "Watched" entry dictionary
							watched_entry_dictionary = original_dictionary[entry_name]

						# If the updated entry name key is inside the original "Entries" dictionary
						if updated_entry_name["en"] in original_dictionary:
							# Get the media item "Watched" entry dictionary
							watched_entry_dictionary = original_dictionary[updated_entry_name["en"]]

						# If the media "Watched" entry dictionary is not empty
						if watched_entry_dictionary != {}:
							# Get the list of titles
							titles = watched_entry_dictionary["Episode"]["Titles"]

							# If the English title is the same as the Portuguese time
							if titles["en"] == titles["pt"]:
								# Store the dictionary
								dictionaries["Media"] = watched_entry_dictionary

								# Switch the "titles are the same" switch to True
								titles_are_the_same = True

					# If the "Media item titles" key is in the entry dictionary
					# Or the media does has a media item list
					# And the "The media item is the root media" state is True
					# (That means the media item is the root media)
					if (
						"Media item titles" in entry or
						(
							root_media_dictionary["States"]["Has a list of media items"] == True and
							root_media_dictionary["States"]["The media item is the root media"] == True
						)
					):
						# Define the media item "Watched" entry dictionary as an empty dictionary
						watched_entry_dictionary = {}

						# Define a shortcut to the original dictionary
						original_dictionary = media["Watched (media items)"][media_item_title]["Entries"]["Original"]["Dictionary"]

						# If the entry name key is inside the original "Entries" dictionary
						if entry_name in original_dictionary:
							# Get the media item "Watched" entry dictionary
							watched_entry_dictionary = original_dictionary[entry_name]

						# If the updated entry name key is inside the original "Entries" dictionary
						if updated_entry_name["en"] in original_dictionary:
							# Get the media item "Watched" entry dictionary
							watched_entry_dictionary = original_dictionary[updated_entry_name["en"]]

						# If the media item "Watched" entry dictionary is not empty
						if watched_entry_dictionary != {}:
							# Get the list of titles
							titles = watched_entry_dictionary["Episode"]["Titles"]

							# If the English title is the same as the Portuguese time
							if titles["en"] == titles["pt"]:
								# Store the dictionary
								dictionaries["Media item"] = watched_entry_dictionary

								# Switch the "titles are the same" switch to True
								titles_are_the_same = True

					# If the "titles are the same" switch is True
					# And the English title is not inside the defined list
					# And the "SIMULACRA" text is not inside the English title
					# And the "CUBE ESCAPE" text is not inside the English title
					# And the "Dr. Stone" text is not inside the media title
					if (
						titles_are_the_same == True and
						titles["en"] not in [
							"EP07 \"VIPS\"",
							"EP13 \"X = Ben + 2\"",
							"EP01(14) \"Happy Party!\"",
							"EP02(15) \"BLACK SHOUT\"",
							"EP03(16) \"Sing Girls\"",
							"EP05(18) \"Rainy Ring-Dong-Dance\"",
							"EP06(19) \"You Only Live Once\"",
							"EP10(23) \"R·I·O·T\"",
							"EP12(25) \"Returns\"",
							"EP13(26) \"Kizuna Music♪\"",
							"EP05(21) \"PoPi-V!\"",
							"EP86 \"Erza Vs. Erza\"",
							"EP07(122) \"Stradivarius\"",
							"EP11(96) \"New World\"",
							"EP95 \"Lisanna\"",
							"EP12 \"Eromanga Festival\"",
							"EP100 \"Mest!\"",
							"EP04 \"Let's Cheer UP!\"",
							"Izzy Box [Anthology 7.05]",
							"GRIS",
							"Ping!",
							"MINECRAFT 2016",
							"POKEMON GO",
							"300"
						] and
						"SIMULACRA" not in titles["en"] and
						"CUBE ESCAPE" not in titles["en"] and
						"pony.lol" not in titles["en"] and 
						"Dr. Stone" not in media_title and
						"GameBlaster 38" not in media_title
					):
						# Show the dictionaries
						for dictionary_key, dictionary in dictionaries.items():
							print()
							print(dictionary_key + " dictionary:")

							self.JSON.Show(dictionary)

						# Ask for user input before continuing
						self.Input.Type()

				# --- #

				# [X] - Adjust entry times in the user's timezone, accounting for the UTC offset during Brazilian Daylight Saving Time (DST):
				# DST started in Brazil at: 21:00 04/11/2018
				# And ended at: 21:00 17/02/2019
				# 
				# Update the entry names (which contain the user's timezone entry times) in the:
				# Root "Entry list.txt" file (to update the entry name)

				# Add the updated entry name to the updated Watch History "Entry list" list
				updated_entry_list.append(updated_entry_name["en"])

				# ----- #

				# Iterate through the Watch History entries to update the:
				# 
				# Media type:
				# - "Entries.json" file
				# - "Entry list.txt" file

				# [X] - Adjust entry times in the user's timezone, accounting for the UTC offset during Brazilian Daylight Saving Time (DST):
				# DST started in Brazil at: 21:00 04/11/2018
				# And ended at: 21:00 17/02/2019
				# 
				# Update the entry names (which contain the user's timezone entry times) in the:
				# Media type "Entries.json" file (to update the entry name in the "Entries" list and "Dictionary" dictionary)

				# Add the updated entry name to the "Entries" list of the updated media type "Entries" dictionary
				media_type_entries["Updated"]["Entries"].append(updated_entry_name["en"])

				# Add the entry dictionary to the "Dictionary" dictionary of the updated media type "Entries" dictionary
				media_type_entries["Updated"]["Dictionary"][updated_entry_name["en"]] = entry

				# --- #

				# [X] - Adjust entry times in the user's timezone, accounting for the UTC offset during Brazilian Daylight Saving Time (DST):
				# DST started in Brazil at: 21:00 04/11/2018
				# And ended at: 21:00 17/02/2019
				# 
				# Update the entry names (which contain the user's timezone entry times) in the:
				# Media type "Entry list.txt" file (to update the entry name)

				# Add the updated entry name to the updated media type "Entry list" list
				media_type_entry_list["Updated"].append(updated_entry_name["en"])

				# ----- #

				# Iterate through the medias inside the root medias dictionary:
				# 
				# For medias with no media items, update the "Watched":
				# - Root media "Entries.json" file
				# - Root media "Entry list.txt" file

				# [X] - Adjust entry times in the user's timezone, accounting for the UTC offset during Brazilian Daylight Saving Time (DST):
				# DST started in Brazil at: 21:00 04/11/2018
				# And ended at: 21:00 17/02/2019
				# 
				# Update the entry names (which contain the user's timezone entry times):
				# - For medias with no media items, update the "Watched":
				# - Root media "Entries.json" file (to update the entry name in the "Entries" list and "Dictionary" dictionary)
				# - Root media "Entry list.txt" file (to update the entry name)

				# If the media does not have a media item list
				if root_media_dictionary["States"]["Has a list of media items"] == False:
					# Add the updated entry name to the "Entries" list of the updated watched "Entries" dictionary
					media["Watched"]["Entries"]["Updated"]["Entries"].append(updated_entry_name["en"])

					# Add the entry dictionary to the "Dictionary" dictionary of the updated watched "Entries" dictionary
					media["Watched"]["Entries"]["Updated"]["Dictionary"][updated_entry_name["en"]] = entry

					# --- #

					# Add the updated entry name to the updated watched "Entry list" list
					media["Watched"]["Entry list"]["Updated"].append(updated_entry_name["en"])

				# ----- #

				# Iterate through the medias inside the root medias dictionary:
				# 
				# For medias with media items, update the "Watched":
				# - Media item "Entries.json" file
				# - Media item "Entry list.txt" file

				# [X] - Adjust entry times in the user's timezone, accounting for the UTC offset during Brazilian Daylight Saving Time (DST):
				# DST started in Brazil at: 21:00 04/11/2018
				# And ended at: 21:00 17/02/2019
				# 
				# Update the entry names (which contain the user's timezone entry times):
				# - For medias with media items, update the "Watched":
				# - Media item "Entries.json" file (to update the entry name in the "Entries" list and "Dictionary" dictionary)
				# - Media item "Entry list.txt" file (to update the entry name)
				# (For all media items of the root media)

				# If the "Media item titles" key is in the entry dictionary
				# Or the media does has a media item list
				# And the "The media item is the root media" state is True
				# (That means the media item is the root media)
				if (
					"Media item titles" in entry or
					(
						root_media_dictionary["States"]["Has a list of media items"] == True and
						root_media_dictionary["States"]["The media item is the root media"] == True
					)
				):
					# Add the updated entry name to the "Entries" list of the updated media item watched "Entries" dictionary
					media["Watched (media items)"][media_item_title]["Entries"]["Updated"]["Entries"].append(updated_entry_name["en"])

					# Add the entry dictionary to the "Dictionary" dictionary of the updated media item watched "Entries" dictionary
					media["Watched (media items)"][media_item_title]["Entries"]["Updated"]["Dictionary"][updated_entry_name["en"]] = entry

					# --- #

					# Add the updated entry name to the updated media item watched "Entry list" list
					media["Watched (media items)"][media_item_title]["Entry list"]["Updated"].append(updated_entry_name["en"])

				# ----- #

				# Iterate through the Watch History entries to update the:
				# 
				# Watch History (by media type) entry text files
				#
				# Year:
				# - "Watched media" entry text files
				# - "Firsts of the Year" entry text files
				# 
				# For medias with no media items, update the "Watched":
				# - Root media entry text files
				# 
				# For medias with media items, update the "Watched":
				# - Media item entry text files

				# [X] - Adjust entry times in the user's timezone, accounting for the UTC offset during Brazilian Daylight Saving Time (DST):
				# DST started in Brazil at: 21:00 04/11/2018
				# And ended at: 21:00 17/02/2019
				# 
				# Update the entry names (which contain the user's timezone entry times) in the:
				# Entry text files (to update the "Entry" and "When I finished watching" texts):
				# - Media type entry text files
				# - Year "Watched media" entry text files
				# - Year "Firsts of the Year" entry text files
				# - For medias with no media items, update the "Watched" root media entry text files
				# - For medias with media items, update the "Watched" media item entry text files (for all media items of the root media)
				# (And also rename the file to update the entry time in the file name)

				# Define a dictionary of entry files to update
				entry_files = {
					"Watch History (by media type)": {},
					"Watched media (Português)": {},
					"Watched media (English)": {},
					"Firsts of the Year (Português)": {},
					"Firsts of the Year (English)": {},
					"Watched": {},
					"Watched (media item)": {}
				}

				# Define the "Watch History (by media type)" entry file dictionary
				# With the updated entry name as a file name
				entry_files["Watch History (by media type)"] = {
					"File key text": self.language_texts["entry_file_in_the_watch_history_by_media_type_folder"],
					"Text language": self.language["Small"],
					"File name language": "en",
					"Folder": media_type_folders["Files"]["root"],
					"File": media_type_folders["Files"]["root"] + entry_names["Updated"]["Sanitized"]["en"] + ".txt"
				}

				# Iterate through the language keys and dictionaries
				for small_language, language in self.languages["Dictionary"].items():
					# Define a shortcut to the full language
					full_language = language["Full"]

					# Define a shortcut to the folder
					folder = year["Folders"]["Year"]["Watched media"][small_language][plural_media_type]["root"]

					# Define the language "Watched media" entry file dictionary
					# With the updated entry name as a file name
					entry_files["Watched media ({})".format(full_language)] = {
						"File key text": self.language_texts["entry_file_in_the_watched_media_folder_by_year"],
						"Text language": small_language,
						"File name language": small_language,
						"Folder": folder,
						"File": folder + entry_names["Updated"]["Sanitized"][small_language] + ".txt"
					}

					# If the watched media is the first one in the year
					if watched_media_number == 1:
						# Define a shortcut to the folder
						folder = year["Folders"]["Year"]["Firsts of the Year"][small_language]["root"]

						# Define the language "Firsts of the Year" entry file dictionary
						# With the updated entry name as a file name
						entry_files["Firsts of the Year ({})".format(full_language)] = {
							"File key text": self.Language.language_texts["entry_file_in_the_firsts_of_the_year_folder_by_year"],
							"Text language": small_language,
							"Folder": folder,
							"File name language": small_language,
							"File": folder + entry_names["Updated"]["Sanitized"][small_language] + ".txt"
						}

				# ----- #

				# If the media does not have a media item list
				if root_media_dictionary["States"]["Has a list of media items"] == False:
					# Define a shortcut to the watched "Files" folder
					folder = media["Folders"]["Watched"]["Files"]["root"]

					# Define the media "Watched" entry file
					entry_files["Watched"] = {
						"File key text": self.language_texts["entry_file_in_the_watched_folder_of_a_media_without_media_items"],
						"Text language": self.language["Small"],
						"File name language": self.language["Small"],
						"Folder": folder,
						"File": folder + entry_names["Updated"]["Sanitized"][self.language["Small"]] + ".txt"
					}

				# ----- #

				# If the "Media item titles" key is in the entry dictionary
				# Or the media does has a media item list
				# And the "The media item is the root media" state is True
				# (That means the media item is the root media)
				if (
					"Media item titles" in entry or
					(
						root_media_dictionary["States"]["Has a list of media items"] == True and
						root_media_dictionary["States"]["The media item is the root media"] == True
					)
				):
					# Define a shortcut to the folder
					folder = media["Folders"]["Watched (media items)"][media_item_title]["Files"]["root"]

					# Define the media item "Watched" entry file
					entry_files["Watched (media item)"] = {
						"File key text": self.language_texts["entry_file_in_the_watched_folder_of_a_media_item"],
						"Text language": self.language["Small"],
						"File name language": self.language["Small"],
						"Folder": folder,
						"File": folder + entry_names["Updated"]["Sanitized"][self.language["Small"]] + ".txt"
					}

				# ----- #

				# Define a "shown files" switch as False by default
				shown_files = False

				# Define a "renamed file" switch as False by default
				renamed_file = False

				# Define a list of added notices
				# (When entry file conditions are met, they are added here)
				added_notices = []

				# Define the notices text
				notices_text = ""

				# Define a list of updated files
				updated_files = []

				# Define the updated files text
				updated_files_text = ""

				# Iterate through the dictionary of entry text files
				for key, dictionary in entry_files.items():
					# If the dictionary is not empty
					if dictionary != {}:
						# Get the text language
						text_language = dictionary["Text language"]

						# Get the file
						entry_file = dictionary["File"]

						# Define a shortcut to the folder
						folder = dictionary["Folder"]

						# Get the file name language
						file_name_language = dictionary["File name language"]

						# Define the old file with the original entry name
						old_file = folder + entry_names["Original"]["Sanitized"][file_name_language] + ".txt"

						# Define the new file with the updated entry name
						new_file = folder + entry_names["Updated"]["Sanitized"][file_name_language] + ".txt"

						# If the new file does not exist
						if self.File.Exists(new_file) == False:
							# Rename the file
							self.File.Move(old_file, new_file)

							# Switch the "renamed file" switch to True
							renamed_file = True

						# Update the entry file
						entry_file = new_file

						# If the "Testing" switch is enabled
						if self.switches["Testing"] == True:
							# Define the entry file as the old file for the verbose text to be shown
							entry_file = old_file

						# Get the file text contents
						contents = self.File.Contents(entry_file)

						# Define a dictionary of files to show
						files = {
							"File": entry_file,

							# Format the file to show to the user (make it clickable in a better console, like ConEmu)
							"File link": self.Language.language_texts["file_format, type: format"].format(entry_file.replace(" ", "%20"))
						}

						# Update the entry text to fix some wrong texts
						# Passing the entry dictionary, the file text contents, and the text language as method parameters
						# And getting back the updated entry text
						entry_text = self.Update_Entry_Text(entry, contents, text_language)

						# Define a dictionary of conditions
						conditions = {
							"The file text is different than the updated entry text, the file will be updated": \
							contents["String"] != entry_text,

							"The old entry time was wrong and will be updated": \
							(
								entry_time != new_entry_time or
								updated_entry_time == True
							),

							"The entry file was renamed": \
							renamed_file == True,

							"The season ordinal number was added": \
							added_season_ordinal_number == True,

							"A new media item title was added to the entry files and JSON files": \
							added_a_new_media_item_title == True,

							"The entry file does not exist": \
							self.File.Exists(entry_file) == False
						}

						# Define a list of language texts dictionaries to search through
						texts_dictionaries = [
							self.language_texts,
							self.Language.language_texts,
							self.File.language_texts
						]

						# If any of the conditions are met
						# And the "Notices" text is not inside the list of added notices
						if (
							any(conditions.values()) and
							"Notices" not in added_notices
						):
							# Add the notices text to the notices text
							notices_text += f"""
							
							{self.Language.language_texts["notices, title()"]}:""".replace("\t", "")

							# Add the "Notices" text to the list of added notices
							added_notices.append("Notices")

						# If the file text is different than the updated entry text
						# And the "Updated files" text is not inside the list of added notices
						if (
							contents["String"] != entry_text and
							"Updated files" not in updated_files
						):
							# Add the updated files text to the updated files text string
							updated_files_text += f"""
							
							{self.Language.language_texts["updated_files"]}:""".replace("\t", "")

							# Add the "Updated files" text to the list of updated files
							updated_files.append("Updated files")

						# Iterate through the dictionary of conditions
						for condition_key, condition in conditions.items():
							# Check if the condition is met
							if condition:
								# Make a text key with the condition key
								text_key = condition_key.lower().replace(" ", "_").replace(",", "")

								# Iterate through the list of language texts dictionaries
								for text_dictionary in texts_dictionaries:
									# If the text key is inside the current text dictionary
									if text_key in text_dictionary:
										# Define it as the local language texts dictionary
										language_texts = text_dictionary

								# Get a language text for the condition
								language_text = language_texts[text_key]

								# If the condition is not inside the list of added notices
								if condition_key not in added_notices:
									# Add the language text to the notices text
									notices_text += f"""
									[{language_text}]""".replace("\t", "")

								# If the "updated entry text" is inside the condition key
								if "updated entry text" in condition_key:
									# Show a ten dash space separator
									print()
									print(self.separators["10"])
									print()

									# Show the language text of the condition
									print(language_text + ".")
									print()

									# Show the files
									for file_key, file in files.items():
										# If the file key is "File"
										if file_key == "File":
											# Define the text as the "File" text
											text = self.File.language_texts["file, title()"]

										# If the file key is "File link"
										if file_key == "File link":
											# Define the text as the "File link" text
											text = self.File.language_texts["file_link"]

										# Show the text and the file
										print(text + ":")
										print(file)
										print()

									# Show the "Updated entry text" text and the entry text
									print(self.Language.language_texts["updated_entry_text"] + ":")
									print("[" + entry_text + "]")

								# If the file key is not inside the list of updated files
								if key not in updated_files:
									# Add it to the list of updated files
									updated_files.append(key)

									# Get the file key text
									file_key_text = dictionary["File key text"]

									# Get the "in language" text for the file name language
									in_language = self.Language.texts["in_[language]"][file_name_language][self.language["Small"]]

									# Add it to the file key text
									file_key_text += " " + in_language

									# If the file key text is not in the updated files text
									if file_key_text not in updated_files_text:
										# Add the file key text to the updated files text
										updated_files_text += f"""
										[{file_key_text}]""".replace("\t", "")

								# Add the condition to the list of added notices
								added_notices.append(condition_key)

								# Switch the "shown files" switch to True
								shown_files = True

						# Write the updated entry text into the entry file
						self.File.Edit(entry_file, entry_text, "w")

				# If the updated files text is not empty
				if updated_files_text != "":
					# Add it to the entry information text
					entry_information += updated_files_text

				# If the notices text is not empty
				if notices_text != "":
					# Add it to the entry information text
					entry_information += notices_text

				# Show the entry information text again, as the entry files and entry text are very big texts
				print(entry_information)

				# If the "Testing" switch is enabled
				# And the "Skip input" year setting is False
				# And the current entry is not the last one in the list
				# And the "shown files" switch is True
				if (
					self.switches["Testing"] == True and
					year_settings["Skip"]["Input"] == False and
					entry_name != entries["Entries"][-1] and
					shown_files == True
				):
					# Define the next text
					next_text = self.Language.language_texts["next, feminine"] + " " + self.Language.language_texts["entry"]

					# Format it
					next_text = " ({})".format(next_text.lower())

					# Ask the user to press Enter to advance to the next entry
					self.Input.Type(self.Language.language_texts["continue, title()"] + next_text)

				# ----- #

				# Increment the entry number by one
				entry_number += 1

			# ---------- #

			# Iterate through the Watch History entries to update the:
			# 
			# Root:
			# - "Entries.json" file
			# - "Entry list.txt" file

			# [X] - Adjust entry times in the user's timezone, accounting for the UTC offset during Brazilian Daylight Saving Time (DST):
			# DST started in Brazil at: 21:00 04/11/2018
			# And ended at: 21:00 17/02/2019
			# 
			# Update the entry names (which contain the user's timezone entry times) in the:
			# Root "Entries.json" file (to update the entry name in the "Entries" list and "Dictionary" dictionary)
			# Root "Entry list.txt" file (to update the entry name)

			# Update the "Total" number of entries
			updated_entries["Numbers"]["Total"] = len(updated_entries["Entries"])

			# Update the root "Entries.json" file with the updated root "Entries" dictionary
			self.JSON.Edit(entries_file, updated_entries, full_verbose = self.states["Verbose"]["Full verbose"])

			# Convert the entry list into a text
			updated_entry_list = self.Text.From_List(updated_entry_list, next_line = True)

			# Update the root "Entry list.txt" file with the updated root "Entry list" list
			self.File.Edit(entry_list_file, updated_entry_list, "w", full_verbose = self.states["Verbose"]["Full verbose"])

			# ---------- #

			# Define a local media type number as one
			media_type_number = 1

			# Get the number of media types
			number_of_media_types = str(len(self.media_types["Plural"]["en"]))

			# Iterate through the English plural media types list
			for plural_media_type in self.media_types["Plural"]["en"]:
				# Get the root media type dictionary
				root_media_type = self.media_types[plural_media_type]

				# Get the language media type for the user language
				language_media_type = root_media_type["Plural"][self.language["Small"]]

				# Get the media type folders
				media_type_folders = year["Folders"]["Watch History (by media type)"][plural_media_type]["Folders"]

				# Show the year information text
				print(year_information)

				# Show the number of the media type
				print()
				print(self.language_texts["number_of_the_media_type"] + ":")
				print("[" + str(media_type_number) + "/" + str(number_of_media_types) + "]")

				# Show the language media type
				print()
				print(self.language_texts["media_type"] + ":")
				print("[" + language_media_type + "]")

				# ---------- #

				# Iterate through the Watch History entries to update the:
				# 
				# Media type:
				# - "Entries.json" file
				# - "Entry list.txt" file

				# [X] - Adjust entry times in the user's timezone, accounting for the UTC offset during Brazilian Daylight Saving Time (DST):
				# DST started in Brazil at: 21:00 04/11/2018
				# And ended at: 21:00 17/02/2019
				# 
				# Update the entry names (which contain the user's timezone entry times) in the:
				# Media type "Entries.json" file (to update the entry name in the "Entries" list and "Dictionary" dictionary)
				# Media type "Entry list.txt" file (to update the entry name)

				# Get the "Watch History (by media type)" dictionary of the current media type
				media_type_dictionary = year["Watch History (by media type)"][plural_media_type]

				# ----- #

				# Define a shortcut to the media type "Entries.json" file of the current year
				media_type_entries_file = media_type_folders["Entries"]

				# Define a shortcut the media type "Entries" dictionary of the current year
				media_type_entries = media_type_dictionary["Entries"]

				# Define a shortcut to the updated media type "Entries" dictionary
				updated_media_type_entries = media_type_entries["Updated"]

				# Update the "Total" number of entries
				updated_media_type_entries["Numbers"]["Total"] = len(updated_media_type_entries["Entries"])

				# Update the media type "Entries.json" file with the updated media type "Entries" dictionary
				self.JSON.Edit(media_type_entries_file, updated_media_type_entries, full_verbose = self.states["Verbose"]["Full verbose"])

				# ----- #

				# Define a shortcut to the media type "Entry list.txt" file of the current year
				media_type_entry_list_file = media_type_folders["Entry list"]

				# Define a shortcut the media type "Entry list" dictionary of the current year
				media_type_entry_list = media_type_dictionary["Entry list"]

				# Define a shortcut to the updated media type "Entry list" dictionary
				updated_media_type_entry_list = media_type_entry_list["Updated"]

				# Convert the entry list into a text
				updated_media_type_entry_list = self.Text.From_List(updated_media_type_entry_list, next_line = True)

				# Update the media type "Entry list.txt" file with the updated media type "Entry list" list
				self.File.Edit(media_type_entry_list_file, updated_media_type_entry_list, "w", full_verbose = self.states["Verbose"]["Full verbose"])

				# ---------- #

				# Add one to the media type number
				media_type_number += 1

			# ---------- #

			# Increment the current year index by one
			current_year_index += 1

			# ---------- #

			# If the "Testing" switch is enabled
			# And the "Wait for input" state is active
			# And the current year is not the last one in the list
			if (
				self.switches["Testing"] == True and
				self.states["Wait for input"] == True and
				year_number != self.years["List"][-1]
			):
				# Show a ten dash space separator
				print()
				print(self.separators["10"])

				# Define the next text
				next_text = self.Language.language_texts["next, title()"] + " " + self.Date.language_texts["year, title()"]

				# Format it
				next_text = " ({})".format(next_text.lower())

				# Ask the user to press Enter to advance to the next year
				self.Input.Type(self.Language.language_texts["continue, title()"] + next_text)

		# ---------- #

		# Show a ten dash space separator
		print()
		print(self.separators["10"])

		# Initialize the index of the current media, starting at one
		current_media_index = 1

		# Get the number of medias
		number_of_medias = str(self.medias["Numbers"]["Total"])

		# Iterate through the dictionary of medias, getting the media title and dictionary
		for media_title, media in self.medias["Dictionary"].items():
			# Show the number of the media
			print()
			print(self.language_texts["number_of_the_media"] + ":")
			print("[" + str(current_media_index) + "/" + str(number_of_medias) + "]")

			# ----- #

			# Define a shortcut to the root media dictionary
			root_media_dictionary = media["Root dictionary"]["Media"]

			if "Titles" not in root_media_dictionary:
				self.JSON.Show(media)
				input()

			# Define a shortcut to the media titles dictionary
			media_titles = root_media_dictionary["Titles"]

			# Get the original media title
			media_title = self.Define_Title(media_titles, add_language = False)

			# Get the language media title
			language_media_title = self.Define_Title(media_titles)

			# Show the language media title
			print()
			print(self.language_texts["media_title"] + ":")
			print("[" + language_media_title + "]")

			# ----- #

			# Iterate through the medias inside the root medias dictionary:
			# 
			# For medias with no media items, update the "Watched":
			# - Root media "Entries.json" file
			# - Root media "Entry list.txt" file

			# [X] - Adjust entry times in the user's timezone, accounting for the UTC offset during Brazilian Daylight Saving Time (DST):
			# DST started in Brazil at: 21:00 04/11/2018
			# And ended at: 21:00 17/02/2019
			# 
			# Update the entry names (which contain the user's timezone entry times):
			# - For medias with no media items, update the "Watched":
			# - Root media "Entries.json" file (to update the entry name in the "Entries" list and "Dictionary" dictionary)
			# - Root media "Entry list.txt" file (to update the entry name)

			# If the media does not have a media item list
			if root_media_dictionary["States"]["Has a list of media items"] == False:
				# Define a shortcut to the media watched "Entries.json" file
				media_entries_file = media["Folders"]["Watched"]["Entries"]

				# Define a shortcut to the updated media watched "Entries" dictionary
				media_entries = media["Watched"]["Entries"]["Updated"]

				# Update the "Total" number of entries
				media_entries["Numbers"]["Total"] = len(media_entries["Entries"])

				# Update the media watched "Entries.json" file with the updated media watched "Entries" dictionary
				self.JSON.Edit(media_entries_file, media_entries, full_verbose = self.states["Verbose"]["Full verbose"])

				# --- #

				# Define a shortcut to the media watched "Entry list.txt" file
				media_entry_list_file = media["Folders"]["Watched"]["Entry list"]

				# Define a shortcut to the updated media watched "Entry list" dictionary
				media_entry_list = media["Watched"]["Entry list"]["Updated"]

				# Convert the entry list into a text
				media_entry_list = self.Text.From_List(media_entry_list, next_line = True)

				# Update the media watched "Entry list.txt" file with the updated media watched "Entry list" list
				self.File.Edit(media_entry_list_file, media_entry_list, "w")

			# ----- #

			# Iterate through the medias inside the root medias dictionary:
			# 
			# For medias with media items, update the "Watched":
			# - Media item "Entries.json" file
			# - Media item "Entry list.txt" file
			# (For all media items of the root media)

			# [X] - Adjust entry times in the user's timezone, accounting for the UTC offset during Brazilian Daylight Saving Time (DST):
			# DST started in Brazil at: 21:00 04/11/2018
			# And ended at: 21:00 17/02/2019
			# 
			# Update the entry names (which contain the user's timezone entry times):
			# - For medias with media items, update the "Watched":
			# - Media item "Entries.json" file (to update the entry name in the "Entries" list and "Dictionary" dictionary)
			# - Media item "Entry list.txt" file (to update the entry name)
			# (For all media items of the root media)

			# If the "Watched (media items)" dictionary is not empty
			if media["Watched (media items)"] != {}:
				# Initialize the index of the current media item, starting at one
				current_media_item_index = 1

				# Get the number of media items
				number_of_media_items = str(len(list(media["Watched (media items)"].keys())))

				# Iterate through the media items
				for media_item_title in media["Watched (media items)"]:
					# Show the number of the media item
					print()
					print(self.language_texts["number_of_the_media_item"] + ":")
					print("[" + str(current_media_item_index) + "/" + str(number_of_media_items) + "]")

					# ----- #

					# Define the media item dictionary
					media["Root dictionary"] = self.Define_Media_Item(media["Root dictionary"], media_item = media_item_title)

					# Define a shortcut to the root media dictionary
					root_media_dictionary = media["Root dictionary"]["Media"]

					# Define a shortcut to the media item dictionary
					media_item = root_media_dictionary["Item"]

					# ----- #

					# Define a shortcut to the media item titles dictionary
					media_item_titles = media_item["Titles"]

					# Get the original media item title
					media_item_title = self.Define_Title(media_item_titles, add_language = False)

					# Get the language media item title
					language_media_item_title = self.Define_Title(media_item_titles)

					# Show the language media item title
					print()
					print(self.language_texts["media_item_title"] + ":")
					print("[" + language_media_item_title + "]")

					# ----- #

					# Iterate through the medias inside the root medias dictionary:
					# 
					# For medias with media items, update the "Watched":
					# - Media item "Entries.json" file
					# - Media item "Entry list.txt" file
					# (For all media items of the root media)

					# [X] - Adjust entry times in the user's timezone, accounting for the UTC offset during Brazilian Daylight Saving Time (DST):
					# DST started in Brazil at: 21:00 04/11/2018
					# And ended at: 21:00 17/02/2019
					# 
					# Update the entry names (which contain the user's timezone entry times):
					# - For medias with media items, update the "Watched":
					# - Media item "Entries.json" file (to update the entry name in the "Entries" list and "Dictionary" dictionary)
					# - Media item "Entry list.txt" file (to update the entry name)
					# (For all media items of the root media)

					# Define a shortcut to the media item "Watched" folders
					media_item_watched_folders = media["Folders"]["Watched (media items)"][media_item_title]

					# Define a shortcut to the media item "Watched" dictionary
					media_item_watched = media["Watched (media items)"][media_item_title]

					# --- #

					# Define a shortcut to the media item watched "Entries.json" file
					media_item_entries_file = media_item_watched_folders["Entries"]

					# Define a shortcut to the updated "Entries" dictionary of the media item
					media_item_entries = media_item_watched["Entries"]["Updated"]

					# Update the "Total" number of entries
					media_item_entries["Numbers"]["Total"] = len(media_item_entries["Entries"])

					# Update the media item watched "Entries.json" file with the updated media item "Entries" dictionary
					self.JSON.Edit(media_item_entries_file, media_item_entries, full_verbose = self.states["Verbose"]["Full verbose"])

					# --- #

					# Define a shortcut to the media item watched "Entry list.txt" file
					media_item_entry_list_file = media_item_watched_folders["Entry list"]

					# Define a shortcut to the updated media item watched "Entry list" dictionary
					media_item_entry_list = media_item_watched["Entry list"]["Updated"]

					# Convert the entry list into a text
					media_item_entry_list = self.Text.From_List(media_item_entry_list, next_line = True)

					# Update the media item watched "Entry list.txt" file with the updated media item watched "Entry list" list
					self.File.Edit(media_item_entry_list_file, media_item_entry_list, "w")

					# ----- #

					# Increment the current media item index by one
					current_media_item_index += 1

			# ----- #

			# Increment the current media index by one
			current_media_index += 1

			# ---------- #

			# If the "Testing" switch is enabled
			# And the "Wait for input" state is active
			# And the current media is not the last one in the list
			if (
				self.switches["Testing"] == True and
				self.states["Wait for input"] == True and
				media_title != self.medias["List"][-1]
			):
				# Show a ten dash space separator
				print()
				print(self.separators["10"])

				# Define the next text
				next_text = self.Language.language_texts["next, title(), feminine"] + " " + self.Language.language_texts["media, title()"]

				# Format it
				next_text = " ({})".format(next_text.lower())

				# Ask the user to press Enter to advance to the next media
				self.Input.Type(self.Language.language_texts["continue, title()"] + next_text)

	def Update_Entry_Text(self, entry, contents, language):
		# Define the entry text variable as the "String" key (the text string)
		entry_text = contents["String"]

		# Define the lines variable as the "Lines" key (the text lines)
		lines = contents["Lines"]

		# Add None to the start of the list so the indexes start at one and not zero
		lines = [None] + lines

		# ---------- #
		
		# Define the search text as the "Media type" text
		search_text = self.texts["media_type"][language]

		# If the seventh line is not "Media type:"
		if lines[7] != search_text + ":":
			# Make a backup of the search line and remove it from the entry text
			search_result = re.search(rf"{search_text}:\n(.+)\n\n", entry_text)
			entry_text = re.sub(rf"{search_text}:\n(.+)\n\n", "", entry_text)

			# Define the after line as "Watched media number by media type" text
			after_line = self.texts["watched_media_number_by_media_type"][language]

			# Re-add the line after the after line
			if search_result:
				# Define a shortcut to the media type text
				media_type = "\n" + (search_result.group(0))[:-1]

				entry_text = re.sub(
					rf"({after_line}:\n.*\n)",
					r"\1" + media_type,
					entry_text
				)

		# ---------- #

		# Define the search text as the "Entry" text
		search_text = self.Language.texts["entry, title()"][language]

		# If the tenth line is not "Entry:"
		if lines[10] != search_text + ":":
			# Make a backup of the search line and remove it
			search_result = re.search(rf"{search_text}:\n(.*)", entry_text)
			entry_text = re.sub(rf"(?:\n\n)?{search_text}:\n(.*)", "", entry_text)

			# Define the after line as "Media type" text
			after_line = self.texts["media_type"][language]

			# Re-add the line after the after line
			if search_result:
				# Define a shortcut to the media type text
				media_type = "\n" + (search_result.group(0)) + "\n"

				entry_text = re.sub(
					rf"({after_line}:\n.*\n)",
					r"\1" + media_type,
					entry_text
				)

		# ---------- #

		# Replace the entry name
		entry_text = re.sub(
			rf"({search_text}:\n)(.+\n)",
			r"\g<1>" + entry["Entry"] + "\n",
			entry_text
		)

		# ---------- #

		# Define the search text as the "When I finished watching" text
		search_text = self.texts["when_i_finished_watching"][language] + ":"

		# Search for the search text in the entry text
		search_result = re.search(rf"({search_text})", entry_text)

		# Check if the search found results
		# And the "When I started watching" text is not inside the entry text
		# And the "Started watching" key is inside the entry "Times" dictionary
		if (
			search_result and
			self.texts["when_i_started_watching"][language] + ":" not in entry_text and
			"Started watching" in entry["Times"]
		):
			# Group the result
			result = search_result.group(0)

			# Define the new value
			new_value = self.texts["when_i_started_watching"][language] + ":" + "\n" + \
			entry["Times"]["Started watching"] + "\n\n" + \
			result

			# Re-add the line with the new value
			entry_text = re.sub(
				result,
				new_value,
				entry_text
			)

		# ---------- #

		# Define the "When I finished watching" text shortcut
		finished_watching_text = self.texts["when_i_finished_watching"][language]

		# Get the old finished watching time from the entry text
		old_time = re.search(rf"{finished_watching_text}:\n(.+)", entry_text)

		# If the text was found
		if old_time != None:
			# Group it
			old_time = old_time.group(1)

			# Get the JSON finished watching time
			finished_watching_time = entry["Times"]["Finished watching"]

			# If the two times are not equal
			if old_time != finished_watching_time:
				# Replace it with the time inside the entry text
				entry_text = re.sub(
					rf"({finished_watching_text}:\n).*",
					rf"\g<1>{finished_watching_time}",
					entry_text
				)

		# ---------- #

		# Get the media title and media titles texts
		media_title_text = self.texts["media_title"][language]
		media_titles_text = self.texts["media_titles"][language]

		# If the "Romanized" key is in the media titles dictionary
		if "Romanized" in entry["Media titles"]:
			# Get the original media title
			original_title = entry["Media titles"]["Original"]

			# If the original title is not already present in the entry text
			if original_title not in entry_text:
				# Replace the "Media title" text with the "Media titles" text
				entry_text = entry_text.replace(media_title_text + ":", media_titles_text + ":")

				# Insert the original title below the romainzed title
				entry_text = re.sub(
					rf"({media_titles_text}:\n)(.+\n)",
					rf"\1{original_title}\n\2",
					entry_text
				)

		# ---------- #

		# Iterate through the list of small languages
		for local_language in self.languages["Small"]:
			# If the language is in the list of media titles
			if local_language in entry["Media titles"]:
				# Get the language title
				language_title = entry["Media titles"][local_language]

				# If the language title is not already present in the entry text
				if language_title not in entry_text:
					# Replace the "Media title" text with the "Media titles" text
					entry_text = re.sub(rf"{media_title_text}:", f"{media_titles_text}:", entry_text)

					# Insert the original title below the romainzed title
					entry_text = re.sub(
						rf"({media_titles_text}:\n.+\n)",
						rf"\1{language_title}\n",
						entry_text
					)

		# ---------- #

		# If the Japanese language is in the list of media titles
		# And the romanized one is also
		if (
			"ja" in entry["Media titles"] and
			"Romanized" in entry["Media titles"]
		):
			# Get the Japanese language title
			japanese_language_title = entry["Media titles"]["ja"]

			# Get the romanized title
			romanized_title = entry["Media titles"]["Romanized"]

			# If the Japanese language title is not already present in the entry text
			if japanese_language_title not in entry_text:
				# Insert the Japanese title above the romainzed title
				entry_text = re.sub(
					rf"({romanized_title})",
					rf"{japanese_language_title}\n\g<1>",
					entry_text
				)

		# ---------- #

		# Search for the "Media titles" text
		match = re.search(rf"({media_titles_text}:\n)((?:.+\n)+?)\n", entry_text)

		# If the text is found
		if match:
			header = match.group(1) # The text with a line break
			titles_block = match.group(2) # The block with the media titles
			titles = titles_block.strip().split("\n") # The list with the media titles

			# If there is only one title, change the header text to the singular form
			if len(titles) == 1:
				entry_text = entry_text.replace(media_titles_text + ":", media_title_text + ":")

		# ---------- #

		# Get the singular and plural "Episode titles" texts
		episode_title_text = self.texts["episode_title"][language]
		episode_titles_text = self.texts["episode_titles"][language]

		# Search for the "Episode titles" text
		match = re.search(rf"({episode_titles_text}:\n)((?:.+\n)+?)\n", entry_text)

		# If the text is found
		if match:
			header = match.group(1) # The text with a line break
			titles_block = match.group(2) # The block with the episode titles
			titles = titles_block.strip().split("\n") # The list with the episode titles

			# If there is only one title
			if len(titles) == 1:
				# Replace with the singular text
				replace_with = episode_title_text

			# If there is more than one title
			if len(titles) >= 2:
				# Replace with the plural text
				replace_with = episode_titles_text

			# Replace the header text with the "replace with" text
			entry_text = entry_text.replace(header, replace_with + ":\n")

		# ---------- #

		# Get the media title and media titles texts
		media_item_title = self.texts["media_item_title"][language]
		media_item_titles = self.texts["media_item_titles"][language]

		# If the "Media item titles" key is in the entry dictionary
		if "Media item titles" in entry:
			# Get the media item titles
			titles = entry["Media item titles"]

			# If the "Romanized" key is inside the media item titles dictionary
			if "Romanized" in titles:
				# Get the original media title
				original_title = self.Sanitize_Title(titles["Original"])

				# If the original title is not already present
				if original_title not in entry_text:
					# Replace the "Media item title" text with the "Media item titles" text
					entry_text = entry_text.replace(media_item_title + ":", media_item_titles + ":")

					# Insert the original title below the romainzed title
					entry_text = re.sub(
						rf"({media_item_titles}:\n)(.+\n)",
						rf"\g<1>{original_title}\n\g<2>",
						entry_text
					)

			# Iterate through the list of small languages
			for local_language in self.languages["Small"]:
				# If the language is inside the list of media item titles
				if local_language in titles:
					# Get the language title
					language_title = titles[local_language]

					# If the language title is not already present
					if language_title not in entry_text:
						# Change the "Media item title" text with the "Media item titles" text
						entry_text = entry_text.replace(media_item_title + ":", media_item_titles + ":")

						# Insert the original title below the romainzed title
						entry_text = re.sub(
							rf"({media_item_titles}:\n[^\n]+(?:\n[^\n]+)?)",
							rf"\g<1>\n{language_title}",
							entry_text
						)

		# Search for the "Media item titles" text
		match = re.search(rf"({media_item_titles}:\n)((?:.+\n)+?)\n", entry_text)

		# If the text is found
		if match:
			header = match.group(1) # The text with a line break
			titles_block = match.group(2) # The block with the media item titles
			titles = titles_block.strip().split("\n") # The list with the media item titles

			# If there is only one title, change the header text to the singular form
			if len(titles) == 1:
				entry_text = re.sub(
					rf"{media_item_titles}:",
					f"{media_item_title}:",
					entry_text,
					flags = re.MULTILINE
				)

		# ---------- #

		# Remove the ": " at the start of lines if it exists
		entry_text = re.sub(
			r"^: ",
			"",
			entry_text,
			flags = re.MULTILINE
		)

		# ---------- #

		# Split the text into a list of lines
		lines = entry_text.splitlines()

		# Define a list of lines to keep
		lines_to_keep = []

		# Iterate through each line
		for line in lines:
			# Define the "keep line" switch as False
			keep_line = False

			# Check if the line contains only numbers
			if line.strip().isdigit():
				keep_line = True # Keep lines that contain only numbers

			# Check if the line is not just numbers (else) and not already in the list
			# Or the line is empty
			elif (
				line not in lines_to_keep or
				line == ""
			):
				keep_line = True # Keep lines that are not just numbers, are not in the list, or are empty

			# If the "keep line" switch is True
			if keep_line == True:
				# Keep the line
				lines_to_keep.append(line)

		# Transform the list of lines to keep into a text string
		entry_text = self.Text.From_List(lines_to_keep, next_line = True)

		# ---------- #

		# Return the entry text
		return entry_text
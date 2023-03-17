# Watch History.py

# Main class Watch_History that provides variables to the classes that implement it
class Watch_History(object):
	def __init__(self):
		self.Define_Basic_Variables()

		# Define module folders
		from Utility.Define_Folders import Define_Folders as Define_Folders

		Define_Folders(self)

		self.Define_Texts()

		# Import Years class
		from Years.Years import Years as Years
		self.Years = Years()

		# Import Christmas class
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

		self.switches = Global_Switches().switches["global"]

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
		if hasattr(self, "current_year") == False:
			self.current_year = self.Years.current_year

		if self.folders == self.Folder.folders:
			# Folders dictionary
			self.folders = self.Folder.Contents(self.folders["notepad"]["networks"]["audiovisual_media_network"]["root"], lower_key = True)["dictionary"]

		# Audiovisual Media Network root files
		self.folders["audiovisual_media_network"]["watch_list"] = self.folders["audiovisual_media_network"]["root"] + "Watch List.txt"

		self.folders["watch_history"]["current_year"] = self.folders["watch_history"][self.current_year["Number"]]

	def Define_Lists_And_Dictionaries(self):
		# Lists
		self.media_details_parameters = [
			self.JSON.Language.language_texts["original_name"],
			self.JSON.Language.language_texts["[language]_name"],
			self.language_texts["year, title()"],
			self.language_texts["has_dub"],
			self.language_texts["status, title()"],
			self.language_texts["origin_type"]
		]

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

		self.media_details_string_parameters = {
			self.JSON.Language.language_texts["original_name"]: {
				"select_text": self.JSON.Language.language_texts["original_name"],
				"default": ""
			},

			self.JSON.Language.language_texts["language_name"][self.user_language]: {
				"select_text": self.JSON.Language.language_texts["language_name"][self.user_language],
				"default": {
					"format_name": self.JSON.Language.language_texts["original_name"]
				},
			},

			self.language_texts["year, title()"]: {
				"select_text": self.language_texts["year, title()"],
				"default": self.date["year"]
			}
		}

		self.media_details_choice_list_parameters = {
			self.language_texts["status, title()"]: {
				"language_list": self.language_texts["watching_statuses, type: list"],
				"english_list": self.language_texts["watching_statuses, type: list"],
				"select_text": self.language_texts["select_one_watching_status_from_the_status_list"]
			},

			self.language_texts["origin_type"]: {
				"language_list": self.language_texts["origin_types, type: list"],
				"english_list": self.language_texts["origin_types, type: list"],
				"select_text": self.language_texts["select_one_origin_type_from_the_list"]
			}
		}

		self.media_details_yes_or_no_definer_parameters = {
			self.language_texts["has_dub"]: self.language_texts["has_dub"]
		}

		self.media_item_details_parameters = {
			self.JSON.Language.language_texts["original_name"]: {
				"mode": "string",
				"select_text": self.JSON.Language.language_texts["original_name"]
			},

			self.JSON.Language.language_texts["language_name"][self.user_language]: {
				"mode": "string/default-format",
				"select_text": self.JSON.Language.language_texts["language_name"][self.user_language],
				"default": {
					"format_name": self.JSON.Language.language_texts["original_name"],
					"functions": [
						str
					]
				}
			},

			self.language_texts["episode, title()"]: {
				"mode": "string/default",
				"select_text": self.language_texts["episode, title()"],
				"default": "None"
			},

			self.language_texts["origin_location"]: {
				"mode": "string/default-format",
				"select_text": self.language_texts["origin_location"],
				"default": {
					"format_name": self.JSON.Language.language_texts["original_name"],
					"functions": [
						self.Text.Lower,
						self.Sanitize
					]
				}
			}
		}

	def Define_Types(self):
		self.media_types = self.JSON.To_Python(self.folders["data"]["types"])

		self.media_types = {
			"singular": self.media_types["singular"],
			"plural": self.media_types["plural"],
			"genders": self.JSON.Language.texts["genders, type: dict"],
			"gender_items": self.JSON.Language.texts["gender_items"],
			"media_list": {
				"Number": 0,
				"Numbers": {}
			}
		}

		# Iterate through the English plural media types list
		i = 0
		for plural_media_type in self.media_types["plural"]["en"]:
			language_media_type = self.media_types["plural"][self.user_language][i]

			# Create media type dictionary
			self.media_types[plural_media_type] = {
				"singular": {},
				"plural": {},
				"genders": {},
				"folders": {},
				"subfolders": {},
				"status": [
					self.texts["watching, title()"]["en"],
					self.texts["re_watching, title()"]["en"]
				],
				"texts": {}
			}

			# Define singular and plural media types
			for language in self.languages["small"]:
				for text_type in ["singular", "plural"]:
					self.media_types[plural_media_type][text_type][language] = self.media_types[text_type][language][i]

			# Define select text for "Videos" media type
			if self.media_types[plural_media_type]["plural"]["en"] == self.texts["videos, title()"]["en"]:
				self.media_types[plural_media_type]["singular"]["select"] = self.language_texts["channel, title()"]
				self.media_types[plural_media_type]["plural"]["select"] = self.language_texts["channels, title()"]

			# Define genders
			gender = "masculine"

			if plural_media_type == self.texts["series, title()"]["en"]:
				gender = "feminine"

			for language in self.languages["small"]:
				self.media_types[plural_media_type]["genders"][language] = self.media_types["genders"][language][gender]

			# Create folders
			for root_folder in ["Media Info", "Watch History"]:
				root_key = root_folder.lower().replace(" ", "_")
				key = plural_media_type.lower().replace(" ", "_")

				if root_folder == "Media Info":
					self.folders[root_key][key] = {
						"root": self.folders[root_key]["root"] + language_media_type + "/",
					}

					self.Folder.Create(self.folders[root_key][key]["root"])

				# Watch History Per Media Type folder
				if root_folder == "Watch History":
					self.folders[root_key]["current_year"]["per_media_type"][key] = {
						"root": self.folders[root_key]["current_year"]["per_media_type"]["root"] + plural_media_type + "/"
					}

					self.Folder.Create(self.folders[root_key]["current_year"]["per_media_type"][key]["root"])

					# Create "Entries.json" file in "Per Media Type" media type folder
					self.folders[root_key]["current_year"]["per_media_type"][key]["entries"] = self.folders[root_key]["current_year"]["per_media_type"][key]["root"] + "Entries.json"
					self.File.Create(self.folders[root_key]["current_year"]["per_media_type"][key]["entries"])

					# Create "Entry list.txt" file in "Per Media Type" media type folder
					self.folders[root_key]["current_year"]["per_media_type"][key]["entry_list"] = self.folders[root_key]["current_year"]["per_media_type"][key]["root"] + "Entry list.txt"
					self.File.Create(self.folders[root_key]["current_year"]["per_media_type"][key]["entry_list"])

					# Create "Files" folder on "Per Media Type" media type folder
					self.folders[root_key]["current_year"]["per_media_type"][key]["files"] = {
						"root": self.folders[root_key]["current_year"]["per_media_type"][key]["root"] + "Files/",
					}

					self.Folder.Create(self.folders[root_key]["current_year"]["per_media_type"][key]["files"]["root"])

			# Define media type folders and files
			key = self.media_types[plural_media_type]["plural"]["en"].lower().replace(" ", "_")

			self.media_types[plural_media_type]["folders"] = {
				"media_info": self.folders["media_info"][key],
				"per_media_type": self.folders["watch_history"]["current_year"]["per_media_type"][key]
			}

			# Define "Info.json" file
			self.media_types[plural_media_type]["folders"]["media_info"]["info"] = self.media_types[plural_media_type]["folders"]["media_info"]["root"] + "Info.json"
			self.File.Create(self.media_types[plural_media_type]["folders"]["media_info"]["info"])

			# Define media type subfolders
			text = self.media_types[plural_media_type]["singular"][self.user_language]

			if plural_media_type != self.texts["movies, title()"]["en"]:
				text = "season"

			if plural_media_type == self.texts["videos, title()"]["en"]:
				text = "serie"

			for text_type in ["singular", "plural"]:
				if text_type == "plural":
					text += "s"

				self.media_types[plural_media_type]["subfolders"][text_type] = text

				if text + ", title()" in self.language_texts:
					self.media_types[plural_media_type]["subfolders"][text_type] = self.language_texts[text + ", title()"]

			# Define current "season/series" folder
			text = self.media_types[plural_media_type]["subfolders"]["singular"]

			if "{" not in self.language_texts["current_{}"][0]:
				text = text.lower()

			self.media_types[plural_media_type]["subfolders"]["current"] = self.language_texts["current_{}"].format(text)

			# Read "Info.json" file
			self.media_types[plural_media_type]["json"] = self.JSON.To_Python(self.media_types[plural_media_type]["folders"]["media_info"]["info"])

			# Check the "watching status" of the media item list
			# Add the media inside the correct "watching status" list if it is not there already
			# Remove the media from the wrong "watching status" list if it is there
			self.media_types[plural_media_type] = self.Check_Status(self.media_types[plural_media_type])

			# Add the media number to the media number
			self.media_types["media_list"]["Number"] += self.media_types[plural_media_type]["json"]["Number"]

			# Add the media number to the media type media numbers
			self.media_types["media_list"]["Numbers"][plural_media_type] = self.media_types[plural_media_type]["json"]["Number"]

			# Get media item list with "Watching" and "Re-watching" statuses
			self.media_types[plural_media_type]["media_list"] = self.Get_Media_List(self.media_types[plural_media_type])

			add_status = False			

			# Add status to "media item list option" list if add_status is True
			if add_status == True:
				self.media_types[plural_media_type]["media_list_option"] = self.media_types[plural_media_type]["media_list"].copy()

				i = 0
				for media in self.media_types[plural_media_type]["media_list"]:
					for status in self.media_types[plural_media_type]["status"]:
						if media in self.media_types[plural_media_type]["json"]["Status"][status]:
							language_status = self.Get_Language_Status(status)

					self.media_types[plural_media_type]["media_list_option"][i] = "{} [{}]".format(self.media_types[plural_media_type]["media_list_option"][i], language_status)

					i += 1

			self.media_types[plural_media_type].pop("json")

			# Add media item list length numbers to media types list to show on select media type
			for language in self.languages["small"]:
				for text_type in ["singular", "plural"]:
					self.media_types[plural_media_type][text_type]["show"] = self.media_types[plural_media_type][text_type][self.user_language] + " (" + str(len(self.media_types[plural_media_type]["media_list"])) + ")"

			self.media_types[plural_media_type]["texts"]["show"] = self.Text.By_Number(self.media_types[plural_media_type]["media_list"], self.media_types[plural_media_type]["singular"]["show"], self.media_types[plural_media_type]["plural"]["show"])

			i += 1

		if self.current_year["Number"] == str(self.date["year"]):
			# Write media types dictionary into "Media Types.json" file
			self.JSON.Edit(self.folders["data"]["types"], self.media_types)

		# Update "Info.json" file on "Media Info" folder
		dictionary = self.JSON.To_Python(self.folders["media_info"]["info"])
		dictionary.update(self.media_types["media_list"])

		self.JSON.Edit(self.folders["media_info"]["info"], dictionary)

	def Define_Registry_Format(self):
		from copy import deepcopy
		import collections

		# Define default Entries dictionary template
		self.template = {
			"Numbers": {
				"Total": 0,
				"Comments": 0
			},
			"Entries": [],
			"Dictionary": {}
		}

		self.dictionaries = {
			"History": self.JSON.To_Python(self.folders["watch_history"]["history"]),
			"Entries": deepcopy(self.template),
			"Watched": deepcopy(self.template),
			"Media Type": {},
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

		# If current year is not inside the "History" years list, add it to the list
		if self.current_year["Number"] not in self.dictionaries["History"]["Years"]:
			self.dictionaries["History"]["Years"].append(self.current_year["Number"])

		# Update the number of years with the length of the years list
		self.dictionaries["History"]["Numbers"]["Years"] = len(self.dictionaries["History"]["Years"])

		# Define the total number of comments as the number gotten from the root comments file
		self.dictionaries["History"]["Numbers"]["Comments"] = self.JSON.To_Python(self.folders["comments"]["comments"])["Numbers"]["Total"]

		# Update the "History.json" file with the new History dictionary
		self.JSON.Edit(self.folders["watch_history"]["history"], self.dictionaries["History"])

		# If Entries.json is not empty and has entries, get Entries dictionary from it
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

		# Update the "Entries.json" file with Entries dictionary
		self.JSON.Edit(self.folders["watch_history"]["current_year"]["entries"], self.dictionaries["Entries"])

		# Iterate through English media types list
		for plural_media_type in self.media_types["plural"]["en"]:
			key = plural_media_type.lower().replace(" ", "_")

			# Define default media type dictionary
			self.dictionaries["Media Type"][plural_media_type] = deepcopy(self.template)

			# If media type "Entries.json" is not empty, get media type Entries dictionary from it
			if self.File.Contents(self.folders["watch_history"]["current_year"]["per_media_type"][key]["entries"])["lines"] != [] and self.JSON.To_Python(self.folders["watch_history"]["current_year"]["per_media_type"][key]["entries"])["Entries"] != []:
				self.dictionaries["Media Type"][plural_media_type] = self.JSON.To_Python(self.folders["watch_history"]["current_year"]["per_media_type"][key]["entries"])

			if self.current_year["Number"] not in self.dictionaries["Root comments"]["Numbers"]["Type"][plural_media_type]["Years"]:
				self.dictionaries["Root comments"]["Numbers"]["Type"][plural_media_type]["Years"][self.current_year["Number"]] = 0

			# Get media type comment number per year
			self.dictionaries["Media Type"][plural_media_type]["Numbers"]["Comments"] = self.dictionaries["Root comments"]["Numbers"]["Type"][plural_media_type]["Years"][self.current_year["Number"]]

			self.JSON.Edit(self.folders["watch_history"]["current_year"]["per_media_type"][key]["entries"], self.dictionaries["Media Type"][plural_media_type])

			if plural_media_type not in self.dictionaries["Root comments"]["Numbers"]["Type"]:
				self.dictionaries["Root comments"]["Numbers"]["Type"][plural_media_type] = {
					"Total": 0,
					"Years": {}
				}

			# If the current year is not inside the media type year comment number dictionary, add it
			if self.current_year["Number"] not in self.dictionaries["Root comments"]["Numbers"]["Type"][plural_media_type]["Years"]:
				self.dictionaries["Root comments"]["Numbers"]["Type"][plural_media_type]["Years"][self.date["year"]] = 0

			# Sort media type years list
			self.dictionaries["Root comments"]["Numbers"]["Type"][plural_media_type]["Years"] = dict(collections.OrderedDict(sorted(self.dictionaries["Root comments"]["Numbers"]["Type"][plural_media_type]["Years"].items())))

		# Update "Comments.json" file with updated Comments dictionary
		self.JSON.Edit(self.folders["comments"]["comments"], self.dictionaries["Root comments"])

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
			to_remove = [to_remove]

		media_types = deepcopy(self.media_types)

		for text in to_remove:
			if text in media_types:
				media_types.pop(text)

		dictionary = {
			"to_remove": to_remove,
			"media_types": media_types,
			"list": {}
		}

		# Iterate through English plural media types list
		for plural_media_type in self.media_types["plural"]["en"]:
			# If the plural media type is inside the local media types dictionary
			if plural_media_type in dictionary["media_types"]:
				# Get the media type dictionary
				media_type = dictionary["media_types"][plural_media_type]

				# Iterate through small languages list
				for language in self.languages["small"]:
					# Create empty language list if it does not exist
					if language not in dictionary["list"]:
						dictionary["list"][language] = []

					# Add to the plural media types list
					dictionary["list"][language].append(media_type["plural"][language])

		return dictionary

	def Select_Media_Type(self, options = None):
		dictionary = {
			"texts": {
				"show": self.language_texts["media_types"],
				"select": self.language_texts["select_one_media_type_to_watch"]
			},
			"list": {
				"en": self.media_types["plural"]["en"].copy(),
				self.user_language: self.media_types["plural"][self.user_language].copy()
			},
			"status": [
				self.texts["watching, title()"]["en"],
				self.texts["re_watching, title()"]["en"]
			]
		}

		if options != None:
			dictionary = self.Define_Options(dictionary, options)

		# Get the media type media numbers
		numbers = self.JSON.To_Python(self.folders["media_info"]["info"])["Numbers"]

		i = 0
		for plural_media_type in self.media_types["plural"]["en"]:
			if plural_media_type in dictionary["list"]["en"]:
				for language in self.languages["small"]:
					dictionary["list"][language][i] = dictionary["list"][language][i] + " (" + str(numbers[plural_media_type]) + ")"

				i += 1

		# Select the media type
		if "option" not in dictionary and "number" not in dictionary:
			dictionary["option"] = self.Input.Select(dictionary["list"]["en"], dictionary["list"][self.user_language], show_text = dictionary["texts"]["show"], select_text = dictionary["texts"]["select"])["option"]
			dictionary["option"] = dictionary["option"].split(" (")[0]

		if "number" in dictionary:
			dictionary["option"] = dictionary["list"]["en"][dictionary["number"]]

		# Get selected media type dictionary from media types dictionary
		dictionary.update(self.media_types[dictionary["option"]])

		# Get status from options dictionary
		if "status" in options:
			dictionary["status"] = options["status"]

		# Get the media list using the correct status
		dictionary["media_list"] = self.Get_Media_List(dictionary, dictionary["status"])

		return dictionary

	def Select_Media(self, options = None, item = False, watch = False, select_media_item = False):
		self.item = item

		dictionary = {}

		if options != None:
			dictionary = self.Define_Options(dictionary, options)

		media = dictionary["Media"]

		if self.item == True:
			media = dictionary["Media"]["item"]

		dictionary["texts"] = dictionary["media_type"]["texts"]

		# Define select text
		text = dictionary["media_type"]["singular"][self.user_language]

		if "select" in dictionary["media_type"]["singular"]:
			text = dictionary["media_type"]["singular"]["select"]

		dictionary["texts"]["select"] = self.language_texts["select_{}_to_watch"].format(dictionary["media_type"]["genders"][self.user_language]["a"] + " " + text)

		# Select media
		if "title" not in media:
			language_options = dictionary["media_type"]["media_list"]

			if "media_list_option" in dictionary["media_type"]:
				language_options = dictionary["media_type"]["media_list_option"]

			media.update({
				"title": self.Input.Select(dictionary["media_type"]["media_list"], language_options = language_options, show_text = dictionary["texts"]["show"], select_text = dictionary["texts"]["select"])["option"]
			})

		sanitized_title = self.Sanitize_Title(media["title"])

		if media["title"] != "[" + self.JSON.Language.language_texts["finish_selection"] + "]":
			# Define media info and local media folder
			if "folders" in media:
				if "root" not in media["folders"]:
					media["folders"].update({
						"root": dictionary["media_type"]["folders"]["media_info"]["root"] + self.Sanitize(sanitized_title, restricted_characters = True) + "/"
					})

				media["folders"].update({
					"media": {
						"root": dictionary["Media"]["folders"]["media"]["root"]
					}
				})

				if sanitized_title + "/" not in media["folders"]["media"]["root"]:
					media["folders"]["media"]["root"] += self.Sanitize(sanitized_title, restricted_characters = True) + "/"

				# Create folders
				for key in media["folders"]:
					folder = media["folders"][key]

					if "root" in folder:
						folder = folder["root"]

					self.Folder.Create(folder)

			if "folders" not in media:
				media["folders"] = {
					"root": dictionary["media_type"]["folders"]["media_info"]["root"] + self.Sanitize(sanitized_title, restricted_characters = True) + "/",
					"media": {
						"root": self.Folder.folders["root"]["mídias"]["root"] + self.Sanitize_Title(sanitized_title) + "/"
					}
				}

				# Create folders
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
				"Key": "",
				"Dictionary": {}
			}

			# Define "[Singular media type].json" or "Season.json" file (media information file) for non-video media
			if dictionary["media_type"]["plural"]["en"] != self.texts["videos, title()"]["en"]:
				media["Information"]["File name"] = dictionary["media_type"]["singular"]["en"]

				if self.item == True and media["title"] != dictionary["Media"]["title"] and dictionary["media_type"]["plural"]["en"] != self.texts["movies, title()"]["en"]:
					media["Information"]["File name"] = "Season"

				file_names.append(media["Information"]["File name"] + ".json")

			# Define "Channel.json" or "Playlist.json" file for video media
			if dictionary["media_type"]["plural"]["en"] == self.texts["videos, title()"]["en"]:
				media["Information"]["File name"] = "Channel"

				if self.item == True:
					media["Information"]["File name"] = "Playlist"

				file_names.append(media["Information"]["File name"] + ".json")

			media["Information"]["Key"] = media["Information"]["File name"].lower().replace(" ", "_")

			# Define media text files
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

			if self.File.Contents(media["folders"][media["Information"]["File name"].lower()])["lines"] != []:
				media["Information"]["Dictionary"] = self.JSON.To_Python(media["folders"][media["Information"]["File name"].lower()])

			# Define media details
			media["details"] = self.File.Dictionary(media["folders"]["details"])

			if self.item == False:
				# Define the default media language as the user language
				media["Language"] = self.full_user_language

				# Define the media language as "日本語" (Nihongo, Japanese) for anime media
				if dictionary["media_type"]["plural"]["en"] == self.texts["animes, title()"]["en"]:
					media["Language"] = "日本語"

				# Define the default media language as the user language for video media
				if dictionary["media_type"]["plural"]["en"] == self.texts["videos, title()"]["en"]:
					media["Language"] = self.full_user_language

				# Change user language to original media language if the key exists inside the media details
				if self.JSON.Language.language_texts["original_language"] in media["details"]:
					media["Language"] = media["details"][self.JSON.Language.language_texts["original_language"]]

				if media["Language"] in list(self.languages["full"].values()):
					# Iterate through full languages list to find small language from the full language
					for small_language in self.languages["full"]:
						full_language = self.languages["full"][small_language]

						if full_language == media["Language"]:
							media["Language"] = small_language

				# Define media states dictionary
				states = {
					"remote": False,
					"local": False,
					"hybrid": False,
					"video": False,
					"series_media": True,
					"episodic": False,
					"single_unit": False,
					"Replace title": False,
					"Media item list": False,
					"Has Dubbing": False,
					"dubbed_to_title": False,
					"Watch dubbed": False,
					"Re-watching": False,
					"Christmas": False,
					"Commented": False,
					"Completed media": False,
					"Completed media item": False,
					"First entry in year": False,
					"First media type entry in year": False,
					"finished_watching": False
				}

				if "States" in media:
					media["States"].update(states)

				if "States" not in media:
					media["States"] = states

				if self.Today_Is_Christmas == True:
					media["States"]["Christmas"] = True

				# Define origin type state
				for key in ["local", "remote", "hybrid"]:
					if self.language_texts["origin_type"] in media["details"]:
						if media["details"][self.language_texts["origin_type"]] == self.language_texts[key + ", title()"]:
							media["States"][key] = True

				if self.language_texts["origin_type"] not in media["details"]:
					media["States"]["remote"] = True

					media["details"][self.language_texts["origin_type"]] = self.language_texts["remote, title()"]

				# Define video state for videos
				if dictionary["media_type"]["plural"]["en"] == self.texts["videos, title()"]["en"]:
					media["States"]["video"] = True
					media["States"]["episodic"] = False

				if self.language_texts["episodic, title()"] in media["details"]:
					media["States"]["episodic"] = self.Input.Define_Yes_Or_No(media["details"][self.language_texts["episodic, title()"]])

				# Define single unit state
				if self.language_texts["single_unit"] in media["details"]:
					media["States"]["single_unit"] = self.Input.Define_Yes_Or_No(media["details"][self.language_texts["single_unit"]])

				# Define non-series media state for movies
				if dictionary["media_type"]["plural"]["en"] == self.texts["movies, title()"]["en"]:
					media["States"]["series_media"] = False

				if media["States"]["video"] == True:
					dictionary["Media"]["folders"]["channel"] = dictionary["Media"]["folders"]["root"] + "Channel.json"
					self.File.Create(dictionary["Media"]["folders"]["channel"])

					if self.File.Contents(dictionary["Media"]["folders"]["channel"])["lines"] == []:
						# Get channel information
						dictionary["Media"]["channel"] = self.Get_YouTube_Information("channel", dictionary["Media"]["details"]["ID"])

						# Define channel date
						channel_date = self.Date.From_String(dictionary["Media"]["channel"]["Time"])

						# Update "Date" key of media details
						dictionary["Media"]["details"][self.Date.language_texts["start_date"]] = self.Date.To_String(channel_date["date"].astimezone(), self.Date.language_texts["date_time_format"])

						# Update "Year" key of media details
						dictionary["Media"]["details"][self.Date.language_texts["year, title()"]] = channel_date["year"]

						# Update media details dictionary
						self.File.Edit(dictionary["Media"]["folders"]["details"], self.Text.From_Dictionary(dictionary["Media"]["details"]), "w")

						# Update "Channel.json" file
						self.JSON.Edit(dictionary["Media"]["folders"]["channel"], dictionary["Media"]["channel"])

					else:
						# Get channel information
						dictionary["Media"]["channel"] = self.JSON.To_Python(dictionary["Media"]["folders"]["channel"])

				# Define remote origin for animes or videos media type
				if self.language_texts["remote_origin, title()"] not in dictionary["Media"]["details"]:
					remote_origin = "None"

					if dictionary["media_type"]["plural"]["en"] == self.texts["animes, title()"]["en"]:
						remote_origin = "Animes Vision"

					if dictionary["media_type"]["plural"]["en"] == self.texts["videos, title()"]["en"]:
						remote_origin = "YouTube"

					if remote_origin != "None":
						dictionary["Media"]["details"][self.language_texts["remote_origin, title()"]] = remote_origin

				# Define Re-watching state for Re-watching status
				if self.language_texts["status, title()"] in media["details"] and media["details"][self.language_texts["status, title()"]] == self.language_texts["re_watching, title()"]:
					media["States"]["Re-watching"] = True

				media["episode"] = {
					"title": "",
					"titles": {},
					"Sanitized": "",
					"number": 1,
					"number_text": "1",
					"separator": ""
				}

				if media["States"]["remote"] == True or self.language_texts["remote_origin, title()"] in media["details"]:
					media["episode"]["remote"] = {
						"title": "",
						"link": "",
						"code": ""
					}

				media["episodes"] = {
					"number": 0
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
		if dictionary["Media"]["States"]["series_media"] == True:
			# Define the media items dictionary with the folders and number keys
			dictionary["Media"]["items"] = {
				"folders": {
					"root": dictionary["Media"]["folders"]["root"] + dictionary["media_type"]["subfolders"]["plural"] + "/",
				},
				"number": 1
			}

			# If the media items folder exists
			if self.Folder.Exist(dictionary["Media"]["items"]["folders"]["root"]) == True:
				# Iterate through item type keys
				for name in ["list", "current"]:
					key = name

					if name == "list":
						key = "plural"

					# Define the item type text file
					dictionary["Media"]["items"]["folders"][name] = dictionary["Media"]["items"]["folders"]["root"] + dictionary["media_type"]["subfolders"][key] + ".txt"
					self.File.Create(dictionary["Media"]["items"]["folders"][name])

					# Get the contents of the text file
					dictionary["Media"]["items"][name] = self.File.Contents(dictionary["Media"]["items"]["folders"][name])["lines"]

					# If the contents is not empty and the item type is "current"
					if dictionary["Media"]["items"][name] != [] and name == "current":
						# Define the contents as the first line of the text file
						dictionary["Media"]["items"][name] = dictionary["Media"]["items"][name][0]

					# If the item type is "list"
					if name == "list":
						# Define the items number as the number of lines of the text file
						dictionary["Media"]["items"]["number"] = len(dictionary["Media"]["items"]["list"])

				# Define media item folders
				for name in dictionary["Media"]["items"]["list"]:
					name = self.Sanitize_Title(name)

					dictionary["Media"]["items"]["folders"][name] = dictionary["Media"]["items"]["folders"]["root"] + name + "/"
					self.Folder.Create(dictionary["Media"]["items"]["folders"][name])

				# Define current media item
				title = dictionary["Media"]["items"]["current"]

				# The media has a media items list
				dictionary["Media"]["States"]["Media item list"] = True

				show_text = self.Text.Capitalize(dictionary["media_type"]["subfolders"]["plural"])
				select_text = self.language_texts["select_a_season"]

				items_list = dictionary["Media"]["items"]["list"].copy()

				# Define show and select text for video media
				if dictionary["Media"]["States"]["video"] == True:
					show_text = self.Text.Capitalize(self.language_texts["youtube_video_series"])
					select_text = self.language_texts["select_a_youtube_video_series"]

				# Iterate through media items list
				for media_list_item in dictionary["Media"]["items"]["list"].copy():
					folders = {
						"root": dictionary["Media"]["items"]["folders"]["root"] + self.Sanitize_Title(media_list_item) + "/"
					}

					# Define details file
					folders["details"] = folders["root"] + self.JSON.Language.language_texts["details, title()"] + ".txt"

					# Read details file
					details = self.File.Dictionary(folders["details"])

					# If the media item is a single unit media item and the "Type" key is inside the details
					if self.JSON.Language.language_texts["type, title()"] in details:
						# Define the empty secondary types list
						if "Secondary types" not in dictionary["Media"]["items"]:
							dictionary["Media"]["items"]["Secondary types"] = []

						self.secondary_types = [
							"pilot",
							"special",
							"movie"
						]

						if dictionary["media_type"]["plural"]["en"] == self.texts["animes, title()"]["en"]:
							self.secondary_types.extend([
								"OVA",
								"ONA"
							])

						# Iterate through the single unit type keys list
						for key in self.secondary_types:
							# If the key is inside the "language_texts" dictionary of the Language class, use it as the list
							if key in self.JSON.Language.language_texts:
								texts_list = self.JSON.Language.language_texts

							# If the key is inside the "language_texts" dictionary of "Watch_History"
							if key in self.language_texts:
								texts_list = self.language_texts

							singular_type = key
							plural_type = key + "s"

							# Define the singular text
							if key in texts_list:
								singular_type = texts_list[key].title()

							# Define the plural text
							if key + "s" in texts_list:
								plural_type = texts_list[key + "s"].title()

							# If the type inside the media item details is equal to the singular type
							if details[self.JSON.Language.language_texts["type, title()"]] == singular_type:
								# Define the item type as the singular type
								item_type = singular_type

								# If the key is not "pilot", define the item type as the plural type
								if key != "pilot":
									item_type = plural_type

								if key not in ["OVA", "ONA"]:
									item_type = item_type.lower()

								if item_type not in dictionary["Media"]["items"]["Secondary types"]:
									# Add the item type to the secondary types list
									dictionary["Media"]["items"]["Secondary types"].append(item_type)

					# If the "Status" key is present inside the details dictionary and the status is "Completed", remove the media item from the media items list
					if self.language_texts["status, title()"] in details and details[self.language_texts["status, title()"]] == self.JSON.Language.language_texts["completed, title()"]:
						items_list.remove(media_list_item)

					if self.caller == "Fill_Media_Files" and self.language_texts["single_unit"] not in details:
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

					if self.language_texts["single_unit"] in details:
						items_list.remove(media_list_item)

				if dictionary["Media"]["States"]["video"] == True or select_media_item == True:
					if watch == True and len(dictionary["Media"]["items"]["list"]) != 1:
						title = self.Input.Select(items_list, show_text = show_text, select_text = select_text)["option"]

				if media_item != None:
					title = media_item

				sanitized_title = self.Sanitize_Title(title)

				# Define media item dictionary with titles and folder
				dictionary["Media"]["item"] = {
					"title": title,
					"Titles": {},
					"Sanitized": sanitized_title,
					"folders": {
						"root": dictionary["Media"]["items"]["folders"]["root"] + sanitized_title + "/"
					},
					"number": 0
				}

				dictionary["Media"]["episodes"]["number"] = 0

				i = 0
				for name in dictionary["Media"]["items"]["list"]:
					if dictionary["Media"]["item"]["title"] == name:
						dictionary["Media"]["item"]["number"] = i

					# Get media item details file
					folder = dictionary["Media"]["items"]["folders"]["root"] + self.Sanitize_Title(name) + "/"
					details_file = folder + self.JSON.Language.language_texts["details, title()"] + ".txt"
					details = self.File.Dictionary(details_file)

					# If the item is not a single unit, add its episode number to the root episode number
					if self.language_texts["single_unit"] not in details:
						titles_folder = folder + self.JSON.Language.language_texts["titles, title()"] + "/"
						titles_file = titles_folder + self.languages["full"]["en"] + ".txt"

						dictionary["Media"]["episodes"]["number"] += self.File.Contents(titles_file)["length"]

					i += 1

				# Add the episode number after the "Final date" or "Start date" key or update it
				key_value = {
					"key": self.language_texts["episodes, title()"],
					"value": dictionary["Media"]["episodes"]["number"]
				}

				after_key = self.Date.language_texts["end_date"]

				if after_key not in dictionary["Media"]["details"]:
					after_key = self.Date.language_texts["start_date"]

				dictionary["Media"]["details"] = self.JSON.Add_Key_After_Key(dictionary["Media"]["details"], key_value, after_key = after_key)

				# Define the key to the plural media items text
				key = dictionary["media_type"]["subfolders"]["plural"]

				# If the media has secondary types, define the correct key
				if "Secondary types" in dictionary["Media"]["items"]:
					secondary_types = dictionary["Media"]["items"]["Secondary types"]

					# Iterate through secondary item types list
					for item_type in secondary_types:
						# If the list has more types and the item type is not the last one, add the comma
						if len(secondary_types) > 1:
							key += ", "

						# If the secondary item types list has just one type or has more and the type is the last one
						# Add the " and " text
						if (
							len(secondary_types) == 1 or
							len(secondary_types) > 1 and item_type == secondary_types[-1]
						):
							if len(secondary_types) == 1:
								key += " "

							key += self.JSON.Language.language_texts["and"] + " "

						# Add the item type
						key += item_type

				# Add the media subfolders plural text after the "Episodes" key or update it
				key_value = {
					"key": key,
					"value": dictionary["Media"]["items"]["number"]
				}

				dictionary["Media"]["details"] = self.JSON.Add_Key_After_Key(dictionary["Media"]["details"], key_value, self.language_texts["episodes, title()"], number_to_add = 0)

				# If the media has secondary types and the items list plural text key is inside the details
				if "Secondary types" in dictionary["Media"]["items"] and dictionary["media_type"]["subfolders"]["plural"] in dictionary["Media"]["details"]:
					# Remove the key
					dictionary["Media"]["details"].pop(dictionary["media_type"]["subfolders"]["plural"])

				dict_ = deepcopy(dictionary["Media"]["details"])

				if self.language_texts["remote_origin, title()"] in dict_:
					if dict_[self.language_texts["remote_origin, title()"]] == "Animes Vision":
						dict_.pop(self.language_texts["remote_origin, title()"])

					elif dict_[self.language_texts["remote_origin, title()"]] == "YouTube":
						dict_.pop(self.language_texts["remote_origin, title()"])

				# Update the media details file
				self.File.Edit(dictionary["Media"]["folders"]["details"], self.Text.From_Dictionary(dict_), "w")

				dictionary = self.Select_Media(dictionary, item = True)

				dictionary["Media"]["States"]["single_unit"] = False

				# Define the single unit state
				if self.language_texts["single_unit"] in dictionary["Media"]["item"]["details"]:
					dictionary["Media"]["States"]["single_unit"] = self.Input.Define_Yes_Or_No(dictionary["Media"]["item"]["details"][self.language_texts["single_unit"]])

				if dictionary["Media"]["States"]["single_unit"] == True:
					dictionary["Media"]["item"]["folders"]["media"]["root"] = dictionary["Media"]["folders"]["media"]["root"]

			if self.Folder.Exist(dictionary["Media"]["items"]["folders"]["root"]) == False:
				dictionary["Media"]["States"]["Media item list"] = False

				dictionary["Media"]["items"]["list"] = [dictionary["Media"]["title"]]

		# Define media item as the media for media that has no media item list
		if dictionary["Media"]["States"]["series_media"] == False or dictionary["Media"]["States"]["Media item list"] == False:
			dictionary["Media"]["item"] = dictionary["Media"].copy()

		# Create "Watched" folder
		dictionary["Media"]["item"]["folders"]["watched"] = {
			"root": dictionary["Media"]["item"]["folders"]["root"] + self.language_texts["watched, title()"] + "/"
		}

		self.Folder.Create(dictionary["Media"]["item"]["folders"]["watched"]["root"])

		# Create "Entry list.txt" file inside "Watched" folder
		dictionary["Media"]["item"]["folders"]["watched"]["entry_list"] = dictionary["Media"]["item"]["folders"]["watched"]["root"] + "Entry list.txt"
		self.File.Create(dictionary["Media"]["item"]["folders"]["watched"]["entry_list"])

		# Create "Comments" folder
		dictionary["Media"]["item"]["folders"]["comments"] = {
			"root": dictionary["Media"]["item"]["folders"]["root"] + self.JSON.Language.language_texts["comments, title()"] + "/"
		}

		self.Folder.Create(dictionary["Media"]["item"]["folders"]["comments"]["root"])

		# Define media comments folder comments file
		dictionary["Media"]["item"]["folders"]["comments"]["comments"] = dictionary["Media"]["item"]["folders"]["comments"]["root"] + self.JSON.Language.texts["comments, title()"]["en"] + ".json"
		self.File.Create(dictionary["Media"]["item"]["folders"]["comments"]["comments"])

		# Define media item folders
		if dictionary["Media"]["States"]["series_media"] == True and dictionary["Media"]["States"]["single_unit"] == False:
			dictionary["Media"]["item"]["folders"]["titles"] = {
				"root": dictionary["Media"]["item"]["folders"]["root"] + self.JSON.Language.language_texts["titles, title()"] + "/",
			}

			self.Folder.Create(dictionary["Media"]["item"]["folders"]["titles"]["root"])

			for language in self.languages["small"]:
				full_language = self.languages["full"][language]

				# Define episode titles file
				dictionary["Media"]["item"]["folders"]["titles"][language] = dictionary["Media"]["item"]["folders"]["titles"]["root"] + full_language + ".txt"
				self.File.Create(dictionary["Media"]["item"]["folders"]["titles"][language])

			if dictionary["Media"]["States"]["video"] == True:
				# Define ids file
				dictionary["Media"]["item"]["folders"]["titles"]["ids"] = dictionary["Media"]["item"]["folders"]["titles"]["root"] + self.JSON.Language.language_texts["ids, title()"] + ".txt"
				self.File.Create(dictionary["Media"]["item"]["folders"]["titles"]["ids"])

			# Update "Playlist.json" file for video media type
			if dictionary["Media"]["States"]["video"] == True and dictionary["Media"]["States"]["Media item list"] == True:
				# Get ID (origin location) from link
				if self.language_texts["origin_location"] in dictionary["Media"]["item"]["details"] and dictionary["Media"]["item"]["details"][self.language_texts["origin_location"]] == "?":
					dictionary["Media"]["item"]["details"][self.language_texts["origin_location"]] = dictionary["Media"]["item"]["details"][self.JSON.Language.language_texts["link, title()"]].split("list=")[-1]

				dictionary["Media"]["item"]["folders"]["playlist"] = dictionary["Media"]["item"]["folders"]["root"] + "Playlist.json"
				self.File.Create(dictionary["Media"]["item"]["folders"]["playlist"])

				if self.File.Contents(dictionary["Media"]["item"]["folders"]["playlist"])["lines"] == [] and dictionary["Media"]["item"]["details"][self.language_texts["origin_location"]] != "?":
					# Get playlist information
					dictionary["Media"]["item"]["playlist"] = self.Get_YouTube_Information("playlist", dictionary["Media"]["item"]["details"][self.language_texts["origin_location"]])

					# Define playlist date variable
					dictionary["Media"]["item"]["playlist"]["Time"] = self.Date.From_String(dictionary["Media"]["item"]["playlist"]["Time"])
					playlist_date = dictionary["Media"]["item"]["playlist"]["Time"]

					# Get the first video date
					video_id = self.File.Contents(dictionary["Media"]["item"]["folders"]["titles"]["root"] + self.JSON.Language.language_texts["ids, title()"] + ".txt")["lines"][0]
					video_date = self.Date.From_String(self.Get_YouTube_Information("video", video_id)["Time"])

					# If the first video date is older than playlist creation date
					# Define the playlist time as the video date
					if video_date["date"] < playlist_date["date"]:
						dictionary["Media"]["item"]["playlist"]["Time"] = video_date

					# Update "Date" key of media item details
					dictionary["Media"]["item"]["details"][self.Date.language_texts["start_date"]] = self.Date.To_String(dictionary["Media"]["item"]["playlist"]["Time"]["date"].astimezone(), self.Date.language_texts["date_time_format"])

					# Update "Year" key of media item details
					dictionary["Media"]["item"]["details"][self.Date.language_texts["year, title()"]] = dictionary["Media"]["item"]["playlist"]["Time"]["year"]

					dictionary["Media"]["item"]["playlist"]["Time"] = dictionary["Media"]["item"]["playlist"]["Time"]["date"]

					# Update media item details dictionary
					self.File.Edit(dictionary["Media"]["item"]["folders"]["details"], self.Text.From_Dictionary(dictionary["Media"]["item"]["details"]), "w")

					# Update "Playlist.json" file
					self.JSON.Edit(dictionary["Media"]["item"]["folders"]["playlist"], dictionary["Media"]["item"]["playlist"])

				if self.File.Contents(dictionary["Media"]["item"]["folders"]["playlist"])["lines"] != [] and dictionary["Media"]["item"]["details"][self.language_texts["origin_location"]] != "?":
					# Get playlist from JSON file
					dictionary["Media"]["item"]["playlist"] = self.JSON.To_Python(dictionary["Media"]["item"]["folders"]["playlist"])

		folder = dictionary["Media"]["item"]["folders"]["comments"]

		# Define the comments dictionary as the template
		self.dictionaries["Comments"] = deepcopy(self.template)

		# If the "Comments" key is inside the numbers dictionary, remove it
		if "Comments" in self.dictionaries["Comments"]["Numbers"]:
			self.dictionaries["Comments"]["Numbers"].pop("Comments")

		# If the comments file is empty or has no entries
		if self.File.Contents(folder["comments"])["lines"] == [] or self.JSON.To_Python(folder["comments"])["Entries"] == []:
			# If the media type is video
			if dictionary["Media"]["States"]["video"] == True:
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
			if dictionary["Media"]["States"]["video"] == True:
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

		if dictionary["Media"]["States"]["video"] == True:
			# If the channel inside the comments dictionary file is not empty, define it as the dictionary channel
			if file_dictionary["Channel"] != {}:
				self.dictionaries["Comments"]["Channel"] = file_dictionary["Channel"]

			# If the channel inside the comments dictionary is empty, define it as the channel gotten from the "Channel.json" file
			if self.dictionaries["Comments"]["Channel"] == {}:
				self.dictionaries["Comments"]["Channel"] = dictionary["Media"]["channel"]

			# If the playlist exists inside the dictionary
			if "Playlist" in self.dictionaries["Comments"]:
				# And the playlist inside the comments dictionary file is not empty, define it as the dictionary playlist
				if file_dictionary["Playlist"] != {}:
					self.dictionaries["Comments"]["Playlist"] = file_dictionary["Playlist"]

				# If the playlist inside the comments dictionary file is empty, define it as the playlist gotten from the "Playlist.json" file
				if file_dictionary["Playlist"] == {}:
					self.dictionaries["Comments"]["Playlist"] = dictionary["Media"]["item"]["playlist"]

		# Update the total comments number with the length of the entries list
		self.dictionaries["Comments"]["Numbers"]["Total"] = len(self.dictionaries["Comments"]["Entries"])

		# Define "Comments" dictionary inside the media item dictionary
		dictionary["Media"]["item"]["Comments"] = deepcopy(self.dictionaries["Comments"])

		# Update "Comments.json" file
		self.JSON.Edit(folder["comments"], self.dictionaries["Comments"])

		# Create "Files" folder file inside "Watched" folder
		dictionary["Media"]["item"]["folders"]["watched"]["files"] = {
			"root": dictionary["Media"]["item"]["folders"]["watched"]["root"] + self.File.language_texts["files, title()"] + "/"
		}

		self.Folder.Create(dictionary["Media"]["item"]["folders"]["watched"]["files"]["root"])

		# Create "Entries.json" file inside "Watched" folder
		dictionary["Media"]["item"]["folders"]["watched"]["entries"] = dictionary["Media"]["item"]["folders"]["watched"]["root"] + "Entries.json"
		self.File.Create(dictionary["Media"]["item"]["folders"]["watched"]["entries"])

		# Define the watched dictionary as the template
		self.dictionaries["Watched"] = deepcopy(self.template)

		# Get watched dictionary from file if the dictionary is not empty and has entries
		if self.File.Contents(dictionary["Media"]["item"]["folders"]["watched"]["entries"])["lines"] != [] and self.JSON.To_Python(dictionary["Media"]["item"]["folders"]["watched"]["entries"])["Entries"] != []:
			self.dictionaries["Watched"] = self.JSON.To_Python(dictionary["Media"]["item"]["folders"]["watched"]["entries"])

		# Get the total comment number from the comments dictionary
		self.dictionaries["Watched"]["Numbers"]["Comments"] = self.dictionaries["Comments"]["Numbers"]["Total"]

		# Update the number of entries with the length of the entries list
		self.dictionaries["Watched"]["Numbers"]["Total"] = len(self.dictionaries["Watched"]["Entries"])

		# Define "Watched" dictionary inside the media item dictionary
		dictionary["Media"]["item"]["Watched"] = deepcopy(self.dictionaries["Watched"])

		# Write the default or file dictionary into the "Watched.json" file
		self.JSON.Edit(dictionary["Media"]["item"]["folders"]["watched"]["entries"], self.dictionaries["Watched"])

		# Define the media item files
		dictionary["Media"]["item"]["folders"]["dates"] = dictionary["Media"]["item"]["folders"]["root"] + self.Date.language_texts["dates, title()"] + ".txt"
		self.File.Create(dictionary["Media"]["item"]["folders"]["dates"])

		# Define the episodes dictionary
		if dictionary["Media"]["States"]["series_media"] == True:
			dictionary["Media"]["item"]["episodes"] = {
				"number": 0,
				"titles": {
					"files": {}
				}
			}

			# Define episode number name as "EP"
			dictionary["Media"]["episode"].update({
				"separator": "EP"
			})

			# Or custom episode number name
			if self.language_texts["episode_number_name"] in dictionary["Media"]["details"]:
				dictionary["Media"]["episode"]["separator"] = dictionary["Media"]["details"][self.language_texts["episode_number_name"]]

			if self.language_texts["episode_number_name"] in dictionary["Media"]["item"]["details"]:
				dictionary["Media"]["episode"]["separator"] = dictionary["Media"]["item"]["details"][self.language_texts["episode_number_name"]]

			if dictionary["Media"]["States"]["video"] == True:
				dictionary["Media"]["episode"]["separator"] = ""

			if dictionary["Media"]["States"]["video"] == True:
				dictionary["Media"]["item"]["episodes"]["titles"]["files"]["ids"] = dictionary["Media"]["item"]["folders"]["titles"]["ids"]
				dictionary["Media"]["item"]["episodes"]["titles"]["ids"] = self.File.Contents(dictionary["Media"]["item"]["episodes"]["titles"]["files"]["ids"])["lines"]

			# Define episode titles files and lists
			for language in self.languages["small"]:
				full_language = self.languages["full"][language]

				if dictionary["Media"]["States"]["single_unit"] == False:
					# Define episode titles on titles dictionary file
					dictionary["Media"]["item"]["episodes"]["titles"]["files"][language] = dictionary["Media"]["item"]["folders"]["titles"][language]

					# Get language episode titles from file
					dictionary["Media"]["item"]["episodes"]["titles"][language] = self.File.Contents(dictionary["Media"]["item"]["episodes"]["titles"]["files"][language])["lines"]

				# Iterate through episode titles
				if dictionary["Media"]["episode"]["separator"] != "" and dictionary["Media"]["States"]["single_unit"] == False:
					import re

					i = 1
					for episode_title in dictionary["Media"]["item"]["episodes"]["titles"][language]:
						number = str(self.Text.Add_Leading_Zeroes(i))

						separator = dictionary["Media"]["episode"]["separator"]

						if separator == "EP" and self.language_texts["episodic, title()"] not in dictionary["Media"]["details"]:
							dictionary["Media"]["States"]["episodic"] = True

						for alternative_episode_type in self.alternative_episode_types:
							if re.search(alternative_episode_type + " [0-9]{1,2}", episode_title) != None:
								separator = ""

								if self.language_texts["episodic, title()"] not in dictionary["Media"]["details"]:
									dictionary["Media"]["States"]["episodic"] = True

						# Add episode number name to local episode title
						episode_title = separator + number + " " + episode_title

						# Add episode number name to episode titles if the number name is not present
						if separator != "" and number not in dictionary["Media"]["item"]["episodes"]["titles"][language][i - 1]:
							dictionary["Media"]["item"]["episodes"]["titles"][language][i - 1] = episode_title

						i += 1

			if dictionary["Media"]["States"]["single_unit"] == True:
				dictionary["Media"]["episode"]["title"] = dictionary["Media"]["item"]["title"]
				dictionary["Media"]["episode"]["titles"] = dictionary["Media"]["item"]["Titles"]

				for language in self.languages["small"]:
					if language not in dictionary["Media"]["episode"]["titles"]:
						dictionary["Media"]["episode"]["titles"][language] = self.Get_Media_Title(dictionary, item = True)

			if dictionary["Media"]["States"]["single_unit"] == False:
				# Add the episode number to the episode "number" key
				dictionary["Media"]["item"]["episodes"]["number"] = len(dictionary["Media"]["item"]["episodes"]["titles"]["en"])

			# Add the episode number after the "Status" key
			key_value = {
				"key": self.language_texts["episodes, title()"],
				"value": dictionary["Media"]["item"]["episodes"]["number"]
			}

			dictionary["Media"]["item"]["details"] = self.JSON.Add_Key_After_Key(dictionary["Media"]["item"]["details"], key_value, self.language_texts["status, title()"])

			# Update media item details file
			self.File.Edit(dictionary["Media"]["item"]["folders"]["details"], self.Text.From_Dictionary(dictionary["Media"]["item"]["details"]), "w")

		if self.dictionaries["Entries"]["Numbers"]["Total"] == 0:
			dictionary["Media"]["States"]["First entry in year"] = True

		if self.dictionaries["Media Type"][dictionary["media_type"]["plural"]["en"]]["Numbers"]["Total"] == 0:
			dictionary["Media"]["States"]["First media type entry in year"] = True

		# Define media texts to be used in the "Show_Media_Information" root method
		dictionary["Media"]["texts"] = {
			"genders": dictionary["media_type"]["genders"]
		}

		# Define the container, item, and unit texts as the media type (for movies)
		for item_type in ["container", "item", "unit"]:
			dictionary["Media"]["texts"][item_type] = dictionary["media_type"]["singular"].copy()

		dictionary["Media"]["item"]["Type"] = {}

		# Define the item type
		if self.JSON.Language.language_texts["type, title()"] in dictionary["Media"]["item"]["details"]:
			dictionary["Media"]["item"]["Type"] = dictionary["Media"]["item"]["details"][self.JSON.Language.language_texts["type, title()"]]

		# Define the container, item, and unit for series media
		if dictionary["Media"]["States"]["series_media"] == True:
			# Define the unit text as the "episode" text per language
			dictionary["Media"]["texts"]["unit"] = {}

			for language in self.languages["small"]:
				dictionary["Media"]["texts"]["unit"][language] = self.texts["episode"][language]

			if dictionary["Media"]["States"]["Media item list"] == True and dictionary["Media"]["item"]["title"] != dictionary["Media"]["title"]:
				dictionary["Media"]["texts"]["item"] = {}

			if dictionary["Media"]["item"]["Type"] != {}:
				for key in self.secondary_types:
					# If the key is inside the "language_texts" dictionary of the Language class, use it as the list
					if key in self.JSON.Language.language_texts:
						texts_list = self.JSON.Language

					# If the key is inside the "language_texts" dictionary of "Watch_History"
					if key in self.language_texts:
						texts_list = self

					singular_type = key
					plural_type = key + "s"

					# Define the singular text
					if key in texts_list.language_texts:
						singular_type = texts_list.language_texts[key].title()

					# Define the plural text
					if key + "s" in texts_list.language_texts:
						plural_type = texts_list.language_texts[key + "s"].title()

					if dictionary["Media"]["item"]["Type"] == singular_type:
						dictionary["Media"]["item"]["Type"] = {}

						for language in self.languages["small"]:
							text = singular_type

							if key in texts_list.texts:
								text = texts_list.texts[key][language]

							dictionary["Media"]["texts"]["item"][language] = text
							dictionary["Media"]["texts"]["unit"][language] = text
							dictionary["Media"]["item"]["Type"][language] = text

			# Define the item text as the "season" text for media that have a media item list
			if dictionary["Media"]["States"]["Media item list"] == True and dictionary["Media"]["item"]["title"] != dictionary["Media"]["title"] and dictionary["Media"]["texts"]["item"] == {}:
				for language in self.languages["small"]:
					dictionary["Media"]["texts"]["item"][language] = self.texts["season"][language]

					if dictionary["Media"]["States"]["single_unit"] == True:
						dictionary["Media"]["texts"]["item"][language] = self.texts["episode"][language]

			# Define the container, item, and unit texts for video series media
			if dictionary["Media"]["States"]["video"] == True:
				for language in self.languages["small"]:
					dictionary["Media"]["texts"]["container"][language] = self.texts["youtube_channel"][language]
					dictionary["Media"]["texts"]["item"][language] = self.texts["youtube_video_serie"][language]
					dictionary["Media"]["texts"]["unit"][language] = self.texts["video"][language]

			if dictionary["Media"]["item"]["Type"] == {}:
				dictionary["Media"]["item"]["Type"] = dictionary["Media"]["texts"]["item"]

		dict_ = deepcopy(dictionary["Media"]["texts"])

		# Define media texts by item and gender
		for text_type in ["the", "this", "of"]:
			for key in dict_:
				if key != "genders":
					if text_type + "_" + key not in dictionary["Media"]["texts"]:
						dictionary["Media"]["texts"][text_type + "_" + key] = {}

					for language in self.languages["small"]:
						if dictionary["Media"]["texts"][key][language] not in [self.texts["season"][language], self.texts["youtube_video_serie"][language]]:
							item_text = dictionary["media_type"]["genders"][language][text_type]

						if dictionary["Media"]["texts"][key][language] in [self.texts["season"][language], self.texts["youtube_video_serie"][language]]:
							for gender_key in dict_["genders"][language]:

								gender = dict_["genders"][language][gender_key]

								if text_type == gender_key:
									item_text = self.media_types["genders"][language]["feminine"][gender_key]

						text = dictionary["Media"]["texts"][key][language].lower()

						if "youtube" in text:
							text = text.replace("youtube", "YouTube")

						dictionary["Media"]["texts"][text_type + "_" + key][language] = item_text + " " + text

		# Add "Christmas special" text to unit text
		if dictionary["Media"]["States"]["video"] == False and self.Today_Is_Christmas == True:
			dict_ = {}

			for language in self.languages["small"]:
				dict_[language] = self.texts["christmas_special_{}"][language].format(dictionary["Media"]["texts"]["unit"][language])

			dictionary["Media"]["texts"]["unit"] = dict_

		if self.language_texts["replace_title"] in dictionary["Media"]["item"]["details"]:
			dictionary["Media"]["States"]["Replace title"] = True

		return dictionary

	def Select_Media_Type_And_Media(self, options = None, watch = False, select_media_item = False):
		dictionary = {
			"media_type": {
				"select": True,
				"status": [
					self.texts["watching, title()"]["en"],
					self.texts["re_watching, title()"]["en"]
				]
			},
			"Media": {
				"select": True,
				"list": {}
			}
		}

		if options != None:
			dictionary = self.Define_Options(dictionary, options)

		if dictionary["media_type"]["select"] == True:
			dictionary["media_type"] = self.Select_Media_Type(dictionary["media_type"])

		if dictionary["Media"]["select"] == True:
			dictionary["Media"] = self.Select_Media(dictionary, watch = watch, select_media_item = select_media_item)["Media"]

		return dictionary

	def Define_Media_Titles(self, dictionary, item = False):
		media = dictionary["Media"]

		if item == True:
			media = dictionary["Media"]["item"]

		if self.File.Exist(media["folders"]["details"]) == True:
			media["details"] = self.File.Dictionary(media["folders"]["details"])

			if self.JSON.Language.language_texts["original_name"] not in media["details"]:
				text = self.JSON.Language.language_texts["original_name"] + ": {}" + "\n" + self.language_texts["episode, title()"] + ": None"
				text = text.format(media["folders"]["details"].split("/")[-2])
				self.File.Edit(media["folders"]["details"], text, "w")

				media["details"] = self.File.Dictionary(media["folders"]["details"])

			# Define titles key
			media["Titles"] = {
				"Original": media["details"][self.JSON.Language.language_texts["original_name"]],
				"Sanitized": media["details"][self.JSON.Language.language_texts["original_name"]],
			}

			media["Titles"]["Language"] = media["Titles"]["Original"]

			# If media type is "Animes" or the "romanized_name" key exists inside the media details, define the romanized name and ja name
			if dictionary["media_type"]["plural"]["en"] == self.texts["animes, title()"]["en"] or self.language_texts["romanized_name"] in media["details"]:
				if self.language_texts["romanized_name"] in media["details"]:
					media["Titles"]["Romanized"] = media["details"][self.language_texts["romanized_name"]]
					media["Titles"]["Language"] = media["Titles"]["Romanized"]

				if "Romanized" in media["Titles"]:
					media["Titles"]["Sanitized"] = media["Titles"]["Romanized"]

				media["Titles"]["ja"] = media["details"][self.JSON.Language.language_texts["original_name"]]

			if " (" in media["Titles"]["Original"] and " (" not in media["Titles"]["Language"]:
				media["Titles"]["Language"] = media["Titles"]["Language"] + " (" + media["Titles"]["Original"].split(" (")[-1]

				if self.user_language in media["Titles"]:
					media["Titles"][self.user_language] = media["Titles"][self.user_language] + " (" + media["Titles"]["Original"].split(" (")[-1]

			# Define media titles per language
			for language in self.languages["small"]:
				language_name = self.JSON.Language.texts["language_name"][language][self.user_language]

				for key in media["details"]:
					if language_name == key:
						media["Titles"][language] = media["details"][language_name]

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
			titles = dictionary["Media"]["item"]["Titles"]

		if episode == True:
			titles = dictionary["Media"]["episode"]["titles"]

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

		title = self.Sanitize(title, restricted_characters = True)

		return title

	def Show_Media_Title(self, dict_, media_item = False):
		self.media_item = media_item

		media = dict_["Media"]

		if self.media_item == True:
			media = dict_["Media"]["item"]	

		if media["Titles"]["Language"] == media["Titles"]["Original"]:
			print(media["Titles"]["Original"])

			if dict_["Media"]["States"]["video"] == True and self.media_item == False:				
				print()
				print(self.Text.Capitalize(dict_["Media"]["texts"]["item"][self.user_language]) + ":")
				print(dict_["Media"]["item"]["title"])

		if media["Titles"]["Language"] != media["Titles"]["Original"]:
			print("\t" + media["Titles"]["Original"])
			print("\t" + media["Titles"]["Language"])

			for language in self.languages["small"]:
				language_name = self.JSON.Language.texts["language_name"][language][self.user_language]

				if language in media["Titles"] and media["Titles"][language] != media["Titles"]["Original"] and media["Titles"][language] != media["Titles"]["Language"]:
					print("\t" + media["Titles"][language])

	def Define_States_Dictionary(self, dictionary):
		states_dictionary = {
			"States": {},
			"Texts": {}
		}

		# Define keys for the states
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
			if dictionary["Media"]["States"][key] == True:
				if key not in state_texts:
					key = key.capitalize()

				# If key has a different state text, get it
				if key in state_texts:
					key = state_texts[key]

				# Define the state as true
				state = True

				# If the key is the "Re-watched" key, get its state dictionary
				if key == "Re-watched":
					state = {
						"Times": dictionary["Media"]["episode"]["re_watched"]["times"]
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
						if dictionary["Media"]["States"]["series_media"] == True:
							unit = dictionary["Media"]["texts"]["unit"][language] + " " + self.JSON.Language.texts["of, neutral"][language] + " " + dictionary["Media"]["texts"]["container"][language].lower()

						# Define the language text as the "first_{}_in_year" formatted with the media unit text
						if key == "First media type entry in year":
							language_text = self.JSON.Language.texts["first_{}_in_year"][language].format(unit)

						# If the media is completed
						if key == "Completed media":
							# Define the "the text" as the "the" text and the container
							the_text = dictionary["Media"]["texts"]["genders"][language]["the"] + " " + dictionary["Media"]["texts"]["container"][language].lower()

						# If the media item is completed
						if key == "Completed media item":
							# Define the "the text" as the "the" text plus the item text, plus the gender "of" text, plus the container text
							the_text = self.media_types["genders"][language]["feminine"]["the"] + " " + dictionary["Media"]["texts"]["item"][language] + " " + dictionary["Media"]["texts"]["genders"][language]["of"] + " " + dictionary["Media"]["texts"]["container"][language].lower()

							if dictionary["Media"]["item"]["title"] == dictionary["Media"]["title"]:
								if dictionary["media_type"]["plural"]["en"] != self.texts["videos, title()"]["en"]:
									the_text = the_text.replace(dictionary["Media"]["texts"]["item"][language], self.texts["season"][language])

								if dictionary["media_type"]["plural"]["en"] == self.texts["videos, title()"]["en"]:
									the_text = the_text.replace(dictionary["Media"]["texts"]["item"][language], self.texts["series"][language])

							if dictionary["Media"]["States"]["single_unit"] == True:
								the_text = the_text.replace(self.media_types["genders"][language]["feminine"]["the"], self.media_types["genders"][language]["masculine"]["the"])

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
						text += dictionary["Media"]["episode"]["re_watched"]["re_watched_text"][language] + " (" + str(dictionary["Media"]["episode"]["re_watched"]["times"]) + "x)"

					# Define the state text per language
					states_dictionary["Texts"][key][language] = text

		return states_dictionary

	def Get_Language_Status(self, status):
		return_english = False

		if status in self.texts["watching_statuses, type: list"][self.user_language]:
			return_english = True

		w = 0
		for english_status in self.texts["watching_statuses, type: list"]["en"]:
			# Return user language status
			if return_english == False and english_status == status:
				status_to_return = self.texts["watching_statuses, type: list"][self.user_language][w]

			# Return English status
			if return_english == True and status == self.texts["watching_statuses, type: list"][self.user_language][w]:
				status_to_return = english_status

			w += 1

		return status_to_return

	def Change_Status(self, dictionary, status = ""):
		if status == "":
			status = self.JSON.Language.language_texts["completed, title()"]

		# Update status key in media details
		dictionary["Media"]["details"][self.language_texts["status, title()"]] = status

		# Update media details file
		self.File.Edit(dictionary["Media"]["folders"]["details"], self.Text.From_Dictionary(dictionary["Media"]["details"]), "w")

		self.Check_Status(dictionary)

	def Check_Status(self, dictionary):
		media_type = dictionary

		if "media_type" in dictionary:
			media_type = dictionary["media_type"]

			self.language_status = dictionary["Media"]["details"][self.language_texts["status, title()"]]

			# Get English watching status from language status of media details
			self.status = self.Get_Language_Status(self.language_status)

		dictionary["json"] = self.JSON.To_Python(media_type["folders"]["media_info"]["info"])

		# Update number of media
		dictionary["json"]["Number"] = len(dictionary["json"]["Titles"])

		# Sort titles list
		dictionary["json"]["Titles"] = sorted(dictionary["json"]["Titles"], key=str.lower)

		titles = []

		if "media_type" not in dictionary:
			titles.extend(dictionary["json"]["Titles"])

		if "media_type" in dictionary:
			titles.append(dictionary["Media"]["title"])

		# Iterate through watching statuses list
		for self.watching_status in self.texts["watching_statuses, type: list"]["en"]:
			for media_title in titles:
				if "media_type" not in dictionary:
					folder = media_type["folders"]["media_info"]["root"] + self.Sanitize_Title(media_title) + "/"
					details_file = folder + self.JSON.Language.language_texts["details, title()"] + ".txt"
					details = self.File.Dictionary(details_file)

					self.language_status = details[self.language_texts["status, title()"]]

					# Get English watching status from language status of media details
					self.status = self.Get_Language_Status(self.language_status)

				# If media status is equal to watching status
				# And media is not in the watching status list, add it to the list
				if self.status == self.watching_status and media_title not in dictionary["json"]["Status"][self.watching_status]:
					dictionary["json"]["Status"][self.watching_status].append(media_title)

				# If media status is not equal to watching status
				# And media is in the wrong watching status list, remove it from the list
				if self.status != self.watching_status and media_title in dictionary["json"]["Status"][self.watching_status]:
					dictionary["json"]["Status"][self.watching_status].remove(media_title)

			# Sort media item list
			dictionary["json"]["Status"][self.watching_status] = sorted(dictionary["json"]["Status"][self.watching_status], key=str.lower)

		# Update media type "Info.json" file
		self.JSON.Edit(media_type["folders"]["media_info"]["info"], dictionary["json"])

		return dictionary

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
		status_list = dictionary["status"].copy()

		# If the status parameter is not None, use it as the status
		if status != None:
			status_list = status

		# If the type of the status list is string, make it a list of only the string
		if type(status_list) == str:
			status_list = [status_list]

		# Get the media type "Info.json" file and read it
		dictionary["json"] = self.JSON.To_Python(dictionary["folders"]["media_info"]["info"])

		# Define the empty media list
		media_list = []

		# Add the media of each watching status to the media list
		for status in status_list:
			media_list.extend(dictionary["json"]["Status"][status])

		# Sort the media list
		media_list = sorted(media_list, key=str.lower)

		return media_list

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
				for id in dict_["Videos"]:
					video = dict_["Videos"][id]

					if "Images" in video:
						video.pop("Images")

					if "Language" in video:
						video.pop("Language")

		return dict_

	def Show_Media_Information(self, dictionary):
		# Show opening this media text
		header_text = dictionary["media_type"]["singular"][self.user_language] + ":"

		if "header_text" in dictionary and "header_text" not in ["", None]:
			header_text = dictionary["header_text"]

		print()
		print(self.large_bar)

		# Show congratulations text if the user finished the media
		if dictionary["Media"]["States"]["Re-watching"] == False and dictionary["Media"]["States"]["Completed media"] == True:
			print()
			print(self.language_texts["congratulations"] + "! :3")

		print()
		print(header_text)

		# Show the title of the media
		self.Show_Media_Title(dictionary)

		print()

		# Show finished watching media texts and times
		if dictionary["Media"]["States"]["Re-watching"] == False and dictionary["Media"]["States"]["Completed media"] == True:
			print(self.language_texts["new_watching_status"] + ":")
			print(dictionary["Media"]["details"][self.language_texts["status, title()"]])
			print()

			if "finished_watching_text" in dictionary["Media"]:
				print(dictionary["Media"]["finished_watching_text"])
				print()

		# Show media episode if the media is series media (not a movie)
		if dictionary["Media"]["States"]["series_media"] == True:
			if dictionary["Media"]["States"]["video"] == True:
				dictionary["media_type"]["genders"][self.user_language]["of_the"] = self.media_types["genders"][self.user_language]["feminine"]["of_the"]

			media_episode_text = "{} {}".format(self.Text.Capitalize(dictionary["Media"]["texts"]["unit"][self.user_language]), dictionary["media_type"]["genders"][self.user_language]["of_the"]) + " "

			if dictionary["Media"]["States"]["video"] == False:
				media_episode_text = media_episode_text.replace(dictionary["media_type"]["genders"][self.user_language]["of_the"], dictionary["Media"]["texts"]["container_text"]["of_the"])

			if dictionary["Media"]["States"]["Media item list"] == False or dictionary["Media"]["States"]["video"] == True:
				text = dictionary["Media"]["texts"]["item"][self.user_language]

				if dictionary["Media"]["States"]["video"] == False:
					text = text.lower()

			else:
				text = dictionary["Media"]["texts"]["container_text"]["container"]

			if text not in media_episode_text:
				media_episode_text += text

			if " " in media_episode_text[-1]:
				media_episode_text = media_episode_text[:-1]

			title = dictionary["Media"]["episode"]["title"]

			if dictionary["Media"]["Language"] != self.user_language:
				title = dictionary["Media"]["episode"]["titles"][self.user_language]

			if dictionary["Media"]["States"]["Re-watching"] == True:
				title += dictionary["Media"]["episode"]["re_watched"]["text"]

			print(media_episode_text + ":")
			print(title)
			print()

			text = self.language_texts["with_{}_title"]

			if dictionary["Media"]["States"]["video"] == True:
				text = self.language_texts["with_{}"]

			text_to_show = self.Text.Capitalize(dictionary["Media"]["texts"]["unit"][self.user_language]) + " " + text.format(dictionary["Media"]["texts"]["container_text"]["the"])

			# Show media episode (episode with media item) if the media has a media item list
			if (
				dictionary["Media"]["States"]["Media item list"] == True and
				dictionary["Media"]["States"]["video"] == False and
				dictionary["Media"]["item"]["title"] != dictionary["Media"]["title"] and
				self.language_texts["single_unit"] not in dictionary["Media"]["item"]["details"] and
				dictionary["Media"]["States"]["Replace title"] == False
			):
				media_episode_text = self.Text.Capitalize(dictionary["Media"]["texts"]["unit"][self.user_language]) + " " + self.language_texts["with_{}"].format(dictionary["Media"]["texts"]["item"][self.user_language])

				print(media_episode_text + ":")

				title = dictionary["Media"]["episode"]["with_item"][self.user_language]

				if dictionary["Media"]["States"]["Re-watching"] == True:
					title += dictionary["Media"]["episode"]["re_watched"]["text"]

				print(title)
				print()

				text_to_show += " " + self.language_texts["and_{}"].format(dictionary["Media"]["texts"]["item"][self.user_language])

				key = "with_title_and_item"

			# Show only media title with episode if the media has no media item list
			if (
				dictionary["Media"]["States"]["Media item list"] == False or
				dictionary["Media"]["States"]["video"] == True or
				dictionary["Media"]["item"]["title"] == dictionary["Media"]["title"] or
				self.language_texts["single_unit"] in dictionary["Media"]["item"]["details"] or
				dictionary["Media"]["States"]["Replace title"] == True
			):
				key = "with_title"

			title = dictionary["Media"]["episode"][key][self.user_language]

			if dictionary["Media"]["States"]["Re-watching"] == True:
				title += dictionary["Media"]["episode"]["re_watched"]["text"]

			if dictionary["Media"]["States"]["Replace title"] == False:
				print(text_to_show + ":")
				print(title)
				print()

		# Show media type
		print(self.language_texts["media_type"] + ":")
		print(dictionary["media_type"]["plural"][self.user_language])

		if dictionary["Media"]["States"]["Re-watching"] == False and dictionary["Media"]["States"]["Completed media item"] == True:
			print()
			print("-")
			print()
			print(self.language_texts["congratulations"] + "! :3")
			print()

			text_to_show = self.language_texts["you_finished_watching"] + " " + dictionary["Media"]["texts"]["this_item"][self.user_language] + " " + dictionary["Media"]["texts"]["container_text"]["of_the"] + ' "' + dictionary["Media"]["Titles"]["Language"] + '"'

			if dictionary["Media"]["States"]["Media item list"] == True and dictionary["Media"]["item"]["title"] == dictionary["Media"]["title"]:
				text_to_show = self.language_texts["you_finished_watching"] + " " + dictionary["Media"]["texts"]["this_container"][self.user_language]

			print(text_to_show + ":")

			self.Show_Media_Title(dictionary, media_item = True)

			if dictionary["Media"]["States"]["Completed media"] == False and dictionary["Media"]["States"]["video"] == False:
				item_type = dictionary["Media"]["item"]["next"]["Type"][self.user_language]

				text = self.language_texts["next_{}_to_watch, feminine"]

				if item_type not in [self.texts["season"][self.user_language], self.texts["series"][self.user_language]]:
					text = self.language_texts["next_{}_to_watch, masculine"]

				print()
				print(text.format(item_type) + ": ")

				dict_ = { 
					"Media": {
						"item": {
							"Titles": dictionary["Media"]["item"]["next"]["Titles"]
						},
						"States": dictionary["Media"]["States"],
						"texts": dictionary["Media"]["texts"]
					}
				}

				self.Show_Media_Title(dict_, media_item = True)

		if "unit" in dictionary["Media"]["episode"]:
			# Show media unit text and episode unit
			print()
			print(self.language_texts["media_unit"] + ":")
			print(dictionary["Media"]["episode"]["unit"])

		if "Entry" in dictionary and "Time" in dictionary["Entry"]:
			text = self.language_texts["when_i_finished_watching"] + " " + dictionary["Media"]["texts"]["the_unit"][self.user_language]

			# Replaced "watching" with "re-watching" text
			if dictionary["Media"]["States"]["Re-watching"] == True:
				text = text.replace(self.language_texts["watching, infinitive"], self.language_texts["re_watching, infinitive"] + " " + dictionary["Media"]["episode"]["re_watched"]["time_text"][self.user_language])

			print()
			print(text + ":")

			if dictionary["Entry"]["Time"] != {}:
				time = self.Date.To_Timezone(dictionary["Entry"]["Time"])["hh:mm DD/MM/YYYY"]

			if dictionary["Entry"]["Time"] == {}:
				time = self.current_year["Number"]

			print(time)

		if (
			"finished_watching_text" in dictionary["Media"]["item"] and dictionary["Media"]["item"]["finished_watching_text"] != "" or

			dictionary["Media"]["States"]["finished_watching"] == True and
			dictionary["Media"]["States"]["First entry in year"] == True or

			dictionary["Media"]["States"]["finished_watching"] == True and
			dictionary["Media"]["States"]["First media type entry in year"] == True or

			"id" in dictionary["Media"]["episode"] or
			"next" in dictionary["Media"]["episode"]
		):
			print()

		if "id" in dictionary["Media"]["episode"]:
			print(self.JSON.Language.language_texts["id, upper()"] + ":")
			print(dictionary["Media"]["episode"]["id"])

			if (
				"next" in dictionary["Media"]["episode"] or
				dictionary["Media"]["States"]["Re-watching"] == False and dictionary["Media"]["States"]["Completed media item"] == True and "finished_watching_text" in dictionary["Media"]["item"]
			):
				print()

		# Show next episode to watch if it is present in the "episode" dictionary
		if "next" in dictionary["Media"]["episode"]:
			text = self.language_texts["next_{}_to_watch, masculine"]

			if dictionary["Media"]["States"]["Re-watching"] == True:
				text = text.replace(self.language_texts["watch"], self.language_texts["re_watch"])

			print(text.format(dictionary["Media"]["texts"]["unit"][self.user_language]) + ": ")
			print(dictionary["Media"]["episode"]["next"])

			if (
				"finished_watching_text" in dictionary["Media"]["item"] and dictionary["Media"]["item"]["finished_watching_text"] != "" or

				dictionary["Media"]["States"]["finished_watching"] == True and
				dictionary["Media"]["States"]["First entry in year"] == True or

				dictionary["Media"]["States"]["finished_watching"] == True and
				dictionary["Media"]["States"]["First media type entry in year"] == True
			):
				print()

		# Show finished watching media (started and finished watching dates) text when user completed a media item
		if (
			dictionary["Media"]["States"]["Re-watching"] == False and
			dictionary["Media"]["States"]["Completed media item"] == True and
			dictionary["Media"]["States"]["single_unit"] == False and 
			"finished_watching_text" in dictionary["Media"]["item"] and
			dictionary["Media"]["item"]["finished_watching_text"] != ""
		):
			print(dictionary["Media"]["item"]["finished_watching_text"])

			if dictionary["Media"]["States"]["finished_watching"] == True and "Old history" not in dictionary:
				print()

		if dictionary["Media"]["States"]["finished_watching"] == True:
			# Show "first watched media in year" text if this is the first media that the user watched in the year
			if dictionary["Media"]["States"]["First entry in year"] == True:
				container = dictionary["Media"]["texts"]["container"][self.user_language]

				if dictionary["Media"]["States"]["video"] == False:
					container = container.lower()

				items = [
					self.media_types["genders"][self.user_language]["feminine"]["this"].title(),
					self.media_types["genders"][self.user_language]["feminine"]["the"] + " " + self.media_types["genders"][self.user_language]["feminine"]["first"] + " "+ self.JSON.Language.language_texts["media"]
				]

				items.append(self.JSON.Language.language_texts["genders, type: dict"]["in"] + " " + self.current_year["Number"])

				print(self.language_texts["{}_is_{}_that_you_watched_{}"].format(*items) + ".")

				if dictionary["Media"]["States"]["First media type entry in year"] == True:
					print()

			# Show "first media type media watched in year" text if this is the first media that the user watched in the year, per media type
			if dictionary["Media"]["States"]["First media type entry in year"] == True:
				container = dictionary["Media"]["texts"]["container"][self.user_language]

				if dictionary["Media"]["States"]["video"] == False:
					container = container.lower()

				if dictionary["Media"]["States"]["series_media"] == True:
					container = dictionary["Media"]["texts"]["unit"][self.user_language] + " " + self.JSON.Language.language_texts["of, neutral"] + " " + container

				if dictionary["Media"]["States"]["First entry in year"] == False:
					items = [
						dictionary["media_type"]["genders"][self.user_language]["this"].title(),
						dictionary["media_type"]["genders"][self.user_language]["the"] + " " + dictionary["media_type"]["genders"][self.user_language]["first"] + " " + container
					]

					items.append(self.JSON.Language.language_texts["genders, type: dict"]["in"] + " " + self.current_year["Number"])

					text = self.language_texts["{}_is_{}_that_you_watched_{}"].format(*items)

				if dictionary["Media"]["States"]["First entry in year"] == True:
					text = self.JSON.Language.language_texts["and_also"].capitalize() + " " + dictionary["media_type"]["genders"][self.user_language]["the"] + " " + dictionary["media_type"]["genders"][self.user_language]["first"] + " " + container

				print(text + ".")

			# If the user finished watching, ask for input beforing ending execution
			if "Old history" not in dictionary:
				print()
				print(self.large_bar)

				self.Input.Type(self.JSON.Language.language_texts["press_enter_when_you_finish_reading_the_info_summary"])
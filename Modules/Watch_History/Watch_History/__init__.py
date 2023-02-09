# Watch History.py

from copy import deepcopy

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
		self.current_year = self.Years.current_year

		# Folders dictionary
		self.folders = self.Folder.Contents(self.folders["notepad"]["networks"]["audiovisual_media_network"]["root"], lower_key = True)["dictionary"]

		# Audiovisual Media Network root files
		self.folders["audiovisual_media_network"]["watch_list"] = self.folders["audiovisual_media_network"]["root"] + "Watch List.txt"

		self.folders["watch_history"]["current_year"] = self.folders["watch_history"][str(self.date["year"])]

	def Define_Lists_And_Dictionaries(self):
		# Lists
		self.media_details_parameters = [
			self.language_texts["original_name"],
			self.language_texts["[language]_name"],
			self.language_texts["year, title()"],
			self.language_texts["has_dub"],
			self.language_texts["status, title()"],
			self.language_texts["origin_type"]
		]

		self.movie_details_parameters = [
			self.language_texts["original_name"],
			self.language_texts["[language]_name"],
			self.language_texts["director, title()"],
			self.language_texts["productor, title()"],
			self.language_texts["director, title()"]
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
			self.language_texts["original_name"]: {
				"select_text": self.language_texts["original_name"],
				"default": "",
			},

			self.language_texts["language_name"][self.user_language]: {
				"select_text": self.language_texts["language_name"][self.user_language],
				"default": {
					"format_name": self.language_texts["original_name"],
				},
			},

			self.language_texts["year, title()"]: {
				"select_text": self.language_texts["year, title()"],
				"default": self.date["year"],
			},
		}

		self.media_details_choice_list_parameters = {
			self.language_texts["status, title()"]: {
				"language_list": self.language_texts["watching_statuses, type: list"],
				"english_list": self.language_texts["watching_statuses, type: list"],
				"select_text": self.language_texts["select_one_watching_status_from_the_status_list"],
			},

			self.language_texts["origin_type"]: {
				"language_list": self.language_texts["origin_types, type: list"],
				"english_list": self.language_texts["origin_types, type: list"],
				"select_text": self.language_texts["select_one_origin_type_from_the_list"],
			},
		}

		self.media_details_yes_or_no_definer_parameters = {
			self.language_texts["has_dub"]: self.language_texts["has_dub"],
		}

		self.media_item_details_parameters = {
			self.language_texts["original_name"]: {
				"mode": "string",
				"select_text": self.language_texts["original_name"],
			},

			self.language_texts["language_name"][self.user_language]: {
				"mode": "string/default-format",
				"select_text": self.language_texts["language_name"][self.user_language],
				"default": {
					"format_name": self.language_texts["original_name"],
					"functions": [
						str,
					],
				},
			},

			self.language_texts["episode, title()"]: {
				"mode": "string/default",
				"select_text": self.language_texts["episode, title()"],
				"default": "None",
			},

			self.language_texts["origin_location"]: {
				"mode": "string/default-format",
				"select_text": self.language_texts["origin_location"],
				"default": {
					"format_name": self.language_texts["original_name"],
					"functions": [
						self.Text.Lower,
						self.Sanitize,
					],
				},
			},
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

		# Iterate through English plural media types list
		i = 0
		for plural_media_type in self.media_types["plural"]["en"]:
			language_media_type = self.media_types["plural"][self.user_language][i]

			# Create media type dictionary
			self.media_types[plural_media_type] = {
				"singular": {},
				"plural": {},
				"texts": {},
				"folders": {},
				"subfolders": {},
				"genders": {},
				"status": [
					self.texts["watching, title()"]["en"],
					self.texts["re_watching, title()"]["en"]
				]
			}

			# Define singular and plural media types
			for language in self.languages["small"]:
				for item in ["singular", "plural"]:
					self.media_types[plural_media_type][item][language] = self.media_types[item][language][i]

			# Define select text for "Videos" media type
			if self.media_types[plural_media_type]["plural"]["en"] == self.texts["videos"]["en"]:
				self.media_types[plural_media_type]["singular"]["select"] = self.language_texts["channel, title()"]
				self.media_types[plural_media_type]["plural"]["select"] = self.language_texts["channels, title()"]

			# Define media type subfolders
			if plural_media_type != self.texts["movies, title()"]["en"]:
				text = "season"

				if plural_media_type == self.texts["videos, title()"]["en"]:
					text = "serie"

				for item in ["singular", "plural"]:
					if item == "plural":
						text += "s"

					self.media_types[plural_media_type]["subfolders"][item] = self.language_texts[text + ", title()"]

				# Define current "season/series" folder
				text = self.media_types[plural_media_type]["subfolders"]["singular"]

				if "{" not in self.language_texts["current_{}"][0]:
					text = text.lower()

				self.media_types[plural_media_type]["subfolders"]["current"] = self.language_texts["current_{}"].format(text)

			# Define genders
			gender = "masculine"

			if plural_media_type == self.texts["series, title()"]["en"]:
				gender = "feminine"

			self.media_types[plural_media_type]["genders"] = self.media_types["genders"][self.user_language][gender]

			# Create folders
			for root_folder in ["Comments", "Media Info", "Watch History"]:
				root_key = root_folder.lower().replace(" ", "_")
				key = plural_media_type.lower().replace(" ", "_")

				if root_folder != "Watch History":
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

					# Create "Episodes.json" file in "Per Media Type" media type folder
					self.folders[root_key]["current_year"]["per_media_type"][key]["episodes"] = self.folders[root_key]["current_year"]["per_media_type"][key]["root"] + "Episodes.json"
					self.File.Create(self.folders[root_key]["current_year"]["per_media_type"][key]["episodes"])

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
				"comments": self.folders["comments"][key],
				"media_info": self.folders["media_info"][key],
				"per_media_type": self.folders["watch_history"]["current_year"]["per_media_type"][key]
			}

			# Define "Info.json" file
			self.media_types[plural_media_type]["folders"]["media_info"]["info"] = self.media_types[plural_media_type]["folders"]["media_info"]["root"] + "Info.json"
			self.File.Create(self.media_types[plural_media_type]["folders"]["media_info"]["info"])

			# Read "Info.json" file
			self.media_types[plural_media_type]["json"] = self.JSON.To_Python(self.media_types[plural_media_type]["folders"]["media_info"]["info"])

			# Check the "watching status" of the media list
			# Add the media inside the correct "watching status" list if it is not there already
			# Remove the media from the wrong "watching status" list if it is there
			self.media_types[plural_media_type] = self.Check_Status(self.media_types[plural_media_type])

			# Add the media number to the media number
			self.media_types["media_list"]["Number"] += self.media_types[plural_media_type]["json"]["Number"]

			# Add the media number to the media type media numbers
			self.media_types["media_list"]["Numbers"][plural_media_type] = self.media_types[plural_media_type]["json"]["Number"]

			# Define media list
			self.media_types[plural_media_type]["media_list"] = []

			self.media_types[plural_media_type]["media_list"] = self.Get_Media_List(self.media_types[plural_media_type])

			add_status = False			

			# Add status to "media list option" list if add_status is True
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

			# Add media list length numbers to media types list to show on select media type
			for language in self.languages["small"]:
				for item in ["singular", "plural"]:
					self.media_types[plural_media_type][item]["show"] = self.media_types[plural_media_type][item][self.user_language] + " (" + str(len(self.media_types[plural_media_type]["media_list"])) + ")"

			self.media_types[plural_media_type]["texts"]["show"] = self.Text.By_Number(self.media_types[plural_media_type]["media_list"], self.media_types[plural_media_type]["singular"]["show"], self.media_types[plural_media_type]["plural"]["show"])

			i += 1

		# Write media types dictionary into "Media Types.json" file
		self.JSON.Edit(self.folders["data"]["types"], self.media_types)

		# Update "Info.json" file on "Media Info" folder
		dictionary = self.JSON.To_Python(self.folders["media_info"]["info"])
		dictionary.update(self.media_types["media_list"])

		self.JSON.Edit(self.folders["media_info"]["info"], dictionary)

	def Define_Registry_Format(self):
		# Define default Episodes dictionary template
		self.template = {
			"Numbers": {
				"Total": 0,
				"Comments": 0
			},
			"Entries": [],
			"Dictionary": {}
		}

		self.episodes = self.template.copy()

		# If Episodes.json is not empty and has entries, get Episodes dictionary from it
		if self.File.Contents(self.folders["watch_history"]["current_year"]["episodes"])["lines"] != [] and self.JSON.To_Python(self.folders["watch_history"]["current_year"]["episodes"])["Entries"] != []:
			self.episodes = self.JSON.To_Python(self.folders["watch_history"]["current_year"]["episodes"])

		self.JSON.Edit(self.folders["watch_history"]["current_year"]["episodes"], self.episodes)

		self.comments = {
			"Numbers": {
				"Total": 0,
				"Years": {},
				"Type": {}
			}
		}

		if self.File.Contents(self.folders["comments"]["comments"])["lines"] != [] and self.JSON.To_Python(self.folders["comments"]["comments"])["Numbers"]["Total"] != 0:
			# Get Comments dictionary from file
			self.comments = self.JSON.To_Python(self.folders["comments"]["comments"])

		# If current year is not inside "year comment numbers" dictionary, add it to the dictionary as zero
		if str(self.date["year"]) not in self.comments["Numbers"]["Years"]:
			self.comments["Numbers"]["Years"][str(self.date["year"])] = 0

		# Define root Media Type Episodes dictionary
		self.media_type_episodes = {}

		# Iterate through English media types list
		for plural_media_type in self.media_types["plural"]["en"]:
			key = plural_media_type.lower().replace(" ", "_")

			# Define default media type dictionary
			self.media_type_episodes[plural_media_type] = deepcopy(self.template)

			# If media type "Episodes.json" is not empty, get media type Episodes dictionary from it
			if self.File.Contents(self.folders["watch_history"]["current_year"]["per_media_type"][key]["episodes"])["lines"] != [] and self.JSON.To_Python(self.folders["watch_history"]["current_year"]["per_media_type"][key]["episodes"])["Entries"] != []:
				self.media_type_episodes[plural_media_type] = self.JSON.To_Python(self.folders["watch_history"]["current_year"]["per_media_type"][key]["episodes"])

			self.JSON.Edit(self.folders["watch_history"]["current_year"]["per_media_type"][key]["episodes"], self.media_type_episodes[plural_media_type])

			if plural_media_type not in self.comments["Numbers"]["Type"]:
				self.comments["Numbers"]["Type"][plural_media_type] = {
					"Total": 0,
					"Years": {}
				}

			# If the current year is not inside the media type year comment number dictionary, add it
			if str(self.date["year"]) not in self.comments["Numbers"]["Type"][plural_media_type]["Years"]:
				self.comments["Numbers"]["Type"][plural_media_type]["Years"][self.date["year"]] = 0

		# Define total comment number as zero
		self.comments["Numbers"]["Total"] = 0

		# Count comment numbers of all years to get total comment number
		for year in self.comments["Numbers"]["Years"]:
			number = self.comments["Numbers"]["Years"][year]

			self.comments["Numbers"]["Total"] += number

		# Update "Comments.json" file with updated Comments dictionary
		self.JSON.Edit(self.folders["comments"]["comments"], self.comments)

	def Remove_Media_Type(self, media_types_list):
		if type(media_types_list) == str:
			media_types_list = [media_types_list]

		media_types = self.media_types.copy()

		for language in self.languages["small"]:
			for item in media_types_list:
				if item in media_types["plural"][language]:
					media_types["plural"][language].remove(item)

				if item in self.folders["media_info"]:
					self.folders["media_info"].pop(item)

		return texts

	def Define_Options(self, dictionary, options):
		for key in options:
			if type(options[key]) == dict:
				if key in dictionary and dictionary[key] != {}:
					for sub_key in dictionary[key]:
						if sub_key in options[key]:
							dictionary[key][sub_key] = options[key][sub_key]

				if key not in dictionary or dictionary[key] == {}:
					dictionary[key] = options[key]

			if type(options[key]) in [str, list]:
				dictionary[key] = options[key]

		return dictionary

	def Select_Media_Type(self, options = None):
		dictionary = {
			"texts": {
				"show": self.language_texts["media_types"],
				"select": self.language_texts["select_one_media_type_to_watch"],
			},
			"list": {
				"en": self.media_types["plural"]["en"].copy(),
				self.user_language: self.media_types["plural"][self.user_language].copy(),
			},
			"status": [
				self.texts["watching, title()"]["en"],
				self.texts["re_watching, title()"]["en"],
			],
		}

		# Define media type media numbers
		numbers = self.JSON.To_Python(self.folders["media_info"]["info"])["Numbers"]

		i = 0
		for plural_media_type in self.media_types["plural"]["en"]:
			for language in self.languages["small"]:
				dictionary["list"][language][i] = dictionary["list"][language][i] + " (" + str(numbers[plural_media_type]) + ")"

			i += 1

		if options != None:
			dictionary = self.Define_Options(dictionary, options)

		# Select the media type
		if "option" not in dictionary:
			dictionary["option"] = self.Input.Select(dictionary["list"]["en"], dictionary["list"][self.user_language], show_text = dictionary["texts"]["show"], select_text = dictionary["texts"]["select"])["option"]
			dictionary["option"] = dictionary["option"].split(" (")[0]

		# Get selected media type dictionary from media types dictionary
		dictionary.update(self.media_types[dictionary["option"]])

		return dictionary

	def Select_Media(self, options = None, item = False, watch = False):
		self.item = item

		dictionary = {}

		if options != None:
			dictionary = self.Define_Options(dictionary, options)

		media = dictionary["media"]

		if self.item == True:
			media = dictionary["media"]["item"]

		dictionary["texts"] = dictionary["media_type"]["texts"]

		# Define select text
		text = dictionary["media_type"]["singular"][self.user_language]

		if "select" in dictionary["media_type"]["singular"]:
			text = dictionary["media_type"]["singular"]["select"]

		dictionary["texts"]["select"] = self.language_texts["select_{}_to_watch"].format(dictionary["media_type"]["genders"]["a"] + " " + text)

		# Select media
		if "title" not in media:
			language_options = dictionary["media_type"]["media_list"]

			if "media_list_option" in dictionary["media_type"]:
				language_options = dictionary["media_type"]["media_list_option"]

			media.update({
				"title": self.Input.Select(dictionary["media_type"]["media_list"], language_options = language_options, show_text = dictionary["texts"]["show"], select_text = dictionary["texts"]["select"])["option"],
			})

		sanitized_title = self.Sanitize_Title(media["title"])

		# Define media info and local media folder
		if "folders" in media:
			if "root" not in media["folders"]:
				media["folders"].update({
					"root": dictionary["media_type"]["folders"]["media_info"]["root"] + self.Sanitize(sanitized_title, restricted_characters = True) + "/",
				})

			media["folders"].update({
				"media": {
					"root": dictionary["media"]["folders"]["media"]["root"]
				},
				"media_type_comments": {
					"root": dictionary["media"]["folders"]["media_type_comments"]["root"] + self.Sanitize(sanitized_title, restricted_characters = True) + "/"
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
					"root": self.Folder.folders["root"]["mídias"]["root"] + self.Sanitize(sanitized_title, restricted_characters = True) + "/"
				},
				"media_type_comments": {
					"root": self.folders["comments"][dictionary["media_type"]["plural"]["en"].lower()]["root"] + self.Sanitize(sanitized_title, restricted_characters = True) + "/"
				}
			}

			# Create folders
			for key in media["folders"]:
				folder = media["folders"][key]

				if "root" in folder:
					folder = folder["root"]

				self.Folder.Create(folder)

		# Define media text files
		for file_name in ["Details.txt", "Dates.txt"]:
			key = file_name.lower().replace(" ", "_").replace(".txt", "").replace(".json", "")
			extension = "." + file_name.split(".")[-1]

			if "dates" not in key:
				text = self.language_texts[key + ", title()"]

			if "dates" in key:
				text = self.Date.language_texts[key + ", title()"]

			file_name = text + extension

			media["folders"][key] = media["folders"]["root"] + file_name
			self.File.Create(media["folders"][key])

		# Define media details
		media["details"] = self.File.Dictionary(media["folders"]["details"])

		if self.item == False:
			# Define media states dictionary
			states = {
				"remote": False,
				"local": False,
				"hybrid": False,
				"video": False,
				"series_media": True,
				"episodic": False,
				"single_unit": False,
				"media_list": False,
				"re_watching": False,
				"christmas": False,
				"has_dubbing": False,
				"watch_dubbed": False,
				"dubbed_to_title": False,
				"completed": False,
				"completed_item": False,
				"first_episode_in_year": False,
				"first_media_type_episode_in_year": False,
				"finished_watching": False
			}

			if "States" in media:
				media["States"].update(states)

			if "States" not in media:
				media["States"] = states

			if self.Today_Is_Christmas == True:
				media["States"]["christmas"] = True

			# Define origin type state
			for key in ["local", "remote", "hybrid"]:
				if self.language_texts["origin_type"] in media["details"]:
					if media["details"][self.language_texts["origin_type"]] == self.language_texts[key + ", title()"]:
						media["States"][key] = True

			if self.language_texts["origin_type"] not in media["details"]:
				media["States"]["remote"] = True

			# Define video state for videos
			if dictionary["media_type"]["plural"]["en"] == self.texts["videos"]["en"]:
				media["States"]["video"] = True
				media["States"]["episodic"] = False

			if self.language_texts["episodic, title()"] in media["details"]:
				media["States"]["episodic"] = self.Input.Define_Yes_Or_No(media["details"][self.language_texts["episodic, title()"]])

			# Define single unit state
			if self.language_texts["single_unit"] in media["details"]:
				media["States"]["single_unit"] = self.Input.Define_Yes_Or_No(media["details"][self.language_texts["single_unit"]])

			# Define non-series media state for movies
			if dictionary["media_type"]["plural"]["en"] == self.texts["movies"]["en"]:
				media["States"]["series_media"] = False

			if media["States"]["video"] == True:
				dictionary["media"]["folders"]["channel"] = dictionary["media"]["folders"]["root"] + "Channel.json"
				self.File.Create(dictionary["media"]["folders"]["channel"])

				if self.File.Contents(dictionary["media"]["folders"]["channel"])["lines"] == []:
					# Get channel information
					dictionary["media"]["channel"] = self.Get_YouTube_Information("channel", dictionary["media"]["details"]["ID"])

					# Define channel date
					channel_date = self.Date.From_String(dictionary["media"]["channel"]["Time"])

					# Update "Date" key of media details
					dictionary["media"]["details"][self.Date.language_texts["date, title()"]] = self.Date.To_String(channel_date["date"].astimezone(), self.Date.language_texts["date_time_format"])

					# Update "Year" key of media details
					dictionary["media"]["details"][self.Date.language_texts["year, title()"]] = channel_date["year"]

					# Update media details dictionary
					self.File.Edit(dictionary["media"]["folders"]["details"], self.Text.From_Dictionary(dictionary["media"]["details"]), "w")

					# Update "Channel.json" file
					self.JSON.Edit(dictionary["media"]["folders"]["channel"], dictionary["media"]["channel"])

				else:
					# Get channel information
					dictionary["media"]["channel"] = self.JSON.To_Python(dictionary["media"]["folders"]["channel"])

			# Define remote origin for animes or videos media type
			if self.language_texts["remote_origin, title()"] not in dictionary["media"]["details"]:
				if dictionary["media_type"]["plural"]["en"] == self.texts["animes"]["en"]:
					remote_origin = "Animes Vision"

				if dictionary["media_type"]["plural"]["en"] == self.texts["videos"]["en"]:
					remote_origin = "YouTube"

				dictionary["media"]["details"][self.language_texts["remote_origin, title()"]] = remote_origin

			# Define Re-Watching state for Re-Watching status
			if self.language_texts["status, title()"] in media["details"] and media["details"][self.language_texts["status, title()"]] == self.language_texts["re_watching, title()"]:
				media["States"]["re_watching"] = True

			media["episode"] = {
				"title": "",
				"titles": {},
				"sanitized": "",
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
			dictionary = self.Define_Media_Item(dictionary, watch)

		return dictionary

	def Define_Media_Item(self, dictionary, watch = False, media_item = None):
		if dictionary["media"]["States"]["series_media"] == True:
			dictionary["media"]["items"] = {
				"folders": {
					"root": dictionary["media"]["folders"]["root"] + dictionary["media_type"]["subfolders"]["plural"] + "/",
				},
				"number": 0
			}

			if self.Folder.Exist(dictionary["media"]["items"]["folders"]["root"]) == True:
				for name in ["list", "current"]:
					key = name

					if name == "list":
						key = "plural"

					dictionary["media"]["items"]["folders"][name] = dictionary["media"]["items"]["folders"]["root"] + dictionary["media_type"]["subfolders"][key] + ".txt"
					self.File.Create(dictionary["media"]["items"]["folders"][name])

					dictionary["media"]["items"][name] = self.File.Contents(dictionary["media"]["items"]["folders"][name])["lines"]

					if dictionary["media"]["items"][name] != [] and name == "current":
						dictionary["media"]["items"][name] = dictionary["media"]["items"][name][0]

					if name == "list":
						dictionary["media"]["items"]["number"] = len(dictionary["media"]["items"]["list"])

				# Define media item folders
				for name in dictionary["media"]["items"]["list"]:
					name = self.Sanitize_Title(name)

					dictionary["media"]["items"]["folders"][name] = dictionary["media"]["items"]["folders"]["root"] + name + "/"
					self.Folder.Create(dictionary["media"]["items"]["folders"][name])

				# Define current media item
				title = dictionary["media"]["items"]["current"]

				# Has media list
				dictionary["media"]["States"]["media_list"] = True

				# Select video series from channel for video series media
				if dictionary["media"]["States"]["video"] == True:
					show_text = self.Text.Capitalize(self.language_texts["youtube_video_series"])
					select_text = self.language_texts["select_a_youtube_video_series"]

					list_ = dictionary["media"]["items"]["list"].copy()

					for series in dictionary["media"]["items"]["list"].copy():
						folders = {
							"root": dictionary["media"]["items"]["folders"]["root"] + self.Sanitize(series, restricted_characters = True) + "/"
						}

						folders["details"] = folders["root"] + self.language_texts["details, title()"] + ".txt"

						folders["titles"] = {
							"root": folders["root"] + self.JSON.Language.language_texts["titles, title()"] + "/"
						}

						folders["titles"]["file"] = folders["titles"]["root"] + self.full_user_language + ".txt"

						titles = self.File.Contents(folders["titles"]["file"])["lines"]

						details = self.File.Dictionary(folders["details"])

						if titles == [] or details[self.language_texts["episode, title()"]] == titles[-1]:
							list_.remove(series)

					if watch == True and len(dictionary["media"]["items"]["list"]) != 1:
						title = self.Input.Select(list_, show_text = show_text, select_text = select_text)["option"]

				if media_item != None:
					title = media_item

				sanitized_title = self.Sanitize_Title(title)

				# Define media item dictionary with titles and folder
				dictionary["media"]["item"] = {
					"title": title,
					"sanitized": sanitized_title,
					"titles": {},
					"folders": {
						"root": dictionary["media"]["items"]["folders"]["root"] + sanitized_title + "/"
					},
					"number": 0
				}

				dictionary["media"]["episodes"]["number"] = 0

				i = 0
				for name in dictionary["media"]["items"]["list"]:
					if dictionary["media"]["item"]["title"] == name:
						dictionary["media"]["item"]["number"] = i

					# Get media item details file
					folder = dictionary["media"]["items"]["folders"]["root"] + self.Sanitize_Title(name) + "/"
					details_file = folder + self.language_texts["details, title()"] + ".txt"
					details = self.File.Dictionary(details_file)

					# If the item is not a single unit, add its episode number to the root episode number
					if self.language_texts["single_unit"] not in details:
						titles_folder = folder + self.JSON.Language.language_texts["titles, title()"] + "/"
						titles_file = titles_folder + self.languages["full"]["en"] + ".txt"

						dictionary["media"]["episodes"]["number"] += len(self.File.Contents(titles_file)["lines"])

					# If the item is a single unit, add one to the root episode number
					if self.language_texts["single_unit"] in details:
						dictionary["media"]["episodes"]["number"] += 1

					i += 1

				# Add the episode number to the media details
				keys = list(dictionary["media"]["details"].keys())
				values = list(dictionary["media"]["details"].values())

				# Add episodes key or update it if it already exists
				i = 0
				for key in keys.copy():
					if self.language_texts["episodes, title()"] not in keys and key == self.language_texts["status, title()"]:
						keys.insert(i + 1, self.language_texts["episodes, title()"])
						values.insert(i + 1, dictionary["media"]["episodes"]["number"])

					if self.language_texts["episodes, title()"] in keys and key == self.language_texts["episodes, title()"]:
						values[i] = dictionary["media"]["episodes"]["number"]

					i += 1

				# Add media items number key or update it if it already exists
				i = 0
				for key in keys.copy():
					if dictionary["media_type"]["subfolders"]["plural"] not in keys and key == self.language_texts["episodes, title()"]:
						keys.insert(i, dictionary["media_type"]["subfolders"]["plural"])
						values.insert(i, dictionary["media"]["items"]["number"])

					if dictionary["media_type"]["subfolders"]["plural"] in keys and key == dictionary["media_type"]["subfolders"]["plural"]:
						values[i] = dictionary["media"]["items"]["number"]

					i += 1

				dictionary["media"]["details"] = dict(zip(keys, values))

				# Update media item details file
				self.File.Edit(dictionary["media"]["folders"]["details"], self.Text.From_Dictionary(dictionary["media"]["details"]), "w")

				dictionary = self.Select_Media(dictionary, item = True)

				dictionary["media"]["States"]["single_unit"] = False

				# Define single unit state
				if self.language_texts["single_unit"] in dictionary["media"]["item"]["details"]:
					dictionary["media"]["States"]["single_unit"] = self.Input.Define_Yes_Or_No(dictionary["media"]["item"]["details"][self.language_texts["single_unit"]])

				if dictionary["media"]["States"]["single_unit"] == True:
					dictionary["media"]["item"]["folders"]["media"]["root"] = dictionary["media"]["folders"]["media"]["root"]

			if self.Folder.Exist(dictionary["media"]["items"]["folders"]["root"]) == False:
				dictionary["media"]["States"]["media_list"] = False

		# Define media item as the media for media that has no media list
		if dictionary["media"]["States"]["media_list"] == False or dictionary["media"]["States"]["series_media"] == False:
			dictionary["media"]["item"] = dictionary["media"].copy()

		dictionary["media"]["item"]["folders"]["watched"] = {
			"root": dictionary["media"]["item"]["folders"]["root"] + self.language_texts["watched, title()"] + "/"
		}

		self.Folder.Create(dictionary["media"]["item"]["folders"]["watched"]["root"])

		# Define media item folders
		if dictionary["media"]["States"]["series_media"] == True and dictionary["media"]["States"]["single_unit"] == False:
			for name in ["Comments", "Titles"]:
				key = name.lower().replace(" ", "_")
				name = self.JSON.Language.language_texts[key + ", title()"]

				dictionary["media"]["item"]["folders"][key] = {
					"root": dictionary["media"]["item"]["folders"]["root"] + name + "/",
				}

				self.Folder.Create(dictionary["media"]["item"]["folders"][key]["root"])

				if key == "titles":
					for language in self.languages["small"]:
						full_language = self.languages["full"][language]

						# Define episode titles file
						dictionary["media"]["item"]["folders"]["titles"][language] = dictionary["media"]["item"]["folders"]["titles"]["root"] + full_language + ".txt"
						self.File.Create(dictionary["media"]["item"]["folders"]["titles"][language])

			folder = dictionary["media"]["item"]["folders"]["comments"]

			# Update "Playlist.json" file for video media type
			if dictionary["media"]["States"]["video"] == True and dictionary["media"]["States"]["media_list"] == True:
				if self.language_texts["origin_location"] in dictionary["media"]["item"]["details"] and dictionary["media"]["item"]["details"][self.language_texts["origin_location"]] == "?":
					dictionary["media"]["item"]["details"][self.language_texts["origin_location"]] = dictionary["media"]["item"]["details"][self.JSON.Language.language_texts["link, title()"]].split("list=")[-1]

				dictionary["media"]["item"]["folders"]["playlist"] = dictionary["media"]["item"]["folders"]["root"] + "Playlist.json"
				self.File.Create(dictionary["media"]["item"]["folders"]["playlist"])

				if self.File.Contents(dictionary["media"]["item"]["folders"]["playlist"])["lines"] == [] and dictionary["media"]["item"]["details"][self.language_texts["origin_location"]] != "?":
					# Get playlist information
					dictionary["media"]["item"]["playlist"] = self.Get_YouTube_Information("playlist", dictionary["media"]["item"]["details"][self.language_texts["origin_location"]])

					# Define playlist date variable
					dictionary["media"]["item"]["playlist"]["Time"] = self.Date.From_String(dictionary["media"]["item"]["playlist"]["Time"])
					playlist_date = dictionary["media"]["item"]["playlist"]["Time"]

					# Get the first video date
					video_id = self.File.Contents(dictionary["media"]["item"]["folders"]["titles"]["root"] + self.language_texts["ids"] + ".txt")["lines"][0]
					video_date = self.Date.From_String(self.Get_YouTube_Information("video", video_id)["Time"])

					# If the first video date is older than playlist creation date
					# Define the playlist time as the video date
					if video_date["date"] < playlist_date["date"]:
						dictionary["media"]["item"]["playlist"]["Time"] = video_date

					# Update "Date" key of media item details
					dictionary["media"]["item"]["details"][self.Date.language_texts["date, title()"]] = self.Date.To_String(dictionary["media"]["item"]["playlist"]["Time"]["date"].astimezone(), self.Date.language_texts["date_time_format"])

					# Update "Year" key of media item details
					dictionary["media"]["item"]["details"][self.Date.language_texts["year, title()"]] = dictionary["media"]["item"]["playlist"]["Time"]["year"]

					dictionary["media"]["item"]["playlist"]["Time"] = dictionary["media"]["item"]["playlist"]["Time"]["date"]

					# Update media item details dictionary
					self.File.Edit(dictionary["media"]["item"]["folders"]["details"], self.Text.From_Dictionary(dictionary["media"]["item"]["details"]), "w")

					# Update "Playlist.json" file
					self.JSON.Edit(dictionary["media"]["item"]["folders"]["playlist"], dictionary["media"]["item"]["playlist"])

				if self.File.Contents(dictionary["media"]["item"]["folders"]["playlist"])["lines"] != [] and dictionary["media"]["item"]["details"][self.language_texts["origin_location"]] != "?":
					# Get playlist from JSON file
					dictionary["media"]["item"]["playlist"] = self.JSON.To_Python(dictionary["media"]["item"]["folders"]["playlist"])

		if dictionary["media"]["States"]["series_media"] == False or dictionary["media"]["States"]["single_unit"] == True:
			folder = dictionary["media"]["item"]["folders"]

		# Define media comments folder comments file for media with media list
		folder["comments"] = folder["root"] + self.JSON.Language.texts["comments, title()"]["en"] + ".json"
		self.File.Create(folder["comments"])

		# Define media type comments folder comments file for media with media list
		dictionary["media"]["item"]["folders"]["media_type_comments"]["comments"] = dictionary["media"]["item"]["folders"]["media_type_comments"]["root"] + self.JSON.Language.texts["comments, title()"]["en"] + ".json"
		self.File.Create(dictionary["media"]["item"]["folders"]["media_type_comments"]["comments"])

		dictionaries = {
			"Watched": deepcopy(self.template),
			"Comments": deepcopy(self.template)
		}

		# If comments file is empty or has no entries
		if self.File.Contents(folder["comments"])["lines"] == [] or self.JSON.To_Python(folder["comments"])["Entries"] == []:
			file_dictionary = self.JSON.To_Python(folder["comments"])

			# Define default dictionary
			dictionaries["Comments"] = deepcopy(self.template)
			dictionaries["Comments"]["Numbers"].pop("Comments")

			# If the media type is video
			if dictionary["media"]["States"]["video"] == True:
				# Define default video dictionary with "channel" and "playlist" keys
				dictionaries["Comments"] = {
					"Numbers": {
						"Total": 0,
					},
					"Channel": {},
					"Playlist": {},
					"Entries": [],
					"Dictionary": {}
				}

				# If the media has no media list, remove "Playlist" key from dictionary
				if dictionary["media"]["States"]["media_list"] == False:
					dictionaries["Comments"].pop("Playlist")

				# If the channel dictionary inside the comment file is not empty, define it as the dictionary channel
				if file_dictionary["Channel"] != {}:
					dictionaries["Comments"]["Channel"] = file_dictionary["Channel"]

				# If the playlist exists inside the dictionary and the playlist inside the file dictionary is not empty, define it as the dictionary playlist
				if "Playlist" in dictionaries["Comments"] and file_dictionary["Playlist"] != {}:
					dictionaries["Comments"]["Playlist"] = file_dictionary["Playlist"]

		# Get comments dictionary from file
		if self.File.Contents(folder["comments"])["lines"] != [] and self.JSON.To_Python(folder["comments"])["Entries"] != []:
			dictionaries["Comments"] = self.JSON.To_Python(folder["comments"])

			comments_dictionary = {
				"Numbers": {
					"Total": dictionaries["Comments"]["Number"],
				},
				"Channel": dictionaries["Comments"]["Channel"]
			}

			# If the media has media list, add the "Playlist" key to the dictionary
			if dictionary["media"]["States"]["media_list"] == True:
				comments_dictionary["Playlist"] = dictionaries["Comments"]["Playlist"]

			comments_dictionary.update({
				"Entries": dictionaries["Comments"]["Entries"],
				"Dictionary": dictionaries["Comments"]["Dictionary"]
			})

			dictionaries["Comments"] = comments_dictionary

		# Update number with length of entries list
		dictionaries["Comments"]["Numbers"]["Total"] = len(dictionaries["Comments"]["Entries"])

		self.JSON.Edit(folder["comments"], dictionaries["Comments"])
		self.JSON.Edit(dictionary["media"]["item"]["folders"]["media_type_comments"]["comments"], dictionaries["Comments"])

		# Create "Files" folder file inside "Watched" folder
		dictionary["media"]["item"]["folders"]["watched"]["files"] = {
			"root": dictionary["media"]["item"]["folders"]["watched"]["root"] + self.File.language_texts["files, title()"] + "/"
		}

		self.Folder.Create(dictionary["media"]["item"]["folders"]["watched"]["files"]["root"])

		# Create "Watched.json" file inside "Watched" folder
		dictionary["media"]["item"]["folders"]["watched"]["watched"] = dictionary["media"]["item"]["folders"]["watched"]["root"] + "Watched.json"
		self.File.Create(dictionary["media"]["item"]["folders"]["watched"]["watched"])

		# Get watched dictionary from file
		if self.File.Contents(dictionary["media"]["item"]["folders"]["watched"]["watched"])["lines"] != [] and self.JSON.To_Python(dictionary["media"]["item"]["folders"]["watched"]["watched"])["Entries"] != []:
			dictionaries["Watched"] = self.JSON.To_Python(dictionary["media"]["item"]["folders"]["watched"]["watched"])

		# Get comment number from comments dictionary
		dictionaries["Watched"]["Numbers"]["Comments"] = dictionaries["Comments"]["Numbers"]["Total"]

		# Update number with length of entries list
		dictionaries["Watched"]["Numbers"]["Total"] = len(dictionaries["Watched"]["Entries"])

		# Write default or file dictionary into "Watched.json" file
		self.JSON.Edit(dictionary["media"]["item"]["folders"]["watched"]["watched"], dictionaries["Watched"])

		# Define media item files
		dictionary["media"]["item"]["folders"]["date"] = dictionary["media"]["item"]["folders"]["root"] + self.Date.language_texts["date, title()"] + ".txt"
		self.File.Create(dictionary["media"]["item"]["folders"]["date"])

		# Define episodes dictionary
		if dictionary["media"]["States"]["series_media"] == True:
			dictionary["media"]["item"]["episodes"] = {
				"number": 0,
				"titles": {
					"files": {}
				}
			}

			# Define episode number name as "EP"
			dictionary["media"]["episode"].update({
				"separator": "EP"
			})

			# Or custom episode number name
			if self.language_texts["episode_number_name"] in dictionary["media"]["details"]:
				dictionary["media"]["episode"]["separator"] = dictionary["media"]["details"][self.language_texts["episode_number_name"]]

			if self.language_texts["episode_number_name"] in dictionary["media"]["item"]["details"]:
				dictionary["media"]["episode"]["separator"] = dictionary["media"]["item"]["details"][self.language_texts["episode_number_name"]]

			if dictionary["media"]["States"]["video"] == True:
				dictionary["media"]["episode"]["separator"] = ""

			# Define episode titles files and lists
			for language in self.languages["small"]:
				full_language = self.languages["full"][language]

				if dictionary["media"]["States"]["single_unit"] == False:
					# Define episode titles on titles dictionary file
					dictionary["media"]["item"]["episodes"]["titles"]["files"][language] = dictionary["media"]["item"]["folders"]["titles"][language]

					# Get language episode titles from file
					dictionary["media"]["item"]["episodes"]["titles"][language] = self.File.Contents(dictionary["media"]["item"]["episodes"]["titles"]["files"][language])["lines"]

				# Iterate through episode titles
				if dictionary["media"]["episode"]["separator"] != "" and dictionary["media"]["States"]["single_unit"] == False:
					import re

					i = 1
					for episode_title in dictionary["media"]["item"]["episodes"]["titles"][language]:
						number = str(self.Text.Add_Leading_Zeros(i))

						separator = dictionary["media"]["episode"]["separator"]

						for alternative_episode_type in self.alternative_episode_types:
							if re.search(alternative_episode_type + " [0-9]{1,2}", episode_title) != None:
								separator = ""

						# Add episode number name to local episode title
						episode_title = separator + number + " " + episode_title

						# Add episode number name to episode titles if the number name is not present
						if separator != "" and number not in dictionary["media"]["item"]["episodes"]["titles"][language][i - 1]:
							dictionary["media"]["item"]["episodes"]["titles"][language][i - 1] = episode_title

						i += 1

			if dictionary["media"]["States"]["single_unit"] == True:
				dictionary["media"]["episode"]["title"] = dictionary["media"]["item"]["title"]
				dictionary["media"]["episode"]["titles"] = dictionary["media"]["item"]["titles"]

				for language in self.languages["small"]:
					if language not in dictionary["media"]["episode"]["titles"]:
						dictionary["media"]["episode"]["titles"][language] = self.Get_Media_Title(dictionary, item = True)

			if dictionary["media"]["States"]["single_unit"] == False:
				# Add the episode number to the episode "number" key
				dictionary["media"]["item"]["episodes"]["number"] = len(dictionary["media"]["item"]["episodes"]["titles"]["en"])

			# Add the episode number to the media item details
			keys = list(dictionary["media"]["item"]["details"].keys())
			values = list(dictionary["media"]["item"]["details"].values())

			i = 0
			for key in keys.copy():
				if self.language_texts["episodes, title()"] not in keys and key == self.language_texts["status, title()"]:
					keys.insert(i + 1, self.language_texts["episodes, title()"])
					values.insert(i + 1, dictionary["media"]["item"]["episodes"]["number"])

				if self.language_texts["episodes, title()"] in keys and key == self.language_texts["episodes, title()"]:
					values[i] = dictionary["media"]["item"]["episodes"]["number"]

				i += 1

			dictionary["media"]["item"]["details"] = dict(zip(keys, values))

			# Update media item details file
			self.File.Edit(dictionary["media"]["item"]["folders"]["details"], self.Text.From_Dictionary(dictionary["media"]["item"]["details"]), "w")

		if self.episodes["Numbers"]["Total"] == 0:
			dictionary["media"]["States"]["first_episode_in_year"] = True

		if self.media_type_episodes[dictionary["media_type"]["plural"]["en"]]["Numbers"]["Total"] == 0:
			dictionary["media"]["States"]["first_media_type_episode_in_year"] = True

		# Define media texts to be used in the "Show_Media_Information" root method
		dictionary["media"]["texts"] = {
			"genders": dictionary["media_type"]["genders"]
		}

		# Define the container, item, and unit texts as the media type (for movies)
		for item in ["container", "item", "unit"]:
			dictionary["media"]["texts"][item] = dictionary["media_type"]["singular"].copy()

		# Define the container, item, and unit for series media
		if dictionary["media"]["States"]["series_media"] == True:
			# Define the unit text as the "episode" text per language
			dictionary["media"]["texts"]["unit"] = {}

			for language in self.languages["small"]:
				dictionary["media"]["texts"]["unit"][language] = self.texts["episode"][language]

			# Define the item text as the "season" text for media that have a media list
			if dictionary["media"]["States"]["media_list"] == True and dictionary["media"]["item"]["title"] != dictionary["media"]["title"]:
				dictionary["media"]["texts"]["item"] = {}

				for language in self.languages["small"]:
					dictionary["media"]["texts"]["item"][language] = self.texts["season"][language]

					if dictionary["media"]["States"]["single_unit"] == True:
						dictionary["media"]["texts"]["item"][language] = self.texts["episode"][language]

			# Define the container, item, and unit texts for video series media
			if dictionary["media"]["States"]["video"] == True:
				for language in self.languages["small"]:
					dictionary["media"]["texts"]["container"][language] = self.texts["youtube_channel"][language]
					dictionary["media"]["texts"]["item"][language] = self.texts["youtube_video_serie"][language]
					dictionary["media"]["texts"]["unit"][language] = self.texts["video"][language]

		dict_ = dictionary["media"]["texts"].copy()

		for item in ["the", "this", "of"]:
			for key in dict_:
				if key != "genders":
					if item + "_" + key not in dictionary["media"]["texts"]:
						dictionary["media"]["texts"][item + "_" + key] = {}

					for language in self.languages["small"]:
						if dictionary["media"]["texts"][key][language] not in [self.texts["season"][language], self.texts["youtube_video_serie"][language]]:
							item_text = dictionary["media_type"]["genders"][item]

						if dictionary["media"]["texts"][key][language] in [self.texts["season"][language], self.texts["youtube_video_serie"][language]]:
							for gender_key in dict_["genders"]:

								gender = dict_["genders"][gender_key]

								if item == gender_key:
									item_text = self.media_types["genders"][language]["feminine"][gender_key]

						dictionary["media"]["texts"][item + "_" + key][language] = item_text + " " + dictionary["media"]["texts"][key][language]

		# Add "Christmas special" text to unit text
		if dictionary["media"]["States"]["video"] == False and self.Today_Is_Christmas == True:
			dictionary["media"]["texts"]["unit"] = {}

			for language in self.languages["small"]:
				dictionary["media"]["texts"]["unit"][language] = self.texts["christmas_special_{}"][language].format(dictionary["media"]["texts"]["unit"][language])

		return dictionary

	def Select_Media_Type_And_Media(self, options = None, watch = False):
		dictionary = {
			"media_type": {
				"select": True,
				"status": self.texts["watching, title()"]["en"]
			},
			"media": {
				"select": True,
				"list": {}
			}
		}

		if options != None:
			dictionary = self.Define_Options(dictionary, options)

		if dictionary["media_type"]["select"] == True:
			dictionary["media_type"] = self.Select_Media_Type(dictionary["media_type"])

		if dictionary["media"]["select"] == True:
			dictionary["media"] = self.Select_Media(dictionary, watch = watch)["media"]

		return dictionary

	def Define_Media_Titles(self, dictionary, item = False):
		self.item = item

		media = dictionary["media"]

		if self.item == True:
			media = dictionary["media"]["item"]

		if self.File.Exist(media["folders"]["details"]) == True:
			media["details"] = self.File.Dictionary(media["folders"]["details"])

			if self.language_texts["original_name"] not in media["details"]:
				text = self.language_texts["original_name"] + ": {}" + "\n" + self.language_texts["episode, title()"] + ": None"
				text = text.format(media["folders"]["details"].split("/")[-2])
				self.File.Edit(media["folders"]["details"], text, "w")

				media["details"] = self.File.Dictionary(media["folders"]["details"])

			# Define titles key
			media["titles"] = {
				"original": media["details"][self.language_texts["original_name"]],
				"sanitized": media["details"][self.language_texts["original_name"]],
			}

			media["titles"]["language"] = media["titles"]["original"]

			# If media type is "Animes", define romanized name and jp name
			if dictionary["media_type"]["plural"]["en"] == self.texts["animes"]["en"]:
				if self.language_texts["romanized_name"] in media["details"]:
					media["titles"]["romanized"] = media["details"][self.language_texts["romanized_name"]]
					media["titles"]["language"] = media["titles"]["romanized"]

				if "romanized" in media["titles"]:
					media["titles"]["sanitized"] = media["titles"]["romanized"]

				media["titles"]["jp"] = media["details"][self.language_texts["original_name"]]

			if " (" in media["titles"]["original"] and " (" not in media["titles"]["language"]:
				media["titles"]["language"] = media["titles"]["language"] + " (" + media["titles"]["original"].split(" (")[-1]

				if self.user_language in media["titles"]:
					media["titles"][self.user_language] = media["titles"][self.user_language] + " (" + media["titles"]["original"].split(" (")[-1]

			# Define media titles per language
			for language in self.languages["small"]:
				language_name = self.texts["language_name"][language][self.user_language]

				for key in media["details"]:
					if language_name == key:
						media["titles"][language] = media["details"][language_name]

			media["titles"]["language"] = media["titles"]["original"]

			if self.user_language in media["titles"]:
				media["titles"]["language"] = media["titles"][self.user_language]

			if self.user_language not in media["titles"] and dictionary["media_type"]["plural"]["en"] == self.texts["animes"]["en"] and "romanized" in media["titles"]:
				media["titles"]["language"] = media["titles"]["romanized"]

			# Sanitize media title
			media["titles"]["sanitized"] = self.Sanitize_Title(media["titles"]["sanitized"])

		return dictionary

	def Get_Media_Title(self, dictionary, language = None, item = False, episode = False):
		self.item = item

		titles = dictionary["media"]["titles"]

		if self.item == True:
			titles = dictionary["media"]["item"]["titles"]

		if episode == True:
			titles = dictionary["media"]["episode"]["titles"]

		if language not in titles:
			title = titles["original"]

			if dictionary["media_type"]["plural"]["en"] == self.texts["animes"]["en"] and "romanized" in titles:
				title = titles["romanized"]

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

	def Show_Media_Title(self, dictionary, media_item = False):
		self.media_item = media_item

		media = dictionary["media"]

		if self.media_item == True:
			media = dictionary["media"]["item"]	

		if media["titles"]["language"] == media["titles"]["original"]:
			print(media["titles"]["original"])

			if dictionary["media"]["States"]["video"] == True and self.media_item == False:				
				print()
				print(self.Text.Capitalize(dictionary["media"]["texts"]["item"][self.user_language]) + ":")
				print(dictionary["media"]["item"]["title"])

		if media["titles"]["language"] != media["titles"]["original"]:
			print("\t" + media["titles"]["original"])
			print("\t" + media["titles"]["language"])

			for language in self.languages["small"]:
				language_name = self.texts["language_name"][language][self.user_language]

				if language in media["titles"] and media["titles"][language] != media["titles"]["original"]:
					print("\t" + media["titles"][language])

	def Define_States_Dictionary(self, dictionary):
		dict_ = {}

		keys = [
			"re_watching",
			"christmas",
			"watch_dubbed",
			"first_episode_in_year",
			"first_media_type_episode_in_year"
		]

		for key in keys:
			if dictionary["media"]["States"][key] == True:
				if key == "watch_dubbed":
					key = "dubbed"

				state = True

				if key == "re_watching":
					key = "re_watched"

					state = {
						"Times": dictionary["media"]["episode"]["re_watched"]["times"]
					}

				key = key.title()

				dict_[key] = state

		return dict_

	def Get_Language_Status(self, status):
		return_english = False

		if status in self.texts["watching_statuses, type: list"][self.user_language]:
			return_english = True

		w = 0
		for watching_status in self.texts["watching_statuses, type: list"]["en"]:
			if return_english == False and watching_status == status:
				status_to_return = self.texts["watching_statuses, type: list"][self.user_language][w]

			if return_english == True and status == self.texts["watching_statuses, type: list"][self.user_language][w]:
				status_to_return = watching_status

			w += 1

		return status_to_return

	def Change_Status(self, dictionary, status):
		# Update status key in media details
		dictionary["media"]["details"][self.language_texts["status, title()"]] = status

		# Update media details file
		self.File.Edit(dictionary["media"]["folders"]["details"], self.Text.From_Dictionary(dictionary["media"]["details"]), "w")

		self.Check_Status(dictionary)

	def Check_Status(self, dictionary):
		media_type = dictionary

		if "media_type" in dictionary:
			media_type = dictionary["media_type"]

			self.language_status = dictionary["media"]["details"][self.language_texts["status, title()"]]

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
			titles.append(dictionary["media"]["title"])

		# Iterate through watching statuses list
		for self.watching_status in self.texts["watching_statuses, type: list"]["en"]:
			for media_title in titles:
				if "media_type" not in dictionary:
					folder = media_type["folders"]["media_info"]["root"] + self.Sanitize_Title(media_title) + "/"
					details_file = folder + self.language_texts["details, title()"] + ".txt"
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

			# Sort media list
			dictionary["json"]["Status"][self.watching_status] = sorted(dictionary["json"]["Status"][self.watching_status], key=str.lower)

		# Update media type "Info.json" file
		self.JSON.Edit(media_type["folders"]["media_info"]["info"], dictionary["json"])

		return dictionary

	def Get_Media_List(self, dictionary, status = None):
		# Get status list
		status_list = dictionary["status"].copy()

		if status != None:
			status_list = status

		# Define empty media list
		media_list = []

		if type(status_list) == str:
			status_list = [status_list]

		# Get media type "Info.json" file and read it
		dictionary["json"] = self.JSON.To_Python(dictionary["folders"]["media_info"]["info"])

		# Add the media of each watching status to the media list
		for status in status_list:
			media_list.extend(dictionary["json"]["Status"][status])

		# Sort media list
		media_list = sorted(media_list, key=str.lower)

		return media_list

	def Get_YouTube_Information(self, name, link):
		ids = {
			"video": "v",
			"playlist": "list",
			"comment": "lc"
		}

		id = link

		if "youtube" in link:
			from urllib.parse import urlparse, parse_qs

			link = urlparse(link)
			query = link.query
			parameters = parse_qs(query)
			id = parameters[ids[name]][0]

		youtube = {
			"item": name + "s",
			"id": id
		}

		dict_ = self.API.Call("YouTube", youtube)["Dictionary"][youtube["id"]]

		return dict_

	def Show_Media_Information(self, dictionary):
		# Show opening this media text
		header_text = dictionary["media_type"]["singular"][self.user_language] + ":"

		if "header_text" in dictionary and "header_text" not in ["", None]:
			header_text = dictionary["header_text"]

		print()
		print(self.large_bar)

		# Show congratulations text if the user finished the media
		if dictionary["media"]["States"]["completed"] == True:
			print()
			print(self.language_texts["congratulations"] + "! :3")

		print()
		print(header_text)

		# Show the title of the media
		self.Show_Media_Title(dictionary)

		print()

		# Show finished watching media texts and times
		if dictionary["media"]["States"]["completed"] == True:
			print(self.language_texts["new_watching_status"] + ":")
			print(dictionary["media"]["details"][self.language_texts["status, title()"]])
			print()

			print(self.media_dictionary["media"]["finished_watching_text"])
			print()

		# Show media episode if the media is series media (not a movie)
		if dictionary["media"]["States"]["series_media"] == True:
			if dictionary["media"]["States"]["video"] == True:
				dictionary["media_type"]["genders"]["of_the"] = self.media_types["genders"]["feminine"]["of_the"]

			media_episode_text = "{} {}".format(self.Text.Capitalize(dictionary["media"]["texts"]["unit"][self.user_language]), dictionary["media_type"]["genders"]["of_the"]) + " "

			if dictionary["media"]["States"]["media_list"] == False or dictionary["media"]["States"]["video"] == True:
				text = dictionary["media"]["texts"]["item"][self.user_language]

				if dictionary["media"]["States"]["video"] == False:
					text = text.lower()

			else:
				text = dictionary["media"]["texts"]["container_text"]["container"]

			media_episode_text += text

			title = dictionary["media"]["episode"]["title"]

			if dictionary["media"]["States"]["re_watching"] == True:
				title += dictionary["media"]["episode"]["re_watched"]["text"]

			print(media_episode_text + ":")
			print(title)
			print()

			text = self.language_texts["with_{}_title"]

			if dictionary["media"]["States"]["video"] == True:
				text = self.language_texts["with_{}"]

			text_to_show = self.Text.Capitalize(dictionary["media"]["texts"]["unit"][self.user_language]) + " " + text.format(dictionary["media"]["texts"]["container_text"]["the"])

			# Show media episode (episode with media item) if the media has a media list
			if dictionary["media"]["States"]["media_list"] == True and dictionary["media"]["item"]["title"] != dictionary["media"]["title"] and dictionary["media"]["States"]["video"] == False and self.language_texts["single_unit"] not in self.media_dictionary["media"]["item"]["details"]:
				media_episode_text = self.Text.Capitalize(dictionary["media"]["texts"]["unit"][self.user_language]) + " " + self.language_texts["with_{}"].format(dictionary["media"]["texts"]["item"][self.user_language])

				print(media_episode_text + ":")

				title = dictionary["media"]["episode"]["with_item"][self.user_language]

				if dictionary["media"]["States"]["re_watching"] == True:
					title += dictionary["media"]["episode"]["re_watched"]["text"]

				print(title)
				print()

				text_to_show += " " + self.language_texts["and_{}"].format(dictionary["media"]["texts"]["item"][self.user_language])

				key = "with_title_and_item"

			# Show only media title with episode if the media has no media list
			if dictionary["media"]["States"]["media_list"] == False or dictionary["media"]["item"]["title"] == dictionary["media"]["title"] or dictionary["media"]["States"]["video"] == True or self.language_texts["single_unit"] in self.media_dictionary["media"]["item"]["details"]:
				key = "with_title"

			title = dictionary["media"]["episode"][key][self.user_language]

			if dictionary["media"]["States"]["re_watching"] == True:
				title += dictionary["media"]["episode"]["re_watched"]["text"]

			print(text_to_show + ":")
			print(title)
			print()

		# Show media type
		print(self.language_texts["media_type"] + ":")
		print(dictionary["media_type"]["plural"][self.user_language])

		# Show mixed media type for non-anime media types
		if dictionary["media_type"]["plural"]["en"] != self.texts["animes"]["en"]:
			print()
			print(self.language_texts["mixed_media_type"] + ":")
			print(dictionary["media_type"]["plural"]["en"] + " - " + dictionary["media_type"]["plural"][self.user_language])

		if dictionary["media"]["States"]["completed_item"] == True:
			print()
			print("-")
			print()
			print(self.language_texts["congratulations"] + "! :3")
			print()

			print(self.language_texts["you_finished_watching"] + " " + dictionary["media"]["texts"]["this_item"][self.user_language] + " " + dictionary["media"]["texts"]["container_text"]["of_the"] + ' "' + dictionary["media"]["titles"]["language"] + '"' + ":")
			self.Show_Media_Title(dictionary, media_item = True)

			if dictionary["media"]["States"]["completed"] == False and dictionary["media"]["States"]["video"] == False:
				if dictionary["media"]["States"]["single_unit"] == True:
					dictionary["media"]["texts"]["item"][self.user_language] = self.language_texts["season"]

				print()
				print(self.language_texts["next_{}_to_watch, feminine"].format(dictionary["media"]["texts"]["item"][self.user_language]) + ": ")

				dict_ = { 
					"media": {
						"States": dictionary["media"]["States"],
						"titles": dictionary["media"]["item"]["next"]["titles"],
						"texts": dictionary["media"]["texts"]
					}
				}

				self.Show_Media_Title(dict_)

		if "unit" in dictionary["media"]["episode"]:
			# Show media unit text and episode unit
			print()
			print(self.language_texts["media_unit"] + ":")
			print(dictionary["media"]["episode"]["unit"])

		if "finished_watching" in dictionary["media"]:
			text = self.language_texts["when_i_finished_watching"] + " " + dictionary["media"]["texts"]["the_unit"][self.user_language]

			# Replaced "watching" with "re-watching" text
			if dictionary["media"]["States"]["re_watching"] == True:
				text = text.replace(self.language_texts["watching, infinitive"], self.language_texts["re_watching, infinitive"] + " " + dictionary["media"]["episode"]["re_watched"]["time_text"][self.user_language])

			print()
			print(text + ":")
			print(dictionary["media"]["finished_watching"]["date_time_format"][self.user_language])

		if dictionary["media"]["States"]["finished_watching"] == True:
			print()

		if "id" in dictionary["media"]["episode"]:
			if dictionary["media"]["States"]["finished_watching"] == False:
				print()
				
			print(self.language_texts["id"] + ":")
			print(dictionary["media"]["episode"]["id"])

			if "next" in dictionary["media"]["episode"] or dictionary["media"]["States"]["completed_item"] == True:
				print()

		# Show next episode to watch if it is present in the "episode" dictionary
		if "next" in dictionary["media"]["episode"]:
			text = self.language_texts["next_{}_to_watch, masculine"]

			if dictionary["media"]["States"]["re_watching"] == True:
				text = text.replace(self.language_texts["watch"], self.language_texts["re_watch"])

			print(text.format(dictionary["media"]["texts"]["unit"][self.user_language]) + ": ")
			print(dictionary["media"]["episode"]["next"])
			print()

		# Show finished watching media (started and finished watching dates) text when user completed a media item
		if dictionary["media"]["States"]["completed_item"] == True and self.language_texts["single_unit"] not in self.media_dictionary["media"]["item"]["details"]:
			print(self.media_dictionary["media"]["item"]["finished_watching_text"])
			print()

		# Show "first watched in year" text if this is the first episode or movie that the user watched in the year, per media type
		if dictionary["media"]["States"]["finished_watching"] == True and dictionary["media"]["States"]["first_episode_in_year"] == True:
			container = dictionary["media"]["texts"]["container"][self.user_language]

			if dictionary["media"]["States"]["video"] == False:
				container = container.lower()

			items = [
				dictionary["media_type"]["genders"]["this"].title(),
				dictionary["media_type"]["genders"]["the"],
				dictionary["media_type"]["genders"]["first"],
				dictionary["media"]["texts"]["unit"][self.user_language] + " " + self.language_texts["of, neutral"] + " " + container,
				str(self.date["year"])
			]

			print(self.language_texts["{}_is_{}_{}_{}_that_you_watched_in_{}"].format(*items) + ".")
			print()

		# If the user finished watching, ask for input beforing ending execution
		if dictionary["media"]["States"]["finished_watching"] == True:
			print(self.large_bar)

			self.Input.Type(self.JSON.Language.language_texts["press_enter_when_you_finish_reading_the_info_summary"])
# Watch History.py

from Global_Switches import Global_Switches as Global_Switches

from Language import Language as Language
from File import File as File
from Folder import Folder as Folder
from Date import Date as Date
from Input import Input as Input
from JSON import JSON as JSON
from Text import Text as Text

from Years.Years import Years as Years
from Christmas.Christmas import Christmas as Christmas

import re
from copy import deepcopy

# Main class Watch_History that provides variables to the classes that implement it
class Watch_History(object):
	def __init__(self, parameter_switches = None, custom_year = None):
		self.parameter_switches = parameter_switches

		self.Define_Basic_Variables()
		self.Define_Module_Folder()
		self.Define_Texts()

		# Load Years module
		self.Years = Years(self.global_switches, select_year = False)

		# Load Christmas module
		self.Christmas = Christmas(self.global_switches)
		self.Today_Is_Christmas = self.Christmas.Today_Is_Christmas()

		self.Define_Folders_And_Files()
		self.Define_Lists_And_Dictionaries()
		self.Define_Media_Types()
		self.Define_Episodes_Files()

	def Define_Basic_Variables(self):
		# Global Switches dictionary
		self.global_switches = Global_Switches().global_switches

		if self.parameter_switches != None:
			self.global_switches.update(self.parameter_switches)

		self.Language = Language(self.global_switches)
		self.File = File(self.global_switches)
		self.Folder = Folder(self.global_switches)
		self.Date = Date(self.global_switches)
		self.Input = Input(self.global_switches)
		self.JSON = JSON(self.global_switches)
		self.Text = Text(self.global_switches)

		self.app_settings = self.Language.app_settings
		self.languages = self.Language.languages
		self.small_languages = self.languages["small"]
		self.full_languages = self.languages["full"]
		self.translated_languages = self.languages["full_translated"]

		self.user_language = self.Language.user_language
		self.full_user_language = self.Language.full_user_language

		self.Sanitize = self.File.Sanitize

		self.folders = self.Folder.folders
		self.root_folders = self.folders["root"]
		self.user_folders = self.folders["user"]
		self.apps_folders = self.folders["apps"]
		self.mega_folders = self.folders["mega"]
		self.notepad_folders = self.folders["notepad"]

		self.date = self.Date.date

	def Define_Module_Folder(self):
		self.module = {
			"name": self.__module__,
		}

		if "." in self.module["name"]:
			self.module["name"] = self.module["name"].split(".")[0]

		self.module["key"] = self.module["name"].lower()

		self.apps_folders["modules"][self.module["key"]] = {
			"root": self.apps_folders["modules"]["root"] + self.module["name"] + "/",
		}

		self.apps_folders["module_files"][self.module["key"]] = {
			"root": self.apps_folders["module_files"]["root"] + self.module["name"] + "/",
		}

		for item in ["module_files", "modules"]:
			self.apps_folders[item][self.module["key"]] = self.apps_folders[item]["root"] + self.module["name"] + "/"
			self.apps_folders[item][self.module["key"]] = self.Folder.Contents(self.apps_folders[item][self.module["key"]], lower_key = True)["dictionary"]

	def Define_Texts(self):
		self.texts = self.JSON.To_Python(self.apps_folders["module_files"][self.module["key"]]["texts"])

		self.language_texts = self.Language.Item(self.texts)

		self.large_bar = "-----"
		self.dash_space = "-"

	def Define_Folders_And_Files(self):
		self.current_year = self.Years.current_year

		# Folders dictionary
		self.folders = self.Folder.Contents(self.notepad_folders["networks"]["audiovisual_media_network"]["root"], lower_key = True)["dictionary"]

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

	def Define_Media_Types(self):
		self.media_types = {
			"singular": self.texts["media_types, type: list"],
			"plural": self.texts["plural_media_types, type: list"],
			"genders": {},
			"gender_items": ["the", "these", "this", "a", "of", "of_the", "first", "last"],
			"media_list": {
				"Number": 0,
				"Numbers": {}
			}
		}

		for gender in ["masculine", "feminine"]:
			self.media_types["genders"][gender] = {}

			for item in self.media_types["gender_items"]:
				self.media_types["genders"][gender][item] = self.language_texts[item + ", " + gender]

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
					self.texts["re_watching, title()"]["en"],
				]
			}

			# Define singular and plural media types
			for language in self.small_languages:
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

			for item in self.media_types["gender_items"]:
				self.media_types[plural_media_type]["genders"][item] = self.language_texts[item + ", " + gender]

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
						"root": self.folders[root_key]["current_year"]["per_media_type"]["root"] + language_media_type + "/",
					}

					self.Folder.Create(self.folders[root_key]["current_year"]["per_media_type"][key]["root"])

					# Episodes.json file
					self.folders[root_key]["current_year"]["per_media_type"][key]["episodes"] = self.folders[root_key]["current_year"]["per_media_type"][key]["root"] + "Episodes.json"
					self.File.Create(self.folders[root_key]["current_year"]["per_media_type"][key]["episodes"])

					# File list.txt file
					self.folders[root_key]["current_year"]["per_media_type"][key]["file_list"] = self.folders[root_key]["current_year"]["per_media_type"][key]["root"] + "File list.txt"
					self.File.Create(self.folders[root_key]["current_year"]["per_media_type"][key]["file_list"])

					# Files folder
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

			# Get the number of media titles
			self.media_types[plural_media_type]["json"]["Number"] = len(self.media_types[plural_media_type]["json"]["Titles"])

			# Sort "Titles" list of the "Info.json" file
			self.media_types[plural_media_type]["json"]["Titles"] = sorted(self.media_types[plural_media_type]["json"]["Titles"])

			# Sort "Status" lists of the "Info.json" file
			for watching_status in self.texts["watching_statuses, type: list"]["en"]:
				self.media_types[plural_media_type]["json"]["Status"][watching_status] = sorted(self.media_types[plural_media_type]["json"]["Status"][watching_status])

			# Update the "Info.json" file with the new number
			self.JSON.Edit(self.media_types[plural_media_type]["folders"]["media_info"]["info"], self.media_types[plural_media_type]["json"])

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
			for language in self.small_languages:
				for item in ["singular", "plural"]:
					self.media_types[plural_media_type][item]["show"] = self.media_types[plural_media_type][item][self.user_language] + " (" + str(len(self.media_types[plural_media_type]["media_list"])) + ")"

			self.media_types[plural_media_type]["texts"]["show"] = self.Text.By_Number(self.media_types[plural_media_type]["media_list"], self.media_types[plural_media_type]["singular"]["show"], self.media_types[plural_media_type]["plural"]["show"])

			i += 1

		# Write media types dictionary into "Media Types.json" file
		self.JSON.Edit(self.folders["network_data"]["media_types"], self.media_types)

		# Update "Info.json" file on "Media Info" folder
		dictionary = self.JSON.To_Python(self.folders["media_info"]["info"])
		dictionary.update(self.media_types["media_list"])

		self.JSON.Edit(self.folders["media_info"]["info"], dictionary)

	def Define_Episodes_Files(self):
		# Define default Episodes dictionary template
		self.template = {
			"Number": 0,
			"Comments": 0,
			"Number. Media Type (Time)": [],
			"Dictionary": {},
			"Lists": {
				"Media": [],
				"Episode titles": {},
				"Media Types": [],
				"Times": {
					"ISO8601": [],
					"Language DateTime": {}
				},
				"YouTube IDs": []
			}
		}

		self.episodes = self.template.copy()

		# Add language lists to media and episode titles and episode Language DateTime dictionaries
		for language in self.small_languages:
			self.episodes["Lists"]["Episode titles"][language] = []
			self.episodes["Lists"]["Times"]["Language DateTime"][language] = []

		# If Episodes.json is not empty, get Episodes dictionary from it
		if self.File.Contents(self.folders["watch_history"]["current_year"]["episodes"])["lines"] != []:
			self.episodes = self.JSON.To_Python(self.folders["watch_history"]["current_year"]["episodes"])

		# If Episodes.json is empty, write default Episodes dictionary inside it
		if self.File.Contents(self.folders["watch_history"]["current_year"]["episodes"])["lines"] == []:
			self.JSON.Edit(self.folders["watch_history"]["current_year"]["episodes"], self.episodes)

		# Define default Media Type Episodes dictionary
		self.media_type_episodes = {}

		for plural_media_type in self.media_types["plural"]["en"]:
			key = plural_media_type.lower().replace(" ", "_")

			self.media_type_episodes[plural_media_type] = deepcopy(self.template)
			self.media_type_episodes[plural_media_type]["Lists"].pop("Media Types")

			# Add language lists to media and episode titles and episode Language DateTime dictionaries
			for language in self.small_languages:
				self.media_type_episodes[plural_media_type]["Lists"]["Episode titles"][language] = []
				self.media_type_episodes[plural_media_type]["Lists"]["Times"]["Language DateTime"][language] = []

			if plural_media_type != self.texts["videos"]["en"]:
				self.media_type_episodes[plural_media_type]["Lists"].pop("YouTube IDs")

			if plural_media_type == self.texts["movies"]["en"]:
				self.media_type_episodes[plural_media_type]["Lists"].pop("Episode titles")

			# If Media Type Episodes.json is not empty, get Media Type Episodes dictionary from it
			if self.File.Contents(self.folders["watch_history"]["current_year"]["per_media_type"][key]["episodes"])["lines"] != []:
				self.media_type_episodes[plural_media_type] = self.JSON.To_Python(self.folders["watch_history"]["current_year"]["per_media_type"][key]["episodes"])

			# If Media Type Episodes.json is empty, write default Media Type Episodes dictionary inside it
			if self.File.Contents(self.folders["watch_history"]["current_year"]["per_media_type"][key]["episodes"])["lines"] == []:
				self.JSON.Edit(self.folders["watch_history"]["current_year"]["per_media_type"][key]["episodes"], self.media_type_episodes[plural_media_type])

		# Get Comments dictionary from file
		self.comments = self.JSON.To_Python(self.folders["comments"]["comments"])

		# If current year is not inside "media type year numbers" dictionary, create the current year media type dictionary
		# And define all of the media type comment numbers as zero
		if str(self.date["year"]) not in self.comments["Media type year numbers"]:
			self.comments["Media type year numbers"][self.date["year"]] = {}

			for plural_media_type in self.media_types["plural"]["en"]:
				self.comments["Media type year numbers"][self.date["year"]][plural_media_type] = 0

			# Update "Comments.json" file with new Comments dictionary
			self.JSON.Edit(self.folders["comments"]["comments"], self.comments)

	def Remove_Media_Type(self, media_types_list):
		if type(media_types_list) == str:
			media_types_list = [media_types_list]

		media_types = self.media_types.copy()

		for language in self.small_languages:
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

	def Get_Language_Status(self, status):
		w = 0
		for watching_status in self.texts["watching_statuses, type: list"]["en"]:
			if watching_status == status:
				language_status = self.texts["watching_statuses, type: list"][self.user_language][w]

			w += 1

		return language_status

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
			for language in self.small_languages:
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
				"media": dictionary["media"]["folders"]["media"],
				"media_type_comments": {
					"root": dictionary["media"]["folders"]["media_type_comments"]["root"] + self.Sanitize(sanitized_title, restricted_characters = True) + "/"
				}
			})

			if sanitized_title + "/" not in media["folders"]["media"]:
				media["folders"]["media"] += self.Sanitize(sanitized_title, restricted_characters = True) + "/"

			# Create folders
			for key in media["folders"]:
				folder = media["folders"][key]

				if "root" in folder:
					folder = folder["root"]

				self.Folder.Create(folder)

		if "folders" not in media:
			media["folders"] = {
				"root": dictionary["media_type"]["folders"]["media_info"]["root"] + self.Sanitize(sanitized_title, restricted_characters = True) + "/",
				"media": self.root_folders["media"] + self.Sanitize(sanitized_title, restricted_characters = True) + "/",
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
		for file_name in ["Details.txt", "Information.json", "Dates.txt"]:
			key = file_name.lower().replace(" ", "_").replace(".txt", "").replace(".json", "")
			extension = "." + file_name.split(".")[-1]

			file_name = self.language_texts[key + ", title()"] + extension

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
				"episodic": True,
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

			if "states" in media:
				media["states"].update(states)

			if "states" not in media:
				media["states"] = states

			if self.Today_Is_Christmas == True:
				media["states"]["christmas"] = True

			# Define origin type state
			for key in ["local", "remote", "hybrid"]:
				if self.language_texts["origin_type"] in media["details"]:
					if media["details"][self.language_texts["origin_type"]] == self.language_texts[key + ", title()"]:
						media["states"][key] = True

			# Define video state for videos
			if dictionary["media_type"]["plural"]["en"] == self.texts["videos"]["en"]:
				media["states"]["video"] = True
				media["states"]["episodic"] = False

			if self.language_texts["episodic, title()"] in media["details"]:
				media["states"]["episodic"] = self.Input.Define_Yes_Or_No(media["details"][self.language_texts["episodic, title()"]])

			# Define non-series media state for movies
			if dictionary["media_type"]["plural"]["en"] == self.texts["movies"]["en"]:
				media["states"]["series_media"] = False

			# Define remote origin for animes or videos media type
			if self.language_texts["remote_origin, title()"] not in dictionary["media"]["details"]:
				if dictionary["media_type"]["plural"]["en"] == self.texts["animes"]["en"]:
					remote_origin = "Animes Vision"

				if dictionary["media_type"]["plural"]["en"] == self.texts["videos"]["en"]:
					remote_origin = "YouTube"

				dictionary["media"]["details"][self.language_texts["remote_origin, title()"]] = "Animes Vision"

			# Define Re-Watching state for Re-Watching status
			if self.language_texts["status, title()"] in media["details"] and media["details"][self.language_texts["status, title()"]] == self.language_texts["re_watching, title()"]:
				media["states"]["re_watching"] = True

			media["episode"] = {
				"title": "",
				"titles": {},
				"sanitized": "",
				"number": 1,
				"number_text": "1",
				"separator": ""
			}

			if media["states"]["remote"] == True or self.language_texts["remote_origin, title()"] in media["details"]:
				media["episode"]["remote"] = {
					"title": "",
					"link": "",
					"code": ""
				}

		dictionary = self.Define_Media_Titles(dictionary, self.item)

		if self.item == False:
			dictionary = self.Define_Media_Item(dictionary, watch)

		return dictionary

	def Define_Media_Item(self, dictionary, watch = False, media_item = None):
		if dictionary["media"]["states"]["series_media"] == True:
			dictionary["media"]["items"] = {
				"folders": {
					"root": dictionary["media"]["folders"]["root"] + dictionary["media_type"]["subfolders"]["plural"] + "/",
				}
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

				# Define media item folders
				for name in dictionary["media"]["items"]["list"]:
					name = self.Sanitize_Title(name)

					dictionary["media"]["items"]["folders"][name] = dictionary["media"]["items"]["folders"]["root"] + name + "/"
					self.Folder.Create(dictionary["media"]["items"]["folders"][name])

				# Define current media item
				title = dictionary["media"]["items"]["current"]

				# Has media list
				dictionary["media"]["states"]["media_list"] = True

				# Select video series from channel for video series media
				if dictionary["media"]["states"]["video"] == True:
					show_text = self.Text.Capitalize(self.language_texts["youtube_video_series"])
					select_text = self.language_texts["select_a_youtube_video_series"]

					list_ = dictionary["media"]["items"]["list"].copy()

					for series in dictionary["media"]["items"]["list"].copy():
						folders = {
							"root": dictionary["media"]["items"]["folders"]["root"] + self.Sanitize(series, restricted_characters = True) + "/"
						}

						folders["details"] = folders["root"] + self.language_texts["details, title()"] + ".txt"

						folders["titles"] = {
							"root": folders["root"] + self.language_texts["titles, title()"] + "/"
						}

						folders["titles"]["file"] = folders["titles"]["root"] + self.full_user_language + ".txt"

						titles = self.File.Contents(folders["titles"]["file"])["lines"]

						details = self.File.Dictionary(folders["details"])

						if details[self.language_texts["episode, title()"]] == titles[-1]:
							list_.remove(series)

					if watch == True:
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

				i = 0
				for name in dictionary["media"]["items"]["list"]:
					if dictionary["media"]["item"]["title"] == name:
						dictionary["media"]["item"]["number"] = i

					i += 1

				dictionary = self.Select_Media(dictionary, item = True)

				# Define single unit state
				if self.language_texts["single_unit"] in dictionary["media"]["item"]["details"]:
					dictionary["media"]["states"]["single_unit"] = False

				if dictionary["media"]["states"]["single_unit"] == True:
					dictionary["media"]["item"]["folders"]["media"] = dictionary["media"]["folders"]["media"]

			if self.Folder.Exist(dictionary["media"]["items"]["folders"]["root"]) == False:
				dictionary["media"]["states"]["media_list"] = False

		# Define media item as the media for media that has no media list
		if dictionary["media"]["states"]["media_list"] == False or dictionary["media"]["states"]["series_media"] == False:
			dictionary["media"]["item"] = dictionary["media"].copy()

		dictionary["media"]["item"]["folders"]["watched"] = {
			"root": dictionary["media"]["item"]["folders"]["root"] + self.language_texts["watched, title()"] + "/"
		}

		self.Folder.Create(dictionary["media"]["item"]["folders"]["watched"]["root"])

		# Define media item folders
		if dictionary["media"]["states"]["series_media"] == True:
			for name in ["Comments", "Titles"]:
				key = name.lower().replace(" ", "_")
				name = self.language_texts[key + ", title()"]

				dictionary["media"]["item"]["folders"][key] = {
					"root": dictionary["media"]["item"]["folders"]["root"] + name + "/",
				}

				self.Folder.Create(dictionary["media"]["item"]["folders"][key]["root"])

			folder = dictionary["media"]["item"]["folders"]["comments"]

		if dictionary["media"]["states"]["series_media"] == False or dictionary["media"]["states"]["single_unit"] == True:
			folder = dictionary["media"]["item"]["folders"]

		# Define media comments folder comments file for media with media list
		folder["comments"] = folder["root"] + self.texts["comments, title()"]["en"] + ".json"
		self.File.Create(folder["comments"])

		# Define media type comments folder comments file for media with media list
		dictionary["media"]["item"]["folders"]["media_type_comments"]["comments"] = dictionary["media"]["item"]["folders"]["media_type_comments"]["root"] + self.texts["comments, title()"]["en"] + ".json"
		self.File.Create(dictionary["media"]["item"]["folders"]["media_type_comments"]["comments"])

		dict_ = {
			"File names": [],
			"Dictionary": {}
		}

		if self.File.Contents(folder["comments"])["lines"] == []:
			self.JSON.Edit(folder["comments"], dict_)

		if self.File.Contents(dictionary["media"]["item"]["folders"]["media_type_comments"]["comments"])["lines"] == []:
			self.JSON.Edit(dictionary["media"]["item"]["folders"]["media_type_comments"]["comments"], dict_)

		# Create "Files" folder file inside "Watched" folder
		dictionary["media"]["item"]["folders"]["watched"]["files"] = {
			"root": dictionary["media"]["item"]["folders"]["watched"]["root"] + self.File.language_texts["files, title()"] + "/"
		}

		self.Folder.Create(dictionary["media"]["item"]["folders"]["watched"]["files"]["root"])

		# Create "Watched.json" file inside "Watched" folder
		dictionary["media"]["item"]["folders"]["watched"]["watched"] = dictionary["media"]["item"]["folders"]["watched"]["root"] + "Watched.json"
		self.File.Create(dictionary["media"]["item"]["folders"]["watched"]["watched"])

		# Write default dictionary into "Watched.json" file
		if self.File.Contents(dictionary["media"]["item"]["folders"]["watched"]["watched"])["lines"] == [] or self.JSON.To_Python(dictionary["media"]["item"]["folders"]["watched"]["watched"])["Lists"]["Episode titles"]["en"] == []:
			template = deepcopy(self.template)

			for key in ["Media", "Media Types", "Number. Media Type (Time)", "Dictionary"]:
				if key not in template["Lists"]:
					template.pop(key)

				if key in template["Lists"]:
					template["Lists"].pop(key)

			# If not video, remove "YouTube IDs" key
			if dictionary["media"]["states"]["video"] == False:
				template["Lists"].pop("YouTube IDs")

			lists = template["Lists"].copy()
			template.pop("Lists")

			file_name = "Movie"

			if dictionary["media"]["states"]["single_unit"] == True:
				file_name = "Episode"

			if dictionary["media"]["states"]["series_media"] == True and dictionary["media"]["states"]["single_unit"] == False:
				template["File name"] = []

			if dictionary["media"]["states"]["series_media"] == False or dictionary["media"]["states"]["single_unit"] == True:
				template["File name"] = file_name

			template["Dictionary"] = {}
			template["Lists"] = lists

			self.JSON.Edit(dictionary["media"]["item"]["folders"]["watched"]["watched"], template)

		# Define media item files
		file_names = ["Dates"]

		if dictionary["media"]["states"]["video"] == True:
			file_names.append("YouTube IDs")

		for name in file_names:
			key = name.lower().replace(" ", "_")
			name = self.language_texts[key + ", title()"]

			dictionary["media"]["item"]["folders"][key] = dictionary["media"]["item"]["folders"]["root"] + name + ".txt"
			self.File.Create(dictionary["media"]["item"]["folders"][key])

		# Define episodes dictionary
		if dictionary["media"]["states"]["series_media"] == True:
			dictionary["media"]["item"]["episodes"] = {
				"number": 0,
				"titles": {
					"files": {},
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

			if dictionary["media"]["states"]["video"] == True:
				dictionary["media"]["episode"]["separator"] = ""

			# Define episode titles files and lists
			for language in self.small_languages:
				full_language = self.full_languages[language]

				if dictionary["media"]["states"]["single_unit"] == False:
					# Define episode titles file
					dictionary["media"]["item"]["episodes"]["titles"]["files"][language] = dictionary["media"]["item"]["folders"]["titles"]["root"] + full_language + ".txt"
					self.File.Create(dictionary["media"]["item"]["episodes"]["titles"]["files"][language])

					# Get language episode titles from file
					dictionary["media"]["item"]["episodes"]["titles"][language] = self.File.Contents(dictionary["media"]["item"]["episodes"]["titles"]["files"][language])["lines"]

				# Iterate through episode titles
				if dictionary["media"]["episode"]["separator"] != "" and dictionary["media"]["states"]["single_unit"] == False or dictionary["media"]["states"]["episodic"] == False:
					i = 1
					for episode_title in dictionary["media"]["item"]["episodes"]["titles"][language]:
						number = str(self.Text.Add_Leading_Zeros(i))

						if dictionary["media"]["episode"]["separator"] != "":
							separator = dictionary["media"]["episode"]["separator"]

							for alternative_episode_type in self.alternative_episode_types:
								if re.search(alternative_episode_type + " [0-9]{1,2}", episode_title) != None:
									separator = ""

							# Add episode number name to local episode title
							episode_title = separator + number + " " + episode_title

							# Add episode number name to episode titles if the number name is not present
							if separator != "" and number not in dictionary["media"]["item"]["episodes"]["titles"][language][i - 1]:
								dictionary["media"]["item"]["episodes"]["titles"][language][i - 1] = episode_title

						if dictionary["media"]["states"]["episodic"] == False:
							if re.search(self.texts["part, title()"][language] + " [0-9]{1,2}", episode_title) != None or re.search(" \#[0-9]{1,2}$", episode_title) != None:
								dictionary["media"]["states"]["episodic"] = True

						i += 1

			if dictionary["media"]["states"]["single_unit"] == True:
				dictionary["media"]["episode"]["title"] = dictionary["media"]["item"]["title"]
				dictionary["media"]["episode"]["titles"] = dictionary["media"]["item"]["titles"]

				for language in self.small_languages:
					if language not in dictionary["media"]["episode"]["titles"]:
						dictionary["media"]["episode"]["titles"][language] = self.Get_Media_Title(dictionary, item = True)

			if dictionary["media"]["states"]["single_unit"] == False:
				# Add the episode number to the episode "number" key
				dictionary["media"]["item"]["episodes"]["number"] = len(dictionary["media"]["item"]["episodes"]["titles"]["en"])

			# Add the episode number to the media item details
			keys = list(dictionary["media"]["item"]["details"].keys())
			values = list(dictionary["media"]["item"]["details"].values())

			i = 0
			for key in keys.copy():
				if key == self.language_texts["episode, title()"]:
					keys.insert(i + 1, self.language_texts["episodes, title()"])
					values.insert(i + 1, dictionary["media"]["item"]["episodes"]["number"])

				i += 1

			dictionary["media"]["item"]["details"] = dict(zip(keys, values))

			# Update media item details file
			self.File.Edit(dictionary["media"]["item"]["folders"]["details"], self.Text.From_Dictionary(dictionary["media"]["item"]["details"]), "w")

			if dictionary["media"]["states"]["media_list"] == True and dictionary["media"]["item"]["title"] == self.File.Contents(dictionary["media"]["items"]["folders"]["current"])["lines"][0]:
				# Write dictionary into media item "Information.json" file
				self.JSON.Edit(dictionary["media"]["item"]["folders"]["information"], dictionary["media"]["item"])

		if self.episodes["Number"] == 0:
			dictionary["media"]["states"]["first_episode_in_year"] = True

		if self.media_type_episodes[dictionary["media_type"]["plural"]["en"]]["Number"] == 0:
			dictionary["media"]["states"]["first_media_type_episode_in_year"] = True

		# Define media texts to be used in the "Show_Media_Information" root method
		dictionary["media"]["texts"] = {
			"genders": dictionary["media_type"]["genders"]
		}

		# Define the container, item, and unit texts as the media type (for movies)
		for item in ["container", "item", "unit"]:
			dictionary["media"]["texts"][item] = dictionary["media_type"]["singular"].copy()

		# Define the container, item, and unit for series media
		if dictionary["media"]["states"]["series_media"] == True:
			# Define the unit text as the "episode" text per language
			dictionary["media"]["texts"]["unit"] = {}

			for language in self.small_languages:
				dictionary["media"]["texts"]["unit"][language] = self.texts["episode"][language]

			# Define the item text as the "season" text for media that have a media list
			if dictionary["media"]["states"]["media_list"] == True and dictionary["media"]["item"]["title"] != dictionary["media"]["title"]:
				dictionary["media"]["texts"]["item"] = {}

				for language in self.small_languages:
					dictionary["media"]["texts"]["item"][language] = self.texts["season"][language]

					if dictionary["media"]["states"]["single_unit"] == True:
						dictionary["media"]["texts"]["item"][language] = self.texts["episode"][language]

			# Define the container, item, and unit texts for video series media
			if dictionary["media"]["states"]["video"] == True:
				for language in self.small_languages:
					dictionary["media"]["texts"]["container"][language] = self.texts["youtube_channel"][language]
					dictionary["media"]["texts"]["item"][language] = self.texts["youtube_video_serie"][language]
					dictionary["media"]["texts"]["unit"][language] = self.texts["video"][language]

		dict_ = dictionary["media"]["texts"].copy()

		for item in ["the", "this", "of"]:
			for key in dict_:
				if key != "genders":
					if item + "_" + key not in dictionary["media"]["texts"]:
						dictionary["media"]["texts"][item + "_" + key] = {}

					for language in self.small_languages:
						if dictionary["media"]["texts"][key][language] != self.texts["season"][language]:
							item_text = dictionary["media_type"]["genders"][item]

						if dictionary["media"]["texts"][key][language] == self.texts["season"][language]:
							for gender_key in dict_["genders"]:

								gender = dict_["genders"][gender_key]

								if item == gender_key:
									item_text = self.media_types["genders"]["feminine"][gender_key]

						dictionary["media"]["texts"][item + "_" + key][language] = item_text + " " + dictionary["media"]["texts"][key][language]

		# Add "Christmas special" text to unit text
		if dictionary["media"]["states"]["video"] == False and self.Today_Is_Christmas == True:
			dictionary["media"]["texts"]["unit"] = {}

			for language in self.small_languages:
				dictionary["media"]["texts"]["unit"][language] = self.texts["christmas_special_{}"][language].format(dictionary["media"]["texts"]["unit"][language])

		dictionary_copy = dictionary["media"].copy()
		dictionary_copy.pop("texts")
		dictionary_copy.pop("states")

		if dictionary["media"]["states"]["series_media"] == True:
			if dictionary["media"]["states"]["media_list"] == False:
				# Write dictionary into media "Information.json" file
				dictionary_copy.pop("item")

				self.JSON.Edit(dictionary["media"]["folders"]["information"], dictionary_copy)

			if dictionary["media"]["states"]["media_list"] == True and dictionary["media"]["item"]["title"] == self.File.Contents(dictionary["media"]["items"]["folders"]["current"])["lines"][0]:
				# Write dictionary into media "Information.json" file
				self.JSON.Edit(dictionary["media"]["folders"]["information"], dictionary_copy)

		if dictionary["media"]["states"]["series_media"] == False:
			# Write dictionary into media "Information.json" file
			dictionary_copy.pop("item")

			self.JSON.Edit(dictionary["media"]["folders"]["information"], dictionary_copy)

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
			for language in self.small_languages:
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

	def Show_Media_Title(self, dictionary):
		if dictionary["media"]["titles"]["language"] == dictionary["media"]["titles"]["original"]:
			print(dictionary["media"]["titles"]["original"])

			if dictionary["media"]["states"]["video"] == True:				
				print()
				print(self.Text.Capitalize(dictionary["media"]["texts"]["item"][self.user_language]) + ":")
				print(dictionary["media"]["item"]["title"])

		if dictionary["media"]["titles"]["language"] != dictionary["media"]["titles"]["original"]:
			print("\t" + dictionary["media"]["titles"]["original"])
			print("\t" + dictionary["media"]["titles"]["language"])

			for language in self.small_languages:
				language_name = self.texts["language_name"][language][self.user_language]

				if language in dictionary["media"]["titles"] and dictionary["media"]["titles"][language] != dictionary["media"]["titles"]["original"]:
					print("\t" + dictionary["media"]["titles"][language])

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
			if dictionary["media"]["states"][key] == True:
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

	def Change_Status(self, dictionary, status):
		# Update status key in media details
		dictionary["media"]["details"][self.language_texts["status, title()"]] = status

		# Update media details file
		self.File.Edit(dictionary["media"]["folders"]["details"], self.Text.From_Dictionary(dictionary["media"]["details"]), "w")

		self.Check_Status(dictionary)

	def Check_Status(self, dictionary):
		dictionary["json"] = self.JSON.To_Python(dictionary["media_type"]["folders"]["media_info"]["info"])

		language_status = dictionary["media"]["details"][self.language_texts["status, title()"]]

		# Get English watching status from language status of media details
		i = 0
		for watching_status in self.texts["watching_statuses, type: list"]["en"]:
			if language_status == self.texts["watching_statuses, type: list"]["pt"][i]:
				language_status = watching_status

			i += 1

		# Iterate through watching statuses list
		for watching_status in self.texts["watching_statuses, type: list"]["en"]:
			# If media status is equal to watching status
			# And media is not in the watching status list, add it to the list
			if language_status == watching_status and dictionary["media"]["title"] not in dictionary["json"]["Status"][watching_status]:
				dictionary["json"]["Status"][watching_status].append(dictionary["media"]["title"])

			# If media status is not equal to watching status
			# And media is in the wrong watching status list, remove it from the list
			if language_status != watching_status and dictionary["media"]["title"] in dictionary["json"]["Status"][watching_status]:
				dictionary["json"]["Status"][watching_status].remove(dictionary["media"]["title"])

		# Sort each media list of each watching status
		for watching_status in self.texts["watching_statuses, type: list"]["en"]:
			dictionary["json"]["Status"][watching_status] = sorted(dictionary["json"]["Status"][watching_status])

		# Update media type "Info.json" file
		self.JSON.Edit(dictionary["media_type"]["folders"]["media_info"]["info"], dictionary["json"])

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
		media_list = sorted(media_list)

		return media_list

	def Show_Media_Information(self, dictionary):
		# Show opening this media text
		header_text = dictionary["media_type"]["singular"][self.user_language] + ":"

		if "header_text" in dictionary and "header_text" not in ["", None]:
			header_text = dictionary["header_text"]

		print()
		print(self.large_bar)

		# Show congratulations text if the user finished the media
		if dictionary["media"]["states"]["completed"] == True:
			print()
			print(self.language_texts["congratulations"] + "! :3")

		print()
		print(header_text)

		# Show the title of the media
		self.Show_Media_Title(dictionary)

		print()

		# Show finished watching media texts and times
		if dictionary["media"]["states"]["completed"] == True:
			print(self.language_texts["new_watching_status"] + ":")
			print(dictionary["media"]["details"][self.language_texts["status, title()"]])
			print()

			print(self.media_dictionary["media"]["finished_watching_text"])
			print()

		# Show media episode if the media is series media (not a movie)
		if dictionary["media"]["states"]["series_media"] == True:
			if dictionary["media"]["states"]["video"] == True:
				dictionary["media_type"]["genders"]["of_the"] = self.media_types["genders"]["feminine"]["of_the"]

			media_episode_text = "{} {}".format(self.Text.Capitalize(dictionary["media"]["texts"]["unit"][self.user_language]), dictionary["media_type"]["genders"]["of_the"]) + " "

			if dictionary["media"]["states"]["media_list"] == False or dictionary["media"]["states"]["video"] == True:
				text = dictionary["media"]["texts"]["item"][self.user_language]

				if dictionary["media"]["states"]["video"] == False:
					text = text.lower()

			else:
				text = dictionary["media"]["texts"]["container_text"]["container"]

			media_episode_text += text

			title = dictionary["media"]["episode"]["title"]

			if dictionary["media"]["states"]["re_watching"] == True:
				title += dictionary["media"]["episode"]["re_watched"]["text"]

			print(media_episode_text + ":")
			print(title)
			print()

			text = self.language_texts["with_{}_title"]

			if dictionary["media"]["states"]["video"] == True:
				text = self.language_texts["with_{}"]

			text_to_show = self.Text.Capitalize(dictionary["media"]["texts"]["unit"][self.user_language]) + " " + text.format(dictionary["media"]["texts"]["container_text"]["the"])

			# Show media episode (episode with media item) if the media has a media list
			if dictionary["media"]["states"]["media_list"] == True and dictionary["media"]["item"]["title"] != dictionary["media"]["title"] and dictionary["media"]["states"]["video"] == False and self.language_texts["single_unit"] not in self.media_dictionary["media"]["item"]["details"]:
				media_episode_text = self.Text.Capitalize(dictionary["media"]["texts"]["unit"][self.user_language]) + " " + self.language_texts["with_{}"].format(dictionary["media"]["texts"]["item"][self.user_language])

				print(media_episode_text + ":")

				title = dictionary["media"]["episode"]["with_item"][self.user_language]

				if dictionary["media"]["states"]["re_watching"] == True:
					title += dictionary["media"]["episode"]["re_watched"]["text"]

				print(title)
				print()

				text_to_show += " " + self.language_texts["and_{}"].format(dictionary["media"]["texts"]["item"][self.user_language])

				key = "with_title_and_item"

			# Show only media title with episode if the media has no media list
			if dictionary["media"]["states"]["media_list"] == False or dictionary["media"]["item"]["title"] == dictionary["media"]["title"] or dictionary["media"]["states"]["video"] == True or self.language_texts["single_unit"] in self.media_dictionary["media"]["item"]["details"]:
				key = "with_title"

			title = dictionary["media"]["episode"][key][self.user_language]

			if dictionary["media"]["states"]["re_watching"] == True:
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

		if dictionary["media"]["states"]["completed_item"] == True:
			print()
			print("-")
			print()
			print(self.language_texts["congratulations"] + "! :3")
			print()

			print(self.language_texts["you_finished_watching"] + " " + dictionary["media"]["texts"]["this_item"][self.user_language] + " " + dictionary["media"]["texts"]["container_text"]["of_the"] + ' "' + dictionary["media"]["titles"]["language"] + '"' + ":")

			dict_ = { 
				"media": {
					"states": dictionary["media"]["states"],
					"titles": dictionary["media"]["item"]["titles"]
				}
			}

			self.Show_Media_Title(dict_)

			if dictionary["media"]["states"]["completed"] == False and dictionary["media"]["states"]["video"] == False:
				if dictionary["media"]["states"]["single_unit"] == True:
					dictionary["media"]["texts"]["item"][self.user_language] = self.language_texts["season"]

				print()
				print(self.language_texts["next_{}_to_watch, feminine"].format(dictionary["media"]["texts"]["item"][self.user_language]) + ": ")

				dict_ = { 
					"media": {
						"states": dictionary["media"]["states"],
						"titles": dictionary["media"]["item"]["next"]["titles"]
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
			if dictionary["media"]["states"]["re_watching"] == True:
				text = text.replace(self.language_texts["watching, infinitive"], self.language_texts["re_watching, infinitive"] + " " + dictionary["media"]["episode"]["re_watched"]["time_text"][self.user_language])

			print()
			print(text + ":")
			print(dictionary["media"]["finished_watching"]["date_time_format"][self.user_language])

		if dictionary["media"]["states"]["finished_watching"] == True:
			print()

		if "youtube_id" in dictionary["media"]["episode"]:
			if "next" not in dictionary["media"]["episode"]:
				print()

			print(self.language_texts["youtube_id"] + ":")
			print(dictionary["media"]["episode"]["youtube_id"])

			if "next" in dictionary["media"]["episode"]:
				print()

		# Show next episode to watch if it is present in the "episode" dictionary
		if "next" in dictionary["media"]["episode"]:
			text = self.language_texts["next_{}_to_watch, masculine"]

			if dictionary["media"]["states"]["re_watching"] == True:
				text = text.replace(self.language_texts["watch"], self.language_texts["re_watch"])

			print(text.format(dictionary["media"]["texts"]["unit"][self.user_language]) + ": ")
			print(dictionary["media"]["episode"]["next"])
			print()

		# Show finished watching media (started and finished watching dates) text when user completed a media item
		if dictionary["media"]["states"]["completed_item"] == True and self.language_texts["single_unit"] not in self.media_dictionary["media"]["item"]["details"]:
			print(self.media_dictionary["media"]["item"]["finished_watching_text"])
			print()

		# Show "first watched in year" text if this is the first episode or movie that the user watched in the year, per media type
		if dictionary["media"]["states"]["finished_watching"] == True and dictionary["media"]["states"]["first_episode_in_year"] == True:
			container = dictionary["media"]["texts"]["container"][self.user_language]

			if dictionary["media"]["states"]["video"] == False:
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
		if dictionary["media"]["states"]["finished_watching"] == True:
			print(self.large_bar)

			self.Input.Type(self.Language.language_texts["press_enter_when_you_finish_reading_the_info_summary"])
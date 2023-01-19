# Watch History.py

from Global_Switches import Global_Switches as Global_Switches

from Language import Language as Language
from File import File as File
from Folder import Folder as Folder
from Date import Date as Date
from Input import Input as Input
from Text import Text as Text

from Christmas.Christmas import Christmas as Christmas

# Main class Watch_History that provides variables to the classes that implement it
class Watch_History(object):
	def __init__(self, parameter_switches = None, custom_year = None):
		self.parameter_switches = parameter_switches

		self.Define_Basic_Variables()
		self.Define_Module_Folder()
		self.Define_Texts()

		self.Define_Folders_And_Files()
		self.Define_Lists_And_Dictionaries()
		self.Define_Media_Types()
		self.Define_Episodes_Files()

		# Load Christmas module
		self.Christmas = Christmas()
		self.christmas = self.Christmas.christmas
		self.Today_Is_Christmas = self.Christmas.Today_Is_Christmas

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
		self.texts = self.Language.JSON_To_Python(self.apps_folders["module_files"][self.module["key"]]["texts"])

		self.language_texts = self.Language.Item(self.texts)

		self.large_bar = "-----"
		self.dash_space = "-"

	def Define_Folders_And_Files(self):
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
			self.language_texts["origin_type"],
		]

		self.movie_details_parameters = [
			"Original name - Nome original",
			"Portuguese name - Nome Português",
			"Productor - Produtor",
			"Distributor - Distribuidor",
			"Director - Diretor",
		]

		self.alternative_episode_types = [
			"OVA",
			"ONA",
			"Special",
		]

		# Dictionaries
		self.remote_origins = {
			"Animes Vision": "https://animes.vision/",
			"YouTube": "https://www.youtube.com/",
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
				"media_info": self.folders["media_info"][key],
				"per_media_type": self.folders["watch_history"]["current_year"]["per_media_type"][key]
			}

			# Define "Info.json" file
			self.media_types[plural_media_type]["folders"]["media_info"]["info"] = self.media_types[plural_media_type]["folders"]["media_info"]["root"] + "Info.json"
			self.File.Create(self.media_types[plural_media_type]["folders"]["media_info"]["info"])

			# Read "Info.json" file
			self.media_types[plural_media_type]["json"] = self.Language.JSON_To_Python(self.media_types[plural_media_type]["folders"]["media_info"]["info"])

			# Define media list
			self.media_types[plural_media_type]["media_list"] = []

			format = "{} [{}]"

			if type(self.media_types[plural_media_type]["status"]) == str:
				self.media_types[plural_media_type]["status"] = [self.media_types[plural_media_type]["status"]]

			for status in self.media_types[plural_media_type]["status"]:
				self.media_types[plural_media_type]["media_list"].extend(self.media_types[plural_media_type]["json"]["Status"][status])

			self.media_types[plural_media_type]["media_list"] = sorted(self.media_types[plural_media_type]["media_list"])

			add_status = False			

			# Add status to "media list option" list if add_status is True
			if add_status == True:
				self.media_types[plural_media_type]["media_list_option"] = self.media_types[plural_media_type]["media_list"].copy()

				i = 0
				for media in self.media_types[plural_media_type]["media_list"]:
					for status in self.media_types[plural_media_type]["status"]:
						if media in self.media_types[plural_media_type]["json"]["Status"][status]:
							language_status = self.Get_Language_Status(status)

					self.media_types[plural_media_type]["media_list_option"][i] = format.format(self.media_types[plural_media_type]["media_list_option"][i], language_status)

					i += 1

			self.media_types[plural_media_type].pop("json")

			# Add media list length numbers to media types list to show on select media type
			for language in self.small_languages:
				for item in ["singular", "plural"]:
					self.media_types[plural_media_type][item]["show"] = self.media_types[plural_media_type][item][self.user_language] + " (" + str(len(self.media_types[plural_media_type]["media_list"])) + ")"

			self.media_types[plural_media_type]["texts"]["show"] = self.Text.By_Number(self.media_types[plural_media_type]["media_list"], self.media_types[plural_media_type]["singular"]["show"], self.media_types[plural_media_type]["plural"]["show"])

			i += 1

		# Write media types dictionary into "Media Types.json" file
		self.File.Edit(self.folders["network_data"]["media_types"], self.Language.Python_To_JSON(self.media_types), "w")

	def Define_Episodes_Files(self):
		# Define default Episodes dictionary template
		template = {
			"Number": 0,
			"Comments": 0,
			"Media": [],
			"Episode titles": {},
			"Media Types": [],
			"Times": {
				"ISO8601": [],
				"Language DateTime": {}
			},
			"YouTube IDs": [],
			"Number. Media Type (Time)": [],
			"Dictionary": {}
		}

		self.episodes = template.copy()

		# Add language lists to media and episode titles and episode Language DateTime dictionaries
		for language in self.small_languages:
			self.episodes["Episode titles"][language] = []
			self.episodes["Times"]["Language DateTime"][language] = []

		# If Episodes.json is not empty, get Episodes dictionary from it
		if self.File.Contents(self.folders["watch_history"]["current_year"]["episodes"])["lines"] != []:
			self.episodes = self.Language.JSON_To_Python(self.folders["watch_history"]["current_year"]["episodes"])

		# If Episodes.json is empty, write default Episodes dictionary inside it
		if self.File.Contents(self.folders["watch_history"]["current_year"]["episodes"])["lines"] == []:
			self.File.Edit(self.folders["watch_history"]["current_year"]["episodes"], self.Language.Python_To_JSON(self.episodes), "w")

		# Define default Media Type Episodes dictionary
		self.media_type_episodes = {}

		for plural_media_type in self.media_types["plural"]["en"]:
			key = plural_media_type.lower().replace(" ", "_")

			self.media_type_episodes[plural_media_type] = template.copy()
			self.media_type_episodes[plural_media_type].pop("Media Types")

			# Add language lists to media and episode titles and episode Language DateTime dictionaries
			for language in self.small_languages:
				self.media_type_episodes[plural_media_type]["Episode titles"][language] = []
				self.media_type_episodes[plural_media_type]["Times"]["Language DateTime"][language] = []

			# If Media Type Episodes.json is not empty, get Media Type Episodes dictionary from it
			if self.File.Contents(self.folders["watch_history"]["current_year"]["per_media_type"][key]["episodes"])["lines"] != []:
				self.media_type_episodes[plural_media_type] = self.Language.JSON_To_Python(self.folders["watch_history"]["current_year"]["per_media_type"][key]["episodes"])

			# If Media Type Episodes.json is empty, write default Media Type Episodes dictionary inside it
			if self.File.Contents(self.folders["watch_history"]["current_year"]["per_media_type"][key]["episodes"])["lines"] == []:
				self.File.Edit(self.folders["watch_history"]["current_year"]["per_media_type"][key]["episodes"], self.Language.Python_To_JSON(self.media_type_episodes[plural_media_type]), "w")

		# Get Comments dictionary from file
		self.comments = self.Language.JSON_To_Python(self.folders["comments"]["comments"])

		# If current year is not inside "media type year numbers" dictionary, create the current year media type dictionary
		# And define all of the media type comment numbers as zero
		if str(self.date["year"]) not in self.comments["Media type year numbers"]:
			self.comments["Media type year numbers"][self.date["year"]] = {}

			for plural_media_type in self.media_types["plural"]["en"]:
				self.comments["Media type year numbers"][self.date["year"]][plural_media_type] = 0

			# Update "Comments.json" file with new Comments dictionary
			self.File.Edit(self.folders["comments"]["comments"], self.Language.Python_To_JSON(self.comments), "w")

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
		numbers = self.Language.JSON_To_Python(self.folders["media_info"]["info"])["Numbers"]

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

	def Select_Media(self, options = None, item = False):
		dictionary = {}

		if options != None:
			dictionary = self.Define_Options(dictionary, options)

		media = dictionary["media"]

		if item == True:
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

		# Define media info and local media folder
		if "folders" in media and "root" in media["folders"]:
			media["folders"].update({
				"media": dictionary["media"]["folders"]["media"] + self.Sanitize(media["title"], restricted_characters = True) + "/",
				"media_type_comments": {
					"root": dictionary["media"]["folders"]["media_type_comments"]["root"] + self.Sanitize(media["title"], restricted_characters = True) + "/"
				}
			})

		if "folders" in media and "root" not in media["folders"]:
			media["folders"].update({
				"root": dictionary["media_type"]["folders"]["media_info"]["root"] + self.Sanitize(media["title"], restricted_characters = True) + "/",
				"media": self.root_folders["media"] + self.Sanitize(media["title"], restricted_characters = True) + "/",
			})

		if "folders" not in media:
			media["folders"] = {
				"root": dictionary["media_type"]["folders"]["media_info"]["root"] + self.Sanitize(media["title"], restricted_characters = True) + "/",
				"media": self.root_folders["media"] + self.Sanitize(media["title"], restricted_characters = True) + "/",
				"media_type_comments": {
					"root": self.folders["comments"][dictionary["media_type"]["plural"]["en"].lower()]["root"] + self.Sanitize(media["title"], restricted_characters = True) + "/"
				}
			}

			media["folders"]["media_type_comments"]["comments"] = media["folders"]["media_type_comments"]["root"] + self.texts["comments, title()"]["en"] + ".json"
			self.File.Create(media["folders"]["media_type_comments"]["comments"])

			dict_ = {
				"File names": [],
				"Dictionary": {}
			}

			if self.File.Contents(media["folders"]["media_type_comments"]["comments"])["lines"] == []:
				self.File.Edit(media["folders"]["media_type_comments"]["comments"], self.Language.Python_To_JSON(dict_), "w")

			if dictionary["media_type"]["plural"]["en"] != self.texts["movies"]["en"]:
				media["folders"]["comments"] = {
					"root": media["folders"]["root"] + self.language_texts["comments, title()"] + "/"
				}

		# Create folders
		for key in media["folders"]:
			folder = media["folders"][key]

			if "root" in folder:
				folder = folder["root"]

			if "." not in folder:
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

		dictionary = self.Define_Media_Titles(dictionary, item)

		return dictionary

	def Select_Media_Type_And_Media(self, options = None, status_text = None):
		dictionary = {
			"media_type": {
				"select": True,
				"status": self.texts["watching, title()"]["en"],
			},
			"media": {
				"select": True,
				"list": {},
			},
		}

		if options != None:
			dictionary = self.Define_Options(dictionary, options)

		if dictionary["media_type"]["select"] == True:
			dictionary["media_type"] = self.Select_Media_Type(dictionary["media_type"])

		if dictionary["media"]["select"] == True:
			dictionary["media"] = self.Select_Media(dictionary)["media"]

		return dictionary

	def Define_Media_Titles(self, dictionary, item = False):
		media = dictionary["media"]

		if item == True:
			media = dictionary["media"]["item"]

		if self.File.Exist(media["folders"]["details"]) == True:
			media["details"] = self.File.Dictionary(media["folders"]["details"])

			# Define titles key
			media["titles"] = {
				"original": media["details"][self.language_texts["original_name"]],
				"sanitized": media["details"][self.language_texts["original_name"]],
			}

			# If media type is "Animes", define romanized name and jp name
			if dictionary["media_type"]["plural"]["en"] == self.texts["animes"]["en"]:
				if self.language_texts["romanized_name"] in media["details"]:
					media["titles"]["romanized"] = media["details"][self.language_texts["romanized_name"]]

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
			if media["titles"]["sanitized"][0] + media["titles"]["sanitized"][1] == ": ":
				media["titles"]["sanitized"] = media["titles"]["sanitized"][2:]

			media["titles"]["sanitized"] = self.Sanitize(media["titles"]["sanitized"], restricted_characters = True)

		return dictionary

	def Get_Media_Title(self, dictionary, language = None, item = False, episode = False):
		titles = dictionary["media"]["titles"]

		if item == True:
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

	def Show_Media_Title(self, dictionary):
		if dictionary["media"]["titles"]["language"] == dictionary["media"]["titles"]["original"]:
			print(dictionary["media"]["titles"]["original"])

			if dictionary["media"]["states"]["video"] == True:				
				print()
				print(self.Text.Capitalize(dictionary["media"]["texts"]["item"]) + ":")
				print(dictionary["media"]["item"]["title"])

		if dictionary["media"]["titles"]["language"] != dictionary["media"]["titles"]["original"]:
			print("\t" + dictionary["media"]["titles"]["original"])
			print("\t" + dictionary["media"]["titles"]["language"])

			for language in self.small_languages:
				language_name = self.texts["language_name"][language][self.user_language]

				if language in dictionary["media"]["titles"] and dictionary["media"]["titles"][language] != dictionary["media"]["titles"]["original"]:
					print("\t" + dictionary["media"]["titles"][language])

	def Show_Media_Information(self, dictionary):
		# Show opening this media text
		header_text = dictionary["media_type"]["singular"][self.user_language] + ":"

		if "header_text" in dictionary and "header_text" not in ["", None]:
			header_text = dictionary["header_text"]

		print()
		print(self.large_bar)

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

			media_episode_text = "{} {}".format(self.Text.Capitalize(dictionary["media"]["texts"]["unit"]), dictionary["media_type"]["genders"]["of_the"]) + " "

			if dictionary["media"]["states"]["media_list"] == False or dictionary["media"]["states"]["video"] == True:
				media_episode_text += dictionary["media"]["texts"]["item"]

			else:
				media_episode_text += dictionary["media"]["texts"]["container"]

			print(media_episode_text + ":")
			print(dictionary["media"]["episode"]["title"])
			print()

			text_to_show = self.Text.Capitalize(dictionary["media"]["texts"]["unit"]) + " " + self.language_texts["with_{}_title"].format(dictionary["media_type"]["genders"]["the"] + " " + dictionary["media"]["texts"]["container"])

			# Show media episode (episode with media item) if the media has a media list
			if dictionary["media"]["states"]["media_list"] == True and dictionary["media"]["states"]["video"] == False:
				if dictionary["media"]["item"]["title"] != dictionary["media"]["title"]:
					media_episode_text = self.Text.Capitalize(dictionary["media"]["texts"]["unit"]) + " " + self.language_texts["with_{}"].format(dictionary["media"]["texts"]["item"])

					print(media_episode_text + ":")
					print(dictionary["media"]["episode"]["with_item"][self.user_language])
					print()

					text_to_show += " " + self.language_texts["and_{}"].format(dictionary["media"]["texts"]["item"])

				key = "with_title_and_item"

			# Show only media title with episode if the media has no media list
			if dictionary["media"]["states"]["media_list"] == False and dictionary["media"]["states"]["video"] == False:
				key = "with_title"

			if dictionary["media"]["states"]["video"] == True:
				text_to_show = self.Text.Capitalize(dictionary["media"]["texts"]["unit"]) + " " + self.language_texts["with_{}"].format(self.language_texts["youtube_channel"])

			print(text_to_show + ":")
			print(dictionary["media"]["episode"][key][self.user_language])
			print()

		if "finished_watching" in dictionary["media"]:
			print(self.language_texts["when_i_finished_watching"] + " " + dictionary["media_type"]["genders"]["the"] + " " + dictionary["media"]["texts"]["unit"] + ":")
			print(dictionary["media"]["finished_watching"]["date_time_format"][self.user_language])
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

			print(self.language_texts["you_finished_watching"] + " " + dictionary["media"]["texts"]["this_item"] + " " + dictionary["media_type"]["genders"]["of_the"] + " " + dictionary["media"]["texts"]["container"] + ' "' + dictionary["media"]["titles"]["language"] + '"' + ":")

			dict_ = { 
				"media": {
					"states": dictionary["media"]["states"],
					"titles": dictionary["media"]["item"]["titles"]
				}
			}

			self.Show_Media_Title(dict_)

			if dictionary["media"]["states"]["completed"] == False and dictionary["media"]["states"]["video"] == False:
				print()
				print(self.language_texts["next_{}_to_watch, feminine"].format(dictionary["media"]["texts"]["item"]) + ": ")

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

		if dictionary["media"]["states"]["finished_watching"] == True:
			print()

		if "youtube_id" in dictionary["media"]["episode"]:
			if "next" not in dictionary["media"]["episode"]:
				print()

			print(self.language_texts["youtube_id"] + ":")
			print(dictionary["media"]["episode"]["youtube_id"])

			if "next" in dictionary["media"]["episode"]:
				print()

		if "next" in dictionary["media"]["episode"]:
			text = self.language_texts["next_{}_to_watch, masculine"]

			if dictionary["media"]["texts"]["unit"][0] not in ["C", "N"]:
				dictionary["media"]["texts"]["unit"] = self.Text.Capitalize(dictionary["media"]["texts"]["unit"], lower = True)

			print(text.format(dictionary["media"]["texts"]["unit"]) + ": ")
			print(dictionary["media"]["episode"]["next"])
			print()

		if "completed" in dictionary["media"]["states"] and dictionary["media"]["states"]["completed"] == True:
			print(self.media_dictionary["media"]["item"]["finished_watching_text"])
			print()

		if "first_episode_in_year" in dictionary["media"]["states"] and dictionary["media"]["states"]["first_episode_in_year"] == True:
			items = [
				dictionary["media_type"]["genders"]["this"].title(),
				dictionary["media_type"]["genders"]["the"],
				dictionary["media_type"]["genders"]["first"],
				dictionary["media"]["texts"]["unit"] + " " + self.language_texts["of, neutral"] + " " + dictionary["media"]["texts"]["container"],
				str(self.date["year"])
			]

			print(self.language_texts["{}_is_{}_{}_{}_that_you_watched_in_{}"].format(*items) + ".")
			print()

		if "finished_watching" in dictionary["media"]["states"] and dictionary["media"]["states"]["finished_watching"] == True:
			print(self.large_bar)

			self.Input.Type(self.Language.language_texts["press_enter_when_you_finish_reading_the_info_summary"])
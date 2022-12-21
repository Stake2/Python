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

		self.Define_Lists_And_Dictionaries()
		self.Define_Folders_And_Files()

		self.Christmas = Christmas()
		self.christmas = self.Christmas.christmas
		self.Today_Is_Christmas = self.Christmas.Today_Is_Christmas

		# Create media type texts array with " (number of medias of each media type)" on the right of each media type
		# To use as the choice list of the select media type of Watch_Media() class

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
		self.module_name = self.__module__

		if "." in self.module_name:
			self.module_name = self.module_name.split(".")[0]

		self.module_name_lower = self.module_name.lower()

		self.apps_folders["app_text_files"][self.module_name_lower] = {
			"root": self.apps_folders["app_text_files"]["root"] + self.module_name + "/",
		}

		self.Folder.Create(self.apps_folders["app_text_files"][self.module_name_lower]["root"])

		self.apps_folders["app_text_files"][self.module_name_lower]["texts"] = self.apps_folders["app_text_files"][self.module_name_lower]["root"] + "Texts.json"
		self.File.Create(self.apps_folders["app_text_files"][self.module_name_lower]["texts"])

	def Define_Texts(self):
		self.texts = self.Language.JSON_To_Python(self.apps_folders["app_text_files"][self.module_name_lower]["texts"])

		self.language_texts = self.Language.Item(self.texts)

		self.large_bar = "-----"
		self.dash_space = "-"

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

			"Origin location": {
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

		self.media_type_sub_folders = {}

		for plural_media_type in self.texts["plural_media_types, type: list"]["en"]:
			if plural_media_type != self.texts["plural_media_types, type: list"]["en"][3]:
				self.media_type_sub_folders[plural_media_type] = {}

				self.media_type_sub_folders[plural_media_type]["media_list_text"] = self.texts["seasons, title(), en - pt"]
				self.media_type_sub_folders[plural_media_type]["english_singular_media_list_text"] = self.texts["season"]["en"]

				if plural_media_type == self.texts["plural_media_types, type: list"]["en"][4]:
					self.media_type_sub_folders[plural_media_type]["media_list_text"] = self.texts["series, title(), en - pt"]
					self.media_type_sub_folders[plural_media_type]["english_singular_media_list_text"] = self.texts["series"]["en"]

		self.gender_the_texts = {}

		self.gender_items = ["the", "this", "a", "of", "of_the"]

		for english_plural_media_type in self.texts["plural_media_types, type: list"]["en"]:
			self.gender_the_texts[english_plural_media_type] = {}
			self.gender_the_texts[english_plural_media_type]["masculine"] = {}
			self.gender_the_texts[english_plural_media_type]["feminine"] = {}

			for item in self.gender_items:
				self.gender_the_texts[english_plural_media_type][item] = self.language_texts[item + ", masculine"]

			self.gender_the_texts[english_plural_media_type]["masculine"]["the"] = self.language_texts["the, masculine"]
			self.gender_the_texts[english_plural_media_type]["masculine"]["this"] = self.language_texts["this, masculine"]
			self.gender_the_texts[english_plural_media_type]["masculine"]["of_the"] = self.language_texts["of_the, masculine"]

			self.gender_the_texts[english_plural_media_type]["feminine"]["the"] = self.language_texts["the, feminine"]
			self.gender_the_texts[english_plural_media_type]["feminine"]["this"] = self.language_texts["this, feminine"]
			self.gender_the_texts[english_plural_media_type]["feminine"]["of_the"] = self.language_texts["of_the, feminine"]

			if english_plural_media_type == self.texts["series, title()"]["en"]:
				for item in self.gender_items:
					self.gender_the_texts[english_plural_media_type][item] = self.language_texts[item + ", feminine"]

				self.gender_the_texts[english_plural_media_type]["feminine"]["the"] = self.language_texts["the, feminine"]
				self.gender_the_texts[english_plural_media_type]["feminine"]["this"] = self.language_texts["this, feminine"]
				self.gender_the_texts[english_plural_media_type]["feminine"]["of_the"] = self.language_texts["of_the, feminine"]

	def Define_Folders_And_Files(self):
		# Folder variables
		if "media_folder" in self.app_settings:
			self.root_folders["media"] = self.app_settings["media_folder"]

		self.watch_history_folder = self.notepad_folders["networks"]["audiovisual_media_network"] + "Watch History/"
		self.Folder.Create(self.watch_history_folder)

		self.watched_folder = self.watch_history_folder + "Watched/"
		self.Folder.Create(self.watched_folder)

		self.current_year_watched_media_folder = self.watched_folder + str(self.date["year"]) + "/"
		self.Folder.Create(self.current_year_watched_media_folder)

		self.total_watched_number_current_year_file = self.current_year_watched_media_folder + "Number.txt"

		if self.File.Exist(self.total_watched_number_current_year_file) == False:
			self.File.Edit(self.total_watched_number_current_year_file, "0", "w")

		self.current_year_episode_file = self.current_year_watched_media_folder + "Episodes.txt"
		self.File.Create(self.current_year_episode_file)

		self.episodes_file = self.current_year_watched_media_folder + "Episodes.json"
		self.File.Create(self.episodes_file)

		self.all_watched_files_current_year_folder = self.current_year_watched_media_folder + "All Watched Files/"
		self.Folder.Create(self.all_watched_files_current_year_folder)

		self.per_media_type_current_year_folder = self.current_year_watched_media_folder + "Per Media Type/"
		self.Folder.Create(self.per_media_type_current_year_folder)

		self.per_media_type_files_folder = self.per_media_type_current_year_folder + "Files/"
		self.Folder.Create(self.per_media_type_files_folder)

		self.per_media_type_folders_folder = self.per_media_type_current_year_folder + "Folders/"
		self.Folder.Create(self.per_media_type_folders_folder)

		self.movies_folder = self.watch_history_folder + "Movies/"
		self.Folder.Create(self.movies_folder)

		self.media_info_folder = self.notepad_folders["networks"]["audiovisual_media_network"] + "Media Info/"
		self.Folder.Create(self.media_info_folder)

		self.media_list_file = self.media_info_folder + "Media list - Lista de mídias.txt"
		self.File.Create(self.media_list_file)

		self.media_info_media_details_folder = self.media_info_folder + "Media details/"
		self.Folder.Create(self.media_info_media_details_folder)

		self.media_number_file = self.media_info_media_details_folder + "Media number.txt"
		self.File.Create(self.media_number_file)

		self.comment_writer_folder = self.notepad_folders["networks"]["audiovisual_media_network"] + "Comment_Writer/"
		self.Folder.Create(self.comment_writer_folder)

		self.year_comment_numbers_folder = self.comment_writer_folder + "Year comment numbers/"
		self.Folder.Create(self.year_comment_numbers_folder)

		self.current_year_comment_number_folder = self.year_comment_numbers_folder + str(self.date["year"]) + "/"
		self.Folder.Create(self.current_year_comment_number_folder)

		self.all_comments_folder = self.comment_writer_folder + "All comments - Todos os comentários/"
		self.Folder.Create(self.all_comments_folder)

		# Media info folders and media details folders dictionary
		self.media_info_folders = {}
		self.media_details_folders = {}
		self.watching_status_folders = {}
		self.per_media_type_folder_folders_dict = {}
		self.per_media_type_files_folders = {}
		self.all_comments_media_type_folders = {}

		self.media_info_name_files = {}
		self.media_info_number_files = {}
		self.per_media_type_episode_files = {}
		self.per_media_type_time_files = {}
		self.per_media_type_number_files = {}
		self.all_comment_number_media_type_files = {}
		self.watching_status_files = {}

		self.episode_data = {}

		i = 1
		for plural_media_type in self.texts["plural_media_types, type: list"]["en"]:
			self.watching_status_files[plural_media_type] = {}

			mixed_plural_media_type = self.texts["plural_media_types, type: list, en - pt"][i - 1]

			self.media_info_folders[plural_media_type] = self.media_info_folder + mixed_plural_media_type + "/"
			self.media_details_folders[plural_media_type] = self.media_info_media_details_folder + mixed_plural_media_type + "/"
			self.watching_status_folders[plural_media_type] = self.media_info_media_details_folder + mixed_plural_media_type + "/Watching status/"
			self.per_media_type_folder_folders_dict[plural_media_type] = self.per_media_type_folders_folder + mixed_plural_media_type + "/"
			self.per_media_type_files_folders[plural_media_type] = self.per_media_type_files_folder + mixed_plural_media_type + "/"
			self.all_comments_media_type_folders[plural_media_type] = self.all_comments_folder + mixed_plural_media_type + "/"

			self.Folder.Create(self.media_info_folders[plural_media_type])
			self.Folder.Create(self.media_details_folders[plural_media_type])
			self.Folder.Create(self.watching_status_folders[plural_media_type])
			self.Folder.Create(self.per_media_type_folder_folders_dict[plural_media_type])
			self.Folder.Create(self.per_media_type_files_folders[plural_media_type])
			self.Folder.Create(self.all_comments_media_type_folders[plural_media_type])

			self.media_info_name_files[plural_media_type] = self.media_details_folders[plural_media_type] + "Names.txt"
			self.media_info_number_files[plural_media_type] = self.media_details_folders[plural_media_type] + "Number.txt"
			self.per_media_type_episode_files[plural_media_type] = self.per_media_type_files_folders[plural_media_type] + "Episodes.txt"
			self.per_media_type_time_files[plural_media_type] = self.per_media_type_files_folders[plural_media_type] + "Times.txt"
			self.per_media_type_number_files[plural_media_type] = self.per_media_type_files_folders[plural_media_type] + "Number.txt"
			self.all_comment_number_media_type_files[plural_media_type] = self.all_comments_media_type_folders[plural_media_type] + "/Number.txt"

			if self.File.Exist(self.per_media_type_number_files[plural_media_type]) == False:
				self.File.Edit(self.per_media_type_number_files[plural_media_type], "0", "w")

			if self.File.Contents(self.all_comment_number_media_type_files[plural_media_type])["length"] == 0:
				self.File.Edit(self.all_comment_number_media_type_files[plural_media_type], "0", "w")

			self.File.Create(self.media_info_name_files[plural_media_type])
			self.File.Create(self.media_info_number_files[plural_media_type])
			self.File.Create(self.per_media_type_episode_files[plural_media_type])
			self.File.Create(self.per_media_type_time_files[plural_media_type])
			self.File.Create(self.per_media_type_number_files[plural_media_type])
			self.File.Create(self.all_comment_number_media_type_files[plural_media_type])

			for watching_status in self.language_texts["watching_statuses, type: list"]:
				self.watching_status_files[plural_media_type][watching_status] = self.watching_status_folders[plural_media_type] + watching_status + ".txt"
				self.File.Create(self.watching_status_files[plural_media_type][watching_status])

			self.episode_data[plural_media_type] = self.File.Contents(self.per_media_type_episode_files[plural_media_type])["lines"]

			i += 1

		self.watched_files = {}

		for watched_text in ["Episodes", "Media Types", "Times", "Names"]:
			self.watched_files[watched_text] = self.current_year_watched_media_folder + watched_text + ".txt"
			self.File.Create(self.watched_files[watched_text])

		self.movie_files = {}

		for movie_text in ["Names", "Times"]:
			self.movie_files[movie_text] = self.movies_folder + movie_text + ".txt"
			self.File.Create(self.movie_files[movie_text])

		# All Comments Number file
		self.all_comments_number_file = self.comment_writer_folder + "All comments number.txt"
		self.File.Create(self.all_comments_number_file)

		if self.File.Contents(self.all_comments_number_file)["length"] == 0:
			self.File.Edit(self.all_comments_number_file, "0", "w")

		# Year Comment Number file
		self.year_comment_number_file = self.current_year_comment_number_folder + "Number.txt"
		self.File.Create(self.year_comment_number_file)

		if self.File.Contents(self.year_comment_number_file)["length"] == 0:
			self.File.Edit(self.year_comment_number_file, "0", "w")

		self.episode_data["watched_number"] = self.File.Contents(self.total_watched_number_current_year_file)["lines"][0]
		self.episode_data["comment_number"] = self.File.Contents(self.year_comment_number_file)["lines"][0]

		self.File.Edit(self.episodes_file, self.Language.Python_To_JSON(self.episode_data), "w")

	def Define_The_Text(self, plural_media_type, item_dictionary = None):
		if type(plural_media_type) == dict:
			plural_media_type = plural_media_type["en"]

		the_text = self.gender_the_texts[plural_media_type]["the"]
		this_text = self.gender_the_texts[plural_media_type]["this"]
		of_text = self.gender_the_texts[plural_media_type]["of"]
		of_the_text = self.gender_the_texts[plural_media_type]["of_the"]

		if item_dictionary != None:
			item_dictionary["main_media_type"] = item_dictionary["singular_media_types"]["language"]
			item_dictionary["media_item_name"] = item_dictionary["singular_media_types"]["language"]

			if self.is_series_media == True:
				item_dictionary["main_media_type"] = self.language_texts["season"]
				item_dictionary["media_item_name"] = self.language_texts["season"]
				item_dictionary["the_text"] = self.gender_the_texts[self.plural_media_types["en"]]["feminine"]["the"]

				if self.is_video_series_media == True:
					item_dictionary["main_media_type"] = self.language_texts["channel"]
					item_dictionary["media_item_name"] = self.language_texts["youtube_video_series"]

			return item_dictionary

		if item_dictionary == None:
			return the_text, this_text, of_text, of_the_text

	def Remove_Media_Type(self, media_types):
		if type(media_types) == str:
			media_types = [media_types]

		texts = self.texts.copy()

		for language in self.small_languages:
			for item in media_types:
				if item in texts["plural_media_types, type: list"][language]:
					texts["plural_media_types, type: list"][language].remove(item)

				if item in self.media_info_folders:
					self.media_info_folders.pop(item)

		return texts

	def Create_Media_List(self, status_text = None, plural_media_types = None):
		if status_text == None:
			status_text = self.language_texts["watching, title()"]

		if plural_media_types == None:
			plural_media_types = self.texts["plural_media_types, type: list"]["en"]

		# Media titles dictionary
		media_titles = {}

		i = 0
		for media_info_folder in self.media_info_folders.values():
			current_watching_status = []

			english_media_type = plural_media_types[i]

			if type(status_text) == str:
				self.first_status_file = self.watching_status_files[english_media_type][status_text]

				current_watching_status.extend(self.File.Contents(self.first_status_file)["lines"])

				if status_text == self.language_texts["watching, title()"]:
					self.second_status_file = self.watching_status_files[english_media_type][self.language_texts["re_watching, title()"]]

					current_watching_status.extend(self.File.Contents(self.second_status_file)["lines"])

			if type(status_text) == list:
				for local_status_text in status_text:
					self.status_file = self.watching_status_files[english_media_type][local_status_text]

					current_watching_status.extend(self.File.Contents(self.status_file)["lines"])

			media_titles[english_media_type] = sorted(current_watching_status)

			for self.media_title in media_titles[english_media_type]:
				self.local_media_folder = self.root_folders["media"] + self.Sanitize(self.media_title, restricted_characters = True) + "/"
				self.Folder.Create(self.local_media_folder)

			i += 1

		return media_titles

	def Select_Media_Type(self, language_media_type_list = None, texts = None):
		show_text = self.language_texts["media_types"]

		if texts != None and texts[0] != None:
			show_text = texts[0]

		select_text = self.language_texts["select_one_media_type_to_watch"]

		if texts != None and texts[1] != None:
			select_text = texts[1]

		self.language_media_type_list = self.language_texts["plural_media_types, type: list"]

		if language_media_type_list != None:
			self.language_media_type_list = language_media_type_list

		# Select
		dictionary = self.Input.Select(self.texts["plural_media_types, type: list"]["en"], self.language_media_type_list, show_text = show_text, select_text = select_text)

		option_info = {
			"media_type_number": dictionary["number"],
		}

		media_type_number = option_info["media_type_number"]

		option_info["plural_media_type"] = {}

		for language in self.small_languages:
			if language in self.texts["plural_media_types, type: list"]:
				option_info["plural_media_type"][language] = self.texts["plural_media_types, type: list"][language][media_type_number]

		option_info["plural_media_type"]["language"] = self.Language.Item(option_info["plural_media_type"])

		option_info["singular_media_type"] = {}

		for language in self.small_languages:
			if language in self.texts["media_types, type: list"]:
				option_info["singular_media_type"][language] = self.texts["media_types, type: list"][language][media_type_number]

		option_info["singular_media_type"]["language"] = self.Language.Item(option_info["singular_media_type"])

		option_info["language_singular_media_type"] = self.Language.Item(option_info["singular_media_type"])

		option_info["mixed_plural_media_type"] = self.texts["plural_media_types, type: list, en - pt"][media_type_number]

		option_info["media_info_media_type_folder"] = self.media_info_folders[option_info["plural_media_type"]["en"]]

		option_info["watching_status_files"] = {}

		for watching_status in self.language_texts["watching_statuses, type: list"]:
			option_info["watching_status_files"][watching_status] = self.watching_status_files[option_info["plural_media_type"]["en"]][watching_status]

		option_info["watching_status_media"] = {}

		for watching_status in option_info["watching_status_files"]:
			option_info["watching_status_media"][watching_status] = self.File.Contents(option_info["watching_status_files"][watching_status])["lines"]

		return option_info

	def Define_Media_Titles(self, option_info):
		if self.File.Exist(option_info["media_details_file"]) == True:
			option_info["media_details"] = self.File.Dictionary(option_info["media_details_file"])

			option_info["media_titles"] = {}

			option_info["media_titles"]["original"] = option_info["media_details"][self.language_texts["original_name"]]

			if option_info["plural_media_types"]["en"] == self.texts["animes"]["en"]:
				if self.language_texts["romanized_name"] in option_info["media_details"]:
					option_info["media_titles"]["romanized"] = option_info["media_details"][self.language_texts["romanized_name"]]

				option_info["media_titles"]["jp"] = option_info["media_details"][self.language_texts["original_name"]]

			for language in self.small_languages:
				language_name = self.texts["language_name"][language][self.user_language]

				for key in option_info["media_details"]:
					if language_name == key:
						option_info["media_titles"][language] = option_info["media_details"][language_name]

			option_info["media_titles"]["language"] = option_info["media_titles"]["original"]

			if self.user_language in option_info["media_titles"]:
				option_info["media_titles"]["language"] = option_info["media_titles"][self.user_language]

			if self.user_language not in option_info["media_titles"] and option_info["plural_media_types"]["en"] == self.texts["animes"]["en"]:
				option_info["media_titles"]["language"] = option_info["media_titles"]["romanized"]

		return option_info

	def Select_Media(self, plural_media_types, singular_media_types, mixed_plural_media_type, media_list, media_info_media_type_folder, texts = None):
		self.a_text = self.gender_the_texts[plural_media_types["en"]]["a"]

		show_text = self.Text.By_Number(media_list, singular_media_types["language"], plural_media_types["language"])

		select_text = singular_media_types["language"].lower()

		if plural_media_types["en"] == self.texts["videos"]["en"]:
			show_text = self.Text.By_Number(media_list, self.language_texts["channel, title()"], self.language_texts["channels, title()"])
			select_text = self.language_texts["channel, title()"]

		if texts != None and texts[0] != None:
			show_text = texts[0]

		select_text = self.language_texts["select_{}_to_watch"].format(self.a_text + " " + select_text)

		if texts != None and texts[1] != None:
			select_text = texts[1]

		option_info = {}

		option_info["plural_media_types"] = plural_media_types

		# Select
		option_info["media"] = self.Input.Select(media_list, show_text = show_text, select_text = select_text)["option"]

		option_info["media_folder"] = media_info_media_type_folder + self.Sanitize(option_info["media"], restricted_characters = True) + "/"

		option_info["media_details_file"] = option_info["media_folder"] + "Media details.txt"

		option_info["media_details"] = {}

		option_info = self.Define_Media_Titles(option_info)

		if plural_media_types["en"] == self.texts["movies"]["en"]:
			option_info["movie_details_file"] = option_info["media_folder"] + "Movie details.txt"
			option_info["movie_details"] = self.File.Dictionary(option_info["movie_details_file"], next_line = True)

		return option_info

	def Select_Media_Type_And_Media(self, options = None, status_text = None):
		self.select_media_type = True
		self.select_media = True

		self.media_type_list = self.texts["plural_media_types, type: list"]["en"]
		self.language_media_type_list = self.language_texts["plural_media_types, type: list"]

		items = [
			"media_type_list",
			"language_media_type_list",
			"select_media_type",
			"select_media",
			"media_list",
			"media_type_show_text",
			"media_type_select_text",
			"media_show_text",
			"media_select_text",
		]

		if options == None:
			options = {}

			for item in items:
				if item not in ["select_media_type", "select_media"]:
					options[item] = None

			options["select_media_type"] = True
			options["select_media"] = True

		if options != None:
			for item in items:
				if item not in ["select_media_type", "select_media"] and item not in options:
					options[item] = None

			if "select_media_type" not in options:
				options["select_media_type"] = True

			if "select_media" not in options:
				options["select_media"] = True

		if "media_type_list" in options and options["media_type_list"] != None:
			self.media_type_list = options["media_type_list"]

		if "media_list" in options and options["media_list"] != None:
			self.media_list = options["media_list"]

		self.status_text = status_text

		if self.status_text == None:
			self.status_text = self.language_texts["watching, title()"]

		option_info = {}

		if options["select_media_type"] == True:
			option_info.update(self.Select_Media_Type(language_media_type_list = self.language_media_type_list, texts = [options["media_type_show_text"], options["media_type_select_text"]]))

			self.media_type_number = option_info["media_type_number"]

			self.plural_media_types = option_info["plural_media_type"]
			self.singular_media_types = option_info["singular_media_type"]
			self.mixed_plural_media_type = option_info["mixed_plural_media_type"]

			self.media_info_media_type_folder = option_info["media_info_media_type_folder"]

			watching_status_files = option_info["watching_status_files"]
			watching_status_media = option_info["watching_status_media"]

			self.all_media_names = self.File.Contents(self.media_info_name_files[self.plural_media_types["en"]])["lines"]

			self.media_titles = self.Create_Media_List(self.status_text, self.media_type_list)

			if options == None or "media_list" not in options or "media_list" in options and options["media_list"] == None:
				self.media_list = self.media_titles[self.plural_media_types["en"]]

			if options != None and "media_list" in options and options["media_list"] != None:
				self.media_list = options["media_list"]

				if options["media_list"] == "all":
					self.media_list = self.all_media_names

		if options["select_media"] == True:
			media_information = self.Select_Media(self.plural_media_types, self.singular_media_types, self.mixed_plural_media_type, self.media_list, self.media_info_media_type_folder, texts = [options["media_show_text"], options["media_select_text"]])

			self.media = media_information["media"]

			self.media_folder = media_information["media_folder"]

			self.media_details = media_information["media_details"]
			self.media_details_file = media_information["media_details_file"]

			self.is_series_media = True

			if self.plural_media_types["en"] == self.texts["movies"]["en"]:
				self.is_series_media = False
		
			if self.is_series_media == False:
				self.movie_details_file = media_information["movie_details_file"]
				self.movie_details = media_information["movie_details"]

			media_information.update(option_info)
			option_info = media_information

		return option_info

	def Show_Media_Title(self, media_dictionary):
		if media_dictionary["media_titles"]["language"] == media_dictionary["media_titles"]["original"]:
			print(media_dictionary["media_titles"]["original"])

			if media_dictionary["is_video_series_media"] == True:				
				print()
				print(self.Text.Capitalize(media_dictionary["media_item_name"]) + ":")
				print(media_dictionary["media_item"])

		if media_dictionary["media_titles"]["language"] != media_dictionary["media_titles"]["original"]:
			print("\t" + media_dictionary["media_titles"]["original"])

			if media_dictionary["is_video_series_media"] == False:
				if media_dictionary["plural_media_types"]["en"] == self.texts["animes"]["en"]:
					print("\t" + media_dictionary["media_titles"]["romanized"])

				for language in self.small_languages:
					language_name = self.texts["language_name"][language][self.user_language]

					if language in media_dictionary["media_titles"] and media_dictionary["media_titles"][language] not in [media_dictionary["media_titles"]["original"]]:
						print("\t" + media_dictionary["media_titles"][language])

	def Show_Media_Information(self, media_dictionary):
		media_title = media_dictionary["media_title"]
		media_titles = media_dictionary["media_titles"]

		media_details = media_dictionary["media_details"]

		media_item = media_dictionary["media_item"]
		language_media_item = media_dictionary["language_media_item"]

		media_episode = media_dictionary["media_episode"]

		plural_media_types = media_dictionary["plural_media_types"]
		singular_media_types = media_dictionary["singular_media_types"]
		mixed_plural_media_type = media_dictionary["mixed_plural_media_type"]

		is_series_media = media_dictionary["is_series_media"]
		is_video_series_media = media_dictionary["is_video_series_media"]

		no_media_list = media_dictionary["no_media_list"]

		media_the_text = self.media_dictionary["of_the_text"] + " " + singular_media_types["language"].lower()

		# Show opening this media text
		header_text = singular_media_types["language"] + ":"

		if "header_text" in media_dictionary and "header_text" not in ["", None]:
			header_text = media_dictionary["header_text"]

		print()
		print(self.large_bar)

		if "completed_media" in media_dictionary and media_dictionary["completed_media"] == True:
			print()
			print(self.language_texts["congratulations"] + "! :3")

		print()
		print(header_text)

		self.Show_Media_Title(media_dictionary)

		print()

		# Show media episode if the media is series media (not a movie)
		if is_series_media == True:
			if is_video_series_media == True:
				self.media_dictionary["of_the_text"] = self.gender_the_texts[plural_media_types["en"]]["feminine"]["of_the"]

			media_episode_text = "{} {}".format(self.Text.Capitalize(media_dictionary["media_unit_name"]), self.media_dictionary["of_the_text"]) + " "

			if no_media_list == True or is_video_series_media == True:
				media_episode_text += media_dictionary["media_item_name"]

			else:
				media_episode_text += media_dictionary["media_container_name"]

			print(media_episode_text + ":")
			print(media_episode)
			print()

			text_to_show = self.Text.Capitalize(media_dictionary["media_unit_name"]) + " " + self.language_texts["with_{}_title"].format(self.media_dictionary["the_text"] + " " + media_dictionary["media_container_name"])

			# Show media item episode (media episode with media item) if the media has a media list
			if no_media_list == False and is_video_series_media == False:
				if media_item != media_title:
					media_episode_text = self.Text.Capitalize(media_dictionary["media_unit_name"]) + " " + self.language_texts["with_{}"].format(media_dictionary["media_item_name"])

					print(media_episode_text + ":")
					print(language_media_item["language"]["episode"])
					print()

				if media_item != media_title:
					text_to_show += " " + self.language_texts["and_{}"].format(media_dictionary["media_item_name"])

			if is_video_series_media == True:
				text_to_show = self.Text.Capitalize(media_dictionary["media_unit_name"]) + " " + self.language_texts["with_{}"].format(self.language_texts["youtube_channel"])

			print(text_to_show + ":")
			print(language_media_item[self.user_language]["episode_with_title"])
			print()

		if "completed_media_item" in media_dictionary and media_dictionary["completed_media_item"] == True:
			print(self.language_texts["congratulations"] + "! :3")
			print()

			print(self.language_texts["you_finished_watching_this_{}_of_{}"].format(media_dictionary["media_item_name"], self.media_dictionary["of_the_text"] + " " + singular_media_types["language"].lower() + ' "' + media_dictionary["media_titles"]["language"] + '"') + ":")
			print(media_dictionary["language_media_item"]["language"]["title"])

			if media_dictionary["completed_media"] == False and media_dictionary["is_video_series_media"] == False:
				print()
				print(self.language_texts["next_{}_to_watch, feminine"].format(media_dictionary["media_item_name"]) + ": ")
				print(media_dictionary["language_next_media_item"])

			print()

		# Show media type
		print(self.language_texts["media_type"] + ":")
		print(self.Language.Item(plural_media_types))
		print()

		# Show mixed media type
		if plural_media_types["en"] != self.texts["plural_media_types, type: list"]["en"][0]:
			print(self.language_texts["mixed_media_type"] + ":")
			print(mixed_plural_media_type)
			print()

		if "media_unit" in media_dictionary:
			# Show media unit text and Media_Unit
			print(self.language_texts["media_unit"] + ":")
			print(media_dictionary["media_unit"])

		if "youtube_video_id" in media_dictionary and media_dictionary["youtube_video_id"] != None:
			if "next_episode_to_watch" not in media_dictionary:
				print()

			print(self.language_texts["youtube_ids"] + ":")
			print(media_dictionary["youtube_video_id"])

			if "next_episode_to_watch" in media_dictionary:
				print()

		if "first_watched_in_year" in media_dictionary and media_dictionary["first_watched_in_year"] == True:
			print(self.language_texts["this_is_{}_first_{}_that_you_watch_in_{}"].format(self.media_dictionary["of_the_text"], singular_media_types["language"].lower(), self.date["year"]) + ".")
			print()

		if "finished_watching_time" in media_dictionary:
			print(self.language_texts["when_i_finished_watching"] + " " + self.media_dictionary["of_the_text"] + " " + media_dictionary["media_unit_name"] + ":")
			print(media_dictionary["finished_watching_time"])
			print()

		if "food" in media_dictionary:
			print(self.language_texts["food, en - pt"] + ":")
			print(media_dictionary["food"])
			print()

		if "drink" in media_dictionary:
			print(self.language_texts["drink, en - pt"] + ":")
			print(media_dictionary["drink"])
			print()

		if "next_episode_to_watch" in media_dictionary:
			text = self.language_texts["next_{}_to_watch, masculine"]

			if media_dictionary["media_unit_name"][0] not in ["C", "N"]:
				media_dictionary["media_unit_name"] = self.Text.Capitalize(media_dictionary["media_unit_name"], lower = True)

			print(text.format(media_dictionary["media_unit_name"]) + ": ")
			print(media_dictionary["next_episode_to_watch"])
			print()

		if "completed_media" in media_dictionary and media_dictionary["completed_media"] == True:
			print(self.language_texts["new_watching_status"] + ":")
			print(media_details[self.language_texts["status, title()"]])
			print()

			# Started watching media time text and day
			print(self.language_texts["when_you_started_to_watch"] + ":")
			print(media_dictionary["started_watching"])
			print()

			# Finished watching media time text and day
			print(self.language_texts["when_you_finished_watching"] + ":")
			print(media_dictionary["finished_watching"])
			print()

			print(self.language_texts["time_that_you_spent_watching"] + ":")
			print(media_dictionary["time_spent_watching"])
			print()

		if "finished_watching" in media_dictionary:
			print(self.large_bar)

			self.Input.Type(self.Language.language_texts["press_enter_when_you_finish_reading_the_info_summary"])
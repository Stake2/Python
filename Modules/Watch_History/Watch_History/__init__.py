# Watch History.py

# Script Helper importer
from Script_Helper import *

# Main class Watch_History that provides lists, dictionaries, folders, and files to other classes that implements it
class Watch_History(object):
	def __init__(self, parameter_switches = None, custom_year = None):
		# Verbose variable
		self.verbose = False

		self.testing_script = False

		self.parameter_switches = parameter_switches

		self.current_year = current_year
		self.custom_year = custom_year

		self.Define_Basic_Variables()

		if self.custom_year != None:
			self.current_year = str(self.custom_year)

		self.Define_Media_Types()
		self.Define_Texts()
		self.Define_Watch_History_Folders()
		self.Create_Arrays_And_Dictionaries()
		self.Define_File_Lists()
		self.Create_Unexistent_Folders_And_Files()

		# Create media type texts array with " (number of medias of each media type)" on the right of each media type
		# To use as the choice list of the select media type of Watch_Media() class

	def Define_Basic_Variables(self):
		self.option = True

		# Global Switches dictionary
		self.global_switches = {
			"write_to_file": self.option,
			"create_files": self.option,
			"create_folders": self.option,
			"move_files": self.option,
			"verbose": self.verbose,
			"testing_script": self.testing_script,
		}

		if self.parameter_switches != None:
			self.global_switches = self.parameter_switches
			self.testing_script = self.global_switches["testing_script"]

		if self.global_switches["testing_script"] == True:
			print(Language_Item_Definer("Testing script: Yes", "Testando script: Sim"))

		if self.global_switches["verbose"] == True:
			print(Language_Item_Definer("Verbose on", "Verbose ligado") + ".")

		if self.global_switches["testing_script"] == True:
			self.global_switches["write_to_file"] = False
			self.global_switches["create_files"] = False
			self.global_switches["move_files"] = False

		self.dot_text = ".txt"

		self.media_type_separator = " - "
		self.media_info_setting_separator = ": "
		self.dot_mp4 = ".mp4"
		self.dot_mkv = ".mkv"

	# Defines the Watch History texts
	def Define_Media_Types(self):
		# Media Type text arrays
		self.media_type_names = [
			None,
			"Animes",
			"Cartoons",
			"Series",
			"Movies",
			"Videos",
		]

		self.media_type_names_without_none = [
			"Animes",
			"Cartoons",
			"Series",
			"Movies",
			"Videos",
		]

		self.media_type_names_english = [
			None,
			"Anime",
			"Cartoon",
			"Series",
			"Movie",
			"Video",
		]

		self.media_type_names_english_plural = [
			None,
			"Animes",
			"Cartoons",
			"Series",
			"Movies",
			"Videos",
		]

		self.media_type_names_portuguese = [
			None,
			"Anime",
			"Desenho",
			"Série",
			"Filme",
			"Vídeo",
		]

		self.media_type_names_portuguese_plural = [
			None,
			"Animes",
			"Desenhos",
			"Séries",
			"Filmes",
			"Vídeos",
		]

		# Media Type text variables
		self.anime_media_type_number = 1
		self.anime_media_type = self.media_type_names[self.anime_media_type_number]
		self.anime_media_type_english = self.media_type_names_english[self.anime_media_type_number]
		self.anime_media_type_portuguese = self.media_type_names_portuguese[self.anime_media_type_number]
		self.anime_media_type_english_plural = self.media_type_names_english_plural[self.anime_media_type_number]
		self.anime_media_type_portuguese_plural = self.media_type_names_portuguese_plural[self.anime_media_type_number]

		self.cartoon_media_type_number = 2
		self.cartoon_media_type = self.media_type_names[self.cartoon_media_type_number]
		self.cartoon_media_type_english = self.media_type_names_english[self.cartoon_media_type_number]
		self.cartoon_media_type_portuguese = self.media_type_names_portuguese[self.cartoon_media_type_number]
		self.cartoon_media_type_english_plural = self.media_type_names_english_plural[self.cartoon_media_type_number]
		self.cartoon_media_type_portuguese_plural = self.media_type_names_portuguese_plural[self.cartoon_media_type_number]

		self.series_media_type_number = 3
		self.series_media_type = self.media_type_names[self.series_media_type_number]
		self.series_media_type_english = self.media_type_names_english[self.series_media_type_number]
		self.series_media_type_portuguese = self.media_type_names_portuguese[self.series_media_type_number]
		self.series_media_type_english_plural = self.media_type_names_english_plural[self.series_media_type_number]
		self.series_media_type_portuguese_plural = self.media_type_names_portuguese_plural[self.series_media_type_number]

		self.movie_media_type_number = 4
		self.movie_media_type = self.media_type_names[self.movie_media_type_number]
		self.movie_media_type_english = self.media_type_names_english[self.movie_media_type_number]
		self.movie_media_type_portuguese = self.media_type_names_portuguese[self.movie_media_type_number]
		self.movie_media_type_english_plural = self.media_type_names_english_plural[self.movie_media_type_number]
		self.movie_media_type_portuguese_plural = self.media_type_names_portuguese_plural[self.movie_media_type_number]

		self.video_media_type_number = 5
		self.video_media_type = self.media_type_names[self.video_media_type_number]
		self.video_media_type_english = self.media_type_names_english[self.video_media_type_number]
		self.video_media_type_portuguese = self.media_type_names_portuguese[self.video_media_type_number]
		self.video_media_type_english_plural = self.media_type_names_english_plural[self.video_media_type_number]
		self.video_media_type_portuguese_plural = self.media_type_names_portuguese_plural[self.video_media_type_number]

		self.mixed_media_type_names = [
			None,
			self.anime_media_type,
			self.cartoon_media_type_english + self.media_type_separator + self.cartoon_media_type_portuguese,
			self.series_media_type_english + self.media_type_separator + self.series_media_type_portuguese,
			self.movie_media_type_english + self.media_type_separator + self.movie_media_type_portuguese,
			self.video_media_type_english + self.media_type_separator + self.video_media_type_portuguese,
		]

		self.mixed_media_type_names_plural = [
			None,
			self.anime_media_type,
			self.cartoon_media_type_english_plural + self.media_type_separator + self.cartoon_media_type_portuguese_plural,
			self.series_media_type_english_plural + self.media_type_separator + self.series_media_type_portuguese_plural,
			self.movie_media_type_english_plural + self.media_type_separator + self.movie_media_type_portuguese_plural,
			self.video_media_type_english_plural + self.media_type_separator + self.video_media_type_portuguese_plural,
		]

		self.mixed_media_type_names_plural_without_none = [
			self.anime_media_type,
			self.cartoon_media_type_english_plural + self.media_type_separator + self.cartoon_media_type_portuguese_plural,
			self.series_media_type_english_plural + self.media_type_separator + self.series_media_type_portuguese_plural,
			self.movie_media_type_english_plural + self.media_type_separator + self.movie_media_type_portuguese_plural,
			self.video_media_type_english_plural + self.media_type_separator + self.video_media_type_portuguese_plural,
		]

		self.mixed_media_type_anime = self.mixed_media_type_names[self.anime_media_type_number]
		self.mixed_media_type_cartoon = self.mixed_media_type_names[self.cartoon_media_type_number]
		self.mixed_media_type_series = self.mixed_media_type_names[self.series_media_type_number]
		self.mixed_media_type_movie = self.mixed_media_type_names[self.movie_media_type_number]
		self.mixed_media_type_video = self.mixed_media_type_names[self.video_media_type_number]

		self.mixed_media_type_anime_plural = self.mixed_media_type_names_plural[self.anime_media_type_number]
		self.mixed_media_type_cartoon_plural = self.mixed_media_type_names_plural[self.cartoon_media_type_number]
		self.mixed_media_type_series_plural = self.mixed_media_type_names_plural[self.series_media_type_number]
		self.mixed_media_type_movie_plural = self.mixed_media_type_names_plural[self.movie_media_type_number]
		self.mixed_media_type_video_plural = self.mixed_media_type_names_plural[self.video_media_type_number]

	def Define_Texts(self):
		self.large_bar = "-----"
		self.dash_space = "-"

		# File and folder texts variables
		self.watched_english_text = "Watched"
		self.movies_english_text = "Movies"

		self.all_watched_files_english_text = "All Watched Files"
		self.per_media_type_english_text = "Per Media Type"

		self.episodes_english_text = "Episodes"
		self.folders_english_text = "Folders"
		self.files_english_text = "Files"
		self.media_types_english_text = "Media Types"
		self.status_english_text = "Status"

		self.names_english_text = "Names"
		self.times_english_text = "Times"

		self.titles_english_text = "Titles"
		self.titles_portuguese_text = "Títulos"
		self.titles_text = Language_Item_Definer(self.titles_english_text, self.titles_portuguese_text)
		self.mixed_titles_text = self.titles_english_text + self.media_type_separator + self.titles_portuguese_text

		self.dates_english_text = "Dates"
		self.dates_portuguese_text = "Datas"
		self.dates_text = Language_Item_Definer(self.dates_english_text, self.dates_portuguese_text)
		self.mixed_dates_text = self.dates_english_text + self.media_type_separator + self.dates_portuguese_text

		self.youtube_name = "YouTube"
		self.animes_vision_name = "Animes Vision"

		self.remote_origin_names = [
			self.animes_vision_name,
			self.youtube_name,		
		]

		self.remote_origin_links = {
			self.animes_vision_name: "https://animes.vision/",
			self.youtube_name: "https://www.youtube.com/",
		}

		self.remote_origin_link_names = {
			self.animes_vision_name: self.animes_vision_name,
			self.youtube_name: self.youtube_name,
		}

		self.english_season_text = "Season"
		self.english_seasons_text = self.english_season_text + "s"
		self.mixed_seasons_text = self.english_seasons_text + self.media_type_separator + "Temporadas"

		self.english_series_text = "Series"
		self.mixed_series_text = self.english_series_text + self.media_type_separator + "Séries"

		self.youtube_ids_english_text = self.youtube_name + " IDs"

		self.comment_english_text = "Comment"
		self.comments_english_text = self.comment_english_text + "s"

		self.comment_portuguese_text = "Comentário"
		self.comments_portuguese_text = self.comment_portuguese_text + "s"

		self.comment_text = Language_Item_Definer(self.comment_english_text, self.comment_portuguese_text)
		self.comments_text = Language_Item_Definer(self.comments_english_text, self.comments_portuguese_text)

		self.mixed_comment_text = self.comment_english_text + self.media_type_separator + self.comment_portuguese_text
		self.mixed_comments_text = self.comments_english_text + self.media_type_separator + self.comments_portuguese_text

		self.started_watching_in_english_text = "Started watching in"
		self.started_watching_in_portuguese_text = "Comecei a assistir em"
		self.started_watching_in_text = Language_Item_Definer(self.started_watching_in_english_text, self.started_watching_in_portuguese_text)
		self.mixed_started_watching_in_text = self.started_watching_in_english_text + self.media_type_separator + self.started_watching_in_portuguese_text

		self.torrent_text = "Torrent"

		self.number_english_text = "Number"
		self.number_portuguese_text = "Número"
		self.number_text = Language_Item_Definer(self.number_english_text, self.number_portuguese_text)
		self.numbers_english_text = self.number_english_text + "s"
		self.numbers_portuguese_text = self.number_english_text + "s"

		self.and_english_text = "And"
		self.and_portuguese_text = "E"
		self.and_text = Language_Item_Definer(self.and_english_text, self.and_portuguese_text)
		self.and_text_lower = self.and_text.lower()

		self.media_details_english_text = "Media Details"
		self.movie_details_english_text = "Movie Details"
		self.series_details_english_text = "Series Details"

		self.subbed_english_text = "Subbed"
		self.dubbed_english_text = "Dubbed"

		self.subbed_portuguese_text = "Legendado"
		self.dubbed_portuguese_text = "Dublado"

		self.mixed_subbed_text = self.subbed_english_text + self.media_type_separator + self.subbed_portuguese_text
		self.mixed_dubbed_text = self.dubbed_english_text + self.media_type_separator + self.dubbed_portuguese_text

		self.remote_english_text = "Remote"
		self.local_english_text = "Local"
		self.hybrid_english_text = "Hybrid"

		self.english_origin_types = [
			self.remote_english_text,
			self.local_english_text,
			self.hybrid_english_text,
		]

		self.portuguese_origin_types = [
			"Remoto",
			"Local",
			"Híbrido",
		]

		self.portuguese_origin_types_dict = {
			"Remote": "Remoto",
			"Local": "Local",
			"Hybrid": "Híbrido",
		}

		self.english_watching_statuses = [
			"Plan To Watch",
			"Watching",
			"Completed",
			"Re-Watching",
			"On Hold",
		]

		self.portuguese_watching_statuses = [
			"Planejo Assistir",
			"Assistindo",
			"Completado",
			"Re-Assistindo",
			"Em Pausa",
		]

		self.alternative_episode_types = [
			"OVA",
			"ONA",
			"Special",
		]

		self.origin_types_language = Language_Item_Definer(self.english_origin_types, self.portuguese_origin_types)
		self.watching_statuses_language = Language_Item_Definer(self.english_watching_statuses, self.portuguese_watching_statuses)

		self.default_portuguese_template_parameters = {
			"Original Name": "Nome Original",
			"Portuguese Name": "Nome Português",
			"Year": "Ano",
			"Has Dub": "Tem Dublagem",
			"Status": "Status",
			"Origin Type": "Tipo de Origem",
			"Origin Location": "Local de Origem",
			"Remote Origin": "Origem Remota",
			"Episode": "Episódio",
		}

		self.media_details_parameters = [
			"Original Name",
			"Year",
			"Has Dub",
			"Status",
			"Origin Type",
		]

		self.media_details_string_parameters = {
			"Original Name": {
				"choice_text": Language_Item_Definer("Original Name", self.default_portuguese_template_parameters["Original Name"]),
				"default": "",
			},

			"Portuguese Name": {
				"choice_text": Language_Item_Definer("Portuguese Name", self.default_portuguese_template_parameters["Portuguese Name"]),
				"default": {
					"format_name": "Original Name",
				},
			},

			"Year": {
				"choice_text": Language_Item_Definer("Year", self.default_portuguese_template_parameters["Year"]),
				"default": time.strftime("%Y"),
			},
		}

		self.media_details_choice_list_parameters = {
			"Status": {
				"list": self.watching_statuses_language,
				"english_list": self.english_watching_statuses,
				"choice_text": Language_Item_Definer("Select one Watching Status from the status list", "Selecione um Status de Assistindo da lista de status")
			},

			"Origin Type": {
				"list": self.origin_types_language,
				"english_list": self.english_origin_types,
				"choice_text": Language_Item_Definer("Select one origin type from the list", "Selecione um tipo de origem da lista")
			},
		}

		self.media_details_yes_or_no_definer_parameters = {
			"Has Dub": Language_Item_Definer("Has Dub", "Tem Dublagem"),
		}

		self.movie_details_parameters = [
			"Original Name - Nome Original",
			"Portuguese Name - Nome Português",
			"Distributor - Distribuidor",
			"Director - Diretor",
		]

		self.media_type_sub_folders = {}

		for local_mixed_media_type in self.mixed_media_type_names_plural_without_none:
			if local_mixed_media_type != None and local_mixed_media_type != self.movie_media_type_english_plural:
				self.media_type_sub_folders[local_mixed_media_type] = {}

				self.media_type_sub_folders[local_mixed_media_type]["media_list_text"] = self.mixed_seasons_text
				self.media_type_sub_folders[local_mixed_media_type]["english_singular_media_list_text"] = self.english_season_text

				if local_mixed_media_type == self.mixed_media_type_video_plural:
					self.media_type_sub_folders[local_mixed_media_type]["media_list_text"] = self.mixed_series_text
					self.media_type_sub_folders[local_mixed_media_type]["english_singular_media_list_text"] = self.english_series_text

		self.gender_the_texts = {}

		for local_mixed_media_type in self.mixed_media_type_names_plural_without_none:
			if local_mixed_media_type != None:
				self.gender_the_texts[local_mixed_media_type] = {}
				self.gender_the_texts[local_mixed_media_type]["masculine"] = {}
				self.gender_the_texts[local_mixed_media_type]["feminine"] = {}

				self.gender_the_texts[local_mixed_media_type]["the"] = Language_Item_Definer("the", "o")
				self.gender_the_texts[local_mixed_media_type]["this"] = Language_Item_Definer("this", "esse")
				self.gender_the_texts[local_mixed_media_type]["a"] = Language_Item_Definer("one", "um")

				self.gender_the_texts[local_mixed_media_type]["masculine"]["the"] = self.gender_the_texts[local_mixed_media_type]["the"]
				self.gender_the_texts[local_mixed_media_type]["masculine"]["this"] = Language_Item_Definer("this", "esse")

				self.gender_the_texts[local_mixed_media_type]["feminine"]["the"] = Language_Item_Definer("this", "a")
				self.gender_the_texts[local_mixed_media_type]["feminine"]["this"] = Language_Item_Definer("this", "essa")

				if local_mixed_media_type == self.mixed_media_type_series_plural:
					self.gender_the_texts[local_mixed_media_type]["the"] = Language_Item_Definer("the", "a")
					self.gender_the_texts[local_mixed_media_type]["this"] = Language_Item_Definer("this", "essa")
					self.gender_the_texts[local_mixed_media_type]["a"] = Language_Item_Definer("one", "uma")

					self.gender_the_texts[local_mixed_media_type]["feminine"]["the"] = self.gender_the_texts[local_mixed_media_type]["the"]
					self.gender_the_texts[local_mixed_media_type]["feminine"]["this"] = self.gender_the_texts[local_mixed_media_type]["this"]

		self.media_item_details_parameters = {
			"Original Name": {
				"mode": "string",
				"choice_text": Language_Item_Definer("Original Name", self.default_portuguese_template_parameters["Original Name"]),
			},

			"Portuguese Name": {
				"mode": "string",
				"choice_text": Language_Item_Definer("Portuguese Name", self.default_portuguese_template_parameters["Portuguese Name"]),
			},

			"Episode": {
				"mode": "string/default",
				"choice_text": Language_Item_Definer("Episode", self.default_portuguese_template_parameters["Episode"]),
				"default": "None",
			},

			"Origin Location": {
				"mode": "string/default-format",
				"choice_text": Language_Item_Definer("Origin Location", self.default_portuguese_template_parameters["Origin Location"]),
				"default": {
					"format_name": "Original Name",
					"functions": [
						Lower_Text,
						Replace_Space_By_Dash,
						Remove_Dot,
					],
				},
			},
		}

		self.movie_details_template = '''Name - Nome:
{}

Original Name - Nome Original:
{}

Year - Ano:
{}

Director - Diretor:
{}'''

		self.posted_on_social_networks_text_template = "Postei o texto de assistido e uma print do {} no status do WhatsApp, Instagram, Facebook, e tweet no Twitter."

		i = 0

		self.plan_to_watch_english_text = self.english_watching_statuses[i]
		i += 1

		self.watching_english_text = self.english_watching_statuses[i]
		i += 1

		self.completed_english_text = self.english_watching_statuses[i]
		i += 1

		self.rewatching_english_text = self.english_watching_statuses[i]
		i += 1

		self.on_hold_english_text = self.english_watching_statuses[i]
		i += 1

		i = 0

		self.plan_to_watch_portuguese_text = self.portuguese_watching_statuses[i]
		i += 1

		self.watching_portuguese_text = self.portuguese_watching_statuses[i]
		i += 1

		self.completed_portuguese_text = self.portuguese_watching_statuses[i]
		i += 1

		self.rewatching_portuguese_text = self.portuguese_watching_statuses[i]
		i += 1

		self.on_hold_portuguese_text = self.portuguese_watching_statuses[i]
		i += 1

		self.watching_status_english_text = "Watching Status"

		self.mixed_rewatched_format_text = "(Rewatched {}x - Reassistido {}x)"
		self.mixed_rewatched_regex_text = r" \(Rewatched [0-9]x \- Reassistido [0-9]x\)"
		self.one_episode_number_regex = r"[0-9][0-9]"
		self.two_episode_numbers_regex = r"[0-9][0-9]\-[0-9][0-9]"
		self.episode_and_bracket_number = r"[0-9][0-9]\([0-9][0-9]\)"

		# File and folder texts arrays
		self.watched_texts = [
			self.episodes_english_text,
			self.media_types_english_text,
			self.times_english_text,
			self.number_english_text,
		]

		self.movie_texts = [
			self.names_english_text,
			self.times_english_text,
		]

		self.accepted_file_extensions = [
			"mp4",
			"mkv",
		]

		self.social_networks_links = {
			"WhatsApp": "https://web.whatsapp.com/",
		}

	# Defines the Watch History folders
	def Define_Watch_History_Folders(self):
		# Folder variables
		self.local_medias_folder = hard_drive_letter + "Mídias/"

		if "local_medias_folder" in settings:
			self.local_medias_folder = settings["local_medias_folder"]

		self.media_network_folder = networks_folder + "Audiovisual Media Network/"
		self.watch_history_folder = self.media_network_folder + "Watch History/"
		self.watch_history_watched_folder = self.watch_history_folder + self.watched_english_text + "/"

		self.current_year_watched_media_folder = self.watch_history_watched_folder + self.current_year + "/"
		Create_Folder(self.current_year_watched_media_folder, self.global_switches["create_folders"])

		self.total_watched_number_current_year_file = self.current_year_watched_media_folder + self.number_english_text + self.dot_text

		if is_a_file(self.total_watched_number_current_year_file) == False:
			Write_To_File(self.total_watched_number_current_year_file, "0", self.global_switches)

		self.all_watched_files_current_year_folder = self.current_year_watched_media_folder + self.all_watched_files_english_text + "/"
		Create_Folder(self.all_watched_files_current_year_folder, self.global_switches["create_folders"])

		self.per_media_type_current_year_folder = self.current_year_watched_media_folder + self.per_media_type_english_text + "/"
		Create_Folder(self.per_media_type_current_year_folder, self.global_switches["create_folders"])

		self.per_media_type_files_folder = self.per_media_type_current_year_folder + self.files_english_text + "/"
		Create_Folder(self.per_media_type_files_folder, self.global_switches["create_folders"])

		self.per_media_type_folders_folder = self.per_media_type_current_year_folder + self.folders_english_text + "/"
		Create_Folder(self.per_media_type_folders_folder, self.global_switches["create_folders"])

		self.movies_folder = self.watch_history_folder + self.movies_english_text + "/"
		Create_Folder(self.movies_folder, self.global_switches["create_folders"])

		self.media_info_folder = self.media_network_folder + "Media Info/"
		Create_Folder(self.media_info_folder, self.global_switches["create_folders"])

		self.media_list_file = self.media_info_folder + "Media List - Lista de Mídias" + self.dot_text

		self.media_info_media_details_folder = self.media_info_folder + "Media Details/"
		Create_Folder(self.media_info_media_details_folder, self.global_switches["create_folders"])
		self.all_media_number_file = self.media_info_media_details_folder + "All Medias Number" + self.dot_text

		self.type = "/"

		# Media info folders dictionary
		self.media_info_folders = {
			self.anime_media_type: self.media_info_folder + self.mixed_media_type_anime_plural + self.type, 
			self.cartoon_media_type: self.media_info_folder + self.mixed_media_type_cartoon_plural + self.type,
			self.series_media_type: self.media_info_folder + self.mixed_media_type_series_plural + self.type,
			self.movie_media_type: self.media_info_folder + self.mixed_media_type_movie_plural + self.type,
			self.video_media_type: self.media_info_folder + self.mixed_media_type_video_plural + self.type,
		}

		# Media info media details dictionary
		self.media_info_media_details_folders = {
			self.anime_media_type: self.media_info_media_details_folder + self.mixed_media_type_anime_plural + self.type, 
			self.cartoon_media_type: self.media_info_media_details_folder + self.mixed_media_type_cartoon_plural + self.type,
			self.series_media_type: self.media_info_media_details_folder + self.mixed_media_type_series_plural + self.type,
			self.movie_media_type: self.media_info_media_details_folder + self.mixed_media_type_movie_plural + self.type,
			self.video_media_type: self.media_info_media_details_folder + self.mixed_media_type_video_plural + self.type,
		}

		# Media info media details dictionary
		self.media_info_media_details_watching_status_folders = {}

		self.type = "/"
		self.sub_text = self.watching_status_english_text

		For_Append_With_Key(self.mixed_media_type_names_plural, self.media_info_media_details_watching_status_folders, value_string = self.media_info_media_details_folder + "{}/" + self.sub_text + self.type, pop_none = True)

		# Media info name text files dictionary
		self.media_info_name_files = {
			self.anime_media_type: self.media_info_media_details_folders[self.anime_media_type] + self.names_english_text + self.dot_text,
			self.cartoon_media_type: self.media_info_media_details_folders[self.cartoon_media_type] + self.names_english_text + self.dot_text,
			self.series_media_type: self.media_info_media_details_folders[self.series_media_type] + self.names_english_text + self.dot_text,
			self.movie_media_type: self.media_info_media_details_folders[self.movie_media_type] + self.names_english_text + self.dot_text,
			self.video_media_type: self.media_info_media_details_folders[self.video_media_type] + self.names_english_text + self.dot_text,
		}

		# Media info number text files dictionary
		self.media_info_number_files = {
			self.anime_media_type: self.media_info_media_details_folders[self.anime_media_type] + self.number_english_text + self.dot_text,
			self.cartoon_media_type: self.media_info_media_details_folders[self.cartoon_media_type] + self.number_english_text + self.dot_text,
			self.series_media_type: self.media_info_media_details_folders[self.series_media_type] + self.number_english_text + self.dot_text,
			self.movie_media_type: self.media_info_media_details_folders[self.movie_media_type] + self.number_english_text + self.dot_text,
			self.video_media_type: self.media_info_media_details_folders[self.video_media_type] + self.number_english_text + self.dot_text,
		}

		self.type = self.dot_text

		# Media info media watching status dictionary
		self.media_info_media_watching_status_files = {
			self.anime_media_type: {
				self.plan_to_watch_english_text: self.media_info_media_details_watching_status_folders[self.anime_media_type] + self.plan_to_watch_english_text + self.type, 
				self.watching_english_text: self.media_info_media_details_watching_status_folders[self.anime_media_type] + self.watching_english_text + self.type,
				self.completed_english_text: self.media_info_media_details_watching_status_folders[self.anime_media_type] + self.completed_english_text + self.type,
				self.rewatching_english_text: self.media_info_media_details_watching_status_folders[self.anime_media_type] + self.rewatching_english_text + self.type,
				self.on_hold_english_text: self.media_info_media_details_watching_status_folders[self.anime_media_type] + self.on_hold_english_text + self.type,
			},

			self.cartoon_media_type: {
				self.plan_to_watch_english_text: self.media_info_media_details_watching_status_folders[self.mixed_media_type_cartoon_plural] + self.plan_to_watch_english_text + self.type, 
				self.watching_english_text: self.media_info_media_details_watching_status_folders[self.mixed_media_type_cartoon_plural] + self.watching_english_text + self.type,
				self.completed_english_text: self.media_info_media_details_watching_status_folders[self.mixed_media_type_cartoon_plural] + self.completed_english_text + self.type,
				self.rewatching_english_text: self.media_info_media_details_watching_status_folders[self.mixed_media_type_cartoon_plural] + self.rewatching_english_text + self.type,
				self.on_hold_english_text: self.media_info_media_details_watching_status_folders[self.mixed_media_type_cartoon_plural] + self.on_hold_english_text + self.type,
			},

			self.series_media_type: {
				self.plan_to_watch_english_text: self.media_info_media_details_watching_status_folders[self.mixed_media_type_series_plural] + self.plan_to_watch_english_text + self.type, 
				self.watching_english_text: self.media_info_media_details_watching_status_folders[self.mixed_media_type_series_plural] + self.watching_english_text + self.type,
				self.completed_english_text: self.media_info_media_details_watching_status_folders[self.mixed_media_type_series_plural] + self.completed_english_text + self.type,
				self.rewatching_english_text: self.media_info_media_details_watching_status_folders[self.mixed_media_type_series_plural] + self.rewatching_english_text + self.type,
				self.on_hold_english_text: self.media_info_media_details_watching_status_folders[self.mixed_media_type_series_plural] + self.on_hold_english_text + self.type,
			},

			self.movie_media_type: {
				self.plan_to_watch_english_text: self.media_info_media_details_watching_status_folders[self.mixed_media_type_movie_plural] + self.plan_to_watch_english_text + self.type, 
				self.watching_english_text: self.media_info_media_details_watching_status_folders[self.mixed_media_type_movie_plural] + self.watching_english_text + self.type,
				self.completed_english_text: self.media_info_media_details_watching_status_folders[self.mixed_media_type_movie_plural] + self.completed_english_text + self.type,
				self.rewatching_english_text: self.media_info_media_details_watching_status_folders[self.mixed_media_type_movie_plural] + self.rewatching_english_text + self.type,
				self.on_hold_english_text: self.media_info_media_details_watching_status_folders[self.mixed_media_type_movie_plural] + self.on_hold_english_text + self.type,
			},

			self.video_media_type: {
				self.plan_to_watch_english_text: self.media_info_media_details_watching_status_folders[self.mixed_media_type_video_plural] + self.plan_to_watch_english_text + self.type, 
				self.watching_english_text: self.media_info_media_details_watching_status_folders[self.mixed_media_type_video_plural] + self.watching_english_text + self.type,
				self.completed_english_text: self.media_info_media_details_watching_status_folders[self.mixed_media_type_video_plural] + self.completed_english_text + self.type,
				self.rewatching_english_text: self.media_info_media_details_watching_status_folders[self.mixed_media_type_video_plural] + self.rewatching_english_text + self.type,
				self.on_hold_english_text: self.media_info_media_details_watching_status_folders[self.mixed_media_type_video_plural] + self.on_hold_english_text + self.type,
			},
		}

		self.type = "/"

		# Per Media Type folder folders dictionary
		self.per_media_type_folder_folders_dict = {
			self.anime_media_type: self.per_media_type_folders_folder + self.mixed_media_type_anime_plural + self.type, 
			self.cartoon_media_type: self.per_media_type_folders_folder + self.mixed_media_type_cartoon_plural + self.type,
			self.series_media_type: self.per_media_type_folders_folder + self.mixed_media_type_series_plural + self.type,
			self.movie_media_type: self.per_media_type_folders_folder + self.mixed_media_type_movie_plural + self.type,
			self.video_media_type: self.per_media_type_folders_folder + self.mixed_media_type_video_plural + self.type,
		}

		for folder in self.per_media_type_folder_folders_dict.values():
			Create_Folder(folder, self.global_switches["create_folders"])

		# Per Media Type files folder dictionary
		self.per_media_type_files_folders = {
		self.anime_media_type: self.per_media_type_files_folder + self.mixed_media_type_anime_plural + self.type, 
		self.cartoon_media_type: self.per_media_type_files_folder + self.mixed_media_type_cartoon_plural + self.type,
		self.series_media_type: self.per_media_type_files_folder + self.mixed_media_type_series_plural + self.type,
		self.movie_media_type: self.per_media_type_files_folder + self.mixed_media_type_movie_plural + self.type,
		self.video_media_type: self.per_media_type_files_folder + self.mixed_media_type_video_plural + self.type,
		}

		for folder in self.per_media_type_files_folders.values():
			Create_Folder(folder, self.global_switches["create_folders"])

		self.sub_text = self.episodes_english_text
		self.type = self.dot_text

		# Per Media Type episode files
		self.per_media_type_episode_files = {
		self.anime_media_type: self.per_media_type_files_folders[self.anime_media_type] + self.sub_text + self.type, 
		self.cartoon_media_type: self.per_media_type_files_folders[self.cartoon_media_type] + self.sub_text + self.type,
		self.series_media_type: self.per_media_type_files_folders[self.series_media_type] + self.sub_text + self.type,
		self.movie_media_type: self.per_media_type_files_folders[self.movie_media_type] + self.sub_text + self.type,
		self.video_media_type: self.per_media_type_files_folders[self.video_media_type] + self.sub_text + self.type,
		}

		self.sub_text = self.times_english_text

		# Per Media Type time files
		self.per_media_type_time_files = {
		self.anime_media_type: self.per_media_type_files_folders[self.anime_media_type] + self.sub_text + self.type, 
		self.cartoon_media_type: self.per_media_type_files_folders[self.cartoon_media_type] + self.sub_text + self.type,
		self.series_media_type: self.per_media_type_files_folders[self.series_media_type] + self.sub_text + self.type,
		self.movie_media_type: self.per_media_type_files_folders[self.movie_media_type] + self.sub_text + self.type,
		self.video_media_type: self.per_media_type_files_folders[self.video_media_type] + self.sub_text + self.type,
		}

		self.sub_text = self.number_english_text

		# Per Media Type number files
		self.per_media_type_number_files = {
		self.anime_media_type: self.per_media_type_files_folders[self.anime_media_type] + self.sub_text + self.type, 
		self.cartoon_media_type: self.per_media_type_files_folders[self.cartoon_media_type] + self.sub_text + self.type,
		self.series_media_type: self.per_media_type_files_folders[self.series_media_type] + self.sub_text + self.type,
		self.movie_media_type: self.per_media_type_files_folders[self.movie_media_type] + self.sub_text + self.type,
		self.video_media_type: self.per_media_type_files_folders[self.video_media_type] + self.sub_text + self.type,
		}

		for file in self.per_media_type_number_files:
			file = self.per_media_type_number_files[file]

			if is_a_file(file) == False:
				Write_To_File(file, "0", self.global_switches)

		# Watch History folders array
		self.watch_history_folders = []

		self.watch_history_folders.append(self.local_medias_folder)
		self.watch_history_folders.append(self.media_network_folder)
		self.watch_history_folders.append(self.watch_history_folder)
		self.watch_history_folders.append(self.current_year_watched_media_folder)
		self.watch_history_folders.append(self.all_watched_files_current_year_folder)
		self.watch_history_folders.append(self.movies_folder)

		self.watch_history_folders.append(self.media_info_folder)

		For_Append(self.media_info_folders.values(), self.watch_history_folders)
		For_Append(self.media_info_media_details_folders.values(), self.watch_history_folders)
		For_Append(self.media_info_media_details_watching_status_folders.values(), self.watch_history_folders)
		For_Append(self.per_media_type_folder_folders_dict.values(), self.watch_history_folders)
		For_Append(self.per_media_type_files_folders.values(), self.watch_history_folders)

		# Watch History folder names array
		self.watch_history_folder_names = [
		"local_medias_folder",
		"media_network_folder",
		"watch_history_folder",
		"current_year_watched_media_folder",
		"movies_folder",
		"media_info_folder",
		"media_info_folders",
		"media_info_media_details_folders",
		]

	# Creates the Watch History arrays and dictionaries
	def Create_Arrays_And_Dictionaries(self):
		# Watch History folders dictionary creator
		self.watch_history_folders_keys = {}
		For_Append_With_Key(self.watch_history_folder_names, self.watch_history_folders_keys, value = self.watch_history_folders)

		# Watched files array creator
		self.watched_files = {}
		For_Append_With_Key(self.watched_texts, self.watched_files, value_string = self.current_year_watched_media_folder + "{}" + self.dot_text)

		# Watched files array creator
		self.per_media_type_files = {}
		For_Append_With_Key(self.watched_texts, self.watched_files, value_string = self.current_year_watched_media_folder + "{}" + self.dot_text)

		####################################################

		# Movie files dictionary creator
		self.movie_files = {}
		For_Append_With_Key(self.movie_texts, self.movie_files, value_string = self.movies_folder + "{}" + self.dot_text)

		####################################################

		# Media Info Names read lines array creator
		self.media_info_names_read_lines = []
		For_Append(self.media_info_name_files.values(), self.media_info_names_read_lines, Function = Create_Array_Of_File, function_parameter = True)

		# Media Info Names file texts dictionary creator
		self.media_info_names_file_texts = {}
		For_Append_With_Key(self.media_type_names_without_none, self.media_info_names_file_texts, value = self.media_info_names_read_lines)

		# Media Info Numbers read lines array creator
		self.media_info_numbers_read_lines = []
		For_Append(self.media_info_number_files.values(), self.media_info_numbers_read_lines, Function = Create_Array_Of_File, function_parameter = True)

		# Media Info Numbers file texts dictionary creator
		self.media_info_numbers_file_texts = {}
		For_Append_With_Key(self.media_type_names_without_none, self.media_info_numbers_file_texts, value = self.media_info_numbers_read_lines)

		####################################################

		# Watch History files array creator
		self.watch_history_files = []

		For_Append(self.watched_files.values(), self.watch_history_files)
		For_Append(self.movie_files.values(), self.watch_history_files)
		For_Append(self.media_info_name_files.values(), self.watch_history_files)
		For_Append(self.media_info_number_files.values(), self.watch_history_files)
		For_Append(self.per_media_type_episode_files.values(), self.watch_history_files)
		For_Append(self.per_media_type_time_files.values(), self.watch_history_files)
		For_Append(self.per_media_type_number_files.values(), self.watch_history_files)

		for media_type in self.media_type_names:
			i = 0
			if media_type != None:
				watching_status = self.english_watching_statuses[i]
				For_Append(self.media_info_media_watching_status_files[media_type].values(), self.watch_history_files)

				i += 1

	def Define_File_Lists(self):
		# Watch History array texts
		self.watch_history_array_texts = [
		"media_info_folders",
		"media_info_name_files",
		"media_info_names_file_texts",
		"media_info_number_files",
		"media_info_numbers_file_texts",
		"watch_history_folders",
		"watch_history_folders_keys",
		"watch_history_files",
		"watched_texts",
		"watched_files",
		"movie_texts",
		"movie_files",
		]

		# Watch History arrays
		self.watch_history_arrays = [
		self.media_info_folders,
		self.media_info_name_files,
		self.media_info_names_file_texts,
		self.media_info_number_files,
		self.media_info_numbers_file_texts,
		self.watch_history_folders,
		self.watch_history_folders_keys,
		self.watch_history_files,
		self.watched_texts,
		self.watched_files,
		self.movie_texts,
		self.movie_files,
		]

		####################################################

		self.system_verbose = False

		# Watch History arrays lister if verbose == True
		if self.system_verbose == True:
			i = 0
			for array in self.watch_history_arrays:
				text = self.watch_history_array_texts[i]

				print(text + ", {}: ".format(type(array)))

				if type(array) == list:
					if len(array) != 0 and type(array[0]) == list:
						c = 0
						while c <= len(array):
							print(array[c])

							c += 1

					else:
						print(array)

				if type(array) == type(dict):
					print(array)

				if array != self.watch_history_arrays[-1]:
					print()

				i += 1

	# Create files that do not exist
	# Using the watch_history_folders and watch_history_files arrays
	def Create_Unexistent_Folders_And_Files(self):
		for folder in self.watch_history_folders:
			if is_a_folder(folder) == False:
				Create_Folder(folder, self.global_switches["create_folders"])

		for file in self.watch_history_files:
			if is_a_file(file) == False:
				Create_Text_File(file, self.global_switches["create_files"])
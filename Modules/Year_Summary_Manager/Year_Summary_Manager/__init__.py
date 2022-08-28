# Year_Summary_Manager.py

from Script_Helper import *

class Year_Summary_Manager(object):
	def __init__(self, parameter_switches = None, select_year = True):
		# Verbose variable
		self.verbose = False

		self.testing_script = False

		self.parameter_switches = parameter_switches

		self.select_year = select_year

		self.Define_Basic_Variables()
		self.Define_Folders()
		self.Define_Lists()

		if self.select_year == True:
			self.Select_Year()
			self.Define_Year_Variables()

			self.variables_dict = {}
			self.variables_dict["language_year_folders"] = self.language_year_folders
			self.variables_dict["experienced_media_sub_folders"] = self.experienced_media_sub_folders
			self.variables_dict["full_language"] = self.full_language
			self.variables_dict["experienced_media_database_folders"] = self.experienced_media_database_folders

	def Define_Basic_Variables(self):
		self.option = True

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

		self.dot_text = ".txt"

	def Define_Folders(self):
		self.root_years_folder = notepad_folder_years

	def Define_Lists(self):
		self.year_folder_texts = {
			"Experienced Media": {
				full_language_en: "Experienced Media",
				full_language_pt: "Mídias Experimentadas",
			},
		}

		self.firsts_of_the_year_folder_names = {
			full_language_en: "Firsts Of The Year",
			full_language_pt: "Primeiros Do Ano",
		}

		self.firsts_of_the_year_sub_folder_names = {
			full_language_en: [
				"Art",
				"Media",
				"Programming",
				"Normal",
			],

			full_language_pt: [
				"Arte",
				"Mídia",
				"Programação",
				"Normal",
			],
		}

		self.firsts_of_the_year_sub_folder_translated_names = {
			"Arte": "Art",
			"Mídia": "Media",
			"Programação": "Programming",
			"Normal": "Normal",
		}

		self.firsts_of_the_year_sub_sub_folder_names = {
			"Art": {
				full_language_en: [
					"Drawing",
					"Story",
					"Story Chapter",
					"Video",
				],

				full_language_pt: [
					"Desenho",
					"História",
					"Capítulo de História",
					"Vídeo",
				],
			},

			"Media": {
				full_language_en: [
					"Anime",
					"Cartoon",
					"Game",
					"Movie",
					"Music",
					"Series",
					"Video",
				],

				full_language_pt: [
					"Anime",
					"Desenho",
					"Filme",
					"Jogo",
					"Música",
					"Série",
					"Vídeo",
				],
			},

			"Programming": {
				full_language_en: [
					"PHP",
					"Python",
				],

				full_language_pt: [
					"PHP",
					"Python",
				],
			},

			"Normal": {
				full_language_en: [
					"Body",
					"Body/Bath",
					"Mind",
				],

				full_language_pt: [
					"Corpo",
					"Corpo/Banho",
					"Mente",
				],
			},
		}

		self.experienced_media_sub_folder_names = {
			full_language_en: [
				"Anime",
				"Cartoon",
				"Series",
				"Movie",
				"Video",
				"Games",
				"Music",
				"Stories",
			],

			full_language_pt: [
				"Anime",
				"Desenho",
				"Série",
				"Filme",
				"Vídeos",
				"Jogos",
				"Música",
				"Histórias",
			],
		}

		self.experienced_media_database_file_names = {
			"Music": [
				"Name",
				"Artist",
				"Channel",
				"SoundCloud Links",
				"YouTube Links",
				"SoundCloud Playlist Links",
				"YouTube Playlist Links",
			],
		}

		self.experienced_media_database_file_names_language = {
			"Music": {
				full_language_en: [
					"Song name",
					"Artist",
					"Channel",
					"SoundCloud Link",
					"YouTube Link",
					"SoundCloud Playlist Links",
					"YouTube Playlist Links",
				],

				full_language_pt: [
					"Nome da Música",
					"Artista",
					"Canal",
					"Link do SoundCloud",
					"Link do YouTube",
					"Links da Playlist do SoundCloud",
					"Links da Playlist do YouTube",
				]
			},

			"Music Translated": {
				full_language_pt: {
					"Name": "Nome",
					"Artist": "Artista",
					"Channel": "Canal",
					"SoundCloud Links": "Links do SoundCloud",
					"YouTube Links": "Links do YouTube",
					"SoundCloud Playlist Links": "Links da Playlist do SoundCloud",
					"YouTube Playlist Links": "Links da Playlist do YouTube",
				},

				full_language_en: {
					"Nome": "Name",
					"Artista": "Artist",
					"Canal": "Channel",
					"Links do SoundCloud": "SoundCloud Links",
					"Links do YouTube": "YouTube Links",
					"Links da Playlist do SoundCloud": "SoundCloud Playlist Links",
					"Links da Playlist do YouTube": "YouTube Playlist Links",
				},
			},
		}

		self.experienced_media_format_texts = {
			"Music": [
				Language_Item_Definer("Song name", "Nome da Música") + ":\n{}\n\n",
				Language_Item_Definer("Artist", "Artista") + ":\n{}\n\n",
				Language_Item_Definer("Channel", "Canal") + ":\n{}\n\n",
				Language_Item_Definer("SoundCloud Link", "Link do SoundCloud") + ":\n{}\n\n",
				Language_Item_Definer("YouTube Link", "Link do YouTube") + ":\n{}\n\n",
				Language_Item_Definer("SoundCloud Playlist Links", "Links da Playlist do SoundCloud") + ":\n{}?in=stake2/sets/dubstep-[]\n\n".replace("[]", current_year),
				Language_Item_Definer("YouTube Playlist Links", "Links da Playlist do YouTube") + ":\n" + "{}&list=PLh4DEvPQ2wKMoex4j0pFrM6gl77VePMCD&index=" + "",
			],
		}

		self.experienced_media_parameters_not_to_ask = {
			"Music": [
				"SoundCloud Playlist Links",
				"YouTube Playlist Links",
			],
		}

		self.experienced_media_parameter_values = {
			"Music": {
				"SoundCloud Playlist Links": "SoundCloud Links",
				"YouTube Playlist Links": "YouTube Links",
			},
		}

	def Select_Year(self):
		self.year_list = Convert_Array_Item_Type(list(range_one(2018, int(current_year))))

		first_list = self.year_list
		self.choice_text = Language_Item_Definer("Select one Year to manage", "Selecione um Ano para gerenciar")
		self.selected_year = Select_Choice_From_List(first_list, local_script_name, self.choice_text, second_choices_list = first_list, return_second_item_parameter = True, add_none = True, return_number = True)[0]

	def Define_Year_Variables(self):
		self.full_language = Language_Item_Definer(full_language_en, full_language_pt)

		self.root_year_folder = self.root_years_folder + self.selected_year + "/"
		Create_Folder(self.root_year_folder, self.global_switches)

		self.language_year_folder = self.root_year_folder + self.full_language + "/"
		Create_Folder(self.language_year_folder, self.global_switches)

		self.language_year_folders = {}

		self.language_year_folders[full_language_en] = self.root_year_folder + full_language_en + "/"
		self.language_year_folders[full_language_pt] = self.root_year_folder + full_language_pt + "/"

		for folder in self.language_year_folders.values():
			Create_Folder(folder, self.global_switches)

		self.firsts_of_the_year_folders = {}

		self.firsts_of_the_year_folders[full_language_en] = self.language_year_folders[full_language_en] + self.firsts_of_the_year_folder_names[full_language_en] + "/"
		self.firsts_of_the_year_folders[full_language_pt] = self.language_year_folders[full_language_pt] + self.firsts_of_the_year_folder_names[full_language_pt] + "/"

		for folder in self.firsts_of_the_year_folders.values():
			Create_Folder(folder, self.global_switches)

		self.firsts_of_the_year_sub_folders = {}
		self.firsts_of_the_year_sub_folders[full_language_en] = []
		self.firsts_of_the_year_sub_folders[full_language_pt] = []

		for full_language in full_languages_not_none:
			for folder in self.firsts_of_the_year_sub_folder_names[full_language]:
				folder = self.firsts_of_the_year_folders[full_language] + folder + "/"

				self.firsts_of_the_year_sub_folders[full_language].append(folder)
				Create_Folder(folder, self.global_switches)

		self.firsts_of_the_year_sub_sub_folders = {}
		self.firsts_of_the_year_sub_sub_folders[full_language_en] = []
		self.firsts_of_the_year_sub_sub_folders[full_language_pt] = []

		for full_language in full_languages_not_none:
			for folder in self.firsts_of_the_year_sub_folder_names[full_language]:
				original_folder = folder
				parent_folder = folder

				if full_language == full_language_pt:
					parent_folder = self.firsts_of_the_year_sub_folder_translated_names[folder]

				for folder in self.firsts_of_the_year_sub_sub_folder_names[parent_folder][full_language]:
					folder = self.firsts_of_the_year_folders[full_language] + original_folder + "/" + folder + "/"

					self.firsts_of_the_year_sub_sub_folders[full_language].append(folder)
					Create_Folder(folder, self.global_switches)

		self.experienced_media_folders = {}

		for language in self.language_year_folders:
			self.experienced_media_folders[language] = self.language_year_folders[language] + self.year_folder_texts["Experienced Media"][language] + "/"
			Create_Folder(self.experienced_media_folders[language], self.global_switches)

		self.experienced_media_sub_folders = {}

		for language in self.language_year_folders:
			folder_names = self.experienced_media_sub_folder_names[language]
			self.experienced_media_sub_folders[language] = {}

			i = 0
			while i <= len(folder_names) - 1:
				folder_name = folder_names[i]

				folder = self.experienced_media_folders[language] + folder_name + "/"
				Create_Folder(folder, self.global_switches)

				self.experienced_media_sub_folders[language][folder_name] = folder

				i += 1

		self.experienced_media_database_folder = self.experienced_media_folders[full_language_en] + "Database/"
		self.experienced_media_database_folders = {}

		Create_Folder(self.experienced_media_database_folder, self.global_switches)

		language = "English"
		folders = self.experienced_media_sub_folders[language]
		folder_names = self.experienced_media_sub_folder_names[language]
		self.experienced_media_database_folders[language] = {}
		database_folder = self.experienced_media_folders[language] + "Database/"
		Create_Folder(database_folder, self.global_switches)

		i = 0
		while i <= len(folder_names) - 1:
			folder_name = folder_names[i]

			folder = database_folder + folder_name + "/"
			Create_Folder(folder, self.global_switches)

			self.experienced_media_database_folders[language][folder_name] = folder

			i += 1

		self.christmas_folders = {}

		self.christmas_folders[full_language_en] = self.language_year_folders[full_language_en] + "Christmas/"
		self.christmas_folders[full_language_pt] = self.language_year_folders[full_language_pt] + "Natal/"

		for full_language in self.christmas_folders:
			folder = self.christmas_folders[full_language]
			Create_Folder(folder, self.global_switches)

			self.planning_text_file = folder + Language_Item_Definer("Planning", "Planejamento", full_language) + self.dot_text
			Create_Text_File(self.planning_text_file, self.global_switches)

			self.eat_file = folder + Language_Item_Definer("Eat", "Comer", full_language) + self.dot_text
			Create_Text_File(self.eat_file, self.global_switches)

			self.watch_folder = folder + Language_Item_Definer("Watch", "Assistir", full_language)
			Create_Folder(self.watch_folder, self.global_switches)

			if full_language == full_language_en:
				self.objects_file = folder + "Objects" + self.dot_text
				Create_Text_File(self.objects_file, self.global_switches)

		self.christmas_posts_folder = self.root_year_folder + "Christmas Posts - Posts de Natal/"
		Create_Folder(self.christmas_posts_folder, self.global_switches)

		self.christmas_planning_of_posts_file = self.christmas_posts_folder + "Planning of Posts - Planejamento de Posts" + self.dot_text
		Create_Text_File(self.christmas_planning_of_posts_file, self.global_switches)

		self.christmas_tweets_file = self.christmas_posts_folder + "Tweets" + self.dot_text
		Create_Text_File(self.christmas_tweets_file, self.global_switches)

		self.happy_new_year_folder = self.root_year_folder + "Happy New Year - Feliz Ano Novo/"
		Create_Folder(self.happy_new_year_folder, self.global_switches)

		self.new_year_planning_of_posts_file = self.happy_new_year_folder + "Planning of Posts - Planejamento de Posts" + self.dot_text
		Create_Text_File(self.new_year_planning_of_posts_file, self.global_switches)

		self.new_year_tweets_file = self.happy_new_year_folder + "Tweets" + self.dot_text
		Create_Text_File(self.new_year_tweets_file, self.global_switches)

		self.summary_files = {}

		self.summary_files[full_language_en] = self.language_year_folders[full_language_en] + "Summary" + self.dot_text
		self.summary_files[full_language_pt] = self.language_year_folders[full_language_pt] + "Sumário" + self.dot_text

		for file in self.summary_files.values():
			Create_Text_File(file, self.global_switches)

		self.this_year_i_files = {}

		self.this_year_i_files[full_language_en] = self.language_year_folders[full_language_en] + "This Year I" + self.dot_text
		self.this_year_i_files[full_language_pt] = self.language_year_folders[full_language_pt] + "Esse Ano Eu" + self.dot_text

		for file in self.this_year_i_files.values():
			Create_Text_File(file, self.global_switches)
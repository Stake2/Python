# GamePlayer.py

from Script_Helper import *

local_script_name = "GamePlayer.py"

class GamePlayer(object):
	def __init__(self, parameter_switches = None):
		# Verbose variable
		self.verbose = False

		self.testing_script = False

		self.parameter_switches = parameter_switches

		self.Define_Basic_Variables()
		self.Define_Texts()
		self.Define_Folders()
		self.Define_Files()

	def Define_Basic_Variables(self):
		self.option = True

		self.global_switches = {
		"write_to_file": self.option,
		"create_files": self.option,
		"create_folders": self.option,
		"move_files": self.option,
		"open_game": self.option,
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
			self.global_switches["open_game"] = False

		self.dot_text = ".txt"
		self.media_type_separator = " - "
		self.media_info_setting_separator = ": "

	def Define_Texts(self):
		self.dot_text = ".txt"
		self.dot_bat = ".bat"
		self.dot_exe = ".exe"
		self.dot_lnk = ".lnk"
		self.dot_url = ".url"
		self.dot_swf = ".swf"
		self.dot_z64 = "z64"
		self.dot_n64 = "n64"
		self.dot_zip = "zip"

		self.extensions_list = ["bat", "exe", "lnk", "url", "swf", "z64", "n64", "zip"]

		self.extensions_dict = {
			"bat": ".bat",
			"exe": ".exe",
			"EXE": ".EXE",
			"lnk": ".lnk",
			"url": ".url",
			"swf": ".swf",
			"z64": ".z64",
			"n64": ".n64",
			"zip": ".zip",
			"txt": ".txt",
		}

		self.global_texts = {
			"times_mixed": "Times - Tempos",
			"when_mixed": "When - Quando",

			full_language_en: {
				"game": "game",
				"games": "games",
				"game_genre": "Game genre",
				"count_playing_time": "Count playing time",
				"select_game_from_list": "Select a game from the list to play",
				"opening_this_game": "Opening this game {}",
				"in_this_game_folder": "In this game folder",
				"file_opened": "File opened",
				"and": "and",
			},

			full_language_pt: {
				"game": "jogo",
				"games": "jogos",
				"game_genre": "Gênero de jogo",
				"count_playing_time": "Contar tempo de jogatina",
				"select_game_from_list": "Selecione um jogo da lista para jogar",
				"opening_this_game": "Abrindo esse jogo {}",
				"in_this_game_folder": "Nesta pasta de jogo",
				"file_opened": "Arquivo aberto",
				"and": "e",
			}
		}

		self.global_texts[full_language_en]["opening_this_game"] = self.global_texts[full_language_en]["opening_this_game"].format("to play")
		self.global_texts[full_language_en]["opening_this_game_file"] = self.global_texts[full_language_en]["opening_this_game"].format("file")

		self.global_texts[full_language_pt]["opening_this_game"] = self.global_texts[full_language_pt]["opening_this_game"].format("para jogar")
		self.global_texts[full_language_pt]["opening_this_game_file"] = self.global_texts[full_language_pt]["opening_this_game"].replace(" jogo para jogar", " arquivo de jogo")

		self.game_folder_texts = {
			full_language_en: {
				"folder_setting_empty": "The game folder setting is empty",
				"type_game_folder": "Type your game shortcut folder",
				"type_folder": "Type the folder",
				"find_folder": "Find it",
				"select_a_folder": "Select a folder from the list to add",
				"select_folder_to_list": "Select a folder to list the games inside it",
				"choose_folder": "Choose this folder",
				"list_folder": "List files inside this folder",
				"select_option_from_list": "Select an option from the list",
				"type_folder_path": "Type the entire folder path without disk letter",
				"folder_does_not_exist": "This folder does not exist, please type another one",
				"add_game_shortcut_folder": "Add a folder with game shortcuts",
			},

			full_language_pt: {
				"folder_setting_empty": "A configuração de pasta de jogo está vazia",
				"type_game_folder": "Digite a sua pasta de atalhos de jogos",
				"type_folder": "Digite a pasta",
				"find_folder": "Encontre-a",
				"select_a_folder": "Selecione uma pasta da lista para adicionar",
				"select_folder_to_list": "Selecione uma pasta para listar os jogos dentro dela",
				"choose_folder": "Escolher essa pasta",
				"list_folder": "Listar arquivos dentro desta pasta",
				"select_option_from_list": "Selecione uma opção da lista",
				"type_folder_path": "Digite o caminho inteiro da pasta sem a letra do disco",
				"folder_does_not_exist": "Esta pasta não existe, por favor digite outra",
				"add_game_shortcut_folder": "Adicione uma pasta com atalhos de jogos",
			}
		}

		self.playing_texts = {
			full_language_en: {
				"playing_the_game_for": 'I am playing the "{}" game called "{}" for {}, current time: {}',
				"played_the_game_for": 'I played the game the "{}" game called "{}" for {}, current time: {}',
			},

			full_language_pt: {
				"playing_the_game_for": 'Estou jogando o jogo de "{}" chamado "{}" por {}, horário atual: {}',
				"played_the_game_for": 'Joguei o jogo de "{}" chamado "{}" por {}, horário atual: {}',
			}
		}

		self.time_texts = {
			full_language_en: {
				"hour": "hour",
				"hours": "hours",
				"minute": "minute",
				"minutes": "minutes",
			},

			full_language_pt: {
				"hour": "hora",
				"hours": "horas",
				"minute": "minuto",
				"minutes": "minutos",
			}
		}

		self.remove_folder_names = [
		"C:/Jogos/",
		"D:/Jogos/",
		"Shortcuts - Atalhos/",
		]

		self.global_texts_language = self.global_texts[Language_Item_Definer(full_language_en, full_language_pt)]
		self.game_folder_texts_language = self.game_folder_texts[Language_Item_Definer(full_language_en, full_language_pt)]
		self.playing_texts_language = self.playing_texts[Language_Item_Definer(full_language_en, full_language_pt)]
		self.time_texts_language = self.time_texts[Language_Item_Definer(full_language_en, full_language_pt)]

		self.singular_games_text = self.global_texts_language["game"]
		self.plural_games_text = self.global_texts_language["games"]

		self.whatsapp_link = "https://web.whatsapp.com/"

	def Define_Folders(self):
		self.scripts_folder = scripts_folder
		self.scripts_shortcuts_folder = self.scripts_folder + "Atalhos/"
		self.game_script_shortcuts_folder = self.scripts_shortcuts_folder + "Games/"

		if "." in __name__:
			name = __name__.split(".")[0]

		self.module_text_files_folder = script_text_files_folder + name + "/"
		Create_Folder(self.module_text_files_folder, self.global_switches["create_folders"])

		self.game_folder_file = self.module_text_files_folder + "Folders.txt"
		Create_Text_File(self.game_folder_file, self.global_switches["create_files"])
		self.game_folder_text = Create_Array_Of_File(self.game_folder_file)

		self.game_network_folder = networks_folder + "Game Network/"
		self.media_network_data_folder = self.game_network_folder + "Media Network Data/"
		self.game_types_file = self.media_network_data_folder + "Game Types" + self.dot_text
		self.play_history_folder = self.game_network_folder + "Play History/"
		self.played_folder = self.play_history_folder + "Played/"
		self.current_year_played_folder = self.played_folder + str(current_year) + "/"
		self.played_texts_folder = self.current_year_played_folder + "Played Texts - Textos de Jogatina/"

		Create_Folder(self.game_network_folder, self.global_switches["create_folders"])
		Create_Folder(self.play_history_folder, self.global_switches["create_folders"])
		Create_Folder(self.played_folder, self.global_switches["create_folders"])
		Create_Folder(self.current_year_played_folder, self.global_switches["create_folders"])
		Create_Folder(self.played_texts_folder, self.global_switches["create_folders"])

		self.all_played_files_folder = self.current_year_played_folder + "All Played Files/"
		self.game_files_folder = self.current_year_played_folder + "Game Files/"
		self.per_media_type_folder = self.current_year_played_folder + "Per Media Type/"
		self.per_media_type_files_folder = self.per_media_type_folder + "Files/"
		self.per_media_type_folders_folder = self.per_media_type_folder + "Folders/"

		Create_Folder(self.all_played_files_folder, self.global_switches["create_folders"])
		Create_Folder(self.game_files_folder, self.global_switches["create_folders"])
		Create_Folder(self.per_media_type_folder, self.global_switches["create_folders"])
		Create_Folder(self.per_media_type_files_folder, self.global_switches["create_folders"])
		Create_Folder(self.per_media_type_folders_folder, self.global_switches["create_folders"])

		for game_type in Create_Array_Of_File(self.game_types_file):
			self.media_type_files_folder = self.per_media_type_files_folder + game_type + "/"
			self.media_type_folders_folder = self.per_media_type_folders_folder + game_type + "/"

			Create_Folder(self.media_type_files_folder, self.global_switches["create_folders"])
			Create_Folder(self.media_type_folders_folder, self.global_switches["create_folders"])

			if is_a_file(self.media_type_files_folder + "Number" + self.dot_text) == False:
				Write_To_File(self.media_type_files_folder + "Number" + self.dot_text, "0")

			Create_Text_File(self.media_type_files_folder + "Games" + self.dot_text, self.global_switches["create_files"])
			Create_Text_File(self.media_type_files_folder + "Times" + self.dot_text, self.global_switches["create_files"])
			Create_Text_File(self.media_type_files_folder + "Time Spent" + self.dot_text, self.global_switches["create_files"])

			Create_Folder(self.media_type_folders_folder + "All Files/", self.global_switches["create_folders"])

		self.has_multiple_game_folders = False

		if len(self.game_folder_text) > 1:
			self.has_multiple_game_folders = True

		if len(self.game_folder_text) != 0:
			if self.has_multiple_game_folders == False:
				self.game_folder = hard_drive_letter + game_folder_text[0].replace("\\", "/")
				Create_Folder(self.game_folder, self.global_switches["create_folders"])

			if self.has_multiple_game_folders == True:
				self.game_folders = []

				for folder in self.game_folder_text:
					folder = hard_drive_letter + folder.replace("\\", "")

					Create_Folder(folder, self.global_switches["create_folders"])

					if len(List_Files(folder, add_none = False)) != 0:
						self.game_folders.append(folder)

			self.is_new_game_folder = False

		else:
			#Folder_Chooser_Module()

			print(self.game_folder_texts_language["folder_setting_empty"])
			print()

			self.game_folder_name = Select_Choice(self.game_folder_texts_language["type_game_folder"] + ": " + hard_drive_letter, custom_text = True, first_space = False)
			self.game_folder = hard_drive_letter + self.game_folder_name + "/"
			Create_Folder(self.game_folder, self.global_switches["create_folders"])

			self.is_new_game_folder = True

		if self.is_new_game_folder == True:
			text_to_write = self.game_folder_name
			Write_To_File(self.game_folder_file, text_to_write, self.global_switches)

		if self.has_multiple_game_folders == False:
			self.game_names = List_Filenames(game_folder, add_none = False)
			self.game_files = List_Files(game_folder, add_none = False)

		if self.has_multiple_game_folders == True:
			self.games_numbers = []
			self.all_games_number = 0

			for folder in self.game_folders:
				self.games_number = len(List_Files(folder)) - 1
				self.games_numbers.append(self.games_number)

				self.all_games_number += self.games_number

			self.game_names_dict = {}
			self.game_files_names_dict = {}

			self.game_folder_names = []

			i = 0
			for folder in self.game_folders:
				folder_backup = folder

				folder = self.Sanitize_Game_Folder_Name(folder_backup, folder)

				if len(List_Files(folder_backup, add_none = False)) != 0:
					self.game_folder_names.append(folder)

				i += 1

	def Define_Files(self):
		self.game_played_time_files = {
			"Games": self.current_year_played_folder + "Games" + self.extensions_dict["txt"],
			"Number": self.current_year_played_folder + "Number" + self.extensions_dict["txt"],
			"Game Types": self.current_year_played_folder + "Game Types" + self.extensions_dict["txt"],
			"Times": self.current_year_played_folder + "Times" + self.extensions_dict["txt"],
			"Time Spent": self.current_year_played_folder + "Time Spent" + self.extensions_dict["txt"],
			"Played Time " + full_language_en: self.played_texts_folder + full_language_en + self.extensions_dict["txt"],
			"Played Time " + full_language_pt: self.played_texts_folder + full_language_pt + self.extensions_dict["txt"],
		}

		for file in self.game_played_time_files:
			file_name = file
			file = self.game_played_time_files[file]

			if file_name != "Number":
				Create_Text_File(file, self.global_switches["create_files"])

			if file_name == "Number":
				if is_a_file(file) == False:
					Write_To_File(file, "0", self.global_switches)

		self.extensions_dict.pop("txt")

	def Sanitize_Game_Folder(self, folder):
		if "Shortcuts - Atalhos/" in folder:
			folder = folder.replace("Shortcuts - Atalhos/", "")

		return folder

	def Sanitize_Game_Folder_Name(self, games_folder, game_folder_name):
		games_number_length = len(List_Files(games_folder)) - 1

		games_text = Define_Text_By_Number(games_number_length, self.singular_games_text, self.plural_games_text)

		for folder in self.remove_folder_names:
			if folder in game_folder_name:
				game_folder_name = game_folder_name.replace(folder, "")

		game_folder_name = game_folder_name.replace(hard_drive_letter, "")

		game_folder_name += " ({} ".format(games_number_length) + games_text + ")"

		if "/" in game_folder_name:
			game_folder_name = game_folder_name.replace("/", "")

		return game_folder_name

class Add_New_Game_Folder(GamePlayer):
	def __init__(self):
		super().__init__()

		self.game_folders = []
		self.game_folder_names = []

		self.choices = [
		self.game_folder_texts_language["type_folder"],
		self.game_folder_texts_language["find_folder"],
		]

		self.choices_dict = {
		"type_folder": self.choices[0],
		"find_folder": self.choices[1],
		}

		self.choice_text = self.game_folder_texts_language["select_option_from_list"]
		self.selected_choice = Select_Choice_From_List(self.choices, local_script_name, self.choice_text, second_choices_list = self.choices, add_none = True, return_second_item_parameter = True, return_first_and_second_item = True, return_number = True, second_space = False)[0]

		if self.selected_choice == self.choices_dict["type_folder"]:
			self.folder_path = Select_Choice(self.game_folder_texts_language["type_folder_path"], second_space = False)

			self.folder = hard_drive_letter + self.folder_path.replace("\\", "/") + "/"

			self.game_folder_exists = False

			if is_a_folder(self.folder) == True:
				self.game_folder_name = self.Sanitize_Game_Folder_Name(self.folder, self.folder)

				self.game_folder_exists = True

			else:
				while is_a_folder(self.folder) == False:
					print()
					print(self.game_folder_texts_language["folder_does_not_exist"] + ".")

					self.folder_path = Select_Choice(self.game_folder_texts_language["type_folder_path"], first_space = False, second_space = False)

					self.folder = hard_drive_letter + self.folder_path.replace("\\", "/") + "/"

				if is_a_folder(self.folder) == True:
					self.game_folder_name = self.Sanitize_Game_Folder_Name(self.folder, self.folder)

					self.game_folder_exists = True

		if self.selected_choice == self.choices_dict["find_folder"]:
			self.disk_root_folders = List_Folder(hard_drive_letter, add_folder_path = True)

			self.choice_text = self.game_folder_texts_language["select_a_folder"]
			self.folder = Select_Choice_From_List(self.disk_root_folders, local_script_name, self.choice_text, second_choices_list = self.disk_root_folders, add_none = True, return_second_item_parameter = True, return_first_and_second_item = True, return_number = True, second_space = False)[0]

			self.find_folder_choices = [
			self.game_folder_texts_language["choose_folder"],
			self.game_folder_texts_language["list_folder"],
			]

			self.find_folder_choices_dict = {
			"choose_folder": self.find_folder_choices[0],
			"list_folder": self.find_folder_choices[1],
			}

			self.choice_text = self.game_folder_texts_language["select_option_from_list"]
			self.find_folder_option = Select_Choice_From_List(self.find_folder_choices, local_script_name, self.choice_text, second_choices_list = self.find_folder_choices, add_none = True, return_second_item_parameter = True, return_first_and_second_item = True, return_number = True, second_space = False)[0]

			if self.find_folder_option == self.find_folder_choices_dict["choose_folder"]:
				self.game_folder_name = self.Sanitize_Game_Folder_Name(self.folder, self.folder)

				self.game_folder_exists = True

			if self.find_folder_option == self.find_folder_choices_dict["list_folder"]:
				while self.find_folder_option == self.find_folder_choices_dict["list_folder"]:
					self.folders_list = List_Folder(self.folder, add_folder_path = True)

					self.choice_text = self.game_folder_texts_language["select_a_folder"]
					self.folder = Select_Choice_From_List(self.folders_list, local_script_name, self.choice_text, second_choices_list = self.folders_list, add_none = True, return_second_item_parameter = True, return_first_and_second_item = True, return_number = True, second_space = False)[0]

					choice_text = self.game_folder_texts_language["select_option_from_list"]
					self.find_folder_option = Select_Choice_From_List(self.choices, local_script_name, self.choice_text, second_choices_list = self.choices, add_none = True, return_second_item_parameter = True, return_first_and_second_item = True, return_number = True, second_space = False)[0]

				if self.find_folder_option == self.find_folder_choices_dict["choose_folder"]:
					self.game_folder_name = self.Sanitize_Game_Folder_Name(self.folder, self.folder)
					self.folder = Sanitize_Game_Folder_Path(self.folder)

					self.game_folder_exists = True

		if self.game_folder_exists == True:
			self.game_folders.append(self.folder)
			self.game_folder_names.append(self.game_folder_name)

			self.game_folders_text = Create_Array_Of_File(self.game_folder_file)
			self.game_folders_text.append(self.folder.replace(hard_drive_letter, ""))

			self.new_game_folders_text = []

			for text in self.game_folders_text:
				if "\\" in text:
					text = text.replace("\\", "/")

				self.new_game_folders_text.append(text)

			text_to_write = Stringfy_Array(self.new_game_folders_text, add_line_break = True)
			Write_To_File(self.game_folder_file, text_to_write, self.global_switches)

	def Sanitize_Game_Folder_Name(self, games_folder, game_folder_name):
		games_number_length = len(List_Files(games_folder)) - 1

		games_text = Define_Text_By_Number(games_number_length, self.singular_games_text, self.plural_games_text)

		game_folder_name = game_folder_name.replace(hard_drive_letter, "")

		game_folder_name += " ({} ".format(games_number_length) + games_text + ")"

		for folder in self.remove_folder_names:
			if folder in game_folder_name:
				game_folder_name = game_folder_name.replace(folder, "")

		if "/" in game_folder_name:
			game_folder_name = game_folder_name.replace("/", "")

		return game_folder_name

def Sanitize_Game_Folder_Path(folder):
	folder_path = folder.replace(hard_drive_letter, "")

	if "/" in str(folder_path)[-1]:
		folder_path = folder_path[:-1]

	return folder_path
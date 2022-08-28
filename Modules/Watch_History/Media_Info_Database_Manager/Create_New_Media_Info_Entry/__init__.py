# Create_New_Media_Info_Entry.py

# Script Helper importer
from Script_Helper import *

from Watch_History.Watch_History import Watch_History as Watch_History

from Watch_History.Select_Media_Type_And_Media import Select_Media_Type_And_Media as Select_Media_Type_And_Media
from Watch_History.Media_Manager import *

class Create_New_Media_Info_Entry(Watch_History):
	def __init__(self, run_as_module = False):
		super().__init__()

		self.run_as_module = run_as_module

		if self.run_as_module == False:
			self.Select_Media_Type()
			self.Type_Media_Info()

			if self.has_media_list == True:
				self.Type_Media_List()

			self.Define_Media_Variables()
			self.Write_To_Files()
			self.Show_Info_Summary()

	def Select_Media_Type(self):
		self.lists_dict = {}

		self.lists_dict["select_media"] = False
		self.lists_dict["media_type_choice_text"] = Language_Item_Definer("Select the media type of the new entry", "Selecione o tipo de mídia da nova entrada")

		self.choice_info = Select_Media_Type_And_Media(self.lists_dict, status_text = self.status_text)

		self.media_names_file = self.media_info_name_files[self.english_media_type]
		self.media_number_file = self.media_info_number_files[self.english_media_type]

		# Media Type variables definition
		self.english_media_type = self.choice_info.english_media_type
		self.portuguese_media_type = self.choice_info.portuguese_media_type
		self.language_singular_media_type = self.choice_info.language_singular_media_type
		self.mixed_media_type = self.choice_info.mixed_media_type

		self.is_series_media = True
		self.is_video_series_media = False

		# Series media, video series media, and re-watching variables definition
		if self.english_media_type == self.movie_media_type_english_plural:
			self.is_series_media = False

		if self.english_media_type == self.video_media_type_english_plural:
			self.is_video_series_media = True

		self.media_info_media_type_folder = self.choice_info.media_info_media_type_folder

		self.all_media_names = Create_Array_Of_File(self.media_info_name_files[self.english_media_type])

		self.media_list = self.all_media_names

		self.media_type_media_names = Create_Array_Of_File(self.media_names_file)

	def Type_Media_Info(self):
		self.is_new_media = True

		self.add_media_items = False

		if self.is_series_media == True:
			self.add_media_items = Yes_Or_No_Definer(Language_Item_Definer("Add media items to media", "Adicionar itens de mídia á mídia"), first_space = False)

		if self.add_media_items == False:
			self.Type_Media_Details()

			if self.is_series_media == False:
				self.Type_Movie_Details()

		self.media_list_text = self.media_type_sub_folders[self.mixed_media_type]["media_list_text"]
		self.singular_media_list_text = self.media_type_sub_folders[self.mixed_media_type]["english_singular_media_list_text"]
		self.current_media_item_text = "Current " + self.singular_media_list_text

		if self.add_media_items == True:
			self.choice_info = Select_Media(self.selected_mixed_media_type, self.selected_media_type_singular_per_language, self.media_list, self.media_info_media_type_folder, True, add_none = True, first_space = False)

			self.media_details = self.choice_info.media_details

			self.media_folder = self.choice_info.media_folder
			Create_Folder(self.media_folder, self.global_switches)

			if self.is_series_media == True:
				self.media_list_folder = self.media_folder + self.media_list_text + "/"
				Create_Folder(self.media_list_folder, self.global_switches) 

				self.media_list_file = self.media_list_folder + self.media_list_text + self.dot_text
				Create_Text_File(self.media_list_file, self.global_switches)

		self.watching_status = self.media_details["Status"]
		self.origin_type = self.media_details["Origin Type"]

		self.watching_status_file = self.media_info_media_watching_status_files[self.english_media_type][self.watching_status]

		if self.media_details["Original Name"] in self.media_type_media_names:
			self.is_new_media = False

		if self.is_series_media == True:
			if self.media_details["Origin Type"] in ["Remote", "Hybrid"]:
				self.media_item_details_parameters["Remote Origin"] = {
					"mode": "choice_dict",
					"choice_text": Language_Item_Definer("Remote Origin", self.default_portuguese_template_parameters["Remote Origin"]),
					"list": list(self.remote_origin_links.keys()),
					"dict": self.remote_origin_link_names,
				}

			self.choice_text = Language_Item_Definer("Has Media List (like seasons or video series)", "Tem Lista de Mídias (como temporadas ou série de vídeos)")

			if self.add_media_items == False:
				self.has_media_list = Yes_Or_No_Definer(self.choice_text, second_space = False)

			if self.add_media_items == True:
				self.has_media_list = True

	def Type_Media_Details(self):
		self.media_details = {}

		print("-----")
		print()
		print(Language_Item_Definer("Please type the media details", "Por favor digite os detalhes da mídia") + ": ")

		for self.parameter_name in self.media_details_parameters:
			if self.parameter_name in self.media_details_string_parameters:
				self.parameter_data = self.media_details_string_parameters[self.parameter_name]
				self.choice_text = self.parameter_data["choice_text"]
				self.default_parameter = self.parameter_data["default"]

				if type(self.default_parameter) == dict:
					self.default_parameter = self.media_details[self.parameter_data["default"]["format_name"]]

				self.input_parameter = Select_Choice(self.choice_text, accept_enter = True, enter_equals_empty = True, first_space = False, second_space = False)

				if self.input_parameter == "":
					self.input_parameter = self.default_parameter

			if self.parameter_name in self.media_details_choice_list_parameters:
				self.parameter_data = self.media_details_choice_list_parameters[self.parameter_name]
				self.choice_text = self.parameter_data["choice_text"]
				self.list_ = self.parameter_data["list"]
				self.english_list = self.parameter_data["english_list"]

				self.first_space = True
				self.second_space = False

				if self.parameter_name == list(self.media_details_choice_list_parameters.keys())[0]:
					self.first_space = False

				self.input_parameter = Select_Choice_From_List(self.list_, alternative_choice_text = self.choice_text, second_choices_list = self.english_list, return_second_item_parameter = True, return_number = True, add_none = True, first_space = self.first_space, second_space = self.second_space)[0]

			if self.parameter_name in self.media_details_yes_or_no_definer_parameters:
				self.input_parameter = Yes_Or_No_Definer(self.media_details_yes_or_no_definer_parameters[self.parameter_name], convert_to_yes_or_no = True, first_space = True)

			self.media_details[self.parameter_name] = self.input_parameter

		print()
		print(Language_Item_Definer("Finished typing media details", "Terminou de digitar os detalhes da mídia") + ".")
		print()
		print("-----")

	def Type_Movie_Details(self):
		self.movie_details = {}

		if "Year" in self.media_details:
			self.movie_details["Year"] = self.media_details["Year"]

		print("-----")
		print()
		print(Language_Item_Definer("Please type the movie details", "Por favor digite os detalhes do filme") + ": ")

		for self.parameter_name in self.movie_details_parameters:
			self.choice_text = self.parameter_name.split(" - ")[Language_Item_Definer(0, 1)]

			self.movie_details[self.parameter_name] = Select_Choice(self.choice_text, accept_enter = False, first_space = False, second_space = False)

		print()
		print(Language_Item_Definer("Finished typing movie details", "Terminou de digitar os detalhes do filme") + ".")
		print()
		print("-----")

	def Type_Media_List(self):
		self.media_list = {}
		self.media_list_names = []
		self.old_media_list_names = []

		if self.is_new_media == False:
			self.old_media_list_names.extend(self.media_list_names)

			self.media_list_names.extend(Create_Array_Of_File(self.media_list_file))

			for media_item in Create_Array_Of_File(self.media_list_file):
				media_item_folder = self.media_list_folder + Remove_Non_File_Characters(media_item) + "/"
				media_item_details_file = media_item_folder + "Media Details" + self.dot_text

				self.media_list[media_item] = Make_Setting_Dictionary(media_item_details_file, read_file = True)

		self.add_more_media = True

		while self.add_more_media == True:
			self.media_item_details = {}

			print()
			print("-----")
			print()
			print(Language_Item_Definer("Please type the media item details", "Por favor digite os detalhes do item de mídia") + ": ")

			for self.parameter_name in self.media_item_details_parameters:
				self.parameter_data = self.media_item_details_parameters[self.parameter_name]
				self.choice_text = self.parameter_data["choice_text"]

				if self.parameter_data["mode"] == "string":
					self.input_parameter = Select_Choice(self.choice_text, accept_enter = False, first_space = False, second_space = False)

				if self.parameter_data["mode"] == "string/default":
					self.default_parameter = self.parameter_data["default"]

					self.input_parameter = Select_Choice(self.choice_text, accept_enter = True, enter_equals_empty = True, first_space = False, second_space = False)

					if self.input_parameter == "":
						self.input_parameter = self.default_parameter

				if self.parameter_data["mode"] == "string/default-format":
					if self.is_video_series_media == False:
						self.default_parameter = self.media_details[self.parameter_data["default"]["format_name"]] + "-" + self.media_item_details[self.parameter_data["default"]["format_name"]]

						for function in self.parameter_data["default"]["functions"]:
							self.default_parameter = function(self.default_parameter)

						self.input_parameter = Select_Choice(self.choice_text, enter_equals_empty = True, first_space = False, second_space = False)

						if self.input_parameter == "":
							self.input_parameter = self.default_parameter

					if self.is_video_series_media == True:
						self.choice_text = Language_Item_Definer("Type the video series playlist link", "Digite o link da playlist da série de vídeos")
						self.input_parameter = Select_Choice(self.choice_text, enter_equals_empty = True, first_space = False, second_space = False)

						self.input_parameter = self.input_parameter.split("playlist?list=")[1]

				if self.parameter_data["mode"] == "choice_dict":
					self.parameter_data = self.media_item_details_parameters[self.parameter_name]
					self.choice_text = self.parameter_data["choice_text"]
					self.list_ = self.parameter_data["list"]
					self.dict_ = self.parameter_data["dict"]

					self.input_parameter = Select_Choice_From_List(self.list_, alternative_choice_text = self.choice_text, return_first_item = True, add_none = True, first_space = True, second_space = False)
					self.input_parameter = self.dict_[self.input_parameter]

				self.media_item_details[self.parameter_name] = self.input_parameter

			self.media_list[self.media_item_details["Original Name"]] = self.media_item_details
			self.media_list_names.append(self.media_item_details["Original Name"])
			self.old_media_list_names.append(self.media_item_details["Original Name"])

			print()
			print(Language_Item_Definer("Finished typing media item details", "Terminou de digitar os detalhes do item de mídia") + ".")
			print()
			print("-----")

			self.choice_text = Language_Item_Definer("Add more media", "Adicionar mais mídias")
			self.add_more_media = Yes_Or_No_Definer(self.choice_text, second_space = False)

	def Define_Media_Variables(self):
		self.media_folder = self.media_info_media_type_folder + Remove_Non_File_Characters(self.media_details["Original Name"]) + "/"
		Create_Folder(self.media_folder, self.global_switches)

		self.media_details_file = self.media_folder + self.media_details_english_text + self.dot_text
		Create_Text_File(self.media_details_file, self.global_switches)

		if self.is_series_media == False:
			self.movie_details_file = self.media_folder + self.movie_details_english_text + self.dot_text
			Create_Text_File(self.movie_details_file, self.global_switches)	

		if self.is_new_media == False:
			self.media_details = Make_Setting_Dictionary(self.media_details_file, read_file = True)

		if self.is_series_media == True:
			self.media_list_folder = self.media_folder + self.media_list_text + "/"
			Create_Folder(self.media_list_folder, self.global_switches)

			self.media_list_file = self.media_list_folder + self.media_list_text + self.dot_text
			Create_Text_File(self.media_list_file, self.global_switches)

			self.current_media_item_file = self.media_list_folder + self.current_media_item_text + self.dot_text
			Create_Text_File(self.current_media_item_file, self.global_switches)

			if self.has_media_list == True:
				media_list_names = []
				media_list_names.extend(self.media_list_names)

				self.media_list_names = media_list_names

				for media_item in self.media_list_names:
					self.current_media_list_folder = self.media_list_folder + Remove_Non_File_Characters(media_item) + "/"
					Create_Folder(self.current_media_list_folder, self.global_switches)

					self.media_item_details_file = self.current_media_list_folder + "Media Details" + self.dot_text
					Create_Text_File(self.media_item_details_file, self.global_switches)

					self.comments_folder = self.current_media_list_folder + self.mixed_comments_text + "/"
					Create_Folder(self.comments_folder, self.global_switches)

					self.titles_folder = self.current_media_list_folder + self.mixed_titles_text + "/"
					Create_Folder(self.titles_folder, self.global_switches)

					self.english_titles_file = self.titles_folder + full_language_en + self.dot_text
					Create_Text_File(self.english_titles_file, self.global_switches)

					self.portuguese_titles_file = self.titles_folder + full_language_pt + self.dot_text
					Create_Text_File(self.portuguese_titles_file, self.global_switches)

					if self.origin_type == self.remote_english_text or self.origin_type == self.hybrid_english_text:
						self.links_file = self.current_media_list_folder + "Links" + self.dot_text
						Create_Text_File(self.links_file, self.global_switches)

					if self.is_video_series_media == self.video_media_type_english_plural:
						self.youtube_ids_file = self.current_media_list_folder + self.youtube_ids_english_text + self.dot_text
						Create_Text_File(self.youtube_ids_file, self.global_switches)

			if self.has_media_list == False:
				self.media_list_names = []

		if self.is_series_media == False:
			self.files_to_create = [
				self.mixed_comment_text,
			]

			self.folders_to_create = [
				self.torrent_text,
				"Magnets",
			]

			for file in self.files_to_create:
				Create_Text_File(self.media_folder + file + self.dot_text, self.global_switches)

			for folder in self.folders_to_create:
				Create_Folder(self.media_folder + folder + "/", self.global_switches)

	def Write_To_Files(self):
		if Read_String(self.media_details_file) != Stringfy_Dict(self.media_details):
			Write_To_File(self.media_details_file, Stringfy_Dict(self.media_details), self.global_switches)

		if self.is_series_media == False:
			if Read_String(self.movie_details_file) != Stringfy_Dict(self.movie_details):	
				Write_To_File(self.movie_details_file, Stringfy_Dict(self.movie_details), self.global_switches)

		if self.is_series_media == True:
			if self.has_media_list == True:
				if Read_String(self.media_list_file) != Stringfy_Array(self.media_list_names, add_line_break = True):
					Write_To_File(self.media_list_file, Stringfy_Array(self.media_list_names, add_line_break = True), self.global_switches)

				if Read_String(self.current_media_item_file) != self.media_list_names[0]:
					Write_To_File(self.current_media_item_file, self.media_list_names[0], self.global_switches)

				for media_item in self.media_list_names:
					self.current_media_list_folder = self.media_list_folder + Remove_Non_File_Characters(media_item) + "/"
					Create_Folder(self.current_media_list_folder, self.global_switches)

					self.media_item_details_file = self.current_media_list_folder + "Media Details" + self.dot_text
					Create_Text_File(self.media_item_details_file, self.global_switches)

					if Read_String(self.media_item_details_file) != Stringfy_Dict(self.media_list[media_item]):
						Write_To_File(self.media_item_details_file, Stringfy_Dict(self.media_list[media_item]), self.global_switches)

		self.watching_status_text = Create_Array_Of_File(self.watching_status_file)

		if self.media_details["Original Name"] not in self.watching_status_text:
			self.watching_status_text.append(self.media_details["Original Name"])

		self.watching_status_text = Stringfy_Array(sorted(self.watching_status_text), add_line_break = True)

		if Read_String(self.watching_status_file) != self.watching_status_text:
			Write_To_File(self.watching_status_file, self.watching_status_text, self.global_switches)

		if self.media_details["Original Name"] not in self.media_type_media_names:
			self.media_type_media_names.append(self.media_details["Original Name"])

			self.media_type_media_names = Stringfy_Array(sorted(self.media_type_media_names), add_line_break = True)

			if Read_String(self.media_names_file) != self.media_type_media_names:
				Write_To_File(self.media_names_file, self.media_type_media_names, self.global_switches)

		self.media_number = Create_Array_Of_File(self.media_number_file)[0]
		self.all_media_number = Create_Array_Of_File(self.all_media_number_file)[0]

		if self.media_details["Original Name"] not in self.media_type_media_names:
			text_to_write = self.media_number + 1

			if Read_String(self.media_number_file) != text_to_write:
				Write_To_File(self.media_number_file, text_to_write, self.global_switches)

			text_to_write = self.all_media_number + 1

			if Read_String(self.all_media_number_file) != text_to_write:
				Write_To_File(self.all_media_number_file, text_to_write, self.global_switches)

	def Show_Info_Summary(self):
		self.large_bar = "-----"
		self.dash_space = "-"

		# This text defined by language and word gender (this, esse) for non-series, and (this, essa) for series
		self.this_text = self.gender_the_texts[self.mixed_media_type]["this"]

		self.this_media_text = format(self.this_text) + " " + self.language_singular_media_type

		print()
		print(self.large_bar)
		print()

		if self.is_new_media == True:
			print(Language_Item_Definer("Added", "Adicionado") + self.this_media_text + ":")
			print(self.media_details["Original Name"])

		if self.is_new_media == False:
			this = Define_Text_By_Number(len(self.old_media_list_names), Language_Item_Definer("this", "esse"), Language_Item_Definer("these", "esses"))
			item = Define_Text_By_Number(len(self.old_media_list_names), Language_Item_Definer("item", "item"), Language_Item_Definer("items", "itens"))
			s = Define_Text_By_Number(len(self.old_media_list_names), "", "s")

			english_media_item_text = "{} media {} to this".format(this, item)
			portuguese_media_item_text = "{} {} de mídia a ".format(this, item) + "ess{}".format(self.this_text)

			self.text_to_show = Language_Item_Definer("Added", "Adicionado") + " " + Language_Item_Definer(english_media_item_text, portuguese_media_item_text)

			if self.is_video_series_media == True:
				this_text = Language_Item_Definer(this + " " + self.youtube_name + " video series", "essa{} série{} de vídeos do ".format(s, s) + self.youtube_name)
				self.text_to_show = self.text_to_show.replace(Language_Item_Definer(english_media_item_text, portuguese_media_item_text), this_text)

			if self.is_video_series_media == False:
				this_text = Language_Item_Definer(this + " season{}".format(s), "essa{} temporada{}".format(s, s))
				self.text_to_show = self.text_to_show.replace(Language_Item_Definer(english_media_item_text, portuguese_media_item_text), this_text)

			if self.is_video_series_media == True:
				self.language_singular_media_type = Language_Item_Definer("channel", "canal")

			self.on_the_text = Language_Item_Definer("on the {} below", "n{}".format(self.this_text) + " {} abaixo").format(self.language_singular_media_type.lower())

			print(self.text_to_show + " " + self.on_the_text + ":")
			print()

			print(self.english_media_type.title() + ": ")
			print(self.media_details["Original Name"])
			print()
	
			print(Language_Item_Definer("Media " + item, item.capitalize() + " de Mídia") + ": ")
			print()

			print("-")
			print()

			for item in self.old_media_list_names:
				self.media_item_details = self.media_list[item]

				print(item)
				print()

				print(Language_Item_Definer("Episode", "Episódio") + ": " + self.media_item_details["Episode"])

				if "Remote Origin" in self.media_item_details:
					print(Language_Item_Definer("Remote Origin", "Origem Remota") + ": " + self.media_item_details["Remote Origin"])

				if len(self.old_media_list_names) != 1 and item != self.old_media_list_names[-1]:
					print()
					print(self.large_bar)

		if self.is_new_media == True:
			print()

			print(Language_Item_Definer("Year", self.default_portuguese_template_parameters["Year"]) + ":")
			print(self.media_details["Year"])
			print()

			print(Language_Item_Definer("Has Dub", self.default_portuguese_template_parameters["Has Dub"]) + ":")
			
			if Define_Yes_Or_No(self.media_details["Has Dub"]) == True:
				text_to_show = Language_Item_Definer("Yes", "Sim")

			if Define_Yes_Or_No(self.media_details["Has Dub"]) == False:
				text_to_show = Language_Item_Definer("No", "Não")
			
			print(text_to_show)

			print()
			print(Language_Item_Definer("Origin Type", self.default_portuguese_template_parameters["Origin Type"]) + ":")
			print(Language_Item_Definer(self.media_details["Origin Type"], self.portuguese_origin_types_dict[self.media_details["Origin Type"]]))

			print()
			print(Language_Item_Definer("Media type", "Tipo de mídia") + ":")
			print(self.singular_media_type_per_language.capitalize())

			print()
			print(Language_Item_Definer("Mixed media type", "Tipo de mídia misturado") + ":")
			print(self.mixed_media_type)

		print()
		print(self.large_bar)
		print()
		input(Language_Item_Definer("Press Enter when you finish reading the Info Summary", "Pressione Enter quando terminar de ler o Resumo de Informações") + ": ")
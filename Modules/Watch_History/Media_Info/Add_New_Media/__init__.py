# Add_New_Media.py

from Watch_History.Watch_History import Watch_History as Watch_History

from Watch_History.Media_Info.Fill_Episode_Titles import Fill_Episode_Titles as Fill_Episode_Titles

class Add_New_Media(Watch_History):
	def __init__(self, run_as_module = False):
		super().__init__()

		self.run_as_module = run_as_module

		if self.run_as_module == False:
			self.Define_Media_Type_Variables()
			self.Type_Media_Information()

			if self.has_media_list == True:
				self.Type_Media_List()

			self.Define_Media_Variables()
			self.Write_To_Files()
			self.Show_Information()
			Fill_Episode_Titles(self.option_info)

	def Define_Media_Type_Variables(self):
		dictionary = {}

		dictionary["select_media"] = False
		dictionary["media_type"] = {
			"select": self.language_texts["select_the_media_type_of_the_new_entry"],
		}

		self.option_info = self.Select_Media_Type_And_Media(dictionary, status_text = None)

		# Media Type variables definition
		self.plural_media_types = self.option_info["plural_media_type"]
		self.singular_media_types = self.option_info["singular_media_type"]
		self.mixed_plural_media_type = self.option_info["mixed_plural_media_type"]

		self.option_info["plural_media_types"] = self.option_info["plural_media_type"]

		self.media_names_file = self.media_info_name_files[self.plural_media_types["en"]]
		self.media_type_number_file = self.media_info_number_files[self.plural_media_types["en"]]

		self.media_dictionary["Media"]["States"]["series_media"] = True
		self.option_info["is_video_series_media"] = False

		# Series media, video series media, and re-watching variables definition
		if self.plural_media_types["en"] == self.texts["movies"]["en"]:
			self.media_dictionary["Media"]["States"]["series_media"] = False

		if self.plural_media_types["en"] == self.texts["videos"]["en"]:
			self.option_info["is_video_series_media"] = True

		self.media_info_media_type_folder = self.option_info["media_info_media_type_folder"]

		self.all_media_names = self.File.Contents(self.media_info_name_files[self.plural_media_types["en"]])["lines"]

		self.media_list = self.all_media_names

		self.media_type_media_names = self.File.Contents(self.media_names_file)["lines"]

	def Type_Media_Information(self):
		self.is_new_media = True

		self.add_media_items = False

		if self.media_dictionary["Media"]["States"]["series_media"] == True:
			self.add_media_items = self.Input.Yes_Or_No(self.language_texts["add_media_items_to_media"])

		if self.add_media_items == False:
			self.Type_Media_Details()

			if self.media_dictionary["Media"]["States"]["series_media"] == False:
				self.Type_Movie_Details()

		self.media_list_text = self.media_types["subfolders"][self.plural_media_types["en"]]["media_list"]
		self.singular_media_list_text = self.media_types["subfolders"][self.plural_media_types["en"]]["singular_media_list"]
		self.current_media_item_text = "Current " + self.singular_media_list_text

		if self.add_media_items == True:
			self.option_info = self.Select_Media(self.plural_media_types, self.singular_media_types, self.mixed_plural_media_type, self.media_list, self.media_info_media_type_folder)

			self.option_info["media_folder"] = self.option_info["media_folder"]
			self.Folder.Create(self.option_info["media_folder"])

			if self.media_dictionary["Media"]["States"]["series_media"] == True:
				self.media_dictionary["Media"]["item"]["folders"]["root"] = self.option_info["media_folder"] + self.media_list_text + "/"
				self.Folder.Create(self.media_dictionary["Media"]["item"]["folders"]["root"]) 

				self.media_list_file = self.media_dictionary["Media"]["item"]["folders"]["root"] + self.media_list_text + ".txt"
				self.File.Create(self.media_list_file)

		self.watching_status = self.option_info["media_details"][self.language_texts["status, title()"]]
		self.media_dictionary["Media"]["details"][self.language_texts["origin_type"]] = self.option_info["media_details"][self.language_texts["origin_type"]]

		self.watching_status_file = self.watching_status_files[self.plural_media_types["en"]][self.watching_status]

		if self.option_info["media_details"][self.JSON.Language.language_texts["original_name"]] in self.media_type_media_names:
			self.is_new_media = False

		if self.media_dictionary["Media"]["States"]["series_media"] == True:
			if self.option_info["media_details"][self.language_texts["origin_type"]] in [self.language_texts["remote, title()"], self.texts["hybrid, title()"]["en"]]:
				self.media_item_details_parameters["Remote origin"] = {
					"mode": "choice_dict",
					"select_text": self.language_texts["remote_origin"],
					"language_list": list(self.remote_origins.keys()),
					"dictionary": self.remote_origins
				}

			if self.add_media_items == False:
				self.has_media_list = self.Input.Yes_Or_No(self.language_texts["has_media_list_(like_seasons_or_video_series)"])

			if self.add_media_items == True:
				self.has_media_list = True

			if self.has_media_list == False:
				dict_ = dict()

				for key in self.option_info["media_details"].copy():
					dict_[key] = self.option_info["media_details"][key]

					if key == self.language_texts["status, title()"]:
						dict_.update({self.language_texts["episode, title()"]: "None"})

				self.option_info["media_details"] = dict_
				del dict_

	def Type_Media_Details(self):
		self.option_info["media_details"] = {}

		print()
		print("-----")
		print()
		print(self.language_texts["please_type_the_media_details"] + ":")

		for self.parameter_name in self.media_details_parameters:
			if self.parameter_name in self.media_details_string_parameters:
				self.parameter_data = self.media_details_string_parameters[self.parameter_name]
				self.type_text = self.parameter_data["select_text"]
				self.default_parameter = self.parameter_data["default"]

				if type(self.default_parameter) == dict:
					self.default_parameter = self.option_info["media_details"][self.default_parameter["format_name"]]

				self.input_parameter = self.Input.Type(self.type_text, next_line = True)

				if self.input_parameter == "":
					self.input_parameter = self.default_parameter

			if self.parameter_name in self.media_details_choice_list_parameters:
				self.parameter_data = self.media_details_choice_list_parameters[self.parameter_name]
				self.show_text = self.parameter_data["select_text"]
				self.language_list = self.parameter_data["language_list"]
				self.english_list = self.parameter_data["english_list"]

				self.input_parameter = self.Input.Select(self.english_list, self.language_list, show_text = self.show_text)["option"]

			if self.parameter_name in self.media_details_yes_or_no_definer_parameters:
				self.input_parameter = self.Input.Yes_Or_No(self.media_details_yes_or_no_definer_parameters[self.parameter_name])

			if self.parameter_name == self.language_texts["has_dub"] and self.input_parameter == True:
				self.option_info["media_details"][self.parameter_name] = "Yes"

			if self.parameter_name == self.JSON.Language.language_texts["language_name"][self.user_language] and self.input_parameter != self.option_info["media_details"][self.JSON.Language.language_texts["original_name"]]:
				self.option_info["media_details"][self.parameter_name] = self.input_parameter

			if self.parameter_name not in [self.JSON.Language.language_texts["language_name"][self.user_language], self.language_texts["has_dub"]]:
				self.option_info["media_details"][self.parameter_name] = self.input_parameter

			if self.parameter_name == self.JSON.Language.language_texts["language_name"][self.user_language] and self.plural_media_types["en"] == self.texts["animes"]["en"]:
				self.select_text = self.language_texts["romanized_name"]

				self.input_parameter = self.Input.Type(self.select_text, next_line = True)

				self.option_info["media_details"][self.language_texts["romanized_name"]] = self.input_parameter

		print()
		print(self.language_texts["you_finished_typing_the_media_details"] + ".")
		print()
		print("-----")

	def Type_Movie_Details(self):
		self.movie_details = {}

		if self.language_texts["year, title()"] in self.option_info["media_details"]:
			self.movie_details[self.language_texts["year, title()"]] = self.option_info["media_details"][self.language_texts["year, title()"]]

		print()
		print("-----")
		print()
		print(self.language_texts["please_type_the_movie_details"] + ":")

		for parameter in self.movie_details_parameters:
			self.movie_details[parameter] = self.Input.Type(parameter, accept_enter = False, next_line = True)

		print()
		print(self.language_texts["you_finished_typing_the_movie_details"] + ".")
		print()
		print("-----")

	def Type_Media_List(self):
		self.media_list = {}
		self.media_list_names = []
		self.old_media_list_names = []

		if self.is_new_media == False:
			self.old_media_list_names.extend(self.media_list_names)

			self.media_list_names.extend(self.File.Contents(self.media_list_file)["lines"])

			for media_item in self.File.Contents(self.media_list_file)["lines"]:
				media_item_folder = self.media_dictionary["Media"]["item"]["folders"]["root"] + self.Sanitize(media_item, restricted_characters = True) + "/"
				media_item_details_file = media_item_folder + "Media details.txt"

				self.media_list[media_item] = self.File.Dictionary(media_item_details_file)

		self.add_more_media = True

		while self.add_more_media == True:
			self.media_dictionary["Media"]["item"]["details"] = {}

			print()
			print("-----")
			print()
			print(self.language_texts["please_type_the_media_item_details"] + ":")

			for self.parameter_name in self.media_item_details_parameters:
				self.parameter_data = self.media_item_details_parameters

				if type(self.parameter_data) == dict:
					self.parameter_data = self.parameter_data[self.parameter_name]

				self.select_text = self.parameter_data["select_text"]

				if self.parameter_data["mode"] == "string":
					self.input_parameter = self.Input.Type(self.select_text + ":", accept_enter = False, next_line = True)

				if self.parameter_data["mode"] == "string/default":
					self.default_parameter = self.parameter_data["default"]

					self.input_parameter = self.Input.Type(self.select_text, next_line = True)

					if self.input_parameter == "":
						self.input_parameter = self.default_parameter

				if self.parameter_data["mode"] == "string/default-format":
					if self.option_info["is_video_series_media"] == False:
						self.default_parameter = self.media_dictionary["Media"]["item"]["details"][self.parameter_data["default"]["format_name"]]

						if self.parameter_name == self.language_texts["origin_location"] and self.default_parameter != self.media_dictionary["Media"]["item"]["details"][self.parameter_data["default"]["format_name"]]:
							self.default_parameter += "-" + self.media_dictionary["Media"]["item"]["details"][self.parameter_data["default"]["format_name"]]

						for function in self.parameter_data["default"]["functions"]:
							self.default_parameter = function(self.default_parameter)

						self.input_parameter = self.Input.Type(self.select_text, next_line = True)

						if self.input_parameter == "":
							self.input_parameter = self.default_parameter

					if self.option_info["is_video_series_media"] == True and self.parameter_name == self.JSON.Language.language_texts["[language]_name"]:
						self.default_parameter = self.media_dictionary["Media"]["item"]["details"][self.parameter_data["default"]["format_name"]]

						for function in self.parameter_data["default"]["functions"]:
							self.default_parameter = function(self.default_parameter)

						self.input_parameter = self.Input.Type(self.select_text, next_line = True)

						if self.input_parameter == "":
							self.input_parameter = self.default_parameter

					if self.option_info["is_video_series_media"] == True and self.parameter_name == self.language_texts["origin_location"]:
						self.select_text = self.language_texts["type_the_video_series_playlist_link"]
						self.input_parameter = self.Input.Type(self.select_text, next_line = True).split("playlist?list=")[1]

				if self.parameter_data["mode"] == "choice_dict":
					self.parameter_data = self.media_item_details_parameters[self.parameter_name]
					self.show_text = self.parameter_data["select_text"]
					self.language_list = self.parameter_data["language_list"]
					self.dictionary = self.parameter_data["dictionary"]

					self.input_parameter = self.Input.Select(self.language_list, show_text = self.show_text)["option"]

					self.input_parameter = self.dictionary[self.input_parameter]

				if self.parameter_name == self.JSON.Language.language_texts["[language]_name"] and self.input_parameter != self.media_dictionary["Media"]["item"]["details"][self.JSON.Language.language_texts["original_name"]]:
					self.media_dictionary["Media"]["item"]["details"][self.parameter_name] = self.input_parameter

				if self.parameter_name != self.JSON.Language.language_texts["[language]_name"]:
					self.media_dictionary["Media"]["item"]["details"][self.parameter_name] = self.input_parameter

			self.media_list[self.media_dictionary["Media"]["item"]["details"][self.JSON.Language.language_texts["original_name"]]] = self.media_dictionary["Media"]["item"]["details"]
			self.media_list_names.append(self.media_dictionary["Media"]["item"]["details"][self.JSON.Language.language_texts["original_name"]])
			self.old_media_list_names.append(self.media_dictionary["Media"]["item"]["details"][self.JSON.Language.language_texts["original_name"]])

			print()
			print(self.language_texts["you_finished_typing_the_media_item_details"] + ".")
			print()
			print("-----")

			self.show_text = self.language_texts["add_more_media"]
			self.add_more_media = self.Input.Yes_Or_No(self.show_text)

	def Define_Media_Variables(self):
		name = self.option_info["media_details"][self.JSON.Language.language_texts["original_name"]]

		if self.plural_media_types["en"] == self.texts["animes"]["en"]:
			name = self.option_info["media_details"][self.language_texts["romanized_name"]]

		self.option_info["media_folder"] = self.media_info_media_type_folder + self.Sanitize(name, restricted_characters = True) + "/"
		self.Folder.Create(self.option_info["media_folder"])

		self.option_info["media_details_file"] = self.option_info["media_folder"] + "Media details.txt"
		self.File.Create(self.option_info["media_details_file"])

		if self.media_dictionary["Media"]["States"]["series_media"] == False:
			self.movie_details_file = self.option_info["media_folder"] + "Movie details.txt"
			self.File.Create(self.movie_details_file)	

		if self.is_new_media == False:
			self.option_info["media_details"] = self.File.Dictionary(self.option_info["media_details_file"])

		if self.media_dictionary["Media"]["States"]["series_media"] == True:
			if self.has_media_list == True:
				self.media_dictionary["Media"]["item"]["folders"]["root"] = self.option_info["media_folder"] + self.media_list_text + "/"
				self.Folder.Create(self.media_dictionary["Media"]["item"]["folders"]["root"])

				self.media_list_file = self.media_dictionary["Media"]["item"]["folders"]["root"] + self.media_list_text + ".txt"
				self.File.Create(self.media_list_file)

				self.current_media_item_file = self.media_dictionary["Media"]["item"]["folders"]["root"] + self.current_media_item_text + ".txt"
				self.File.Create(self.current_media_item_file)

				media_list_names = []
				media_list_names.extend(self.media_list_names)

				self.media_list_names = media_list_names

				for media_item in self.media_list_names:
					self.current_media_list_folder = self.media_dictionary["Media"]["item"]["folders"]["root"] + self.Sanitize(media_item, restricted_characters = True) + "/"
					self.Folder.Create(self.current_media_list_folder)

					self.media_dictionary["Media"]["item"]["folders"]["details"] = self.current_media_list_folder + "Media details.txt"
					self.File.Create(self.media_dictionary["Media"]["item"]["folders"]["details"])

					self.comments_folder = self.current_media_list_folder + self.texts["comments, title(), en - pt"] + "/"
					self.Folder.Create(self.comments_folder)

					self.titles_folder = self.current_media_list_folder + self.texts["titles, title(), en - pt"] + "/"
					self.Folder.Create(self.titles_folder)

					for full_language in list(self.JSON.Language.languages["full"].values()):
						self.titles_file = self.titles_folder + full_language + ".txt"
						self.File.Create(self.titles_file)

					if self.media_dictionary["Media"]["details"][self.language_texts["origin_type"]] == self.language_texts["remote, title()"] or self.media_dictionary["Media"]["details"][self.language_texts["origin_type"]] == self.language_texts["hybrid, title()"]:
						self.links_file = self.current_media_list_folder + "Links.txt"
						self.File.Create(self.links_file)

					if self.option_info["is_video_series_media"] == True:
						self.youtube_ids_file = self.current_media_list_folder + self.texts["youtube_ids"]["en"] + ".txt"
						self.File.Create(self.youtube_ids_file)

			if self.has_media_list == False:
				self.media_list_names = []

		if self.media_dictionary["Media"]["States"]["series_media"] == False:
			self.files_to_create = [
				self.texts["comment, title(), en - pt"],
			]

			self.folders_to_create = [
				"Torrent",
				"Magnets",
			]

			for file in self.files_to_create:
				self.File.Create(self.option_info["media_folder"] + file + ".txt")

			for folder in self.folders_to_create:
				self.Folder.Create(self.option_info["media_folder"] + folder + "/")

		self.File.Edit(self.option_info["media_details_file"], self.Text.From_Dictionary(self.option_info["media_details"]), "w")

		self.option_info = self.Define_Media_Titles(self.option_info)

	def Write_To_Files(self):
		self.File.Edit(self.option_info["media_details_file"], self.Text.From_Dictionary(self.option_info["media_details"]), "w")

		if self.media_dictionary["Media"]["States"]["series_media"] == False:
			self.File.Edit(self.movie_details_file, self.Text.From_Dictionary(self.movie_details, next_line_value = True), "w")

		if self.media_dictionary["Media"]["States"]["series_media"] == True and self.has_media_list == True:
			self.File.Edit(self.media_list_file, self.Text.From_List(self.media_list_names), "w")

			self.File.Edit(self.current_media_item_file, self.media_list_names[0], "w")

			for media_item in self.media_list_names:
				self.current_media_list_folder = self.media_dictionary["Media"]["item"]["folders"]["root"] + Remove_Non_File_Characters(media_item) + "/"
				self.Folder.Create(self.current_media_list_folder)

				self.media_dictionary["Media"]["item"]["folders"]["details"] = self.current_media_list_folder + "Media details.txt"
				self.File.Create(self.media_dictionary["Media"]["item"]["folders"]["details"])

				self.File.Edit(self.media_dictionary["Media"]["item"]["folders"]["details"], self.Text.From_Dictionary(self.media_list[media_item]), "w")

		self.watching_status_text = self.File.Contents(self.watching_status_file)["lines"]

		name = self.option_info["media_details"][self.JSON.Language.language_texts["original_name"]]

		if self.plural_media_types["en"] == self.texts["animes"]["en"]:
			name = self.option_info["media_details"][self.language_texts["romanized_name"]]

		if name not in self.watching_status_text:
			self.watching_status_text.append(name)

		self.watching_status_text = self.Text.From_List(sorted(self.watching_status_text, key=str.lower))

		self.File.Edit(self.watching_status_file, self.watching_status_text, "w")

		# Add to media type names file
		if name not in self.media_type_media_names:
			self.media_type_media_names.append(name)

			self.media_type_media_names = self.Text.From_List(sorted(self.media_type_media_names, key=str.lower))

			# Edit media type names file
			self.File.Edit(self.media_names_file, self.media_type_media_names, "w")

			self.all_media_number = self.File.Contents(self.media_number_file)["lines"][0]
			self.media_number = self.File.Contents(self.media_type_number_file)["lines"][0]

			# Add to all media number file
			text = str(int(self.all_media_number) + 1)
			self.File.Edit(self.media_number_file, text, "w")

			# Add to media type number file
			text = str(int(self.media_number) + 1)
			self.File.Edit(self.media_type_number_file, text, "w")

	def Show_Information(self):
		self.the_text, self.this_text, self.of_text = self.Define_The_Text(self.plural_media_types)

		self.this_media_text = {
			"en": self.language_texts["added"].title(),
			"pt": self.language_texts["added"][:-1].title() + self.the_text,
		}

		if self.option_info["is_video_series_media"] == True:
			self.singular_media_types["language"] = self.language_texts["channel"]

		self.text_to_show = self.JSON.Language.Item(self.this_media_text)

		if self.is_new_media == True:
			self.text_to_show += " " + self.this_text + " " + self.singular_media_types["language"].lower()

		if self.is_new_media == False:
			this = self.Text.By_Number(self.old_media_list_names, self.language_texts["this, masculine"], self.language_texts["this, masculine"])
			these = self.Text.By_Number(self.old_media_list_names, self.language_texts["these, masculine"], self.language_texts["these, masculine"])
			item = self.Text.By_Number(self.old_media_list_names, self.language_texts["item"], self.language_texts["item"])
			serie = self.Text.By_Number(self.old_media_list_names, self.language_texts["serie"], self.language_texts["series"])
			season = self.Text.By_Number(self.old_media_list_names, self.language_texts["season"], self.language_texts["seasons"])
			s = self.Text.By_Number(self.old_media_list_names, "", "s")

			texts = {
				"en": "{} media {} to this".format(this, item),
				"pt": "{} {} de mídia a ".format(this, item) + this,
			}

			media_item_text = self.JSON.Language.Item(texts)
			self.text_to_show += " " + media_item_text

			if self.option_info["is_video_series_media"] == True:
				texts = {
					"en": this + " YouTube video " + serie,
					"pt": this + " {} de vídeos do YouTube".format(serie, s),
				}

				this_text = self.JSON.Language.Item(texts)
				self.text_to_show = self.text_to_show.replace(media_item_text, this_text)

			if self.option_info["is_video_series_media"] == False:
				this_text = this + " " + season
				self.text_to_show = self.text_to_show.replace(media_item_text, this_text)

			texts = {
				"en": "on the {} below",
				"pt": "n{}".format(self.this_text) + " {} abaixo".format(self.singular_media_types["language"].lower()),
			}

			self.text_to_show += " " + self.JSON.Language.Item(texts)

		print()
		print(self.large_bar)
		print()

		if self.is_new_media == True:
			print(self.text_to_show + ":")

			self.Show_Media_Title(self.option_info)

			print()
			print(self.language_texts["year, title()"] + ":")
			print(self.option_info["media_details"][self.language_texts["year, title()"]])
			print()

			print(self.language_texts["has_dub"].capitalize() + ":")

			if self.language_texts["has_dub"] in self.option_info["media_details"]:
				if self.Input.Define_Yes_Or_No(self.option_info["media_details"][self.language_texts["has_dub"]]) == True:
					text_to_show = self.language_texts["yes, title()"]

				if self.Input.Define_Yes_Or_No(self.option_info["media_details"][self.language_texts["has_dub"]]) == False:
					text_to_show = self.language_texts["no, title()"]

			if self.language_texts["has_dub"] not in self.option_info["media_details"]:
				text_to_show = self.language_texts["no, title()"]

			print(text_to_show)

			print()
			print(self.language_texts["origin_type"] + ":")
			print(self.option_info["media_details"][self.language_texts["origin_type"]])

			print()
			print(self.language_texts["media_type"] + ":")
			print(self.singular_media_types["language"].capitalize())

			if self.plural_media_types["en"] != self.texts["animes"]["en"]:
				print()
				print(self.language_texts["mixed_media_type"] + ":")
				print(self.mixed_plural_media_type)

		if self.is_new_media == False:
			print(self.singular_media_types["language"].title() + ":")
			print(self.option_info["media_details"][self.JSON.Language.language_texts["original_name"]])

			if self.JSON.Language.language_texts["[language]_name"] in self.option_info["media_details"] and self.option_info["media_details"][self.JSON.Language.language_texts["[language]_name"]] != self.option_info["media_details"][self.JSON.Language.language_texts["original_name"]]:
				print(self.option_info["media_details"][self.JSON.Language.language_texts["[language]_name"]])

			print()

		if self.has_media_list == True:
			item = self.Text.By_Number(self.old_media_list_names, self.language_texts["item"], self.language_texts["item"])

			media_item_texts = {
				"en": "Media " + item,
				"pt": item.capitalize() + " de mídia",
			}

			media_item_texts = self.JSON.Language.Item(media_item_texts)

			print(media_item_texts + ":")
			print()

			print("-")
			print()

			for item in self.old_media_list_names:
				self.media_dictionary["Media"]["item"]["details"] = self.media_list[item]

				text = item

				if self.JSON.Language.language_texts["[language]_name"] in self.media_dictionary["Media"]["item"]["details"] and self.media_dictionary["Media"]["item"]["details"][self.JSON.Language.language_texts["[language]_name"]] != self.media_dictionary["Media"]["item"]["details"][self.JSON.Language.language_texts["original_name"]]:
					text += "\n\t" + self.media_dictionary["Media"]["item"]["details"][self.JSON.Language.language_texts["[language]_name"]]

				print(text + ":")
				print()

				print("\t" + self.language_texts["episode, title()"] + ":")
				print("\t" + self.media_dictionary["Media"]["item"]["details"][self.language_texts["episode, title()"]])

				if "Remote origin" in self.media_dictionary["Media"]["item"]["details"]:
					print()
					print("\t" + self.language_texts["remote_origin"] + ":")
					print("\t" + self.media_dictionary["Media"]["item"]["details"]["Remote origin"])

				if len(self.old_media_list_names) != 1 and item != self.old_media_list_names[-1]:
					print()
					print(self.large_bar)

		print()
		print(self.large_bar)

		self.Input.Type(self.JSON.Language.language_texts["press_enter_when_you_finish_reading_the_info_summary"])
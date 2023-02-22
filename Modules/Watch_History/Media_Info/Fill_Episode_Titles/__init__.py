# Fill_Episode_Titles.py

from Watch_History.Watch_History import Watch_History as Watch_History

from Watch_History.Watch_Media import Watch_Media

class Fill_Episode_Titles(Watch_History):
	def __init__(self, option_info = None):
		super().__init__()

		texts = self.Remove_Media_Type([self.texts["movies"]["en"], self.texts["movies"]["pt"]])

		self.option_info = option_info

		if self.option_info == None:
			self.lists_dict = {}
			self.lists_dict["media_type_list"] = self.media_types["singular"]["en"]
			self.lists_dict["language_media_type_list"] = self.media_types["singular"][self.user_language]
			self.lists_dict["media_type_show_text"] = self.language_texts["media_types_that_contain_episode_titles_files"]
			self.lists_dict["media_type_select_text"] = self.language_texts["select_a_media_type_to_list_their_media"]

			self.lists_dict["media_select_text"] = self.language_texts["select_a_media_to_fill_its_episode_titles_file"]
			self.lists_dict["media_list"] = "all"

			self.option_info = self.Select_Media_Type_And_Media(self.lists_dict)

		# Media Type variables definition
		self.plural_media_types = self.option_info["plural_media_type"]
		self.singular_media_types = self.option_info["singular_media_type"]
		self.mixed_plural_media_type = self.option_info["mixed_plural_media_type"]

		# Media variables definition (folder, details file, and details)
		self.media_folder = self.option_info["media_folder"]
		self.media_details_file = self.option_info["media_details_file"]
		self.media_details = self.File.Dictionary(self.media_details_file)

		self.Watch_Media = Watch_Media(run_as_module = True, open_media = False, option_info_parameter = self.option_info)

		self.episode_titles_files = self.Watch_Media.episode_titles_files

		self.media_dictionary["Media"]["States"]["video"] = self.Watch_Media.is_video_series_media
		self.media_dictionary["Media"]["States"]["media_list"] = self.Watch_Media.no_media_list

		print()
		print("-----")

		self.Define_Variables()
		self.Fill_Files()

		if self.media_dictionary["Media"]["States"]["video"] == True:
			self.Fill_YouTube_IDs_File()

			print()
			print(self.language_texts["finished_filling_the_youtube_ids_file"] + ".")

	def Define_Variables(self):
		print()
		print(self.language_texts["filling_the_episode_titles_files"] + "...")

		for language in self.languages["small"]:
			translated_language = self.languages["full_translated"][language][self.user_language]

			print()
			print(self.language_texts["episode_titles_file_in_{}"].format(translated_language) + ":")
			print(self.episode_titles_files[language])

		print()

		self.episode_number_text = self.language_texts["type_the_number_of_episodes"]

		try:
			self.episode_number = int(self.Input.Type(self.episode_number_text + " " + "(Ex: 01)", first_space = False)) + 1

		except ValueError:
			self.episode_number = 1

		if self.media_dictionary["Media"]["States"]["media_list"] == False:
			try:
				self.all_episode_number = self.Input.Type(self.language_texts["type_the_number_of_all_media_episodes"], first_space = False)

				if self.all_episode_number != "":
					self.all_episode_number = int(self.all_episode_number)

			except ValueError:
				self.all_episode_number = 1

		print()
		print("---")
		print()

	def Replace_Text(self, text):
		items_to_remove = [
			"(",
			")",
			"\t",
			'"',
		]

		if " " in text[0]:
			text = text[:1]

		if " " in text[-1]:
			text = text[:-1]

		for item in items_to_remove:
			if item in text:
				text = text.replace(item, "")

		return text

	def Fill_Files(self):
		i = 1
		while i <= self.episode_number:
			for language in self.languages["small"]:
				translated_language = self.languages["full_translated"][language][self.user_language]

				self.episode_titles_file = self.episode_titles_files[language]

				print(str(i) + "/" + str(self.episode_number + 1) + ":")

				episode_title = self.Input.Type(self.language_texts["type_or_paste_the_episode_title_in_{}"].format(translated_language), accept_enter = False, next_line = True, first_space = False)

				episode_title = '"' + self.Replace_Text(episode_title) + '"'

				if self.media_dictionary["Media"]["States"]["media_list"] == False and self.all_episode_number != "":
					all_episodes_number_text = "(" + str(self.Text.Add_Leading_Zeros(self.all_episode_number)) + ")"

				current_episode_number = str(self.Text.Add_Leading_Zeros(i))

				full_episode_title = "EP" + current_episode_number

				if self.media_dictionary["Media"]["States"]["media_list"] == False and self.all_episode_number != "":
					full_episode_title += str(all_episodes_number_text)

				full_episode_title += " " + episode_title

				text_to_append = episode_title
				self.File.Edit(self.episode_titles_file, full_episode_title, "a")

				print()
				print(translated_language + ":")
				print(full_episode_title)
				print()
				print("---")
				print()

				if self.media_dictionary["Media"]["States"]["media_list"] == False and self.all_episode_number != "":
					self.all_episode_number += 1

			i += 1

		print(self.language_texts["finished_filling_episode_titles_files"] + ".")

	def Fill_YouTube_IDs_File(self):
		from urllib.parse import urlparse, parse_qs
		import validators

		print()
		print("---")

		print()
		print(self.language_texts["please_paste_the_youtube_video_links_below_separated_by_lines"] + ":")

		self.links = self.Input.Lines(accept_enter = False)["lines"]

		self.youtube_ids = []

		for link in self.links:
			link = self.Replace_Text(link)

			if validators.url(link) == True:
				link = urlparse(link)
				query = link.query
				parameters = parse_qs(query)

				if "v" in parameters:
					id = parameters["v"][0]

					self.youtube_ids.append(id)

		self.youtube_video_ids_file = self.Watch_Media.youtube_video_ids_file

		self.File.Edit(self.youtube_video_ids_file, self.Text.From_List(self.youtube_ids), "w")
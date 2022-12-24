# Watch_List_Of_Media.py

from Watch_History.Watch_History import Watch_History as Watch_History

from Watch_History.Watch_Media import Watch_Media as Watch_Media

class Watch_List_Of_Media(Watch_History):
	def __init__(self):
		super().__init__()

		self.finish_selection_text = "[" + self.Language.language_texts["finish_selection"] + "]"

		self.Define_Media_List_Dict()

		self.selected_option = ""

		self.media_title = ""
		self.media_titles = [0]

		if self.File.Exist(self.watch_list_file) == True:
			self.media_titles = self.File.Contents(self.watch_list_file)["lines"]

		self.i = 2
		f = 0
		while self.selected_option != self.finish_selection_text and self.media_title != self.media_titles[-1]:
			if self.File.Exist(self.watch_list_file) == True and f < len(self.media_titles):
				self.media_title = self.media_titles[f]

			self.option_info = self.Select_Media_To_Watch()

			if self.selected_option not in self.media_list_dict:
				self.i = 2

			if self.selected_option == self.finish_selection_text:
				print()

			if self.option_info != None:
				print(self.language_texts["current_media_list"] + ":")

				self.Show_Media_List()

			f += 1

		print()
		print("-----")
		print()
		print(self.language_texts["starting_to_watch_the_list_of_media"] + "...")
		print()

		media_number = len(list(self.media_list_dict.keys()))

		self.i = 1
		for media_title in self.media_list_dict.copy():
			self.option_info = self.media_list_dict[media_title]

			self.singular_media_type = self.option_info["singular_media_type"]["language"]

			if self.i != 1:
				print()
				print("---")
				print()

			print(self.language_texts["list_of_media_to_watch"] + ":")

			self.Show_Media_List(media_title)

			print()
			print(self.language_texts["number, title()"] + ": " + str(self.i) + "/" + str(len(list(self.media_list_dict))))

			self.Start_Watching_Media(self.option_info)

			self.i += 1

		print()
		print("-----")
		print()
		print(self.language_texts["you_finished_watching_your_list_of_media"] + ".")
		print()

		print(self.language_texts["list_of_watched_media"] + ":")

		self.Show_Media_List()

		print()
		print("-----")

	def Define_Media_List_Dict(self):
		self.media_list_dict = {}

	def Select_Media_To_Watch(self, media = None):
		self.status_text = [self.language_texts["watching, title()"], self.language_texts["re_watching, title()"]]

		if self.File.Exist(self.watch_list_file) == False:
			option_infos = [self.Select_Media_Type()]

		if self.File.Exist(self.watch_list_file) == True:
			option_infos = []

			i = 0
			for media_type in self.texts["plural_media_types, type: list"]["en"]:
				option_infos.append(self.Select_Media_Type(dictionary = {"number": i}))

				i += 1

		media_is_defined = False

		i = 0
		for option_info in option_infos:
			# Media Type variables definition
			self.plural_media_types = option_info["plural_media_type"]
			self.singular_media_types = option_info["singular_media_type"]
			self.mixed_plural_media_type = option_info["mixed_plural_media_type"]

			self.media_info_media_type_folder = option_info["media_info_media_type_folder"]

			media_list = self.Create_Media_List(self.status_text)[self.plural_media_types["en"]]

			if self.media_list_dict != {}:
				media_list.append(self.finish_selection_text)

			if self.File.Exist(self.watch_list_file) == False:
				option_info.update(self.Select_Media(self.plural_media_types, self.singular_media_types, self.mixed_plural_media_type, media_list, self.media_info_media_type_folder))

			if self.File.Exist(self.watch_list_file) == True:
				if self.media_title in media_list:
					option_info.update(self.Select_Media(self.plural_media_types, self.singular_media_types, self.mixed_plural_media_type, media_list, self.media_info_media_type_folder, option_info_parameter = {"media": self.media_title}))

					option_info["media"] = self.media_title

				if self.media_title not in media_list:
					option_info["media"] = ""

			self.selected_option = option_info["media"]

			if self.selected_option != self.finish_selection_text and self.selected_option != "":
				self.Watch_Media = Watch_Media(run_as_module = True, open_media = False, option_info_parameter = option_info)

				option_info.update(self.Watch_Media.media_dictionary)

				self.media_details = self.Watch_Media.media_details
				self.media_item_details = self.Watch_Media.media_item_details

				print()
				print("[" + self.singular_media_types["language"] + ":")

				self.Show_Media_Title(option_info)

				if self.language_texts["episode, title()"] in self.media_item_details:
					print()
					print(self.language_texts["episode, title()"] + ":")
					print(self.media_item_details[self.language_texts["episode, title()"]] + "]")
					print()

				if option_info["media"] not in self.media_list_dict:
					self.i = 2

				if option_info["media"] in self.media_list_dict:
					if option_info["media"] + " (2x)" in list(self.media_list_dict.keys()):
						self.i += 1

					option_info["media"] += " (" + str(self.i) + "x)"

				self.media_list_dict[option_info["media"]] = option_info

				self.option_info = option_info
				media_is_defined = True

				if self.File.Exist(self.watch_list_file) == False:
					self.media_titles[-1] = self.media_title

		if media_is_defined == True:
			return self.option_info

	def Show_Media_List(self, media_title = None):
		number = 1
		for item in self.media_list_dict:
			text = str(number)

			if item == media_title:
				text += " (" + self.language_texts["watching, title()"] + ")"

			if media_title != None and self.i > number and item != media_title:
				text += " (" + self.language_texts["watched, title()"] + ")"

			text += ": " + item

			print(text)

			number += 1

	def Start_Watching_Media(self, option_info):
		self.Watch_Media = Watch_Media(option_info_parameter = option_info)
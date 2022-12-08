# Watch_List_Of_Media.py

from Watch_History.Watch_History import Watch_History as Watch_History

from Watch_History.Watch_Media import Watch_Media as Watch_Media

class Watch_List_Of_Media(Watch_History):
	def __init__(self):
		super().__init__()

		self.finish_selection_text = self.Language.language_texts["finish_selection"]

		self.Define_Media_List_Dict()

		self.media_title = ""

		self.i = 2
		while self.media_title != self.finish_selection_text:
			self.option_info = self.Select_Media_To_Watch()

			if self.media_title == self.finish_selection_text:
				print()

			print(self.language_texts["current_media_list"] + ":")
			print(list(self.media_list_dict.keys()))

		print()
		print("-----")
		print()
		print(self.language_texts["starting_to_watch_the_list_of_media"] + "...")
		print()

		media_number = len(list(self.media_list_dict.keys()))

		i = 1
		for media_title in self.media_list_dict:
			self.option_info = self.media_list_dict[media_title]

			self.singular_media_type = self.option_info["singular_media_type"]["language"]

			print(self.Language.language_texts["list, title()"] + ": " + str(i) + "/" + str(media_number))
			print()
			print("---")
			print()

			self.Start_Watching_Media(self.option_info)

			i += 1

		print()
		print("-----")
		print()
		print(self.language_texts["you_finished_watching_your_list_of_media"] + ".")

	def Define_Media_List_Dict(self):
		self.media_list_dict = {}

	def Select_Media_To_Watch(self):
		self.status_text = [self.language_texts["watching, title()"], self.language_texts["re_watching, title()"]]

		option_info = self.Select_Media_Type()

		# Media Type variables definition
		self.plural_media_types = option_info["plural_media_type"]
		self.singular_media_types = option_info["singular_media_type"]
		self.mixed_plural_media_type = option_info["mixed_plural_media_type"]

		self.media_info_media_type_folder = option_info["media_info_media_type_folder"]

		media_list = self.Create_Media_List(self.status_text)[self.plural_media_types["en"]]

		if self.media_list_dict != {}:
			media_list.append(self.finish_selection_text)

		option_info.update(self.Select_Media(self.plural_media_types, self.singular_media_types, self.mixed_plural_media_type, media_list, self.media_info_media_type_folder))

		self.media_title = option_info["media"]

		if self.media_title != self.finish_selection_text:
			self.Watch_Media = Watch_Media(run_as_module = True, open_media = False, option_info = option_info)

			self.media_details = self.Watch_Media.media_details
			self.media_item_details = self.Watch_Media.media_item_details

			print()
			print(self.singular_media_types["language"] + ":")
			print(self.media_title)

			if self.language_texts["episode, title()"] in self.media_item_details:
				print()
				print(self.language_texts["episode, title()"] + ":")
				print(self.media_item_details[self.language_texts["episode, title()"]])

				print()

			if self.media_title in self.media_list_dict:
				self.media_list_dict[self.media_title + " (" + str(self.i) + "x)"] = option_info

				self.i += 1

			if self.media_title not in self.media_list_dict:
				self.media_list_dict[self.media_title] = option_info

		return option_info

	def Start_Watching_Media(self, option_info):
		self.Watch_Media = Watch_Media(run_as_module = True, option_info = option_info)
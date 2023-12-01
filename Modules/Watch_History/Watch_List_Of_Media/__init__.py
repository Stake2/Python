# Watch_List_Of_Media.py

from Watch_History.Watch_History import Watch_History as Watch_History

from Watch_History.Watch_Media import Watch_Media as Watch_Media

class Watch_List_Of_Media(Watch_History):
	def __init__(self):
		super().__init__()

		self.finish_selection_text = "[" + self.JSON.Language.language_texts["finish_selection"] + "]"

		self.Define_Media_List_Dict()

		self.selected_option = ""

		self.media_title = ""
		self.media_titles = [0]

		if self.File.Exist(self.folders["Audiovisual Media"]["Watch List"]) == True:
			self.media_titles = self.File.Contents(self.folders["Audiovisual Media"]["Watch List"])["lines"]

		self.i = 2
		f = 0
		while self.selected_option != self.finish_selection_text and self.media_title != self.media_titles[-1]:
			if self.File.Exist(self.folders["Audiovisual Media"]["Watch List"]) == True and f < len(self.media_titles):
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
		self.status_text = [
			self.language_texts["watching, title()"],
			self.language_texts["re_watching, title()"]
		]

		if self.File.Exist(self.folders["Audiovisual Media"]["Watch List"]) == False:
			option_infos = [
				self.Select_Media_Type()
			]

		if self.File.Exist(self.folders["Audiovisual Media"]["Watch List"]) == True:
			option_infos = []

			i = 0
			for plural_media_type in self.media_types["Plural"]["en"]:
				option_infos.append(self.Select_Media_Type(options = {"number": i}))

				i += 1

		media_is_defined = False

		i = 0
		for option_info in option_infos:
			media_list = self.Get_Media_List(option_info)

			if self.media_list_dict != {}:
				media_list.append(self.finish_selection_text)

			option_info = {
				"Media type": option_info,
				"Media": {
					"select": True,
					"list": {}
				}
			}

			if self.File.Exist(self.folders["Audiovisual Media"]["Watch List"]) == False:
				option_info["Media type"]["Media list"] = media_list

				option_info.update(self.Select_Media(option_info))

			if self.File.Exist(self.folders["Audiovisual Media"]["Watch List"]) == True:
				if self.media_title in media_list:
					option_info.update(self.Select_Media(option_info))

					option_info["Media"]["Title"] = self.media_title

				if self.media_title not in media_list:
					option_info["Media"]["Title"] = ""

			self.selected_option = option_info["Media"]["Title"]

			if self.selected_option != self.finish_selection_text and self.selected_option != "":
				self.Watch_Media = Watch_Media(option_info, run_as_module = True, open_media = False)

				option_info.update(self.Watch_Media.media_dictionary)

				self.media_dictionary = self.Watch_Media.media_dictionary

				print()
				print("[" + option_info["Media type"]["Singular"][self.user_language] + ":")

				self.Show_Media_Title(option_info)

				if self.JSON.Language.language_texts["episode, title()"] in self.media_dictionary["Media"]["Item"]["Details"]:
					print()
					print(self.JSON.Language.language_texts["episode, title()"] + ":")
					print(self.media_dictionary["Media"]["Item"]["Details"][self.JSON.Language.language_texts["episode, title()"]] + "]")
					print()

				key = option_info["Media"]["Title"]

				if option_info["Media"]["Title"] not in self.media_list_dict:
					self.i = 2

				if option_info["Media"]["Title"] in self.media_list_dict:
					if option_info["Media"]["Title"] + " (2x)" in list(self.media_list_dict.keys()):
						self.i += 1

					key = option_info["Media"]["Title"] + " (" + str(self.i) + "x)"

				self.media_list_dict[key] = option_info

				self.option_info = option_info
				media_is_defined = True

		if media_is_defined == True:
			return self.option_info

	def Show_Media_List(self, media_title = None):
		number = 1
		for media_list_item in self.media_list_dict:
			text = str(number)

			if media_list_item == media_title:
				text += " (" + self.language_texts["watching, title()"] + ")"

			if media_title != None and self.i > number and media_list_item != media_title:
				text += " (" + self.language_texts["watched, title()"] + ")"

			text += ": " + media_list_item

			print(text)

			number += 1

	def Start_Watching_Media(self, option_info):
		self.Watch_Media = Watch_Media(option_info)
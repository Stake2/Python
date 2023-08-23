# Show_Story_Information.py

from Stories.Stories import Stories as Stories

class Show_Story_Information(Stories):
	def __init__(self, stories_list = None):
		super().__init__()

		if stories_list == None:
			stories_list = self.stories["List"]

		for story in stories_list:
			story = self.stories[story]

			print()
			print(self.large_bar)
			print()

			print(self.language_texts["story_title"] + ":")

			# Show language titles
			for language in self.languages["small"]:
				translated_language = self.languages["full_translated"][language][self.user_language]

				print("\t" + translated_language + ":")
				print("\t" + story["Information"]["Titles"][language])
				print()

			# Show information items
			i = 0
			for information_item in self.language_texts["information_items, type: list"]:
				english_information_item = self.texts["information_items, type: list"]["en"][i]

				if information_item != self.JSON.Language.language_texts["title, title()"]:
					print(information_item + ":")

					if information_item != self.JSON.Language.language_texts["synopsis, title()"]:
						language_information_item = story["Information"][english_information_item]

						if self.user_language in language_information_item:
							language_information_item = language_information_item[self.user_language]

						print("\t" + language_information_item)

					if information_item == self.JSON.Language.language_texts["synopsis, title()"]:
						for line in story["Information"][english_information_item][self.user_language].splitlines():
							print("\t" + line)

					print()

				i += 1

			print(self.Folder.language_texts["folder, title()"] + ":")
			print("\t" + story["folders"]["root"])
			print()

			print(self.JSON.Language.language_texts["website_link"] + ":")
			print("\t" + story["Information"]["Website"]["link"])
			print()

			print("Wattpad:")

			for key in story["Information"]["Wattpad"]:
				print("\t" + self.language_texts[key.lower() + ", title()"] + ":")

				for language in story["Information"]["Wattpad"][key]:
					translated_language = self.languages["full_translated"][language][self.user_language]

					item = story["Information"]["Wattpad"][key][language]

					print("\t\t" + translated_language + ":")
					print("\t\t" + item)

					if language != list(story["Information"]["Wattpad"][key].keys())[-1]:
						print()

				if key != list(story["Information"]["Wattpad"].keys())[-1]:
					print()

		print()
		print(self.large_bar)
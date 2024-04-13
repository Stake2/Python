# Show_Story_Information.py

from Stories.Stories import Stories as Stories

class Show_Story_Information(Stories):
	def __init__(self, stories_list = None):
		super().__init__()

		self.stories_list = stories_list

		self.Show_Information()

	def Show_Information(self):
		if self.stories_list == None:
			# Select the story
			self.story = self.Select_Story()

			self.stories_list = [
				self.story["Title"]
			]

		for story in self.stories_list:
			story = self.stories[story]

			print()
			print(self.separators["5"])
			print()

			print(self.language_texts["story_title"] + ":")

			# Show language titles
			for language in self.languages["small"]:
				translated_language = self.languages["full_translated"][language][self.user_language]

				print("\t" + translated_language + ":")
				print("\t" + story["Titles"][language])
				print()

			# Show information items
			i = 0
			for information_item in self.language_texts["information_items, type: list"]:
				english_information_item = self.texts["information_items, type: list"]["en"][i]

				if information_item != self.Language.language_texts["title, title()"]:
					print(information_item + ":")

					if information_item != self.Language.language_texts["synopsis, title()"]:
						language_information_item = story["Information"][english_information_item]

						if self.user_language in language_information_item:
							language_information_item = language_information_item[self.user_language]

						if type(language_information_item) != dict:
							print("\t" + language_information_item)

						if type(language_information_item) == dict:
							for item in language_information_item.values():
								if (
									type(item) == dict and
									self.user_language in item
								):
									item = item[self.user_language]

								if (
									information_item != "Status" or
									information_item == "Status" and
									type(item) != int
								):
									print("\t" + str(item))

					if information_item == self.Language.language_texts["synopsis, title()"]:
						for line in story["Information"][english_information_item][self.user_language].splitlines():
							print("\t" + line)

					print()

				i += 1

			print(self.Folder.language_texts["folder, title()"] + ":")
			print("\t" + story["Folders"]["root"])
			print()

			print(self.Language.language_texts["website_image_folder"] + ":")
			print("\t" + story["Folders"]["Covers"]["Websites"]["root"])
			print()

			print(self.Language.language_texts["website_link"] + ":")
			print("\t" + story["Information"]["Website"]["Link"])
			print()

			print("Wattpad:")

			for language in story["Information"]["Wattpad"]:
				translated_language = self.languages["full_translated"][language][self.user_language]

				item = story["Information"]["Wattpad"][language]

				print("\t" + translated_language + ":")
				print("\t" + item["Link"])

				if language != list(story["Information"]["Wattpad"].keys())[-1]:
					print()

		print()
		print(self.separators["5"])
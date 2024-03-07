# Show_Story_Information.py

from Stories.Stories import Stories as Stories

class Show_Story_Information(Stories):
	def __init__(self, stories_list = None):
		super().__init__()

		self.stories_list = stories_list

		self.Show_Information()
		self.Move_Chapter_Covers()

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
			print(self.large_bar)
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

				if information_item != self.JSON.Language.language_texts["title, title()"]:
					print(information_item + ":")

					if information_item != self.JSON.Language.language_texts["synopsis, title()"]:
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

					if information_item == self.JSON.Language.language_texts["synopsis, title()"]:
						for line in story["Information"][english_information_item][self.user_language].splitlines():
							print("\t" + line)

					print()

				i += 1

			print(self.Folder.language_texts["folder, title()"] + ":")
			print("\t" + story["Folders"]["root"])
			print()

			print(self.language_texts["website_image_folder"] + ":")
			print("\t" + story["Folders"]["Covers"]["Websites"]["root"])
			print()

			print(self.JSON.Language.language_texts["website_link"] + ":")
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
		print(self.large_bar)

	def Move_Chapter_Covers(self):
		extensions = [
			"png",
			"jpg",
			"jpeg"
		]

		chapter_number = 1
		for chapter in self.story["Information"]["Chapters"]["Titles"][self.user_language]:
			chapter = {
				"Number": chapter_number,
				"Number with zeroes": str(self.Text.Add_Leading_Zeroes(chapter_number)),
				"Title": chapter,
				"Folders": {},
				"Files": {}
			}

			chapter["Folders"]["Chapters"] = {
				"root": self.story["Folders"]["Covers"]["Websites"]["Chapters"]["root"] + chapter["Number with zeroes"] + "/"
			}

			folder_name = self.Cover_Folder_Name(chapter_number)

			print()
			print(self.large_bar)
			print()
			print(str(chapter_number) + ":")
			print()

			for language in self.languages["small"]:
				full_language = self.languages["full"][language]

				chapter["Folders"][language] = {
					"root": self.story["Folders"]["Covers"]["Websites"][language][folder_name]["root"]
				}

				for extension in extensions:
					old_file = chapter["Folders"][language]["root"] + chapter["Number with zeroes"] + "." + extension

					if self.File.Exist(old_file) == True:
						new_file = chapter["Folders"]["Chapters"]["root"] + full_language + "." + extension

						self.File.Move(old_file, new_file)

						chapter["Files"][language] = new_file

			self.JSON.Show(chapter)

			chapter_number += 1
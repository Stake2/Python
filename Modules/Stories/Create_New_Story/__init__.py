# Create_New_Story.py

from Stories.Stories import Stories as Stories

class Create_New_Story(Stories):
	def __init__(self):
		super().__init__(select_story = False)

		self.Type_Story_Information()
		self.Create_Story_Folder_And_Files()

		super().__init__(select_story = False)

		self.Show_Story_Information([self.story["title"]])

		self.Input.Type(self.JSON.Language.language_texts["press_enter_when_you_finish_reading_the_info_summary"])

	def Type_Story_Information(self):
		self.story_titles = {}

		i = 0
		for information_item in self.language_texts["information_items, type: list"]:
			english_information_item = self.texts["information_items, type: list"]["en"][i]

			if information_item == self.JSON.Language.language_texts["title, title()"]:
				for language in self.languages["small"]:
					translated_language = self.languages["full_translated"][language][self.user_language]

					type_text = self.language_texts["story_title_in_{}"].format(translated_language)

					story_title = self.Input.Type(type_text, next_line = True)

					self.story_titles[language] = story_title

				self.stories[self.story_titles["en"]] = {}
				self.stories[self.story_titles["en"]]["title"] = self.story_titles["en"]

				if "folders" not in self.stories[self.story_titles["en"]]:
					self.stories[self.story_titles["en"]]["folders"] = {}

				if "Information" not in self.stories[self.story_titles["en"]]:
					self.stories[self.story_titles["en"]]["Information"] = {}

				if "Titles" not in self.stories[self.story_titles["en"]]["Information"]:
					self.stories[self.story_titles["en"]]["Information"]["Titles"] = {}

				for language in self.story_titles:
					self.stories[self.story_titles["en"]]["Information"]["Titles"][language] = self.story_titles[language]

			if information_item == self.language_texts["synopsis, title()"]:
				self.stories[self.story_titles["en"]]["Information"]["Wattpad"] = {
					"ID": {},
				}

				for language in self.languages["small"]:
					self.stories[self.story_titles["en"]]["Information"]["Wattpad"]["ID"][language] = "None"

				synopses = {}

				self.stories[self.story_titles["en"]]["Information"][english_information_item] = {}

				for language in self.languages["small"]:
					full_language = self.languages["full"][language]
					translated_language = self.languages["full_translated"][language][self.user_language]

					type_text = self.language_texts["story_synopsis_in_{}"].format(translated_language)

					synopsis = self.Input.Lines(type_text, line_options = {"next_line": True})["string"]

					self.stories[self.story_titles["en"]]["Information"][english_information_item][full_language] = synopsis

				self.stories[self.story_titles["en"]]["Information"]["Website"] = self.links["Stake2 Website"] + self.story_titles["en"] + "/"

			if information_item not in [self.JSON.Language.language_texts["title, title()"], self.language_texts["synopsis, title()"]]:
				if information_item in [self.language_texts["creation_date"], self.language_texts["author, title()"]]:
					information = self.Input.Type(information_item, next_line = True)

					if information != "" and information_item == self.language_texts["author, title()"]:
						information = self.author + "\n" + information

					if information == "":
						information = self.default_information_items[information_item]

				if information_item == self.language_texts["status, title()"]:
					show_text = self.language_texts["writing_statuses"]
					select_text = self.language_texts["select_a_writing_status"]

					information = self.Input.Select(self.language_texts["status, type: list"], show_text = show_text, select_text = select_text)["option"]

				self.stories[self.story_titles["en"]]["Information"][english_information_item] = information

			i += 1

		self.stories[self.story_titles["en"]]["Information"] = dict(sorted(self.stories[self.story_titles["en"]]["Information"].items(), key = str.lower))

	def Create_Story_Folder_And_Files(self):
		# Create root folder
		self.stories[self.story_titles["en"]]["folders"] = {}
		self.stories[self.story_titles["en"]]["folders"]["root"] = self.stories["folders"]["root"] + self.story_titles["en"] + "/"
		self.Folder.Create(self.stories[self.story_titles["en"]]["folders"]["root"])

		# Create subfolders
		for folder_name in self.texts["folder_names, type: list"]:
			self.stories[self.story_titles["en"]]["folders"][folder_name] = {
				"root": self.stories[self.story_titles["en"]]["folders"]["root"] + folder_name + "/"
			}

			self.Folder.Create(self.stories[self.story_titles["en"]]["folders"][folder_name]["root"])

			# Create sub-sub-folders
			if folder_name in self.texts["sub_file_names, type: dict"]:
				for sub_folder_name in self.texts["sub_file_names, type: dict"][folder_name]:
					self.stories[self.story_titles["en"]]["folders"][folder_name][sub_folder_name] = self.stories[self.story_titles["en"]]["folders"][folder_name]["root"] + sub_folder_name + "/"

					self.Folder.Create(self.stories[self.story_titles["en"]]["folders"][folder_name][sub_folder_name])

		self.stories[self.story_titles["en"]]["Information"]["Chapter status"] = self.File.Dictionary(self.stories["folders"]["Database"]["Chapter status template"], next_line = True)

		# Write to information files
		for key in self.texts["file_names, type: list"]:
			file_name = key

			text = ""

			if key in self.stories[self.story_titles["en"]]["Information"]:
				text = self.stories[self.story_titles["en"]]["Information"][key]

			if key in ["Titles", "Wattpad"]:
				text = self.JSON.From_Python(text)
				file_name += ".json"

			if key not in ["Chapter status", "Titles", "Wattpad"]:
				file_name += ".txt"

			if key == "Chapter status":
				text = self.Text.From_Dictionary(text)

			if key != "Author" or key == "Author" and self.stories[self.story_titles["en"]]["Information"]["Author"] != self.author:
				self.stories[self.story_titles["en"]]["folders"]["Information"][key] = self.stories[self.story_titles["en"]]["folders"]["Information"]["root"] + file_name

				self.File.Create(self.stories[self.story_titles["en"]]["folders"]["Information"][key])
				self.File.Edit(self.stories[self.story_titles["en"]]["folders"]["Information"][key], text, "w")

		# Create Synopsis folder
		self.stories[self.story_titles["en"]]["folders"]["Information"]["Synopsis"] = {
			"root": self.stories[self.story_titles["en"]]["folders"]["Information"]["root"] + "Synopsis/",
		}

		# Create Chapters subfolders and Synopsis files
		for language in self.languages["small"]:
			full_language = self.languages["full"][language]

			# Create Chapters subfolder
			self.stories[self.story_titles["en"]]["folders"]["Chapters"][full_language] = self.stories[self.story_titles["en"]]["folders"]["Chapters"]["root"] + full_language + "/"
			self.Folder.Create(self.stories[self.story_titles["en"]]["folders"]["Chapters"][full_language])

			# Create and write to chapters number file
			self.stories[self.story_titles["en"]]["folders"]["Chapters"][self.language_texts["number, title()"]] = self.stories[self.story_titles["en"]]["folders"]["Chapters"]["root"] + self.language_texts["number, title()"] + ".txt"
			self.File.Create(self.stories[self.story_titles["en"]]["folders"]["Chapters"][self.language_texts["number, title()"]])

			self.File.Edit(self.stories[self.story_titles["en"]]["folders"]["Chapters"][self.language_texts["number, title()"]], "0", "w")

			# Create Synopsis file and write synopsis to it
			self.stories[self.story_titles["en"]]["folders"]["Information"]["Synopsis"][full_language] = self.stories[self.story_titles["en"]]["folders"]["Information"]["Synopsis"]["root"] + full_language + ".txt"

			text_to_write = self.stories[self.story_titles["en"]]["Information"]["Synopsis"][full_language]
			self.File.Edit(self.stories[self.story_titles["en"]]["folders"]["Information"]["Synopsis"][full_language], text_to_write, "w")

		# Create Obsidian's Vaults folder
		self.stories[self.story_titles["en"]]["folders"]["Obsidian's Vaults"] = self.folders["mega"]["obsidian_s_vaults"]["creativity"]["literature"]["stories"]["root"] + self.story_titles["en"] + "/"
		self.Folder.Create(self.stories[self.story_titles["en"]]["folders"]["Obsidian's Vaults"])

		self.story = self.stories[self.story_titles["en"]]
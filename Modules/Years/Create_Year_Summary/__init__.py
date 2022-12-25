# Create_Year_Summary.py

from Years.Years import Years as Years

class Create_Year_Summary(Years):
	def __init__(self):
		super().__init__(select_year = False)

		self.Select_The_Year()

		if self.year != None:
			self.Check_Day()

			if self.today_is_summary_day == True:
				self.Define_Language_Folders_And_Files()
				self.Define_Year_Data()
				self.Define_Summary_Text()
				self.Write_Summary_To_Files()
				self.Show_Summary_Information()

	def Select_The_Year(self):
		years_list = self.years_list.copy()

		for year in self.years:
			english_files = self.years[year]["folders"][self.full_languages["en"]]

			if self.texts["summary, title()"]["en"] in english_files and \
			self.File.Contents(english_files[self.texts["summary, title()"]["en"]])["lines"] != []:
				years_list.remove(year)

		select_text = self.language_texts["select_a_year_to_create_its_summary"]

		if years_list == []:
			print()
			print("--------------------")
			print()
			print(self.language_texts["you_already_created_the_summary_for_this_year"] + ":")
			print(self.date["year"])

		self.year = None

		if years_list != []:
			self.year = self.Select_Year(years_list, select_text)

	def Check_Day(self):
		self.today_is_summary_day = False

		if self.date["day"] == self.summary_date["day"] and self.date["month"] == self.summary_date["month"]:
			self.today_is_summary_day = True

		if self.today_is_summary_day == False:
			day_month = self.language_texts["{} {} {}"].format(self.summary_date["day"], self.summary_date["month_name"], self.date["year"])
			today = self.language_texts["{} {} {}"].format(self.date["day"], self.date["month_name"], self.date["year"])

			print()
			print("--------------------")
			print()
			print(self.language_texts["today_is_not_the_{}_run_this_program_again_when_it_is_today_is"].format(day_month) + ":")
			print(today)
			print()
			print("--------------------")

	def Define_Language_Folders_And_Files(self):
		self.language_folders = {}

		for language in self.small_languages:
			full_language = self.full_languages[language]

			self.language_folders[language] = self.year["folders"][full_language]["root"]

		self.language_files = {}

		for language in self.small_languages:
			full_language = self.full_languages[language]

			summary_text = self.texts["summary, title()"][language]

			self.language_files[language] = self.language_folders[language] + summary_text + ".txt"
			self.File.Create(self.language_files[language])

			self.year["folders"][full_language][summary_text] = self.language_files[language]

	def Define_Year_Data(self):
		self.File.Edit(self.year["folders"][self.language_texts["edited_in, en - pt"]], self.Date.Now()["strftime"], "w")

		self.year_data = {
			"header": {
				"author, title()": self.author,
				"created_in": self.File.Contents(self.year["folders"][self.language_texts["created_in, en - pt"]])["lines"][0],
				"edited_in": self.File.Contents(self.year["folders"][self.language_texts["edited_in, en - pt"]])["lines"][0],
			}
		}

		self.year_numbers = {}

		from Tasks.Tasks import Tasks as Tasks
		from GamePlayer.GamePlayer import GamePlayer as GamePlayer
		from Friends.Friends import Friends as Friends

		# GamePlayer instantiate
		self.Tasks = Tasks()
		self.GamePlayer = GamePlayer()

		self.year_numbers["things_done_in_{year}"] = 0

		# Tasks data
		self.tasks = self.Language.JSON_To_Python(self.Tasks.folders["Task History"][str(self.date["year"])]["Tasks.json"])

		# Watch History data
		self.watch_history_data = self.Language.JSON_To_Python(self.episodes_file)

		self.year_numbers["productive_things"] = self.File.Contents(self.Tasks.folders["Task History"][str(self.date["year"])]["Number"])["lines"][0]
		self.year_numbers["watched_things"] = self.watch_history_data["watched_number"]
		self.year_numbers["media_comments"] = self.watch_history_data["comment_number"]
		self.year_numbers["game_matches_played"] = self.GamePlayer.current_year_played_number
		self.year_numbers["known_people"] = Friends(select_social_network = False).current_year_friends_number

		for data in self.year_numbers:
			self.year_numbers["things_done_in_{year}"] += int(self.year_numbers[data])

		del self.watch_history_data["watched_number"], self.watch_history_data["comment_number"]

		self.year_data["detailed"] = {}
		self.year_data["detailed"]["productive_things"] = {}

		for language in self.small_languages:
			self.year_data["detailed"]["productive_things"][language] = self.tasks[language]

			while len(self.year_data["detailed"]["productive_things"][language]) != 10:
				self.year_data["detailed"]["productive_things"][language].pop(0)

		self.itens_per_type = 5

		self.year_data["detailed"]["watched_things"] = self.watch_history_data

		for media_type in self.year_data["detailed"]["watched_things"]:
			media_type_episodes = self.year_data["detailed"]["watched_things"][media_type]

			while len(media_type_episodes) > self.itens_per_type:
				media_type_episodes.pop(0)

		self.texts["plural_media_types, type: list"] = self.Language.JSON_To_Python(self.apps_folders["app_text_files"]["root"] + "Watch_History/Texts.json")["plural_media_types, type: list"]

		self.plural_media_types = self.texts["plural_media_types, type: list"]

		self.year_data["detailed"]["game_matches_played"] = {}

		for language in self.small_languages:
			self.year_data["detailed"]["game_matches_played"][language] = self.GamePlayer.current_year_played_time_language[language]

			while len(self.year_data["detailed"]["game_matches_played"][language]) != self.itens_per_type:
				self.year_data["detailed"]["game_matches_played"][language].pop(0)

	def Define_Summary_Text(self):
		self.summary_text = {}

		i = 0
		for language in self.small_languages:
			self.summary_text[language] = ""

			self.summary_texts = self.texts["year_summary_texts, type: list"][language]

			# Header texts
			for header_text in self.year_data["header"]:
				self.summary_text[language] += self.texts[header_text][language] + ": " + self.year_data["header"][header_text]
				self.summary_text[language] += "\n"

			self.summary_text[language] += "\n" + "-----" + "\n\n"

			# Top numbers text
			for summary_text in self.year_numbers:
				summary_text_backup = summary_text

				summary_text = self.language_texts[summary_text]

				if "{year}" in summary_text:
					summary_text = summary_text.replace("{year}", self.year["number"])

				summary_text += ": "

				if summary_text_backup in self.year_numbers:
					summary_text += str(self.year_numbers[summary_text_backup])

				if self.year["number"] in summary_text:
					summary_text += " (" + self.texts["the_sum_of_numbers_below"][language] + ")"

				if summary_text != self.summary_texts[-1]:
					summary_text += "\n"

				self.summary_text[language] += summary_text

			self.summary_text[language] += "\n" + "-----" + "\n\n"

			self.year_summary_detailed_texts = self.texts["year_summary_detailed_texts, type: list"][language]

			# Detailed texts
			for summary_text in self.year_data["detailed"]:
				self.summary_text[language] += self.language_texts[summary_text]

				if summary_text not in ["productive_things", "watched_things"]:
					number = self.itens_per_type

				if summary_text == "productive_things":
					number = 10

				if summary_text != "watched_things":
					self.summary_text[language] += " (" + self.texts["last, feminine"][language] + " " + self.Date.texts["number_names, type: list"][language][number] + ")"

				self.summary_text[language] += ":\n"

				if summary_text != "watched_things":
					i = 1
					for data in self.year_data["detailed"][summary_text][language]:
						self.summary_text[language] += str(i) + ". " + data

						if data != self.year_data["detailed"][summary_text][language][-1]:
							self.summary_text[language] += "\n"

						i += 1

				if summary_text == "watched_things":
					c = 0
					for media_type in self.year_data["detailed"][summary_text]:
						media_type_episodes = self.year_data["detailed"][summary_text][media_type]

						language_media_type = self.plural_media_types[language][c]

						number_text = " (" + self.texts["last"][language] + " " + self.Date.texts["number_names, type: list"][language][len(media_type_episodes)]

						if media_type != "Movies":
							number_text += " " + self.texts["episodes"][language]

						number_text += ")"

						self.summary_text[language] += "\t" + language_media_type + number_text + ":\n"

						i = 1
						for data in media_type_episodes:
							self.summary_text[language] += "\t\t" + str(i) + ". " + data

							if data != media_type_episodes[-1]:
								self.summary_text[language] += "\n"

							i += 1

						if media_type != list(self.year_data["detailed"][summary_text].keys())[-1]:
							self.summary_text[language] += "\n\n"

						c += 1

				if summary_text != "game_matches_played":
					self.summary_text[language] += "\n\n"

			i += 1

	def Write_Summary_To_Files(self):
		for language in self.small_languages:
			text_to_write = self.summary_text[language]

			self.File.Edit(self.language_files[language], text_to_write, "w")

	def Show_Summary_Information(self):
		print("--------------------")
		print()
		print(self.language_texts["the_summary_of_this_year_was_created"] + ":")
		print(self.year["number"])
		print()

		print(self.language_texts["summary_in"] + " " + self.full_languages[self.user_language] + ":")
		print("____________________")
		print(self.summary_text[self.user_language])
		print("____________________")

		self.File.Open(self.language_files[self.user_language])

		print()
		print(self.language_texts["the_program_has_finished_the_creation_of_the_year_summary_for"] + " " + self.year["number"] + ".")
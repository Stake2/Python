# Create_Year_Summary.py

from Years.Years import Years as Years

class Create_Year_Summary(Years):
	def __init__(self):
		super().__init__(select_year = False)

		self.Define_Year()

		if self.year != None:
			self.Check_Day()

			if self.today_is_summary_day == True:
				self.Define_Language_Folders_And_Files()
				self.Define_Year_Data()
				self.Define_Summary_Text()
				self.Write_Summary_To_Files()
				self.Show_Summary_Information()

	def Define_Year(self):
		years_list = self.years["List"].copy()

		for year in self.years:
			english_files = self.years[year]["folders"][self.languages["full"]["en"]]

			if self.texts["summary, title()"]["en"] in english_files and \
			self.File.Contents(english_files[self.texts["summary, title()"]["en"]])["lines"] != []:
				years_list.remove(year)

		if years_list == []:
			print()
			print("--------------------")
			print()
			print(self.language_texts["you_already_created_the_summary_for_this_year"] + ":")
			print(self.date["Units"]["Year"])
			print()
			print("--------------------")

		self.year = None

		if years_list != []:
			self.year = self.years[str(years_list[0])]

	def Check_Day(self):
		self.today_is_summary_day = False

		if self.date["Units"]["Day"] == self.summary_date["Day"] and self.date["Units"]["Month"] == self.summary_date["Month"]:
			self.today_is_summary_day = True

		if self.today_is_summary_day == False:
			day_month = self.language_texts["{} {} {}"].format(self.summary_date["Day"], self.summary_date["Timezone"]["Texts"]["Month name"], self.date["Units"]["Year"])
			today = self.language_texts["{} {} {}"].format(self.date["Units"]["Day"], self.date["Timezone"]["Texts"]["Month name"], self.date["Units"]["Year"])

			print()
			print("--------------------")
			print()
			print(self.language_texts["today_is_not_the_{}_run_this_program_again_when_it_is_today_is"].format(day_month) + ":")
			print(today)
			print()
			print("--------------------")

	def Define_Language_Folders_And_Files(self):
		self.language_folders = {}

		for language in self.languages["small"]:
			full_language = self.languages["full"][language]

			self.language_folders[language] = self.year["folders"][full_language]["root"]

		self.language_files = {}

		for language in self.languages["small"]:
			full_language = self.languages["full"][language]

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
		self.tasks = self.JSON.To_Python(self.Tasks.folders["Task History"][str(self.date["Units"]["Year"])]["Tasks.json"])
		self.task_times = self.File.Contents(self.Tasks.folders["Task History"][str(self.date["Units"]["Year"])]["Times"])["lines"]

		# Watch History data
		self.watch_history_data = self.JSON.To_Python(self.episodes_file)

		self.year_numbers["productive_things"] = self.File.Contents(self.Tasks.folders["Task History"][str(self.date["Units"]["Year"])]["Number"])["lines"][0]
		self.year_numbers["watched_things"] = self.watch_history_data["Number"]
		self.year_numbers["media_comments"] = self.watch_history_data["Comments"]
		self.year_numbers["game_matches_played"] = self.GamePlayer.current_year_played_number
		self.year_numbers["known_people"] = Friends(self.switches, select_social_network = False).current_year_friends_number

		for data in self.year_numbers:
			self.year_numbers["things_done_in_{year}"] += int(self.year_numbers[data])

		self.year_data["detailed"] = {}
		self.year_data["detailed"]["productive_things"] = {}

		for language in self.languages["small"]:
			self.year_data["detailed"]["productive_things"][language] = self.tasks[language]

			while len(self.year_data["detailed"]["productive_things"][language]) != 10:
				self.year_data["detailed"]["productive_things"][language].pop(0)

		self.itens_per_type = 5

		self.year_data["detailed"]["watched_things"] = self.watch_history_data

		self.plural_media_types = self.JSON.To_Python(self.folders["apps"]["module_files"]["root"] + "Watch_History/Texts.json")["plural_media_types, type: list"]

		for key in self.year_data["detailed"]["watched_things"]:
			if key in self.plural_media_types["en"]:
				media_type_episodes = self.year_data["detailed"]["watched_things"][key]["Episodes"]
				media_type_times = self.year_data["detailed"]["watched_things"][key]["Times"]

				while len(media_type_episodes) > self.itens_per_type:
					media_type_episodes.pop(0)
					media_type_times.pop(0)

		self.year_data["detailed"]["game_matches_played"] = {}

		for language in self.languages["small"]:
			self.year_data["detailed"]["game_matches_played"][language] = self.GamePlayer.current_year_played_time_language[language]

			while len(self.year_data["detailed"]["game_matches_played"][language]) != self.itens_per_type:
				self.year_data["detailed"]["game_matches_played"][language].pop(0)

	def Define_Summary_Text(self):
		self.summary_text = {}

		i = 0
		for language in self.languages["small"]:
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

				summary_text = self.texts[summary_text][language]

				if "{year}" in summary_text:
					summary_text = summary_text.replace("{year}", self.year["Number"])

				summary_text += ": "

				if summary_text_backup in self.year_numbers:
					summary_text += str(self.year_numbers[summary_text_backup])

				if self.year["Number"] in summary_text:
					summary_text += " (" + self.texts["the_sum_of_numbers_below"][language] + ")"

				if summary_text != self.summary_texts[-1]:
					summary_text += "\n"

				self.summary_text[language] += summary_text

			self.summary_text[language] += "\n" + "-----" + "\n\n"

			self.year_summary_detailed_texts = self.texts["year_summary_detailed_texts, type: list"][language]

			# Detailed texts
			for summary_text in self.year_data["detailed"]:
				self.summary_text[language] += self.texts[summary_text][language]

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
						self.summary_text[language] += "\t" + str(i) + ". " + data

						if summary_text == "productive_things":
							self.summary_text[language] += " (" + self.task_times[i] + ")"

						if data != self.year_data["detailed"][summary_text][language][-1]:
							self.summary_text[language] += "\n"

						i += 1

				if summary_text == "watched_things":
					c = 0
					for media_type in self.plural_media_types["en"]:
						media_type_episodes = self.year_data["detailed"][summary_text][media_type]["Episodes"]

						language_media_type = self.plural_media_types[language][c]

						number_text = " (" + self.texts["last"][language] + " " + self.Date.texts["number_names, type: list"][language][len(media_type_episodes)]

						if media_type != "Movies":
							number_text += " " + self.texts["episodes"][language]

						number_text += ")"

						self.summary_text[language] += "\t" + language_media_type + number_text + ":\n"

						i = 1
						for data in media_type_episodes:
							self.summary_text[language] += "\t\t" + str(i) + ". " + data

							self.summary_text[language] += " (" + self.year_data["detailed"][summary_text][media_type]["Times"][i - 1] + ")"

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
		for language in self.languages["small"]:
			text_to_write = self.summary_text[language]

			self.File.Edit(self.language_files[language], text_to_write, "w")

	def Show_Summary_Information(self):
		print("--------------------")
		print()
		print(self.language_texts["the_summary_of_this_year_was_created"] + ":")
		print(self.year["Number"])
		print()

		print(self.language_texts["summary_in"] + " " + self.languages["full"][self.user_language] + ":")
		print("____________________")
		print(self.summary_text[self.user_language])
		print("____________________")

		self.File.Open(self.language_files[self.user_language])

		print()
		print(self.language_texts["the_program_has_finished_the_creation_of_the_year_summary_for"] + " " + self.year["Number"] + ".")
# Show_Year_Information.py

from Years.Years import Years as Years

class Show_Year_Information(Years):
	def __init__(self):
		super().__init__()

		self.Select_The_Year()
		self.Show_Information()

	def Select_The_Year(self):
		select_text = self.language_texts["select_a_year_to_show_its_information"]

		self.year = self.Select_Year(select_text = select_text)

	def Show_File_Text(self, file, tab):
		if self.File.Contents(file)["lines"] != []:
			for line in self.File.Contents(file)["lines"]:
				print(tab + "| " + line)

		if self.File.Contents(file)["lines"] == []:
			print(tab + "| [" + self.JSON.Language.language_texts["empty, title()"] + "]")

	def Show_Information(self):
		print("-----")
		print()

		print(self.JSON.Language.language_texts["{}_information"].format(self.year["Number"]) + ":")
		print()
		print("-----")
		print()
		print("________________________")
		print()

		for key in self.year["Files"]:
			text = key

			if key in self.languages["full"]:
				text = self.languages["full"][key]

			if (
				type(self.year["Files"][key]) == str and
				self.File.Exist(self.year["Files"][key]) == True
			):
				file = self.year["Files"][key]

				print("____" + text + self.language_texts["_(file)"] + ":")

				self.Show_File_Text(file, "\t")

				print("____]")

			sub_dictionary = None

			if type(self.year["Files"][key]) == dict:
				sub_dictionary = self.year["Files"][key]

				print("____" + text + self.language_texts["_(primary_folder)"] + ":")

				for sub_key in self.year["Files"][key]:
					sub_dictionary = self.year["Files"][key][sub_key]

					text = sub_key

					if sub_key in self.languages["full"]:
						text = self.languages["full"][sub_key]

					if sub_key in self.years["Names"]["Root"]["Files"]["Dictionary"]:
						text = self.years["Names"]["Root"]["Files"]["Dictionary"][sub_key][self.user_language]

					if (
						type(sub_dictionary) == str and
						self.File.Exist(sub_dictionary) == True
					):
						file = sub_dictionary

						print("________" + text + self.language_texts["_(file)"] + ":")

						self.Show_File_Text(file, "\t\t")

						if sub_key != list(self.year["Files"][key].keys())[-1]:
							print()

					if (
						type(sub_dictionary) == dict and
						len(sub_dictionary.keys()) != 1
					):
						print("________" + text + self.language_texts["_(secondary_folder)"] + ":")

						for sub_sub_key in sub_dictionary:
							file = sub_dictionary[sub_sub_key]

							text = sub_sub_key

							if sub_sub_key in self.languages["full"]:
								text = self.languages["full"][sub_sub_key]

							for item in ["Root", "Language", "Christmas", "New Year"]:
								if sub_sub_key in self.years["Names"][item]["Files"]["Dictionary"]:
									text = self.years["Names"][item]["Files"]["Dictionary"][sub_sub_key][self.user_language]

							if type(file) == str:
								if self.File.Exist(file) == True:
									print("            " + text + self.language_texts["_(file)"] + ":")

									self.Show_File_Text(file, "\t\t")

									if sub_sub_key != list(sub_dictionary.keys())[-1]:
										print()

							if type(file) == dict:
								dict_ = file

								for sub_sub_sub_key in dict_:
									file = dict_[sub_sub_sub_key]

									text = sub_sub_sub_key

									if sub_sub_sub_key in self.languages["full"]:
										text = self.languages["full"][sub_sub_sub_key]

									for item in ["Root", "Language", "Christmas", "New Year"]:
										local_dictionary = self.years["Names"][item]["Files"]["Dictionary"]

										if sub_sub_sub_key in local_dictionary:
											text = local_dictionary[sub_sub_sub_key][self.user_language]

									for item in ["Planning", "Merry Christmas"]:
										local_dictionary = self.years["Names"]["Additional items"]["Christmas"][item]["Files"]["Dictionary"]

										if sub_sub_sub_key in local_dictionary:
											text = local_dictionary[sub_sub_sub_key][self.user_language]

									print("            " + text + self.language_texts["_(file)"] + ":")

									self.Show_File_Text(file, "\t\t")

									#if sub_sub_sub_key != list(dict_.keys())[-1]:
									print()

					if (
						sub_key != list(self.year["Files"][key].keys())[-1] and
						sub_dictionary == None or
						sub_dictionary != None and
						type(sub_dictionary) != str and
						len(sub_dictionary.keys()) != 1
					):
						print()

			if (
				key != list(self.year["Files"].keys())[-1] or
				sub_dictionary != None and
				type(sub_dictionary) != str and
				len(sub_dictionary.keys()) != 1
			):
				print()

			if (
				self.year["Files"][key] != {} and
				key != list(self.year["Files"].keys())[-1]
			):
				print("________________________")

		print()
		print("-----")
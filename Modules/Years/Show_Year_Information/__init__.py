# Show_Year_Information.py

from Years.Years import Years as Years

import os

class Show_Year_Information(Years):
	def __init__(self):
		super().__init__(select_year = False)

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
			print(tab + "| [" + self.language_texts["empty, title()"] + "]")

	def Show_Information(self):
		print("-----")
		print()

		print(self.language_texts["{}_information"].format(self.year["Number"]) + ":")
		print()
		print("-----")
		print()
		print("________________________")

		for key in self.year["Folders"]:
			if type(self.year["Folders"][key]) == str and os.path.isfile(self.year["Folders"][key]) == True:
				file = self.year["Folders"][key]

				print("____" + key + self.language_texts["_(file)"] + ":")

				self.Show_File_Text(file, "\t")

				print("____]")

			sub_dictionary = None

			if type(self.year["Folders"][key]) == dict:
				sub_dictionary = self.year["Folders"][key]

				print("____" + key + self.language_texts["_(primary_folder)"] + ":")

				for sub_key in self.year["Folders"][key]:
					sub_dictionary = self.year["Folders"][key][sub_key]

					if type(sub_dictionary) == str and os.path.isfile(sub_dictionary) == True:
						file = sub_dictionary

						print("________" + sub_key + self.language_texts["_(file)"] + ":")
						print("____________[")

						self.Show_File_Text(file, "\t\t")

						print("____________]")

					if type(sub_dictionary) == dict and len(sub_dictionary.keys()) != 1:
						print("________" + sub_key + self.language_texts["_(secondary_folder)"] + ":")

						for sub_sub_key in sub_dictionary:
							file = sub_dictionary[sub_sub_key]

							if os.path.isfile(file) == True:
								print("____________" + sub_sub_key + self.language_texts["_(file)"] + ":")
								print("________________[")

								self.Show_File_Text(file, "\t\t\t")

								print("________________]")

								if sub_sub_key != list(sub_dictionary.keys())[-1]:
									print()

					if sub_key != list(self.year["Folders"][key].keys())[-1] and sub_dictionary == None or sub_dictionary != None and type(sub_dictionary) != str and len(sub_dictionary.keys()) != 1:
						print()

			if key != list(self.year["Folders"].keys())[-1] or sub_dictionary != None and type(sub_dictionary) != str and len(sub_dictionary.keys()) != 1:
				print()

			if self.year["Folders"][key] != {} and key != list(self.year["Folders"].keys())[-1]:
				print("________________________")

		print()
		print("-----")
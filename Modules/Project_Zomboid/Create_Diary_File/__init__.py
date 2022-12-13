# Create_Diary_File.py

from Project_Zomboid.Project_Zomboid import Project_Zomboid as Project_Zomboid

class Create_Diary_File(Project_Zomboid):
	def __init__(self):
		super().__init__()

		self.predefined_values = self.Language.JSON_To_Python(self.predefined_values_file)

		self.Select_City()
		self.Select_Character()
		self.Define_Date_Folders()
		self.Define_Date_Variables()
		self.Write_To_Files()
		self.Open_File()
		self.Show_Information()

	def Select_City(self, first_space = False):
		kentucky_city_names = self.kentucky_city_names

		for city in self.kentucky_city_names:
			if self.kentucky_cities[city]["survivors"] == []:
				kentucky_city_names.remove(city)

		if self.predefined_values["City"] == "":
			show_text = self.language_texts["kentucky_cities"]
			select_text = self.language_texts["select_a_kentucky_city_to_use"]

			self.city = self.Input.Select(self.kentucky_city_names, show_text = show_text, select_text = select_text)["option"]

		self.used_predefined_values = False

		if self.predefined_values["City"] != "":
			self.city = self.predefined_values["City"]

			self.used_predefined_values = True

	def Select_Character(self):
		if self.predefined_values["Character"] == "":
			show_text = self.language_texts["survivors, title()"]
			select_text = self.language_texts["select_a_survivor_from_{}_to_survive_as_it"]

			self.survivor = self.Input.Select(self.kentucky_cities[self.city]["survivors"], show_text = show_text, select_text = select_text)["option"]

		if self.predefined_values["Character"] != "":
			self.survivor = self.predefined_values["Character"]

		self.survivor_folder = self.kentucky_cities[self.city]["folder"] + self.survivor + "/"
		self.Folder.Create(self.survivor_folder)

		self.survivor_database_folder = self.survivor_folder + "Database/"
		self.Folder.Create(self.survivor_database_folder)

		self.survivor_date_files = {}

		for item in ["Year", "Month", "Day", "Survival day"]:
			self.survivor_date_files[item] = self.survivor_database_folder + item + ".txt"

	def Define_Date_Folders(self):
		self.dates = {
			"folders": {},
		}

		for item in self.survivor_date_files:
			self.dates[item] = {}

			self.dates[item] = self.File.Contents(self.survivor_date_files[item])["lines"]

			if self.dates[item] != []:
				self.dates[item] = int(self.dates[item][0])

		for item in self.dates:
			if item not in ["folders", "Day", "Survival Day"]:
				number = self.dates[item]

				if item == "Month":
					number = self.Text.Add_Leading_Zeros(number) + " - " + self.Date.language_texts["month_names, type: list"][int(number)]

				self.dates["folders"][item] = self.survivor_folder

				if item == "Month":
					self.dates["folders"][item] = self.dates["folders"]["Year"]

				self.dates["folders"][item] += str(number) + "/"

	def Define_Date_Variables(self):
		self.dates["Day"] += 1
		self.dates["Survival day"] += 1

		self.file_name_template = "Dia {}, {}, {}"

		self.date = self.Date.From_String(str(self.dates["Day"]) + "/" + str(self.dates["Month"]) + "/" + str(self.dates["Year"]), "%d/%m/%Y")

		self.survival_diary_file_name = self.file_name_template.format(str(self.dates["Survival day"]), self.date["day_name"], self.date["%d-%m-%Y"])

		self.diary_header_template = "Hoje é dia {} de {} de {}, {}." + \
		"\n" + \
		"É {} {}." + \
		"\n\n"

		self.day_number_name = self.Date.language_texts["number_names, type: list"][self.dates["Day"]].capitalize()

		self.diary_header = self.diary_header_template.format(self.day_number_name.lower(), self.date["month_name"], self.dates["Year"], self.date["%d/%m/%Y"], self.Date.language_texts["day_names_genders, type: list"][self.date["weekday"]], self.date["day_name"])

		self.survival_diary_file = self.dates["folders"]["Month"] + self.survival_diary_file_name + ".txt"
		self.File.Create(self.survival_diary_file)

	def Write_To_Files(self):
		# Update year, month, day, and survival day numbers on files
		for key in self.dates:
			if key != "folders":
				file = self.survivor_date_files[key]
				text = str(self.dates[key])

				self.File.Edit(file, text, "w")

		# Write diary header to the diary file
		self.File.Edit(self.survival_diary_file, self.diary_header, "w")

	def Open_File(self):
		self.File.Open(self.survival_diary_file)

	def Show_Information(self):
		print()
		print(self.large_bar)
		print()

		if self.used_predefined_values == True:
			print(self.language_texts["the_class_used_predefined_city_and_survivor"] + ".")
			print()

			print(self.language_texts["city, title()"] + ":")
			print(self.city)
			print()

			print(self.language_texts["survivor, title()"] + ":")
			print(self.survivor)
			print()

		print(self.language_texts["this_survival_diary_file_was_created"] + ":")
		print(self.survival_diary_file_name)
		print()

		print(self.survival_diary_file)

		print()
		print(self.large_bar)
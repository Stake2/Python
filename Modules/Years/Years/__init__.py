# Years.py

class Years(object):
	def __init__(self, select_year = False):
		self.select_year = select_year

		self.Define_Basic_Variables()

		# Define module folders
		from Utility.Define_Folders import Define_Folders as Define_Folders

		Define_Folders(self)

		self.Define_Texts()
		self.Define_Folders_And_Files()
		self.Define_Lists_And_Dictionaries()

		if self.select_year == True:
			self.Select_Year()

	def Define_Basic_Variables(self):
		from Utility.Global_Switches import Global_Switches as Global_Switches

		from Utility.File import File as File
		from Utility.Folder import Folder as Folder
		from Utility.Date import Date as Date
		from Utility.Input import Input as Input
		from Utility.JSON import JSON as JSON
		from Utility.Text import Text as Text

		self.switches = Global_Switches().switches["global"]

		self.File = File()
		self.Folder = Folder()
		self.Date = Date()
		self.Input = Input()
		self.JSON = JSON()
		self.Text = Text()

		self.languages = self.JSON.Language.languages

		self.user_language = self.JSON.Language.user_language
		self.full_user_language = self.JSON.Language.full_user_language

		self.Sanitize = self.File.Sanitize

		self.folders = self.Folder.folders

		self.date = self.Date.date

	def Define_Texts(self):
		self.large_bar = "-----"
		self.dash_space = "-"

		self.texts = self.JSON.To_Python(self.folders["apps"]["module_files"][self.module["key"]]["texts"])

		self.texts = self.JSON.Language.Mix(self.texts, "years, title()", ["en", "pt"], item = True)
		self.texts = self.JSON.Language.Mix(self.texts, "new_year", ["en", "pt"], item = True)
		self.texts = self.JSON.Language.Mix(self.texts, "christmas, title()", ["en", "pt"], item = True)
		self.texts = self.JSON.Language.Mix(self.texts, "texts, title()", ["en", "pt"], item = True)
		self.texts = self.JSON.Language.Mix(self.texts, "watch, title()", ["en", "pt"], item = True)
		self.texts = self.JSON.Language.Mix(self.texts, "year_summary_texts, type: list", ["en", "pt"], item = True)

		self.language_texts = self.JSON.Language.Item(self.texts)

		self.language_texts["month_names, type: list"] = self.Date.language_texts["month_names, type: list"]

		self.author = "Izaque Sanvezzo (Stake2, Funkysnipa Cat)"

	def Define_Folders_And_Files(self):
		self.watch_history_folder = self.folders["notepad"]["networks"]["audiovisual_media_network"]["root"] + "Watch History/"
		self.Folder.Create(self.watch_history_folder)

		self.current_year_watched_folder = self.watch_history_folder + str(self.date["year"]) + "/"
		self.Folder.Create(self.current_year_watched_folder)

		self.episodes_file = self.current_year_watched_folder + "Entries.json"
		self.File.Create(self.episodes_file)

		# Year text folders
		self.year_texts_folder = self.folders["notepad"]["effort"]["years"]["root"] + self.texts["texts, title()"]["en"] + "/"
		self.Folder.Create(self.year_texts_folder)

		self.years_file = self.folders["notepad"]["effort"]["years"]["root"] + self.texts["years, title()"]["en"] + ".json"
		self.File.Create(self.years_file)

		# Year image folders
		self.years_image_folder = self.folders["mega"]["image"]["root"] + self.texts["years, en - pt"] + "/"
		self.Folder.Create(self.years_image_folder)

		self.year_images_folder = self.years_image_folder + self.texts["images, title()"]["en"] + "/"
		self.Folder.Create(self.year_images_folder)

	def Define_Lists_And_Dictionaries(self):
		# Lists
		self.summary_date = self.Date.From_String("30/12/{}".format(self.date["year"]))

		# Dictionaries
		self.years = {
			"list": [],
		}

		# Add Years to Years list
		for year in range(2018, int(self.date["year"]) + 1):
			self.years["list"].append(str(year))

		# Dictionaries filling
		for year in self.years["list"]:
			self.years[year] = {}

			self.years[year]["number"] = year

			# Define root folder
			self.years[year]["folder"] = self.folders["notepad"]["effort"]["years"]["root"] + year + "/"
			self.Folder.Create(self.years[year]["folder"])

			# Define image folder
			self.years[year]["image_folder"] = self.years_image_folder + year + "/"
			self.Folder.Create(self.years[year]["image_folder"])

			# Define folders
			self.years[year]["folders"] = self.Folder.Contents(self.years[year]["folder"])["dictionary"]

			for language in self.languages["small"]:
				full_language = self.languages["full"][language]

				if full_language not in self.years[year]["folders"]:
					self.years[year]["folders"][full_language] = {
						"root": self.years[year]["folders"]["root"] + full_language + "/"
					}

				text = self.texts["firsts_of_the_year"][language]

				if text not in self.years[year]["folders"][full_language]:
					self.years[year]["folders"][full_language][text] = {
						"root": self.years[year]["folders"][full_language]["root"] + text + "/"
					}

		# Define "Year Texts" folders and files
		self.years["year_texts"] = self.Folder.Contents(self.year_texts_folder)["dictionary"]

		# Current Year dictionary definition
		self.current_year = self.years[str(self.date["year"])]

		from copy import deepcopy

		# Write Years dictionary converted to JSON on "Years.json" file
		dictionary = deepcopy(self.years)

		for key in dictionary:
			if key not in ["list", "year_texts"]:
				dictionary[key].pop("folders")

		self.JSON.Edit(self.years_file, dictionary)

	def Select_Year(self, years = None, select_text = None):
		if years == None:
			years = self.years["list"]

		show_text = self.language_texts["years, title()"]

		if select_text == None:
			select_text = self.language_texts["select_a_year"]

		year = self.years[self.Input.Select(years, show_text = show_text, select_text = select_text)["option"]]

		return year
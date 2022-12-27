# Years.py

from Global_Switches import Global_Switches as Global_Switches

from Language import Language as Language
from File import File as File
from Folder import Folder as Folder
from Date import Date as Date
from Input import Input as Input
from Text import Text as Text

class Years(object):
	def __init__(self, parameter_switches = None, select_year = True):
		self.parameter_switches = parameter_switches

		self.select_year = select_year

		self.Define_Basic_Variables()
		self.Define_Module_Folder()

		self.Define_Texts()
		self.Define_Folders_And_Files()
		self.Define_Lists_And_Dictionaries()

		if self.select_year == True:
			self.Select_Year()

	def Define_Basic_Variables(self):
		# Global Switches dictionary
		self.global_switches = Global_Switches().global_switches

		if self.parameter_switches != None:
			self.global_switches.update(self.parameter_switches)

		self.Language = Language(self.global_switches)
		self.File = File(self.global_switches)
		self.Folder = Folder(self.global_switches)
		self.Date = Date(self.global_switches)
		self.Input = Input(self.global_switches)
		self.Text = Text(self.global_switches)

		self.app_settings = self.Language.app_settings
		self.languages = self.Language.languages
		self.small_languages = self.languages["small"]
		self.full_languages = self.languages["full"]
		self.translated_languages = self.languages["full_translated"]

		self.user_language = self.Language.user_language
		self.full_user_language = self.Language.full_user_language

		self.Sanitize = self.File.Sanitize

		self.folders = self.Folder.folders
		self.root_folders = self.folders["root"]
		self.user_folders = self.folders["user"]
		self.apps_folders = self.folders["apps"]
		self.mega_folders = self.folders["mega"]
		self.notepad_folders = self.folders["notepad"]

		self.date = self.Date.date

	def Define_Module_Folder(self):
		self.module_name = self.__module__

		if "." in self.module_name:
			self.module_name = self.module_name.split(".")[0]

		self.module_name_lower = self.module_name.lower()

		self.apps_folders["app_text_files"][self.module_name_lower] = {
			"root": self.apps_folders["app_text_files"]["root"] + self.module_name + "/",
		}

		self.Folder.Create(self.apps_folders["app_text_files"][self.module_name_lower]["root"])

		self.apps_folders["app_text_files"][self.module_name_lower]["texts"] = self.apps_folders["app_text_files"][self.module_name_lower]["root"] + "Texts.json"
		self.File.Create(self.apps_folders["app_text_files"][self.module_name_lower]["texts"])

	def Define_Texts(self):
		self.large_bar = "-----"
		self.dash_space = "-"

		self.texts = self.Language.JSON_To_Python(self.apps_folders["app_text_files"][self.module_name_lower]["texts"])

		self.texts = self.Language.Mix(self.texts, "years, title()", ["en", "pt"], item = True)
		self.texts = self.Language.Mix(self.texts, "new_year", ["en", "pt"], item = True)
		self.texts = self.Language.Mix(self.texts, "christmas, title()", ["en", "pt"], item = True)
		self.texts = self.Language.Mix(self.texts, "texts, title()", ["en", "pt"], item = True)
		self.texts = self.Language.Mix(self.texts, "watch, title()", ["en", "pt"], item = True)
		self.texts = self.Language.Mix(self.texts, "year_summary_texts, type: list", ["en", "pt"], item = True)

		self.language_texts = self.Language.Item(self.texts)

		self.language_texts["month_names, type: list"] = self.Date.language_texts["month_names, type: list"]

		self.author = "Izaque Sanvezzo (Stake2, Funkysnipa Cat)"

	def Define_Folders_And_Files(self):
		self.watch_history_folder = self.notepad_folders["networks"]["audiovisual_media_network"] + "Watch History/"
		self.Folder.Create(self.watch_history_folder)

		self.watched_folder = self.watch_history_folder + "Watched/"
		self.Folder.Create(self.watched_folder)

		self.current_year_watched_media_folder = self.watched_folder + str(self.date["year"]) + "/"
		self.Folder.Create(self.current_year_watched_media_folder)

		self.episodes_file = self.current_year_watched_media_folder + "Episodes.json"
		self.File.Create(self.episodes_file)

		# Year text folders
		self.years_folder = self.folders["notepad"]["effort"]["root"] + self.texts["years, title()"]["en"] + "/"
		self.Folder.Create(self.years_folder)

		self.year_texts_folder = self.years_folder + self.texts["texts, title()"]["en"] + "/"
		self.Folder.Create(self.year_texts_folder)

		self.years_file = self.years_folder + self.texts["years, title()"]["en"] + ".json"
		self.File.Create(self.years_file)

		# Year image folders
		self.years_image_folder = self.folders["mega"]["image"]["root"] + self.texts["years, en - pt"] + "/"
		self.Folder.Create(self.years_image_folder)

		self.year_images_folder = self.years_image_folder + self.texts["images, title()"]["en"] + "/"
		self.Folder.Create(self.year_images_folder)

	def Define_Lists_And_Dictionaries(self):
		# Lists
		self.summary_date = self.Date.From_String("26/12/{}".format(self.date["year"]), "%d/%m/%Y")

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
			self.years[year]["folder"] = self.years_folder + year + "/"
			self.Folder.Create(self.years[year]["folder"])

			# Define image folder
			self.years[year]["image_folder"] = self.years_image_folder + year + "/"
			self.Folder.Create(self.years[year]["image_folder"])

			# Define folders
			self.years[year]["folders"] = self.Folder.Contents(self.years[year]["folder"])["dictionary"]

		# Write Years dictionary converted to JSON on "Years.json" file
		text = self.Language.Python_To_JSON(self.years)
		self.File.Edit(self.years_file, text, "w")

		# Define "Year Texts" folders and files
		self.year_texts_contents = self.Folder.Contents(self.year_texts_folder)["dictionary"]

		# Current Year dictionary definition
		self.current_year = self.years[str(self.date["year"])]

	def Select_Year(self, years = None, select_text = None):
		if years == None:
			years = self.years["list"]

		show_text = self.language_texts["years, title()"]

		if select_text == None:
			select_text = self.language_texts["select_a_year"]

		year = self.years[self.Input.Select(years, show_text = show_text, select_text = select_text)["option"]]

		return year
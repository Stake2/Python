# Christmas.py

from Global_Switches import Global_Switches as Global_Switches

from Language import Language as Language
from File import File as File
from Folder import Folder as Folder
from Date import Date as Date
from Input import Input as Input
from Text import Text as Text

from Social_Networks.Social_Networks import Social_Networks as Social_Networks
from Social_Networks.Open_Social_Network import Open_Social_Network as Open_Social_Network

class Christmas():
	def __init__(self, parameter_switches = None):
		self.parameter_switches = parameter_switches

		self.Define_Basic_Variables()
		self.Define_Module_Folder()
		self.Define_Texts()
		self.Today_Is_Christmas()

		self.Define_Folders()
		self.Define_Files()
		self.Define_Lists()

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
		self.small_languages = self.Language.languages["small"]
		self.full_languages = self.Language.languages["full"]
		self.translated_languages = self.Language.languages["full_translated"]

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
		name = self.__module__

		if "." in name:
			name = name.split(".")[0]

		self.module_text_files_folder = self.apps_folders["app_text_files"] + name + "/"
		self.Folder.Create(self.module_text_files_folder)

		self.texts_file = self.module_text_files_folder + "Texts.json"
		self.File.Create(self.texts_file)

	def Define_Texts(self):
		self.large_bar = "-----"
		self.dash_space = "-"

		self.texts = self.Language.JSON_To_Python(self.texts_file)

		self.language_texts = self.Language.Item(self.texts)

		self.christmas = self.Date.From_String("25/12/" + str(self.date["year"]), "%d/%m/%Y")

	def Today_Is_Christmas(self):
		self.today_is_christmas = False

		if self.date["day"] == self.christmas["day"] and self.date["month"] == self.christmas["month"]:
			self.today_is_christmas = True

		return self.today_is_christmas

	def Define_Folders(self):
		self.current_year_folder = self.notepad_folders["years"]["current"]["root"]
		self.Folder.Create(self.current_year_folder)

		self.christmas_folder = self.current_year_folder + self.language_texts["christmas, title(), en - pt"] + "/"
		self.Folder.Create(self.christmas_folder)

		self.language_year_folder = self.current_year_folder + self.full_user_language + "/"
		self.Folder.Create(self.language_year_folder)

		self.language_year_folders = {}
		self.christmas_language_folders = {}

		for language in self.small_languages:
			full_language = self.full_languages[language]

			self.language_year_folders[language] = self.current_year_folder + full_language + "/"
			self.Folder.Create(self.language_year_folders[language])

			self.christmas_language_folders[language] = self.language_year_folders[language] + self.texts["christmas, title()"][language] + "/"
			self.Folder.Create(self.christmas_language_folders[language])

	def Define_Files(self):
		self.planning_files = {}

		for language in self.small_languages:
			self.planning_files[language] = self.christmas_language_folders[language] + self.texts["planning, title()"][language] + ".txt"

		self.planning_file = self.planning_files[self.user_language]
		self.objects_file = self.christmas_language_folders["en"] + "Objects.txt"

		self.things_to_watch_file = self.christmas_folder + self.language_texts["watch, title(), en - pt"] + ".txt"
		self.things_to_eat_file = self.christmas_language_folders[self.user_language] + self.language_texts["eat, title()"] + ".txt"

	def Define_Lists(self):
		self.twitter_scheduled_text = "Twitter Scheduled"
		self.twitter_scheduled_link = "https://twitter.com/compose/tweet/unsent/scheduled"

		self.alternative_social_networks_links = {
			"Github": "https://github.com/Stake2/",
			"DeviantArt": "https://www.deviantart.com/stake2/",
			"YouTube": "https://www.youtube.com/c/TheStake2/",
		}

		self.functions = {
			"Open_File": self.Open_File,
			"Open_Social_Network": self.Open_Social_Network,
			"Run_Script": self.Run_Script,
		}

	def Open_File(self, text):
		files = {
			"Foobar2000": "C:/Program Files (x86)/foobar2000/foobar2000.exe",
			"Theme": self.image_folder + self.language_texts["christmas, title(), en - pt"] + "/Theme/" + self.language_texts["christmas, title(), en - pt"] + ".lnk",
		}

		texts = {
			"Foobar2000": self.language_texts["opening_{}"].format("Foobar2000"),
			"Theme": self.language_texts["defining_{}"].format(self.language_texts["christmas_theme"]),
		}

		file = files[text]
		text = texts[text]

		if self.global_switches["testing"] == False:
			self.File.Open(file)

		print(text + "...")

	def Open_Social_Network(self, social_network):
		social_network_link = None

		social_network_backup = social_network

		social_networks = [""]
		self.option_info = None
		self.second_space = True

		if social_network == self.twitter_scheduled_text:
			social_network_link = self.twitter_scheduled_link
			social_networks = ["Twitter"]
			self.second_space = False

		if social_network_backup != self.twitter_scheduled_text:
			self.Social_Networks = Social_Networks()

			social_networks = self.Social_Networks.social_networks
			social_networks.remove("Habitica")

			self.option_info = {"type": "profile"}

		for social_network in social_networks:
			Open_Social_Network(option_info = self.option_info, social_network_parameter = social_network, custom_link = social_network_link, second_space = self.second_space)

			if social_network_backup != "Twitter Scheduled":
				text = self.language_texts["press_enter_when_you_finish_changing_the_profile_picture_of"] + " " + social_network

				if self.global_switches["testing"] == False:
					self.Input.Type(text)

				if self.global_switches["testing"] == True:
					print(text)

				print()
				print("-")

		if social_network_backup != self.twitter_scheduled_text:
			social_networks = ["Github", "DeviantArt", "YouTube"]

			print()

			for social_network in social_networks:
				link = self.alternative_social_networks_links[social_network]

				print(self.language_texts["opening_{}"].format(social_network) + ":")
				print("\t" + link)
				print()

				if self.global_switches["testing"] == False:
					self.File.Open(link)

				text = self.language_texts["press_enter_when_you_finish_changing_the_profile_picture_of"] + " " + social_network

				if self.global_switches["testing"] == False:
					self.Input.Type(text)

				if self.global_switches["testing"] == True:
					print(text)

				if social_network != social_networks[-1]:
					print()
					print("-")
					print()

	def Run_Script(self, script_name):
		files = self.Folder.Contents(self.white_shortcuts_folder)["file"]["list"]

		self.press_enter_text = self.language_texts["press_enter_when_you"] + " {}"

		script_texts = {
			"Watch_History": self.language_texts["press_enter_when_you_finish_watching_all_of_the_christmas_episodes"],
			"GamePlayer": self.language_texts["press_enter_when_you_finish_spending_time_with_monika_on_the_game"] + ' "Monika After Story"',
		}

		for file in files:
			if "1 Apps.lnk" in file:
				self.script_file = file

		if self.global_switches["testing"] == False and script_name != "GamePlayer":
			self.File.Open(self.script_file)

		if script_name == "Watch_History":
			files = {
				self.language_texts["watch"]: self.things_to_watch_file,
				self.language_texts["eat"]: self.things_to_eat_file,
			}

			for text in files:
				file = files[text]
				lines = self.File.Contents(file)["lines"]

				print()
				print(self.language_texts["to, title()"] + " " + text + ":")

				if lines == []:
					print("1. " + self.language_texts["nothing, title()"])

				i = 1
				for line in lines:
					print(str(i) + ". " + line)

					i += 1

		if self.global_switches["testing"] == False:
			self.Input.Type(script_texts[script_name])

		if self.global_switches["testing"] == True:
			print()
			print(script_texts[script_name])
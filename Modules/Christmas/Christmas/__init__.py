# Christmas.py

class Christmas():
	def __init__(self):
		self.Define_Basic_Variables()

		# Define module folders
		from Utility.Define_Folders import Define_Folders as Define_Folders

		Define_Folders(self)

		# Import "Social_Networks" classes
		from Social_Networks.Social_Networks import Social_Networks
		from Social_Networks.Open_Social_Network import Open_Social_Network

		self.Social_Networks = Social_Networks()
		self.Social_Networks.Open_Social_Network = Open_Social_Network

		self.Define_Texts()
		self.Today_Is_Christmas()

		from Years.Years import Years as Years

		self.Years = Years()

		self.Define_Folders()
		self.Define_Files()
		self.Define_Lists()

	def Define_Basic_Variables(self):
		from Utility.Global_Switches import Global_Switches as Global_Switches

		from Utility.Language import Language as Language
		from Utility.File import File as File
		from Utility.Folder import Folder as Folder
		from Utility.Date import Date as Date
		from Utility.Input import Input as Input
		from Utility.JSON import JSON as JSON
		from Utility.Text import Text as Text

		self.switches = Global_Switches().switches["global"]

		self.Language = Language()
		self.File = File()
		self.Folder = Folder()
		self.Date = Date()
		self.Input = Input()
		self.JSON = JSON()
		self.Text = Text()

		self.languages = self.Language.languages

		self.user_language = self.Language.user_language
		self.full_user_language = self.Language.full_user_language

		self.Sanitize = self.File.Sanitize

		self.folders = self.Folder.folders

		self.date = self.Date.date

	def Define_Texts(self):
		self.large_bar = "-----"
		self.dash_space = "-"

		self.texts = self.JSON.To_Python(self.folders["apps"]["module_files"][self.module["key"]]["texts"])

		self.language_texts = self.Language.Item(self.texts)

		self.christmas = self.Date.From_String("25/12/" + str(self.date["year"]))

	def Today_Is_Christmas(self):
		self.today_is_christmas = False

		if self.date["day"] == self.christmas["day"] and self.date["month"] == self.christmas["month"]:
			self.today_is_christmas = True

		return self.today_is_christmas

	def Define_Folders(self):
		self.current_year = self.Years.current_year

		self.christmas_image_folder = self.folders["mega"]["image"]["root"] + self.language_texts["christmas, title(), en - pt"] + "/"
		self.Folder.Create(self.christmas_image_folder)

	def Define_Files(self):
		if self.full_user_language in self.current_year["folders"]:
			self.planning_file = self.current_year["folders"][self.full_user_language][self.language_texts["christmas, title()"]]
			self.planning_file = self.planning_file[self.language_texts["planning, title()"]]

			self.objects_file = self.current_year["folders"]["English"][self.texts["christmas, title()"]["en"]]["root"] + "Objects.txt"

			self.things_to_watch_file = self.current_year["folders"][self.language_texts["christmas, title(), en - pt"]]["root"] + self.language_texts["watch, title(), en - pt"] + ".txt"

			self.watch_list_file = self.folders["notepad"]["networks"]["audiovisual_media_network"]["root"] + "Watch List.txt"

			self.things_to_eat_file = self.current_year["folders"][self.full_user_language][self.language_texts["christmas, title()"]]["root"] + self.language_texts["eat, title()"] + ".txt"

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
			"Open_Social_Network": self.Social_Networks.Open_Social_Network,
			"Run_Script": self.Run_Script,
		}

	def Open_File(self, key):
		files = {
			"Foobar2000": "C:/Program Files (x86)/foobar2000/foobar2000.exe",
			"Theme": self.christmas_image_folder + "Theme/" + self.language_texts["christmas, title(), en - pt"] + ".lnk",
			"Texts - Textos": self.current_year["folders"][self.language_texts["christmas, title(), en - pt"]]["root"] + self.language_texts["texts, title(), en - pt"] + ".txt",
		}

		texts = {
			"Foobar2000": self.language_texts["opening_{}"].format("Foobar2000"),
			"Theme": self.language_texts["defining_{}"].format(self.language_texts["christmas_theme"]),
			"Texts - Textos": self.language_texts["opening_this_file_{}"].format(self.language_texts["texts, title(), en - pt"] + ".txt"),
		}

		file = files[key]
		text = texts[key]

		if self.switches["testing"] == False or self.switches["testing"] == True and key not in ["Foobar2000", "Theme"]:
			self.File.Open(file)

		if key != self.language_texts["texts, title(), en - pt"]:
			text += "..."

		if key == self.language_texts["texts, title(), en - pt"]:
			text = "\n" + text

		print(text)

	def Open_Social_Network(self, social_network):
		social_network_link = None

		social_network_backup = social_network

		social_networks = [""]
		self.option_info = None

		if social_network == self.twitter_scheduled_text:
			# Unblock Twitter
			import Block_Websites

			Block_Websites.Unblock(websites = self.Social_Networks.social_networks["Names"], time = 60)

			social_network_link = self.twitter_scheduled_link
			social_networks = ["Twitter"]

		if social_network_backup != self.twitter_scheduled_text:
			social_networks = sorted(self.Social_Networks.social_networks["Names"], key=str.lower)
			social_networks.remove("Habitica")

			self.option_info = {"type": "profile"}

		if social_network_backup != self.twitter_scheduled_text:
			self.social_networks_len = str(len(social_networks) + 3)

		i = 1
		for social_network in social_networks:
			if social_network_backup != self.twitter_scheduled_text:
				if social_network == social_networks[0]:
					print()

				print(str(i) + "/" + self.social_networks_len + ": " + social_network)
				print()

			Open_Social_Network(option_info = self.option_info, social_network_parameter = social_network, custom_link = social_network_link, unblock = False, first_space = False, second_space = False)

			text = self.language_texts["press_enter_when_you_finish_adding_the_screenshots_to_the_scheduled_tweet"]

			if social_network_backup != self.twitter_scheduled_text:
				text = self.language_texts["press_enter_when_you_finish_changing_the_profile_picture_of"] + " " + social_network

			self.Input.Type(text)

			if social_network_backup != self.twitter_scheduled_text:
				print()
				print("-")
				print()

			i += 1

		if social_network_backup != self.twitter_scheduled_text:
			social_networks = ["YouTube"]

			for social_network in social_networks:
				link = self.alternative_social_networks_links[social_network]

				print(str(i) + "/" + self.social_networks_len + ": " + social_network)
				print()
				print(self.language_texts["opening_{}"].format(social_network) + ":")
				print("\t" + link)

				if self.switches["testing"] == False:
					self.File.Open(link)

				text = self.language_texts["press_enter_when_you_finish_changing_the_profile_picture_of"] + " " + social_network

				self.Input.Type(text)

				if social_network != social_networks[-1]:
					print()
					print("-")
					print()

				i += 1

	def Run_Script(self, script_name):
		files = self.Folder.Contents(self.folders["apps"]["shortcuts"]["white_shortcuts"])["file"]["list"]

		self.press_enter_text = self.language_texts["press_enter_when_you"] + " {}"

		script_texts = {
			"Watch_History": self.language_texts["press_enter_when_you_finish_watching_all_of_the_christmas_episodes"],
			"GamePlayer": self.language_texts["press_enter_when_you_finish_spending_time_with_monika_on_the_game"] + ' "Monika After Story"',
		}

		for file in files:
			if "1 Apps.lnk" in file:
				self.script_file = file

		if self.switches["testing"] == False and script_name != "GamePlayer":
			self.File.Open(self.script_file)

		if script_name == "Watch_History":
			files = {
				self.language_texts["watch"]: self.things_to_watch_file,
				self.language_texts["watch"] + " (" + self.language_texts["list"] + ")": self.watch_list_file,
				self.language_texts["eat"]: self.things_to_eat_file,
			}

			for text in files:
				file = files[text]
				self.File.Open(file)

				lines = self.File.Contents(file)["lines"]

				print()
				print(self.language_texts["to, title()"] + " " + text + ":")

				if lines == []:
					print("1. " + self.language_texts["nothing, title()"])

				i = 1
				for line in lines:
					print(str(i) + ". " + line)

					i += 1

		self.Input.Type(script_texts[script_name])
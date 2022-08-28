# Christmas.py

from Script_Helper import *

class Christmas():
	def __init__(self, parameter_switches = None):
		# Verbose variable
		self.verbose = False

		self.testing_script = False

		self.parameter_switches = parameter_switches

		self.Define_Basic_Variables()
		self.Define_Folders()
		self.Define_Files()
		self.Define_Lists()
		self.Execute_Steps()

		print(Language_Item_Definer("Your Christmas of {} is finished, congratulatios", "Seu Natal de {} está concluído, parabéns").format(str(current_year)) + "!")

	def Define_Basic_Variables(self):
		self.option = True

		# Global Switches dictionary
		self.global_switches = {
			"write_to_file": self.option,
			"create_files": self.option,
			"create_folders": self.option,
			"move_files": self.option,
			"verbose": self.verbose,
			"testing_script": self.testing_script,
		}

		if self.parameter_switches != None:
			self.global_switches = self.parameter_switches
			self.testing_script = self.global_switches["testing_script"]

		if self.global_switches["testing_script"] == True:
			print(Language_Item_Definer("Testing script: Yes", "Testando script: Sim"))

		if self.global_switches["verbose"] == True:
			print(Language_Item_Definer("Verbose on", "Verbose ligado") + ".")

		if self.global_switches["testing_script"] == True:
			self.global_switches["write_to_file"] = False
			self.global_switches["create_files"] = False

		self.dot_text = ".txt"

	def Define_Folders(self):
		self.main_years_folders = notepad_folder_years

		self.root_year_folder = notepad_folder_years + current_year + "/"
		Create_Folder(self.root_year_folder, self.global_switches)

		self.language_year_folder = self.root_year_folder + Language_Item_Definer(full_language_en, full_language_pt) + "/"
		Create_Folder(self.language_year_folder, self.global_switches)

		self.language_year_folders = {}

		self.language_year_folders[full_language_en] = self.root_year_folder + full_language_en + "/"
		self.language_year_folders[full_language_pt] = self.root_year_folder + full_language_pt + "/"

		for folder in self.language_year_folders.values():
			Create_Folder(folder, self.global_switches)

		self.christmas_language_folders = {}

		self.christmas_language_folders[full_language_en] = self.language_year_folders[full_language_en] + "Christmas" + "/"
		self.christmas_language_folders[full_language_pt] = self.language_year_folders[full_language_pt] + "Natal" + "/"

		self.christmas_watch_folders = {}

		self.christmas_watch_folders[full_language_en] = self.christmas_language_folders[full_language_en] + "Watch" + "/"
		self.christmas_watch_folders[full_language_pt] = self.christmas_language_folders[full_language_pt] + "Assistir" + "/"

	def Define_Files(self):
		self.planning_files = {
			full_language_en: self.christmas_language_folders[full_language_en] + "Planning" + self.dot_text,
			full_language_pt: self.christmas_language_folders[full_language_pt] + "Planejamento" + self.dot_text,
		}                                                                    

		self.full_language = Language_Item_Definer(full_language_en, full_language_pt)
		self.planning_file = self.planning_files[self.full_language]

		self.objects_file = self.christmas_language_folders[full_language_en] + "Objects" + self.dot_text

		self.things_to_watch_file = self.christmas_watch_folders[self.full_language] + "List" + Language_Item_Definer("", "a") + self.dot_text

	def Define_Lists(self):
		self.social_networks_links = {
			"Discord": "https://discord.com/app",
			"WhatsApp": "https://web.whatsapp.com/",
			"Wattpad": "https://www.wattpad.com/stake2",
			"Twitter Scheduled": "https://twitter.com/compose/tweet/unsent/scheduled",
			"Twitter Tweet": "https://twitter.com/Stake2__",
			"Instagram": "https://www.instagram.com/Stake2_",
			"Facebook": "https://www.facebook.com/me",
			"Github": "https://github.com/Stake2/",
			"DeviantArt": "https://www.deviantart.com/stake2/",
			"YouTube": "https://www.youtube.com/c/TheStake2/",
		}

		self.functions = {
			"Open_File": self.Open_File,
			"Open_Link": self.Open_Link,
			"Open_Links": self.Open_Links,
			"Run_Script": self.Run_Script,
		}

	def Open_File(self, text):
		files = {
			"Foobar2000": "C:/Program Files (x86)/foobar2000/foobar2000.exe",
			"Theme": "C:/Mega/Image/Christmas - Natal/Theme/Christmas.lnk",
		}

		file = files[text]

		if text == "Theme":
			text = Language_Item_Definer(text.lower(), "tema")

		if "exe" in file:
			if self.global_switches["testing_script"] == False:
				Open_File(file)

			print(self.opening_text.format(text))

		if "lnk" in file:
			if self.global_switches["testing_script"] == False:
				Open_Link(file)

	def Open_Link(self, website_name):
		link = self.social_networks_links[website_name]

		input(self.opening_text.format(website_name))

		if self.global_switches["testing_script"] == False:
			Open_Link(link)

	def Open_Links(self, website_names):
		website_names = website_names.split(", ")

		print(self.opening_text.format(Language_Item_Definer("Social Networks", "Redes Sociais")))

		for website_name in website_names:
			link = self.social_networks_links[website_name]

			if self.global_switches["testing_script"] == False:
				Open_Link(link)

			input(website_name)

	def Run_Script(self, script_name):
		self.files = List_Files(script_shortcuts_white_icons_folder, ".lnk")

		self.press_enter_text = Language_Item_Definer("Press Enter when you", "Pressione Enter quando você") + " {}"

		script_texts = {
			"Apps.bat": self.press_enter_text.format(Language_Item_Definer("finish watching all of the Christmas episodes", "terminar de assistir todos os episódios de Natal")) + ": ",
			"GamePlayer.bat": self.press_enter_text.format(Language_Item_Definer("finish spending time with Monika on the game", "terminar de passar um tempo com a Monika no jogo") + " \"Monika After Story\""),
		}

		for file in self.files:
			if file != None and script_name in file:
				self.script_file = file

		if self.global_switches["testing_script"] == False:
			Open_Link(self.script_file)

			if script_name == "Apps.bat":
				Open_Text_File(self.things_to_watch_file)

		input(script_texts[script_name])

	def Execute_Steps(self):
		self.planning = Create_Array_Of_File(self.planning_file)
		self.objects = Create_Array_Of_File(self.objects_file)

		self.opening_text = Language_Item_Definer("Opening", "Abrindo") + " {}..."

		print()
		print(Language_Item_Definer("Starting Christmas", "Iniciando Natal") + "...")
		print()

		i = 0
		for text in self.planning:
			object = self.objects[i]

			if object != "":
				function = self.functions[object.split(": ")[0]]
				object_data = object.split(": ")[1]

				print(text)

			else:
				input(text)

			if object != "":
				function(object_data)

			print()

			i += 1
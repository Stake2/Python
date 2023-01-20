# Stories.py

from Global_Switches import Global_Switches as Global_Switches

from Language import Language as Language
from File import File as File
from Folder import Folder as Folder
from Date import Date as Date
from Input import Input as Input
from JSON import JSON as JSON
from Text import Text as Text

from Social_Networks.Social_Networks import Social_Networks as Social_Networks
from Diary_Slim.Write_On_Diary_Slim_Module import Write_On_Diary_Slim_Module as Write_On_Diary_Slim_Module

class Stories(object):
	def __init__(self, parameter_switches = None, select_story = True):
		self.parameter_switches = parameter_switches

		self.Define_Basic_Variables()
		self.Define_Module_Folder()
		self.Define_Texts()

		self.Define_Social_Network_Variables()
		self.Define_Folders_And_Files()
		self.Define_Lists_And_Dictionaries()
		self.Define_Stories_Dictionary()

		if select_story == True:
			self.Select_Story()

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
		self.JSON = JSON(self.global_switches)
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
		self.links = self.Folder.links

		self.date = self.Date.date

	def Define_Module_Folder(self):
		self.module = {
			"name": self.__module__,
		}

		if "." in self.module["name"]:
			self.module["name"] = self.module["name"].split(".")[0]

		self.module["key"] = self.module["name"].lower()

		self.apps_folders["modules"][self.module["key"]] = {
			"root": self.apps_folders["modules"]["root"] + self.module["name"] + "/",
		}

		self.apps_folders["module_files"][self.module["key"]] = {
			"root": self.apps_folders["module_files"]["root"] + self.module["name"] + "/",
		}

		for item in ["module_files", "modules"]:
			self.apps_folders[item][self.module["key"]] = self.apps_folders[item]["root"] + self.module["name"] + "/"
			self.apps_folders[item][self.module["key"]] = self.Folder.Contents(self.apps_folders[item][self.module["key"]], lower_key = True)["dictionary"]

	def Define_Texts(self):
		self.texts = self.JSON.To_Python(self.apps_folders["module_files"][self.module["key"]]["texts"])

		self.language_texts = self.Language.Item(self.texts)

		i = 0
		for item in self.language_texts["copy_actions, type: list"]:
			self.language_texts["copy_actions, type: list"][i] = "[" + self.language_texts["copy_actions, type: list"][i] + "]"

			i += 1

		self.large_bar = "-----"
		self.dash_space = "-"

	def Define_Social_Network_Variables(self):
		self.Social_Networks = Social_Networks(self.global_switches)
		self.social_networks = self.Social_Networks.social_networks

		self.social_networks["Wattpad"]["profile"]["conversations"] = self.social_networks["Wattpad"]["profile"]["profile"] + "/conversations"
		self.social_networks["Wattpad"]["links"]["myworks"] = self.social_networks["Wattpad"]["links"]["link"] + "myworks/"

	def Define_Folders_And_Files(self):
		# Folders
		self.stories = {
			"folders": {
				"root": self.mega_folders["stories"]["root"],
			},
		}

		self.stories["folders"]["Database"] = {
			"root": self.stories["folders"]["root"] + "Database/",
		}

		self.Folder.Create(self.stories["folders"]["Database"]["root"])

		self.stories["folders"]["Database"]["Social Network Card Templates"] = {
			"root": self.stories["folders"]["Database"]["root"] + "Social Network Card Templates/",
		}

		self.Folder.Create(self.stories["folders"]["Database"]["Social Network Card Templates"]["root"])

		# Files
		for file_name in ["Author", "Stories list", "Stories.json"]:
			key = file_name.split(".")[0]

			self.stories["folders"]["Database"][key] = self.stories["folders"]["Database"]["root"] + file_name

			if "json" not in file_name:
				self.stories["folders"]["Database"][key] += ".txt"

			self.File.Create(self.stories["folders"]["Database"][key])

		# Chapter status template file
		self.stories["folders"]["Database"]["Chapter status template"] = self.stories["folders"]["Database"]["root"] + "Chapter status template.txt"
		self.File.Create(self.stories["folders"]["Database"]["Chapter status template"])

		# Create Social Network Card Templates files
		for item in ["Wattpad", "Twitter, Facebook"]:
			file_name = item

			if item == "Twitter, Facebook":
				file_name = "Twitter, Facebook"

			self.stories["folders"]["Database"]["Social Network Card Templates"][item] = self.stories["folders"]["Database"]["Social Network Card Templates"]["root"] + file_name + ".json"
			self.File.Create(self.stories["folders"]["Database"]["Social Network Card Templates"][item])

	def Define_Lists_And_Dictionaries(self):
		# Lists
		self.chapter_status_template = self.File.Contents(self.stories["folders"]["Database"]["Chapter status template"])["string"]

		self.author = self.File.Contents(self.stories["folders"]["Database"]["Author"])["lines"][0]

		# Dictionaries
		self.default_information_items = {
			self.language_texts["creation_date"]: self.Date.Now()["%d/%m/%Y"],
			self.language_texts["author, title()"]: self.author,
		}

	def Define_Stories_Dictionary(self):
		to_remove = [
			"Database",
			"Diary",
			"Diary Slim",
			"Others",
			"Rubbish",
		]

		# List stories on stories folder
		self.stories["list"] = self.Folder.Contents(self.mega_folders["stories"]["root"])["folder"]["names"]
		self.stories["list"] = self.Folder.Remove_Folders(self.stories["list"], to_remove)

		# Update stories list file with new story names
		self.File.Edit(self.stories["folders"]["Database"]["Stories list"], self.Text.From_List(self.stories["list"]), "w")

		self.stories["titles"] = {}
		self.stories["mixed_titles"] = []
		self.stories["number"] = len(self.stories["list"])

		self.stories["authors"] = [
			"Izaque Sanvezzo (Stake2, Funkysnipa Cat)",
			"Júlia",
			"Ana",
		]

		# Dictionaries
		# Add stories to stories dictionary
		for story in self.stories["list"]:
			self.stories[story] = {}
			self.stories[story]["title"] = story

			# Story folders
			self.stories[story]["folders"] = {
				"root": self.stories["folders"]["root"] + story + "/",
			}

			self.Folder.Create(self.stories[story]["folders"]["root"])

			self.stories[story]["Information"] = {}

			# Create subfolders inside story folder
			for folder in self.texts["folder_names, type: list"]:
				key = folder.lower()

				folder_name = folder.split("/")[-1]

				if folder_name == "":
					folder_name = folder.split("/")[-2]

				# Add root folder to folders dictionary
				self.stories[story]["folders"][folder] = {
					"root": self.stories[story]["folders"]["root"] + folder + "/",
				}

				# List contents of subfolder
				contents = self.Folder.Contents(self.stories[story]["folders"][folder]["root"])

				# Add subfolders to folders dictionary
				for sub_folder in contents["folder"]["list"]:
					sub_folder_name = sub_folder.split("/")[-1]

					if sub_folder_name == "":
						sub_folder_name = sub_folder.split("/")[-2]

					self.stories[story]["folders"][folder][sub_folder_name] = self.Folder.Sanitize(sub_folder)

				# Add files to folders dictionary
				for file in contents["file"]["list"]:
					file_name = file.split("/")[-1]

					if file_name == "":
						file_name = file.split("/")[-2]

					file_name = file_name.split(".")[0]

					if self.stories[story]["folders"]["root"].count("/") + 1 == file.count("/"):
						self.stories[story]["folders"][folder][file_name] = file

				for item in self.stories[story]["folders"][folder]:
					if self.Folder.Exist(item) == True:
						self.Folder.Create(item)

					if self.File.Exist(item) == True:
						self.File.Create(item)

			# Add Stake2 Website covers folder
			if self.Folder.Exist(self.mega_folders["websites"]["images"]["story_covers"] + story + "/") == True:
				self.stories[story]["folders"]["Websites Story Covers"] = self.mega_folders["websites"]["images"]["story_covers"] + story + "/"
				self.Folder.Create(self.stories[story]["folders"]["Websites Story Covers"])

			# Add Sony Vegas Files covers folder
			if self.Folder.Exist(self.root_folders["sony_vegas_files"]["story_covers"]["root"] + story + "/") == True:
				self.stories[story]["folders"]["Sony Vegas Covers"] = self.root_folders["sony_vegas_files"]["story_covers"]["root"] + story + "/"
				self.Folder.Create(self.stories[story]["folders"]["Sony Vegas Covers"])

			# Add Obsidian's Vaults folder
			self.stories[story]["folders"]["Obsidian's Vaults"] = {
				"root": self.mega_folders["obsidian_s_vaults"]["creativity"]["literature"]["stories"]["root"] + story + "/",
			}

			self.Folder.Create(self.stories[story]["folders"]["Obsidian's Vaults"]["root"])

			self.stories[story]["folders"]["Obsidian's Vaults"]["Chapters"] = {
				"root": self.stories[story]["folders"]["Obsidian's Vaults"]["root"] + "Chapters/",
			}

			self.Folder.Create(self.stories[story]["folders"]["Obsidian's Vaults"]["Chapters"]["root"])

			for language in self.small_languages:
				full_language = self.full_languages[language]

				self.stories[story]["folders"]["Obsidian's Vaults"]["Chapters"][full_language] = self.stories[story]["folders"]["Obsidian's Vaults"]["Chapters"]["root"] + full_language + "/"
				self.Folder.Create(self.stories[story]["folders"]["Obsidian's Vaults"]["Chapters"][full_language])	

			# Set the default author of the story
			if "Author" not in self.stories[story]["Information"] or "Author" in self.stories[story]["Information"] and self.stories[story]["Information"]["Author"] == "":
				self.stories[story]["Information"]["Author"] = self.author

			# Create files on information folder
			for key in self.texts["file_names, type: list"]:
				file_name = key

				if key in ["Information", "Titles", "Wattpad"]:
					file_name += ".json"

				if key not in ["Information", "Titles", "Wattpad"]:
					file_name += ".txt"

				if key != "Author" or key == "Author" and self.stories[story]["Information"]["Author"] != self.author:
					self.stories[story]["folders"]["Information"][key] = self.stories[story]["folders"]["Information"]["root"] + file_name
					self.File.Create(self.stories[story]["folders"]["Information"][key])

			# Read story Information from files inside Information folder
			for key in self.stories[story]["folders"]["Information"]:
				item = self.stories[story]["folders"]["Information"][key]

				if self.File.Exist(item) == True:
					function = self.File.Contents

					if ".json" in item:
						function = self.JSON.To_Python

					information = function(item)

					if key != "Information":
						self.stories[story]["Information"][key] = information

					if key == "Information":
						for sub_key in information:
							self.stories[story]["Information"][sub_key] = information[sub_key]

					if key == "Chapter status":
						self.stories[story]["Information"][key] = self.File.Dictionary(item, next_line = True)

					if ".txt" in item:
						if key == "Chapter dates":
							self.stories[story]["Information"][key] = self.stories[story]["Information"][key]["lines"]

						if key not in ["Chapter status", "Chapter dates"]:
							self.stories[story]["Information"][key] = self.stories[story]["Information"][key]["string"]

						if len(self.stories[story]["Information"][key]) == 1:
							self.stories[story]["Information"][key] = self.stories[story]["Information"][key][0]

					if key == "Titles":
						for titles_key in self.stories[story]["Information"][key]:
							if titles_key not in self.stories["titles"]:
								self.stories["titles"][titles_key] = []

							self.stories["titles"][titles_key].append(self.stories[story]["Information"][key][titles_key])

			# Add chapter titles files to Chapters dictionary
			for language in self.small_languages:
				full_language = self.full_languages[language]

				titles_text = self.texts["titles, title()"][language]

				# Transform language folder into a dictionary
				self.stories[story]["folders"]["Chapters"][full_language] = {
					"root": self.stories[story]["folders"]["Chapters"][full_language],
				}

				self.Folder.Create(self.stories[story]["folders"]["Chapters"][full_language]["root"])

				# Add titles folder
				self.stories[story]["folders"]["Chapters"][full_language][titles_text] = {
					"root": self.stories[story]["folders"]["Chapters"][full_language]["root"] + titles_text + "/"
				}

				self.Folder.Create(self.stories[story]["folders"]["Chapters"][full_language][titles_text]["root"])

				# Add titles file
				self.stories[story]["folders"]["Chapters"][full_language][titles_text][titles_text] = self.stories[story]["folders"]["Chapters"][full_language][titles_text]["root"] + titles_text + ".txt"

				self.File.Create(self.stories[story]["folders"]["Chapters"][full_language][titles_text][titles_text])

			self.stories[story]["Information"]["Chapter titles"] = {}

			# Read chapter titles
			for language in self.small_languages:
				full_language = self.full_languages[language]

				titles_text = self.texts["titles, title()"][language]

				file = self.stories[story]["folders"]["Chapters"][full_language][titles_text][titles_text]

				self.stories[story]["Information"]["Chapter titles"][language] = self.File.Contents(file)["lines"]

			# Add chapter number
			self.stories[story]["Information"]["Chapter number"] = len(self.stories[story]["Information"]["Chapter titles"]["en"])

			# Update chapter number on "Information.json" file
			file = self.stories[story]["folders"]["Information"]["Information"]

			# Add chapter number to "Information.json" dictionary
			text = self.JSON.To_Python(file)
			text["Chapter number"] = self.stories[story]["Information"]["Chapter number"]
			text = self.JSON.From_Python(text)

			self.File.Edit(file, text, "w")

			# Add language synopsis from synopsis folder inside Information folder
			self.stories[story]["folders"]["Information"]["Synopsis"] = {
				"root": self.stories[story]["folders"]["Information"]["root"] + "Synopsis/",
			}

			self.Folder.Create(self.stories[story]["folders"]["Information"]["Synopsis"]["root"])

			# Create synopsis files
			for full_language in list(self.full_languages.values()):
				self.stories[story]["folders"]["Information"]["Synopsis"][full_language] = self.stories[story]["folders"]["Information"]["Synopsis"]["root"] + full_language + ".txt"	
				self.File.Create(self.stories[story]["folders"]["Information"]["Synopsis"][full_language])

			self.stories[story]["Information"]["Synopsis"] = {}

			# Add synopsis to information dictionary
			for language in self.small_languages:
				full_language = self.full_languages[language]

				self.stories[story]["Information"]["Synopsis"][language] = self.File.Contents(self.stories[story]["folders"]["Information"]["Synopsis"][full_language])["string"]

			# Add writing folder
			self.stories[story]["folders"]["Information"]["Writing"] = {
				"root": self.stories[story]["folders"]["Information"]["root"] + "Writing/",
			}

			self.Folder.Create(self.stories[story]["folders"]["Information"]["Writing"]["root"])

			# Add writing files
			self.stories[story]["folders"]["Information"]["Writing"]["Time"] = self.stories[story]["folders"]["Information"]["Writing"]["root"] + "Time.json"
			self.File.Create(self.stories[story]["folders"]["Information"]["Writing"]["Time"])

			# Write to writing files
			dict_ = {}

			for item in self.texts["writing_modes, type: list"]["en"]:
				dict_[item] = {}
				dict_[item]["first"] = ""
				dict_[item]["last"] = ""

			if self.File.Contents(self.stories[story]["folders"]["Information"]["Writing"]["Time"])["lines"] == []:
				self.JSON.Edit(self.stories[story]["folders"]["Information"]["Writing"]["Time"], dict_)

			# Read writing time file
			self.stories[story]["Information"]["Writing"] = {}
			self.stories[story]["Information"]["Writing"]["Time"] = self.JSON.To_Python(self.stories[story]["folders"]["Information"]["Writing"]["Time"])

			# Add Website link
			self.stories[story]["Information"]["Website"] = {}

			website_folder = story

			# Add custom website link name
			if "Website link name" in self.stories[story]["Information"]:
				website_folder = self.stories[story]["Information"]["Website link name"]

				if "{story}" in website_folder:
					website_folder = website_folder.replace("{story}", story)

			self.stories[story]["Information"]["Website"]["link"] = self.links["Stake2 Website"] + website_folder + "/"

			# Add Wattpad link
			if self.stories[story]["Information"]["Wattpad"]["ID"]["en"] != "None":
				self.stories[story]["Information"]["Wattpad"]["links"] = {}

				for key in self.stories[story]["Information"]["Wattpad"]["ID"]:
					self.stories[story]["Information"]["Wattpad"]["links"][key] = self.social_networks["Wattpad"]["links"]["myworks"] + self.stories[story]["Information"]["Wattpad"]["ID"][key]

			# Add all titles of the story to the mixed_titles list
			for language in self.stories[story]["Information"]["Titles"]:
				story_title = self.stories[story]["Information"]["Titles"][language]

				if story_title not in self.stories["mixed_titles"]:
					self.stories["mixed_titles"].append(story_title)

			self.stories[story]["Information"]["Readers"] = self.File.Contents(self.stories[story]["folders"]["Readers and Reads"]["Readers"])["lines"]

			self.stories[story]["Information"]["Readers number"] = len(self.stories[story]["Information"]["Readers"])

			self.stories[story]["Information"] = dict(sorted(self.stories[story]["Information"].items()))

		# Write stories dictionary to Stories.json
		self.JSON.Edit(self.stories["folders"]["Database"]["Stories"], self.stories)

	def Select_Story(self, select_text_parameter = None):
		show_text = self.language_texts["stories, title()"]

		select_text = select_text_parameter

		if select_text_parameter == None:
			select_text = self.language_texts["select_a_story"]

		class_name = type(self).__name__.lower()

		if select_text_parameter == None and issubclass(type(self), Stories) == True and class_name in self.language_texts:
			select_text = self.language_texts["select_a_story_to"] + " " + self.language_texts[class_name]

		stories = self.stories.copy()

		# Remove stories with all chapters posted if the class is "Post"
		if class_name == "post":
			for story in self.stories["titles"]["en"].copy():
				story = stories[story]

				post = story["Information"]["Chapter status"]["Post"]

				if int(post) == len(story["Information"]["Chapter titles"][self.user_language]):
					for language in self.small_languages:
						stories["titles"][language].remove(story["Information"]["Titles"][language])

		self.option = self.Input.Select(stories["titles"]["en"], language_options = stories["titles"][self.user_language], show_text = show_text, select_text = select_text)["option"]

		self.story = self.stories[self.option]

	def Cover_Folder_Name(self, number):
		if int(number) <= 10:
			folder_name = "1 - 10"

		if int(number) >= 11 and int(number) <= 20:
			folder_name = "11 - 20"

		if int(number) >= 21 and int(number) <= 30:
			folder_name = "21 - 30"

		if int(number) >= 31 and int(number) <= 40:
			folder_name = "31 - 40"

		if int(number) >= 41 and int(number) <= 50:
			folder_name = "41 - 50"

		return folder_name

	def Show_Story_Information(self, stories_list = None):
		if stories_list == None:
			stories_list = self.stories["list"]

		for story in stories_list:
			story = self.stories[story]

			print()
			print(self.large_bar)
			print()

			print(self.language_texts["story_title"] + ":")

			# Show language titles
			for language in self.small_languages:
				translated_language = self.translated_languages[language][self.user_language]

				print("\t" + translated_language + ":")
				print("\t" + story["Information"]["Titles"][language])
				print()

			# Show information items
			i = 0
			for information_item in self.language_texts["information_items, type: list"]:
				english_information_item = self.texts["information_items, type: list"]["en"][i]

				if information_item != self.language_texts["title, title()"]:
					print(information_item + ":")

					if information_item != self.language_texts["synopsis, title()"]:
						print(story["Information"][english_information_item])

					if information_item == self.language_texts["synopsis, title()"]:
						for language in self.small_languages:
							full_language = self.full_languages[language]
							translated_language = self.translated_languages[language][self.user_language]

							print("\t" + translated_language + ":")

							for line in story["Information"][english_information_item][full_language].splitlines():
								print("\t" + line)
							
							if language != self.small_languages[-1]:
								print()

					print()

				i += 1

			print(self.language_texts["folder, title()"] + ":")
			print(story["folders"]["root"])
			print()

			print(self.language_texts["website_link"] + ":")
			print(story["Information"]["Website"]["link"])
			print()

			print("Wattpad:")

			for key in story["Information"]["Wattpad"]:
				print("\t" + self.language_texts[key.lower() + ", title()"] + ":")

				for language in story["Information"]["Wattpad"][key]:
					translated_language = self.translated_languages[language][self.user_language]

					item = story["Information"]["Wattpad"][key][language]

					print("\t" + translated_language + ":")
					print("\t" + item)

					if language != list(story["Information"]["Wattpad"][key].keys())[-1]:
						print()

				if key != list(story["Information"]["Wattpad"].keys())[-1]:
					print()

		json_file = self.stories["folders"]["Database"]["root"]

		print()
		print(self.large_bar)

	def Register_Task(self, task_dictionary, register_task = True):
		if "type" not in task_dictionary:
			task_dictionary["type"] = "Stories"

		if "time" not in task_dictionary:
			task_dictionary["time"] = self.Date.Now()

		# Register task with Tasks module, Register_Task class
		if register_task == True:
			from Tasks.Register_Task import Register_Task as Register_Task

			Register_Task(task_dictionary)

		# Register task on Diary Slim if Tasks did not register the task on Diary Slim
		if register_task == False:
			print()

			Write_On_Diary_Slim_Module(task_dictionary["descriptions"][self.user_language], task_dictionary["time"], show_text = False)
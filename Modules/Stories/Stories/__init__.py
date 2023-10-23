# Stories.py

class Stories(object):
	def __init__(self, story = None):
		self.Define_Basic_Variables()

		# Define module folders
		from Utility.Define_Folders import Define_Folders as Define_Folders

		Define_Folders(self)

		self.Define_Texts()

		self.story = story

		self.Define_Social_Network_Variables()
		self.Define_Folders_And_Files()
		self.Define_Lists_And_Dictionaries()
		self.Define_Stories_Dictionary()

		if hasattr(self, "Select_Story") == False:
			from Stories.Select_Story import Select_Story as Select_Story

			self.Select_Story = Select_Story

	def Define_Basic_Variables(self):
		from Utility.Global_Switches import Global_Switches as Global_Switches

		from Utility.File import File as File
		from Utility.Folder import Folder as Folder
		from Utility.Date import Date as Date
		from Utility.Input import Input as Input
		from Utility.JSON import JSON as JSON
		from Utility.Text import Text as Text

		self.switches = Global_Switches().switches["Global"]

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
		self.links = self.Folder.links

		self.date = self.Date.date

	def Define_Texts(self):
		self.texts = self.JSON.To_Python(self.folders["apps"]["module_files"][self.module["key"]]["texts"])

		self.language_texts = self.JSON.Language.Item(self.texts)

		i = 0
		for item in self.language_texts["copy_actions, type: list"]:
			self.language_texts["copy_actions, type: list"][i] = "[" + self.language_texts["copy_actions, type: list"][i] + "]"

			i += 1

		self.large_bar = "-----"
		self.dash_space = "-"

	def Define_Social_Network_Variables(self):
		from Social_Networks.Social_Networks import Social_Networks as Social_Networks

		self.Social_Networks = Social_Networks()
		self.social_networks = self.Social_Networks.social_networks

		self.social_networks["Wattpad"]["profile"]["conversations"] = self.social_networks["Wattpad"]["profile"]["profile"] + "/conversations"
		self.social_networks["Wattpad"]["links"]["myworks"] = self.social_networks["Wattpad"]["links"]["link"] + "myworks/"

	def Define_Folders_And_Files(self):
		# Folders
		self.stories = {
			"Folders": {
				"root": self.folders["mega"]["stories"]["root"]
			}
		}

		# "Database" folder
		self.stories["Folders"]["Database"] = {
			"root": self.stories["Folders"]["root"] + "Database/"
		}

		self.Folder.Create(self.stories["Folders"]["Database"]["root"])

		# "Social Network post templates" folder
		self.stories["Folders"]["Database"]["Social Network post templates"] = {
			"root": self.stories["Folders"]["Database"]["root"] + "Social Network post templates/"
		}

		self.Folder.Create(self.stories["Folders"]["Database"]["Social Network post templates"]["root"])

		# Database files
		for file_name in ["Author", "Stories list", "Stories.json"]:
			key = file_name.split(".")[0]

			self.stories["Folders"]["Database"][key] = self.stories["Folders"]["Database"]["root"] + file_name

			if "json" not in file_name:
				self.stories["Folders"]["Database"][key] += ".txt"

			self.File.Create(self.stories["Folders"]["Database"][key])

		# Create the "Social Network post templates" files
		for item in ["Wattpad", "Twitter, Facebook"]:
			file_name = item

			self.stories["Folders"]["Database"]["Social Network post templates"][item] = self.stories["Folders"]["Database"]["Social Network post templates"]["root"] + file_name + ".json"
			self.File.Create(self.stories["Folders"]["Database"]["Social Network post templates"][item])

	def Define_Lists_And_Dictionaries(self):
		# Lists
		self.default_author = self.File.Contents(self.stories["Folders"]["Database"]["Author"])["lines"][0]

		# Dictionaries
		self.default_information_items = {
			self.JSON.Language.language_texts["creation_date"]: self.Date.Now()["Formats"]["DD/MM/YYYY"],
			self.JSON.Language.language_texts["author, title()"]: self.default_author
		}

		# Define the default dictionaries dictionary
		self.default_dictionaries = {
			"Pack": {
				"Theme": {
					"Colors": {
						"Text": "#",
						"Background": "#",
						"Highlight": "#"
					}
				},
				"Links": {
					"Websites": {
						"Grammarly": {
							"Link": "https://app.grammarly.com/"
						},
						"Google Translate": {
							"Link": "https://translate.google.com/"
						},
						"TimeAndDate": {
							"Link": "https://www.timeanddate.com/stopwatch/"
						}
					}
				},
				"Soundtrack": {
					"Soundtrack": {
						"First track": {
							"Type": "Playlist",
							"Source": "YouTube Embed",
							"ID": "[ID]",
							"Link": "https://www.youtube-nocookie.com/embed/videoseries?list={}"
						}
					}
				}
			}
		}

		# Define the soundtrack links dictionary
		self.soundtrack_links = {
			"YouTube Embed": {
				"Link": "https://www.youtube-nocookie.com/embed/videoseries?list={}"
			}
		}

	def Define_Stories_Dictionary(self):
		import collections
		from copy import deepcopy

		# Lists
		to_remove = [
			"Database",
			"Diary",
			"Diary Slim",
			"Izaque Sanvezzo",
			"Others",
			"Rubbish"
		]

		# List stories on stories folder
		self.stories["List"] = self.Folder.Contents(self.folders["mega"]["stories"]["root"])["folder"]["names"]
		self.stories["List"] = self.Folder.Remove_Folders(self.stories["List"], to_remove)

		# Update stories list file with new story names
		self.File.Edit(self.stories["Folders"]["Database"]["Stories list"], self.Text.From_List(self.stories["List"]), "w")

		# Story titles list
		self.stories["Titles"] = {}

		# Story number
		self.stories["Number"] = len(self.stories["List"])

		# Authors list
		self.stories["Authors"] = [
			self.default_author,
			"Júlia",
			"Ana"
		]

		# Add the stories to the Stories dictionary
		for story in self.stories["List"]:
			# Define the Story dictionary and keys
			self.stories[story] = {
				"Title": story,
				"Titles": {},
				"Folders": {
					"root": self.stories["Folders"]["root"] + story + "/"
				},
				"Information": {}
			}

			self.Folder.Create(self.stories[story]["Folders"]["root"])

			# Create the subfolders inside the story folder
			for folder in self.texts["folder_names, type: list"]:
				key = folder.lower()

				folder_name = folder.split("/")[-1]

				if folder_name == "":
					folder_name = folder.split("/")[-2]

				# Add root folder to folders dictionary
				self.stories[story]["Folders"][folder] = {
					"root": self.stories[story]["Folders"]["root"] + folder + "/"
				}

				# List contents of subfolder
				contents = self.Folder.Contents(self.stories[story]["Folders"][folder]["root"])

				# Add subfolders to folders dictionary
				for sub_folder in contents["folder"]["list"]:
					sub_folder_name = sub_folder.split("/")[-1]

					if sub_folder_name == "":
						sub_folder_name = sub_folder.split("/")[-2]

					self.stories[story]["Folders"][folder][sub_folder_name] = self.Folder.Sanitize(sub_folder)

				# Add files to folders dictionary
				for file in contents["file"]["list"]:
					file_name = file.split("/")[-1]

					if file_name == "":
						file_name = file.split("/")[-2]

					file_name = file_name.split(".")[0]

					if self.stories[story]["Folders"]["root"].count("/") + 1 == file.count("/"):
						self.stories[story]["Folders"][folder][file_name] = file

				for item in self.stories[story]["Folders"][folder]:
					if self.Folder.Exist(item) == True:
						self.Folder.Create(item)

					if self.File.Exist(item) == True:
						self.File.Create(item)

			# Create the cover folders
			folders = {
				"Websites": self.folders["mega"]["websites"]["images"]["story_covers"],
				"Photoshop": self.folders["art"]["photoshop"]["stories"],
				"Sony Vegas": self.folders["art"]["sony_vegas"]["story_covers"]
			}

			# Iterate through the cover folders dictionary to define and create them
			for name in folders:
				folder = folders[name]["root"]

				cover_folder = folder + story + "/"

				if self.Folder.Exist(cover_folder) == True:
					self.stories[story]["Folders"]["Covers"][name] = {
						"root": cover_folder
					}

					self.Folder.Create(cover_folder)

			# Add the "Obsidian's Vaults" folder
			self.stories[story]["Folders"]["Obsidian's Vaults"] = {
				"root": self.folders["mega"]["obsidian_s_vaults"]["creativity"]["literature"]["stories"]["root"] + story + "/"
			}

			self.Folder.Create(self.stories[story]["Folders"]["Obsidian's Vaults"]["root"])

			# Add the "Obsidian's Vaults" chapters folder
			self.stories[story]["Folders"]["Obsidian's Vaults"]["Chapters"] = {
				"root": self.stories[story]["Folders"]["Obsidian's Vaults"]["root"] + "Chapters/"
			}

			self.Folder.Create(self.stories[story]["Folders"]["Obsidian's Vaults"]["Chapters"]["root"])

			for language in self.languages["small"]:
				full_language = self.languages["full"][language]

				self.stories[story]["Folders"]["Obsidian's Vaults"]["Chapters"][full_language] = self.stories[story]["Folders"]["Obsidian's Vaults"]["Chapters"]["root"] + full_language + "/"
				self.Folder.Create(self.stories[story]["Folders"]["Obsidian's Vaults"]["Chapters"][full_language])	

			# Set the default author of the story
			# If the author is not inside the story information
			# Or the author is inside the story information and is empty
			if (
				"Author" not in self.stories[story]["Information"] or
				"Author" in self.stories[story]["Information"] and
				self.stories[story]["Information"]["Author"] == ""
			):
				self.stories[story]["Information"]["Author"] = self.default_author

			# Add the "Authors" key
			self.stories[story]["Information"]["Authors"] = [
				self.default_author
			]

			json_files = [
				"Information",
				"Chapters",
				"Pack",
				"Writing",
				"Titles",
				"Wattpad"
			]

			# Create the files on the "Information" folder
			for key in self.texts["file_names, type: list"]:
				file_name = key

				if key in json_files:
					file_name += ".json"

				if key not in json_files:
					file_name += ".txt"

				if (
					key != "Author" or
					key == "Author" and
					self.stories[story]["Information"]["Author"] != self.default_author
				):
					self.stories[story]["Folders"]["Information"][key] = self.stories[story]["Folders"]["Information"]["root"] + file_name

					file = self.stories[story]["Folders"]["Information"][key]

					self.File.Create(file)

					if (
						key in json_files and
						self.File.Contents(file)["lines"] == []
					):
						self.JSON.Edit(file, {})

			# Read the story Information from the files inside the "Information" folder
			for key in self.stories[story]["Folders"]["Information"]:
				item = self.stories[story]["Folders"]["Information"][key]

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

					if ".txt" in item:
						if key == "Chapter dates":
							print()
							print(key)
							print(self.stories[story]["Information"][key]["lines"])

						if (
							key == "Chapter dates" or
							key == "Author"
						):
							self.stories[story]["Information"][key] = self.stories[story]["Information"][key]["lines"]

						if key not in ["Chapter dates", "Author"]:
							self.stories[story]["Information"][key] = self.stories[story]["Information"][key]["string"]

						if len(self.stories[story]["Information"][key]) == 1:
							self.stories[story]["Information"][key] = [
								self.stories[story]["Information"][key][0]
							]

						if key == "Chapter dates":
							print(self.stories[story]["Information"][key])

					# Add the story titles to the root titles list
					if key == "Titles":
						# Add the language story titles
						for titles_key in self.stories[story]["Information"][key]:
							if titles_key not in self.stories["Titles"]:
								self.stories["Titles"][titles_key] = []

							self.stories["Titles"][titles_key].append(self.stories[story]["Information"][key][titles_key])

						if "All" not in self.stories["Titles"]:
							self.stories["Titles"]["All"] = []

			# Define the story titles
			self.stories[story]["Titles"] = self.stories[story]["Information"]["Titles"]

			# Update the "Authors" key

			# If the author is a list
			if type(self.stories[story]["Information"]["Author"]) == list:
				# Define the "Authors" as a list with authors
				self.stories[story]["Information"]["Authors"] = self.stories[story]["Information"]["Author"]

				authors = ""

				for author in self.stories[story]["Information"]["Authors"]:
					authors += author

					if author != self.stories[story]["Information"]["Authors"][-1]:
						authors += "\n"

				self.stories[story]["Information"]["Author"] = authors

			# Else, define the "Authors" as a list with the single author
			else:
				self.stories[story]["Information"]["Authors"] = [
					self.stories[story]["Information"]["Author"]
				]

			# Define the default story Chapters dictionary
			self.stories[story]["Information"]["Chapters"] = {
				"Number": 0,
				"Titles": {},
				"Dates": self.stories[story]["Information"]["Chapter dates"]
			}

			# Add the chapter titles files to the "Chapters" dictionary
			for language in self.languages["small"]:
				full_language = self.languages["full"][language]

				# Transform the language folder into a dictionary
				self.stories[story]["Folders"]["Chapters"][full_language] = {
					"root": self.stories[story]["Folders"]["Chapters"][full_language],
				}

				self.Folder.Create(self.stories[story]["Folders"]["Chapters"][full_language]["root"])

				# Add the chapter titles folder
				titles_text = self.JSON.Language.texts["titles, title()"][language]

				self.stories[story]["Folders"]["Chapters"][full_language][titles_text] = {
					"root": self.stories[story]["Folders"]["Chapters"][full_language]["root"] + titles_text + "/"
				}

				self.Folder.Create(self.stories[story]["Folders"]["Chapters"][full_language][titles_text]["root"])

				# Add the chapter titles file
				self.stories[story]["Folders"]["Chapters"][full_language][titles_text][titles_text] = self.stories[story]["Folders"]["Chapters"][full_language][titles_text]["root"] + titles_text + ".txt"

				self.File.Create(self.stories[story]["Folders"]["Chapters"][full_language][titles_text][titles_text])

				# Read the chapter titles file
				file = self.stories[story]["Folders"]["Chapters"][full_language][titles_text][titles_text]

				# Add the chapter titles to the Information dictionary
				self.stories[story]["Information"]["Chapters"]["Titles"][language] = self.File.Contents(file)["lines"]

			# Update the number of chapters
			self.stories[story]["Information"]["Chapters"]["Number"] = len(self.stories[story]["Information"]["Chapters"]["Titles"]["en"])

			# Remove the "Chapter dates" from the Information dictonary cause it is not used
			self.stories[story]["Information"].pop("Chapter dates")

			# Update the chapter number on the "Information.json" file
			information_file = self.stories[story]["Folders"]["Information"]["Information"]

			# Get the Information dictionary
			information = self.JSON.To_Python(information_file)

			# Add the Titles dictionary to the Information dictionary
			information = {
				"Titles": self.stories[story]["Titles"],
				**information
			}

			# Add the Chapters dictionary to the Information dictionary
			key_value = {
				"Chapters": {
					"Number": self.stories[story]["Information"]["Chapters"]["Number"]
				}
			}

			information.pop("Chapters")
			information = self.JSON.Add_Key_After_Key(information, key_value, after_key = "Status", number_to_add = 0)

			# Move some keys to the end of the dictionary
			for key in ["Website link name", "HEX color", "Universe_ID"]:
				if key in information:
					backup = information[key]

					information.pop(key)

					information[key] = backup

			# Update the "Information.json" file
			self.JSON.Edit(information_file, information)

			# Update the "Status" key inside the root Information dictionary
			self.stories[story]["Information"]["Status"] = information["Status"]

			# Remove the "Titles" key from the root Information dictionary
			self.stories[story]["Information"].pop("Titles")

			# Write into the "Chapters.json" file
			self.JSON.Edit(self.stories[story]["Folders"]["Information"]["Chapters"], self.stories[story]["Information"]["Chapters"])

			# Add the language synopsis from the synopsis folder inside the "Information" folder
			self.stories[story]["Folders"]["Information"]["Synopsis"] = {
				"root": self.stories[story]["Folders"]["Information"]["root"] + "Synopsis/"
			}

			self.Folder.Create(self.stories[story]["Folders"]["Information"]["Synopsis"]["root"])

			# Create the synopsis files
			for language in self.languages["small"]:
				full_language = self.languages["full"][language]

				self.stories[story]["Folders"]["Information"]["Synopsis"][full_language] = self.stories[story]["Folders"]["Information"]["Synopsis"]["root"] + full_language + ".txt"
				self.File.Create(self.stories[story]["Folders"]["Information"]["Synopsis"][full_language])

			self.stories[story]["Information"]["Synopsis"] = {}

			# Add the synopsis to the Information dictionary
			for language in self.languages["small"]:
				full_language = self.languages["full"][language]

				self.stories[story]["Information"]["Synopsis"][language] = self.File.Contents(self.stories[story]["Folders"]["Information"]["Synopsis"][full_language])["string"]

			# Define and create more story information files
			for name in ["Writing", "Pack"]:
				# Define the default dictionary for the "Writing.json" file
				if name == "Writing":
					dict_ = {}

					for writing_mode in self.texts["writing_modes, type: list"]["en"]:
						dict_[writing_mode] = {
							"Chapter": 0,
							"Times": {
								"First": "",
								"Last": ""
							}
						}

					self.stories[story]["Information"][name] = dict_

				# Define the default dictionary for the "Pack.json" file
				if name == "Pack":
					self.stories[story]["Information"][name] = deepcopy(self.default_dictionaries["Pack"])

				# If the file is not empty, get the dictionary from it
				if self.File.Contents(self.stories[story]["Folders"]["Information"][name])["lines"] != []:
					folder = self.stories[story]["Folders"]["Information"]

					file = folder[name]

					self.stories[story]["Information"][name] = self.JSON.To_Python(file)

				# Write the default or modified dictionary inside the file
				self.JSON.Edit(self.stories[story]["Folders"]["Information"][name], self.stories[story]["Information"][name])

				# If the name is "Pack"
				if name == "Pack":
					# Create the local "dict_" dictionary
					dict_ = {}

					# Iterate through each Pack dictionary key
					for key in self.default_dictionaries["Pack"]:
						# If the key is not in the current story Pack
						if key not in self.stories[story]["Information"]["Pack"]:
							# Define the local dictionary key as the default key inside the default dictionaries dictionary
							dict_[key] = deepcopy(self.default_dictionaries["Pack"][key])

						# If the key is inside the current story Pack
						else:
							# Redefine the key to be in the correct key order
							dict_[key] = self.stories[story]["Information"]["Pack"][key]

					# Define the current story Pack as the local "dict_" dictionay
					self.stories[story]["Information"]["Pack"] = deepcopy(dict_)

			print()
			print(self.stories[story]["Titles"][self.user_language] + ":")
			self.JSON.Show(self.stories[story]["Information"])
			input()

			# Define specific actions for the "Theme" key of the Pack dictionary
			colors = ""

			# Add each color HEX code to the "colors" string
			for color in self.stories[story]["Information"]["Pack"]["Theme"]["Colors"].values():
				colors += color

			# If the "colors" string is equal to "###", that means it is the default story Theme dictionary
			if colors == "###":
				import re

				hex_color_regex = "^#[A-Fa-f0-9]{6}$"

				# Iterate each color key in the Theme Colors dictionary
				for key in self.stories[story]["Information"]["Pack"]["Theme"]["Colors"]:
					# Ask for the HEX code of the color in the user language
					color = self.Input.Type(self.JSON.Language.language_texts[key.lower() + ", title()"])

					# Ensure that the "#" character is the first one of the HEX color code
					if color[0] != "#":
						color = "#" + color

					# Store the Regex result in a variable
					regex = re.search(hex_color_regex, color)

					# If and while the Regex result is equal to False (the color is not a valid HEX color)
					while bool(regex) == False:
						# Ask again, for the correct HEX code
						color = self.Input.Type(self.JSON.Language.language_texts[key.lower() + ", title()"])

						# Ensure that the "#" character is the first one of the HEX color code
						if color[0] != "#":
							color = "#" + color

						# Make the regex search again
						regex = re.search(hex_color_regex, color)

					# Define the color inside the Colors dictionary
					self.stories[story]["Information"]["Pack"]["Theme"]["Colors"][key] = color

				# Make a copy of the Pack dictionary to write on the "Pack.json" file
				dict_ = deepcopy(self.stories[story]["Information"]["Pack"])

				# Remove the "Links" key of the local Pack dictionary
				dict_.pop("Links")

				# Update the "Pack.json" file with the updated and local Pack dictionary
				self.JSON.Edit(self.stories[story]["Folders"]["Information"]["Pack"], dict_)

			# Create the empty Website dictionary
			self.stories[story]["Information"]["Website"] = {}

			website_folder = story

			# Add the custom website link name if it exists
			if "Parent story" in self.stories[story]["Information"]:
				parent_story = self.stories[story]["Information"]["Parent story"]

				website_folder = parent_story["Title"]

				if "Folder" in parent_story:
					website_folder = parent_story["Folder"]

				website_folder += "/" + story

				self.stories[story]["Information"]["Website"]["Link name"] = website_folder

			# Create the website "Link" key
			self.stories[story]["Information"]["Website"]["Link"] = self.links["Stake2 Website"] + website_folder + "/"

			# Add the story Wattpad link for each language
			link = self.social_networks["Wattpad"]["links"]["myworks"]

			for language in self.languages["small"]:
				if language in self.stories[story]["Information"]["Wattpad"]:					
					id = self.stories[story]["Information"]["Wattpad"][language]["ID"]

					self.stories[story]["Information"]["Wattpad"][language]["Link"] = link + id

			# Update the "Wattpad.json" file
			self.JSON.Edit(self.stories[story]["Folders"]["Information"]["Wattpad"], self.stories[story]["Information"]["Wattpad"])

			# Add all language titles of the story to the "mixed_titles" list
			for language in self.languages["small"]:
				story_title = self.stories[story]["Titles"][language]

				if story_title not in self.stories["Titles"]["All"]:
					self.stories["Titles"]["All"].append(story_title)

			# Get the readers of the story
			readers_list = self.File.Contents(self.stories[story]["Folders"]["Readers and Reads"]["Readers"])

			# Define the Readers dictionary
			self.stories[story]["Information"]["Readers"] = {
				"Number": readers_list["length"],
				"List": readers_list["lines"]
			}

			# Sort the keys of the "Information" dictionary
			self.stories[story]["Information"] = dict(collections.OrderedDict(sorted(self.stories[story]["Information"].items())))

		# Write the "Stories" dictionary to the "Stories.json" file
		self.JSON.Edit(self.stories["Folders"]["Database"]["Stories"], self.stories)

	def Cover_Folder_Name(self, chapter_number):
		chapter_number = int(chapter_number)

		folder_names = []

		# Create the list of numbers from 1 to 10
		numbers = list(range(1, 10 + 1))

		# Iterate through the list of numbers
		for number in numbers:
			number = str(number)

			# "1 - 10"
			if int(number) == 1:
				name = number + " - " + number + "0"

				folder_names.append(name)

			# "11 - 20" and so on
			name = number + "1" + " - " + str(int(number) + 1) + "0"

			folder_names.append(name)

		# Iterate through the list of folder names
		for item in folder_names:
			# Split the folder name
			# (1, 10) for example
			split = item.split(" - ")

			# Make the range of numbers for the folder name
			# [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
			range_list = list(range(int(split[0]), int(split[1]) + 1))

			# If the chapter number is in the range of numbers
			# Define the folder name to return as the current folder name
			if chapter_number in range_list:
				folder_name = item

		'''
		# Old code
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
		'''

		return folder_name

	def Register(self, task_dictionary, register_task = True):
		# If the type is not inside the task dictionary, set it as "Stories"
		if "Type" not in task_dictionary:
			task_dictionary["Type"] = "Stories"

		# If the date is not inside the task dictionary, set it as now
		if "Date" not in task_dictionary["Entry"]:
			task_dictionary["Entry"]["Date"] = self.Date.Now()

		# Register the task with the "Register" class of the "Tasks" module
		if register_task == True:
			import Tasks

			self.Tasks = Tasks()

			sef.Tasks.Register(task_dictionary)

		# Register the task on "Diary Slim" if the "Tasks" module did not
		if register_task == False:
			print()

			from Diary_Slim.Write_On_Diary_Slim_Module import Write_On_Diary_Slim_Module as Write_On_Diary_Slim_Module

			Write_On_Diary_Slim_Module(task_dictionary["Task"]["Descriptions"][self.user_language], self.task_dictionary["Date"]["Formats"]["HH:MM DD/MM/YYYY"], show_text = False)
# Stories.py

# Import the "importlib" module
import importlib

class Stories(object):
	def __init__(self):
		# Define the module folders
		from Utility.Define_Folders import Define_Folders as Define_Folders

		Define_Folders(self)

		# Module related methods
		self.Define_Basic_Variables()
		self.Define_Texts()

		# Import classes method
		self.Import_Classes()

		# Folders, files, lists, and dictionaries methods
		self.Define_Folders_And_Files()
		self.Define_Lists_And_Dictionaries()

		# Class methods
		self.Define_Social_Network_Variables()
		self.Cover_Folder_Name(1)
		self.Define_Stories_Dictionary()

	def Define_Basic_Variables(self):
		from copy import deepcopy

		# Import the JSON module
		from Utility.JSON import JSON as JSON

		self.JSON = JSON()

		# Get the modules list
		self.modules = self.JSON.To_Python(self.folders["apps"]["modules"]["modules"])

		# Create a list of the modules that will not be imported
		remove_list = [
			"Define_Folders",
			"Language",
			"JSON"
		]

		# Iterate through the Utility modules
		for module_title in self.modules["Utility"]["List"]:
			# If the module title is not inside the remove list
			if module_title not in remove_list:
				# Import the module
				module = importlib.import_module("." + module_title, "Utility")

				# Get the sub-class
				sub_class = getattr(module, module_title)

				# Add the sub-class to the current module
				setattr(self, module_title, sub_class())

		# Make a backup of the module folders
		self.module_folders = {}

		for item in ["modules", "module_files"]:
			self.module_folders[item] = deepcopy(self.folders["apps"][item][self.module["key"]])

		# Define the local folders dictionary as the Folder folders dictionary
		self.folders = self.Folder.folders

		self.links = self.Folder.links

		# Restore the backup of the module folders
		for item in ["modules", "module_files"]:
			self.folders["apps"][item][self.module["key"]] = self.module_folders[item]

		# Get the switches dictionary from the "Global Switches" module
		self.switches = self.Global_Switches.switches["Global"]

		# Get the Languages dictionary
		self.languages = self.JSON.Language.languages

		# Get the user language and full user language
		self.user_language = self.JSON.Language.user_language
		self.full_user_language = self.JSON.Language.full_user_language

		# Get the Sanitize method of the File class
		self.Sanitize = self.File.Sanitize

		# Get the current date from the Date module
		self.date = self.Date.date

	def Define_Texts(self):
		self.texts = self.JSON.To_Python(self.folders["apps"]["module_files"][self.module["key"]]["texts"])

		self.language_texts = self.JSON.Language.Item(self.texts)

		i = 0
		for item in self.language_texts["copy_actions, type: list"]:
			self.language_texts["copy_actions, type: list"][i] = "[" + self.language_texts["copy_actions, type: list"][i] + "]"

			i += 1

		# Define the "Separators" dictionary
		self.separators = {}

		# Create separators from one to ten characters
		for number in range(1, 11):
			# Define the empty string
			string = ""

			# Add separators to it
			while len(string) != number:
				string += "-"

			# Add the string to the Separators dictionary
			self.separators[str(number)] = string

	def Import_Classes(self):
		# Define the classes to be imported
		classes = [
			"Social_Networks"
		]

		# Import them
		for title in classes:
			# Import the module
			module = importlib.import_module("." + title, title)

			# Get the sub-class
			sub_class = getattr(module, title)

			# Add the sub-class to the current module
			setattr(self, title, sub_class())

	def Define_Social_Network_Variables(self):
		# Get the "social_networks" variable from the "Social_Networks" module
		self.social_networks = self.Social_Networks.social_networks

		# Define the "Wattpad" key for faster typing
		self.social_networks["Wattpad"] = self.social_networks["Dictionary"]["Wattpad"]

		# Define the additional links
		self.social_networks["Wattpad"]["Profile"]["Links"] = {
			"Conversations": self.social_networks["Wattpad"]["Profile"]["Links"]["Profile"] + "conversations/"
		}

		self.social_networks["Wattpad"]["Information"]["Links"] = {
			"My works": self.social_networks["Wattpad"]["Information"]["Link"] + "myworks/"
		}

	def Define_Folders_And_Files(self):
		# Define the root "Stories" dictionary
		self.stories = {
			"Folders": {
				"root": self.folders["Mega"]["stories"]["root"]
			}
		}

		# Define the "Database" folder
		self.stories["Folders"]["Database"] = {
			"root": self.stories["Folders"]["root"] + "Database/"
		}

		self.Folder.Create(self.stories["Folders"]["Database"]["root"])

		# Define the "Post templates" folder
		self.stories["Folders"]["Database"]["Post templates"] = {
			"root": self.stories["Folders"]["Database"]["root"] + "Post templates/"
		}

		self.Folder.Create(self.stories["Folders"]["Database"]["Post templates"]["root"])

		# Database files
		names = [
			"Author",
			"Stories list",
			"Stories.json"
		]

		for file_name in names:
			key = file_name.split(".")[0]

			self.stories["Folders"]["Database"][key] = self.stories["Folders"]["Database"]["root"] + file_name

			if "json" not in file_name:
				self.stories["Folders"]["Database"][key] += ".txt"

			self.File.Create(self.stories["Folders"]["Database"][key])

		# Create the "Post templates" folders

		# Define the root folder for faster typing
		folder = self.stories["Folders"]["Database"]["Post templates"]

		names = [
			"Wattpad",
			"Twitter, Facebook"
		]

		for folder_name in names:
			folder[folder_name] = {
				"root": folder["root"] + folder_name + "/"
			}

			self.Folder.Create(folder[folder_name]["root"])

		# Create the language files
		for folder_name in names:
			# Iterate through the small languages list
			for language in self.languages["small"]:
				# Get the full language
				full_language = self.languages["full"][language]

				# Define and create the language file
				folder[folder_name][language] = folder[folder_name]["root"] + full_language + ".txt"
				self.File.Create(folder[folder_name][language])

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
						"Text": {
							"Name": "",
							"Code": "#",
						},
						"Background": {
							"Name": "",
							"Code": "#",
						},
						"Highlight": {
							"Name": "",
							"Code": "#",
						}
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
			"Izaque Sanvezzo",
			"Others",
			"Rubbish"
		]

		# List stories on stories folder
		self.stories["List"] = self.Folder.Contents(self.folders["Mega"]["stories"]["root"])["folder"]["names"]
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
		for story_title in self.stories["List"]:
			# Define the Story dictionary and keys
			story = {
				"Title": story_title,
				"Titles": {},
				"Folders": {
					"root": self.stories["Folders"]["root"] + story_title + "/"
				},
				"Information": {}
			}

			self.Folder.Create(story["Folders"]["root"])

			# Create the subfolders inside the story folder
			for folder in self.texts["folder_names, type: list"]:
				key = folder.lower()

				folder_name = folder.split("/")[-1]

				if folder_name == "":
					folder_name = folder.split("/")[-2]

				# Add root folder to folders dictionary
				story["Folders"][folder] = {
					"root": story["Folders"]["root"] + folder + "/"
				}

				# List contents of subfolder
				contents = self.Folder.Contents(story["Folders"][folder]["root"])

				# Add subfolders to folders dictionary
				for sub_folder in contents["folder"]["list"]:
					sub_folder_name = sub_folder.split("/")[-1]

					if sub_folder_name == "":
						sub_folder_name = sub_folder.split("/")[-2]

					story["Folders"][folder][sub_folder_name] = self.Folder.Sanitize(sub_folder)

				# Add files to folders dictionary
				for file in contents["file"]["list"]:
					file_name = file.split("/")[-1]

					if file_name == "":
						file_name = file.split("/")[-2]

					file_name = file_name.split(".")[0]

					if story["Folders"]["root"].count("/") + 1 == file.count("/"):
						story["Folders"][folder][file_name] = file

				for item in story["Folders"][folder]:
					if self.Folder.Exist(item) == True:
						self.Folder.Create(item)

					if self.File.Exist(item) == True:
						self.File.Create(item)

			# Add the "Obsidian's Vaults" folder
			story["Folders"]["Obsidian's Vaults"] = {
				"root": self.folders["Mega"]["Obsidian's Vaults"]["Creativity"]["Literature"]["Stories"]["root"] + story_title + "/"
			}

			self.Folder.Create(story["Folders"]["Obsidian's Vaults"]["root"])

			# Add the "Obsidian's Vaults" chapters folder
			story["Folders"]["Obsidian's Vaults"]["Chapters"] = {
				"root": story["Folders"]["Obsidian's Vaults"]["root"] + "Chapters/"
			}

			self.Folder.Create(story["Folders"]["Obsidian's Vaults"]["Chapters"]["root"])

			for language in self.languages["small"]:
				full_language = self.languages["full"][language]

				story["Folders"]["Obsidian's Vaults"]["Chapters"][full_language] = story["Folders"]["Obsidian's Vaults"]["Chapters"]["root"] + full_language + "/"
				self.Folder.Create(story["Folders"]["Obsidian's Vaults"]["Chapters"][full_language])	

			# Set the default author of the story
			# If the author is not inside the story information
			# Or the author is inside the story information and is empty
			if (
				"Author" not in story["Information"] or
				"Author" in story["Information"] and
				story["Information"]["Author"] == ""
			):
				story["Information"]["Author"] = self.default_author

			# Add the "Authors" key
			story["Information"]["Authors"] = [
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
					story["Information"]["Author"] != self.default_author
				):
					story["Folders"]["Information"][key] = story["Folders"]["Information"]["root"] + file_name

					file = story["Folders"]["Information"][key]

					self.File.Create(file)

					if (
						key in json_files and
						self.File.Contents(file)["lines"] == []
					):
						self.JSON.Edit(file, {})

			# Read the story Information from the files inside the "Information" folder
			for key in story["Folders"]["Information"]:
				item = story["Folders"]["Information"][key]

				if self.File.Exist(item) == True:
					function = self.File.Contents

					if ".json" in item:
						function = self.JSON.To_Python

					information = function(item)

					if key != "Information":
						story["Information"][key] = information

					if key == "Information":
						for sub_key in information:
							story["Information"][sub_key] = information[sub_key]

					if ".txt" in item:
						if (
							key == "Chapter dates" or
							key == "Author"
						):
							story["Information"][key] = story["Information"][key]["lines"]

						if key not in ["Chapter dates", "Author"]:
							story["Information"][key] = story["Information"][key]["string"]

						if len(story["Information"][key]) == 1:
							story["Information"][key] = [
								story["Information"][key][0]
							]

					# Add the story titles to the root titles list
					if key == "Titles":
						# Add the language story titles
						for titles_key in story["Information"][key]:
							if titles_key not in self.stories["Titles"]:
								self.stories["Titles"][titles_key] = []

							self.stories["Titles"][titles_key].append(story["Information"][key][titles_key])

						if "All" not in self.stories["Titles"]:
							self.stories["Titles"]["All"] = []

			# Define the story titles
			story["Titles"] = story["Information"]["Titles"]

			# Create the cover folders
			folders = {
				"Websites": self.folders["Mega"]["Websites"]["Images"],
				"Photoshop": self.folders["Art"]["Photoshop"]["Stories"],
				"Sony Vegas": self.folders["Art"]["Sony Vegas"]["Story covers"]
			}

			# Iterate through the cover folders dictionary to define and create them
			for name in folders:
				folder = folders[name]["root"]

				cover_folder = folder

				if name != "Photoshop":
					cover_folder += story_title + "/"

				if name == "Photoshop":
					cover_folder += story["Titles"][self.user_language] + "/"

				if self.Folder.Exist(cover_folder) == True:
					story["Folders"]["Covers"][name] = {
						"root": cover_folder
					}

					self.Folder.Create(cover_folder)

			# Add the sub-folders of the "Websites" cover folder
			sub_folders = [
				"Chapters"
			]

			for folder in sub_folders:
				story["Folders"]["Covers"]["Websites"][folder] = {
					"root": story["Folders"]["Covers"]["Websites"]["root"] + folder + "/"
				}

			# Define the language folders
			for language in self.languages["small"]:
				full_language = self.languages["full"][language]

				folder = story["Folders"]["Covers"]["Websites"]["root"] + full_language + "/"

				if self.Folder.Exist(folder) == True:
					story["Folders"]["Covers"]["Websites"][language] = {
						"root": folder
					}

				if "Photoshop" in story["Folders"]["Covers"]:
					folder = story["Folders"]["Covers"]["Photoshop"]["root"] + full_language + "/"

					if self.Folder.Exist(folder) == True:
						story["Folders"]["Covers"]["Photoshop"][language] = {
							"root": folder
						}

			# Define the chapter folders
			for language in self.languages["small"]:
				if language in story["Folders"]["Covers"]["Websites"]:
					root_folder = story["Folders"]["Covers"]["Websites"][language]["root"]

					for folder_name in self.folder_names:
						folder = root_folder + folder_name + "/"

						if self.Folder.Exist(folder) == True:
							story["Folders"]["Covers"]["Websites"][language][folder_name] = {
								"root": folder
							}

			# Update the "Authors" key

			# If the author is a list
			if type(story["Information"]["Author"]) == list:
				# Define the "Authors" as a list with authors
				story["Information"]["Authors"] = story["Information"]["Author"]

				authors = ""

				for author in story["Information"]["Authors"]:
					authors += author

					if author != story["Information"]["Authors"][-1]:
						authors += "\n"

				story["Information"]["Author"] = authors

			# Else, define the "Authors" as a list with the single author
			else:
				story["Information"]["Authors"] = [
					story["Information"]["Author"]
				]

			# Define the default story Chapters dictionary
			story["Information"]["Chapters"] = {
				"Number": 0,
				"Titles": {},
				"Dates": story["Information"]["Chapter dates"]
			}

			# Add the chapter titles files to the "Chapters" dictionary
			for language in self.languages["small"]:
				full_language = self.languages["full"][language]

				# Transform the language folder into a dictionary
				story["Folders"]["Chapters"][full_language] = {
					"root": story["Folders"]["Chapters"][full_language],
				}

				self.Folder.Create(story["Folders"]["Chapters"][full_language]["root"])

				# Add the chapter titles folder
				titles_text = self.JSON.Language.texts["titles, title()"][language]

				story["Folders"]["Chapters"][full_language][titles_text] = {
					"root": story["Folders"]["Chapters"][full_language]["root"] + titles_text + "/"
				}

				self.Folder.Create(story["Folders"]["Chapters"][full_language][titles_text]["root"])

				# Add the chapter titles file
				story["Folders"]["Chapters"][full_language][titles_text][titles_text] = story["Folders"]["Chapters"][full_language][titles_text]["root"] + titles_text + ".txt"

				self.File.Create(story["Folders"]["Chapters"][full_language][titles_text][titles_text])

				# Read the chapter titles file
				file = story["Folders"]["Chapters"][full_language][titles_text][titles_text]

				# Add the chapter titles to the Information dictionary
				story["Information"]["Chapters"]["Titles"][language] = self.File.Contents(file)["lines"]

			# Update the number of chapters
			story["Information"]["Chapters"]["Number"] = len(story["Information"]["Chapters"]["Titles"]["en"])

			# Remove the "Chapter dates" from the Information dictonary cause it is not used
			story["Information"].pop("Chapter dates")

			# Update the chapter number on the "Information.json" file
			information_file = story["Folders"]["Information"]["Information"]

			# Get the Information dictionary
			information = self.JSON.To_Python(information_file)

			# Add the Titles dictionary to the Information dictionary
			information = {
				"Titles": story["Titles"],
				**information
			}

			# Add the Chapters dictionary to the Information dictionary, with only the chapters number
			key_value = {
				"Chapters": {
					"Number": story["Information"]["Chapters"]["Number"]
				}
			}

			# Remove the Chapters dictionary
			information.pop("Chapters")

			# Add it again at the end of the Information dictionary
			information = self.JSON.Add_Key_After_Key(information, key_value, after_key = "Status", number_to_add = 0)

			# Move some keys to the end of the dictionary
			for key in ["HEX color", "Universe_ID"]:
				if key in information:
					backup = information[key]

					information.pop(key)

					information[key] = backup

			# Add the "Last posted chapter" key
			key_value = {
				"Last posted chapter": story["Information"]["Chapters"]["Number"]
			}

			information["Chapters"] = self.JSON.Add_Key_After_Key(information["Chapters"], key_value, after_key = "Number")

			story["Information"]["Chapters"] = self.JSON.Add_Key_After_Key(story["Information"]["Chapters"], key_value, after_key = "Number")

			# Update the "Information.json" file
			self.JSON.Edit(information_file, information)

			# Update the "Status" key inside the root Information dictionary
			story["Information"]["Status"] = information["Status"]

			# Remove the "Titles" key from the root Information dictionary
			story["Information"].pop("Titles")

			# Write into the "Chapters.json" file
			self.JSON.Edit(story["Folders"]["Information"]["Chapters"], story["Information"]["Chapters"])

			# Add the language synopsis from the synopsis folder inside the "Information" folder
			story["Folders"]["Information"]["Synopsis"] = {
				"root": story["Folders"]["Information"]["root"] + "Synopsis/"
			}

			self.Folder.Create(story["Folders"]["Information"]["Synopsis"]["root"])

			# Create the synopsis files
			for language in self.languages["small"]:
				full_language = self.languages["full"][language]

				story["Folders"]["Information"]["Synopsis"][full_language] = story["Folders"]["Information"]["Synopsis"]["root"] + full_language + ".txt"
				self.File.Create(story["Folders"]["Information"]["Synopsis"][full_language])

			story["Information"]["Synopsis"] = {}

			# Add the synopsis to the Information dictionary
			for language in self.languages["small"]:
				full_language = self.languages["full"][language]

				story["Information"]["Synopsis"][language] = self.File.Contents(story["Folders"]["Information"]["Synopsis"][full_language])["string"]

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

					story["Information"][name] = dict_

				# Define the default dictionary for the "Pack.json" file
				if name == "Pack":
					story["Information"][name] = deepcopy(self.default_dictionaries["Pack"])

				# If the file is not empty, get the dictionary from it
				if self.File.Contents(story["Folders"]["Information"][name])["lines"] != []:
					folder = story["Folders"]["Information"]

					file = folder[name]

					story["Information"][name] = self.JSON.To_Python(file)

				# If the name is "Pack"
				if name == "Pack":
					# Create the local "dict_" dictionary
					dict_ = {}

					# Iterate through each Pack dictionary key
					for key in self.default_dictionaries["Pack"]:
						# If the key is not in the current story Pack
						if key not in story["Information"]["Pack"]:
							# Define the local dictionary key as the default key inside the default dictionaries dictionary
							dict_[key] = deepcopy(self.default_dictionaries["Pack"][key])

						# If the key is inside the current story Pack
						else:
							# Redefine the key to be in the correct key order
							dict_[key] = story["Information"]["Pack"][key]

					# Define the current story Pack as the local "dict_" dictionay
					story["Information"]["Pack"] = deepcopy(dict_)

				# Write the default or modified dictionary inside the file
				self.JSON.Edit(story["Folders"]["Information"][name], story["Information"][name])

			# Create the empty Website dictionary
			story["Information"]["Website"] = {}

			website_folder = story_title

			# Add the custom website link name if it exists
			if "Parent story" in story["Information"]:
				parent_story = story["Information"]["Parent story"]

				website_folder = parent_story["Title"]

				if "Folder" in parent_story:
					website_folder = parent_story["Folder"]

				website_folder += "/" + story_title

				story["Information"]["Website"]["Link name"] = website_folder

			# Create the website "Link" key
			story["Information"]["Website"]["Link"] = self.links["Stake2 Website"] + website_folder + "/"

			# Add the story Wattpad link for each language
			link = self.social_networks["Wattpad"]["Information"]["Links"]["My works"]

			for language in self.languages["small"]:
				if language in story["Information"]["Wattpad"]:					
					id = story["Information"]["Wattpad"][language]["ID"]

					story["Information"]["Wattpad"][language]["Link"] = link + id

			# Update the "Wattpad.json" file
			self.JSON.Edit(story["Folders"]["Information"]["Wattpad"], story["Information"]["Wattpad"])

			# Add all language titles of the story to the "mixed_titles" list
			for language in self.languages["small"]:
				local_story_title = story["Titles"][language]

				if local_story_title not in self.stories["Titles"]["All"]:
					self.stories["Titles"]["All"].append(local_story_title)

			# Get the readers of the story
			readers_list = self.File.Contents(story["Folders"]["Readers and Reads"]["Readers"])

			# Define the Readers dictionary
			story["Information"]["Readers"] = {
				"Number": readers_list["length"],
				"List": readers_list["lines"]
			}

			# Sort the keys of the "Information" dictionary
			story["Information"] = dict(collections.OrderedDict(sorted(story["Information"].items())))

			self.stories[story_title] = story

		# Write the "Stories" dictionary to the "Stories.json" file
		self.JSON.Edit(self.stories["Folders"]["Database"]["Stories"], self.stories)

	def Cover_Folder_Name(self, chapter_number):
		# Transform the chapter number into an int
		chapter_number = int(chapter_number)

		# Define the empty folder names list
		self.folder_names = []

		# Create the list of numbers from 1 to 10
		numbers = list(range(1, 10 + 1))

		# Iterate through the list of numbers
		for number in numbers:
			number = str(number)

			# "1 - 10"
			if int(number) == 1:
				name = number + " - " + number + "0"

				if name not in self.folder_names:
					self.folder_names.append(name)

			# "11 - 20" and so on
			name = number + "1" + " - " + str(int(number) + 1) + "0"

			if name not in self.folder_names:
				self.folder_names.append(name)

		# Iterate through the list of folder names
		for item in self.folder_names:
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

		return folder_name

	def Register_Task(self, task_dictionary, register_task = True):
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

	def Select_Story(self, select_text_parameter = None, select_class = False):
		from copy import deepcopy

		# Define the show text
		show_text = self.language_texts["stories, title()"]

		# Define the select text
		select_text = select_text_parameter

		if select_text_parameter == None:
			select_text = self.language_texts["select_a_story"]

		# Get the class name
		class_name = type(self).__name__.lower()

		# If the select text parameter is None
		# And the current class is a sub-class of the "Stories" class
		# And the class name is inside the language texts dictionary
		if (
			select_text_parameter == None and
			issubclass(type(self), Stories) == True and
			class_name in self.language_texts
		):
			# Change the select text to add the text of the current class
			select_text = self.language_texts["select_a_story_to"] + " " + self.language_texts[class_name]

		# Make a local copy of the "Stories" dictionary
		stories = deepcopy(self.stories)

		# Remove the stories with all chapters posted if the class is "Post"
		if class_name == "post":
			for story in deepcopy(self.stories["Titles"]["en"]):
				story = stories[story]

				post = story["Information"]["Chapter status"]["Post"]

				if int(post) == len(story["Information"]["Chapters"]["Titles"][self.user_language]):
					for language in self.languages["small"]:
						stories["Titles"][language].remove(story["Information"]["Titles"][language])

		self.option = self.Input.Select(stories["Titles"]["en"], language_options = stories["Titles"][self.user_language], show_text = show_text, select_text = select_text)["option"]

		self.story = self.stories[self.option]

		setattr(Stories, "story", self.story)

		if select_class == True:
			self.Select_Class()

		return self.story

	def Select_Class(self):
		classes = [
			"Write",
			"Post",
			"Manage"
		]

		class_descriptions = []

		for class_ in classes:
			class_description = self.JSON.Language.language_texts[class_.lower() + ", title()"]

			class_descriptions.append(class_description)

		# Select the class
		show_text = self.language_texts["what_to_do_with_the_story"] + " " + '"' + self.story["Titles"][self.user_language] + '"'

		class_ = self.Input.Select(classes, language_options = class_descriptions, show_text = show_text, select_text = self.JSON.Language.language_texts["select_one_thing_to_do"])["option"]

		# Get the module
		module = importlib.import_module("." + class_, "Stories")

		# Get the class
		class_ = getattr(module, class_)

		# Add the "Story" variable to the class
		setattr(class_, "story", self.story)

		# Execute the class
		class_()
# Stories.py

# Import the "importlib" module
import importlib
from copy import deepcopy

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

		# Define the Social Network variables
		self.Define_Social_Network_Variables()

		# Define the cover folder names list
		self.Define_Cover_Folder_Names()

		# Define the "Stories" dictionary
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
		# Get the "Social Networks" dictionary from the "Social_Networks" module
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

		# Define the root files
		names = {
			"Stories.json": "",
			"Stories list": self.language_texts["stories_list"],
			"Authors list": self.JSON.Language.language_texts["authors_list"]
		}

		# Iterate through the items inside the names dictionary
		for key, file_name in names.items():
			# If the file name is an empty string, define it as the key
			if file_name == "":
				file_name = key

			# Split the key to remove possible extensions
			key = key.split(".")[0]

			# Define the file with the root folder and file name
			file = self.stories["Folders"]["root"] + file_name

			# If the "json" extension is not in the file name, add the "txt" extension
			if ".json" not in file_name:
				file += ".txt"

			# Add the file to the "Folders" dictionary
			self.stories["Folders"][key] = file

			# Create the file
			self.File.Create(self.stories["Folders"][key])

		# Define the "Database" folder
		self.stories["Folders"]["Database"] = {
			"root": self.stories["Folders"]["root"] + self.JSON.Language.language_texts["database, title()"] + "/"
		}

		self.Folder.Create(self.stories["Folders"]["Database"]["root"])

		# Define the "Post templates" folder
		self.stories["Folders"]["Database"]["Post templates"] = {
			"root": self.stories["Folders"]["Database"]["root"] + "Post templates/"
		}

		self.Folder.Create(self.stories["Folders"]["Database"]["Post templates"]["root"])

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

		# Define the "Database" files
		names = [
			"Authors.json"
		]

		# Iterate through the file names list
		for file_name in names:
			# Split the file name to remove possible extensions
			key = file_name.split(".")[0]

			# Define the file with the root folder and file name
			file = self.stories["Folders"]["Database"]["root"] + file_name

			# Add the file to the "Database" folders dictionary
			self.stories["Folders"]["Database"][key] = file

			# Create the file
			self.File.Create(self.stories["Folders"]["Database"][key])

	def Define_Lists_And_Dictionaries(self):
		# Define the "Default dictionaries" dictionary
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
						"TimeAndDate": {
							"Link": "https://www.timeanddate.com/stopwatch/"
						},
						"Google Translate": {
							"Link": "https://translate.google.com/"
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

		# Define the "Soundtrack links" dictionary
		self.soundtrack_links = {
			"YouTube Embed": {
				"Link": "https://www.youtube-nocookie.com/embed/videoseries?list={}"
			}
		}

	def Define_Stories_Dictionary(self):
		import collections

		# Define the "Folder and file names" dictionary
		self.stories["Directory names"] = {
			"Folders": [
				"Chapters",
				"Comments",
				"Covers",
				"Information",
				"Lore",
				"Readers and reads"
			],
			"Files": [
				"Author",
				"Creation date",
				"Chapters",
				"Writing",
				"Wattpad"
			],
			"Sub-files": {
				"Covers": [
					"Landscape",
					"Portrait",
					"Resources"
				]
			}
		}

		# ----- #

		# Get the story authors
		self.stories["Authors"] = {
			"Number": 0,
			"List": self.File.Contents(self.stories["Folders"]["Authors list"])["lines"]
		}

		# Define the number of authors
		self.stories["Authors"]["Number"] = len(self.stories["Authors"]["List"])

		# Write the "Authors" dictionary to the database "Authors.json" file
		self.JSON.Edit(self.stories["Folders"]["Database"]["Authors"], self.stories["Authors"])

		# Define the first author
		self.stories["Author"] = self.stories["Authors"]["List"][0]

		# ----- #

		# Define the empty story "Numbers" dictionary
		self.stories["Numbers"] = {}

		# Get the list of stories
		self.stories["List"] = self.JSON.To_Python(self.stories["Folders"]["Stories"])["List"]

		# Update the "Total" key of the "Numbers" dictionary
		self.stories["Numbers"]["Total"] = len(self.stories["List"])

		# Define the "Titles" dictionary and get the story titles
		self.stories["Titles"] = {
			"en": self.stories["List"]
		}

		# Define the language titles
		self.stories["Titles"][self.user_language] = self.File.Contents(self.stories["Folders"]["Stories list"])["lines"]
		self.stories["Titles"]["Language"] = self.stories["Titles"][self.user_language]

		# Define the "All" list
		self.stories["Titles"]["All"] = self.stories["Titles"][self.user_language] + self.stories["Titles"]["en"]

		# Define the "Dictionary" dictionary
		self.stories["Dictionary"] = {}

		# Add the stories to the "Stories" dictionary
		s = 0
		for story_title in self.stories["List"]:
			# Get the language story title
			language_story_title = self.stories["Titles"]["Language"][s]

			# Define the "Story" dictionary and the keys
			story = {
				"Title": story_title,
				"Titles": {},
				"Folders": {
					"root": self.stories["Folders"]["root"] + language_story_title + "/"
				},
				"Information": {}
			}

			# Create the root story folder
			self.Folder.Create(story["Folders"]["root"])

			# Create the sub-folders inside the story folder
			for folder in self.stories["Directory names"]["Folders"]:
				# Add the root folder to the "Folders" dictionary
				story["Folders"][folder] = {
					"root": story["Folders"]["root"] + folder + "/"
				}

				# Create the root folder
				self.Folder.Create(story["Folders"][folder]["root"])

				# List the contents of the sub-folder
				contents = self.Folder.Contents(story["Folders"][folder]["root"])

				# Add the sub-folders to "Folders" dictionary
				for sub_folder in contents["folder"]["list"]:
					sub_folder_name = sub_folder.split("/")[-1]

					if sub_folder_name == "":
						sub_folder_name = sub_folder.split("/")[-2]

					story["Folders"][folder][sub_folder_name] = self.Folder.Sanitize(sub_folder)

			# ---------- #

			# Create the language folders on the "Chapters" folder
			for language in self.languages["small"]:
				# Get the full language
				full_language = self.languages["full"][language]

				# Define the language folder
				story["Folders"]["Chapters"][full_language] = {
					"root": story["Folders"]["Chapters"]["root"] + full_language + "/"
				}

				# Create the folder
				self.Folder.Create(story["Folders"]["Chapters"][full_language]["root"])

			# ---------- #

			# Define the story "Story.json" file
			story["Folders"]["Story"] = story["Folders"]["root"] + "Story.json"
			self.File.Create(story["Folders"]["Story"])

			# Read the "Story.json" file if it is not empty
			if self.File.Contents(story["Folders"]["Story"])["lines"] != []:
				story["Information"] = self.JSON.To_Python(story["Folders"]["Story"])

			# Define the story "Story information.txt" file
			story["Folders"]["Story information"] = story["Folders"]["root"] + self.language_texts["story_information"] + ".txt"
			self.File.Create(story["Folders"]["Story information"])

			# ---------- #

			# Define the chapter "Dates.txt" file
			file_name = self.JSON.Language.language_texts["dates, title()"]

			story["Folders"]["Chapters"]["Dates"] = story["Folders"]["Chapters"]["root"] + file_name + ".txt"
			self.File.Create(story["Folders"]["Chapters"]["Dates"])

			# ---------- #

			# Define the story "Readers.txt" file
			story["Folders"]["Readers and reads"]["Readers"] = story["Folders"]["Readers and reads"]["root"] + "Readers.txt"
			self.File.Create(story["Folders"]["Readers and reads"]["Readers"])

			# ---------- #

			# Set the default author of the story
			# If the author is not inside the story information
			# Or the author is inside the story information and is empty
			if (
				"Author" not in story["Information"] or
				"Author" in story["Information"] and
				story["Information"]["Author"] == ""
			):
				story["Information"]["Author"] = self.stories["Author"]

			# Add the "Authors" key
			story["Information"]["Authors"] = [
				self.stories["Author"]
			]

			# ---------- #

			json_files = [
				"Information",
				"Chapters",
				"Writing",
				"Titles",
				"Wattpad",
				"Story"
			]

			# Create the files on the "Information" folder
			for key in self.stories["Directory names"]["Files"]:
				file_name = key

				if key in json_files:
					file_name += ".json"

				if key not in json_files:
					file_name += ".txt"

				if (
					key != "Author" or
					key == "Author" and
					story["Information"]["Author"] != self.stories["Author"]
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
						if key == "Author":
							story["Information"][key] = story["Information"][key]["lines"]

						if key != "Author":
							story["Information"][key] = story["Information"][key]["string"]

						if len(story["Information"][key]) == 1:
							story["Information"][key] = [
								story["Information"][key][0]
							]

			# ---------- #

			# Define the story titles
			story["Titles"] = story["Information"]["Titles"]

			# Create the cover folders
			folders = {
				"Websites": self.folders["Mega"]["Websites"]["Images"],
				"Photoshop": self.folders["Art"]["Photoshop"]["Stories"]
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

			# ---------- #

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

			# ---------- #

			# Define the default story Chapters dictionary
			story["Information"]["Chapters"] = {
				"Number": 0,
				"Titles": {},
				"Dates": self.File.Contents(story["Folders"]["Chapters"]["Dates"])["lines"]
			}

			# Add the chapter titles files to the "Chapters" dictionary
			for language in self.languages["small"]:
				full_language = self.languages["full"][language]

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

			# Add the "Last posted chapter" key
			key_value = {
				"Last posted chapter": story["Information"]["Chapters"]["Number"]
			}

			story["Information"]["Chapters"] = self.JSON.Add_Key_After_Key(story["Information"]["Chapters"], key_value, after_key = "Number")

			# ---------- #

			# Write the "Chapters" dictionary into the "Chapters.json" file
			self.JSON.Edit(story["Folders"]["Information"]["Chapters"], story["Information"]["Chapters"])

			# ---------- #

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

			# ---------- #

			# Define the default dictionary for the "Writing.json" file
			writing = {}

			for writing_mode in self.texts["writing_modes, type: list"]["en"]:
				writing[writing_mode] = {
					"Chapter": 0,
					"Times": {
						"First": "",
						"Last": ""
					}
				}

			# Read the "Writing.json" file if it is not empty
			if self.File.Contents(story["Folders"]["Information"]["Writing"])["lines"] != []:
				writing = self.JSON.To_Python(story["Folders"]["Information"]["Writing"])

			story["Information"]["Writing"] = writing

			# Write the default or modified "Writing" dictionary inside the "Writing.json" file
			self.JSON.Edit(story["Folders"]["Information"]["Writing"], story["Information"]["Writing"])

			# ---------- #

			# If the "Pack" dictionary does not exist
			if "Pack" not in story["Information"]:
				# Define the default "Pack" dictionary
				story["Information"]["Pack"] = deepcopy(self.default_dictionaries["Pack"])

				# Remove the "Links" key of the "Pack" dictionary
				story["Information"]["Pack"].pop("Links")

				# Create the local "Pack" dictionary
				pack = {}

				# Iterate through each "Pack" dictionary key
				for key in self.default_dictionaries["Pack"]:
					# If the key is not in the current story Pack
					if key not in story["Information"]["Pack"]:
						# Define the local dictionary key as the default key inside the default dictionaries dictionary
						pack[key] = deepcopy(self.default_dictionaries["Pack"][key])

					# If the key is inside the current story Pack
					else:
						# Redefine the key to be in the correct key order
						pack[key] = story["Information"]["Pack"][key]

				# Define the current story Pack as the local "Pack" dictionay
				story["Information"]["Pack"] = deepcopy(pack)

			# ---------- #

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

			# ---------- #

			# Add the story Wattpad link for each language
			link = self.social_networks["Wattpad"]["Information"]["Links"]["My works"]

			for language in self.languages["small"]:
				if language in story["Information"]["Wattpad"]:					
					id = story["Information"]["Wattpad"][language]["ID"]

					story["Information"]["Wattpad"][language]["Link"] = link + id

			# Update the "Wattpad.json" file
			self.JSON.Edit(story["Folders"]["Information"]["Wattpad"], story["Information"]["Wattpad"])

			# ---------- #

			# Get the readers of the story
			readers_list = self.File.Contents(story["Folders"]["Readers and reads"]["Readers"])

			# Define the Readers dictionary
			story["Information"]["Readers"] = {
				"Number": readers_list["length"],
				"List": readers_list["lines"]
			}

			# ---------- #

			# Change the order of the keys inside the "Information" dictionary

			# Define the copy dictionary
			copy = {}

			# Define the list and order of the keys
			keys = [
				"Titles",
				"Chapters",
				"Creation date",
				"Status",
				"Synopsis",
				"Author",
				"Authors",
				"Readers",
				"Pack",
				"Writing",
				"Website",
				"Wattpad"
			]

			# Iterate through the list of keys
			k = 0
			for key in keys:
				# Copy the value of the key
				copy[key] = story["Information"][key]

				# Remove it from the "Information" dictionary
				story["Information"].pop(key)

				# Define the key value dictionary
				key_value = {
					key: copy[key]
				}

				# If the key is the first one
				if key == keys[0]:
					# Define the after key as "Author" (the default first key)
					# And the number to add as zero, to add the key before the "Author" key
					after_key = "Author"
					number_to_add = 0

				# If the key is not the first one
				if key != keys[0]:
					# Define the key as the key that existed before
					after_key = keys[k - 1]

					# And the number to add as one, to add the key after the key above
					number_to_add = 1

				# Add the key to the "Information" dictionary on the correct position
				story["Information"] = self.JSON.Add_Key_After_Key(story["Information"], key_value, after_key = after_key, number_to_add = number_to_add)

				k += 1

			# ---------- #

			# Update the "Story.json" file with the updated story "Information" dictionary
			self.JSON.Edit(story["Folders"]["Story"], story["Information"])

			# Add the "Story" dictionary to the root "Stories" dictionary
			self.stories["Dictionary"][story_title] = story

			# Add one to the "s" number variable
			s += 1

		# Make a copy of the "Stories" dictionary
		stories_dictionary = deepcopy(self.stories)

		# Remove the unneeded keys
		keys = [
			"Folders",
			"Directory names"
		]

		for key in keys:
			stories_dictionary.pop(key)

		# Write the updated local "Stories" dictionary to the "Stories.json" file
		self.JSON.Edit(self.stories["Folders"]["Stories"], stories_dictionary)

	def Define_Cover_Folder_Names(self):
		# Define the empty folder names list
		self.folder_names = []

		# Create the list of numbers from 1 to 10
		numbers = list(range(1, 10 + 1))

		# Iterate through the list of numbers
		for number in numbers:
			# Ensure the number is a string
			number = str(number)

			# "1 - 10" file range
			if int(number) == 1:
				# Define the folder name as the number, a dash with spaces around it, and the number followed by a zero
				name = number + " - " + number + "0"

				if name not in self.folder_names:
					self.folder_names.append(name)

			# "11 - 20" file range and so on
			# (The number followed by a one, a dash with spaces around it, and the number followed by a zero
			name = number + "1" + " - " + str(int(number) + 1) + "0"

			# If the folder name is not inside the list, add it
			if name not in self.folder_names:
				self.folder_names.append(name)

	def Cover_Folder_Name(self, chapter_number):
		# Iterate through the list of folder names
		for item in self.folder_names:
			# Split the folder name
			# (1, 10) for example
			split = item.split(" - ")

			# Make the range of numbers for the folder name
			# (1, 10) for example
			# Numbers starting from 1 up to 10
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
			# Import the "Tasks" module
			import Tasks

			# Run the root class to define its variables
			self.Tasks = Tasks()

			# Register the task
			sef.Tasks.Register(task_dictionary)

		# Register the task on the current "Diary Slim" file if the "Tasks" module did not
		if register_task == False:
			# Show a space separator
			print()

			# Import the "Write_On_Diary_Slim_Module" sub-class
			from Diary_Slim.Write_On_Diary_Slim_Module import Write_On_Diary_Slim_Module as Write_On_Diary_Slim_Module

			# Define the "Write on Diary Slim" dictionary
			dictionary = {
				"Text": task_dictionary["Task"]["Descriptions"][self.user_language],
				"Time": self.task_dictionary["Date"]["Formats"]["HH:MM DD/MM/YYYY"],
				"Show text": False
			}

			# Write the task text on Diary Slim
			Write_On_Diary_Slim_Module(dictionary)

	def Select_Story(self, select_text_parameter = None, select_class = False):
		# Define the show text
		show_text = self.language_texts["stories, title()"]

		# Define the select text
		select_text = select_text_parameter

		if select_text_parameter == None:
			select_text = self.language_texts["select_a_story"]

		# Get the class name
		class_name = type(self).__name__

		# If the select text parameter is None
		# And the current class is a sub-class of the "Stories" class
		# And the class name is inside the language texts dictionary
		if (
			select_text_parameter == None and
			issubclass(type(self), Stories) == True and
			class_name in self.language_texts
		):
			# Change the select text to add the text of the current class, based on its name
			select_text = self.language_texts["select_a_story_to"] + " " + self.language_texts[class_name.lower()]

		# Make a local copy of the "Stories" dictionary
		stories = deepcopy(self.stories)

		# Remove the stories with all chapters posted if the class is "Post"
		if class_name == "Post":
			# Iterate through the English story titles list
			for story in self.stories["Titles"]["en"]:
				# Get the "Story" dictionary
				story = stories[story]

				# Get the last chapter posted
				last_chapter_posted = story["Information"]["Chapters"]["Last posted chapter"]

				# If the last chapter posted is the same as the last chapter
				if last_chapter_posted == story["Information"]["Chapters"]["Number"]:
					# Iterate through the small languages list
					for language in self.languages["small"]:
						# Remove the story from the story titles list in the current language
						stories["Titles"][language].remove(story["Information"]["Titles"][language])

		# Ask for the user to select the story
		options = stories["Titles"]["en"]
		language_options = stories["Titles"][self.user_language]

		option = self.Input.Select(options, language_options = language_options, show_text = show_text, select_text = select_text)["option"]

		# Get the "Story" dictionary
		self.story = self.stories["Dictionary"][option]

		# Set the "Story" attribute inside the "Stories" class as the "Story" dictionary above
		setattr(Stories, "story", self.story)

		# If the "select_class" parameter is True, then ask the user to select a class
		if select_class == True:
			self.Select_Class()

		# Return the "Story" dictionary
		return self.story

	def Select_Class(self):
		# Define the "Classes" dictionary
		classes = {
			"List": [
				"Write",
				"Post",
				"Manage"
			],
			"Descriptions": []
		}

		# Iterate through the classes in the list
		for class_name in classes["List"]:
			# Get the class description
			description = self.JSON.Language.language_texts[class_name.lower() + ", title()"]

			# Add the class description to the "Descriptions" list
			classes["Descriptions"].append(description)

		# Define the show text with the story title in the user language
		show_text = self.language_texts["what_to_do_with_the_story"] + " " + '"' + self.story["Titles"][self.user_language] + '"'

		# Ask the user to select the sub-class
		sub_class = self.Input.Select(classes["List"], language_options = classes["Descriptions"], show_text = show_text, select_text = self.JSON.Language.language_texts["select_one_thing_to_do"])["option"]

		# Get the module of the sub-class
		module = importlib.import_module("." + sub_class, "Stories")

		# Get the sub-class
		sub_class = getattr(module, sub_class)

		# Add the "Story" variable to the sub-class
		setattr(sub_class, "story", self.story)

		# Execute the sub-class
		sub_class()
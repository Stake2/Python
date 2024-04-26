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

		# Folders, files, and dictionaries methods
		self.Define_Folders_And_Files()
		self.Define_Dictionaries()

		# Class methods

		# Define the Social Network variables
		self.Define_Social_Network_Variables()

		# Define the cover folder names list
		self.Define_Cover_Folder_Names()

		# Define the "Information items" dictionary
		self.Define_Information_Items()

		# Define the "Stories" dictionary
		self.Define_Stories_Dictionary()

	def Define_Basic_Variables(self):
		from copy import deepcopy

		# Import the JSON module
		from Utility.JSON import JSON as JSON

		self.JSON = JSON()

		# Define the "Language" class as the same class inside the "JSON" class
		self.Language = self.JSON.Language

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
		self.languages = self.Language.languages

		# Get the user language and full user language
		self.user_language = self.Language.user_language
		self.full_user_language = self.Language.full_user_language

		# Get the Sanitize method of the File class
		self.Sanitize = self.File.Sanitize

		# Get the current date from the Date module
		self.date = self.Date.date

	def Define_Texts(self):
		# Define the "Texts" dictionary
		self.texts = self.JSON.To_Python(self.folders["apps"]["module_files"][self.module["key"]]["texts"])

		# Define the "Language texts" dictionary
		self.language_texts = self.Language.Item(self.texts)

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
				"root": self.folders["Mega"]["Stories"]["root"]
			}
		}

		# Define the root files
		names = {
			"Stories.json": "",
			"Stories list": self.Language.language_texts["stories_list"],
			"Authors list": self.Language.language_texts["authors_list"]
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
			"root": self.stories["Folders"]["root"] + self.Language.language_texts["database, title()"] + "/"
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
			"Authors",
			"Information items"
		]

		# Iterate through the file names list
		for file_name in names:
			# Split the file name to remove possible extensions
			key = file_name

			# Define the file with the root folder and file name
			file = self.stories["Folders"]["Database"]["root"] + file_name + ".json"

			# Add the file to the "Database" folders dictionary
			self.stories["Folders"]["Database"][key] = file

			# Create the file
			self.File.Create(self.stories["Folders"]["Database"][key])

	def Define_Dictionaries(self):
		# Define the "Story pack" dictionary
		self.stories["Story pack"] = {
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
			"Soundtrack": {
				"First track": {
					"Type": "Playlist",
					"Source": "YouTube Embed",
					"ID": "[ID]",
					"Link": "https://www.youtube-nocookie.com/embed/videoseries?list={}"
				}
			}
		}

		# Define the "Writing links" dictionary
		self.stories["Writing links"] = {
			"TimeAndDate": {
				"Link": "https://www.timeanddate.com/stopwatch/"
			},
			"Google Translate": {
				"Link": "https://translate.google.com/"
			}
		}

		# Define the "Directories" dictionary
		self.stories["Directories"] = {
			"Root": {
				"Files": [
					"Story information",
					"Authors"
				],
				"JSON": [
					"Story"
				]
			},
			"Chapters": {
				"Folders": [
					"Language"
				],
				"Files": [
					"Dates"
				]
			},
			"Comments": {},
			"Covers": {
				"Folders": [
					"Landscape",
					"Portrait"
				]
			},
			"Information": {
				"Folders": [
					"Synopsis"
				],
				"Files": [
					"Creation date"
				],
				"JSON": [
					"Chapters",
					"Wattpad",
					"Writing"
				]
			},
			"Lore": {
				"Folders": [
					"Language",
					"Visual"
				]
			},
			"Readers": {
				"Folders": [
					"Reads"
				],
				"Files": [
					"Readers"
				]
			}
		}

	def Define_Information_Items(self):
		# Define the "Information items" dictionary
		dictionary = {
			"Numbers": {
				"Total": 0
			},
			"List": [],
			"Dictionary": {}
		}

		# Read the "Information items.json" file if it is not empty
		file = self.stories["Folders"]["Database"]["Information items"]

		if self.File.Contents(file)["lines"] != []:
			dictionary = self.JSON.To_Python(file)

		# Get the number of information items
		dictionary["Numbers"]["Total"] = len(dictionary["List"])

		# Reset the "Dictionary" key to be an empty dictionary
		dictionary["Dictionary"] = {}

		# Iterate through the information items list
		for key in dictionary["List"]:
			# Create the information item dictionary
			dict_ = {
				"Name": key
			}

			# Define the text key
			text_key = key.lower().replace(" ", "_")

			# Define the text addon
			addon = ""

			if "_" not in text_key:
				addon = ", title()"

			# Create the "Texts" dictionary
			dict_["Texts"] = {}

			# Iterate through the small languages list
			for language in self.languages["small"]:
				# Get the information text
				text = self.Language.texts[text_key + addon][language]

				# Define the language information item inside the local "dict_" dictionary
				dict_["Texts"][language] = text

			# If the key is in the "Formats" dictionary, use the format dictionary inside it
			if key in dictionary["Formats"]:
				dict_["Format"] = dictionary["Formats"][key]

			# If a root method named ["Select_" + key.capitalize()] exists
			method_name = "Select_" + key.capitalize()

			if hasattr(self, method_name) == True:
				# Define it as the method to be used to select the information
				dict_["Method"] = getattr(self, method_name)

			# Add the information item dictionary to the root "Information items" dictionary
			dictionary["Dictionary"][key] = dict_

		# Define the "Information items" dictionary as the local "Information items" dictionary
		self.stories["Information items"] = dictionary

		# Create a local "Information items" dictionary
		local_dictionary = deepcopy(self.stories["Information items"])

		# Iterate through the information items in the "Information items" dictionary
		for key, information_item in local_dictionary["Dictionary"].items():
			# If the "Method" key is inside the information item dictionary
			if "Method" in information_item:
				# Get the name of the method used to select the information item
				information_item["Method"] = information_item["Method"].__name__

		# Update the "Information items.json" file with the updated and local "Information items" dictionary
		self.JSON.Edit(self.stories["Folders"]["Database"]["Information items"], local_dictionary)

	def Define_Stories_Dictionary(self):
		import collections

		# ---------- #

		# Authors

		# Get the contents of the "Authors list" file
		lines = self.File.Contents(self.stories["Folders"]["Authors list"])["lines"]

		# Define the "Author" key, which is the first author
		self.stories["Author"] = lines[0]

		# Get the story authors
		self.stories["Authors"] = {
			"Number": 0,
			"List": lines
		}

		# Define the number of authors
		self.stories["Authors"]["Number"] = len(self.stories["Authors"]["List"])

		# Write the "Authors" dictionary to the database "Authors.json" file
		self.JSON.Edit(self.stories["Folders"]["Database"]["Authors"], self.stories["Authors"])

		# ---------- #

		# Define the "Cover types" dictionary
		self.stories["Cover types"] = {
			"List": [
				"Landscape",
				"Portrait"
			],
			"Dictionary": {}
		}

		# Fill the "Cover types" dictionary
		for key in self.stories["Cover types"]["List"]:
			# Define the text key
			text_key = key.lower() + ", title()"

			# Define the cover type dictionary, with its key, title, titles, and extension
			dictionary = {
				"Key": key,
				"Title": key,
				"Titles": {}
			}

			# Fill the "Titles" dictionary with the language texts
			for language in self.languages["small"]:
				dictionary["Titles"][language] = self.Language.texts[text_key][language]

			# Add the cover type dictionary to the root dictionary
			self.stories["Cover types"]["Dictionary"][key] = dictionary

		# ---------- #

		# "Stories" dictionary

		# Define the empty story "Numbers" dictionary
		self.stories["Numbers"] = {}

		# Get the list of stories
		self.stories["List"] = self.JSON.To_Python(self.stories["Folders"]["Stories"])["List"]

		# Sort the list of stories
		self.stories["List"] = sorted(self.stories["List"], key = str.lower)

		# Update the "Total" key of the "Numbers" dictionary
		self.stories["Numbers"]["Total"] = len(self.stories["List"])

		# Define the "Titles" dictionary and get the story titles
		self.stories["Titles"] = {
			"en": self.stories["List"],
			self.user_language: [],
			"Language": []
		}

		# Define the list of story titles in the user language
		self.stories["Titles"][self.user_language] = self.File.Contents(self.stories["Folders"]["Stories list"])["lines"]

		# Define the "All" list
		self.stories["Titles"]["All"] = []

		# Define the "Dictionary" dictionary
		self.stories["Dictionary"] = {}

		# ---------- #

		# Remove stories which have no folder

		# Define the language story titles list
		language_story_titles = deepcopy(self.stories["Titles"][self.user_language])

		# Iterate through the list of stories
		s = 0
		for story_title in self.stories["List"].copy():
			# Get the language story title
			language_story_title = language_story_titles[s]

			# Define the root story folder
			story_folder = self.stories["Folders"]["root"] + language_story_title + "/"

			# If the root folder does not exist
			if self.Folder.Exist(story_folder) == False:
				# Remove the story from the list of stories
				self.stories["List"].remove(story_title)
				self.stories["Titles"][self.user_language].remove(language_story_title)

			# Add one to the "s" number variable
			s += 1

		# Update the "Total" key of the "Numbers" dictionary
		self.stories["Numbers"]["Total"] = len(self.stories["List"])

		# ---------- #

		# Add the stories to the "Stories" dictionary
		s = 0
		for story_title in self.stories["List"]:
			# Get the language story title
			language_story_title = self.stories["Titles"][self.user_language][s]

			# Define the "Story" dictionary and the keys
			story = {
				"Title": story_title,
				"Titles": {},
				"Folders": {
					"root": self.stories["Folders"]["root"] + language_story_title + "/"
				},
				"Information": {}
			}

			# Create the story sub-folders
			story = self.Create_Story_Sub_Folders(story)

			# ---------- #

			# Read the "Story.json" file if it is not empty
			if self.File.Contents(story["Folders"]["Story"])["lines"] != []:
				story["Information"] = self.JSON.To_Python(story["Folders"]["Story"])

			# ---------- #

			# Define the list of file keys
			keys = list(story["Folders"]["Information"].keys())

			# Remove the "Synopsis" key because its value is a dict, not a file
			keys.remove("Synopsis")

			# Remove files that do not exist
			for key in keys.copy():
				# Get the file
				file = story["Folders"]["Information"][key]

				# Remove the file if it does not exist
				if self.File.Exist(file) == False:
					keys.remove(key)

			# Get the story information from the files inside the "Information" folder
			for key in keys:
				# Get the file
				file = story["Folders"]["Information"][key]

				# Define the default read function as the "Contents" method of the "File" class
				function = self.File.Contents

				# If the file is a JSON file
				if ".json" in file:
					# Define the read function as the "To_Python" method of the "JSON" class
					function = self.JSON.To_Python

				# Read the file and get the information
				information = function(file)

				# If the file is a text file
				if ".txt" in file:
					# If the key is "Author"
					if key == "Author":
						# Get the lines of the information (the authors)
						information = information["lines"]

						# If the number of authors is one
						if len(information) == 1:
							# Make a list with the only author as the first item
							information = [
								information[0]
							]

					# If the key not "Author"
					if key != "Author":
						# Get the string of the information
						information = information["string"]

				# Define the information with its key inside the "Information" dictionary
				story["Information"][key] = information

			# ---------- #

			# Update the "Authors.txt" file with the list of authors
			text_to_write = self.Text.From_List(story["Information"]["Authors"], break_line = True)

			self.File.Edit(story["Folders"]["Authors"], text_to_write, "w")

			# If the number of authors is more than one
			if len(story["Information"]["Authors"]) > 1:
				# Transform the list of authors into a text without line breaks
				story["Information"]["Author"] = self.Text.From_List(story["Information"]["Authors"], language = "en")

			# ---------- #

			# Define the story titles in all languages
			story["Titles"] = story["Information"]["Titles"]

			# Add the language story title to the list of story titles in the user language
			self.stories["Titles"]["Language"].append(story["Titles"][self.user_language])

			# Add the story titles to the "All" list
			for title in story["Titles"].values():
				# If the title is not already in the list
				if title not in self.stories["Titles"]["All"]:
					self.stories["Titles"]["All"].append(title)

			# ---------- #

			# Iterate through the list of cover types
			for cover_type in self.stories["Cover types"]["List"]:
				# Iterate through the small languages list
				for language in self.languages["small"]:
					# Get the full language
					full_language = self.languages["full"][language]

					# Define the full language cover folder
					story["Folders"]["Covers"][cover_type][full_language] = {
						"root": story["Folders"]["Covers"][cover_type]["root"] + full_language + "/"
					}

					# Create the folder
					self.Folder.Create(story["Folders"]["Covers"][cover_type][full_language]["root"])

					# Define the Photoshop cover file
					story["Folders"]["Covers"][cover_type][full_language]["Photoshop"] = story["Folders"]["Covers"][cover_type][full_language]["root"] + "PSD.psd"

			# ---------- #

			# Define the story covers folder inside the "Websites" images folder
			story["Folders"]["Covers"]["Websites"] = {
				"root": self.folders["Mega"]["Websites"]["Images"]["root"] + story_title + "/"
			}

			# Create the folder
			self.Folder.Create(story["Folders"]["Covers"]["Websites"]["root"])

			# Add the sub-folders of the "Websites" cover folder
			folders = [
				"Chapters"
			]

			for folder in folders:
				story["Folders"]["Covers"]["Websites"][folder] = {
					"root": story["Folders"]["Covers"]["Websites"]["root"] + folder + "/"
				}

			# ---------- #

			# Define the default story "Chapters" dictionary
			story["Information"]["Chapters"] = {
				"Numbers": {
					"Total": 0,
					"Last posted chapter": 0
				},
				"Titles": {},
				"Dates": self.File.Contents(story["Folders"]["Chapters"]["Dates"])["lines"]
			}

			# Add the chapter titles to the chapter "Titles" dictionary
			for language in self.languages["small"]:
				# Get the full language
				full_language = self.languages["full"][language]

				# Read the chapter titles file
				file = story["Folders"]["Chapters"][full_language]["Titles"]["Titles"]

				# Add the chapter titles to the chapter "Titles" dictionary
				story["Information"]["Chapters"]["Titles"][language] = self.File.Contents(file)["lines"]

			# Update the number of chapters
			story["Information"]["Chapters"]["Numbers"]["Total"] = len(story["Information"]["Chapters"]["Titles"]["en"])

			# Add the "Last posted chapter" key
			story["Information"]["Chapters"]["Numbers"]["Last posted chapter"] = story["Information"]["Chapters"]["Numbers"]["Total"]

			# Write the "Chapters" dictionary into the "Chapters.json" file
			self.JSON.Edit(story["Folders"]["Information"]["Chapters"], story["Information"]["Chapters"])

			# ---------- #

			# Create the "Synopsis" language files
			for language in self.languages["small"]:
				full_language = self.languages["full"][language]

				story["Folders"]["Information"]["Synopsis"][full_language] = story["Folders"]["Information"]["Synopsis"]["root"] + full_language + ".txt"
				self.File.Create(story["Folders"]["Information"]["Synopsis"][full_language])

			# Define the empty "Synopsis" dictionary
			story["Information"]["Synopsis"] = {}

			# Iterate through the list of small languages
			for language in self.languages["small"]:
				# Get the full language
				full_language = self.languages["full"][language]

				# Add the synopsis in the current language to the "Synopsis" dictionary
				story["Information"]["Synopsis"][language] = self.File.Contents(story["Folders"]["Information"]["Synopsis"][full_language])["string"]

			# ---------- #

			# Define the default "Writing" dictionary
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

			# Define the root "Writing" dictionary as the local dictionary
			story["Information"]["Writing"] = writing

			# Write the default or modified "Writing" dictionary inside the "Writing.json" file
			self.JSON.Edit(story["Folders"]["Information"]["Writing"], story["Information"]["Writing"])

			# ---------- #

			# If the "Pack" dictionary is not present inside the "Information" dictionary
			if "Pack" not in story["Information"]:
				# Define the "Pack" dictionary of the current story as the default "Pack" dictionary
				story["Information"]["Pack"] = deepcopy(self.stories["Story pack"])

			# ---------- #

			# Create the empty "Website" dictionary with the "Link" key
			story["Information"]["Website"] = {
				"Link": ""
			}

			# Define the story website folder as the story title
			website_folder = story_title

			# If the story has a parent story
			if "Parent story" in story["Information"]:
				# Get the parent story dictionary
				parent_story = story["Information"]["Parent story"]

				# Define the website folder
				website_folder = parent_story["Title"]

				# If the parent story has a custom folder, use it
				if "Folder" in parent_story:
					website_folder = parent_story["Folder"]

				# Add the story title to the website folder
				website_folder += "/" + story_title

				# Define the website folder
				story["Information"]["Website"]["Website folder"] = "/" + website_folder + "/"

			# Update the website "Link" key with the website folder
			story["Information"]["Website"]["Link"] = self.links["Stake2 Website"] + website_folder + "/"

			# ---------- #

			# Add the story Wattpad link for each language
			link = self.social_networks["Wattpad"]["Information"]["Links"]["My works"]

			# Iterate through the list of small languages
			for language in self.languages["small"]:
				# If the language is inside the "Wattpad" dictionary
				if language in story["Information"]["Wattpad"]:
					# Get the Wattpad story id
					id = story["Information"]["Wattpad"][language]["ID"]

					# Define the Wattpad story link as the "My works" link plus the Wattpad story id
					story["Information"]["Wattpad"][language]["Link"] = link + id

			# Write the default or modified "Wattpad" dictionary inside the "Wattpad.json" file
			self.JSON.Edit(story["Folders"]["Information"]["Wattpad"], story["Information"]["Wattpad"])

			# ---------- #

			# Get the list of readers of the story
			readers_list = self.File.Contents(story["Folders"]["Readers"]["Readers"])

			# Define the "Readers" dictionary with the number of readers and the list
			story["Information"]["Readers"] = {
				"Number": readers_list["length"],
				"List": readers_list["lines"]
			}

			# ---------- #

			# Change the order of the keys inside the "Information" dictionary to a better order

			# Define the empty copy dictionary
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

		# Update the "Stories list.txt" file with the updated  list of story titles in the user language
		text_to_write = self.Text.From_List(self.stories["Titles"]["Language"], break_line = True)

		self.File.Edit(self.stories["Folders"]["Stories list"], text_to_write, "w")

		# Make a copy of the "Stories" dictionary
		stories_dictionary = deepcopy(self.stories)

		# Remove the unneeded keys
		keys = [
			"Folders",
			"Story pack",
			"Writing links",
			"Directories",
			"Information items",
			"Cover types"
		]

		for key in keys:
			stories_dictionary.pop(key)

		# Remove the "Language" key from the "Titles" dictionary
		stories_dictionary["Titles"].pop("Language")

		# Write the updated local "Stories" dictionary to the "Stories.json" file
		self.JSON.Edit(self.stories["Folders"]["Stories"], stories_dictionary)

	def Create_Story_Sub_Folders(self, story):
		# Iterate through the directories inside the "Directories" dictionary
		for key, directory in self.stories["Directories"].items():
			# Define the folder dictionary
			folder_dictionary = story["Folders"]

			# If the key is not "Root" (the story folder)
			if key != "Root":
				# Define the folder name
				text_key = key.lower() + ", title()"

				# If the key is "Information"
				if key == "Information":
					# Replace the "information" text with the "informations" one
					text_key = text_key.replace("information", "informations")

				folder_name = self.Language.language_texts[text_key]

				# Define the folder
				folder_dictionary[key] = {
					"root": folder_dictionary["root"] + folder_name + "/"
				}

				# Create the folder
				self.Folder.Create(folder_dictionary[key]["root"])

				# Update the folder dictionary
				folder_dictionary = folder_dictionary[key]

			# If the "Folders" key is present, create the folders
			if "Folders" in directory:
				for sub_key in directory["Folders"]:
					# If the sub-key is not "Language"
					if sub_key != "Language":
						# Define the sub-folder name
						text_key = sub_key.lower() + ", title()"

						folder_name = self.Language.language_texts[text_key]

						# Define the sub-folder
						folder_dictionary[sub_key] = {
							"root": folder_dictionary["root"] + folder_name + "/"
						}

						# Create the sub-folder
						self.Folder.Create(folder_dictionary[sub_key]["root"])

					# If the sub-key is "Language"
					if sub_key == "Language":
						# Iterate through the small languages list
						for language in self.languages["small"]:
							# Get the full language
							full_language = self.languages["full"][language]

							# Define the sub-folder
							folder_dictionary[full_language] = {
								"root": folder_dictionary["root"] + full_language + "/"
							}

							# Create the sub-folder
							self.Folder.Create(folder_dictionary[full_language]["root"])

							# If the root key is "Chapters"
							if key == "Chapters":
								# Define the "Titles" folder
								story["Folders"]["Chapters"][full_language]["Titles"] = {
									"root": folder_dictionary[full_language]["root"] + self.Language.texts["titles, title()"][language] + "/"
								}

								# Create the "Titles" folder
								self.Folder.Create(story["Folders"]["Chapters"][full_language]["Titles"]["root"])

								# Define and create the "Titles" file
								story["Folders"]["Chapters"][full_language]["Titles"]["Titles"] = folder_dictionary[full_language]["Titles"]["root"] + self.Language.texts["titles, title()"][language] + ".txt"

								self.File.Create(story["Folders"]["Chapters"][full_language]["Titles"]["Titles"])

			# Define the empty file types list
			file_types = []

			# Iterate through the list of default file types
			for file_type in ["Files", "JSON"]:
				# If the file type is inside the "Directory" dictionary, add it to the file types list
				if file_type in directory:
					file_types.append(file_type)

			# Iterate through the list of file types
			for file_type in file_types:
				# Iterate through the items inside the file type list
				for sub_key in directory[file_type]:
					# Define the default file name with the "json" extension
					file_name = sub_key + ".json"

					# If the file type is "Files"
					if file_type == "Files":
						# Define the file name
						text_key = sub_key.lower().replace(" ", "_")

						if "_" not in text_key:
							text_key += ", title()"

						file_name = self.Language.language_texts[text_key] + ".txt"

					# Define the file
					folder_dictionary[sub_key] = folder_dictionary["root"] + file_name

					# Create the sub-folder
					self.File.Create(folder_dictionary[sub_key])

		# Return the "Story" dictionary
		return story

	def Select_Status(self):
		# Define the parameters dictionary for the "Select" method of the "Input" class
		parameters = {
			"options": self.texts["status, type: list"]["en"],
			"language_options": self.language_texts["status, type: list"],
			"show_text": self.language_texts["writing_statuses"],
			"select_text": self.language_texts["select_a_writing_status"]
		}

		if self.switches["testing"] == False:
			# Ask the user to select a status from the list
			option = self.Input.Select(**parameters)

		if self.switches["testing"] == True:
			option = {
				"number": 0,
				"option": self.texts["writing, title()"]["en"],
				"language_option": self.language_texts["writing, title()"]
			}

			print()
			print(self.language_texts["writing_status"] + ":")
			print(option["language_option"])

		# Create the "Status" dictionary
		status = {
			"Number": option["number"],
			"Names": {
				"en": option["option"],
				self.user_language: option["language_option"]
			}
		}

		# Return the "Status" dictionary
		return status

	def Select_Author(self):
		# Define the authors list with the first author
		authors = [
			self.stories["Authors"]["List"][0]
		]

		# Show the list of authors
		self.Show_Authors_List(authors)

		# Ask if the user wants to add more authors to the list of authors
		question = self.language_texts["do_you_want_to_add_more_authors"]

		if self.switches["testing"] == False:
			add_more = self.Input.Yes_Or_No(question)

		if self.switches["testing"] == True:
			add_more = False

		# If the user wants to add more authors
		if add_more == True:
			# Define the list of authors without the first one
			options = deepcopy(self.stories["Authors"]["List"])
			options.pop(0)

			# Define the parameters dictionary for the "Select" method of the "Input" class
			parameters = {
				"options": options,
				"language_options": deepcopy(options),
				"show_text": self.Language.language_texts["authors, title()"],
				"select_text": self.language_texts["select_an_additional_author"]
			}

			# Add the "[Finish selection]" text to the list of options
			parameters["options"].append("[Finish selection]")

			# Define the language texxt
			language_text = "[" + self.Language.language_texts["finish_selection"] + "]"

			# Add the "[Finish selection]" text in the user language to the list of language options
			parameters["language_options"].append(language_text)

			# Define the "finish selection" variable for easier typing
			finish_selection = "[Finish selection]"

			# Define the default empty option variable
			option = ""

			# While the option is not the "[Finish selection]" text
			while option != finish_selection:
				# Show a five dash space separator
				print()
				print(self.separators["5"])

				# If the list of authors is not empty
				if authors != []:
					# Show the list of authors
					self.Show_Authors_List(authors)

				# Ask the user to select the author
				option = self.Input.Select(**parameters)["option"]

				# If the option is not the "[Finish selection]" text
				if option != finish_selection:
					# Remove the selected text from the parameters dictionary
					parameters["options"].remove(option)
					parameters["language_options"].remove(option)

					# Add the author to the list of authors
					authors.append(option)

					# If the length of the list of options is one
					# That means the user select all of the options of the list
					# Then define the option as the "finish_selection" one, to stop the while loop
					if len(parameters["options"]) == 1:
						option = finish_selection

		# Return the list of authors
		return authors

	def Show_Authors_List(self, authors):
		# Show the "Authors:" text
		print()
		print(self.Language.language_texts["authors, title()"] + ":")

		# Show the list of authors
		print("[")

		# Iterate through the authors in the list
		for author in authors:
			# Make a backup of the author
			backup = author

			# Add one tab to the author
			author = author.replace("\n", "\n\t")

			# Show the author with a tab and quotes around it
			print("\t" + '"' + author + '"')

		# Show the end of the list
		print("]")

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
		show_text = self.Language.language_texts["stories, title()"]

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
			description = self.Language.language_texts[class_name.lower() + ", title()"]

			# Add the class description to the "Descriptions" list
			classes["Descriptions"].append(description)

		# Define the show text with the story title in the user language
		show_text = self.language_texts["what_to_do_with_the_story"] + " " + '"' + self.story["Titles"][self.user_language] + '"?'

		# Ask the user to select the sub-class
		sub_class = self.Input.Select(classes["List"], language_options = classes["Descriptions"], show_text = show_text, select_text = self.Language.language_texts["select_one_thing_to_do"])["option"]

		# Get the module of the sub-class
		module = importlib.import_module("." + sub_class, "Stories")

		# Get the sub-class
		sub_class = getattr(module, sub_class)

		# Add the "Story" variable to the sub-class
		setattr(sub_class, "story", self.story)

		# Execute the sub-class
		sub_class()
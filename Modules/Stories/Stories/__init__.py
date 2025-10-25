# Stories.py

# Import the "importlib" module
import importlib

from copy import deepcopy

class Stories(object):
	def __init__(self):
		# Import the classes
		self.Import_Classes()

		# Define the folders of the module
		self.folders = self.Define_Folders(object = self).folders

		# Module related methods
		self.Define_Basic_Variables()
		self.Define_Texts()

		# Import some usage classes
		self.Import_Usage_Classes()

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

		# Define the "Story websites" dictionary
		self.Define_Story_Websites_Dictionary()

		# Define the "Stories" dictionary
		self.Define_Stories_Dictionary()

	def Import_Classes(self):
		# Define the list of modules to be imported
		modules = [
			"Define_Folders",
			"JSON"
		]

		# Iterate through the list of modules
		for module_title in modules:
			# Import the module
			module = importlib.import_module("." + module_title, "Utility")

			# Get the sub-class
			sub_class = getattr(module, module_title)

			# If the module title is not "Define_Folders"
			if module_title != "Define_Folders":
				# Run the sub-class to define its variable
				sub_class = sub_class()

			# Add the sub-class to the current module
			setattr(self, module_title, sub_class)

		# Define the "Language" class as the same class inside the "JSON" class
		self.Language = self.JSON.Language

	def Define_Basic_Variables(self):
		# Get the dictionary of modules
		self.modules = self.JSON.To_Python(self.folders["Apps"]["Modules"]["Modules"])

		# Create a list of the modules that will not be imported
		remove_list = [
			"Define_Folders",
			"Modules",
			"Language",
			"JSON"
		]

		# Iterate through the list of utility modules
		for module_title in self.modules["Utility"]["List"]:
			# If the module title is not inside the remove list
			if module_title not in remove_list:
				# Import the module
				module = importlib.import_module("." + module_title, "Utility")

				# Get the sub-class of the module
				sub_class = getattr(module, module_title)

				# Add the sub-class to the current class
				setattr(self, module_title, sub_class())

		# ---------- #

		# Get the switches dictionary from the "Global Switches" class
		self.switches = self.Global_Switches.switches["Global"]

		# ---------- #

		# Import some variables from the "Language" class

		# Import the "languages" dictionary
		self.languages = self.Language.languages

		# Import the "language" dictionary
		self.language = self.Language.language

		# Import the "separators" dictionary
		self.separators = self.Language.separators

		# ---------- #

		# Import the "folders" dictionary from the "Folder" class
		self.folders = self.Folder.folders

		# ---------- #

		# Import the "Sanitize" method from the "File" class
		self.Sanitize = self.File.Sanitize

		# ---------- #

		# Get the current date from the "Date" class
		self.date = self.Date.date

		# Get the current year
		self.current_year = str(self.date["Units"]["Year"])

	def Define_Texts(self):
		# Define the "Texts" dictionary
		self.texts = self.JSON.To_Python(self.module["Files"]["Texts"])

		# Define the "Language texts" dictionary
		self.language_texts = self.Language.Item(self.texts)

		i = 0
		for item in self.language_texts["copy_actions, type: list"]:
			self.language_texts["copy_actions, type: list"][i] = "[" + self.language_texts["copy_actions, type: list"][i] + "]"

			i += 1

	def Import_Usage_Classes(self):
		# Define the classes to be imported
		classes = [
			"PHP",
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

		# ---------- #

		# Import the "website" dictionary from the "PHP" class
		self.website = self.PHP.website

		# Import the root methods of the "PHP" class
		for method in ["Define", "Manage"]:
			# Define the method name
			method_name = method + "_Server"

			# Get the method
			method = getattr(self.PHP, method_name)

			# Add the method to the "Stories" class
			setattr(self, method_name, method)

	def Define_Social_Network_Variables(self):
		# Get the "Social Networks" dictionary from the "Social_Networks" module
		self.social_networks = self.Social_Networks.social_networks

		# ---------- #

		# "Wattpad" social network

		# Define the "Wattpad" key for faster typing
		self.social_networks["Wattpad"] = self.social_networks["Dictionary"]["Wattpad"]

		# Define the additional links

		# Define the "Conversations" link
		self.social_networks["Wattpad"]["Profile"]["Links"] = {
			"Conversations": self.social_networks["Wattpad"]["Profile"]["Links"]["Profile"] + "conversations/"
		}

		# Define the "Links" dictionary
		self.social_networks["Wattpad"]["Links"] = {
			"Posts": self.social_networks["Wattpad"]["Profile"]["Links"]["Conversations"]
		}

		# Define the "My works" link
		self.social_networks["Wattpad"]["Information"]["Links"] = {
			"My works": self.social_networks["Wattpad"]["Information"]["Link"] + "myworks/"
		}

		# Define the "Story" link as a shortcut for the "My works" link
		self.social_networks["Wattpad"]["Information"]["Links"]["Story"] = self.social_networks["Wattpad"]["Information"]["Link"] + "story/"

		# Define the "Edit story" link
		self.social_networks["Wattpad"]["Information"]["Links"]["Edit story"] = self.social_networks["Wattpad"]["Information"]["Links"]["My works"]

		# Update the "Wattpad" key
		self.social_networks["Dictionary"]["Wattpad"] = self.social_networks["Wattpad"]

		# ---------- #

		# "Spirit Fanfics" social network

		# Define the "Spirit Fanfics" key for faster typing
		self.social_networks["Spirit Fanfics"] = self.social_networks["Dictionary"]["Spirit Fanfics"]

		# Define the additional links

		# Define the "Activities" link
		self.social_networks["Spirit Fanfics"]["Profile"]["Links"] = {
			"Activities": self.social_networks["Spirit Fanfics"]["Profile"]["Links"]["Profile"] + "atividades/"
		}

		# Define the "Links" dictionary
		self.social_networks["Spirit Fanfics"]["Links"] = {
			"Posts": self.social_networks["Spirit Fanfics"]["Profile"]["Links"]["Activities"]
		}

		# Define the "Story" link
		self.social_networks["Spirit Fanfics"]["Information"]["Links"] = {
			"Story": self.social_networks["Spirit Fanfics"]["Information"]["Link"] + "historia/"
		}

		# Define the story link variable for easier typing
		story_link = self.social_networks["Spirit Fanfics"]["Information"]["Links"]["Story"]

		# Define the "Read story" link
		self.social_networks["Spirit Fanfics"]["Information"]["Links"]["Read story"] = story_link

		# Add the "Edit story" link
		self.social_networks["Spirit Fanfics"]["Information"]["Links"]["Edit story"] = story_link + "editar/"

		# Add the "Manage chapters" link
		self.social_networks["Spirit Fanfics"]["Information"]["Links"]["Manage chapters"] = story_link + "gerenciar/capitulos/"

		# Add the "Add chapter" link
		self.social_networks["Spirit Fanfics"]["Information"]["Links"]["Add chapter"] = story_link + "adicionar/"

		# Update the "Spirit Fanfics" key
		self.social_networks["Dictionary"]["Spirit Fanfics"] = self.social_networks["Spirit Fanfics"]

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

			# If the "json" extension is not in the file name, then add the "txt" extension
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
			"Story websites"
		]

		for folder_name in names:
			folder[folder_name] = {
				"root": folder["root"] + folder_name + "/"
			}

			self.Folder.Create(folder[folder_name]["root"])

		# Iterate through the small languages list
		for language in self.languages["Small"]:
			# Get the full language
			full_language = self.languages["Full"][language]

			# Define and create the language file
			folder[language] = folder["root"] + full_language + ".txt"
			self.File.Create(folder[language])

		# Create the language files inside the sub-folders
		for folder_name in names:
			# Iterate through the small languages list
			for language in self.languages["Small"]:
				# Get the full language
				full_language = self.languages["Full"][language]

				# Define and create the language file
				folder[folder_name][language] = folder[folder_name]["root"] + full_language + ".txt"
				self.File.Create(folder[folder_name][language])

		# Define the "Database" files
		names = [
			"Authors",
			"Information items",
			"Story websites"
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

		# Define the "Writing" dictionary
		self.stories["Writing"] = {
			"Helpers": {
				"Google Translate": {
					"Name": self.Language.language_texts["google_translate"],
					"Link": "https://translate.google.com/"
				}
			},
			"Programs": {
				"Foobar2000": {
					"Name": "Foobar2000",
					"Link": self.folders["Program Files (x86)"]["Foobar2000"]["Foobar2000"]
				}
			}
		}

		# Define the "Translator website" dictionary
		dictionary = self.stories["Writing"]["Helpers"]

		self.stories["Writing"]["Translator website"] = dictionary["Google Translate"]

		# Define the "Music player" dictionary
		dictionary = self.stories["Writing"]["Programs"]

		self.stories["Writing"]["Music player"] = dictionary["Foobar2000"]

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
					"Writing dates"
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
					"Creation date",
					"Story titles",
					"History of story titles",
					"Story links"
				],
				"JSON": [
					"Chapters",
					"Spirit Fanfics",
					"Pack",
					"Wattpad",
					"Website",
					"Writing",
					"Links"
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
		# Define the local "Information items" dictionary
		dictionary = {
			"Numbers": {
				"Total": 0
			},
			"List": [],
			"Dictionary": {}
		}

		# Read the "Information items.json" file if it is not empty to update the local dictionary
		file = self.stories["Folders"]["Database"]["Information items"]

		if self.File.Contents(file)["Lines"] != []:
			dictionary = self.JSON.To_Python(file)

		# Get the number of information items
		dictionary["Numbers"]["Total"] = len(dictionary["List"])

		# Reset the "Dictionary" key to be an empty dictionary
		dictionary["Dictionary"] = {}

		# Iterate through the information items list
		for key in dictionary["List"]:
			# Create the information item dictionary
			information_item = {
				"Name": key
			}

			# Define the text key
			text_key = key.lower().replace(" ", "_")

			# Define the text addon
			addon = ""

			# If the underline character is not inside the text key, add the ", title()" string to get the titlecase text
			if "_" not in text_key:
				addon = ", title()"

			# Create the "Texts" dictionary
			information_item["Texts"] = {}

			# Iterate through the small languages list
			for language in self.languages["Small"]:
				# Get the information text for the current language using the text key and addon
				text = self.Language.texts[text_key + addon][language]

				# Define the language information item inside the "Texts" dictionary
				information_item["Texts"][language] = text

			# If the information item is "Author"
			if key == "Author":
				# Define the "Plural texts" dictionary
				information_item["Plural texts"] = {}

				# Iterate through the small languages list
				for language in self.languages["Small"]:
					# Get the plural information text for the current language using the text key and addon
					text = self.Language.texts[text_key + "s" + addon][language]

					# Define the language plural information item inside the "Plural texts" dictionary
					information_item["Plural texts"][language] = text

			# If the information item is in the "Formats" dictionary, use the format dictionary inside it
			if key in dictionary["Formats"]:
				information_item["Format"] = dictionary["Formats"][key]

			# Define the "Select_" + [Information item] text as the method name
			method_name = "Select_" + key.capitalize().replace(" ", "_")

			# If the method is present inside the root (self) class
			if hasattr(self, method_name) == True:
				# Define it as the method name
				information_item["Method"] = method_name

			# Add the information item dictionary to the root "Information items" dictionary
			dictionary["Dictionary"][key] = information_item

		# Define the "Information items" dictionary as the local dictionary
		self.stories["Information items"] = dictionary

		# Update the "Information items.json" file with the updated "Information items" dictionary
		self.JSON.Edit(self.stories["Folders"]["Database"]["Information items"], self.stories["Information items"])

		# Iterate through the information items in the "Information items" dictionary
		for key, information_item in self.stories["Information items"].items():
			# If the "Method" key is inside the information item dictionary
			# And the method is present inside the root (self) class
			if (
				"Method" in information_item and
				hasattr(self, information_item["Method"]) == True
			):
				# Get the method using the method name and define it as the method to be used to select the information
				information_item["Method"] = getattr(self, information_item["Method"])

	def Define_Story_Websites_Dictionary(self):
		# Define the "Story websites" dictionary
		dictionary = {
			"Numbers": {
				"Total": 0
			},
			"List": [
				"Wattpad",
				"Spirit Fanfics"
			],
			"Dictionary": {}
		}

		# Update the "Total" key of the "Numbers" dictionary with the number of story websites
		dictionary["Numbers"]["Total"] = len(dictionary["List"])

		# Iterate through the story websites list
		for key in dictionary["List"]:
			# Create the story website dictionary
			dict_ = {
				"Name": key
			}

			# Create the "Templates" dictionary
			dict_["Templates"] = {
				"Root": {
					"IDs": {},
					"Links": {}
				},
				"Additional links": {}
			}

			# Define the list of keys and the format
			keys = ["Edit story"]
			format = "{ID}-{Modified story title}"

			# If the story website is "Spirit Fanfics"
			if key == "Spirit Fanfics":
				# Modify the format
				format = "{ID}"

			# Iterate through the list of keys
			for sub_key in keys:
				# Add the key
				dict_["Templates"]["Root"][sub_key] = {}

				# Add the additional link
				dict_["Templates"]["Additional links"][sub_key] = format

			# Add the story website dictionary to the root "Story websites" dictionary
			dictionary["Dictionary"][key] = dict_

		# Define the "Story websites" dictionary as the local "Story websites" dictionary
		self.stories["Story websites"] = dictionary

		# Update the "Story websites.json" file with the updated "Story websites" dictionary
		self.JSON.Edit(self.stories["Folders"]["Database"]["Story websites"], self.stories["Story websites"])

	def Define_Story_Websites(self, story):
		# Import the "inspect" module
		import inspect

		# Get the method name
		method_name = inspect.stack()[1][3]

		# Iterate through the dictionary of story websites
		for key, story_website in self.stories["Story websites"]["Dictionary"].items():
			# If the method name is "Type_Story_Information"
			if method_name == "Type_Story_Information":
				# Create the story website dictionary
				story["Information"][key] = story_website["Templates"]["Root"]

			# Get the root story link of the story website
			root_story_link = self.social_networks[key]["Information"]["Links"]["Story"]

			# If the "IDs" dictionary is not an empty dictionary
			# Or the method name is "Type_Story_Information"
			if (
				story["Information"][key]["IDs"] != {} or
				method_name == "Type_Story_Information"
			):
				# If the method name is "Type_Story_Information"
				if method_name == "Type_Story_Information":
					# Show the story website name
					print()
					print(self.separators["5"])
					print()
					print(key + ":")

				# Iterate through the list of small languages
				for language in self.languages["Small"]:
					# Get the translated language
					translated_language = self.languages["Full (translated)"][language][self.language["Small"]]

					# If the method name is "Type_Story_Information"
					if method_name == "Type_Story_Information":
						# Ask for the story ID
						type_text = self.language_texts["id_of_the_story_in"] + " " + translated_language

						if self.switches["Testing"] == False:
							id = self.Input.Type(type_text, accept_enter = False, next_line = True)

						else:
							id = "[ID " + language + "]"

							print()
							print(type_text + ":")
							print(id)

					# If the method name is not "Type_Story_Information"
					else:
						# Get the story ID
						id = story["Information"][key]["IDs"][language]

					# Add the story ID to the dictionary
					story["Information"][key]["IDs"][language] = id

					# Create the story link with the story ID
					story["Information"][key]["Links"][language] = root_story_link + id

					# If the story website is "Wattpad"
					if key == "Wattpad":
						# Modify the story title
						modified_story_title = story["Titles"][language].lower().replace(" ", "-")

						# Add the modified story title
						story["Information"][key]["Links"][language] += "-" + modified_story_title

					# Iterate through the additional links in the dictionary
					for sub_key, template in story_website["Templates"]["Additional links"].items():
						# Create the additional link dictionary if it does not exists
						if sub_key not in story["Information"][key]:
							story["Information"][key][sub_key] = {}

						# Define the root link
						root_link = self.social_networks[key]["Information"]["Links"][sub_key]

						# Create the formatted template variable
						formatted_template = template

						# If the "{ID}" text is in the template
						if "{ID}" in template:
							# Replace the format text with the story ID
							formatted_template = formatted_template.replace("{ID}", id)

						# If the "{Modified story title}" text is in the template
						if "{Modified story title}" in template:
							# Modify the story title
							modified_story_title = story["Titles"][language].lower().replace(" ", "-")

							# Replace the format text with the modified story title
							formatted_template = formatted_template.replace("{Modified story title}", modified_story_title)

						# Add the root link to the formatted template, creating the additional link
						additional_link = root_link + formatted_template

						# Add the language additional link to its dictionary
						story["Information"][key][sub_key][language] = additional_link

			# Update the story website dictionary inside the "Links" dictionary with the updated story website dictionary
			story["Information"]["Links"][key] = story["Information"][key]

			# If the "Information" key exists in the "Folders" dictionary
			if "Information" in story["Folders"]:
				# Write the default or modified story website dictionary inside the "[Story website].json" file
				self.JSON.Edit(story["Folders"]["Information"][key], story["Information"][key])

			# If the method name is not "Type_Story_Information"
			if method_name != "Type_Story_Information":
				# Remove the story website key
				story["Information"].pop(key)

		# Return the "Story" dictionary
		return story

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
			"Dictionary": {},
			"Extension": "png"
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
			for language in self.languages["Small"]:
				dictionary["Titles"][language] = self.Language.texts[text_key][language]

			# Add the cover type dictionary to the root dictionary
			self.stories["Cover types"]["Dictionary"][key] = dictionary

		# ---------- #

		# Define the "Writing modes" dictionary
		self.stories["Writing modes"] = {
			"List": [
				"Write",
				"Revise",
				"Translate"
			],
			"Dictionary": {},
			"Verb tenses": [
				"Infinitive",
				"Infinitive action",
				"Action",
				"Item",
				"Done",
				"Done plural",
				"Chapter"
			]
		}

		# Iterate through the list of writing modes
		for key in self.stories["Writing modes"]["List"]:
			# Define the writing mode dictionary
			dictionary = {
				"Name": key,
				"Names": {},
				"Texts": {},
				"Language texts": {}
			}

			# Iterate through the list of small languages
			for language in self.languages["Small"]:
				# Define the text key
				text_key = key.lower() + ", title()"

				# Define the text
				text = self.Language.texts[text_key][language]

				# Add it to the "Names" dictionary
				dictionary["Names"][language] = text

			# Define the text key for the writing mode
			text_key = key.lower() + ", type: dictionary"

			# Get the text dictionary of the writing mode
			texts = self.texts[text_key]

			# Iterate through the list of verb tenses
			for tense in self.stories["Writing modes"]["Verb tenses"]:
				# Get the verb tense text
				text = texts[tense]

				# Add it to the "Texts" dictionary
				dictionary["Texts"][tense] = text

				# Add the tense in the user language to the "Language texts" dictionary
				dictionary["Language texts"][tense] = text[self.language["Small"]]

			# Add the local dictionary to the "Writing modes" dictionary
			self.stories["Writing modes"]["Dictionary"][key] = dictionary

		# ---------- #

		# "Stories" dictionary

		# Define the story "Numbers" dictionary with the "Total" key as zero
		self.stories["Numbers"] = {
			"Total": 0
		}

		# Get the list of stories
		self.stories["List"] = self.JSON.To_Python(self.stories["Folders"]["Stories"])["List"]

		# Sort the list of stories while ignoring case sensitivity for the story titles
		self.stories["List"] = sorted(self.stories["List"], key = str.lower)

		# Update the "Total" key of the "Numbers" dictionary with the number of stories
		self.stories["Numbers"]["Total"] = len(self.stories["List"])

		# Define the "Titles" dictionary and get the story titles
		self.stories["Titles"] = {
			"en": self.stories["List"],
			self.language["Small"]: [],
			"Language": []
		}

		# Define the list of story titles in the user language
		self.stories["Titles"][self.language["Small"]] = self.File.Contents(self.stories["Folders"]["Stories list"])["lines"]

		# Define the "All" list
		self.stories["Titles"]["All"] = []

		# Define the "Dictionary" dictionary
		self.stories["Dictionary"] = {}

		# ---------- #

		# Remove stories which have no folder

		# Define the language story titles list
		language_story_titles = deepcopy(self.stories["Titles"][self.language["Small"]])

		# Iterate through the list of stories
		s = 0
		for story_title in self.stories["List"].copy():
			# Get the language story title
			language_story_title = language_story_titles[s]

			# Define the root story folder
			story_folder = self.stories["Folders"]["root"] + language_story_title + "/"

			# If the root folder does not exist
			if self.Folder.Exists(story_folder) == False:
				# Remove the story from the list of stories
				self.stories["List"].remove(story_title)
				self.stories["Titles"][self.language["Small"]].remove(language_story_title)

			# Add one to the "s" number variable
			s += 1

		# Update the "Total" key of the "Numbers" dictionary with the number of stories
		self.stories["Numbers"]["Total"] = len(self.stories["List"])

		# ---------- #

		# Add the stories to the "Stories" dictionary
		s = 0
		for story_title in self.stories["List"]:
			# Get the language story title
			language_story_title = self.stories["Titles"][self.language["Small"]][s]

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
				if self.File.Exists(file) == False:
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

				# If the information from the file is not an empty string, list, or dictionary
				if information not in ["", [], {}]:
					# Define the information with its key inside the "Information" dictionary
					story["Information"][key] = information

			# ---------- #

			# Update the "Authors.txt" file with the list of authors
			text_to_write = self.Text.From_List(story["Information"]["Authors"], next_line = True)

			self.File.Edit(story["Folders"]["Authors"], text_to_write, "w")

			# If the number of authors is more than one
			if len(story["Information"]["Authors"]) > 1:
				# Transform the list of authors into a text without line breaks
				story["Information"]["Author"] = self.Text.From_List(story["Information"]["Authors"], language = "en")

			# ---------- #

			# Define the order as the list of small languages
			order = self.languages["Small"]

			# Sort the dictionary of titles based on the order of languages
			story["Information"]["Titles"] = self.JSON.Sort_Item_List(story["Information"]["Titles"], order)

			# Define the story titles in all languages
			story["Titles"] = story["Information"]["Titles"]

			# Add the language story title to the list of story titles in the user language
			self.stories["Titles"]["Language"].append(story["Titles"][self.language["Small"]])

			# List the story titles
			story_titles = list(story["Titles"].values())

			# Remove duplicate story titles
			story_titles = self.JSON.Remove_Duplicates_From_List(story_titles)

			# Define a local story titles text
			story_titles_text = ""

			# Define the title number as zero
			title_number = 0

			# Iterate through the list of story titles
			for title in story_titles:
				self.stories["Titles"]["All"].append(title)

				# Add the story title to the local story titles text
				story_titles_text += title

				# If the title number is not the number of story titles (the last title)
				if title_number != len(story_titles) - 1:
					# Add a line break
					story_titles_text += "\n"

				# Add one to the title number
				title_number += 1

			# Write the story titles text into the "Story titles.txt" file
			self.File.Edit(story["Folders"]["Information"]["Story titles"], story_titles_text, "w")

			# ---------- #

			# Iterate through the list of cover types
			for cover_type in self.stories["Cover types"]["List"]:
				# Iterate through the small languages list
				for language in self.languages["Small"]:
					# Get the full language
					full_language = self.languages["Full"][language]

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
				"List": [],
				"Lists": {
					"Titles": {}
				},
				"Dictionary": {}
			}

			# Add the chapter titles to the chapter "Titles" dictionary
			for language in self.languages["Small"]:
				# Get the full language for the current language
				full_language = self.languages["Full"][language]

				# Read the chapter "Titles.txt" file for the current language
				file = story["Folders"]["Chapters"][full_language]["Titles"]["Titles"]

				# Add the language chapter titles to the chapter "Titles" dictionary inside the "Lists" dictionary
				story["Information"]["Chapters"]["Lists"]["Titles"][language] = self.File.Contents(file)["lines"]

			# Define a shortcut to the "Chapters.json" file and get its contents
			file = story["Folders"]["Information"]["Chapters"]
			contents = self.File.Contents(file)

			# If the file is not empty
			if contents["Lines"] != []:
				# Get the JSON dictionary from the file
				chapters = self.JSON.To_Python(file)

				# Update the root "Last posted chapter" key with the correct number
				story["Information"]["Chapters"]["Numbers"]["Last posted chapter"] = chapters["Numbers"]["Last posted chapter"]

				# Update the chapters "Dictionary" key
				story["Information"]["Chapters"]["Dictionary"] = chapters["Dictionary"]

			# If the chapters "List" is empty
			if story["Information"]["Chapters"]["List"] == []:
				# Iterate through the list of keys inside the chapters dictionary
				for chapter in story["Information"]["Chapters"]["Dictionary"]:
					# Add the chapter key to the chapters "List" key
					story["Information"]["Chapters"]["List"].append(chapter)

			# Update the total number of chapters based on the number of chapters in the "List" key
			story["Information"]["Chapters"]["Numbers"]["Total"] = len(story["Information"]["Chapters"]["List"])

			# Write the default or updated story "Chapters" dictionary into the "Chapters.json" file
			self.JSON.Edit(story["Folders"]["Information"]["Chapters"], story["Information"]["Chapters"])

			# ---------- #

			# Create the "Synopsis" language files
			for language in self.languages["Small"]:
				full_language = self.languages["Full"][language]

				story["Folders"]["Information"]["Synopsis"][full_language] = story["Folders"]["Information"]["Synopsis"]["root"] + full_language + ".txt"
				self.File.Create(story["Folders"]["Information"]["Synopsis"][full_language])

			# Define the empty "Synopsis" dictionary
			story["Information"]["Synopsis"] = {}

			# Iterate through the list of small languages
			for language in self.languages["Small"]:
				# Get the full language
				full_language = self.languages["Full"][language]

				# Add the synopsis in the current language to the "Synopsis" dictionary
				story["Information"]["Synopsis"][language] = self.File.Contents(story["Folders"]["Information"]["Synopsis"][full_language])["string"]

			# ---------- #

			# Define the default "Writing" dictionary
			writing = {}

			# Create the writing mode dictionaries inside the "Writing" dictionary
			for writing_mode in self.stories["Writing modes"]["List"]:
				# Define the writing mode dictionary
				writing[writing_mode] = {
					"Chapter": 1,
					"Times": {
						"First": "",
						"Last": "",
						"Added": "",
						"Duration": {
							"Units": {},
							"Text": {}
						}
					}
				}

				# If the writing mode is "Write"
				if writing_mode == "Write":
					# Update the chapter number to zero
					writing[writing_mode]["Chapter"] = 0

			# Read the "Writing.json" file if it is not empty
			if self.File.Contents(story["Folders"]["Information"]["Writing"])["Lines"] != []:
				writing = self.JSON.To_Python(story["Folders"]["Information"]["Writing"])

			# Create the writing mode dictionaries inside the "Writing" dictionary
			for writing_mode in self.stories["Writing modes"]["List"]:
				# Define the writing mode dictionary
				if "Added" not in writing[writing_mode]["Times"]:
					writing[writing_mode]["Times"] = {
						"First": writing[writing_mode]["Times"]["First"],
						"Last": writing[writing_mode]["Times"]["Last"],
						"Added": "",
						**writing[writing_mode]["Times"]
					}

			# Define the root "Writing" dictionary as the local dictionary
			story["Information"]["Writing"] = writing

			# Write the default or modified "Writing" dictionary inside the "Writing.json" file
			self.JSON.Edit(story["Folders"]["Information"]["Writing"], story["Information"]["Writing"])

			# ---------- #

			# If the "Pack" dictionary is not present inside the "Information" dictionary
			if "Pack" not in story["Information"]:
				# Define the "Pack" dictionary of the current story as the default "Pack" dictionary
				story["Information"]["Pack"] = deepcopy(self.stories["Story pack"])

			# Write the default or modified "Pack" dictionary inside the "Pack.json" file
			self.JSON.Edit(story["Folders"]["Information"]["Pack"], story["Information"]["Pack"])

			# ---------- #

			# Define the "Links" dictionary
			story["Information"]["Links"] = {
				"Website": {}
			}

			# ---------- #

			# "Website" dictionary

			# Create the empty "Website" dictionary with the "Link" and "Links" keys
			story["Information"]["Website"] = {
				"Link": "",
				"Links": {}
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

			# Define the story website link by adding the website folder to the root Stake2 website link
			story["Information"]["Website"]["Link"] = self.website["URL"] + website_folder + "/"

			# Iterate through the list of small languages
			for language in self.languages["Small"]:
				# Define the language link with the language folder
				story["Information"]["Website"]["Links"][language] = story["Information"]["Website"]["Link"] + language + "/"

			# Update the "Website" dictionary inside the "Links" dictionary with the dictionary above
			story["Information"]["Links"]["Website"] = story["Information"]["Website"]

			# Write the default or modified "Website" dictionary inside the "Website.json" file
			self.JSON.Edit(story["Folders"]["Information"]["Website"], story["Information"]["Website"])

			# ---------- #

			# "Wattpad" and "Spirit Fanfics" dictionaries

			# Define the "Story websites" dictionary for the story
			self.Define_Story_Websites(story)

			# ---------- #

			# Write the default or modified "Links" dictionary inside the "Links.json" file
			self.JSON.Edit(story["Folders"]["Information"]["Links"], story["Information"]["Links"])

			# ----- #

			# Define an initial story links text with the "Story website:" text and a line break
			story_links = self.language_texts["story_website"] + ":" + "\n"

			# Replace spaces with "%20" inside the root website link, to make the link clickable
			link = story["Information"]["Website"]["Link"].replace(" ", "%20")

			# Add the root website link and a line break
			story_links += link + "\n"

			# Get the language website links
			links = list(story["Information"]["Website"]["Links"].values())

			# Iterate through the language website links
			for link in links:
				# Replace spaces with "%20" inside the language website link, to make the link clickable
				replaced_link = link.replace(" ", "%20")

				# Add the language website link
				story_links += replaced_link

				# If the link is not the last one
				if link != links[-1]:
					# Add a line break
					story_links += "\n"

			# Define an empty local story websites dictionary
			story_websites = {}

			# Iterate through the root story websites dictionary
			for key in self.stories["Story websites"]["Dictionary"]:
				# Get the links dictionary of the story website
				links = story["Information"]["Links"][key]["Links"]

				# If the links dictionary is not empty
				if links != {}:
					# List the links and add them to the local story websites dictionary
					story_websites[key] = list(links.values())

			# Get the keys of the local story websites dictionary
			keys = list(story_websites.keys())

			# Iterate through the local story websites dictionary
			for key, links in story_websites.items():
				# If the story website is the first one
				if key == keys[0]:
					# Add a line breaks to the start
					story_links += "\n"

				# Add the story website name, a colon, and a line break
				story_links += "\n" + key + ":" + "\n"

				# List the links

				# Add the language links for the story on the story website
				for link in links:
					story_links += link

					# If the link is not the last one
					if link != links[-1]:
						# Add a line break
						story_links += "\n"

				# If the story website is not the last one
				if key != keys[-1]:
					# Add a line break
					story_links += "\n"

			# Write the story links text into the "Story links.txt" file
			self.File.Edit(story["Folders"]["Information"]["Story links"], story_links, "w")

			# Remove the "Website" key as it is not needed anymore
			story["Information"].pop("Website")

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
				"Links"
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

			# Add the "Title" key to the top of the dictionary
			story["Information"] = {
				"Title": story["Title"],
				**story["Information"]
			}

			# Define a list of keys to remove from the "Information" dictionary
			keys_to_remove = [
				"Story titles",
				"History of story titles",
				"Story links"
			]

			# Iterate through the list of keys
			for key in keys_to_remove:
				# If the key is present, remove it
				if key in story["Information"]:
					story["Information"].pop(key)

			# ---------- #

			# Update the "Story.json" file with the updated story "Information" dictionary
			self.JSON.Edit(story["Folders"]["Story"], story["Information"])

			# ---------- #

			# Add the "Story" dictionary to the root "Stories" dictionary
			self.stories["Dictionary"][story_title] = story

			# Add one to the "s" number variable
			s += 1

		# Update the "Stories list.txt" file with the updated  list of story titles in the user language
		text_to_write = self.Text.From_List(self.stories["Titles"]["Language"], next_line = True)

		self.File.Edit(self.stories["Folders"]["Stories list"], text_to_write, "w")

		# Make a copy of the "Stories" dictionary
		stories_dictionary = deepcopy(self.stories)

		# Remove the unneeded keys
		keys = [
			"Folders",
			"Story pack",
			"Writing",
			"Directories",
			"Information items",
			"Story websites",
			"Cover types",
			"Writing modes"
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
						for language in self.languages["Small"]:
							# Get the full language
							full_language = self.languages["Full"][language]

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

					# Create the file
					self.File.Create(folder_dictionary[sub_key])

					# If the file type is "JSON"
					if file_type == "JSON":
						# Read the contents of the file
						file = folder_dictionary[sub_key]

						contents = self.File.Contents(file)

						# If the file is empty
						if contents["lines"] == []:
							# Write an empty JSON dictionary to the file
							self.JSON.Edit(file, {})

		# Return the "Story" dictionary
		return story

	def Create_Statistics(self, years_list):
		# Define a local dictionary of statistics
		statistics = {
			"Module": "Stories",
			"Statistic key": "Story chapters",
			"Text": {},
			"List": [],
			"Years": {}
		}

		# ---------- #

		# Create a local list of writing modes
		writing_modes = []

		# Iterate through the dictionary of writing modes
		for writing_mode in self.stories["Writing modes"]["Dictionary"].values():
			# Define the writing mode key as the "Chapter" tense
			# Chapter [written/revised/translated]
			key = writing_mode["Texts"]["Chapter"]["en"].capitalize()

			# Add the key to the local writing modes list
			writing_modes.append(key)

		# Iterate through the stories dictionary
		for story_key, story in self.stories["Dictionary"].items():
			# Add the English story title to the statistics list
			statistics["List"].append(story_key)

		# ---------- #

		# Fill the "Years" dictionary

		# Iterate through the list of years from 2020 to the current year
		for year_number in years_list:
			# Create the year dictionary
			year = {
				"Key": year_number,
				"Total": 0,
				"Numbers": {},
				"Months": {}
			}

			# Iterate through the stories dictionary
			for story_key, story in self.stories["Dictionary"].items():
				# Create the year numbers dictionary of the story
				year["Numbers"][story_key] = {
					"Total": 0,
					"Dictionary": {}
				}

				# Iterate through the local list of writing modes in the "Done" tense (Chapter [written/revised/translated])
				for writing_mode in writing_modes:
					# Add the writing mode key to the year numbers dictionary
					year["Numbers"][story_key]["Dictionary"][writing_mode] = 0

			# ---------- #

			# Fill the "Months" dictionary
			for month in range(1, 13):
				# Add leading zeroes to the month number
				month_number = str(self.Text.Add_Leading_Zeroes(month))

				# Create the month dictionary
				month = {
					"Key": month_number,
					"Total": 0,
					"Numbers": {}
				}

				# Iterate through the stories dictionary
				for story_key, story in self.stories["Dictionary"].items():
					# Create the year numbers dictionary of the story
					month["Numbers"][story_key] = {
						"Total": 0,
						"Dictionary": {}
					}

					# Iterate through the local list of writing modes in the "Done" tense (Chapter [written/revised/translated])
					for writing_mode in writing_modes:
						# Add the writing mode key to the month numbers dictionary
						month["Numbers"][story_key]["Dictionary"][writing_mode] = 0

				# Add the month dictionary to the "Months" dictionary of the year dictionary
				year["Months"][month_number] = month

			# ---------- #

			# Add the year dictionary to the "Years" dictionary
			statistics["Years"][year_number] = year

		# Iterate through the stories dictionary
		for story_key, story in self.stories["Dictionary"].items():
			# Iterate through the dictionary of story chapters
			for chapter in story["Information"]["Chapters"]["Dictionary"].values():
				# Make a shortcut for the "Dates" dictionary
				dates = chapter["Dates"]

				# Iterate through the local list of writing modes in the "Done" tense (Chapter [written/revised/translated])
				for writing_mode in writing_modes:
					# Get the date from the current writing mode
					date = dates[writing_mode]

					# If the date is not empty
					if date != "":
						# Split the date
						split = date.split("/")

						# ----- #

						# Get the current year number
						year_number = split[2]

						# If the year number is inside the list of years
						if year_number in years_list:
							# Add one to the total number inside the current year dictionary of the current story
							statistics["Years"][year_number]["Numbers"][story_key]["Total"] += 1

							# Add one to the writing mode number inside the current year dictionary of the current story
							statistics["Years"][year_number]["Numbers"][story_key]["Dictionary"][writing_mode] += 1

							# Add one to the year total chapters number
							statistics["Years"][year_number]["Total"] += 1

							# Define a shortcut for the year dictionary
							year_dictionary = statistics["Years"][year_number]

							# ----- #

							# Get the current month number of the current year
							month_number = split[1]

							# Add one to the total number inside the current year dictionary of the current story
							year_dictionary["Months"][month_number]["Numbers"][story_key]["Total"] += 1

							# Add one to the writing mode number inside the current year dictionary of the current story
							year_dictionary["Months"][month_number]["Numbers"][story_key]["Dictionary"][writing_mode] += 1

							# Add one to the month total chapters number
							year_dictionary["Months"][month_number]["Total"] += 1

		# Iterate through the dictionary of years
		for year in statistics["Years"].values():
			# Iterate through the stories inside the year dictionary
			for story_key, story in deepcopy(year["Numbers"]).items():
				# Define a local number of chapters
				number = 0

				# Iterate through the local list of writing modes in the "Done" tense (Chapter [written/revised/translated])
				for writing_mode in writing_modes:
					# Add the writing mode number to the local number
					number += story["Dictionary"][writing_mode]

				# If the final local number is still zero, remove the story dictionary
				if number == 0:
					year["Numbers"].pop(story_key)

			# Iterate through the month keys and month dictionaries inside the year "Months" dictionary
			for month_key, month in deepcopy(year["Months"]).items():
				# If the number of total chapters of the month is zero
				if month["Total"] == 0:
					# Remove the month from the dictionary of months
					year["Months"].pop(month_key)

				# If it is not zero
				else:
					# Iterate through the stories inside the month dictionary
					for story_key, story in deepcopy(month["Numbers"]).items():
						# Define a local number of chapters
						number = 0

						# Iterate through the local list of writing modes in the "Done" tense (Chapter [written/revised/translated])
						for writing_mode in writing_modes:
							# Add the writing mode number to the local number
							number += story["Dictionary"][writing_mode]

						# If the final local number is still zero, remove the story dictionary
						if number == 0:
							year["Months"][month_key]["Numbers"].pop(story_key)

		# Iterate through the dictionary of years
		for year_key, year in deepcopy(statistics["Years"]).items():
			# If the "Numbers" and "Months" dictionaries are empty
			if (year["Numbers"], year["Months"]) == ({}, {}):
				# Remove the year from the "Years" dictionary
				statistics["Years"].pop(year_key)

		# Add the local statistics dictionary to the root "Stories" dictionary
		self.stories["Statistics"] = statistics

		# Return the "Statistics" dictionary
		return self.stories["Statistics"]

	def Update_Statistics(self, story_titles, writing_mode):
		# Import the "Diary_Slim" module
		from Diary_Slim.Diary_Slim import Diary_Slim as Diary_Slim

		# Define the "Diary_Slim" class inside this class
		self.Diary_Slim = Diary_Slim()

		# Get the "diary_slim" dictionary from the class above
		self.diary_slim = self.Diary_Slim.diary_slim

		# ---------- #

		# Create a local list of writing modes
		writing_modes = []

		# Iterate through the dictionary of writing modes
		for item in self.stories["Writing modes"]["Dictionary"].values():
			# Define the writing mode key as the "Chapter" tense
			# Chapter [written/revised/translated]
			key = item["Texts"]["Chapter"]["en"].capitalize()

			# Add the key to the local writing modes list
			writing_modes.append(key)

		# ---------- #

		# Define a local dictionary of statistics
		statistics = {
			"Module": "Stories",
			"Statistic key": "Story chapters",
			"External statistic": True,
			"Year": {},
			"Month": {},
			"Text": "",
			"Dictionary": {
				"Numbers": {
					"Year": {
						"Old": 0,
						"New": 1
					},
					"Month": {
						"Old": 0,
						"New": 1
					}
				},
				"Text": ""
			}
		}

		# Define a shortcut for the statistic key
		statistic_key = statistics["Statistic key"]

		# ---------- #

		# Iterate through the list of keys
		for key in ["Year", "Month"]:
			# Define the default dictionary as the year dictionary
			dictionary = self.diary_slim["Current year"]

			# If the key is "Month"
			if key == "Month":
				# Define the default dictionary as the month dictionary
				dictionary = self.diary_slim["Current year"]["Month"]

			# Get the year statistics for the "Stories" module
			statistics[key] = dictionary["Statistics"][statistic_key]

			# If the story title is not inside the dictionary of stories
			if story_titles["en"] not in statistics[key]["Dictionary"]:
				# Create the story statistics dictionary
				statistics[key]["Dictionary"][story_titles["en"]] = {
					"Total": 0,
					"Dictionary": {}
				}

				# Iterate through the local list of writing modes in the "Done" tense (Chapter [Written/Revised/Translated])
				for item in writing_modes:
					# Add the writing mode key to the story statistics dictionary
					statistics[key]["Dictionary"][story_titles["en"]]["Dictionary"][item] = 0

			# Add one to the total number of statistics
			statistics[key]["Total"] += 1

			# ---------- #

			# Define the old number as the current number
			statistics["Dictionary"]["Numbers"][key]["Old"] = statistics[key]["Dictionary"][story_titles["en"]]["Dictionary"][writing_mode["Key"]]

			# Add one to the total writing number of the story
			statistics[key]["Dictionary"][story_titles["en"]]["Total"] += 1

			# Update the number of chapters written in the defined writing mode
			statistics[key]["Dictionary"][story_titles["en"]]["Dictionary"][writing_mode["Key"]] += writing_mode["Number"]

			# ---------- #

			# Define the new number as the current number (with the added number)
			statistics["Dictionary"]["Numbers"][key]["New"] = statistics[key]["Dictionary"][story_titles["en"]]["Dictionary"][writing_mode["Key"]]

		# Define the statistic text, formatting the template with the language story title
		statistics["Text"] = self.language_texts["chapters_of_my_story_{}_{}"].format(story_titles[self.language["Small"]], writing_mode["Done plural"])

		# ---------- #

		# Update the external statistics of the current year using the "Update_External_Statistics" root method of the "Diary_Slim" class
		# And return the statistics text
		return self.Diary_Slim.Update_External_Statistics(statistic_key, statistics)

	def Select_Status(self):
		# Define the parameters dictionary for the "Select" method of the "Input" class
		parameters = {
			"options": self.texts["status, type: list"]["en"],
			"language_options": self.language_texts["status, type: list"],
			"show_text": self.language_texts["writing_statuses"],
			"select_text": self.language_texts["select_a_writing_status"]
		}

		if self.switches["Testing"] == False:
			# Ask the user to select a status from the list
			option = self.Input.Select(**parameters)

		if self.switches["Testing"] == True:
			option = {
				"number": 0,
				"option": self.texts["write, type: dictionary"]["Infinitive action"]["en"],
				"language_option": self.language_texts["write, type: dictionary"]["Infinitive action"]
			}

			print()
			print(self.language_texts["writing_status"] + ":")
			print(option["language_option"])

		# Create the "Status" dictionary
		status = {
			"Number": option["number"],
			"Names": {
				"en": option["option"],
				self.language["Small"]: option["language_option"]
			}
		}

		# Return the "Status" dictionary
		return status

	def Select_Author(self):
		# Define a local list of authors with the first root author
		authors = [
			self.stories["Authors"]["List"][0]
		]

		# Show the list of authors
		self.Show_Authors_List(authors)

		# Define the question to ask the user if they want to add more authors to the list of authors
		question = self.language_texts["do_you_want_to_add_more_authors"]

		# If the "Testing" switch is False
		if self.switches["Testing"] == False:
			# Ask the yes or no question
			add_more = self.Input.Yes_Or_No(question)

		# If the "Testing" switch is True
		if self.switches["Testing"] == True:
			# Then do not add more authors
			add_more = False

		# If the user wants to add more authors
		if add_more == True:
			# Make a copy of the root list of authors
			options = deepcopy(self.stories["Authors"]["List"])

			# Remove the first author (me) because it is always the first author of all stories
			options.pop(0)

			# Define the parameters dictionary for the "Select" method of the "Input" class
			parameters = {
				"options": options, # The local list of authors
				"language_options": deepcopy(options), # A copy of the local list of authors
				"show_text": self.Language.language_texts["authors, title()"], # The show text "Authors"
				"select_text": self.language_texts["select_an_additional_author"] # The select text telling the user to select an additional author
			}

			# Define the "finish selection" variable for easier typing
			finish_selection = "[Finish selection]"

			# Add the "[Finish selection]" text to the list of options
			parameters["options"].append(finish_selection)

			# Define the "[Finish selection]" text in the user language
			language_text = "[" + self.Language.language_texts["finish_selection"] + "]"

			# Add the "[Finish selection]" text in the user language to the list of language options
			parameters["language_options"].append(language_text)

			# Define the default option as an empty variable
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

				# Ask the user to select an author from the list
				option = self.Input.Select(**parameters)["Option"]["Normal"]

				# If the option is not the "[Finish selection]" text
				if option != finish_selection:
					# Remove the selected text from the lists of options
					parameters["options"].remove(option)
					parameters["language_options"].remove(option)

					# Add the author to the list of authors
					authors.append(option)

					# If the number of options in the list of options is only one
					# That means the user selected all of the options of the list
					# (The last remaining option is "[Finish selection]")
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

		# ---------- #

		# If the "Entry" key is not inside the task dictionary
		if "Entry" not in task_dictionary:
			# Create it
			task_dictionary["Entry"] = {
				"Times": {}
			}

			# Register the completed task time in the "Times" dictionary
			time_key = "Completed task"
			task_dictionary["Entry"]["Times"][time_key] = self.Date.Now()

			# Register the completed task time in the UTC time
			task_dictionary["Entry"]["Times"][time_key + " (UTC)"] = task_dictionary["Entry"]["Times"][time_key]

		# ---------- #

		# Register the task with the "Register" class of the "Tasks" module
		if register_task == True:
			# Import the "Register" class of the "Tasks" module
			from Tasks.Register import Register as Register

			# Register the task
			Register(task_dictionary)

		# ---------- #

		# Register the task on the current "Diary Slim" file if the "Tasks" module did not
		if register_task == False:
			# Show a space separator
			print()

			# Import the "Write_On_Diary_Slim_Module" sub-class
			from Diary_Slim.Write_On_Diary_Slim_Module import Write_On_Diary_Slim_Module as Write_On_Diary_Slim_Module

			# Define the "Write on Diary Slim" dictionary
			dictionary = {
				"Text": task_dictionary["Task"]["Descriptions"][self.language["Small"]],
				"Time": self.task_dictionary["Entry"]["Date"]["Formats"]["HH:MM DD/MM/YYYY"],
				"Show text": True
			}

			# Write the task text on Diary Slim
			Write_On_Diary_Slim_Module(dictionary)

	def Select_Story(self, stories_list = [], select_text_parameter = None, select_class = False):
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

		# Define the list of stories if it the parameter is an empty list
		if stories_list == []:
			stories_list = self.stories["Titles"]["en"]

		# Empty the titles lists
		for language in self.languages["Small"]:
			stories["Titles"][language] = []

		# If the class name is "Post"
		if class_name == "Post":
			# Iterate through the English story titles list
			for story in stories_list.copy():
				# Get the "Story" dictionary
				story = stories["Dictionary"][story]
			
				# Get the last posted chapter number
				last_posted_chapter = story["Information"]["Chapters"]["Numbers"]["Last posted chapter"]

				# If the last posted chapter is the same as the last chapter
				if last_posted_chapter == story["Information"]["Chapters"]["Numbers"]["Total"]:
					# Remove the story from the list of stories
					stories_list.remove(story["Title"])

		# Iterate through the English story titles list
		for story in stories_list.copy():
			# Get the "Story" dictionary
			story = stories["Dictionary"][story]

			# Iterate through the small languages list
			for language in self.languages["Small"]:
				# Add the story title to the list of titles in the current language
				stories["Titles"][language].append(story["Titles"][language])

		# Define the options and language options lists
		options = stories["Titles"]["en"]
		language_options = stories["Titles"][self.language["Small"]]

		# Ask for the user to select the story
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
		show_text = self.language_texts["what_to_do_with_the_story"] + " " + '"' + self.story["Titles"][self.language["Small"]] + '"?'

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
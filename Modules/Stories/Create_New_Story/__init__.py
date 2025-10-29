# Create_New_Story.py

from Stories.Stories import Stories as Stories

from copy import deepcopy

class Create_New_Story(Stories):
	def __init__(self):
		super().__init__()

		# Define the root dictionary
		self.dictionary = {
			"Story": {}
		}

		# Type the information about the story
		self.Type_Story_Information()

		# Define the "Story" dictionary
		self.Define_Story_Dictionary()

		# Create the folders of the story
		self.Create_Story_Folders()

		# Update the files of the story
		self.Update_Files()

		# Add the list to the list of stories
		self.Add_To_Stories_List()

		# Execute the root class again to define the variables of the story
		super().__init__()

		# Import sub-classes method
		self.Import_Sub_Classes()

		# Show information about the story
		self.Show_Story_Information()

	def Type_Story_Information(self):
		# Define the default local "Story" dictionary
		story = {
			"Title": "",
			"Titles": {},
			"Folders": {},
			"Information": {}
		}

		# Show a five dash space separators
		print()
		print(self.separators["5"])

		# ---------- #

		# Ask for the titles of the story
		for language in self.languages["Small"]:
			# Get the translated language
			translated_language = self.languages["Full (translated)"][language][self.language["Small"]]

			# Ask for the story title
			text = self.language_texts["story_title_in"] + " " + translated_language

			if self.switches["Testing"] == False:
				title = self.Input.Type(text, accept_enter = False, next_line = True)

			if self.switches["Testing"] == True:
				title = self.Language.texts["story_title"][language]

				print()
				print(text + ":")
				print(title)

			# Add the story title to the "Titles" dictionary
			story["Titles"][language] = title

			# If the language is "English", define it as the root story title
			if language == "en":
				story["Title"] = title

		# Add the "Titles" dictionary to the "Information" dictionary
		story["Information"]["Titles"] = story["Titles"]

		# ---------- #

		# Create the "Chapters" dictionary
		story["Information"]["Chapters"] = {
			"Numbers": {
				"Total": 0,
				"Last posted chapter": 0
			},
			"Titles": {},
			"Dates": [],
			"Dictionary": {}
		}

		# ---------- #

		# Show a five dash space separator
		print()
		print(self.separators["5"])
		print()

		# Show the text telling the user to type the details about the story
		print(self.language_texts["type_the_information_of_the_story"] + ":")

		# Define the list of keys
		keys = list(self.stories["Information items"]["Dictionary"].keys())

		# Iterate through the information items in the "Information items" dictionary
		for key, information_item in self.stories["Information items"]["Dictionary"].items():
			# If the information item is not the first one
			if key != keys[0]:
				# Show a five dash space separators
				print()
				print(self.separators["5"])

				# Define the exclude list
				exclude_list = [
					"Status",
					"Synopsis",
					"Author"
				]

				# If the key is not in the list above
				if key not in exclude_list:
					print()

			# If the information item is "Creation date"
			if key == "Creation date":
				# Define the format variable for easier typing
				format = information_item["Format"]

				# Define the text of the information item
				text = information_item["Texts"][self.language["Small"]]

				# Update the information text to add the example
				new_text = text + ":" + "\n" + \
				"(" + self.Language.language_texts["leave_empty_to_use_the_default_value"] + ': "' + format["Example"] + '")'

				if self.switches["Testing"] == False:
					# Ask for the information
					information = self.Input.Type(new_text, next_line = True)

				if self.switches["Testing"] == True:
					information = ""

					print()

				# If the typed information is an empty string
				if information == "":
					# Define the information as the default information value
					information = self.Date.Now()["Formats"]["HH:MM DD/MM/YYYY"]

					# Show the default information
					print(text + ":")
					print(information)

				# If the typed information is not an empty string
				else:
					# Import the "re" module
					import re

					# Search for the regex in the typed information
					search = re.search(format["Regex"], information)

					# If the information does not match the regex
					if search == None:
						# Ask for the information again
						information = self.Input.Type(new_text, accept_enter = False, next_line = True, regex = format)

			# If the information item is "Synopsis"
			if key == "Synopsis":
				# Define the empty "Synopsis" dictionary
				information = {}

				# Iterate through the list of small languages
				for language in self.languages["Small"]:
					# Get the translated language
					translated_language = self.languages["Full (translated)"][language][self.language["Small"]]

					# Define the type text
					type_text = self.language_texts["story_synopsis_in"] + " " + translated_language

					if self.switches["Testing"] == False:
						# Ask for the lines of text for the synopsis
						synopsis = self.Input.Lines(type_text, line_options_parameter = {"next_line": True})["string"]

					if self.switches["Testing"] == True:
						synopsis = self.Language.texts["synopsis, title()"][language]

						print()
						print(type_text + ":")
						print(synopsis)

					# Add the synopsis to the "Synopsis" dictionary
					information[language] = synopsis

			# If there is no root method to select the information
			if "Method" not in information_item:
				# Add the information to the "Information" dictionary of the "Story" dictionary
				story["Information"][key] = information

			# If there is a root method to select the information
			if "Method" in information_item:
				# Use it to select the information
				information = information_item["Method"]()

				# Define the information inside the "Information" dictionary
				story["Information"][key] = information

				# If the information key is "Author"
				if key == "Author":
					# Add the selected information to the "Information" dictionary of the "Story" dictionary
					story["Information"][key] = information[0]

					# Define the list of authors as the information
					story["Information"]["Authors"] = information

					# If the length of the list of authors is more than one
					if len(information) > 1:
						# Transform the root into a text string with all the authors
						story["Information"][key] = self.Text.From_List(information)

		# ---------- #

		# Ask if the story has a parent story
		question = self.language_texts["does_the_story_has_a_parent_story"]

		if self.switches["Testing"] == False:
			parent_story = self.Input.Yes_Or_No(question)

		else:
			parent_story = True

		# If the story has a parent story
		if parent_story == True:
			# Ask for the title of the parent story
			type_text = self.language_texts["type_the_title_of_the_parent_story"]

			if self.switches["Testing"] == False:
				title = self.Input.Type(type_text, accept_enter = False, next_line = True)

			else:
				title = "Parent Story Title"

			# Create the "Parent story" dictionary
			story["Information"]["Parent story"] = {
				"Title": title
			}

		# ---------- #

		# Define the story "Links" dictionary
		story["Information"]["Links"] = {
			"Website": {}
		}

		# ---------- #

		# Define the "Wattpad" and "Spirit Fanfics" link dictionaries

		# Iterate through the dictionary of story websites
		for key, story_website in self.stories["Story websites"]["Dictionary"].items():
			# Ask if the user posted the story on the current story website
			question = self.language_texts["did_you_posted_the_story_on_the_story_website"] + ' "' + key + '"'

			if self.switches["Testing"] == False:
				posted_story = self.Input.Yes_Or_No(question)

			else:
				posted_story = True

			# If the user posted the story on the story website
			if posted_story == True:
				# Define the current story website dictionary inside the story dictionary
				self.Define_Story_Websites(story)

		# ---------- #

		# Define the "story" variable in the root class so it is available to the "Define_Story_Dictionary" method below
		self.story = story

	def Define_Story_Dictionary(self):
		# Define the "Readers" dictionary
		self.story["Information"]["Readers"] = {
			"Number": 0,
			"List": []
		}

		# ---------- #

		# Define the story "Pack" dictionary
		self.story["Information"]["Pack"] = deepcopy(self.stories["Story pack"])

		# ---------- #

		# Define the "Writing" dictionary
		self.story["Information"]["Writing"] = {}

		for writing_mode in self.texts["writing_modes, type: list"]["en"]:
			self.story["Information"]["Writing"][writing_mode] = {
				"Chapter": 0,
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

		# ---------- #

		# "Website" dictionary

		# Create the empty "Website" dictionary with the "Link" and "Links" keys
		self.story["Information"]["Website"] = {
			"Link": "",
			"Links": {}
		}

		# Define the story website folder as the story title
		website_folder = self.story["Title"]

		# If the story has a parent story
		if "Parent story" in self.story["Information"]:
			# Get the parent story dictionary
			parent_story = self.story["Information"]["Parent story"]

			# Define the website folder
			website_folder = parent_story["Title"]

			# If the parent story has a custom folder, use it
			if "Folder" in parent_story:
				website_folder = parent_story["Folder"]

			# Add the story title to the website folder
			website_folder += "/" + self.story["Title"]

			# Define the website folder
			self.story["Information"]["Website"]["Website folder"] = "/" + website_folder + "/"

		# Define the story website link by adding the website folder to the root Stake2 website link
		self.story["Information"]["Website"]["Link"] = self.website["URL"] + website_folder + "/"

		# Iterate through the list of small languages
		for language in self.languages["Small"]:
			# Define the language link with the language folder
			self.story["Information"]["Website"]["Links"][language] = self.story["Information"]["Website"]["Link"] + language + "/"

		# Update the "Website" dictionary inside the "Links" dictionary with the dictionary above
		self.story["Information"]["Links"]["Website"] = self.story["Information"]["Website"]

		# ---------- #

		# Define the "Wattpad" and "Spirit Fanfics" dictionaries

		# Iterate through the dictionary of story websites
		for key, story_website in self.stories["Story websites"]["Dictionary"].items():
			# Define the story website dictionary if it is not already present
			if key not in self.story["Information"]:
				# Define it as the story website root link template
				self.story["Information"][key] = story_website["Templates"]["Root"]

				# Update the story website dictionary inside the "Links" dictionary with the dictionary above
				self.story["Information"]["Links"][key] = self.story["Information"][key]

		# Define the "Story websites" dictionary for the story to update the JSON files for the story websites
		self.Define_Story_Websites(self.story)

		# ---------- #

		# Define the root "Story" dictionary as the local dictionary
		self.dictionary["Story"] = self.story

	def Create_Story_Folders(self):
		# Define and create the story folder
		root_folder = self.stories["Folders"]["root"]

		self.story["Folders"]["root"] = root_folder + self.story["Titles"][self.language["Small"]] + "/"
		self.Folder.Create(self.story["Folders"]["root"])

		# Create the sub-folders and files of the story
		self.story = self.Create_Story_Sub_Folders(self.story)

	def Update_Files(self):
		# Create the language synopsis files and add the synopsis to them

		# Define the root folder
		root_folder = self.story["Folders"]["Information"]["Synopsis"]["root"]

		# Iterate through the list of small languages
		for language in self.languages["Small"]:
			# Get the full language
			full_language = self.languages["Full"][language]

			# Define and create the file
			file = root_folder + full_language + ".txt"
			self.File.Create(file)

			# Write to the file
			self.File.Edit(file, self.story["Information"]["Synopsis"][language])

		# ---------- #
		
		# Update the "Authors.txt" file with the list of authors
		text_to_write = self.Text.From_List(self.story["Information"]["Authors"], next_line = True)

		self.File.Edit(self.story["Folders"]["Authors"], text_to_write, "w")

		# ---------- #

		# Write to the "Creation date" file, the JSON files, and the "Readers" file

		# Define the list of file names
		file_names = [
			"Creation date",
			"Readers"
		]

		# Add the JSON file names
		file_names += self.stories["Directories"]["Information"]["JSON"]

		# Iterate through the files inside the list of file names
		for file_name in file_names:
			# Define the default class for writing into the file
			Class = self.File

			# If the file name is inside the list of JSON files
			if file_name in self.stories["Directories"]["Information"]["JSON"]:
				# Define the class for writing into the file as the "JSON" class
				Class = self.JSON

			# If the file name exists inside the "Information" folders dictionary
			if file_name in self.story["Folders"]["Information"]:
				# Define the file variable for easier typing
				file = self.story["Folders"]["Information"][file_name]

			# If not, then it must be on the "Readers" folder
			else:
				file = self.story["Folders"]["Readers"][file_name]

			# Define the text to be written on the file
			text = self.story["Information"][file_name]

			# If the file name is "Readers"
			if file_name == "Readers":
				# Transform the list of readers into a text string
				text = self.Text.From_List(text["List"], next_line = True)

			# Write to the file
			Class.Edit(file, text)

		# ---------- #

		# Remove the keys inside the "Links" dictionary if they exist outside of it
		for key in self.story["Information"]["Links"]:
			if key in self.story["Information"]:
				self.story["Information"].pop(key)

		# ---------- #

		# Update the "Story.json" file with the new story "Information" dictionary
		self.JSON.Edit(self.story["Folders"]["Story"], self.story["Information"])

	def Add_To_Stories_List(self):
		# Add to the list of stories
		self.stories["List"].append(self.story["Title"])

		# Sort the list of stories
		self.stories["List"] = sorted(self.stories["List"], key = str.lower)

		# Add the story to the stories "Dictionary"
		self.stories["Dictionary"][self.story["Title"]] = self.story

		# Make a copy of the "Stories" dictionary
		stories_dictionary = deepcopy(self.stories)

		# Remove the unneeded keys
		keys = [
			"Folders",
			"Story pack",
			"Writing",
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

		# ---------- #

		# Add to the list of story titles in the user language, in the correct index
		index = self.stories["List"].index(self.story["Title"])
		language_story_title = self.story["Titles"][self.language["Small"]]

		# Update the "Stories list.txt" file with the updated list of story titles in the user language
		text_to_write = self.Text.From_List(self.stories["Titles"][self.language["Small"]], next_line = True)

		self.File.Edit(self.stories["Folders"]["Stories list"], text_to_write, "w")

	def Import_Sub_Classes(self):
		# Import the "importlib" module
		import importlib

		# Define the classes to be imported
		classes = [
			"Show_Story_Information"
		]

		# Import them
		for title in classes:
			# Import the module
			module = importlib.import_module("." + title, self.__module__.split(".")[0])

			# Get the sub-class
			sub_class = getattr(module, title)

			# Add the sub-class to the current module
			setattr(Stories, title, sub_class)

	def Show_Story_Information(self):
		# Define the list of stories
		stories_list = [
			self.story["Title"]
		]

		# Execute the "Show_Story_Information" sub-class
		Stories.Show_Story_Information(self, stories_list)
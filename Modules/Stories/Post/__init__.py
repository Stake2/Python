# Post.py

# Import the root class
from Stories.Stories import Stories as Stories

# Import some useful modules
from copy import deepcopy

class Post(Stories):
	def __init__(self, posting = {}):
		# Run the root class to import its methods and variables
		super().__init__()

		# Define the root "posting" dictionary
		self.posting = {
			"Steps": {
				"List": [],
				"Dictionary": {}
			},
			"Posting modes": {
				"List": [],
				"Dictionary": {}
			},
			"Posting mode": {},
			"Chapter": {}
		}

		# Define the root states dictionary
		self.states = {
			"Has chapters to post": False,
			"Select a chapter": False,
			"Update all chapter covers": False
		}

		# If the posting parameter dictionary is not empty
		# And the "States" dictionary is inside the posting parameter dictionary
		if (
			posting != {} and
			"States" in posting
		):
			# Iterate through the "States" dictionary
			for key, state in posting["States"]:
				# If the state key is present inside the root states dictionary
				if key in self.states:
					# Replace the root state with the local parameter state
					self.states[key] = state

		# ---------- #

		# Import some sub-classes
		self.Import_Sub_Classes()

		# Check if the story has chapters to be posted
		self.Check_Story_Chapters()

		# If the story still has no chapters to post after running the previous method
		if self.states["Has chapters to post"] == False:
			# Check if the story has chapters to be posted
			self.Check_For_Chapters_To_Be_Posted()

		# If the story has chapters to post
		if self.states["Has chapters to post"] == True:
			# Define and run the chapter posting steps
			self.Define_And_Run_Steps()

		# Run the root class to update the files and dictionaries of the selected story
		super().__init__()

	def Import_Sub_Classes(self):
		# Import the "importlib" module
		import importlib

		# Define the classes to be imported
		classes = [
			"Social_Networks.Open_Social_Network",
			"PHP.Update_Websites"
		]

		# Import them
		for class_title in classes:
			# Define the module title as the class title
			module_title = class_title

			# If there is a dot in the module title
			if "." in module_title:
				# Split the module title to get the actual module title
				module_title = module_title.split(".")[0]

				# Get the class title
				class_title = class_title.split(".")[1]

			# Import the module
			module = importlib.import_module("." + class_title, module_title)

			# Get the sub-class
			sub_class = getattr(module, class_title)

			# Add the sub-class to the current module
			setattr(self, class_title, sub_class)

	def Check_Story_Chapters(self):
		# Define a shortcut to the story "Chapters" dictionary
		chapters = self.story["Chapters"]

		# Define a shortcut to the last chapter written
		last_chapter = chapters["Numbers"]["Total"]

		# Define a shortcut to the story "Writing" dictionary
		writing = self.story["Writing"]

		# Define shortcuts for the "Write", "Revise", and "Translate" writing dictionaries
		write = writing["Write"]
		revise = writing["Revise"]
		translate = writing["Translate"]

		# Define a list of the finished status from both revise and translate
		finished_status = [
			revise["Status"]["Finished"],
			translate["Status"]["Finished"]
		]

		# Define a "ready to post" dictionary
		ready_to_post = {
			# If the last written chapter has been finished and has not been posted yet
			"Written chapter": (
				write["Status"]["Finished"] and
				not write["Status"]["Posted"]
			),

			# If the current chapters to revise and translate are the same
			# Both are finished, and the revised chapter has not been posted yet
			"Revised chapter": (
				revise["Current chapter"] == translate["Current chapter"] and
				all(finished_status) and
				not revise["Status"]["Posted"]
			)
		}

		# If any of the conditions are True
		if any(ready_to_post.values()):
			# Then change the "Has chapters to post" state to True
			self.states["Has chapters to post"] = True

	def Check_For_Chapters_To_Be_Posted(self):
		# Define the text template to say that all chapters of that story have been posted
		text_template = self.language_texts["all_chapters_of_the_story_{}_have_been_posted_please_select_another_story"]

		# Make a local copy of the "Stories" dictionary
		stories = deepcopy(self.stories)

		# Define a local list of stories as the story titles in English
		stories_list = stories["Titles"]["en"]

		# While the "Has chapters to post" is False
		# And the list of stories is not empty
		while (
			self.states["Has chapters to post"] == False and
			stories_list != []
		):
			# Show a five dash space separator
			print()
			print(self.separators["5"])
			print()

			# Define the list of items to use to format the text template
			items = [
				self.story["Titles"][self.language["Small"]] # The story title in the user language
			]

			# Format the text template with the list of items
			text = text_template.format(*items)

			# Show the text
			print(text)

			# Remove the previously selected story from the local list of stories
			stories_list.remove(self.story["Title"])

			# Ask the user to select another story to post its chapters
			self.Select_Story(stories_list = self.stories_list)

			# Check if the selected story has chapters to post
			self.Check_Story_Chapters()

		# If all stories have been selected and none of them have chapters to be posted
		if stories_list == []:
			# Show a five dash space separator
			print()
			print(self.separators["5"])
			print()

			# Tell the user that no story has chapters to be posted
			text = self.language_texts["no_story_has_chapters_to_be_posted"]

			print(text + ".")

			# End the program execution
			quit()

	def Define_And_Run_Steps(self):
		# Define the list of chapter posting steps
		self.posting["Steps"]["List"] = [
			"Select posting mode",
			"Define chapter",
			"Create chapter covers",
			"Update story website",
			"Post chapter on story websites",
			"Post on the social networks",
			"Update chapter dictionary",
			"Register task",
			"Write on Diary Slim"
		]

		# If the "Update all chapter covers" state is True
		if self.states["Update all chapter covers"] == True:
			# Define the list of chapter posting steps to be only "Define chapter" and "Create chapter covers"
			self.posting["Steps"]["List"] = [
				"Define chapter",
				"Create chapter covers"
			]

		# Iterate through the list of chapter posting steps
		for key in self.posting["Steps"]["List"]:
			# Define the method name for the step by converting the key into title case and replacing spaces with underlines
			method_name = key.title().replace(" ", "_")

			# Define the posting step dictionary with the key, method name, and method
			self.posting["Steps"]["Dictionary"][key] = {
				"Key": key,
				"Method name": method_name,
				"Method": getattr(self, method_name)
			}

		# Iterate through the posting step dictionaries inside the "Steps" dictionary
		for step in self.posting["Steps"]["Dictionary"].values():
			# If the "Testing" switch is True
			# And the "Method" is a string
			if (
				self.switches["Testing"] == True and
				type(step["Method"]) == str
			):
				# Show the method name
				print()
				print(step["Method name"] + ":")

			# If the step is not "Register task"
			# Or it is and the posting mode is not "Revised"
			if (
				step["Key"] != "Register task" or
				step["Key"] == "Register task" and
				self.posting_mode != "Revised"
			):
				# Run the method of the posting step
				step["Method"]()

	def Select_Posting_Mode(self):
		# Copy the "Writing modes" dictionary and call it "Posting modes"
		self.posting["Posting modes"] = deepcopy(self.stories["Writing modes"])

		# Remove the "Translate" posting mode from the "Posting modes" list and dictionary
		# Because translated chapters are never posted, only written and revised chapters
		self.posting["Posting modes"]["List"].remove("Translate")
		self.posting["Posting modes"]["Dictionary"].pop("Translate")

		# Define the parameters dictionary to use inside the "Select" method of the "Input" utility module
		parameters = {
			"options": self.posting["Posting modes"]["List"], # The list of posting modes
			"language_options": [], # The empty list of language posting modes
			"show_text": self.language_texts["posting_modes"], # The "Posting modes" text in the user language
			"select_text": self.language_texts["select_a_posting_mode"] # The "Select a posting mode" text in the user language
		}

		# ---------- #

		# Define a shortcut to the "language texts" dictionary of the "Language" class
		language_texts = self.Language.language_texts

		# Iterate through the posting modes and posting mode dictionaries
		for posting_mode, posting_mode_dictionary in deepcopy(self.posting["Posting modes"]["Dictionary"]).items():
			# Define a shortcut to the current posting mode dictionary
			writing_dictionary = self.story["Writing"][posting_mode]

			# Define a shortcut to the "Status" dictionary
			status = writing_dictionary["Status"]

			# Get the current chapter of the current posting mode
			current_chapter = writing_dictionary["Current chapter"]

			# ----- #

			# If the chapter was finished and was not posted yet
			if (
				status["Finished"] == True and
				status["Posted"] == False
			):
				# Define the posting mode template text initially as "Post the chapter {} that was {}"
				text_template = self.language_texts["post_the_chapter_{}_that_was_{}"]

				# Define the verb tense to use as the "Chapter" one
				# [written/revised]
				verb_tense = posting_mode_dictionary["Language texts"]["Chapter"]

				# Define the list of items to use to format the text template
				items = [
					str(current_chapter), # The chapter number
					verb_tense # The "Chapter" verb tense ([written/revised])
				]

				# Format the text template with the list of items to create the posting mode text
				posting_mode_text = text_template.format(*items)

				# Add the posting mode text to the list of language options
				parameters["language_options"].append(posting_mode_text)

				# Add the posting mode text to the posting mode dictionary
				posting_mode_dictionary["Posting mode text"] = posting_mode_text

				# ----- #

				# Define the posting mode template text initially as "post_the_{}_chapter"
				text_template = self.language_texts["post_the_{}_chapter"]

				# Define the list of items to use to format the text template
				items = [
					verb_tense # The "Chapter" verb tense ([written/revised])
				]

				# Format the text template with the list of items to create the chapter text
				posting_mode_text = text_template.format(*items)

				# Add the chapter text to the posting mode dictionary
				posting_mode_dictionary["Chapter text"] = posting_mode_text

			# Define the old key as the posting mode
			# [write/revise]
			old_key = posting_mode

			# Define the new key as the "Chapter" verb tense
			# [Written/Revised]
			new_key = posting_mode_dictionary["Texts"]["Chapter"]["en"].capitalize()

			# Update the name to be the new key
			posting_mode_dictionary["Name"] = new_key

			# Update the names to be the "Chapter" verb tense dictionary
			posting_mode_dictionary["Names"] = posting_mode_dictionary["Texts"]["Chapter"]

			# Make a copy of the names
			names = deepcopy(posting_mode_dictionary["Names"])

			# Capitalize the names
			for key, name in names.items():
				posting_mode_dictionary["Names"][key] = name.capitalize()

			# Add the current chapter to the "Chapter" key
			posting_mode_dictionary["Chapter"] = current_chapter

			# Remove the old key
			self.posting["Posting modes"]["List"].remove(old_key)
			self.posting["Posting modes"]["Dictionary"].pop(old_key)

			# Add the new key
			self.posting["Posting modes"]["List"].append(new_key)
			self.posting["Posting modes"]["Dictionary"][new_key] = posting_mode_dictionary

			# If the chapter was finished and is already posted
			if (
				status["Finished"] == True and
				status["Posted"] == True
			):
				# Then remove the posting mode from the list
				self.posting["Posting modes"]["List"].remove(new_key)

		# ----- #

		# Show a five dash space separator
		print()
		print(self.separators["5"])

		# Define a local "automatically selected" state
		automatically_selected = False

		# If there is more than one posting mode
		if len(self.posting["Posting modes"]["List"]) > 1:
			# Ask the user to select a posting mode
			posting_mode = self.Input.Select(**parameters)["Option"]["Original"]

		else:
			# Define the posting mode as the only one
			posting_mode = self.posting["Posting modes"]["List"][0]

			# Change the "automatically selected" state to True
			automatically_selected = True

		# Get the posting mode dictionary for the selected posting mode
		self.posting["Posting mode"] = self.posting["Posting modes"]["Dictionary"][posting_mode]

		# If the posting mode was automatically selected
		if automatically_selected == True:
			# Show the "This posting mode was automatically selected because it was the only one" in the user language and also the chapter text
			print()
			print(self.language_texts["this_posting_mode_was_automatically_selected_because_it_was_the_only_one"] + ":")
			print("[" + self.posting["Posting mode"]["Chapter text"] + "]")

		# Define the "posting mode" root variable as the posting mode name for faster typing
		self.posting_mode = posting_mode

	def Define_Chapter(self, chapter_number = None):
		# If the chapter number parameter is None
		if chapter_number == None:
			# Define it as the chapter of the posting mode
			chapter_number = self.posting["Posting mode"]["Chapter"]

		# Define the "Chapter" dictionary using the root "Select_Chapter" method, passing the chapter number to it
		self.posting["Chapter"] = self.Select_Chapter(chapter_number = chapter_number)

		# Define a shortcut to the chapter dictionary
		self.chapter = self.posting["Chapter"]

		# Get the chapter dictionary key of the posting mode
		chapter_dictionary_key = self.posting["Posting mode"]["Texts"]["Chapter dictionary"]

		# Get the writing dictionary of the selected chapter dictionary
		writing_dictionary = self.chapter["Dictionary"][chapter_dictionary_key]

		# If the posting mode is "Written"
		if self.posting_mode == "Written":
			# Define the writing as the writing dictionary
			writing = writing_dictionary

		# If the posting mode is "Revised"
		if self.posting_mode == "Revised":
			# Get the list of writings
			writings = list(writing_dictionary["Dictionary"].values())

			# Get the last writing and define it as the writing variable
			writing = writings[-1]

		# Get the "Finished" writing date of the writing
		writing_date = writing["Times"]["Finished"]

		# Define the date dictionary using the defined writing date
		date = self.Date.From_String(writing_date, "%H:%M %d/%m/%Y")

		# Define the correct date format text based on the user language
		date_format_text = self.Date.texts["date_format, type: format"][self.language["Small"]]

		# Replace the date strings in the date format text with the units and texts inside the date dictionary
		date_text = self.Date.Replace_Strings_In_Text(date_format_text, date, self.language["Small"])

		# Get the writing time (hours and minutes) of the date
		writing_time = date["Timezone"]["DateTime"]["Formats"]["HH:MM"]

		# Get the writing duration
		writing_duration = writing["Times"]["Duration"]["Text"]

		# Define the writing duration with time units dictionary
		writing_duration_with_time_units = {}

		# Iterate through list of small languages
		for language in self.languages["Small"]:
			# Get the writing duration text in the current language
			duration_text = writing_duration[language]

			# Get the time units
			time_units_text = self.Date.Create_Time_Units_Text({"Difference": writing["Times"]["Duration"]})

			# Add it
			duration_text += " (" + time_units_text + ")"

			# Add the duration text to the dictionary
			writing_duration_with_time_units[language] = duration_text

		# Define the writing dictionary inside the "Chapter" dictionary with the date and time
		self.chapter["Writing"] = {
			"Date": date_text,
			"Time": writing_time,
			"Duration": writing_duration[self.language["Small"]],
			"Duration (with time units)": writing_duration_with_time_units
		}

		# ---------- #

		# Define the chapter "Covers" dictionary
		self.chapter["Covers"] = {
			"Folder name": self.Cover_Folder_Name(self.chapter["Number"]) # Add the cover folder name
		}

		# Iterate through the list of chapter cover types
		for cover_type in self.stories["Cover types"]["List"]:
			# Define the chapter cover type dictionary
			cover_type_dictionary = {
				"Folders": {},
				"Files": {}
			}

			# If the cover type is "Landscape"
			if cover_type == "Landscape":
				# Add the "Story" and "Website" dictionaries to the "Folders" and "Files" dictionaries
				for item_type in ["Folders", "Files"]:
					for item in ["Story", "Website"]:
						cover_type_dictionary[item_type][item] = {}

			# Iterate through the language keys and dictionaries
			for small_language, language in self.languages["Dictionary"].items():
				# Define a shortcut to the full language
				full_language = language["Full"]

				# Define a shortcut to the root cover folder
				root_folder = self.story["Folders"]["Covers"][cover_type][small_language]["root"]

				# Define the local cover folder as the folders dictionary
				cover_folder = cover_type_dictionary["Folders"]

				# If the cover type is "Landscape"
				if cover_type == "Landscape":
					# Change it to the "Story" key
					cover_folder = cover_folder["Story"]

				# Define the story cover folder in the current language as the root cover type folder with the cover folder name
				cover_folder[small_language] = {
					"root": root_folder + self.chapter["Covers"]["Folder name"] + "/"
				}

				# Create the folder
				self.Folder.Create(cover_folder[small_language]["root"])

				# ----- #

				# Define the local story cover file in the current language as the cover folder
				story_cover_file = cover_folder[small_language]["root"]

				# Add the chapter number and the default cover file extension
				story_cover_file += self.chapter["Numbers"]["Leading zeroes"] + "." + self.stories["Cover types"]["Extension"]

				# Define the local cover files as the files dictionary
				cover_files = cover_type_dictionary["Files"]

				# If the cover type is "Landscape"
				if cover_type == "Landscape":
					# Change it to the "Story" key
					cover_files = cover_files["Story"]

				# Add it to the cover file dictionary
				cover_files[small_language] = story_cover_file

				# ----- #

				# If the cover type is "Landscape"
				if cover_type == "Landscape":
					# Define the website cover folder in the current language as the root website chapter cover folder with the chapter number
					cover_type_dictionary["Folders"]["Website"] = {
						"root": self.story["Folders"]["Covers"]["Websites"]["Chapters"]["root"] + self.chapter["Numbers"]["Leading zeroes"] + "/"
					}

					# Define a shortcut to the cover folder
					cover_folder = cover_type_dictionary["Folders"]["Website"]

					# Create the folder
					self.Folder.Create(cover_folder["root"])

					# Define the local website cover file in the current language as the cover folder
					website_cover_file = cover_folder["root"]

					# Add the full language and the default cover file extension
					website_cover_file += full_language + "." + self.stories["Cover types"]["Extension"]

					# Define the local cover files as the website cover files dictionary
					cover_files = cover_type_dictionary["Files"]["Website"]

					# Add it to the "Website" cover file dictionary
					cover_files[small_language] = website_cover_file

			# Add the cover type dictionary to the root dictionary
			self.chapter["Covers"][cover_type] = cover_type_dictionary

		# ---------- #

		# Show information about the chapter
		self.Show_Information(mode = "Start")

	def Create_Chapter_Covers(self):
		# Define a local chapter cover number
		chapter_cover_number = 1

		# Define a local total chapter covers number
		# (The number of cover types plus the number of languages)
		total_chapter_covers = len(self.stories["Cover types"]["List"]) + len(self.languages["Small"])

		# Iterate through the cover types dictionaries
		for cover_type in self.stories["Cover types"]["Dictionary"].values():
			# Get the cover type dictionary inside the chapter dictionary
			cover_type_dictionary = self.chapter["Covers"][cover_type["Title"]]

			# Define a local list of chapter titles
			chapter_titles = [
				# Add only the English chapter title with number
				self.chapter["Titles"]["With number"]["en"]
			]

			# If the "Update all chapter covers" state is True
			if self.states["Update all chapter covers"] == True:
				# Define the list of chapter titles as all chapter titles of the story in English
				chapter_titles = self.story["Chapters"]["Titles"]["en"]

			# Iterate through the language keys and dictionaries
			for small_language, language in self.languages["Dictionary"].items():
				# Define a shortcut to the full language
				full_language = language["Full"]

				# Get the current language translated to the user language
				translated_language = language["Translated"][self.language["Small"]]

				# Define the default text key for the text template to explain the process of updating the chapter covers to the user
				text_key = "opening_the_photoshop_file_of_chapter_covers, type: long"

				# If the "Update all chapter covers" state is True
				if self.states["Update all chapter covers"] == True:
					# Update the text key for the text template to use the plural version of the explanation text
					text_key += ", plural"

				# Get the text template of the explanation text with the correct text key
				text_template = self.language_texts[text_key]

				# Convert the cover extension to uppercase
				extension = self.stories["Cover types"]["Extension"].upper()

				# Define the list of items to use to format the text template
				items = [
					# The title of the cover type in the user language
					cover_type["Titles"][self.language["Small"]],

					# The current language translated to the user language
					translated_language,

					# The title of the cover type in the user language
					cover_type["Titles"][self.language["Small"]],

					# The extension of the cover file in uppercase
					extension
				]

				# If the "Update all chapter covers" state is True
				if self.states["Update all chapter covers"] == True:
					# Update the list of items to use to format the text template
					items = [
						# The title of the cover type in the user language
						cover_type["Titles"][self.language["Small"]],

						# The current language translated to the user language
						translated_language,

						# The total number of story chapters
						self.story["Information"]["Chapters"]["Numbers"]["Total"],

						# The title of the cover type in the user language
						cover_type["Titles"][self.language["Small"]],

						# The extension of the cover file in uppercase
						extension
					]

				# Format the text template with the list of items, making the explanation text
				text = text_template.format(*items)

				# Show a five dash space separator
				print()
				print(self.separators["5"])
				print()

				# Show the current and total chapter covers numbers
				print(self.language_texts["chapter_cover"] + ":")
				print("[" + str(chapter_cover_number) + "/" + str(total_chapter_covers) + "]")
				print()

				# Show the explanation text
				print(text)

				# Get the Photoshop cover file of the story in the current cover type and language
				photoshop_file = self.story["Folders"]["Covers"][cover_type["Title"]][small_language]["Photoshop"]

				# Open the Photoshop file
				self.System.Open(photoshop_file)

				# Iterate through the local list of chapter title
				chapter_number = 1
				for chapter_title in chapter_titles:
					# If the "Update all chapter covers" state is False
					if self.states["Update all chapter covers"] == False:
						# Show a space separator
						print()

						# Copy the chapter title
						self.Copy_Chapter_Title(language)

						# Ask for the user input when they finish rendering the chapter cover
						self.Input.Type(self.language_texts["press_enter_when_you_finish_rendering_the_chapter_cover"])

						# Show a space separator
						print()

					# If the "Update all chapter covers" state is True
					if self.states["Update all chapter covers"] == True:
						# Define the "Chapter" dictionary of the current chapter
						self.Define_Chapter(chapter_number)

						# Update the cover type dictionary
						cover_type_dictionary = self.chapter["Covers"][cover_type["Title"]]

						# If the chapter title is the first one
						if chapter_title == chapter_titles[0]:
							# Ask for the user to press Enter before continuing to the next chapter
							self.Input.Type(self.Language.language_texts["continue, title()"])

						# If the chapter title is not the first one
						if chapter_title != chapter_titles[0]:
							# Show a space separator
							print()

					# Move the cover file to the cover folders
					self.Move_Chapter_Cover(language, cover_type, cover_type_dictionary)

					# Add one to the local chapter number
					chapter_number += 1

				# Add one to the "chapter cover number"
				chapter_cover_number += 1

	def Copy_Chapter_Title(self, language):
		# Define the type text
		type_text = self.language_texts["press_enter_to_copy_the_chapter_title"]

		# Get the local language translated to the user language
		translated_language = language["Translated"][self.language["Small"]]

		# Define the text to show as the "Chapter title in" text
		text = self.language_texts["chapter_title_in"]

		# Add the local language translated to the user language
		text += " " + translated_language

		# Show the text
		print(text + ":")

		# Define a shortcut to the chapter title with number in the current language
		chapter_title = self.chapter["Titles"]["With number"][language["Small"]]

		# Show the chapter title
		print(chapter_title)

		# Ask for the user input to copy the chapter title
		self.Input.Type(type_text)

		# Copy the chapter title
		self.Text.Copy(chapter_title, verbose = False)

	def Move_Chapter_Cover(self, language, cover_type, cover_type_dictionary):
		# Get the cover folder for the current cover type and language
		cover_folder = self.story["Folders"]["Covers"][cover_type["Title"]][language["Small"]]["root"]

		# Define the cover file name
		file_name = "PSD copy"

		# If the "Update all chapter covers" state is True
		if self.states["Update all chapter covers"] == True:
			# Update the file name to be the chapter number with leading zeroes
			file_name = self.chapter["Numbers"]["Leading zeroes"]

			# Update the cover folder to be the Photoshop "Render" folder
			cover_folder = self.folders["Art"]["Photoshop"]["Render"]["root"]

		# Add the default cover type extension to the cover file name
		file_name += "." + self.stories["Cover types"]["Extension"]

		# Define the source file with the cover folder in the current language and the file name above
		# 
		# Examples:
		# [Cover type folder]/PSD copy.png
		# [Cover type folder]/01.png ("Update all chapter covers" = True)
		source_file = cover_folder + file_name

		# Show the source file
		print(self.File.language_texts["source_file"] + ":")
		print(source_file)

		# ---------- #

		# Define destination file as the cover type "Files" dictionary
		destination_file = cover_type_dictionary["Files"]

		# If the cover type is "Landscape"
		if cover_type["Title"] == "Landscape":
			# Change it to the "Story" key
			destination_file = destination_file["Story"]

		# Add the language key
		destination_file = destination_file[language["Small"]]

		# Show the copying information text with the name of the folder and the destination file
		print()
		print(self.language_texts["copying_the_cover_to_the_{}_folder"].format(self.language_texts["mega_stories"]) + ":")
		print(destination_file)

		# Copy the source file to the destination location
		self.File.Copy(source_file, destination_file)

		# ---------- #

		# If the cover type is "Landscape"
		if cover_type["Title"] == "Landscape":
			# Define the destination folder as the folder inside the cover type "Folders" dictionary
			destination_folder = cover_type_dictionary["Folders"]["Website"]["root"]

			# Define the destination file with the full language as the file name and the default cover type extension
			# 
			# Complete example:
			# "/Chapters/01/English.png"
			destination_file = destination_folder + language["Full"] + "." + self.stories["Cover types"]["Extension"]

			# Show the copying information text with the name of the folder and the destination file
			print()
			print(self.language_texts["copying_the_cover_to_the_{}_folder"].format(self.language_texts["website_story_covers"]) + ":")
			print(destination_file)

			# Copy the source file to the destination location
			self.File.Copy(source_file, destination_file)

		# Delete the render file (the original source file)
		self.File.Delete(source_file)

	def Update_Story_Website(self):
		# Define the dictionary to update the story website
		dictionary = {
			"Website": self.story["Title"],
			"Verbose": True
		}

		# Update the website of the selected story using the "Update_Websites" which was imported from the "PHP" class
		self.Update_Websites(dictionary)

	def Post_Chapter_On_Story_Websites(self):
		# Define a local story website number
		story_website_number = 1

		# Define a local total story websites number
		total_story_websites_number = len(self.stories["Story websites"]["List"])

		# Iterate through the dictionary of story websites
		for key, story_website in self.stories["Story websites"]["Dictionary"].items():
			# Show a five dash space separator
			print()
			print(self.separators["5"])
			print()

			# Show the current and total social networks numbers
			print(self.language_texts["story_website"] + ":")
			print("[" + str(story_website_number) + "/" + str(total_story_websites_number) + "]")

			# Iterate through the language keys and dictionaries
			for small_language, language in self.languages["Dictionary"].items():
				# Define a shortcut to the "Links" dictionary of the story website for the selected story
				story_links = self.story["Information"]["Links"][key]

				# Define the default link key as the "Edit story" one
				link_key = "Edit story"

				# If the "Add chapter" key is inside the story website "Links" dictionary for the selected story
				if "Add chapter" in story_links:
					# Update the link key to be
					link_key = "Add chapter"

				# Define the story link to be the one with the link key and the current language
				story_link = story_links[link_key][small_language]

				# Define the "Social Networks" dictionary to use in the "Open_Social_Network" sub-class imported from the "Social_Networks" module
				# With the list of social networks to open and their custom links
				social_networks = {
					"List": [
						key
					],
					"Custom links": {
						key: story_link
					},
					"States": {
						"First separator": False
					}
				}

				# Open the story website social network on the story page in the current language
				self.Open_Social_Network(social_networks)

				# Show a space separator
				print()

				# Copy the chapter title
				self.Copy_Chapter_Title(language)

				# Copy the chapter text
				self.Copy_Chapter_Text(small_language)

				# If the small language is the user language
				if small_language == self.language["Small"]:
					# Define the input text to ask for the chapter link on the story website
					input_text = self.language_texts["paste_the_link_of_the_chapter_on"] + " " + "[" + story_website["Name"] + "]"

					# Add the "in [language]" text
					input_text += " " + self.Language.language_texts["in_[language]"][small_language]

					# Import the validators module
					import validators

					# Define the chapter link variable as an empty string
					chapter_link = ""

					# Define a shortcut to the story website chapter "Links" dictionary
					chapter_links = self.chapter["Links"][key]

					# Define a chapter link format with the "{Chapter ID}" format string removed
					link_format = chapter_links[small_language].replace("{Chapter ID}", "")

					# Show the link format
					print()
					print(self.Language.language_texts["link_format"] + ":")
					print(link_format)

					# While the link format is not inside the chapter link
					# (This is to ensure the chapter link contains the story website and story links)
					while link_format not in chapter_link:
						# Ask for the user to type the link of the chapter posted on the story website
						chapter_link = self.Input.Type(input_text, accept_enter = False, next_line = True)

					# Split the chapter link to get the chapter ID
					chapter_id = chapter_link.split("/")[-1]

					# If there is a hypen in the chapter ID
					if "-" in chapter_id:
						# Split it again to get only the chapter ID
						chapter_id = chapter_id.split("-")[0]

					# Define a shortcut to the root chapter link
					chapter_link = chapter_links[small_language]

					# Replace the "{Chapter ID}" format string with the actual chapter ID in the local chapter link
					chapter_link = chapter_link.replace("{Chapter ID}", chapter_id)

					# Update the root chapter link
					chapter_links[small_language] = chapter_link

			# Add one to the "story website number"
			story_website_number += 1

		# Register the current date
		self.posting["Date"] = self.Date.Now()

	def Copy_Chapter_Text(self, small_language):
		# Get the language chapter file
		chapter_file = self.chapter["Files"][small_language]

		# Get the chapter text from the file above
		chapter_text = self.File.Contents(chapter_file)["string"]

		# Define the type text
		type_text = self.language_texts["press_enter_to_copy_the_chapter_text"]

		# Ask for user input before copying the chapter text
		self.Input.Type(type_text)

		# Copy the chapter text
		self.Text.Copy(chapter_text, verbose = False)

	def Post_On_The_Social_Networks(self):
		# Create the social network post texts
		self.Create_Social_Netowrk_Post_Texts()

		# ---------- #

		# Post the chapter on the social networks

		# Define the "Social Networks" dictionary with the list of social networks to open
		social_networks = {
			"List": [
				"Discord",
				"WhatsApp",
				"Facebook",
				"Twitter",
				"Bluesky",
				"Threads"
			],
			"Without hashtags": [
				"WhatsApp"
			],
			"Dictionary": {}
		}

		# Iterate through the list of social networks to get their dictionaries from the root "social networks" dictionary
		for key in social_networks["List"]:
			social_networks["Dictionary"][key] = self.social_networks["Dictionary"][key]

		# Define a local social network number
		social_network_number = 1

		# Define a local total social networks number
		total_social_networks_number = len(social_networks["List"])

		# Iterate through the list of social networks
		for social_network in social_networks["List"]:
			# Show a five dash space separator
			print()
			print(self.separators["5"])
			print()

			# Show the current and total social networks numbers
			print(self.Language.language_texts["social_network"] + ":")
			print("[" + str(social_network_number) + "/" + str(total_social_networks_number) + "]")

			# Define the social networks dictionary to use in the "Open_Social_Network" sub-class imported from the "Social_Networks" module
			dictionary = {
				"List": [
					social_network
				],
				"Custom links": {},
				"States": {
					"First separator": False
				}
			}

			# If the social network is "Discord"
			if social_network == "Discord":
				# Define the custom link for Discord as the "#stories" channel on my Discord server
				dictionary["Custom links"][social_network] = "https://discord.com/channels/311004778777935872/1041558273708540065"

			# If the social network is not "Discord"
			if social_network != "Discord":
				# Remove the "Custom links" dictionary
				dictionary.pop("Custom links")

			# ----- #

			# Open the social network with its custom link
			self.Open_Social_Network(dictionary)

			# ----- #

			# If the social network is the first one
			if social_network == social_networks["List"][0]:
				# Open the story chapter covers folder in the landscape format
				self.System.Open(self.chapter["Covers"]["Landscape"]["Folders"]["Story"][self.language["Small"]]["root"])

			# ----- #

			# Define a shortcut to the root post text
			post_text = self.chapter["Posting"]["Texts"]["Website"]

			# If the social network is inside the list of social networks without hashtags
			if social_network in social_networks["Without hashtags"]:
				# Remove the hashtags from the post text
				post_text = self.Remove_Hashtags(post_text)

			# If the social network is "Discord"
			if social_network == "Discord":
				# Add the "@Updates" role to the post text
				post_text += "\n\n" + "<@&1172626527175848086>"

			# If the social network is "Facebook"
			if social_network == "Facebook":
				# Get the hashtags
				hashtags = post_text.splitlines()[-1]

				# Remove the hashtags of the card
				post_text = self.Remove_Hashtags(post_text)

				# Iterate through the list of story websites
				for story_website in self.stories["Story websites"]["List"]:
					# Get the post text of the additional story website
					additional_post_text = self.chapter["Posting"]["Texts"][story_website]

					# Remove the hashtags from the story website post text
					additional_post_text = self.Remove_Hashtags(additional_post_text)

					# Add the story website post text to the root post text
					post_text += "\n\n" + "-" + "\n\n" + \
					additional_post_text

				# Add the hashtags back
				post_text += "\n\n" + hashtags

			# Copy the post text
			self.Text.Copy(post_text)

			# Define the input text as "Press Enter when you finish posting the chapter post text on"
			input_text = self.language_texts["press_enter_when_you_finish_posting_the_chapter_post_text_on"]

			# Ask for the user input after they finish posting the chapter post text on the social network
			self.Input.Type(input_text + " " + "[" + social_network + "]")

			# ----- #

			# If the social network is not "Facebook"
			if social_network != "Facebook":
				# Iterate through the list of story websites
				for story_website in self.stories["Story websites"]["List"]:
					# Get the post text of the additional story website
					additional_post_text = self.chapter["Posting"]["Texts"][story_website]

					# Remove the hashtags from the post text
					additional_post_text = self.Remove_Hashtags(additional_post_text)

					# Copy the post text for the current story website
					self.Text.Copy(additional_post_text)

					# Define the text template as "Press Enter when you finish posting the chapter post text from {} on"
					text_template = self.language_texts["press_enter_when_you_finish_posting_the_chapter_post_text_from_{}_on"]

					# Format it with the story website name
					input_text = text_template.format("[" + story_website + "]")

					# Add the social network
					input_text += " " + "[" + social_network + "]"

					# Ask for the user input after they finish posting the chapter post text of the story website on the social network
					self.Input.Type(input_text)

			# Add one to the "social network number"
			social_network_number += 1

		# ---------- #

		# Post the chapter on the story websites

		# Define a local story website number
		story_website_number = 1

		# Define a local total story websites number
		total_story_websites_number = len(self.stories["Story websites"]["List"])

		# Iterate through the dictionary of story websites
		for story_website_name, story_website in self.stories["Story websites"]["Dictionary"].items():
			# Show a five dash space separator
			print()
			print(self.separators["5"])
			print()

			# Show the current and total social networks numbers
			print(self.language_texts["story_website"] + ":")
			print("[" + str(story_website_number) + "/" + str(total_story_websites_number) + "]")

			# Define the social networks dictionary to use in the "Open_Social_Network" sub-class imported from the "Social_Networks" module
			dictionary = {
				"List": [
					story_website_name
				],
				"Custom links": {
					story_website_name: story_website["Links"]["Posts"] # The "Posts" link of the story website
				},
				"States": {
					"First separator": False
				}
			}

			# If the story website is the first one
			if story_website_name == self.stories["Story websites"]["List"][0]:
				# Remove the first separator
				dictionary["States"]["First separator"] = False

			# Open the social network with its custom link
			self.Open_Social_Network(dictionary)

			# ----- #

			# Copy the post text
			self.Text.Copy(post_text)

			# Define the input text as "Press Enter when you finish posting the chapter post text on"
			input_text = self.language_texts["press_enter_when_you_finish_posting_the_chapter_post_text_on"]

			# Ask for the user input after they finish posting the chapter post text on the story website
			self.Input.Type(input_text + " " + "[" + story_website_name + "]")

			# Add one to the "story website number"
			story_website_number += 1

	def Create_Social_Netowrk_Post_Texts(self):
		# Get the timezone formats
		timezone_formats = self.posting["Date"]["Timezone"]["DateTime"]["Formats"]

		# Define the timezone time as the user timezone time format
		timezone_time = timezone_formats["HH:MM DD/MM/YYYY"]

		# Define the text template as the time and the template
		text_template = timezone_time + ":" + "\n" + \
		self.language_texts["i_{}_the_chapter_{}_of_my_story_{}"]

		# Define the list of items to use to format the template
		items = [
			# Define the posting mode text as the "Done" text in the user language
			self.posting["Posting mode"]["Texts"]["Done"][self.language["Small"]],

			# The chapter number name in the user language
			# Examples: [one/two/three/thirty three]
			self.chapter["Numbers"]["Names"][self.language["Small"]],

			# The story title in the user language
			# Example: Story title
			self.story["Titles"][self.language["Small"]]
		]

		# Format the text template with the list of items to create the post text
		post_text = text_template.format(*items)

		# Add a colon and a line break
		post_text += ":" + "\n"

		# Add the chapter title in the user language without the number
		post_text += self.chapter["Titles"]["Normal"][self.language["Small"]]

		# Add two line breaks
		post_text += "\n\n"

		# Define the text template as "I {} for {}"
		text_template = self.language_texts["i_{}_for_{}"]

		# Define the list of items to use to format the template
		items = [
			# Define the posting mode text as the "Done" text in the user language
			self.posting["Posting mode"]["Texts"]["Done"][self.language["Small"]].capitalize(),

			# The [writing/revising] duration
			self.chapter["Writing"]["Duration"]
		]

		# Format the text template with the list of items to create the duration text
		duration_text = text_template.format(*items)

		# Add the duration text to the post text
		post_text += duration_text

		# Add two line breaks
		post_text += "\n\n"

		# Add the "Read it here:" text with a line break
		post_text += self.language_texts["read_it_here"] + ":" + "\n"

		# Define a shortcut to the chapter link in the story website
		chapter_link = self.chapter["Links"]["Website"][self.language["Small"]]

		# Replace spaces with "%20" in the chapter link
		chapter_link = chapter_link.replace(" ", "%20")

		# Add the chapter link in the root story website to the post text
		post_text += chapter_link

		# Add two line breaks
		post_text += "\n\n"

		# Define the main hashtags inside the new "Posting" dictionary
		self.chapter["Posting"] = {
			"Hashtags": "#Stake2 #Brasil #Historias #",
			"Texts": {}
		}

		# Add the story title in the user language without spaces as a hashtag
		self.chapter["Posting"]["Hashtags"] += self.story["Titles"][self.language["Small"]].replace(" ", "")

		# Add the hashtags
		post_text += self.chapter["Posting"]["Hashtags"]

		# Add the post text to the "Posting" dictionary inside the chapter dictionary
		self.chapter["Posting"]["Texts"]["Website"] = post_text

		# ---------- #

		# Iterate through the dictionary of story websites
		for key, story_website in self.stories["Story websites"]["Dictionary"].items():
			# Get the chapter links dictionary
			chapter_links = self.chapter["Links"][key]

			# Define the post text as "On [story website]:" with a line break
			post_text = self.Language.language_texts["on, style: in"].capitalize() + " " + key + ":" + "\n"

			# Add the chapter link in the additional story website
			post_text += chapter_links[self.language["Small"]]

			# Add two line breaks
			post_text += "\n\n"

			# Add the hashtags
			post_text += self.chapter["Posting"]["Hashtags"]

			# Add the post text to the "Posting" dictionary inside the chapter dictionary
			self.chapter["Posting"]["Texts"][key] = post_text

	def Remove_Hashtags(self, post_text):
		# Remove the hashtags from the post text
		post_text = post_text.replace(self.chapter["Posting"]["Hashtags"], "")

		# Transform the post text into a list of lines
		post_text = post_text.splitlines()

		# Remove the last line because it is empty
		post_text.pop(-1)

		# Transform the list into a text with line breaks
		post_text = self.Text.From_List(post_text, next_line = True)

		# Return the post text
		return post_text

	def Update_Chapter_Dictionary(self):
		# Get the timezone formats
		timezone_formats = self.posting["Date"]["Timezone"]["DateTime"]["Formats"]

		# Define the timezone time as the user timezone time format
		timezone_time = timezone_formats["HH:MM DD/MM/YYYY"]

		# Get the UTC formats
		utc_formats = self.posting["Date"]["UTC"]["DateTime"]["Formats"]

		# Define a shortcut to the UTC time format
		utc_time = utc_formats["YYYY-MM-DDTHH:MM:SSZ"]

		# If the "Writing" dictionary is not present in the "Posting" dictionary, add it
		if "Writing" not in self.chapter["Dictionary"]["Posting"]:
			self.chapter["Dictionary"]["Posting"]["Writing"] = {
				"Times": {}
			}

		# If the "Revisions" dictionary is not present in the "Posting" dictionary, add it
		if "Revisions" not in self.chapter["Dictionary"]["Posting"]:
			self.chapter["Dictionary"]["Posting"]["Revisions"] = {
				"List": [],
				"Dictionary": {}
			}

		# If the posting mode is "Written"
		if self.posting_mode == "Written":
			# Define the "Last posted chapter" as the current chapter
			self.story["Chapters"]["Numbers"]["Last posted chapter"] = self.chapter["Number"]

			# If the "Times" dictionary is inside the "Posting" dictionary and it is not empty
			if "Times" in self.chapter["Dictionary"]["Posting"]:
				# Add the "Times" dictionary to the "Writing" dictionary
				self.chapter["Dictionary"]["Posting"]["Writing"]["Times"] = self.chapter["Dictionary"]["Posting"]["Times"]

				# Remove the "Times" key from the "Posting" dictionary
				self.chapter["Dictionary"]["Posting"].pop("Times")

			# Define a shortcut to the "Times" dictionary
			times = self.chapter["Dictionary"]["Posting"]["Writing"]["Times"]

			# Update the "Finished" and "Finished (UTC)" posting times
			times["Finished"] = timezone_time
			times["Finished (UTC)"] = utc_time

		# If the posting mode is "Revised"
		if self.posting_mode == "Revised":
			# Add the timezone time to the revisions "List"
			self.chapter["Dictionary"]["Posting"]["Revisions"]["List"].append(timezone_time)

			# Create the times dictionary
			times = {
				"Finished": timezone_time,
				"Finished (UTC)": utc_time
			}

			# Add it to the new revision dictionary
			self.chapter["Dictionary"]["Posting"]["Revisions"][timezone_time] = {
				"Times": times
			}

		# Update the "Chapters.json" file with the updated "Chapters" dictionary
		self.JSON.Edit(self.story["Folders"]["Information"]["Chapters"], self.story["Chapters"])

	def Register_Task(self):
		# Create the task dictionary to use in the "Tasks" class
		self.task_dictionary = {
			"Task": {
				"Titles": {},
				"Descriptions": {},
				"Custom task item": self.Language.language_texts["posted"]
			}
		}

		# Iterate through the language keys and dictionaries
		for small_language, language in self.languages["Dictionary"].items():
			# Define the text template as the "I posted the chapter {} recently {}..." text in the current language
			text_template = self.texts["i_posted_the_chapter_{}_recently_{}_of_my_story_{}_on_the_storys_website"][small_language]

			# Define the list of items to use to format the text template
			items = [
				# The chapter number name in the user language
				# Examples: [one/two/three/thirty three]
				self.chapter["Numbers"]["Names"][small_language],

				# Define the posting mode text as the "Chapter" text in the current language
				# Example: [written/revised]
				self.posting["Posting mode"]["Texts"]["Chapter"][small_language].lower(),

				# The story title in the user language
				# Example: Story title
				self.story["Titles"][small_language]
			]

			# Format the text template with the list of items to create the task title
			# Example: I posted the chapter one of my story "Story Title" on the story's website
			task_title = text_template.format(*items)

			# ----- #

			# Define the text template as the "and on the {} story websites" text in the current language
			text_template = self.texts["and_on_the_{}_story_websites"][small_language]

			# Define a shortcut to the list of story websites
			story_websites = self.stories["Story websites"]["List"]

			# Define the story websites text as the list of story websites converted into a text
			story_websites_text = self.Text.From_List(story_websites, language = small_language)

			# Format the text template with the story websites string
			text = text_template.format(story_websites_text)

			# Add it to the task title
			# Example: I posted the chapter one of my story "Story Title" on the story's website and on the Wattpad and Spirit Fanfics story websites
			task_title += " " + text

			# Add the task title to the "Task" dictionary
			self.task_dictionary["Task"]["Titles"][small_language] = task_title

			# ----- #

			# Create the task description, initially as the task title in the current language with a dot
			task_description = self.task_dictionary["Task"]["Titles"][small_language] + "."

			# Add two line breaks
			task_description += "\n\n"

			# Add the "The chapter with the titles" text
			task_description += self.texts["the_chapter_with_the_titles"][small_language] + ":" + "\n"

			# List the chapter titles
			chapter_titles = list(self.chapter["Titles"]["Normal"].values())

			# Iterate through the list of chapter titles
			for chapter_title in chapter_titles:
				# Add the chapter title to the description text
				task_description += chapter_title

				# If the chapter title is not the last one, add a line break
				if chapter_title != chapter_titles[-1]:
					task_description += "\n"

			# Example:
			# The chapter with the titles:
			# Chapter Title
			# Chapter Title (in another language)

			# Add two line breaks
			task_description += "\n\n"

			# ----- #

			# If the "Previous titles" dictionary is inside the chapter dictionary
			if "Previous titles" in self.chapter["Dictionary"]:
				# Add the "Previous chapter titles" text
				task_description += self.texts["previous_chapter_titles"][small_language] + ":" + "\n"

				# List the previous chapter titles
				previous_chapter_titles = list(self.chapter["Dictionary"].values())

				# Iterate through the list of previous chapter titles
				for previous_chapter_title in previous_chapter_titles:
					# Add the previous chapter title to the description text
					task_description += previous_chapter_title

					# If the previous chapter title is not the last one, add a line break
					if previous_chapter_title != previous_chapter_titles[-1]:
						task_description += "\n"

				# Example:
				# Previous chapter titles:
				# Previous chapter Title
				# Previous chapter Title (in another language)

				# Add two line breaks
				task_description += "\n\n"

			# ----- #

			# Define the text template as the "I started {} it on {} at {} and finished on {} at" text in the current language
			text_template = self.texts["i_started_{}_it_on_{}_at_{}_and_finished_on_{}_at_{}"][small_language]

			# Define the list of items to use to format the text template
			items = [
				# Define the posting mode text as the "Infinitive action" text in the current language
				# Example: [writing/revising]
				self.posting["Posting mode"]["Texts"]["Infinitive action"][small_language]
			]

			# Get the chapter dictionary key of the posting mode
			chapter_dictionary_key = self.posting["Posting mode"]["Texts"]["Chapter dictionary"]

			# Get the chapter writing dictionary
			writing_dictionary = self.chapter["Dictionary"][chapter_dictionary_key]	

			# Iterate through the defined list of time keys
			for key in ["Started", "Finished"]:
				# If the posting mode is "Written"
				if self.posting_mode == "Written":
					# Define the writing as the writing dictionary
					writing = writing_dictionary

				# If the posting mode is "Revised"
				if self.posting_mode == "Revised":
					# Get the list of writings
					writings = list(writing_dictionary["Dictionary"].values())

					# Get the last writing and define it as the writing variable
					writing = writings[-1]					

				# Get the date
				date = writing["Times"][key]

				# Define the date dictionary using the defined date
				date = self.Date.From_String(date, "%H:%M %d/%m/%Y")

				# Define the correct date format text based on the current language
				date_format_text = self.Date.texts["date_format, type: format"][small_language]

				# Replace the date strings in the date format text with the units and texts inside the date dictionary
				date_text = self.Date.Replace_Strings_In_Text(date_format_text, date, small_language)

				# Add the date text to the list of items
				items.append(date_text)

				# Get the time (hours and minutes) of the date
				time = date["Timezone"]["DateTime"]["Formats"]["HH:MM"]

				# Add the time to the list of items
				items.append(time)

			# Format the text template with the list of items
			# Example: "I started [writing/revising] it on [January 1, 2025] at [12:00] and finished on [January 2, 2025] at [14:00]"
			# Values with [] are replaced using the values inside the list of items
			text = text_template.format(*items)

			# Add the text to the task description with a period
			task_description += text + "."

			# ----- #

			# Add a line break to the task description
			task_description += "\n"

			# Define the text template as the "I {} for {} in total" text in the current language
			text_template = self.texts["i_{}_for_{}_in_total"][small_language]

			# Define the list of items to use to format the text template
			items = [
				# Define the posting mode text as the "Done" text in the current language
				# Example: [wrote/revised]
				self.posting["Posting mode"]["Texts"]["Done"][small_language]
			]

			# Define the total duration text in the current language as the total writing duration text with time units
			# Example: "2 hours, 32 minutes, 33 seconds (02:32:33)"
			total_duration_text = self.chapter["Writing"]["Duration (with time units)"][small_language]

			# Add it to the list of items
			items.append(total_duration_text)

			# Format the text template with the list of items
			# Example: "I [wrote/revised] for [2 hours, 32 minutes, 33 seconds (02:32:33)] in total"
			# Values with [] are replaced using the values inside the list of items
			text = text_template.format(*items)

			# Add the text to the task description with a period
			task_description += text + "."

			# Add the task description to the "Task" dictionary
			self.task_dictionary["Task"]["Descriptions"][small_language] = task_description

		# Register the task with the root "Register_Task" method
		Stories.Register_Task(self, self.task_dictionary)

	def Write_On_Diary_Slim(self):
		# Define the text template as the "I updated the story website of my story" text in the user language
		text_template = self.texts["i_updated_the_website_of_my_story, type: long"][self.language["Small"]]

		# ----- #

		# Define a local list of languages
		languages = []

		# Iterate through the language dictionaries
		for language in self.languages["Dictionary"].values():
			# Get the current language translated to the user language
			translated_language = language["Translated"][self.language["Small"]]

			# Add it to the local list of languages
			languages.append(translated_language)

		# Convert it into a text
		languages = self.Text.From_List(languages)

		# ----- #

		# Define the "add or update text" as "add" by default
		add_or_update_text = "add"

		# If the posting mode is "Revised"
		if self.posting_mode == "Revised":
			# Update the text to be "update"
			add_or_update_text = "update"

		# Get the language text
		add_or_update_text = self.Language.language_texts[add_or_update_text]

		# ----- #

		# Define the posting mode text as the "Chapter" text in the user language
		posting_mode_text = self.posting["Posting mode"]["Language texts"]["Chapter"]

		# If the posting mode is "Revised"
		if self.posting_mode == "Revised":
			# Add the "and" text and a space
			posting_mode_text += self.Language.language_texts["and"] + " "

			# Define a shortcut to the "Translate" writing mode dictionary
			translate = self.stories["Writing modes"]["Dictionary"]["Translate"]

			# Add the translated "Chapter" writing mode text to the posting mode text
			posting_mode_text += translate["Language texts"]["Chapter"]

		# ----- #

		# Define a shortcut to the list of story websites
		story_websites = self.stories["Story websites"]["List"]

		# Define the story websites text as the list of story websites converted into a text
		story_websites_text = self.Text.From_List(story_websites)

		# Get the number name for the number of story websites
		story_websites_number_name = self.Date.language_texts["number_names, type: list"][len(story_websites)]

		# Add one to the number name
		story_websites_number_name_plus_one = self.Date.language_texts["number_names, type: list"][len(story_websites) + 1]

		# Define the story websites text with line breaks as an empty string
		story_websites_text_with_line_breaks = ""

		# Iterate through the list of story websites
		for story_website in self.stories["Story websites"]["List"]:
			# Use the "Of the chapter on" text by default
			text = self.language_texts["of_the_chapter_on"]

			# If the story website is the last one
			if story_website == self.stories["Story websites"]["List"][-1]:
				# Use the "And the chapter on" text
				text = self.language_texts["and_the_chapter_on"]

			# Add the story website
			text += " " + story_website

			# If the story website is not the last one
			if story_website != self.stories["Story websites"]["List"][-1]:
				# Add a line break
				text += "\n"

			# Add it to the story website text with line breaks
			story_websites_text_with_line_breaks += text

		# ----- #

		# Define the local list of social networks
		social_networks = [
			"Twitter",
			"Bluesky",
			"Threads",
			"Facebook (" + self.Language.language_texts["post"] + ")",
			self.language_texts["and_on_my_server_on_{}"].format("Discord")
		]

		# Convert it into a text
		social_networks_text = self.Text.From_List(social_networks, next_line = True)

		# ----- #

		# Define the local list of status social networks
		status_social_networks = [
			"WhatsApp",
			"Instagram",
			self.Language.language_texts["and_on, style: in"].capitalize() + " Facebook"
		]

		# Convert it into a text
		status_social_networks_text = self.Text.From_List(status_social_networks, next_line = True)

		# ----- #

		# Define the list of items to use to format the text template
		items = [
			# The story title in the user language
			# Example: Story title
			self.story["Titles"][self.language["Small"]],

			# The list of languages translated to the user language
			# Example: Portuguese and English
			languages,

			# The "add" or "update" text, depending on the posting mode
			add_or_update_text,

			# The chapter number name in the user language
			# Examples: [one/two/three/thirty three]
			self.chapter["Numbers"]["Names"][self.language["Small"]],

			# The posting mode text
			# Examples: [written/revised and translated]
			posting_mode_text,

			# The list of story websites in text version
			# Example: Wattpad and Spirit Fanfics
			story_websites_text,

			# The number name of the number of story websites
			# Example: two
			story_websites_number_name,

			# The number name of the number of story websites plus one
			# Example: three
			story_websites_number_name_plus_one,

			# The list of story websites in text version with line breaks
			# Example:
			# Of the chapter on Wattpad
			# And the chapter on Spirit Fanfics
			story_websites_text_with_line_breaks,

			# The list of social networks in text version
			# Example:
			# Twitter
			# Bluesky
			# Threads
			# Facebook (post"
			# And on my server on Discord
			social_networks_text,

			# The list of status social networks in text version
			# Example:
			# WhatsApp
			# Instagram
			# And on Facebook
			status_social_networks_text
		]

		# Format the text template with the list of items to create the text to write
		text_to_write = text_template.format(*items)

		# Example:
		# Values with [] are replaced using the values inside the list of items
		"""I have updated the website for my story "[Story Title]" in [Portuguese and English] to [add/update] its chapter [one], which was recently [written/revised and translated].
		I also posted the chapter in both languages on the story's page on [Wattpad and Spirit Fanfics], which are [two] websites where you can post stories.

		There are [three] types of links to the chapter:
		Of the chapter on the story's website
		[Of the chapter on Wattpad]
		[And the chapter on Spirit Fanfics]

		I posted the chapter links, along with its cover, on the following social networks:
		[Twitter]
		[Bluesky]
		[Threads]
		[Facebook (post)]
		[And on my Discord server]

		In addition, I posted it on the status of these social networks:
		[WhatsApp]
		[Instagram]
		[And on Facebook]"""

		# Import the "Write_On_Diary_Slim_Module" sub-module from the "Diary_Slim" module
		from Diary_Slim.Write_On_Diary_Slim_Module import Write_On_Diary_Slim_Module as Write_On_Diary_Slim_Module

		# Define the "Diary Slim" dictionary
		self.posting["Diary Slim"] = {
			# The text to be written in the user language
			"Text": text_to_write,

			# The time to use to write the text
			"Time": self.Date.Now()["Timezone"]["DateTime"]["Formats"]["HH:MM DD/MM/YYYY"],

			# Show the "This text was written to the current Diary Slim" text
			"Show text": True,

			# Do not add the end dot
			"Add": {
				"Dot": False
			}
		}

		# Show a five dash space separator
		print()
		print(self.separators["5"])
		print()

		# Write the task text on Diary Slim
		Write_On_Diary_Slim_Module(self.posting["Diary Slim"])

		# ---------- #

		# Show information about the chapter with the "Finish" mode
		self.Show_Information(mode = "Finish")

	def Show_Information(self, mode = "Start"):
		# Show a five dash space separator
		print()
		print(self.separators["5"])
		print()

		# Show the "Story" text and the story title in the user language
		print(self.Language.language_texts["story, title()"] + ":")
		print("\t" + self.story["Titles"][self.language["Small"]])

		# Show the story titles in other languages
		for small_language, story_title in self.story["Titles"].items():
			# If the language is not the user language
			if small_language != self.language["Small"]:
				# Show the story title with a tab
				print("\t" + story_title)

		# If the "Update all chapter covers" state is False
		if self.states["Update all chapter covers"] == False:
			# Define the default text as "This chapter was selected to be posted"
			text = "this_chapter_was_selected_to_be_posted"

			# If the mode parameter is "Finish"
			if mode == "Finish":
				# Change the text to be "You finished posting this chapter"
				text = "you_finished_posting_this_chapter"

			# Show the defined text and the chapter title with number
			print()
			print(self.language_texts[text] + ":")
			print("\t" + self.chapter["Titles"]["With number"][self.language["Small"]])
			print()

			# Define the text template to be formatted
			text_template = self.language_texts["it_was_{}_on_{}_at_{}"]

			# Define the list of items to use to format the text template
			items = [
				# The chapter text of the posting mode
				self.posting["Posting mode"]["Language texts"]["Chapter"],

				# The chapter [writing/revising] date in the user date format
				self.chapter["Writing"]["Date"],

				# The chapter [writing/revising] time
				self.chapter["Writing"]["Time"]
			]

			# Format the text template with the list of items
			text = text_template.format(*items)

			# Show the text with a period
			print(text + ".")
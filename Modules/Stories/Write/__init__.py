# Write.py

# Import the root class
from Stories.Stories import Stories as Stories

# Import some useful modules
from copy import deepcopy

class Write(Stories):
	def __init__(self):
		super().__init__()

		# Define the root "writing" dictionary
		self.writing = {
			"Steps": {
				"List": [],
				"Dictionary": {}
			},
			"Writing modes": {
				"List": [],
				"Dictionary": {}
			},
			"Writing mode": {},
			"Chapter": {},
			"Session": {}
		}

		# Define a shortcut to the story "Chapters" and "Writing" dictionaries
		for key in ["Chapters", "Writing"]:
			self.story[key] = self.story["Information"][key]

		# Define the root states dictionary
		self.states = {
			"Select chapter": False,
			"A new chapter": False,
			"Ongoing writing session": False,
			"Pause writing session": False,
			"Already paused": False,
			"Postpone writing session": False,
			"Finished writing": False
		}

		# ---------- #

		# Define and run the chapter writing steps
		self.Define_And_Run_Steps()

		# Run the root class to update the files and dictionaries of the selected story
		super().__init__()

	def Define_And_Run_Steps(self):
		# Define the list of chapter writing steps
		self.writing["Steps"]["List"] = [
			"Select writing mode",
			"Define chapter",
			"Define server",
			"Open story website",
			"Open writing pack",
			"Create Discord status",
			"Start writing"
		]

		# Iterate through the list of chapter writing steps
		for key in self.writing["Steps"]["List"]:
			# Define the method name for the step by converting the key into title case and replacing spaces with underlines
			method_name = key.title().replace(" ", "_")

			# Define the writing step dictionary with the key, method name, and method
			self.writing["Steps"]["Dictionary"][key] = {
				"Key": key,
				"Method name": method_name,
				"Method": getattr(self, method_name)
			}

		# Iterate through the writing step dictionaries inside the "Steps" dictionary
		for step in self.writing["Steps"]["Dictionary"].values():
			# Run the method of the writing step
			step["Method"]()

	def Select_Writing_Mode(self):
		# Define the parameters dictionary to use inside the "Select" method of the "Input" utility module
		parameters = {
			"options": self.stories["Writing modes"]["List"], #  The list of writing modes
			"language_options": [], # The empty list of language writing modes
			"show_text": self.language_texts["writing_modes"], # The "Writing modes" text in the user language
			"select_text": self.language_texts["select_a_writing_mode"] # The "Select a writing mode" text in the user language
		}

		# ---------- #

		# Define a shortcut to the total number of chapters for easier typing
		total_chapters = self.story["Chapters"]["Numbers"]["Total"]

		# Iterate through the writing modes and writing mode dictionaries
		for writing_mode, writing_mode_dictionary in self.stories["Writing modes"]["Dictionary"].items():
			# Define a shortcut to the current writing mode dictionary
			writing_dictionary = self.story["Writing"][writing_mode]

			# Make a copy of the current writing mode dictionary
			writing_mode_dictionary = deepcopy(writing_mode_dictionary)

			# Define a shortcut to the "Status" dictionary
			status = writing_dictionary["Status"]

			# ----- #

			# Define the writing mode text initially as an empty string
			writing_mode_text = ""

			# Get the current chapter of the writing mode
			current_chapter = writing_dictionary["Current chapter"]

			# Make a copy of the current chapter
			chapter = current_chapter

			# If the current chapter is not the last chapter
			# And the "Finished" status is True
			if (
				current_chapter != total_chapters and
				status["Finished"] == True
			):
				# Add one to the local chapter number
				# (To write/revise/translate the next chapter)
				chapter += 1

				# Update the "Current chapter" key
				writing_dictionary["Current chapter"] = chapter

				# Reset the keys of the "Times" dictionary
				writing_dictionary["Times"] = {
					"Started": "",
					"Finished": "",
					"Finished (UTC)": "",
					"Durations": {
						"List": [],
						"Dictionary": {}
					}
				}

				# If the "Finished" status key is True, change it to False
				if status["Finished"] == True:
					status["Finished"] = False

			# If the current chapter is the last chapter
			# And  the "Finished" status is True
			if (
				current_chapter == total_chapters and
				status["Finished"] == True
			):
				# If the writing mode is "Revise"
				if writing_mode == "Revise":
					# Change the "Select chapter" state to True
					# (Ask the user to select a chapter to revise if they already revised all chapters)
					self.states["Select chapter"] = True

					# Define the writing mode as "Select a chapter to revise"
					writing_mode_text = self.language_texts["select_a_chapter_to_revise"]

			# ----- #

			# Reset the "Ongoing writing session" state to be False
			self.states["Ongoing writing session"] = False

			# Check if the writing "Started" time is not empty
			# (This means the user has already started writing the chapter)
			if writing_dictionary["Times"]["Started"] != "":
				# Change the "Ongoing writing session" state to True
				self.states["Ongoing writing session"] = True

			# ----- #

			# If the writing mode text is an empty string
			if writing_mode_text == "":
				# Define the writing mode text initially as "Start to"
				writing_mode_text = self.language_texts["start_to"]

				# If the "Ongoing writing session" state is True (the user resumed writing the chapter)
				if self.states["Ongoing writing session"] == True:
					# Change the writing mode text to be "Continue to"
					writing_mode_text = self.language_texts["continue_to"]

				# Add the infinitive verb tense to the writing mode text
				writing_mode_text += " " + writing_mode_dictionary["Language texts"]["Infinitive"]

				# ----- #

				# Define a shortcut to the "language texts" dictionary of the "Language" class
				language_texts = self.Language.language_texts

				# Define the "the chapter" text initially as the "the" masculine text
				the_chapter_text = language_texts["the, masculine"]

				# Add the " chapter" text
				the_chapter_text += " " + language_texts["chapter"]

				# Add the chapter number
				the_chapter_text += " " + str(chapter)

				# ----- #

				# Add the " the chapter" text to the writing mode text
				writing_mode_text += " " + the_chapter_text

			# Add the writing mode text to the list of language options
			parameters["language_options"].append(writing_mode_text)

			# ----- #

			# If the writing mode is "Write"
			if writing_mode == "Write":
				# Define the text addon as "a new chapter"
				writing_mode_dictionary["Text addon"] = self.language_texts["a_new_chapter"]

			# If the writing mode is either "Revise" or "Translate"
			# If the "Ongoing writing session" state is True (the user resumed writing the chapter)
			if (
				writing_mode in ["Revise", "Translate"] and
				self.states["Ongoing writing session"] == True
			):
				# Define the text addon as "in progress"
				writing_mode_dictionary["Text addon"] = self.language_texts["in_progress"]

			# ----- #

			# Add the writing mode dictionary to the "Writing modes" dictionary of the root "writing" dictionary
			self.writing["Writing modes"]["List"].append(writing_mode)
			self.writing["Writing modes"]["Dictionary"][writing_mode] = writing_mode_dictionary

		# Iterate through the list of writing modes
		i = 0
		for writing_mode in self.stories["Writing modes"]["Dictionary"]:
			# Define a shortcut to the current writing mode dictionary
			writing_dictionary = self.story["Writing"][writing_mode]

			# Get the current chapter of the writing mode
			current_chapter = writing_dictionary["Current chapter"]

			# Define a shortcut to the "Status" dictionary
			status = writing_dictionary["Status"]

			# If the writing mode is "Translate"
			if writing_mode == "Translate":
				# Define a shortcut to the "Revise" writing mode dictionary
				revise = self.story["Writing"]["Revise"]

				# If the current chapter is the last chapter
				# And the "Finished" status is True
				# (That means the last chapter was already translated)
				# Or the chapter number is not the last chapter
				# And the current chapter to revise is the same as the current chapter to translate
				# And it has not been revised ("Finished" is False)
				# (That means the user needs to revise the current chapter before translating it)
				if (
					(current_chapter == total_chapters and
					status["Finished"] == True) or
					(current_chapter != total_chapters and
					current_chapter == revise["Current chapter"] and
					revise["Status"]["Finished"] == False)
				):
					# Then remove the "Translate" writing mode from the list of options and language options
					# (All chapters have been translated
					# Or the current chapter to revise has not been revised and it is not the last chapter)
					parameters["options"].remove(writing_mode)
					parameters["language_options"].pop(i)

			# Add one to the "i" number
			i += 1

		# ---------- #

		# Ask the user to select a writing mode
		writing_mode = self.Input.Select(**parameters)["Option"]["Original"]

		# Define the "writing mode" root variable as the writing mode name for faster typing
		self.writing_mode = writing_mode

		# Get the writing mode dictionary
		self.writing["Writing mode"] = self.writing["Writing modes"]["Dictionary"][self.writing_mode]

		# Define a shortcut to the "Writing" dictionary of the writing mode
		self.writing["Writing"] = self.story["Writing"][self.writing_mode]

		# If the writing mode is "Write"
		if self.writing_mode == "Write":
			# Change the "A new chapter" state to True
			self.states["A new chapter"] = True

		# Reset the "Ongoing writing session" state to be False
		self.states["Ongoing writing session"] = False

		# Check if the writing "Started" time is not empty
		# (This means the user has already started writing the chapter)
		if self.writing["Writing"]["Times"]["Started"] != "":
			# Change the "Ongoing writing session" state to True
			self.states["Ongoing writing session"] = True

	def Select_Chapter(self):
		# Ask the user to select a chapter from the list
		chapter_number = self.Input.Select(self.story["Chapters"]["Titles"])["Option"]["Number"]

		# Return the chapter number
		return chapter_number

	def Define_Chapter(self):
		# Define the chapter number as the current chapter in the writing dictionary
		self.writing["Chapter"]["Number"] = self.writing["Writing"]["Current chapter"]

		# If the "Select chapter" state is True
		if self.states["Select chapter"] == True:
			# Ask the user to select a chapter to [write/revise/translate]
			self.writing["Chapter"]["Number"] = self.Select_Chapter()

		# ---------- #

		# Define the "Chapter" dictionary
		self.writing["Chapter"] = {
			"Number": self.writing["Chapter"]["Number"],
			"Numbers": {
				"Leading zeroes": 0,
				"Names": {}
			},
			"Titles": {
				"Normal": {},
				"With number": {}
			},
			"Previous titles": {
				"Normal": {},
				"With number": {}
			},
			"Files": {}
		}

		# Define the chapter number with leading zeroes
		self.writing["Chapter"]["Numbers"]["Leading zeroes"] = str(self.Text.Add_Leading_Zeroes(self.writing["Chapter"]["Number"]))

		# ---------- #

		# Define a shortcut to the chapter dictionary
		self.chapter = self.writing["Chapter"]

		# Define a shortcut to the chapter number
		chapter_number = self.chapter["Number"]

		# Define a shortcut to the chapter titles dictionary for easier typing
		chapter_titles = self.story["Chapters"]["Lists"]["Titles"]

		# Iterate through the language keys and dictionaries
		for small_language, language in self.languages["Dictionary"].items():
			# Define a shortcut to the full language
			full_language = language["Full"]

			# Define the chapter title as the chapter number with leading zeroes
			chapter_title = self.chapter["Numbers"]["Leading zeroes"]

			# If the writing mode is either "Revise" or "Translate"
			if self.writing_mode in ["Revise", "Translate"]:
				# Get the actual chapter title
				# (The chapter number less one because Python list indexes start at zero)
				chapter_title = chapter_titles[small_language][chapter_number - 1]

			# Define the chapter title with the number
			# Examples:
			# 01 (for the "Write" writing mode)
			# Chapter Title (for the "Revise" or "Translate" writing modes)
			chapter_title_with_number = chapter_title

			# If the writing mode is either "Revise" or "Translate"
			if self.writing_mode in ["Revise", "Translate"]:
				# Define the chapter title with the number
				# Example: 01 - Chapter Title
				chapter_title_with_number = self.chapter["Numbers"]["Leading zeroes"] + " - " + chapter_title

			# Add the chapter title to the titles "Normal" language dictionary
			self.chapter["Titles"]["Normal"][small_language] = chapter_title

			# Add the chapter title with the number to the titles "With number" language dictionary
			self.chapter["Titles"]["With number"][small_language] = chapter_title_with_number

			# Get the number name of the chapter number
			number_name = self.Date.texts["number_names, type: list"][small_language][chapter_number]

			# Add it to the number "Names" dictionary
			self.chapter["Numbers"]["Names"][small_language] = number_name

			# ----- #

			# Define the chapter file in the current language as the "Chapters" folder of the selected story
			self.chapter["Files"][small_language] = self.story["Folders"]["Chapters"][full_language]["root"]

			# Sanitize the chapter title with number
			sanitized_chapter_title = self.Sanitize(chapter_title_with_number, restricted_characters = True)

			# Add the sanitized chapter title with number
			self.chapter["Files"][small_language] += sanitized_chapter_title + ".txt"

			# If the writing mode is "Write"
			# And the current language is the user language
			# (The chapters are always written in the user language)
			if (
				self.writing_mode == "Write" and
				small_language == self.language["Small"]
			):
				# Create the chapter file
				self.File.Create(self.chapter["Files"][small_language])

			# If the writing mode is either "Write" or "Revise"
			# And the language is the same as the user language
			if (
				self.writing_mode in ["Write", "Revise"] and
				small_language == self.language["Small"]
			):
				# Define the "Writing language" as the user language dictionary
				# (The chapters are always written or revised in the user language)
				self.chapter["Writing language"] = self.language

		# If the writing mode is "Translate"
		if self.writing_mode == "Translate":
			# Define the "Origin language" dictionary as the user language dictionary
			self.chapter["Origin language"] = self.language

			# Define the "Destiny language" dictionary as the "English" language dictionary
			self.chapter["Destiny language"] = self.languages["Dictionary"]["English"]

			# (The chapters are always translated from the user language to English)

		# ---------- #

		# Check the chapter date texts of the chapter files
		self.Check_Chapter_Date_Texts()

		# ---------- #

		# Show a five dash space separator
		print()
		print(self.separators["5"])
		print()

		# Show the story title in the user language
		print(self.Language.language_texts["story, title()"] + ":")
		print("\t" + self.story["Titles"][self.language["Small"]])
		print()

		# Define the show text as the writing mode in the action verb tense
		show_text = self.writing["Writing mode"]["Language texts"]["Action"].title()

		# Add the " this chapter" text
		show_text += " " + self.language_texts["this_chapter"]

		# Show the text with the writing text in the action tense
		print(show_text + ":")

		# Define a shortcut to the chapter title with number in the user language
		chapter_title = self.chapter["Titles"]["With number"][self.language["Small"]]

		# If there is an text addon, add it
		if "Text addon" in self.writing["Writing mode"]:
			chapter_title += " (" + self.writing["Writing mode"]["Text addon"] + ")"

		# Show the chapter title
		print("\t" + chapter_title)

		# ---------- #

		# Iterate through the language keys and dictionaries
		for small_language, language in self.languages["Dictionary"].items():
			# If the writing mode is either "Write" or "Revise"
			# And the current language is the writing language
			# (The chapters are always written and revised in the user language)
			# Or the writing mode is "Translate"
			# (The chapter files are always opened in both languages for the "Translate" writing mode)
			if (
				(self.writing_mode in ["Write", "Revise"] and
				small_language == self.chapter["Writing language"]["Small"]) or
				(self.writing_mode == "Translate")
			):
				# Get the current language translated to the user language
				translated_language = language["Translated"][self.language["Small"]]

				# Show a three space separator
				print()
				print(self.separators["3"])
				print()

				# Define the text to show as the "Opening the chapter file in [translated language]" text
				text = self.language_texts["opening_the_chapter_file_in"] + " " + translated_language

				# Show the text
				print(text + "...")

				# Get the chapter file in the current language
				file = self.writing["Chapter"]["Files"][small_language]

				# Open the chapter file
				self.System.Open(file, verbose = False)

				# If the "Testing" switch is False
				if self.switches["Testing"] == False:
					# Wait for one second before opening the next chapter file
					self.Date.Sleep(1)

	def Check_Chapter_Date_Texts(self):
		# Iterate through the list of small languages
		for language in self.languages["Small"]:
			# Get the chapter file
			chapter_file = self.writing["Chapter"]["Files"][language]

			# Get the lines of the chapter file in the current language
			lines = self.File.Contents(chapter_file)["Lines"]

			# If the writing mode is "Translate"
			# And the current language is equal to the target translation language
			# And the user started writing this chapter just now
			if (
				self.writing_mode == "Translate" and
				language == self.target_language["Small"] and
				self.states["Ongoing writing session"] == False
			):
				# Get the chapter file for the original (user) chapter language
				language_chapter_file = self.writing["Chapter"]["Files"][self.language["Small"]]

				# Update the list of lines to be the chapter text of the original (user) chapter language
				lines = self.File.Contents(language_chapter_file)["Lines"]

				# Remove the first five lines that come from the original version of the chapter text
				# (The lines say when the chapter was written, revised, and translated for the last time)
				i = 1
				while i <= 5:
					lines.pop(0)

					i += 1

			# Get the language "Dates of the chapter:" text
			dates_of_the_chapter = self.texts["dates_of_the_chapter"][language] + ":"

			# Define the "insert" switch as False
			insert = False

			# If the list of lines is empty
			# Or the first line of the file is not "Dates of the chapter:"
			if (
				lines == [] or
				lines[0] != dates_of_the_chapter
			):
				# Add the "Dates of the chapter:" text to the file
				lines.insert(0, dates_of_the_chapter)

				# Change the "insert" switch to True
				insert = True

			# Iterate through the list of texts about chapter dates
			i = 1
			for key, item in self.texts["chapter_dates, type: dictionary"].items():
				# Define the list of items to use to format the chapter date text
				items = [
					"[date]",
					"[time]"
				]

				# Get the writing mode dictionary
				writing_mode = self.stories["Writing modes"]["Dictionary"][key]

				# Get the English past writing mode (chapter)
				past_writing_mode = writing_mode["Texts"]["Chapter"]["en"].capitalize()

				# If the key is "Translate", add the destination language as the first item
				if key == "Translate":
					# Get the English language dictionary
					english = self.languages["Dictionary"]["en"]

					# Get the English language translated to the local language
					translated_english = english["Translated"][language]

					# Add the translated English language in the current language to the list of items
					items.insert(0, translated_english)

				# Get the text in the current language and format it using the list of items above
				text = item[language].format(*items) + "."

				# Define a shortcut for the chapter number
				chapter_number = str(self.chapter["Number"])

				# If the chapter is not present inside the dictionary of chapters
				if chapter_number not in self.story["Information"]["Chapters"]["Dictionary"]:
					# Create the empty chapter dictionary inside the dictionary of chapters
					self.story["Information"]["Chapters"]["Dictionary"][chapter_number] = {
						"Number": chapter_number,
						"Titles": {},
						"Writing": {
							"Titles": {},
							"Times": {}
						},
						"Revisions": {
							"List": [],
							"Dictionary": {}
						},
						"Translations": {
							"List": [],
							"Dictionary": {}
						},
						"Posting": {
							"Times": {}
						}
					}

				# Define the chapter dictionary for easier typing
				chapter = self.story["Information"]["Chapters"]["Dictionary"][str(self.chapter["Number"])]

				# Get the "chapter dictionary" key for the current writing mode
				chapter_dictionary_key = writing_mode["Texts"]["Chapter dictionary"]

				# Get the writing dictionary for the current writing mode
				writing_dictionary = chapter[chapter_dictionary_key]

				# If the key is "Write"
				# And the "Finished" writing is not empty
				# Or the key is either "Revise" or "Translate"
				# And the list of writings is not empty
				if (
					(key == "Write" and
					writing_dictionary["Times"]["Finished"] != "") or
					(key in ["Revise", "Translate"] and
					writing_dictionary["List"] != [])
				):
					# If the key is "Write"
					if key == "Write":
						# Get the writing date
						writing_date = writing_dictionary["Times"]["Finished"]

					# If the key is not "Write"
					if key != "Write":
						# List the writings
						writings = list(writing_dictionary["Dictionary"].values())

						# Get the last writing
						last_writing = writings[-1]

						# Get the last writing date
						writing_date = last_writing["Times"]["Finished"]

					# Define the date dictionary
					date = self.Date.From_String(writing_date, "%H:%M %d/%m/%Y")

					# Define the date text of the date
					date_text = self.Date.texts["date_format, type: format"][language]

					# Replace the date strings in the date text with the units and texts inside the date dictionary
					date_text = self.Date.Replace_Strings_In_Text(date_text, date, language)

					# Get the time of the date
					time = date["Timezone"]["DateTime"]["Formats"]["HH:MM"]

					# If the "A new chapter" state is False
					if self.states["A new chapter"] == False:
						# Replace the date inside the root text
						text = text.replace("[date]", date_text)

						# Replace the time inside the root text
						text = text.replace("[time]", time)

				# If the insert switch is False
				if insert == False:
					# Replace the line with the text (with replaced date and time)
					lines[i] = text

				# If the insert switch is True
				if insert == True:
					# Insert the current chapter date text into the correct index
					lines.insert(i, text)

				# Add one to the "i" number
				i += 1

			# If the insert switch is True
			if insert == True:
				# Add a space after the lines
				lines.insert(i, "")

				# If the writing mode is "Write"
				# And the user started writing this chapter just now
				if (
					self.writing_mode == "Write" and
					self.states["Ongoing writing session"] == False
				):
					# Add a space after the lines to separate the chapter from the chapter dates
					lines.insert(i, "")

			# Transform the list of lines into a text string
			text = self.Text.From_List(lines, next_line = True)

			# Update the chapter file with the new text
			self.File.Edit(self.writing["Chapter"]["Files"][language], text, "w")

	def Open_Story_Website(self):
		# Open the server
		self.Manage_Server(open = True, separator_number = 3)

		if self.switches["Testing"] == False:
			# Wait for one second
			self.Date.Sleep(1)

		# Get the websites "URL" dictionary
		url = self.JSON.To_Python(self.folders["Mega"]["PHP"]["JSON"]["URL"])

		# Define the template variable for easier typing
		template = url["Code"]["Templates"]["With language"]

		# Define the list of items to use to format the template
		items = [
			self.story["Title"], # The title of the story and website
			self.chapter["Language"]["Destination"]["Full"] # The full chapter destination language
		]

		# Format the template with the items
		url = template.format(*items)

		# Define the list of custom parameters to add to the URL
		parameters = [
			"chapter=" + str(self.chapter["Number"]), # The number of the chapter
			"write=true", # The write switch, to activate the writing mode on the story website
			"show_chapter_covers=true" # Show the chapter covers on the chapter tabs
		]

		# Iterate through the list of parameters
		for parameter in parameters:
			# Add each parameter to the URL
			url += "&" + parameter

		# Show a three dash space separator
		print()
		print(self.separators["3"])

		# Define and show the text about opening the story website
		text = self.language_texts["opening_the_story_website_in"] + " " + self.writing["Chapter"]["Language"]["Destination"]["Translated"][self.language["Small"]]

		print()
		print(text + "...")

		# Open the story website link
		self.System.Open(url, verbose = False)

		# If the "Testing" switch is False
		if self.switches["Testing"] == False:
			# Wait for two seconds
			self.Date.Sleep(2)

	def Open_Writing_Pack(self):
		# If the writing mode is "Translate"
		if self.writing_mode == "Translate":
			# Show the text about opening the translator website
			text = self.Language.language_texts["opening_the"] + " " + self.stories["Writing"]["Translator website"]["Name"]

			print()
			print(self.separators["3"])
			print()
			print(text + "...")

			# Open the link of the translator website
			self.System.Open(self.stories["Writing"]["Translator website"]["Link"], verbose = False)

			if self.switches["Testing"] == False:
				# Wait for one second
				self.Date.Sleep(1)

		# Define the text about opening the music player for the user to listen to the soundtrack of the story
		# Formatting it with the name of the music player
		text = self.language_texts["opening_the_{}_music_player_for_you_to_listen_to_the_soundtrack_of_the_story"].format(self.stories["Writing"]["Music player"]["Name"])

		# Show it
		print()
		print(self.separators["3"])
		print()
		print(text + "...")

		# Open the music player program so the user can listen to the soundtrack of the story
		self.System.Open(self.stories["Writing"]["Music player"]["Link"], verbose = False)

		if self.switches["Testing"] == False:
			# Wait for one second
			self.Date.Sleep(1)

	def Create_Discord_Status(self):
		# Define the Discord status template
		template = self.language_texts["{}_the_chapter_{}_of_my_story_{}"]

		# Define the list of items
		items = [
			self.writing["Writing mode"]["Language texts"]["Action"].title(), # The action of the writing mode
			self.writing["Chapter"]["Numbers"]["Names"][self.language["Small"]], # The number name of the chapter in the user language
			'"' + self.story["Titles"][self.language["Small"]] + '"' # The story title in the user language, with quotes around it
		]

		# Format the template with the items, making the Discord status
		discord_status = template.format(*items)

		# Define the text to show
		text = self.Language.language_texts["copying_the_discord_status"]

		# Show a three space separator
		print()
		print(self.separators["3"])
		print()

		# Show the text to show
		print(text + "...")

		# Copy the Discord status to the clipboard
		self.Text.Copy(discord_status, verbose = False)

	def Make_Backup_Of_Time(self, mode = "Create", time = "Before"):
		# Define the backup file name as "Backup of the time of [writing mode item]"
		file_name = self.language_texts["backup_of_the_time_of"] + " " + self.writing["Writing mode"]["Language texts"]["Item"]

		# Define the backup file
		backup_file = self.stories["Folders"]["Database"]["root"] + file_name + ".txt"

		# If the mode is "Create"
		if mode == "Create":
			# If the file does not exist
			if self.File.Exists(backup_file) == False:
				# Create the backup file
				self.File.Create(backup_file)

			# If the time is "Before"
			if time == "Before":
				# Define the text to write as the before time
				text_to_write = file_name + ":" + "\n" + \
				"\n" + \
				self.Language.language_texts["before, title()"] + ":" + "\n" + \
				self.writing["Session"]["Before"]["Timezone"]["DateTime"]["Formats"]["HH:MM DD/MM/YYYY"]

			# If the time is "After"
			if time == "After":
				# Define the text to write as the after time
				text_to_write = "\n" + \
				"\n" + \
				self.Language.language_texts["after, title()"] + ":" + "\n" + \
				self.writing["Session"]["After"]["Timezone"]["DateTime"]["Formats"]["HH:MM DD/MM/YYYY"]

			# If the time is the duration one
			if time == "Duration":
				# Define the text to write as the duration time
				text_to_write = "\n" + \
				"\n" + \
				self.Language.language_texts["duration, title()"] + ":" + "\n" + \
				self.writing["Writing"]["Duration"]["Text"][self.language["Small"]]

			# Write the text to the file in the append mode
			self.File.Edit(backup_file, text_to_write, "a")

		# If the mode is "Delete"
		if mode == "Delete":
			# Delete the backup file
			self.File.Delete(backup_file)

	def Start_Writing(self):
		# Show a five dash space separator
		print()
		print(self.separators["5"])

		# If the "Ongoing writing session" state is True (the user resumed writing the chapter)
		if self.states["Ongoing writing session"] == True:
			# Show the total writing time text in the user language
			print()
			print(self.Language.language_texts["total_duration_of"] + " " + self.writing["Writing mode"]["Language texts"]["Item"] + ":")
			print("\t" + self.writing["Writing"]["Duration"]["Text"][self.language["Small"]])

		# ---------- #

		# Ask to start counting the writing time
		type_text = self.language_texts["press_enter_to_start_counting_the_time_of"] + " " + self.writing["Writing mode"]["Language texts"]["Item"]

		self.Input.Type(type_text)

		# Define the "Session" dictionary, with the first writing time
		self.writing["Session"] = {
			"Before": self.Date.Now(),
			"After": {},
			"After (copy)": {},
			"Duration": {}
		}

		# Show the now (before) time
		print()
		print(self.Date.language_texts["now, title()"] + ":")
		print("\t" + self.writing["Session"]["Before"]["Timezone"]["DateTime"]["Formats"]["HH:MM DD/MM/YYYY"])

		# ---------- #

		# Make a backup of the before time
		self.Make_Backup_Of_Time("Create", "Before")

		# ---------- #

		# Define the "Pause writing session" state as True
		self.states["Pause writing session"] = True

		# While the "Pause writing session" state is equal to True
		while self.states["Pause writing session"] == True:
			# Ask if the user wants to pause the writing session
			self.Pause_Writing()

		# Show a five dash space separator
		print()
		print(self.separators["5"])

		# ---------- #

		# Define the "postpone writing session" text template
		template = self.language_texts["do_you_want_to_postpone_the_{}_session_to_continue_{}_later"]

		# Define the list of items to format the text template
		items = [
			self.writing["Writing mode"]["Language texts"]["Item"],
			self.writing["Writing mode"]["Language texts"]["Action"]
		]

		# Format the template with the items in the list, making the input text
		input_text = template.format(*items)

		# Define the "ask to postpone" switch
		ask_to_postpone = False

		# If the "ask to postpone" switch is True
		if ask_to_postpone == True:
			# Ask if the user wants to postpone the writing session to continue writing later
			self.states["Postpone writing session"] = self.Input.Yes_Or_No(input_text)

			# Show a five dash space separator
			print()
			print(self.separators["5"])

		# ---------- #

		# Ask for the user to press Enter when they stop writing
		# (Not when the user finished writing the whole chapter)
		type_text = self.language_texts["press_enter_when_you_stop"] + " " + self.writing["Writing mode"]["Language texts"]["Infinitive action"]

		self.Input.Type(type_text)

		# Show a five dash space separator
		print()
		print(self.separators["5"])

		# ---------- #

		# Define the "After" time (now, but after writing)
		self.writing["Session"]["After"] = self.Date.Now()

		# Create the copy of the after time
		self.writing["Session"]["After (copy)"] = deepcopy(self.writing["Session"]["After"])

		# Define the after time as None
		after_time = None

		# ---------- #

		# Make a backup of the after time
		self.Make_Backup_Of_Time("Create", "After")

		# ---------- #

		# Define the empty addon variable
		addon = ""

		# If the "Pause" dictionary is present
		if "Pause" in self.writing["Session"]:
			# Define the addon as the text about the writing time with the pause time subtracted
			addon = " (" + self.language_texts["with_the_pause_time_subtracted"] + ")"

			# Define a subtract dictionary
			subtract = {}

			# Fill the subtract dictionary
			for key, value in self.writing["Session"]["Pause"]["Subtract"].items():
				subtract[key.lower()] = value

			# Define the relative delta
			relative_delta = self.Date.Relativedelta(**subtract)

			# Subtract the subtract time from the after time, creating the after time
			self.writing["Session"]["After (copy)"] = self.Date.Now(self.writing["Session"]["After (copy)"]["Object"] - relative_delta)

			# Update the after time
			after_time = self.writing["Session"]["After (copy)"]

		# ---------- #

		# Define the "add" variable
		add = False

		# If the "Testing" switch is True
		if self.switches["Testing"] == True:
			# Define the "add" variable as True
			add = True

		# Calculate and define the writing duration
		self.writing["Session"]["Duration"] = self.Calculate_Duration(self.writing["Session"], add = add, after_time = after_time)

		# Show the after time (after writing the chapter)
		print()
		print(self.Date.language_texts["after, title()"] + ":")
		print("\t" + self.writing["Session"]["After"]["Timezone"]["DateTime"]["Formats"]["HH:MM DD/MM/YYYY"])

		# Define the text to show
		text = self.Language.language_texts["duration_of"] + " " + self.writing["Writing mode"]["Language texts"]["Item"]

		# Add the addon if it is not empty
		if addon != "":
			text += addon

		# Add the colon
		text += ":"

		# Show the writing duration text in the user language
		print()
		print(text)

		# Show the writing duration (subtracting the pause time)
		print("\t" + self.writing["Session"]["Duration"]["Text"][self.language["Small"]])

		# Show the pause duration time in the user language
		text = self.Language.language_texts["duration_of"] + " " + self.Language.language_texts["pause, type: item"].lower()
		text += " (" + self.language_texts["the_time_subtracted_from_the_total_{}_time"].format(self.writing["Writing mode"]["Language texts"]["Item"]) + ")"

		# If the "Pause" key is present inside the "Session" dictionary
		if "Pause" in self.writing["Session"]:
			# Show the pause duration time in the user language
			text = self.Language.language_texts["duration_of"] + " " + self.Language.language_texts["pause, type: item"].lower()
			text += " (" + self.language_texts["the_time_subtracted_from_the_total_{}_time"].format(self.writing["Writing mode"]["Language texts"]["Item"]) + ")"

			print()
			print(text + ":")
			print("\t" + self.writing["Session"]["Pause"]["Duration"]["Text"][self.language["Small"]])

		# ---------- #

		# If the writing session is the first one for the current chapter
		if self.writing["Writing"]["Duration"]["Units"] == {}:
			# Define the first time of writing as the "Before" time
			self.writing["Writing"]["First"] = self.writing["Session"]["Before"]

		else:
			# Transform the already existing first writing time into a Date dictionary
			self.writing["Writing"]["First"] = self.Date.From_String(self.writing["Writing"]["First"])

		# Define the "Added" time as the first time if it is not present
		if self.writing["Writing"]["Added"] == "":
			self.writing["Writing"]["Added"] = deepcopy(self.writing["Writing"]["First"])

		else:
			# Transform the already existing added writing time into a Date dictionary
			self.writing["Writing"]["Added"] = self.Date.From_String(self.writing["Writing"]["Added"])

		# Define the last time of writing as the "After" time
		self.writing["Writing"]["Last"] = self.writing["Session"]["After"]

		# If the user started writing this chapter just now
		if self.states["Ongoing writing session"] == False:
			# Define the "Duration" dictionary inside the writing "Times" dictionary
			# With the "Units" dictionary being the units of the current session duration
			self.writing["Writing"]["Duration"] = {
				"Units": self.writing["Session"]["Duration"]["Difference"],
				"Text": {},
				"Text (with time units)": {}
			}

		# Calculate and update the writing time
		self.Update_Writing_Time()

		# ---------- #

		# Make a backup of the duration time
		self.Make_Backup_Of_Time("Create", "Duration")

		# ---------- #

		# If the "Ongoing writing session" state is True (the user resumed writing the chapter)
		if self.states["Ongoing writing session"] == True:
			# Show the total writing time text in the user language
			print()
			print(self.Language.language_texts["total_duration_of"] + " " + self.writing["Writing mode"]["Language texts"]["Item"] + ":")
			print("\t" + self.writing["Writing"]["Duration"]["Text"][self.language["Small"]])

		# ---------- #

		# Define the text asking if the user finished writing the whole chapter, not just a part of it
		type_text = self.language_texts["did_you_finished_{}_the_whole_chapter"].format(self.writing["Writing mode"]["Language texts"]["Infinitive action"])

		# If the writing session has not been postponed
		if self.states["Postpone writing session"] == False:
			# Ask if the user finished writing the whole chapter
			self.states["Finished writing"] = self.Input.Yes_Or_No(type_text)

		# Close the server
		self.Manage_Server(close = True, show_text = False)

		# If the user finished writing the whole chapter
		if self.states["Finished writing"] == True:
			# Run the "Finish_Writing" method
			self.Finish_Writing()

		# If the user did not finish writing the whole chapter
		# And the writing session has not been postponed
		if (
			self.states["Finished writing"] == False and
			self.states["Postpone writing session"] == False
		):
			# Show a five dash space separator
			print()
			print(self.separators["5"])

			# Register the writing task only on Diary Slim
			self.Register_Task(register_task = False)

		# ---------- #

		# Delete the backup
		self.Make_Backup_Of_Time("Delete")

	def Pause_Writing(self):
		# Ask if the user wants to pause the writing session
		input_text = self.language_texts["do_you_want_to_pause_the_{}_session"].format(self.writing["Writing mode"]["Language texts"]["Item"])

		self.states["Pause writing session"] = self.Input.Yes_Or_No(input_text)

		# If the user wants to pause the writing session
		if self.states["Pause writing session"] == True:
			# Show a five dash space separator
			print()
			print(self.separators["5"])

			# Show the before time (when starting writing the chapter)
			print()
			print(self.Date.language_texts["before, title()"] + ":")
			print("\t" + self.writing["Session"]["Before"]["Timezone"]["DateTime"]["Formats"]["HH:MM DD/MM/YYYY"])

			# Calculate and define the writing duration
			self.writing["Session"]["Duration"] = self.Calculate_Duration(self.writing["Session"])

			# Show the after time (after writing the chapter)
			print()
			print(self.Date.language_texts["after, title()"] + ":")
			print("\t" + self.writing["Session"]["After"]["Timezone"]["DateTime"]["Formats"]["HH:MM DD/MM/YYYY"])

			# Show the writing duration time in the user language
			print()
			print(self.Language.language_texts["duration_of"] + " " + self.writing["Writing mode"]["Language texts"]["Item"] + ":")
			print("\t" + self.writing["Session"]["Duration"]["Text (with time units)"][self.language["Small"]])

			# ---------- #

			# If the "Pause" key is not in the session dictionary
			if "Pause" not in self.writing["Session"]:
				# Define the "Pause" dictionary
				self.writing["Session"]["Pause"] = {
					"Before": self.Date.Now(),
					"After": {},
					"After (copy)": {},
					"Is pause": True
				}

			# If the "Pause" key is in the session dictionary
			else:
				self.states["Already paused"] = True

			# ---------- #

			# Ask for user input to unpause the writing session
			input_text = self.language_texts["press_enter_to_unpause_the_{}_session"].format(self.writing["Writing mode"]["Language texts"]["Item"])

			self.Input.Type(input_text)

			# ---------- #

			# Show a five dash space separator
			print()
			print(self.separators["5"])

			# If the user did not pause the writing session
			if self.states["Already paused"] == False:
				# Calculate and define the pause duration
				self.writing["Session"]["Pause"]["Duration"] = self.Calculate_Duration(self.writing["Session"]["Pause"])

			# Show the after time (after writing the chapter)
			print()
			print(self.Date.language_texts["after, title()"] + ":")
			print("\t" + self.writing["Session"]["Pause"]["After"]["Timezone"]["DateTime"]["Formats"]["HH:MM DD/MM/YYYY"])

			# ---------- #

			# If the user already paused the writing session
			if self.states["Already paused"] == True:
				if self.switches["Testing"] == False:
					# Define the after time
					after_time = self.Date.Now()

				if self.switches["Testing"] == True:
					relative_delta = self.Date.Relativedelta(minutes = 15)

					after_time = self.Date.Now(self.writing["Session"]["Pause"]["After"]["Object"] + relative_delta)

				# Create the difference between the now and after time
				difference = self.Date.Difference(self.writing["Session"]["Pause"]["After"], after_time)

				# Define the add dictionary
				add = {}

				# Fill the subtract dictionary
				for key, value in difference["Difference"].items():
					add[key.lower()] = value

				# Define the relative delta
				relative_delta = self.Date.Relativedelta(**add)

				# Add the add time to the after time
				self.writing["Session"]["Pause"]["After"] = self.Date.Now(self.writing["Session"]["Pause"]["After"]["Object"] + relative_delta)

			# ---------- #

			# Define the time difference
			self.writing["Session"]["Pause"]["Duration"] = self.Date.Difference(self.writing["Session"]["Pause"]["Before"], self.writing["Session"]["Pause"]["After"])

			# Define the subtract time
			self.writing["Session"]["Pause"]["Subtract"] = self.writing["Session"]["Pause"]["Duration"]["Difference"]

			# ---------- #

			# Define the subtract dictionary
			subtract = {}

			# Fill the subtract dictionary
			for key, value in self.writing["Session"]["Pause"]["Subtract"].items():
				subtract[key.lower()] = value

			# Define the relative delta
			relative_delta = self.Date.Relativedelta(**subtract)

			# Subtract the subtract time from the after time
			after_time = self.Date.Now(self.writing["Session"]["After (copy)"]["Object"] - relative_delta)

			# Define the time difference
			difference = self.Date.Difference(self.writing["Session"]["Before"], after_time)

			# Define the text to show
			text = self.Language.language_texts["duration_of"] + " " + self.writing["Writing mode"]["Language texts"]["Item"]

			# If the "Pause" key is present inside the "Session" dictionary
			if "Pause" in self.writing["Session"]:
				# Add the text about the writing time with the pause time subtracted
				text += " (" + self.language_texts["with_the_pause_time_subtracted"] + ")"

			# Add the colon
			text += ":"

			# Show the writing duration time in the user language (subtracting the pause time)
			print()
			print(text)
			print("\t" + difference["Text (with time units)"][self.language["Small"]])

			# ---------- #

			# Show the pause duration time in the user language
			text = self.Language.language_texts["duration_of"] + " " + self.Language.language_texts["pause, type: item"].lower()
			text += " (" + self.language_texts["the_time_subtracted_from_the_total_{}_time"].format(self.writing["Writing mode"]["Language texts"]["Item"]) + ")"

			print()
			print(text + ":")
			print("\t" + self.writing["Session"]["Pause"]["Duration"]["Text"][self.language["Small"]])

	def Calculate_Duration(self, dictionary, add = True, after_time = None):
		# If the "After" key is an empty dictionary
		if dictionary["After"] == {}:
			# Define the after time
			dictionary["After"] = self.Date.Now()

		# If the "after time" parameter is None
		if after_time == None:
			# Define the local "after time" variable as a copy of the "After" key
			after_time = deepcopy(dictionary["After"])

		# If the "Testing" switch is True
		if self.switches["Testing"] == True:
			# Define the time to add
			time = {
				"hours": 1,
				"minutes": 30,
				"seconds": 4
			}

			# If the "Is pause" key is in the dictionary
			if "Is pause" in dictionary:
				# Define the hours as 0
				time["hours"] = 0

				# Define the minutes as 10
				time["minutes"] = 10

			# Define the relative delta with the time dictionary
			relative_delta = self.Date.Relativedelta(**time)

			# If the "add" parameter is True
			if add == True:
				# Add the relative delta to the after time
				after_time = self.Date.Now(after_time["Object"] + relative_delta)

				if "After (copy)" in dictionary:
					# Update the copy of the after time
					dictionary["After (copy)"] = after_time

				# If the "Is pause" key is in the dictionary
				if "Is pause" in dictionary:
					# Update the after time
					dictionary["After"] = after_time

		# Get the time difference between the before and the after times
		difference = self.Date.Difference(dictionary["Before"], after_time)

		return difference

	def Finish_Writing(self):
		# If the writing mode is inside the defined list
		if self.writing_mode in ["Write", "Revise"]:
			# Add or update the chapter, depending on the writing mode
			self.Update_Chapter()

		# Update the chapter dictionary
		self.Update_Chapter_Dictionary()

		# Update the statistic about the written chapter 
		self.Update_Statistic()

		# Register the writing task
		self.Register_Task()

		# Reset the writing mode "Writing" dictionary to its default version
		self.Update_Writing_Time(purge = True)

	def Update_Writing_Time(self, purge = False):
		# If the "purge" parameter is False
		if purge == False:
			# Create the time units dictionary
			dictionary = {}

			# Iterate through the time difference keys
			for key, unit in self.writing["Session"]["Duration"]["Difference"].items():
				dictionary[key.lower()] = unit

			# Add the writing time difference time unit to the added time date object
			self.writing["Writing"]["Added"]["Object"] += self.Date.Relativedelta(**dictionary)

			# Transform the added time into a date dictionary with the updated object (the added time above)
			self.writing["Writing"]["Added"] = self.Date.Now(self.writing["Writing"]["Added"]["Object"])

			# Make the difference between the first time and the added time
			difference = self.Date.Difference(self.writing["Writing"]["First"]["Object"], self.writing["Writing"]["Added"]["Object"])

			# Define a list of keys to import from the local difference dictionary
			keys = [
				"Text",
				"Text (with time units)",
				"Time units text"
			]

			# Import them
			for key in keys:
				self.writing["Writing"]["Duration"][key] = difference[key]

			# Define the "Units" key to be used later
			self.writing["Writing"]["Duration"]["Units"] = difference["Difference"]

			# Transform the times back into date strings
			for key in ["First", "Last", "Added"]:
				self.writing["Writing"][key] = self.Date.To_String(self.writing["Writing"][key], utc = False)

		# If the "purge" parameter is True
		if purge == True:
			# Reset the writing mode "Times" dictionary to its default version
			self.story["Information"]["Writing"][self.writing_mode]["Times"] = {
				"First": "",
				"Last": "",
				"Added": "",
				"Duration": {
					"Units": {},
					"Text": {}
				}
			}

		# Update the "Writing.json" file
		self.JSON.Edit(self.story["Folders"]["Information"]["Writing"], self.story["Information"]["Writing"])

		# If the "purge" parameter is False
		if purge == False:
			# Transform the date strings back into date dictionaries
			for key in ["First", "Last", "Added"]:
				self.writing["Writing"][key] = self.Date.From_String(self.writing["Writing"][key])

	def Update_Chapter(self):
		# Define the default "update chapter titles" variable
		update_chapter_titles = False

		# If the writing mode is "Revise"
		if self.writing_mode == "Revise":
			# Ask if the user wants to update the chapter titles
			input_text = self.language_texts["do_you_want_to_update_the_chapter_titles"]

			update_chapter_titles = self.Input.Yes_Or_No(input_text)

		# If the writing mode is "Revise"
		# And the "update chapter titles" variable is True
		if (
			self.writing_mode == "Revise" and
			update_chapter_titles == True
		):
			# Make a backup of the old chapter
			self.chapter["Old chapter"] = deepcopy(self.chapter["Titles"])

		# Show a five dash space separator
		print()
		print(self.separators["5"])

		# Iterate through the language keys and dictionaries
		for small_language, language in self.languages["Dictionary"].items():
			# Get the current language translated to the user language
			translated_language = language["Translated"][self.language["Small"]]

			# Define a shortcut to the full language
			full_language = language["Full"]

			# Get the " in [language]" text of the current language
			in_language_text = " " + self.Language.texts["in_[language]"][small_language][self.language["Small"]]

			# Define the type text to ask for the new chapter title in the current language
			type_text = self.language_texts["type_the_new_chapter_title"] + in_language_text

			# Define the default "chapter title" variable as an empty string
			chapter_title = ""

			# If the writing mode is "Revise"
			# And the "update chapter titles" variable is True
			if (
				self.writing_mode == "Revise" and
				update_chapter_titles == True
			):
				# Show the old chapter title with the " in [language]" text
				print()
				print(self.language_texts["old_title"] + in_language_text + ":")
				print(self.chapter["Previous chapter"][small_language])

			# If the writing mode is "Write"
			# Or the writing mode is "Revise"
			# And the "update chapter titles" variable is True
			if (
				self.writing_mode == "Write" or
				self.writing_mode == "Revise" and
				update_chapter_titles == True
			):
				# If the "Testing" switch is False
				if self.switches["Testing"] == False:
					# Ask for the chapter title in the current language
					chapter_title = self.Input.Type(type_text, next_line = True)

				# If the "Testing" switch is True
				if self.switches["Testing"] == True:
					chapter_title = self.texts["a_new_chapter"][small_language].title()

					# Show the defined chapter title
					print()
					print(type_text + ":")
					print(chapter_title)

			# If the "chapter title" variable is not empty
			if chapter_title != "":
				# Add it to the "Titles" dictionary
				self.chapter["Titles"][small_language] = chapter_title

				# If the writing mode is "Revise"
				if self.writing_mode == "Revise":
					# Redefine the chapter title with leading zeroes to be only the number
					self.chapter["Titles (with leading zeroes)"][small_language] = self.chapter["Numbers"]["Leading zeroes"]

				# Add it to the "Titles (with leading zeroes)" dictionary
				self.chapter["Titles (with leading zeroes)"][small_language] += " - " + chapter_title

				# Define the titles file for easier typing
				file = self.story["Folders"]["Chapters"][full_language]["Titles"]["Titles"]

				# Define the default mode (append)
				mode = "a"

				# If the writing mode is "Write"
				if self.writing_mode == "Write":
					# Define the text
					text = chapter_title

				# If the writing mode is "Revise"
				# And the "update chapter titles" variable is True
				if (
					self.writing_mode == "Revise" and
					update_chapter_titles == True
				):
					# Get the list of chapter titles
					titles = self.File.Contents(file)["lines"]
					titles[self.chapter["Number"] - 1] = chapter_title

					# Define the text
					text = self.Text.From_List(titles, next_line = True)

					# Change the writing mode to "write"
					mode = "w"

				# If the writing mode is "Write"
				# Or the writing mode is "Revise"
				# And the "update chapter titles" variable is True
				if (
					self.writing_mode == "Write" or
					self.writing_mode == "Revise" and
					update_chapter_titles == True
				):
					# Edit the language titles file with the define text and mode
					self.File.Edit(file, text, mode)

			# ---------- #

			# Rename or create the chapter file

			# Define the source file
			source_file = self.chapter["Files"][small_language]

			# Define the destination file
			destination_file = self.story["Folders"]["Chapters"][full_language]["root"] + self.Sanitize(self.chapter["Titles (with leading zeroes)"][small_language], restricted_characters = True) + ".txt"

			# If the writing mode is "Write"
			# And the current language is the user language
			# Or the writing mode is "Revise"
			# And the "update chapter titles" variable is True
			if (
				self.writing_mode == "Write" and
				small_language == self.language["Small"] or
				self.writing_mode == "Revise" and
				update_chapter_titles == True
			):
				# Rename the chapter file
				self.File.Move(source_file, destination_file)

			# If the current language is not the user language
			# And the writing mode is not "Revise"
			if (
				small_language != self.language["Small"] and
				self.writing_mode != "Revise"
			):
				# Create the file
				self.File.Create(destination_file)

			# Update the file inside the "Chapter" dictionary
			self.chapter["Files"][small_language] = destination_file

		# ---------- #

		# If the writing mode is "Write"
		if self.writing_mode == "Write":
			# Add the written date of the chapter to the "Writing dates.txt" file
			file = self.story["Folders"]["Chapters"]["Writing dates"]
			date = self.writing["Writing"]["Last"]["Timezone"]["DateTime"]["Formats"]["HH:MM DD/MM/YYYY"]

			self.File.Edit(file, date, "a")

	def Update_Chapter_Dictionary(self):
		# Get the date that the user finished writing the chapter
		date = self.writing["Writing"]["Last"]["Timezone"]["DateTime"]["Formats"]["HH:MM DD/MM/YYYY"]

		# If the writing mode is "Write"
		if self.writing_mode == "Write":
			# Create or update the chapter dictionary
			self.story["Information"]["Chapters"]["Dictionary"][str(self.chapter["Number"])] = {
				"Number": self.chapter["Number"],
				"Titles": self.chapter["Titles"],
				"Dates": {
					"Written": "",
					"Revised": "",
					"Translated": ""
				}
			}

			# Add the writing date to the "Writing dates" list
			self.story["Information"]["Chapters"]["Writing dates"].append(date)

		# Update the "Titles" key
		self.story["Information"]["Chapters"]["Dictionary"][str(self.chapter["Number"])]["Titles"] = self.chapter["Titles"]

		# Define a shortcut variable for the chapter dictionary inside the "Dictionary" key
		chapter = self.story["Information"]["Chapters"]["Dictionary"][str(self.chapter["Number"])]

		# Define the key for the date of the writing mode
		key = self.writing["Writing mode"]["Texts"]["Chapter"]["en"]

		# Update the date key of the correct writing mode
		chapter["Dates"][key.capitalize()] = date

		# Check and update the chapter date texts inside the chapter files
		self.Check_Chapter_Date_Texts()

		# Update the "Chapters.json" file with the updated "Chapters" dictionary
		self.JSON.Edit(self.story["Folders"]["Information"]["Chapters"], self.story["Information"]["Chapters"])

	def Make_Task_Title(self, dictionary):
		# Get the language of the dictionary
		language = dictionary["Language"]

		# If the "Items" key does not exist in the dictionary
		if "Items" not in dictionary:
			# Define the list of items to use to format the template
			dictionary["Items"] = [
				self.writing["Writing mode"]["Texts"]["Infinitive action"][language],
				self.chapter["Numbers"]["Names"][language],
				self.story["Titles"][language]
			]

		# If the "Ongoing writing session" state is True (the user resumed writing the chapter)
		# And is not the last one (the user did not finished writing the whole chapter)
		if (
			self.states["Ongoing writing session"] == True and
			self.states["Finished writing"] == False
		):
			# Update the writing mode text to the "Action" one
			dictionary["Items"][0] = self.writing["Writing mode"]["Texts"]["Action"][language]

		# Define the task title in the current language as the template in the current language
		task_title = dictionary["Template"][language]

		# If the writing mode is "Translate"
		if self.writing_mode == "Translate":
			# Get the origin language translated to the local language
			origin_language = self.chapter["Origin language"]["Translated"][language]

			# Get the English language dictionary
			english = self.languages["Dictionary"]["en"]

			# Get the English language translated to the local language
			translated_english = english["Translated"][language]

			# Add the " from [origin langauge] to English" text
			# (The chapters are always translated from the user language to the English language, so the origin language is the user language)
			task_title += " " + self.Language.texts["from_{}_to_{}"][language].format(origin_language, translated_english)

		# Format the template with the list of items
		task_title = task_title.format(*dictionary["Items"])

		# Return the task title
		return task_title

	def Register_Task(self, register_task = True):
		# Create the task dictionary, to use it on the "Tasks" class
		self.task_dictionary = {
			"Task": {
				"Titles": {},
				"Descriptions": {},
				"Custom task item": self.writing["Writing mode"]["Texts"]["Chapter"]
			}
		}

		# If the "Statistics text" key is present inside the root dictionary
		if "Statistics text" in self.writing:
			# Define the statistics text as the additional text for the "Tasks" class
			self.task_dictionary["Additional text"] = self.writing["Statistics text"]

		# Define the text template for the task as the "I started writing", for the first time
		template = self.texts["i_started_{}_the_chapter_{}_of_my_story_{}"]

		# Define an empty version of the task template
		task_title_template = ""

		# If the "Ongoing writing session" state is True (the user resumed writing the chapter)
		# And is not the last one (the user did not finished writing the whole chapter)
		if (
			self.states["Ongoing writing session"] == True and
			self.states["Finished writing"] == False
		):
			# Define the text template for the task as the "I have been writing", for the middle times
			# (Not the beginning of writing, and not the ending)
			template = self.texts["i_have_been_{}_the_chapter_{}_of_my_story_{}_until_now"]

		# If the user finished writing the whole chapter
		if self.states["Finished writing"] == True:
			# Define the text template for the task as the "I finished writing", for the last time
			template = self.texts["i_finished_{}_the_chapter_{}_of_my_story_{}"]

			# Define the text template for the task title
			task_title_template = self.texts["i_{}_the_chapter_{}_of_my_story_{}"]

		# ---------- #

		# Iterate through the language keys and dictionaries
		for small_language, language in self.languages["Dictionary"].items():
			# Get the user language translated to the current language
			translated_user_language = self.language["Translated"][language]

			# Create the dictionary for the "Make_Task_Title" method
			dictionary = {
				"Language": small_language,
				"Translated user language": translated_user_language,
				"Template": template
			}

			# Create the task title and get it back
			task_title = self.Make_Task_Title(dictionary)

			# Add the task title to the "Task" dictionary
			self.task_dictionary["Task"]["Titles"][small_language] = task_title

			# ---------- #

			# Create the task description, initially as the task title with a dot
			description = self.task_dictionary["Task"]["Titles"][small_language] + "."

			# Add two line breaks
			description += "\n\n"

			# ---------- #

			# Create a different task title for the task if the chapter has been finished

			# If the task title template is not empty
			if task_title_template != "":
				# Define the list of items to use to format the template
				items = [
					self.writing["Writing mode"]["Texts"]["Done"][small_language],
					self.chapter["Numbers"]["Names"][small_language],
					self.story["Titles"][small_language]
				]

				# Create the dictionary for the "Make_Task_Title" method
				dictionary = {
					"Language": small_language,
					"Translated user language": translated_user_language,
					"Template": task_title_template,
					"Items": items
				}

				# Create the task title and get it back
				task_title = self.Make_Task_Title(dictionary)

				# Update the task title in the "Task" dictionary
				self.task_dictionary["Task"]["Titles"][small_language] = task_title

			# ---------- #

			# If the user finished writing the whole chapter
			# And the writing mode is either "Write" or "Revise"
			# Or the writing mode is "Translate"
			if (
				self.states["Finished writing"] == True and
				self.writing_mode in ["Write", "Revise"] or
				self.writing_mode == "Translate"
			):
				# Add the "The chapter with the title" text
				description += self.texts["the_chapter_with_the_title"][small_language] + ":" + "\n"

				# Add the chapter title in the current language
				description += self.chapter["Titles"][small_language]

				# Add two line breaks
				description += "\n\n"

			# ---------- #

			# Define the list of items to use to format the "I started {} and stopped at {}" text template
			# (Split the start and stop dates by a space to get only the hours and minutes)
			items = [
				self.writing["Session"]["Before"]["Formats"]["HH:MM DD/MM/YYYY"].split(" ")[0],
				self.writing["Session"]["After"]["Formats"]["HH:MM DD/MM/YYYY"].split(" ")[0]
			]

			# Format the "I started {} and stopped at {}" text template with the list of items and add it to the description
			description += self.texts["i_started_at_{}_and_stopped_at_{}"][small_language].format(*items)

			# Add a dot and a line break
			description += "." + "\n"

			# ---------- #

			# Add the "I [wrote] for [writing time]" formatted template
			items = [
				self.writing["Writing mode"]["Texts"]["Done"][small_language].lower()
			]

			description += self.texts["i_{}_for"][small_language].format(*items)

			# Add the session writing time text
			# Example: 1 hour, 30 minutes, 10 seconds
			description += " " + self.writing["Session"]["Duration"]["Text"][small_language]

			# Define the local "add_time_units_text" switch as True
			add_time_units_text = True

			# If the "add_time_units_text" switch is True
			if add_time_units_text == True:
				# Add the session writing time units text
				# Example: (01:30:10)
				description += " (" + self.writing["Session"]["Duration"]["Time units text"] + ")"

			# Add the end period
			description += "."

			# ---------- #

			# If the "Ongoing writing session" state is True (the user resumed writing the chapter)
			if self.states["Ongoing writing session"] == True:
				# Add two line breaks
				description += "\n\n"

				# Add the "Totalling " text
				description += self.Language.texts["totaling, title()"][small_language] + " "

				# Add the total writing time text
				# Example: 1 hour, 30 minutes, 10 seconds
				description += self.writing["Writing"]["Duration"]["Text"][small_language]

				# If the "add_time_units_text" switch is True
				if add_time_units_text == True:
					# Add the session writing time units text
					# Example: (01:30:10)
					description += " (" + self.writing["Writing"]["Duration"]["Time units text"] + ")"

				# Add the end period
				description += "."

			# ---------- #

			# Add the task description to the "Task" dictionary
			self.task_dictionary["Task"]["Descriptions"][small_language] = description

		# Register the task with the root method
		Stories.Register_Task(self, self.task_dictionary, register_task = register_task)

	def Update_Statistic(self):
		# Define the local story title variable
		story_titles = self.story["Titles"]

		# Define the local writing mode dictionary with the key and number
		writing_mode = {
			"Key": self.writing["Writing mode"]["Texts"]["Chapter"]["en"].capitalize(),
			"Number": 1,
			"Done plural": self.writing["Writing mode"]["Texts"]["Done plural"][self.language["Small"]]
		}

		# Update the story statistics for the current year and month, passing the story titles and writing mode dictionary
		self.writing["Statistics text"] = Stories.Update_Statistics(self, story_titles, writing_mode)
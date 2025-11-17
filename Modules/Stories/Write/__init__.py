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
			"Writing": {},
			"Chapter": {},
			"Session": {}
		}

		# Define the root states dictionary
		self.states = {
			"Select a chapter to revise": False,
			"A new chapter": False,
			"Ongoing writing session": False,
			"Pause writing session": False,
			"Already paused": False,
			"Postpone writing session": False,
			"Update chapter titles": False,
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
			# If the "Testing" switch is True
			# And the "Method" is a string
			if (
				self.switches["Testing"] == True and
				type(step["Method"]) == str
			):
				# Show the method name
				print()
				print(step["Method name"] + ":")

			# Run the method of the writing step
			step["Method"]()

	def Select_Writing_Mode(self):
		# Define the parameters dictionary to use inside the "Select" method of the "Input" utility module
		parameters = {
			"options": self.stories["Writing modes"]["List"], # The list of writing modes
			"language_options": [], # The empty list of language writing modes
			"show_text": self.language_texts["writing_modes"], # The "Writing modes" text in the user language
			"select_text": self.language_texts["select_a_writing_mode"] # The "Select a writing mode" text in the user language
		}

		# ---------- #

		# Define a shortcut to the total number of chapters for easier typing
		total_chapters = self.story["Chapters"]["Numbers"]["Total"]

		# Make a backup of the "Writing" dictionary
		self.story["Writing (backup)"] = deepcopy(self.story["Writing"])

		# Define a shortcut to the "language texts" dictionary of the "Language" class
		language_texts = self.Language.language_texts

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

			# Get the current chapter of the current writing mode
			current_chapter = writing_dictionary["Current chapter"]

			# Make a copy of the current chapter
			chapter = current_chapter

			# If the "Finished" status is True
			if status["Finished"] == True:
				# If the current chapter is not the last chapter
				if current_chapter != total_chapters:
					# Define the next chapter to be written
					chapter, writing_dictionary, status = self.Next_Chapter(chapter, writing_dictionary, status)

				# If the current chapter is the last chapter
				if current_chapter == total_chapters:
					# If the writing mode is "Write"
					if writing_mode == "Write":
						# Define the next chapter to be written
						chapter, writing_dictionary, status = self.Next_Chapter(chapter, writing_dictionary, status)

					# If the writing mode is "Revise"
					if writing_mode == "Revise":
						# Change the "Select a chapter to revise" state to True
						# (Ask the user to select a chapter to revise if they already revised all chapters)
						self.states["Select a chapter to revise"] = True

						# Define the writing mode as "Select a chapter to revise"
						writing_mode_text = self.language_texts["select_a_chapter_to_revise"]

			# Update the root current chapter
			current_chapter = chapter

			# ----- #

			# Define a local "Ongoing writing session" state as False
			# (This state is related to the current writing mode)
			ongoing_writing_session = False

			# Check if the writing "Started" time is not empty
			# (This means the user has already started writing the chapter)
			if writing_dictionary["Times"]["Started"] != "":
				# Change the local "Ongoing writing session" state to True
				ongoing_writing_session = True

			# ----- #

			# If the writing mode text is an empty string
			if writing_mode_text == "":
				# Define the writing mode text initially as "Start to"
				writing_mode_text = self.language_texts["start_to"]

				# Define the verb tense to use as the "Infinitive" one
				# [write/revise/translate]
				verb_tense = writing_mode_dictionary["Language texts"]["Infinitive"]

				# If the local "Ongoing writing session" state is True (the user resumed writing the chapter)
				if ongoing_writing_session == True:
					# Change the writing mode text to be "Continue"
					writing_mode_text = self.Language.language_texts["continue, title()"]

					# Define the verb tense to use as the "Action" one
					# [writing/revising/translating]
					verb_tense = writing_mode_dictionary["Language texts"]["Action"]

				# Add the defined verb tense to the writing mode text
				writing_mode_text += " " + verb_tense

				# ----- #

				# Define the "the chapter" text initially as the "the" masculine text
				the_chapter_text = language_texts["the, masculine"]

				# Add the " chapter" text
				the_chapter_text += " " + language_texts["chapter"]

				# Add the chapter number
				the_chapter_text += " " + str(chapter)

				# ----- #

				# Add the " the chapter" text to the writing mode text
				writing_mode_text += " " + the_chapter_text

			# Define the "Text addon" as an empty dictionary
			writing_mode_dictionary["Text addon"] = {}

			# If the writing mode is "Write"
			if writing_mode == "Write":
				# Define the "Text addon" dictionary as the "a new chapter" text dictionary
				writing_mode_dictionary["Text addon"] = self.texts["a_new_chapter"]

			# If the writing mode is either "Revise" or "Translate"
			# If the local "Ongoing writing session" state is True (the user resumed writing the chapter)
			if (
				writing_mode in ["Revise", "Translate"] and
				ongoing_writing_session == True
			):
				# Define the "Text addon" dictionary as the "in progress" text dictionary
				writing_mode_dictionary["Text addon"] = self.Language.texts["in_progress"]

			# If the "Text addon" dictionary is not empty
			if writing_mode_dictionary["Text addon"] != {}:
				# Add its user language version to to the writing mode text
				writing_mode_text += " (" + writing_mode_dictionary["Text addon"][self.language["Small"]] + ")"

			# Add the writing mode text to the list of language options
			parameters["language_options"].append(writing_mode_text)

			# ----- #

			# Add the writing mode dictionary to the "Writing modes" dictionary of the root "writing" dictionary
			self.writing["Writing modes"]["List"].append(writing_mode)
			self.writing["Writing modes"]["Dictionary"][writing_mode] = writing_mode_dictionary

		# ---------- #

		# Define the local writing mode as "Translate"
		writing_mode = "Translate"

		# Define a shortcut to the "Translate" writing mode dictionary
		writing_dictionary = self.story["Writing"][writing_mode]

		# Get the current chapter of the "Translate" writing mode
		current_chapter = writing_dictionary["Current chapter"]

		# Define a shortcut to the "Status" dictionary
		status = writing_dictionary["Status"]

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
			# Or the current chapter to revise has not been revised and it is not the last chapter
			# The current chapter needs to be revised before it can be translated)
			parameters["options"].remove(writing_mode)
			parameters["language_options"].pop(-1)

		# ---------- #

		# Ask the user to select a writing mode
		writing_mode = self.Input.Select(**parameters)["Option"]["Original"]

		# Get the writing mode dictionary for the selected writing mode
		self.writing["Writing mode"] = self.writing["Writing modes"]["Dictionary"][writing_mode]

		# Define a shortcut to the "Writing" dictionary of the writing mode
		self.writing["Writing"] = self.story["Writing"][writing_mode]

		# If the writing mode is "Write"
		if writing_mode == "Write":
			# Change the "A new chapter" state to True
			self.states["A new chapter"] = True

		# Define the "writing mode" root variable as the writing mode name for faster typing
		self.writing_mode = writing_mode

	def Next_Chapter(self, chapter, writing_dictionary, status):
		# Add one to the local chapter number
		# (To write/revise/translate the next chapter)
		chapter += 1

		# Update the "Current chapter" key
		writing_dictionary["Current chapter"] = chapter

		# Reset the keys of the "Times" dictionary
		writing_dictionary["Times"] = {
			"Started": "",
			"Finished": "",
			"Finished (UTC)": ""
		}

		# Reset the keys of the "Durations" dictionary
		writing_dictionary["Durations"] = {
			"List": [],
			"Dictionary": {}
		}

		# Reset the "Total duration" dictionary
		writing_dictionary["Total duration"] = {}

		# Iterate through the keys inside the "Status" dictionary
		for key in status:
			# If the status is True, change it to False
			if status[key] == True:
				status[key] = False

		# Return the chapter, writing dictionary, and status
		return chapter, writing_dictionary, status

	def Define_Chapter(self):
		# Define the chapter number as the current chapter in the writing dictionary
		self.writing["Chapter"]["Number"] = self.writing["Writing"]["Current chapter"]

		# If the "Select a chapter to revise" state is True
		if self.states["Select a chapter to revise"] == True:
			# Define a local custom parameters dictionary
			custom_parameters = {
				# Update the select text to be the "Select a chapter to revise" text in the user language
				"select_text": self.language_texts["select_a_chapter_to_revise"]
			}

			# Ask the user to select a chapter to revise, passing the custom parameters dictionary to the root "Select_Chapter" method
			self.writing["Chapter"]["Number"] = self.Select_Chapter(custom_parameters)

		# Update the chapter number inside the "Writing" dictionary
		self.writing["Writing"]["Current chapter"] = self.writing["Chapter"]["Number"]

		# ---------- #

		# Define the "Chapter" dictionary using the root "Select_Chapter" method, passing the chapter number to it
		self.writing["Chapter"] = self.Select_Chapter(chapter_number = self.writing["Chapter"]["Number"])

		# Define a shortcut to the chapter dictionary
		self.chapter = self.writing["Chapter"]

		# Reset the "Ongoing writing session" state to be False
		self.states["Ongoing writing session"] = False

		# Check if the writing "Started" time is not empty
		# (This means the user has already started writing the chapter and is resuming it)
		if self.writing["Writing"]["Times"]["Started"] != "":
			# Change the "Ongoing writing session" state to True
			self.states["Ongoing writing session"] = True

		# Define a shortcut to the chapter titles dictionary for easier typing
		chapter_titles = self.story["Chapters"]["Lists"]["Titles"]

		# Iterate through the language keys and dictionaries
		for small_language, language in self.languages["Dictionary"].items():
			# Define a shortcut to the full language
			full_language = language["Full"]

			# Define the default chapter title as the chapter number with leading zeroes
			chapter_title = self.chapter["Numbers"]["Leading zeroes"]

			# If the writing mode is either "Revise" or "Translate"
			if self.writing_mode in ["Revise", "Translate"]:
				# Get the actual chapter title
				# (The chapter number less one because Python list indexes start at zero)
				chapter_title = chapter_titles[small_language][self.chapter["Number"] - 1]

			# Define the chapter title with the number
			# Examples:
			# 01 (for the "Write" writing mode)
			# [Chapter Title] (for the "Revise" or "Translate" writing modes)
			chapter_title_with_number = chapter_title

			# If the writing mode is either "Revise" or "Translate"
			if self.writing_mode in ["Revise", "Translate"]:
				# Define the chapter title with the number
				# Example: 01 - [Chapter Title]
				chapter_title_with_number = self.chapter["Numbers"]["Leading zeroes"] + " - " + chapter_title

			# Add the chapter title to the titles "Normal" language dictionary
			self.chapter["Titles"]["Normal"][small_language] = chapter_title

			# Add the chapter title with the number to the titles "With number" language dictionary
			self.chapter["Titles"]["With number"][small_language] = chapter_title_with_number

			# Get the number name of the chapter number
			number_name = self.Date.texts["number_names, type: list"][small_language][self.chapter["Number"]]

			# Add it to the number "Names" dictionary
			self.chapter["Numbers"]["Names"][small_language] = number_name

			# ----- #

			# Define the chapter file in the current language as the "Chapters" folder of the selected story
			self.chapter["Files"][small_language] = self.story["Folders"]["Chapters"][full_language]["root"]

			# Sanitize the chapter title with number
			sanitized_chapter_title = self.Sanitize(chapter_title_with_number, restricted_characters = True)

			# Add it to the "Sanitized" key
			self.chapter["Titles"]["Sanitized"][small_language] = sanitized_chapter_title

			# Add the sanitized chapter title with number
			self.chapter["Files"][small_language] += self.chapter["Titles"]["Sanitized"][small_language] + ".txt"

			# ----- #

			# If the chapter number is inside the story "Chapters" dictionary
			if str(self.chapter["Number"]) in self.story["Chapters"]["Dictionary"]:
				# Get the chapter dictionary
				self.chapter["Dictionary"] = self.story["Chapters"]["Dictionary"][str(self.chapter["Number"])]

			# If it is not
			else:
				# Copy the root default "Chapter" dictionary
				self.chapter["Dictionary"] = deepcopy(self.stories["Chapter"])

				# Update the chapter "Number" key
				self.chapter["Dictionary"]["Number"] = int(self.chapter["Number"])

				# Update the chapter "Titles" key
				self.chapter["Dictionary"]["Titles"] = self.chapter["Titles"]["Normal"]

			# ----- #

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
			self.chapter["Destiny language"] = self.languages["Dictionary"]["en"]

			# Define the writing language as the destiny language
			self.chapter["Writing language"] = self.chapter["Destiny language"]

			# (The chapters are always translated from the user language to English)

		# ---------- #

		# Check the chapter date texts of the chapter files
		self.Check_Chapter_Date_Texts()

		# ---------- #

		# Show a five dash space separator
		print()
		print(self.separators["5"])
		print()

		# Show the "Writing this story" text and the story title in the user language
		print(self.language_texts["writing_this_story"] + ":")
		print("\t" + self.story["Titles"][self.language["Small"]])

		# Show the story titles in other languages
		for small_language, story_title in self.story["Titles"].items():
			# If the language is not the user language
			if small_language != self.language["Small"]:
				# Show the story title with a tab
				print("\t" + story_title)

		# Show a space after the story titles
		print()

		# Define the show text as the writing mode in the action verb tense
		show_text = self.writing["Writing mode"]["Language texts"]["Action"].title()

		# Add the " this chapter" text
		show_text += " " + self.language_texts["this_chapter"]

		# Show the text with the writing text in the action tense
		print(show_text + ":")

		# Show the chapter titles
		for small_language, chapter_title in self.chapter["Titles"]["With number"].items():
			# If the "Text addon" dictionary is not empty, add the text addon in the current language
			if self.writing["Writing mode"]["Text addon"] != {}:
				chapter_title += " (" + self.writing["Writing mode"]["Text addon"][small_language] + ")"

			# Show the chapter title in the current language
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
		# Iterate through the language keys and dictionaries
		for small_language, language in self.languages["Dictionary"].items():
			# Get the chapter file in the current language
			chapter_file = self.writing["Chapter"]["Files"][small_language]

			# Get the lines of the chapter file in the current language
			lines = self.File.Contents(chapter_file)["Lines"]

			# ---------- #

			# If the selected writing mode is "Translate"
			# And if the current language dictionary matches the "Destiny language" dictionary
			# (The destiny language is the language into which the chapter will be translated)
			# And if the user has just started writing this chapter
			if (
				self.writing_mode == "Translate" and
				small_language == self.chapter["Destiny language"] and
				self.states["Ongoing writing session"] == False
			):
				# Define a shortcut to the origin language
				origin_language = self.chapter["Origin language"]

				# Get the chapter file in the origin language (the user language)
				language_chapter_file = self.writing["Chapter"]["Files"][origin_language["Small"]]

				# Update the list of lines to be the chapter text of the original (user) chapter language
				lines = self.File.Contents(language_chapter_file)["Lines"]

				# Remove the first five lines that come from the original version of the chapter text
				# (The lines that say when the chapter was written, revised, and translated for the last time
				# The first four lines contain the chapter dates text, and the last one is an empty line)
				i = 1
				while i <= 5:
					lines.pop(0)

					i += 1

			# ---------- #

			# Get the language "Dates of the chapter:" text in the current language
			dates_of_the_chapter = self.texts["dates_of_the_chapter"][small_language] + ":"

			# Define the local insert switch as False
			insert = False

			# If the list of lines is empty
			# Or the first line of the file is not "Dates of the chapter:"
			if (
				lines == [] or
				lines[0] != dates_of_the_chapter
			):
				# Insert the "Dates of the chapter:" text at the beginning of the list of lines
				lines.insert(0, dates_of_the_chapter)

				# Change the local insert switch to True
				insert = True

			# ---------- #

			# Define a shortcut to the "chapter dates" text dictionary
			chapter_date_texts = self.texts["chapter_dates, type: dictionary"]

			# Iterate through the list of chapter date texts
			i = 1
			for key, text_template in chapter_date_texts.items():
				# Define the list of items to use to format the current chapter date text
				items = [
					"[date]",
					"[time]"
				]

				# ---------- #

				# If the key is "Translate"
				if key == "Translate":
					# Get the English language dictionary
					english_language = self.languages["Dictionary"]["en"]

					# Get the English language translated into the current language
					translated_english_language = english_language["Translated"][small_language]

					# Add the translated English language to the list of items
					# (The "Translate" chapter date text template includes an additional "{}" format string to insert the "Destiny language")
					items.insert(0, translated_english_language)

				# ---------- #

				# Format the chapter date text template in the current language
				# using the list of items and append a period at the end
				chapter_date_text = text_template[small_language].format(*items) + "."

				# Define a shortcut to the chapter number
				chapter_number = str(self.chapter["Number"])

				# If the chapter is not present inside the dictionary of chapters
				if chapter_number not in self.story["Chapters"]["Dictionary"]:
					# Copy the root default "Chapter" dictionary
					chapter = deepcopy(self.stories["Chapter"])

					# Convert the root chapter number into an integer and add it to the local chapter dictionary
					chapter["Number"] = int(chapter_number)

					# Add the local chapter dictionary to the root dictionary of chapters
					self.story["Chapters"]["Dictionary"][chapter_number] = chapter

				# Define a shortcut to the chapter dictionary
				chapter = self.story["Chapters"]["Dictionary"][chapter_number]

				# Define a shortcut to the writing mode dictionary of the current chapter date text
				writing_mode = self.stories["Writing modes"]["Dictionary"][key]

				# Get the "chapter dictionary" key for the current writing mode
				chapter_dictionary_key = writing_mode["Texts"]["Chapter dictionary"]

				# Get the writing dictionary for the current writing mode
				writing_dictionary = chapter[chapter_dictionary_key]

				# ---------- #

				# Define a local empty times dictionary
				times = {}

				# If the key is "Write"
				if key == "Write":
					# Get the correct "Times" dictionary for the "Write" dictionary
					times = writing_dictionary["Times"]

				# ---------- #

				# If the key is "Write"
				# And the "Times" dictionary is not empty
				# And the "Finished" writing time is not empty
				# Or the key is either "Revise" or "Translate"
				# And the list of writings is not empty
				if (
					(key == "Write" and
					times != {} and
					times["Finished"] != "") or
					(key in ["Revise", "Translate"] and
					writing_dictionary["List"] != [])
				):
					# If the key is "Write"
					if key == "Write":
						# Get the "Finished" writing date
						writing_date = times["Finished"]

					# If the key is not "Write"
					if key != "Write":
						# Get the list of writings
						writings = list(writing_dictionary["Dictionary"].values())

						# Get the last writing
						last_writing = writings[-1]

						# Get the last "Finished" writing date
						writing_date = last_writing["Times"]["Finished"]

					# Define the date dictionary using the defined writing date
					date = self.Date.From_String(writing_date, "%H:%M %d/%m/%Y")

					# Define the correct date format text based on the current language
					date_format_text = self.Date.texts["date_format, type: format"][small_language]

					# Replace the date strings in the date format text with the units and texts inside the date dictionary
					date_text = self.Date.Replace_Strings_In_Text(date_format_text, date, small_language)

					# Replace the "[date]" format text inside the chapter date text with the date text
					chapter_date_text = chapter_date_text.replace("[date]", date_text)

					# Get the writing time (hours and minutes) of the date
					writing_time = date["Timezone"]["DateTime"]["Formats"]["HH:MM"]

					# Replace the "[time]" format text inside the chapter date text with the writing time
					chapter_date_text = chapter_date_text.replace("[time]", writing_time)

				# ---------- #

				# If the local insert switch is False
				if insert == False:
					# Replace the chapter text line with the chapter date text
					# (With the date and time format strings replaced by the actual date and time)
					# (Insert is False when the "Dates of the chapter:" text is already present inside the chapter text lines
					# So the chapter date texts need to be updated, not added)
					lines[i] = chapter_date_text

				# If the local insert switch is True
				if insert == True:
					# Insert the chapter date text into the correct index inside the list of chapter text lines
					# (With the date and time format strings replaced by the actual date and time)
					# (Insert is True when the "Dates of the chapter:" text is not already present inside the chapter text lines
					# So the chapter date texts need to be added, not updated)
					lines.insert(i, chapter_date_text)

				# Add one to the "i" number
				i += 1

			# If the local insert switch is True
			if insert == True:
				# Insert a space after the last chapter date text to separate the chapter date texts from the chapter text
				lines.insert(i, "")

			# Transform the list of chapter text lines into a text string
			chapter_text = self.Text.From_List(lines, next_line = True)

			# Update the chapter file in the current language with the new text
			self.File.Edit(chapter_file, chapter_text, "w")

	def Open_Story_Website(self):
		# Open the server executable
		self.Manage_Server(open = True, separator_number = 3)

		# If the "Testing" switch is False
		if self.switches["Testing"] == False:
			# Wait for one second
			self.Date.Sleep(1)

		# ----- #

		# Get the PHP websites "URL" dictionary
		url = self.JSON.To_Python(self.folders["Mega"]["PHP"]["JSON"]["URL"])

		# Get the "Code" URL template with language and define it as the local template
		template = url["Code"]["Templates"]["With language"]

		# Define the list of items to use to format the URL template
		items = [
			# The story title and website title in English
			self.story["Title"],

			# The writing language (the language in which the chapter will be written)
			self.chapter["Writing language"]["Translated"][self.language["Small"]]
		]

		# Format the URL template with the list of items
		url = template.format(*items)

		# ----- #

		# Import the "urlencode" module to use it
		from urllib.parse import urlencode

		# Define the dictionary of custom parameters to add to the URL
		parameters = {
			"chapter": str(self.chapter["Number"]), # The number of the chapter
			"write": "true", # The write switch, to activate the writing mode in the story website
			"show_chapter_covers": "true" # To show the story chapter covers in the chapter tabs
		}

		# Encode the parameters into a query string
		query_string = urlencode(parameters)

		# Add the query string to the URL
		url += "&" + query_string

		# Define the language chapter link inside the chapter "Links" dictionary
		self.chapter["Links"] = {
			"Local website": {
				self.language["Small"]: url
			}
		}

		# ----- #

		# Show a three dash space separator
		print()
		print(self.separators["3"])

		# Define and show the text about opening the story website in the writing language
		text = self.language_texts["opening_the_local_story_website_in"] + " " + self.chapter["Writing language"]["Translated"][self.language["Small"]]

		print()
		print(text + "...")

		# Open the story website link in the current chapter in the default browser
		self.System.Open_Link(self.chapter["Links"]["Local website"][self.language["Small"]], verbose = False)

		# If the "Testing" switch is False
		if self.switches["Testing"] == False:
			# Wait for two seconds
			self.Date.Sleep(2)

	def Open_Writing_Pack(self):
		# If the writing mode is "Translate"
		# Or the "Testing" switch is True
		if (
			self.writing_mode == "Translate" or
			self.switches["Testing"] == True
		):
			# Show a three space separator
			print()
			print(self.separators["3"])
			print()

			# Define the text about opening the translator website
			text = self.language_texts["opening_the_translator_website"] + " "

			# Add the name of the translator website around quotes to the defined text
			text += '"' + self.stories["Writing"]["Translator website"]["Name"] + '"'

			# If the writing mode is not "Translate"
			# And the "Testing" switch is True
			if (
				self.writing_mode != "Translate" and
				self.switches["Testing"] == True
			):
				# Add the " (testing mode)" text to the text
				text += " (" + self.Language.language_texts["testing_mode"] + ")"

			# Show the text
			print(text + "...")

			# Open the link of the translator website in the default browser
			self.System.Open_Link(self.stories["Writing"]["Translator website"]["Link"], verbose = False)

			# If the "Testing" switch is False
			if self.switches["Testing"] == False:
				# Wait for one second
				self.Date.Sleep(1)

		# ---------- #

		# Show a three space separator
		print()
		print(self.separators["3"])
		print()

		# ---------- #

		# Define a shortcut to the text about opening the music player for the user to listen to the soundtrack of the story
		text = self.language_texts["opening_the_{}_music_player_for_you_to_listen_to_the_soundtrack_of_the_story"]

		# Format the text with the name of the music player
		text = text.format(self.stories["Writing"]["Music player"]["Name"])

		# Show the text
		print(text + "...")

		# Open the music player program so the user can listen to the soundtrack of the story
		self.System.Open(self.stories["Writing"]["Music player"]["Link"], verbose = False)

		# If the "Testing" switch is False
		if self.switches["Testing"] == False:
			# Wait for one second
			self.Date.Sleep(1)

	def Create_Discord_Status(self):
		# Define the Discord status template
		template = self.language_texts["{}_the_chapter_{}_of_my_story_{}"]

		# Define the list of items
		items = [
			# The action text of the writing mode in title case
			self.writing["Writing mode"]["Language texts"]["Action"].title(),

			# The number name of the chapter in the user language
			self.writing["Chapter"]["Numbers"]["Names"][self.language["Small"]],

			# The story title in the user language, with quotes around it
			'"' + self.story["Titles"][self.language["Small"]] + '"'
		]

		# Format the template with the items, making the Discord status
		discord_status = template.format(*items)

		# Define it inside the "Chapter" dictionary
		self.chapter["Discord"] = {
			"Status": discord_status
		}

		# ----- #

		# Define the text to show as the "Copying the Discord status" text
		text = self.Language.language_texts["copying_the_discord_status"]

		# Show a three space separator
		print()
		print(self.separators["3"])
		print()

		# Show the text to show
		print(text + "...")

		# Copy the Discord status to the clipboard
		self.Text.Copy(self.chapter["Discord"]["Status"])

	def Make_Backup_Of_Duration(self, mode = "Create", time = "Before"):
		# Define the backup file name as "Backup of the duration of [writing mode item]"
		file_name = self.language_texts["backup_of_the_duration_of"] + " " + self.writing["Writing mode"]["Language texts"]["Item"]

		# Define the folder
		folder = self.stories["Folders"]["Database"]["root"]

		# Define the backup file
		backup_file = folder + file_name + ".txt"

		# ---------- #

		# If the mode is "Create"
		if mode == "Create":
			# If the backup file does not exist
			if self.File.Exists(backup_file) == False:
				# Create it
				self.File.Create(backup_file)

			# If the time is "Before"
			if time == "Before":
				# Define the text to write as the before time
				text_to_write = file_name + ":" + "\n" + \
				"\n" + \
				self.Date.language_texts["before_time"] + ":" + "\n"

			# If the time is "After"
			if time == "After":
				# Define the text to write as the after time
				text_to_write = "\n" + \
				"\n" + \
				self.Date.language_texts["after_time"] + ":" + "\n"

			# Define the time
			time_dictionary = self.writing["Session"][time]

			# If the time is either "Before" or "After"
			if time in ["Before", "After"]:
				# Get the timezone datetime dictionary
				time_dictionary = time_dictionary["Timezone"]["DateTime"]

				# Get the correct format and define it as the time string
				time_string = time_dictionary["Formats"]["HH:MM DD/MM/YYYY"]

			# If the time is the duration one
			if time == "Duration":
				# Define the text to write as the duration
				text_to_write = "\n" + \
				"\n" + \
				self.Language.language_texts["duration, title()"] + ":" + "\n"

				# Define the time string
				time_string = time_dictionary["Text"][self.language["Small"]]

			# Add the time string to the text to write
			text_to_write += time_string

			# Write the text to the file in the append mode
			self.File.Edit(backup_file, text_to_write, "a")

		# ---------- #

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
			# Define a shortcut to the total writing duration dictionary
			total_duration = self.writing["Writing"]["Total duration"]

			# Show the total writing duration text in the user language
			print()
			print(self.Language.language_texts["total_duration_of"] + " " + self.writing["Writing mode"]["Language texts"]["Item"] + ":")
			print("\t" + total_duration["Text"][self.language["Small"]])

		# ---------- #

		# If the "Testing" switch is True
		if self.switches["Testing"] == True:
			# Show the "Chapter" text
			print()
			print("Chapter:")
			print()

			# Show the "Chapter" dictionary with the JSON format
			self.JSON.Show(self.chapter)

		# Define the type text to ask the user to press Enter to start counting the duration of [writing/revision/translation]
		type_text = self.language_texts["press_enter_to_start_counting_the_duration_of"] + " " + self.writing["Writing mode"]["Language texts"]["Item"]

		# Ask for user input with the text
		self.Input.Type(type_text)

		# Define the "Session" dictionary with the first (Before) writing time
		self.writing["Session"] = {
			"Before": self.Date.Now(),
			"After": {},
			"After (copy)": {},
			"Duration": {}
		}

		# Show the now (before) writing time (before starting to write the chapter)
		print()
		print(self.Date.language_texts["now_time"] + ":")
		print("\t" + self.writing["Session"]["Before"]["Timezone"]["DateTime"]["Formats"]["HH:MM DD/MM/YYYY"])

		# ---------- #

		# Make a backup of the before writing time
		self.Make_Backup_Of_Duration("Create", "Before")

		# ---------- #

		# Define the "Pause writing session" state initially as True
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

		# Define the list of items to use to format the text template
		items = [
			# The item text of the writing mode
			self.writing["Writing mode"]["Language texts"]["Item"],

			# The action text of the writing mode
			self.writing["Writing mode"]["Language texts"]["Action"]
		]

		# Format the template with the items in the list, making the input text
		input_text = template.format(*items)

		# Define the "ask to postpone" switch
		ask_to_postpone = False

		# If the "ask to postpone" switch is True
		if ask_to_postpone == True:
			# If the "Testing" switch is False
			if self.switches["Testing"] == False:
				# Ask if the user wants to postpone the writing session to continue writing later
				self.states["Postpone writing session"] = self.Input.Yes_Or_No(input_text)

			# If the "Testing" switch is True
			if self.switches["Testing"] == True:
				# Show the input text
				print(input_text)

			# Show a five dash space separator
			print()
			print(self.separators["5"])

		# ---------- #

		# Ask the user to press Enter when they stop writing
		# (Not when the user finishes writing the whole chapter, but when they write for a while and want to continue writing later)
		type_text = self.language_texts["press_enter_when_you_stop"] + " " + self.writing["Writing mode"]["Language texts"]["Infinitive action"]

		self.Input.Type(type_text)

		# Show a five dash space separator
		print()
		print(self.separators["5"])

		# ---------- #

		# Define the "After" writing time (now, but after writing)
		self.writing["Session"]["After"] = self.Date.Now()

		# Create a copy of the after writing time
		self.writing["Session"]["After (copy)"] = deepcopy(self.writing["Session"]["After"])

		# Define the local after writing time as None
		after_time = None

		# ---------- #

		# Make a backup of the after writing time
		self.Make_Backup_Of_Duration("Create", "After")

		# ---------- #

		# Define the empty text addon variable
		text_addon = ""

		# If the "Pause" dictionary is present
		if "Pause" in self.writing["Session"]:
			# Define the text addon as the text about the writing duration with the pause time subtracted
			text_addon = " (" + self.language_texts["with_the_pause_duration_subtracted"] + ")"

			# Define a local subtract dictionary
			subtract = {}

			# Define a shortcut to the "Pause" dictionary
			pause = self.writing["Session"]["Pause"]

			# Add the time units inside the pause "Subtract" dictionary to the local subtract dictionary
			for key, value in pause["Subtract"].items():
				subtract[key.lower()] = value

			# Define the relative delta method with the time to subtract
			relative_delta = self.Date.Relativedelta(**subtract)

			# Subtract the pause subtract time from the after writing time, creating the new after writing time
			self.writing["Session"]["After (copy)"] = self.Date.Now(self.writing["Session"]["After (copy)"]["Object"] - relative_delta)

			# Update the local after writing time to be the copy of the after writing time
			after_time = self.writing["Session"]["After (copy)"]

		# ---------- #

		# Define the "add" variable initially as False
		add = False

		# If the "Testing" switch is True
		if self.switches["Testing"] == True:
			# Define the "add" variable as True
			add = True

		# Calculate and define the writing duration using the "Calculate_Duration" method and passing the add and after time variables to it
		self.writing["Session"]["Duration"] = self.Calculate_Duration(self.writing["Session"], add = add, after_time = after_time)

		# Define a shortcut to the after writing date dictionary
		after = self.writing["Session"]["After"]

		# Show the after writing time (after writing the chapter)
		print()
		print(self.Date.language_texts["after_time"] + ":")
		print("\t" + after["Timezone"]["DateTime"]["Formats"]["HH:MM DD/MM/YYYY"])

		# ---------- #

		# If the "Pause" key is present inside the "Session" dictionary
		if "Pause" in self.writing["Session"]:
			# Define the text to show as the "Duration of the pause" in the user language
			text = self.Language.language_texts["duration_of_the_pause"]

			# Add the " (the pause duration which is subtracted from the total [writing] duration)" text to the text to show
			text += " (" + self.language_texts["the_pause_duration_which_is_subtracted_from_the_total_{}_duration"]

			# Format the text with the item of the writing mode
			text = text.format(self.writing["Writing mode"]["Language texts"]["Item"]) + ")"

			# Show the text
			print()
			print(text + ":")

			# Define a shortcut to the pause duration dictionary
			pause_duration = self.writing["Session"]["Pause"]["Duration"]

			# Show the writing duration text in the user language (with the pause duration subtracted)
			print("\t" + pause_duration["Text"][self.language["Small"]])

		# ---------- #

		# Define the text to show as the "Duration of writing" text
		text = self.Language.language_texts["duration_of"] + " " + self.writing["Writing mode"]["Language texts"]["Item"]

		# Add the text addon if it is not empty
		if text_addon != "":
			text += text_addon

		# Add the colon
		text += ":"

		# Show the "Duration of writing" text in the user language
		print()
		print(text)

		# Define a shortcut to the writing duration dictionary
		writing_duration = self.writing["Session"]["Duration"]

		# Show the writing duration text in the user language (with the pause duration subtracted)
		print("\t" + writing_duration["Text"][self.language["Small"]])

		# ---------- #

		# If the user has just started writing this chapter
		if self.states["Ongoing writing session"] == False:
			# Define the "Started" (writing) time as the "Before" time
			self.writing["Writing"]["Times"]["Started"] = self.writing["Session"]["Before"]

		# Define a shortcut to the after writing time in the user timezone
		after_writing_time = self.writing["Session"]["After"]["Timezone"]["DateTime"]["Formats"]["HH:MM DD/MM/YYYY"]

		# Add the "After" (writing) time string to the "Durations" list
		self.writing["Writing"]["Durations"]["List"].append(after_writing_time)

		# Define a shortcut to the "Duration" dictionary
		duration = self.writing["Session"]["Duration"]

		# Define a shortcut to the time units dictionary
		time_units = duration["Difference"]

		# Define a local duration dictionary
		duration = {
			"Units": time_units, # Define the difference dictionary as the time units dictionary
			"Text": duration["Text"] # Add the duration text
		}

		# Add the duration dictionary to the "Durations" dictionary with the "After" (writing) time string as a key
		self.writing["Writing"]["Durations"]["Dictionary"][after_writing_time] = duration

		# Calculate and update the writing duration
		self.Update_Writing_Duration()

		# ---------- #

		# Make a backup of the duration
		self.Make_Backup_Of_Duration("Create", "Duration")

		# ---------- #

		# If the "Ongoing writing session" state is True (the user resumed writing the chapter)
		if self.states["Ongoing writing session"] == True:
			# Define a shortcut to the total writing duration dictionary
			total_duration = self.writing["Writing"]["Total duration"]

			# Show the total writing time text in the user language
			print()
			print(self.Language.language_texts["total_duration_of"] + " " + self.writing["Writing mode"]["Language texts"]["Item"] + ":")
			print("\t" + total_duration["Text"][self.language["Small"]])

		# ---------- #

		# Define the text asking if the user finished writing the whole chapter, not just a part of it
		type_text = self.language_texts["did_you_finished_{}_the_whole_chapter"]

		# Format the text with the infinitive action of the writing mode
		type_text = type_text.format(self.writing["Writing mode"]["Language texts"]["Infinitive action"])

		# If the writing session has not been postponed
		if self.states["Postpone writing session"] == False:
			# Ask if the user finished writing the whole chapter
			self.states["Finished writing"] = self.Input.Yes_Or_No(type_text)

		# Close the server
		self.Manage_Server(close = True, show_text = False)

		# ---------- #

		# If the user finished writing the whole chapter
		if self.states["Finished writing"] == True:
			# Update the "Finished" time key to be the after writing time
			self.writing["Writing"]["Times"]["Finished"] = after_writing_time

			# Get the after writing time in the UTC timezone and format
			utc_time = self.writing["Session"]["After"]["UTC"]["DateTime"]["Formats"]["YYYY-MM-DDTHH:MM:SSZ"]

			# Update the "Finished (UTC)" time key to be the after writing time in the UTC timezone
			self.writing["Writing"]["Times"]["Finished (UTC)"] = utc_time

			# Run the "Finish_Writing" method
			self.Finish_Writing()

		# ---------- #

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

		# Delete the backup file
		self.Make_Backup_Of_Duration("Delete")

	def Pause_Writing(self):
		# Define a shortcut to the text to ask if the user wants to pause the writing session
		input_text = self.language_texts["do_you_want_to_pause_the_{}_session"]

		# Format the text with the item of the writing mode
		input_text = input_text.format(self.writing["Writing mode"]["Language texts"]["Item"])

		# Ask if the user wants to pause the writing session
		self.states["Pause writing session"] = self.Input.Yes_Or_No(input_text)

		# If the user wants to pause it
		if self.states["Pause writing session"] == True:
			# Show a five dash space separator
			print()
			print(self.separators["5"])

			# ----- #

			# Define a shortcut to the before writing date dictionary
			before = self.writing["Session"]["Before"]

			# Show the before writing time (when the user started writing the chapter)
			print()
			print(self.Date.language_texts["before_time"] + ":")
			print("\t" + before["Timezone"]["DateTime"]["Formats"]["HH:MM DD/MM/YYYY"])

			# Calculate and define the writing duration
			self.writing["Session"]["Duration"] = self.Calculate_Duration(self.writing["Session"])

			# ----- #

			# Define the after writing time text
			after_time_text = self.language_texts["time_after_{}_for_a_while"]

			# Format the text with the infinitive action of the writing mode
			after_time_text = after_time_text.format(self.writing["Writing mode"]["Language texts"]["Infinitive action"])

			# Define a shortcut to the after writing date dictionary
			after = self.writing["Session"]["After"]

			# If the "Testing" switch is True
			if self.switches["Testing"] == True:
				# Define the after shortcut as the "After" time inside the "Duration" dictionary
				after = self.writing["Session"]["Duration"]["After"]

			# Show the after writing time (after writing the chapter for a while)
			print()
			print(after_time_text + ":")
			print("\t" + after["Timezone"]["DateTime"]["Formats"]["HH:MM DD/MM/YYYY"])

			# Show the writing duration in the user language
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
				# Define the "Already paused" state as True
				self.states["Already paused"] = True

			# ---------- #

			# Define a shortcut to the text to ask the user to press Enter to unpause the writing session
			input_text = self.language_texts["press_enter_to_unpause_the_{}_session"]

			# Format the text with the item of the writing mode
			input_text = input_text.format(self.writing["Writing mode"]["Language texts"]["Item"])

			# Ask the user to press Enter to unpause the writing session
			self.Input.Type(input_text)

			# ---------- #

			# Show a five dash space separator
			print()
			print(self.separators["5"])

			# If the user did not pause the writing session
			if self.states["Already paused"] == False:
				# Calculate and define the pause duration
				self.writing["Session"]["Pause"]["Duration"] = self.Calculate_Duration(self.writing["Session"]["Pause"])

			# Define the after pausing time text
			after_time_text = self.language_texts["time_after_the_pause"]

			# Define a shortcut to the after pausing date dictionary
			after = self.writing["Session"]["Pause"]["After"]

			# Show the after pausing time (after pausing and waiting for a while)
			print()
			print(after_time_text + ":")
			print("\t" + after["Timezone"]["DateTime"]["Formats"]["HH:MM DD/MM/YYYY"])

			# ---------- #

			# If the user already paused the writing session
			if self.states["Already paused"] == True:
				# If the "Testing" switch is False
				if self.switches["Testing"] == False:
					# Define the after pausing time (now)
					after_time = self.Date.Now()

				# If the "Testing" switch is True
				if self.switches["Testing"] == True:
					# Define the relative delta with the time to add as 15 minutes
					relative_delta = self.Date.Relativedelta(minutes = 15)

					# Add 15 minutes to the local after time
					# (The second pause adds 15 pause minutes)
					after_time = self.Date.Now(self.writing["Session"]["Pause"]["After"]["Object"] + relative_delta)

				# Get the difference between the before pausing time and the after pausing time
				difference = self.Date.Difference(self.writing["Session"]["Pause"]["After"], after_time)

				# Define the local add dictionary
				add = {}

				# Add the time units inside the pause "Difference" dictionary to the local add dictionary
				for key, value in difference["Difference"].items():
					add[key.lower()] = value

				# Define the relative delta method with the time to add
				relative_delta = self.Date.Relativedelta(**add)

				# Add the add time to the after pausing time
				self.writing["Session"]["Pause"]["After"] = self.Date.Now(self.writing["Session"]["Pause"]["After"]["Object"] + relative_delta)

			# ---------- #

			# Define the pause duration difference between the before and after pausing times
			self.writing["Session"]["Pause"]["Duration"] = self.Date.Difference(self.writing["Session"]["Pause"]["Before"], self.writing["Session"]["Pause"]["After"])

			# Define the time to be subtracted from the pausing time
			self.writing["Session"]["Pause"]["Subtract"] = self.writing["Session"]["Pause"]["Duration"]["Difference"]

			# ---------- #

			# Define the local subtract dictionary
			subtract = {}

			# Add the time units inside the pause "Subtract" dictionary to the local subtract dictionary
			for key, value in self.writing["Session"]["Pause"]["Subtract"].items():
				subtract[key.lower()] = value

			# Define the relative delta method with the time to subtract
			relative_delta = self.Date.Relativedelta(**subtract)

			# Define the local after time as the copy of the after writing time with the pause subtract time subtracted
			after_time = self.Date.Now(self.writing["Session"]["After (copy)"]["Object"] - relative_delta)

			# Define the time difference between the before writing time and the local after time
			difference = self.Date.Difference(self.writing["Session"]["Before"], after_time)

			# Define the text to show as the "Duration of writing" text
			text = self.Language.language_texts["duration_of"] + " " + self.writing["Writing mode"]["Language texts"]["Item"]

			# If the "Pause" key is present inside the "Session" dictionary
			if "Pause" in self.writing["Session"]:
				# Add the text about the writing time with the pause time subtracted
				text += " (" + self.language_texts["with_the_pause_duration_subtracted"] + ")"

			# Add the colon
			text += ":"

			# Show the writing duration in the user language (subtracting the pause time)
			print()
			print(text)
			print("\t" + difference["Text (with time units)"][self.language["Small"]])

			# If the "Testing" switch is True
			if self.switches["Testing"] == True:
				# Define the after writing time text
				after_time_text = self.language_texts["time_after_{}_for_a_while"]

				# Format the text with the infinitive action of the writing mode
				after_time_text = after_time_text.format(self.writing["Writing mode"]["Language texts"]["Infinitive action"])

				# Add the " (testing mode)" text to the after time text
				after_time_text += " (" + self.Language.language_texts["testing_mode"] + ")"

				# Define the after shortcut as the "After" time inside the "Duration" dictionary
				after = difference["After"]

				# Show the after writing time (after writing the chapter for a while)
				print()
				print(after_time_text + ":")
				print("\t" + after["Timezone"]["DateTime"]["Formats"]["HH:MM DD/MM/YYYY"])

			# ---------- #

			# Define the text to show as the "Duration of the pause" in the user language
			text = self.Language.language_texts["duration_of_the_pause"]

			# Add the " (the pause duration which is subtracted from the total [writing] duration)" text to the text to show
			text += " (" + self.language_texts["the_pause_duration_which_is_subtracted_from_the_total_{}_duration"]

			# Format the text with the infinitive action of the writing mode
			text = text.format(self.writing["Writing mode"]["Language texts"]["Item"]) + ")"

			# Show the text
			print()
			print(text + ":")

			# Define a shortcut to the pause duration dictionary
			pause_duration = self.writing["Session"]["Pause"]["Duration"]

			# Show the writing duration text in the user language (with the pause duration subtracted)
			print("\t" + pause_duration["Text"][self.language["Small"]])

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
			# Define the time to add as 1 hour, 30 minutes, and 10 seconds
			time = {
				"hours": 1,
				"minutes": 30,
				"seconds": 10
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

				# If the "After (copy)" key is inside the dictionary
				if "After (copy)" in dictionary:
					# Update the copy of the after time
					dictionary["After (copy)"] = after_time

				# If the "Is pause" key is in the dictionary
				if "Is pause" in dictionary:
					# Update the root after time with the local after time
					dictionary["After"] = after_time

		# Get the time difference between the before and the after times
		difference = self.Date.Difference(dictionary["Before"], after_time)

		# Return the difference dictionary
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
		self.Update_Writing_Duration(purge = True)

	def Update_Chapter(self):
		# If the writing mode is "Revise"
		if self.writing_mode == "Revise":
			# Ask if the user wants to update the chapter titles
			input_text = self.language_texts["do_you_want_to_update_the_chapter_titles"]

			self.states["Update chapter titles"] = self.Input.Yes_Or_No(input_text)

			# If the "Update chapter titles" state is True
			if self.states["Update chapter titles"] == True:
				# Add the previous chapter titles to the previous titles "Normal" dictionary
				self.chapter["Previous titles"]["Normal"] = deepcopy(self.chapter["Titles"]["Normal"])

				# Add the previous chapter titles with number to the previous titles "With number" dictionary
				self.chapter["Previous titles"]["With number"] = deepcopy(self.chapter["Titles"]["With number"])

		# ---------- #

		# Show a five dash space separator
		print()
		print(self.separators["5"])

		# Iterate through the language keys and dictionaries
		for small_language, language in self.languages["Dictionary"].items():
			# Define a shortcut to the full language
			full_language = language["Full"]

			# Get the current language translated to the user language
			translated_language = language["Translated"][self.language["Small"]]

			# Get the " in [language]" text of the current translated language
			in_language_text = " " + self.Language.texts["in_[language]"][small_language][self.language["Small"]]

			# Define the type text to ask for the new chapter title in the current language
			type_text = self.language_texts["type_the_new_chapter_title"] + in_language_text

			# Define the default chapter title variable as an empty string
			chapter_title = ""

			# ---------- #

			# If the writing mode is "Revise"
			# And the "Update chapter titles" state is True
			if (
				self.writing_mode == "Revise" and
				self.states["Update chapter titles"] == True
			):
				# Show the previous chapter title with number and the " in [language]" text
				print()
				print(self.language_texts["previous_title"] + in_language_text + ":")
				print(self.chapter["Previous titles"]["With number"][small_language])

			# ---------- #

			# If the writing mode is "Write"
			# Or the writing mode is "Revise"
			# And the "Update chapter titles" state is True
			if (
				self.writing_mode == "Write" or
				self.writing_mode == "Revise" and
				self.states["Update chapter titles"] == True
			):
				# If the "Testing" switch is False
				if self.switches["Testing"] == False:
					# Ask for the chapter title in the current language
					chapter_title = self.Input.Type(type_text, next_line = True)

				# If the "Testing" switch is True
				if self.switches["Testing"] == True:
					# Define the chapter title as "A New Chapter" in the current language
					chapter_title = self.texts["a_new_chapter"][small_language].title()

					# Show the type text and the defined chapter title
					print()
					print(type_text + ":")
					print(chapter_title)

			# ---------- #

			# If the chapter title is not empty
			if chapter_title != "":
				# Add or update the chapter title inside the chapter titles "Normal" dictionary in the current language
				self.chapter["Titles"]["Normal"][small_language] = chapter_title

				# Add or update the chapter title inside the chapter titles "With number" dictionary in the current language
				self.chapter["Titles"]["With number"][small_language] = self.chapter["Numbers"]["Leading zeroes"] + " - " + chapter_title

				# Define a shortcut to the titles file for easier typing
				titles_file = self.story["Folders"]["Chapters"][full_language]["Titles"]["Titles"]

				# Define the default write mode as "append"
				write_mode = "a"

				# If the writing mode is "Write"
				if self.writing_mode == "Write":
					# Define the text as the chapter title
					text_to_write = chapter_title

					# Add the chapter title to the "Titles" dictionary and the language list
					self.story["Chapters"]["Lists"]["Titles"][small_language].append(chapter_title)

				# If the writing mode is "Revise"
				# And the "Update chapter titles" state is True
				if (
					self.writing_mode == "Revise" and
					self.states["Update chapter titles"] == True
				):
					# Get the list of chapter titles
					chapter_titles = self.File.Contents(titles_file)["Lines"]

					# Define a shortcut to the chapter number less one
					chapter_number = self.chapter["Number"] - 1

					# Update the line of the current chapter
					chapter_titles[chapter_number] = chapter_title

					# Update the list of chapter titles in the current language to be the local updated list
					self.story["Chapters"]["Lists"]["Titles"][small_language] = chapter_titles

					# Define the text to be written
					text_to_write = self.Text.From_List(chapter_titles, next_line = True)

					# Change the write mode to "write"
					write_mode = "w"

				# If the writing mode is "Write"
				# Or the writing mode is "Revise"
				# And the "Update chapter titles" state is True
				if (
					self.writing_mode == "Write" or
					self.writing_mode == "Revise" and
					self.states["Update chapter titles"] == True
				):
					# Edit the language chapter titles file with the defined text to write and the write mode
					self.File.Edit(titles_file, text_to_write, write_mode)

			# ---------- #

			# Rename or create the chapter file

			# Define the source file
			source_file = self.chapter["Files"][small_language]

			# Define the destination folder
			destination_folder = self.story["Folders"]["Chapters"][full_language]["root"]

			# Sanitize the chapter title with number
			sanitized_chapter_title = self.Sanitize(self.chapter["Titles"]["With number"][small_language], restricted_characters = True)

			# Define the destination file
			destination_file = destination_folder + sanitized_chapter_title + ".txt"

			# If the writing mode is "Write"
			# And the current language is the user language
			# Or the writing mode is "Revise"
			# And the "Update chapter titles" state is True
			if (
				self.writing_mode == "Write" and
				small_language == self.language["Small"] or
				self.writing_mode == "Revise" and
				self.states["Update chapter titles"] == True
			):
				# Rename the chapter file
				self.File.Move(source_file, destination_file)

			# If the writing mode is "Write"
			# And the current language is not the user language
			if (
				self.writing_mode == "Write" and
				small_language != self.language["Small"]
			):
				# Create the file
				self.File.Create(destination_file)

			# Update the file inside the chapter "Files" dictionary
			self.chapter["Files"][small_language] = destination_file

		# ---------- #

		# If the writing mode is "Write"
		if self.writing_mode == "Write":
			# Add the finished writing time to the "Writing dates.txt" file

			# Define a shortcut to the "Writing dates.txt" file
			writing_dates_file = self.story["Folders"]["Chapters"]["Writing dates"]

			# Define a shortcut to the finished writing time
			finished_writing_time = self.writing["Writing"]["Times"]["Finished"]

			# Edit the "Writing dates.txt" to add the finished writing time
			self.File.Edit(writing_dates_file, finished_writing_time, "a")

	def Update_Chapter_Dictionary(self):
		# Define a shortcut to the started writing time
		started_writing_time = self.writing["Writing"]["Times"]["Started"]

		# Define a shortcut to the finished writing time
		finished_writing_time = self.writing["Writing"]["Times"]["Finished"]

		# Copy the root default "Chapter" dictionary
		chapter = deepcopy(self.stories["Chapter"])

		# Update the chapter number inside the local chapter dictionary with the root chapter number
		chapter["Number"] = int(self.chapter["Number"])

		# Update the "Titles" key
		chapter["Titles"] = self.chapter["Titles"]["Normal"]

		# Get the root chapter dictionary
		root_chapter = self.chapter["Dictionary"]

		# If the "Posting" dictionary of the root chapter dictionary is not the same as the local one
		if chapter["Posting"] != root_chapter["Posting"]:
			# Import the one from the root chapter dictionary
			chapter["Posting"] = root_chapter["Posting"]

		# ---------- #

		# Get the "chapter dictionary" key for current writing mode
		# [Revisions/Translations]
		chapter_dictionary_key = self.writing["Writing mode"]["Texts"]["Chapter dictionary"]

		# Define a shortcut to the total writing duration dictionary
		total_duration = self.writing["Writing"]["Total duration"]

		# ---------- #

		# If the writing mode is "Write"
		# And the root "Writing" dictionary is empty
		if (
			self.writing_mode == "Write" and
			root_chapter["Writing"]["Titles"] == {}
		):
			# Define the chapter titles inside the writing "Titles" dictionary
			chapter["Writing"]["Titles"] = self.chapter["Titles"]["Normal"]

			# Define the "Writing language" dictionary as the same dictionary inside the root "Chapter" dictionary
			chapter["Writing"]["Writing language"] = self.chapter["Writing language"]

			# Define the chapter "Times" dictionary
			chapter["Writing"]["Times"] = {
				**self.writing["Writing"]["Times"], # Import the keys and values from the writing "Times" dictionary
				"Duration": {
					**total_duration["Units"], # Import the keys from the total duration "Units" dictionary
					"Text": total_duration["Text"] # Add the duration text
				}
			}

			# Add the chapter number to the root chapters "List"
			self.story["Chapters"]["List"].append(str(chapter["Number"]))

			# Update the number of chapters
			self.story["Chapters"]["Numbers"]["Total"] = len(self.story["Chapters"]["List"])

		# ---------- #

		# If the writing mode is either "Revise" or "Translate"
		if self.writing_mode in ["Revise", "Translate"]:
			# Import the "Writing" dictionary from the root chapter dictionary
			chapter["Writing"] = root_chapter["Writing"]

			# If the root writings dictionary is not empty
			if root_chapter[chapter_dictionary_key]["List"] != []:
				# Update the local dictionary with the root one
				chapter[chapter_dictionary_key] = root_chapter[chapter_dictionary_key]

			# Get the writings dictionary for the writing mode
			writings_dictionary = chapter[chapter_dictionary_key]

			# Add the finished writing time to the "List" of the writings dictionary
			writings_dictionary["List"].append(finished_writing_time)

			# Define a local writing (singular) dictionary
			writing_dictionary = {}

			# ---------- #

			# If the writing mode is "Revise"
			if self.writing_mode == "Revise":
				# If the local writings dictionary is empty (this is the first [revision/translation] of this chapter)
				if writings_dictionary["List"] == []:
					# If the local "Titles" dictionary is not the same as the root one
					if chapter["Titles"] != root_chapter["Titles"]:
						# Add the "Titles" dictionary to the local writing (singular) dictionary
						writing_dictionary["Titles"] = chapter["Titles"]["Normal"]

					# Define the "Writing language" dictionary as the same dictionary inside the root "Chapter" dictionary
					writing_dictionary["Writing language"] = self.chapter["Writing language"]

				# If the local writings dictionary is not empty (this is not the first [revision/translation] of this chapter)
				if writings_dictionary["List"] != []:
					# Define the last titles and last languages as the ones inside the root "Writing" dictionary
					last_titles = chapter["Writing"]["Titles"]
					last_language = chapter["Writing"]["Writing language"]

					# Iterate through the writing dictionaries inside the writings dictionary
					for writing in writings_dictionary["Dictionary"].values():
						# If the "Titles" key is inside the writing dictionary
						if "Titles" in writing:
							# Define the titles of the current writing dictonary as the local last titles variable
							last_titles = writing["Titles"]

						# If the "Writing language" key is inside the writing dictionary
						if "Writing language" in writing:
							# Define the writing language of the current writing dictonary as the local last language variable
							last_language = writing["Writing language"]

					# If the chapter "Titles" dictionary is not the same as the last titles dictionary found
					if chapter["Titles"] != last_titles:
						# Add the "Titles" dictionary to the local writing (singular) dictionary
						writing_dictionary["Titles"] = chapter["Titles"]

						# Add the "Previous titles" (last titles) dictionary to the local writing (singular) dictionary
						writing_dictionary["Previous titles"] = last_titles

					# If the root chapter "Writing language" dictionary is not the same as the last language dictionary found
					if self.chapter["Writing language"] != last_language:
						# Add the "Writing language" dictionary to the local writing (singular) dictionary
						writing_dictionary["Writing language"] = self.chapter["Writing language"]

			# ---------- #

			# If the writing mode is "Translate"
			if self.writing_mode == "Translate":
				# Define the "Origin language" dictionary as the same dictionary inside the root "Chapter" dictionary
				writing_dictionary["Origin language"] = self.chapter["Origin language"]

				# Define the "Destiny language" dictionary as the same dictionary inside the root "Chapter" dictionary
				writing_dictionary["Destiny language"] = self.chapter["Destiny language"]

			# Define the chapter "Times" dictionary
			writing_dictionary["Times"] = {
				**self.writing["Writing"]["Times"], # Import the keys and values from the writing "Times" dictionary
				"Duration": {
					**total_duration["Units"], # Import the keys from the total duration "Units" dictionary
					"Text": total_duration["Text"] # Add the duration text
				}
			}

			# Add the writing dictionary to the writings "Dictionary"
			writings_dictionary["Dictionary"][finished_writing_time] = writing_dictionary

		# ---------- #

		# Update the root chapter dictionary inside the root "Chapters" dictionary
		self.story["Chapters"]["Dictionary"][str(chapter["Number"])] = chapter

		# Update the "Dictionary" inside the root chapter dictionary
		self.chapter["Dictionary"] = chapter

		# ---------- #

		# Check and update the chapter date texts inside the chapter files
		self.Check_Chapter_Date_Texts()

		# ---------- #

		# Make a copy of the "Chapters" dictionary
		chapters_copy = deepcopy(self.story["Information"]["Chapters"])

		# Copy the local chapter dictionary
		chapter_copy = deepcopy(chapter)

		# ----- #

		# Define a local times dictionary
		times = {
			"Started": started_writing_time,
			"Finished": finished_writing_time
		}

		# Iterate through the times inside the times dictionary
		for key, time in deepcopy(times).items():
			# Make a copy of the original writing time
			time = deepcopy(time)

			# If the key is "Finished"
			if key == "Finished":
				# If the time is a string
				if isinstance(time, str) == True:
					# Convert it into a date dictionary
					date = self.Date.From_String(time, "%H:%M %d/%m/%Y")

				# Get the UTC formats
				utc_formats = date["UTC"]["DateTime"]["Formats"]

				# Add the "Finished (UTC)" key as the UTC timezone time format to the times dictionary
				times["Finished (UTC)"] = utc_formats["YYYY-MM-DDTHH:MM:SSZ"]

			# If the "Timezone" key is inside the time dictionary
			if "Timezone" in time:
				# Get the timezone formats
				formats = time["Timezone"]["DateTime"]["Formats"]

				# Define the time as the user timezone time format
				time = formats["HH:MM DD/MM/YYYY"]

			# Update the key inside the times dictionary
			times[key] = time

		# ---------- #

		# If the writing mode is "Write"
		if self.writing_mode == "Write":
			# Update the writing "Started" time key
			chapter_copy["Writing"]["Times"]["Started"] = times["Started"]

			# ----- #

			# Update the writing "Finished" time key
			chapter_copy["Writing"]["Times"]["Finished"] = times["Finished"]

			# Update the writing "Finished (UTC)" time key
			chapter_copy["Writing"]["Times"]["Finished (UTC)"] = times["Finished (UTC)"]

		# If the writing mode is either "Revise" or "Translate"
		if self.writing_mode in ["Revise", "Translate"]:
			# Update the writing "Started" time key
			writing_dictionary["Times"]["Started"] = times["Started"]

			# ----- #

			# Update the writing "Finished" time key
			writing_dictionary["Times"]["Finished"] = times["Finished"]

			# Update the writing "Finished (UTC)" time key
			writing_dictionary["Times"]["Finished (UTC)"] = times["Finished (UTC)"]

			# ----- #

			# Update the writing dictionary inside the root dictionary
			chapter_copy[chapter_dictionary_key]["Dictionary"][times["Finished"]] = writing_dictionary

		# Update the chapter dictionary inside the copy of the "Chapters" dictionary
		chapters_copy["Dictionary"][str(chapter["Number"])] = chapter_copy

		# ----- #

		# If the "Testing" switch is True
		if self.switches["Testing"] == True:
			# Show the "Chapters" text
			print()
			print("Chapters:")
			print()

			# Show the local "Chapters" dictionary
			self.JSON.Show(chapters_copy)

		# Update the "Chapters.json" file with the updated "Chapters" dictionary
		self.JSON.Edit(self.story["Folders"]["Information"]["Chapters"], chapters_copy)

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

	def Update_Writing_Duration(self, purge = False):
		# If the "purge" parameter is False
		if purge == False:
			# Define a shortcut to the started writing time
			started_writing_time = self.writing["Writing"]["Times"]["Started"]

			# If the "Started" writing time is a string
			if type(started_writing_time) == str:
				# Convert it into a date dictionary
				started_writing_time = self.Date.From_String(started_writing_time, "%H:%M %d/%m/%Y")

			# Define the added time variable as an empty dictionary
			added_time = {}

			# ---------- #

			# If the "Total duration" dictionary is not empty
			if self.writing["Writing"]["Total duration"] != {}:
				# Define a shortcut to the total writing duration dictionary
				total_duration = self.writing["Writing"]["Total duration"]

				# Define the local add dictionary
				add = {}

				# Add the time units inside the total duration "Units" dictionary to the local add dictionary
				for key, value in total_duration["Units"].items():
					add[key.lower()] = value

				# Define the relative delta method with the time to add
				relative_delta = self.Date.Relativedelta(**add)

				# Make a copy of the date dictionary
				added_time = deepcopy(started_writing_time)

				# Add the relative delta to the started writing time object to create the added time
				added_time = self.Date.Now(started_writing_time["Object"] + relative_delta)

			# ---------- #

			# Get the list of writing durations
			durations = list(self.writing["Writing"]["Durations"]["Dictionary"].values())

			# Get the last duration
			last_duration = durations[-1]

			# Define the local add dictionary
			add = {}

			# Add the time units inside the last duration "Units" dictionary to the local add dictionary
			for key, value in last_duration["Units"].items():
				add[key.lower()] = value

			# Define the relative delta method with the time to add
			relative_delta = self.Date.Relativedelta(**add)

			# Define the time to add as the started writing time
			time_to_add = deepcopy(started_writing_time)

			# If the added time is not an empty dictionary
			if added_time != {}:
				# Define the time to add as the already defined added time
				time_to_add = added_time

			# Add the relative delta to the time to add object to create the added time
			added_time = self.Date.Now(time_to_add["Object"] + relative_delta)

			# Get the difference between the started writing time and the added time
			difference = self.Date.Difference(started_writing_time, added_time)

			# Define a shortcut to the time units dictionary
			time_units = difference["Difference"]

			# Define the "Total duration" dictionary with the time unit and duration text
			self.writing["Writing"]["Total duration"] = {
				"Units": time_units, # Import the time units dictionary into the "Units"
				"Text": difference["Text"], # Add the duration text
				"Text (with time units)": difference["Text (with time units)"] # Add the duration text with time units
			}

		# ---------- #

		# If the "purge" parameter is True
		if purge == True:
			# Define a shortcut to the "Status" dictionary
			status = self.writing["Writing"]["Status"]

			# If the "Finished" status key is False, change it to True
			if status["Finished"] == False:
				status["Finished"] = True

		# ---------- #

		# Make a copy of the "Writing" dictionary
		writing_copy = deepcopy(self.story["Information"]["Writing"])

		# Define a shortcut to the started writing time
		started_writing_time = writing_copy[self.writing_mode]["Times"]["Started"]

		# If the "Timezone" key is inside the started writing time variable
		if "Timezone" in started_writing_time:
			# Get the timezone datetime dictionary
			started_writing_time = started_writing_time["Timezone"]["DateTime"]

			# Get the correct time format
			started_writing_time = started_writing_time["Formats"]["HH:MM DD/MM/YYYY"]

			# Update the writing "Started" time key
			writing_copy[self.writing_mode]["Times"]["Started"] = started_writing_time

		# Iterate through the writing modes and writing mode dictionaries
		for writing_mode, writing_mode_dictionary in self.stories["Writing modes"]["Dictionary"].items():
			# If the writing mode is not the selected one
			if writing_mode != self.writing_mode:
				# Then redefine its dictionary to the backup version of it
				writing_copy[writing_mode] = self.story["Writing (backup)"][writing_mode]

		# If the root writing mode is "Revise"
		# And the user finished writing the whole chapter
		# And the "Select a chapter to revise" state is True (the user selected a chapter to revise)
		if (
			self.writing_mode == "Revise" and
			self.states["Finished writing"] == True and
			self.states["Select a chapter to revise"] == True
		):
			# Get the "Translate" writing mode dictionary
			translate = writing_copy["Translate"]

			# If its "Finished" status is True
			if translate["Status"]["Finished"] == True:
				# Change the current chapter to be translated to the chapter that has been revised
				translate["Current chapter"] = self.chapter["Number"]

				# Change its "Finished" status to False
				translate["Status"]["Finished"] = False

		# If the "Testing" switch is True
		if self.switches["Testing"] == True:
			# Show the "Writing" text
			print()
			print("Writing:")
			print()

			# Show the local "Writing" dictionary
			self.JSON.Show(writing_copy)

			# Copy it
			self.JSON.Copy(writing_copy)

		# Update the "Writing.json" file
		self.JSON.Edit(self.story["Folders"]["Information"]["Writing"], writing_copy)

	def Create_Task_Title(self, dictionary):
		# Get the small language from the dictionary
		small_language = dictionary["Small language"]

		# Define the list of items to use to format the template
		dictionary["Items"] = [
			# Define the index of the writing mode text
			"",

			# The chapter number name in the local language, examples: [one/two/three/thirty three]
			self.chapter["Numbers"]["Names"][small_language],

			# The story title in the local language, example: Story title
			self.story["Titles"][small_language]
		]

		# ---------- #

		# Define the writing mode text as the "Infinitive action" one by default
		# Examples: [writing/revising/translating]
		writing_mode_text = "Infinitive action"

		# If the "Ongoing writing session" state is True (the user resumed writing the chapter)
		# And is not the last writing session (the user did not finished writing the whole chapter)
		if (
			self.states["Ongoing writing session"] == True and
			self.states["Finished writing"] == False
		):
			# Update the writing mode text to be the "Action" one
			# Examples: [writing/revising/translating]
			# (The "Action" text is different from the "Infinitive action" text for non-English languages)
			writing_mode_text = "Action"

		# If the "Writing mode text" is inside the parameter dictionary
		if "Writing mode text" in dictionary:
			# Define it as the local writing mode text
			writing_mode_text = dictionary["Writing mode text"]

		# Update the writing mode text to be the local variable one
		dictionary["Items"][0] = self.writing["Writing mode"]["Texts"][writing_mode_text][small_language]

		# ---------- #

		# Get the text template in the current language
		text_template = dictionary["Text template"][small_language]

		# If the writing mode is "Translate"
		if self.writing_mode == "Translate":
			# Get the origin language translated to the local language
			origin_language = self.chapter["Origin language"]["Translated"][small_language]

			# Get the destiny language translated to the local language
			destiny_language = self.chapter["Destiny language"]["Translated"][small_language]

			# Define the translation template as the " from {} to {}" text in the current language
			translation_template = self.Language.texts["from_{}_to_{}"][small_language]

			# Format the translation template with the origin and the destiny languages
			# (The user language and the English language
			# The chapters are always translated from the user language to the English language
			# So the origin language is always the user language and the destiny language is always English)
			translation_text = translation_template.format(origin_language, destiny_language)

			# Add the translation text to the text template
			text_template += " " + translation_text

		# Format the text template with the list of items to create the task title
		task_title = text_template.format(*dictionary["Items"])

		# Return the task title
		return task_title

	def Register_Task(self, register_task = True):
		# Create the task dictionary to use in the "Tasks" class
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

		# ---------- #

		# Define an empty task title template
		task_title_template = ""

		# Define the text template to create the task title as the "I started [writing/revising/translating]" one
		text_template = self.texts["i_started_{}_the_chapter_{}_of_my_story_{}"]

		# If the "Ongoing writing session" state is True (the user resumed writing the chapter)
		# And is not the last writing session (the user did not finished writing the whole chapter)
		if (
			self.states["Ongoing writing session"] == True and
			self.states["Finished writing"] == False
		):
			# Define the text template to create the task title as the "I continued [writing/revising/translating]" one
			# (When the user resumed writing the chapter)
			text_template = self.texts["i_continued_{}_the_chapter_{}_of_my_story_{}_until_now"]

		# If the user finished writing the whole chapter
		if self.states["Finished writing"] == True:
			# Define the text template for the task as the "I finished writing", for the last time
			text_template = self.texts["i_finished_{}_the_chapter_{}_of_my_story_{}"]

			# Update the task title template for the task title
			task_title_template = self.texts["i_{}_the_chapter_{}_of_my_story_{}"]

		# ---------- #

		# Iterate through the language keys and dictionaries
		for small_language, language in self.languages["Dictionary"].items():
			# Get the user language translated to the current language
			translated_user_language = self.language["Translated"][small_language]

			# Create the dictionary for the "Create_Task_Title" method with the language and the text template
			dictionary = {
				"Small language": small_language,
				"Text template": text_template
			}

			# Create the task title using the method
			task_title = self.Create_Task_Title(dictionary)

			# Add the task title to the "Task" dictionary
			self.task_dictionary["Task"]["Titles"][small_language] = task_title

			# ---------- #

			# Create the task description, initially as the task title in the current language with a dot
			task_description = self.task_dictionary["Task"]["Titles"][small_language] + "."

			# Add two line breaks to the task description
			task_description += "\n\n"

			# ---------- #

			# Create a different task title for the task if the chapter has been finished

			# If the task title template is not empty
			if task_title_template != "":
				# Define the writing mode text as the "Done" one
				# Examples: I [wrote/revised/translated]
				writing_mode_text = "Done"

				# Create the dictionary for the "Create_Task_Title" method with the language, the text template, and the custom writing mode text
				dictionary = {
					"Small language": small_language,
					"Text template": task_title_template,
					"Writing mode text": writing_mode_text
				}

				# Create the task title and get it back
				task_title = self.Create_Task_Title(dictionary)

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
				# Add the "The chapter with the titles" text to the task description
				task_description += self.texts["the_chapter_with_the_titles"][small_language] + ":" + "\n"

				# List the chapter titles
				chapter_titles = list(self.chapter["Titles"]["Normal"].values())

				# Iterate through the list of chapter titles
				for chapter_title in chapter_titles:
					# Add the chapter title to the task description text
					task_description += chapter_title

					# If the chapter title is not the last one, add a line break
					if chapter_title != chapter_titles[-1]:
						task_description += "\n"

				# Add two line breaks to the task description
				task_description += "\n\n"

				# If the "Update chapter titles" state is True
				if self.states["Update chapter titles"] == True:
					# Add the "Previous chapter titles" text to the task description
					task_description += self.texts["previous_chapter_titles"][small_language] + ":" + "\n"

					# List the previous chapter titles
					previous_chapter_titles = list(self.chapter["Previous titles"]["Normal"].values())

					# Iterate through the list of previous chapter titles
					for previous_chapter_title in previous_chapter_titles:
						# Add the previous chapter title to the task description text
						task_description += previous_chapter_title

						# If the previous chapter title is not the last one, add a line break
						if previous_chapter_title != previous_chapter_titles[-1]:
							task_description += "\n"

					# Add two line breaks to the task description
					task_description += "\n\n"

			# ---------- #

			# Create the "I started [started time] and stopped at [stopped time]" text

			# Define an empty items list
			items = []

			# Iterate through the defined list of time keys
			for key in ["Before", "After"]:
				# Get the time
				time = self.writing["Session"][key]

				# Get the timezone datetime dictionary
				time = time["Timezone"]["DateTime"]

				# Get the correct time format
				time = time["Formats"]["HH:MM DD/MM/YYYY"]

				# Split it with a space and get the time (HH:MM, Hours and Minutes)
				time = time.split(" ")[0]

				# Add it to the list of items
				items.append(time)

			# Define the template as the "I started {} and stopped at {}" text in the current language
			template = self.texts["i_started_at_{}_and_stopped_at_{}"][small_language]

			# Format the template with the list of items
			# Example: "I started at 20:00 and stopped at 23:00"
			text = template.format(*items)

			# Add the formatted template to the task description text
			task_description += text

			# Add a dot and a line break to the task description
			task_description += "." + "\n"

			# ----- #

			# Create the "I [wrote] for [writing time], including pauses" text

			# Define the empty list of items
			items = []

			# Define the template as the "I [wrote] for [writing time], including pauses" text in the current language
			template = self.texts["i_{}_for_{}_including_pauses"][small_language]

			# Define a shortcut to the "Done" writing mode text
			# Examples: I [wrote/revised/translated]
			done_text = self.writing["Writing mode"]["Texts"]["Done"][small_language]

			# If the first two characters of the template text are a format string
			if template[0] + template[1] == "{}":
				# Capitalize the done text
				done_text = done_text.capitalize()

			# Add the done text to the list of items
			items.append(done_text)

			# ----- #

			# Define a shortcut to the session duration dictionary
			duration = self.writing["Session"]["Duration"]

			# Define the duration text in the current language as the writing duration text with time units
			# Example: "1 hour, 30 minutes, 32 seconds (01:30:32)"
			duration_text = duration["Text (with time units)"][small_language]

			# Add the writing duration text to the list of items
			items.append(duration_text)

			# Format the template with the list of items
			# Example: "I [wrote/revised/translated] for [writing time], including pauses"
			text = template.format(*items)

			# Add the formatted template to the task description text
			task_description += template.format(*items)

			# Add the end period to the task description
			task_description += "."

			# ---------- #

			# If the "Ongoing writing session" state is True (the user resumed writing the chapter)
			if self.states["Ongoing writing session"] == True:
				# Add a line break to the task description
				task_description += "\n"

				# Add the "Totalling " text in the current language to the task description
				task_description += self.Language.texts["totaling, title()"][small_language] + " "

				# Define a shortcut to the total writing duration dictionary
				total_duration = self.writing["Writing"]["Total duration"]

				# Define the total duration text in the current language as the total writing duration text with time units
				# Example: "2 hours, 32 minutes, 33 seconds (02:32:33)"
				total_duration_text = total_duration["Text (with time units)"][small_language]

				# Add the total duration text to the task description text
				task_description += total_duration_text

				# Get the list of durations
				durations = list(self.writing["Writing"]["Durations"]["Dictionary"].values())

				# Get the penultimate duration
				penultimate_duration = durations[-2]

				# If the list has at least two durations
				if len(durations) >= 2:
					# Add the "along with the previous duration" text in the current language to the task description
					task_description += " " + self.Language.texts["along_with_the_previous_duration"][small_language] + " "

					# Add its text to the task description text
					task_description += "(" + penultimate_duration["Text"][small_language] + ")"

				# Add the end period to the task description
				task_description += "."

			# ---------- #

			# Add the task description to the "Task" dictionary
			self.task_dictionary["Task"]["Descriptions"][small_language] = task_description

		# Register the task with the root "Register_Task" method
		Stories.Register_Task(self, self.task_dictionary, register_task = register_task)
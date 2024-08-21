# Write.py

from Stories.Stories import Stories as Stories

from copy import deepcopy

class Write(Stories):
	def __init__(self):
		super().__init__()

		# Define the root dictionary
		self.dictionary = {
			"Chapters": {
				"Numbers": {
					"Last posted chapter": 1
				},
				"Titles": {}
			},
			"Chapter": {},
			"Steps": {
				"List": [
					"Define writing modes",
					"Select writing mode",
					"Define chapter",
					"Define server",
					"Open story website",
					"Open writing pack",
					"Create Discord status",
					"Start writing"
				],
				"Dictionary": {}
			},
			"Writing modes": {},
			"Writing mode": {},
			"Writing": {},
			"Session": {}
		}

		# Define the "States" dictionary
		self.states = {
			"First time writing": False,
			"Pause writing session": False,
			"Already paused": False,
			"Postpone writing session": False,
			"Finished writing": False
		}

		# ---------- #

		# Define the steps of chapter writing
		self.Define_Steps()

		# Run the chapter writing steps
		self.Run_Steps()

		# Run the root class to update the files and dictionaries
		super().__init__()

	def Define_Steps(self):
		# Iterate through the list of chapter writing steps
		for key in self.dictionary["Steps"]["List"]:
			# Update the step dictionary
			self.dictionary["Steps"]["Dictionary"][key] = {
				"Key": key,
				"Method": getattr(self, key.title().replace(" ", "_"))
			}

	def Run_Steps(self):
		# Iterate through the step dictionaries inside the "Steps" dictionary
		for step in self.dictionary["Steps"]["Dictionary"].values():
			# Run the method of the chapter writing step
			step["Method"]()

	def Define_Writing_Modes(self):
		# Define the "Writing modes" dictionary
		self.dictionary["Writing modes"] = {
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
				"Chapter"
			]
		}

		# Iterate through the list of writing modes
		for key in self.dictionary["Writing modes"]["List"]:
			# Define the writing mode dictionary
			dictionary = {
				"Name": key,
				"Names": {},
				"Texts": {},
				"Language texts": {}
			}

			# Iterate through the list of small languages
			for language in self.languages["small"]:
				# Define the text key
				text_key = key.lower() + ", title()"

				# Define the text
				text = self.Language.texts[text_key][language]

				# Add it to the "Names" dictionary
				dictionary["Names"][language] = text

			# Get the text dictionary of the writing mode
			text_key = key.lower() + ", type: dictionary"

			texts = self.texts[text_key]

			# Iterate through the list of verb tenses
			for tense in self.dictionary["Writing modes"]["Verb tenses"]:
				# Get the verb tense text
				text = texts[tense]

				# Add it to the "Texts" dictionary
				dictionary["Texts"][tense] = text

				# Add the tense in the user language to the "Language texts" dictionary
				dictionary["Language texts"][tense] = text[self.user_language]

			# Add the local dictionary to the "Writing modes" dictionary
			self.dictionary["Writing modes"]["Dictionary"][key] = dictionary

	def Select_Writing_Mode(self):
		# Define the parameters dictionary to use inside the "Select" method of the "Input" utility module
		parameters = {
			"options": self.dictionary["Writing modes"]["List"],
			"language_options": [],
			"show_text": self.language_texts["writing_modes"],
			"select_text": self.language_texts["select_a_writing_mode"]
		}

		# Iterate through the dictionary of writing modes
		for writing_mode in self.dictionary["Writing modes"]["Dictionary"].values():
			# Add the infinitive text to the list of language options
			parameters["language_options"].append(writing_mode["Language texts"]["Infinitive"].title())

		# ---------- #

		# Define the total chapter number variable for easier typing
		total_chapter_number = self.story["Information"]["Chapters"]["Numbers"]["Total"]

		# Iterate through the list of writing modes
		i = 0
		for writing_mode in self.dictionary["Writing modes"]["List"]:
			# Get the chapter of the writing mode
			chapter = self.story["Information"]["Writing"][writing_mode]["Chapter"]

			# If the chapter of the writing mode is equal to the total chapter number
			# And the writing mode is not "Write"
			if (
				chapter == total_chapter_number and
				writing_mode != "Write"
			):
				# Then remove the writing mode from the list of options
				parameters["options"].remove(writing_mode)

			# Define the addon as the " the chapter [number name]" text
			addon = " " + self.Language.texts["genders, type: dict"][self.user_language]["masculine"]["the"] + " "

			# Add the "chapter " text
			addon += self.Language.language_texts["chapter, title()"].lower() + " "

			# If the user did not started writing the chapter in the current writing mode
			if self.story["Information"]["Writing"][writing_mode]["Times"]["Duration"]["Units"] == {}:
				# Add one to the local chapter number
				chapter += 1

			# Add the chapter number
			addon += str(chapter)

			# If the writing mode is "Write"
			if writing_mode == "Write":
				# Create the text to add as "a new chapter"
				text_to_add = " (" + self.language_texts["a_new_chapter"] + ")"

				# Add the text above to the addon variable
				addon += text_to_add

				# Add the addon to the writing mode dictionary
				self.dictionary["Writing modes"]["Dictionary"][writing_mode]["Addon"] = text_to_add

			# If the writing mode is either "Revise" or "Translate"
			# And the user already started writing the chapter
			if (
				writing_mode in ["Revise", "Translate"] and
				self.story["Information"]["Writing"][writing_mode]["Times"]["Duration"]["Units"] != {}
			):
				# Create the text to add as "in progress"
				text_to_add = " (" + self.Language.language_texts["in_progress"] + ")"

				# Add the text above to the addon variable
				addon += text_to_add

				# Add the addon to the writing mode dictionary
				self.dictionary["Writing modes"]["Dictionary"][writing_mode]["Addon"] = text_to_add

			# Update the language option of the writing mode to add the addon above
			parameters["language_options"][i] = parameters["language_options"][i] + addon

			i += 1

		# ---------- #

		# Ask the user to select the writing mode
		writing_mode = self.Input.Select(**parameters)["option"]

		# Get the writing mode dictionary
		self.dictionary["Writing mode"] = self.dictionary["Writing modes"]["Dictionary"][writing_mode]

		# Define the writing mode key
		self.writing_mode = writing_mode

	def Define_Chapter(self):
		# Define the chapter "Titles" key
		self.dictionary["Chapters"]["Titles"] = deepcopy(self.story["Information"]["Chapters"]["Titles"])

		# Update the last posted chapter number with the number inside the story "Information" dictionary
		self.dictionary["Chapters"]["Numbers"]["Last posted chapter"] = self.story["Information"]["Chapters"]["Numbers"]["Last posted chapter"]

		# ---------- #

		# Define a shortcut for the story "Writing" dictionary in the current writing mode
		self.dictionary["Writing"] = self.story["Information"]["Writing"][self.writing_mode]["Times"]

		# If the user did not started writing the chapter in the writing mode
		if self.dictionary["Writing"]["Duration"]["Units"] == {}:
			# Add one to the chapter of the writing mode
			self.story["Information"]["Writing"][self.writing_mode]["Chapter"] += 1

			# Define the "First time writing" as True
			self.states["First time writing"] = True

		# Update the "Writing.json" file with the updated "Writing" dictionary
		self.JSON.Edit(self.story["Folders"]["Information"]["Writing"], self.story["Information"]["Writing"])

		# ---------- #

		# Define the "Chapter" dictionary
		self.dictionary["Chapter"] = {
			"Number": 1,
			"Numbers": {
				"Leading zeroes": 1,
				"Names": {}
			},
			"Titles": {},
			"Titles (with leading zeroes)": {},
			"Language": {},
			"Discord": {},
			"Folders": {},
			"Files": {}
		}

		# Define the number
		self.dictionary["Chapter"]["Number"] = self.story["Information"]["Writing"][self.writing_mode]["Chapter"]

		# Define the number with leading zeroes
		self.dictionary["Chapter"]["Numbers"]["Leading zeroes"] = str(self.Text.Add_Leading_Zeroes(self.dictionary["Chapter"]["Number"]))

		# ---------- #

		# Define the titles variable for easier typing and more beautiful code
		titles = self.dictionary["Chapters"]["Titles"]

		# Iterate through the list of small languages
		for language in self.languages["small"]:
			# Define the chapter title as the chapter number with leading zeroes
			title = self.dictionary["Chapter"]["Numbers"]["Leading zeroes"]

			# If the writing mode is either "Revise" or "Translate"
			if self.writing_mode in ["Revise", "Translate"]:
				# Update the title of the chapter
				title = titles[language][self.dictionary["Chapter"]["Number"] - 1]

			# Define the full chapter title
			# [01 - Chapter Title]
			full_title = title

			# If the writing mode is either "Revise" or "Translate"
			if self.writing_mode in ["Revise", "Translate"]:
				# Define the full chapter title
				# [01 - Chapter Title]
				full_title = self.dictionary["Chapter"]["Numbers"]["Leading zeroes"] + " - " + title

			# Add the chapter title to the "Titles" dictionary
			self.dictionary["Chapter"]["Titles"][language] = title

			# Add the full title to the "Titles (with leading zeroes)" dictionary
			self.dictionary["Chapter"]["Titles (with leading zeroes)"][language] = full_title

			# Get the number name of the chapter number
			number_name = self.Date.texts["number_names, type: list"][language][int(self.dictionary["Chapter"]["Number"])]

			# Add it to the "Names" dictionary
			self.dictionary["Chapter"]["Numbers"]["Names"][language] = number_name

		# ---------- #

		# Define the root folder of the chapter
		self.dictionary["Chapter"]["Folders"] = self.story["Folders"]["Chapters"]

		# ---------- #

		# Iterate through the list of small languages
		for language in self.languages["small"]:
			# Get the full and translated languages
			full_language = self.languages["full"][language]
			translated_language = self.languages["full_translated"][language][self.user_language]

			# Define the chapter file
			self.dictionary["Chapter"]["Files"][language] = self.dictionary["Chapter"]["Folders"][full_language]["root"]

			# Add the chapter title
			self.dictionary["Chapter"]["Files"][language] += self.dictionary["Chapter"]["Titles (with leading zeroes)"][language] + ".txt"

			# If the writing mode is "Write"
			# And the current language is the user language
			# (The chapters are always written in the user language)
			if (
				self.writing_mode == "Write" and
				language == self.user_language
			):
				# Create the file
				self.File.Create(self.dictionary["Chapter"]["Files"][language])

			# If the writing mode is either "Write" or "Revise"
			# And the language is the same as the user language
			# (The chapters are always written or revised in the user language)
			if (
				self.writing_mode in ["Write", "Revise"] and
				language == self.user_language
			):
				# Define the source language of the chapter as the current small and full language
				self.dictionary["Chapter"]["Language"]["Source"] = {
					"Small": language,
					"Full": full_language,
					"Translated": translated_language
				}

		# If the writing mode is "Translate"
		if self.writing_mode == "Translate":
			# Define the source language of the chapter as the English language
			# (The chapters are always translated in the English language)
			self.dictionary["Chapter"]["Language"]["Source"] = {
				"Small": "en",
				"Full": self.languages["full"]["en"],
				"Translated": self.languages["full_translated"]["en"][self.user_language]
			}

			# If the writing session is the first one for the current chapter
			if self.states["First time writing"] == True:
				# Write the user language chapter text into the English file
				text = self.File.Contents(self.dictionary["Chapter"]["Files"][self.user_language])["string"]

				self.File.Edit(self.dictionary["Chapter"]["Files"]["en"], text, "w")

		# ---------- #

		# Define a shortcut for the "Chapter" dictionary
		self.chapter = self.dictionary["Chapter"]

		# ---------- #

		# Show a five dash space separator
		print()
		print(self.separators["5"])
		print()

		# Show the story title in the user language
		print(self.Language.language_texts["story, title()"] + ":")
		print("\t" + self.story["Titles"][self.user_language])
		print()

		# Define the show text
		show_text = " " + self.language_texts["this_chapter"]
		show_text = self.dictionary["Writing mode"]["Language texts"]["Action"].title() + show_text

		# Show the information with the writing text in the action tense
		print(show_text + ":")

		# Define the chapter title
		chapter_title = self.chapter["Titles (with leading zeroes)"][self.user_language]

		# If there is an addon, add it
		if "Addon" in self.dictionary["Writing mode"]:
			chapter_title += self.dictionary["Writing mode"]["Addon"]

		# Show the chapter title
		print("\t" + chapter_title)

		# ---------- #

		# Iterate through the list of small languages
		for language in self.languages["small"]:
			# Get the translated language
			translated_language = self.languages["full_translated"][language][self.user_language]

			# Get the chapter file
			file = self.dictionary["Chapter"]["Files"][language]

			# Show the "Opening the chapter file in [language]" text
			text = self.language_texts["opening_the_chapter_file_in"] + " " + translated_language

			print()
			print(self.separators["3"])
			print()
			print(text + "...")

			# Open it
			self.System.Open(file, verbose = False)

			if self.switches["Testing"] == False:
				# Wait for one second
				self.Date.Sleep(1)

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
			self.chapter["Language"]["Source"]["Full"] # The full chapter source language
		]

		# Format the template with the items
		url = template.format(*items)

		# Define the list of custom parameters to add to the URL
		parameters = [
			"chapter=" + str(self.chapter["Number"]), # The number of the chapter
			"write=true", # The write switch, to activate writing mode on the story website
			"show_chapter_covers=true" # Show chapter covers on the chapter tabs
		]

		# Iterate through the list of parameters
		for parameter in parameters:
			url += "&" + parameter

		# Show the text about opening the story website
		text = self.language_texts["opening_the_story_website_in"] + " " + self.dictionary["Chapter"]["Language"]["Source"]["Translated"]

		print()
		print(self.separators["3"])
		print()
		print(text + "...")

		# Open the URL
		self.System.Open(url, verbose = False)

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
		# Define the template
		template = self.language_texts["{}_the_chapter_{}_of_my_story_{}"]

		# Define the list of items
		items = [
			self.dictionary["Writing mode"]["Language texts"]["Action"].title(), # The action of the writing mode
			self.dictionary["Chapter"]["Numbers"]["Names"][self.user_language], # The number name of the chapter in the user language
			'"' + self.story["Titles"][self.user_language] + '"' # The story title in the user language, with quotes around it
		]

		# Format the template with the items, making the Discord status
		self.chapter["Discord"]["Status"] = template.format(*items)

		# Define the text to show
		text = self.Language.language_texts["copying_the_discord_status"]

		# Show it
		print()
		print(self.separators["3"])
		print()
		print(text + "...")

		# Copy the status to the clipboard
		self.Text.Copy(self.chapter["Discord"]["Status"], verbose = False)

	def Start_Writing(self):
		# Show a five dash space separator
		print()
		print(self.separators["5"])

		# If this is not the first time the user writes the current chapter
		if self.states["First time writing"] == False:
			# Show the total writing time text in the user language
			print()
			print(self.Language.language_texts["total_duration_of"] + " " + self.dictionary["Writing mode"]["Language texts"]["Item"] + ":")
			print("\t" + self.dictionary["Writing"]["Duration"]["Text"][self.user_language])

		# ---------- #

		# Ask to start counting the writing time
		type_text = self.language_texts["press_enter_to_start_counting_the_time_of"] + " " + self.dictionary["Writing mode"]["Language texts"]["Item"]

		self.Input.Type(type_text)

		# Define the "Session" dictionary, with the first writing time
		self.dictionary["Session"] = {
			"Before": self.Date.Now(),
			"After": {},
			"After (copy)": {},
			"Duration": {}
		}

		# Show the now time
		print()
		print(self.Date.language_texts["now, title()"] + ":")
		print("\t" + self.dictionary["Session"]["Before"]["Timezone"]["DateTime"]["Formats"]["HH:MM DD/MM/YYYY"])

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
			self.dictionary["Writing mode"]["Language texts"]["Item"],
			self.dictionary["Writing mode"]["Language texts"]["Action"]
		]

		# Format the template with the items in the list, making the input text
		input_text = template.format(*items)

		# Ask if the user wants to postpone the writing session to continue writing later
		self.states["Postpone writing session"] = self.Input.Yes_Or_No(input_text)

		# Show a five dash space separator
		print()
		print(self.separators["5"])

		# ---------- #

		# Ask for the user to press Enter when they stop writing
		# (Not when the user finished writing the whole chapter)
		type_text = self.language_texts["press_enter_when_you_stop"] + " " + self.dictionary["Writing mode"]["Language texts"]["Infinitive action"]

		self.Input.Type(type_text)

		# Show a five dash space separator
		print()
		print(self.separators["5"])

		# ---------- #

		# Define the "After" time (now, but after writing)
		self.dictionary["Session"]["After"] = self.Date.Now()

		# Create the copy of the after time
		self.dictionary["Session"]["After (copy)"] = deepcopy(self.dictionary["Session"]["After"])

		# Define the after time as None
		after_time = None

		# ---------- #

		# Define the empty addon variable
		addon = ""

		# If the "Pause" dictionary is present
		if "Pause" in self.dictionary["Session"]:
			# Define the addon as the text about the writing time with the pause time subtracted
			addon = " (" + self.language_texts["with_the_pause_time_subtracted"] + ")"

			# Define the subtract dictionary
			subtract = {}

			# Fill the subtract dictionary
			for key, value in self.dictionary["Session"]["Pause"]["Subtract"].items():
				subtract[key.lower()] = value

			# Define the relative delta
			relative_delta = self.Date.Relativedelta(**subtract)

			# Subtract the subtract time from the after time
			self.dictionary["Session"]["After (copy)"] = self.Date.Now(self.dictionary["Session"]["After (copy)"]["Object"] - relative_delta)

			# Update the after time
			after_time = self.dictionary["Session"]["After (copy)"]

		# ---------- #

		# Define the "add" variable
		add = False

		# If the "Testing" switch is True
		if self.switches["Testing"] == True:
			# Define the "add" variable as True
			add = True

		# Calculate and define the writing duration
		self.dictionary["Session"]["Duration"] = self.Calculate_Duration(self.dictionary["Session"], add = add, after_time = after_time)

		# Show the after time (after writing the chapter)
		print()
		print(self.Date.language_texts["after, title()"] + ":")
		print("\t" + self.dictionary["Session"]["After"]["Timezone"]["DateTime"]["Formats"]["HH:MM DD/MM/YYYY"])

		# Define the text to show
		text = self.Language.language_texts["duration_of"] + " " + self.dictionary["Writing mode"]["Language texts"]["Item"]

		# Add the addon if it is not empty
		if addon != "":
			text += addon

		# Add the colon
		text += ":"

		# Show the writing duration text in the user language
		print()
		print(text)

		# Show the writing duration (subtracting the pause time)
		print("\t" + self.dictionary["Session"]["Duration"]["Text"][self.user_language])

		# Show the pause duration time in the user language
		text = self.Language.language_texts["duration_of"] + " " + self.Language.language_texts["pause, type: item"].lower()
		text += " (" + self.language_texts["the_time_subtracted_from_the_total_{}_time"].format(self.dictionary["Writing mode"]["Language texts"]["Item"]) + ")"

		# If the "Pause" key is present inside the "Session" dictionary
		if "Pause" in self.dictionary["Session"]:
			# Show the pause duration time in the user language
			text = self.Language.language_texts["duration_of"] + " " + self.Language.language_texts["pause, type: item"].lower()
			text += " (" + self.language_texts["the_time_subtracted_from_the_total_{}_time"].format(self.dictionary["Writing mode"]["Language texts"]["Item"]) + ")"

			print()
			print(text + ":")
			print("\t" + self.dictionary["Session"]["Pause"]["Duration"]["Text"][self.user_language])

		# ---------- #

		# If the writing session is the first one for the current chapter
		if self.dictionary["Writing"]["Duration"]["Units"] == {}:
			# Define the first time of writing as the "Before" time
			self.dictionary["Writing"]["First"] = self.dictionary["Session"]["Before"]

		else:
			# Transform the already existing first writing time into a Date dictionary
			self.dictionary["Writing"]["First"] = self.Date.From_String(self.dictionary["Writing"]["First"])

		# Define the "Added" time as the first time if it is not present
		if self.dictionary["Writing"]["Added"] == "":
			self.dictionary["Writing"]["Added"] = deepcopy(self.dictionary["Writing"]["First"])

		else:
			# Transform the already existing added writing time into a Date dictionary
			self.dictionary["Writing"]["Added"] = self.Date.From_String(self.dictionary["Writing"]["Added"])

		# Define the last time of writing as the "After" time
		self.dictionary["Writing"]["Last"] = self.dictionary["Session"]["After"]

		# If the writing session is the first one for the current chapter
		if self.states["First time writing"] == True:
			# Define the "Duration" dictionary inside the writing "Times" dictionary
			# With the "Units" dictionary being the units of the current session duration
			self.dictionary["Writing"]["Duration"] = {
				"Units": self.dictionary["Session"]["Duration"]["Difference"],
				"Text": {}
			}

		# Calculate and update the writing time
		self.Update_Writing_Time()

		# ---------- #

		# If this is not the first time the user writes the current chapter
		if self.states["First time writing"] == False:
			# Show the total writing time text in the user language
			print()
			print(self.Language.language_texts["total_duration_of"] + " " + self.dictionary["Writing mode"]["Language texts"]["Item"] + ":")
			print("\t" + self.dictionary["Writing"]["Duration"]["Text"][self.user_language])

		# ---------- #

		# Define the text asking if the user finished writing the whole chapter, not just a part of it
		type_text = self.language_texts["did_you_finished_{}_the_whole_chapter"].format(self.dictionary["Writing mode"]["Language texts"]["Infinitive action"])

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

	def Pause_Writing(self):
		# Ask if the user wants to pause the writing session
		input_text = self.language_texts["do_you_want_to_pause_the_{}_session"].format(self.dictionary["Writing mode"]["Language texts"]["Item"])

		self.states["Pause writing session"] = self.Input.Yes_Or_No(input_text)

		# If the user wants to pause the writing session
		if self.states["Pause writing session"] == True:
			# Show a five dash space separator
			print()
			print(self.separators["5"])

			# Show the before time (when starting writing the chapter)
			print()
			print(self.Date.language_texts["before, title()"] + ":")
			print("\t" + self.dictionary["Session"]["Before"]["Timezone"]["DateTime"]["Formats"]["HH:MM DD/MM/YYYY"])

			# Calculate and define the writing duration
			self.dictionary["Session"]["Duration"] = self.Calculate_Duration(self.dictionary["Session"])

			# Show the after time (after writing the chapter)
			print()
			print(self.Date.language_texts["after, title()"] + ":")
			print("\t" + self.dictionary["Session"]["After"]["Timezone"]["DateTime"]["Formats"]["HH:MM DD/MM/YYYY"])

			# Show the writing duration time in the user language
			print()
			print(self.Language.language_texts["duration_of"] + " " + self.dictionary["Writing mode"]["Language texts"]["Item"] + ":")
			print("\t" + self.dictionary["Session"]["Duration"]["Text"][self.user_language])

			# ---------- #

			# If the "Pause" key is not in the session dictionary
			if "Pause" not in self.dictionary["Session"]:
				# Define the "Pause" dictionary
				self.dictionary["Session"]["Pause"] = {
					"Before": self.Date.Now(),
					"After": {},
					"Is pause": True
				}

			# If the "Pause" key is in the session dictionary
			else:
				self.states["Already paused"] = True

			# ---------- #

			# Ask for user input to unpause the writing session
			input_text = self.language_texts["press_enter_to_unpause_the_{}_session"].format(self.dictionary["Writing mode"]["Language texts"]["Item"])

			self.Input.Type(input_text)

			# ---------- #

			# Show a five dash space separator
			print()
			print(self.separators["5"])

			# If the user did not pause the writing session
			if self.states["Already paused"] == False:
				# Calculate and define the pause duration
				self.dictionary["Session"]["Pause"]["Duration"] = self.Calculate_Duration(self.dictionary["Session"]["Pause"])

			# Show the after time (after writing the chapter)
			print()
			print(self.Date.language_texts["after, title()"] + ":")
			print("\t" + self.dictionary["Session"]["Pause"]["After"]["Timezone"]["DateTime"]["Formats"]["HH:MM DD/MM/YYYY"])

			# ---------- #

			# If the user already paused the writing session
			if self.states["Already paused"] == True:
				if self.switches["Testing"] == False:
					# Define the after time
					after_time = self.Date.Now()

				if self.switches["Testing"] == True:
					relative_delta = self.Date.Relativedelta(minutes = 15)

					after_time = self.Date.Now(self.dictionary["Session"]["Pause"]["After"]["Object"] + relative_delta)

				# Create the difference between the now and after time
				difference = self.Date.Difference(self.dictionary["Session"]["Pause"]["After"], after_time)

				# Define the add dictionary
				add = {}

				# Fill the subtract dictionary
				for key, value in difference["Difference"].items():
					add[key.lower()] = value

				# Define the relative delta
				relative_delta = self.Date.Relativedelta(**add)

				# Add the add time to the after time
				self.dictionary["Session"]["Pause"]["After"] = self.Date.Now(self.dictionary["Session"]["Pause"]["After"]["Object"] + relative_delta)

			# ---------- #

			# Define the time difference
			self.dictionary["Session"]["Pause"]["Duration"] = self.Date.Difference(self.dictionary["Session"]["Pause"]["Before"], self.dictionary["Session"]["Pause"]["After"])

			# Define the subtract time
			self.dictionary["Session"]["Pause"]["Subtract"] = self.dictionary["Session"]["Pause"]["Duration"]["Difference"]

			# ---------- #

			# Define the subtract dictionary
			subtract = {}

			# Fill the subtract dictionary
			for key, value in self.dictionary["Session"]["Pause"]["Subtract"].items():
				subtract[key.lower()] = value

			# Define the relative delta
			relative_delta = self.Date.Relativedelta(**subtract)

			# Subtract the subtract time from the after time
			after_time = self.Date.Now(self.dictionary["Session"]["After (copy)"]["Object"] - relative_delta)

			# Define the time difference
			difference = self.Date.Difference(self.dictionary["Session"]["Before"], after_time)

			# Define the text to show
			text = self.Language.language_texts["duration_of"] + " " + self.dictionary["Writing mode"]["Language texts"]["Item"]

			# If the "Pause" key is present inside the "Session" dictionary
			if "Pause" in self.dictionary["Session"]:
				# Add the text about the writing time with the pause time subtracted
				text += " (" + self.language_texts["with_the_pause_time_subtracted"] + ")"

			# Add the colon
			text += ":"

			# Show the writing duration time in the user language (subtracting the pause time)
			print()
			print(text)
			print("\t" + difference["Text"][self.user_language])

			# ---------- #

			# Show the pause duration time in the user language
			text = self.Language.language_texts["duration_of"] + " " + self.Language.language_texts["pause, type: item"].lower()
			text += " (" + self.language_texts["the_time_subtracted_from_the_total_{}_time"].format(self.dictionary["Writing mode"]["Language texts"]["Item"]) + ")"

			print()
			print(text + ":")
			print("\t" + self.dictionary["Session"]["Pause"]["Duration"]["Text"][self.user_language])

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

		# Get the time difference
		difference = self.Date.Difference(dictionary["Before"], after_time)

		return difference

	def Finish_Writing(self):
		# If the writing mode is inside the defined list
		if self.writing_mode in ["Write", "Revise"]:
			# Add or update the chapter, depending on the writing mode
			self.Update_Chapter()

		# Update the chapter dictionary
		self.Update_Chapter_Dictionary()

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
			for key, unit in self.dictionary["Session"]["Duration"]["Difference"].items():
				dictionary[key.lower()] = unit

			# Add the writing time difference time unit to the added time date object
			self.dictionary["Writing"]["Added"]["Object"] += self.Date.Relativedelta(**dictionary)

			# Transform the added time into a date dictionary with the updated object (the added time above)
			self.dictionary["Writing"]["Added"] = self.Date.Now(self.dictionary["Writing"]["Added"]["Object"])

			# Make the difference between the first time and the added time
			difference = self.Date.Difference(self.dictionary["Writing"]["First"]["Object"], self.dictionary["Writing"]["Added"]["Object"])

			# Update the time units of the "Duration" dictionary
			self.dictionary["Writing"]["Duration"]["Units"] = difference["Difference"]

			# Create the writing time text using the "Make_Time_Text" method of the "Date" module
			self.dictionary["Writing"]["Duration"]["Text"] = self.Date.Make_Time_Text(difference)

			# Transform the times back into date strings
			for key in ["First", "Last", "Added"]:
				self.dictionary["Writing"][key] = self.Date.To_String(self.dictionary["Writing"][key], utc = False)

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
				self.dictionary["Writing"][key] = self.Date.From_String(self.dictionary["Writing"][key])

	def Update_Chapter(self):
		# Define the default "update chapter titles" variable
		update_chapter_titles = False

		# If the writing mode is "Revise"
		if self.writing_mode == "Revise":
			# Ask if the user wants to update the chapter titles
			input_text = self.language_texts["do_you_want_to_update_the_chapter_titles"]

			update_chapter_titles = self.Input.Yes_Or_No(input_text)

		# Iterate through the list of small languages
		for language in self.languages["small"]:
			# Get the full and translated languages
			full_language = self.languages["full"][language]
			translated_language = self.languages["full_translated"][language][self.user_language]

			# Ask for the chapter title in the current language
			type_text = self.language_texts["type_the_chapter_title_in_{}"].format(translated_language)

			# Define the default "chapter title" variable
			chapter_title = ""

			# If the writing mode is "Write"
			# Or the writing mode is "Revise"
			# And the "update chapter titles" variable is True
			if (
				self.writing_mode == "Write" or
				self.writing_mode == "Revise" and
				update_chapter_titles == True
			):
				# If the "testing" switch is False
				if self.switches["Testing"] == False:
					# Ask for the chapter title in the current language
					chapter_title = self.Input.Type(type_text, next_line = True)

				# If the "testing" switch is True
				if self.switches["Testing"] == True:
					chapter_title = self.texts["a_new_chapter"][language].title()

					# Show the defined chapter title
					print()
					print(type_text + ":")
					print(chapter_title)

			# If the "chapter title" variable is not empty
			if chapter_title != "":
				# Add it to the "Titles" dictionary
				self.chapter["Titles"][language] = chapter_title

				# If the writing mode is "Revise"
				if self.writing_mode == "Revise":
					# Redefine the chapter title with leading zeroes to be only the number
					self.chapter["Titles (with leading zeroes)"][language] = self.chapter["Numbers"]["Leading zeroes"]

				# Add it to the "Titles (with leading zeroes)" dictionary
				self.chapter["Titles (with leading zeroes)"][language] += " - " + chapter_title

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
					text = self.Text.From_List(titles, break_line = True)

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
			source_file = self.chapter["Files"][language]

			# Define the destination file
			destination_file = self.story["Folders"]["Chapters"][full_language]["root"] + self.chapter["Titles (with leading zeroes)"][language] + ".txt"

			# If the writing mode is "Write"
			# And the current language is the user language
			# Or the writing mode is "Revise"
			# And the "update chapter titles" variable is True
			if (
				self.writing_mode == "Write" and
				language == self.user_language or
				self.writing_mode == "Revise" and
				update_chapter_titles == True
			):
				# Rename the chapter file
				self.File.Move(source_file, destination_file)

			# If the current language is not the user language
			# And the writing mode is not "Revise"
			if (
				language != self.user_language and
				self.writing_mode != "Revise"
			):
				# Create the file
				self.File.Create(destination_file)

		# ---------- #

		# If the writing mode is "Write"
		if self.writing_mode == "Write":
			# Add the written date of the chapter to the "Writing dates.txt" file
			file = self.story["Folders"]["Chapters"]["Writing dates"]
			date = self.dictionary["Writing"]["Last"]["Timezone"]["DateTime"]["Formats"]["HH:MM DD/MM/YYYY"]

			self.File.Edit(file, date, "a")

	def Update_Chapter_Dictionary(self):
		# Get the date that the user finished writing the chapter
		date = self.dictionary["Writing"]["Last"]["Timezone"]["DateTime"]["Formats"]["HH:MM DD/MM/YYYY"]

		# If the writing mode is "Write"
		if self.writing_mode == "Write":
			# Create or update the chapter dictionary
			self.story["Information"]["Chapters"]["Dictionary"][self.chapter["Number"]] = {
				"Number": self.chapter["Number"],
				"Titles": self.chapter["Titles"],
				"Dates": {
					"Written": "",
					"Revised": "",
					"Translated": ""
				}
			}

		# Update the "Titles" key
		self.story["Information"]["Chapters"]["Dictionary"][str(self.chapter["Number"])]["Titles"] = self.chapter["Titles"]

		# Define a shortcut variable for the chapter dictionary inside the "Dictionary" key
		chapter = self.story["Information"]["Chapters"]["Dictionary"][str(self.chapter["Number"])]

		# Define the key for the date of the writing mode
		key = self.dictionary["Writing mode"]["Texts"]["Chapter"]["en"]

		# Update the date key of the correct writing mode
		chapter["Dates"][key.capitalize()] = date

		# Update the "Chapters.json" file with the updated "Chapters" dictionary
		self.JSON.Edit(self.story["Folders"]["Information"]["Chapters"], self.story["Information"]["Chapters"])

	def Register_Task(self, register_task = True):
		# Create the task dictionary, to use it on the "Tasks" class
		self.task_dictionary = {
			"Task": {
				"Titles": {},
				"Descriptions": {},
				"Custom task item": self.dictionary["Writing mode"]["Texts"]["Chapter"]
			}
		}

		# Define the text template for the task as the "I started writing", for the first time
		template = self.texts["i_started_{}_the_chapter_{}_of_my_story_{}"]

		# If this is not the first time the user writes the current chapter
		# And is not the last one (the user did not finished writing the whole chapter)
		if (
			self.states["First time writing"] == False and
			self.states["Finished writing"] == False
		):
			# Define the text template for the task as the "I have been writing", for the middle times
			# (Not the beginning of writing, and not the ending)
			template = self.texts["i_have_been_{}_the_chapter_{}_of_my_story_{}_until_now"]

		# If the user finished writing the whole chapter
		if self.states["Finished writing"] == True:
			# Define the text template for the task as the "I finished writing", for the last time
			template = self.texts["i_finished_{}_the_chapter_{}_of_my_story_{}"]

		# ---------- #

		# Iterate through the list of small languages
		for language in self.languages["small"]:
			# Get the full and translated user languages
			full_language = self.languages["full"][language]
			translated_user_language = self.languages["full_translated"][self.user_language][language]

			# Define the list of items to use to format the template
			items = [
				self.dictionary["Writing mode"]["Texts"]["Infinitive action"][language],
				self.chapter["Numbers"]["Names"][language],
				self.story["Titles"][language]
			]

			# If this is not the first time the user writes the current chapter
			# And is not the last one (the user did not finished writing the whole chapter)
			if (
				self.states["First time writing"] == False and
				self.states["Finished writing"] == False
			):
				# Update the writing mode text to the "Action" one
				items[0] = self.dictionary["Writing mode"]["Texts"]["Action"][language]

			# Define the task title in the current language as the template in the current language
			task_title = template[language]

			# If the writing mode is "Translate"
			if self.writing_mode == "Translate":
				# Define the English translated language
				translated_language = self.languages["full_translated"]["en"][language]

				# Add the "from [User langauge] to English" text
				task_title += " " + self.Language.texts["from_{}_to_{}"][language].format(translated_user_language, translated_language)

			# Format the template with the list of items
			task_title = task_title.format(*items)

			# Add the task title to the "Task" dictionary
			self.task_dictionary["Task"]["Titles"][language] = task_title

			# ---------- #

			# Create the task description, initially as the task title with a dot
			description = self.task_dictionary["Task"]["Titles"][language] + "."

			# Add two line breaks
			description += "\n\n"

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
				description += self.texts["the_chapter_with_the_title"][language] + ":" + "\n"

				# Add the chapter title in the current language
				description += self.chapter["Titles"][language]

				# Add two line breaks
				description += "\n\n"

			# ---------- #

			# Add the "I started at, and stopped at" formatted template
			items = [
				self.dictionary["Session"]["Before"]["Formats"]["HH:MM DD/MM/YYYY"].split(" ")[0],
				self.dictionary["Session"]["After"]["Formats"]["HH:MM DD/MM/YYYY"].split(" ")[0]
			]

			description += self.texts["i_started_at_{}_and_stopped_at_{}"][language].format(*items)

			# Add the dot and line break
			description += "." + "\n"

			# ---------- #

			# Add the "I [wrote] for [writing time]" formatted template
			items = [
				self.dictionary["Writing mode"]["Texts"]["Done"][language].lower()
			]

			description += self.texts["i_{}_for"][language].format(*items)

			# Add the session writing time text
			# Example: 1 hour, 30 minutes, 10 seconds
			description += " " + self.dictionary["Session"]["Duration"]["Text"][language]

			# Define the "add_time_format" switch
			add_time_format = False

			# If the "add_time_format" switch is True
			if add_time_format == True:
				# Add the session writing time units
				# Example: (01:30:10)
				description += " ("

				# Define the list of keys
				keys = list(self.dictionary["Session"]["Duration"]["Difference"].keys())

				# Iterate through the list of units
				for key, unit in self.dictionary["Session"]["Duration"]["Difference"].items():
					# Add the unit number with leading zeroes
					description += str(self.Text.Add_Leading_Zeroes(unit))

					# If the unit is not the last one, add a colon
					if key != keys[-1]:
						description += ":"

				# Close the parenthesis and add the dot
				description += ")"

			# Add the end period
			description += "."

			# ---------- #

			# If this is not the first time the user writes the current chapter
			if self.states["First time writing"] == False:
				# Add two line breaks
				description += "\n\n"

				# Add the "Totalling " text
				description += self.Language.texts["totaling, title()"][language] + " "

				# Add the total writing time text
				# Example: 1 hour, 30 minutes, 10 seconds
				description += self.dictionary["Writing"]["Duration"]["Text"][language]

				# Create the session writing time units
				# Example: (01:30:10)
				dictionary = {
					"Difference": self.dictionary["Writing"]["Duration"]["Units"],
					"Time format": ""
				}

				dictionary["Time format"] = self.Date.Create_Time_Format(dictionary)

				# If the "add_time_format" switch is False
				if add_time_format == False:
					# Add the time format text to the description text
					description += " (" + dictionary["Time format"] + ")"

				# If the "add_time_format" switch is True
				if add_time_format == True:
					# Add the total writing time units
					# Example: (01:30:10)
					description += " ("

					# Define the list of keys
					keys = list(self.dictionary["Writing"]["Duration"]["Units"].keys())

					# Iterate through the list of units
					for key, unit in self.dictionary["Writing"]["Duration"]["Units"].items():
						# Add the unit number with leading zeroes
						description += str(self.Text.Add_Leading_Zeroes(unit))

						# If the unit is not the last one, add a colon
						if key != keys[-1]:
							description += ":"

					# Close the parenthesis and add the dot
					description += ")"

				# Add the end period
				description += "."

			# ---------- #

			# Add the task description to the "Task" dictionary
			self.task_dictionary["Task"]["Descriptions"][language] = description

		# Register the task with the root method
		Stories.Register_Task(self, self.task_dictionary, register_task = register_task)
# Convert_Data.py

# Import the root class
from Stories.Stories import Stories as Stories

# Import some useful modules
from copy import deepcopy

class Convert_Data(Stories):
	def __init__(self):
		# Run the root class to import its methods and variables
		super().__init__()

		# Define the root "convert" dictionary
		self.convert = {
			"Stories list": self.stories["Titles"]["en"]
		}

		# Iterate through the list of stories
		self.Iterate_Through_Stories_List()

		# Run the root class to update the files and dictionaries of all stories
		super().__init__()

	def Iterate_Through_Stories_List(self):
		# Define the total stories number as the length of the list of stories
		total_stories_number = len(self.convert["Stories list"])

		# Iterate through the list of English story titles
		for story_number, story_title in enumerate(self.convert["Stories list"], start = 1):
			# Define the story information text
			story_information = f"""
			{self.separators["10"]}

			{self.language_texts["story_number"]}:
			[{story_number}/{total_stories_number}]""".replace("\t", "")

			# ----- #

			# Get the dictionary of the story
			story = self.stories["Dictionary"][story_title]

			# Define a shortcut to the story "Chapters" and "Writing" dictionaries
			for key in ["Chapters", "Writing"]:
				story[key] = story["Information"][key]

			# Add the story title in the user language to the story information text
			story_information += f"""
			
			{self.Language.language_texts["story_title"]}:
			{story["Titles"][self.language["Small"]]}""".replace("\t", "")

			# Show the story information text
			print(story_information)

			# ----- #

			# Update the story "Writing" dictionary
			self.Update_Writing_Dictionary(story)

			# Update the story "Chapters" dictionary
			self.Update_Chapters_Dictionary(story, story_information)

			# ----- #

			# If the story is not the last one
			if story_title != self.convert["Stories list"][-1]:
				# Ask for the user to press Enter before continuing to the next story
				self.Input.Type(self.Language.language_texts["continue, title()"])

		# Show a final five dash space separator
		print()
		print(self.separators["5"])

	def Update_Writing_Dictionary(self, story):
		# Iterate through the writing modes and writing mode dictionaries
		for writing_mode, writing_mode_dictionary in self.stories["Writing modes"]["Dictionary"].items():
			# Define a shortcut to the current writing mode dictionary
			writing_dictionary = story["Writing"][writing_mode]

			# If the "Chapter" key is inside the current writing dictionary
			# (That means it is in the old format)
			if "Chapter" in writing_dictionary:
				# Define the old key as "Chapter"
				old_key = "Chapter"

				# Define the new key as "Current chapter"
				new_key = "Current chapter"

				# Replace the "Chapter" key with the "Current chapter" key
				writing_dictionary = self.JSON.Add_Key_After_Key(writing_dictionary, new_key, after_key = old_key, remove_after_key = True)

				# If the "Current chapter" is zero, change it to one
				writing_dictionary["Current chapter"] = 1

				# If the writing mode is "Write"
				if writing_mode == "Write":
					# Change the "Current chapter" to the total number of chapters
					writing_dictionary["Current chapter"] = story["Chapters"]["Numbers"]["Total"]

				# ----- #

				# If the "First" string of the "Times" dictionary is an empty string
				if writing_dictionary["Times"]["First"] == "":
					# Remove the "Times" key
					writing_dictionary.pop("Times")

					# Add it again with the new format
					writing_dictionary["Times"] = {
						"Started": "",
						"Finished": "",
						"Finished (UTC)": ""
					}

				# ----- #

				# Add the "Durations", "Total duration", and "Status" dictionaries
				writing_dictionary.update({
					"Durations": {
						"List": [],
						"Dictionary": {}
					},
					"Total duration": {},
					"Status": {
						"Finished": False
					}
				})

				# ----- #

				# If the writing mode is not "Translate"
				if writing_mode != "Translate":
					# Add the "Posted" status to the "Status" dictionary
					writing_dictionary["Status"]["Posted"] = False

				# If the writing mode is "Write"
				if writing_mode == "Write":
					# Change the "Finished" and "Posted" statuses to True
					writing_dictionary["Status"] = {
						"Finished": True,
						"Posted": True
					}

				# ----- #

				# Update the writing dictionary in the root "Writing" dictionary
				story["Writing"][writing_mode] = writing_dictionary

		# Update the "Writing.json" file with the updated "Writing" dictionary
		self.JSON.Edit(story["Folders"]["Information"]["Writing"], story["Writing"])

	def Update_Chapters_Dictionary(self, story, story_information):
		# Define a shortcut to the total chapters number
		total_chapters_number = story["Chapters"]["Numbers"]["Total"]

		# Replace the ten dash space separator from the story information with a five dash space separator
		story_information = story_information.replace(self.separators["10"], self.separators["5"])

		# Iterate through the chapters dictionaries
		for chapter_number, chapter in enumerate(story["Chapters"]["Dictionary"].values(), start = 1):
			# Show the story information text
			print(story_information)

			# Show the "Chapter number" text, the current chapter number, and the total chapters number
			print()
			print(self.language_texts["chapter_number"] + ":")
			print("[" + str(chapter_number) + "/" + str(total_chapters_number) + "]")

			# ----- #

			# If the "Dates" key is inside the current chapter dictionary
			# (That means it is in the old format)
			if "Dates" in chapter:
				# Make a backup and copy of the "Dates" dictionary
				dates = deepcopy(chapter["Dates"])

				# Remove it
				chapter.pop("Dates")

				# Define a list of keys to import from the root default "Chapter" dictionary
				keys_to_import = [
					"Writing",
					"Revisions",
					"Translations",
					"Posting"
				]

				# Import them
				for key in keys_to_import:
					# Define the key
					chapter[key] = deepcopy(self.stories["Chapter"][key])

				# List the dates
				dates_list = dates.values()

				# If at least one date string is not empty
				if any(date != "" for date in dates_list):
					# Add the "Dates" key again
					chapter["Dates"] = dates

			# ----- #

			# If the only key inside the "Posting" dictionary is "Times"
			# (That means it is in the old format)
			if chapter["Posting"].keys() == ["Times"]:
				# Make a backup and copy of the "Times" dictionary
				times = deepcopy(chapter["Posting"]["Times"])

				# Remove it
				chapter["Posting"].pop("Times")

				# Import the "Posting" dictionary from the root default "Chapter" dictionary
				chapter["Posting"] = deepcopy(self.stories["Chapter"]["Posting"])

				# Update the "Times" dictionary of the "Writing" dictionary with the local backup
				chapter["Posting"]["Writing"]["Times"] = times

			# ----- #

			# If the "Finished" key is present inside the writing "Times" dictionary
			if "Finished" in chapter["Writing"]["Times"]:
				# Define a shortcut to the "Finished" time of the "Writing" dictionary
				finished_writing_timezone = chapter["Writing"]["Times"]["Finished"]

				# Transform it into a date dictionary using the timezone format
				finished_writing = self.Date.From_String(finished_writing_timezone, format = "%H:%M %d/%m/%Y")

				# Update the "Finished (UTC)" time to the correct one
				chapter["Writing"]["Times"]["Finished (UTC)"] = finished_writing["UTC"]["DateTime"]["Formats"]["YYYY-MM-DDTHH:MM:SSZ"]

			# ----- #

			# Iterate through the local list of writing modes
			for writing_mode in ["Revisions", "Translations"]:
				# Get the writing mode dictionary
				writing_mode_dictionary = chapter[writing_mode]

				# Define a shortcut to the writings dictionary
				writings = writing_mode_dictionary["Dictionary"]

				# Iterate through the list of writing keys and dictionaries
				for key, writing in writings.items():
					# Define a shortcut to the "Finished" time of the writing dictionary
					finished_writing_timezone = writing["Times"]["Finished"]

					# Transform it into a date dictionary using the timezone format
					finished_writing = self.Date.From_String(finished_writing_timezone, format = "%H:%M %d/%m/%Y")

					# Update the "Finished (UTC)" time to the correct one
					writing["Times"]["Finished (UTC)"] = finished_writing["UTC"]["DateTime"]["Formats"]["YYYY-MM-DDTHH:MM:SSZ"]

					# Update the writing dictionary with the local one
					writing_mode_dictionary["Dictionary"][key] = writing

			# ----- #

			# Update the chapter dictionary in the root "Chapters" dictionary
			story["Chapters"]["Dictionary"][str(chapter_number)] = chapter

		# Update the "Chapters.json" file with the updated "Chapters" dictionary
		self.JSON.Edit(story["Folders"]["Information"]["Chapters"], story["Chapters"])
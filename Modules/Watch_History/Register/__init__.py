# Register.py

from Watch_History.Watch_History import Watch_History as Watch_History

from copy import deepcopy

class Register(Watch_History):
	def __init__(self, dictionary = {}):
		super().__init__()

		# Define the class dictionary as the parameter dictionary
		self.dictionary = dictionary

		# Update the "Entry" dictionary with additional structured data:
		# "Diary Slim": initializes empty fields for Diary Slim related text entries
		# "States": sets the initial state for social network posting as False
		self.dictionary["Entry"].update({
			"Diary Slim": {
				"Text": ""
			},
			"States": {
				"Post on the Social Networks": False
			}
		})

		# Define the media variable to make typing the media dictionary easier
		self.media = self.dictionary["Media"]

		# Check the media status
		self.Check_Media_Status()

		# If the user is re-watching the media and media item
		if self.media["States"]["Re-watching"] == False:
			# If the user completed the media or the media item
			if (
				self.media["States"]["Completed media"] == True or
				self.media["States"]["Completed media item"] == True
			):
				# Check the media and media item dates and the date files
				self.Check_Media_Dates()

		# Flag to control whether test-specific behavior should be executed
		test_stuff = False

		# Execute the full workflow only if not in test mode
		if test_stuff == False:
			# Save the entry to the database in the JSON format
			self.Register_In_JSON()

			# Create the individual entry file for the completed task
			self.Create_Entry_File()

			# Create the entry files inside their corresponding year folders
			self.Add_Entry_File_To_Year_Folder()

			# Generate the Diary Slim text for the watched media
			self.Define_Diary_Slim_Text()

			# If the "Defined title" key is not inside the root dictionary
			if "Defined title" not in self.dictionary:
				# Post about the watched media (and item) on the social networks
				self.Post_On_Social_Networks()

			# Write the final Diary Slim text in the user's language on the Diary Slim
			self.Write_On_Diary_Slim()

		# Update the statistic about the media watched
		self.Update_Statistic()

		# If the "Defined title" key is not inside the root dictionary
		if "Defined title" not in self.dictionary:
			# Show information about the watched media (item)
			self.Show_Information()

		# Re-initiate the root class to update the files
		del self.folders

		super().__init__()

	def Register_In_JSON(self):
		# Define a shortcut for the plural form of the media type in English
		self.media_type = self.dictionary["Media type"]["Plural"]["en"]

		# ---------- #

		# Re-read the "Watched.json" file to retrieve the most up-to-date data
		self.dictionaries["Watched"] = self.JSON.To_Python(self.media["Item"]["Folders"]["Watched"]["entries"])

		# If the "Defined title" key is not inside the root dictionary
		if "Defined title" not in self.dictionary:
			# Re-read the "Entries.json" file to retrieve the most up-to-date data
			self.dictionaries["Entries"] = self.JSON.To_Python(self.folders["Watch History"]["Current year"]["Entries"])

		# Check if the "Dictionaries" key exists in the root dictionary
		if "Dictionaries" in self.dictionary:
			# Set the local "dictionaries" variable to the value inside the root dictionary
			self.dictionaries = self.dictionary["Dictionaries"]

			# If the "Watched" key exists, add it to the local dictionaries
			if "Watched" in self.dictionary:
				self.dictionaries["Watched"] = self.dictionary["Watched"]

		# ---------- #

		# Create a local list of dictionaries to update
		dictionaries_to_update = [
			self.dictionaries["Entries"],
			self.dictionaries["Media type"][self.media_type],
			self.dictionaries["Watched"]
		]

		# Increment the total count for entries, media type entries, and root media type entries
		for current_dict in dictionaries_to_update:
			current_dict["Numbers"]["Total"] += 1

			# If the "By media type" key exists, increment the count for the specific media type
			if "By media type" in current_dict["Numbers"]:
				current_dict["Numbers"]["By media type"][self.media_type] += 1

		# ---------- #

		# Define shortcuts for the total entries number and the entry times 
		entries_number = self.dictionaries["Entries"]["Numbers"]["Total"]
		entry_time = self.dictionary["Entry"]["Times"]["Finished watching"]["Formats"]["HH:MM DD/MM/YYYY"]

		# Define the entry "Name" dictionary
		self.dictionary["Entry"]["Name"] = {}

		# Define the template for the entry name
		template = "{}. {} ({})"

		# Iterate through the list of small languages
		for language in self.languages["Small"]:
			# Get the language media type
			language_media_type = self.dictionary["Media type"]["Plural"][language]

			# Define the list of items to use to format the template
			items = [
				entries_number,
				language_media_type,
				entry_time
			]

			# Format the template with the list of items, making the entry name
			entry_name = template.format(*items)

			# Create the language entry name dictionary
			dictionary = {
				"Normal": entry_name,
				"Sanitized": entry_name.replace(":", ";").replace("/", "-")
			}

			# Add the dictionary to the "Languages" dictionary
			self.dictionary["Entry"]["Name"][language] = dictionary

		# Add the entry name to the "Entries" lists in each dictionary
		for current_dict in dictionaries_to_update:
			if self.dictionary["Entry"]["Name"]["en"]["Normal"] not in current_dict["Entries"]:
				current_dict["Entries"].append(self.dictionary["Entry"]["Name"]["en"]["Normal"])

		# ---------- #

		# Update the total number of entries in all dictionaries based on the length of the "Entries" list
		for current_dict in dictionaries_to_update:
			current_dict["Numbers"]["Total"] = len(current_dict["Entries"])

		# ---------- #

		# Create local copies of the media and media item titles to modify them
		media_titles = self.media["Titles"].copy()
		item_titles = self.media["Item"]["Titles"].copy()

		# Define a list of title dictionaries to remove specific keys
		titles = [
			media_titles,
			item_titles
		]

		# Remove specified keys from each title dictionary
		for current_dict in titles:
			# Remove the "Language" key
			current_dict.pop("Language")

			# If the "ja" (Japanese) key is inside the dictionary of titles
			# And the "Romanized" key is inside it too
			# (That means the original title is already the Japanese title, so we remove the key)
			if (
				"ja" in current_dict and
				"Romanized" in current_dict
			):
				current_dict.pop("ja")

			# Remove the "Sanitized" key
			current_dict.pop("Sanitized")

			# Remove language keys that match the original or romanized titles
			for language in self.languages["Small"]:
				if language in current_dict:
					if (
						current_dict["Original"] == current_dict[language] or
						("Romanized" in current_dict and current_dict["Romanized"] == current_dict[language])
					):
						current_dict.pop(language, None) # Use None to avoid KeyError if the key does not exist

		# ---------- #

		# Get the normal entry name from the dictionary
		self.entry_name = self.dictionary["Entry"]["Name"]["en"]["Normal"]

		# Add the "Entry" dictionary to the "Dictionary" dictionary
		self.dictionaries["Entries"]["Dictionary"][self.entry_name] = {
			"Watched media number": self.dictionaries["Entries"]["Numbers"]["Total"], # The number of the watched media, by year
			"Watched media number by media type": self.dictionaries["Media type"][self.media_type]["Numbers"]["Total"], # The number of the watched media by media type and by year
			"Media type": self.media_type, # The media type
			"Times": deepcopy(self.dictionary["Entry"]["Times"]), # The dictionary of the watched times, including the started and finished watching time and the duration between those two
			"Entry": self.dictionary["Entry"]["Name"]["en"]["Normal"], # The English name of the entry
			"Media titles": media_titles, # The dictionary of the media titles
			"Media item titles": item_titles, # The dictionary of the media item titles
			"Episode": { # The media episode dictionary
				"Number": 1, # The episode number (currently fixed at 1, will be changed later)
				"Titles": self.media["Episode"]["Titles"] # The episode titles
			}
		}

		# Define a shortcut for the entry dictionary
		self.entry_dictionary = self.dictionaries["Entries"]["Dictionary"][self.entry_name]

		# ---------- #

		# Remove the "Media item titles" key from the dictionary if:
		# 1. The media does not contain a media item list, OR
		# 2. The media item title is the same as the media title
		if (
			self.media["States"]["Has a list of media items"] == False or
			self.media["States"]["The media item is the root media"] == True
		):
			self.dictionaries["Entries"]["Dictionary"][self.entry_name].pop("Media item titles")

		# Remove the "Episode" key from the dictionary if:
		# 1. The media is non-series media, OR
		# 2. The media is a single unit
		if (
			self.media["States"]["Series media"] == False or
			self.media["States"]["Single unit"] == True
		):
			self.dictionaries["Entries"]["Dictionary"][self.entry_name].pop("Episode")

		# Define the episode number in the dictionary if:
		# 1. The media is a series
		# 2. The media is not a single unit
		# 3. The media is episodic
		if (
			self.media["States"]["Series media"] == True and
			self.media["States"]["Single unit"] == False and
			self.media["States"]["Episodic"] == True
		):
			self.dictionaries["Entries"]["Dictionary"][self.entry_name]["Episode"]["Number"] = self.media["Episode"]["Number"]

		# ---------- #

		# Define a list of time keys
		time_keys = [
			"Started watching",
			"Finished watching",
			"Finished watching (UTC)"
		]

		# Iterate through the list of time types
		for time_key in time_keys:
			# Define the timezone key as "Timezone"
			timezone_key = "Timezone"

			# Define the format as the timezone one
			format = "HH:MM DD/MM/YYYY"

			# If the "UTC" text is inside the time key
			if "UTC" in time_key:
				# Update the timezone key to be the UTC one
				timezone_key = "UTC"

				# Define the format as the UTC one
				format = "YYYY-MM-DDTHH:MM:SSZ"

			# Get the time for the current time type, timezone, and format
			time = self.entry_dictionary["Times"][time_key][timezone_key]["DateTime"]["Formats"][format]

			# Update the entry dictionary with the obtained time
			self.entry_dictionary["Times"][time_key] = time

		# Define the "Watching session duration" as the "Text" key
		self.entry_dictionary["Times"]["Watching session duration"] = self.entry_dictionary["Times"]["Watching session duration"]["Text"]

		# ---------- #

		# Remove the "Number" key from the "Episode" dictionary if:
		# 1. The "Episode" dictionary exists
		# 2. The media is non-episodic
		if (
			"Episode" in self.dictionaries["Entries"]["Dictionary"][self.entry_name] and
			self.media["States"]["Episodic"] == False
		):
			self.dictionaries["Entries"]["Dictionary"][self.entry_name]["Episode"].pop("Number")

		# ---------- #

		# If the "ID" key exists in the "Episode" dictionary
		if "ID" in self.media["Episode"]:
			# Create the episode "Link" dictionary
			self.dictionaries["Entries"]["Dictionary"][self.entry_name]["Episode link"] = {
				"ID": self.media["Episode"]["ID"], # The ID of the episode
				"Link": self.media["Episode"]["Remote"]["Link"] # The link of the episode
			}

		# ---------- #

		# Add the "Comment" dictionary if it exists in the "Comment Writer" dictionary
		if "Comment" in self.dictionary["Comment Writer"]:
			self.dictionaries["Entries"]["Dictionary"][self.entry_name]["Comment"] = self.dictionary["Comment Writer"]["Comment"]

			# Define a shortcut for the "Comment" dictionary
			comment = self.dictionaries["Entries"]["Dictionary"][self.entry_name]["Comment"]

			# If the "Comment times" is in the comment dictionary
			if "Comment times" in comment:
				# Change the "Comment times" to just "Times", because the context is already the comment
				new_key = "Times"
				after_key = "Comment times"
				comment = self.JSON.Add_Key_After_Key(comment, {new_key: comment[after_key]}, after_key = after_key, remove_after_key = True)

			# If the "Comment link" is in the comment dictionary
			if "Comment link" in comment:
				# Change the "Comment link" to just "Link", because the context is already the comment
				new_key = "Link"
				after_key = "Comment link"
				comment = self.JSON.Add_Key_After_Key(comment, {new_key: comment[after_key]}, after_key = after_key, remove_after_key = True)

			# Update the root comment dictionary
			self.dictionaries["Entries"]["Dictionary"][self.entry_name]["Comment"] = comment

			# If the only comment key is "Times"
			# And the timezone time of the comment is the same as the finished watching timezone time
			if (
				comment.keys() == {"Times"} and
				comment["Times"]["Timezone"] == self.dictionary["Entry"]["Times"]["Finished watching"]
			):
				# Remove the comment dictionay
				self.dictionaries["Entries"]["Dictionary"][self.entry_name].pop("Comment")

		# ---------- #

		# Get the "States" dictionary with its states and state texts using the "Define_States_Dictionary" root method
		self.dictionary["States"] = self.Define_States_Dictionary(self.dictionary)

		# Add the "States" dictionary to the entry dictionary if it is not empty
		if self.dictionary["States"]["States"] != {}: # Check if the "States" dictionary is not empty
			self.dictionaries["Entries"]["Dictionary"][self.entry_name]["States"] = self.dictionary["States"]["States"]

		# ---------- #

		# Add the entry dictionary to the media type and watched entry dictionaries
		for current_dict in dictionaries_to_update:
			if current_dict is not self.dictionaries["Entries"]: # Ensure we do not update the "Entries" dictionary itself
				current_dict["Dictionary"][self.entry_name] = self.dictionaries["Entries"]["Dictionary"][self.entry_name].copy()

		# ---------- #

		# Get the "Comments" dictionary from the file
		comments = self.JSON.To_Python(self.folders["Comments"]["Comments"])

		# Get the number of comments for the current year from the "Comments.json" file
		self.dictionaries["Entries"]["Numbers"]["Comments"] = comments["Numbers"]["Years"][self.current_year["Number"]]

		# Get the number of comments for the current year and current media type from the "Comments.json" file
		self.dictionaries["Media type"][self.media_type]["Numbers"]["Comments"] = comments["Numbers"]["Type"][self.media_type]["Years"][self.current_year["Number"]]

		# Increment the number of comments by one if the user has written a comment for the media
		if self.dictionary["Comment Writer"]["States"]["Write"] == True:
			self.dictionaries["Watched"]["Numbers"]["Comments"] += 1

		# ---------- #

		# Update the "Entries.json" file with the current entries
		self.JSON.Edit(self.folders["Watch History"]["Current year"]["Entries"], self.dictionaries["Entries"])

		# Update the media type "Entries.json" file with the current media type entries
		self.JSON.Edit(self.dictionary["Media type"]["Folders"]["By media type"]["Entries"], self.dictionaries["Media type"][self.media_type])

		# Update the media "Watched.json" file with the current watched entries
		self.JSON.Edit(self.media["Item"]["Folders"]["Watched"]["entries"], self.dictionaries["Watched"])

		# ---------- #

		# Make a list of "Entry list.txt" files to add to
		files = [
			self.folders["Watch History"]["Current year"]["Entry list"],
			self.dictionary["Media type"]["Folders"]["By media type"]["Entry list"],
			self.media["Item"]["Folders"]["Watched"]["entry_list"]
		]

		# Iterate through those files
		for file in files:
			# Get the lines of the file
			lines = self.File.Contents(file)["Lines"]

			# If the entry name is not inside the text file, add it
			if self.entry_name not in lines:
				self.File.Edit(file, self.entry_name, "a")

	def Create_Entry_File(self):
		# This is a template for organizing the episode information in a text file
		# Each section contains placeholders that should be replaced with actual data
		# The structure includes details about the episode, media type, watching times and states
		# Optional values are indicated in parentheses

		# Watched media number:
		# [Watched media number]
		# 
		# Watched media number by media type:
		# [Watched media number by media type]
		# 
		# Media type:
		# [Media type]
		# 
		# Entry:
		# [Watched media number. Media type (Finished watching time)]
		#
		# Media titles:
		# [Media titles]
		# 
		# (
		# Media item titles:
		# [Item titles]
		# 
		# Episode titles:
		# [Episode titles]
		# )
		# 
		# When I started watching:
		# [Started watching time in local timezone]
		# 
		# When I finished watching:
		# [Finished watching time in the local timezone]
		# 
		# When I finished watching (UTC):
		# [Finished watching time in the UTC time]
		# 
		# Watching session duration:
		# [Watching session duration]
		# 
		# (
		# States:
		# [State texts]
		# )

		# ---------- #

		# Define the watched media folder, file name, and file by media type
		by_media_type_folder = self.dictionary["Media type"]["Folders"]["By media type"]["Files"]["root"]
		file_name = self.dictionary["Entry"]["Name"]["en"]["Sanitized"] + ".txt"
		file = by_media_type_folder + file_name

		# Create the watched media file inside the "By media type" folder
		self.File.Create(file)

		# ---------- #

		# Define the dictionary for the watched media texts
		self.dictionary["Entry"]["Text"] = {
			"General": self.Define_File_Text("General")
		}

		# Fill the entry "Text" dictionary with the entry texts of each language
		for language in self.languages["Small"]:
			self.dictionary["Entry"]["Text"][language] = self.Define_File_Text(language)

		# ---------- #

		# Write the general entry text into the general entry file
		self.File.Edit(file, self.dictionary["Entry"]["Text"]["General"], "w")

		# ---------- #

		# Define the entry file for the "Watched" folder of the media item folder
		watched_folder = self.media["Item"]["Folders"]["Watched"]["files"]["root"]
		file_name = self.dictionary["Entry"]["Name"][self.language["Small"]]["Sanitized"] + ".txt"
		file = watched_folder + file_name

		# Create the watched entry file
		self.File.Create(file)

		# Write the entry text in the user's language into the watched entry file
		self.File.Edit(file, self.dictionary["Entry"]["Text"][self.language["Small"]], "w")

	def Define_Titles(self, language_parameter, language, titles_dictionary):
		# Initialize a variable to hold the media (item) titles
		media_titles = []

		# Initialize the key to access the original media (item) title
		key = "Original"

		# Check if there is a romanized title available
		if "Romanized" in titles_dictionary:
			# If a romanized title exists, add the original title to the list of titles
			media_titles.append(titles_dictionary["Original"])

			# Update the key to access the romanized title for later use
			key = "Romanized"

		# Add the original or romanized title to the list of titles
		media_titles.append(titles_dictionary[key])

		# Check if the language parameter is "General"
		# And if the language title is different from the original or romanized title
		if (
			language_parameter == "General" and
			titles_dictionary["Language"] != titles_dictionary[key]
		):
			# Add the language title to the list of titles
			media_titles.append(titles_dictionary["Language"])

			# Iterate through the small languages list
			for local_language in self.languages["Small"]:
				# Check if the local language exists in the titles dictionary
				# And if the title in that language is different from the language title
				if (
					local_language in titles_dictionary and
					titles_dictionary[local_language] != titles_dictionary["Language"]
				):
					# Add the current local language title to the list of titles
					media_titles.append(titles_dictionary[local_language])

		# Check if the language parameter is not "General"
		# And if the specified language exists in the media (item) titles
		if (
			language_parameter != "General" and
			language in titles_dictionary
		):
			# Add the language title to the list of titles
			media_titles.append(titles_dictionary[language])

		# Return the list of titles
		return media_titles

	def Define_File_Text(self, language_parameter = None):
		# Check if a specific language parameter is provided
		if language_parameter != "General":
			language = language_parameter # Use the provided language parameter

		# If the language parameter is "General", use the user's preferred language
		if language_parameter == "General":
			language = self.language["Small"]

		# Retrieve the full language name from the languages dictionary
		full_language = self.languages["Full"][language]

		# ---------- #

		# Define the list of entry text lines
		lines = [
			# Add the watched media number
			self.texts["watched_media_number"][language] + ":" + "\n" + str(self.dictionaries["Entries"]["Numbers"]["Total"]) + "\n",

			# Add the watched media number by media type
			self.texts["watched_media_number_by_media_type"][language] + ":" + "\n" + str(self.dictionaries["Media type"][self.media_type]["Numbers"]["Total"]) + "\n",

			# Add the media type
			self.texts["media_type"][language] + ":" + "\n" + self.dictionary["Media type"]["Plural"][language] + "\n",

			# Add the entry text and the entry name
			self.Language.texts["entry, title()"][language] + ":" + "\n" + self.dictionary["Entry"]["Name"]["en"]["Normal"] + "\n"
		]

		# ---------- #

		# Get the list of media titles
		media_titles = self.Define_Titles(language_parameter, language, self.media["Titles"])

		# Determine the appropriate media title text based on the list of media titles
		text = self.texts["media_title"][language]

		# If it has more than one title, use the plural text
		if len(media_titles) > 1:
			text = self.texts["media_titles"][language]

		# Add a newline and the "media title(s)" text
		lines.append(text + ":" + "\n" + "{}")

		# ---------- #

		# Add the item and episode titles lines if the media is a series
		if self.media["States"]["Series media"] == True:
			# Check if the media has a media item list and the media item is not the root media
			if (
				self.media["States"]["Has a list of media items"] == True and
				self.media["States"]["The media item is the root media"] == False
			):
				# Get the list of media item titles
				item_titles = self.Define_Titles(language_parameter, language, self.media["Item"]["Titles"])

				# Determine if we should use singular or plural based on the number of titles
				text = self.texts["media_item_title"][language]

				# If it has more than one title, use the plural text
				if len(item_titles) > 1:
					text = self.texts["media_item_titles"][language]

				# Add a newline and the "media title(s)" text
				lines.append(text + ":" + "\n" + "{}")

			# Check if the media is not a single unit
			if self.media["States"]["Single unit"] == False:
				# Determine the appropriate episode title text based on the language parameter
				text = self.texts["episode_titles"][language]

				if language_parameter != "General":
					text = self.texts["episode_title"][language]

				# Create a list to store unique episode titles
				titles = []

				# Iterate through the episode titles and add unique titles to the list
				for title in list(self.media["Episode"]["Titles"].values()):
					if title not in titles:
						titles.append(title)

				# Determine if we should use a singular or plural text based on the number of titles
				if len(titles) == 1:
					text = self.texts["episode_title"][language] # Singular text

				else:
					# Use plural only if the language parameter is "General"
					if language_parameter == "General":
						text = self.texts["episode_titles"][language] # Plural text

					else:
						text = self.texts["episode_title"][language] # Singular text for non-general

				# Add the "Episode title(s)" text to the list of lines
				lines.append(text + ":" + "\n" + "{}")

		# ---------- #

		# Add the "When I started watching" (local timezone) title and format string
		started_watching_text = self.texts["when_i_started_watching"][language] + ":" + "\n" + "{}"
		lines.append(started_watching_text)

		# Add the "When I finished watching" (local timezone) title and format string
		finished_watching_timezone_text = self.texts["when_i_finished_watching"][language] + ":" + "\n" + "{}"
		lines.append(finished_watching_timezone_text)

		# Add the "When I finished watching (UTC)" title and format string
		finished_watching_utc_text = self.texts["when_i_finished_watching"][language] + " (" + self.Date.texts["utc"][language] + ")" + ":" + "\n" + "{}"
		lines.append(finished_watching_utc_text)

		# Add the "Watching session duration" title and format string
		duration_text = self.texts["watching_session_duration"][language] + ":" + "\n" + "{}"
		lines.append(duration_text)

		# ---------- #

		# Add the state texts lines if there are any state texts defined
		if self.dictionary["States"]["Texts"] != {}:
			# Initialize the text for the states section
			text = "\n" + self.Language.texts["states, title()"][language] + ":" + "\n"

			# Iterate through each state text in the dictionary
			for key in self.dictionary["States"]["Texts"]:
				# Get the text for the current state in the specified language
				language_text = self.dictionary["States"]["Texts"][key][language]

				# Append the current state text to the overall text
				text += language_text

				# Add a newline if this is not the last state text
				if key != list(self.dictionary["States"]["Texts"].keys())[-1]:
					text += "\n"

			# Append the constructed state text to the list of lines
			lines.append(text)

		# ---------- #

		# Define the language entry text by converting the list of lines to a single text block
		file_text = self.Text.From_List(lines, next_line = True)

		# ---------- #

		# Initialize the list of items to hold all items for template formatting
		items = []

		# ---------- #

		# Now create the string with the media titles to add to the list of items
		titles = "\n".join(media_titles) + "\n"

		# Add the media titles to the list of items
		items.append(titles)

		# ---------- #

		# Check if the media is a series media
		if self.media["States"]["Series media"] == True:
			# Check if the media has a media item list and the media item is not the root media
			if (
				self.media["States"]["Has a list of media items"] == True and
				self.media["States"]["The media item is the root media"] == False
			):
				# Now create the string with the media item titles to add to the list of items
				titles = "\n".join(item_titles) + "\n"

				# Add the media item titles to the list of items
				items.append(titles)

			# Check if the media is not a single unit
			if self.media["States"]["Single unit"] == False:
				# Initialize the string to hold episode titles
				episode_titles = ""

				# If the language parameter is not "General", get the episode title in the specified language
				if language_parameter != "General":
					episode_title = self.media["Episode"]["Titles"][language]

					# If the episode title is empty, set a placeholder
					if episode_title == "":
						episode_title = "[" + self.Language.texts["empty, title()"][language] + "]"

					episode_titles = episode_title + "\n" # Add the episode title to the string

				# If the language parameter is "General", add titles for all languages
				if language_parameter == "General":
					for local_language in self.languages["Small"]:
						episode_title = self.media["Episode"]["Titles"][local_language]

						# If the episode title is empty, set a placeholder
						if episode_title == "":
							episode_title = "[" + self.Language.texts["empty, title()"][language] + "]"

						# Add the episode title if it is not already included
						if episode_title + "\n" not in episode_titles:
							episode_titles += episode_title + "\n"

				# Append the constructed episode titles to the list of items
				items.append(episode_titles)

		# ---------- #

		# Add the started watching time
		items.append(self.entry_dictionary["Times"]["Started watching"] + "\n")

		# Iterate over the relevant keys to obtain the times
		for time_key in ["Finished watching", "Finished watching (UTC)"]:
			# Check if the key exists
			if time_key in self.dictionary["Entry"]["Times"]:
				# Define the timezone key as "Timezone"
				timezone_key = "Timezone"

				# Define the format as the timezone one
				format = "HH:MM DD/MM/YYYY"

				# If the "UTC" text is inside the time key
				if "UTC" in time_key:
					# Update the timezone key to be the UTC one
					timezone_key = "UTC"

					# Define the format as the UTC one
					format = "YYYY-MM-DDTHH:MM:SSZ"

				# Retrieve the formatted datetime string from the "Times" dictionary,
				# using the specified time key (e.g., "Finished watching"), timezone key (e.g., "UTC"),
				# and format (e.g., "YYYY-MM-DDTHH:MM:SSZ")
				time = self.dictionary["Entry"]["Times"][time_key][timezone_key]["DateTime"]["Formats"][format]

				# Append the times to the list of items
				items.append(time + "\n")

		# Add the watching session duration (the difference between the start and finished watching times)
		items.append(self.entry_dictionary["Times"]["Watching session duration"][language])

		# ---------- #

		# Return the formatted text with the items, including the times
		return file_text.format(*items)

	def Add_Entry_File_To_Year_Folder(self):
		# Iterate through the list of small languages
		for language in self.languages["Small"]:
			# Get the full language
			full_language = self.languages["Full"][language]

			# Define a shortcut for the folder
			folder = self.current_year["Folders"][language]["Watched media"]

			# Define the media type folder name
			media_type_folder = self.dictionary["Media type"]["Plural"][language]

			# Define and create the media type folder
			folder["Media type"] = {
				"root": folder["root"] + media_type_folder + "/"
			}

			self.Folder.Create(folder["Media type"]["root"])

			# Update the folder to be the media type folder
			folder = folder["Media type"]

			# Get the entry file name
			entry_file_name = self.dictionary["Entry"]["Name"][language]["Sanitized"]

			# Define and create the entry file
			folder["Entry file"] = folder["root"] + entry_file_name + ".txt"
			self.File.Create(folder["Entry file"])

			# Write the entry text by language inside the year entry file
			self.File.Edit(folder["Entry file"], self.dictionary["Entry"]["Text"][language], "w")

			# ---------- #

			# Create the "First of the Year" entry file
			if self.media["States"]["First media type entry in year"] == True:
				# Define the folder shortcut
				folder = self.current_year["Folders"][language]["Firsts of the Year"]["Media"]

				# Define and create the "First of the Year" entry file
				folder["Entry file"] = folder["root"] + entry_file_name + ".txt"
				self.File.Create(folder["Entry file"])

				# Write the entry text by language inside the "First of the Year" entry file
				self.File.Edit(folder["Entry file"], self.dictionary["Entry"]["Text"][language], "w")

	def Check_Media_Status(self):
		if self.media["States"]["Series media"] == True:
			# If the media has a list of media items
			# And the episode title is the last one
			if (
				self.media["States"]["Has a list of media items"] == True and
				self.media["Episode"]["Title"] == self.media["Item"]["Episodes"]["Titles"][self.media["Language"]][-1]
			):
				# And the media is not a YouTube channel
				if self.media["States"]["Video"] == False:
					# If the media item is the last media item, define the media as completed
					if self.media["Item"]["Title"] == self.media["Items"]["List"][-1]:
						self.media["States"]["Completed media"] = True

					# If the media item is not the last media item (media is not completed), get next media item
					if self.media["Item"]["Title"] != self.media["Items"]["List"][-1]:
						item_title = self.media["Items"]["List"][self.media["Item"]["Number"] + 1]

						sanitized_title = self.Sanitize_Title(item_title)

						# Define the next media item prototype dictionary
						self.media["Item"]["Next"] = {
							"Title": item_title,
							"Titles": {},
							"Sanitized": sanitized_title,
							"Folders": {
								"root": self.media["Items"]["Folders"]["root"] + sanitized_title + "/",
								"Media": {
									"root": self.media["Folders"]["Media"]["root"] + sanitized_title + "/"
								}
							},
							"Number": self.media["Item"]["Number"] + 1
						}

						# Define other variables for the next media item
						self.media["Item"]["Next"] = self.Define_Media_Item(deepcopy(self.dictionary), media_item = item_title)["Media"]["Item"]

						# Update current media item file
						self.File.Edit(self.media["Items"]["Folders"]["current"], self.media["Item"]["Next"]["Title"], "w")

					# Add the "Status" key and value "Completed" to the end of the media item details
					key_value = {
						"key": self.Language.language_texts["status, title()"],
						"value": self.Language.language_texts["completed, title()"]
					}

					self.media["Item"]["Details"] = self.JSON.Add_Key_After_Key(self.media["Item"]["Details"], key_value, add_to_end = True)

				# If the "Episode" key is inside the media item details
				# And the media item is a single unit
				if (
					self.Language.language_texts["episode, title()"] in self.media["Item"]["Details"] and
					self.media["States"]["Single unit"] == True
				):
					# Remove the "Episode" key
					self.media["Item"]["Details"].pop(self.Language.language_texts["episode, title()"])

				# Update the media item details file with the updated media item details dictionary
				self.File.Edit(self.media["Item"]["Folders"]["details"], self.Text.From_Dictionary(self.media["Item"]["Details"]), "w")

				# If the media is not a video channel
				# And the media item is not the last one on the list of media items
				if (
					self.media["States"]["Video"] == False and
					len(self.media["Items"]["List"]) != 1
				):
					# Define the media item as completed
					self.media["States"]["Completed media item"] = True

			# If the media has no media item list
			# And the episode title is the last one
			# And the media is not a video channel
			if (
				self.media["States"]["Has a list of media items"] == False and
				self.media["Episode"]["Title"] == self.media["Item"]["Episodes"]["Titles"][self.media["Language"]][-1] and
				self.media["States"]["Video"] == False
			):
				# Define the media as completed
				self.media["States"]["Completed media"] = True

		# If the media is a movie, define it as completed
		if self.media["States"]["Series media"] == False:
			self.media["States"]["Completed media"] = True

		# If the media and media item are not completed, get next episode number
		if (
			self.media["States"]["Completed media"] == False and
			self.media["States"]["Completed media item"] == False and
			len(self.media["Item"]["Episodes"]["Titles"][self.media["Language"]]) != 1
		):
			try:
				# Get next episode language title
				self.media["Episode"]["Next"] = self.media["Item"]["Episodes"]["Titles"][self.media["Language"]][self.media["Episode"]["Number"]]

				# Define current episode to watch as the next episode
				self.media["Item"]["Details"][self.Language.language_texts["episode, title()"]] = self.media["Episode"]["Next"]

				# Update media item details file
				self.File.Edit(self.media["Item"]["Folders"]["details"], self.Text.From_Dictionary(self.media["Item"]["Details"]), "w")

			except IndexError:
				pass

		# If the media is completed, define its status as completed
		if self.media["States"]["Completed media"] == True:
			if self.Language.language_texts["remote_origin"] in self.media["Details"]:
				if self.media["Details"][self.Language.language_texts["remote_origin"]] == "Animes Vision":
					self.media["Details"].pop(self.Language.language_texts["remote_origin"])

				elif self.media["Details"][self.Language.language_texts["remote_origin"]] == "YouTube":
					self.media["Details"].pop(self.Language.language_texts["remote_origin"])

			# Define the new status as "Completed"
			self.media["Status change"] = {
				"Old": self.media["Details"][self.Language.language_texts["status, title()"]],
				"New": self.Language.language_texts["completed, title()"]
			}

			# Update the status key in the media details
			self.Change_Status(self.dictionary)

		# Check if the media item has a correspondent movie inside the movies folder
		if (
			self.media["States"]["Series media"] == True and
			"Type" in self.media["Item"] and
			self.media["Item"]["Type"][self.language["Small"]] == self.language_texts["movie"]
		):
			self.movies = self.Get_Media_List(self.media_types[self.texts["movies, title()"]["en"]], self.texts["plan_to_watch, title()"]["en"])

			for movie_title in self.movies:
				# If the media item title is inside the movies list and the media type is not "Movies"
				if self.media["Item"]["Title"] in movie_title:
					# Define the movie prototype dictionary
					self.movie_dictionary = {
						"Media type": self.media_types[self.texts["movies, title()"]["en"]],
						"Media": {
							"Title": movie_title
						}
					}

					# Define other variables for the movie
					self.movie_dictionary = self.Select_Media(self.movie_dictionary)

					# Copy the contents of the media comments folder to the movie comments folder
					self.Folder.Copy(self.media["Item"]["Folders"]["comments"]["root"], self.movie_dictionary["Media"]["Item"]["Folders"]["comments"]["root"])

					# Change the status of the movie to "Completed"
					self.Change_Status(self.movie_dictionary)

		# Check if the movie has a correspondent media item inside the series media folders
		if self.media["States"]["Series media"] == False:
			# Define the empty series list of media
			self.series_media_list = {}

			# Define the list of media types to not get a list of media
			remove_list = [
				self.texts["movies, title()"]["en"],
				self.texts["videos, title()"]["en"]
			]

			# Define the status list to use to get the media with the statuses on the list
			status_list = [
				self.Language.texts["on_hold, title()"]["en"],
				self.texts["watching, title()"]["en"],
				self.texts["re_watching, title()"]["en"]
			]

			# Iterate through the English plural media types list
			for plural_media_type in self.media_types["Plural"]["en"]:
				if plural_media_type not in remove_list:
					media_list = self.Get_Media_List(self.media_types[plural_media_type], status_list)

					# Extend the series list of media with the current list of media
					self.series_media_list[plural_media_type] = media_list

			# Iterate through the English plural media types list
			for plural_media_type in self.media_types["Plural"]["en"]:
				if plural_media_type in self.series_media_list:
					# Get the list of media of the current media type
					media_list = self.series_media_list[plural_media_type]

					# Iterate through the list of media
					for media_title in media_list:
						media_folder = self.media_types[plural_media_type]["Folders"]["Media information"]["root"] + self.Sanitize_Title(media_title) + "/"

						media_items_folder = media_folder + self.media_types[plural_media_type]["Subfolders"]["Plural"] + "/"

						# If the media items folder exists
						if self.Folder.Exists(media_items_folder) == True:
							media_items_file = media_items_folder + self.media_types[plural_media_type]["Subfolders"]["Plural"] + ".txt"

							# Get the list of media of items
							media_items = self.File.Contents(media_items_file)["lines"]

							# Iterate through the list of media of items
							for item_title in media_items:
								item_folder = media_items_folder + self.Sanitize_Title(item_title) + "/"
								item_details_file = item_folder + self.Language.language_texts["details, title()"] + ".txt"

								item_details = self.File.Dictionary(item_details_file)

								# If the media item title is equal to the root media item title (the one that was watched)
								# Or is inside the item title and the year of the movie is the same as the year of the item
								if (
									item_title == self.media["Item"]["Title"] or
									self.media["Item"]["Title"].split(" (")[0] in item_title and
									self.media["Item"]["Details"][self.Date.language_texts["year, title()"]] == item_details[self.Date.language_texts["year, title()"]]
								):
									# Define the media prototype dictionary
									media_dictionary = {
										"Media type": self.media_types[plural_media_type],
										"Media": {
											"Title": media_title
										}
									}

									# Define other variables for the media
									media_dictionary = self.Select_Media(media_dictionary)

									# Define the media item as the current media item
									media_dictionary["Media"]["Item"] = self.Define_Media_Item(deepcopy(media_dictionary), media_item = item_title)["Media"]["Item"]

									# Add the "Status" key and value "Completed" to the end of the details
									key_value = {
										"key": self.Language.language_texts["status, title()"],
										"value": self.Language.language_texts["completed, title()"]
									}

									media_dictionary["Media"]["Item"]["Details"] = self.JSON.Add_Key_After_Key(media_dictionary["Media"]["Item"]["Details"], key_value, add_to_end = True)

									# Update the media item details file
									self.File.Edit(media_dictionary["Media"]["Item"]["Folders"]["details"], self.Text.From_Dictionary(media_dictionary["Media"]["Item"]["Details"]), "w")

	def Check_Media_Dates(self):
		# Define the "Finished watching time" text template
		template = self.language_texts["when_i_finished_watching"] + ":" + "\n" + \
		self.dictionary["Entry"]["Times"]["Finished watching"]["Formats"]["HH:MM DD/MM/YYYY"] + "\n" + \
		"\n" + \
		"{}" + ":" + "\n" + \
		"{}"

		# Gets the date that the user started and finished watching the media item and writes it into the media item dates file
		# If the user completed the media item
		if self.media["States"]["Completed media item"] == True:
			# Gets the item dates from the item dates file
			self.media["Item"]["dates"] = self.File.Dictionary(self.media["Item"]["Folders"]["dates"], next_line = True)

			# Define the key to use to find the started watching time
			key = self.language_texts["when_i_started_watching"]

			# Define the key as the finished watching time for single unit media items
			if self.media["States"]["Single unit"] == True:
				self.media["Item"]["dates"][key] = self.dictionary["Entry"]["Times"]["Finished watching"]["Formats"]["HH:MM DD/MM/YYYY"]

			# Transform started watching time into a date dictionary
			self.media["Item"]["Started watching"] = self.Date.From_String(self.media["Item"]["dates"][key])

			# Get the difference between the two dates
			difference = self.Date.Difference(self.media["Item"]["Started watching"]["Object"], self.dictionary["Entry"]["Times"]["Finished watching"]["Object"])

			# Define time spent watching using started watching time and finished watching time
			self.media["Item"]["Time spent watching"] = difference["Text"][self.language["Small"]]

			if self.media["Item"]["Time spent watching"][0] + self.media["Item"]["Time spent watching"][1] == ", ":
				self.media["Item"]["Time spent watching"] = self.media["Item"]["Time spent watching"][2:]

			# Define a shortcut to the "the item" text
			the_item_text = self.media["Texts"]["the_item"][self.language["Small"]]

			# Define the list of items to use to format the template
			items = [
				# The "How long did it take you to finish" text plus the " the item" text
				# Example
				# "How long did it take you to finish" + " the season"
				self.language_texts["how_long_did_it_take_you_to_finish"] + " " + the_item_text,

				# The time spent watchins
				self.media["Item"]["Time spent watching"]
			]

			# Format the time template with the list of items
			self.media["Item"]["Formatted datetime template"] = "\n\n" + template.format(*items)

			# Define a shortcut to the media item "Dates.txt" file
			dates_file = self.media["Item"]["Folders"]["dates"]

			# Get the file contents
			contents = self.File.Contents(dates_file)

			# Read the media item dates file
			self.media["Item"]["Finished watching text"] = contents["string"]

			# Add the time template to the item dates text
			self.media["Item"]["Finished watching text"] += self.media["Item"]["Formatted datetime template"]

			# Add the "the item" text to the "Finished watching text"
			self.media["Item"]["Finished watching text"] = self.media["Item"]["Finished watching text"].replace(self.language_texts["when_i_started_watching"], self.language_texts["when_i_started_watching"] + " " + the_item_text)

			# Update the media "Dates.txt" file with the new "Finished watching text"
			self.File.Edit(self.media["Item"]["Folders"]["dates"], self.media["Item"]["Finished watching text"], "w")

			# Add the "Finished watching text" to the Diary Slim text if the media is not completed
			# And the media item is not a single unit one
			if (
				self.media["States"]["Completed media"] == False and
				self.media["States"]["Single unit"] == False
			):
				# Add two line breaks and the "Finished watching text" to the Diary Slim "Dates" key
				self.dictionary["Entry"]["Diary Slim"]["Dates"] = "\n\n" + self.media["Item"]["Finished watching text"]

		# Gets the date that the user started and finished watching the media and writes it to the media dates text file
		# If the user completed the media
		# Or the media item title is the same as the media title
		if (
			self.media["States"]["Completed media"] == True or
			self.media["States"]["The media item is the root media"] == True
		):
			# Gets the media dates from the media dates file
			self.media["dates"] = self.File.Dictionary(self.media["Folders"]["dates"], next_line = True)

			# Define the key to use to find the started watching time
			key = self.language_texts["when_i_started_watching"]

			# Transform started watching time into a date dictionary
			self.media["Started watching"] = self.Date.From_String(self.media["dates"][key])

			# Get the difference between the two dates
			difference = self.Date.Difference(self.media["Started watching"]["Object"], self.dictionary["Entry"]["Times"]["Finished watching"]["Object"])

			# Define time spent watching using started watching time and finished watching time
			self.media["Time spent watching"] = difference["Text"][self.language["Small"]]

			if self.media["Time spent watching"][0] + self.media["Time spent watching"][1] == ", ":
				self.media["Time spent watching"] = self.media["Time spent watching"][2:]

			# Define a shortcut to the "the item" text
			the_item_text = self.media["Texts"]["Container texts"]["The"]

			# Define the list of items to use to format the template
			items = [
				# The "How long did it take you to finish" text plus the " the container" text
				# Example
				# "How long did it take you to finish" + " the anime"
				self.language_texts["how_long_did_it_take_you_to_finish"] + " " + the_item_text,

				# The time spent watchins
				self.media["Time spent watching"]
			]

			# Format the time template with the list of items
			self.media["Formatted datetime template"] = "\n\n" + template.format(*items)

			# Define a shortcut to the media "Dates.txt" file
			dates_file = self.media["Folders"]["dates"]

			# Get the file contents
			contents = self.File.Contents(dates_file)

			# Get the lines of the file
			lines = contents["Lines"]

			# If the number of lines is more than two
			if len(lines) > 2:
				# While the number of lines is more than two
				while len(lines) > 2:
					# Remove the lines to remove the "Finished watching" and "Duration" times
					lines.pop(2)

				# Update the "String" key to be a text version of the list of lines
				contents["String"] = self.Text.From_List(lines, next_line = True)

			# Define the "Finished watching text" as the text string of the file
			self.media["Finished watching text"] = contents["String"]

			# Add the time template to the media dates text
			self.media["Finished watching text"] += self.media["Formatted datetime template"]

			# Add the "the container" text to the finished watching text
			self.media["Finished watching text"] = self.media["Finished watching text"].replace(self.language_texts["when_i_started_watching"], self.language_texts["when_i_started_watching"] + " " + the_item_text)

			# Update the media "Dates.txt" file with the new "Finished watching text"
			self.File.Edit(self.media["Folders"]["dates"], self.media["Finished watching text"], "w")

			# If the "Dates" key is not inside the Diary Slim "Text" dictionary, add it as an empty string
			if "Dates" not in self.dictionary["Entry"]["Diary Slim"]["Text"]:
				self.dictionary["Entry"]["Diary Slim"]["Dates"] = ""

			# Add two line breaks and the "Finished watching text" to the Diary Slim "Dates" key
			self.dictionary["Entry"]["Diary Slim"]["Dates"] += "\n\n" + self.media["Finished watching text"]

	def Define_Diary_Slim_Text(self):
		# Define the text template as "I just finished watching {}"
		template = self.language_texts["i_just_finished_watching_{}"]

		# Replaced the "watching" text with the "re-watching [number of times]" text if the "Re-watching" state is True
		# Example:
		# I just finished re-watching one time
		# I just finished re-watching two times
		if self.media["States"]["Re-watching"] == True:
			watching = self.language_texts["watching, infinitive"]
			re_watching = self.language_texts["re_watching, infinitive"] + " " + self.media["Episode"]["Re-watching"]["Texts"]["Times"][self.language["Small"]]

			template = template.replace(watching, re_watching)

		# ---------- #

		# If the media is a series media
		if self.media["States"]["Series media"] == True:
			# Add quotes and another format character to the text template
			template += ' "{}"'

			# Define the "this text" as the "this" text in the masculine gender
			this_text = self.Language.language_texts["genders, type: dictionary, masculine"]["this"]

			# Define the unit text as the media unit text in the user language
			unit_text = self.media["Texts"]["unit"][self.language["Small"]]

			# If the media item is a single unit one
			if self.media["States"]["Single unit"] == True:
				# Define the unit text as the media item type text in the user language
				unit_text = self.media["Item"]["Type"][self.language["Small"]].lower()

			# Define the text as the "of the" text in the default gender, in the user language
			of_the_text = self.dictionary["Media type"]["Genders"][self.language["Small"]]["of_the"]

			# If the media type is not "Series", define the text as the masculine "of the" text
			# (The default gender for "Series" media is feminine)
			if self.dictionary["Media type"]["Plural"]["en"] != "Series":
				of_the_text = self.media_types["Genders"][self.language["Small"]]["masculine"]["of_the"]

			# Define the watched item text as the "this text" plus the "unit text" plus the "of the" text
			watched_item_text = this_text + " " + unit_text + " " + of_the_text

			# ----- #

			# If the media item is not a single unit one
			# And the media is not a video channel
			if (
				self.media["States"]["Single unit"] == False and
				self.media["States"]["Video"] == False
			):
				# Define a shortcut to the list of titles
				titles = self.media["Item"]["Episodes"]["Titles"][self.media["Language"]]

				# Replace the "this" text with "the first" text if the episode is the first one
				if self.media["Episode"]["Title"] == titles[0]:
					watched_item_text = watched_item_text.replace(this_text, self.Language.language_texts["the_first, masculine"])

				# Replace the "this" text with "the last" text if the episode is the last one
				# Or the number of titles is only one
				# (Normally this would mean that the media item is a single unit one, I have never seen a media item (season) that has only one episode, it rarely happens)
				if (
					self.media["Episode"]["Title"] == titles[-1] or
					len(titles) == 1
				):
					# Replace the "this" text with "the last" text if the episode is the last one
					watched_item_text = watched_item_text.replace(this_text, self.Language.language_texts["the_last, masculine"])

			# ----- #

			# If the "Movie" text is inside the media episode title in the user language
			if "Movie" in self.media["Episode"]["Titles"][self.media["Language"]]:
				# Replace the "episode" text with the "movie" text
				watched_item_text = watched_item_text.replace(self.language_texts["episode"], self.language_texts["movie"])

			# ----- #

			# Define the "of the" text template
			of_the_text = self.Language.language_texts["of_the_{}"]

			# If the media has a list of media items
			# And the media item is not the root media
			# And the media item is not a single unit one
			if (
				self.media["States"]["Has a list of media items"] == True and
				self.media["States"]["The media item is the root media"] == False and
				self.media["States"]["Single unit"] == False
			):
				# If the media is not a video channel
				if self.media["States"]["Video"] == False:
					# Define a media item text as an empty string by default
					media_item_text = ""

					# Replace the "of the" text with "of the first" if the media item is the first one
					if self.media["Item"]["Title"] == self.media["Items"]["List"][0]:
						media_item_text = self.Language.language_texts["first, feminine"] + " "

					# Replace the "of the" text with "of the last" if the media item is the last one
					if self.media["Item"]["Title"] == self.media["Items"]["List"][-1]:
						media_item_text = self.Language.language_texts["last, feminine"] + " "

					# Get the lowercase season text
					season_text = self.language_texts["season, title()"].lower()

					# Format the "of the" text to add the media item text and the "season" text
					of_the_text = of_the_text.format(media_item_text + season_text)

					# Define a shortcut to the unit text
					unit_text = self.media["Texts"]["unit"][self.language["Small"]]

					# Add the "of the" text to the right of the unit ("episode") text
					watched_item_text = watched_item_text.replace(unit_text, unit_text + " {}".format(of_the_text))

					# Define the media item title
					media_item_title = self.Define_Title(self.media["Item"]["Titles"])

					# Define a shortcut to the uppercase " Season" text
					uppercase_season_text = " " + self.language_texts["season, title()"]

					# If the uppercase " Season" text is not inside the media item title
					if uppercase_season_text not in media_item_title:
						# Add quotes around the media item title
						media_item_title = '"' + media_item_title + '"'

					# Add the media item title after the "of the" text
					watched_item_text = watched_item_text.replace(of_the_text, of_the_text + " " + media_item_title)

					# If the " Season" text is inside the media item title
					if uppercase_season_text in media_item_title:
						# Remove the lowercase season text
						watched_item_text = watched_item_text.replace(" " + season_text.lower(), "")

				# If the media is a video channel
				if self.media["States"]["Video"] == True:
					# Format the "of the" text to add the "video series" text
					of_the_text = of_the_text.format(self.language_texts["video_series, type: singular"])

				# Remove the media title with space in the media item if it exists
				if self.media["Title"] + " " in self.media["Item"]:
					watched_item_text = watched_item_text.replace(self.media["Title"] + " ", "")

			# If the "Dubbing" dictionary is present inside the "Episode" dictionary
			if "Dubbing" in self.media["Episode"]:
				# Add the dubbing text to the text template
				template += self.media["Episode"]["Dubbing"]["Text"]

			# Define a shortcut to the "Container texts" dictionary 
			container_texts = self.media["Texts"]["Container texts"]

			# Add the container (media type or "YouTube channel" text for the "Videos" media type) to the watched item text
			watched_item_text += " " + container_texts["Container"]

			# Define the "Diary Slim" text as the template formatted with the "watched item text" and the media title by language
			self.dictionary["Entry"]["Diary Slim"]["Text"] = template.format(watched_item_text, self.media["Titles"]["Language"])

		# ---------- #

		# If the media is a movie (not a series media)
		# Only add the "this" text and the media type "movie" text in user language
		if self.media["States"]["Series media"] == False:
			# Define a shortcut to the "this" text
			this_text = self.dictionary["Media type"]["Genders"][self.language["Small"]]["this"]

			# Define a shortcut to the media type text
			media_type_text = self.dictionary["Media type"]["Singular"][self.language["Small"]].lower()

			# Add the two to define the Diary Slim text
			self.dictionary["Entry"]["Diary Slim"]["Text"] = template.format(this_text + " " + media_type_text)

		# ---------- #

		# Define a local language as the media language
		language = self.media["Language"]

		# If the media language is not the user language
		if self.media["Language"] != self.language["Small"]:
			# Change the local language to the user language
			language = self.language["Small"]

		# ---------- #

		# Get the media or user language episode title
		episode_title = self.media["Episode"]["Titles"][language]

		# If the length of the title is greater than one
		# And the first two characters of the title are a space and a colon
		if (
			len(episode_title) > 1 and
			episode_title[0] + episode_title[1] == ": "
		):
			# Remove them
			episode_title = episode_title[2:]

		# Add a colon, a line break, and the episode title to the Diary Slim text
		self.dictionary["Entry"]["Diary Slim"]["Text"] += ":\n" + episode_title

		# ---------- #

		# For movies, add additional details about the movie that are present inside the parentheses of the original movie title
		if self.media["States"]["Series media"] == False:
			self.dictionary["Entry"]["Diary Slim"]["Text"] += " (" + self.media["Episode"]["Titles"]["Original"].split("(")[1]

		# If the "Re-watching" state is True, add the number text of re-watched times in the user language
		if self.media["States"]["Re-watching"] == True:
			self.dictionary["Entry"]["Diary Slim"]["Text"] += self.media["Episode"]["Re-watching"]["Texts"]["Number"][self.language["Small"]]

		# If the "Remote" dictionary is inside the "Episode" dictionary
		# And there is a link inside the "Remote" dictionary
		# And the remote title is not "Animes Vision"
		if (
			"Remote" in self.media["Episode"] and
			"Link" in self.media["Episode"]["Remote"] and
			self.media["Episode"]["Remote"]["Title"] != "Animes Vision"
		):
			# Add two line breaks and the remote link
			self.dictionary["Entry"]["Diary Slim"]["Text"] += "\n\n" + self.media["Episode"]["Remote"]["Link"]

		# If there are states, add the state texts to the Diary Slim text
		if self.dictionary["States"]["States"] != {}:
			# Add two line breaks and the "States:" text, followed by another like break
			self.dictionary["Entry"]["Diary Slim"]["Text"] += "\n\n" + self.Language.language_texts["states, title()"] + ":" + "\n"

			# Define a shortcut to the state "Texts" dictionary
			texts =	self.dictionary["States"]["Texts"]

			# List the state keys
			keys = list(texts.keys())

			# Iterate through the state keys inside the state "Texts" dictionary
			for key in keys:
				# Add the state text in the user language to the Diary Slim text
				self.dictionary["Entry"]["Diary Slim"]["Text"] += texts[key][self.language["Small"]]

				# If the is not the last one, add a line break after the state text
				if key != keys[-1]:
					self.dictionary["Entry"]["Diary Slim"]["Text"] += "\n"

		# If there are dates inside the "Diary Slim" dictionary, add them to the Diary Slim text
		if "Dates" in self.dictionary["Entry"]["Diary Slim"]:
			self.dictionary["Entry"]["Diary Slim"]["Text"] += self.dictionary["Entry"]["Diary Slim"]["Dates"]

	def Post_On_Social_Networks(self):
		# Define the "Social Networks" dictionary
		self.social_networks = {
			"List": [
				"Discord",
				"WhatsApp",
				"Instagram",
				"Facebook"
			],
			"List text": ""
		}

		# Define the list text, with all the Social Networks separated by commas
		self.social_networks["List text"] = self.Text.From_List(self.social_networks["List"])

		# Remove the "Discord" social networks
		self.social_networks["List"].remove("Discord")

		# Define the list text, with all the Social Networks separated by commas
		# But without Discord
		self.social_networks["List text (without Discord)"] = self.Text.From_List(self.social_networks["List"])

		# Define the item text to be used
		self.social_networks["Item text"] = self.language_texts["the_episode_cover"]

		if self.media["States"]["Series media"] == False:
			self.social_networks["Item text"] = self.social_networks["Item text"].replace(self.language_texts["episode"], self.language_texts["movie"])

		if self.media["States"]["Video"] == True:
			self.social_networks["Item text"] = self.social_networks["Item text"].replace(self.language_texts["episode"], self.Language.language_texts["video, title()"].lower())

		# Define the "posted" template
		self.social_networks["Template"] = self.language_texts["i_posted_the_watched_text, type: template"] + "."

		# Define the template list of items
		self.social_networks["Items"] = [
			self.social_networks["Item text"],
			"Discord",
			self.social_networks["List text (without Discord)"],
			"Twitter, Bluesky, " + self.Language.language_texts["and"] + " Threads"
		]

		# Format the template with the list of items
		self.dictionary["Entry"]["Diary Slim"]["Posted on the Social Networks text"] = self.social_networks["Template"].format(*self.social_networks["Items"])

		# Define the text to show while asking the user if they want to post on the social networks
		text = self.language_texts["post_on_the_social_networks"] + " (" + self.social_networks["List text"] 

		# Add the "and others" text
		text += ", " + self.Language.language_texts["and_others, feminine"]

		# Add the closing parenthesis
		text += ")"

		# Define the "ask for input" switch as False
		ask_for_input = False

		# Define the "Post on the social networks" state as True
		self.dictionary["Entry"]["States"]["Post on the Social Networks"] = True

		# If the "Testing" switch is False
		# If the "ask for input" switch is True
		if (
			self.switches["Testing"] == False and
			ask_for_input == True
		):
			# Show a separator
			print()
			print(self.separators["5"])

			# Ask if the user wants to post the watched media status on the social networks
			self.dictionary["Entry"]["States"]["Post on the Social Networks"] = self.Input.Yes_Or_No(text)

		# If the user answer is yes
		if self.dictionary["Entry"]["States"]["Post on the Social Networks"] == True:
			# Import the "Open_Social_Network" sub-class of the "Social_Networks" module
			from Social_Networks.Open_Social_Network import Open_Social_Network as Open_Social_Network

			# Define the Social Networks dictionary
			social_networks = {
				"List": [
					"WhatsApp",
					"Facebook",
					"Discord"
				],
				"Custom links": {
					"Discord": "https://discord.com/channels/311004778777935872/641352970352459776" # "#watch-history" channel on my Discord server
				}
			}

			# Open the Social Networks, one by one
			# (Commented out because this class is not working properly)
			#Open_Social_Network(social_networks)

		# Show a five dash space separator
		print()
		print(self.separators["5"])
		print()

	def Write_On_Diary_Slim(self):
		# Add "Posted on Social Networks" text if the user wanted to post the entry text on the Social Networks
		if self.dictionary["Entry"]["States"]["Post on the Social Networks"] == True:
			self.dictionary["Entry"]["Diary Slim"]["Text"] += "\n\n" + self.dictionary["Entry"]["Diary Slim"]["Posted on the Social Networks text"]

		from Diary_Slim.Write_On_Diary_Slim_Module import Write_On_Diary_Slim_Module as Write_On_Diary_Slim_Module

		# Define the "Write on Diary Slim" dictionary
		dictionary = {
			"Text": self.dictionary["Entry"]["Diary Slim"]["Text"],
			"Time": self.dictionary["Entry"]["Times"]["Finished watching"]["Formats"]["HH:MM DD/MM/YYYY"],
			"Add": {
				"Dot": False
			}
		}

		# Write the entry text on Diary Slim
		Write_On_Diary_Slim_Module(dictionary)

	def Get_The_Media_Title(self, is_media_item = False, media_item = None, language = False, no_media_title = False):
		# Define the key to get the media title
		key = "Original"

		if "Romanized" in self.media["Titles"]:
			key = "Romanized"

		# If the "language" parameter is True
		if language == True:
			# Define the media title key as the "Language" one
			key = "Language"

		# Define the local media title variable
		media_title = self.media["Titles"][key]

		# If the "is media item" parameter is True
		# And there is a media item inside the media dictionary
		# And the media item is not the root media
		if (
			is_media_item == True and
			"Item" in self.media and
			self.media["States"]["The media item is the root media"] == False
		):
			# If the media item parameter is None
			if media_item == None:
				media_item = self.media["Item"]

			# Define the key to get the media item title
			key = "Original"

			if "Romanized" in media_item["Titles"]:
				key = "Romanized"

			# If the "language" parameter is True
			if language == True:
				# Define the media title key as the "Language" one
				key = "Language"

			# Get the media item title using the key
			media_item_title = media_item["Titles"][key]

			# If the first two characters of the title are not a colon and a space
			if media_item_title[0] + media_item_title[1] != ": ":
				# Add a space
				media_title += " "

			# If the "no media title" parameter is True
			if no_media_title == True:
				# Reset the media title to an empty string
				media_title = ""

			# Add the media item title to the root media title
			media_title += media_item_title

			# If the "no media title" parameter is True
			# And the first two characters of the media title are a colon and a space
			if (
				no_media_title == True and
				media_title[0] + media_title[1] == ": "
			):
				# Remove the colon and space
				media_title = media_title[2:]

		# Return the media title
		return media_title

	def Update_Statistic(self):
		# Define a local media dictionary
		media = {
			"Titles": {
				"Original": self.Get_The_Media_Title(),
				"Language": self.Get_The_Media_Title(language = True)
			}
		}

		# Copy the "texts" dictionary of the root media dictionary to the local one
		media["Texts"] = self.media["Texts"]

		# If there is a media item inside the media dictionary
		if "Item" in self.media:
			# Copy the "Item" dictionary of the root media dictionary to the local one
			media["Item"] = self.media["Item"]

			# Create a media item titles dictionary and add it to the "Item" key
			media["Titles"]["Item"] = {
				"Original": self.Get_The_Media_Title(is_media_item = True),
				"Original (no media title)": self.Get_The_Media_Title(is_media_item = True, no_media_title = True),
				"Language": self.Get_The_Media_Title(is_media_item = True, language = True)
			}

		# If the media contains media items
		if "Items" in self.media:
			# Pass the "Items" dictionary to the local media dictionary
			media["Items"] = self.media["Items"]

		# Define the media type dictionary
		media_type = {
			"Plural": self.media_type,
			"The": self.media["Texts"]["Container texts"]["The"]
		}

		# Update the media statistics for the current year and month, passing the local media dictionary and the media type
		# And getting the statistics text back
		self.dictionary["Statistics text"] = Watch_History.Update_Statistics(self, self.dictionary, media, media_type)

	def Show_Information(self):
		# Define the header text key as the selected container text (generally the media type)
		# Examples:
		# Anime:
		# Dubbed anime:
		# 
		# (Selected means it maybe a normal or dubbed container text
		# "anime" or "dubbed anime")
		self.dictionary["Header text"] = self.Text.Capitalize(self.media["Texts"]["Selected container texts"]["Container"]) + ":"

		# If the "Completed media" state is True (the media has been completed)
		if self.media["States"]["Completed media"] == True:
			# Define the text as the "this container" text
			text = self.media["Texts"]["Selected container texts"]["This"]

			# Update the header text to be the "You finished watching [this container]:" text
			# Examples:
			# You finished watching this anime:
			# You finished watching this cartoon:
			# You finished watching this series:
			# You finished watching this movie:
			# You finished watching this YouTube channel:
			self.dictionary["Header text"] = self.language_texts["you_finished_watching"] + " " + text + ":"

		# If the "Re-watching" state is True
		if self.media["States"]["Re-watching"] == True:
			# Replace the "watching" text with the "re-watching" text inside the header text
			self.dictionary["Header text"] = self.dictionary["Header text"].replace(self.language_texts["watching, infinitive"], self.language_texts["re_watching, infinitive"])

		# Show information about the media
		self.Show_Media_Information(self.dictionary)
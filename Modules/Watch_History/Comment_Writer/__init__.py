# Comment_Writer.py

from Watch_History.Watch_History import Watch_History as Watch_History

class Comment_Writer(Watch_History):
	def __init__(self, dictionary, add_comment = False):
		super().__init__()

		# Define the class dictionary as the parameter dictionary
		self.dictionary = dictionary

		# Make a shortcut to the "Media" dictionary
		self.media = self.dictionary["Media"]

		# Define the root "Comment Writer" dictionary, with its "States" dictionary
		self.dictionary["Comment Writer"] = {
			"States": {
				"Backup": True,
				"New": True,
				"Make": False,
				"Write": False,
				"Add": add_comment
			},
			"Comments": {
				"Root": {},
				"Media": {}
			}
		}

		# If the "Add" state is not False
		if self.dictionary["Comment Writer"]["States"]["Add"] != False:
			# Define the "Write" state as the "Add" state
			self.dictionary["Comment Writer"]["States"]["Write"] = self.dictionary["Comment Writer"]["States"]["Add"]

		# Define the backup file for the comment
		self.folders["Comments"]["Backups"]["Backup"] = self.folders["Comments"]["Backups"]["root"] + "Backup.txt"

		# If the comment backup file exists
		if self.File.Exists(self.folders["Comments"]["Backups"]["Backup"]) == True:
			# The comment is not a new one, and the user is going to write it
			self.dictionary["Comment Writer"]["States"]["New"] = False
			self.dictionary["Comment Writer"]["States"]["Write"] = True

		# If the backup file does not exist
		# And the "Write" state is False
		if (
			self.File.Exists(self.folders["Comments"]["Backups"]["Backup"]) == False and
			self.dictionary["Comment Writer"]["States"]["Write"] == False
		):
			# If the "Testing" switch is False
			if self.switches["Testing"] == False:
				# Ask if the user wants to write a comment for the media (item)
				self.dictionary["Comment Writer"]["States"]["Write"] = self.Input.Yes_Or_No(self.language_texts["write_a_comment"])

			else:
				# Show the question text
				print()
				print(self.language_texts["write_a_comment"] + "?")
				print("\t" + self.Language.language_texts["yes"].capitalize())

				# Define the "Write" state as True
				self.dictionary["Comment Writer"]["States"]["Write"] = True

		# If the user wants to write a comment for the media (item)
		if self.dictionary["Comment Writer"]["States"]["Write"] == True:
			# Define the media "Commented" state as True
			self.media["States"]["Commented"] = True

			# Create the comment backup file if the "Backup" state is True
			if self.dictionary["Comment Writer"]["States"]["Backup"] == True:
				self.File.Create(self.folders["Comments"]["Backups"]["Backup"])

			# Define the comment files
			self.Define_Files()

			# Execute the steps of preparing the comment text and asking the user to write the comment
			self.Write_Comment()

			# Show the text showing that the user finished writing the comment
			print()
			print("----------")
			print()
			print(self.language_texts["you_finished_writing_the_comment"] + ".")

			# Define the media types where the user can post comments in the Internet
			self.media_types["Post comment"] = [
				"Animes",
				"Cartoons",
				"Videos"
			]

			# Define the dictionary that says which remote origin the user can post comments
			self.post_comments_on = {
				"Animes Vision": False,
				"YouTube": True
			}

			# If the media type is inside the "Post comment" list
			# And there is a remote origin inside the "Episode" dictionary
			# And the remote episode link is not empty
			# And the remote origin in the "Post comments on" dictionary is on (comment posting on that remote origin is on)
			# And the "Add" (comment) state is False
			# -
			# Then open the remote episode link to post the comment
			if (
				self.dictionary["Media type"]["Plural"]["en"] in self.media_types["Post comment"] and
				"Remote" in self.media["Episode"] and
				self.media["Episode"]["Remote"]["Link"] != "" and
				self.post_comments_on[self.media["Episode"]["Remote"]["Title"]] == True and
				self.dictionary["Comment Writer"]["States"]["Add"] == False
			):
				# Copy the comment text to the user's clipboard
				self.Text.Copy(self.media["Comment"]["Text"]["String"])

				# If the media (item) being watched is a local one
				# (Because for remote media, the remote media unit (link) is already opened)
				if self.media["States"]["Local"] == True:
					# Open the remote episode link
					self.System.Open(self.media["Episode"]["Remote"]["Link"])

				# If the "Testing" switch is False
				if self.switches["Testing"] == False:
					# Ask for user input after they finish posting the comment on the remote episode link
					self.Input.Type(self.language_texts["press_enter_when_you_finish_posting_the_comment"])

			# Run the method to write the comment text to the comment files
			self.Write_Comment_To_Files()

	def Define_Files(self):
		# Define the "Comment" dictionary
		self.media["Comment"] = {
			"File name": "",
			"File name (sanitized)": "",
			"Text": {
				"String": "",
				"Lines": []
			},
			"Line number": 0,
			"Comment time text": {
				"Normal": self.language_texts["comment_time"],
				"Brackets": "[" + self.language_texts["comment_time"] + "]"
			}
		}

		# If the media is a series media (not a movie)
		if self.media["States"]["Series media"] == True:
			# Define the local "add episode separator" state as False
			add_episode_separator = False

			# Iterate through the list of alternative episode types
			# alternative_episode_types = ["OVA", "ONA", "Special", "Especial", "Shorts", "Curtas"]
			for alternative_episode_type in self.alternative_episode_types:
				# If the alternative episode type is inside the media episode separator
				if alternative_episode_type in self.media["Episode"]["Separator"]:
					# Define the state above as True
					add_episode_separator = True

			# If the "add episode separator" state is True
			if add_episode_separator == True:
				# Add the episode separator to the comment file name
				self.media["Comment"]["File name"] += self.media["Episode"]["Separator"] + " "

			# If the media (item) is an episodic one (not a single unit media item)
			if self.media["States"]["Episodic"] == True:
				# If the "Number text" key is inside the "Episode" dictionary, add the number text to the comment file name
				if "Number text" in self.media["Episode"]:
					self.media["Comment"]["File name"] += self.media["Episode"]["Number text"]

				# Else, add the episode number with added leading zeroes
				else:
					self.media["Comment"]["File name"] += str(self.Text.Add_Leading_Zeroes(self.media["Episode"]["Number"]))

			# If the media (item) is not an episodic one (a single unit media item for example)
			if self.media["States"]["Episodic"] == False:
				# Define the comment file name as only the media episode title
				self.media["Comment"]["File name"] = self.media["Episode"]["Title"]

		# If the media is not a series media (it is a movie)
		# Or the media item is a single unit
		if (
			self.media["States"]["Series media"] == False or
			self.media["States"]["Single unit"] == True
		):
			# Define the comment file name as only "Comment"
			self.media["Comment"]["File name"] = self.Language.language_texts["comment, title()"]

		# If the user is re-watching the media (item)
		if self.media["States"]["Re-watching"] == True:
			# Add the re-watching number to the comment file name
			self.media["Comment"]["File name"] += self.media["Episode"]["Re-watching"]["Texts"]["Number"][self.language["Small"]]

		# Define the sanitized version of the comment file name
		self.media["Comment"]["File name (sanitized)"] = self.Sanitize(self.media["Comment"]["File name"], restricted_characters = True)

		# Define and create the comment file inside the media (item) folder
		self.media["Item"]["Folders"]["comments"]["files"]["comment"] = self.media["Item"]["Folders"]["comments"]["files"]["root"] + self.media["Comment"]["File name (sanitized)"] + ".txt"

		self.File.Create(self.media["Item"]["Folders"]["comments"]["files"]["comment"])

		# Read the "Comments.json" file to get the "Root comments" dictionary
		self.dictionary["Comment Writer"]["Comments"]["Root"] = self.JSON.To_Python(self.folders["Comments"]["Comments"])

		# Read the selected media "Comments.json" file to get the media "Comments" dictionary
		self.dictionary["Comment Writer"]["Comments"]["Media"] = self.JSON.To_Python(self.media["Item"]["Folders"]["comments"]["comments"])

	def Write_Comment(self):
		# If the "Backup" state is True (to make backups of the comment)
		# And the "New" state is False (not a new comment)
		if (
			self.dictionary["Comment Writer"]["States"]["Backup"] == True and
			self.dictionary["Comment Writer"]["States"]["New"] == False
		):
			# Get the comment text from the backup file
			text = self.File.Contents(self.folders["Comments"]["Backups"]["Backup"])["string"]

			# Add the text to the "String" and "Lines" keys
			self.media["Comment"]["Text"]["String"] += text
			self.media["Comment"]["Text"]["Lines"].append(text)

			# Show the text telling the user that an already written comment has been loaded
			print()
			print(self.separators["5"])
			print()
			print(self.language_texts["loading_already_written_comment"] + "...")

		# Define the show text to be shown in the "Input.Lines()" method, with the comment file name
		show_text = self.separators["10"] + "\n\n"
		show_text += self.language_texts["comment_file_name"] + ":" + "\n"
		show_text += self.media["Comment"]["File name (sanitized)"] + "\n"
		show_text += "\n"

		# Add the gender text based on the gender "the" text of the media type and the media unit text
		show_text += self.language_texts["type_the_comment_for"] + " " + self.dictionary["Media type"]["Genders"][self.language["Small"]]["the"] + " " + self.media["Texts"]["unit"][self.language["Small"]] + ": "

		# Add ten dash separators
		show_text += "\n\n" + self.separators["10"]

		# If the comment is a new one
		if self.dictionary["Comment Writer"]["States"]["New"] == True:
			# Define the normal media key as the "with_title" one
			key = "with_title"

			# If the media has a list of media items
			# And the media item is not the root media
			# And the media is not a video channel
			# And the media item is not a single unit
			# And the "Replace title" state is False
			if (
				self.media["States"]["Has a list of media items"] == True and
				self.media["States"]["The media item is the root media"] == False and
				self.media["States"]["Video"] == False and
				self.language_texts["single_unit"] not in self.media["Item"]["Details"] and
				self.media["States"]["Replace title"] == False
			):
				# Define the media key as the "with_title_and_item" one
				key = "with_title_and_item"

			# If the key is inside the media "Episode" dictionary
			if key in self.media["Episode"]:
				# Define the title as the title with the key in the user language
				title = self.media["Episode"][key][self.language["Small"]]

			# If the media is not a series media (it is a movie)
			if self.media["States"]["Series media"] == False:
				# Define the title as the media episode title (the movie title in the media language) plus the year the movie was released
				title = self.media["Episode"]["Titles"][self.media["Language"]] + " (" + self.media["Episode"]["Titles"]["Original"].split("(")[1]

			# If the user is re-watching the media, add the re-watching number in the user language
			if self.media["States"]["Re-watching"] == True:
				title += self.media["Episode"]["Re-watching"]["Texts"]["Number"][self.language["Small"]]

			# Define the title text
			title_text = self.language_texts["episode_title"]

			# Get the title text template
			title_template = self.language_texts["{}_title"]

			# If the item type is not in the list of main media types
			# And the item type is inside the list of alternative episode types
			# alternative_episode_types = ["OVA", "ONA", "Special", "Especial", "Shorts", "Curtas"]
			if (
				self.media["Item"]["Type"]["en"] not in self.media_types["Singular"]["en"] and
				self.media["Item"]["Type"]["en"] in self.alternative_episode_types
			):
				# Format it as "Title of the [item type]" in the user language
				with_ = title_template.format(self.media["Item"]["Type"][self.language["Small"]].lower())

			# If the media type is "Movies"
			# Or the media type is "Videos" and the media is not episodic
			if (
				self.dictionary["Media type"]["Plural"]["en"] == "Movies" or
				(self.dictionary["Media type"]["Plural"]["en"] == "Videos" and
				not self.media["States"]["Episodic"])
			):
				# Define a shortcut for the singular media type
				singular_media_type = self.dictionary["Media type"]["Singular"][self.language["Small"]]

				# Determine the case of the singular media type based on the position of the "{}" characters
				if title_template.startswith("{}"):
					# If "{}" is at the beginning, use the media type as is (already in uppercase)
					title_text = title_template.format(singular_media_type)

				else:
					# If "{}" is at the end, convert the media type to lowercase
					title_text = title_template.format(singular_media_type.lower())

			# Define the episode text (title) as the defined title text plus the defined title above
			episode_text = title_text + ":" + "\n" + title + "\n"

			# Add the episode text to the comment text string
			self.media["Comment"]["Text"]["String"] += episode_text

			# Add it to the list of comment text lines
			self.media["Comment"]["Text"]["Lines"].append(self.Language.language_texts["title, title()"] + ":")
			self.media["Comment"]["Text"]["Lines"].append(title)

			# If the media is a video channel
			if self.media["States"]["Video"] == True:
				# Add the media episode ID to the "String" and "Lines" keys
				self.media["Comment"]["Text"]["String"] += self.media["Episode"]["ID"] + "\n"
				self.media["Comment"]["Text"]["Lines"].append(self.media["Episode"]["ID"])

			# Add a line break to both the keys
			self.media["Comment"]["Text"]["String"] += "\n"
			self.media["Comment"]["Text"]["Lines"].append("")

			# Add the user language "Comment time" text
			# And the user language "[Comment time]" text to the root comment text
			# (It will be replaced by the actual comment time when the user finishes writing the comment later)
			self.media["Comment"]["Text"]["String"] += self.media["Comment"]["Comment time text"]["Normal"] + ":" + "\n" + \
			self.media["Comment"]["Comment time text"]["Brackets"] + "\n"

			self.media["Comment"]["Text"]["Lines"].append(self.media["Comment"]["Comment time text"]["Normal"] + ":")
			self.media["Comment"]["Text"]["Lines"].append(self.media["Comment"]["Comment time text"]["Brackets"])

			# If the "Backup" state is True
			if self.dictionary["Comment Writer"]["States"]["Backup"] == True:
				# Make a backup of the current comment text
				self.File.Edit(self.folders["Comments"]["Backups"]["Backup"], self.media["Comment"]["Text"]["String"], "a", next_line = False)

			# Add the comment text to the show text
			show_text += "\n" + self.media["Comment"]["Text"]["String"]

			# Add a line break to the comment text after adding it to the show text, to have a space before the input line
			self.media["Comment"]["Text"]["String"] += "\n"
			self.media["Comment"]["Text"]["Lines"].append("")

		# If the comment is not a new one, get the already written comment from the backup file and add it to the show text
		if self.dictionary["Comment Writer"]["States"]["New"] == False:
			show_text += "\n" + self.File.Contents(self.folders["Comments"]["Backups"]["Backup"])["string"]

		# If the "Add" (comment) state is False
		if self.dictionary["Comment Writer"]["States"]["Add"] == False:
			# If the "Testing" switch is False
			if self.switches["Testing"] == False:
				# Ask the user to write the comment using the "Lines" method of the "Input" class
				# With the parameters:
				# next_line: False, do not show a space before asking for each line
				# backup_file: the backup file to where each line will be written
				# second_space: False, do not show a space after finishing to write the comment
				dictionary = self.Input.Lines(show_text, line_options_parameter = {"print": True, "next_line": False}, backup_file = self.folders["Comments"]["Backups"]["Backup"], second_space = False)

			else:
				# Make a shortcut for the "Comment" text in the user language, with brackets added
				comment_text = "[" + self.Language.language_texts["comment, title()"] + "]"

				# Make a default dictionary of lines
				dictionary = {
					"lines": [
						comment_text
					],
					"string": comment_text,
					"length": 1
				}

		# If the "Add comment" state is True
		if self.dictionary["Comment Writer"]["States"]["Add"] == True:
			# Create the "Comment.txt" file
			comment_file = self.media["Item"]["Folders"]["comments"]["root"] + "Comment.txt"
			self.File.Create(comment_file)

			# Open it
			self.System.Open(comment_file)

			# Wait for user to add the comment text to the comment file above
			self.Input.Type(self.Language.language_texts["continue, title()"])

			# Update the dictionary with the updated contents of the comment file
			dictionary = self.File.Contents(comment_file)

			# Add the comment text to the backup file
			self.File.Edit(self.folders["Comments"]["Backups"]["Backup"], dictionary["string"], "a")

			# Delete the old comment file
			self.File.Delete(comment_file)

		# Get the updated comment text from the backup file
		# (The user may have edited the comment text from inside the backup file after writing something wrong)
		contents = self.File.Contents(self.folders["Comments"]["Backups"]["Backup"])

		# If the text the backup file is different from the text inside the comment text dictionary
		# And the text inside the backup file is not empty
		if (
			contents["string"] != dictionary["string"] and
			contents["string"] != ""
		):
			# Define the comment text keys as the backup file text keys
			self.media["Comment"]["Text"]["String"] = contents["string"]
			self.media["Comment"]["Text"]["Lines"] = contents["lines"]

		# Else, add the written comment ("Input.Lines" dictionary) to the comment string and lines keys
		else:
			self.media["Comment"]["Text"]["String"] += dictionary["string"]
			self.media["Comment"]["Text"]["Lines"].extend(dictionary["lines"])

		# Get the number of lines of the comment text
		self.media["Comment"]["Line number"] = len(self.media["Comment"]["Text"]["Lines"])

		# Define the comment date dictionary
		comment_date = self.Date.Now()

		# Define the comment time
		self.media["Comment"]["Comment times"] = {
			"Timezone": comment_date["Timezone"]["DateTime"]["Formats"]["HH:MM DD/MM/YYYY"],
			"UTC": comment_date["UTC"]["DateTime"]["Formats"]["YYYY-MM-DDTHH:MM:SSZ"]
		}

		# Get the time in a good format
		comment_time = self.media["Comment"]["Comment times"]["Timezone"]

		# Replace the "Comment time" text in the comment text with the correct comment time
		self.media["Comment"]["Text"]["String"] = self.media["Comment"]["Text"]["String"].replace(self.media["Comment"]["Comment time text"]["Brackets"], comment_time)

		# If the number of lines inside the comment text is greater than or equal to 4
		if len(self.media["Comment"]["Text"]["Lines"]) >= 4:
			# Replace the "[Comment time]" text in the comment text with the correct comment time
			self.media["Comment"]["Text"]["Lines"][4] = self.media["Comment"]["Text"]["Lines"][4].replace(self.media["Comment"]["Comment time text"]["Brackets"], comment_time)

		# Update the backup file to update the comment time inside it
		self.File.Edit(self.folders["Comments"]["Backups"]["Backup"], self.media["Comment"]["Text"]["String"], "w")

	def Write_Comment_To_Files(self):
		from copy import deepcopy

		# ---------- #

		# Delete the comment backup file
		if self.dictionary["Comment Writer"]["States"]["Backup"] == True:
			self.File.Delete(self.folders["Comments"]["Backups"]["Backup"])

		# ---------- #

		# Add to the total number of comments
		self.dictionary["Comment Writer"]["Comments"]["Root"]["Numbers"]["Total"] += 1

		# Add to the total number of comments in the current year
		self.dictionary["Comment Writer"]["Comments"]["Root"]["Numbers"]["Years"][str(self.date["Units"]["Year"])] += 1

		# Add to the total number of comments for the media type of the media
		self.dictionary["Comment Writer"]["Comments"]["Root"]["Numbers"]["Type"][self.dictionary["Media type"]["Plural"]["en"]]["Total"] += 1

		# Add to the total number of comments for the media type of the media in the current year
		self.dictionary["Comment Writer"]["Comments"]["Root"]["Numbers"]["Type"][self.dictionary["Media type"]["Plural"]["en"]]["Years"][str(self.date["Units"]["Year"])] += 1

		# Update the root "Comments.json" file to update the numbers
		self.JSON.Edit(self.folders["Comments"]["Comments"], self.dictionary["Comment Writer"]["Comments"]["Root"])

		# ---------- #

		# Define the comment key (the comment file name)
		self.comment_file_name = self.media["Comment"]["File name"]

		# Add the comment file name to the list of file names (entries)
		self.dictionary["Comment Writer"]["Comments"]["Media"]["Entries"].append(self.comment_file_name)

		# Update the total number of comments for the media (item)
		self.dictionary["Comment Writer"]["Comments"]["Media"]["Numbers"]["Total"] = len(self.dictionary["Comment Writer"]["Comments"]["Media"]["Entries"])

		# ---------- #

		# Create the comment dictionary with its keys and add it to the comments dictionary of the media
		self.dictionary["Comment Writer"]["Comments"]["Media"]["Dictionary"][self.comment_file_name] = {
			"Comment number": self.dictionary["Comment Writer"]["Comments"]["Media"]["Numbers"]["Total"], # The comment number
			"Media type": self.dictionary["Media type"]["Plural"]["en"], # The media type
			"Entry": self.comment_file_name, # The comment entry name
			"Comment times": self.media["Comment"]["Comment times"], # The comment times dictionary
			"Titles": self.media["Episode"]["Titles"], # The comment titles (media episode or media titles)
			"Number of comment lines": self.media["Comment"]["Line number"] # The number of lines the comment has
		}

		# ---------- #

		# If the media is not a series media (it is a movie)
		if self.media["States"]["Series media"] == False:
			# Define a shortcut (by reference) for the titles dictionary
			titles = self.dictionary["Comment Writer"]["Comments"]["Media"]["Dictionary"][self.comment_file_name]["Titles"]

			# Remove the "ja" and "Sanitized" keys of the local titles dictionary if they exist
			for key in ["ja", "Sanitized"]:
				if key in titles:
					titles.pop(key)

			# Iterate through the list of small languages
			for language in self.languages["small"]:
				# If the language is inside the dictionary of titles
				if language in titles:
					# If the "Original" key exists
					# And the original title is the same as the language title
					# Or the "Romanized" key exists
					# And the romanized title is the same as the language title
					if (
						"Original" in titles and
						titles["Original"] == titles[language] or
						"Romanized" in titles and
						titles["Romanized"] == titles[language]
					):
						# Remove the language title
						titles.pop(language)

			# If the "Language" key exists
			# And the language title is the same as the media language title
			# (For example, a cartoon that has the same title in English or Portuguese, such as "Ben 10")
			if (
				"Language" in titles and
				titles["Language"] == titles[self.media["Language"]]
			):
				# Remove the "Language" key
				titles.pop("Language")

		# ---------- #

		# If the media is a video channel
		# (Add the YouTube video ID, comment link, and comment ID to the comment dictionary)
		if self.media["States"]["Video"] == True:
			# Define a shortcut to the comment dictionary
			comment = self.dictionary["Comment Writer"]["Comments"]["Media"]["Dictionary"][self.comment_file_name]

			# Update the comment dictionary to add the comment "Link" and "Video" dictionaries
			comment.update({
				"Comment link": { # The comment "Link" dictionary
					"ID": "",
					"Link": ""
				},
				"Video": { # The comment "Video" dictionary
					"ID": self.media["Episode"]["ID"],
					"Link": self.remote_origins["YouTube"]["Link templates"]["Video"].replace("{Video}", self.media["Episode"]["ID"]),
					"Times": {
						"Timezone": "",
						"UTC": ""
					}
				}
			})

			# ---------- #

			# Define a shortcut to the video dictionary
			video = comment["Video"]

			# Define a shortcut to the video link
			video_link = video["Link"]

			# Get the video information from the root "Get_YouTube_Information" method that uses the "API" utility class to access the YouTube API
			# Giving it the "Video" and video link parameters
			video_information = self.Get_YouTube_Information("Video", video_link)

			# Define the video "Times" dictionary as the video published "Times" dictionary gotten from the YouTube API
			video["Times"] = video_information["Times"]

			# ---------- #

			# Import the validators module
			import validators

			# Define the original link variable as an empty string
			original_link = ""

			# Define the "found comment parameter" switch as False
			found_comment_parameter = False

			# While the "found comment parameter" switch is False
			while found_comment_parameter == False:
				# If the "Testing" switch is False
				if self.switches["Testing"] == False:
					# Ask for the link of the comment
					original_link = self.Input.Type(self.language_texts["paste_the_comment_link_of_youtube"])

					# If the original link is an URL
					if validators.url(original_link) == True:
						# Parse the link to get the comment ID
						comment_id = self.Parse_Link(original_link, "Comment")

						# If the comment ID is not None
						if comment_id != None:
							# Switch the "found comment parameter" switch to True
							found_comment_parameter = True

				# If the "Testing" switch is True
				if self.switches["Testing"] == True:
					# Define the comment link
					original_link = "https://www.youtube.com/watch?v=bbmtQkCcWY4&lc="

					# Define the comment ID
					comment_id = "UgxuNs35fO-gFEDY7l14AaABAg"

					# Add it to the link
					original_link += comment_id

					# Show the input text and the defined comment link
					print()
					print(self.language_texts["paste_the_comment_link_of_youtube"] + ":")
					print(original_link)

					# Switch the "found comment parameter" switch to True
					found_comment_parameter = True

			# Add the comment ID and link to the "Comment link" dictionary
			comment["Comment link"] = {
				"ID": comment_id, # The comment ID
				"Link": "" # The video link with the comment ID
			}

			# Define the comment link as the "Video and comment" template
			link = self.remote_origins["YouTube"]["Link templates"]["Video and comment"]

			# Add the video ID
			link = link.replace("{Video}", video["ID"])

			# Add the comment ID
			link = link.replace("{Comment}", comment_id)

			# Add the comment link to the "Link" key
			comment["Comment link"]["Link"] = link

			# ---------- #

			# Get the comment information from the root "Get_YouTube_Information" method that uses the "API" utility class to access the YouTube API
			# Giving it the "Comment" and comment link parameters
			comment_information = self.Get_YouTube_Information("Comment", comment["Comment link"]["Link"])

			# Define the comment "Times" dictionary as the comment published "Times" dictionary gotten from the YouTube API
			comment["Comment times"] = comment_information["Times"]

			# ---------- #

			# Update the comment time in the comment text

			# Split the lines of the comment text
			self.media["Comment"]["Text"]["String"] = self.media["Comment"]["Text"]["String"].splitlines()

			# Define the line five (5) as the comment time
			# Line zero (0) will be "Title:", line one (1) will be the actual media episode title
			# Line two (2) will be the video ID, line three (3) will be a space
			# And line four (4) will be the "Comment time:" text
			self.media["Comment"]["Text"]["String"][5] = comment_information["Times"]["Timezone"]

			# Convert the list of lines of the comment text to a string
			self.media["Comment"]["Text"]["String"] = self.Text.From_List(self.media["Comment"]["Text"]["String"], next_line = True)

		# If the "Add comment" state is True
		if self.dictionary["Comment Writer"]["States"]["Add"] == True:
			# Copy the comment text
			self.Text.Copy(self.media["Comment"]["Text"]["String"])

		# Write the comment into the comment file inside the media (item) folder
		self.File.Edit(self.media["Item"]["Folders"]["comments"]["files"]["comment"], self.media["Comment"]["Text"]["String"], "w")

		# Get the "States" dictionary of the watched media
		states_dictionary = self.Define_States_Dictionary(self.dictionary)["States"]

		# If the "Add comment" state is True
		if self.dictionary["Comment Writer"]["States"]["Add"] == True:
			# Define the list of first entry keys
			first_entry_keys = [
				"First entry in year",
				"First media type entry in year"
			]

			# Iterate through those keys
			for key in first_entry_keys:
				# If the key is inside the local states dictionary, remove it
				# (Those keys are not related to comments, only to the watched media)
				if key in states_dictionary:
					states_dictionary.pop(key)

		# Remove the "Commented" state from the dictionary
		# (Because it is obvious that the user commented on the media, it is a comment dictionary, not a watched media one)
		if "Commented" in states_dictionary:
			states_dictionary.pop("Commented")

		# If the states dictionary is not empty, add it to the comment dictionary
		if states_dictionary != {}:
			self.dictionary["Comment Writer"]["Comments"]["Media"]["Dictionary"][self.comment_file_name]["States"] = states_dictionary

		# Import the collections module to sort the comments dictionary
		import collections

		# Define the "sort comments" switch as False
		sort_comments = False

		# If the "sort comments" switch is True
		if sort_comments == True:
			# Sort the list of comments (the comment file names) in the "Entries" key
			self.dictionary["Comment Writer"]["Comments"]["Media"]["Entries"] = sorted(self.dictionary["Comment Writer"]["Comments"]["Media"]["Entries"], key = str.lower)

			# Sort the dictionary of comments based on their keys
			self.dictionary["Comment Writer"]["Comments"]["Media"]["Dictionary"] = dict(collections.OrderedDict(sorted(self.dictionary["Comment Writer"]["Comments"]["Media"]["Dictionary"].items())))

			# Re-numerate the "Comment number" keys inside each comment dictionary based on their position (index) on the "Entries" list
			# (Numbers of the non-episodic media are wrong when updated because the episode title is used as the dictionary key
			# And also to fix numbers of comment dictionaries from episodic media if they are wrong
			# Non-episodic media include video channels with random videos not watched in a specific order)
			number = 1
			for entry_name in self.dictionary["Comment Writer"]["Comments"]["Media"]["Entries"]:
				self.dictionary["Comment Writer"]["Comments"]["Media"]["Dictionary"][entry_name]["Comment number"] = number

				number += 1

		# Create the "Comment" dictionary inside the "Comment Writer" dictionary
		self.dictionary["Comment Writer"]["Comment"] = deepcopy(self.dictionary["Comment Writer"]["Comments"]["Media"]["Dictionary"][self.comment_file_name])

		# Define the list of keys to remove from the comment dictionary
		keys_to_remove = [
			"Media type",
			"Titles",
			"States",
			"Number of comment lines"
		]

		# If the media is a non-episodic one
		if self.media["States"]["Episodic"] == False:
			# Remove the "Comment number" key
			keys_to_remove.append("Comment number")

			# If the "Episode" key is inside the media dictionary
			# And the media unit (episode) has titles
			# And the media unit (episode) inside the comment dictionary is the same as the media unit title
			if (
				"Episode" in self.media and
				"Titles" in self.media["Episode"] and
				self.dictionary["Comment Writer"]["Comment"]["Titles"][self.media["Language"]] == self.media["Episode"]["Titles"][self.media["Language"]]
			):
				# Add the "Entry" key to be removed from the comment dictionary that will be used by the "Register" class
				# (This means that the comment file name is the same as the media unit (episode) title, so the entry will be the same as it)
				keys_to_remove.append("Entry")

		# Remove the not useful keys from the comment dictionary
		for key in keys_to_remove:
			if key in self.dictionary["Comment Writer"]["Comment"]:
				self.dictionary["Comment Writer"]["Comment"].pop(key)

		# Update the media (item) "Comments.json" file
		self.JSON.Edit(self.media["Item"]["Folders"]["comments"]["comments"], self.dictionary["Comment Writer"]["Comments"]["Media"])
# Comment_Writer.py

from Watch_History.Watch_History import Watch_History as Watch_History

class Comment_Writer(Watch_History):
	def __init__(self, dictionary, add_comment = False):
		super().__init__()

		self.dictionary = dictionary

		self.media = self.dictionary["Media"]

		self.dictionary["Comment Writer"] = {
			"States": {
				"Backup": True,
				"New": True,
				"Make": False,
				"Write": False,
				"Add": add_comment
			}
		}

		if self.dictionary["Comment Writer"]["States"]["Add"] != False:
			self.dictionary["Comment Writer"]["States"]["Write"] = self.dictionary["Comment Writer"]["States"]["Add"]

		self.folders["Comments"]["Backups"]["Backup"] = self.folders["Comments"]["Backups"]["root"] + "Backup.txt"

		# If the backup file exists, it is not a new comment and the user is going to write the comment
		if self.File.Exist(self.folders["Comments"]["Backups"]["Backup"]) == True:
			self.dictionary["Comment Writer"]["States"]["New"] = False

			self.dictionary["Comment Writer"]["States"]["Write"] = True

		# If the backup file does not exist, ask the user if it wants to write a comment
		if (
			self.File.Exist(self.folders["Comments"]["Backups"]["Backup"]) == False and
			self.dictionary["Comment Writer"]["States"]["Write"] == False
		):
			self.dictionary["Comment Writer"]["States"]["Write"] = self.Input.Yes_Or_No(self.language_texts["write_a_comment"])

		if self.dictionary["Comment Writer"]["States"]["Write"] == True:
			self.media["States"]["Commented"] = True

			# Create backup file
			if self.dictionary["Comment Writer"]["States"]["Backup"] == True:
				self.File.Create(self.folders["Comments"]["Backups"]["Backup"])

			# Run methods
			self.Define_Files()
			self.Write_Comment()

			# Show the text showing that the user finished writing the comment
			print("----------")
			print()
			print(self.language_texts["you_finished_writing_the_comment"] + ".")

			# Define the media types where the user can post comments
			self.media_types["Post comment"] = [
				self.texts["animes, title()"]["en"],
				self.texts["cartoons, title()"]["en"],
				self.texts["videos, title()"]["en"]
			]

			# Define the dictionary that says if comment posting on the remote media is activated
			self.post_comments_on = {
				"Animes Vision": False,
				"YouTube": True
			}

			# If the media type is inside the "Post comment" list
			# And the episode is a remote one
			# And the remote episode link is not empty
			# And the remote origin in the dictionary above is on (comment posting is on)
			# -
			# Open the remote episode link to post the comment
			if (
				self.dictionary["Media type"]["Plural"]["en"] in self.media_types["Post comment"] and
				"Remote" in self.media["Episode"] and
				self.media["Episode"]["Remote"]["Link"] != "" and
				self.post_comments_on[self.media["Episode"]["Remote"]["Title"]] == True
			):
				if self.dictionary["Comment Writer"]["States"]["Add"] == False:
					# Copy the comment text
					self.Text.Copy(self.media["Comment"]["Text"]["String"])

				# If the media is not a remote one, open the remote episode link
				# (Because for remote media, the episode is already opened)
				if (
					self.media["States"]["Remote"] == False and
					self.dictionary["Comment Writer"]["States"]["Add"] == False
				):
					# Open remote episode link
					self.System.Open(self.media["Episode"]["Remote"]["Link"])

				if self.dictionary["Comment Writer"]["States"]["Add"] == False:
					# Wait for the user to finish posting the comment on the episode link
					self.finished_posting_comment = self.Input.Type(self.language_texts["press_enter_when_you_finish_posting_the_comment"])

			self.Write_Comment_To_Files()

	def Define_Files(self):
		self.media["Comment"] = {
			"File name": "",
			"Text": {
				"String": "",
				"Lines": []
			},
			"Line number": 0
		}

		# Comment file name for non-movies
		if self.media["States"]["Series media"] == True:
			add = False

			for alternative_episode_type in self.alternative_episode_types:
				if alternative_episode_type in self.media["Episode"]["Separator"]:
					add = True

			if add == True:
				self.media["Comment"]["File name"] += self.media["Episode"]["Separator"] + " "

			if self.media["States"]["Episodic"] == True:
				if "Number text" in self.media["Episode"]:
					self.media["Comment"]["File name"] += self.media["Episode"]["Number text"]

				else:
					self.media["Comment"]["File name"] += str(self.Text.Add_Leading_Zeroes(self.media["Episode"]["Number"]))

			if self.media["States"]["Episodic"] == False:
				self.media["Comment"]["File name"] = self.media["Episode"]["Title"]

		# Comment file name for movies or single unit media items
		if (
			self.media["States"]["Series media"] == False or
			self.media["States"]["Single unit"] == True
		):
			self.media["Comment"]["File name"] = self.Language.language_texts["comment, title()"]

		# Add Re-watching text to comment file name if it exists
		if self.media["States"]["Re-watching"] == True:
			self.media["Comment"]["File name"] += self.media["Episode"]["re_watched"]["text"]

		# Media folder comment file
		self.media["Item"]["Folders"]["comments"]["files"]["comment"] = self.media["Item"]["Folders"]["comments"]["files"]["root"] + self.Sanitize(self.media["Comment"]["File name"], restricted_characters = True) + ".txt"
		self.File.Create(self.media["Item"]["Folders"]["comments"]["files"]["comment"])

		# Read the "Comments.json" file to get the Comments dictionary
		self.dictionaries["Root comments"] = self.JSON.To_Python(self.folders["Comments"]["Comments"])

		# Read the selected media "Comments.json" file to get the media comments dictionary
		self.dictionaries["Comments"] = self.JSON.To_Python(self.media["Item"]["Folders"]["comments"]["comments"])

	def Write_Comment(self):
		# If backup is true and the comment is not a new one, get the comment from the backup file
		if self.dictionary["Comment Writer"]["States"]["Backup"] == True and self.dictionary["Comment Writer"]["States"]["New"] == False:
			text = self.File.Contents(self.folders["Comments"]["Backups"]["Backup"])["string"]

			self.media["Comment"]["Text"]["String"] += text
			self.media["Comment"]["Text"]["Lines"].append(text)

			print()
			print("---")
			print()
			print(self.language_texts["loading_already_written_comment"] + "...")

		# Define the show text to be shown in the "Input.Lines" method
		show_text = "----------" + "\n\n"
		show_text += self.language_texts["comment_file_name"] + ":" + "\n"
		show_text += self.media["Comment"]["File name"] + "\n"
		show_text += "\n"

		# Define masculine or feminine text based on masculine or feminine text with function
		show_text += self.language_texts["type_the_comment_for"] + " " + self.dictionary["Media type"]["Genders"][self.user_language]["the"] + " " + self.media["texts"]["unit"][self.user_language] + ": "

		show_text += "\n\n" + "----------"

		# If the comment is a new one, add the episode text to the comment
		if self.dictionary["Comment Writer"]["States"]["New"] == True:
			key = "with_title"

			if (
				self.media["States"]["Media item list"] == True and
				self.media["States"]["Media item is media"] == False and
				self.media["States"]["Video"] == False and
				self.language_texts["single_unit"] not in self.media["Item"]["Details"] and
				self.media["States"]["Replace title"] == False
			):
				key = "with_title_and_item"

			if key in self.media["Episode"]:
				title = self.media["Episode"][key][self.user_language]

			if self.media["States"]["Series media"] == False:
				title = self.media["Episode"]["Titles"][self.media["Language"]] + " (" + self.media["Episode"]["Titles"]["Original"].split("(")[1]

			if self.media["States"]["Re-watching"] == True:
				title += self.media["Episode"]["re_watched"]["text"]

			# Define episode text (title)
			episode_text = self.Language.language_texts["title, title()"] + ":" + "\n" + title + "\n"

			self.media["Comment"]["Text"]["String"] += episode_text

			self.media["Comment"]["Text"]["Lines"].append(self.Language.language_texts["title, title()"] + ":")
			self.media["Comment"]["Text"]["Lines"].append(title)

			if self.media["States"]["Video"] == True:
				self.media["Comment"]["Text"]["String"] += self.media["Episode"]["ID"] + "\n"
				self.media["Comment"]["Text"]["Lines"].append(self.media["Episode"]["ID"])

			self.media["Comment"]["Text"]["String"] += "\n"
			self.media["Comment"]["Text"]["Lines"].append("")

			# Add the time text to the comment to be replaced by the commented time after finishing the comment
			self.media["Comment"]["Text"]["String"] += self.Date.language_texts["time, title()"] + ":" + "\n" + "[Time]" + "\n"

			self.media["Comment"]["Text"]["Lines"].append(self.Date.language_texts["time, title()"] + ":")
			self.media["Comment"]["Text"]["Lines"].append("[Time]")

			# If backup is true, backup comment to file
			if self.dictionary["Comment Writer"]["States"]["Backup"] == True:
				self.File.Edit(self.folders["Comments"]["Backups"]["Backup"], self.media["Comment"]["Text"]["String"], "a", next_line = False)

			# Add comment to show text
			show_text += "\n" + self.media["Comment"]["Text"]["String"]

			# Add "\n" to comment after adding comment to show text, to have a correct space before the input line
			self.media["Comment"]["Text"]["String"] += "\n"
			self.media["Comment"]["Text"]["Lines"].append("")

		# If the comment is not a new one, load already written comment from backup file
		if self.dictionary["Comment Writer"]["States"]["New"] == False:
			show_text += "\n" + self.File.Contents(self.folders["Comments"]["Backups"]["Backup"])["string"]

		# If the "Add comment" state is False
		if self.dictionary["Comment Writer"]["States"]["Add"] == False:
			# Ask for the user to write the comment
			dictionary = self.Input.Lines(show_text, line_options_parameter = {"print": True, "next_line": False}, backup_file = self.folders["Comments"]["Backups"]["Backup"])

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

			# Delete the comment file
			self.File.Delete(comment_file)

		# Get the comment from the backup file
		# (The user may have edited the comment inside the backup file)
		contents = self.File.Contents(self.folders["Comments"]["Backups"]["Backup"])

		# If the number of lines inside the backup file are different from the lines inside the comment text dictionary
		# And the number of lines inside the backup file are not zero
		if (
			len(contents["lines"]) != len(dictionary["lines"]) and
			len(contents["lines"]) != 0
		):
			# Define the comment text dictionary as the backup file text dictionary
			self.media["Comment"]["Text"]["String"] = contents["string"]
			self.media["Comment"]["Text"]["Lines"] = contents["lines"]

		# Else, add the written comment to the comment string and lines list
		else:
			# Add comment to the comment text string and lines list
			self.media["Comment"]["Text"]["String"] += dictionary["string"]
			self.media["Comment"]["Text"]["Lines"].extend(dictionary["lines"])

		# Get line number
		self.media["Comment"]["Line number"] = len(self.media["Comment"]["Text"]["Lines"])

		# Define comment time
		self.media["Comment"]["Date"] = self.Date.Now()

		# Replace time text in comment with comment time
		self.media["Comment"]["Text"]["String"] = self.media["Comment"]["Text"]["String"].replace("[Time]", self.media["Comment"]["Date"]["Formats"]["HH:MM DD/MM/YYYY"])

		# If the number of lines inside the comment text is greater than or equal to 4
		if len(self.media["Comment"]["Text"]["Lines"]) >= 4:
			# Replace the time text in the comment with the comment time
			self.media["Comment"]["Text"]["Lines"][4] = self.media["Comment"]["Text"]["Lines"][4].replace("[Time]", self.media["Comment"]["Date"]["Formats"]["HH:MM DD/MM/YYYY"])

		# Update the backup file to update the comment time
		self.File.Edit(self.folders["Comments"]["Backups"]["Backup"], self.media["Comment"]["Text"]["String"], "w")

	def Write_Comment_To_Files(self):
		from copy import deepcopy

		# Delete the backup file
		if self.dictionary["Comment Writer"]["States"]["Backup"] == True:
			self.File.Delete(self.folders["Comments"]["Backups"]["Backup"])

		# Add to the total comment number
		self.dictionaries["Root comments"]["Numbers"]["Total"] += 1

		# Add to the year comment number
		self.dictionaries["Root comments"]["Numbers"]["Years"][str(self.date["Units"]["Year"])] += 1

		# Add to the media type comment number
		self.dictionaries["Root comments"]["Numbers"]["Type"][self.dictionary["Media type"]["Plural"]["en"]]["Total"] += 1

		# Add to the media type comment number per year
		self.dictionaries["Root comments"]["Numbers"]["Type"][self.dictionary["Media type"]["Plural"]["en"]]["Years"][str(self.date["Units"]["Year"])] += 1

		# Update the root "Comments.json" file to update the numbers
		self.JSON.Edit(self.folders["Comments"]["Comments"], self.dictionaries["Root comments"])

		self.key = self.media["Comment"]["File name"]

		# Add the comment file name to the file names list
		self.dictionaries["Comments"]["Entries"].append(self.key)

		# Update the media comments number
		self.dictionaries["Comments"]["Numbers"]["Total"] = len(self.dictionaries["Comments"]["Entries"])

		# Add the comment file name, times, and the titles keys to the Comment dictionary
		self.dictionaries["Comments"]["Dictionary"][self.key] = {
			"Number": self.dictionaries["Comments"]["Numbers"]["Total"],
			"Entry": self.key,
			"Type": self.dictionary["Media type"]["Plural"]["en"],
			"Titles": self.media["Episode"]["Titles"],
			"Date": self.media["Comment"]["Date"]["UTC"]["DateTime"]["Formats"]["YYYY-MM-DDTHH:MM:SSZ"],
			"Lines": self.media["Comment"]["Line number"]
		}

		# If the media is a movie
		if self.media["States"]["Series media"] == False:
			dict_ = self.dictionaries["Comments"]["Dictionary"][self.key]["Titles"]

			# Remove "ja" and "Sanitized" keys
			for key in ["ja", "Sanitized"]:
				if key in dict_:
					dict_.pop(key)

			# Remove language keys if the original or romanized keys are the same as the original key
			for language in self.languages["small"]:
				if language in dict_:
					if (
						"Original" in dict_ and
						dict_["Original"] == dict_[language] or
						"Romanized" in dict_ and
						dict_["Romanized"] == dict_[language]
					):
						dict_.pop(language)

			# Remove the "Language" key
			if (
				"Language" in dict_ and
				dict_["Language"] == dict_[self.media["Language"]]
			):
				dict_.pop("Language")

		# Add the YouTube video ID, comment link, and the comment ID to the Comment dictionary
		if self.media["States"]["Video"] == True:
			self.dictionaries["Comments"]["Dictionary"][self.key].pop("Date")

			lines = self.dictionaries["Comments"]["Dictionary"][self.key]["Lines"]
			self.dictionaries["Comments"]["Dictionary"][self.key].pop("Lines")

			self.dictionaries["Comments"]["Dictionary"][self.key].update({
				"ID": "",
				"Link": "",
				"Date": "",
				"Lines": lines,
				"Video": {
					"ID": self.media["Episode"]["ID"],
					"Link": self.remote_origins["YouTube"] + "watch?v=" + self.media["Episode"]["ID"],
					"Date": ""
				}
			})

			video_information = self.Get_YouTube_Information("video", self.dictionaries["Comments"]["Dictionary"][self.key]["Video"]["Link"])

			# Define the video time as the video published time gotten from the YouTube API
			self.dictionaries["Comments"]["Dictionary"][self.key]["Video"]["Date"] = video_information["Date"]

			original_link = ""

			from urllib.parse import urlparse, parse_qs
			import validators

			while validators.url(original_link) != True:
				# Ask for the YouTube comment link
				if self.switches["testing"] == False:
					original_link = self.Input.Type(self.language_texts["paste_the_comment_link_of_youtube"])

				if self.switches["testing"] == True:
					original_link = "https://www.youtube.com/watch?v=bbmtQkCcWY4&lc=UgxuNs35fO-gFEDY7l14AaABAg"

					print(self.language_texts["paste_the_comment_link_of_youtube"] + ":")
					print(original_link)

			# Parse the link to get the query string (parameters)
			link = urlparse(original_link)
			query = link.query
			parameters = parse_qs(query)

			# Add comment ID and link to comment dictionary
			self.dictionaries["Comments"]["Dictionary"][self.key].update({
				"ID": parameters["lc"][0],
				"Link": self.dictionaries["Comments"]["Dictionary"][self.key]["Video"]["Link"] + "&lc=" + parameters["lc"][0]
			})

			# Get the comment information dictionary from the YouTube API
			comment_information = self.Get_YouTube_Information("comment", self.dictionaries["Comments"]["Dictionary"][self.key]["Link"])

			# Convert the comment date to a string using the date time format
			comment_date = self.Date.From_String(comment_information["Date"])

			# Define the comment time as the comment published time gotten from the YouTube API
			self.dictionaries["Comments"]["Dictionary"][self.key]["Date"] = self.Date.To_String(comment_date, utc = True)

			# Update the time in the comment text
			self.media["Comment"]["Text"]["String"] = self.media["Comment"]["Text"]["String"].splitlines()
			self.media["Comment"]["Text"]["String"][5] = self.Date.To_Timezone(comment_date)["Formats"]["HH:MM DD/MM/YYYY"]
			self.media["Comment"]["Text"]["String"] = self.Text.From_List(self.media["Comment"]["Text"]["String"], break_line = True)

		# If the "Add comment" state is True
		if self.dictionary["Comment Writer"]["States"]["Add"] == True:
			self.Text.Copy(self.media["Comment"]["Text"]["String"])

		# Write the comment into the media folder comment file
		self.File.Edit(self.media["Item"]["Folders"]["comments"]["files"]["comment"], self.media["Comment"]["Text"]["String"], "w")

		# Get the states dictionary
		states_dictionary = self.Define_States_Dictionary(self.dictionary)["States"]

		if self.dictionary["Comment Writer"]["States"]["Add"] == True:
			for key in ["First entry in year", "First media type entry in year"]:
				if key in states_dictionary:
					states_dictionary.pop(key)

		# Remove the "Commented" state from the dictionary
		# (Because it is obvious that the user commented, it is a comment dictionary)
		if "Commented" in states_dictionary:
			states_dictionary.pop("Commented")

		# If the states dictionary is not empty, add it to the comment dictionary
		if states_dictionary != {}:
			self.dictionaries["Comments"]["Dictionary"][self.key]["States"] = states_dictionary

		# Import the collections module to sort the comments dictionary
		import collections

		self.sort_comments = False

		# If the media is non-episodic
		#if self.media["States"]["Episodic"] == False:
		if self.sort_comments == True:
			# Sort the media entries list and dictionary
			self.dictionaries["Comments"]["Entries"] = sorted(self.dictionaries["Comments"]["Entries"], key = str.lower)
			self.dictionaries["Comments"]["Dictionary"] = dict(collections.OrderedDict(sorted(self.dictionaries["Comments"]["Dictionary"].items())))

			# Re-numerate the Entry numbers inside entry dictionaries
			# (Numbers of the non-episodic media are wrong when updated because the episode title is used as the dictionary key)
			# (And also to fix Comment dictionary numbers of episodic media if they are wrong)
			number = 1
			for entry_name in self.dictionaries["Comments"]["Entries"]:
				self.dictionaries["Comments"]["Dictionary"][entry_name]["Number"] = number

				number += 1

		# Create the "Comment" dictionary inside the "Comment Writer" dictionary
		self.dictionary["Comment Writer"]["Comment"] = deepcopy(self.dictionaries["Comments"]["Dictionary"][self.key])

		# Define the keys to be removed from the "Comment" dictionary
		keys_to_remove = [
			"Type",
			"Titles",
			"States",
			"Lines"
		]

		# If the media is not episodic, remove the "Number" key from the "Comment" dictionary
		if self.media["States"]["Episodic"] == False:
			keys_to_remove.append("Number")

			# If the media has a media unit
			# And the media unit has titles
			# And the media unit inside the Comment dictionary is the same as the media unit title
			if (
				"Episode" in self.media and
				"Titles" in self.media["Episode"] and
				self.dictionary["Comment Writer"]["Comment"]["Titles"][self.media["Language"]] == self.media["Episode"]["Titles"][self.media["Language"]]
			):
				# Add the "Entry" key to be removed from the Comment dictionary that will be used by the Register class
				# To be added into the media Entry dictionary
				keys_to_remove.append("Entry")

		# Remove the not useful keys from the "Comment" dictionary
		for key in keys_to_remove:
			if key in self.dictionary["Comment Writer"]["Comment"]:
				self.dictionary["Comment Writer"]["Comment"].pop(key)

		# Update the media "Comments.json" file
		self.JSON.Edit(self.media["Item"]["Folders"]["comments"]["comments"], self.dictionaries["Comments"])
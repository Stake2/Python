# Comment_Writer.py

from Watch_History.Watch_History import Watch_History as Watch_History

class Comment_Writer(Watch_History):
	def __init__(self, dictionary, write_comment = False):
		super().__init__()

		self.dictionary = dictionary
		self.write_comment = write_comment

		self.media = self.dictionary["Media"]

		self.dictionary["Comment Writer"] = {
			"States": {
				"backup": True,
				"new": True,
				"make": False,
				"write": False
			}
		}

		if self.write_comment != False:
			self.dictionary["Comment Writer"]["States"]["write"] = self.write_comment

		self.folders["comments"]["backups"]["backup"] = self.folders["comments"]["backups"]["root"] + "Backup.txt"

		# If the backup file exists, it is not a new comment and the user is going to write the comment
		if self.File.Exist(self.folders["comments"]["backups"]["backup"]) == True:
			self.dictionary["Comment Writer"]["States"]["new"] = False

			self.dictionary["Comment Writer"]["States"]["write"] = True

		# If the backup file does not exist, ask the user if it wants to write a comment
		if self.File.Exist(self.folders["comments"]["backups"]["backup"]) == False and self.dictionary["Comment Writer"]["States"]["write"] == False:
			self.dictionary["Comment Writer"]["States"]["write"] = self.Input.Yes_Or_No(self.language_texts["write_a_comment"])

		if self.dictionary["Comment Writer"]["States"]["write"] == True:
			self.media["States"]["Commented"] = True

			# Create backup file
			if self.dictionary["Comment Writer"]["States"]["backup"] == True:
				self.File.Create(self.folders["comments"]["backups"]["backup"])

			# Run methods
			self.Define_Files()
			self.Write_Comment()

			# Show text showing that the user finished writing the comment
			print("----------")
			print()
			print(self.language_texts["you_finished_writing_the_comment"] + ".")

			# Define media types where user can post comments
			self.media_types["comment_posting"] = [
				self.texts["animes, title()"]["en"],
				self.texts["cartoons, title()"]["en"],
				self.texts["videos, title()"]["en"]
			]

			# If media type is inside the above list, and the episode is a remote one, open remote episode link to post comment
			if self.dictionary["Media type"]["Plural"]["en"] in self.media_types["comment_posting"] and \
				"remote" in self.media["Episode"] and self.media["Episode"]["Remote"]["Link"] != "":
				# Copy the comment
				self.Text.Copy(self.media["comment"]["comment"]["Text"])

				if self.media["States"]["Remote"] == False:
					# Open remote episode link
					self.File.Open(self.media["Episode"]["Remote"]["Link"])

				# Wait for user to finish posting comment
				self.finished_posting_comment = self.Input.Type(self.language_texts["press_enter_when_you_finish_posting_the_comment"])

			self.Write_Comment_To_Files()

	def Define_Files(self):
		self.media["comment"] = {
			"file_name": "",
			"file": ""
		}

		# Comment file name for non-movies
		if self.media["States"]["Series media"] == True:
			add = False

			for alternative_episode_type in self.alternative_episode_types:
				if alternative_episode_type in self.media["Episode"]["Separator"]:
					add = True

			if add == True:
				self.media["comment"]["file_name"] += self.media["Episode"]["Separator"] + " "

			if self.media["States"]["Episodic"] == True:
				if "Number text" in self.media["Episode"]:
					self.media["comment"]["file_name"] += self.media["Episode"]["Number text"]

				else:
					self.media["comment"]["file_name"] += str(self.Text.Add_Leading_Zeroes(self.media["Episode"]["Number"]))

			if self.media["States"]["Episodic"] == False:
				self.media["comment"]["file_name"] = self.media["Episode"]["Title"]

		# Comment file name for movies or single unit media items
		if self.media["States"]["Series media"] == False or self.media["States"]["Single unit"] == True:
			self.media["comment"]["file_name"] = self.JSON.Language.language_texts["comment, title()"]

		# Add Re-watching text to comment file name if it exists
		if self.media["States"]["Re-watching"] == True:
			self.media["comment"]["file_name"] += self.media["Episode"]["re_watched"]["text"]

		# Media folder comment file
		self.media["Item"]["folders"]["comments"]["comment"] = self.media["Item"]["folders"]["comments"]["root"] + self.Sanitize(self.media["comment"]["file_name"], restricted_characters = True) + ".txt"
		self.File.Create(self.media["Item"]["folders"]["comments"]["comment"])

		# Read Comments.json file to get comments dictionary
		self.dictionaries["Root comments"] = self.JSON.To_Python(self.folders["comments"]["comments"])

		# Read selected media "Comments.json" file to get media comments dictionary
		self.dictionaries["Comments"] = self.JSON.To_Python(self.media["Item"]["folders"]["comments"]["comments"])

	def Write_Comment(self):
		# Define comment as an empty string
		self.media["comment"]["comment"] = {
			"Text": "",
			"Lines": [],
			"Line number": 0
		}

		# If backup is true and the comment is not a new one, get the comment from the backup file
		if self.dictionary["Comment Writer"]["States"]["backup"] == True and self.dictionary["Comment Writer"]["States"]["new"] == False:
			text = self.File.Contents(self.folders["comments"]["backups"]["backup"])["string"]

			self.media["comment"]["comment"]["Text"] += text
			self.media["comment"]["comment"]["Lines"].append(text)

			print()
			print("---")
			print()
			print(self.language_texts["loading_already_written_comment"] + "...")

		# Define the show text to be shown in the "Input.Lines" method
		show_text = "----------" + "\n\n"
		show_text += self.language_texts["comment_file_name"] + ":" + "\n"
		show_text += self.media["comment"]["file_name"] + "\n"
		show_text += "\n"

		# Define masculine or feminine text based on masculine or feminine text with function
		show_text += self.language_texts["type_the_comment_for_{}"].format(self.dictionary["Media type"]["Genders"][self.user_language]["the"] + " " + self.media["texts"]["unit"][self.user_language]) + ": "

		show_text += "\n\n" + "----------"

		# If the comment is a new one, add episode text to comment
		if self.dictionary["Comment Writer"]["States"]["new"] == True:
			key = "with_title"

			if self.media["States"]["Media item list"] == True and self.media["Item"]["Title"] != self.media["Title"] and self.media["States"]["Video"] == False and self.media["States"]["Single unit"] == False:
				key = "with_title_and_item"

			title = self.media["Episode"][key][self.user_language]

			if self.media["States"]["Series media"] == False:
				title += " (" + self.media["details"][self.JSON.Language.language_texts["original_name"]].split(" (")[-1]

			if self.media["States"]["Re-watching"] == True:
				title += self.media["Episode"]["re_watched"]["text"]

			# Define episode text (title)
			episode_text = self.JSON.Language.language_texts["title, title()"] + ":" + "\n" + title + "\n"

			self.media["comment"]["comment"]["Text"] += episode_text

			self.media["comment"]["comment"]["Lines"].append(self.JSON.Language.language_texts["title, title()"] + ":")
			self.media["comment"]["comment"]["Lines"].append(title)

			if self.media["States"]["Video"] == True:
				self.media["comment"]["comment"]["Text"] += self.media["Episode"]["ID"] + "\n"
				self.media["comment"]["comment"]["Lines"].append(self.media["Episode"]["ID"])

			self.media["comment"]["comment"]["Text"] += "\n"
			self.media["comment"]["comment"]["Lines"].append("")

			# Add the time text to the comment to be replaced by the commented time after finishing the comment
			self.media["comment"]["comment"]["Text"] += self.language_texts["time, title()"] + ":" + "\n" + "[Time]" + "\n"

			self.media["comment"]["comment"]["Lines"].append(self.language_texts["time, title()"] + ":")
			self.media["comment"]["comment"]["Lines"].append("[Time]")

			# If backup is true, backup comment to file
			if self.dictionary["Comment Writer"]["States"]["backup"] == True:
				self.File.Edit(self.folders["comments"]["backups"]["backup"], self.media["comment"]["comment"]["Text"], "a", next_line = False)

			# Add comment to show text
			show_text += "\n" + self.media["comment"]["comment"]["Text"]

			# Add "\n" to comment after adding comment to show text, to have a correct space before the input line
			self.media["comment"]["comment"]["Text"] += "\n"
			self.media["comment"]["comment"]["Lines"].append("")

		# If the comment is not a new one, load already written comment from backup file
		if self.dictionary["Comment Writer"]["States"]["new"] == False:
			show_text += "\n" + self.File.Contents(self.folders["comments"]["backups"]["backup"])["string"]

		# Ask for user to write comment
		dictionary = self.Input.Lines(show_text, line_options = {"print": True, "next_line": False}, backup_file = self.folders["comments"]["backups"]["backup"])

		# Add comment to the comment text string and lines list
		self.media["comment"]["comment"]["Text"] += dictionary["string"]
		self.media["comment"]["comment"]["Lines"].extend(dictionary["lines"])

		# Get line number
		self.media["comment"]["comment"]["Line number"] = len(self.media["comment"]["comment"]["Lines"])

		# Define comment time
		self.media["comment"]["time"] = self.Date.Now()

		# Replace time text in comment with comment time
		self.media["comment"]["comment"]["Text"] = self.media["comment"]["comment"]["Text"].replace("[Time]", self.Date.To_String(self.media["comment"]["time"]["date"].astimezone(), self.Date.language_texts["date_time_format"]))

		# Replace time text in comment with comment time
		self.media["comment"]["comment"]["Lines"][4] = self.media["comment"]["comment"]["Lines"][4].replace("[Time]", self.Date.To_String(self.media["comment"]["time"]["date"].astimezone(), self.Date.language_texts["date_time_format"]))

	def Write_Comment_To_Files(self):
		from copy import deepcopy

		# Delete backup file
		if self.dictionary["Comment Writer"]["States"]["backup"] == True:
			self.File.Delete(self.folders["comments"]["backups"]["backup"])

		# Add to total comment number
		self.dictionaries["Root comments"]["Numbers"]["Total"] += 1

		# Add to year comment number
		self.dictionaries["Root comments"]["Numbers"]["Years"][str(self.date["year"])] += 1

		# Add to media type comment number
		self.dictionaries["Root comments"]["Numbers"]["Type"][self.dictionary["Media type"]["Plural"]["en"]]["Total"] += 1

		# Add to media type comment number per year
		self.dictionaries["Root comments"]["Numbers"]["Type"][self.dictionary["Media type"]["Plural"]["en"]]["Years"][str(self.date["year"])] += 1

		# Update root Comments.json file to update numbers
		self.JSON.Edit(self.folders["comments"]["comments"], self.dictionaries["Root comments"])

		self.key = self.media["comment"]["file_name"]

		# Add comment file name to file names list
		self.dictionaries["Comments"]["Entries"].append(self.key)

		# Update media comments number
		self.dictionaries["Comments"]["Numbers"]["Total"] = len(self.dictionaries["Comments"]["Entries"])

		# Add comment file name, times, and titles keys to comment dictionary
		self.dictionaries["Comments"]["Dictionary"][self.key] = {
			"Number": self.dictionaries["Comments"]["Numbers"]["Total"],
			"Entry": self.key,
			"Type": self.dictionary["Media type"]["Plural"]["en"],
			"Titles": self.media["Episode"]["Titles"],
			"Time": self.Date.To_String(self.media["comment"]["time"]["utc"]),
			"Lines": self.media["comment"]["comment"]["Line number"]
		}

		# Add YouTube video ID, comment link, and comment ID to comment dictionary
		if self.media["States"]["Video"] == True:
			self.dictionaries["Comments"]["Dictionary"][self.key].pop("Time")

			lines = self.dictionaries["Comments"]["Dictionary"][self.key]["Lines"]
			self.dictionaries["Comments"]["Dictionary"][self.key].pop("Lines")

			self.dictionaries["Comments"]["Dictionary"][self.key].update({
				"ID": "",
				"Link": "",
				"Time": "",
				"Lines": lines,
				"Video": {
					"ID": self.media["Episode"]["ID"],
					"Link": self.remote_origins["YouTube"] + "watch?v=" + self.media["Episode"]["ID"],
					"Time": ""
				}
			})

			video_information = self.Get_YouTube_Information("video", self.dictionaries["Comments"]["Dictionary"][self.key]["Video"]["Link"])

			# Define video time as video published time gotten from YouTube API
			self.dictionaries["Comments"]["Dictionary"][self.key]["Video"]["Time"] = video_information["Time"]

			original_link = ""

			from urllib.parse import urlparse, parse_qs
			import validators

			while validators.url(original_link) != True:
				# Ask for YouTube comment link
				original_link = self.Input.Type(self.language_texts["paste_the_comment_link_of_youtube"])

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
			comment_date = self.Date.From_String(comment_information["Time"])

			# Define comment time as comment published time gotten from YouTube API
			self.dictionaries["Comments"]["Dictionary"][self.key]["Time"] = self.Date.To_String(comment_date)

			# Update time in comment file
			self.media["comment"]["comment"]["Text"] = self.media["comment"]["comment"]["Text"].splitlines()
			self.media["comment"]["comment"]["Text"][5] = self.Date.To_Timezone(comment_date)["date_time_format"][self.user_language]
			self.media["comment"]["comment"]["Text"] = self.Text.From_List(self.media["comment"]["comment"]["Text"])

		# Write comment into media folder comment file
		self.File.Edit(self.media["Item"]["folders"]["comments"]["comment"], self.media["comment"]["comment"]["Text"], "w")

		# Get states dictionary
		states_dictionary = self.Define_States_Dictionary(self.dictionary)["States"]

		if self.write_comment == True:
			for key in ["First entry in year", "First media type entry in year"]:
				if key in states_dictionary:
					states_dictionary.pop(key)

		# Remove the "Commented" state from the dictionary (because it is obvious that the user commented, it is a comment dictionary)
		if "Commented" in states_dictionary:
			states_dictionary.pop("Commented")

		# If the state dictionary is not empty, add it to the comment dictionary
		if states_dictionary != {}:
			self.dictionaries["Comments"]["Dictionary"][self.key]["States"] = states_dictionary

		# Import the collections module to sort the comments dictionary
		import collections

		# Sort media entries list and dictionary
		self.dictionaries["Comments"]["Entries"] = sorted(self.dictionaries["Comments"]["Entries"], key = str.lower)
		self.dictionaries["Comments"]["Dictionary"] = dict(collections.OrderedDict(sorted(self.dictionaries["Comments"]["Dictionary"].items())))

		if self.media["States"]["Episodic"] == False:
			# Re-numerate the Entry numbers inside entry dictionaries
			# (Numbers of the non-episodic media are wrong because the episode title is used as the dictionary key)
			number = 1
			for entry_name in self.dictionaries["Comments"]["Entries"]:
				self.dictionaries["Comments"]["Dictionary"][entry_name]["Number"] = number

				number += 1

		# Create "Comment" dictionary inside "Comment Writer" 
		self.dictionary["Comment Writer"]["Comment"] = deepcopy(self.dictionaries["Comments"]["Dictionary"][self.key])

		# Define the keys to be removed from the "Comment" dictionary
		keys_to_remove = [
			"Type",
			"Titles",
			"States",
			"Lines"
		]

		if self.media["States"]["Episodic"] == False:
			keys_to_remove.append("Number")

		# Remove not useful keys from "Comment" dictionary
		for key in keys_to_remove:
			if key in self.dictionary["Comment Writer"]["Comment"]:
				self.dictionary["Comment Writer"]["Comment"].pop(key)

		# Update the "Comments.json" file
		self.JSON.Edit(self.media["Item"]["folders"]["comments"]["comments"], self.dictionaries["Comments"])
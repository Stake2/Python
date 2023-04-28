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
				"Backup": True,
				"New": True,
				"Make": False,
				"Write": False
			}
		}

		if self.write_comment != False:
			self.dictionary["Comment Writer"]["States"]["Write"] = self.write_comment

		self.folders["comments"]["backups"]["backup"] = self.folders["comments"]["backups"]["root"] + "Backup.txt"

		# If the backup file exists, it is not a new comment and the user is going to write the comment
		if self.File.Exist(self.folders["comments"]["backups"]["backup"]) == True:
			self.dictionary["Comment Writer"]["States"]["New"] = False

			self.dictionary["Comment Writer"]["States"]["Write"] = True

		# If the backup file does not exist, ask the user if it wants to write a comment
		if self.File.Exist(self.folders["comments"]["backups"]["backup"]) == False and self.dictionary["Comment Writer"]["States"]["Write"] == False:
			self.dictionary["Comment Writer"]["States"]["Write"] = self.Input.Yes_Or_No(self.language_texts["write_a_comment"])

		if self.dictionary["Comment Writer"]["States"]["Write"] == True:
			self.media["States"]["Commented"] = True

			# Create backup file
			if self.dictionary["Comment Writer"]["States"]["Backup"] == True:
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
			if (
				self.dictionary["Media type"]["Plural"]["en"] in self.media_types["comment_posting"] and
				"Remote" in self.media["Episode"] and self.media["Episode"]["Remote"]["Link"] != "" and
				self.media["Episode"]["Remote"]["Title"] != "Animes Vision"
			):
				# Copy the comment
				self.Text.Copy(self.media["Comment"]["Text"]["String"])

				if self.media["States"]["Remote"] == False:
					# Open remote episode link
					self.File.Open(self.media["Episode"]["Remote"]["Link"])

				# Wait for user to finish posting comment
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
		if self.media["States"]["Series media"] == False or self.media["States"]["Single unit"] == True:
			self.media["Comment"]["File name"] = self.JSON.Language.language_texts["comment, title()"]

		# Add Re-watching text to comment file name if it exists
		if self.media["States"]["Re-watching"] == True:
			self.media["Comment"]["File name"] += self.media["Episode"]["re_watched"]["text"]

		# Media folder comment file
		self.media["Item"]["folders"]["comments"]["comment"] = self.media["Item"]["folders"]["comments"]["root"] + self.Sanitize(self.media["Comment"]["File name"], restricted_characters = True) + ".txt"
		self.File.Create(self.media["Item"]["folders"]["comments"]["comment"])

		# Read Comments.json file to get comments dictionary
		self.dictionaries["Root comments"] = self.JSON.To_Python(self.folders["comments"]["comments"])

		# Read selected media "Comments.json" file to get media comments dictionary
		self.dictionaries["Comments"] = self.JSON.To_Python(self.media["Item"]["folders"]["comments"]["comments"])

	def Write_Comment(self):
		# If backup is true and the comment is not a new one, get the comment from the backup file
		if self.dictionary["Comment Writer"]["States"]["Backup"] == True and self.dictionary["Comment Writer"]["States"]["New"] == False:
			text = self.File.Contents(self.folders["comments"]["backups"]["backup"])["string"]

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
		show_text += self.language_texts["type_the_comment_for_{}"].format(self.dictionary["Media type"]["Genders"][self.user_language]["the"] + " " + self.media["texts"]["unit"][self.user_language]) + ": "

		show_text += "\n\n" + "----------"

		# If the comment is a new one, add episode text to comment
		if self.dictionary["Comment Writer"]["States"]["New"] == True:
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

			self.media["Comment"]["Text"]["String"] += episode_text

			self.media["Comment"]["Text"]["Lines"].append(self.JSON.Language.language_texts["title, title()"] + ":")
			self.media["Comment"]["Text"]["Lines"].append(title)

			if self.media["States"]["Video"] == True:
				self.media["Comment"]["Text"]["String"] += self.media["Episode"]["ID"] + "\n"
				self.media["Comment"]["Text"]["Lines"].append(self.media["Episode"]["ID"])

			self.media["Comment"]["Text"]["String"] += "\n"
			self.media["Comment"]["Text"]["Lines"].append("")

			# Add the time text to the comment to be replaced by the commented time after finishing the comment
			self.media["Comment"]["Text"]["String"] += self.language_texts["time, title()"] + ":" + "\n" + "[Time]" + "\n"

			self.media["Comment"]["Text"]["Lines"].append(self.language_texts["time, title()"] + ":")
			self.media["Comment"]["Text"]["Lines"].append("[Time]")

			# If backup is true, backup comment to file
			if self.dictionary["Comment Writer"]["States"]["Backup"] == True:
				self.File.Edit(self.folders["comments"]["backups"]["backup"], self.media["Comment"]["Text"]["String"], "a", next_line = False)

			# Add comment to show text
			show_text += "\n" + self.media["Comment"]["Text"]["String"]

			# Add "\n" to comment after adding comment to show text, to have a correct space before the input line
			self.media["Comment"]["Text"]["String"] += "\n"
			self.media["Comment"]["Text"]["Lines"].append("")

		# If the comment is not a new one, load already written comment from backup file
		if self.dictionary["Comment Writer"]["States"]["New"] == False:
			show_text += "\n" + self.File.Contents(self.folders["comments"]["backups"]["backup"])["string"]

		# Ask for user to write comment
		dictionary = self.Input.Lines(show_text, line_options = {"print": True, "next_line": False}, backup_file = self.folders["comments"]["backups"]["backup"])

		# Add comment to the comment text string and lines list
		self.media["Comment"]["Text"]["String"] += dictionary["string"]
		self.media["Comment"]["Text"]["Lines"].extend(dictionary["lines"])

		# Get line number
		self.media["Comment"]["Line number"] = len(self.media["Comment"]["Text"]["Lines"])

		# Define comment time
		self.media["Comment"]["Date"] = self.Date.Now()

		# Replace time text in comment with comment time
		self.media["Comment"]["Text"]["String"] = self.media["Comment"]["Text"]["String"].replace("[Time]", self.media["Comment"]["Date"]["Formats"]["HH:MM DD/MM/YYYY"])

		# Replace time text in comment with comment time
		self.media["Comment"]["Text"]["Lines"][4] = self.media["Comment"]["Text"]["Lines"][4].replace("[Time]", self.media["Comment"]["Date"]["Formats"]["HH:MM DD/MM/YYYY"])

	def Write_Comment_To_Files(self):
		from copy import deepcopy

		# Delete backup file
		if self.dictionary["Comment Writer"]["States"]["Backup"] == True:
			self.File.Delete(self.folders["comments"]["backups"]["backup"])

		# Add to total comment number
		self.dictionaries["Root comments"]["Numbers"]["Total"] += 1

		# Add to year comment number
		self.dictionaries["Root comments"]["Numbers"]["Years"][str(self.date["Units"]["Year"])] += 1

		# Add to media type comment number
		self.dictionaries["Root comments"]["Numbers"]["Type"][self.dictionary["Media type"]["Plural"]["en"]]["Total"] += 1

		# Add to media type comment number per year
		self.dictionaries["Root comments"]["Numbers"]["Type"][self.dictionary["Media type"]["Plural"]["en"]]["Years"][str(self.date["Units"]["Year"])] += 1

		# Update root Comments.json file to update numbers
		self.JSON.Edit(self.folders["comments"]["comments"], self.dictionaries["Root comments"])

		self.key = self.media["Comment"]["File name"]

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
			"Date": self.media["Comment"]["Date"]["UTC"]["DateTime"]["Formats"]["YYYY-MM-DDTHH:MM:SSZ"],
			"Lines": self.media["Comment"]["Line number"]
		}

		# Add YouTube video ID, comment link, and comment ID to comment dictionary
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

			# Define video time as video published time gotten from YouTube API
			self.dictionaries["Comments"]["Dictionary"][self.key]["Video"]["Date"] = video_information["Date"]

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
			comment_date = self.Date.From_String(comment_information["Date"] )

			# Define comment time as comment published time gotten from YouTube API
			self.dictionaries["Comments"]["Dictionary"][self.key]["Date"] = self.Date.To_String(comment_date, utc = True)

			# Update time in comment file
			self.media["Comment"]["Text"]["String"] = self.media["Comment"]["Text"]["String"].splitlines()
			self.media["Comment"]["Text"]["String"][5] = self.Date.To_Timezone(comment_date)["Formats"]["HH:MM DD/MM/YYYY"]
			self.media["Comment"]["Text"]["String"] = self.Text.From_List(self.media["Comment"]["Text"]["String"])

		# Write comment into media folder comment file
		self.File.Edit(self.media["Item"]["folders"]["comments"]["comment"], self.media["Comment"]["Text"]["String"], "w")

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
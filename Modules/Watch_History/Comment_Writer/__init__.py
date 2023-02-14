# Comment_Writer.py

from Watch_History.Watch_History import Watch_History as Watch_History

class Comment_Writer(Watch_History):
	def __init__(self, media_dictionary, only_comment = False):
		super().__init__()

		self.media_dictionary = media_dictionary
		self.only_comment = only_comment

		self.media_dictionary["Comment Writer"] = {
			"States": {
				"backup": True,
				"new": True,
				"make": False,
				"write": False
			}
		}

		if self.only_comment != False:
			self.media_dictionary["Comment Writer"]["States"]["write"] = self.only_comment

		self.folders["comments"]["backups"]["backup"] = self.folders["comments"]["backups"]["root"] + "Backup.txt"

		# If the backup file exists, it is not a new comment and the user is going to write the comment
		if self.File.Exist(self.folders["comments"]["backups"]["backup"]) == True:
			self.media_dictionary["Comment Writer"]["States"]["new"] = False

			self.media_dictionary["Comment Writer"]["States"]["write"] = True

		# If the backup file does not exist, ask the user if it wants to write a comment
		if self.File.Exist(self.folders["comments"]["backups"]["backup"]) == False and self.media_dictionary["Comment Writer"]["States"]["write"] == False:
			self.media_dictionary["Comment Writer"]["States"]["write"] = self.Input.Yes_Or_No(self.language_texts["write_a_comment"])

		if self.media_dictionary["Comment Writer"]["States"]["write"] == True:
			self.media_dictionary["Media"]["States"]["Commented"] = True

			# Create backup file
			if self.media_dictionary["Comment Writer"]["States"]["backup"] == True:
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
				self.texts["animes"]["en"],
				self.texts["cartoons"]["en"],
				self.texts["videos"]["en"]
			]

			# If media type is inside the above list, and the episode is a remote one, open remote episode link to post comment
			if self.media_dictionary["media_type"]["plural"]["en"] in self.media_types["comment_posting"] and \
				"remote" in self.media_dictionary["Media"]["episode"] and self.media_dictionary["Media"]["episode"]["remote"]["link"] != "":
				# Copy the comment
				self.Text.Copy(self.media_dictionary["Media"]["comment"]["comment"])

				if self.media_dictionary["Media"]["States"]["remote"] == False:
					# Open remote episode link
					self.File.Open(self.media_dictionary["Media"]["episode"]["remote"]["link"])

				# Wait for user to finish posting comment
				self.finished_posting_comment = self.Input.Type(self.language_texts["press_enter_when_you_finish_posting_the_comment"])

			self.Write_Comment_To_Files()

	def Define_Files(self):
		self.media_dictionary["Media"]["comment"] = {
			"file_name": "",
			"file": ""
		}

		# Comment file name for non-movies
		if self.media_dictionary["Media"]["States"]["series_media"] == True:
			add = False

			for alternative_episode_type in self.alternative_episode_types:
				if alternative_episode_type in self.media_dictionary["Media"]["episode"]["separator"]:
					add = True

			if add == True:
				self.media_dictionary["Media"]["comment"]["file_name"] += self.media_dictionary["Media"]["episode"]["separator"] + " "

			if "number_text" in self.media_dictionary["Media"]["episode"] and self.media_dictionary["Media"]["States"]["episodic"] == True:
				self.media_dictionary["Media"]["comment"]["file_name"] += self.media_dictionary["Media"]["episode"]["number_text"]

			if self.media_dictionary["Media"]["States"]["video"] == True and self.media_dictionary["Media"]["States"]["episodic"] == False:
				self.media_dictionary["Media"]["comment"]["file_name"] = self.media_dictionary["Media"]["episode"]["title"]

			else:
				self.media_dictionary["Media"]["comment"]["file_name"] += str(self.Text.Add_Leading_Zeros(self.media_dictionary["Media"]["episode"]["number"]))

		# Comment file name for movies
		if self.media_dictionary["Media"]["States"]["series_media"] == False or self.media_dictionary["Media"]["States"]["single_unit"] == True:
			self.media_dictionary["Media"]["comment"]["file_name"] = self.language_texts["comment, title()"]

		# Media folder comment file
		self.media_dictionary["Media"]["item"]["folders"]["comments"]["comment"] = self.media_dictionary["Media"]["item"]["folders"]["comments"]["root"] + self.media_dictionary["Media"]["comment"]["file_name"] + ".txt"
		self.File.Create(self.media_dictionary["Media"]["item"]["folders"]["comments"]["comment"])

		# Read Comments.json file to get comments dictionary
		self.dictionaries["Root Comments"] = self.JSON.To_Python(self.folders["comments"]["comments"])

		# Read selected media "Comments.json" file to get media comments dictionary
		self.dictionaries["Comments"] = self.JSON.To_Python(self.media_dictionary["Media"]["item"]["folders"]["comments"]["comments"])

	def Write_Comment(self):
		# Define comment as an empty string
		self.media_dictionary["Media"]["comment"]["comment"] = ""

		# If backup is true and the comment is not a new one, get the comment from the backup file
		if self.media_dictionary["Comment Writer"]["States"]["backup"] == True and self.media_dictionary["Comment Writer"]["States"]["new"] == False:
			self.media_dictionary["Media"]["comment"]["comment"] += self.File.Contents(self.folders["comments"]["backups"]["backup"])["string"]

			print()
			print("---")
			print()
			print(self.language_texts["loading_already_written_comment"] + "...")

		# Define the show text to be shown in the "Input.Lines" method
		show_text = "----------" + "\n\n"
		show_text += self.language_texts["comment_file_name"] + ":" + "\n"
		show_text += self.media_dictionary["Media"]["comment"]["file_name"] + "\n"
		show_text += "\n"

		# Define masculine or feminine text based on masculine or feminine text with function
		show_text += self.language_texts["type_the_comment_for_{}"].format(self.media_dictionary["media_type"]["genders"][self.user_language]["the"] + " " + self.media_dictionary["Media"]["texts"]["unit"][self.user_language]) + ": "

		show_text += "\n\n" + "----------"

		# If the comment is a new one, add episode text to comment
		if self.media_dictionary["Comment Writer"]["States"]["new"] == True:
			key = "with_title"

			if self.media_dictionary["Media"]["States"]["media_list"] == True and self.media_dictionary["Media"]["item"]["title"] != self.media_dictionary["Media"]["title"] and self.media_dictionary["Media"]["States"]["video"] == False and self.media_dictionary["Media"]["States"]["single_unit"] == False:
				key = "with_title_and_item"

			title = self.media_dictionary["Media"]["episode"][key][self.user_language]

			if self.media_dictionary["Media"]["States"]["re_watching"] == True:
				title += self.media_dictionary["Media"]["episode"]["re_watched"]["text"]

			# Define episode text (episode title)
			episode_text = self.JSON.Language.language_texts["title, title()"] + ":" + "\n" + title + "\n"

			self.media_dictionary["Media"]["comment"]["comment"] += episode_text

			if self.media_dictionary["Media"]["States"]["video"] == True:
				self.media_dictionary["Media"]["comment"]["comment"] += self.media_dictionary["Media"]["episode"]["id"] + "\n"

			self.media_dictionary["Media"]["comment"]["comment"] += "\n"

			# Add the time text to the comment to be replaced by the commented time after finishing the comment
			self.media_dictionary["Media"]["comment"]["comment"] += self.language_texts["time, title()"] + ":" + "\n" + "[Time]" + "\n"

			# If backup is true, backup comment to file
			if self.media_dictionary["Comment Writer"]["States"]["backup"] == True:
				self.File.Edit(self.folders["comments"]["backups"]["backup"], self.media_dictionary["Media"]["comment"]["comment"], "a", next_line = False)

			# Add comment to show text
			show_text += "\n" + self.media_dictionary["Media"]["comment"]["comment"]

			# Add "\n" to comment after adding comment to show text, to have a correct space before the input line
			self.media_dictionary["Media"]["comment"]["comment"] += "\n"

		# If the comment is not a new one, load already written comment from backup file
		if self.media_dictionary["Comment Writer"]["States"]["new"] == False:
			show_text += "\n" + self.File.Contents(self.folders["comments"]["backups"]["backup"])["string"]

		# Ask for user to write comment
		self.media_dictionary["Media"]["comment"]["comment"] += self.Input.Lines(show_text, line_options = {"print": True, "next_line": False}, backup_file = self.folders["comments"]["backups"]["backup"])["string"]

		# Define comment time
		self.media_dictionary["Media"]["comment"]["time"] = self.Date.Now()

		# Replace time text in comment with comment time
		self.media_dictionary["Media"]["comment"]["comment"] = self.media_dictionary["Media"]["comment"]["comment"].replace("[Time]", self.Date.To_String(self.media_dictionary["Media"]["comment"]["time"]["date"].astimezone(), self.Date.language_texts["date_time_format"]))

	def Write_Comment_To_Files(self):
		# Delete backup file
		if self.media_dictionary["Comment Writer"]["States"]["backup"] == True:
			self.File.Delete(self.folders["comments"]["backups"]["backup"])

		# Update comments dictionary to add to comment numbers
		if self.only_comment == False:
			# Add to total comment number
			self.dictionaries["Root Comments"]["Numbers"]["Total"] += 1

			# Add to year comment number
			self.dictionaries["Root Comments"]["Numbers"]["Years"][str(self.date["year"])] += 1

			# Add to media type comment number
			self.dictionaries["Root Comments"]["Numbers"]["Type"][self.media_dictionary["media_type"]["plural"]["en"]]["Total"] += 1

			# Add to media type comment number per year
			self.dictionaries["Root Comments"]["Numbers"]["Type"][self.media_dictionary["media_type"]["plural"]["en"]]["Years"][str(self.date["year"])] += 1

			# Update root Comments.json file to update numbers
			self.JSON.Edit(self.folders["comments"]["comments"], self.dictionaries["Root Comments"])

		# Add comment file name to file names list
		self.dictionaries["Comments"]["Entries"].append(self.media_dictionary["Media"]["comment"]["file_name"])

		# Update media comments number
		self.dictionaries["Comments"]["Numbers"]["Total"] = len(self.dictionaries["Comments"]["Entries"])

		# Add comment file name, times, and titles keys to comment dictionary
		self.dictionaries["Comments"]["Dictionary"][self.media_dictionary["Media"]["comment"]["file_name"]] = {
			"Number": 0,
			"Entry": self.media_dictionary["Media"]["comment"]["file_name"],
			"Type": self.media_dictionary["media_type"]["plural"]["en"],
			"Titles": self.media_dictionary["Media"]["episode"]["titles"],
			"Time": self.Date.To_String(self.media_dictionary["Media"]["comment"]["time"]["utc"])
		}

		# Add YouTube video ID, comment link, and comment ID to comment dictionary
		if self.media_dictionary["Media"]["States"]["video"] == True:
			self.dictionaries["Comments"]["Dictionary"][self.media_dictionary["Media"]["comment"]["file_name"]].pop("Time")

			self.dictionaries["Comments"]["Dictionary"][self.media_dictionary["Media"]["comment"]["file_name"]].update({
				"ID": "",
				"Link": "",
				"Time": "",
				"Video": {
					"ID": self.media_dictionary["Media"]["episode"]["id"],
					"Link": self.media_dictionary["Media"]["episode"]["remote"]["link"],
					"Time": ""
				}
			})

			video_information = self.Get_YouTube_Information("video", self.dictionaries["Comments"]["Dictionary"][self.media_dictionary["Media"]["comment"]["file_name"]]["Video"]["Link"])

			# Define video time as video published time gotten from YouTube API
			self.dictionaries["Comments"]["Dictionary"][self.media_dictionary["Media"]["comment"]["file_name"]]["Video"]["Time"] = video_information["Time"]

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
			self.dictionaries["Comments"]["Dictionary"][self.media_dictionary["Media"]["comment"]["file_name"]].update({
				"ID": parameters["lc"][0],
				"Link": self.dictionaries["Comments"]["Dictionary"][self.media_dictionary["Media"]["comment"]["file_name"]]["Video"]["Link"] + "&lc=" + parameters["lc"][0]
			})

			comment_information = self.Get_YouTube_Information("comment", self.dictionaries["Comments"]["Dictionary"][self.media_dictionary["Media"]["comment"]["file_name"]]["Link"])

			comment_date = self.Date.From_String(comment_information["Time"])

			# Define comment time as comment published time gotten from YouTube API
			self.dictionaries["Comments"]["Dictionary"][self.media_dictionary["Media"]["comment"]["file_name"]]["Time"] = self.Date.To_String(comment_date)

			# Update time in comment file
			self.media_dictionary["Media"]["comment"]["comment"] = self.media_dictionary["Media"]["comment"]["comment"].splitlines()
			self.media_dictionary["Media"]["comment"]["comment"][5] = self.Date.To_Timezone(comment_date)["date_time_format"][self.user_language]
			self.media_dictionary["Media"]["comment"]["comment"] = self.Text.From_List(self.media_dictionary["Media"]["comment"]["comment"])

		# Write comment into media folder comment file
		self.File.Edit(self.media_dictionary["Media"]["item"]["folders"]["comments"]["comment"], self.media_dictionary["Media"]["comment"]["comment"], "w")

		if self.only_comment == False:
			dict_ = self.Define_States_Dictionary(self.media_dictionary)

			if "Commented" in dict_:
				dict_.pop("Commented")

			if dict_ != {}:
				self.dictionaries["Comments"]["Dictionary"][self.media_dictionary["Media"]["comment"]["file_name"]]["States"] = dict_

		# Re-numerate entry numbers inside entry dictionaries
		# (Numbers can be wrong if the media is non-episodic and uses the episode title as the dictionary key)
		number = 1
		for entry_name in self.dictionaries["Comments"]["Entries"]:
			self.dictionaries["Comments"]["Dictionary"][entry_name]["Number"] = number

			number += 1

		import collections

		# Sort media entries list and dictionary
		self.dictionaries["Comments"]["Entries"] = sorted(self.dictionaries["Comments"]["Entries"], key=str.lower)
		self.dictionaries["Comments"]["Dictionary"] = dict(collections.OrderedDict(sorted(self.dictionaries["Comments"]["Dictionary"].items())))

		# Update "Comments.json" file
		self.JSON.Edit(self.media_dictionary["Media"]["item"]["folders"]["comments"]["comment"], self.dictionaries["Comments"])
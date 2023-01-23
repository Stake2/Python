# Comment_Writer.py

from Watch_History.Watch_History import Watch_History as Watch_History

from urllib.parse import urlparse, parse_qs
import validators

class Comment_Writer(Watch_History):
	def __init__(self, media_dictionary):
		super().__init__()

		self.media_dictionary = media_dictionary

		self.media_dictionary["media"]["states"]["comment_writer"] = {
			"backup": True,
			"new": True,
			"make": False
		}

		self.folders["comments"]["backups"]["backup"] = self.folders["comments"]["backups"]["root"] + "Backup.txt"

		# If the backup file exists, it is not a new comment and the user is going to write the comment
		if self.File.Exist(self.folders["comments"]["backups"]["backup"]) == True:
			self.media_dictionary["media"]["states"]["comment_writer"]["new"] = False

			self.media_dictionary["media"]["states"]["comment_writer"]["write"] = True

		# If the backup file does not exist, ask the user if it wants to write a comment
		if self.File.Exist(self.folders["comments"]["backups"]["backup"]) == False:
			self.media_dictionary["media"]["states"]["comment_writer"]["write"] = self.Input.Yes_Or_No(self.language_texts["write_a_comment"])

		if self.media_dictionary["media"]["states"]["comment_writer"]["write"] == True:
			# Create backup file
			if self.media_dictionary["media"]["states"]["comment_writer"]["backup"] == True:
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
				self.texts["videos"]["en"],
			]

			# If media type is inside the above list, and the episode is a remote one, open remote episode link to post comment
			if self.media_dictionary["media_type"]["plural"]["en"] in self.media_types["comment_posting"] and \
				"remote" in self.media_dictionary["media"]["episode"] and self.media_dictionary["media"]["episode"]["remote"]["link"] != "":
				# Copy the comment
				self.Text.Copy(self.media_dictionary["media"]["comment"]["comment"])

				# Open remote episode link
				self.File.Open(self.media_dictionary["media"]["episode"]["remote"]["link"])

				# Wait for user to finish posting comment
				self.finished_posting_comment = self.Input.Type(self.language_texts["press_enter_when_you_finish_posting_the_comment"])

			self.Write_Comment_To_Files()

	def Define_Files(self):
		self.media_dictionary["media"]["comment"] = {
			"file_name": ""
		}

		# Media type comment file name for non-movies
		if self.media_dictionary["media"]["states"]["series_media"] == True:
			add = False
			for alternative_episode_type in self.alternative_episode_types:
				if alternative_episode_type in self.media_dictionary["media"]["episode"]["separator"]:
					add = True

			if add == True:
				self.media_dictionary["media"]["comment"]["file_name"] += self.media_dictionary["media"]["episode"]["separator"] + " "

			if "number_text" in self.media_dictionary["media"]["episode"]:
				self.media_dictionary["media"]["comment"]["file_name"] += self.media_dictionary["media"]["episode"]["number_text"]

			else:
				self.media_dictionary["media"]["comment"]["file_name"] += str(self.Text.Add_Leading_Zeros(self.media_dictionary["media"]["episode"]["number"]))

		# Media type comment file name for movies
		if self.media_dictionary["media"]["states"]["series_media"] == False:
			self.media_dictionary["media"]["comment"]["file_name"] = self.language_texts["comment, title()"]

		# Media type comments folder comment file
		self.media_dictionary["media"]["item"]["folders"]["media_type_comments"]["comment"] = self.media_dictionary["media"]["item"]["folders"]["media_type_comments"]["root"] + self.media_dictionary["media"]["comment"]["file_name"] + ".txt"
		self.File.Create(self.media_dictionary["media"]["item"]["folders"]["media_type_comments"]["comment"])

		# Media folder comment file
		self.media_dictionary["media"]["item"]["folders"]["comments"]["comment"] = self.media_dictionary["media"]["item"]["folders"]["comments"]["root"] + self.media_dictionary["media"]["comment"]["file_name"] + ".txt"
		self.File.Create(self.media_dictionary["media"]["item"]["folders"]["comments"]["comment"])

		# Read Comments.json file to get comments dictionary
		self.comments = self.JSON.To_Python(self.folders["comments"]["comments"])

		# Read selected media "Comments.json" file to get media comments dictionary
		self.media_comments = self.JSON.To_Python(self.media_dictionary["media"]["item"]["folders"]["media_type_comments"]["comments"])

	def Write_Comment(self):
		# Define comment as an empty string
		self.media_dictionary["media"]["comment"]["comment"] = ""

		# If backup is true and the comment is not a new one, get the comment from the backup file
		if self.media_dictionary["media"]["states"]["comment_writer"]["backup"] == True and self.media_dictionary["media"]["states"]["comment_writer"]["new"] == False:
			self.media_dictionary["media"]["comment"]["comment"] += self.File.Contents(self.folders["comments"]["backups"]["backup"])["string"]

			print()
			print("---")
			print()
			print(self.language_texts["loading_already_written_comment"] + "...")

		# Define the show text to be shown in the "Input.Lines" method
		show_text = "----------" + "\n\n"
		show_text += self.language_texts["comment_file_name"] + ":" + "\n"
		show_text += self.media_dictionary["media"]["comment"]["file_name"] + "\n"
		show_text += "\n"

		# Define masculine or feminine text based on masculine or feminine text with function
		show_text += self.language_texts["type_the_comment_for_{}"].format(self.media_dictionary["media_type"]["genders"]["the"] + " " + self.media_dictionary["media_type"]["singular"][self.user_language].lower()) + ": "

		show_text += "\n\n" + "----------"

		# If the comment is a new one, add episode text to comment
		if self.media_dictionary["media"]["states"]["comment_writer"]["new"] == True:
			key = "with_title"

			if self.media_dictionary["media"]["states"]["media_list"] == True and self.media_dictionary["media"]["item"]["title"] != self.media_dictionary["media"]["title"]:
				key = "with_title_and_item"

			title = self.media_dictionary["media"]["episode"][key][self.user_language]

			if self.media_dictionary["media"]["states"]["re_watching"] == True:
				title += self.media_dictionary["media"]["episode"]["re_watched"]["text"]

			# Define episode text (episode title)
			episode_text = self.language_texts["title, title()"] + ":" + "\n" + title + "\n"

			self.media_dictionary["media"]["comment"]["comment"] += episode_text + "\n"

			# Add the time text to the comment to be replaced by the commented time after finishing the comment
			self.media_dictionary["media"]["comment"]["comment"] += self.language_texts["time, title()"] + ":" + "\n" + "[Time]" + "\n"

			# If backup is true, backup comment to file
			if self.media_dictionary["media"]["states"]["comment_writer"]["backup"] == True:
				self.File.Edit(self.folders["comments"]["backups"]["backup"], self.media_dictionary["media"]["comment"]["comment"], "a", next_line = False)

			# Add comment to show text
			show_text += "\n" + self.media_dictionary["media"]["comment"]["comment"]

			# Add "\n" to comment after adding comment to show text, to have a correct space before the input line
			self.media_dictionary["media"]["comment"]["comment"] += "\n"

		# If the comment is not a new one, load already written comment from backup file
		if self.media_dictionary["media"]["states"]["comment_writer"]["new"] == False:
			show_text += "\n" + self.File.Contents(self.folders["comments"]["backups"]["backup"])["string"]

		# Ask for user to write comment
		self.media_dictionary["media"]["comment"]["comment"] += self.Input.Lines(show_text, line_options = {"print": True, "next_line": False}, backup_file = self.folders["comments"]["backups"]["backup"])["string"]

	def Write_Comment_To_Files(self):
		# Delete backup file
		if self.media_dictionary["media"]["states"]["comment_writer"]["backup"] == True:
			self.File.Delete(self.folders["comments"]["backups"]["backup"])

		# Define comment time
		self.media_dictionary["media"]["comment"]["time"] = self.Date.Now()

		# Replace time text in comment with comment time
		self.media_dictionary["media"]["comment"]["comment"] = self.media_dictionary["media"]["comment"]["comment"].replace("[Time]", self.media_dictionary["media"]["comment"]["time"]["date_time_format"][self.user_language])

		# Media type comment file
		self.File.Edit(self.media_dictionary["media"]["item"]["folders"]["media_type_comments"]["comment"], self.media_dictionary["media"]["comment"]["comment"], "w")

		# Media folder comment file
		self.File.Edit(self.media_dictionary["media"]["item"]["folders"]["comments"]["comment"], self.media_dictionary["media"]["comment"]["comment"], "w")

		# Add comment file name to file names list
		self.media_comments["File names"].append(self.media_dictionary["media"]["comment"]["file_name"])

		# Add comment file name, times, and titles keys to comment dictionary
		self.media_comments["Dictionary"][self.media_dictionary["media"]["comment"]["file_name"]] = {
			"File name": self.media_dictionary["media"]["comment"]["file_name"],
			"Times": {
				"date": str(self.media_dictionary["media"]["comment"]["time"]["date"]),
				"date_time_format": self.media_dictionary["media"]["comment"]["time"]["date_time_format"][self.user_language]
			},
			"Titles": self.media_dictionary["media"]["episode"]["titles"]
		}

		# Add YouTube video ID, comment link, and comment ID to comment dictionary
		if self.media_dictionary["media"]["states"]["video"] == True:
			self.media_comments["Dictionary"][self.media_dictionary["media"]["comment"]["file_name"]].update({
				"YouTube ID": self.media_dictionary["media"]["episode"]["youtube_id"],
			})

			if self.media_dictionary["media_type"]["plural"]["en"] in self.media_types["comment_posting"] and \
				"remote" in self.media_dictionary["media"]["episode"] and self.media_dictionary["media"]["episode"]["remote"]["link"] != "":
				link = ""

				while validators.url(link) != True:
					# Ask for YouTube comment link
					link = self.Input.Type(self.language_texts["paste_the_comment_link_of_youtube"])

				if validators.url(link) == True:
					self.media_comments["Dictionary"][self.media_dictionary["media"]["comment"]["file_name"]]["Link"] = link

					link = urlparse(link)
					query = link.query
					parameters = parse_qs(query)

					self.media_comments["Dictionary"][self.media_dictionary["media"]["comment"]["file_name"]]["ID"] = parameters["lc"][0]

		dict_ = {}

		keys = [
			"re_watching",
			"christmas",
			"watch_dubbed"
		]

		for key in keys:
			if self.media_dictionary["media"]["states"][key] == True:
				if key == "watch_dubbed":
					key = "dubbed"

				state = True

				if key == "re_watching":
					key = "re_watched"

					state = {
						"Times": self.media_dictionary["media"]["episode"]["re_watched"]["times"]
					}

				key = key.title()

				dict_[key] = state

		if dict_ != {}:
			self.media_comments["Dictionary"][self.media_dictionary["media"]["comment"]["file_name"]]["States"] = dict_

		# Update media type Comments.json file
		self.JSON.Edit(self.media_dictionary["media"]["item"]["folders"]["media_type_comments"]["comments"], self.media_comments)

		# --- #

		# Update comments dictionary to add to comment numbers

		# Add to total comment number
		self.comments["Number"] += 1

		# Add to year comment number
		self.comments["Year numbers"][str(self.date["year"])] += 1

		# Add to media type comment number
		self.comments["Media type numbers"][self.media_dictionary["media_type"]["plural"]["en"]] += 1

		# Add to media type year comment number
		self.comments["Media type year numbers"][str(self.date["year"])][self.media_dictionary["media_type"]["plural"]["en"]] += 1

		# Update root Comments.json file
		self.JSON.Edit(self.folders["comments"]["comments"], self.comments)
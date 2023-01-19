# Comment_Writer.py

from Watch_History.Watch_History import Watch_History as Watch_History

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
			if self.media_dictionary["media"]["states"]["comment_writer"]["backup"] == True:
				self.File.Create(self.folders["comments"]["backups"]["backup"])

			self.Define_Files()
			self.Write_Comment()
			self.Write_Comment_To_Files()

			print("----------")
			print()
			print(self.language_texts["you_finished_writing_the_comment"] + ".")

			media_types_with_comment_posting = [
				self.texts["animes"]["en"],
				self.texts["cartoons"]["en"],
				self.texts["videos"]["en"],
			]

			if self.media_dictionary["media_type"]["plural"]["en"] in media_types_with_comment_posting and \
				"remote" in self.media_dictionary["media"]["episode"] and self.media_dictionary["media"]["episode"]["remote"]["link"] != "":
				self.Text.Copy(self.media_dictionary["media"]["comment"]["comment"])

				self.File.Open(self.media_dictionary["media"]["episode"]["remote"]["link"])

				self.finished_posting_comment = self.Input.Type(self.language_texts["press_enter_when_you_finish_posting_the_comment"])

				if self.media_dictionary["media_type"]["plural"]["en"] == self.texts["videos"]["en"]:
					self.youtube_comment_link = self.Input.Type(self.language_texts["paste_the_comment_link_of_youtube"])

					self.youtube_comment_id = self.youtube_comment_link.split("&lc=")[1]

					self.File.Edit(self.all_comments_media_type_youtube_id_file, self.youtube_comment_id + "\n" + self.youtube_comment_link, "w")

	def Define_Files(self):
		self.media_dictionary["media"]["comment"] = {
			"file_name": ""
		}

		# Media type comment file name for non-movies
		if self.media_dictionary["media"]["states"]["series_media"] == True:
			for alternative_episode_type in self.alternative_episode_types:
				if alternative_episode_type in self.media_dictionary["media"]["episode"]["title"]:
					self.media_dictionary["media"]["comment"]["file_name"] += self.media_dictionary["media"]["episode"]["separator"] + " "

			if "number_text" in self.media_dictionary["media"]["episode"]:
				self.media_dictionary["media"]["comment"]["file_name"] += self.media_dictionary["media"]["episode"]["number_text"]

			else:
				self.media_dictionary["media"]["comment"]["file_name"] += str(self.Text.Add_Leading_Zeros(self.media_dictionary["media"]["episode"]["number"]))

			if self.media_dictionary["media"]["states"]["re_watching"] == True and self.media_dictionary["media"]["episode"]["re_watched"]["text"] != "":
				self.media_dictionary["media"]["comment"]["file_name"] += " " + self.media_dictionary["media"]["episode"]["re_watched"]["text"]

		# Media type comment file name for movies
		if self.media_dictionary["media"]["states"]["series_media"] == False:
			self.media_dictionary["media"]["comment"]["file_name"] = self.texts["comment, title()"]

		# Media type comments folder comment file
		self.media_dictionary["media"]["item"]["folders"]["media_type_comments"]["comment"] = self.media_dictionary["media"]["item"]["folders"]["media_type_comments"]["root"] + self.media_dictionary["media"]["comment"]["file_name"] + ".txt"
		self.File.Create(self.media_dictionary["media"]["item"]["folders"]["media_type_comments"]["comment"])

		# Media folder comment file
		self.media_dictionary["media"]["item"]["folders"]["comments"]["comment"] = self.media_dictionary["media"]["item"]["folders"]["comments"]["root"] + self.media_dictionary["media"]["comment"]["file_name"] + ".txt"
		self.File.Create(self.media_dictionary["media"]["item"]["folders"]["comments"]["comment"])

		# Read Comments.json file to get comments dictionary
		self.comments = self.Language.JSON_To_Python(self.folders["comments"]["comments"])

		self.media_comments = self.Language.JSON_To_Python(self.media_dictionary["media"]["item"]["folders"]["media_type_comments"]["comments"])

	def Write_Comment(self):
		self.media_dictionary["media"]["comment"]["comment"] = ""

		if self.media_dictionary["media"]["states"]["comment_writer"]["backup"] == True and self.media_dictionary["media"]["states"]["comment_writer"]["new"] == False:
			self.media_dictionary["media"]["comment"]["comment"] += self.File.Contents(self.folders["comments"]["backups"]["backup"])["string"]

			print()
			print("---")
			print()
			print(self.language_texts["loading_already_written_comment"] + "...")

		show_text = "----------" + "\n\n"
		show_text += self.language_texts["comment_file_name"] + ":" + "\n"
		show_text += self.media_dictionary["media"]["comment"]["file_name"] + "\n"
		show_text += "\n"

		# Define masculine or feminine text based on masculine or feminine text with function
		show_text += self.language_texts["type_the_comment_for_{}"].format(self.media_dictionary["media_type"]["genders"]["the"] + " " + self.media_dictionary["media_type"]["singular"][self.user_language].lower()) + ": "

		show_text += "\n\n" + "----------"

		if self.media_dictionary["media"]["states"]["comment_writer"]["new"] == True:
			key = "with_title"

			if self.media_dictionary["media"]["states"]["media_list"] == True:
				key = "with_title_and_item"

			episode_text = self.language_texts["title, title()"] + ":" + "\n" + self.media_dictionary["media"]["episode"][key][self.user_language] + "\n"

			self.media_dictionary["media"]["comment"]["comment"] += episode_text + "\n"

			self.media_dictionary["media"]["comment"]["comment"] += self.language_texts["time, title()"] + ":" + "\n" + "[Time]" + "\n"

			if self.media_dictionary["media"]["states"]["comment_writer"]["backup"] == True:
				self.File.Edit(self.folders["comments"]["backups"]["backup"], self.media_dictionary["media"]["comment"]["comment"], "a", next_line = False)

			show_text += "\n" + self.media_dictionary["media"]["comment"]["comment"]

			self.media_dictionary["media"]["comment"]["comment"] += "\n"

		if self.media_dictionary["media"]["states"]["comment_writer"]["new"] == False:
			show_text += "\n" + self.File.Contents(self.folders["comments"]["backups"]["backup"])["string"]

		self.media_dictionary["media"]["comment"]["comment"] += self.Input.Lines(show_text, line_options = {"print": True, "next_line": False}, backup_file = self.folders["comments"]["backups"]["backup"])["string"]

	def Write_Comment_To_Files(self):
		if self.media_dictionary["media"]["states"]["comment_writer"]["backup"] == True:
			self.File.Delete(self.folders["comments"]["backups"]["backup"])

		# Media type comment file
		self.File.Edit(self.media_dictionary["media"]["item"]["folders"]["media_type_comments"]["comment"], self.media_dictionary["media"]["comment"]["comment"], "w")

		# Media folder comment file
		self.File.Edit(self.media_dictionary["media"]["item"]["folders"]["comments"]["comment"], self.media_dictionary["media"]["comment"]["comment"], "w")
	
		# Define comment time
		self.media_dictionary["media"]["comment"]["time"] = self.Date.Now()

		# Replace time text in comment with comment time
		self.media_dictionary["media"]["comment"]["comment"] = self.media_dictionary["media"]["comment"]["comment"].replace("[Time]", self.media_dictionary["media"]["comment"]["time"]["date_time_format"][self.user_language])

		# Add comment file name to file names list
		self.media_comments["File names"].append(self.media_dictionary["media"]["comment"]["file_name"])

		# Add comment file name key to comments dictionary
		self.media_comments["Dictionary"][self.media_dictionary["media"]["comment"]["file_name"]] = {
			"File name": self.media_dictionary["media"]["comment"]["file_name"],
			"Times": {
				"date": str(self.media_dictionary["media"]["comment"]["time"]["date"]),
				"date_time_format": self.media_dictionary["media"]["comment"]["time"]["date_time_format"][self.user_language]
			},
			"Titles": self.media_dictionary["media"]["episode"]["titles"]
		}

		if self.media_dictionary["media"]["states"]["video"] == True:
			self.media_comments["Dictionary"][self.media_dictionary["media"]["comment"]["file_name"]]["YouTube ID"] = self.media_dictionary["media"]["episode"]["youtube_id"]

		# Update media type Comments.json file
		self.File.Edit(self.media_dictionary["media"]["item"]["folders"]["media_type_comments"]["comments"], self.Language.Python_To_JSON(self.media_comments), "w")

		# --- #

		# Update comments dictionary to add to comment numbers

		# Add to total comment number
		self.comments["Number"] += 1

		# Add to year comment number
		self.comments["Year numbers"][str(self.date["year"])] += 1

		# Add to media type comment number
		self.comments["Media type numbers"][self.media_dictionary["media_type"]["plural"]["en"]] += 1

		# Update root Comments.json file
		self.File.Edit(self.folders["comments"]["comments"], self.Language.Python_To_JSON(self.comments), "w")
# Comment_Writer.py

from Watch_History.Watch_History import Watch_History as Watch_History

class Comment_Writer(Watch_History):
	def __init__(self, media_dictionary):
		super().__init__()

		self.media_title = media_dictionary["media_title"]

		self.media_folder = media_dictionary["media_folder"]

		self.media_dictionary["media"]["episode"]["title"] = media_dictionary["media_episode"]

		self.plural_media_types = media_dictionary["plural_media_types"]
		self.singular_media_types = media_dictionary["singular_media_types"]
		self.mixed_plural_media_type = media_dictionary["mixed_plural_media_type"]

		self.media_dictionary["media"]["states"]["series_media"] = media_dictionary["is_series_media"]

		if self.media_dictionary["media"]["states"]["series_media"] == True:
			self.episode_number = media_dictionary["episode_number"]
			self.episode_number_text = media_dictionary["episode_number_text"]

		self.media_dictionary["media"]["states"]["media_list"] = media_dictionary["no_media_list"]
		self.media_dictionary["media"]["states"]["re_watching"] = media_dictionary["re_watching"]
		self.re_watched_string = media_dictionary["re_watched_string"]

		if self.media_dictionary["media"]["states"]["series_media"] == True:
			self.comments_folder = media_dictionary["comments_folder"]

		self.media_dictionary["media"]["item"] = media_dictionary["media_item"]
		self.media_dictionary["media"]["item"]["title_sanitized"] = media_dictionary["media_item_file_safe"]
		self.media_item_episode_with_title = media_dictionary["media_item_episode_with_title"]

		self.media_link = ""

		if "media_link" in media_dictionary:
			self.media_link = media_dictionary["media_link"]

		self.do_backup = True

		self.is_anime = False
		self.is_cartoon = False
		self.is_video = False

		self.all_comments_media_type_folder = self.all_comments_media_type_folders[self.plural_media_types["en"]]

		self.comment_backup_file = self.comment_writer_folder + "Comment Backup.txt"

		self.comment_backup_file_exists = False
		self.new_comment = True

		if self.File.Exist(self.comment_backup_file) == True:
			self.comment_backup_file_exists = True
			self.make_comment = True

			self.new_comment = False

		if self.comment_backup_file_exists == False:
			self.make_comment = self.Input.Yes_Or_No(self.language_texts["write_a_comment"])

		if self.make_comment == True:
			if self.do_backup == True:
				self.File.Create(self.comment_backup_file)

			self.Define_Files()
			self.Write_The_Comment()
			self.Write_The_Comment_To_Files()

			print("----------")
			print()
			print(self.language_texts["you_finished_writing_the_comment"] + ".")

			media_types_with_comment_posting = [
				self.texts["animes"]["en"],
				self.texts["cartoons"]["en"],
				self.texts["videos"]["en"],
			]

			if self.plural_media_types["en"] in media_types_with_comment_posting and self.media_link != "":
				self.Text.Copy(self.comment)

				self.File.Open(self.media_link)

				self.finished_posting_comment = self.Input.Type(self.language_texts["press_enter_when_you_finish_posting_the_comment"])

				if self.plural_media_types["en"] == self.texts["videos"]["en"]:
					self.youtube_comment_link = self.Input.Type(self.language_texts["paste_the_comment_link_of_youtube"])

					self.youtube_comment_id = self.youtube_comment_link.split("&lc=")[1]

					self.File.Edit(self.all_comments_media_type_youtube_id_file, self.youtube_comment_id + "\n" + self.youtube_comment_link, "w")

	def Define_Files(self):
		# Comment file for non-movies
		if self.media_dictionary["media"]["states"]["series_media"] == True:
			self.comment_file = self.comments_folder

			self.comment_file_name = ""

			for alternative_episode_type in self.alternative_episode_types:
				if alternative_episode_type in self.media_dictionary["media"]["episode"]["title"]:
					self.comment_file_name += alternative_episode_type + " "

			self.comment_file_name += self.episode_number_text

			if self.media_dictionary["media"]["states"]["re_watching"] == True and self.re_watched_string != "":
				self.comment_file_name += " " + self.re_watched_string

		# Comment file for movies
		if self.media_dictionary["media"]["states"]["series_media"] == False:
			self.comment_file = self.media_folder
			self.comment_file_name = self.texts["comment, title(), en - pt"]

		self.comment_file += self.comment_file_name + ".txt"

		self.File.Create(self.comment_file)

		# Media name folder on All comments folder by media type
		self.all_comments_media_type_media_title_folder = self.all_comments_media_type_folder + self.Sanitize(self.media_title, restricted_characters = True) + "/"
		self.Folder.Create(self.all_comments_media_type_media_title_folder)

		if self.media_dictionary["media"]["states"]["media_list"] == False and self.media_dictionary["media"]["item"] != self.media_title:
			self.all_comments_media_type_media_title_folder += self.media_dictionary["media"]["item"]["title_sanitized"] + "/"
			self.Folder.Create(self.all_comments_media_type_media_title_folder)

		if self.plural_media_types["en"] == self.texts["videos"]["en"]:
			self.all_comments_media_type_youtube_ids_folder = self.all_comments_media_type_media_title_folder + self.texts["youtube_ids"]["en"] + "/"
			self.Folder.Create(self.all_comments_media_type_youtube_ids_folder)

			self.all_comments_media_type_youtube_id_file = self.all_comments_media_type_youtube_ids_folder + self.comment_file_name + ".txt"
			self.File.Create(self.all_comments_media_type_youtube_id_file)

		# Media type comment file
		self.media_type_comment_file = self.all_comments_media_type_media_title_folder + self.comment_file_name + ".txt"
		self.File.Create(self.media_type_comment_file)

		# Media type comment number file
		self.media_type_comment_number_file = self.all_comment_number_media_type_files[self.plural_media_types["en"]]

		# Times file
		if self.media_dictionary["media"]["states"]["series_media"] == True:
			self.comment_times_folder = self.all_comments_media_type_media_title_folder + "Times/"
			self.Folder.Create(self.comment_times_folder)

			self.comment_times_file = self.comment_times_folder + self.comment_file_name + ".txt"
			self.File.Create(self.comment_times_file)

		if self.media_dictionary["media"]["states"]["series_media"] == False:
			self.comment_times_file = self.all_comments_media_type_media_title_folder + self.texts["when_commented, en - pt"] + ".txt"
			self.File.Create(self.comment_times_file)

		if self.global_switches["verbose"] == True:
			print()
			print(self.language_texts["comment_file"] + ":")
			print(self.comment_file)

			print()
			print(self.language_texts["media_type_comment_file"] + ":")
			print(self.media_type_comment_file)

			print()
			print(self.language_texts["media_type_comment_time_file"] + ":")
			print(self.comment_times_file)
			print()

	def Write_The_Comment(self):
		self.comment = ""

		if self.do_backup == True and self.new_comment == False:
			self.comment += self.File.Contents(self.comment_backup_file)["string"]

			print()
			print("---")
			print()
			print(self.language_texts["loading_already_written_comment"] + "...")

		self.the_text = self.gender_the_texts[self.plural_media_types["en"]]["the"]

		self.show_text = "----------" + "\n"
		self.show_text += "\n"
		self.show_text += self.language_texts["comment_file_name"] + ":" + "\n"
		self.show_text += self.comment_file_name + "\n"
		self.show_text += "\n"

		# Define masculine or feminine text based on masculine or feminine text with function
		self.show_text += self.language_texts["type_the_comment_for_{}"].format(self.the_text + " " + self.singular_media_types["language"].lower()) + ": "

		self.show_text += "\n\n" + "----------"

		if self.new_comment == True:
			self.full_episode_text = self.language_texts["title, title()"] + ":" + "\n" + self.media_item_episode_with_title + "\n"

			self.comment += self.full_episode_text

			if self.do_backup == True:
				self.File.Edit(self.comment_backup_file, self.comment, "a", next_line = False)

			self.comment += "\n"

			self.show_text += "\n" + self.full_episode_text[:-1] + "\n"

		if self.new_comment == False:
			self.show_text += "\n" + self.File.Contents(self.comment_backup_file)["string"]

		self.comment += self.Input.Lines(self.show_text, line_options = {"print": True, "next_line": False}, backup_file = self.comment_backup_file)["string"]

	def Write_The_Comment_To_Files(self):
		self.File.Edit(self.comment_file, self.comment, "w")

		self.File.Edit(self.media_type_comment_file, self.comment, "w")

		if self.do_backup == True:
			self.File.Delete(self.comment_backup_file)

		# All Comments Number file
		text_to_write = str(int(self.File.Contents(self.all_comments_number_file)["lines"][0]) + 1)
		self.File.Edit(self.all_comments_number_file, text_to_write, "w")

		# Year Comment Number file
		text_to_write = str(int(self.File.Contents(self.year_comment_number_file)["lines"][0]) + 1)
		self.File.Edit(self.year_comment_number_file, text_to_write, "w")

		# Media type comment number file
		text_to_write = str(int(self.File.Contents(self.media_type_comment_number_file)["lines"][0]) + 1)
		self.File.Edit(self.media_type_comment_number_file, text_to_write, "w")

		# Write current time to times comment file
		self.comment_time = self.Date.Now()["strftime"]

		text_to_write = self.comment_time
		self.File.Edit(self.comment_times_file, text_to_write, "w")
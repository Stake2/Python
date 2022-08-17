# Comment_Writer.py

from Script_Helper import *

from Watch_History.Watch_History import Watch_History as Watch_History

class Comment_Writer(Watch_History):
	def __init__(self):
		super().__init__()

		self.comment_writer_folder = self.media_network_folder + "Comment_Writer/"
		Create_Folder(self.comment_writer_folder, self.global_switches["create_folders"])

		self.all_comments_folder = self.comment_writer_folder + "All Comments - Todos Os Comentários/"
		Create_Folder(self.all_comments_folder, self.global_switches["create_folders"])

		for media_type in self.mixed_media_type_names_plural_without_none:
			media_type_comments_folder = self.all_comments_folder + media_type + "/"

			Create_Folder(media_type_comments_folder, self.global_switches["create_folders"])

		self.all_comments_media_type_folders = {}

		for media_type in self.mixed_media_type_names_plural_without_none:
			media_type_comments_folder = self.all_comments_folder + media_type + "/"

			Create_Folder(media_type_comments_folder, self.global_switches["create_folders"])

			self.all_comments_media_type_folders[media_type] = media_type_comments_folder

		self.all_comment_number_media_type_files = {}

		for media_type in self.mixed_media_type_names_plural_without_none:
			media_type_comment_number_file = self.all_comments_folder + media_type + "/Number" + self.dot_text

			Create_Text_File(media_type_comment_number_file, self.global_switches["create_files"])

			if len(Create_Array_Of_File(media_type_comment_number_file)) == 0:
				Write_To_File(media_type_comment_number_file, "0", self.global_switches)

			self.all_comment_number_media_type_files[media_type] = media_type_comment_number_file

		if self.global_switches["testing_script"] == True:
			self.global_switches["create_files"] = False

		# All Comments Number file
		self.all_comments_number_file = self.comment_writer_folder + "All Comments Number" + self.dot_text
		Create_Text_File(self.all_comments_number_file, self.global_switches["create_files"])

		if len(Create_Array_Of_File(self.all_comments_number_file)) == 0:
			Write_To_File(self.all_comments_number_file, "0", self.global_switches)

		self.year_comment_numbers_folder = self.comment_writer_folder + "Year Comment Numbers/"
		Create_Folder(self.year_comment_numbers_folder, self.global_switches["create_folders"])

		self.current_year_comment_number_folder = self.year_comment_numbers_folder + str(current_year) + "/"
		Create_Folder(self.current_year_comment_number_folder, self.global_switches["create_folders"])

		# Year Comment Number file
		self.year_comment_number_file = self.current_year_comment_number_folder + "Number" + self.dot_text
		Create_Text_File(self.year_comment_number_file, self.global_switches["create_files"])

		if len(Create_Array_Of_File(self.year_comment_number_file)) == 0:
			Write_To_File(self.year_comment_number_file, "0", self.global_switches)

class Write_Comment(Comment_Writer):
	def __init__(self, media_dict):
		super().__init__()

		self.media_title = media_dict["media_title"]

		self.media_folder = media_dict["media_folder"]

		self.media_episode = media_dict["media_episode"]

		self.english_media_type = media_dict["english_media_type"]
		self.mixed_media_type = media_dict["mixed_media_type"]
		self.language_singular_media_type = media_dict["language_singular_media_type"]

		self.is_series_media = media_dict["is_series_media"]

		if self.is_series_media == True:
			self.media_episode_number = media_dict["media_episode_number"]
			self.media_episode_number_text = media_dict["media_episode_number_text"]

		self.no_media_list = media_dict["no_media_list"]

		if self.is_series_media == True:
			self.comments_folder = media_dict["comments_folder"]

		self.media_item = media_dict["media_item"]
		self.media_item_file_safe = media_dict["media_item_file_safe"]
		self.media_item_episode_with_title = media_dict["media_item_episode_with_title"]

		self.do_backup = True

		self.is_anime = False
		self.is_cartoon = False
		self.is_video = False

		if self.mixed_media_type == self.mixed_media_type_anime_plural:
			self.is_anime = True

		if self.mixed_media_type == self.mixed_media_type_cartoon_plural:
			self.is_cartoon = True

		if self.mixed_media_type == self.mixed_media_type_video_plural:
			self.is_video = True

		self.all_comments_media_type_folder = self.all_comments_media_type_folders[self.mixed_media_type]

		self.comment_backup_file = self.comment_writer_folder + "Comment Backup" + self.dot_text

		self.comment_backup_file_exists = False
		self.new_comment = True

		if is_a_file(self.comment_backup_file) == True:
			self.comment_backup_file_exists = True
			self.make_comment = True

			self.new_comment = False

		if self.comment_backup_file_exists == False:
			self.make_comment = Yes_Or_No_Definer(Language_Item_Definer("Make comment", "Fazer comentário"), second_space = False)

		if self.make_comment == True:
			if self.do_backup == True:
				Create_Text_File(self.comment_backup_file, self.global_switches["create_files"])

			self.Define_Files()
			self.Write_Comment()
			self.Write_Comment_To_Files()

			print("----------")
			print()
			print(Language_Item_Definer("Finished writing comment", "Terminou de escrever comentário") + ".")

			if self.is_video == False:
				if self.is_anime == True or self.is_cartoon == True:
					Copy_Text(self.comment)

					self.choice_text = Language_Item_Definer("Press Enter when you finish posting the comment", "Pressione Enter quando você terminar de postar o comentário")

					self.finished_posting_comment = Select_Choice(self.choice_text, second_space = False)

	def Define_Files(self):
		# Comment file for non-movies
		if self.is_series_media == True:
			self.comment_file = self.comments_folder

			self.added_alternative_episode_type = False

			self.comment_file_name = ""

			for alternative_episode_type in self.alternative_episode_types:
				if alternative_episode_type in self.media_episode:
					self.comment_file_name += alternative_episode_type + " "

					self.added_alternative_episode_type = True

			self.comment_file_name += self.media_episode_number_text

		# Comment file for movies
		if self.is_series_media == False:
			self.comment_file = self.media_folder
			self.comment_file_name = self.mixed_comment_text

		self.comment_file += self.comment_file_name + self.dot_text

		Create_Text_File(self.comment_file, self.global_switches["create_files"])

		# Media name folder on All comments folder by media type
		self.all_comments_media_type_media_title_folder = self.all_comments_media_type_folder + Remove_Non_File_Characters(self.media_title) + "/"
		Create_Folder(self.all_comments_media_type_media_title_folder, self.global_switches["create_folders"])

		if self.no_media_list == False:
			self.all_comments_media_type_media_title_folder += self.media_item_file_safe + "/"
			Create_Folder(self.all_comments_media_type_media_title_folder, self.global_switches["create_folders"])

		# Media type comment file
		self.media_type_comment_file = self.all_comments_media_type_media_title_folder + self.comment_file_name + self.dot_text
		Create_Text_File(self.media_type_comment_file, self.global_switches["create_files"])

		if self.is_video == True:
			self.all_comments_media_type_youtube_ids_folder = self.all_comments_media_type_media_title_folder + "YouTube IDs/"
			Create_Folder(self.all_comments_media_type_youtube_ids_folder, self.global_switches["create_folders"])

			self.all_comments_media_type_youtube_id_file = self.all_comments_media_type_youtube_ids_folder + self.comment_file_name + self.dot_text
			Create_Text_File(self.all_comments_media_type_youtube_id_file, self.global_switches["create_folders"])

		# Media type comment number file
		self.media_type_comment_number_file = self.all_comment_number_media_type_files[self.mixed_media_type]

		# Times file
		if self.is_series_media == True:
			self.comment_times_folder = self.all_comments_media_type_media_title_folder + "Times/"
			Create_Folder(self.comment_times_folder, self.global_switches["create_folders"])

			self.comment_times_file = self.comment_times_folder + self.comment_file_name + self.dot_text
			Create_Text_File(self.comment_times_file, self.global_switches["create_files"])

		if self.is_series_media == False:
			self.comment_times_file = self.all_comments_media_type_media_title_folder + "When Commented - Quando Comentou" + self.dot_text
			Create_Text_File(self.comment_times_file, self.global_switches["create_files"])

		if self.global_switches["verbose"] == True:
			print()
			print("Comment File Name:")
			print(self.comment_file_name)

			print()
			print("Comment File:")
			print(self.comment_file)

			print()
			print("Media Type Comment File:")
			print(self.media_type_comment_file)

			print()
			print("Media Type Times Comment File:")
			print(self.comment_times_file)
			print()

	def Write_Comment(self):
		self.comment = ""

		if self.do_backup == True and self.new_comment == False:
			self.comment += Read_String(self.comment_backup_file)

			print()
			print(Language_Item_Definer("Loading already written comment", "Carregando comentário já escrito") + "...")

		self.the_text = self.gender_the_texts[self.mixed_media_type]["the"]

		self.show_text = "----------" + "\n\n"

		# Define masculine or feminine text based on masculine or feminine text with function
		self.show_text += Language_Item_Definer("Type the comment for {} {}", "Digite o comentário para {} {}").format(self.the_text, self.language_singular_media_type.lower()) + ": "

		self.show_text += "\n\n" + "----------"

		if self.new_comment == True:
			self.full_episode_text = "Título:\n" + self.media_item_episode_with_title + "\n"

			self.comment += self.full_episode_text

			if self.do_backup == True:
				Append_To_File(self.comment_backup_file, self.comment, self.global_switches)

			self.comment += "\n"

			self.show_text += "\n" + self.full_episode_text[:-1] + "\n"

		if self.new_comment == False:
			self.show_text += "\n" + Read_String(self.comment_backup_file)

		self.comment += Text_Writer(self.show_text, finish_text = "default_list", second_space = False, backup_file = self.comment_backup_file)

	def Write_Comment_To_Files(self):
		Write_To_File(self.comment_file, self.comment, self.global_switches)

		Write_To_File(self.media_type_comment_file, self.comment, self.global_switches)

		if self.is_video == True:
			print()

			Copy_Text(self.comment)

			self.youtube_comment_link = Select_Choice(Language_Item_Definer("Paste the YouTube Comment Link", "Cole o Link do Comentário do YouTube"), first_space = False)
			self.youtube_comment_id = self.youtube_comment_link.split("&lc=")[1]

			Write_To_File(self.all_comments_media_type_youtube_id_file, self.youtube_comment_id + "\n" + self.youtube_comment_link, self.global_switches)

		if self.do_backup == True:
			Remove_File(self.comment_backup_file)

		# All Comments Number file
		text_to_write = str(int(Create_Array_Of_File(self.all_comments_number_file)[0]) + 1)
		Write_To_File(self.all_comments_number_file, text_to_write, self.global_switches)

		# Year Comment Number file
		text_to_write = str(int(Create_Array_Of_File(self.year_comment_number_file)[0]) + 1)
		Write_To_File(self.year_comment_number_file, text_to_write, self.global_switches)

		# Media type comment number file
		text_to_write = str(int(Create_Array_Of_File(self.media_type_comment_number_file)[0]) + 1)
		Write_To_File(self.media_type_comment_number_file, text_to_write, self.global_switches)

		# Write current time to times comment file
		self.comment_time = time.strftime("%H:%M %d/%m/%Y")

		text_to_write = self.comment_time
		Write_To_File(self.comment_times_file, text_to_write, self.global_switches)
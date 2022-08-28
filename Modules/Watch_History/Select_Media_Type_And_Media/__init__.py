# Select_Media_Type_And_Media.py

# Script Helper importer
from Script_Helper import *

from Watch_History.Watch_History import Watch_History as Watch_History

from Watch_History.Media_Manager import *

class Select_Media_Type_And_Media(Watch_History):
	def __init__(self, lists_dict = None, status_text = None, first_space = False, second_space = True):
		super().__init__()

		self.language_media_type_list = Language_Item_Definer(self.media_type_names_english_plural, self.media_type_names_portuguese_plural)

		if "language_media_type_list" in lists_dict:
			self.language_media_type_list = lists_dict["language_media_type_list"]

		self.select_media_type = True

		if "select_media_type" in lists_dict:
			self.select_media_type = lists_dict["select_media_type"]

		self.select_media = True

		if "select_media" in lists_dict:
			self.select_media = lists_dict["select_media"]

		self.status_text = status_text

		if self.status_text == None:
			self.status_text = self.watching_english_text

		self.first_space = first_space
		self.second_space = second_space

		if self.select_media_type == True:
			self.Select_Media_Type()

			self.all_media_names = Create_Array_Of_File(self.media_info_name_files[self.english_media_type])

			self.media_info_names = Check_Media_Watching_Status(self.status_text).media_info_names

			if "media_list" not in lists_dict:
				self.media_list = self.media_info_names[self.english_media_type]

			if "media_list" in lists_dict and lists_dict["media_list"] == None:
				self.media_list = self.media_info_names[self.english_media_type]

			if "media_list" in lists_dict and lists_dict["media_list"] != None:
				self.media_list = lists_dict["media_list"]

				if lists_dict["media_list"] == "all":
					self.media_list = self.all_media_names

		if self.select_media == True:
			self.Select_Media()

	def Select_Media_Type(self):
		self.choice_info = Select_Media_Type(language_media_type_list = self.language_media_type_list, return_value = True, first_space = True, second_space = self.second_space)

		self.media_type_number = self.choice_info.media_type_number

		self.english_media_type = self.choice_info.english_media_type
		self.portuguese_media_type = self.choice_info.portuguese_media_type
		self.mixed_media_type = self.choice_info.mixed_media_type

		self.singular_media_type = self.choice_info.singular_media_type
		self.language_singular_media_type = self.choice_info.language_singular_media_type

		self.media_info_media_type_folder = self.choice_info.media_info_media_type_folder

		self.watching_status_files = self.choice_info.watching_status_files
		self.watching_status_media = self.choice_info.watching_status_media

	def Select_Media(self):
		self.choice_info = Select_Media(self.english_media_type, self.mixed_media_type, self.language_singular_media_type, self.media_list, self.media_info_media_type_folder, add_none = True, first_space = self.first_space, second_space = self.second_space)

		self.media = self.choice_info.media

		self.media_folder = self.choice_info.media_folder

		self.media_details = self.choice_info.media_details
		self.media_details_file = self.choice_info.media_details_file

		self.is_series_media = True

		if self.english_media_type == self.movie_media_type_english_plural:
			self.is_series_media = False
	
		if self.is_series_media == False:
			self.movie_details_file = self.choice_info.movie_details_file
			self.movie_details = self.choice_info.movie_details
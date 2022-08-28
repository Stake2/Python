# Select_Media.py

# Script Helper importer
from Script_Helper import *

from Watch_History.Watch_History import Watch_History as Watch_History

# Class for selecting media
class Select_Media(Watch_History):
	def __init__(self, english_media_type, mixed_media_type, language_singular_media_type, media_list, media_info_media_type_folder, add_none = False, first_space = False, second_space = True):
		super().__init__()

		self.add_none = add_none

		self.english_media_type = english_media_type
		self.language_singular_media_type = language_singular_media_type
		self.mixed_media_type = mixed_media_type
		self.media_list = media_list
		self.media_info_media_type_folder = media_info_media_type_folder

		if self.add_none == True:
			list_ = [None]
			list_.extend(self.media_list)
			self.media_list = list_

		self.first_space = first_space
		self.second_space = second_space

		self.Select()

	def Select(self):
		self.a_text = self.gender_the_texts[self.mixed_media_type]["a"]

		self.choice_text = Language_Item_Definer("Select {} {} to watch", "Selecione {} {} para assistir").format(self.a_text, self.language_singular_media_type)

		self.media = Select_Choice_From_List(self.media_list, alternative_choice_text = self.choice_text, add_none = False, return_first_item = True, first_space = self.first_space, second_space = self.second_space)

		self.media_folder = self.media_info_media_type_folder + Remove_Non_File_Characters(self.media) + "/"

		self.media_details_file = self.media_folder + self.media_details_english_text + self.dot_text
		self.media_details = Make_Setting_Dictionary(self.media_details_file, read_file = True)

		if self.english_media_type == self.movie_media_type_english_plural:
			self.movie_details_file = self.media_folder + self.movie_details_english_text + self.dot_text
			self.movie_details = Make_Setting_Dictionary(self.movie_details_file, read_file = True)
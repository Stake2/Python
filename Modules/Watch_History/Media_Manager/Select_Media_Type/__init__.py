# Select_Media_Type.py

# Script Helper importer
from Script_Helper import *

from Watch_History.Watch_History import Watch_History as Watch_History

# Class for selecting media type
class Select_Media_Type(Watch_History):
	def __init__(self, choice_text = None, language_media_type_list = None, return_value = False, first_space = False, second_space = True):
		super().__init__()

		self.choice_text = Language_Item_Definer("Select one media type to watch", "Selecione um tipo de mídia para assistir")

		if choice_text != None:
			self.choice_text = choice_text

		self.language_media_type_list = Language_Item_Definer(self.media_type_names_english_plural, self.media_type_names_portuguese_plural)

		if language_media_type_list != None:
			self.language_media_type_list = language_media_type_list

		self.english_media_type_list = self.media_type_names_english_plural
		self.portuguese_media_type_list = self.media_type_names_portuguese_plural

		self.return_value = return_value

		self.first_space = first_space
		self.second_space = second_space

		self.Select()

	def Select(self):
		self.choice_info = Select_Choice_From_List(self.language_media_type_list, alternative_choice_text = self.choice_text, second_choices_list = self.english_media_type_list, add_none = False, return_second_item_parameter = True, return_number = True, first_space = self.first_space, second_space = self.second_space)

		self.media_type_number = self.choice_info[1]

		self.english_media_type = self.english_media_type_list[self.media_type_number]
		self.portuguese_media_type = self.portuguese_media_type_list[self.media_type_number]
		self.mixed_media_type = self.mixed_media_type_names_plural_without_none[self.media_type_number - 1]

		self.singular_media_type = self.media_type_names_english[self.media_type_number]
		self.language_singular_media_type = Language_Item_Definer(self.media_type_names_english[self.media_type_number], self.media_type_names_portuguese[self.media_type_number])

		self.media_info_media_type_folder = self.media_info_folders[self.english_media_type]

		self.watching_status_files = {
			self.plan_to_watch_english_text: self.media_info_media_watching_status_files[self.english_media_type][self.plan_to_watch_english_text],
			self.watching_english_text: self.media_info_media_watching_status_files[self.english_media_type][self.watching_english_text],
			self.on_hold_english_text: self.media_info_media_watching_status_files[self.english_media_type][self.on_hold_english_text],
		}

		self.watching_status_media = {
			self.plan_to_watch_english_text: Create_Array_Of_File(self.watching_status_files[self.plan_to_watch_english_text]),
			self.watching_english_text: Create_Array_Of_File(self.watching_status_files[self.watching_english_text]),
			self.on_hold_english_text: Create_Array_Of_File(self.watching_status_files[self.on_hold_english_text]),
		}

		if self.return_value == True:
			return [self.english_media_type, self.media_info_media_type_folder]
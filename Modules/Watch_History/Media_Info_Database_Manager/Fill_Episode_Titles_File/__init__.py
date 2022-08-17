# Fill_Episode_Titles_File.py

# Script Helper importer
from Script_Helper import *

from Watch_History.Watch_History import Watch_History as Watch_History

from Watch_History.Media_Manager import *
from Watch_History.Select_Media_Type_And_Media import Select_Media_Type_And_Media as Select_Media_Type_And_Media
from Watch_History.Watch_Media import Watch_Media

class Fill_Episode_Titles_File(Watch_History):
	def __init__(self):
		super().__init__()

		self.media_info_names = Check_Media_Watching_Status().media_info_names

		self.movie_names = [
			"Movies",
			"Filmes",
		]

		self.media_type_names_english_plural.pop(0)

		for item in self.movie_names:
			if item in self.media_type_names_english_plural:
				self.media_type_names_english_plural.remove(item)

			if item in self.media_type_names_portuguese_plural:
				self.media_type_names_portuguese_plural.remove(item)

		self.language_media_type_list = Language_Item_Definer(self.media_type_names_english_plural, self.media_type_names_portuguese_plural)

		self.lists_dict = {}

		self.lists_dict["select_media"] = False
		self.lists_dict["language_media_type_list"] = self.language_media_type_list

		self.lists_dict["media_list"] = "all"

		self.choice_info = Select_Media_Type_And_Media(self.lists_dict, media_list = "all")

		# Media Type variables definition
		self.english_media_type = self.choice_info.english_media_type
		self.portuguese_media_type = self.choice_info.portuguese_media_type
		self.language_singular_media_type = self.choice_info.language_singular_media_type
		self.mixed_media_type = self.choice_info.mixed_media_type

		# Media variables definition (name, folder, and details)
		self.media_folder = self.choice_info.media_folder
		self.media_details = self.choice_info.media_details
		self.media_details_file = self.choice_info.media_details_file

		# Media variables definition (name, folder, and details)
		self.media_folder = self.choice_info.media_folder
		self.media_details = self.choice_info.media_details
		self.media_details_file = self.choice_info.media_details_file

		self.Watch_Media = Watch_Media(run_as_module = True, open_media = False, FETF = self)

		self.english_titles_file = self.Watch_Media.english_titles_file
		self.portuguese_titles_file = self.Watch_Media.portuguese_titles_file

		self.no_media_list = self.Watch_Media.no_media_list

		self.Define_Variables()
		self.Fill_Files()

		print(Language_Item_Definer("Finished filling episode title files", "Terminou de preencher os arquivos de título de episódio") + ".")

	def Define_Variables(self):
		self.episode_number_text = Language_Item_Definer("Type the number of episodes", "Digite o número de episódios")

		try:
			self.episode_number = Select_Choice(self.episode_number_text + " " + "(Ex: 01)", first_space = False, second_space = False, accept_enter = True, enter_equals_empty = True)
			self.episode_number = int(self.episode_number)

		except ValueError:
			self.episode_number = 1

		if self.no_media_list == False:
			try:
				self.all_episode_number = Select_Choice(Language_Item_Definer("Type the number of all media episodes", "Digite o número de todos os episódios da mídia"), first_space = False, second_space = False, accept_enter = True, enter_equals_empty = True)
				self.all_episode_number = int(self.all_episode_number)

			except ValueError:
				self.all_episode_number = 1

		print()
		print("---")
		print()

		self.items_to_remove = [
		"(",
		")",
		"\t",
		'"',
		]

	def Fill_Files(self):
		i = 1
		while i <= self.episode_number:
			self.english_title = Select_Choice(Language_Item_Definer("Paste the English episode title", "Cole o título de episódio em Inglês"), first_space = False, second_space = False)
			self.portuguese_title = Select_Choice(Language_Item_Definer("Paste the Portuguese episode title", "Cole o título de episódio em Português"), first_space = False, second_space = False)

			if " " in self.english_title[0]:
				self.english_title = self.english_title[:1]

			if " " in self.portuguese_title[0]:
				self.portuguese_title = self.portuguese_title[:1]

			if " " in self.english_title[-1]:
				self.english_title = self.english_title[:-1]

			if " " in self.portuguese_title[-1]:
				self.portuguese_title = self.portuguese_title[:-1]

			for item in self.items_to_remove:
				self.english_title = self.english_title.replace(item, "")
				self.portuguese_title = self.portuguese_title.replace(item, "")

			self.english_title = '"' + self.english_title + '"'
			self.portuguese_title = '"' + self.portuguese_title + '"'

			if self.no_media_list == False:
				self.local_all_episodes_number_text = "(" + str(Add_Leading_Zeros(self.all_episode_number)) + ")"

			self.current_episode_number = str(Add_Leading_Zeros(i))

			self.full_english_episode_title = "EP" + self.current_episode_number
			self.full_portuguese_episode_title = "EP" + self.current_episode_number

			if self.no_media_list == False:
				self.full_english_episode_title += str(self.local_all_episodes_number_text)
				self.full_portuguese_episode_title += str(self.local_all_episodes_number_text)

			self.full_english_episode_title += " " + self.english_title
			self.full_portuguese_episode_title += " " + self.portuguese_title

			text_to_append = self.full_english_episode_title
			Append_To_File(self.english_titles_file, text_to_append, self.global_switches, check_file_length = True)

			text_to_append = self.full_portuguese_episode_title
			Append_To_File(self.portuguese_titles_file, text_to_append, self.global_switches, check_file_length = True)

			print()
			print(self.full_english_episode_title)
			print(self.full_portuguese_episode_title)
			print()

			print("---")
			print()

			i += 1

			if self.no_media_list == False:
				self.all_episode_number += 1
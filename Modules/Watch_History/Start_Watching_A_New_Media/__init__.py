# Start_Watching_A_New_Media.py

# Script Helper importer
from Script_Helper import *

from Watch_History.Watch_History import Watch_History as Watch_History

from Watch_History.Watch_Media import *
from Watch_History.Media_Manager import *

# Class to set medias as To_Watch
class Start_Watching_A_New_Media(Watch_History):
	def __init__(self):
		super().__init__()

		self.Select_Media()

		self.Define_Media_Variables()
		self.Write_Media_Details()
		self.Write_Watching_Status()
		self.Show_Media_Info()
		self.Watch_Media()

	def Select_Media(self):
		self.status_text = [
			self.plan_to_watch_english_text,
			self.on_hold_english_text,
		]

		self.choice_info = Watch_Media(open_media = False, status_text = self.status_text)

	def Define_Media_Variables(self):
		# Media Type variables definition
		self.english_media_type = self.choice_info.english_media_type
		self.portuguese_media_type = self.choice_info.portuguese_media_type
		self.language_singular_media_type = self.choice_info.language_singular_media_type
		self.mixed_media_type = self.choice_info.mixed_media_type

		# Media variables definition (name, folder, and details)
		self.media_folder = self.choice_info.media_item_folder
		self.media_details = self.choice_info.media_details
		self.media_details_file = self.choice_info.media_details_file

		# Media title and Portuguese media title variables
		self.media_title = self.media_details["Original Name"]

		# Watching Status files and media
		self.watching_status_files = self.choice_info.watching_status_files
		self.watching_status_media = self.choice_info.watching_status_media

		self.plan_to_watch_file = self.watching_status_files[self.plan_to_watch_english_text]
		self.watching_file = self.watching_status_files[self.watching_english_text]
		self.on_hold_file = self.watching_status_files[self.on_hold_english_text]

		self.plan_to_watch_media = self.watching_status_media[self.plan_to_watch_english_text]
		self.watching_media = self.watching_status_media[self.watching_english_text]
		self.on_hold_media = self.watching_status_media[self.on_hold_english_text]

		self.no_media_list = self.choice_info.no_media_list

		self.is_series_media = self.choice_info.is_series_media

		if self.is_series_media == False:
			self.movie_details_file = self.choice_info.movie_details_file
			self.movie_details = self.choice_info.movie_details

		if self.is_series_media == True:
			self.portuguese_titles = self.choice_info.portuguese_titles

		if self.no_media_list == False:
			self.media_item_details = self.choice_info.media_item_details
			self.media_item_details_file = self.choice_info.media_item_details_file

		self.media_dates_file = self.media_folder + self.mixed_dates_text + self.dot_text
		self.media_dates = Create_Array_Of_File(self.media_dates_file)

		# Gets the first watching time where the user started watching the media
		self.started_watching_time = time.strftime("%H:%M %d/%m/%Y")

		self.watching_dates_text = self.mixed_started_watching_in_text + ":\n"

		self.watching_dates_text += self.started_watching_time

	def Write_Media_Details(self):
		# Writes the first watching time where the user started watching the media
		text_to_write = self.watching_dates_text
		Write_To_File(self.media_dates_file, text_to_write, self.global_switches)

		# Changes status to watching
		self.media_details["Status"] = self.watching_english_text

		# Writes first episode to media details file
		if self.is_series_media == True:
			self.media_episode = self.portuguese_titles[0]

			# Writes episode to media item details file
			if self.no_media_list == False:
				self.media_item_details["Episode"] = self.media_episode

				text_to_write = Stringfy_Dict(self.media_item_details)

				if Read_String(self.media_item_details_file) != text_to_write:
					Write_To_File(self.media_item_details_file, text_to_write, self.global_switches)

			if self.no_media_list == True:
				self.media_details["Episode"] = self.media_episode

		# Writes new status and episode to media details file
		text_to_write = Stringfy_Dict(self.media_details)

		if Read_String(self.media_details_file) != text_to_write:
			Write_To_File(self.media_details_file, text_to_write, self.global_switches)

	def Write_Watching_Status(self):
		text_to_write = ""

		self.file_to_write = None

		# Gets the file and text to write, to remove the selected media from the "plan to watch" or "on hold" Watching Status files
		for watching_status in self.status_text:
			watching_status_file = self.watching_status_files[watching_status]
			watching_status_media = self.watching_status_media[watching_status]

			if watching_status_media != []:
				for media_title in watching_status_media:
					if media_title == self.media_title:
						watching_status_media.remove(media_title)

						self.file_to_write = watching_status_file

				self.text_to_write = Stringfy_Array(sorted(watching_status_media), add_line_break = True)

		print(self.file_to_write)

		if Read_String(self.file_to_write) != text_to_write:
			Write_To_File(self.file_to_write, text_to_write, self.global_switches)

		# If media title is not in "Watching" Watching Status media list, then add it to the list
		if self.media_title not in self.watching_media:
			self.watching_media.append(self.media_title)

		text_to_write = Stringfy_Array(sorted(self.watching_media), add_line_break = True)

		if Read_String(self.watching_file) != text_to_write:
			Write_To_File(self.watching_file, text_to_write, self.global_switches)

	def Show_Media_Info(self):
		large_bar = "-----"
		dash_space = "-"

		# This text defined by language and word gender (this, esse) for non-series, and (this, essa) for series
		self.this_text = self.gender_the_texts[self.mixed_media_type]["this"]
		self.the_text = self.gender_the_texts[self.mixed_media_type]["the"]

		self.this_media_text = format(self.this_text) + " " + self.language_singular_media_type.lower()
		self.the_media_text = format(self.the_text) + " " + self.language_singular_media_type.lower()

		print()
		print(large_bar)
		print()
		print(Language_Item_Definer("Starting to watch {}", "Começando a assistir {}").format(self.this_media_text) + ":")
		print(self.media_title)
		print()

		print(Language_Item_Definer("At this time", "Nessa hora") + ":")
		print(self.started_watching_time)
		print()

		print(Language_Item_Definer("{} Details", "Detalhes d{}").format(self.the_media_text) + ":")

		for key in self.media_details:
			print(Language_Item_Definer(key, self.default_portuguese_template_parameters[key]) + ": " + self.media_details[key])

			if self.is_series_media == False:
				for movie_key in self.movie_details:
					if movie_key in ["Original Name - Nome Original", "Portuguese Name - Nome Português"] and key == "Original Name":
						print(movie_key + ": " + self.movie_details[movie_key])

		if self.is_series_media == False:
			for key in self.movie_details:
				if key not in ["Year - Ano", "Original Name - Nome Original", "Portuguese Name - Nome Português"]:
					print(key + ": " + self.movie_details[key])

		if self.no_media_list == False:
			print()
			print(Language_Item_Definer("Media Item Details", "Detalhes do Item de Mídi") + ":")

			for line in self.current_media_item_details:
				print(line)

			print()

			print(Language_Item_Definer("Episode", "Episódio") + ":")
			print(self.current_episode)

		print()
		print(large_bar)

	def Watch_Media(self):
		Watch_Media(run_as_module = True, choice_info = self.choice_info)
# Check_Media_Watching_Status.py

# Script Helper importer
from Script_Helper import *

from Watch_History.Watch_History import Watch_History as Watch_History

# Makes a list of the medias with a Watching status of "Watching" from the Watching status text file
class Check_Media_Watching_Status(Watch_History):
	def __init__(self, status_text = None):
		super().__init__()

		self.status_text = status_text

		if self.status_text == None:
			self.status_text = self.watching_english_text

		# Media info folders dictionary
		self.media_info_names = {}

		self.i = 1
		for media_info_folder in self.media_info_folders.values():
			if media_info_folder != None:
				self.current_watching_status = []

				self.english_media_type = self.media_type_names_english_plural[self.i]

				if type(self.status_text) == str:
					self.first_status_file = self.media_info_media_watching_status_files[self.english_media_type][self.status_text]

					if self.status_text == self.watching_english_text:
						self.second_status_file = self.media_info_media_watching_status_files[self.english_media_type][self.rewatching_english_text]

					self.current_watching_status.extend(Create_Array_Of_File(self.first_status_file))

					if self.status_text == self.watching_english_text:
						self.current_watching_status.extend(Create_Array_Of_File(self.second_status_file))

				if type(self.status_text) == list:
					for local_status_text in self.status_text:
						self.first_status_file = self.media_info_media_watching_status_files[self.english_media_type][local_status_text]

						if self.status_text == self.watching_english_text:
							self.second_status_file = self.media_info_media_watching_status_files[self.english_media_type][self.rewatching_english_text]

						self.current_watching_status.extend(Create_Array_Of_File(self.first_status_file))

						if self.status_text == self.watching_english_text:
							self.current_watching_status.extend(Create_Array_Of_File(self.second_status_file))

				self.media_info_names[self.english_media_type] = self.current_watching_status

				for self.media_title in self.media_info_names[self.english_media_type]:
					self.local_media_folder = self.local_medias_folder + Remove_Non_File_Characters(self.media_title) + "/"
					Create_Folder(self.local_media_folder, self.global_switches["create_folders"])

				self.i += 1

	def __dict__(self):
		return self.media_info_names
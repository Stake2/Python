# Start_Watching_Media.py

from Watch_History.Watch_History import Watch_History as Watch_History

from Watch_History.Watch_Media import Watch_Media as Watch_Media

# Class to set medias as To_Watch
class Start_Watching_Media(Watch_History):
	def __init__(self):
		super().__init__()

		self.Select_Media_To_Watch()
		self.Define_Media_Variables()

		self.Write_Media_Details()
		self.Write_Watching_Status()

		self.Watch_The_Media()

	def Select_Media_To_Watch(self):
		self.status_text = [
			self.language_texts["plan_to_watch, title()"],
			self.language_texts["on_hold, title()"],
		]

		self.Watch_Media = Watch_Media(open_media = False, status_text = self.status_text)

	def Define_Media_Variables(self):
		self.option_info = self.Watch_Media.option_info

		# Media Type variables definition
		self.plural_media_types = self.option_info["plural_media_type"]
		self.singular_media_types = self.option_info["singular_media_type"]
		self.mixed_plural_media_type = self.option_info["mixed_plural_media_type"]

		# Media variables definition (folder, details file, and details)
		self.media_folder = self.option_info["media_folder"]
		self.media_details_file = self.option_info["media_details_file"]
		self.media_details = self.File.Dictionary(self.media_details_file)

		# Media title and Portuguese media title variables
		self.media_title = self.media_details[self.language_texts["original_name"]]

		# Watching Status files and media
		self.watching_status_files = self.option_info["watching_status_files"]
		self.watching_status_media = self.option_info["watching_status_media"]

		self.media_dictionary["media"]["states"]["media_list"] = self.Watch_Media.no_media_list

		self.media_dictionary["media"]["states"]["series_media"] = self.Watch_Media.is_series_media

		if self.media_dictionary["media"]["states"]["series_media"] == True:
			self.episode_titles = self.Watch_Media.episode_titles
			self.language_episode_titles = self.Watch_Media.language_episode_titles

		if self.media_dictionary["media"]["states"]["media_list"] == False:
			self.media_dictionary["media"]["item"]["folders"]["root"] = self.Watch_Media.media_item_folder
			self.media_dictionary["media"]["item"]["details"] = self.Watch_Media.media_item_details
			self.media_dictionary["media"]["item"]["folders"]["details"] = self.Watch_Media.media_item_details_file

		self.media_dictionary = self.Watch_Media.media_dictionary

		self.media_dates_file = self.media_folder + self.texts["dates, title(), en - pt"] + ".txt"
		self.File.Create(self.media_dates_file)

		if self.media_dictionary["media"]["states"]["media_list"] == False:
			self.media_item_dates_file = self.media_dictionary["media"]["item"]["folders"]["root"] + self.texts["dates, title(), en - pt"] + ".txt"
			self.File.Create(self.media_item_dates_file)

		# Gets the first watching time where the user started watching the media
		self.started_watching_time = self.Date.Now()["strftime"]

		self.media_dates_text = self.language_texts["when_i_started_to_watch"] + ":\n"
		self.media_dates_text += self.started_watching_time

		self.item_dates_text = self.language_texts["when_i_started_to_watch"] + " " + self.media_dictionary["the_item_text"] + " " + self.media_dictionary["media"]["texts"]["item"] + ":\n"
		self.item_dates_text += self.started_watching_time

	def Write_Media_Details(self):
		# Writes the first watching time where the user started watching the media
		text_to_write = self.media_dates_text
		self.File.Edit(self.media_dates_file, text_to_write, "w")

		if self.media_dictionary["media"]["states"]["media_list"] == False:
			text_to_write = self.item_dates_text
			self.File.Edit(self.media_item_dates_file, text_to_write, "w")

		# Changes status to watching
		self.media_details[self.language_texts["status, title()"]] = self.language_texts["watching, title()"]

		# Writes first episode to media details file
		if self.media_dictionary["media"]["states"]["series_media"] == True:
			self.first_episode_title = self.language_episode_titles[0]

			# Writes episode to media item details file
			if self.media_dictionary["media"]["states"]["media_list"] == False:
				self.media_dictionary["media"]["item"]["details"][self.language_texts["episode, title()"]] = self.first_episode_title

				text_to_write = self.Text.From_Dictionary(self.media_dictionary["media"]["item"]["details"])

				self.File.Edit(self.media_dictionary["media"]["item"]["folders"]["details"], text_to_write, "w")

			if self.media_dictionary["media"]["states"]["media_list"] == True and self.media_dictionary["media"]["item"]["title"] != self.media_dictionary["media"]["title"]:
				self.media_details["Episode"] = self.first_episode_title

		# Writes new status and episode to media details file
		text_to_write = self.Text.From_Dictionary(self.media_details)

		self.File.Edit(self.media_details_file, text_to_write, "w")

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

				self.text_to_write = self.Text.From_List(sorted(watching_status_media, key=str.lower))

		self.File.Edit(self.file_to_write, text_to_write, "w")

		# If media title is not in "Watching" Watching Status media list, then add it to the list
		if self.media_title not in self.watching_status_media[self.language_texts["watching, title()"]]:
			self.watching_status_media[self.language_texts["watching, title()"]].append(self.media_title)

		text_to_write = self.Text.From_List(sorted(self.watching_status_media[self.language_texts["watching, title()"]], key=str.lower))
		self.File.Edit(self.watching_status_files[self.language_texts["watching, title()"]], text_to_write, "w")

	def Watch_The_Media(self):
		Watch_Media(run_as_module = True, option_info_parameter = self.option_info)
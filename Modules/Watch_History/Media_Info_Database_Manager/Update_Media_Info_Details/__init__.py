# Update_Media_Info_Details.py

from Watch_History.Watch_History import Watch_History as Watch_History

class Update_Media_Info_Details(Watch_History):
	def __init__(self):
		super().__init__()

		# Write to the "Media List - Lista de Mídias.txt" text file
		self.Update_Media_List()

		# Update Media Details Watching Status text files
		self.Update_Media_Watching_Status()

	def Update_Media_List(self):
		self.all_medias_number = 0
		for plural_media_type in self.texts["plural_media_types, type: list"]["en"]:
			media_type_number_file = self.media_info_number_files[plural_media_type]
			self.media_number = self.File.Contents(media_type_number_file)["lines"][0]

			self.all_medias_number += int(self.media_number)

		text_to_write = str(self.all_medias_number)

		self.File.Edit(self.media_number_file, text_to_write, "w")

		text_to_write = "Index - Sumário:\n\nNumber of Medias - Número de Mídias:\n" + str(self.all_medias_number) + "\n\n"

		i = 0
		self.all_medias_number = 0
		for plural_media_type in self.texts["plural_media_types, type: list"]["en"]:
			self.media_names_file = self.media_info_name_files[plural_media_type]
			media_type_number_file = self.media_info_number_files[plural_media_type]

			self.media_names = self.File.Contents(self.media_names_file)["lines"]
			self.media_number = self.File.Contents(media_type_number_file)["lines"][0]

			text_to_write += plural_media_type + ": " + self.media_number + "\n" + self.Text.From_List(self.media_names)

			if plural_media_type != self.texts["plural_media_types, type: list"]["en"][-1]:
				text_to_write += "\n\n"

			i += 1

		self.File.Edit(self.media_list_file, text_to_write, "w")

	def Update_Media_Watching_Status(self):
		self.sub_folders_to_remove = [
			"Completed - Completo",
			"Drawer - Gaveta",
			"Series List",
		]

		self.settings_to_remove = [
			"Current Episode",
			"Remote origin",
			"Origin location",
		]

		i = 0
		for plural_media_type in self.texts["plural_media_types, type: list"]["en"]:
			self.media_type_info_folder = self.media_info_folders[plural_media_type]

			self.media_names_file = self.media_info_name_files[plural_media_type]
			self.media_number_file = self.media_info_number_files[plural_media_type]

			self.media_names = self.File.Contents(self.media_names_file)["lines"]
			self.media_number = self.File.Contents(self.media_number_file)["lines"][0]

			for media_name in self.media_names:
				self.media_folder = self.media_type_info_folder + self.Sanitize(media_name, restricted_characters = True) + "/"
				self.media_details_file = self.media_folder + "Media details.txt"
				self.media_details = self.File.Dictionary(self.media_details_file)

				self.media_title = self.media_details[self.language_texts["original_name"]]

				if plural_media_type == self.texts["animes"]["en"]:
					if self.language_texts["romanized_name"] not in self.media_details:
						self.File.Open(self.media_details_file)
						input()
						self.media_details = self.File.Dictionary(self.media_details_file)

					self.media_title = self.media_details[self.language_texts["romanized_name"]]

				self.media_status = self.media_details[self.language_texts["status, title()"]]

				if plural_media_type != self.texts["movies"]["en"]:
					self.plural_file_name = self.media_type_sub_folders[plural_media_type]["media_list_text"]
					self.file_name = self.media_type_sub_folders[plural_media_type]["english_singular_media_list_text"]
					self.current_media_item_text = "Current " + self.file_name

					self.media_list_folder = self.media_folder + self.plural_file_name + "/"

					self.no_media_list = False

					if self.Folder.Exist(self.media_list_folder) == False:
						self.no_media_list = True

					if self.no_media_list == False:
						self.Folder.Create(self.media_list_folder)

						self.media_list_file = self.media_list_folder + self.plural_file_name + ".txt"
						self.File.Create(self.media_list_file)

						self.current_media_item_file = self.media_list_folder + self.current_media_item_text + ".txt"
						self.File.Create(self.current_media_item_file)

						self.media_list_names = self.File.Contents(self.media_list_file)["lines"]
						
						if self.media_list_names == None:
							self.media_list_names = []

						contents = self.Folder.Contents(self.media_list_folder)

						for item in self.sub_folders_to_remove:
							if item in contents["folder"]["names"]:
								contents["folder"]["names"].remove(item)

							if self.media_list_folder + item + "/" in contents["folder"]["list"]:
								contents["folder"]["list"].remove(self.media_list_folder + item + "/")

						if self.File.Contents(self.media_list_file)["lines"] == []:
							self.File.Edit(self.media_list_file, self.Text.From_List(contents["folder"]["names"]), "w")

				for watching_status in self.language_texts["watching_statuses, type: list"]:
					self.watching_status_file = self.watching_status_files[plural_media_type][watching_status]

					if self.media_details[self.language_texts["status, title()"]] not in self.watching_status_files[plural_media_type]:
						print(self.media_details_file)
						self.File.Open(self.media_details_file)
						input()
						self.media_details = self.File.Dictionary(self.media_details_file)

					self.correct_watching_status_file = self.watching_status_files[plural_media_type][self.media_details[self.language_texts["status, title()"]]]

					if self.media_title not in self.File.Contents(self.correct_watching_status_file)["lines"]:
						texts = self.File.Contents(self.correct_watching_status_file)["lines"]
						texts.append(self.media_title)

						self.File.Edit(self.correct_watching_status_file, self.Text.From_List(sorted(texts)), "w")

					if self.media_title in self.File.Contents(self.watching_status_file)["lines"] and self.media_status != watching_status:
						texts = self.File.Contents(self.watching_status_file)["lines"]

						if self.media_title in texts:
							texts.remove(self.media_title)

						self.File.Edit(self.watching_status_file, self.Text.From_List(sorted(texts)), "w")

			i += 1
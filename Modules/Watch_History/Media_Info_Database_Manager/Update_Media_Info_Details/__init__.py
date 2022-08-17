# Update_Media_Info_Details.py

# Script Helper importer
from Script_Helper import *

from Watch_History.Watch_History import Watch_History as Watch_History

class Update_Media_Info_Details(Watch_History):
	def __init__(self):
		super().__init__()

		# Write to the "Media List - Lista de Mídias.txt" text file
		self.Update_Media_List()

		# Update Media Details Watching Status text files
		self.Update_Media_Watching_Status()

	def Update_Media_List(self):
		i = 0
		self.all_medias_number = 0
		for mixed_plural_media_type in self.mixed_media_type_names_plural_without_none:
			singular_media_type = self.media_type_names[i + 1]
			self.media_number_file = self.media_info_number_files[singular_media_type]
			self.media_number = Create_Array_Of_File(self.media_number_file)[0]

			i += 1
			self.all_medias_number += int(self.media_number)

		text_to_write = str(self.all_medias_number)

		if Read_String(self.all_media_number_file) != text_to_write:
			Write_To_File(self.all_media_number_file, text_to_write, self.global_switches)

		text_to_write = "Index - Sumário:\n\nNumber of Medias - Número de Mídias:\n" + str(self.all_medias_number) + "\n\n"

		i = 0
		self.all_medias_number = 0
		for mixed_plural_media_type in self.mixed_media_type_names_plural_without_none:
			singular_media_type = self.media_type_names[i + 1]

			self.media_names_file = self.media_info_name_files[singular_media_type]
			self.media_number_file = self.media_info_number_files[singular_media_type]

			self.media_names = Create_Array_Of_File(self.media_names_file)
			self.media_number = Create_Array_Of_File(self.media_number_file)[0]

			text_to_write += mixed_plural_media_type + ": " + self.media_number + "\n" + Stringfy_Array(self.media_names, add_line_break = True)

			if mixed_plural_media_type != self.mixed_media_type_names_plural_without_none[-1]:
				text_to_write += "\n\n"

			i += 1

		if text_to_write != Read_String(self.media_list_file):
			Write_To_File(self.media_list_file, text_to_write, self.global_switches)

	def Update_Media_Watching_Status(self):
		self.sub_folders_to_remove = [
			"Completed - Completo",
			"Drawer - Gaveta",
			"Series List",
		]

		self.settings_to_remove = [
			"Current Episode",
			"Remote Origin",
			"Origin Location",
		]

		i = 0
		for mixed_plural_media_type in self.mixed_media_type_names_plural_without_none:
			singular_media_type = self.media_type_names[i + 1]
			self.media_type_info_folder = self.media_info_folders[singular_media_type]

			self.media_names_file = self.media_info_name_files[singular_media_type]
			self.media_number_file = self.media_info_number_files[singular_media_type]

			self.media_names = Create_Array_Of_File(self.media_names_file)
			self.media_number = Create_Array_Of_File(self.media_number_file)[0]

			for media_name in self.media_names:
				self.media_folder = self.media_type_info_folder + Remove_Non_File_Characters(media_name) + "/"
				self.media_details_file = self.media_folder + "Media Details" + self.dot_text
				self.media_details = Make_Setting_Dictionary(self.media_details_file, read_file = True)

				self.media_full_name = self.media_details["Original Name"]
				self.media_status = self.media_details["Status"]

				self.plural_file_name = self.media_type_sub_folders[mixed_plural_media_type]["media_list_text"]
				self.file_name = self.media_type_sub_folders[mixed_plural_media_type]["english_singular_media_list_text"]
				self.current_media_item_text = "Current " + self.file_name

				self.media_list_folder = self.media_folder + self.plural_file_name + "/"

				self.no_media_list = False

				if is_a_folder(self.media_list_folder) == False:
					self.no_media_list = True

				if mixed_plural_media_type == self.mixed_media_type_movie_plural:
					self.movie_details_file = self.media_folder + "Movie Details" + self.dot_text

					if is_a_file(self.movie_details_file) == True:
						string = Read_String(self.movie_details_file)

						if "Name - Nome:" in string:
							string = string.replace("Name - Nome", "Original Name - Nome Original")

						string = string.replace("Translated Name - Nome Traduzido", "Portuguese Name - Nome Português")
						string = string.replace("Distribution - Distribuição", "Distributor - Distribuidor")

						if "Translated Original Name - Nome Original Traduzido:" in string:
							string = string.replace("Translated Original Name - Nome Original Traduzido", "Portuguese Name - Nome Português")

						if string != Read_String(self.movie_details_file):
							Write_To_File(self.movie_details_file, string, self.global_switches)

				if mixed_plural_media_type != self.mixed_media_type_movie_plural:
					if "Episode" in self.media_details:
						self.new_media_details = {}

						if "Original Name" in self.media_details:
							self.new_media_details["Original Name"] = self.media_details["Original Name"]

						if "Full Name" in self.media_details:
							self.new_media_details["Original Name"] = self.media_details["Full Name"]

						if "Year" in self.media_details:
							self.new_media_details["Year"] = self.media_details["Year"]

						self.new_media_details["Status"] = self.media_details["Status"]

						if "Episode" in self.media_details:
							self.new_media_details["Episode"] = self.media_details["Episode"]

						if "Origin Type" in self.media_details:
							self.new_media_details["Origin Type"] = self.media_details["Origin Type"]

						if "Remote Origin" in self.media_details:
							self.new_media_details["Remote Origin"] = self.media_details["Remote Origin"]

						if "Origin Location" in self.media_details:
							self.new_media_details["Origin Location"] = self.media_details["Origin Location"]

						if self.new_media_details != self.media_details:
							Write_To_File(self.media_details_file, Stringfy_Dict(self.new_media_details), self.global_switches)

					if self.no_media_list == False:
						Create_Folder(self.media_list_folder, self.global_switches["create_folders"])

						self.season_file = self.media_list_folder + self.english_season_text + self.dot_text

						if is_a_file(self.season_file) == True:
							Remove_File(self.season_file, self.global_switches)

						# "Seasons.txt" > "Seasons - Temporadas.txt"
						self.seasons_file = self.media_list_folder + self.english_seasons_text + self.dot_text
						self.mixed_seasons_file = self.media_list_folder + self.mixed_seasons_text + self.dot_text

						# "Series.txt" > "Series - Séries.txt"
						self.series_file = self.media_list_folder + self.english_series_text + self.dot_text
						self.mixed_series_file = self.media_list_folder + self.mixed_series_text + self.dot_text

						if is_a_file(self.seasons_file) == True or is_a_file(self.series_file) == True:
							self.file_template = self.media_list_folder + "{}" + self.dot_text

							print()
							print(self.media_full_name)

							if is_a_file(self.seasons_file) == True:
								self.old_file = self.file_template.format(self.english_seasons_text)
								self.new_file = self.file_template.format(self.mixed_seasons_text)

							if is_a_file(self.series_file) == True:
								self.old_file =self.file_template.format(self.english_series_text)
								self.new_file = self.file_template.format(self.mixed_series_text)

							print(self.new_file)

							Move_File(self.old_file, self.new_file)

						self.media_list_file = self.media_list_folder + self.plural_file_name + self.dot_text
						Create_Text_File(self.media_list_file, self.global_switches["create_files"])

						self.current_media_item_file = self.media_list_folder + self.current_media_item_text + self.dot_text
						Create_Text_File(self.current_media_item_file, self.global_switches["create_files"])

						self.media_list_names = Create_Array_Of_File(self.media_list_file)
						
						if self.media_list_names == None:
							self.media_list_names = []

						folders = List_Folder(self.media_list_folder, add_none = False)

						for item in self.sub_folders_to_remove:
							if item in folders:
								folders.remove(item)

						if Read_String(self.media_list_file) != Stringfy_Array(folders, add_line_break = True) and Create_Array_Of_File(self.media_list_file) == []:
							Write_To_File(self.media_list_file, Stringfy_Array(folders, add_line_break = True), self.global_switches)

						self.delete_media_list_folder = False

						if Create_Array_Of_File(self.current_media_item_file) == [] and self.media_list_names != [] or Create_Array_Of_File(self.current_media_item_file) == [] and self.media_list_names == []:
							print()
							print(self.media_full_name)
							print(self.media_list_folder)

						if Create_Array_Of_File(self.current_media_item_file) == [] and self.media_list_names != []:
							print(self.current_media_item_file)

							if Read_String(self.current_media_item_file) != self.media_list_names[0]:
								Write_To_File(self.current_media_item_file, self.media_list_names[0], self.global_switches)
								input()

						if Create_Array_Of_File(self.current_media_item_file) == [] and self.media_list_names == []:
							print()
							print(Language_Item_Definer("Media list folder exists but no current media is defined", "Pasta de lista de mídia existe mas nenhuma mídia atual está definida") + ".")

							self.delete_media_list_folder = Yes_Or_No_Definer(Language_Item_Definer("Delete media list folder", "Apagar pasta de lista de mídia"), second_space = False)

							if self.delete_media_list_folder == False:
								Open_Text_File(self.media_list_file)
								Open_Text_File(self.current_media_item_file)
								input()
								self.media_list_names = Create_Array_Of_File(self.media_list_file)

							if self.delete_media_list_folder == True:
								Remove_Folder(self.media_list_folder, self.global_switches)

								if self.current_media_item_text in self.media_details:
									self.media_details.pop(self.current_media_item_text)

						if self.delete_media_list_folder == False:
							self.current_media_item = Create_Array_Of_File(self.current_media_item_file)[0]
							self.current_media_item_folder = self.media_list_folder + Remove_Non_File_Characters(self.current_media_item) + "/"
							Create_Folder(self.current_media_item_folder, self.global_switches["create_folders"])

							self.media_item_details_file = self.current_media_item_folder + "Media Details" + self.dot_text
							Create_Text_File(self.media_item_details_file, self.global_switches["create_files"])

							self.new_media_details = {}

							if self.current_media_item_text in self.media_details:
								list_ = [
								"Status",
								self.current_media_item_text,
								"Origin Type",
								"Has Dub",
								"Year",
								]

								self.new_media_details.update(self.media_details)

								if self.current_media_item_text in self.media_details:
									self.new_media_details["Full Name"] = self.media_details[self.current_media_item_text]

								for item in list_:
									if item in self.new_media_details:
										self.new_media_details.pop(item)

							if Read_String(self.media_item_details_file) != Stringfy_Dict(self.new_media_details) and Create_Array_Of_File(self.media_item_details_file) == []:
								Write_To_File(self.media_item_details_file, Stringfy_Dict(self.new_media_details), self.global_switches)

							if self.current_media_item_text in self.media_details:
								self.media_details.pop(self.current_media_item_text)

							for item in self.settings_to_remove:
								if item in self.media_details:
									self.media_details.pop(item)

							if Read_String(self.media_details_file) != Stringfy_Dict(self.media_details):
								Write_To_File(self.media_details_file, Stringfy_Dict(self.media_details), self.global_switches)

							for media_item in self.media_list_names:
								self.current_media_item_folder = self.media_list_folder + Remove_Non_File_Characters(media_item) + "/"
								Create_Folder(self.current_media_item_folder, self.global_switches["create_folders"])

								self.media_item_details_file = self.current_media_item_folder + "Media Details" + self.dot_text
								Create_Text_File(self.media_item_details_file, self.global_switches["create_files"])

								self.titles_folder = self.current_media_item_folder + self.mixed_titles_text + "/"
								Create_Folder(self.titles_folder, self.global_switches["create_folders"])

								self.english_titles_file = self.titles_folder + full_language_en + self.dot_text
								Create_Text_File(self.english_titles_file, self.global_switches["create_files"])

								self.portuguese_titles_file = self.titles_folder + full_language_pt + self.dot_text
								Create_Text_File(self.portuguese_titles_file, self.global_switches["create_files"])

								self.media_item_details = Make_Setting_Dictionary(self.media_item_details_file, read_file = True)

								if "Current Episode" in self.media_item_details:
									self.new_media_item_details = {}

									if "Original Name" in self.media_item_details:
										self.new_media_item_details["Original Name"] = self.media_item_details["Original Name"]

									if "Full Name" in self.media_item_details:
										self.new_media_item_details["Original Name"] = self.media_item_details["Full Name"]

									if "Year" in self.media_item_details:
										self.new_media_item_details["Year"] = self.media_item_details["Year"]

									if "Status" in self.media_item_details:
										self.new_media_item_details["Status"] = self.media_item_details["Status"]

									if "Current Episode" in self.media_item_details:
										self.new_media_item_details["Episode"] = self.media_item_details["Current Episode"]

									if "Episode" in self.media_item_details:
										self.new_media_item_details["Episode"] = self.media_item_details["Episode"]

									if "Origin Type" in self.media_item_details:
										self.new_media_item_details["Origin Type"] = self.media_item_details["Origin Type"]

									if "Remote Origin" in self.media_item_details:
										self.new_media_item_details["Remote Origin"] = self.media_item_details["Remote Origin"]

									if "Origin Location" in self.media_item_details:
										self.new_media_item_details["Origin Location"] = self.media_item_details["Origin Location"]

									if Read_String(self.correct_watching_status_file) != Stringfy_Dict(self.new_media_item_details):
										Write_To_File(self.media_item_details_file, Stringfy_Dict(self.new_media_item_details), self.global_switches)

								self.media_item_details = {}
								self.media_item_details.update(self.new_media_details)

								self.media_item_details["Original Name"] = media_item
								self.media_item_details["Episode"] = "None"

				for watching_status in self.english_watching_statuses:
					self.watching_status_file = self.media_info_media_watching_status_files[singular_media_type][watching_status]
					self.correct_watching_status_file = self.media_info_media_watching_status_files[singular_media_type][self.media_details["Status"]]

					if self.media_full_name not in Create_Array_Of_File(self.correct_watching_status_file):
						texts = Create_Array_Of_File(self.correct_watching_status_file)
						texts.append(self.media_full_name)

						if Read_String(self.correct_watching_status_file) != Stringfy_Array(sorted(texts), add_line_break = True):
							Write_To_File(self.correct_watching_status_file, Stringfy_Array(sorted(texts), add_line_break = True), self.global_switches)

					if self.media_full_name in Create_Array_Of_File(self.watching_status_file) and self.media_status != watching_status:
						texts = Create_Array_Of_File(self.watching_status_file)

						if self.media_full_name in texts:
							texts.remove(self.media_full_name)

						if Read_String(self.watching_status_file) != Stringfy_Array(sorted(texts), add_line_break = True):
							Write_To_File(self.watching_status_file, Stringfy_Array(sorted(texts), add_line_break = True), self.global_switches)

			i += 1
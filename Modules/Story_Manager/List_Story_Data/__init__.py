# List_Story_Data.py

# Script Helper importer
from Script_Helper import *

from Story_Manager.Story_Manager import *

class List_Story_Data(Story_Manager):
	def __init__(self):
		super().__init__(select_story = False)

		self.Make_Lists()
		self.Show_Lists()

	def Make_Lists(self):
		self.story_names = Create_Array_Of_File(self.story_database_files["Names"])
		self.story_authors_text = Create_Array_Of_File(self.story_database_files["Author(s)"])
		self.story_creation_dates_text = Create_Array_Of_File(self.story_database_files["Creation Date"])
		self.story_statuses_text = Create_Array_Of_File(self.story_database_files["Status"])
		self.story_website_link_names_text = Create_Array_Of_File(self.story_database_files["Website Link Name"])

		self.english_story_names = {}
		self.portuguese_story_names = {}
		self.story_folders = {}
		self.story_authors = {}
		self.story_creation_dates = {}
		self.story_statuses = {}
		self.story_website_link_names = {}
		self.story_chapter_numbers = {}
		self.story_reader_numbers = {}
		self.story_reader_files = {}

		i = 0
		for story_name in self.story_names:
			split = story_name.split(", ")
			english_story_name = split[0]
			portuguese_story_name = split[1]

			story_folder_name = Split_And_Add_Text(english_story_name, new_separator = "/")

			story_folder = self.stories_folder + story_folder_name + "/"
			self.story_info_folder = story_folder + "Story Info/"

			self.story_chapters_folder = story_folder + self.main_story_folders[0] + "/"
			Create_Folder(self.story_chapters_folder, self.global_switches["create_folders"])

			self.english_chapters_folder = self.story_chapters_folder + full_language_en + "/"
			Create_Folder(self.english_chapters_folder, self.global_switches["create_folders"])

			self.english_chapter_titles_folder = self.english_chapters_folder + "Titles/"
			Create_Folder(self.english_chapter_titles_folder, self.global_switches["create_folders"])

			self.english_chapter_titles_file = self.english_chapter_titles_folder + "Titles" + self.dot_text
			Create_Text_File(self.english_chapter_titles_file, self.global_switches["create_files"])

			readers_and_reads_folder = story_folder + self.main_story_folders[2] + "/"
			Create_Folder(readers_and_reads_folder, self.global_switches["create_folders"])

			story_reader_file = readers_and_reads_folder + "Readers" + self.dot_text
			Create_Text_File(story_reader_file, self.global_switches["create_files"])

			self.story_authors_file = self.story_info_folder + "Author" + self.dot_text
			Create_Text_File(self.story_authors_file, self.global_switches["create_files"])
			story_authors_text = Create_Array_Of_File(self.story_authors_file)

			story_creation_date = self.story_creation_dates_text[i]

			story_status = self.story_statuses_text[i]

			if "SpaceLiving" in story_folder_name:
				story_folder_name = "New World/" + story_folder_name

			story_website_link_name = mega_stake2_website_link + story_folder_name + "/"

			self.english_chapter_titles = Create_Array_Of_File(self.english_chapter_titles_file)

			story_chapter_number = Language_Item_Definer("None", "Nenhum")

			if self.english_chapter_titles != None:
				story_chapter_number = len(self.english_chapter_titles)

			reader_number = len(Create_Array_Of_File(story_reader_file))

			if reader_number == 1 and Create_Array_Of_File(story_reader_file)[0] == "No Readers - Sem Leitores":
				reader_number = Language_Item_Definer("None", "Nenhum")

			# ---

			self.english_story_names[english_story_name] = english_story_name
			self.portuguese_story_names[english_story_name] = portuguese_story_name
			self.story_folders[english_story_name] = story_folder
			self.story_authors[english_story_name] = story_authors_text
			self.story_creation_dates[english_story_name] = story_creation_date
			self.story_statuses[english_story_name] = story_status
			self.story_website_link_names[english_story_name] = story_website_link_name
			self.story_chapter_numbers[english_story_name] = story_chapter_number
			self.story_reader_numbers[english_story_name] = reader_number
			self.story_reader_files[english_story_name] = story_reader_file

			# ---

			i += 1

	def Show_Lists(self):
		for self.english_story_name in self.english_story_names.values():
			self.portuguese_story_name = self.portuguese_story_names[self.english_story_name]
			self.story_folder = self.story_folders[self.english_story_name]
			self.local_story_authors = self.story_authors[self.english_story_name]
			self.story_creation_date = self.story_creation_dates[self.english_story_name]
			self.story_status = self.story_statuses[self.english_story_name]
			self.story_website_link_name = self.story_website_link_names[self.english_story_name]
			self.story_chapter_number = self.story_chapter_numbers[self.english_story_name]
			self.story_reader_number = self.story_reader_numbers[self.english_story_name]
			self.story_reader_file = self.story_reader_files[self.english_story_name]

			# ---

			print("---")
			print()
			print(Language_Item_Definer("Story name", "Nome da história") + ": ")
			print(Language_Item_Definer(self.english_story_name, self.portuguese_story_name))
			print()

			self.author_show_text = Language_Item_Definer("Author", "Autor")

			if len(self.local_story_authors) != 1:
				self.author_show_text += Language_Item_Definer("s", "es")

			if len(self.local_story_authors) == 0:
				self.local_story_authors = [Language_Item_Definer("None", "Nenhum")]

			if len(self.local_story_authors) != 0:
				
				print(self.author_show_text + ": ")
			
			for author in self.local_story_authors:
				print(author)

			print()

			print(Language_Item_Definer("Creation date", "Data de criação") + ": ")
			print(self.story_creation_date)
			print()
			print("Status" + ": ")
			print(Language_Item_Definer(self.story_status, self.portuguese_story_status_list[self.story_status]))
			print()
			print(Language_Item_Definer("Folder", "Pasta") + ": ")
			print(self.story_folder)
			print()
			print(Language_Item_Definer("Website link", "Link de site") + ": ")
			print(self.story_website_link_name)
			print()
			print(Language_Item_Definer("Chapter number", "Número de capítulos") + ": ")
			print(self.story_chapter_number)
			print()
			print(Language_Item_Definer("Reader number", "Número de leitores") + ": ")
			print(self.story_reader_number)
			print()

			input()
# Story_Manager.py

# Script Helper importer
from Script_Helper import *

from Diary_Slim.Write_On_Diary_Slim_Module import Write_On_Diary_Slim_Module as Write_On_Diary_Slim_Module

from pyperclip import copy
from time import sleep
from datetime import datetime, timedelta
import winshell, win32com.client
import re

# Script name
local_script_name = "Story_Manager.py"

class Story_Manager(object):
	def __init__(self, parameter_switches = None, runned_function_name = None, select_story = True, second_space = True, custom_story_array = False):
		self.verbose = False

		self.testing_script = False

		self.parameter_switches = parameter_switches

		self.runned_function_name = runned_function_name
		self.select_story = select_story
		self.second_space = second_space
		self.custom_story_array = custom_story_array

		self.Define_Basic_Variables()
		self.Define_Main_Variables()
		self.Define_Folders_And_Files()
		self.Define_Texts()
		self.Create_Unexistent_Folders_And_Files()
		self.Define_Select_Story_Variables()

		if self.select_story == True:
			self.Select_Story()
			self.Define_Story_Variables()

	def Define_Basic_Variables(self):
		self.option = True

		# Global Switches dictionary
		self.global_switches = {
		"write_to_file": self.option,
		"create_files": self.option,
		"create_folders": self.option,
		"move_files": self.option,
		"verbose": self.verbose,
		"testing_script": self.testing_script,
		}

		if self.parameter_switches != None:
			self.global_switches = self.parameter_switches
			self.testing_script = self.global_switches["testing_script"]

		if self.global_switches["testing_script"] == True:
			print(Language_Item_Definer("Testing script: Yes", "Testando script: Sim"))

		if self.global_switches["verbose"] == True:
			print(Language_Item_Definer("Verbose on", "Verbose ligado") + ".")

		if self.global_switches["testing_script"] == True:
			self.global_switches["write_to_file"] = False
			self.global_switches["create_files"] = False
			self.global_switches["move_files"] = False

		self.dot_text = ".txt"
		self.dot_md = ".md"
		self.dash_separator = " - "
		self.comma_separator = ", "

	def Define_Main_Variables(self):
		self.action_texts = {
		"Write_Chapter": Language_Item_Definer("write", "escrever"),
		"Post_Chapter": Language_Item_Definer("post", "postar"),
		"Update_Chapter_Covers": Language_Item_Definer("update its chapter covers", "atualizar suas capas de capítulo"),
		}

		self.action_text = Language_Item_Definer("manage", "gerenciar")

		if self.runned_function_name != None:
			self.action_text = self.action_texts[self.runned_function_name]

		self.wattpad_url = "https://www.wattpad.com/"
		self.wattpad_profile_url = self.wattpad_url + "user/stake2"
		self.wattpad_profile_conversations_url = self.wattpad_profile_url + "/conversations"

		self.twitter_url = "https://twitter.com/Stake2_"
		self.facebook_url = "https://www.facebook.com/me/"
		self.google_translate_url = "https://translate.google.com/"
		self.grammarly_url = "https://app.grammarly.com/"

		self.replace_list = ["?", ":", "\\", "/", '"', "*", "<", ">", "|"]

		self.current_diary_slim_file = Read_Lines(diary_slim_folder + "Current File" + self.dot_text)[0]

		self.now = time.strftime("%H:%M %d/%m/%Y")

	def Define_Folders_And_Files(self):
		self.scripts_folder = scripts_folder
		self.modules_folder = self.scripts_folder + "Modules/"
		self.script_text_files_folder = self.scripts_folder + "Script Text Files/"

		name = __name__

		if "." in __name__:
			name = __name__.split(".")[0]

		self.module_text_files_folder = self.script_text_files_folder + name + "/"
		Create_Folder(self.module_text_files_folder, self.global_switches)

		self.chapter_status_template_file = self.module_text_files_folder + "Chapter Status Template" + self.dot_text
		Create_Text_File(self.chapter_status_template_file)

		self.chapter_status_template = Read_String(self.chapter_status_template_file)

		self.obsidian_folder = mega_folder + "Obsidian's Vaults/"
		self.obsidian_creativity_folder = self.obsidian_folder + "Creativity/"
		self.obsidian_creativity_literature_folder = self.obsidian_creativity_folder + "Literature/"
		self.obsidian_stories_folder = self.obsidian_creativity_literature_folder + "Stories/"

		self.stories_folder = mega_stories_folder
		self.stories_database_folder = self.stories_folder + "Story Database/"
		self.story_names_file = self.stories_database_folder + "Names" + self.dot_text
		self.story_creation_dates_file = self.stories_database_folder + "Creation Dates" + self.dot_text
		self.story_authors_file = self.stories_database_folder + "Authors" + self.dot_text
		self.story_links_file = self.stories_database_folder + "Links" + self.dot_text
		self.story_wattpad_ids_file = self.stories_database_folder + "Wattpad IDs" + self.dot_text
		self.story_number_file = self.stories_database_folder + "Number" + self.dot_text
		self.story_status_file = self.stories_database_folder + "Status" + self.dot_text
		self.stories_to_slice_file = self.stories_database_folder + "Stories To Slice" + self.dot_text

		self.story_database_files = {
			"Mixed Story Name": self.story_names_file,
			"Creation Date": self.story_creation_dates_file,
			"Author(s)": self.story_authors_file,
			"Website Link Name": self.story_links_file,
			"Wattpad IDs": self.story_wattpad_ids_file,
			"Number": self.story_number_file,
			"Status": self.story_status_file,
		}

		self.story_database_files["Names"] = self.story_database_files["Mixed Story Name"]

		self.main_story_folders = [
			"Chapters",
			"Comments",
			"Readers and Reads",
			"Story Info",
		]

		self.story_folders = {}
		self.current_status_files = {}

		local_story_names_array_enus = []
		local_story_names_array_enus.extend(story_names_array_enus)
		local_story_names_array_enus.pop(0)

		for story_name in local_story_names_array_enus:
			if story_name != None:
				story_folder = story_name

				story_folder = Split_And_Add_Text(story_folder, new_separator = "/")

				story_folder = self.stories_folder + story_folder + "/"
				Create_Folder(story_folder, self.global_switches)

				Create_Folder(story_folder + "Story Info/", self.global_switches)
				Create_Folder(story_folder + "Story Info/Writing - Escrita/", self.global_switches)

				current_status_file = story_folder + "Story Info/Writing - Escrita/Current Status" + self.dot_text
				Create_Text_File(current_status_file)

				self.story_folders[story_name] = story_folder
				self.current_status_files[story_name] = current_status_file

	def Define_Texts(self):
		self.english_titles_text = "Titles"
		self.portuguese_titles_text = "Títulos"
		self.titles_text = Language_Item_Definer(self.english_titles_text, self.portuguese_titles_text)
		self.mixed_titles_text = self.english_titles_text + self.dash_separator + self.portuguese_titles_text

		self.english_number_text = "Number"
		self.portuguese_number_text = "Número"
		self.mixed_number_text = self.english_number_text + self.dash_separator + self.portuguese_number_text

		self.english_portrait_text = "Portrait"
		self.english_landscape_text = "Landscape"

		self.portuguese_portrait_text = "Retrato"
		self.portuguese_landscape_text = "Paisagem"

		self.portrait_text = Language_Item_Definer(self.english_portrait_text, self.portuguese_portrait_text)
		self.landscape_text = Language_Item_Definer(self.english_landscape_text, self.portuguese_landscape_text)

		self.english_published_text = "Published"
		self.brazilian_portuguese_published_text = "Publiquei"
		self.published_text = Language_Item_Definer(self.english_published_text, self.brazilian_portuguese_published_text)

		self.default_author = "Izaque Sanvezzo (Stake2, Funkysnipa Cat)"

		self.english_story_status_list = {
		"Writing": "Writing",
		"Rewriting": "Rewriting",
		"Reviewing and Rewriting": "Reviewing and Rewriting",
		"Reviewing": "Reviewing",
		"Finished and Published": "Finished and Published",
		"Finished": "Finished",
		"Paused": "Paused",
		}

		self.portuguese_story_status_list = {
		"Writing": "Escrevendo",
		"Rewriting": "Reescrevendo",
		"Reviewing and Rewriting": "Revisando e Reescrevendo",
		"Reviewing": "Revisando",
		"Finished and Published": "Completada e Publicada",
		"Finished": "Completada",
		"Paused": "Pausada",
		}

		self.story_status_list = Language_Item_Definer(self.english_story_status_list, self.portuguese_story_status_list)
		self.english_chapter_text = "Chapter"
		self.portuguese_chapter_text = "Capítulo"
		self.chapter_text = Language_Item_Definer(self.english_chapter_text, self.portuguese_chapter_text)

	def Create_Unexistent_Folders_And_Files(self):
		for file in self.story_database_files.values():
			Create_Text_File(file, self.global_switches)

	def Define_Select_Story_Variables(self):
		self.story_names = [None]
		self.english_story_names = []
		self.portuguese_story_names = []

		i = 1
		for story_name in story_names:
			if story_name != None:
				story_name = Split_And_Add_Text(story_name, new_separator = {0: ": ", 1: " - "})

				english_story_name_backup = story_names_array_enus[i]				

				english_story_name = Split_And_Add_Text(english_story_name_backup, new_separator = {0: ": ", 1: " - "})
				portuguese_story_name = Split_And_Add_Text(story_names_array_ptbr[i], new_separator = {0: ": ", 1: " - "})

				self.english_story_names.append(english_story_name)
				self.portuguese_story_names.append(portuguese_story_name)

				current_status = Create_Array_Of_File(self.current_status_files[english_story_name_backup])

				if current_status != []:
					story_name += " ({})".format(current_status[0].split(", ")[Language_Item_Definer(0, 1)])

				self.story_names.append(story_name)

				i += 1

		self.story_names_backup = self.story_names

		if self.custom_story_array != False:
			self.story_names = self.custom_story_array
			self.english_story_names = []
			self.portuguese_story_names = []

			i = 0
			for story_name in self.story_names:
				if story_name != None:
					english_story_name = Split_And_Add_Text(story_name)
					portuguese_story_name = Split_And_Add_Text(story_name)

					if ", " in story_name:
						story_name = story_name.split(", ")
						english_story_name = english_story_name.split(", ")[0]
						portuguese_story_name = portuguese_story_name.split(", ")[1]

						self.english_story_names.append(english_story_name)
						self.portuguese_story_names.append(portuguese_story_name)

						self.story_names[i] = story_name[Language_Item_Definer(0, 1)]

					if ", " not in story_name:
						self.english_story_names.append(english_story_name)
						self.portuguese_story_names.append(portuguese_story_name)

				i += 1

			self.story_name_numbers_array = []

			i = 0
			for story in self.story_names_backup:
				c = 0
				while c <= len(self.story_names) - 1:
					if story == self.story_names[c]:
						self.story_name_numbers_array.append(i)

					c += 1

				i += 1

		self.story_wattpad_ids_enus = [None]
		self.story_wattpad_ids_ptbr = [None]

		self.wattpad_ids = Create_Array_Of_File(self.story_wattpad_ids_file)

		for self.wattpad_id in self.wattpad_ids:
			if self.wattpad_id != "None":
				self.wattpad_id = self.wattpad_id.split(", ")

				self.story_wattpad_ids_enus.append(self.wattpad_id[0])
				self.story_wattpad_ids_ptbr.append(self.wattpad_id[1])

			if self.wattpad_id == "None":
				self.story_wattpad_ids_enus.append(None)
				self.story_wattpad_ids_ptbr.append(None)

	def Select_Story(self):
		self.choice_text = Language_Item_Definer("Select one story to", "Selecione uma história para") + " " + self.action_text

		self.choice_info = Make_Choices(self.story_names, None, run = False, alternative_choice_list_text = self.choice_text, return_choice = True, export_number = True, second_space = self.second_space)

		self.story_name = self.choice_info[0]
		self.story_name_key = self.story_name.replace(" ", "_").lower()

		if " (" in self.story_name:
			self.story_name = self.story_name.split(" (")[0]

		if self.custom_story_array == False:
			self.story_number = self.choice_info[1]

		if self.custom_story_array != False:
			self.story_number = self.story_name_numbers_array[self.choice_info[1]]

	def Define_Story_Variables(self):
		self.english_story_name = story_names_array_enus[self.story_number]
		self.english_story_name_underlined = self.english_story_name.replace(" ", "_")
		self.portuguese_story_name = story_names_array_ptbr[self.story_number]
		self.english_story_name_key = self.english_story_name.replace(" ", "_").lower()
		self.global_story_name = Language_Item_Definer(self.english_story_name, self.portuguese_story_name)
		self.story_name_underlined = self.story_name.replace(" ", "_")

		self.story_folder = self.story_folders[self.english_story_name]
		self.story_covers_folder = self.story_folder + "Covers/"

		self.language_story_name = Language_Item_Definer(self.english_story_name, self.portuguese_story_name)

		self.website_images_story_covers_folder = mega_stake2_website_media_story_covers_folder + self.english_story_name + "/"

		self.obsidian_story_folder = self.obsidian_stories_folder + self.english_story_name + "/"
		Create_Folder(self.obsidian_story_folder, self.global_switches)

		self.wattpad_id_enus = story_wattpad_ids_enus[self.story_number]
		self.wattpad_id_ptbr = story_wattpad_ids_ptbr[self.story_number]

		if self.wattpad_id_enus != None:
			self.wattpad_link_enus = self.wattpad_url + "myworks/" + self.wattpad_id_enus

		if self.wattpad_id_ptbr != None:
			self.wattpad_link_ptbr = self.wattpad_url + "myworks/" + self.wattpad_id_ptbr

		self.story_website_link = mega_stake2_website_link + self.english_story_name.replace(" ", "%20") + "/"

		if self.english_story_name == "SpaceLiving":
			self.story_website_link = self.story_website_link.replace(self.english_story_name, "New%20World/" + self.english_story_name)

		self.story_info_folder = self.story_folder + "Story Info/"
		Create_Folder(self.story_info_folder, self.global_switches)

		self.story_readers_and_reads_folder = self.story_folder + "Readers and Reads/"
		Create_Folder(self.story_readers_and_reads_folder, self.global_switches)

		self.readers_file = self.story_readers_and_reads_folder + "Readers" + self.dot_text

		if is_a_file(self.readers_file) == False:
			Write_To_File(self.readers_file, "No Readers - Sem Leitores", self.global_switches)		

		self.story_template_file = self.story_info_folder + "Template" + self.dot_text
		self.story_settings_file = self.story_info_folder + "Story Settings" + self.dot_text

		self.story_writing_folder = self.story_info_folder + "Writing - Escrita/"
		Create_Folder(self.story_writing_folder, self.global_switches)

		self.story_chapter_times_folder = self.story_writing_folder + "Chapter Times/"
		Create_Folder(self.story_chapter_times_folder, self.global_switches)

		self.last_chapters_folder = self.story_writing_folder + "Last Chapters/"
		Create_Folder(self.last_chapters_folder, self.global_switches)

		self.story_obsidian_links_folder = self.story_writing_folder + "Obsidian Links/"
		Create_Folder(self.story_obsidian_links_folder, self.global_switches)

		self.chapter_status_file = self.story_writing_folder + "Chapter Status" + self.dot_text

		self.current_status_file = self.story_writing_folder + "Current Status" + self.dot_text
		Create_Text_File(self.current_status_file, self.global_switches)

		if is_a_file(self.chapter_status_file) == False:
			Write_To_File(self.chapter_status_file, self.chapter_status_template, self.global_switches)

		self.chapter_status = Read_Lines(self.chapter_status_file)
		self.chapter_status_array = Create_Array_Of_File(self.chapter_status_file, add_none = True)
		self.chapter_status_string = Read_String(self.chapter_status_file)

		self.chapter_time_files = [
		self.story_chapter_times_folder + "Write" + self.dot_text,
		self.story_chapter_times_folder + "Revise" + self.dot_text,
		self.story_chapter_times_folder + "Translate" + self.dot_text,
		]

		self.chapter_time_files_dict = {
		"Write": self.story_chapter_times_folder + "Write" + self.dot_text,
		"Revise": self.story_chapter_times_folder + "Revise" + self.dot_text,
		"Translate": self.story_chapter_times_folder + "Translate" + self.dot_text,
		}

		for file in self.chapter_time_files:
			Create_Text_File(file, self.global_switches)

		self.last_chapters_names = [
		"Written",
		"Revised",
		"Translated",
		]

		self.last_chapters_files = {}

		for last_chapter_name in self.last_chapters_names:
			file = self.last_chapters_folder + last_chapter_name + self.dot_text

			if is_a_file(file) == False:
				Write_To_File(file, "0", self.global_switches)

			self.last_chapters_files[last_chapter_name] = file

		self.last_written_chapter_file = self.last_chapters_folder + "Written" + self.dot_text

		self.last_revised_chapter_file = self.last_chapters_folder + "Revised" + self.dot_text

		self.last_translated_chapter_file = self.last_chapters_folder + "Translated" + self.dot_text

		if self.select_story == True:
			if Create_Array_Of_File(self.last_written_chapter_file, add_none = True) != None:
				self.last_written_chapter = int(Create_Array_Of_File(self.last_written_chapter_file, add_none = True)[1])

			if Create_Array_Of_File(self.last_revised_chapter_file, add_none = True) != None:
				self.last_revised_chapter = int(Create_Array_Of_File(self.last_revised_chapter_file, add_none = True)[1])

			if Create_Array_Of_File(self.last_translated_chapter_file, add_none = True) != None:
				self.last_translated_chapter = int(Create_Array_Of_File(self.last_translated_chapter_file, add_none = True)[1])

		self.chapter_to_post_line_number = 11
		self.chapter_to_post = self.chapter_status_array[self.chapter_to_post_line_number]
		self.last_posted_chapter_line_number = 14
		self.last_posted_chapter = self.chapter_status_array[self.last_posted_chapter_line_number]

		self.story_chapters_folder = self.story_folder + "Chapters/"
		self.story_chapters_enus_folder = self.story_chapters_folder + full_language_en + "/"
		self.story_chapters_ptbr_folder = self.story_chapters_folder + full_language_pt + "/"

		self.obsidian_story_chapters_folder = self.obsidian_story_folder + "Chapters/"
		self.obsidian_story_chapters_enus_folder = self.obsidian_story_chapters_folder + full_language_en + "/"
		self.obsidian_story_chapters_ptbr_folder = self.obsidian_story_chapters_folder + full_language_pt + "/"

		Create_Folder(self.obsidian_story_chapters_folder, self.global_switches)
		Create_Folder(self.obsidian_story_chapters_enus_folder, self.global_switches)
		Create_Folder(self.obsidian_story_chapters_ptbr_folder, self.global_switches)

		self.story_vegas_files_folder = story_covers_vegas_files_folder + self.english_story_name + "/"

		self.story_chapter_titles_folder = Language_Item_Definer(self.story_chapters_enus_folder, self.story_chapters_ptbr_folder)

		self.story_chapter_titles_file = self.story_chapter_titles_folder + self.titles_text + "/" + self.titles_text + self.dot_text
		self.story_chapter_titles_enus_file = self.story_chapters_enus_folder + self.english_titles_text + "/" + self.english_titles_text + self.dot_text
		self.story_chapter_titles_ptbr_file = self.story_chapters_ptbr_folder + self.portuguese_titles_text + "/" + self.portuguese_titles_text + self.dot_text

		self.story_chapter_number_file = self.story_chapters_folder + self.mixed_number_text + self.dot_text

		if is_a_file(self.story_chapter_number_file) == False:
			Create_Text_File(self.story_chapter_number_file, self.global_switches)
			Write_To_File(self.story_chapter_number_file, "1", self.global_switches)

		if is_a_file(self.story_chapter_number_file) == True:
			self.story_chapter_number = Read_Lines(self.story_chapter_number_file)[0]

		if self.select_story == True:
			self.story_chapter_titles = Create_Array_Of_File(self.story_chapter_titles_file, add_none = True)

			self.english_chapter_titles = Create_Array_Of_File(self.story_chapter_titles_enus_file, add_none = True)
			self.portuguese_chapter_titles = Create_Array_Of_File(self.story_chapter_titles_ptbr_file, add_none = True)

			self.english_chapter_titles_not_none = Create_Array_Of_File(self.story_chapter_titles_enus_file, add_none = False)
			self.portuguese_chapter_titles_not_none = Create_Array_Of_File(self.story_chapter_titles_ptbr_file, add_none = False)

			self.story_chapter_titles_multilanguage = self.english_chapter_titles, self.portuguese_chapter_titles

		self.story_website_story_covers_folder = mega_stake2_website_media_story_covers_folder + self.english_story_name + "/"

		self.story_disk_root_story_covers_folder = disk_root_story_covers_folder + self.english_story_name + "/"

		self.write_line_number = 2
		self.revise_line_number = 5
		self.translate_line_number = 8
		self.post_line_number = 11

		self.chapter_status_write = self.chapter_status_array[self.write_line_number]
		self.chapter_status_revise = self.chapter_status_array[self.revise_line_number]
		self.chapter_status_translate = self.chapter_status_array[self.translate_line_number]
		self.chapter_status_post = self.chapter_status_array[self.post_line_number]

		self.chapter_statuses = [
		None,
		self.chapter_status_write,
		self.chapter_status_revise,
		self.chapter_status_translate,
		]

		self.writing_modes_enus = [
		None,
		"Write",
		"Revise",
		"Translate",
		]

		self.write_enus = self.writing_modes_enus[1]
		self.revise_enus = self.writing_modes_enus[2]
		self.translate_enus = self.writing_modes_enus[3]

		self.writing_modes_ptbr = [
		None,
		"Escrever",
		"Revisar",
		"Traduzir",
		]

		self.writing_modes_present_enus = [
		None,
		"Writing",
		"Revising",
		"Translating",
		]

		self.writing_modes_present_ptbr = [
		None,
		"Escrito",
		"Revisado",
		"Traduzido",
		]

		self.writing_modes_infinitive_enus = [
		None,
		"Written",
		"Revised",
		"Translated",
		]

		self.writing_modes_infinitive_ptbr = [
		None,
		"Escrito",
		"Revisado",
		"Traduzido",
		]

		self.writing_modes_action_ptbr = [
		None,
		"Escrever",
		"Revisar",
		"Traduzir",
		]

		self.writing_modes_past_action_enus = [
		None,
		"Wrote",
		"Revised",
		"Translated",
		]

		self.writing_modes_past_action_ptbr = [
		None,
		"Escrevi",
		"Revisei",
		"Traduzi",
		]

		self.writing_modes_past_present_action_ptbr = [
		None,
		"Escrita",
		"Revisão",
		"Tradução",
		]

		self.post_text = Language_Item_Definer("Post", "Postar")

		self.no_chapter_text = Language_Item_Definer("No Chapter", "Sem Capítulo")

		self.writing_modes = Language_Item_Definer(self.writing_modes_enus, self.writing_modes_ptbr)

		self.new_writing_modes = [None, "", "", ""]

		self.chapter_actions_ptbr = [
		None,
		"Comecei",
		"Continuei",
		]

		self.chapter_actions_enus = [
		None,
		"Started",
		"Continued",
		]

		self.setting_texts = [
		Language_Item_Definer("Reverse translate", "Tradução reversa"),
		Language_Item_Definer("Register task", "Registrar tarefa"),
		]

		self.default_settings = [
		False,
		True,
		]

		i = 0
		self.reverse_translate_setting_text = self.setting_texts[i]
		i += 1

		self.register_task_setting_text = self.setting_texts[i]

		if is_a_file(self.story_settings_file) == True:
			self.story_settings = Make_Setting_Dictionary(Create_Array_Of_File(self.story_settings_file), setting_splitter = ": ", define_yes_or_no = True)

			self.new_story_settings = {}

			setting_number = 0
			for setting in self.setting_texts:
				supposed_setting = [
				setting,
				setting.lower(),
				setting.title(),
				setting.capitalize(),
				setting.lower().title(),
				setting.title(),
				setting.capitalize(),
				]

				found_setting = False

				i = 0
				while i <= len(supposed_setting) - 1:
					new_setting = supposed_setting[i]

					if new_setting in self.story_settings:
						self.new_story_settings[setting] = self.story_settings[new_setting]

						found_setting = True

					if found_setting == False:
						self.new_story_settings[setting] = self.default_settings[setting_number]

					i += 1

				setting_number += 1

			self.story_settings = self.new_story_settings

			self.reverse_translate = self.story_settings[self.reverse_translate_setting_text]
			self.register_task = self.story_settings[self.register_task_setting_text]

		else:
			self.reverse_translate = False
			self.register_task = True

	def Register_Finished_Task(self, register_task = True, register_on_diary_slim = True, custom_write_text = None, custom_time = None):
		self.register_task = register_task
		self.register_on_diary_slim = register_on_diary_slim
		self.custom_write_text = custom_write_text
		self.custom_time = custom_time

		self.press_any_key_text = Language_Item_Definer("Press any key to copy the Task Name in {}", "Pressione qualquer tecla para copiar o Nome da Tarefa em {}")

		self.task_name = Language_Item_Definer(self.task_name_enus, self.task_name_ptbr)

		if self.register_task == True:
			from Tasks.Register_Task_Module import Register_Task_Module as Register_Task_Module

			if self.runned_function_name == "Write_Chapter":
				self.english_task_description = self.english_task_description.splitlines()
				self.english_task_description.pop(0)
				self.english_task_description = Stringfy_Array(self.english_task_description, add_line_break = True)

				self.portuguese_task_description = self.portuguese_task_description.splitlines()
				self.portuguese_task_description.pop(0)
				self.portuguese_task_description = Stringfy_Array(self.portuguese_task_description, add_line_break = True)

			if self.global_switches["testing_script"] == False:
				Register_Task_Module(self.experienced_media_type, self.english_task_description, self.portuguese_task_description, self.experienced_media_time, show_text = False)

			self.print_text = Language_Item_Definer("This Task was registered", "Esta Tarefa foi registrada")

		print("---")

		if self.register_task == False:
			print()

		if self.register_on_diary_slim == True:
			self.now = time.strftime("%H:%M %d/%m/%Y")

			if self.custom_write_text != None:
				if self.register_task == False:
					self.portuguese_task_description = self.portuguese_task_description.splitlines()
					self.portuguese_task_description.pop(0)
					self.portuguese_task_description = Stringfy_Array(self.portuguese_task_description, add_line_break = True)

				Write_On_Diary_Slim_Module(self.portuguese_task_description[:-1], self.custom_time, self.global_switches)

			if self.register_task == True:
				print()
				Write_On_Diary_Slim_Module(self.task_name_ptbr, self.now, self.global_switches)
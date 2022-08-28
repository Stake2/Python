# Write_Chapter.py

# Script Helper importer
from Script_Helper import *

from Story_Manager.Story_Manager import *

from os.path import expanduser

class Write_Chapter(Story_Manager):
	def __init__(self):
		super().__init__(runned_function_name = "Write_Chapter")

		self.Select_Writing_Mode()

		if self.global_switches["testing_script"] == False:
			sleep(1)
			Open_Link(self.grammarly_url)
			sleep(1)
			Open_Link(self.google_translate_url)
			sleep(3)

		self.Open_Obsidian()

		self.Finish_Writing()
		self.Close_Obsidian()

	def Select_Writing_Mode(self):
		self.choice_text = Language_Item_Definer("Select one writing mode to use", "Selecione um modo de escrita para usar")

		i = 1
		self.local_chapter_status = self.chapter_status_write

		if self.local_chapter_status == "None":
			self.local_chapter_status = Language_Item_Definer("Choose one chapter", "Escolha um capítulo")

		self.new_writing_modes[i] = self.writing_modes[i] + " (" + self.local_chapter_status + ")"
		i += 1

		self.local_chapter_status = self.chapter_status_revise

		if self.local_chapter_status == "None":
			self.local_chapter_status = Language_Item_Definer("Choose one chapter", "Escolha um capítulo")

		self.new_writing_modes[i] = self.writing_modes[i] + " (" + self.local_chapter_status + ")"
		i += 1

		self.local_chapter_status = self.chapter_status_translate

		if self.local_chapter_status == "None":
			self.local_chapter_status = Language_Item_Definer("Choose one chapter", "Escolha um capítulo")

		self.new_writing_modes[i] = self.writing_modes[i] + " (" + self.local_chapter_status + ")"
		i += 1

		self.writing_modes_present = Language_Item_Definer(self.writing_modes_present_enus, self.writing_modes_present_ptbr)
		self.writing_modes_infinitive = Language_Item_Definer(self.writing_modes_infinitive_enus, self.writing_modes_infinitive_ptbr)
		self.writing_modes_action = Language_Item_Definer(self.writing_modes_present_enus, self.writing_modes_action_ptbr)
		self.writing_modes_past_action = Language_Item_Definer(self.writing_modes_past_action_enus, self.writing_modes_past_action_ptbr)

		self.choice_info = Make_Choices(self.new_writing_modes, None, run = False, alternative_choice_list_text = self.choice_text, return_choice = True, export_number = True)

		self.writing_mode_number = self.choice_info[1]
		self.writing_mode = self.writing_modes[self.writing_mode_number]
		self.english_writing_mode = self.writing_modes_enus[self.writing_mode_number]
		self.present_writing_mode = self.writing_modes_present[self.writing_mode_number]
		self.english_present_writing_mode = self.writing_modes_present_enus[self.writing_mode_number]
		self.infinitive_writing_mode = self.writing_modes_infinitive[self.writing_mode_number]
		self.english_infinitive_writing_mode = self.writing_modes_infinitive_enus[self.writing_mode_number]
		self.action_writing_mode = self.writing_modes_action[self.writing_mode_number]
		self.english_action_writing_mode = self.writing_modes_past_action_enus[self.writing_mode_number]
		self.past_action_writing_mode = self.writing_modes_past_action_ptbr[self.writing_mode_number]
		self.past_action_writing_mode_enus = self.writing_modes_past_action_enus[self.writing_mode_number]
		self.past_action_writing_mode_ptbr = self.writing_modes_past_action_ptbr[self.writing_mode_number]
		self.past_present_writing_mode = self.writing_modes_past_present_action_ptbr[self.writing_mode_number]

		self.write = self.writing_modes[1]
		self.revise = self.writing_modes[2]
		self.translate = self.writing_modes[3]

		self.writing = self.writing_modes_present[1]
		self.revising = self.writing_modes_present[2]
		self.translating = self.writing_modes_present[3]

		if self.writing_mode != self.translate:
			self.next_writing_mode = self.writing_modes_action[self.writing_mode_number + 1]

		self.writing_mode_enus = self.writing_modes_enus[self.writing_mode_number]
		self.writing_mode_ptbr = self.writing_modes_ptbr[self.writing_mode_number]

		self.Get_Status(self.writing_mode, self.infinitive_writing_mode, self.writing_mode_number)

	def Chapter_Chooser(self, choice_text, chapter_to_write = None, first_space = True, different_chapter_titles_array = None):
		self.choice_text = choice_text
		self.chapter_to_write = chapter_to_write
		self.first_space = first_space
		self.different_chapter_titles_array = different_chapter_titles_array

		if self.different_chapter_titles_array == None:
			self.array_to_use = self.story_chapter_titles

		if different_chapter_titles_array != None:
			self.array_to_use = self.different_chapter_titles_array

		self.array = [None]
		i = 1
		for self.chapter_title in self.array_to_use:
			if self.chapter_title != None:
				self.chapter_title = str(i) + self.dash_separator + self.chapter_title

				self.array.append(self.chapter_title)

				i += 1

		self.array_to_use = self.array

		if self.chapter_to_write == None:
			self.chapter_to_write = self.last_revised_chapter

		self.new_array = [None]

		i = 1
		while i <= self.chapter_to_write:
			self.array_to_use.pop(1)

			i += 1

		self.array_to_use.pop(0)

		self.append_no_chapter = False

		if self.append_no_chapter == True:
			# Append "No Chapter" text to the array of chapter titles
			i = 1
			while i <= self.chapter_to_write:
				self.new_array.append(self.no_chapter_text)
			
				i += 1

		self.new_array.extend(self.array_to_use)

		self.array_to_use = self.new_array

		if self.first_space == True:
			print()

		self.choice_info = Make_Choices(self.array_to_use, None, run = False, alternative_choice_list_text = self.choice_text, return_choice = True, export_number = True)
		self.chapter_title = self.choice_info[0]
		self.chapter_number = self.chapter_title.split(" - ")[0]

		return None, self.chapter_title, self.chapter_number

	def Get_Status(self, writing_mode, infinitive_writing_mode, writing_mode_number):
		self.is_new_chapter = False

		self.writing_mode = writing_mode
		self.infinitive_writing_mode = infinitive_writing_mode
		self.writing_mode_number = writing_mode_number

		self.writing_mode_line_numbers = [
		None,
		2,
		5,
		8,
		]

		self.writing_mode_line_number = self.writing_mode_line_numbers[self.writing_mode_number]

		self.writing_mode_status = self.chapter_status_array[self.writing_mode_line_number]

		self.none_string_list = Language_Item_Definer("The current chapter being {} is none, listing chapters to " + self.writing_mode + ".", "O capítulo sendo {} atualmente é nenhum, listando os capítulos para {}.")

		self.none_string_open = Language_Item_Definer('The current chapter being {} is ' + self.writing_mode_status + ", opening Obsidian to " + self.writing_mode + " it.", 'O capítulo atualmente sendo {} é "{}", abrindo o Obsidian para {} ele.')

		if self.writing_mode == self.write:
			self.list_chapters = False

		if self.writing_mode != self.write:
			self.list_chapters = True

		if self.writing_mode == self.write or self.writing_mode == self.revise:
			self.chapter_language = full_language_en

		if self.writing_mode == self.translate and self.reverse_translate == False:
			self.chapter_language = full_language_pt

		if self.writing_mode == self.translate and self.reverse_translate == True:
			self.chapter_language = full_language_en

		if self.writing_mode == self.revise:
			self.chapter_to_write = self.last_revised_chapter

		if self.writing_mode == self.translate:
			self.chapter_to_write = self.last_translated_chapter

		if self.writing_mode_status == "None" and self.list_chapters == True:
			self.local_writing_mode = self.writing_mode.lower()
			self.local_infinitive_writing_mode = self.infinitive_writing_mode.lower()

			if self.writing_mode == self.translate and self.reverse_translate == True:
				self.local_writing_mode = Language_Item_Definer("reverse " + self.infinitive_writing_mode, self.local_writing_mode + " inversamente")
				self.local_infinitive_writing_mode = Language_Item_Definer("reverse " + self.local_infinitive_writing_mode, self.local_infinitive_writing_mode + " inversamente")

			self.status_text = self.none_string_list.format(self.local_infinitive_writing_mode, self.local_writing_mode)

			print(self.status_text)

			self.local_writing_mode = self.writing_mode.lower()

			if self.writing_mode == self.translate and self.reverse_translate == True:
				self.local_writing_mode = Language_Item_Definer("reverse " + self.local_writing_mode, self.local_writing_mode + " inversamente")

			self.choice_text = Language_Item_Definer("Select one chapter to " + self.local_writing_mode, "Selecione um capítulo para " + self.local_writing_mode)

			if self.writing_mode == self.revise:
				self.array_to_use = self.english_chapter_titles

			if self.writing_mode == self.translate:
				self.array_to_use = self.portuguese_chapter_titles

				if self.reverse_translate == True:
					self.array_to_use = self.english_chapter_titles

			self.choice_info = self.Chapter_Chooser(self.choice_text, self.chapter_to_write, different_chapter_titles_array = self.array_to_use)
			self.chapter_title = self.choice_info[1]
			self.chapter_number = self.choice_info[2]

			self.is_new_chapter = True

		if self.writing_mode_status == "None" and self.list_chapters == False:
			print(Language_Item_Definer("You have no chapter to " + self.writing_mode.lower(), "Você não tem capítulo para " + self.writing_mode.lower()) + ".")

			self.new_chapter_number = self.last_written_chapter + 1

			text = Language_Item_Definer("Creating a new chapter to {}, number {}", "Criando um novo capítulo para {}, número {}")

			print(text.format(self.writing_mode.lower(), str(self.new_chapter_number)) + ".")

			self.chapter_number = self.new_chapter_number

			self.chapter_title = str(self.new_chapter_number) + self.dash_separator + str(Add_Leading_Zeros(self.new_chapter_number))

			self.is_new_chapter = True

		if self.writing_mode_status != "None" and self.list_chapters == True:
			self.status_text = self.none_string_open.format(self.infinitive_writing_mode.lower(), self.writing_mode_status, self.writing_mode.lower())

			print(self.status_text)

			self.chapter_title = self.writing_mode_status
			self.chapter_number = self.writing_mode_status.split(" - ")[0]

			self.is_new_chapter = False

		if self.writing_mode_status != "None" and self.list_chapters == False:
			self.status_text = self.none_string_open.format(self.infinitive_writing_mode.lower(), self.writing_mode_status, self.writing_mode.lower())

			print(self.status_text)

			self.chapter_title = self.writing_mode_status
			self.chapter_number = self.writing_mode_status.split(" - ")[0]

			self.is_new_chapter = False

		if self.writing_mode == self.revise:
			self.chapter_title = self.chapter_number + self.dash_separator + self.english_chapter_titles[int(self.chapter_number)]

		if self.writing_mode == self.translate:
			self.chapter_title = self.chapter_number + self.dash_separator + self.portuguese_chapter_titles[int(self.chapter_number)]

			if self.reverse_translate == True:
				self.chapter_title = self.chapter_number + self.dash_separator + self.english_chapter_titles[int(self.chapter_number)]

		if self.writing_mode_status == "None":
			self.continued_writing = False

		if self.writing_mode_status != "None":
			self.continued_writing = True

		has_two_chapter_files = False

		if self.is_new_chapter == True:
			self.old_chapter = "None"
			self.Set_Status(self.writing_mode, self.present_writing_mode, self.chapter_title, self.old_chapter, self.is_new_chapter)

		if self.writing_mode == self.write or self.writing_mode == self.revise:
			folder_to_use = self.story_chapters_enus_folder

			self.chapter_number = str(Add_Leading_Zeros(self.chapter_number))

			chapter_title = self.chapter_number + self.dash_separator + str(Add_Leading_Zeros(self.chapter_number))
			chapter_title = chapter_title.replace("?", "")

			self.obsidian_chapter_file = self.obsidian_story_chapters_enus_folder + chapter_title + self.dot_md

		if self.writing_mode == self.translate and self.reverse_translate == False:
			chapter_number = str(Add_Leading_Zeros(self.chapter_number))

			chapter_title = chapter_number + self.dash_separator + self.portuguese_chapter_titles[int(self.chapter_number)]
			chapter_title = chapter_title.replace("?", "")

			self.first_file = self.story_chapters_ptbr_folder + chapter_title + self.dot_text

			self.obsidian_chapter_file = self.obsidian_story_chapters_ptbr_folder + chapter_title + self.dot_md

			chapter_title = chapter_number + self.dash_separator + self.english_chapter_titles[int(self.chapter_number)]
			self.second_file = self.story_chapters_enus_folder + chapter_title + self.dot_text

			has_two_chapter_files = True

		if self.writing_mode == self.translate and self.reverse_translate == True:
			chapter_number = str(Add_Leading_Zeros(self.chapter_number))

			chapter_title = chapter_number + self.dash_separator + self.english_chapter_titles[int(self.chapter_number)]
			chapter_title = chapter_title.replace("?", "")

			self.first_file = self.story_chapters_enus_folder + chapter_title + self.dot_text

			self.obsidian_chapter_file = self.obsidian_story_chapters_enus_folder + chapter_title + self.dot_md

			chapter_title = chapter_number + self.dash_separator + self.portuguese_chapter_titles[int(self.chapter_number)]
			self.second_file = self.story_chapters_ptbr_folder + chapter_title + self.dot_text

			has_two_chapter_files = True

		if has_two_chapter_files == False:
			Create_Text_File(self.obsidian_chapter_file, self.global_switches)

		if has_two_chapter_files == True:
			Create_Text_File(self.first_file, self.global_switches)
			Create_Text_File(self.second_file, self.global_switches)

			Create_Text_File(self.obsidian_chapter_file, self.global_switches)

			text_to_write = Read_String(self.second_file)

			if len(Read_Lines(self.first_file)) == 0:
				Write_To_File(self.first_file, text_to_write, self.global_switches)

			if len(Read_Lines(self.obsidian_chapter_file)) == 0:
				Write_To_File(self.obsidian_chapter_file, text_to_write, self.global_switches)

			if self.global_switches["testing_script"] == False:
				Open_Text_File(self.first_file)
				sleep(1)
				Open_Text_File(self.second_file)

		self.current_written_time_file = self.chapter_time_files_dict[self.writing_mode_enus]

		if self.global_switches["testing_script"] == False:
			sleep(2)
			Open_Text_File(self.chapter_status_file)

	def Set_Status(self, writing_mode, present_writing_mode, new_chapter, old_chapter = "None", is_new_chapter = True, finished_writing = False):
		self.set_status = True

		self.writing_mode = writing_mode
		self.present_writing_mode = present_writing_mode
		self.new_chapter = new_chapter
		self.old_chapter = old_chapter
		self.is_new_chapter = is_new_chapter
		self.finished_writing = finished_writing

		if self.is_new_chapter == True:
			self.text_to_replace = "Chapter To " + self.writing_mode_enus + ":\n" + "None"

			self.text_to_add = "Chapter To " + self.writing_mode_enus + ":\n" + self.new_chapter

		if self.is_new_chapter == False:
			self.text_to_replace = "Chapter To " + self.writing_mode_enus + ":\n" + self.old_chapter

			self.text_to_add = "Chapter To " + self.writing_mode_enus + ":\n" + self.new_chapter

		self.text_to_write = self.chapter_status_string.replace(self.text_to_replace, self.text_to_add)

		if self.set_status == True:
			Write_To_File(self.chapter_status_file, self.text_to_write, self.global_switches)

		if self.finished_writing == True:
			self.new_chapter = self.old_chapter.split(" - ")[0]
			self.text_to_write = self.new_chapter

		if self.writing_mode == self.write:
			self.file_to_write = self.last_written_chapter_file

		if self.writing_mode == self.revise:
			self.file_to_write = self.last_revised_chapter_file
	
		if self.writing_mode == self.translate:
			self.file_to_write = self.last_translated_chapter_file

		if self.finished_writing == True and self.set_status == True:
			Write_To_File(self.file_to_write, self.text_to_write, self.global_switches)

		# Writes to Current Status text file
		if self.finished_writing == False:
			self.text_to_write = self.writing_mode_enus + ": " + self.english_chapter_text + " " + str(self.chapter_number) + ", " + self.writing_mode_ptbr + ": " + self.portuguese_chapter_text + " " + str(self.chapter_number)

		if self.finished_writing == True:
			self.text_to_write = ""

		Write_To_File(self.current_status_file, self.text_to_write, self.global_switches)

	def Open_Obsidian(self):
		self.open_obsidian = True

		if self.global_switches["testing_script"] == True:
			self.open_obsidian = False

		self.local_replace_list = [
		"á",
		"ã",
		"â",
		"ç",
		"í",
		"ó",
		"ú",
		"❤️",
		"🎄",
		"🎁",
		]

		self.text_list = [
		"%C3%A1",
		"%C3%A3",
		"%C3%A2",
		"%C3%A7",
		"%C3%AD",
		"%C3%B3",
		"%C3%BA",
		"%E2%9D%A4%EF%B8%8F",
		"%F0%9F%8E%84",
		"%F0%9F%8E%81",
		]

		self.new_chapter_language = self.chapter_language.replace(" ", "%20").replace("ê", "%C3%AA")

		self.edited_chapter_title = self.chapter_title.split(" - ")[1]
		self.edited_chapter_number = str(Add_Leading_Zeros(self.chapter_title.split(" - ")[0]))

		self.edited_chapter_title = str(self.edited_chapter_number) + self.dash_separator + self.edited_chapter_title

		if self.global_switches["verbose"] == True:
			print(self.edited_chapter_title)

		i = 0
		for text in self.local_replace_list:
			self.edited_chapter_title = self.edited_chapter_title.replace(text, self.text_list[i])

			i += 1

		self.edited_chapter_title = self.edited_chapter_title.replace(" ", "%20")

		i = 0
		for text in self.replace_list:
			self.edited_chapter_title = self.edited_chapter_title.replace(text, "")

			i += 1

		self.edited_chapter_title = self.edited_chapter_title.replace("?", "")

		self.edited_chapter_title = self.edited_chapter_title.replace(" ", "%20")

		self.obsidian_link = "obsidian://open?vault=Creativity&file=Literature%2FStories%2F{}%2FChapters%2F{}%2F{}"

		self.obsidian_link = self.obsidian_link.format(self.english_story_name.replace(" ", "%20"), self.new_chapter_language, self.edited_chapter_title)

		self.obsidian_link_show = self.obsidian_link.replace("%2F", "_")
		self.obsidian_link_show = self.obsidian_link_show.replace("%20", " ")

		print()
		print(Language_Item_Definer("Obsidian link", "Link do Obsidian") + ": ")
		print()

		if self.global_switches["verbose"] == True:
			print(self.obsidian_link)

		print()

		self.Opener = Open_Link

		self.fall_back = True

		if self.fall_back == True:
			self.file_name = self.writing_mode_enus + " Link.lnk"
			self.path = self.story_obsidian_links_folder + self.file_name
			self.target = self.obsidian_link
			self.icon = expanduser("~") + r"\AppData\Local\Obsidian\Obsidian.exe"

			if self.global_switches["verbose"] == True:
				print(self.path)

			self.shell = win32com.client.Dispatch("WScript.Shell")
			self.shortcut = self.shell.CreateShortCut(self.path)
			self.shortcut.Targetpath = self.target
			self.shortcut.IconLocation = self.icon
			self.shortcut.save()

			self.obsidian_link = self.story_obsidian_links_folder + self.writing_mode_enus + " Link.bat"
			Create_Text_File(self.obsidian_link, self.global_switches)

			self.text_to_write = "@Echo off\nchcp 65001\n" + '"' + self.path + '"'
			Write_To_File(self.obsidian_link, self.text_to_write, self.global_switches)

			self.Opener = Open_File

		if self.open_obsidian == True:
			self.Opener(self.obsidian_link)

	def Close_Obsidian(self):
		Close_Program("Obsidian.exe")

	def Format_Written_Time(self):
		self.calculate_total_time = False

		self.choice_text = Language_Item_Definer("Paste the {} time".format(self.past_present_writing_mode.lower()), "Cole o tempo de {}".format(self.past_present_writing_mode.lower()))

		self.text_to_replace_in = Select_Choice(self.choice_text, first_space = False)

		self.texts_to_replace = ["\n", "\r", "HRS", "MIN", "SEC", "MS"]

		for text in self.texts_to_replace:
			self.text_to_replace_in = self.text_to_replace_in.replace(text, "")

		self.time_with_text = self.text_to_replace_in.split(" ")

		if self.global_switches["verbose"] == True:
			print(self.time_with_text)

		i = 0
		self.hours_in_text = self.time_with_text[i]
		i += 1

		self.minutes = self.time_with_text[i]
		i += 1

		self.seconds = self.time_with_text[i]
		i += 1

		if self.hours_in_text == "00":
			self.has_hours = False

			self.hours = ""
			self.hours_text = ""
			self.hours_separator = ""

		if self.hours_in_text != "00":
			self.has_hours = True

			self.hours = self.hours_in_text
			self.hours_separator = ":"

			self.hours_text = "hora, " if int(self.hours) <= 1 else "horas, "

		self.minutes_text = "minuto" if int(self.minutes) <= 1 else "minutos"

		self.seconds_text = "segundo" if int(self.seconds) <= 1 else "segundos"

		if self.continued_writing == True and self.calculate_total_time == True:
			self.has_total_time = True

			self.now = time.strftime("%H:%M %d/%m/%Y")
			self.now_datetime = datetime.now()

			self.previous_written_time = datetime.strptime(Read_Lines(self.current_written_time_file)[0], '%Y-%m-%d %H:%M:%S.%f')

			self.hour_written_time = self.previous_written_time.hour

			if self.has_hours == True:
				self.total_written_time = self.previous_written_time + timedelta(hours = int(self.hours), minutes = int(self.minutes), seconds = int(self.seconds))	

			if self.has_hours == False:
				self.total_written_time = self.previous_written_time + timedelta(minutes = int(self.minutes), seconds = int(self.seconds))

			self.time_difference = self.now_datetime - self.previous_written_time

			self.time_difference = str(self.time_difference)[:-7].split(":")

			if self.time_difference[0] == "0":
				self.has_total_hours = False

			if self.time_difference[0] != "0":
				self.has_total_hours = True

			self.total_hours = self.time_difference[0]
			self.total_minutes = self.time_difference[1]
			self.total_seconds = self.time_difference[2]

			if int(self.total_hours) <= 9:
				oself.ther_total_hours = "0" + str(self.total_hours)

			if int(self.total_minutes) <= 9:
				self.other_total_minutes = "0" + str(self.total_minutes)

			if int(self.total_seconds) <= 9:
				self.other_total_seconds = "0" + str(self.total_seconds)

			if int(self.total_hours) > 9:
				self.other_total_hours = self.total_hours

			if int(self.total_minutes) > 9:
				self.other_total_minutes = self.total_minutes

			if int(self.total_seconds) > 9:
				self.other_total_seconds = self.total_seconds

			if self.has_total_hours == True:
				self.backup_time_difference = self.other_total_hours + ":" + self.other_total_minutes + ":" + self.other_total_seconds

			if self.has_total_hours == False:
				self.backup_time_difference = self.other_total_minutes + ":" + self.other_total_seconds

			if "0" in str(self.total_hours[0]):
				self.total_hours = self.total_hours.replace("0", "")

			if "0" in str(self.total_minutes[0]):
				self.total_minutes = self.total_minutes.replace("0", "")

			if "0" in str(self.total_seconds[0]):
				self.total_seconds = self.total_seconds.replace("0", "")

			self.total_written_time_datetime = datetime.strptime(str(self.total_written_time),  '%Y-%m-%d %H:%M:%S.%f')

			self.total_written_time = self.time_difference

			if self.has_total_hours == True:
				self.total_hours_text = "s" if int(self.total_hours) > 1 else ""

			else:
				self.total_hours_text = ""

			self.total_minutes_text = "s" if int(self.total_minutes) > 1 else ""
			self.total_seconds_text = "s" if int(self.total_seconds) > 1 else ""

			if self.has_total_hours == True:
				self.total_written_time_text = self.total_hours + " hora" + self.total_hours_text + ", " + self.total_minutes + " minuto" + self.total_minutes_text + ", e " + self.total_seconds + " segundo" + self.total_seconds_text

			if self.has_total_hours == False:
				self.total_written_time_text = self.total_minutes + " minuto" + self.total_minutes_text + " e " + self.total_seconds + " segundo" + self.total_seconds_text

			self.string_to_format = "Totalizando {} ({})."
			self.total_written_time_text = self.string_to_format.format(self.total_written_time_text, self.backup_time_difference)

			if self.finished_writing_chapter == False:
				self.text_to_write = str(self.total_written_time_datetime)

			if self.finished_writing_chapter == True:
				self.text_to_write = ""

			Write_To_File(self.current_written_time_file, self.text_to_write, self.global_switches)

		if self.continued_writing == False and self.calculate_total_time == True:
			self.has_total_time = False

			self.current_written_time_file = self.chapter_time_files_dict[self.writing_mode_enus]

			self.text_to_write = str(datetime.now())

			Write_To_File(self.current_written_time_file, self.text_to_write, self.global_switches)

			self.total_written_time_text = None

		if self.calculate_total_time == False:
			self.total_written_time_text = None

			self.has_total_time = False

		self.hours_in_text = str(int(self.hours_in_text)) if "0" in str(self.hours_in_text) else self.hours_in_text

		self.minutes = str(int(self.minutes)) if "0" in str(self.minutes) else self.minutes

		self.seconds = str(int(self.seconds)) if "0" in str(self.seconds) else self.seconds

		if self.has_hours == True:
			self.hours_space = " "
			self.minutes_comma = ","

		if self.has_hours == False:
			self.hours_space = ""
			self.minutes_comma = ""

		self.hours_text = self.hours + self.hours_space + self.hours_text

		if self.minutes != "00":
			self.minutes_text = self.minutes + " " + self.minutes_text

		else:
			self.minutes_text = ""

		self.seconds_text = self.seconds + " " + self.seconds_text

		self.written_time_text = self.hours_text + self.minutes_text + self.minutes_comma + " e " + self.seconds_text

		self.hours_in_text = "0" + self.hours_in_text if int(self.hours_in_text) <= 9 else self.hours_in_text

		self.minutes = "0" + self.minutes if int(self.minutes) <= 9 else self.minutes

		self.seconds = "0" + self.seconds if int(self.seconds) <= 9 else self.seconds

		self.written_time = self.hours + self.hours_separator + self.minutes + ":" + self.seconds

		return [self.written_time_text, self.written_time], self.total_written_time_text

	def Define_Diary_Slim_Texts(self):
		if self.continued_writing == False:
			self.local_chapter_status = self.chapter_actions_ptbr[1]
			self.english_local_chapter_status = self.chapter_actions_enus[1]

		if self.continued_writing == True:
			self.local_chapter_status = self.chapter_actions_ptbr[2]
			self.english_local_chapter_status = self.chapter_actions_enus[2]

		self.chapter_past_action = self.past_action_writing_mode
		self.english_chapter_past_action = self.past_action_writing_mode_enus

		self.chapter_done_header = ""
		self.english_chapter_done_header = ""

		self.diary_slim_note_header = self.past_written_time + ":\n"

		self.chapter_done_header += self.diary_slim_note_header
		self.english_chapter_done_header += self.diary_slim_note_header

		self.text_to_add = " em Inglês" if self.writing_mode == self.write or self.writing_mode == self.revise else ""
		self.english_text_to_add = " in English" if self.writing_mode == self.write or self.writing_mode == self.revise else ""

		self.local_action_writing_mode = self.action_writing_mode.lower()
		self.local_english_action_writing_mode = self.english_action_writing_mode.lower()
		self.local_english_infinitive_writing_mode = self.english_infinitive_writing_mode.lower()
		self.local_english_present_writing_mode = self.english_present_writing_mode.lower()

		if self.writing_mode == self.translate and self.reverse_translate == True:
			self.local_action_writing_mode = Language_Item_Definer("reverse " + self.local_action_writing_mode, self.local_action_writing_mode + " inversamente")
			self.local_english_action_writing_mode = "reverse " + self.local_english_action_writing_mode
			self.local_english_infinitive_writing_mode = "reverse " + self.local_english_infinitive_writing_mode
			self.local_english_present_writing_mode = "reverse " + self.local_english_present_writing_mode

		self.string_to_format = self.local_chapter_status + " a {} o capítulo {} de {}" + self.text_to_add + "."
		self.formatted_string = self.string_to_format.format(self.local_action_writing_mode, str(Remove_Leading_Zeros(self.chapter_number)), "\"" + self.story_name + "\"")

		self.string_to_format = self.english_local_chapter_status + " to {} the chapter {} of {}" + self.english_text_to_add + "."
		self.english_formatted_string = self.string_to_format.format(self.english_writing_mode, str(Remove_Leading_Zeros(self.chapter_number)), "\"" + self.english_story_name + "\"")

		self.chapter_done_header += self.formatted_string + "\n\n"
		self.english_chapter_done_header += self.english_formatted_string + "\n\n"

		self.string_to_format = self.chapter_past_action + " por {}."
		self.formatted_string = self.string_to_format.format(self.time_difference)

		self.chapter_done_header += self.formatted_string + "\n"

		self.string_to_format = self.english_chapter_past_action + " for {}."
		self.formatted_string = self.string_to_format.format(self.english_time_difference)

		self.english_chapter_done_header += self.formatted_string + "\n"

		self.chapter_done_header += "\n"
		self.english_chapter_done_header += "\n"

		self.string_to_format = "{}Terminei de " + self.local_action_writing_mode + " o capítulo."

		if self.finished_writing_chapter == True:
			self.formatted_string = self.string_to_format.replace("{}", "")

		if self.finished_writing_chapter == False:
			self.formatted_string = self.string_to_format.format("Ainda não ").replace("T", "t")

		self.chapter_done_header += self.formatted_string

		self.string_to_format = "{}Finished " + self.local_english_present_writing_mode + " the chapter."

		if self.finished_writing_chapter == True:
			self.formatted_string = self.string_to_format.replace("{}", "")

		if self.finished_writing_chapter == False:
			self.formatted_string = self.string_to_format.format("Still did not ").replace("F", "f")

		self.english_chapter_done_header += self.formatted_string

	def Finish_Writing(self):
		self.print_text = Language_Item_Definer("Press Enter when you finish {} the chapter", "Pressione Enter quando você terminar de {} o capítulo")

		self.past_written_time = time.strftime("%H:%M %d/%m/%Y")

		Select_Choice(Language_Item_Definer("Press Enter to start counting time", "Pressione Enter para começar a contar o tempo"), first_space = False, second_space = False, accept_enter = True, enter_equals_empty = True)

		print()
		self.time_difference, self.total_time, self.original_time = Make_Time_Difference(self.current_written_time_file, True, global_language, self.print_text.format(self.action_writing_mode.lower()), show_texts = True)
		self.english_time_difference = Make_Time_Text(str(self.original_time), "enus", add_original_time = True)

		print()

		self.local_action_writing_mode = self.action_writing_mode.lower()

		if self.writing_mode == self.translate and self.reverse_translate == True:
			self.local_action_writing_mode = Language_Item_Definer("reverse " + self.local_action_writing_mode, self.local_action_writing_mode + " inversamente")

		if self.writing_mode == self.write:
			self.choice_text = Language_Item_Definer("Finished {} the chapter", "Terminou de {} o capítulo")

			self.finished_writing_chapter = Yes_Or_No_Definer(self.choice_text.format(self.local_action_writing_mode), first_space = False)

		if self.writing_mode == self.revise:
			self.choice_text = Language_Item_Definer("Finished {} the chapter (ready to {})", "Terminou de {} o capítulo (pronto para {})")

			self.finished_writing_chapter = Yes_Or_No_Definer(self.choice_text.format(self.local_action_writing_mode, self.next_writing_mode.lower()), first_space = False)

		if self.writing_mode == self.translate:
			self.choice_text = Language_Item_Definer("Finished {} the chapter (ready to {})", "Terminou de {} o capítulo (pronto para {})")

			self.finished_writing_chapter = Yes_Or_No_Definer(self.choice_text.format(self.local_action_writing_mode, self.post_text.lower()), first_space = False)

			self.new_writing_mode = "None"
			self.new_present_writing_mode = "None"

		if self.writing_mode != self.translate:
			self.new_writing_mode = self.writing_modes[self.writing_mode_number + 1]
			self.new_present_writing_mode = self.writing_modes_present[self.writing_mode_number + 1]

		self.choice_text = Language_Item_Definer("Select one chapter to {} next", "Selecione o próximo capítulo para {}")

		self.backup_chapter_title = self.chapter_title

		if self.writing_mode == self.write and self.finished_writing_chapter == True:
			self.new_chapter = "None"
			self.old_chapter = self.chapter_title

			# Ask for the new English chapter title of the new chapter
			self.new_chapter_title = Select_Choice(Language_Item_Definer("Type or paste the new chapter title in English", "Digite ou cole o novo título de capítulo em Inglês"), first_space = False)

			# Makes the full English chapter title like "30 - [New chapter title]"
			self.full_chapter_title = str(self.chapter_number) + self.dash_separator + self.new_chapter_title

			# Ask for the new Portuguese chapter title of the new chapter
			self.new_portuguese_chapter_title = Select_Choice(Language_Item_Definer("Type the new chapter title in Portuguese", "Digite o novo título de capítulo em Português"), first_space = False)

			# Makes the full Portuguese chapter title like "30 - [New chapter title]"
			self.full_portuguese_chapter_title = str(self.chapter_number) + self.dash_separator + self.new_portuguese_chapter_title

			# Writes the new list of English chapter titles to the English chapter titles file
			text_to_append = self.new_chapter_title
			Append_To_File(self.story_chapter_titles_enus_file, text_to_append, self.global_switches, check_file_length = True)

			# Append the Portuguese chapter title to the Portuguese chapter titles file
			text_to_append = self.new_portuguese_chapter_title
			Append_To_File(self.story_chapter_titles_ptbr_file, text_to_append, self.global_switches, check_file_length = True)

			# Reads the chapter text from the English Obsidian chapter file into one string variable
			self.english_chapter_file_text = Read_String(self.obsidian_chapter_file)

			# Creates the English chapter file with filename like "30 - [New chapter title].txt"
			self.chapter_file = self.story_chapters_enus_folder + self.full_chapter_title + self.dot_text
			Create_Text_File(self.chapter_file, self.global_switches)

			# Writes the English chapter file text to the English chapter file
			text_to_write = self.english_chapter_file_text
			Write_To_File(self.chapter_file, text_to_write, self.global_switches)

			# Creates the Portuguese chapter file with filename like "30 - [New chapter title].txt"
			self.portuguese_chapter_file = self.story_chapters_ptbr_folder + self.full_portuguese_chapter_title + self.dot_text
			Create_Text_File(self.portuguese_chapter_file, self.global_switches)

			# Writes the English chapter file text to the Portuguese chapter file for translating later
			text_to_write = self.english_chapter_file_text
			Write_To_File(self.portuguese_chapter_file, text_to_write, self.global_switches)

			# Renames the old English Obsidian chapter file like "30 - 30.md" to "30 - [New chapter title].md"
			self.old_file = self.obsidian_chapter_file
			self.new_file = self.obsidian_chapter_file.replace(self.edited_chapter_title.replace("%20", " "), self.full_chapter_title)
			Move_File(self.old_file, self.new_file, self.global_switches["move_files"])

			# Creates the Portuguese Obsidian chapter file with filename like "30 - [New chapter title].md"
			self.obsidian_portuguese_chapter_file = self.obsidian_story_chapters_ptbr_folder + self.full_portuguese_chapter_title + self.dot_md
			Create_Text_File(self.obsidian_portuguese_chapter_file, self.global_switches)

			# Writes the English chapter file text to the Portuguese Obsidian chapter file for translating later
			text_to_write = self.english_chapter_file_text
			Write_To_File(self.obsidian_portuguese_chapter_file, text_to_write, self.global_switches)

			# Opens the English chapter file on Notepad++
			Open_Text_File(self.chapter_file)

			if self.global_switches["testing_script"] == False:
				sleep(1)

			# Opens the Portuguese chapter file on Notepad++
			Open_Text_File(self.portuguese_chapter_file)

			self.chapter_title = self.full_chapter_title

		if self.writing_mode == self.revise and self.finished_writing_chapter == True:
			self.new_chapter = "None"
			self.old_chapter = self.backup_chapter_title

		if self.writing_mode == self.translate and self.finished_writing_chapter == True:
			self.new_chapter = "None"

			self.chapter_title = str(self.chapter_number) + self.dash_separator + self.english_chapter_titles[int(self.chapter_number)]

			self.old_chapter = self.chapter_title

			self.chapter_file_text = Read_String(self.obsidian_chapter_file)

			text_to_write = self.chapter_file_text
			Write_To_File(self.first_file, text_to_write, self.global_switches)

		if self.finished_writing_chapter == True and self.testing_script == False:
			self.Set_Status(self.writing_mode, self.new_present_writing_mode, self.new_chapter, self.old_chapter, is_new_chapter = False, finished_writing = self.finished_writing_chapter)

		self.Define_Diary_Slim_Texts()

		if self.writing_mode == self.write or self.writing_mode == self.revise:
			self.add_text = " in English", " em Inglês"

		if self.writing_mode == self.translate and self.reverse_translate == False:
			self.add_text = " to Portuguese", " para Brasileiro"

		if self.writing_mode == self.translate and self.reverse_translate == True:
			self.add_text = " in English", " em Inglês"

		self.local_past_action_writing_mode_enus = self.past_action_writing_mode_enus
		self.local_past_action_writing_mode_ptbr = self.past_action_writing_mode_ptbr

		if self.writing_mode == self.translate and self.reverse_translate == True:
			self.local_past_action_writing_mode_enus = "Reverse " + self.local_past_action_writing_mode_enus.lower()
			self.local_past_action_writing_mode_ptbr = self.local_past_action_writing_mode_ptbr + " inversamente"

		self.task_name_enus = "{} the chapter {} of \"{}\"".format(self.local_past_action_writing_mode_enus, number_names_en[int(self.chapter_number)], self.english_story_name) + self.add_text[0]
		self.task_name_ptbr = "{} o capítulo {} de \"{}\"".format(self.local_past_action_writing_mode_ptbr, number_names_pt[int(self.chapter_number)], self.portuguese_story_name) + self.add_text[1]

		self.experienced_media_type = "Writing - Escrita"
		self.english_task_description = self.english_chapter_done_header
		self.portuguese_task_description = self.chapter_done_header
		self.experienced_media_time = time.strftime("%H:%M %d/%m/%Y")

		self.custom_write_text = self.chapter_done_header
		self.custom_time = self.past_written_time

		self.register_task_backup = self.register_task

		if self.finished_writing_chapter == True and self.register_task_backup == True:
			self.register_task = True

		if self.finished_writing_chapter == False:
			self.register_task = False

		if self.global_switches["testing_script"] == False:
			self.Register_Finished_Task(register_task = self.register_task, register_on_diary_slim = True, custom_write_text = self.custom_write_text, custom_time = self.custom_time)
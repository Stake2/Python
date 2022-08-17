# Register_Task.py

from Script_Helper import *

from Tasks.Tasks import Tasks as Tasks

from Diary_Slim.Write_On_Diary_Slim_Module import Write_On_Diary_Slim_Module as Write_On_Diary_Slim_Module

class Register_Task(Tasks):
	def __init__(self, run_as_module = False, task_data = {}, show_text = True, skip_input = False, parameter_switches = None):
		super().__init__(parameter_switches)

		self.run_as_module = run_as_module
		self.task_data = task_data
		self.show_text = show_text
		self.skip_input = skip_input

		if self.run_as_module == False:
			self.Select_Type()
			self.Ask_For_Task_Info()

		if self.run_as_module == True:
			self.experienced_media_type = self.task_data["experienced_media_type"]
			self.english_task_description = self.task_data["english_task_description"]
			self.portuguese_task_description = self.task_data["portuguese_task_description"]
			self.experienced_media_time = self.task_data["experienced_media_time"]

			self.english_task_name = self.english_task_description.splitlines()[0]

			if "." in self.english_task_name[-1]:
				self.english_task_name = self.english_task_name[:-1]

			self.portuguese_task_name = self.portuguese_task_description.splitlines()[0]

			if "." in self.portuguese_task_name[-1]:
				self.portuguese_task_name = self.portuguese_task_name[:-1]

			self.task_name = Language_Item_Definer(self.english_task_name, self.portuguese_task_name)

			self.language_experienced_media_type = self.experienced_media_type

			if " - " in self.experienced_media_type:
				self.language_experienced_media_type = self.language_experienced_media_type.split(" - ")[Language_Item_Definer(0, 1)]

			self.task_descriptions = {
			full_language_en: self.english_task_description,
			full_language_pt: self.portuguese_task_description,
			}

		self.Add_To_Experienced_Numbers()
		self.Make_Task_Text()
		self.Add_Experienced_Media_To_Text_Files()
		self.Create_Experienced_Media_Text_Files()
		self.Check_First_Done_In_Year()

		if self.show_text == True:
			self.Show_Task_Data()
			self.Register_Experienced_Media_On_Diary_Slim()

			if self.skip_input == False:
				print()
				print("---")
				print()
				input(Language_Item_Definer("Press Enter when you finish reading the Info Summary", "Pressione Enter quando terminar de ler o Resumo de Informações") + ": ")

	def Select_Type(self):
		self.choice_text = Language_Item_Definer("Select a Task Type to use", "Selecione um Tipo de Tarefa para usar")
		self.experienced_media_type = Select_Choice_From_List(self.language_media_types, local_script_name, self.choice_text, second_choices_list = self.media_types, return_second_item_parameter = True, return_number = True, add_none = True, second_space = False)

		self.language_experienced_media_type = self.language_media_types[self.experienced_media_type[1] - 1]
		self.experienced_media_type = self.experienced_media_type[0]

	def Ask_For_Task_Info(self):
		self.describe_task_text = Language_Item_Definer("Describe the Task in {}", "Descreva a Tarefa em {}")

		translated_language = full_languages_translated_dict[full_language_en][language_number]
		self.choice_text = self.describe_task_text.format(translated_language)
		self.english_task_description = Text_Writer(self.choice_text + ":", finish_text = "default_list", second_space = False, capitalize_lines = True, auto_add_dots = True, accept_enter = True)

		translated_language = full_languages_translated_dict[full_language_pt][language_number]
		self.choice_text = self.describe_task_text.format(translated_language)
		self.portuguese_task_description = Text_Writer(self.choice_text + ":", finish_text = "default_list", second_space = False, capitalize_lines = True, auto_add_dots = True, accept_enter = True)
		self.experienced_media_time = time.strftime("%H:%M %d/%m/%Y")

		self.english_task_name = self.english_task_description.splitlines()[0].replace(".", "")
		self.portuguese_task_name = self.portuguese_task_description.splitlines()[0].replace(".", "")
		self.task_name = Language_Item_Definer(self.english_task_name, self.portuguese_task_name)

		self.task_descriptions = {
			full_language_en: self.english_task_description,
			full_language_pt: self.portuguese_task_description,
		}

	def Add_To_Experienced_Numbers(self):
		self.media_type_experienced_number_file = self.per_media_type_number_files[self.experienced_media_type]

		# Current Year Experienced Media Folder >

			# Per Media Type >
				# Files (Writes) > 
					# [Media Type] >
						# Number.txt

			# Writes:
				# Number.txt

		self.total_experienced_number = Change_Number(Create_Array_Of_File(self.total_experienced_number_current_year_file)[0], "more", 1)
		self.media_type_experienced_number = Change_Number(Create_Array_Of_File(self.media_type_experienced_number_file)[0], "more", 1)

		# Number.txt
		text_to_write = str(self.total_experienced_number)

		if Read_String(self.total_experienced_number_current_year_file) != text_to_write:
			Write_To_File(self.total_experienced_number_current_year_file, text_to_write, self.global_switches)

		# Files (Writes) > [Media Type] > Number.txt
		text_to_write = str(self.media_type_experienced_number)

		if Read_String(self.media_type_experienced_number_file) != text_to_write:
			Write_To_File(self.media_type_experienced_number_file, text_to_write, self.global_switches)

	def Make_Task_Text(self):
		self.task_text_file_contents = self.total_experienced_number + ", " + self.media_type_experienced_number + "\n" + self.experienced_media_type + "\n" + self.experienced_media_time + "\n\n" + self.english_task_description + "\n\n-\n\n" + self.portuguese_task_description

		self.replaced_experienced_media_time = Text_Replacer(Text_Replacer(self.experienced_media_time, "/", "-"), ":", ";")

		self.root_task_file_name = self.experienced_media_type + " " + self.replaced_experienced_media_time
		self.media_type_task_file_name = self.replaced_experienced_media_time

	def Add_Experienced_Media_To_Text_Files(self):
		# Current Year Experienced Media Folder >

			# Appends:
				# Tasks.txt
				# Task Types.txt
				# Times.txt

		# Tasks.txt
		text_to_append = self.english_task_name
		Append_To_File(self.experienced_files[self.english_tasks_text], text_to_append, self.global_switches, check_file_length = True)

		# Task Types.txt
		text_to_append = self.experienced_media_type
		Append_To_File(self.experienced_files["Task Types"], text_to_append, self.global_switches, check_file_length = True)

		# Times.txt
		text_to_append = self.experienced_media_time
		Append_To_File(self.experienced_files[self.times_english_text], text_to_append, self.global_switches, check_file_length = True)

		# ------------------ #

		# Current Year Experienced Media Folder >

			# Per Media Type >
				# Files (Appends) > 
					# [Media Type] >
						# Tasks.txt, Times.txt

		self.per_media_type_files_folder = self.per_media_type_files_folders[self.experienced_media_type]
		self.tasks_file = self.per_media_type_task_files[self.experienced_media_type]
		self.times_file = self.per_media_type_time_files[self.experienced_media_type]

		# Files (Appends) > [Media Type] > Tasks.txt
		text_to_append = self.english_task_name
		Append_To_File(self.tasks_file, text_to_append, self.global_switches, check_file_length = True)

		# Files (Appends) > [Media Type] > Times.txt
		text_to_append = self.experienced_media_time
		Append_To_File(self.times_file, text_to_append, self.global_switches, check_file_length = True)

		# ------------------ #

		# Current Year Experienced Media Folder >
			# All Experienced Files (Creates) >
				# [Experienced number]. [Media name] [Media task title].txt
					# Contents:
					# [All Tasks Number]
					# [Media type]
					# [Experienced time]
					# 
					# [English Task description]
					# 
					# -
					# 
					# [Portuguese Task description]

			# Per Media Type >
				# Files (Appends) > 
					# [Media Type] >
						# Tasks.txt, Times.txt, Number.txt

				# Folders >
					# [Media Type] (Creates) >
						# [Media name] >
							# [Media task title without media name].txt
								# Contents:
								# [All Tasks Number], [Per Media Type Number]
								# [Media type]
								# [Experienced time]
								# 
								# [English Task description]
								# 
								# -
								# 
								# [Portuguese Task description]

			# Appends:
				# Tasks.txt
				# Task Types.txt
				# Times.txt
				# Number.txt

		text = ""

	def Create_Experienced_Media_Text_Files(self):
		# Current Year Experienced Media Folder >

			# All Experienced Files (Creates) >
				# [Experienced number]. [Media name] [Media task title].txt
					# Contents:
					# [All Tasks Number]
					# [Media type]
					# [Experienced time]
					# 
					# [English Task description]
					# 
					# -
					# 
					# [Portuguese Task description]

		# [Experienced number]. [Media name] [Media task title].txt
		self.current_task_file = self.all_experienced_files_current_year_folder + str(self.total_experienced_number) + ". " + self.root_task_file_name + self.dot_text
		Create_Text_File(self.current_task_file, self.global_switches["create_files"])

		text_to_write = self.task_text_file_contents
		Write_To_File(self.current_task_file, text_to_write, self.global_switches)

		# ------------------ #

		self.per_media_type_folder = self.per_media_type_folder_folders_dict[self.experienced_media_type]

		# Current Year Experienced Media Folder >

			# Per Media Type >
				# Folders >
					# [Media Type] (Creates) >
						# [Media name] >
							# [Media task title without media name].txt
								# Contents:
								# [All Tasks Number], [Per Media Type Number]
								# [Media type]
								# [Experienced time]
								# 
								# [English Task description]
								# 
								# -
								# 
								# [Portuguese Task description]

		self.per_media_type_media_task_file = self.per_media_type_folder + self.media_type_task_file_name + self.dot_text
		Create_Text_File(self.per_media_type_media_task_file, self.global_switches["create_files"])

		text_to_write = self.task_text_file_contents
		Write_To_File(self.per_media_type_media_task_file, text_to_write, self.global_switches)

		# ------------------ #

		text = ""

	def Check_First_Done_In_Year(self):
		self.firsts_of_the_year_language_texts = {
		full_language_en: "Firsts Of The Year",
		full_language_pt: "Primeiros Do Ano",
		}

		self.media_language_text = self.experienced_media_type

		if self.experienced_media_type == "Stories - Histórias":
			self.media_language_text = "Art/Story - Arte/História"

		if self.experienced_media_type == "Writing - Escrita":
			self.media_language_text = "Art/Story Chapter - Arte/Capítulo de História"

		if self.experienced_media_type == "Python" or self.experienced_media_type == "PHP":
			self.media_language_text = "Programming/" + self.experienced_media_type + " - " + "Programação/" + self.experienced_media_type

		if self.experienced_media_type == "Drawings - Desenhos":
			self.media_language_text = "Art/Drawing - Arte/Desenho"

		if self.experienced_media_type == "Videos - Vídeos":
			self.media_language_text = "Art/Video - Arte/Vídeo"

		english = self.media_language_text
		portuguese = self.media_language_text

		if " - " in self.media_language_text:
			self.media_language_text = self.media_language_text.split(" - ")
			english = self.media_language_text[0]
			portuguese = self.media_language_text[1]

		self.media_language_texts = {
		full_language_en: english,
		full_language_pt: portuguese,
		}

		self.firsts_of_the_year_folders = {}
		self.firsts_of_the_year_media_type_folders = {}

		for full_language in full_languages_not_none:
			self.firsts_of_the_year_folders[full_language] = current_notepad_year_folder + full_language + "/" + self.firsts_of_the_year_language_texts[full_language] + "/"
			self.firsts_of_the_year_media_type_folders[full_language] = self.firsts_of_the_year_folders[full_language] + self.media_language_texts[full_language] + "/"

			Create_Folder(self.firsts_of_the_year_folders[full_language], self.global_switches["create_folders"])
			Create_Folder(self.firsts_of_the_year_media_type_folders[full_language], self.global_switches["create_folders"])

		self.first_done_task_file_name = self.total_experienced_number + ". " + self.root_task_file_name

		self.is_first_made_task_per_type = False

		if len(Create_Array_Of_File(self.tasks_file)) == 0:
			self.is_first_made_task_per_type = True

		if self.is_first_made_task_per_type == True:
			for full_language in full_languages_not_none:
				media_type_folder = self.firsts_of_the_year_media_type_folders[full_language]

				self.first_done_task_file = media_type_folder + self.first_done_task_file_name + self.dot_text
				Create_Text_File(self.first_done_task_file, self.global_switches["create_files"])

				self.text_to_write = self.task_text_file_contents
				Write_To_File(self.first_done_task_file, self.text_to_write, self.global_switches)

				if self.global_switches["verbose"] == True:
					print("[" + self.text_to_write + "]")

	def Register_Experienced_Media_On_Diary_Slim(self):
		Write_On_Diary_Slim_Module(self.portuguese_task_description, self.experienced_media_time, self.global_switches, show_text = self.show_text)

	def Show_Task_Data(self):
		if self.skip_input == False:
			print()

		self.registered_task_text = Language_Item_Definer("This Task was registred", "Esta Tarefa foi registrada") + ":"

		if self.global_switches["write_to_file"] == False:
			self.registered_task_text = self.registered_task_text.replace(Language_Item_Definer("was", "foi"), Language_Item_Definer("was not", "não foi"))
			self.registered_task_text = self.registered_task_text.replace(":", ' ("write_to_file" ' + Language_Item_Definer('is "False"', 'é "False"') + "):")

		print("---")
		print()
		print(self.registered_task_text)
		print(self.task_name)
		print()
		print(Language_Item_Definer("Type", "Tipo") + ": " + self.experienced_media_type)
		print(Language_Item_Definer("Type in Language", "Tipo no Idioma") + ": " + self.language_experienced_media_type)
		print()
		print(Language_Item_Definer("When", "Quando") + ": " + self.experienced_media_time)
		print()

		for language in full_languages_not_none:
			translated_language = full_languages_translated_dict[language][language_number]

			print(Language_Item_Definer("{} Task description", "Descrição da Tarefa em {}").format(translated_language) + ": ")
			print("[" + self.task_descriptions[language] + "]")
			print()
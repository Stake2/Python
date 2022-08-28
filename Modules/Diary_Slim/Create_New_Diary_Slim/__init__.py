# Create_New_Diary_Slim.py

from Script_Helper import *

import re

from Diary_Slim.Diary_Slim import Diary_Slim as Diary_Slim

from Diary_Slim.Write_On_Diary_Slim_Module import Write_On_Diary_Slim_Module as Write_On_Diary_Slim_Module

class Create_New_Diary_Slim(Diary_Slim):
	def __init__(self):
		super().__init__()

		self.text_header_prototype = "- Diário Slim, {} -"
		today_is_text_header_prototype = "Hoje é {}, Dia {} de {} de {}."

		self.diary_slim_header_prototype = '''Fui dormir {}, acordei {}, levantei.
Lavei o rosto, liguei o computador.
Bebi um pouco de água, fiz login no computador.
Abri o Diary_Slim.py, criei o novo Diário Slim e o Diary_Slim.py escreveu nele.
Hoje é dia de {}.'''

		self.finished_registering_things_text = Language_Item_Definer("Finished registering things on Habitica and Microsoft Todo", "Terminou de registrar as coisas no Habitica e Microsoft Todo")

		self.Define_Times()

		self.formatted_file_name_string = "{} {}, {}".format(self.current_day, self.today, self.today_extended)

		self.Define_Files()
		self.Write_To_Files()

		if self.diary_slim_exists == False:
			self.Change_Double_State_Texts(reset_current_state = True)
			self.Finish_Registering_Things()

	def Define_Times(self):
		now = datetime.datetime.now()
		today = datetime.datetime.today()

		self.current_month = now.month
		self.current_month_name = month_names_ptbr[int(self.current_month)]

		self.current_day = Add_Leading_Zeros(now.day)
		self.week_day = today.weekday()
		self.today = now.strftime("%A")

		i = 1
		while i <= len(day_names_ptbr) - 1:
			if self.today == day_names_enus[i]:
				self.today = day_names_ptbr[i]

			i += 1

		self.today_extended = time.strftime("%d-%m-%Y")

	def Define_Files(self):
		self.current_month_folder_name = str(Add_Leading_Zeros(self.current_month)) + " - " + self.current_month_name

		# Current month folder
		self.diary_slim_current_month_folder = self.diary_slim_current_year_folder + self.current_month_folder_name + "/"
		Create_Folder(self.diary_slim_current_month_folder, self.global_switches)

		# Current day file
		self.diary_slim_current_day_file = self.diary_slim_current_month_folder + self.formatted_file_name_string + self.dot_text

	def Make_Header(self):
		self.today_is = "Hoje é {}, Dia {} de {} de {}.".format(self.today, self.current_day, self.current_month_name, current_year)
		self.text_header = "- Diário Slim, {} -".format(self.formatted_file_name_string)

		self.things_to_do = Create_Array_Of_File(self.diary_slim_things_to_do_file)[self.week_day]

		self.type_the_time_that_you_text = Language_Item_Definer("Type the time that you", "Digite a hora que você")
		self.format_text = " (" + Language_Item_Definer("format", "formato") + ": 00:00)"

		self.choice_text = self.type_the_time_that_you_text + " " + Language_Item_Definer("have gone to sleep", "foi dormir") + self.format_text

		self.sleeping_time = Select_Choice(self.choice_text, first_space = False, second_space = False)
		self.Match_Time_Pattern(self.sleeping_time)
		self.sleeping_time = self.time

		print()

		self.choice_text = self.type_the_time_that_you_text + " " + Language_Item_Definer("woke up", "acordou") + self.format_text

		self.waking_time = Select_Choice(self.choice_text, first_space = False, second_space = False)
		self.Match_Time_Pattern(self.waking_time)
		self.waking_time = self.time

		self.header = self.diary_slim_header_prototype.format(self.sleeping_time, self.waking_time, self.things_to_do)

	def Match_Time_Pattern(self, time):
		pattern = "^[0-9][0-9]:[0-9][0-9]$"

		self.time = time

		if re.match(pattern, self.time) == None:
			i = 1
			while re.match(pattern, self.time) == None:
				choice_text = Language_Item_Definer("Wrong format, utilize this one", "Formato incorreto, utilize este") + ": 00:00 " + "({})".format(str(i))

				self.time = Select_Choice(choice_text, first_space = False, second_space = False)

				i += 1

	def Write_To_Files(self):
		self.diary_slim_exists = False

		if is_a_file(self.diary_slim_current_day_file) == False:
			Create_Text_File(self.diary_slim_current_day_file, self.global_switches)

			self.Make_Header()

			text_to_write = self.diary_slim_current_day_file
			Write_To_File(self.current_diary_slim_file, text_to_write, self.global_switches)

			self.read_file = Create_Array_Of_File(self.diary_slim_current_day_file)

			self.now = time.strftime("%H:%M %d/%m/%Y")

			text_to_write = self.text_header + "\n\n" + self.now + ":\n" + self.today_is + "\n\n" + self.header

			if len(self.read_file) == 0:
				print()

				Write_On_Diary_Slim_Module(text_to_write, parameter_switches = self.global_switches, add_time = False, write = True)

				print()
				print(Language_Item_Definer("The file was created, opening it", "O arquivo foi criado, abrindo ele") + "...")

				Open_Text_File(self.diary_slim_current_day_file)

			self.diary_slim_exists = False

		else:
			print(Language_Item_Definer("The file already exists, opening it", "O arquivo já existe, abrindo ele") + "...")

			Open_Text_File(self.diary_slim_current_day_file)

			self.diary_slim_exists = True

		self.current_month_database_folder = self.diary_slim_database_year_folders[current_year] + self.current_month_folder_name + "/"
		Create_Folder(self.current_month_database_folder, self.global_switches)

		# ----- #

		# All File Names.txt
		text_to_append = self.formatted_file_name_string

		if text_to_append not in Create_Array_Of_File(self.all_file_names_file) and self.diary_slim_exists == False:
			Append_To_File(self.all_file_names_file, text_to_append, self.global_switches, check_file_length = True)

		# All Year Folders.txt
		text_to_append = str(current_year) + "/"

		if self.diary_slim_exists == False:
			Append_To_File(self.all_year_folders_file, text_to_append, self.global_switches, check_file_length = True)

		# All Month Folders.txt
		text_to_append = str(self.current_month_folder_name + "/")

		if self.diary_slim_exists == False:
			Append_To_File(self.all_month_folders_file, text_to_append, self.global_switches, check_file_length = True)

		# ----- #

		# Current year and month text files

		self.current_year_database_file_names_file = self.diary_slim_database_year_folders[current_year] + "Year File Names" + self.dot_text
		Create_Text_File(self.current_year_database_file_names_file, self.global_switches)

		self.current_month_database_file_names_file = self.current_month_database_folder + "Month File Names.txt"
		Create_Text_File(self.current_month_database_file_names_file, self.global_switches)

		text_to_append = self.formatted_file_name_string

		# [Year]/Year File Names.txt
		if text_to_append not in Create_Array_Of_File(self.current_year_database_file_names_file) and self.diary_slim_exists == False:
			Append_To_File(self.current_year_database_file_names_file, text_to_append, self.global_switches, check_file_length = True)

		# [Year]/[Month]/Month File Names.txt
		if text_to_append not in Create_Array_Of_File(self.current_month_database_file_names_file) and self.diary_slim_exists == False:
			Append_To_File(self.current_month_database_file_names_file, text_to_append, self.global_switches, check_file_length = True)

		# ----- #

	def Finish_Registering_Things(self):
		self.finished_registering_things = Yes_Or_No_Definer(self.finished_registering_things_text, second_space = False)

		if self.finished_registering_things == False:
			i = 1
			while self.finished_registering_things == False:
				self.finished_registering_things = Yes_Or_No_Definer(self.finished_registering_things_text + " ({}x)".format(str(i)), second_space = False)

				i += 1

		if self.finished_registering_things == True:
			print()

			text_to_write = "Abri o Firefox e marquei as coisas no Microsoft Todo e Habitica."
			Write_On_Diary_Slim_Module(text_to_write, time.strftime("%H:%M %d/%m/%Y"), self.global_switches)
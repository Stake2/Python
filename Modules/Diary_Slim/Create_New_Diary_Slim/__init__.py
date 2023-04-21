# Create_New_Diary_Slim.py

from Diary_Slim.Diary_Slim import Diary_Slim as Diary_Slim

from Diary_Slim.Write_On_Diary_Slim_Module import Write_On_Diary_Slim_Module as Write_On_Diary_Slim_Module

import re

class Create_New_Diary_Slim(Diary_Slim):
	def __init__(self):
		super().__init__()

		self.Define_Times()

		print()
		print(self.large_bar)
		print()
		print(self.language_texts["today_is"] + ":")
		print(self.day_of_of_text.replace("Dia ", "").format(self.date["day"], self.date["month_name"], self.date["year"]))
		print()

		self.Define_Slim_File()

		if self.diary_slim_exists == False:
			print(self.language_texts["creating_diary_slim_for_the_current_day"] + "...")
			print()

		if self.diary_slim_exists == True:
			print(self.language_texts["the_file_{}_opening_it"].format(self.language_texts["already_existed"]) + "...")

		if self.diary_slim_exists == False:
			self.Make_Header()

		self.Write_To_Files()

		if self.diary_slim_exists == False:
			# Reset all states to have no current order
			self.Update_State(new_order = "")

		print()
		print(self.large_bar)

	def Define_Times(self):
		self.date = self.Date.Now()

		self.file_name_string = "{} {}, {}".format(self.Text.Add_Leading_Zeroes(self.date["day"]), self.date["day_name"], self.date["%d-%m-%Y"])

	def Make_Header(self):
		self.today_is = self.today_is_text_header_prototype.format(self.date["day_name"], self.date["day"], self.date["month_name"], self.date["year"])
		self.text_header = self.text_header_prototype.format(self.file_name_string)

		self.select_text = self.language_texts["type_the_time_that_you_{}"].format(self.language_texts["have_gone_to_sleep"])
		self.sleeping_time = self.Match_Time_Pattern(self.select_text)

		self.select_text = self.language_texts["type_the_time_that_you_{}"].format(self.language_texts["woke_up"])
		self.waking_time = self.Match_Time_Pattern(self.select_text)

		self.header = self.diary_slim_header.format(self.sleeping_time, self.waking_time)

	def Match_Time_Pattern(self, select_text):
		pattern = "^[0-9][0-9]:[0-9][0-9]$"

		time = ""

		format_text = " ({}: 00:00)"

		select_text += format_text.format(self.language_texts["format"])

		if re.match(pattern, time) == None:
			i = 1
			while re.match(pattern, time) == None:
				if time != "":
					select_text += format_text.format(self.language_texts["wrong_format_utilize_this_one"])

				time = self.Input.Type(select_text, first_space = False)

				print()

				i += 1

		if re.match(pattern, time) != None:
			return time

	def Define_Slim_File(self):
		self.diary_slim_exists = False

		# Current day file
		self.current_day_file = self.current_month_folder + self.file_name_string + ".txt"

		if self.File.Exist(self.current_day_file) == True:
			self.diary_slim_exists = True

		if self.File.Exist(self.current_day_file) == False:
			self.File.Create(self.current_day_file)

	def Write_To_Files(self):
		if self.diary_slim_exists == False:
			print(self.dash_space)
			print()

			self.current_day_file_text = self.File.Contents(self.current_day_file)["string"]

			if self.current_day_file_text == "":
				self.File.Edit(self.current_diary_slim_file, self.current_day_file, "w")

			text_to_write = self.text_header + "\n\n" + self.Date.Now()["%H:%M %d/%m/%Y"] + ":\n" + self.today_is + "\n\n" + self.header

			if self.current_day_file_text == "":
				Write_On_Diary_Slim_Module(text_to_write, add_time = False, check_file_length = False)

			print()
			print(self.dash_space)

		self.File.Open(self.current_day_file)

		# ----- #

		if self.diary_slim_exists == False:
			# Year folders.txt
			text_to_append = str(self.date["year"]) + "/"

			self.File.Edit(self.year_folders_file, text_to_append, "a")

			# Month folders.txt
			text_to_append = str(self.month_folder_name + "/")

			self.File.Edit(self.month_folders_file, text_to_append, "a")

			# File names.txt
			text_to_append = self.file_name_string

			if text_to_append not in self.File.Contents(self.file_names_file)["lines"]:
				self.File.Edit(self.file_names_file, text_to_append, "a")

		# ----- #

		if self.diary_slim_exists == False:
			text_to_append = self.file_name_string

			# [Year]/Year file names.txt
			if text_to_append not in self.File.Contents(self.current_year_file_names_file)["lines"]:
				self.File.Edit(self.current_year_file_names_file, text_to_append, "a")

			# [Year]/[Month]/Month file names.txt
			if text_to_append not in self.File.Contents(self.current_month_file_names_file)["lines"]:
				self.File.Edit(self.current_month_file_names_file, text_to_append, "a")

		# ----- #
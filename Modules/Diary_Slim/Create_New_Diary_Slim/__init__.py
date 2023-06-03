# Create_New_Diary_Slim.py

from Diary_Slim.Diary_Slim import Diary_Slim as Diary_Slim

from Diary_Slim.Write_On_Diary_Slim_Module import Write_On_Diary_Slim_Module as Write_On_Diary_Slim_Module

import re

class Create_New_Diary_Slim(Diary_Slim):
	def __init__(self):
		super().__init__()

		print()
		print(self.large_bar)
		print()
		print(self.language_texts["today_is"] + ":")
		print(self.day_of_of_text.replace("Dia ", "").format(self.date["Units"]["Day"], self.date["Texts"]["Month name"][self.user_language], self.date["Units"]["Year"]))
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

	def Make_Header(self):
		self.today_is = self.today_is_text_header_prototype.format(self.date["Texts"]["Day name"][self.user_language], self.date["Units"]["Day"], self.date["Texts"]["Month name"][self.user_language], self.date["Units"]["Year"])

		self.text_header = self.text_header_prototype.format(self.current_day)

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
		current_month = list(self.current_year["Year"]["Months"].keys())[-1]

		if self.File.Exist(self.current_year["File"]) == True:
			self.diary_slim_exists = True

		if self.File.Exist(self.current_year["File"]) == False:
			self.File.Create(self.current_year["File"])

	def Write_To_Files(self):
		from copy import deepcopy

		# Write the header text
		if self.diary_slim_exists == False:
			print(self.dash_space)
			print()

			self.current_day_file_text = self.File.Contents(self.current_year["File"])["string"]

			text_to_write = self.text_header + "\n\n" + self.Date.Now()["Formats"]["HH:MM DD/MM/YYYY"] + ":\n" + self.today_is + "\n\n" + self.header

			if self.current_day_file_text == "":
				Write_On_Diary_Slim_Module(text_to_write, add_time = False, check_file_length = False)

			print()
			print(self.dash_space)

		# Open the Diary Slim file
		self.File.Open(self.current_year["File"])

		# ----- #

		if self.diary_slim_exists == False:
			day = deepcopy(self.templates["Day"])

			# Create the Day dictionary
			day["Day"] = self.date["Units"]["Day"]
			day["Names"] = self.date["Texts"]["Day name"]
			day["Formats"]["DD-MM-YYYY"] = self.date["Formats"]["DD-MM-YYYY"]
			day["Creation time"]["HH:MM"] = self.date["Formats"]["HH:MM"]
			day["Creation time"]["Hours"] = self.date["Units"]["Hour"]
			day["Creation time"]["Minutes"] = self.date["Units"]["Minute"]
			day["Data"]["Sleep times"] = {
				"Slept": self.sleeping_time,
				"Woke up": self.waking_time
			}

			# Edit the Month dictionary
			key = self.current_day

			# Add to the Diary Slims dictionary
			self.current_year["Month"]["Dictionary"]["Diary Slims"][key] = day

			# Update the "Diary Slims" number
			self.current_year["Month"]["Dictionary"]["Numbers"]["Diary Slims"] = len(list(self.current_year["Month"]["Dictionary"]["Diary Slims"].keys()))

			# Edit the "Month.json" file
			self.JSON.Edit(self.current_year["Month"]["File"], self.current_year["Month"]["Dictionary"])

			# Edit the "Year.json" file
			self.current_year["Year"]["Months"][self.current_year["Month"]["Name"]] = self.current_year["Month"]["Dictionary"]

			self.JSON.Edit(self.folders["diary_slim"]["current_year"]["year"], self.current_year["Year"])

			super().__init__()
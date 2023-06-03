# Create_New_Diary_Slim.py

from Diary_Slim.Diary_Slim import Diary_Slim as Diary_Slim

from Diary_Slim.Write_On_Diary_Slim_Module import Write_On_Diary_Slim_Module as Write_On_Diary_Slim_Module

class Create_New_Diary_Slim(Diary_Slim):
	def __init__(self, dictionary = {}):
		super().__init__()

		self.dictionary = dictionary

		if "Date" not in self.dictionary:
			self.dictionary["Date"] = self.Date.Now()

		self.current_diary_slim = self.Current_Diary_Slim(date = self.dictionary["Date"])

		if "File" not in self.dictionary:
			self.dictionary["File"] = self.current_diary_slim["File"]

		if "Check" not in self.dictionary:
			print()

		text = self.JSON.Language.language_texts["today_is"]

		if "Check" in self.dictionary:
			text = self.language_texts["skipped_diary_slim_day"]

		self.today_is_text = text + ":" + "\n" + \
		self.day_of_of_text.replace("Dia ", "").format(self.dictionary["Date"]["Units"]["Day"], self.dictionary["Date"]["Texts"]["Month name"][self.user_language], self.dictionary["Date"]["Units"]["Year"])

		print(self.large_bar)
		print()
		print(self.today_is_text)
		print()

		self.Define_Slim_File()

		if self.dictionary["Diary Slim exists"] == False:
			text = self.language_texts["creating_the_diary_slim_for_the_current_day"]

			if "Check" in self.dictionary:
				text = self.language_texts["creating_the_skipped_diary_slim"]

			print(text + "...")

			if "Check" not in self.dictionary:
				print()

		if self.dictionary["Diary Slim exists"] == True and "Check" not in self.dictionary:
			print(self.File.language_texts["the_file_{}_opening_it"].format(self.File.language_texts["already_existed"]) + "...")

		if self.dictionary["Diary Slim exists"] == False:
			self.Make_Header()

		self.Write_To_Files()

		if self.dictionary["Diary Slim exists"] == False:
			# Reset all states to have no current order
			self.Update_State(new_order = "")

		if "Check" not in self.dictionary:
			print()
			print(self.large_bar)

	def Make_Header(self):
		self.dictionary["Today is"] = self.today_is_text_header_prototype.format(self.dictionary["Date"]["Texts"]["Day name"][self.user_language], self.dictionary["Date"]["Units"]["Day"], self.dictionary["Date"]["Texts"]["Month name"][self.user_language], self.dictionary["Date"]["Units"]["Year"])

		self.dictionary["Text header"] = self.text_header_prototype.format(self.current_diary_slim["Day"])

		type_text = self.JSON.Language.language_texts["type_the_time_that_you_{}"]

		self.select_text = type_text.format(self.JSON.Language.language_texts["have_gone_to_sleep"])
		self.dictionary["Sleeping time"] = self.Match_Time_Pattern(self.select_text)

		self.select_text = type_text.format(self.JSON.Language.language_texts["woke_up"])
		self.dictionary["Waking time"] = self.Match_Time_Pattern(self.select_text)

		self.dictionary["Header"] = self.diary_slim_header.format(self.dictionary["Sleeping time"], self.dictionary["Waking time"])

	def Match_Time_Pattern(self, select_text):
		pattern = "^[0-9][0-9]:[0-9][0-9]$"

		time = ""

		format_text = " ({}: 00:00)"

		select_text += format_text.format(self.JSON.Language.language_texts["format"])

		format_text_helper = self.JSON.Language.language_texts["wrong_format_utilize_this_one"]

		import re

		if re.match(pattern, time) == None:
			i = 1
			while re.match(pattern, time) == None:
				formatted_text = format_text.format(format_text_helper)

				if time != "" and formatted_text not in select_text:
					select_text += formatted_text

				#if self.switches["testing"] == False:
				if "Check" in self.dictionary:
					print()
				time = self.Input.Type(select_text, first_space = False)

				if "Check" not in self.dictionary:
					print()

				#if self.switches["testing"] == True:
				time = "00:00"

				i += 1

		if re.match(pattern, time) != None:
			return time

	def Define_Slim_File(self):
		self.dictionary["Diary Slim exists"] = False

		# Current day file
		if self.File.Exist(self.dictionary["File"]) == True:
			self.dictionary["Diary Slim exists"] = True

		if self.File.Exist(self.dictionary["File"]) == False:
			self.File.Create(self.dictionary["File"])

			if "Check" not in self.dictionary:
				self.Check_Diary_Slims()

				print()
				print(self.today_is_text)
				print()

	def Check_Diary_Slims(self):
		# Define today
		today_date = self.date
		self.dictionary["Today"] = self.Current_Diary_Slim(date = today_date)["Day"]

		# Define yesterday
		yesterday_date = self.Date.Now(self.date["Object"] - self.Date.Timedelta(days = 1))
		self.dictionary["Yesterday"] = self.Current_Diary_Slim(date = yesterday_date)["Day"]

		# Define the Diary Slims list for a more organized code
		diary_slims_list = list(self.current_month["Dictionary"]["Diary Slims"].keys())

		# If yesterday is not inside the Diary Slims list
		# Then the user skipped a Diary Slim
		if self.dictionary["Yesterday"] not in diary_slims_list:
			# Define the days list
			days_list = list(range(1, self.date["Units"]["Month days"] + 1))
			diary_slims_dictionary = {}

			# Iterate through the days list
			for day in days_list:
				# Define the date and day text
				date = self.Date.Now(self.Date.Date(year = int(self.date["Units"]["Year"]), month = int(self.date["Units"]["Month"]), day = day))

				day_text = self.Current_Diary_Slim(date = date)["Day"]

				# If the day text is not inside the Diary Slims list
				# And the day is less than the current day
				if day_text not in diary_slims_list and day < int(self.date["Units"]["Day"]):
					# Create the day dictionary
					diary_slims_dictionary[day_text] = {
						"Day text": day_text,
						"Date": date
					}

		# Create the skipped Diary Slims
		if diary_slims_dictionary != {}:
			# Define the text to show
			text = self.language_texts["you_skipped_creating_this_diary_slim"]

			if len(list(diary_slims_dictionary.keys())) > 1:
				text = self.language_texts["you_skipped_creating_these_diary_slims"]

			# Show the text
			print(text + ":")

			# Show the names of the skipped Diary Slims
			for day in diary_slims_dictionary:
				day = diary_slims_dictionary[day]

				print(day["Day text"])

			print()

			# Create the skipped Diary Slims
			for day in diary_slims_dictionary:
				day = diary_slims_dictionary[day]

				dictionary = {
					"Date": day["Date"],
					"Check": True
				}

				Create_New_Diary_Slim(dictionary)

				print()

			print(self.large_bar)

	def Write_To_Files(self):
		from copy import deepcopy

		# Write the header text into the Diary Slim
		if self.dictionary["Diary Slim exists"] == False:
			if "Check" in self.dictionary:
				print()

			print(self.dash_space)

			if "Check" not in self.dictionary:
				print()

			# Get the file text
			self.current_day_file_text = self.File.Contents(self.dictionary["File"])["string"]

			# Define the text to write
			text_to_write = self.dictionary["Text header"] + "\n\n" + self.dictionary["Date"]["Formats"]["HH:MM DD/MM/YYYY"] + ":\n" + self.dictionary["Today is"] + "\n\n" + self.dictionary["Header"]

			# If the file is empty
			if self.current_day_file_text == "":
				verbose = None

				if "Check" in self.dictionary:
					verbose = False

				# Write the header text into the Diary Slim file
				Write_On_Diary_Slim_Module(text_to_write, add_time = False, check_file_length = False, verbose = verbose)

			#if "Check" not in self.dictionary:
			#	print()
			#	print(self.dash_space)

		# Open the Diary Slim file
		self.File.Open(self.dictionary["File"])

		# ----- #

		# Add the Diary Slim to the database
		if self.dictionary["Diary Slim exists"] == False:
			day = deepcopy(self.templates["Day"])

			# Create the Day dictionary
			day["Day"] = self.dictionary["Date"]["Units"]["Day"]
			day["Names"] = self.dictionary["Date"]["Texts"]["Day name"]
			day["Formats"]["DD-MM-YYYY"] = self.dictionary["Date"]["Formats"]["DD-MM-YYYY"]
			day["Creation time"]["HH:MM"] = self.dictionary["Date"]["Formats"]["HH:MM"]
			day["Creation time"]["Hours"] = self.dictionary["Date"]["Units"]["Hour"]
			day["Creation time"]["Minutes"] = self.dictionary["Date"]["Units"]["Minute"]
			day["Data"]["Sleep times"] = {
				"Slept": self.dictionary["Sleeping time"],
				"Woke up": self.dictionary["Waking time"]
			}

			# Edit the Month dictionary
			key = self.current_diary_slim["Day"]

			# Add to the Diary Slims dictionary
			self.current_month["Dictionary"]["Diary Slims"][key] = day

			# Update the "Diary Slims" number
			self.current_month["Dictionary"]["Numbers"]["Diary Slims"] = len(list(self.current_month["Dictionary"]["Diary Slims"].keys()))

			# Edit the "Month.json" file
			self.JSON.Edit(self.current_month["File"], self.current_month["Dictionary"], verbose = False)

			# Update the Month dictionary inside the Year dictionary
			self.current_year["Year"]["Months"][self.current_month["Name"]] = self.current_month["Dictionary"]

			# Edit the "Year.json" file
			self.JSON.Edit(self.folders["diary_slim"]["current_year"]["year"], self.current_year["Year"], verbose = False)

			super().__init__()
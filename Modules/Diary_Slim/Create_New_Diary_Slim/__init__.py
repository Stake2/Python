# Create_New_Diary_Slim.py

from Diary_Slim.Diary_Slim import Diary_Slim as Diary_Slim

from Diary_Slim.Write_On_Diary_Slim_Module import Write_On_Diary_Slim_Module as Write_On_Diary_Slim_Module

class Create_New_Diary_Slim(Diary_Slim):
	def __init__(self, dictionary = {}):
		super().__init__()

		self.dictionary = dictionary

		if "Date" not in self.dictionary:
			self.dictionary["Date"] = self.Date.Now()

		self.current_diary_slim = self.Current_Diary_Slim(date = self.dictionary["Date"], current_diary_slim = False)

		if "File" not in self.dictionary:
			self.dictionary["File"] = self.current_diary_slim["File"]

		if "Check" not in self.dictionary:
			print()

		text = self.JSON.Language.language_texts["today_is"]

		if "Check" in self.dictionary:
			text = self.language_texts["skipped_diary_slim_day"]

		date = self.dictionary["Date"]

		units = date["Timezone"]["DateTime"]["Units"]

		self.today_is_text = text + ":" + "\n" + \
		date["Timezone"]["DateTime"]["Texts"]["Day name"][self.user_language] + "\n" + \
		"\n" + \
		self.day_of_of_text.format(units["Day"], date["Timezone"]["DateTime"]["Texts"]["Month name"][self.user_language], units["Year"]) + " (" + date["Formats"]["DD/MM/YYYY"] + ")"

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
		units = self.dictionary["Date"]["Timezone"]["DateTime"]["Units"]
		texts = self.dictionary["Date"]["Timezone"]["DateTime"]["Texts"]

		self.dictionary["Today is"] = self.today_is_text_header_prototype.format(texts["Day name"][self.user_language], units["Day"], texts["Month name"][self.user_language], units["Year"])

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

				if self.switches["testing"] == False:
					if "Check" in self.dictionary:
						print()

					time = self.Input.Type(select_text, first_space = False)

					if "Check" not in self.dictionary:
						print()

				if self.switches["testing"] == True:
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

				if "Checked" in self.dictionary:
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
		diary_slims_list = list(self.current_month["Month"]["Diary Slims"].keys())

		# If yesterday is not inside the Diary Slims list
		# Then the user skipped a Diary Slim
		if self.dictionary["Yesterday"] not in diary_slims_list:
			# Define the days list
			days_list = list(range(1, self.date["Units"]["Month days"] + 1))

			diary_slims_dictionary = {}

			# Iterate through the days list
			for day in days_list:
				# Define the date and day text
				units = self.dictionary["Date"]["Timezone"]["DateTime"]["Units"]

				date = self.Date.Now(self.Date.Date(year = int(units["Year"]), month = int(units["Month"]), day = day))

				day_text = self.Current_Diary_Slim(date = date)["Day"]

				# If the day text is not inside the Diary Slims list
				# And the day is less than the current day
				if (
					day_text not in diary_slims_list and
					day < int(units["Day"])
				):
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

				if hasattr(self, "Create_New_Diary_Slim") == False:
					from Diary_Slim.Create_New_Diary_Slim import Create_New_Diary_Slim as Create_New_Diary_Slim

					self.Create_New_Diary_Slim = Create_New_Diary_Slim

				# Create the skipped Diary Slims
				for day in diary_slims_dictionary:
					day = diary_slims_dictionary[day]

					dictionary = {
						"Date": day["Date"],
						"Check": True
					}

					# Create
					self.object = self.Create_New_Diary_Slim(dictionary)

					# Update local year and month variables here with the new variables
					self.current_year = self.object.current_year
					self.current_month = self.object.current_month

					print()

				print(self.large_bar)

			self.dictionary["Checked"] = True

	def Write_To_Files(self):
		from copy import deepcopy

		# Add the Diary Slim to the database
		if self.dictionary["Diary Slim exists"] == False:
			day = deepcopy(self.templates["Day"])

			units = self.dictionary["Date"]["Timezone"]["DateTime"]["Units"]
			texts = self.dictionary["Date"]["Timezone"]["DateTime"]["Texts"]

			# Create the Day dictionary
			day = {
				"Day": units["Day"],
				"Names": texts["Day name"],
				"Formats": {
					"DD-MM-YYYY": self.dictionary["Date"]["Timezone"]["DateTime"]["Formats"]["DD-MM-YYYY"],
				},
				"Creation time": {
					"HH:MM": self.dictionary["Date"]["Timezone"]["DateTime"]["Formats"]["HH:MM"],
					"Hours": units["Hour"],
					"Minutes": units["Minute"]
				}
			}

			# Check if the sleep times items are inside the dictionary
			keys = [
				"Slept",
				"Woke up"
			]

			i = 0
			for item in ["Sleeping", "Waking"]:
				item = item + " time"

				# If the item is inisde the dictionary
				if item in self.dictionary:
					# Create the data dictionary if it does not exist
					if "Data" not in day:
						day["Data"] = {
							"Sleep times": {}
						}

					# Add the sleep time to the Day dictionary
					day["Data"]["Sleep times"][keys[i]] = self.dictionary[item]

				i += 1

			# Edit the Month dictionary
			key = self.current_diary_slim["Day"]

			# Add to the "Diary Slims" dictionary inside the Month dictionary
			self.current_month["Month"]["Diary Slims"][key] = day

			# Update the month "Diary Slims" number inside the Month dictionary
			self.current_month["Month"]["Numbers"]["Diary Slims"] = len(list(self.current_month["Month"]["Diary Slims"].keys()))

			# Edit the "Month.json" file with the new Month dictionary
			self.JSON.Edit(self.current_month["File"], self.current_month["Month"])

			# ----- #

			# Edit the Year dictionary

			# Update the Month dictionary inside the Year dictionary
			self.current_year["Year"]["Months"][self.current_month["Name"]] = self.current_month["Month"]

			# Update the "Months" number inside the Year dictionary
			self.current_year["Year"]["Numbers"]["Months"] = len(list(self.current_year["Year"]["Months"].keys()))

			# Update the Year "Diary Slims" number inside the Year dictionary
			self.current_year["Year"]["Numbers"]["Diary Slims"] = 0

			# Iterate through the Months list to add to the Year "Diary Slims" number
			for month in self.current_year["Year"]["Months"].values():
				self.current_year["Year"]["Numbers"]["Diary Slims"] += month["Numbers"]["Diary Slims"]

			# Edit the "Year.json" file with the new Year dictionary
			self.JSON.Edit(self.folders["Diary Slim"]["current_year"]["year"], self.current_year["Year"])

		# ----- #

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
			text_to_write = self.dictionary["Text header"] + "\n\n" + \
			self.dictionary["Date"]["Timezone"]["DateTime"]["Formats"]["HH:MM DD/MM/YYYY"] + ":\n" + \
			self.dictionary["Today is"] + "\n\n" + \
			self.dictionary["Header"]

			# If the file is empty
			if self.current_day_file_text == "":
				verbose = None
				current_diary_slim = True

				if "Check" in self.dictionary:
					verbose = False
					current_diary_slim = False

				# Write the header text into the Diary Slim file
				Write_On_Diary_Slim_Module(text_to_write, add_time = False, check_file_length = False, current_diary_slim = current_diary_slim, verbose = verbose)

		# Open the current Diary Slim file
		self.System.Open(self.dictionary["File"])
# Create_New_Diary_Slim.py

from Diary_Slim.Diary_Slim import Diary_Slim as Diary_Slim

from Diary_Slim.Write_On_Diary_Slim_Module import Write_On_Diary_Slim_Module as Write_On_Diary_Slim_Module

class Create_New_Diary_Slim(Diary_Slim):
	def __init__(self, dictionary = {}):
		super().__init__()

		# Define the dictionary as the dictionary parameter
		self.dictionary = dictionary

		# Create the "Texts" key in the dictionary
		self.dictionary["Texts"] = {}

		# If the "Date" dictionary is not present inside the root dictionary
		if "Date" not in self.dictionary:
			# Get a new "Date" dictionary from now
			self.dictionary["Date"] = self.Date.Now()

		# Get the "curreny Diary Slim" dictionary
		self.current_diary_slim = self.Current_Diary_Slim(date = self.dictionary["Date"], current_diary_slim = False)

		# If the "File" key is not inside the dictionary
		if "File" not in self.dictionary:
			# Get the new Diary Slim file from the "current Diary Slim" dictionary
			self.dictionary["File"] = self.current_diary_slim["File"]

		# If the "Check" key is not inside the dictionary, show a space separator
		if "Check" not in self.dictionary:
			print()

		# Define the first text to show as the "Today is" text
		text = self.JSON.Language.language_texts["today_is"]

		# If the "Check" key is inside
		if "Check" in self.dictionary:
			# Define the first text to show as the "Skipped Diary Slim day" text
			text = self.language_texts["skipped_diary_slim_day"]

		# Define the "Date" and "Units" variables for easier typing
		date = self.dictionary["Date"]
		units = date["Timezone"]["DateTime"]["Units"]

		# Define the "Today is text" key with the day and date format text
		self.dictionary["Today is text"] = self.Date.language_texts["day, title()"].lower() + " " + date["Formats"]["[Day] [Month name] [Year]"][self.user_language]

		# Define the root "Today is text" that is going to be shown to the user
		self.today_is_text = text + ":" + "\n" + \
		"\t" + date["Timezone"]["DateTime"]["Texts"]["Day name"][self.user_language] + ", " + \
		self.dictionary["Today is text"] + " (" + date["Formats"]["DD/MM/YYYY"] + ")"

		# Show a five dash space separator
		print(self.separators["5"])
		print()

		# Show the today is text
		print(self.today_is_text)
		print()

		self.Define_Slim_File()

		if self.dictionary["Diary Slim exists"] == False:
			text = self.language_texts["creating_a_diary_slim_for_the_current_day"]

			if "Check" in self.dictionary:
				text = self.language_texts["creating_the_skipped_diary_slim"]

			print(text + "...")

		if (
			self.dictionary["Diary Slim exists"] == True and
			"Check" not in self.dictionary
		):
			print(self.File.language_texts["the_file_{}_opening_it"].format(self.File.language_texts["already_existed"]) + "...")

		if self.dictionary["Diary Slim exists"] == False:
			self.Make_Header()

		self.Write_To_Files()

		if self.dictionary["Diary Slim exists"] == False:
			# Reset all states to have no current order
			self.Update_State(new_order = "")

		if "Check" not in self.dictionary:
			print()
			print(self.separators["5"])

		if (
			"Checked" in self.dictionary and
			self.dictionary["Checked"] == True and
			"Skipped" in self.dictionary["Texts"]
		):
			print()

			# Show the "skipped Diary Slims" text
			print(self.dictionary["Texts"]["Skipped"])

			print(self.language_texts["they_were_created_by_the_program"] + ".")

	def Make_Header(self):
		# Define the units and texts dictionaries for easier typing
		units = self.dictionary["Date"]["Timezone"]["DateTime"]["Units"]
		texts = self.dictionary["Date"]["Timezone"]["DateTime"]["Texts"]

		# Define the "today is" template
		template = self.JSON.Language.language_texts["today_is"] + " {}."

		# Define the "today is" text with the day name
		item = texts["Day name"][self.user_language] + ", " + self.dictionary["Today is text"]

		# Format the template with the item
		self.dictionary["Today is"] = template.format(item)

		# Define the "Diary Slim" date template
		template = "- " + self.language_texts["diary_slim"] + ", {} -"

		# Define the item (Diary Slim day)
		item = self.current_diary_slim["Day"]

		# Format the template with the item
		self.dictionary["Text header"] = template.format(item)

		# Define the "type the time" text template
		type_text = self.JSON.Language.language_texts["type_the_time_that_you_{}"]

		# Ask for the time the user have gone to sleep
		type_text = type_text.format(self.JSON.Language.language_texts["have_gone_to_sleep"])

		self.dictionary["Sleeping time"] = self.Match_Time_Pattern(type_text)

		# Ask for the time the user woke up
		type_text = type_text.format(self.JSON.Language.language_texts["woke_up"])

		self.dictionary["Waking time"] = self.Match_Time_Pattern(type_text)

		print()

		# Format the header template
		self.dictionary["Header"] = self.diary_slim["Header"].format(self.dictionary["Sleeping time"], self.dictionary["Waking time"])

		if "Check" in self.dictionary:
			self.dictionary["Header"] = self.dictionary["Header"].splitlines()[0]

			self.dictionary["Header"] += "\n\n"

			self.dictionary["Header"] += self.language_texts["this_diary_slim_was_written"] + "."

	def Match_Time_Pattern(self, type_text, time = "", first_space = True):
		pattern = "^[0-9][0-9]:[0-9][0-9]$"

		format_text = " ({}: 00:00)"

		type_text += format_text.format(self.JSON.Language.language_texts["format"])

		format_text_helper = self.JSON.Language.language_texts["wrong_format_utilize_this_one"]

		import re

		if re.match(pattern, time) == None:
			i = 1
			while re.match(pattern, time) == None:
				formatted_text = format_text.format(format_text_helper)

				if (
					time != "" and
					formatted_text not in type_text
				):
					type_text += formatted_text

				if self.switches["testing"] == False:
					time = self.Input.Type(type_text, next_line = True, first_space = first_space)

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

				if (
					"Checked" in self.dictionary and
					self.date["Units"]["Day"] != 1
				):
					print()
					print(self.today_is_text)
					print()

	def Check_Diary_Slims(self):
		# Define today
		today_date = self.date

		self.dictionary["Today"] = self.Current_Diary_Slim(date = today_date, current_diary_slim = False)["Day"]

		# Define yesterday
		yesterday_date = self.Date.Now(self.date["Object"] - self.Date.Timedelta(days = 1))

		self.dictionary["Yesterday"] = self.Current_Diary_Slim(date = yesterday_date, current_diary_slim = False)["Day"]

		# Define the Diary Slims list for a more organized code
		diary_slims_list = list(self.current_month["Dictionary"]["Diary Slims"].keys())

		# If yesterday is not inside the Diary Slims list
		# Then the user skipped a Diary Slim
		if (
			self.dictionary["Yesterday"] not in diary_slims_list and
			self.date["Units"]["Month"] != 1
		):
			# Define the days list
			days_list = list(range(1, self.date["Units"]["Month days"] + 1))

			diary_slims_dictionary = {}

			# Iterate through the days list
			for day in days_list:
				# Define the date and day text
				units = self.dictionary["Date"]["Timezone"]["DateTime"]["Units"]

				date = self.Date.Now(self.Date.Date(year = int(units["Year"]), month = int(units["Month"]), day = day))

				day_text = self.Make_Diary_Slim_Dictionary(date = date)["Day"]

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
				# Define the number of skipped Diary Slims
				number = len(list(diary_slims_dictionary.keys()))

				# Define the singular or plural text
				texts = self.language_texts

				singular = texts["you_skipped_creating_this_diary_slim"]
				plural = texts["you_skipped_creating_these_diary_slims"]

				text = self.Text.By_Number(number, singular, plural)

				# Create the "skipped Diary Slims" text
				text = text + ":" + "\n"

				# Add the names of the skipped Diary Slims
				for day in diary_slims_dictionary:
					day = diary_slims_dictionary[day]

					text += "\t" + day["Day text"] + "\n"

				# Show the "skipped Diary Slims" text
				print(text)

				# Add the text to the root dictionary
				self.dictionary["Texts"]["Skipped"] = text

				if hasattr(self, "Create_New_Diary_Slim") == False:
					from Diary_Slim.Create_New_Diary_Slim import Create_New_Diary_Slim as Create_New_Diary_Slim

					self.Create_New_Diary_Slim = Create_New_Diary_Slim

				# Create the skipped Diary Slims
				for day in diary_slims_dictionary.values():
					dictionary = {
						"Date": day["Date"],
						"Check": True
					}

					# Create it using the "Create_New_Diary_Slim" sub-class
					self.object = self.Create_New_Diary_Slim(dictionary)

					# Update the local year and month variables here with the new variables from the object
					self.diary_slim["Current year"] = self.object.current_year
					self.current_month = self.object.current_month

					print()

				print(self.separators["5"])

			self.dictionary["Checked"] = True

	def Write_To_Files(self):
		from copy import deepcopy

		# Add the Diary Slim to the database
		if self.dictionary["Diary Slim exists"] == False:
			day = deepcopy(self.templates["Day"])

			units = self.dictionary["Date"]["Timezone"]["DateTime"]["Units"]
			texts = self.dictionary["Date"]["Timezone"]["DateTime"]["Texts"]

			# Define the creation time dictionary
			self.creation_time = {
				"HH:MM": self.dictionary["Date"]["Timezone"]["DateTime"]["Formats"]["HH:MM"],
				"Hours": units["Hour"],
				"Minutes": units["Minute"]
			}

			first_date = self.dictionary["Date"]["Timezone"]["DateTime"]["Formats"]["DD-MM-YYYY"]
			second_date = self.date["Timezone"]["DateTime"]["Formats"]["DD-MM-YYYY"]

			# If the "Checked" variable exists inside the root dictionary
			# And it is True
			# Or the date inside the root dictionary is not the same as the current date
			# Then it means that the creation of some Diary Slims were skipped
			if (
				"Checked" in self.dictionary and
				self.dictionary["Checked"] == True or
				first_date != second_date
			):
				# Define the type text
				type_text = self.language_texts["type_a_custom_creation_time_for_the_file, type: explanation"]

				# Ask for the user to type the time
				if self.switches["testing"] == False:
					typed = self.Input.Type(type_text, first_space = False, next_line = True)

				if self.switches["testing"] == True:
					typed = "10:00"

				# If the typed time is not empty (not Enter)
				if typed != "":
					# Check if the typed time is in the correct format
					typed = self.Match_Time_Pattern(type_text, time = typed)

					# Update the creation time dictionary
					self.creation_time["HH:MM"] = typed

					split = typed.split(":")

					self.creation_time["Hours"] = split[0]
					self.creation_time["Minutes"] = split[1]

			# Create the Day dictionary
			day = {
				"Day": units["Day"],
				"Names": texts["Day name"],
				"Formats": {
					"DD-MM-YYYY": self.dictionary["Date"]["Timezone"]["DateTime"]["Formats"]["DD-MM-YYYY"],
				},
				"Creation time": {
					"HH:MM": self.creation_time["HH:MM"],
					"Hours": self.creation_time["Hours"],
					"Minutes": self.creation_time["Minutes"]
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
			self.current_month["Dictionary"]["Diary Slims"][key] = day

			# Update the month "Diary Slims" number inside the Month dictionary
			self.current_month["Dictionary"]["Numbers"]["Diary Slims"] = len(list(self.current_month["Dictionary"]["Diary Slims"].keys()))

			# Edit the "Month.json" file with the new Month dictionary
			self.JSON.Edit(self.current_month["File"], self.current_month["Dictionary"])

			# ----- #

			# Edit the Year dictionary

			# Update the Month dictionary inside the Year dictionary
			self.diary_slim["Current year"]["Year"]["Months"][self.current_month["Name"]] = self.current_month["Dictionary"]

			# Update the "Months" number inside the Year dictionary
			self.diary_slim["Current year"]["Year"]["Numbers"]["Months"] = len(list(self.diary_slim["Current year"]["Year"]["Months"].keys()))

			# Update the Year "Diary Slims" number inside the Year dictionary
			self.diary_slim["Current year"]["Year"]["Numbers"]["Diary Slims"] = 0

			# Iterate through the Months list to add to the Year "Diary Slims" number
			for month in self.diary_slim["Current year"]["Year"]["Months"].values():
				self.diary_slim["Current year"]["Year"]["Numbers"]["Diary Slims"] += month["Numbers"]["Diary Slims"]

			# Edit the "Year.json" file with the new Year dictionary
			self.JSON.Edit(self.diary_slim["Current year"]["Folders"]["Year"], self.diary_slim["Current year"]["Year"])

		# ----- #

		# Write the header text into the Diary Slim
		if self.dictionary["Diary Slim exists"] == False:
			if "Check" in self.dictionary:
				print()

			print(self.separators["5"])

			if "Check" not in self.dictionary:
				print()

			# Get the file text
			self.current_day_file_text = self.File.Contents(self.dictionary["File"])["lines"]

			# Define the text to write
			text_to_write = self.dictionary["Text header"] + "\n\n" + \
			self.creation_time["HH:MM"] + " " + self.dictionary["Date"]["Timezone"]["DateTime"]["Formats"]["DD/MM/YYYY"] + ":" + "\n" + \
			self.dictionary["Today is"] + "\n\n" + \
			self.dictionary["Header"]

			# If the file is empty
			if self.current_day_file_text == []:
				verbose = None
				current_diary_slim = True

				if "Check" in self.dictionary:
					verbose = False
					current_diary_slim = False

				# Write the header text into the Diary Slim file
				Write_On_Diary_Slim_Module(text_to_write, custom_date = self.dictionary["Date"], add_time = False, check_file_length = False, current_diary_slim = current_diary_slim, verbose = verbose)

		# Open the current Diary Slim file
		self.System.Open(self.dictionary["File"])
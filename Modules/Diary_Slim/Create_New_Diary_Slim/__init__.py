# Create_New_Diary_Slim.py

from Diary_Slim.Diary_Slim import Diary_Slim as Diary_Slim

from Diary_Slim.Write_On_Diary_Slim_Module import Write_On_Diary_Slim_Module as Write_On_Diary_Slim_Module

class Create_New_Diary_Slim(Diary_Slim):
	def __init__(self, dictionary = {}):
		super().__init__()

		# Define the root dictionary
		self.dictionary = {
			"Dates": {
				"Now": self.Date.Now()
			},
			"Current Diary Slim": "",
			"File": "",
			"Texts": {},
			"Times": {}
		}

		# If the "Date" key is inside the parameter dictionary
		if "Date" in dictionary:
			# Update the "Now" date inside the "Dates" dictionary
			self.dictionary["Dates"]["Now"] = dictionary["Date"]

		# Define the current Diary Slim
		self.dictionary["Current Diary Slim"] = self.Current_Diary_Slim(date = self.dictionary["Dates"]["Now"], current_diary_slim = False)

		# Define the Diary Slim file
		self.dictionary["File"] = self.dictionary["Current Diary Slim"]["File"]

		# Define the "States" dictionary
		self.states = {
			"Diary Slim exists": False,
			"Skipped Diary Slims": {
				"Check": False,
				"Checked": False
			}
		}

		# If the "Check" key is inside the parameter dictionary
		if "Check" in dictionary:
			# Update the "Check for skipped Diary Slim" state inside the "States" dictionary
			self.states["Skipped Diary Slims"]["Check"] = dictionary["Check"]

		# Show information about the Diary Slim
		self.Show_Information()

		# Check if the Diary Slim file exists
		self.Check_For_File_Existence()

		# If the Diary Slim file does not exist
		if self.states["Diary Slim exists"] == False:
			# Define the "creating" text as the "Creating a Diary Slim for the current day" text
			self.dictionary["Texts"]["Creating"] = self.language_texts["creating_a_diary_slim_for_the_current_day"]

			# If the "Check for skipped Diary Slim" state is True
			if self.states["Skipped Diary Slims"]["Check"] == True:
				# Define the creating text as the "Creating the skipped Diary Slim" text
				self.dictionary["Texts"]["Creating"] = self.language_texts["creating_the_skipped_diary_slim"]

			# Show the text with three periods
			print(self.dictionary["Texts"]["Creating"] + "...")

		# If the Diary Slim file exists
		# And the "Check for skipped Diary Slim" state is False
		if (
			self.states["Diary Slim exists"] == True and
			self.states["Skipped Diary Slims"]["Check"] == False
		):
			# Show the text telling the user that the file was created and is going to be open
			print(self.File.language_texts["the_file_{}_opening_it"].format(self.File.language_texts["already_existed"]) + "...")

		# If the Diary Slim file does not exist
		if self.states["Diary Slim exists"] == False:
			# Create the Diary Slim header
			self.Create_Diary_Slim_Header()

		# Write to the files
		self.Write_To_Files()

		# If the "Check for skipped Diary Slim" state is False
		if self.states["Skipped Diary Slims"]["Check"] == False:
			# Show a space and a five dash space separator
			print()
			print(self.separators["5"])

		# If the "Checked for skipped Diary Slim" state is True
		# And the "Skipped Diary Slims" is inside the "Texts" dictionary
		if (
			self.states["Skipped Diary Slims"]["Checked"] == True and
			"Skipped Diary Slims" in self.dictionary["Texts"]
		):
			# Show a space separator
			print()

			# Show the "Skipped Diary Slims" text
			print(self.dictionary["Texts"]["Skipped Diary Slims"])

			# Show the information text telling the user that the skipped Diary Slims were created by the program (Create_New_Diary_Slim)
			print(self.language_texts["they_were_created_by_the_program"] + ".")

	def Show_Information(self):
		# If the "Check for skipped Diary Slim" state is False, show a space separator
		if self.states["Skipped Diary Slims"]["Check"] == False:
			print()

		# Define the information text
		self.dictionary["Texts"]["Information"] = self.JSON.Language.language_texts["today_is"]

		# If the "Check for skipped Diary Slim" state is True
		if self.states["Skipped Diary Slims"]["Check"] == True:
			# Define the information text as the "Skipped Diary Slim day" text
			self.dictionary["Texts"]["Information"] = self.language_texts["skipped_diary_slim_day"]

		# Define the "Date" and "Units" variables for easier typing
		date = self.dictionary["Dates"]["Now"]
		units = date["Timezone"]["DateTime"]["Units"]

		# Define the "Day" text with the day and date format text
		self.dictionary["Texts"]["Day"] = self.Date.language_texts["day, title()"].lower() + " " + date["Formats"]["[Day] [Month name] [Year]"][self.user_language]

		# Define the show text that is going to be shown to the user
		self.dictionary["Texts"]["Show"] = self.dictionary["Texts"]["Information"] + ":" + "\n" + \
		"\t" + date["Timezone"]["DateTime"]["Texts"]["Day name"][self.user_language] + ", " + \
		self.dictionary["Texts"]["Day"] + " (" + date["Formats"]["DD/MM/YYYY"] + ")"

		# Show a five dash space separator
		print(self.separators["5"])
		print()

		# Show the show text to the user
		print(self.dictionary["Texts"]["Show"])
		print()

	def Check_For_File_Existence(self):
		# If the Diary Slim file exists, change the state to True
		if self.File.Exist(self.dictionary["File"]) == True:
			self.states["Diary Slim exists"] = True

		# If the Diary Slim file does not exist
		if self.File.Exist(self.dictionary["File"]) == False:
			# Create the Diary Slim file
			self.File.Create(self.dictionary["File"])

			# If the "Check for skipped Diary Slim" state is False
			if self.states["Skipped Diary Slims"]["Check"] == False:
				# Check for skipped Diary Slims
				self.Check_For_Skipped_Diary_Slims()

			# If the "Check for skipped Diary Slim" state is True
			# And the day number is not the first one (of the month)
			if (
				self.states["Skipped Diary Slims"]["Check"] == True and
				self.date["Units"]["Day"] != 1
			):
				# Show spaces and the show text
				print()
				print(self.dictionary["Texts"]["Show"])
				print()

	def Check_For_Skipped_Diary_Slims(self):
		# Define the today variable for easier typing
		today_date = self.date

		# Get the Diary Slim day for today
		self.dictionary["Dates"]["Today"] = self.Current_Diary_Slim(date = today_date, current_diary_slim = False)["Day"]

		# Define the yesterday variable for easier typing
		yesterday_date = self.Date.Now(self.date["Object"] - self.Date.Timedelta(days = 1))

		# Get the Diary Slim day for yesterday
		self.dictionary["Yesterday"] = self.Current_Diary_Slim(date = yesterday_date, current_diary_slim = False)["Day"]

		# Define the Diary Slims list variable for a more organized code
		diary_slims_list = list(self.current_month["Dictionary"]["Diary Slims"].keys())

		# If yesterday is not inside the Diary Slims list
		# And the month is not the first of the year
		# Then the user skipped the creation of one Diary Slim or more
		if (
			self.dictionary["Yesterday"] not in diary_slims_list and
			self.date["Units"]["Month"] != 1
		):
			# Define the days list for easier typing
			days_list = list(range(1, self.date["Units"]["Month days"] + 1))

			# Create the empty "Skipped Diary Slims" dictionary
			self.dictionary["Skipped Diary Slims"] = {}

			# Iterate through the days list
			for day in days_list:
				# Define the "Units" and "Date" for easier typing
				units = self.dictionary["Dates"]["Now"]["Timezone"]["DateTime"]["Units"]

				date = self.Date.Now(self.Date.Date(year = int(units["Year"]), month = int(units["Month"]), day = day))

				# Get the day text
				day_text = self.Make_Diary_Slim_Dictionary(date = date)["Day"]

				# If the day text is not inside the Diary Slims list
				# And the day is lesser than the current day
				if (
					day_text not in diary_slims_list and
					day < int(units["Day"])
				):
					# Create the day dictionary with the day text and date
					# And add it to the "Skipped Diary Slims" dictionary
					self.dictionary["Skipped Diary Slims"][day_text] = {
						"Day text": day_text,
						"Date": date
					}

			# If the "Skipped Diary Slims" dictionary is not empty
			# Then create the skipped Diary Slims
			if self.dictionary["Skipped Diary Slims"] != {}:
				# Define the number of skipped Diary Slims
				number = len(list(self.dictionary["Skipped Diary Slims"].keys()))

				# Define the singular or plural text
				texts = self.language_texts

				singular = texts["you_skipped_creating_this_diary_slim"]
				plural = texts["you_skipped_creating_these_diary_slims"]

				# Define the "Skipped Diary Slims" text
				self.dictionary["Texts"]["Skipped Diary Slims"] = self.Text.By_Number(number, singular, plural) + ":" + "\n"

				# Add the names of the skipped Diary Slims
				for day in self.dictionary["Skipped Diary Slims"].values():
					self.dictionary["Texts"]["Skipped Diary Slims"] += "\t" + day["Day text"] + "\n"

				# Show the "Skipped Diary Slims" text
				print(self.dictionary["Texts"]["Skipped Diary Slims"])

				# If the "Create_New_Diary_Slim" object is not present inside the object of this class
				if hasattr(self, "Create_New_Diary_Slim") == False:
					# Import the class
					from Diary_Slim.Create_New_Diary_Slim import Create_New_Diary_Slim as Create_New_Diary_Slim

					# And define the object inside the class
					self.Create_New_Diary_Slim = Create_New_Diary_Slim

				# Create the skipped Diary Slims
				for day in self.dictionary["Skipped Diary Slims"].values():
					# Define the day dictionary with the date and check state
					dictionary = {
						"Date": day["Date"],
						"Check": True
					}

					# Create the skipped Diary Slim using the "Create_New_Diary_Slim" sub-class inside this object
					# Getting the object back
					self.object = self.Create_New_Diary_Slim(dictionary)

					# Update the local "Current year" dictionary and month variables in this class with the new variables from the local object
					self.diary_slim["Current year"] = self.object.current_year
					self.current_month = self.object.current_month

					# Show a space separator
					print()

				# Show a five dash space separator
				print(self.separators["5"])

			# Define the "Checked for skipped Diary Slims" state as True
			self.states["Skipped Diary Slims"]["Checked"] = True

	def Create_Diary_Slim_Header(self):
		# Define the units and texts variables for easier typing
		units = self.dictionary["Dates"]["Now"]["Timezone"]["DateTime"]["Units"]
		texts = self.dictionary["Dates"]["Now"]["Timezone"]["DateTime"]["Texts"]

		# Define the "Today is" text template
		template = self.JSON.Language.language_texts["today_is"] + " {}."

		# Define the item which is the day name and the root "Day" text
		item = texts["Day name"][self.user_language] + ", " + self.dictionary["Texts"]["Day"]

		# Format the template with the item, defining the "Today is" text
		self.dictionary["Texts"]["Today is"] = template.format(item)

		# Define the "Diary Slim" date text template
		template = "- " + self.language_texts["diary_slim"] + ", {} -"

		# Define the item (the Diary Slim day)
		item = self.dictionary["Current Diary Slim"]["Day"]

		# Format the template with the item
		self.dictionary["Texts"]["Diary Slim date text"] = template.format(item)

		# Define the "type the time that you" text template
		template = self.JSON.Language.language_texts["type_the_time_that_you_{}"]

		# Ask for the time the user have gone to sleep
		type_text = template.format(self.JSON.Language.language_texts["have_gone_to_sleep"])

		self.dictionary["Times"]["Sleeping"] = self.Match_Time_Pattern(type_text)

		# Ask for the time the user woke up
		type_text = template.format(self.JSON.Language.language_texts["woke_up"])

		self.dictionary["Times"]["Waking"] = self.Match_Time_Pattern(type_text)

		# Format the root header template, making the Diary Slim header
		self.dictionary["Texts"]["Header"] = self.diary_slim["Header template"].format(self.dictionary["Times"]["Sleeping"], self.dictionary["Times"]["Waking"])

		# If the "Check for skipped Diary Slim" state is True
		if self.states["Skipped Diary Slims"]["Check"] == True:
			# Split the lines of the text header
			self.dictionary["Texts"]["Header"] = self.dictionary["Texts"]["Header"].splitlines()[0]

			# Add two line breaks
			self.dictionary["Texts"]["Header"] += "\n\n"

			# Add a text explaining that the Diary Slim was written on the phone
			# (Assuming that the Diary Slim was written on the phone)
			self.dictionary["Texts"]["Header"] += self.language_texts["this_diary_slim_was_written_on_the_phone"] + "."

	def Match_Time_Pattern(self, type_text, time = "", first_space = True):
		# Define the pattern and format text
		pattern = "^[0-9][0-9]:[0-9][0-9]$"

		format_text = " ({}: 00:00)"

		# Format the format text with the "format" text
		type_text += format_text.format(self.JSON.Language.language_texts["format"])

		# Define the helper text variable for easier typing
		format_text_helper = self.JSON.Language.language_texts["wrong_format_utilize_this_one"]

		# Import the "Re" module
		import re

		# If the time is not in the correct format
		if re.match(pattern, time) == None:
			# Ask for the correct format from the user
			i = 1
			while re.match(pattern, time) == None:
				# Define the formatted text with the helper text
				formatted_text = format_text.format(format_text_helper)

				# If the time is not empty
				# And the formatted text is not in the tpye text
				if (
					time != "" and
					formatted_text not in type_text
				):
					# Add the formatted text
					type_text += formatted_text

				# If the "testing" switch is deactivated
				if self.switches["testing"] == False:
					# Ask for the time
					time = self.Input.Type(type_text, next_line = True, first_space = first_space)

				# If the "testing" switch is activated
				if self.switches["testing"] == True:
					# Define the time as "00:00"
					time = "00:00"

				i += 1

		# If the time is in the correct format
		if re.match(pattern, time) != None:
			# Return the time
			return time

	def Write_To_Files(self):
		from copy import deepcopy

		# If the Diary file Slim does not exist
		if self.states["Diary Slim exists"] == False:
			# ----- #

			# Define the "Creation time" dictionary

			# Define the day, units, and texts variables for easier typing
			day = deepcopy(self.templates["Day"])

			units = self.dictionary["Dates"]["Now"]["Timezone"]["DateTime"]["Units"]
			texts = self.dictionary["Dates"]["Now"]["Timezone"]["DateTime"]["Texts"]

			# Define the "Creation time" dictionary
			self.creation_time = {
				"HH:MM": self.dictionary["Dates"]["Now"]["Timezone"]["DateTime"]["Formats"]["HH:MM"],
				"Hours": units["Hour"],
				"Minutes": units["Minute"]
			}

			# Define the first and second date
			first_date = self.dictionary["Dates"]["Now"]["Timezone"]["DateTime"]["Formats"]["DD-MM-YYYY"]
			second_date = self.date["Timezone"]["DateTime"]["Formats"]["DD-MM-YYYY"]

			# If the "Checked for skipped Diary Slim" state is True
			# And the date inside the root dictionary is not the same as the current date
			# Then it means that the creation of some Diary Slims were skipped
			if (
				self.states["Skipped Diary Slims"]["Checked"] == True and
				first_date != second_date
			):
				# Define the type text for the custom creation time of the file
				type_text = self.language_texts["type_a_custom_creation_time_for_the_file, type: explanation"]

				# Ask for the user to type the time if the "testing" switch is deactivated
				if self.switches["testing"] == False:
					typed = self.Input.Type(type_text, first_space = False, next_line = True)

				# Else, define the time as "10:00"
				if self.switches["testing"] == True:
					typed = "10:00"

				# If the typed time is not empty (not Enter)
				if typed != "":
					# Check if the typed time is in the correct format
					typed = self.Match_Time_Pattern(type_text, time = typed)

					# If it is, them update the current "HH:MM" (hours and minutes) time inside the "Creation time" dictionary
					self.creation_time["HH:MM"] = typed

					# Split the time string
					split = typed.split(":")

					# And define the separate hours and minutes inside the "Creation time" dictionary
					self.creation_time["Hours"] = split[0]
					self.creation_time["Minutes"] = split[1]

			# ----- #

			# Define the "Day" dictionary and define the sleeping and waking times

			# Create the "Day" dictionary with its keys
			day = {
				"Day": units["Day"],
				"Names": texts["Day name"],
				"Formats": {
					"DD-MM-YYYY": self.dictionary["Dates"]["Now"]["Timezone"]["DateTime"]["Formats"]["DD-MM-YYYY"],
				},
				"Creation time": {
					"HH:MM": self.creation_time["HH:MM"],
					"Hours": self.creation_time["Hours"],
					"Minutes": self.creation_time["Minutes"]
				}
			}

			# Check if the sleep times items are inside the dictionary
			times = {
				"Sleeping": {
					"Key": "Slept"
				},
				"Waking": {
					"Key": "Woke up"
				}
			}

			i = 0
			for key, time in times.items():
				# If the key is inisde the dictionary
				if key in self.dictionary["Times"]:
					# Create the data dictionary if it does not exist
					if "Data" not in day:
						day["Data"] = {
							"Sleep times": {}
						}

					# Add the sleep time to the "Day" dictionary
					day["Data"]["Sleep times"][time["Key"]] = self.dictionary["Times"][key]

				i += 1

			# ----- #

			# Edit the "Month" dictionary

			# Define the key as the Diary Slim day name
			key = self.dictionary["Current Diary Slim"]["Day"]

			# Add the Day dictionary to the "Diary Slims" dictionary inside the "Month" dictionary
			self.current_month["Dictionary"]["Diary Slims"][key] = day

			# Update the month "Diary Slims" number inside the "Month" dictionary
			self.current_month["Dictionary"]["Numbers"]["Diary Slims"] = len(list(self.current_month["Dictionary"]["Diary Slims"].keys()))

			# Edit the "Month.json" file with the new "Month" dictionary
			self.JSON.Edit(self.current_month["File"], self.current_month["Dictionary"])

			# ----- #

			# Edit the "Year" dictionary

			# Update the "Month" dictionary inside the "Year" dictionary
			self.diary_slim["Current year"]["Year"]["Months"][self.current_month["Name"]] = self.current_month["Dictionary"]

			# Update the "Months" number inside the "Year" dictionary
			self.diary_slim["Current year"]["Year"]["Numbers"]["Months"] = len(list(self.diary_slim["Current year"]["Year"]["Months"].keys()))

			# Update the Year "Diary Slims" number inside the "Year" dictionary
			# (Reset it to zero first)
			self.diary_slim["Current year"]["Year"]["Numbers"]["Diary Slims"] = 0

			# Iterate through the months list to add to the Year "Diary Slims" number
			for month in self.diary_slim["Current year"]["Year"]["Months"].values():
				self.diary_slim["Current year"]["Year"]["Numbers"]["Diary Slims"] += month["Numbers"]["Diary Slims"]

			# Edit the "Year.json" file with the new "Year" dictionary
			self.JSON.Edit(self.diary_slim["Current year"]["Folders"]["Year"], self.diary_slim["Current year"]["Year"])

		# ----- #

		# If the Diary file Slim does not exist
		if self.states["Diary Slim exists"] == False:
			# Get the current day file text
			file_text = self.File.Contents(self.dictionary["File"])["lines"]

			# Define the text to write (the full Diary Slim header text)
			# With the Diary Slim date text
			# Hours, minutes, day, month, and year (full date and time)
			# The "Today is" text, showing the day name, number, month name, and year
			# And the formatted header text with the sleeping and waking time
			self.dictionary["Texts"]["To write"] = self.dictionary["Texts"]["Diary Slim date text"] + "\n\n" + \
			self.creation_time["HH:MM"] + " " + self.dictionary["Dates"]["Now"]["Timezone"]["DateTime"]["Formats"]["DD/MM/YYYY"] + ":" + "\n" + \
			self.dictionary["Texts"]["Today is"] + "\n\n" + \
			self.dictionary["Texts"]["Header"]

			# If the Diary Slim file is empty
			if file_text == []:
				# Define the verbose and current Diary Slim variables for easier typing
				verbose = True
				current_diary_slim = True

				# If the "Check for skipped Diary Slim" state is True
				if self.states["Skipped Diary Slims"]["Check"] == True:
					# Define the two variables above as False
					verbose = False
					current_diary_slim = False

				# Write the full Diary Slim header text into the Diary Slim file
				# With the text and the custom date
				# Without the time (it is already in the full text)
				# And with the two local "current Diary Slim" and "verbose" variables above
				dictionary = {
					"Text": self.dictionary["Texts"]["To write"],
					"Date": self.dictionary["Dates"]["Now"],
					"Add": {
						"Time": False
					},
					"Current_Diary_Slim": current_diary_slim,
					"Verbose": verbose
				}

				Write_On_Diary_Slim_Module(dictionary)

		# Open the current Diary Slim file
		self.System.Open(self.dictionary["File"], verbose = False)
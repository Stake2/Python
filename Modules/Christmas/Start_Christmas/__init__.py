# Start_Christmas.py

# Import the root class
from Christmas.Christmas import Christmas as Christmas

# Import some useful modules
from copy import deepcopy

class Start_Christmas(Christmas):
	def __init__(self):
		# Run the root class to import its methods and variables
		super().__init__()

		# Define the root "start Christmas" dictionary
		self.start_christmas = {
			"Dates": {
				"Today": self.date
			},
			"Steps": {},
			"Finish text": ""
		}

		# Define the root states dictionary
		self.states = {
			"Current month is December": False,
			"Today is Christmas": False,
			"Today is in the first step date range": False,
			"Completed non Christmas day steps": False, 
			"Today is a chosen Christmas day": False
		}

		# ---------- #

		# Define the Christmas "Steps" dictionary
		self.Define_Christmas_Steps()

		# Check the step dates
		self.Check_Step_Dates()

		# If today is in the date range of the first Christmas step
		# And the "Completed non Christmas day steps" state is False
		# (The user did not complete all of the Christmas steps that are not done on the Christmas day)
		# Or today is a chosen Christmas day (days 24 or 25)
		if (
			self.states["Today is in the first step date range"] == True and
			self.states["Completed non Christmas day steps"] == False or
			self.states["Today is a chosen Christmas day"] == True
		):
			# Execute the Christmas steps
			self.Execute_Christmas_Steps()

	def Define_Christmas_Steps(self):
		# Define the root "Steps" dictionary
		self.start_christmas["Steps"] = {
			"Numbers": {
				"Total": 0
			},
			"List": [],
			"Dictionary": {},
			"Date ranges": {},
			"Categories": {
				"Non-Christmas day": {
					"Number": 0,
					"List": []
				},
				"Christmas day": {
					"Number": 0,
					"List": []
				}
			},
			"Completed": {
				"Non-Christmas day": [],
				"Christmas day": []
			}
		}

		# Read the root Christmas "Steps" file to get its JSON dictionary
		self.start_christmas["Steps (JSON)"] = self.JSON.To_Python(self.christmas["Files"]["Steps"])

		# List the keys inside the "Steps (JSON)" dictionary
		keys = list(self.start_christmas["Steps (JSON)"].keys())

		# Define the list of keys as the root "List
		self.start_christmas["Steps"]["List"] = keys

		# Update the total number of steps to be the number of keys
		self.start_christmas["Steps"]["Numbers"]["Total"] = len(keys)

		# Define the local step number
		step_number = 1

		# Define a list of keys to import
		keys_to_import = [
			"Texts",
			"Methods",
			"Values",
			"Input text",
			"Date ranges",
			"Completed",
			"Christmas-day step",
			"Ask to make a pause"
		]

		# Define a local "JSON verbose" switch
		json_verbose = False

		# Iterate through the root step keys and dictionaries inside the "Steps (JSON)" dictionary
		for step_key, root_step in self.start_christmas["Steps (JSON)"].items():
			# Create the local new step dictionary
			step = {
				"Number": step_number,
				"Key": step_key,
				"Texts": {},
				"Text": {},
				"Input text": "",
				"Methods": {},
				"Values": {},
				"Date ranges": {},
				"States": {
					"Ask for input": True,
					"Has methods": False,
					"First space": True
				},
				"Completed": False,
				"Christmas-day step": True,
				"Ask to make a pause": False
			}

			# ---------- #

			# Iterate through the list of keys to import
			for key in keys_to_import:
				# If the key is inside the root step dictionary
				if key in root_step:
					# If the key is not "Methods"
					if key != "Methods":
						# Add it to the local step dictionary
						step[key] = root_step[key]

					# If the key is "Methods"
					if key == "Methods":
						# Update the "Methods" dictionary to contain the "Numbers" dictionary, the "List" of step methods, and the empty "Dictionary"
						step[key] = {
							"Numbers": {
								"Total": len(root_step[key])
							},
							"List": root_step[key],
							"Dictionary": {}
						}

					# Make a copy of the value
					step[key] = deepcopy(step[key])

				# Else, if the key is not inside the defined list
				elif key not in ["Completed", "Christmas-day step"]:
					# Remoev the key from the local step dictionary
					step.pop(key)

			# ---------- #

			# If the "Date ranges" key is not inside the step dictionary
			if "Date ranges" not in step:
				# Define the "Date ranges" list as the 24 and 25 days of December
				step["Date ranges"] = [
					"24/12/{current_year}",
					"25/12/{current_year}"
				]

			# Iterate through the date numbers and strings inside the list of "Date ranges"
			for date_number, date_string in enumerate(step["Date ranges"]):
				# Replace the "{current_year}" format string with the current year number inside the date string
				date_string = self.Years.Replace_Year_Format_Strings(date_string)

				# Define the date dictionary using the date string
				date = self.Date.From_String(date_string, format = "%d/%m/%Y")

				# Update the date inside the "Date ranges" list
				step["Date ranges"][date_number] = date

			# Add the date range of the step dictionary to the root "Date ranges" dictionary
			self.Define_Date_Range(step)

			# ---------- #

			# Define the step "Text" key as the step text in the user language
			step["Text"] = step["Texts"][self.language["Small"]]

			# Create a shortcut to the "[Current year]" text
			current_year_text = "[" + self.Language.language_texts["current_year"] + "]"

			# If the "[Current year]" text is inside the step text
			if current_year_text in step["Text"]:
				# Replace the "[Current year]" text with the actual current year number
				step["Text"] = step["Text"].replace(current_year_text, str(self.date["Units"]["Year"]))

			# ---------- #

			# If the "Methods" key is inside the step dictionary
			if "Methods" in step:
				# Change the step "Has methods" state to True
				step["States"]["Has methods"] = True

				# Define a local method number
				method_number = 1

				# Iterate through the list of step method names
				for method_name in step["Methods"]["List"]:
					# If the method name is inside the list of methods to not ask for input
					if method_name in self.christmas["Methods"]["Do not ask for input"]:
						# Change the step "Ask for input" state to False
						step["States"]["Ask for input"] = False

					# Create the local method dictionary
					method = {
						"Number": method_number,
						"Name": method_name,
						"Object": self.christmas["Methods"]["Dictionary"][method_name]
					}

					# If both the "Testing" and "Verbose" switches are True
					# And the local "JSON verbose" switch is True
					if (
						self.switches["Testing"] == True and
						self.switches["Verbose"] == True and
						json_verbose == True
					):
						# Convert the method "Object" into a string
						method["Object"] = str(method["Object"])

					# If the "Values" key is inside the step dictionary
					if "Values" in step:
						# If the "Values" key is a list
						if type(step["Values"]) == list:
							# Get the value of the method using the method number less one as an index
							method["Value"] = step["Values"][method_number - 1]

						# If the "Values" key is a dictionary
						if type(step["Values"]) == dict:
							# Define the method value initially as the "Values" dictionary
							method["Value"] = step["Values"]

							# If the number of methods is more than one
							if len(step["Methods"]["List"]) > 1:
								# If the method name is inside the "Values" dictionary
								if method_name in step["Values"]:
									# Get the value of the method using the method name as a key
									method["Value"] = step["Values"][method_name]

								# Else, remove the "Value" key
								else:
									method.pop("Value")

					# Add the method dictionary to the methods "Dictionary"
					step["Methods"]["Dictionary"][method_name] = method

					# Add one to the local method number
					method_number += 1

				# If the "Values" key is inside the step dictionary, remove it
				if "Values" in step:
					step.pop("Values")

			# ---------- #

			# Define the category key initially as "Christmas day"
			category_key = "Christmas day"

			# If the "Christmas-day step" is False
			if step["Christmas-day step"] == False:
				# Change the category key to "Non-Christmas day"
				category_key = "Non-Christmas day"

			# Get the category dictionary
			category = self.start_christmas["Steps"]["Categories"][category_key]

			# Add one to the number of category steps
			category["Number"] += 1

			# Add the step key to the category list
			category["List"].append(step_key)

			# If the "Completed" key is True (the step was completed)
			if step["Completed"] == True:
				# Get the completed list
				completed = self.start_christmas["Steps"]["Completed"][category_key]

				# Add the step key to the completed list
				completed.append(step_key)

			# ---------- #

			# If the "Christmas-day step" key is not present in the root step dictionary
			if "Christmas-day step" not in root_step:
				# Define it as True
				root_step["Christmas-day step"] = True

			# If the "Completed" key is not present in the root step dictionary
			if "Completed" not in root_step:
				# Define it as False
				root_step["Completed"] = False

			# Update the root step dictionary to reflect this change
			self.start_christmas["Steps (JSON)"][step_key] = root_step

			# Add the local step dictionary to the root "Steps" dictionary
			self.start_christmas["Steps"]["Dictionary"][step_key] = step

			# ---------- #

			# Add one to the local step number
			step_number += 1

		# Update the root "Steps.json" file with the updated "Steps (JSON)" dictionary
		self.JSON.Edit(self.christmas["Files"]["Steps"], self.start_christmas["Steps (JSON)"])	

	def Update_Steps(self, step_to_complete = None, reset = True):
		# Iterate through the step keys and dictionaries inside the "Steps" dictionary
		for step_key, step in self.start_christmas["Steps"]["Dictionary"].items():
			# Get the root step dictionary
			root_step = self.start_christmas["Steps (JSON)"][step_key]

			# Update the step dictionary in the root "Steps" dictionary
			self.start_christmas["Steps"]["Dictionary"][step_key] = step

			# Define the new value initially as False
			new_value = False

			# Define the local update switch initially as False
			update = False

			# If the "reset" parameter is True
			if reset == True:
				# Change the local update switch to True
				update = True

			# If the "reset" parameter is False
			# And the "step to complete" parameter is not None
			# And the current step is the same as the step to complete
			if (
				reset == False and
				step_to_complete != None and
				step_key == step_to_complete
			):
				# Change the new value to True
				new_value = True

				# Change the local update switch to True
				update = True

			# If the local update switch is True
			if update == True:
				# Change the "Completed" step state to the new value in the current step dictionary
				step["Completed"] = new_value

				# Also change the "Completed" step state to the new value in the root step dictionary
				root_step["Completed"] = new_value

			# Update the root step dictionary to reflect the reset
			self.start_christmas["Steps (JSON)"][step_key] = root_step

		# Update the root "Steps.json" file with the updated "Steps (JSON)" dictionary
		self.JSON.Edit(self.christmas["Files"]["Steps"], self.start_christmas["Steps (JSON)"])

	def Define_Date_Range(self, step):
		# Get the first date from the step "Date ranges" list
		first_date = step["Date ranges"][0]

		# Define the start and end dates as the first date
		start_date = first_date
		end_date = first_date

		# Iterate through the list of dates
		for date in step["Date ranges"]:
			# Get the day of the current date
			day = date["Units"]["Day"]

			# If the current day is earlier than the day of the start date
			if day < start_date["Units"]["Day"]:
				# Update the start date to be the current date
				start_date = date

			# If the current day is later than the end date
			if day > end_date["Units"]["Day"]:
				# Update the end date to be the current date
				end_date = date

		# If the start date is not equal to the end date
		if start_date != end_date:
			# Define the text template as "Between the days {} and {}"
			text_template = "Between the days {} and {}"

			# Format the text template with the start and end days to create the range key
			range_key = text_template.format(start_date["Units"]["Day"], end_date["Units"]["Day"])

		else:
			# Define the text template as only "Day {}"
			text_template = "Day {}"

			# Format the text template with the first day
			range_key = text_template.format(first_date["Units"]["Day"])

		# If the date range dictionary is not present inside the root "Date ranges" dictionary
		if range_key not in self.start_christmas["Steps"]["Date ranges"]:
			# Create it
			self.start_christmas["Steps"]["Date ranges"][range_key] = {
				"List": step["Date ranges"],
				"Steps": {}
			}

		# Add the current step dictionary to the date range "Steps" dictionary
		self.start_christmas["Steps"]["Date ranges"][range_key]["Steps"][step["Key"]] = step

	def Define_List_Of_Days(self, dates):
		# Define the empty list of days
		days = []

		# Iterate through the dates inside the first step date range
		for date in dates:
			# Get the day
			day = date["Units"]["Day"]

			# Add it to the list of days
			days.append(day)

		# Create a range of days from the first day to the last day
		days = list(range(days[0], days[-1] + 1))

		# Return the list of days
		return days

	def Check_Step_Dates(self):
		# If the "Testing" switch is True
		if self.switches["Testing"] == True:
			# Define today as "30 of November"
			#self.start_christmas["Dates"]["Today"] = self.Date.Now(self.date["Object"].replace(day = 30, month = 11))

			# Define today as "19 of December"
			#self.start_christmas["Dates"]["Today"] = self.Date.Now(self.date["Object"].replace(day = 19))

			# Define today as "20 of December"
			#self.start_christmas["Dates"]["Today"] = self.Date.Now(self.date["Object"].replace(day = 20))

			# Define today as "24 of December"
			self.start_christmas["Dates"]["Today"] = self.Date.Now(self.date["Object"].replace(day = 24))

			# Change the "Completed non Christmas day steps" to True
			self.states["Completed non Christmas day steps"] = True

		# Create a shortcut to the today date
		today = self.start_christmas["Dates"]["Today"]

		# Check if today is Christmas and update the "Today is Christmas" state with the returned boolean
		# Checking if today is either 24 or 25 of December (days = [24, 25])
		self.states["Today is Christmas"] = self.Today_Is_Day(days = [24, 25], today = today)

		# ---------- #

		# Check if the current month is December and update the "Current month is December" state with the returned boolean
		self.states["Current month is December"] = self.Current_Month_Is_December(today = today)

		# If the current month is not December
		if self.states["Current month is December"] == False:
			# Reset the "Completed" state of the step dictionaries
			self.Update_Steps()

		# ---------- #

		# List the date range dictionaries
		date_ranges = list(self.start_christmas["Steps"]["Date ranges"].values())

		# Get the first step date range
		first_step_date_range = date_ranges[0]

		# Get the first step date inside the date range
		first_step_date = first_step_date_range["List"][0]

		# Define the "Date of the first step" date key as the first step date
		self.start_christmas["Dates"]["Date of the first step"] = first_step_date

		# Define the list of days based on the list of dates
		days = self.Define_List_Of_Days(first_step_date_range["List"])

		# Check if the current day is within the first step date range and update the "Today is in the first step date range" state with the returned boolean
		self.states["Today is in the first step date range"] = self.Today_Is_Day(days = days, today = today)

		# ----- #

		# Define the category key as "Non-Christmas day"
		category_key = "Non-Christmas day"

		# Get the category dictionary
		category = self.start_christmas["Steps"]["Categories"][category_key]

		# Get the completed list
		completed = self.start_christmas["Steps"]["Completed"][category_key]

		# If the number of category steps is the same as the number of steps in the completed list
		if category["Number"] == len(completed):
			# Then change the "Completed non Christmas day steps" to True
			self.states["Completed non Christmas day steps"] = True

		# ----- #

		# Iterate through the date ranges
		for date_range in date_ranges:
			# Get the list of dates
			dates = date_range["List"]

			# Create a shortcut to the end date
			end_date = dates[-1]

			# If the end date is "25 of December"
			# And the user completed all of the Christmas steps that are not done on the Christmas day
			if (
				end_date["Units"]["Day"] == 25 and
				self.states["Completed non Christmas day steps"] == True
			):
				# Define the list of days based on the list of dates
				days = self.Define_List_Of_Days(dates)

				# Check if the current day is inside the list of days and update the "Today is a chosen Christmas day" state with the returned boolean
				self.states["Today is a chosen Christmas day"] = self.Today_Is_Day(days = days, today = today)

		# ---------- #

		# Show a five dash space separator
		print()
		print(self.separators["5"])
		print()

		# Define the date format to use
		date_format = "[Day] [Month name] [Year] ([Day name])"

		# Get the current date text in the defined date format
		self.start_christmas["Dates"]["Today date text"] = today["Formats"][date_format][self.language["Small"]]

		# Show the "Today is" text in the user language
		print(self.Language.language_texts["today_is"] + ":")

		# Show the current date text in the defined date format
		print("\t" + self.start_christmas["Dates"]["Today date text"])
		print()

		# ---------- #

		# Define the show text initially as an empty string
		show_text = ""

		# Define the local "calculate remaining time" switch initially as False
		calculate_remaining_time = False

		# ---------- #

		# If the current month is not December
		# Or today is not in the date range of the first Christmas step
		if (
			self.states["Current month is December"] == False or
			self.states["Today is in the first step date range"] == False
		):
			# Define the end date as the date of the first step
			end_date = self.start_christmas["Dates"]["Date of the first step"]

			# Define the show text as "Today is not the day of the first step"
			show_text = self.language_texts["today_is_not_the_day_of_the_first_christmas_step"]

			# Change the local "calculate remaining time" switch to True
			calculate_remaining_time = True

		# ---------- #

		# If today is in the date range of the first Christmas step
		# And the "Completed non Christmas day steps" state is False
		# (The user did not complete all of the Christmas steps that are not done on the Christmas day)
		if (
			self.states["Today is in the first step date range"] == True and
			self.states["Completed non Christmas day steps"] == False
		):
			# Define the show text as "Executing the Christmas steps that are not done on Christmas-dedicated days"
			show_text = self.language_texts["executing_the_christmas_steps_that_are_not_done_on_christmas_dedicated_days"] + "..."

			# Define the root "Finish text" as "You finished completing the Christmas steps that are not done on Christmas-dedicated days"
			self.start_christmas["Finish text"] = self.language_texts["you_finished_completing_the_christmas_steps, type: long"] + "."

			# Add two line breaks to the "Finish text"
			self.start_christmas["Finish text"] += "\n\n"

			# Add the "Today is" text in the user language and a line break
			self.start_christmas["Finish text"] += self.Language.language_texts["today_is"] + ":" + "\n"

			# Add the current date text in the defined date format and a line break
			self.start_christmas["Finish text"] += "\t" + self.start_christmas["Dates"]["Today date text"] + "\n"

			# Add one line breaks to the "Finish text"
			self.start_christmas["Finish text"] += "\n"

			# Add the "Come back when it is" text
			self.start_christmas["Finish text"] += self.Language.language_texts["come_back_when_it_is"] + " "

			# Get the step key of the first Christmas-day step
			step_key = self.start_christmas["Steps"]["Categories"]["Christmas day"]["List"][0]

			# Get the step dictionary
			step = self.start_christmas["Steps"]["Dictionary"][step_key]

			# Create a shortcut to the list of date ranges
			date_ranges = step["Date ranges"]

			# Get the start date
			start_date = date_ranges[0]

			# Get the end date
			end_date = date_ranges[-1]

			# Define the date range text template as the "day {} of {}" text template of the "Date" utility class
			text_template = self.Date.language_texts["day_{}_of_{}"]

			# Define the list of items to use to format the date range text template
			items = [
				# The day of the end date
				end_date["Units"]["Day"],

				# The month name in the user language
				end_date["Texts"]["Month name"][self.language["Small"]]
			]

			# If the number of date ranges is more than one
			if len(date_ranges) > 1:
				# Change the date range text template to the "Between the days {} and {} of {}" text template of the "Date" utility class
				text_template = self.Date.language_texts["between_the_days_{}_and_{}_of_{}"].lower()

				# Add the start date to the list of items
				items.insert(0, start_date["Units"]["Day"])

			# Format the date range text template with the list of items to create the date range text
			date_range_text = text_template.format(*items)

			# Add the date range text
			self.start_christmas["Finish text"] += date_range_text + "."

		# ---------- #

		# If the "Completed non Christmas day steps" state is True
		# (The user completed all of the Christmas steps that are not done on the Christmas day)
		# And today is not a chosen Christmas day (not day 24 or 25)
		if (
			self.states["Completed non Christmas day steps"] == True and
			self.states["Today is a chosen Christmas day"] == False
		):
			# Define the end date as "24 of December" date
			end_date = self.christmas["Dates"]["24 of December"]

			# Define the show text as "You completed all the Christmas steps that are not for the actual Christmas days, and today is not a day chosen to celebrate Christmas"
			show_text = self.language_texts["you_completed_all_the_christmas_steps_that_are_not_for_the_for_the_actual_christmas, type: long"]

			# Change the local "calculate remaining time" switch to True
			calculate_remaining_time = True

		# ---------- #

		# If today is a chosen Christmas day (days 24 or 25)
		if self.states["Today is a chosen Christmas day"] == True:
			# Define the text template as "Starting Christmas day for the year of {}"
			text_template = self.language_texts["starting_christmas_day_for_the_year_of_{}"]

			# Format the text template with the current year number to create the show text
			show_text = text_template.format(self.date["Units"]["Year"]) + "..."

			# Define the text template as "Your Christmas of {} is finished, congratulations!"
			text_template = self.language_texts["your_christmas_of_{}_is_finished_congratulations"]

			# Format the text template with the current year number to create the finish text
			self.start_christmas["Finish text"] = text_template.format(self.date["Units"]["Year"])

		# ---------- #

		# If the show text is not an empty string
		if show_text != "":
			# Show the "Status of the Christmas steps" text in the user language and the show text with a tab
			print(self.language_texts["status_of_the_christmas_steps"] + ":")
			print("\t" + show_text)

			# If the local "calculate remaining time" switch is True
			if calculate_remaining_time == True:
				# Show the "Today is not the Christmas day, wait until" text in the user language
				print()
				print(self.Language.language_texts["wait_until"] + ":")

				# Get the end date text in the defined date format
				date_text = end_date["Formats"][date_format][self.language["Small"]]

				# Show the Christmas date text
				print("\t" + date_text)

				# Then calculate the remaining time and show it
				self.Calculate_Remaining_Time(today, end_date)

	def Calculate_Remaining_Time(self, today, end_date):
		# Create a shortcut to the units of the current date
		current_date_units = today["Units"]

		# Create a shortcut to the units of the end date
		end_date_units = end_date["Units"]

		# ---------- #

		# Define a dictionary to store the remaining time until Christmas
		time_left = {}

		# Calculate the difference in years from the current year to the end year
		years_left = (current_date_units["Year"] - end_date_units["Year"])

		# Calculate the difference in months from the current month to the Christmas month
		months_left = (current_date_units["Month"] - end_date_units["Month"])

		# Convert the years left to months (years left times 12) and add the months left
		time_left["Months"] = years_left * 12 + months_left

		# Calculate the absolute difference in days from the current date to Christmas
		days_left = abs((today["Object"] - end_date["Object"]).days)

		# Calculate the total number of days left in the current month,
		# by multiplying the months left until Christmas by the number of days in the current month
		month_days_left = time_left["Months"] * self.Date.Monthrange(current_date_units["Year"], current_date_units["Month"])[1]

		# Define the number of days left
		time_left["Days"] = days_left - abs(month_days_left)

		# Get the absolute value of each time
		for key in time_left:
			time_left[key] = abs(time_left[key])

		# ---------- #

		# Create a shortcut to the language texts dictionary of the "Date" class
		texts_dictionary = self.Date.language_texts

		# Iterate through the items and times inside the time left
		for item, time in time_left.items():
			# Define the plural text key
			plural_text_key = item.lower()

			# Define the singular text key (by removing the "s" letter from the end)
			singular_text_key = plural_text_key[:-1]

			# If the time is not zero
			if time != 0:
				# Define the list of items
				items = [
					time,
					texts_dictionary[singular_text_key + "_left"],
					texts_dictionary[plural_text_key + "_left"]
				]

				# Define the singular or plural time text based on the time
				time_text = self.Text.By_Number(*items)

				# Show the time text and the time left
				print()
				print(time_text + ":")
				print("\t" + str(time) + " " + time_text.lower())

	def Execute_Christmas_Steps(self):
		# Show a three dash space separator
		print()
		print(self.separators["3"])

		# ---------- #

		# If today is in the date range of the first Christmas step
		# And the "Completed non Christmas day steps" state is False
		# (The user did not complete all of the Christmas steps that are not done on the Christmas day)
		if (
			self.states["Today is in the first step date range"] == True and
			self.states["Completed non Christmas day steps"] == False
		):
			# Define the category key as "Non-Christmas day"
			category_key = "Non-Christmas day"

		# If today is a chosen Christmas day (days 24 or 25)
		if self.states["Today is a chosen Christmas day"] == True:
			# Define the category key as "Christmas day"
			category_key = "Christmas day"

		# Define the list of steps as the list of [category key] steps
		steps = self.start_christmas["Steps"]["Categories"][category_key]["List"]

		# Iterate through the Christmas step keys inside the local list of steps
		for step_key in steps.copy():
			# Get the Christmas step dictionary
			step = self.start_christmas["Steps"]["Dictionary"][step_key]

			# If the step has been completed
			if step["Completed"] == True:
				# Remove the step from the local list of steps
				steps.remove(step_key)

		# Get the total number of steps in the local list of steps
		total_steps_number = len(steps)

		# Define the local last date range text as an empty string
		last_date_range_text = ""

		# Iterate through the Christmas step numbers and keys inside the local list of steps
		for step_number, step_key in enumerate(steps, start = 1):
			# Get the Christmas step dictionary
			step = self.start_christmas["Steps"]["Dictionary"][step_key]

			# ---------- #

			# Show the current and total Christmas step numbers
			print()
			print(self.Language.language_texts["christmas_step"] + ":")
			print("\t" + "[" + str(step_number) + "/" + str(total_steps_number) + "]")

			# Show the Christmas step text
			print()
			print(self.Language.language_texts["christmas_step_text"] + ":")
			print("\t" + step["Text"])

			# ---------- #

			# Create a shortcut to the list of date ranges
			date_ranges = step["Date ranges"]

			# Get the start date
			start_date = date_ranges[0]

			# Get the end date
			end_date = date_ranges[-1]

			# Define the text to show as "Day to complete the Christmas step"
			text_to_show = self.language_texts["day_to_complete_the_christmas_step"]

			# Define the date range text template as the "At the day {} of {}" text template of the "Date" utility class
			text_template = self.Date.language_texts["at_the_day_{}_of_{}"]

			# Define the list of items to use to format the date range text template
			items = [
				# The day of the end date
				end_date["Units"]["Day"],

				# The month name in the user language
				end_date["Texts"]["Month name"][self.language["Small"]]
			]

			# If the number of date ranges is more than one
			if len(date_ranges) > 1:
				# Define the text to show as "Interval of days to complete the Christmas step"
				text_to_show = self.language_texts["interval_of_days_to_complete_the_christmas_step"]

				# Change the date range text template to the "Between the days {} and {} of {}" text template of the "Date" utility class
				text_template = self.Date.language_texts["between_the_days_{}_and_{}_of_{}"]

				# Add the start date to the list of items
				items.insert(0, start_date["Units"]["Day"])

			# Format the date range text template with the list of items to create the date range text
			date_range_text = text_template.format(*items)

			# If the current date range text is not the same as the last one
			if date_range_text != last_date_range_text:
				# Show the "Today is" text in the user language
				print()
				print(self.Language.language_texts["today_is"] + ":")

				# Define the date format to use
				date_format = "[Day] [Month name] [Year]"

				# Get the current date text in the defined date format
				date_text = self.start_christmas["Dates"]["Today"]["Formats"][date_format][self.language["Small"]]

				# Show the current date text in the defined date format
				print("\t" + date_text)

				# Show the text to show
				print()
				print(text_to_show + ":")

				# Show the date range text
				print("\t" + date_range_text)

			# Update the local last date range text
			last_date_range_text = date_range_text

			# ---------- #

			# If the Christmas step has a "Methods" dictionary
			if step["States"]["Has methods"] == True:
				# Iterate through the method names and dictionaries inside the Christmas step methods "Dictionary"
				for method_name, method in step["Methods"]["Dictionary"].items():
					# Show a space separator before each method
					print()

					# If the method dictionary has a "Value" 
					if "Value" in method:
						# Run the method with the value
						method["Object"](method["Value"])

					# Else, run the method without the value
					else:
						method["Object"]()

			# ---------- #

			# If the "Ask for input" step state is True
			# And the step is not the last one
			# Or the "Input text" key is inside the step dictionary
			if (
				step["States"]["Ask for input"] == True and
				step_number != total_steps_number or
				"Input text" in step
			):
				# Define the input text as the "Continue" text in the user language
				input_text = self.Language.language_texts["continue, title()"]

				# If the "Input text" is inside the Christmas step dictionary
				if "Input text" in step:
					# Define the input text as the text inside that key and in the user language
					input_text = step["Input text"][self.language["Small"]]

				# Ask for user input before continuing to the next Christmas step
				self.Input.Type(input_text, first_space = step["States"]["First space"])

			# ---------- #

			# After the Christmas step was completed, define it as completed inside the root "Steps" dictionary
			self.Update_Steps(step_to_complete = step_key, reset = False)

			# ---------- #

			# If the "Ask to make a pause" key is inside the Christmas step dictionary
			if "Ask to make a pause" in step:
				# Show a five dash space separator
				print()
				print(self.separators["5"])

				# Define the question as "Do you want to make a pause and continue later?"
				question = self.language_texts["do_you_want_to_make_a_pause_and_continue_later"]

				# Ask the user if they want to make a pause
				make_a_pause = self.Input.Yes_Or_No(question)

				# If the user wants to make a pause
				if make_a_pause == True:
					# Define the text template as the "day {} of {}" text template of the "Date" utility class
					text_template = self.Date.language_texts["day_{}_of_{}"]

					# Define the list of items to use to format the date range text template
					items = [
						# The day of the end date
						end_date["Units"]["Day"],

						# The month name in the user language
						end_date["Texts"]["Month name"][self.language["Small"]]
					]

					# Format the text template with the list of items to create the date text
					date_text = text_template.format(*items)

					# Define the text template as "Come back when you want to continue completing the Christmas steps for the {}!"
					text_template = self.language_texts["come_back_when_you_want_to_continue_completing_the_christmas_steps, type: long"]

					# Format the new text template with the date text
					text = text_template.format(date_text)

					# Update the root "Finish text"
					self.start_christmas["Finish text"] = text

					# End the loop here
					break

			# ---------- #

			# Show a five dash space separator
			print()
			print(self.separators["5"])

		# Show the root "Finish text"
		print()
		print(self.start_christmas["Finish text"])
# Start_Christmas.py

# Import the root class
from Christmas.Christmas import Christmas as Christmas

# Import some useful modules
from copy import deepcopy

class Start_Christmas(Christmas):
	def __init__(self):
		# Run the root class to import its methods and variables
		super().__init__()

		# Define the "start Christmas" dictionary
		self.start_christmas = {
			"Steps": {
				"List": [],
				"Dictionary": {}
			},
			"States": {
				"Today is Christmas": False
			},
			"Dictionaries": {}
		}

		# Iterate through the list of defined keys
		for key in ["Planning", "Objects"]:
			# Get the text file from the root "Christmas" dictionary
			text_file = self.christmas["Files"][key]

			# If the key is "Planning"
			if key == "Planning":
				# Get the "Planning" from the file using the "Dictionary" method of the "File" utility class
				dictionary = self.File.Dictionary(text_file, next_line = True)

			# If the key is "Objects"
			if key == "Objects":
				# Get the "Objects" dictionary "To_Python" method of the "JSON" utility class
				dictionary = self.JSON.To_Python(text_file)

			# Add the local dictionary to the "Dictionaries" dictionary
			self.start_christmas["Dictionaries"][key] = dictionary

		# Check if today is the Christmas day
		self.Check_For_Christmas_Day()

		# Show a ten dash space separator at the end
		print()
		print(self.separators["10"])

	def Check_For_Christmas_Day(self):
		# Show a five dash space separator
		print()
		print(self.separators["5"])
		print()

		# If the "Testing" switch is True
		if self.switches["Testing"] == True:
			# Define today as "24 of December" for testing purposes
			self.date = self.Date.Now(self.date["Object"].replace(day = 24))

		# Check if today is Christmas and update the "Today is Christmas" state with the returned boolean
		self.start_christmas["States"]["Today is Christmas"] = self.Today_Is_Christmas(self.date)

		# Define the date format to use
		date_format = "[Day] [Month name] [Year], [Day name]"

		# Get the current date text in the defined date format
		date_text = self.date["Formats"][date_format][self.language["Small"]]

		# Show the "Today is" text in the user language
		print(self.Language.language_texts["today_is"] + ":")

		# Show the current date text in the defined date format
		print("\t" + date_text)
		print()

		# If today is not Christmas
		if self.start_christmas["States"]["Today is Christmas"] == False:
			# Create a shortcut to the units of the current date
			date_units = self.date["Units"]

			# Create a shortcut to the units of the Christmas date
			christmas_date_units = self.christmas["Date"]["Units"]

			# Define a dictionary to store the remaining time until Christmas
			time_left = {}

			# Calculate the difference in years from the current year to the Christmas year
			years_left = (date_units["Year"] - christmas_date_units["Year"])

			# Calculate the difference in months from the current month to the Christmas month
			months_left = (date_units["Month"] - christmas_date_units["Month"])

			# Convert the years left to months (years left times 12) and add the months left
			time_left["Months"] = years_left * 12 + months_left

			# Calculate the absolute difference in days from the current date to Christmas
			days_left = abs((self.date["Object"] - self.christmas["Date"]["Object"]).days)

			# Calculate the total number of days left in the current month,
			# by multiplying the months left until Christmas by the number of days in the current month
			month_days_left = time_left["Months"] * self.Date.Monthrange(date_units["Year"], date_units["Month"])[1]

			# Define the number of days left
			time_left["Days"] = days_left - abs(month_days_left)

			# Get the absolute value of each time
			for key in time_left:
				time_left[key] = abs(time_left[key])

			# Show the "Today is not the Christmas day, wait until" text in the user language
			print(self.language_texts["today_is_not_the_christmas_day_wait_until"] + ":")

			# Get the Christmas date text in the defined date format
			date_text = self.christmas["Date"]["Formats"][date_format][self.language["Small"]]

			# Show the Christmas date text
			print("\t" + date_text)

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

		# If today is Christmas
		if self.start_christmas["States"]["Today is Christmas"] == True:
			# Define the Christmas steps
			self.Define_Christmas_Steps()

			# Execute the Christmas steps
			self.Execute_Christmas_Steps()

			# Show the text telling the user that they finished their Christmas of the current year
			print(self.language_texts["your_christmas_of_{}_is_finished_congratulations!"].format(self.date["Units"]["Year"]))

	def Define_Christmas_Steps(self):
		# Define the local step number
		number = 1

		# Iterate through the step keys and texts
		for key, text in self.start_christmas["Dictionaries"]["Planning"].items():
			# Create the local step dictionary
			step = {
				"Number": number,
				"Key": key,
				"Text": text,
				"Ask for input": True,
				"Has object": False,
				"First space": True,
				"Methods": {}
			}

			# Create a shortcut to the "[Current year]" text
			current_year_text = "[" + self.Language.language_texts["current_year"] + "]"

			# If the "[Current year]" text is inside the step text
			if current_year_text in step["Text"]:
				# Replace the "[Current year]" text with the actual current year number
				step["Text"] = step["Text"].replace(current_year_text, str(self.date["Units"]["Year"]))

			# If the step key is inside the "Objects" dictionary
			if key in self.start_christmas["Dictionaries"]["Objects"]:
				# Change the "Has object" switch to True
				step["Has object"] = True

				# Update the local step dictionary with the one inside the "Objects" dictionary
				step.update(self.start_christmas["Dictionaries"]["Objects"][key])

				# If the "Method" key is inside the step dictionary
				if "Method" in step:
					# If the method is inside the list of methods to not ask for input
					if step["Method"] in self.christmas["Methods"]["Do not ask for input"]:
						# Change its "Ask for input" switch to False
						step["Ask for input"] = False

					# Create the local method dictionary
					method = {
						"Name": step["Method"],
						"Object": self.christmas["Methods"]["Dictionary"][step["Method"]]
					}

					# If the "Value" key is present, add it to the method dictionary
					if "Value" in step:
						method["Value"] = step["Value"]

					# Add it to the dictionary of methods
					step["Methods"][method["Name"]] = method

				# Else, if the "Methods" key is inside the step dictionary
				elif "Methods" in step:
					# Create a copy of the "Methods" dictionary
					methods_copy = deepcopy(step["Methods"])

					# Reset the "Methods" dictionary to be empty
					step["Methods"] = {}

					# Iterate through the copy of the "Methods" dictionary
					for method_name in methods_copy:
						# If the method is inside the list of methods to not ask for input
						if method_name in self.christmas["Methods"]["Do not ask for input"]:
							# Change its "Ask for input" switch to False
							step["Ask for input"] = False

						# Create the local method dictionary
						method = {
							"Name": method_name,
							"Object": self.christmas["Methods"]["Dictionary"][method_name]
						}

						# If the "Values" key is present
						if "Values" in step:
							# Get the value for the method
							value = step["Values"][method_name]

							# Add it to the method dictionary
							method["Value"] = value

						# Add it to the dictionary of methods
						step["Methods"][method_name] = method

			# Add the local step dictionary to the root "Steps" dictionary
			self.start_christmas["Steps"]["Dictionary"][key] = step

			# Add one to the step number
			number += 1

	def Execute_Christmas_Steps(self):
		# Get the "Starting Christmas day for the year {}" text template
		text_template = self.language_texts["starting_christmas_day_for_the_year_{}"]

		# Format it with the current year
		text = text_template.format(self.date["Units"]["Year"])

		# Show the "Starting Christmas day in [current year]" text
		print(text + "...")
		print()

		# Show a three dash space separator
		print(self.separators["3"])
		print()

		# Show the "Opening the Christmas planning file" text in the user language
		print(self.language_texts["opening_the_christmas_planning_file"] + "...")

		# Open the user language "Planning" file
		self.System.Open(self.christmas["Files"]["Planning"])

		# Show a three dash space separator
		print()
		print(self.separators["3"])
		print()

		# Iterate through the step dictionaries inside the root "Steps" dictionary
		for step in self.start_christmas["Steps"]["Dictionary"].values():
			# Define the text as the step number, a dot and a space, and the step text
			text = str(step["Number"]) + ". " + step["Text"]

			# Show the text
			print(text)

			# If the step does has an object dictionary
			# And the "Methods" dictionary is not empty
			if (
				step["Has object"] == True and
				step["Methods"] != {}
			):
				# Show a space separator
				print()

			# Iterate through the dictionary of step methods
			for method_name, method in step["Methods"].items():
				# If the "Value" key is inside the method dictionary
				if "Value" in method:
					# Run the method with the value
					method["Object"](method["Value"])

				# Else, run the method without the value
				else:
					method["Object"]()

			# If the "Ask for input" switch is True
			if step["Ask for input"] == True:
				# Define the input text as the "Continue" text in the user language
				input_text = self.Language.language_texts["continue, title()"]

				# If the "Input text" is inside the step dictionary
				if "Input text" in step:
					# Get the text key
					text_key = step["Input text"]

					# Get the input text
					input_text = self.language_texts[text_key]

				# Ask for user input before continuing to the next Christmas step
				self.Input.Type(input_text, first_space = step["First space"])

			# Show a five dash space separator
			print()
			print(self.separators["5"])
			print()
# Start_Christmas.py

from Christmas.Christmas import Christmas as Christmas

from calendar import monthrange

class Start_Christmas(Christmas):
	def __init__(self):
		super().__init__()

		# Define the "Start Christmas" dictionary
		self.start_christmas = {
			"Dates": {
				"Today": self.date,
				"Christmas": self.christmas["Date"]
			},
			"Files": {
				"Planning": self.year_texts["Folders"]["Christmas"]["Planning"][self.user_language],
				"Objects": self.year_texts["Folders"]["Christmas"]["Planning"]["Objects"]
			},
			"Dictionaries": {}
		}

		# Read the dictionary files
		for key, file in self.start_christmas["Files"].items():
			# Read the language planning file using the "Dictionary" method of the "File" class
			if key == "Planning":
				dictionary = self.File.Dictionary(file, next_line = True)

			# Read the objects using the "To_Python" method of the "JSON" class
			if key == "Objects":
				dictionary = self.JSON.To_Python(file)

			self.start_christmas[key] = dictionary

		# Show a separator
		print()
		print(self.separators["5"])
		print()

		# Define today as "24 of December" for testing purposes
		if self.switches["Testing"] == True:
			self.start_christmas["Dates"]["Today"] = self.Date.Now(self.date["Object"].replace(day = 24))

		# Define the date and Christmas date units for easier typing
		date = self.start_christmas["Dates"]["Today"]
		date_units = date["Units"]

		christmas_date = self.start_christmas["Dates"]["Christmas"]
		christmas_date_units = christmas_date["Units"]

		# If today is "24 of December"
		if (
			date_units["Day"] == christmas_date_units["Day"] - 1 and
			date_units["Month"] == christmas_date_units["Month"]
		):
			# It is acceptable to be Christmas (almost midnight)
			self.christmas["States"]["Today is Christmas"] = True

		# Show the current date text
		print(self.Language.language_texts["today_is"] + ":")

		date_text = date["Formats"]["[Day name], [Day] [Month name] [Year]"][self.user_language]

		print("\t" + date_text)
		print()

		# If today is not Christmas day
		if self.christmas["States"]["Today is Christmas"] == False:
			# Define the items left dictionary
			items_left = {
				"Months": (date_units["Year"] - christmas_date_units["Year"]) * 12 + (date_units["Month"] - christmas_date_units["Month"])
			}

			# Define the number of days left
			items_left["Days"] = abs((date["Object"] - christmas_date["Object"]).days - 1) - (items_left["Months"] * monthrange(date_units["Year"], date_units["Month"])[1])

			# Get the absolute value of each item
			for key in items_left:
				items_left[key] = abs(items_left[key])

			# Show that today is not Christmas day
			print(self.language_texts["today_is_not_christmas_day_wait_until"] + ":")

			# Show the Christmas date text
			date_text = christmas_date["Formats"]["[Day name], [Day] [Month name] [Year]"][self.user_language]

			print("\t" + date_text)

			# Define the texts dictionary for easier typing
			texts_dictionary = self.Date.language_texts

			# Iterate through the items left dictionary
			for item in items_left:
				# Define the text key
				text_key = item.lower()

				# Define the number of items left
				number = items_left[item]

				# If the number is not zero
				if number != 0:
					# Define the items list
					items = [
						number,
						texts_dictionary[text_key[:-1] + "_left"],
						texts_dictionary[text_key + "_left"]
					]

					# Create the number text (singular or plural)
					number_text = self.Text.By_Number(*items)

					# Show it, along with the number of items left
					print()
					print(number_text + ":")
					print("\t" + str(number) + " " + number_text.lower())

		# If today is Christmas day
		if self.christmas["States"]["Today is Christmas"] == True:
			# Execute the Christmas steps
			self.Execute_Christmas_Steps()

			# Show the text of a finished Christmas
			print(self.language_texts["your_christmas_of_{}_is_finished_congratulations!"].format(self.date["Units"]["Year"]))

		# Show a final separator
		print()
		print("----------")

	def Execute_Christmas_Steps(self):
		# Define the "Starting Christmas" text and format it
		text = self.language_texts["starting_{}_day_in_{}"]

		text = text.format(self.Language.language_texts["christmas, title()"], self.date["Units"]["Year"])

		# Show the "Starting Christmas" text
		print(text)
		print()

		# Show a one dash space separator
		print(self.separators["1"])
		print()

		# Open the language "Planning" file
		self.System.Open(self.start_christmas["Files"]["Planning"], verbose = False)

		# Define the list of planning keys
		keys = list(self.start_christmas["Planning"].keys())

		# Iterate through the Christmas steps
		i = 0
		for key, text in self.start_christmas["Planning"].items():
			# Define the step text
			text = str(i + 1) + ". " + text

			# Show it
			print(text)

			# Define the "ask_for_input" variable as True by default
			ask_for_input = True

			# If the step does not have an object
			if key not in self.start_christmas["Objects"]:
				print()

			# If the step haves an object
			if key in self.start_christmas["Objects"]:
				# Get the object dictionary
				object = self.start_christmas["Objects"][key]

				# Get the function dictionary of the object
				dictionary = self.christmas["Functions"][object["Function"]]

				# If the value key exists inside the object
				if "Value" in object:
					# Get the value
					value = object["Value"]

					# If the local value is not a dictionary
					# And the function has a values dictionary
					# And the local value is inside that values dictionary
					if (
						type(value) != dict and
						"Values" in dictionary and
						value in dictionary["Values"]
					):
						# Get the value from the values dictionary
						value = dictionary["Values"][value]

					# If the "Function" key is not inside the dictionary
					if "Function" not in dictionary:
						# Then define the function as the default "Open" function
						dictionary["Function"] = self.Open

					# Run the function with the value
					dictionary["Function"](value)

				else:
					# Run the function with no value
					dictionary["Function"]()

				if "Ask for input" in dictionary:
					# Update the "ask_for_input" variable with the value inside the function dictionary
					ask_for_input = dictionary["Ask for input"]

			# If the program needs to ask for user input before continuing to the next step
			if ask_for_input == True:
				# Define the type text for easier typing
				type_text = self.Language.language_texts["continue, title()"]

				# Define the first space variable
				first_space = False

				if key in self.start_christmas["Objects"]:
					first_space = True

				# Ask for user input before continuing to the next step
				self.Input.Type(type_text, first_space = first_space)

			# Show a separator
			print()
			print("-----")
			print()

			i += 1
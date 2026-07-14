# Meal_Times.py

# Import some useful modules
import importlib

# Define the main "Meal_Times" class
class Meal_Times():
	def __init__(self):
		# Define the variables of the class
		self.Define_Variables()

		# ---------- #

		# Define the root "Meal_Times" (class) dictionary
		self.meal_times = {
			# Define the root "Register" switch initially as True
			# (To always register the meal times when no active arguments are present)
			"Register": True,

			# Define the meal times text initially as "registered in"
			"Text": self.language_texts["registered_in"]
		}

		# If this class has an arguments dictionary
		if self.has_arguments == True:
			# Parse the arguments
			# (The dictionary of arguments was received from the "Module_Selector" module)
			self.Parse_Arguments()

		# Define the meal times dictionary
		self.Define_Times()

		# Show the meal times
		self.Show_Times()

	def Define_Variables(self):
		# Import the "JSON" class
		from Utility.JSON import JSON as JSON

		# Instance it and add it to the current class
		self.JSON = JSON()

		# Import the "folders" dictionary from the "JSON" class
		self.folders = self.JSON.folders

		# ---------- #

		# Get the dictionary of Python modules
		self.modules = self.JSON.To_Python(self.folders["Python"]["Modules"]["Modules"])

		# Define a list of utility classes to not import
		do_not_import = [
			"API",
			"File",
			"System",
			"Text"
		]

		# Iterate through the list of utility classes
		for class_title in self.modules["Utility"]["List"]:
			# If the class is not already inside the self class (Meal_Times)
			# And the class title is not inside the list of utility classes to not import
			if (
				hasattr(self, class_title) == False and
				class_title not in do_not_import
			):
				# Import the module of the class
				module = importlib.import_module("." + class_title, "Utility")

				# Get the class object inside the module
				class_object = getattr(module, class_title)

				# If the class title is not "Modules"
				if class_title != "Modules":
					# Run the class object to define its attributes
					class_object = class_object()

				# Add the class object to the root class
				setattr(self, class_title, class_object)

		# ---------- #

		# Define the module dictionary and the module folders and files
		self.Modules(class_object = self, module_files = "Times")

		# ---------- #

		# Import the switches dictionary from the "Global Switches" class
		self.switches = self.Global_Switches.switches["Global"]

		# ---------- #

		# Define the "Language" class as the same class inside the "JSON" class
		self.Language = self.JSON.Language

		# Import some attributes from the "Language" class

		# Import the "languages" dictionary
		self.languages = self.Language.languages

		# Import the "language" dictionary
		self.language = self.Language.language

		# Import the "separators" dictionary
		self.separators = self.Language.separators

		# ---------- #

		# Define the "Texts" dictionary
		self.texts = self.JSON.To_Python(self.module["Files"]["Texts"])

		# Define the "Language texts" dictionary
		self.language_texts = self.Language.Item(self.texts)

	def Parse_Arguments(self):
		# If the "Verbose" switch is True
		if self.switches["Verbose"] == True:
			# Show the arguments dictionary
			print()
			print(self.Language.language_texts["arguments, title()"] + ":")
			print()
			self.JSON.Show(self.arguments)
			print()
			print(self.separators["5"])

		# Iterate through the arguments dictionary which was received from the "Module_Selector" module
		for key, argument in self.arguments.items():
			# If the argument is "Show" (the meal times)
			# And its value is True
			if (
				key == "Show" and
				argument["Value"] == True
			):
				# Change the root "Register" switch to be False
				# (So the meal times will not be registered)
				self.meal_times["Register"] = False

				# Change the root meal times text to be "obtained from"
				self.meal_times["Text"] = self.language_texts["obtained_from"]

	def Define_Times(self):
		# Define the default times dictionary
		self.times = {
			"Numbers": {
				"Total": 0
			},
			"List": [
				"Ate",
				"Can drink water",
				"Will be hungry"
			],
			"Dictionary": {}
		}

		# Update the total number of times with the length of the list of times
		self.times["Numbers"]["Total"] = len(self.times["List"])

		# Iterate through the times in the list of times
		for time_name in self.times["List"]:
			# Create the default time dictionary
			time = {
				"Texts": {},
				"Time to add": {
					"Unit": {},
					"Quantity": 0
				},
				"Current time": {
					"Object": {},
					"Time": ""
				}
			}

			# Iterate through the list of small languages
			for language in self.languages["Small"]:
				# Define the text as the "This is the time when you" text in the current language and a space
				text = self.texts["this_is_the_time_when_you"][language] + " "

				# Define the text key using the time name
				text_key = time_name.lower().replace(" ", "_")

				# Get the time text for the time in the current language
				time_text = self.texts[text_key][language]

				# Add the time text to the defined text
				text += time_text

				# Add the text to the time "Texts" dictionary in the key of the current language
				time["Texts"][language] = text

			# If the time name is "Ate"
			if time_name == "Ate":
				# Remove the "Time to add" dictionary as it is not needed
				# (The "Ate" time is not added to, it is the base time for the other two times)
				time.pop("Time to add")

			# If the time name is not "Ate"
			if time_name != "Ate":
				# Define the time unit initially as "minutes"
				unit = "minutes"

				# Define the time quantity to be 40 minutes
				quantity = 40

				# If the time name is "Will be hungry"
				if time_name == "Will be hungry":
					# Change the time unit to be "hours"
					unit = "hours"

					# Change the time quantity to be 3 hours
					quantity = 3

				# Define the time to add "Unit" key as the time unit text dictionary
				time["Time to add"]["Unit"] = self.Date.texts[unit]

				# Define the time to add "Quantity" key as the local time quantity
				time["Time to add"]["Quantity"] = quantity

			# If the meal times need to be registered and shown
			if self.meal_times["Register"] == True:
				# Define the local date initially as the current time dictionary
				date = self.Date.Now()

				# If the time name is not "Ate"
				if time_name != "Ate":
					# Change the local object to be the object of the "Ate" time
					object = self.times["Dictionary"]["Ate"]["Current time"]["Object"]

					# Create shortcuts to the English time unit and time quantity so the code looks better and easier to understand
					unit = time["Time to add"]["Unit"]["en"]
					quantity = time["Time to add"]["Quantity"]

					# Define the local time unit dictionary
					time_unit = {
						# Define the time unit to add to the "Ate" time
						# 
						# Examples:
						# minutes: 40
						# hours: 3
						unit: quantity
					}

					# Add the defined time units to the "Ate" time using the "Relativedelta" method of the "Date" utility class
					date = self.Date.Now(object + self.Date.Relativedelta(**time_unit))

				# Define the local object initially as the current time object
				object = date["Object"]

				# Define the current time "Object" key as the local object
				time["Current time"]["Object"] = object

				# Define the current "Time" key as the "HH:MM" (Hours:Minutes) time format of the current time in the "for" loop
				time["Current time"]["Time"] = date["Formats"]["HH:MM"]

			# If the meal times do not need to be registered, only shown
			if self.meal_times["Register"] == False:
				# Read the "Times.json" file to get its JSON dictionary and define it as the local times dictionary
				local_times = self.JSON.To_Python(self.module["Files"]["Times"])

				# Get the local time dictionary using the current time name as a key
				local_time = local_times["Dictionary"][time_name]

				# Change the "Current" time dictionary to be the one inside the "Times.json" file
				time["Current time"] = local_time["Current time"]

			# Add the local time dictionary to the root times "Dictionary"
			self.times["Dictionary"][time_name] = time

		# Update the "Times.json" file with the updated "Times" dictionary
		self.JSON.Edit(self.module["Files"]["Times"], self.times)

	def Set_Timer(self):
		# Define website timer to countdown to "Will be hungry" time
		from urllib.parse import urlencode

		# Define URL template to use
		self.timer_url_template = "https://www.timeanddate.com/countdown/generic?"

		# Define default URL parameters
		parameters = {
			"p0": "543",
			"msg": self.language_texts["time_that_you_will_be_hungry"],
			"font": "slab"
		}

		self.timer_url_template = self.timer_url_template + urlencode(parameters)

		# Define English "minute" and "second" texts
		self.minute_and_second_texts = [
			self.Date.texts["minute"]["en"],
			self.Date.texts["second"]["en"]
		]

		self.timer_url = self.timer_url_template

		self.time_parameters = {}

		# Iterate through date and time attributes
		for attribute in self.Date.texts["date_attributes, type: list"]["en"]:
			self.time_parameters[attribute.capitalize()] = {
				"Parameter": attribute.capitalize()
			}

			# If the attribute name is "minute" or "second", remove the three last characters (for Time And Date URL to work)
			if attribute in self.minute_and_second_texts:
				self.time_parameters[attribute.capitalize()]["Parameter"] = attribute[:-3]

			# If the attribute is the first one, then add "&" to start adding URL parameters
			if attribute == self.Date.texts["date_attributes, type: list"]["en"][0]:
				self.timer_url += "&"

			# Add the attribute name, an equals sign, and the attribute (from date)
			date = self.Date.From_String(self.times["Will be hungry"]["Object"])

			self.timer_url += self.time_parameters[attribute.capitalize()]["Parameter"] + "=" + str(date["Units"][attribute.capitalize()])

			# If the attribute is not the last one, then add "&" to continue adding URL parameters
			if attribute != self.Date.texts["date_attributes, type: list"]["en"][-1]:
				self.timer_url += "&"

		# Open formatted timer URL with parameters
		#self.System.Open(self.timer_url)

		# Define scheduled task to play alarm sound when the "Will be hungry" time is reached
		self.parameters = {
			"task_title": self.language_texts["play_alarm_sound_when_you_are_hungry"],
			#"path": contents["Play_Alarm"]["__init__"],
			"start_time": self.times["Will be hungry"]["Object"]
		}

		self.Date.Schedule_Task(**self.parameters)

	def Show_Times(self):
		# Show the "Showing the meal times below" in the user language
		print()
		print(self.language_texts["showing_the_meal_times_below"] + ":")

		# Create a shortcut to the "The times were {}" text template in the user language
		text_template = self.language_texts["the_times_were_{}_the_times_file"]

		# Format the template with the meal times text
		text = text_template.format(self.meal_times["Text"])

		# Show the meal times text inside parenthesis
		print("({})".format(text))

		# Iterate through the time names and dictionaries in the dictionary of times
		for time_name, time in self.times["Dictionary"].items():
			# Show a first space
			print()

			# Show the time text
			print(time["Texts"][self.language["Small"]] + ":")

			# Define the local time text as the "HH:MM" (Hours:Minutes) time format of the current time in the "for" loop
			time_text = time["Current time"]["Time"]

			# If the time name is not "Ate"
			if time_name != "Ate":
				# Create shortcuts to the "Ate" time, and "Time to add" quantity and unit
				ate_time = self.times["Dictionary"]["Ate"]["Current time"]["Time"]
				quantity = time["Time to add"]["Quantity"]
				unit = time["Time to add"]["Unit"][self.language["Small"]]

				# Add the time that is added to the "Ate" time to the local time text
				# 
				# Examples:
				# (12:30 + 40 minutes)
				# (12:30 + 3 hours)
				time_text += " ({} + {} {})".format(
					ate_time,
					quantity,
					unit
				)

			# Show the local time text
			print(time_text)
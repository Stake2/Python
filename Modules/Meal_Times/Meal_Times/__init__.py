# Meal_Times.py

# Import some useful modules
import importlib

# Define the main "Meal_Times" class
class Meal_Times():
	def __init__(self):
		# Define the variables of the class
		self.Define_Variables()

		# Lists and dictionaries method
		self.Define_Lists_And_Dictionaries()

		# Set the default value of the "register" switch as on
		self.register_time = True

		# If the dictionary of arguments is present inside this class
		if hasattr(self, "arguments") == True:
			# Parse the arguments
			# (The dictionary of arguments was received from the "Module_Selector" module)
			self.Parse_Arguments()

		self.registered_text = self.language_texts["the_times_were_obtained_from_the_times_file"]

		if self.register_time == True:
			self.registered_text = self.language_texts["the_times_were_recorded_in_the_times_file"]

			self.Get_Time()
			self.Set_Timer()

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

	def Define_Lists_And_Dictionaries(self):
		# Read the "Times.json" file
		self.times = self.JSON.To_Python(self.module["Files"]["Times"])

		# Iterate through text time types list
		for time_type in self.times["Types"]:
			# If the dictionary of the time type is not present in JSON, add it
			if time_type not in self.times:
				# Define the dictionary
				self.times[time_type] = {
					"Object": {},
					"Time": self.times["Times"][time_type],
					"Time text": "",
					"Unit": {},
					"Texts": {}
				}

				# Define the time unit text
				self.times[time_type]["Unit"]["en"] = "Hours"

				if time_type == "Can drink water":
					self.times[time_type]["Unit"]["en"] = "Minutes"

				text_key = time_type.lower().replace(" ", "_")

				# Define the unit name text
				for language in self.languages["Small"]:
					self.times[time_type]["Unit"][language] = self.texts[self.times[time_type]["Unit"]["en"].lower()][language]

					prefix = self.texts["this_is_the_time_that_you"][language] + " "

					self.times[time_type]["Texts"][language] = prefix + self.texts[text_key][language]

	def Parse_Arguments(self):
		# If the "Verbose" switch is True
		if self.switches["Verbose"] == True:
			# Show the dictionary of arguments
			print()
			print(self.Language.language_texts["arguments, title()"] + ":")
			print()
			self.JSON.Show(self.arguments)
			print()
			print(self.separators["5"])

		# Iterate through the dictionary of arguments which was received from the "Module_Selector" module
		for key, argument in self.arguments.items():
			# If the argument is "Show" (the meal times) and it is True
			if (
				key == "Show" and
				argument["Value"] == True
			):
				# Then the meal times will not be registered
				self.register_time = False

			# If the argument is "Register" (the meal times) and it is True
			if (
				key == "Register" and
				argument["Value"] == True
			):
				# Then the meal times will be registered
				self.register_time = True

	def Get_Time(self):
		# Iterate through time types
		for time_type in self.times["Types"]:
			# If the time type is "Ate", its date is only a normal date
			if time_type == "Ate":
				self.times[time_type]["Object"] = self.Date.Now()["Object"]

			# If the time type is not "Ate", its date is the "ate" date plus the relativedelta of the time type "time to add"
			if time_type != "Ate":
				dictionary = {
					self.times[time_type]["Unit"]["en"]: self.times[time_type]["Time"]
				}

				# Add the "ate" date to the relativedelta of the "time to add" of the time type
				self.times[time_type]["Object"] = self.Date.Now(self.times["Ate"]["Object"] + self.Date.Relativedelta(**dictionary))["Object"]

			# Format the date as "Hours:Minutes", "HH:MM"
			self.times[time_type]["Time text"] = self.Date.Now(self.times[time_type]["Object"])["Formats"]["HH:MM"]

		# Stringfy "datetime" objects to write them into the JSON file
		for time_type in self.times["Types"]:
			self.times[time_type]["Object"] = str(self.times[time_type]["Object"])

		# Write the new time type dictionaries with the stringfied datetimes
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

		#self.Date.Schedule_Task(**self.parameters)

	def Show_Times(self):
		print()
		print(self.language_texts["showing_the_meal_times_below"] + ":")
		print("(" + self.registered_text + ")")

		# Iterate through time types
		for time_type in self.times["Types"]:
			print()

			# Show time type text ("this_is_the_time_that_you" + the time type text in user language)
			print(self.times[time_type]["Texts"][self.language["Small"]] + ":")

			# Define the time as the date format (HH:MM)
			time = self.times[time_type]["Time text"]

			# If time type is not ate, add the time that is added into the "ate" time, examples: (ate + 40 minutes), (ate + 3 hours)
			if time_type != "Ate":
				time += " ({} + {} {})".format(self.times["Ate"]["Time text"], self.times[time_type]["Time"], self.times[time_type]["Unit"][self.language["Small"]])

			print(time)
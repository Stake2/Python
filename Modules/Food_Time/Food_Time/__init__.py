# Food_Time.py

# Import the "importlib" module
import importlib

class Food_Time():
	def __init__(self):
		# Import the classes
		self.Import_Classes()

		# Define the folders of the module
		self.folders = self.Define_Folders(object = self, files = ["Times"]).folders

		# Module related methods
		self.Define_Basic_Variables()
		self.Define_Texts()

		# Lists and dictionaries method
		self.Define_Lists_And_Dictionaries()

		# Set the default value of the "register" switch as on
		self.register_time = True

		# If this module has the "arguments" variable, which was received from the "Module_Selector.py" module
		if hasattr(self, "arguments") == True:
			# Parse the arguments
			self.Parse_Arguments()

		self.registered_text = self.language_texts["times_taken_from_the_times_file"]

		if self.register_time == True:
			self.registered_text = self.language_texts["times_registered_into_the_times_file"]

			self.Get_Time()
			self.Set_Timer()

		self.Show_Times()

	def Import_Classes(self):
		# Define the list of modules to be imported
		modules = [
			"Define_Folders",
			"JSON"
		]

		# Iterate through the list of modules
		for module_title in modules:
			# Import the module
			module = importlib.import_module("." + module_title, "Utility")

			# Get the sub-class
			sub_class = getattr(module, module_title)

			# If the module title is not "Define_Folders"
			if module_title != "Define_Folders":
				# Run the sub-class to define its variable
				sub_class = sub_class()

			# Add the sub-class to the current module
			setattr(self, module_title, sub_class)

		# Define the "Language" class as the same class inside the "JSON" class
		self.Language = self.JSON.Language

	def Define_Basic_Variables(self):
		# Get the modules list
		self.modules = self.JSON.To_Python(self.folders["Apps"]["Modules"]["Modules"])

		# Create a list of the modules that will not be imported
		remove_list = [
			"Define_Folders",
			"Modules",
			"Language",
			"JSON"
		]

		# Iterate through the Utility modules
		for module_title in self.modules["Utility"]["List"]:
			# If the module title is not inside the remove list
			if module_title not in remove_list:
				# Import the module
				module = importlib.import_module("." + module_title, "Utility")

				# Get the sub-class
				sub_class = getattr(module, module_title)

				# Add the sub-class to the current module
				setattr(self, module_title, sub_class())

		# Get the switches dictionary from the "Global Switches" module
		self.switches = self.Global_Switches.switches["Global"]

		# Get the Languages dictionary
		self.languages = self.Language.languages

		# Get the user language and full user language
		self.user_language = self.Language.user_language
		self.full_user_language = self.Language.full_user_language

		# Define the local "folders" dictionary as the dictionary inside the "Folder" class
		self.folders = self.Folder.folders

		# Get the Sanitize method of the File class
		self.Sanitize = self.File.Sanitize

		# Get the current date from the Date module
		self.date = self.Date.date

	def Define_Texts(self):
		# Define the "Texts" dictionary
		self.texts = self.JSON.To_Python(self.module["Files"]["Texts"])

		# Define the "Language texts" dictionary
		self.language_texts = self.Language.Item(self.texts)

		# Define the "Separators" dictionary
		self.separators = {}

		# Create separators from one to ten characters
		for number in range(1, 11):
			# Define the empty string
			string = ""

			# Add separators to it
			while len(string) != number:
				string += "-"

			# Add the string to the Separators dictionary
			self.separators[str(number)] = string

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
				for language in self.languages["small"]:
					self.times[time_type]["Unit"][language] = self.texts[self.times[time_type]["Unit"]["en"].lower()][language]

					prefix = self.texts["this_is_the_time_that_you"][language] + " "

					self.times[time_type]["Texts"][language] = prefix + self.texts[text_key][language]

	def Parse_Arguments(self):
		if self.switches["Verbose"] == True:
			print()
			print(self.Language.language_texts["arguments, title()"] + ":")
			print()
			self.JSON.Show(self.arguments)
			print()
			print(self.separators["5"])

		# Get the arguments from the "Module_Selector.py" module
		for key, argument in self.arguments.items():
			# If the argument is "Set" and it is True
			if (
				key == "Set" and
				argument["Value"] == True
			):
				# Then the meal times will be registered
				self.register_time = True

			# If the argument is "Check" and it is True
			if (
				key == "Check" and
				argument["Value"] == True
			):
				# Then the meal times will not be registered
				self.register_time = False

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

		# List the contents of the module folder
		contents = self.Folder.Contents(self.module["Folders"]["Modules"]["root"])["dictionary"]

		# Define scheduled task to play alarm sound when the "Will be hungry" time is reached
		self.parameters = {
			"task_title": self.language_texts["play_alarm_sound_when_you_are_hungry"],
			"path": contents["Play_Alarm"]["__init__"],
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
			print(self.times[time_type]["Texts"][self.user_language] + ":")

			# Define the time as the date format (HH:MM)
			time = self.times[time_type]["Time text"]

			# If time type is not ate, add the time that is added into the "ate" time, examples: (ate + 40 minutes), (ate + 3 hours)
			if time_type != "Ate":
				time += " ({} + {} {})".format(self.times["Ate"]["Time text"], self.times[time_type]["Time"], self.times[time_type]["Unit"][self.user_language])

			print(time)
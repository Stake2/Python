# Food_Time.py

class Food_Time():
	def __init__(self):
		self.Define_Basic_Variables()

		# Define module folders
		from Utility.Define_Folders import Define_Folders as Define_Folders

		Define_Folders(self, ["Times"])

		self.folders["apps"]["modules"][self.module["key"]] = self.Folder.Contents(self.folders["apps"]["modules"][self.module["key"]]["root"], lower_key = True)["dictionary"]

		self.Define_Texts()

		self.Define_Lists_And_Dictionaries()

		self.registered_text = self.language_texts["times_taken_from_the_times_file"]

		if self.register_time == True:
			self.registered_text = self.language_texts["times_registered_into_the_times_file"]

			self.Get_Time()
			self.Set_Timer()

		self.Show_Times()

	def Define_Basic_Variables(self):
		from Utility.Global_Switches import Global_Switches as Global_Switches

		from Utility.File import File as File
		from Utility.Folder import Folder as Folder
		from Utility.Date import Date as Date
		from Utility.Input import Input as Input
		from Utility.JSON import JSON as JSON
		from Utility.Text import Text as Text

		self.switches = Global_Switches().switches["global"]

		self.File = File()
		self.Folder = Folder()
		self.Date = Date()
		self.Input = Input()
		self.JSON = JSON()
		self.Text = Text()

		self.languages = self.JSON.Language.languages

		self.user_language = self.JSON.Language.user_language
		self.full_user_language = self.JSON.Language.full_user_language

		self.Sanitize = self.File.Sanitize

		self.folders = self.Folder.folders

		self.date = self.Date.date

	def Define_Texts(self):
		self.texts = self.JSON.To_Python(self.folders["apps"]["module_files"][self.module["key"]]["texts"])

		self.language_texts = self.JSON.Language.Item(self.texts)

		self.large_bar = "-----"
		self.dash_space = "-"

	def Define_Lists_And_Dictionaries(self):
		# Read the "Times.json" file
		self.times = self.JSON.To_Python(self.folders["apps"]["module_files"][self.module["key"]]["times"])

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
		self.JSON.Edit(self.folders["apps"]["module_files"][self.module["key"]]["times"], self.times)

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
		#self.File.Open(self.timer_url)

		# Define scheduled task to play alarm sound when the "Will be hungry" time is reached
		self.parameters = {
			"task_title": self.language_texts["play_alarm_sound_when_you_are_hungry"],
			"path": self.folders["apps"]["modules"][self.module["key"]]["play_alarm"]["__init__"],
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
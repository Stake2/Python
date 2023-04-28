# Date.py

from datetime import datetime, timedelta, timezone
import pytz

class Date():
	def __init__(self):
		# Define module folders
		from Utility.Define_Folders import Define_Folders as Define_Folders

		Define_Folders(self)

		from Utility.JSON import JSON as JSON
		from Utility.Text import Text as Text

		self.JSON = JSON()
		self.Text = Text()

		self.languages = self.JSON.Language.languages
		self.user_language = self.JSON.Language.user_language
		self.user_timezone = self.JSON.Language.user_timezone

		self.Define_Texts()
		self.Number_Name_Generator()

		self.date = self.Now()

	def Define_Texts(self):
		self.texts = self.JSON.To_Python(self.folders["apps"]["module_files"]["utility"][self.module["key"]]["texts"])

		self.language_texts = self.JSON.Language.Item(self.texts)

	def Now(self, date_parameter = None):
		if date_parameter == None:
			date_parameter = datetime.now()

		date = {
			"User timezone": {
				"String": self.user_timezone,
				"UTC Offset": date_parameter.replace(microsecond = 0).astimezone().strftime("%z"),
				"Name": date_parameter.replace(microsecond = 0).astimezone().strftime("%Z")
			},
			"Object": {},
			"Units": {},
			"Texts": {},
			"Formats": {},
			"UTC": {
				"Object": date_parameter.replace(microsecond = 0).astimezone(pytz.UTC)
			},
			"Timezone": {
				"Object": date_parameter.replace(microsecond = 0).astimezone()
			}
		}

		# Iterate through the date names list
		for date_name in ["UTC", "Timezone"]:
			# Iterate through the date types list
			for date_type in ["Date", "Time"]:
				date[date_name][date_type] = {
					"Object": date[date_name]["Object"],
					"Units": {
						"Day": 0,
						"Week day": 0,
						"Month": 0,
						"Year": 0
					},
					"Texts": {
						"Day name": {},
						"Day gender": {},
						"Day": {},
						"Month name": {}
					},
					"Formats": {
						"YYYY-MM-DD": "",
						"DD/MM/YYYY": "",
						"DD-MM-YYYY": ""
					}
				}

				formats = [
					"%Y-%m-%d",
					"%d/%m/%Y",
					"%d-%m-%Y"
				]

				# If the date type is "Time", define its unique object and its own unit, text, and format keys
				if date_type == "Time":
					date[date_name][date_type] = {
						"Object": date[date_name][date_type]["Object"].time(),
						"Units": {
							"Hour": 0,
							"Minute": 0,
							"Second": 0
						},
						"Texts": {
							"Hour": {},
							"Minute": {},
							"Second": {}
						},
						"Formats": {
							"HH:MM": ""
						}
					}

					formats = [
						"%H:%M"
					]

				# Add the date or time units
				for key in date[date_name][date_type]["Units"]:
					data_key = key.lower()

					if " " in data_key:
						data_key = data_key.replace(" ", "")

					date[date_name][date_type]["Units"][key] = getattr(date[date_name][date_type]["Object"], data_key)

					if key == "Week day":
						date[date_name][date_type]["Units"][key] = date[date_name][date_type]["Units"][key]()

				# Add the date or time texts
				for key in date[date_name][date_type]["Texts"]:
					for language in self.languages["small"]:
						if key == "Day name":
							date[date_name][date_type]["Texts"][key][language] = self.texts["day_names, type: list"][language][date[date_name][date_type]["Units"]["Week day"]]

						elif key == "Day":
							date[date_name][date_type]["Texts"][key][language] = self.Text.By_Number(date[date_name][date_type]["Units"][key], self.texts[key.lower()][language], self.texts[key.lower() + "s"][language])

						elif key == "Month name":
							date[date_name][date_type]["Texts"][key][language] = self.texts["month_names, type: list"][language][date[date_name][date_type]["Units"]["Month"]]

						elif key == "Day gender":
							date[date_name][date_type]["Texts"][key][language] = self.texts["day_names_genders, type: list"][language][date[date_name][date_type]["Units"]["Week day"]]

						else:
							date[date_name][date_type]["Texts"][key][language] = self.Text.By_Number(date[date_name][date_type]["Units"][key], self.texts[key.lower()][language], self.texts[key.lower() + "s"][language])

				# Add the date or time formats
				i = 0
				for format in formats:
					format_key = list(date[date_name][date_type]["Formats"].keys())[i]

					date[date_name][date_type]["Formats"][format_key] = date[date_name]["Object"].strftime(format)

					i += 1

			# Create the "DateTime" key
			if "DateTime" not in date[date_name]:
				date[date_name]["DateTime"] = {}

			# Import all of the variables from inside the "Date" and "Time" dictionaries
			for date_type in ["Date", "Time"]:
				for key in ["Units", "Texts", "Formats"]:
					if key not in date[date_name]["DateTime"]:
						date[date_name]["DateTime"][key] = {}

					for sub_key in date[date_name][date_type][key]:
						date[date_name]["DateTime"][key][sub_key] = date[date_name][date_type][key][sub_key]

			keys = [
				"HH:MM DD/MM/YYYY",
				"YYYY-MM-DDTHH:MM:SSZ"
			]

			formats = [
				"%H:%M %d/%m/%Y",
				"%Y-%m-%dT%H:%M:%S"
			]

			i = 0
			for format in formats:
				format_key = keys[i]

				object = date[date_name]["Object"]

				if format_key == "YYYY-MM-DDTHH:MM:SSZ":
					if object.strftime("%Z") in ["UTC", ""]:
						format += "Z"

					else:
						format += "%z"

				date[date_name]["DateTime"]["Formats"][format_key] = object.strftime(format)

				if object.strftime("%Z") not in ["UTC", ""] and format_key == "YYYY-MM-DDTHH:MM:SSZ":
					list_ = list(date[date_name]["DateTime"]["Formats"][format_key])
					list_.insert(22, ":")

					date[date_name]["DateTime"]["Formats"][format_key] = self.Text.From_List(list_, break_line = False)

				i += 1

			# Import all of the variables from inside the "Timezone" dictionary since the modules usually use the timezone dates and times
			if date_name == "Timezone":
				date["Object"] = date[date_name]["Object"]

				for key in date[date_name]["DateTime"]:
					date[key] = date[date_name]["DateTime"][key]

		return date

	def Check(self, date, utc = False):
		if type(date) == dict:
			if utc == False and "Object" in date:
				date = date["Object"]

			if utc == True:
				date = date["UTC"]["Object"]

		if type(date) == str:
			date = self.From_String(date)

		return date

	def To_String(self, date, format = "", utc = False):
		date = self.Check(date, utc)

		if format == "":
			format = self.texts["default_format"]

			if date.strftime("%Z") in ["UTC", ""]:
				format += "Z"

			else:
				format += "%z"

		return date.strftime(format)

	def From_String(self, string, format = ""):
		from dateutil import parser

		if format == "":
			date = parser.parse(string)

		if format != "":
			date = datetime.strptime(string, format)

		date = self.Now(date)

		return date

	def Timedelta(self, **arguments):
		return timedelta(**arguments)

	def To_UTC(self, date):
		date = self.Check(date)

		date = self.Now(date.astimezone(pytz.UTC))

		return date

	def To_Timezone(self, date):
		date = self.Check(date)

		date = self.Now(date.astimezone())

		return date

	def Difference(self, before, after):
		date = {
			"before": before,
			"after": after
		}

		for key in date:
			if type(date[key]) == str:
				date[key] = self.Check(date[key])

			if type(date[key]) == datetime:
				date[key] = self.Now(date[key])

		string = date["after"]["Object"] - date["before"]["Object"]

		date["difference"] = {}

		texts = self.texts.copy()

		for attribute in texts["plural_date_attributes, type: list"]["en"]:
			if hasattr(string, attribute):
				date["difference"][attribute.capitalize()] = getattr(string, attribute)

		if hasattr(string, "years") == False and "Days" in date["difference"]:
			if (date["difference"]["Days"] // 365) != 0:
				date["difference"]["Years"] = date["difference"]["Days"] // 365
		
			if (date["difference"]["Days"] // 365) == 0:
				date["difference"]["Years"] = 0

		if date["difference"]["Years"] == -1:
			date["difference"]["Years"] = 0

		date["difference"]["Year days"] = 0
		date["difference"]["Month days"] = 0

		if (date["difference"]["Days"] // 365) not in [0, 1]:
			date["difference"]["Year days"] = date["difference"]["Years"] * 365

		if hasattr(string, "months") == False and ((date["difference"]["Days"] - date["difference"]["Year days"]) // 30) != 0:
			date["difference"]["Months"] = (date["difference"]["Days"] - date["difference"]["Year days"]) // 30
			date["difference"]["Month days"] = date["difference"]["Months"] * 30

		date["difference"]["Days"] = date["difference"]["Days"] - date["difference"]["Year days"] - date["difference"]["Month days"]

		if "Seconds" not in date["difference"]:
			date["difference"]["Seconds"] = 0

		date["difference"]["Seconds"] = date["difference"]["Seconds"] % (24 * 3600)
		date["difference"]["Hours"] = date["difference"]["Seconds"] // 3600
		date["difference"]["Seconds"] %= 3600
		date["difference"]["Minutes"] = date["difference"]["Seconds"] // 60 
		date["difference"]["Seconds"] %= 60

		singular = {}
		plural = {}

		i = 0
		for attribute in texts["plural_date_attributes, type: list"]["en"]:
			attribute = attribute.capitalize()

			if attribute in date["difference"]:
				if date["difference"][attribute] != 0:
					for language in self.languages["small"]:
						if language not in singular:
							singular[language] = []

						if language not in plural:
							plural[language] = []

						singular_attribute = texts["date_attributes, type: list"][language][i]
						plural_attribute = texts["plural_date_attributes, type: list"][language][i]

						singular[language].append(singular_attribute)
						plural[language].append(plural_attribute)

				if date["difference"][attribute] == 0:
					date["difference"].pop(attribute)

			i += 1

		for attribute in date["difference"].copy():
			if date["difference"][attribute] == 0:
				date["difference"].pop(attribute)

		texts["date_attributes, type: list"] = singular

		texts["plural_date_attributes, type: list"] = plural

		language_texts = self.JSON.Language.Item(texts)

		date["difference_strings"] = {}
		date["difference_string"] = ""

		i = 0
		for attribute in texts["plural_date_attributes, type: list"]["en"]:
			attribute = attribute.capitalize()

			if attribute in date["difference"]:
				if attribute != texts["plural_date_attributes, type: list"]["en"][0].capitalize():
					if len(date["difference"]) > 1 and len(date["difference"]) != 2:
						date["difference_string"] += ", "

					if len(date["difference"]) == 2:
						date["difference_string"] += " " + self.JSON.Language.language_texts["and"] + " "

				date["difference_string"] += str(date["difference"][attribute])

				list_ = language_texts["date_attributes, type: list"]

				if date["difference"][attribute] > 1:
					list_ = language_texts["plural_date_attributes, type: list"]

				date["difference_string"] += " " + list_[i]

			i += 1

		i = 0
		for attribute in texts["plural_date_attributes, type: list"]["en"]:
			attribute = attribute.capitalize()

			if attribute in date["difference"]:
				for language in self.languages["small"]:
					if language not in date["difference_strings"]:
						date["difference_strings"][language] = ""

					if attribute != "years" and attribute != texts["plural_date_attributes, type: list"]["en"][0].capitalize():
						# Add the ", " text (comma and space) if the number of time units is more than 1 and not 2 (can be more than 2)
						if len(date["difference"]) > 1 and len(date["difference"]) != 2:
							date["difference_strings"][language] += ", "

						# Add the " and " text if the number of time units is 2
						if len(date["difference"]) == 2:
							date["difference_strings"][language] += " " + self.JSON.Language.texts["and"][language] + " "

					# Add "and " text if the attribute is the last one and the number of time units is more than 2
					if attribute == texts["plural_date_attributes, type: list"]["en"][-1].capitalize() and len(date["difference"]) > 2:
						date["difference_strings"][language] += self.JSON.Language.texts["and"][language] + " "

					if attribute == "months" and date["difference"][attribute] != 12:
						date["difference_strings"][language] += str(date["difference"][attribute])

					else:
						date["difference_strings"][language] += str(date["difference"][attribute])

					list_ = texts["date_attributes, type: list"][language]

					if date["difference"][attribute] > 1:
						list_ = texts["plural_date_attributes, type: list"][language]

					if attribute == "months" and date["difference"][attribute] != 12:
						date["difference_strings"][language] += " " + list_[i]

					else:
						date["difference_strings"][language] += " " + list_[i]

			i += 1

		date["Difference"] = date["difference"]
		date["Text"] = date["difference_strings"]

		return date

	def Number_Name_Generator(self):
		self.numbers = {}
		self.numbers["list"] = {}
		self.numbers["list_feminine"] = {}
		self.numbers["string"] = {}

		for language in self.languages["small"]:
			self.numbers["list"][language] = ["zero"]
			self.numbers["list_feminine"][language] = []
			self.numbers["string"][language] = "zero\n"

		for language in self.languages["small"]:
			if language in self.numbers["list"] and language in self.texts["first_numbers"]:
				numbers = self.numbers["list"][language]

				i = 1
				while i <= 100:
					if i <= 10:
						numbers.append(self.texts["first_numbers"][language][i])

					if language == "pt":
						if i == 11:
							numbers.append("onze")

						if i == 12:
							number = self.texts["first_numbers"][language][2][:-2]
							numbers.append(number + "ze")

						if i == 13:
							number = self.texts["first_numbers"][language][3][:-1].replace("ê", "e")
							numbers.append(number + "ze")

						if i == 14:
							number = self.texts["first_numbers"][language][4].replace("ro", "or")
							numbers.append(number + "ze")

						if i == 15:
							numbers.append("quinze")

						if i >= 16 and i <= 17:
							number = str(i).replace("1", "")
							number = self.texts["first_numbers"][language][10] + "es" + self.texts["first_numbers"][language][int(number)]

							numbers.append(number)

						if i >= 18 and i <= 19:
							number = str(i).replace("1", "")
							number = self.texts["first_numbers"][language][10] + self.texts["first_numbers"][language][int(number)]

							if i == 19:
								number = number.replace(self.texts["first_numbers"][language][10], self.texts["first_numbers"][language][10] + "e")

							numbers.append(number)

						if i > 19 and i < 100:
							number = str(i)[:-1]

							if int(str(i)[1]) != 0:
								number = self.texts["ten_names"][language][int(number)] + self.texts["number_separator"][language] + self.texts["first_numbers"][language][int(str(i)[1])]

							else:
								number = self.texts["ten_names"][language][int(number)]

							numbers.append(number)

						if i == 100:
							numbers.append(self.texts["ten_names"][language][10])

					if language == "en":
						if i >= 11 and i <= 19:
							numbers.append(self.texts["first_numbers"][language][i])

						if i >= 20 and "0" in str(i)[1]:
							first_number = int(str(i)[:-1])

							numbers.append(self.texts["ten_names"][language][first_number])

						if i >= 20 and "0" not in str(i)[1]:
							first_number = int(str(i)[:-1])
							second_number = int(str(i)[1:])

							numbers.append(self.texts["ten_names"][language][first_number] + self.texts["number_separator"][language] + self.texts["first_numbers"][language][second_number])

					i += 1

				i = 1
				for number_name in self.numbers["list"][language]:
					if number_name != None:
						self.numbers["string"][language] += number_name

						if number_name != self.numbers["list"][language][-1]:
							self.numbers["string"][language] += "\n"

						i += 1

		for language in self.languages["small"]:
			if language in self.numbers["list_feminine"]:
				self.numbers["list_feminine"][language].extend(self.numbers["list"][language])

		i = 0
		for number in self.language_texts["first_numbers_feminine"]:
			if number != None:
				self.numbers["list_feminine"]["pt"][i] = number

			i += 1

		self.texts["number_names, type: list"] = self.numbers["list"]
		self.texts["number_names_feminine, type: list"] = self.numbers["list_feminine"]

		self.language_texts["number_names, type: list"] = self.JSON.Language.Item(self.numbers["list"])
		self.language_texts["number_names_feminine, type: list"] = self.JSON.Language.Item(self.numbers["list_feminine"])

	def Create_Years_List(self, mode = "list", start = 2018, plus = 0, function = str, string_format = None):
		if mode == "list":
			list_ = []

		if mode == "dict":
			dict_ = {}

		current_year = self.Now()["Units"]["Year"] + plus

		while start <= current_year:
			year = function(start)

			if string_format != None:
				year = string_format.format(year)

			if mode == "list":
				list_.append(year)

			if mode == "dict":
				dict_[start] = year

			start = int(start) + 1

		if mode == "list":
			return list_

		if mode == "dict":
			return dict_

	def Sleep(self, ms):
		import time
		time.sleep(ms)

	def Time_Text(self, time_string, language, add_original_time = False):
		language_texts = self.JSON.Language.Item(self.texts, language)

		time = time_string.split(":")
		hour = time[0]
		minute = time[1]

		if len(time) > 2:
			second = time[2]

		texts = {}

		time_keys = ["hours", "minutes", "seconds"]

		for item in time_keys:
			texts[item] = ""

		# Hours
		if hour not in ["0", "00"]:
			texts["hours"] = self.Text.By_Number(int(hour), language_texts["hour"], language_texts["hours"])

		# Minutes
		if minute not in ["0", "00"]:
			texts["minutes"] = self.Text.By_Number(int(minute), language_texts["minute"], language_texts["minutes"])

		# Seconds
		if len(time) > 2 and second not in ["0", "00"]:
			texts["seconds"] = self.Text.By_Number(int(second), language_texts["second"], language_texts["seconds"])

		text = ""

		if texts["hours"] != "":
			text += self.Text.Remove_Leading_Zeroes(hour) + " " + texts["hours"]

			if texts["minutes"] != "" and texts["seconds"] == "":
				text += " " + language_texts["and"] + " "

		if texts["hours"] != "" and texts["minutes"] != "" and texts["seconds"] != "" and texts["seconds"] != "00":
			text += ", "

		if texts["minutes"] != "":
			text += self.Text.Remove_Leading_Zeroes(minute) + " " + texts["minutes"]

		if texts["minutes"] != "" and texts["seconds"] != "":
			text += " " + language_texts["and"] + " "

		if texts["seconds"] != "" and texts["seconds"] != "00":
			text += self.Text.Remove_Leading_Zeroes(second) + " " + texts["seconds"]

		if add_original_time == True:
			text += " " + "("

			if texts["hours"] != "":
				text += str(self.Text.Add_Leading_Zeroes(hour)) + ":"

			if texts["minutes"] != "":
				text += str(self.Text.Add_Leading_Zeroes(minute)) + ":"

			if texts["seconds"] != "":
				text += str(self.Text.Add_Leading_Zeroes(second))

			text += ")"

		return text

	def Schedule_Task(self, task_title, path = "", start_time = "", time_from_now = 5):
		import win32com.client

		# Initiate
		scheduler = win32com.client.Dispatch("Schedule.Service")
		scheduler.Connect()
		root_folder = scheduler.GetFolder("\\Stake2")
		task_def = scheduler.NewTask(0)

		# Create trigger
		if start_time == "":
			start_time = self.Now()["Object"] + self.Timedelta(minutes = time_from_now)

		TASK_TRIGGER_TIME = 1 # Triggers the task at a specific time of day.
		trigger = task_def.Triggers.Create(TASK_TRIGGER_TIME)
		trigger.StartBoundary = start_time.isoformat()

		# Create action
		TASK_ACTION_EXEC = 0 # performs a command-line operation, for example, the action could run a script
		action = task_def.Actions.Create(TASK_ACTION_EXEC)
		action.ID = task_title

		if path != "":
			action.Path = path

		# Set parameters
		task_def.RegistrationInfo.Description = task_title
		task_def.Settings.AllowDemandStart = True
		task_def.Settings.AllowHardTerminate = True
		task_def.Settings.DisallowStartIfOnBatteries = False
		task_def.Settings.Enabled = True
		task_def.Settings.ExecutionTimeLimit = "PT0S"

		TASK_INSTANCES_STOP_EXISTING = 3
		task_def.Settings.MultipleInstances = False
		task_def.Settings.RunOnlyIfIdle = False
		task_def.Settings.StartWhenAvailable = False
		task_def.Settings.StopIfGoingOnBatteries = False

		# Register task
		# If task already exists, it will be updated
		TASK_CREATE_OR_UPDATE = 6
		TASK_LOGON_NONE = 0
		root_folder.RegisterTaskDefinition(
			task_title, # Task name
			task_def, # Task definition
			TASK_CREATE_OR_UPDATE, # 6, The Task Scheduler either registers the task as a new task or as an updated version if the task already exists
			"", # No user
			"", # No password
			TASK_LOGON_NONE # The logon method is not specified. Used for non-NT credentials. 
		)
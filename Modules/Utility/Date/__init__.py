# Date.py

from datetime import date, time, datetime, timedelta, timezone
from dateutil.relativedelta import relativedelta
from calendar import monthrange
from time import sleep
import pytz
import pandas as pd
from copy import deepcopy

class Date():
	def __init__(self):
		# Import the classes
		self.Import_Classes()

		# Define the folders of the module
		self.Define_Folders(object = self)

		# Define the texts of the module
		self.Define_Texts()

		# Generate the number names
		self.Number_Name_Generator()

		# Define the list of methods to be imported
		methods = [
			"sleep",
			"date",
			"time",
			"datetime",
			"timedelta",
			"timezone",
			"relativedelta",
			"combine"
		]

		# Define the globals variable for easier typing
		globals_dictionary = globals()

		# Iterate through the list of methods
		for key in methods:
			# If the method is in the globals dictionary
			if key in globals_dictionary:
				# Get the method
				method = globals_dictionary[key]

			# If the method key is "combine"
			if key == "combine":
				method = getattr(self.Datetime, "combine")

			# Add it to the object of this class
			setattr(self, key.capitalize(), method)

		self.date = self.Now()

	def Import_Classes(self):
		import importlib

		# ---------- #

		# Define the list of modules to be imported
		modules = [
			"Define_Folders",
			"JSON",
			"Text"
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

		# ---------- #

		# Define the "Language" class as the same class inside the "JSON" class
		self.Language = self.JSON.Language

		# Import some variables from the "Language" class

		# Import the "languages" dictionary
		self.languages = self.Language.languages

		# Import the "user" dictionary
		self.user = self.Language.user

	def Define_Texts(self):
		# Define the "Texts" dictionary
		self.texts = self.JSON.To_Python(self.module["Files"]["Texts"])

		# Define the "Language texts" dictionary
		self.language_texts = self.Language.Item(self.texts)

	def Now(self, date_parameter = None):
		# If the date parameter is not None
		if date_parameter != None:
			today = self.Datetime.now()

			# Only the date
			if type(date_parameter) == type(self.Date(today.year, today.month, today.day)):
				# Combine the provided date with the today time
				date_parameter = self.Combine(date_parameter, today.time())

			# Only the time
			if type(date_parameter) == type(self.Time(today.hour, today.minute)):
				# Combine the provided time with the today date
				date_parameter = self.Combine(self.Date(today.year, today.month, today.day), date_parameter)

		# If the date parameter is None
		if date_parameter == None:
			date_parameter = self.Datetime.now()

		# Define a shortcut to the user timezone
		user_timezone = self.user["Timezone"]

		# Define the user timezone variable
		timezone = {
			"String": str(user_timezone["String"]),
			"Name": "",
			"UTC offset": "",
			"Timezone information": user_timezone["Timezone information"]
		}

		# Remove the microsecond from the date object
		date_parameter = date_parameter.replace(microsecond = 0)

		# Get the user timezone using pytz and the user timezone information
		user_timezone = pytz.timezone(str(timezone["Timezone information"]))

		# Try to add the timezone to the date
		try:
			# Add the timezone to the date
			date_parameter = user_timezone.localize(date_parameter)

		except ValueError:
			pass

		# Define the date object in the user timezone
		user_timezone_date = deepcopy(date_parameter).astimezone(user_timezone)

		# Define the date dictionary
		date = {
			"User timezone": {
				"String": timezone["String"],
				"Name": user_timezone_date.strftime("%Z"),
				"UTC offset": user_timezone_date.strftime("%z"),
				"Timezone information": timezone["Timezone information"]
			},
			"Object": {},
			"Units": {},
			"Texts": {},
			"Formats": {},
			"UTC": {
				"Object": date_parameter.astimezone(pytz.UTC)
			},
			"Timezone": {
				"Object": user_timezone_date
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
						"Month days": 0,
						"Month": 0,
						"Year": 0,
						"Year days": 0
					},
					"Texts": {
						"Day name": {},
						"Day name with number": {},
						"Day gender": {},
						"Day": {},
						"Month name": {},
						"Month name with number": {}
					},
					"Formats": {
						"YYYY-MM-DD": "",
						"DD/MM/YYYY": "",
						"DD-MM-YYYY": "",
						"[Day] [Month name] [Year]": "",
						"[Day name], [Day] [Month name] [Year]": ""
					}
				}

				formats = [
					"%Y-%m-%d",
					"%d/%m/%Y",
					"%d-%m-%Y",
					"",
					""
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

					if hasattr(date[date_name][date_type]["Object"], data_key) == True:
						date[date_name][date_type]["Units"][key] = getattr(date[date_name][date_type]["Object"], data_key)

					if key == "Week day":
						date[date_name][date_type]["Units"][key] = date[date_name][date_type]["Units"][key]()

					if key == "Month days":
						date[date_name][date_type]["Units"][key] = self.Monthrange(year = date["UTC"]["Object"].year, month = date["UTC"][
						"Object"].month)[1]

					if key == "Year days":
						p = pd.Period(str(date[date_name][date_type]["Units"]["Year"]) + "-01-01")

						if p.is_leap_year:
						   days = 366

						else:
						   days = 365

						date[date_name][date_type]["Units"][key] = days

				# Add the date or time texts
				for key in date[date_name][date_type]["Texts"]:
					for language in self.languages["Small"]:
						if key == "Day name":
							# Get the week day number
							week_day_number = date[date_name][date_type]["Units"]["Week day"]

							# Get the day name and define it in the dictionary
							date[date_name][date_type]["Texts"][key][language] = self.texts["day_names, type: list"][language][week_day_number]

						# If the key is "Day name with number"
						elif key == "Day name with number":
							# Get the day number
							day_number = date[date_name][date_type]["Units"]["Day"]

							# Add leading zeroes to the day number
							day_number = str(self.Text.Add_Leading_Zeroes(day_number))

							# Get the week day number
							week_day_number = date[date_name][date_type]["Units"]["Week day"]

							# Get the day name
							day_name = self.texts["day_names, type: list"][language][week_day_number]

							# Add the day number and day name to the dictionary
							date[date_name][date_type]["Texts"][key][language] = day_number + " - " + day_name

						elif key == "Day":
							date[date_name][date_type]["Texts"][key][language] = self.Text.By_Number(date[date_name][date_type]["Units"][key], self.texts[key.lower()][language], self.texts[key.lower() + "s"][language])

						elif key == "Month name":
							date[date_name][date_type]["Texts"][key][language] = self.texts["month_names, type: list"][language][date[date_name][date_type]["Units"]["Month"]]

						elif key == "Month name with number":
							date[date_name][date_type]["Texts"][key][language] = str(self.Text.Add_Leading_Zeroes(date[date_name][date_type]["Units"]["Month"])) + " - " + self.texts["month_names, type: list"][language][date[date_name][date_type]["Units"]["Month"]]

						elif key == "Day gender":
							date[date_name][date_type]["Texts"][key][language] = self.texts["day_names_genders, type: list"][language][date[date_name][date_type]["Units"]["Week day"]]

						else:
							date[date_name][date_type]["Texts"][key][language] = self.Text.By_Number(date[date_name][date_type]["Units"][key], self.texts[key.lower()][language], self.texts[key.lower() + "s"][language])

				# Add the date or time formats
				i = 0
				for format in formats:
					format_key = list(date[date_name][date_type]["Formats"].keys())[i]

					date[date_name][date_type]["Formats"][format_key] = date[date_name]["Object"].strftime(format)

					format_list = [
						"[Day] [Month name] [Year]",
						"[Day name], [Day] [Month name] [Year]"
					]

					for format_name in format_list:
						if format_key == format_name:
							date[date_name][date_type]["Formats"][format_key] = {}

							template = self.texts["{} {} {}"]

							date_shortcut = date[date_name][date_type]

							if format_name == "[Day name], [Day] [Month name] [Year]":
								template = self.texts["{}, {} {} {}"]

							for language in self.languages["Small"]:
								items = []

								if format_name == "[Day name], [Day] [Month name] [Year]":
									items.append(date_shortcut["Texts"]["Day name"][language])

								items.extend([
									date[date_name][date_type]["Units"]["Day"],
									date[date_name][date_type]["Texts"]["Month name"][language],
									date[date_name][date_type]["Units"]["Year"]
								])

								date[date_name][date_type]["Formats"][format_key][language] = template[language].format(*items)

					i += 1

				#date[date_name][date_type]["Formats"]["Unix"] = self.Datetime(1970, 1, 1).replace(microsecond = 0).astimezone(pytz.UTC)
				#date[date_name][date_type]["Formats"]["Unix"] = self.Datetime(1970, 1, 1).astimezone(pytz.UTC)
				#date[date_name][date_type]["Formats"]["Unix"] = date["UTC"]["Object"] - date[date_name][date_type]["Formats"]["Unix"]
				#date[date_name][date_type]["Formats"]["Unix"] = date[date_name][date_type]["Formats"]["Unix"].total_seconds()

				date[date_name][date_type]["Formats"]["Unix"] = int(date[date_name]["Object"].timestamp())

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
				"HH:MM:SS DD/MM/YYYY",
				"YYYY-MM-DDTHH:MM:SSZ"
			]

			formats = [
				"%H:%M %d/%m/%Y",
				"%H:%M:%S %d/%m/%Y",
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

				if (
					object.strftime("%Z") not in ["UTC", ""] and
					format_key == "YYYY-MM-DDTHH:MM:SSZ"
				):
					#list_ = list(date[date_name]["DateTime"]["Formats"][format_key])
					#list_.insert(20, ":")

					#date[date_name]["DateTime"]["Formats"][format_key] = self.Text.From_List(list_)
					true = True

				i += 1

			# Import all of the variables from inside the "Timezone" dictionary since the modules usually use the timezone dates and times
			if date_name == "Timezone":
				date["Object"] = date[date_name]["Object"]

				for key in date[date_name]["DateTime"]:
					date[key] = date[date_name]["DateTime"][key]

		return date

	def Daylight_Saving_Time(self, date):
		# Returns True if the DST is different from zero
		return bool(date.dst())

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

			if date.strftime("%Z") in ["UTC", "", None]:
				date = date.replace(tzinfo = pytz.UTC)

		if format != "":
			date = self.Datetime.strptime(string, format)

		date = self.Now(date)

		return date

	def To_UTC(self, date):
		date = self.Now(date["UTC"]["Object"])

		return date

	def To_Timezone(self, date, utc = False):
		date = self.Check(date, utc)

		date = self.Now(date.astimezone())

		return date

	def Monthrange(self, year = None, month = None):
		arguments = [
			year,
			month
		]

		i = 0
		for argument in ["year", "month"]:
			if arguments[i] == None:
				arguments[i] = getattr(self.Datetime.now(), argument)

			i += 1

		return monthrange(*arguments)

	def Replace_Strings_In_Text(self, text, date, language):
		# Define the timezone datetime shortcut
		timezone_datetime = date["Timezone"]["DateTime"]

		# Iterate through the list of date attributes
		for attribute in self.texts["date_attributes, type: list"]["en"]:
			# Define the key of the attribute
			key = attribute.capitalize()

			# If the attribute is inside the text
			if attribute in text:
				# Define the attribute text
				attribute_text = "[" + attribute + "]"

				# Get the unit of the attribute
				unit = timezone_datetime["Units"][key]

				# Replace the attribute text with the unit
				text = text.replace(attribute_text, str(unit))

		# Iterate through the list of datetime texts
		for key in timezone_datetime["Texts"]:
			# Lower the key
			key = key.lower()

			# If the key is inside the text
			if key in text:
				# Define the attribute text
				attribute_text = "[" + key + "]"

				# Get the date text
				date_text = timezone_datetime["Texts"][key.capitalize()][language]

				# Replace the attribute text with the date text
				text = text.replace(attribute_text, date_text)

		# Return the text
		return text

	def Difference(self, before, after):
		# Define the dictionary
		dictionary = {
			"Before": before,
			"After": after,
			"Object": {},
			"Difference": {},
			"Unit texts": {},
			"Text": {},
			"Text (with time units)": {},
			"Time units text": ""
		}

		# Get the object of the "Before" and "After" dates
		for key in ["Before", "After"]:
			if type(dictionary[key]) == str:
				dictionary[key] = self.Check(dictionary[key])

			if type(dictionary[key]) == self.Datetime:
				dictionary[key] = self.Now(dictionary[key])

		# Define the object of the date difference, with the relative delta
		dictionary["Object"] = self.Relativedelta(dictionary["After"]["Object"], dictionary["Before"]["Object"])

		# Iterate through the plural date attributes list in English
		i = 0
		for key in self.texts["plural_date_attributes, type: list"]["en"]:
			# If the key is inside the list of keys of the "Object" dictionary
			# And the number is not zero
			if (
				key in dir(dictionary["Object"]) and
				getattr(dictionary["Object"], key) != 0
			):
				# Get the absolute value of the number
				number = abs(getattr(dictionary["Object"], key))

				# Transform the key into title case
				key = key.title()

				# Define the difference number as the absolute number
				dictionary["Difference"][key] = abs(number)

				# Create the unit text empty dictionary
				dictionary["Unit texts"][key] = {}

				# Define the text list
				text_list = self.texts["date_attributes, type: list"]

				# If the number is greater than one
				if number > 1:
					# Define the text list as its plural version
					text_list = self.texts["plural_date_attributes, type: list"]

				# Iterate through the list of small languages
				for language in self.languages["Small"]:
					# Define the unit text of the number in the current language
					dictionary["Unit texts"][key][language] = text_list[language][i]

			# Add one to the "i" number
			i += 1

		# Create the time text of the date difference
		dictionary["Text"] = self.Make_Time_Text(dictionary)

		# Create the time units text
		dictionary["Time units text"] = self.Create_Time_Units_Text(dictionary)

		# Iterate through the list of small languages
		for language in self.languages["Small"]:
			# Create the language key if it does not exist
			if language not in dictionary["Text (with time units)"]:
				# Define the language key as the text in the current language
				dictionary["Text (with time units)"][language] = dictionary["Text"][language]

			# Add the time units text to the full text
			dictionary["Text (with time units)"][language] += " (" + dictionary["Time units text"] + ")"

		# Return the dictionary
		return dictionary

	def Make_Time_Text(self, dictionary):
		# Import the "deepcopy" module
		from copy import deepcopy

		# Transform the "Text" key into a dictionary if it is a string
		if (
			"Text" in dictionary and
			type(dictionary["Text"]) == str
		):
			dictionary["Text"] = {}

		# If the "Difference" key is not in the dictionary
		if "Difference" not in dictionary:
			# Make a backup of the dictionary
			backup = deepcopy(dictionary)

			# Recreate the dictionary with the "Text" and "Dictionary" keys
			dictionary = {
				"Text": {},
				"Difference": dictionary
			}

			# If the "Units" key is in the backup dictionary
			# Define the date dictionary difference as the units
			if "Units" in backup:
				dictionary["Difference"] = backup["Units"]

		# Iterate through the list of small languages to create the language keys in the "Text" dictionary
		for language in self.languages["Small"]:
			dictionary["Text"][language] = ""

		# Define the list of keys in the date difference
		keys = list(dictionary["Difference"].keys())

		# Define the number of keys
		number_of_keys = len(keys)

		# Make the time texts by language
		for key in keys:
			for language in self.languages["Small"]:
				# Get the difference number
				number = str(dictionary["Difference"][key])

				# If the key is the last one
				# And the number of time attributes is 2 or more than 2
				if (
					key == keys[-1] and
					number_of_keys >= 2
				):
					# Add the "and " text in the current language
					dictionary["Text"][language] += self.Language.texts["and"][language] + " "

				# Define the text key
				text_key = key.lower()

				# Define the text key by singular or plural, based on the difference number
				text_key = self.Text.By_Number(dictionary["Difference"][key], text_key[:-1], text_key)

				# Define the time text in the current language
				text = self.texts[text_key][language]

				# If the "Unit texts" key is in the difference dictionary
				if "Unit texts" in dictionary:
					# Define the text as the unit text in the current language
					text = dictionary["Unit texts"][key][language]

				# Add the number and the time text (plural or singular)
				dictionary["Text"][language] += number + " " + text

				# If the number of time attributes is equal to 2, add a space
				if number_of_keys == 2:
					dictionary["Text"][language] += " "

				# If the key is not the last one
				# And the number of time attributes is more than 2, add the ", " text (comma)
				if (
					key != keys[-1] and
					number_of_keys > 2
				):
					dictionary["Text"][language] += ", "

		# Remove spaces at the end of the texts if they are present
		for key in dictionary["Text"]:
			# Get the text
			text = dictionary["Text"][key]

			# If there is a space, remove it
			if " " in text[-1]:
				text = text[:-1]

			# Update the text
			dictionary["Text"][key] = text

		# Return the "Text" dictionary
		return dictionary["Text"]

	def Create_Time_Units_Text(self, dictionary):
		# Define the list of time keys
		time_keys = [
			"Hours",
			"Minutes",
			"Seconds"
		]

		# Define the list of keys in the time difference
		keys = list(dictionary["Difference"].keys())

		# Define the number of keys
		number_of_keys = len(keys)

		# If the "Time units text" key is not present, create it
		dictionary["Time units text"] = ""

		# Iterate through the list of time keys
		for key in time_keys:
			# If the is not inside the time difference keys
			if key not in keys:
				# Define the "add" switch as False
				add = False

				# If the key is "Minutes"
				# And the time difference contains hours
				if (
					key == "Minutes" and
					"Hours" in keys
				):
					# Define the "add" switch as True
					add = True

				# If the key is "Seconds"
				# And the time difference contains minutes
				if (
					key == "Seconds" and
					"Minutes" in keys
				):
					# Define the "add" switch as True
					add = True

				# If the list time difference keys has only "Hours"
				if keys == ["Hours"]:
					# Define the "add" switch as True
					add = True

				# If the "add" switch is True
				if add == True:
					# If there is no colon on the end of the time units text, add it
					if ":" not in dictionary["Time units text"][-1]:
						dictionary["Time units text"] += ":"

					# Add the zero time units
					dictionary["Time units text"] += "00"

			# If the is inside the time difference keys
			if key in keys:
				# Define the number and add leading zeroes
				number = str(self.Text.Add_Leading_Zeroes(dictionary["Difference"][key]))

				# Add the number
				dictionary["Time units text"] += number

			# Add a colon to the time format
			# If the key is not the last one in the time keys list
			# And the last character is not a colon
			if (
				key != time_keys[-1] and
				dictionary["Time units text"] != "" and
				dictionary["Time units text"][-1] != ":"
			):
				dictionary["Time units text"] += ":"

		# Return the time format string
		return dictionary["Time units text"]

	def Number_Name_Generator(self):
		self.numbers = {}
		self.numbers["list"] = {}
		self.numbers["list_feminine"] = {}
		self.numbers["string"] = {}

		for language in self.languages["Small"]:
			self.numbers["list"][language] = ["zero"]
			self.numbers["list_feminine"][language] = []
			self.numbers["string"][language] = "zero\n"

		for language in self.languages["Small"]:
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

		for language in self.languages["Small"]:
			if language in self.numbers["list_feminine"]:
				self.numbers["list_feminine"][language].extend(self.numbers["list"][language])

		i = 0
		for number in self.language_texts["first_numbers_feminine"]:
			if number != None:
				self.numbers["list_feminine"]["pt"][i] = number

			i += 1

		self.texts["number_names, type: list"] = self.numbers["list"]
		self.texts["number_names_feminine, type: list"] = self.numbers["list_feminine"]

		self.language_texts["number_names, type: list"] = self.Language.Item(self.numbers["list"])
		self.language_texts["number_names_feminine, type: list"] = self.Language.Item(self.numbers["list_feminine"])

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
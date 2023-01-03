# Food_Time.py

from Global_Switches import Global_Switches as Global_Switches

from Language import Language as Language
from File import File as File
from Folder import Folder as Folder
from Date import Date as Date
from Input import Input as Input
from Text import Text as Text

class Food_Time():
	def __init__(self, parameter_switches = None, show_text = True, register_time = True):
		self.parameter_switches = parameter_switches

		self.show_text = show_text
		self.register_time = register_time

		self.Define_Basic_Variables()
		self.Define_Module_Folder()
		self.Define_Texts()

		self.Define_Lists_And_Dictionaries()

		if self.show_text == True:
			if self.register_time == True:
				self.Get_Time()
				self.Set_Timer()

			self.Show_Times()

	def Define_Basic_Variables(self):
		# Global Switches dictionary
		self.global_switches = Global_Switches().global_switches

		if self.parameter_switches != None:
			self.global_switches.update(self.parameter_switches)

		self.Language = Language(self.global_switches)
		self.File = File(self.global_switches)
		self.Folder = Folder(self.global_switches)
		self.Date = Date(self.global_switches)
		self.Input = Input(self.global_switches)
		self.Text = Text(self.global_switches)

		self.app_settings = self.Language.app_settings
		self.languages = self.Language.languages
		self.small_languages = self.languages["small"]
		self.full_languages = self.languages["full"]
		self.translated_languages = self.languages["full_translated"]

		self.user_language = self.Language.user_language
		self.full_user_language = self.Language.full_user_language

		self.Sanitize = self.File.Sanitize

		self.folders = self.Folder.folders
		self.root_folders = self.folders["root"]
		self.user_folders = self.folders["user"]
		self.apps_folders = self.folders["apps"]
		self.mega_folders = self.folders["mega"]
		self.notepad_folders = self.folders["notepad"]

		self.date = self.Date.date

	def Define_Module_Folder(self):
		self.module = self.__module__

		self.module = {
			"name": self.__module__,
		}

		if "." in self.module["name"]:
			self.module["name"] = self.module["name"].split(".")[0]

		if self.module["name"] == "__main__":
			self.module["name"] = "Food_Time"

		self.module["key"] = self.module["name"].lower()

		for item in ["module_files", "modules"]:
			self.apps_folders[item][self.module["key"]] = self.apps_folders[item]["root"] + self.module["name"] + "/"
			self.apps_folders[item][self.module["key"]] = self.Folder.Contents(self.apps_folders[item][self.module["key"]], lower_key = True)["dictionary"]

	def Define_Texts(self):
		self.texts = self.Language.JSON_To_Python(self.apps_folders["module_files"][self.module["key"]]["texts"])

		self.language_texts = self.Language.Item(self.texts)

		self.large_bar = "-----"
		self.dash_space = "-"

	def Define_Lists_And_Dictionaries(self):
		# Read Times.json file
		self.times = self.Language.JSON_To_Python(self.apps_folders["module_files"][self.module["key"]]["times"])

		# Iterate through time types
		for time_type in self.times["types"]:
			# If the dictionary of the time type is not present in JSON, add it
			if time_type not in self.times:
				# Define dictionary
				self.times[time_type] = {
					"time": self.times["times"][time_type],
				}

				# Define time unit
				if len(str(self.times[time_type]["time"])) == 1:
					self.times[time_type]["unit_name"] = "hours"

				if len(str(self.times[time_type]["time"])) == 2:
					self.times[time_type]["unit_name"] = "minutes"

				# Define unit name text
				self.times[time_type]["unit"] = self.texts[self.times[time_type]["unit_name"]]

				# Format "this_is_the_time_that_you" text with the time type text per language
				self.times[time_type]["texts"] = {}

				for language in self.small_languages:
					prefix = self.texts["this_is_the_time_that_you"][language] + " "

					self.times[time_type]["texts"][language] = prefix + self.texts[time_type][language]

	def Get_Time(self):
		# Iterate through time types
		for time_type in self.times["types"]:
			# If the time type is "ate", its date is only a normal date
			if time_type == "ate":
				self.times[time_type]["date"] = self.Date.Now()["date"]

			# If the time type is not "ate", its date is the "ate" date plus the timedelta of the time type "time to add"
			if time_type != "ate":
				dictionary = {
					self.times[time_type]["unit_name"]: self.times[time_type]["time"],
				}

				# Add the "ate" date to the timedelta of the "time to add" of the time type
				self.times[time_type]["date"] = self.Date.Now(self.times["ate"]["date"] + self.Date.Timedelta(**dictionary))["date"]

			# Format the date as "Hours:Minutes", "HH:MM"
			self.times[time_type]["time_string"] = self.Date.Now(self.times[time_type]["date"])["%H:%M"]

		# Stringfy "datetime" objects to write them into the JSON file
		for time_type in self.times["types"]:
			self.times[time_type]["date"] = str(self.times[time_type]["date"])

		# Write the new time type dictionaries with the stringfied datetimes
		self.File.Edit(self.apps_folders["module_files"][self.module["key"]]["times"], self.Language.Python_To_JSON(self.times), "w")

	def Set_Timer(self):
		# Define website timer to countdown to "will_be_hungry" time
		from urllib.parse import urlencode

		# Define URL template to use
		self.timer_url_template = "https://www.timeanddate.com/countdown/generic?"

		# Define default URL parameters
		parameters = {
			"p0": "543",
			"msg": self.language_texts["time_that_you_will_be_hungry"],
			"font": "slab",
		}

		self.timer_url_template = self.timer_url_template + urlencode(parameters)

		# Define English "minute" and "second" texts
		self.minute_and_second_texts = [
			self.Date.texts["minute"]["en"],
			self.Date.texts["second"]["en"],
		]

		self.timer_url = self.timer_url_template

		self.time_parameters = {}

		# Iterate through date and time attributes
		for attribute in self.Date.texts["date_attributes, type: list"]["en"]:
			self.time_parameters[attribute] = {
				"parameter": attribute,
			}

			# If the attribute name is "minute" or "second", remove the three last characters (for Time And Date URL to work)
			if attribute in self.minute_and_second_texts:
				self.time_parameters[attribute]["parameter"] = attribute[:-3]

			# If the attribute is the first one, then add "&" to start adding URL parameters
			if attribute == self.Date.texts["date_attributes, type: list"]["en"][0]:
				self.timer_url += "&"

			# Add the attribute name, an equals sign, and the attribute (from date)
			date = self.Date.From_String(self.times["will_be_hungry"]["date"], "%Y-%m-%d %H:%M:%S.%f")

			self.timer_url += self.time_parameters[attribute]["parameter"] + "=" + str(date[attribute])

			# If the attribute is not the last one, then add "&" to continue adding URL parameters
			if attribute != self.Date.texts["date_attributes, type: list"]["en"][-1]:
				self.timer_url += "&"

		# Open formatted timer URL with parameters
		#self.File.Open(self.timer_url)

		# Define scheduled task to play alarm sound when the "will_be_hungry" time is reached
		self.parameters = {
			"task_title": self.language_texts["play_alarm_sound_when_you_are_hungry"],
			"path": self.apps_folders["modules"][self.module["key"]]["play_alarm"]["__init__"],
			"start_time": self.times["will_be_hungry"]["date"],
		}

		#self.Date.Schedule_Task(**self.parameters)

	def Show_Times(self):
		print()
		print(self.language_texts["showing_the_meal_times_below"] + ":")

		# Iterate through time types
		for time_type in self.times["types"]:
			print()

			# Show time type text ("this_is_the_time_that_you" + the time type text in user language)
			print(self.times[time_type]["texts"][self.user_language] + ":")

			# Define the time as the date format (HH:MM)
			time = self.times[time_type]["time_string"]

			# If time type is not ate, add the time that is added into the "ate" time, examples: (ate + 40 minutes), (ate + 3 hours)
			if time_type != "ate":
				time += " ({} + {} {})".format(self.times["ate"]["time_string"], self.times[time_type]["time"], self.times[time_type]["unit"][self.user_language])

			print(time)
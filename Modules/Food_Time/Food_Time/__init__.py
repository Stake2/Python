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

		self.Define_Files()

		if self.show_text == True:
			if self.register_time == True:
				self.Get_Time()
				self.Define_Times()
				self.Register_Times()
				self.Set_Timer()

			if self.register_time == False:
				self.Get_Times_From_File()

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

		self.times = {
			"can_drink_water": 40,
			"will_be_hungry": 3,
		}

		self.time_units = {
			"can_drink_water": self.texts["minutes"],
			"will_be_hungry": self.texts["hours"],
		}

		self.show_texts = {}

		self.time_types = ["ate", "can_drink_water", "will_be_hungry"]

		for language in self.small_languages:
			self.show_texts[language] = {}

			prefix = self.texts["this_is_the_time_that_you"][language] + " "

			for time_type in self.time_types:
				self.show_texts[language][time_type] = prefix + self.texts[time_type][language]

	def Define_Files(self):
		self.file_path = self.notepad_folders["food_and_water_registers"]["food"]["root"] + "{}.txt"

		self.raw_times_file = self.file_path.format(self.texts["raw_times, en - pt"])
		self.File.Create(self.raw_times_file)

	def Get_Time(self):
		self.date = self.Date.Now()

		self.dates = {
			"ate": self.date,
			"can_drink_water": self.Date.Now(self.date["date"] + self.Date.Timedelta(minutes = self.times["can_drink_water"])),
			"will_be_hungry": self.Date.Now(self.date["date"] + self.Date.Timedelta(hours = self.times["will_be_hungry"])),
		}

		self.food_times = {
			"ate": self.dates["ate"]["%H:%M"],
			"can_drink_water": self.Date.Strftime(self.dates["can_drink_water"]["date"], format = "%H:%M"),
			"will_be_hungry": self.Date.Strftime(self.dates["will_be_hungry"]["date"], format = "%H:%M"),
		}

	def Define_Times(self):
		self.food_time_texts = {}

		for language in self.small_languages:
			self.food_time_texts[language] = {}

			for time_type in self.time_types:
				self.food_time_texts[language][time_type] = self.show_texts[language][time_type] + ": " + self.food_times[time_type]

				if time_type != "ate":
					self.food_time_texts[language][time_type] += " ({} + {} {})".format(self.food_times["ate"].split(" ")[0], self.times[time_type], self.time_units[time_type][language])

		self.language_food_time_texts = self.food_time_texts[self.user_language]

	def Register_Times(self):
		text_to_write = ""

		for food_time in self.food_times.values():
			text_to_write += food_time

			if food_time != list(self.food_times.values())[-1]:
				text_to_write += "\n"

		self.File.Edit(self.raw_times_file, text_to_write, "w")

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
			self.timer_url += self.time_parameters[attribute]["parameter"] + "=" + str(self.dates["will_be_hungry"][attribute])

			# If the attribute is not the last one, then add "&" to continue adding URL parameters
			if attribute != self.Date.texts["date_attributes, type: list"]["en"][-1]:
				self.timer_url += "&"

		# Open formatted timer URL with parameters
		self.File.Open(self.timer_url)

		# Define scheduled task to play alarm sound when the "will_be_hungry" time is reached
		self.parameters = {
			"task_title": self.language_texts["play_alarm_sound_when_you_are_hungry"],
			"path": self.apps_folders["modules"][self.module["key"]]["play_alarm"]["__init__"],
			"start_time": self.dates["will_be_hungry"]["date"],
		}

		self.Date.Schedule_Task(**self.parameters)

	def Get_Times_From_File(self):
		self.food_times = {}

		i = 0
		for food_time in self.File.Contents(self.raw_times_file)["lines"]:
			self.food_times[self.time_types[i]] = food_time

			i += 1

	def Show_Times(self):
		print()
		print(self.language_texts["showing_the_meal_times_below"] + ":")

		i = 0
		for food_time in self.File.Contents(self.raw_times_file)["lines"]:
			time_type = self.time_types[i]

			print()
			print(self.show_texts[self.user_language][time_type] + ":")

			if time_type != "ate":
				food_time += " ({} + {} {})".format(self.food_times["ate"].split(" ")[0], self.times[time_type], self.time_units[time_type][self.user_language])

			print(food_time)

			i += 1
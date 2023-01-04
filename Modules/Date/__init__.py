# Date.py

from Global_Switches import Global_Switches as Global_Switches

from Language import Language as Language
from Text import Text as Text

import os
import win32com.client
import time
from datetime import datetime, timedelta

class Date():
	def __init__(self, parameter_switches = None):
		# Global Switches dictionary
		self.global_switches = Global_Switches().global_switches

		self.global_switches.update({
			"folder": {
				"create": True,
			},
			"file": {
				"create": True,
			},
		})

		if parameter_switches != None:
			self.global_switches.update(parameter_switches)

		self.Language = Language(self.global_switches)
		self.Text = Text(self.global_switches)

		self.small_languages = self.Language.languages["small"]
		self.user_language = self.Language.user_language

		self.Define_Folders()
		self.Define_Texts()
		self.Number_Name_Generator()

		self.date = self.Now()

	def Define_Folders(self):
		self.app_text_files_folder = self.Language.app_text_files_folder

		self.module = {
			"name": self.__module__,
		}

		if "." in self.module["name"]:
			self.module["name"] = self.module["name"].split(".")[0]

		if __name__ == "__main__":
			self.module["name"] = "Date"

		self.module["key"] = self.module["name"].lower()

		self.module_text_files_folder = self.app_text_files_folder + self.module["name"] + "/"

		self.texts_file = self.module_text_files_folder + "Texts.json"

	def Sanitize(self, path):
		path = os.path.normpath(path).replace("\\", "/")

		if "/" not in path[-1] and os.path.splitext(path)[-1] == "":
			path += "/"

		return path

	def Create(self, item = None, text = None):
		item = self.Sanitize(item)

		if os.path.splitext(item)[-1] == "":
			if self.global_switches["folder"]["create"] == True and os.path.isdir(item) == False:
				os.mkdir(item)

		if os.path.splitext(item)[-1] != "":
			if self.global_switches["file"]["create"] == True and os.path.isfile(item) == False:
				create = open(item, "w", encoding = "utf8")
				create.close()

		return item

	def Define_Texts(self):
		self.texts = self.Language.JSON_To_Python(self.texts_file)

		self.language_texts = self.Language.Item(self.texts)

	def Now(self, date_parameter = None):
		date = {}

		if date_parameter == None:
			date["date"] = datetime.now()

		if date_parameter != None:
			date["date"] = date_parameter

		# Day
		date["day"] = date["date"].day
		date["weekday"] = date["date"].weekday()
		date["day_name"] = self.language_texts["day_names, type: list"][date["weekday"]]

		date["day_names"] = {}

		for language in self.small_languages:
			date["day_names"][language] = self.texts["day_names, type: list"][language][date["weekday"]]

		# Month
		date["month"] = date["date"].month
		date["month_name"] = self.language_texts["month_names, type: list"][date["month"]]

		date["month_names"] = {}

		for language in self.small_languages:
			date["month_names"][language] = self.texts["month_names, type: list"][language][date["month"]]

		# Year
		date["year"] = date["date"].year

		# Time
		date["time"] = date["date"].time()
		date["hour"] = date["date"].hour
		date["minute"] = date["date"].minute
		date["second"] = date["date"].second

		# Date formats
		date["%d/%m/%Y"] = date["date"].strftime("%d/%m/%Y")
		date["%d-%m-%Y"] = date["date"].strftime("%d-%m-%Y")

		date["date_format"] = {}

		for language in self.small_languages:
			date["date_format"][language] = date["date"].strftime(self.texts["date_format"][language])

		# Time formats
		date["%H:%M"] = date["date"].strftime("%H:%M")

		# Date time formats
		date["date_time_format"] = {}

		for language in self.small_languages:
			date["date_time_format"][language] = date["date"].strftime(self.texts["date_time_format"][language])

		date["ISO8601"] = date["date"].strftime("%Y-%m-%dT%H:%M:%S")
		date["%Y-%m-%dT%H:%M:%S"] = date["ISO8601"]
		date["%Y-%m-%d %H:%M:%S"] = date["date"].strftime("%Y-%m-%d %H:%M:%S")
		date["%H:%M %d/%m/%Y"] = date["date"].strftime("%H:%M %d/%m/%Y")

		return date

	def Timedelta(self, **arguments):
		return timedelta(**arguments)

	def Strftime(self, date, format = "%H:%M %d/%m/%Y"):
		date = date.strftime(format)

		return date

	def From_String(self, string, format = "%H:%M %d/%m/%Y"):
		date = datetime.strptime(string, format)

		date = self.Now(date)

		return date

	def Difference(self, before, after, format = "%H:%M %d/%m/%Y"):
		date = {}

		date["before"] = before

		if type(date["before"]) == str:
			date["before"] = self.From_String(before, format)

		date["after"] = after

		if type(date["after"]) == str:
			date["after"] = self.From_String(after, format)

		string = date["after"]["date"] - date["before"]["date"]

		date["difference"] = {}

		texts = self.texts.copy()

		for attribute in texts["plural_date_attributes, type: list"]["en"]:
			if hasattr(string, attribute):
				date["difference"][attribute] = getattr(string, attribute)

		if hasattr(string, "years") == False and "days" in date["difference"]:
			if (date["difference"]["days"] // 365) != 0:
				date["difference"]["years"] = date["difference"]["days"] // 365
		
			if (date["difference"]["days"] // 365) == 0:
				date["difference"]["years"] = 0

		if date["difference"]["years"] == -1:
			date["difference"]["years"] = 0

		date["difference"]["year_days"] = 0
		date["difference"]["month_days"] = 0

		if (date["difference"]["days"] // 365) not in [0, 1]:
			date["difference"]["year_days"] = date["difference"]["years"] * 365

		if hasattr(string, "months") == False and ((date["difference"]["days"] - date["difference"]["year_days"]) // 30) != 0:
			date["difference"]["months"] = (date["difference"]["days"] - date["difference"]["year_days"]) // 30
			date["difference"]["month_days"] = date["difference"]["months"] * 30

		date["difference"]["days"] = date["difference"]["days"] - date["difference"]["year_days"] - date["difference"]["month_days"]

		if "seconds" not in date["difference"]:
			date["difference"]["seconds"] = 0

		date["difference"]["seconds"] = date["difference"]["seconds"] % (24 * 3600)
		date["difference"]["hours"] = date["difference"]["seconds"] // 3600
		date["difference"]["seconds"] %= 3600
		date["difference"]["minutes"] = date["difference"]["seconds"] // 60 
		date["difference"]["seconds"] %= 60

		singular = {}
		plural = {}

		i = 0
		for attribute in texts["plural_date_attributes, type: list"]["en"]:
			if attribute in date["difference"] and date["difference"][attribute] != 0:
				for language in self.small_languages:
					if language not in singular:
						singular[language] = []

					if language not in plural:
						plural[language] = []

					singular_attribute = texts["date_attributes, type: list"][language][i]
					plural_attribute = texts["plural_date_attributes, type: list"][language][i]

					singular[language].append(singular_attribute)
					plural[language].append(plural_attribute)

			if attribute in date["difference"] and date["difference"][attribute] == 0:
				del date["difference"][attribute]

			i += 1

		texts["date_attributes, type: list"] = singular

		texts["plural_date_attributes, type: list"] = plural

		language_texts = self.Language.Item(texts)

		date["difference_strings"] = {}
		date["difference_string"] = ""

		i = 0
		for attribute in texts["plural_date_attributes, type: list"]["en"]:
			if attribute in date["difference"]:
				if attribute != texts["plural_date_attributes, type: list"]["en"][0]:
					date["difference_string"] += ", "

				date["difference_string"] += str(date["difference"][attribute])

				list_ = language_texts["date_attributes, type: list"]

				if date["difference"][attribute] > 1:
					list_ = language_texts["plural_date_attributes, type: list"]

				date["difference_string"] += " " + list_[i]

			i += 1

		i = 0
		for attribute in texts["plural_date_attributes, type: list"]["en"]:
			if attribute in date["difference"]:
				for language in self.small_languages:
					if language not in date["difference_strings"]:
						date["difference_strings"][language] = ""

					if attribute != texts["plural_date_attributes, type: list"]["en"][0]:
						date["difference_strings"][language] += ", "

					date["difference_strings"][language] += str(date["difference"][attribute])

					list_ = texts["date_attributes, type: list"][language]

					if date["difference"][attribute] > 1:
						list_ = texts["plural_date_attributes, type: list"][language]

					date["difference_strings"][language] += " " + list_[i]

			i += 1

		return date

	def Number_Name_Generator(self):
		self.numbers = {}
		self.numbers["list"] = {}
		self.numbers["list_feminine"] = {}
		self.numbers["string"] = {}

		for language in self.small_languages:
			self.numbers["list"][language] = ["zero"]
			self.numbers["list_feminine"][language] = []
			self.numbers["string"][language] = "zero\n"

		for language in self.small_languages:
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

		for language in self.small_languages:
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

		current_year = self.Now()["year"] + plus

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
		time.sleep(ms)

	def Time_Text(self, time, language, add_original_time = False):
		language_texts = self.Language.Item(self.texts, language)

		time = time.split(":")
		hour = time[0]
		minute = time[1]

		if len(time) > 2:
			second = time[2]

		texts = {}

		time_keys = ["hours", "minutes", "seconds"]

		for item in time_keys:
			texts[item] = ""

		# Hours
		if hour != "0":
			texts["hours"] = self.Text.By_Number(int(hour), language_texts["hour"], language_texts["hours"])

		# Minutes
		if minute != "00":
			texts["minutes"] = self.Text.By_Number(int(minute), language_texts["minute"], language_texts["minutes"])

		# Seconds
		if len(time) > 2 and second != "00":
			texts["seconds"] = self.Text.By_Number(int(second), language_texts["second"], language_texts["seconds"])

		text = ""

		if texts["hours"] != "":
			text += self.Text.Remove_Leading_Zeros(hour) + " " + texts["hours"]

			if texts["minutes"] != "" and texts["seconds"] == "":
				text += " " + language_texts["and"] + " "

		if texts["hours"] != "" and texts["minutes"] != "" and texts["seconds"] != "":
			text += ", "

		if texts["minutes"] != "":
			text += self.Text.Remove_Leading_Zeros(minute) + " " + texts["minutes"]

		if texts["minutes"] != "" and texts["seconds"] != "":
			text += language_texts["and"] + ", "

		if texts["seconds"] != "":
			text += self.Text.Remove_Leading_Zeros(second) + " " + texts["seconds"]

		if add_original_time == True:
			text += " " + "("

			if texts["hours"] != "":
				text += str(self.Text.Add_Leading_Zeros(hour)) + ":"

			if texts["minutes"] != "":
				text += str(self.Text.Add_Leading_Zeros(minute)) + ":"

			if texts["seconds"] != "":
				text += str(self.Text.Add_Leading_Zeros(second))

			text += ")"

		return text

	def Schedule_Task(self, task_title, path = "", start_time = "", time_from_now = 5):
		# Initiate 
		scheduler = win32com.client.Dispatch("Schedule.Service")
		scheduler.Connect()
		root_folder = scheduler.GetFolder("\\Stake2")
		task_def = scheduler.NewTask(0)

		# Create trigger
		if start_time == "":
			start_time = self.Now()["date"] + self.Timedelta(minutes = time_from_now)

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
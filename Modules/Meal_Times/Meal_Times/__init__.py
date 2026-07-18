# Meal_Times.py

# Import some useful modules
import importlib
from copy import deepcopy

# Define the main "Meal_Times" class
class Meal_Times():
	def __init__(self):
		# Define the variables of the class
		self.Define_Variables()

		# ---------- #

		# Define the root "Meal_Times" (class) dictionary
		self.meal_times = {
			# Define the root "Show" (times) switch initially as True
			# (To always show the meal times by default)
			"Show": True,

			# Define the root "Register" switch initially as True
			# (To always register the meal times when no active arguments are present)
			"Register": True,

			# Define the meal times text initially as "registered in"
			"Text": self.language_texts["registered_in"],

			# Define the empty "Reminders" dictionary
			"Reminders": {}
		}

		# Define the "Reminders" dictionary
		self.Define_Reminders()

		# If this class has an arguments dictionary
		if self.has_arguments == True:
			# Parse the arguments
			# (The dictionary of arguments was received from the "Module_Selector" module)
			self.Parse_Arguments()

		# Define the meal times dictionary
		self.Define_Times()

		# If the root "Show" (times) switch is True
		if self.meal_times["Show"] == True:
			# Show the meal times
			self.Show_Times()

		# If there is an active reminder
		if self.meal_times["Reminders"]["Active"] != {}:
			# Create a shortcut to the reminder dictionary
			reminder = self.meal_times["Reminders"]["Active"]

			# Run the method of the reminder
			reminder["Method"]()

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
			"File",
			"Text"
		]

		# Define a list of optional utility classes to import
		optional_classes = [
			"Task_Scheduler"
		]

		# Iterate through the list of utility classes
		for class_title in self.modules["Utility"]["List"]:
			# If the class is not already inside the self class (Meal_Times)
			if hasattr(self, class_title) == False:
				# If the class title is not inside the list of utility classes to not import
				# And it is is not inside the list of optional classes
				# Or it is inside the list of optional classes to import
				if (
					class_title not in do_not_import and
					class_title not in self.modules["Utility"]["Optional"] or
					class_title in optional_classes
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

	def Define_Reminders(self):
		# Define a local reminders dictionary
		reminders = {
			"Numbers": {
				"Total": 0
			},
			"List": [
				"Drink water",
				"Go eat"
			],
			"Dictionary": {},
			"Active": {}
		}

		# Update the total number of reminders with the length of the list of reminders
		reminders["Numbers"]["Total"] = len(reminders["List"])

		# Iterate through the reminders in the list of reminders
		for reminder_name in reminders["List"]:
			# Create the default reminder dictionary
			reminder = {
				# Define the "Texts" dictionary of the reminder
				"Texts": {},

				# Define the empty "File" and "Method" keys
				"File": "",
				"Method": "",

				# Define the reminder switch initially as False
				"Switch": False
			}

			# Define the text key for the reminder as "Remind the user to " plus the reminder name
			text_key = "Remind the user to " + reminder_name.lower()

			# Make it lowercase and replace spaces with underscores
			text_key = text_key.lower().replace(" ", "_")

			# Get the texts dictionary for the reminder
			reminder["Texts"] = self.texts[text_key]

			# ----- #

			# Define the file name for the reminder as the reminder text in the user language
			file_name = reminder["Texts"][self.language["Small"]]

			# Create a shortcut to the "Bats" Python shortcuts folder
			bats_folder = self.folders["Python"]["Shortcuts"]["Bats"]

			# Define the bat file for the reminder
			# (The bat file will be used to run the reminder)
			reminder["File"] = bats_folder["root"] + file_name + ".bat"

			# ----- #

			# Define the method name for the reminder as the reminder text in English
			method_name = reminder["Texts"]["en"]

			# Remove the " the" text
			method_name = method_name.replace(" the", "")

			# Make it title case and replace spaces with underscores
			method_name = method_name.title().replace(" ", "_")

			# Get the method for the reminder using the method name
			reminder["Method"] = getattr(self, method_name)

			# ----- #

			# Add the local reminder dictionary to the root reminders "Dictionary"
			reminders["Dictionary"][reminder_name] = reminder

		# Define the root "Reminders" dictionary as the local one
		self.meal_times["Reminders"] = reminders

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
				# Switch the root "Register" switch to False
				# (So the meal times will not be registered)
				self.meal_times["Register"] = False

				# Change the root meal times text to be "obtained from"
				self.meal_times["Text"] = self.language_texts["obtained_from"]

			# If the "Remind" text is inside the argument key
			# And its value is True
			if (
				"Remind" in key and
				argument["Value"] == True
			):
				# Switch the root "Register" switch to False
				# (So the meal times will not be registered)
				self.meal_times["Register"] = False

				# Switch the root "Show" switch to False
				# (So the meal times will not be shown)
				self.meal_times["Show"] = False

				# Iterate through the reminder names and dictionaries inside the "Reminders" dictionary
				for reminder_name, reminder in self.meal_times["Reminders"]["Dictionary"].items():
					# If the lowercase reminder name is inside the argument key
					if reminder_name.lower() in key:
						# Switch the reminder "Switch" to True
						reminder["Switch"] = True

						# Define it as the active reminder
						self.meal_times["Reminders"]["Active"] = reminder

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
				},
				"Reminder": {}
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

				# Remove the "Reminder" dictionary as it is not needed
				# (The "Ate" time does not need a reminder cause it is the first and now time)
				time.pop("Reminder")

			# If the meal times do not need to be registered, only shown
			if self.meal_times["Register"] == False:
				# Read the "Times.json" file to get its JSON dictionary and define it as the local times dictionary
				local_times = self.JSON.To_Python(self.module["Files"]["Times"])

				# Get the local time dictionary using the current time name as a key
				local_time = local_times["Dictionary"][time_name]

				# Change the "Current" time dictionary to be the one inside the "Times.json" file
				time["Current time"] = local_time["Current time"]

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

				# ----- #

				# Create shortcuts to the "Ate" time and "Time to add" unit
				ate_time = self.times["Dictionary"]["Ate"]["Current time"]["Time"]
				unit = time["Time to add"]["Unit"][self.language["Small"]]

				# Define the time text as the time that is added to the "Ate" time
				# 
				# Examples:
				# (12:30 + 40 minutes)
				# (12:30 + 3 hours)
				time_text = " ({} + {} {})".format(
					ate_time,
					quantity,
					unit
				)

				# Define the current "Added time" key as the time text defined above
				time["Current time"]["Added time"] = time_text

				# Define the current "Time with added time" key as the "Time" key plus the "Added time"
				time["Current time"]["Time with added time"] = time["Current time"]["Time"] + time["Current time"]["Added time"]

				# ----- #

				# Define the reminder name of the time initially as "Drink water"
				reminder_name = "Drink water"

				# If the time name is "Will be hungry"
				if time_name == "Will be hungry":
					# Change the reminder name to be "Go eat"
					reminder_name = "Go eat"

				# Get the root reminder dictionary using the reminder name
				reminder = self.meal_times["Reminders"]["Dictionary"][reminder_name].copy()

				# Convert the method of the reminder into a string
				reminder["Method"] = str(reminder["Method"].__name__)

				# Define the "Reminder" key inside the time dictionary as the reminder dictionary
				time["Reminder"] = reminder

			# If the meal times do not need to be registered, only shown
			# And the time name is not "Ate"
			if (
				self.meal_times["Register"] == False and
				time_name != "Ate"
			):
				# Define the current "Time with added time" key as the "Time" key plus the backup of the "Added time"
				time["Current time"]["Time with added time"] = time["Current time"]["Time"] + time["Current time"]["Added time"]

			# If the meal times need to be registered
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

				# If the time name is not "Ate"
				if time_name != "Ate":
					# Define the current "Time with added time" key as the "Time" key plus the "Added time"
					time["Current time"]["Time with added time"] = time["Current time"]["Time"] + time["Current time"]["Added time"]

					# Create the task dictionary to be used to schedule a task using Windows Task Scheduler
					task = {
						# Define the task title as the reminder text in the user language
						"Title": reminder["Texts"][self.language["Small"]],

						# Define the task time as the task time object
						"Time": date,

						# Define the custom time as the "Time with added time"
						"Custom time": time["Current time"]["Time with added time"],

						# Define the task file as the reminder file
						"File": reminder["File"]
					}

					# Schedule the task using the "Schedule_Task" method of the "Task_Scheduler" utility class
					self.Task_Scheduler.Schedule_Task(task)

			# Add the local time dictionary to the root times "Dictionary"
			self.times["Dictionary"][time_name] = time

		# Create a local copy of the root times dictionary
		local_times = deepcopy(self.times)

		# Define a list of keys to remove
		to_remove = [
			"Added time",
			"Time with added time"
		]

		# Iterate through the times in the local copy of the dictionary of times
		for time in local_times["Dictionary"].values():
			# Iterate through the keys inside the list of keys to remove
			for key in to_remove:
				# If the key is present
				if key in time["Current time"]:
					# Remove it
					time["Current time"].pop(key)

			# If the time contains a reminder
			if "Reminder" in time:
				# Convert the method of the reminder into a string
				time["Reminder"]["Method"] = str(time["Reminder"]["Method"])

				# Remove the "Switch" key
				time["Reminder"].pop("Switch")

		# Update the "Times.json" file with the updated local copy of the "Times" dictionary
		self.JSON.Edit(self.module["Files"]["Times"], local_times)

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
				# Change the local time text to be the "Time with added time"
				time_text = time["Current time"]["Time with added time"]

			# Show the local time text
			print(time_text)

	def Show_Header(self):
		# Show the module name in the user language
		print(self.language_texts["Meal_Times"] + ".py" + ":")

		# Show a space
		print()

		# Play a sound to alert the user
		sound_file = self.module["Folders"]["Files"]["root"] + "Ninja Dance Emote (Fortnite).mp3"

		# Define the media player
		media_player = self.folders["Program Files"]["VideoLAN"]["VLC"]["VLC"]

		# Define the list of commands
		commands = [
			# Hide the media player window
			"--intf",
			"dummy",

			# Play the sound file and exit the media player
			"--play-and-exit",

			# Define the volume to be 256
			"--volume",
			"256",

			# The sound file to play
			"file:///" + sound_file
		]

		self.System.Open(media_player, open = True, commands = commands, verbose = False)

	def Remind_User_To_Drink_Water(self):
		# Show the header of the module and play the alarm sound
		self.Show_Header()

		# Create a shortcut to the "Block input" AutoHotKey script
		block_input = self.folders["Programming"]["AutoHotKey"]["Block input"]

		# Block the user input using an "AutoHotKey" script, allowing the user to press "Enter" to unblock the user input
		self.System.Open(block_input, verbose = False)

		# Show the user their water drinking time
		print(self.language_texts["your_water_drinking_time_is"] + ":")

		# Get the water drinking time text
		time_text = self.times["Dictionary"]["Can drink water"]["Current time"]["Time with added time"]

		# Show it
		print(time_text)

		# Show a space
		print()

		# Tell the user that it is time to drink water
		print(self.language_texts["now_it_is_time_to_drink_water"])

		# ----- #

		# Define the input text as "Press Enter when you pick up your water bottle to drink" text
		input_text = self.language_texts["press_enter_when_you_pick_up_your_water_bottle_to_drink"]

		# Ask for user input before continuing
		# (When the user presses "Enter", the user input will be unblocked)
		self.Input.Type(input_text)

		# End the execution of the module
		quit()

	def Remind_User_To_Go_Eat(self):
		# Show the header of the module and play the alarm sound
		self.Show_Header()

		# Show the user their eating time
		print(self.language_texts["your_eating_time_is"] + ":")

		# Get the eating time text
		time_text = self.times["Dictionary"]["Will be hungry"]["Current time"]["Time with added time"]

		# Show it
		print(time_text)

		# Show a space
		print()

		# Tell the user that it is time to go eat something
		print(self.language_texts["now_it_is_time_to_go_drink_something"])

		# ----- #

		# Define the input text as "Press Enter when you choose and open a video to watch on YouTube while you eat" text
		input_text = self.language_texts["press_enter_when_you_choose_and_open_a_video_to_watch_on_youtube_while_you_eat"]

		# Ask for user input before continuing
		self.Input.Type(input_text)

		# Create a shortcut to the "Block input" AutoHotKey script
		block_input = self.folders["Programming"]["AutoHotKey"]["Block input"]

		# Block the user input using an "AutoHotKey" script, allowing the user to press "Enter" to unblock the user input
		self.System.Open(block_input, verbose = False)

		# Define the input text as "Press Enter when you are finished making something to eat while watching" text
		input_text = self.language_texts["press_enter_when_you_are_finished_making_something_to_eat_while_watching"]

		# Ask for user input before continuing
		# (When the user presses "Enter", the user input will be unblocked)
		self.Input.Type(input_text)

		# End the execution of the module
		quit()
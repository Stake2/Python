# Task_Scheduler.py

# Import some useful modules
import win32com.client

# Define the main "Task_Scheduler" class
class Task_Scheduler():
	def __init__(self):
		# Define the variables of the class
		self.Define_Variables()

		# Start the Task Scheduler service inside this class
		self.Start_Task_Scheduler()

	def Define_Variables(self):
		import importlib

		# Define the list of modules to be imported
		classes = [
			"Modules",
			"Global_Switches",
			"JSON",
			"Text"
		]

		# Iterate through the list of classes to import
		for class_title in classes:
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

		# Define the "Language" class as the same class inside the "JSON" class
		self.Language = self.JSON.Language

		# Import some attributes from the "Language" class

		# Import the "language" dictionary
		self.language = self.Language.language

		# Import the "user" dictionary
		self.user = self.Language.user

		# ---------- #

		# Define the module dictionary and the module folders and files
		self.Modules(class_object = self, utility_mode = True)

		# ---------- #

		# Get the "Switches" dictionary from the "Global_Switches" module
		self.switches = self.Global_Switches.switches["Global"]

		# ---------- #

		# Define the "Texts" dictionary
		self.texts = self.JSON.To_Python(self.module["Files"]["Texts"])

		# Define the "Language texts" dictionary
		self.language_texts = self.Language.Item(self.texts)

	def Verbose(self, text, item = None, verbose = True, first_space = True, item_tab = "\t"):
		import inspect

		# Define the verbose text
		verbose_text = ""

		# If the "first space" parameter is True
		if first_space == True:
			# Add a first space
			verbose_text += "\n"

		# Get the name of the method which ran this method (the "Verbose" one)
		runner_method_name = inspect.stack()[1][3]

		# Add the module name (System) and the method which ran this method (the "Verbose" one) to the verbose text
		verbose_text += self.module["Module"] + "." + runner_method_name + "():"

		# If the tab is not in the text, add it
		if "\t" not in text[0]:
			text = "\t" + text

		# Add the text to the verbose text
		verbose_text += "\n" + text + ":"

		# If the item is not None, show it
		if item != None:
			# Add the verbose item with the item tab to the verbose text
			verbose_text += "\n" + item_tab + item

		# If the "Verbose" switch is True
		# And the verbose parameter is None
		# Or the verbose parameter is True
		if (
			self.switches["Verbose"] == True and
			verbose == None or
			verbose == True
		):
			# Show the verbose text
			print(verbose_text)

		# Return the verbose text
		return verbose_text

	def Start_Task_Scheduler(self):
		# Create a COM object for the Windows Task Scheduler engine
		# This gives access to the Task Scheduler API (Schedule.Service)
		self.task_scheduler = win32com.client.Dispatch("Schedule.Service")

		# Establish a connection to the Task Scheduler service running on the local machine
		# After connecting, we can navigate folders and register or get tasks
		self.task_scheduler.Connect()

	def Schedule_Task(self, task):
		# If the "Folder" key is not present inside the task dictionary
		# Or it is and is empty
		if (
			"Folder" not in task or
			"Folder" in task and
			task["Folder"] == ""
		):
			# Define the task folder as the user name folder
			task["Folder"] = self.user["Name"]

		# Get the task folder and define it as the task folder
		task["Task folder"] = self.task_scheduler.GetFolder("\\" + task["Folder"])

		# ----- #

		# Define a new task inside the Task Scheduler
		task["Definition"] = self.task_scheduler.NewTask(0)

		# Define the task description as the task title
		task["Definition"].RegistrationInfo.Description = task["Title"]

		# ----- #

		# Define the task trigger time
		# (1 starts the task at a specific time of the day)
		TASK_TRIGGER_TIME = 1

		# Define the task trigger inside the task definition
		task["Trigger"] = task["Definition"].Triggers.Create(TASK_TRIGGER_TIME)

		# Define the ID of the task trigger as the task title
		task["Trigger"].ID = task["Title"]

		# Define a local task time as the task "Time" key
		task_time = task["Time"]

		# If the "Time" key is a dictionary
		# And the "Object" key is inside it
		if (
			type(task["Time"]) == dict and
			"Object" in task["Time"]
		):
			# Change the local task time to be the "Object" task time key
			task_time = task_time["Object"]

		# Define the start time of the task trigger using the "Time" inside the task dictionary
		task["Trigger"].StartBoundary = task_time.isoformat()

		# ----- #

		# Define the task action
		# (0 performs a command-line operation, for example running a program or a script)
		TASK_ACTION_EXEC = 0

		# Define the task action inside the task definition
		task["Action"] = task["Definition"].Actions.Create(TASK_ACTION_EXEC)

		# Define the ID of the task action as the task title with accents removed
		task["Action"].ID = self.Text.Remove_Accents(task["Title"])

		# Define the task path as the task file
		task["Action"].Path = task["File"]

		# ----- #

		# Allow the task to be started on demand (in addition to running via triggers)
		task["Definition"].Settings.AllowDemandStart = True

		# Allow the Task Scheduler to terminate the task using a hard/forceful kill
		# (If False, it will try to stop it more gracefully)
		task["Definition"].Settings.AllowHardTerminate = True

		# Prevent the task from starting when the computer is running on battery power
		# (Here it is False, so the task is allowed to start on batteries)
		task["Definition"].Settings.DisallowStartIfOnBatteries = False

		# Do not stop the task if the computer is running on batteries 
		task["Definition"].Settings.StopIfGoingOnBatteries = False

		# Enable the task
		task["Definition"].Settings.Enabled = True

		# What to do with existing instances of the task when a new instance is started
		# (3 means to "Stop existing instances", the scheduler stops running instances and starts a new one)
		TASK_INSTANCES_STOP_EXISTING = 3

		# Define the "Instances stop existing" inside the "MultipleInstances" setting as the value defined above
		task["Definition"].Settings.MultipleInstances = TASK_INSTANCES_STOP_EXISTING

		# Set the maximum allowed runtime for the task, uses ISO 8601 duration format
		# "PT0S" means "no time limit"
		task["Definition"].Settings.ExecutionTimeLimit = "PT0S"

		# Do not run the task only if the computer is idle (False)
		task["Definition"].Settings.RunOnlyIfIdle = False

		# Start the task as soon as the scheduler/conditions allow if a scheduled run was missed
		# (Here it is False, so it will not auto-start after being missed)
		task["Definition"].Settings.StartWhenAvailable = False

		# ----- #

		# Creation flag used when registering the task
		# (6 means to "Create or update", register it as new if it does not exist, otherwise update the existing task)
		TASK_CREATE_OR_UPDATE = 6

		# Logon type used when registering the task
		# (0 corresponds to "Logon none", the task is registered without specifying a user logon method)
		TASK_LOGON_NONE = 0

		# Define the task path as the task title
		task["Path"] = task["Title"]

		# Define a local "register task" switch initially as True
		register_task = True

		# If the "Testing" switch is True
		if self.switches["Testing"] == True:
			# Then switch the "register task" switch to False
			register_task = False

		# If the local "register task" is True
		if register_task == True:
			# Register the task in Windows Task Scheduler under the user-specific folder
			# If the task already exists, it will be updated
			task["Task folder"].RegisterTaskDefinition(
				# Add the task path
				task["Path"],

				# Add the task definition (actions, triggers, and settings)
				task["Definition"],

				# Add the "Create or update" flag
				# (6 means to "Create or update", register it as new if it does not exist, otherwise update the existing task)
				TASK_CREATE_OR_UPDATE,

				# Do not specify a user
				# (This is paired with TASK_LOGON_NONE to indicate no explicit user logon)
				"",

				# Do not specify a password
				# (Left blank because no user credentials are being provided)
				"",

				# Add the logon method flag
				# (0 corresponds to "Logon none", the task is registered without specifying a user logon method)
				TASK_LOGON_NONE 
			)

			# Define the verbose text as "This task was scheduled"
			verbose_text = self.language_texts["this_task_was_{}"].format(self.Language.language_texts["scheduled, feminine"])

			# Define the verbose item as the task title
			item = task["Title"]

			# Add two new lines
			item += "\n\n"

			# Add the "It will be executed at" text in the user language
			item += "\t" + self.language_texts["it_will_be_executed_at"] + ":" + "\n"

			# Define a local task time as the "[Day] [Month Name] [Year] at [Hour] [Minute]" format of the task time
			task_time = task["Time"]["Formats"]["[Day] [Month Name] [Year] at [Hour] [Minute]"]

			# If the "Custom time" key is inside the task dictionary
			if "Custom time" in task:
				# Change the local task time to be the custom time
				task_time = task["Custom time"]

			# Add the task time
			item += "\t" + task_time

		# If the local "register task" is False
		if register_task == False:
			# Define the verbose text as "This task was not scheduled (the testing mode is on)"
			verbose_text = self.language_texts["this_task_was_not_{}_the_testing_mode_is_on"].format(self.Language.language_texts["scheduled, feminine"])

			# Define the verbose item as the task title
			item = task["Title"]

		# Show the verbose text saying that the task was scheduled and showing the task time
		self.Verbose(verbose_text, item)

	def Delete_Task(self, task):
		# If the "Folder" key is not present inside the task dictionary
		# Or it is and is empty
		if (
			"Folder" not in task or
			"Folder" in task and
			task["Folder"] == ""
		):
			# Define the task folder as the user name folder
			task["Folder"] = self.user["Name"]

		# Get the task folder
		task["Folder"] = self.task_scheduler.GetFolder("\\" + task["Folder"])

		# Delete the task
		task_folder.DeleteTask(task_name, 0)

		# Define the verbose text as "This task was deleted"
		verbose_text = self.language_texts["this_task_was_{}"].format(self.Language.language_texts["deleted, feminine"])

		# Show the verbose text saying that the task was deleted
		self.Verbose(verbose_text, task["Title"])
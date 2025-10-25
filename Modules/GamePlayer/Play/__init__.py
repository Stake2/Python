# Play.py

from GamePlayer.GamePlayer import GamePlayer as GamePlayer

class Play(GamePlayer):
	def __init__(self, dictionary = {}, open_game = True):
		# If this module has the "arguments" variable, which was received from the "Module_Selector.py" module
		if hasattr(self, "arguments") == True:
			# Add it to the parent class
			setattr(GamePlayer, "arguments", self.arguments)

		# Initiate the root class and import its variables and methods
		super().__init__()

		# If this module has the "arguments" variable, which was received from the "Module_Selector.py" module
		if hasattr(self, "arguments") == True:
			# Parse the arguments
			self.Parse_Arguments()

		# Import sub-classes method
		self.Import_Sub_Classes()

		# Define the class dictionary as the parameter dictionary
		self.dictionary = dictionary

		# Define the states dictionary, importing the "open game" parameter
		self.states = {
			"Open game": open_game
		}

		# Define the game dictionary
		self.Define_Game_Dictionary()

		# Show information about the game
		self.Show_Information(self.dictionary)

		# If the "Open game" state is True
		# And the "Testing" switch is False
		if (
			self.states["Open game"] == True and
			self.switches["Testing"] == False
		):
			# Open the game
			self.Open_Game()

		# Register the gaming session
		self.Register_The_Session()

	def Import_Sub_Classes(self):
		# Import the "importlib" module
		import importlib

		# Define the classes to be imported
		classes = [
			"Register"
		]

		# Import them
		for title in classes:
			# Import the module
			module = importlib.import_module("." + title, self.__module__.split(".")[0])

			# Get the sub-class
			sub_class = getattr(module, title)

			# Add the sub-class to the current module
			setattr(self, title, sub_class)

	def Define_Game_Dictionary(self):
		# If the "Automatically selected class" switch exists
		# And the class (Play) was automatically selected
		if (
			hasattr(self, "automatically_selected_class") == True and
			self.automatically_selected_class == True
		):
			# If the "Verbose" switch is False
			if self.switches["Verbose"] == False:
				# Show a ten dash space separator
				print()
				print(self.separators["10"])

			# Define the class name
			class_name = self.Language.language_texts["play, title()"]

			# Show the module and class name
			print()
			print("GamePlayer." + class_name + "():")

		# Select the game type and the game if the dictionary is empty
		if self.dictionary == {}:
			# Define the default value for the game title variable
			game_title = None

			# If there is a game inside the arguments dictionary
			# That means the module has been run by the "Module_Selector"
			# And the game inside the arguments will be auto-selected
			if "Game" in self.arguments:
				game_title = self.arguments["Game"]["Value"]

			# ---------- #

			# Define the default value for the sub-game title variable
			sub_game_title = None

			# If there is a sub-game inside the arguments dictionary
			# That means the module has been run by the "Module_Selector"
			# And the sub-game inside the arguments will be auto-selected
			if "Sub-game" in self.arguments:
				sub_game_title = self.arguments["Sub-game"]["Value"]

			# ---------- #

			# Ask the user to select a game type and game
			self.dictionary = self.Select_Game_Type_And_Game(game_title = game_title, sub_game_title = sub_game_title, play = True)

		# Define a shortcut for the "Game" dictionary
		self.game = self.dictionary["Game"]

		# Define the playing status list for "Plan to play" related statuses
		status_list = [
			self.texts["plan_to_play, title()"][self.language["Small"]],
			self.Language.texts["on_hold, title()"][self.language["Small"]]
		]

		# If the game playing status is inside the status list
		if self.game["Details"][self.Language.language_texts["status, title()"]] in status_list:
			# Change the playing status to "Playing"
			self.Change_Status(self.dictionary, self.language_texts["playing, title()"])

		# If the game "Dates.txt" file is empty
		if self.File.Contents(self.game["Folders"]["dates"])["lines"] == []:
			# Get the first playing time where the user started playing the game (which is now)
			self.game["Started playing time"] = self.Date.Now()["Formats"]["HH:MM DD/MM/YYYY"]

			# Create the game dates text in the "Dates" key, with the "When I started to play" text
			self.game["Dates"] = self.language_texts["when_i_started_playing"] + ":\n"
			self.game["Dates"] += self.game["Started playing time"]

			# Add that date to the "Dates.txt" file
			self.File.Edit(self.game["Folders"]["dates"], self.game["Dates"], "w")

			# Transform the "Dates" string into a dictionary
			# With the text as key and the date as value
			# (This is to be used in the "Show_Information" root method to show the game dates)
			self.game["Dates"] = {
				self.language_texts["when_i_started_playing"]: self.game["Started playing time"]
			}

	def Open_Game(self):
		# If the "Bat" key is inside the dictionary of files
		if "Bat" in self.game["Files"]:
			# Open the bat file (probably a file that runs a Python created for the game)
			self.System.Open(self.game["Files"]["Bat"])

			# Ask for user input after the user finishes using the Python module of the game
			self.Input.Type(self.language_texts["press_enter_when_you_finish_using_the_python_module_of_the_game"])

		# Define shortcuts for the game platform and gaming environment
		platform = self.game["Platform"]
		gaming_environment = self.game["Gaming environment"]

		# If the game platform and gaming environment are the same
		if platform == gaming_environment:
			# Open the game file
			self.System.Open(self.game["Files"]["Shortcut"]["File"])

		# If the gaming environment is "NVIDIA GeForce Now"
		if gaming_environment[self.language["Small"]] == "NVIDIA GeForce Now":
			# Define the browser in which to open the game
			browser = "Google Chrome"

			# Define the link template
			template = "https://play.geforcenow.com/games?game-id={}&lang={}&asset-id={}&utm_source=shortcut"

			# Define a list of items to use to format the link template
			items = [
				self.game["Game ID"],
				self.language["With country"],
				self.game["Asset ID"]
			]

			# Format the link with the list of items to get the game link
			game_link = template.format(*items)

			# Open the link to the game
			self.System.Open_Link(game_link, browser = browser)

	def Register_The_Session(self):
		# Show a five dash space separator
		print()
		print(self.separators["5"])
		print()

		# ---------- #

		# Ask the user to press Enter to start counting the gaming time
		if self.states["Open game"] == True:
			# If the "Testing" switch is False
			if self.switches["Testing"] == False:
				self.Input.Type(self.language_texts["press_enter_to_start_counting_the_gaming_time"], first_space = False)

			else:
				# Show only the text
				print(self.language_texts["press_enter_to_start_counting_the_gaming_time"] + ":")

		# Define the entry dictionary, the "Before" time (now)
		self.dictionary["Entry"] = {
			"Session duration": {
				"Before": self.Date.Now(),
				"After": {}
			},
			"Times": {
				"Started playing": {},
				"Finished playing": {},
				"Finished playing (UTC)": {},
				"Gaming session duration": {}
			}
		}

		# Define the "Started playing" time as the "Before" time
		self.dictionary["Entry"]["Times"]["Started playing"] = self.dictionary["Entry"]["Session duration"]["Before"]

		# If the "Open game" state is True
		if self.states["Open game"] == True:
			# Show a space
			print()

		# ---------- #

		# Show the current time when the user starts playing the game
		print(self.Date.language_texts["now, title()"] + ":")
		print("\t" + self.dictionary["Entry"]["Session duration"]["Before"]["Formats"]["HH:MM DD/MM/YYYY"])

		# If the "Open game" state is True
		if self.states["Open game"] == True:
			# If the "Testing" switch is False
			if self.switches["Testing"] == False:
				# Ask the user to press Enter when they finish playing the game
				self.Input.Type(self.language_texts["press_enter_when_you_finish_playing_the_game"])

			else:
				# Show only the text
				print()
				print(self.language_texts["press_enter_when_you_finish_playing_the_game"] + ":")

		# ---------- #

		# Set the "Finished playing" state to True
		self.game["States"]["Finished playing"] = True

		# Define the "After" time (now, but after playing)
		self.dictionary["Entry"]["Session duration"]["After"] = self.Date.Now()

		# If the "Testing" switch is True
		if self.switches["Testing"] == True:
			# Add 2 hours, 30 minutes, and 28 seconds to the gaming session time, for testing purposes
			self.dictionary["Entry"]["Session duration"]["After"] = self.Date.Now(self.dictionary["Entry"]["Session duration"]["Before"]["Object"] + self.Date.Relativedelta(hours = 2, minutes = 30, seconds = 28))

		# Show the time after the user finishes playing the game
		print()
		print(self.Date.language_texts["after, title()"] + ":")
		print("\t" + self.dictionary["Entry"]["Session duration"]["After"]["Formats"]["HH:MM DD/MM/YYYY"])

		# ---------- #

		# Define shortcuts for the start and finish times
		start_time = self.dictionary["Entry"]["Session duration"]["Before"]
		finish_time = self.dictionary["Entry"]["Session duration"]["After"]

		# Calculate the time difference between the start and finish times
		self.dictionary["Entry"]["Session duration"]["Difference"] = self.Date.Difference(start_time, finish_time)

		# Define the "Gaming session duration" key as the session duration difference
		self.dictionary["Entry"]["Times"]["Gaming session duration"] = self.dictionary["Entry"]["Session duration"]["Difference"]

		# Show the session duration text in the user language
		print()
		print(self.Language.language_texts["gaming_session_duration"] + ":")
		print("\t" + self.dictionary["Entry"]["Times"]["Gaming session duration"]["Text"][self.language["Small"]])

		# ---------- #

		# Register the finished playing time in the "Times" dictionary
		time_key = "Finished playing"
		self.dictionary["Entry"]["Times"][time_key] = self.dictionary["Entry"]["Session duration"]["After"]

		# Register the finished playing time in the UTC time
		self.dictionary["Entry"]["Times"][time_key + " (UTC)"] = self.dictionary["Entry"]["Times"][time_key]

		# ---------- #

		# Calculate the gaming time
		self.dictionary["Game"] = self.Calculate_Gaming_Time(self.dictionary)

		# If the game has sub-games
		if self.game["States"]["Has sub-games"] == True:
			# And the sub-game title is not the same as the game title
			if self.game["Sub-game"]["Title"] != self.game["Title"]:
				# Calculate the gaming time for the sub-game
				self.dictionary["Game"]["Sub-game"] = self.Calculate_Gaming_Time(self.dictionary, item = True)

			# And the sub-game title is the same as the game title
			if self.game["Sub-game"]["Title"] == self.game["Title"]:
				# Calculate the gaming time for the sub-game which is the root game
				self.dictionary["Game"]["Sub-game"] = self.Calculate_Gaming_Time(self.dictionary, item = False)

		# ---------- #

		# Use the "Register" class to register the played game, and giving the dictionary to it
		if self.Register != None:
			self.Register(self.dictionary)
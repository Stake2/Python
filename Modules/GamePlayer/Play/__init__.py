# Play.py

from GamePlayer.GamePlayer import GamePlayer as GamePlayer

class Play(GamePlayer):
	def __init__(self, dictionary = {}, open_game = True):
		# If this module has the "arguments" variable, which was received from the "Module_Selector.py" module
		if hasattr(self, "arguments") == True:
			# Add it to the parent class
			setattr(GamePlayer, "arguments", self.arguments)

		super().__init__()

		# If this module has the "arguments" variable, which was received from the "Module_Selector.py" module
		if hasattr(self, "arguments") == True:
			# Parse the arguments
			self.Parse_Arguments()

		# Import sub-classes method
		self.Import_Sub_Classes()

		self.dictionary = dictionary
		self.open_game = open_game

		self.Define_Game_Dictionary()

		self.Show_Information(self.dictionary)

		if self.open_game == True:
			self.Open_Game()

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
		# Select the game type and the game if the dictionary is empty
		if self.dictionary == {}:
			game_title = None

			# If there is a game inside the arguments dictionary
			# That means the module has been run by the "Module_Selector"
			# And the game inside the arguments will be auto-selected
			if "Game" in self.arguments:
				game_title = self.arguments["Game"]["Value"]

			# Ask the user to select a game type and game
			self.dictionary = self.Select_Game_Type_And_Game(game_title = game_title, play = True)

		self.game = self.dictionary["Game"]

		# Define the playing status list for "Plan to play" related statuses
		status_list = [
			self.texts["plan_to_play, title()"][self.user_language],
			self.Language.texts["on_hold, title()"][self.user_language]
		]

		# If the game playing status is inside the status list
		if self.game["Details"][self.Language.language_texts["status, title()"]] in status_list:
			# Change the playing status to "Playing"
			self.Change_Status(self.dictionary, self.language_texts["playing, title()"])

		# If the game "Dates.txt" file is empty
		if self.File.Contents(self.game["Folders"]["dates"])["lines"] == []:
			# Get the first playing time where the user started playing the game
			self.game["Started playing time"] = self.Date.Now()["Formats"]["HH:MM DD/MM/YYYY"]

			# Create the Dates text
			self.game["Dates"] = self.language_texts["when_i_started_to_play"] + ":\n"
			self.game["Dates"] += self.game["Started playing time"]

			self.File.Edit(self.game["Folders"]["dates"], self.game["Dates"], "w")

	def Open_Game(self):
		if self.switches["testing"] == False:
			if "Bat" in self.game["Files"]:
				self.System.Open(self.game["Files"]["Bat"])

				self.Input.Type(self.language_texts["press_enter_when_you_finish_using_the_python_module_of_the_game"])

			self.System.Open(self.game["Files"]["Shortcut"]["File"])

	def Register_The_Session(self):
		# Show a five dash space separator
		print()
		print(self.separators["5"])
		print()

		# ---------- #

		# Ask the user to press Enter to start counting the session time
		if self.open_game == True:
			self.Input.Type(self.language_texts["start_counting_the_session_time"], first_space = False)

		# Define the Entry dictionary and the "Before" time (now)
		self.dictionary["Entry"] = {
			"Session duration": {
				"Before": self.Date.Now(),
				"After": {}
			}
		}

		if self.open_game == True:
			print()

		# ---------- #

		# Show the now time
		print(self.Date.language_texts["now, title()"] + ":")
		print("\t" + self.dictionary["Entry"]["Session duration"]["Before"]["Formats"]["HH:MM DD/MM/YYYY"])

		if self.open_game == True:
			self.Input.Type(self.language_texts["press_enter_when_you_finish_playing_the_game"])

		# ---------- #

		self.game["States"]["Finished playing"] = True

		# Define the "After" time (now, but after playing)
		self.dictionary["Entry"]["Session duration"]["After"] = self.Date.Now()

		if self.switches["testing"] == True:
			self.dictionary["Entry"]["Session duration"]["After"] = self.Date.Now(self.dictionary["Entry"]["Session duration"]["Before"]["Object"] + self.Date.Relativedelta(hours = 2, minutes = 30, seconds = 28))

		# Show the after time (after playing the game)
		print()
		print(self.Date.language_texts["after, title()"] + ":")
		print("\t" + self.dictionary["Entry"]["Session duration"]["After"]["Formats"]["HH:MM DD/MM/YYYY"])

		# ---------- #

		# Define the time difference
		self.dictionary["Entry"]["Session duration"]["Difference"] = self.Date.Difference(self.dictionary["Entry"]["Session duration"]["Before"], self.dictionary["Entry"]["Session duration"]["After"])

		# Get the difference text
		self.dictionary["Entry"]["Session duration"]["Text"] = self.dictionary["Entry"]["Session duration"]["Difference"]["Text"]

		# Get the time units of the time difference
		self.dictionary["Entry"]["Session duration"]["Difference"] = self.dictionary["Entry"]["Session duration"]["Difference"]["Difference"]

		# Show the session duration text in the user language
		print()
		print(self.language_texts["session_duration"] + ":")
		print("\t" + self.dictionary["Entry"]["Session duration"]["Text"][self.user_language])

		# ---------- #

		# Register the finished playing time
		self.dictionary["Entry"]["Date"] = self.dictionary["Entry"]["Session duration"]["After"]

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
				# Calculate the gaming time for the sub-game
				self.dictionary["Game"]["Sub-game"] = self.Calculate_Gaming_Time(self.dictionary, item = True)

		# ---------- #

		# Use the "Register" class to register the played game, and giving the dictionary to it
		if self.Register != None:
			self.Register(self.dictionary)
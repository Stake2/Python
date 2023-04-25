# Play.py

from GamePlayer.GamePlayer import GamePlayer as GamePlayer

class Play(GamePlayer):
	def __init__(self, dictionary = {}):
		super().__init__()

		import importlib

		classes = [
			"Register"
		]

		for title in classes:
			class_ = getattr(importlib.import_module("."  + title, "GamePlayer"), title)
			setattr(self, title, class_)

		self.dictionary = dictionary

		self.Define_Game_Dictionary()
		self.Show_Information(self.dictionary)
		self.Open_Game()
		self.Register_The_Session()

		'''
			self.File.Delete(self.played_time_backup_file)

			self.game_dictionary["texts"] = {
				"Games": self.game["name"],
				"Number": int(self.File.Contents(self.game_played_files["Number"])["lines"][0]) + 1,
				"Game categories": self.game["category"]["name"],
				"Times": self.Date.Now()["%H:%M %d/%m/%Y"],
				"Time spent": self.game_dictionary["time_list"]["en"] + " - " + self.game_dictionary["time_list"]["pt"],
			}

			for language in self.languages["small"]:
				translated_language = self.languages["full_translated"][language]["en"]
				text = self.texts["i_played_the_{}_game_called_{}_for_{}_current_time_{}"][language]

				self.game_dictionary["texts"][translated_language + " played time"] = text.format(self.game["category"]["names"][language], self.game["name"], self.game_dictionary["time_list"][language], self.now_time)
		'''

	def Define_Game_Dictionary(self):
		# Select the game type and the game if the dictionary is empty
		if self.dictionary == {}:
			# Ask the user to select a game type and game
			self.dictionary = self.Select_Game_Type_And_Game()

		self.game = self.dictionary["Game"]

	def Open_Game(self):
		if self.switches["testing"] == False:
			if "Bat" in self.game["Files"]:
				self.File.Open(self.game["Files"]["Bat"])

				self.Input.Type(self.language_texts["press_enter_when_you_finish_using_the_python_module_of_the_game"])

			self.File.Open(self.game["Files"]["Shortcut"])

	def Register_The_Session(self):
		print()
		print(self.large_bar)
		print()

		# Ask the user to press Enter to start counting the session time
		self.Input.Type(self.language_texts["start_counting_the_session_time"], first_space = False)

		# Define the Entry dictionary and the "Before" time (now)
		self.dictionary["Entry"] = {
			"Session duration": {
				"Before": self.Date.Now(),
				"After": ""
			}
		}

		print()
		print(self.Date.language_texts["now, title()"] + ":")
		print(self.dictionary["Entry"]["Session duration"]["Before"]["hh:mm DD/MM/YYYY"])

		text = self.language_texts["press_enter_when_you_finish_playing_the_game"]

		self.game["States"]["Finished playing"] = self.Input.Type(text)
		self.game["States"]["Finished playing"] = True

		# Define the "After" time (now, after playing)
		#self.dictionary["Entry"]["Session duration"]["After"] = self.Date.Now()
		self.dictionary["Entry"]["Session duration"]["After"] = self.Date.Now(self.Date.Now()["date"] + self.Date.Timedelta(hours = 1))

		print()
		print(self.Date.language_texts["after, title()"] + ":")
		print(self.dictionary["Entry"]["Session duration"]["After"]["hh:mm DD/MM/YYYY"])

		# Define the time difference
		self.dictionary["Entry"]["Session duration"]["Difference"] = self.Date.Difference(self.dictionary["Entry"]["Session duration"]["Before"], self.dictionary["Entry"]["Session duration"]["After"])

		# Define the time difference text key
		self.dictionary["Entry"]["Session duration"]["Text"] = self.dictionary["Entry"]["Session duration"]["Difference"]["Text"]

		# Register the finished playing time
		self.dictionary["Entry"]["Time"] = self.dictionary["Entry"]["Session duration"]["After"]

		# Use the "Register" class to register the played game, and giving the dictionary to it
		if self.Register != None:
			self.Register(self.dictionary)
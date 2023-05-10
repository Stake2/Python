# Iterate_Through_The_Game_List.py

from GamePlayer.GamePlayer import GamePlayer as GamePlayer

class Iterate_Through_The_Game_List(GamePlayer):
	def __init__(self):
		super().__init__()

		from copy import deepcopy

		# Iterate through English game types list
		i = 0
		for game_type in self.game_types["Types"]["en"]:
			# Define the key of the game type for getting game type folders
			key = game_type.lower().replace(" ", "_")

			# Define the language game type
			language_game_type = self.game_types["Types"][self.user_language][i]

			# Get game with all "watching statuses", not just the "Watching" and "Re-watching" ones
			game_list = self.Get_Game_List(self.game_types[game_type], self.texts["statuses, type: list"]["en"])

			# Sort the game item list as case insensitive
			game_list = sorted(game_list, key = str.lower)

			# Show language game type
			print()
			print("----------")
			print()
			print(language_game_type + ":")

			game_types_to_remove = []

			# Remove a game type from the list (optional)
			if game_type not in game_types_to_remove:
				# For game in game item list
				for self.game_title in game_list:
					# Define root dictionary with game type and game
					self.dictionary = {
						"Type": self.game_types[game_type],
						"Game": {
							"Title": self.game_title
						}
					}

					# Select game and define its variables, returning the game dictionary (without asking user to select the game)
					self.dictionary = self.Select_Game(self.dictionary)

					self.game = self.dictionary["Game"]

					self.Show_Information(self.dictionary)

					# Add missing game information
					self.Add_Game_Information()

			if self.switches["testing"] == True and game_type != self.game_types["Types"]["en"][-1] and game_type not in game_types_to_remove:
				self.Input.Type(self.JSON.Language.language_texts["continue, title()"])

			i += 1

	def Add_Game_Information(self):
		if hasattr(self, "Add_A_New_Game") == False:
			from GamePlayer.Manage.Add_A_New_Game import Add_A_New_Game as Add_A_New_Game

			self.Add_A_New_Game = Add_A_New_Game

		self.Add_A_New_Game(self.dictionary)
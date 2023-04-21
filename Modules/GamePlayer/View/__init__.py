# View.py

from GamePlayer.GamePlayer import GamePlayer as GamePlayer

class View(GamePlayer):
	def __init__(self):
		super().__init__()

		self.Select_Game_Type()

		self.Select_View_Type()

		self.Select_Game_Type_Item()
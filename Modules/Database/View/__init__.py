# View.py

from Database.Database import Database as Database

class View(Database):
	def __init__(self):
		super().__init__()

		self.Select_Type()

		self.Select_View_Type()

		self.Select_Type_Item()
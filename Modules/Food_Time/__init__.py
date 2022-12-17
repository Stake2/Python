# Food_Time.py

from Food_Time.Food_Time import Food_Time as Food_Time

class Run(Food_Time):
	def __init__(self, register_time = True):
		super().__init__(register_time = register_time)
# Food_Time.py

class Run():
	def __init__(self):
		if hasattr(self, "register_time") == False:
			self.register_time = True

		from Food_Time.Food_Time import Food_Time as Food_Time

		setattr(Food_Time, "register_time", self.register_time)

		self.Food_Time = Food_Time()

separate_arguments = [
	"set",
	"check"
]
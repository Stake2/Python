# Food_Time.py

class Run():
	def __init__(self):
		from Food_Time.Food_Time import Food_Time as Food_Time

		# If the self object (Run) has the "arguments" dictionary
		# Add it to the module sub-class
		if hasattr(self, "arguments") == True:
			setattr(Food_Time, "arguments", self.arguments)

		self.Food_Time = Food_Time()

# Define the custom arguments for the module
custom_arguments = [
	"set",
	"check"
]
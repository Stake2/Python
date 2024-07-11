# Food_Time.py

class Run():
	def __init__(self):
		from Food_Time.Food_Time import Food_Time as Food_Time

		# If the self object (Run) has the "arguments" dictionary
		# Add it to the module sub-class
		if hasattr(self, "arguments") == True:
			setattr(Food_Time, "arguments", self.arguments)

		# If the "Do not run class" variable is not present in this class
		if hasattr(self, "do_not_run_class") == False:
			# Run the "Food_Time" class
			self.Food_Time = Food_Time()

# Define the custom arguments for the module
custom_arguments = [
	"set",
	"check"
]
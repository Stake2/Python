# Diary_Slim.py

class Run():
	def __init__(self):
		# Run the root class of the "Modules" module
		self.Modules(class_object = self, select_class = True)

# Define the list of alternative arguments that can be used to run the module
alternative_arguments = [
	"slim"
]

# If the script is being executed directly, run the local "Run" class
if __name__ == "__main__":
	Run()
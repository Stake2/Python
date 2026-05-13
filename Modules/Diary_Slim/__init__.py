# Diary_Slim.py

class Run():
	def __init__(self):
		# Run the root class of the "Modules" module
		self.Modules(object = self, select_class = True)

# Define the alternative arguments for the module
alternative_arguments = [
	"slim"
]

# If the script is being executed directly, run the local "Run" class
if __name__ == "__main__":
	Run()
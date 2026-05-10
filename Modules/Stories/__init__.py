# Stories.py

class Run():
	def __init__(self):
		# Run the root class of the "Modules" module
		self.Modules(object = self, select_class = True)

# Define the list of alternate arguments for the module
alternate_arguments = [
	"story"
]

# If the "__name__" variable is "__main__"
if __name__ == "__main__":
	# Run the "Run" class to select a sub-class of the module
	Run()
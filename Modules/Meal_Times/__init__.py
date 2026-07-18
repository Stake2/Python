# Meal_Times.py

class Run():
	def __init__(self):
		# Run the root class of the "Modules" module
		self.Modules(class_object = self, module_files = "Times", select_class = True, return_class = True)

		# Define the root "has arguments" switch initially as False
		self.has_arguments = False

		# Define the "has active arguments" variable as False
		has_active_arguments = False

		# Create a shortcut to the "Classes" dictionary for faster typing
		classes = self.module["Classes"]

		# If the self object (Run) contains the "arguments" dictionary
		if hasattr(self, "arguments") == True:
			# Switch the root local "has arguments" switch to True
			self.has_arguments = True

			# Impot the "deepcopy" module
			from copy import deepcopy

			# Make a local copy of the arguments dictionary
			arguments_copy = deepcopy(self.arguments)

			# Define the "Active arguments" key as a dictionary
			self.arguments["Active arguments"] = {}

			# Iterate through the list of arguments
			for name, argument in arguments_copy.items():
				# If the argument action is "store_true"
				# And the argument value is True
				# (Different from the default value of the "store_true" action, which is "False")
				if (
					argument["Action"] == "store_true" and
					argument["Value"] == True
				):
					# Add the argument to the "Active arguments" dictionary
					self.arguments["Active arguments"][name] = argument

					# Then the arguments dictionary has active arguments
					has_active_arguments = True

			# Add the "has arguments" switch to the selected class object
			setattr(classes["Selected"]["Object"], "has_arguments", self.has_arguments)

			# Add the dictionary arguments to the selected class object
			setattr(classes["Selected"]["Object"], "arguments", self.arguments)

		# Run the object of the selected class
		classes["Selected"]["Object"]()

# Define the dictionary of custom arguments for the module to change the behavior of the class
custom_arguments = {
	"register": {
		"Action": "store_true"
	},
	"show": {
		"Action": "store_true"
	},
	"remind_user_to_drink_water": {
		"Action": "store_true"
	},
	"remind_user_to_go_eat": {
		"Action": "store_true"
	}
}

# If this script file is being executed directly, run the local "Run" class
if __name__ == "__main__":
	Run()
# GamePlayer.py

# Import the "importlib" module
import importlib

class Run():
	def __init__(self):
		# Run its root class
		self.Modules = self.Modules(object = self, select_class = False)

		# Define the "has active arguments" variable as False
		has_active_arguments = False

		# If the self object (Run) contains the "arguments" dictionary
		if hasattr(self, "arguments") == True:
			from copy import deepcopy

			# Make a local copy of the arguments dictionary
			arguments_copy = deepcopy(self.arguments)

			# Define the "Active arguments" key as a dictionary
			self.arguments["Active arguments"] = {}

			# Iterate through the list of arguments
			for name, argument in arguments_copy.items():
				# If the argument action is "store"
				# And the argument value is not "None"
				# (Different from the default value of the "store" action, which is "None")
				# Or the argument action is "store_true"
				# And the argument value is True
				# (Different from the default value of the "store_true" action, which is "False")
				if (
					argument["Action"] == "store" and
					argument["Value"] != None or
					argument["Action"] == "store_true" and
					argument["Value"] == True
				):
					# Then the arguments dictionary has active arguments
					has_active_arguments = True

					# Add the argument to the "Active arguments" dictionary
					self.arguments["Active arguments"][name] = argument

					# If the "Auto-class" key is inside the argument dictionary
					# (The auto-class is the class that will be auto-executed)
					if "Auto-class" in argument:
						# Store the argument inside the arguments dictionary as the active argument
						self.arguments["Active argument"] = argument

			# If the module has active arguments
			if has_active_arguments == True:
				# Get the auto-class (the class that will be auto-executed) from the active argument dictionary
				class_ = self.arguments["Active argument"]["Auto-class"]

				# Import the module
				module = importlib.import_module("." + class_, self.__module__)

				# Get the class of the module and create its dictionary
				class_ = {
					"Object": getattr(module, class_)
				}

		# If the module has no active arguments
		if has_active_arguments == False:
			# If the "Do not run class" variable is not present in this class
			if hasattr(self, "do_not_run_class") == False:
				# Ask the user to select a class
				class_ = self.Modules.Select_Class(return_class = True)

		# If the self object (Run) has the "arguments" dictionary
		# Add it to the module class
		if hasattr(self, "arguments") == True:
			setattr(class_["Object"], "arguments", self.arguments)

		# If the "Do not run class" variable is not present in this class
		if hasattr(self, "do_not_run_class") == False:
			# Run the object of the class
			class_["Object"]()

# Define the alternate arguments for the module
alternate_arguments = [
	"play"
]

# Define the custom arguments for the module
custom_arguments = {
	"game": {
		"Action": "store",
		"Auto-class": "Play"
	},
	"sub_game": {
		"Action": "store"
	},
	"play": {
		"Action": "store_true",
		"Auto-class": "Play"
	}
}

# If the __name__ is "__main__", run the local "Run" class
if __name__ == "__main__":
	Run()
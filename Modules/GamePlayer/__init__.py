# GamePlayer.py

class Run():
	def __init__(self):
		import os
		import importlib

		from Utility.Input import Input as Input
		from Utility.JSON import JSON as JSON

		self.Input = Input()
		self.JSON = JSON()

		self.current_folder = os.path.split(__file__)[0] + "\\"

		self.descriptions_file = self.current_folder + "Descriptions.json"
		self.descriptions = self.JSON.To_Python(self.descriptions_file)

		self.classes = []

		for key in self.descriptions:
			if key != "show_text":
				self.classes.append(key)

		self.class_descriptions = []

		for class_ in self.classes:
			class_description = self.descriptions[class_]

			self.class_descriptions.append(self.JSON.Language.Item(class_description))

		self.language_texts = self.JSON.Language.Item(self.descriptions)

		has_active_arguments = False

		# If the self object (Run) has the "arguments" dictionary
		if hasattr(self, "arguments") == True:
			from copy import deepcopy

			# Iterate through the arguments list
			for argument in deepcopy(self.arguments).values():
				# If the argument has the "Action" key
				# And the action is "store"
				# And the value of the argument is not "None"
				# (Different from the default of the "store" action, which is "None")
				# Or the value of the argument is "True"
				# (Different from the default of the "store_true" action, which is "False")
				if (
					"Action" in argument and
					argument["Action"] == "store" and
					argument["Value"] != None or
					argument["Value"] == True
				):
					# Then the arguments dictionary has active arguments
					has_active_arguments = True

					# If the "Auto-class" key is inside the argument dictionary
					# (The auto-class is the class that will be auto-executed)
					if "Auto-class" in argument:
						# Store the argument inside the arguments dictionary as the active argument
						self.arguments["Active argument"] = argument

		# If the module has no active arguments
		if has_active_arguments == False:
			# Ask for the user to select a class
			option = self.Input.Select(self.classes, language_options = self.class_descriptions, show_text = self.language_texts["show_text"], select_text = self.JSON.Language.language_texts["select_one_class_to_execute"])["option"]

		# If the module has active arguments
		if has_active_arguments == True:
			# Get the auto-class (the class that will be auto-executed) from the active argument dictionary
			option = self.arguments["Active argument"]["Auto-class"]

		# Import the module
		module = importlib.import_module("." + option, self.__module__)

		# Get the module sub-class
		sub_class = getattr(module, option)

		# If the self object (Run) has the "arguments" dictionary
		# Add it to the module sub-class
		if hasattr(self, "arguments") == True:
			setattr(sub_class, "arguments", self.arguments)

		# Run the sub-class
		sub_class()

# Define the alternate arguments for the module
alternate_arguments = [
	"play"
]

# Define the custom arguments for the module
custom_arguments = {
	"game": {
		"Action": "store",
		"Auto-class": "Play"
	}
}

if __name__ == "__main__":
	Run()
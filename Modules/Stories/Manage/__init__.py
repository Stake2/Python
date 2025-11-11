# Manage.py

# Import the root class
from Stories.Stories import Stories as Stories

class Manage(Stories):
	def __init__(self):
		# Run its root class
		self.Modules(object = self, select_class = False)

		# If there is no selected story in the current class
		if hasattr(self, "story") == False:
			# Select the story
			self.story = self.Select_Story()

		# Ask the user to select a class
		selected_class = self.Modules.Select_Class(return_class = True)

		# Add the story dictionary to the class
		setattr(selected_class["Object"], "story", self.story)

		# Run the object of the class
		selected_class["Object"]()
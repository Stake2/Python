# Manage.py

from Stories.Stories import Stories as Stories

class Manage(Stories):
	def __init__(self):
		# Initiate the parent class
		super().__init__()

		import os
		import importlib

		self.current_folder = os.path.split(__file__)[0] + "\\"

		# Define the "Language" class as the same class inside the "JSON" class
		self.Language = self.JSON.Language

		self.descriptions_file = self.current_folder + "Descriptions.json"
		self.descriptions = self.JSON.To_Python(self.descriptions_file)

		self.classes = []

		for key in self.descriptions:
			if key != "show_text":
				self.classes.append(key)

		self.class_descriptions = []

		for class_ in self.classes:
			class_description = self.descriptions[class_]

			self.class_descriptions.append(self.Language.Item(class_description))

		# Select the story
		self.story = self.Select_Story()

		# Select the class
		show_text = self.language_texts["manage_the_story"] + " " + '"' + self.story["Titles"][self.user_language] + '"'

		class_ = self.Input.Select(self.classes, language_options = self.class_descriptions, show_text = show_text, select_text = self.Language.language_texts["select_one_class_to_execute"])["option"]

		# Get the module
		module = importlib.import_module("." + class_, self.__module__)

		# Get the class
		class_ = getattr(module, class_)

		# Add the story variable to the class
		setattr(class_, "story", self.story)

		# Execute the class
		class_()
# Select_Story.py

from Stories.Stories import Stories as Stories

class Select_Story(Stories):
	def __init__(self):
		super().__init__(story = "Select")

		self.Select()
		self.Select_Class()

	def Select(self, select_text_parameter = None):
		from copy import deepcopy

		show_text = self.language_texts["stories, title()"]

		select_text = select_text_parameter

		if select_text_parameter == None:
			select_text = self.language_texts["select_a_story"]

		class_name = type(self).__name__.lower()

		if (
			select_text_parameter == None and
			issubclass(type(self), Stories) == True and
			class_name in self.language_texts
		):
			select_text = self.language_texts["select_a_story_to"] + " " + self.language_texts[class_name]

		stories = deepcopy(self.stories)

		# Remove the stories with all chapters posted if the class is "Post"
		if class_name == "post":
			for story in deepcopy(self.stories["Titles"]["en"]):
				story = stories[story]

				post = story["Information"]["Chapter status"]["Post"]

				if int(post) == len(story["Information"]["Chapters"]["Titles"][self.user_language]):
					for language in self.languages["small"]:
						stories["Titles"][language].remove(story["Information"]["Titles"][language])

		self.option = self.Input.Select(stories["Titles"]["en"], language_options = stories["Titles"][self.user_language], show_text = show_text, select_text = select_text)["option"]

		self.story = self.stories[self.option]

		setattr(Stories, "story", self.story)

	def Select_Class(self):
		classes = [
			"Write",
			"Post",
			"Manage"
		]

		class_descriptions = []

		for class_ in classes:
			class_description = self.JSON.Language.language_texts[class_.lower() + ", title()"]

			class_descriptions.append(class_description)

		# Select the class
		show_text = self.language_texts["what_to_do_with_the_story"] + " " + '"' + self.story["Titles"][self.user_language] + '"'

		class_ = self.Input.Select(classes, language_options = class_descriptions, show_text = show_text, select_text = self.JSON.Language.language_texts["select_one_thing_to_do"])["option"]

		import importlib

		# Get the module
		module = importlib.import_module("." + class_, "Stories")

		# Get the class
		class_ = getattr(module, class_)

		# Execute the class
		class_(story = self.story)
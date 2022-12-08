# Select_Story.py

from Stories.Stories import Stories as Stories

from Stories.Write import Write as Write
from Stories.Post import Post as Post
from Stories.Update_Chapter_Covers import Update_Chapter_Covers as Update_Chapter_Covers

class Select_Story(Stories):
	def __init__(self):
		super().__init__()

		self.classes = [
			Write,
			Post,
			Update_Chapter_Covers,
		]

		self.class_descriptions = []

		for class_ in self.classes:
			class_description = self.language_texts[class_.__name__]

			self.class_descriptions.append(class_description)

		# Select class
		class_ = self.Input.Select(self.classes, language_options = self.class_descriptions, show_text = self.language_texts["select_one_story_class_to_execute"], select_text = self.Language.language_texts["select_one_class_to_execute"])["option"]

		# Execute class
		class_(story = self.story)
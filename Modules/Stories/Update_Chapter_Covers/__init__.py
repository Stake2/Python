# Update_Chapter_Covers.py

from Stories.Stories import Stories as Stories
from Stories.Post import Post as Post

class Update_Chapter_Covers(Stories):
	def __init__(self, story = None):
		super().__init__(select_story = False)

		self.story = story

		print()
		print(self.large_bar)
		print()
		print(self.language_texts["updating_the_chapter_covers_of_this_story"] + ":")
		print(self.story["Information"]["Titles"][self.user_language])
		print()

		Post(run_as_module = True, story = self.story)

		print(self.large_bar)
		print()
		print(self.language_texts["finished_updating_the_chapter_covers"] + ".")
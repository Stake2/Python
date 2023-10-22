# Update_Chapter_Covers.py

from Stories.Stories import Stories as Stories

class Update_Chapter_Covers(Stories):
	def __init__(self, story = None):
		super().__init__(story = story)

		print()
		print(self.large_bar)
		print()
		print(self.language_texts["updating_the_chapter_covers_of_this_story"] + ":")
		print(self.story["Titles"][self.user_language])
		print()

		from Stories.Post import Post as Post

		Post(run_as_module = True, story = self.story)

		print(self.large_bar)
		print()
		print(self.language_texts["finished_updating_the_chapter_covers"] + ".")
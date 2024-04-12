# Select_Story.py

from Stories.Stories import Stories as Stories

class Select_Story(Stories):
	def __init__(self):
		super().__init__()

		# Ask the user to select the story
		self.Select_Story(select_class = True)
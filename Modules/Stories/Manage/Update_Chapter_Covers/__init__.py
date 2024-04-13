# Update_Chapter_Covers.py

from Stories.Stories import Stories as Stories

class Update_Chapter_Covers(Stories):
	def __init__(self):
		super().__init__()

		# Import sub-classes method
		self.Import_Sub_Classes()

		# Show space separators and a dash space separator
		print()
		print(self.separators["5"])
		print()

		# Show the information text with the story title in the user language
		print(self.language_texts["updating_the_chapter_covers_of_this_story"] + ":")
		print(self.story["Titles"][self.user_language])
		print()

		# Run the "Post" class as a module to update all of the chapter covers
		self.Post(run_as_module = True)

		# Show the finish text with the story title in the user language
		print(self.separators["5"])
		print()
		print(self.language_texts["you_finished_updating_the_chapter_covers_of_this_story"] + ":")
		print(self.story["Titles"][self.user_language])

		# Show a five dash space separator
		print(self.separators["5"])

	def Import_Sub_Classes(self):
		# Import the "importlib" module
		import importlib

		# Define the classes to be imported
		classes = [
			"Post"
		]

		# Import them
		for title in classes:
			# Import the module
			module = importlib.import_module("." + title, self.__module__.split(".")[0])

			# Get the sub-class
			sub_class = getattr(module, title)

			# Add the sub-class to the current module
			setattr(self, title, sub_class)

		# Add the "Story" variable to the "Post" sub-class
		setattr(self.Post, "story", self.story)
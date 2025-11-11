# Update_Chapter_Covers.py

from Stories.Stories import Stories as Stories

class Update_Chapter_Covers(Stories):
	def __init__(self):
		super().__init__()

		# Import some sub-classes
		self.Import_Sub_Classes()

		# Update the chapter covers
		self.Update()

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

		# Add the story dictionary to the "Post" class
		setattr(self.Post, "story", self.story)

	def Update(self):
		# Show a five dash space separator
		print()
		print(self.separators["5"])
		print()

		# Show the information text with the story title in the user language
		print(self.language_texts["updating_the_chapter_covers_of_this_story"] + ":")
		print("\t" + self.story["Titles"][self.language["Small"]])

		# Define the local "posting" dictionary to use on the "Post" class, to only run the "Create chapter covers" posting step
		posting = {
			"Steps": [
				"Create chapter covers"
			]
		}

		# Run the "Post" class and give the local "posting" dictionary to it as a parameter
		self.Post(posting)

		# Show a five dash space separator
		print()
		print(self.separators["5"])
		print()

		# Show the finish text with the story title in the user language
		print(self.language_texts["you_finished_updating_the_chapter_covers_of_this_story"] + ":")
		print("\t" + self.story["Titles"][self.language["Small"]])

		# Show a five dash space separator
		print()
		print(self.separators["5"])
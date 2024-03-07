# Add_To_Comments_Dictionary.py

from Watch_History.Watch_History import Watch_History as Watch_History

class Add_To_Comments_Dictionary(Watch_History):
	def __init__(self):
		super().__init__()

		# Define the root dictionary with the media type dictionary
		options = {
			"Media type": {
				"Status": self.texts["statuses, type: list"]["en"],

				# Remove the "Movies" media type from the media type dictionary, returning a local media types dictionary
				"List": self.Remove_Media_Type(self.texts["movies, title()"]["en"])
			}
		}

		# Ask for the user to select the media type and media
		self.dictionary = self.Select_Media_Type_And_Media(options, watch = True)

		# Import sub-classes method
		self.Import_Sub_Classes()

		# Define the "Select episode" key inside the dictionary
		self.dictionary["Select episode"] = True

		# Define the media dictionary with the already selected media type and media
		self.dictionary = self.Watch_Media(self.dictionary, open_media = False).dictionary

		# Comment on the media without having to register the watched media unit (episode, video, or movie)
		self.Comment_Writer(self.dictionary, add_comment = True)

	def Import_Sub_Classes(self):
		# Import the "importlib" module
		import importlib

		# Define the classes to be imported
		classes = [
			"Watch_Media",
			"Comment_Writer"
		]

		# Import them
		for title in classes:
			# Import the module
			module = importlib.import_module("." + title, self.__module__.split(".")[0])

			# Get the sub-class
			sub_class = getattr(module, title)

			# Add the sub-class to the current module
			setattr(self, title, sub_class)
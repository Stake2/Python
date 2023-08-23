# Add_To_Comments_Dictionary.py

from Watch_History.Watch_History import Watch_History as Watch_History

class Add_To_Comments_Dictionary(Watch_History):
	def __init__(self):
		super().__init__()

		options = {
			"Media type": {
				"Status": self.texts["statuses, type: list"]["en"],

				# Remove the "Movies" media type from the media type dictionary, returning a local media types dictionary
				"List": self.Remove_Media_Type(self.texts["movies, title()"]["en"])
			}
		}

		self.dictionary = self.Select_Media_Type_And_Media(options, watch = True)

		import importlib

		classes = [
			"Watch_Media",
			"Comment_Writer"
		]

		for title in classes:
			class_ = getattr(importlib.import_module("."  + title, "Watch_History"), title)
			setattr(self, title, class_)

		# Define media dictionary with already selected media type and media
		self.dictionary = self.Watch_Media(self.dictionary, open_media = False).dictionary

		# Comment on media without having to register the watched media unit (episode, video, or movie)
		self.Comment_Writer(self.dictionary, write_comment = True)
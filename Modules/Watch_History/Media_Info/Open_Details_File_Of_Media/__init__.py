# Open_Details_File_Of_Media.py

from Watch_History.Watch_History import Watch_History as Watch_History

class Open_Details_File_Of_Media(Watch_History):
	def __init__(self):
		super().__init__()

		self.option_info = self.Select_Media_Type_And_Media({"media_list": "all"})

		self.media_details_file = self.option_info["media_details_file"]

		print()
		print(self.language_texts["opening_this_media_details_file"] + ": ")
		print(self.media_details_file)

		self.File.Open(self.media_details_file)
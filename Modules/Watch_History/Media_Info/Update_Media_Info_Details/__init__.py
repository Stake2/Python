# Update_Media_Info_Details.py

from Watch_History.Watch_History import Watch_History as Watch_History

class Update_Media_Info_Details(Watch_History):
	def __init__(self):
		super().__init__()

		#self.Iterate()

	def Iterate(self):
		for plural_media_type in self.media_types["plural"]["en"]:
			key = plural_media_type.lower().replace(" ", "_")

			media_list = self.media_types[plural_media_type]["media_list"]
			comments_folder = self.folders["comments"][key]["root"]

			print()
			print("-----")
			print()
			print(plural_media_type + ":")

			for media in media_list:
				self.dictionary = {
					"media_type": self.media_types[plural_media_type],
					"media": {
						"title": media
					}
				}

				print()
				self.dictionary = self.Select_Media(self.dictionary)

				self.Convert_Comments()

	def Convert_Comments(self):
		print(self.dictionary["media"]["item"]["folders"]["media_type_comments"]["root"])
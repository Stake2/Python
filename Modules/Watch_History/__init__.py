# Watch_History.py

class Run():
	def __init__(self):
		from Utility.Modules import Modules as Modules

		# Get modules dictionary
		self.modules = Modules().Set(self, ["Folder", "Input", "JSON", "Language"])

		self.current_folder = self.Folder.Sanitize(self.Folder.Split(__file__)[0])

		self.descriptions_file = self.current_folder + "Descriptions.json"
		self.descriptions = self.JSON.To_Python(self.descriptions_file)

		from Watch_History.Watch_Media import Watch_Media as Watch_Media
		from Watch_History.Start_Watching_Media import Start_Watching_Media as Start_Watching_Media
		from Watch_History.Media_Info import Media_Info as Media_Info
		from Watch_History.Watch_List_Of_Media import Watch_List_Of_Media as Watch_List_Of_Media

		self.classes = [
			Watch_Media,
			Watch_List_Of_Media,
			Start_Watching_Media,
			Media_Info,
		]

		self.class_descriptions = []

		for class_ in self.classes:
			class_description = self.descriptions[class_.__name__]

			self.class_descriptions.append(self.Language.Item(class_description))

		self.language_texts = self.Language.Item(self.descriptions)

		self.Input.Select(self.classes, language_options = self.class_descriptions, show_text = self.language_texts["show_text"], select_text = self.Language.language_texts["select_one_class_to_execute"], function = True)

if __name__ == "__main__":
	Run()
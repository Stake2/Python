# Diary_Slim.py



class Run():
	def __init__(self):
		from Utility.Modules import Modules as Modules

		# Get modules dictionary
		self.modules = Modules().Set(self, ["Folder", "Input", "JSON", "Language"])

		self.current_folder = self.Folder.Sanitize(self.Folder.Split(__file__)[0])

		self.descriptions_file = self.current_folder + "Descriptions.json"
		self.descriptions = self.JSON.To_Python(self.descriptions_file)

		from Diary_Slim.Create_New_Diary_Slim import Create_New_Diary_Slim as Create_New_Diary_Slim
		from Diary_Slim.Write_On_Diary_Slim import Write_On_Diary_Slim as Write_On_Diary_Slim

		self.classes = [
			Create_New_Diary_Slim,
			Write_On_Diary_Slim,
		]

		self.class_descriptions = []

		for class_ in self.classes:
			class_description = self.descriptions[class_.__name__]

			self.class_descriptions.append(self.Language.Item(class_description))

		self.language_texts = self.Language.Item(self.descriptions)

		self.Input.Select(self.classes, language_options = self.class_descriptions, show_text = self.language_texts["show_text"], select_text = self.Language.language_texts["select_one_class_to_execute"], function = True)

arguments = ["slim"]

if __name__ == "__main__":
	Run()
# Python.py

class Run():
	def __init__(self):
		self.modules = self.Modules.Set(self, ["Folder", "Input", "JSON", "Language"])

		self.current_folder = self.Folder.Sanitize(self.Folder.Split(__file__)[0])

		self.descriptions_file = self.current_folder + "Descriptions.json"
		self.descriptions = self.JSON.To_Python(self.descriptions_file)

		from Python.Create_New_Module import Create_New_Module as Create_New_Module
		from Python.Create_Language_Text import Create_Language_Text as Create_Language_Text
		from Python.List_Modules import List_Modules as List_Modules

		self.classes = [
			Create_New_Module,
			Create_Language_Text,
			List_Modules,
		]

		self.class_descriptions = []

		for class_ in self.classes:
			class_description = self.descriptions[class_.__name__]

			self.class_descriptions.append(self.Language.Item(class_description))

		self.language_texts = self.Language.Item(self.descriptions)

		option = self.Input.Select(self.classes, language_options = self.class_descriptions, show_text = self.language_texts["show_text"], select_text = self.Language.language_texts["select_one_class_to_execute"])["option"]

		import importlib
		self.sub_class = getattr(importlib.import_module("." + option, self.__module__), option)

		# Add Modules module to sub class
		setattr(self.sub_class, "Modules", self.Modules)

		# Run selected sub_class
		self.sub_class()

if __name__ == "__main__":
	Run()
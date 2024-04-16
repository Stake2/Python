# Years.py

class Run():
	def __init__(self):
		import os
		import importlib

		from Utility.Input import Input as Input
		from Utility.JSON import JSON as JSON

		self.Input = Input()
		self.JSON = JSON()

		# Define the "Language" class as the same class inside the "JSON" class
		self.Language = self.JSON.Language

		self.current_folder = os.path.split(__file__)[0] + "\\"

		self.descriptions_file = self.current_folder + "Descriptions.json"
		self.descriptions = self.JSON.To_Python(self.descriptions_file)

		self.classes = []

		for key in self.descriptions:
			if key != "show_text":
				self.classes.append(key)

		self.class_descriptions = []

		for class_ in self.classes:
			class_description = self.descriptions[class_]

			self.class_descriptions.append(self.Language.Item(class_description))

		self.language_texts = self.Language.Item(self.descriptions)

		option = self.Input.Select(self.classes, language_options = self.class_descriptions, show_text = self.language_texts["show_text"], select_text = self.Language.language_texts["select_one_class_to_execute"])["option"]

		module = importlib.import_module("." + option, self.__module__)
		sub_class = getattr(module, option)()

if __name__ == "__main__":
	Run()
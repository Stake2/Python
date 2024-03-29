# Diary_Slim.py

class Run():
	def __init__(self):
		import os
		import importlib

		from Utility.Input import Input as Input
		from Utility.JSON import JSON as JSON

		self.Input = Input()
		self.JSON = JSON()

		self.current_folder = os.path.split(__file__)[0] + "\\"

		self.descriptions_file = self.current_folder + "Descriptions.json"
		self.descriptions = self.JSON.To_Python(self.descriptions_file)

		self.classes = []

		for key in self.descriptions:
			if key not in ["show_text", "Remove list"]:
				if (
					"Remove list" not in self.descriptions or
					"Remove list" in self.descriptions and key not in self.descriptions["Remove list"]
				):
					self.classes.append(key)

		self.class_descriptions = []

		for class_ in self.classes:
			class_description = self.descriptions[class_]

			self.class_descriptions.append(self.JSON.Language.Item(class_description))

		self.language_texts = self.JSON.Language.Item(self.descriptions)

		option = self.Input.Select(self.classes, language_options = self.class_descriptions, show_text = self.language_texts["show_text"], select_text = self.JSON.Language.language_texts["select_one_class_to_execute"])["option"]

		module = importlib.import_module("." + option, self.__module__)
		sub_class = getattr(module, option)()

# Define the alternate arguments for the module
alternate_arguments = [
	"slim"
]

if __name__ == "__main__":
	Run()
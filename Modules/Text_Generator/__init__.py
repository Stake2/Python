# Text_Generator.py

from Text_Generator.Generate_CSS_Selectors import Generate_CSS_Selectors as Generate_CSS_Selectors

from Language import Language as Language
from Input import Input as Input
from Folder import Folder as Folder

class Run():
	def __init__(self):
		# Global Switches dictionary
		self.global_switches = {
			"verbose": False,
		}

		self.Language = Language(self.global_switches)
		self.Folder = Folder(self.global_switches)
		self.Input = Input(self.global_switches)

		self.current_folder = self.Folder.Sanitize(self.Folder.Split(__file__)[0])

		self.descriptions_file = self.current_folder + "Descriptions.json"
		self.descriptions = self.Language.JSON_To_Python(self.descriptions_file)

		self.classes = [
			Generate_CSS_Selectors,
		]

		self.class_descriptions = []

		for class_ in self.classes:
			class_description = self.descriptions[class_.__name__]

			self.class_descriptions.append(self.Language.Item(class_description))

		self.language_texts = self.Language.Item(self.descriptions)

		self.Input.Select(self.classes, language_options = self.class_descriptions, show_text = self.language_texts["show_text"], select_text = self.Language.language_texts["select_one_class_to_execute"], function = True)

if __name__ == "__main__":
	Run()
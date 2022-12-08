# Years.py

from Years.Verify_Current_Year import Verify_Current_Year as Verify_Current_Year
from Years.Create_Year_Summary import Create_Year_Summary as Create_Year_Summary
from Years.Show_Year_Information import Show_Year_Information as Show_Year_Information

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
			Verify_Current_Year,
			Create_Year_Summary,
			Show_Year_Information,
		]

		self.class_descriptions = []

		for class_ in self.classes:
			class_description = self.descriptions[class_.__name__]

			self.class_descriptions.append(self.Language.Item(class_description))

		self.language_texts = self.Language.Item(self.descriptions)

		self.Input.Select(self.classes, language_options = self.class_descriptions, show_text = self.language_texts["show_text"], select_text = self.Language.language_texts["select_one_class_to_execute"], function = True)

if __name__ == "__main__":
	Run()
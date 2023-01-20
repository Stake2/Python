# Stories.py

from Stories.Select_Story import Select_Story as Select_Story
from Stories.Create_New_Story import Create_New_Story as Create_New_Story
from Stories.Show_Story_Information import Show_Story_Information as Show_Story_Information
from Stories.Copy_Story_Titles import Copy_Story_Titles as Copy_Story_Titles

from Language import Language as Language
from Input import Input as Input
from Folder import Folder as Folder
from JSON import JSON as JSON

class Run():
	def __init__(self):
		# Global Switches dictionary
		self.global_switches = {
			"verbose": False,
		}

		self.Language = Language(self.global_switches)
		self.Folder = Folder(self.global_switches)
		self.Input = Input(self.global_switches)
		self.JSON = JSON(self.global_switches)

		self.current_folder = self.Folder.Sanitize(self.Folder.Split(__file__)[0])

		self.descriptions_file = self.current_folder + "Descriptions.json"
		self.descriptions = self.JSON.To_Python(self.descriptions_file)

		self.classes = [
			Select_Story,
			Create_New_Story,
			Show_Story_Information,
			Copy_Story_Titles,
		]

		self.class_descriptions = []

		for class_ in self.classes:
			class_description = self.descriptions[class_.__name__]

			self.class_descriptions.append(self.Language.Item(class_description))

		self.language_texts = self.Language.Item(self.descriptions)

		self.Input.Select(self.classes, language_options = self.class_descriptions, show_text = self.language_texts["show_text"], select_text = self.Language.language_texts["select_one_class_to_execute"], function = True)

arguments = ["story"]

if __name__ == "__main__":
	Run()
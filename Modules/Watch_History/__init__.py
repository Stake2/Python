# Watch_History.py

from Watch_History.Watch_Media import Watch_Media as Watch_Media
from Watch_History.Start_Watching_A_New_Media import Start_Watching_A_New_Media as Start_Watching_A_New_Media
from Watch_History.Media_Info_Database_Manager import Media_Info_Database_Manager as Media_Info_Database_Manager
from Watch_History.Watch_List_Of_Media import Watch_List_Of_Media as Watch_List_Of_Media

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
			Watch_Media,
			Watch_List_Of_Media,
			Start_Watching_A_New_Media,
			Media_Info_Database_Manager,
		]

		self.class_descriptions = []

		for class_ in self.classes:
			class_description = self.descriptions[class_.__name__]

			self.class_descriptions.append(self.Language.Item(class_description))

		self.language_texts = self.Language.Item(self.descriptions)

		self.Input.Select(self.classes, language_options = self.class_descriptions, show_text = self.language_texts["show_text"], select_text = self.Language.language_texts["select_one_class_to_execute"], function = True)

if __name__ == "__main__":
	Run()
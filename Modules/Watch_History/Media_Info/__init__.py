# Media_Info.py

from Watch_History.Media_Info.Add_New_Media import Add_New_Media as Add_New_Media
from Watch_History.Media_Info.Open_Details_File import Open_Details_File as Open_Details_File
from Watch_History.Media_Info.Fill_Episode_Titles import Fill_Episode_Titles as Fill_Episode_Titles
from Watch_History.Media_Info.Update_Media_Info_Details import Update_Media_Info_Details as Update_Media_Info_Details

from Language import Language as Language
from Input import Input as Input
from Folder import Folder as Folder

class Media_Info():
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
			Add_New_Media,
			Open_Details_File,
			Fill_Episode_Titles,
		]

		self.class_descriptions = []

		for class_ in self.classes:
			class_description = self.descriptions[class_.__name__]

			self.class_descriptions.append(self.Language.Item(class_description))

		self.language_texts = self.Language.Item(self.descriptions)

		self.Input.Select(self.classes, language_options = self.class_descriptions, show_text = self.language_texts["show_text"], select_text = self.Language.language_texts["select_one_class_to_execute"], function = True)

Update_Media_Info_Details()
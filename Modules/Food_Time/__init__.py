# Food_Time.py

from Food_Time.Food_Time import Food_Time as Food_Time

from Language import Language as Language
from Input import Input as Input
from Folder import Folder as Folder

class Run(Food_Time):
	def __init__(self, run = True, register_time = True):
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

		self.language_texts = self.Language.Item(self.descriptions)

		if run == True:
			super().__init__(register_time = register_time)

run = Run(run = False)

arguments = {
	"set": {
		"text": run.language_texts["set"]
	},
	"check": {
		"text": run.language_texts["check"]
	}
}
# Food_Time.py

from Food_Time.Food_Time import Food_Time as Food_Time

class Run(Food_Time):
	def __init__(self, run = True, register_time = True):
		from Utility.Modules import Modules as Modules

		# Get modules dictionary
		self.modules = Modules().Set(self, ["Folder", "Input", "JSON", "Language"])

		self.current_folder = self.Folder.Sanitize(self.Folder.Split(__file__)[0])

		self.descriptions_file = self.current_folder + "Descriptions.json"
		self.descriptions = self.JSON.To_Python(self.descriptions_file)

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
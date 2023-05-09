# List_Modules.py

from Python.Python import Python as Python

class List_Modules(Python):
	def __init__(self):
		super().__init__()

		print()
		print(self.large_bar)
		print()
		print(self.language_texts["these_are_the_modules_that_exist_in_the_modules_folder"] + ":")

		for key in ["Utility", "Usage"]:
			if self.modules[key]["List"] != []:
				print()
				print(self.language_texts[key.lower() + "_modules"] + ":")

				for module in self.modules[key]["List"]:
					print(module)

		print()
		print(self.large_bar)
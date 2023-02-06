# List_Modules.py

from Python.Python import Python as Python

class List_Modules(Python):
	def __init__(self):
		super().__init__()

		print()
		print(self.large_bar)
		print()
		print(self.language_texts["these_are_the_modules_that_exist_in_the_modules_folder"] + ":")

		for key in ["utility", "usage"]:
			if self.modules[key]["list"] != []:
				print()
				print(self.language_texts[key + "_modules"] + ":")

				for module in self.modules[key]["list"]:
					print(module)

		print()
		print(self.large_bar)
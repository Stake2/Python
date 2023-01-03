# List_Modules.py

from Python.Python import Python as Python

class List_Modules(Python):
	def __init__(self):
		super().__init__()

		print()
		print(self.large_bar)
		print()
		print(self.language_texts["these_are_the_modules_that_exist_in_the_modules_folder"] + ":")

		for module_type in self.module_files:
			file = self.module_files[module_type]

			lines = self.File.Contents(file)["lines"]

			if lines != []:
				print()
				print(module_type + ":")

				for module in lines:
					print(module)

		print()
		print(self.large_bar)
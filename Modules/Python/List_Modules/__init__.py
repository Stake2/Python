# List_Modules.py

from Python.Python import Python as Python

class List_Modules(Python):
	def __init__(self):
		super().__init__()

		# Show a five dash space separator
		print()
		print(self.separators["5"])
		print()

		# Show the description text about the modules
		print(self.language_texts["these_are_the_modules_that_exist_in_the_modules_folder"] + ":")

		# Iterate through the module types
		for key in self.python["Modules"]["Types"]["List"]:
			# If the list of modules is not empty
			if self.modules[key]["List"] != []:
				# Show a space separator	
				print()

				# Show the text of the module, along with the number of modules
				text = self.language_texts[key.lower() + "_modules"]
				text += " (" + str(len(self.modules[key]["List"])) + "):"

				print(text)

				# Iterate through the modules in the list
				m = 1
				for module in self.modules[key]["List"]:	
					# Define the module text
					text = "\t"

					# Add the module number and the space
					text += str(m) + " - "

					# Add the module name
					text += module

					print(text)

					m += 1

		# Show a five dash space separator
		print()
		print(self.separators["5"])
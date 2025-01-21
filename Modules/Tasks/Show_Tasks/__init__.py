# Show_Tasks.py

from Tasks.Tasks import Tasks as Tasks

class Show_Tasks(Tasks):
	def __init__(self):
		super().__init__()

		# Read the "Tasks.json" file of the current year to get the "Tasks" dictionary
		self.dictionaries["Tasks"] = self.JSON.From_Python(self.dictionaries["Tasks"])

		# Replace a lot of characters in the "Tasks" dictionary to make it easier to read
		self.dictionaries["Tasks"] = self.dictionaries["Tasks"].replace("{", "[")
		self.dictionaries["Tasks"] = self.dictionaries["Tasks"].replace("}", "]")
		self.dictionaries["Tasks"] = self.dictionaries["Tasks"].replace("],", "]\n")
		self.dictionaries["Tasks"] = self.dictionaries["Tasks"].replace(",\n    ", "\n\n    ")
		self.dictionaries["Tasks"] = self.dictionaries["Tasks"].replace(",", "")
		self.dictionaries["Tasks"] = self.dictionaries["Tasks"].replace('    \"', '"')
		self.dictionaries["Tasks"] = self.dictionaries["Tasks"].replace("    ]", "]")
		self.dictionaries["Tasks"] = self.dictionaries["Tasks"][1:]
		self.dictionaries["Tasks"] = self.dictionaries["Tasks"][:-2]

		# Show a five dash space separator
		print()
		print(self.separators["5"])

		# Show the edited "Tasks" dictionary text
		print(self.dictionaries["Tasks"])

		# Show a five dash space separator
		print()
		print(self.separators["5"])
# Show_Tasks.py

from Tasks.Tasks import Tasks as Tasks

class Show_Tasks(Tasks):
	def __init__(self):
		super().__init__()

		self.dictionaries["Tasks"] = self.JSON.From_Python(self.dictionaries["Tasks"])
		self.dictionaries["Tasks"] = self.dictionaries["Tasks"].replace("{", "[")
		self.dictionaries["Tasks"] = self.dictionaries["Tasks"].replace("}", "]")
		self.dictionaries["Tasks"] = self.dictionaries["Tasks"].replace("],", "]\n")
		self.dictionaries["Tasks"] = self.dictionaries["Tasks"].replace(",\n    ", "\n\n    ")
		self.dictionaries["Tasks"] = self.dictionaries["Tasks"].replace(",", "")
		self.dictionaries["Tasks"] = self.dictionaries["Tasks"].replace('    \"', '"')
		self.dictionaries["Tasks"] = self.dictionaries["Tasks"].replace("    ]", "]")
		self.dictionaries["Tasks"] = self.dictionaries["Tasks"][1:]
		self.dictionaries["Tasks"] = self.dictionaries["Tasks"][:-2]

		print()
		print(self.separators["5"])
		print(self.dictionaries["Tasks"])
		print()
		print(self.separators["5"])
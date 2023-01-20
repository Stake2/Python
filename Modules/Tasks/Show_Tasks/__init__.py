# Show_Tasks.py

from Tasks.Tasks import Tasks as Tasks

class Show_Tasks(Tasks):
	def __init__(self):
		super().__init__()

		self.tasks = self.JSON.From_Python(self.tasks)
		self.tasks = self.tasks.replace("{", "[")
		self.tasks = self.tasks.replace("}", "]")
		self.tasks = self.tasks.replace("],", "]\n")
		self.tasks = self.tasks.replace(",\n    ", "\n\n    ")
		self.tasks = self.tasks.replace(",", "")
		self.tasks = self.tasks.replace('    \"', '"')
		self.tasks = self.tasks.replace("    ]", "]")
		self.tasks = self.tasks[1:]
		self.tasks = self.tasks[:-2]

		print()
		print(self.large_bar)
		print(self.tasks)
		print()
		print(self.large_bar)
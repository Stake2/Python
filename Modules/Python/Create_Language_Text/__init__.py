# Create_Language_Text.py

from Python.Python import Python as Python

class Create_Language_Text(Python):
	def __init__(self):
		super().__init__()

		self.question = self.language_texts["create_more_texts"]

		self.create_more = True

		while self.create_more == True:
			self.JSON.Language.Create_Language_Text()

			self.create_more = self.Input.Yes_Or_No(self.question)
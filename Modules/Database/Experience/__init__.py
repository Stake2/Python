# Experience.py

from Database.Database import Database as Database

class Experience(Database):
	def __init__(self, dictionary = {}):
		super().__init__()

		import importlib

		classes = [
			"Register"
		]

		for title in classes:
			class_ = getattr(importlib.import_module("."  + title, "Database"), title)
			setattr(self, title, class_)

		self.dictionary = dictionary

		self.Define_Data_Dictionary()
		self.Register_The_Data()

	def Define_Data_Dictionary(self):
		# Select the data type and the data if the dictionary is empty
		if self.dictionary == {}:
			# Ask the user to select a data type and data
			self.dictionary = self.Select_Data_Type_And_Data()

		self.data = self.dictionary["Data"]

	def Register_The_Data(self):
		text = self.language_texts["press_enter_when_you_finish_experiencing_the_data"]

		self.data["States"]["Finished experiencing"] = self.Input.Type(text)
		self.data["States"]["Finished experiencing"] = True

		# Register the finished experiencing time
		self.dictionary["Entry"] = {
			"Time": self.Date.Now()
		}

		# Use the "Register" class to register the experienced data, and giving the dictionary to it
		self.Register(self.dictionary)
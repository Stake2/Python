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

		# Define the experiencing status list for "Plan to experience" related statuses
		status_list = [
			self.texts["plan_to_experience, title()"][self.user_language],
			self.JSON.Language.texts["on_hold, title()"][self.user_language]
		]

		# If the game experiencing status is inside the status list
		if self.data["details"][self.JSON.Language.language_texts["status, title()"]] in status_list:
			# If the data "Dates.txt" file is empty
			if self.File.Contents(self.data["folders"]["dates"])["lines"] == []:
				# Get the first experiencing time where the user started experiencing the data
				self.data["Started experiencing time"] = self.Date.Now()["hh:mm DD/MM/YYYY"]

				# Create the Dates text
				self.data["Dates"] = self.language_texts["when_i_started_to_experience"] + ":\n"
				self.data["Dates"] += self.data["Started experiencing time"]

				self.File.Edit(self.data["folders"]["dates"], self.data["Dates"], "w")

			# Change the experiencing status to "Experiencing"
			self.Change_Status(self.dictionary, self.language_texts["experiencing, title()"])

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
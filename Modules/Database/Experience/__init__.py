# Experience.py

from Database.Database import Database as Database

class Experience(Database):
	def __init__(self, dictionary = {}):
		super().__init__()

		# Import sub-classes method
		self.Import_Sub_Classes()

		self.dictionary = dictionary

		self.Define_Data_Dictionary()
		self.Register_The_Data()

	def Import_Sub_Classes(self):
		# Import the "importlib" module
		import importlib

		# Define the classes to be imported
		classes = [
			"Register"
		]

		# Import them
		for title in classes:
			# Import the module
			module = importlib.import_module("." + title, self.__module__.split(".")[0])

			# Get the sub-class
			sub_class = getattr(module, title)

			# Add the sub-class to the current module
			setattr(self, title, sub_class)

	def Define_Data_Dictionary(self):
		# Select the data type and the data if the dictionary is empty
		if self.dictionary == {}:
			# Ask the user to select a data type and data
			self.dictionary = self.Select_Data_Type_And_Data()

		self.data = self.dictionary["Data"]

		# Define the experiencing status list for "Plan to experience" related statuses
		status_list = [
			self.texts["plan_to_experience, title()"][self.language["Small"]],
			self.Language.texts["on_hold, title()"][self.language["Small"]]
		]

		# If the game experiencing status is inside the status list
		if self.data["Details"][self.Language.language_texts["status, title()"]] in status_list:
			# If the data "Dates.txt" file is empty
			if self.File.Contents(self.data["Folders"]["dates"])["lines"] == []:
				# Get the first experiencing time where the user started experiencing the data
				self.data["Started experiencing time"] = self.Date.Now()["Formats"]["HH:MM DD/MM/YYYY"]

				# Create the Dates text
				self.data["Dates"] = self.language_texts["when_i_started_to_experience"] + ":\n"
				self.data["Dates"] += self.data["Started experiencing time"]

				self.File.Edit(self.data["Folders"]["dates"], self.data["Dates"], "w")

			# Change the experiencing status to "Experiencing"
			self.Change_Status(self.dictionary, self.language_texts["experiencing, title()"])

	def Register_The_Data(self):
		text = self.language_texts["press_enter_when_you_finish_experiencing_the_data"]

		self.data["States"]["Finished experiencing"] = self.Input.Type(text)
		self.data["States"]["Finished experiencing"] = True

		# Register the finished experiencing time
		self.dictionary["Entry"] = {
			"Date": self.Date.Now()
		}

		# Use the "Register" class to register the experienced data, and giving the dictionary to it
		self.Register(self.dictionary)
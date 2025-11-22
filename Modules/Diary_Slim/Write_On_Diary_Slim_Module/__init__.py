# Write_On_Diary_Slim_Module.py

from Diary_Slim.Diary_Slim import Diary_Slim as Diary_Slim

class Write_On_Diary_Slim_Module(Diary_Slim):
	def __init__(self, dictionary = {}):
		super().__init__()

		# Define the root dictionary
		self.dictionary = {
			"Texts": {
				"To write": "",
				"To show": ""
			},
			"Time string": "",
			"Date": self.date,
			"Show text": True,
			"Add": {
				"Time": True,
				"Dot": True
			},
			"Current Diary Slim": True,
			"Verbose": True,
			"First space": False
		}

		# Get the keys and values from the "dictionary" parameter
		self.Update_Dictionary(dictionary)

		# Write the text to the current Diary Slim
		self.Write()

	def Update_Dictionary(self, dictionary):
		# Get the "Text" key
		if "Text" in dictionary:
			self.dictionary["Texts"]["To write"] = dictionary["Text"]

		# Get the "Time" key
		if "Time" in dictionary:
			self.dictionary["Time string"] = dictionary["Time"]

		# Get the "Date" key
		if "Date" in dictionary:
			self.dictionary["Date"] = dictionary["Date"]

		# Update the "Add" dictionary
		if "Add" in dictionary:
			for key in dictionary["Add"]:
				self.dictionary["Add"][key] = dictionary["Add"][key]

		# Update the "Current Diary Slim" and "Verbose" keys
		keys = [
			"Show text",
			"Current Diary Slim",
			"Verbose",
			"First space"
		]

		for key in keys:
			if key in dictionary:
				self.dictionary[key] = dictionary[key]

	def Write(self):
		# If the time string is empty, get a time string from the current date
		if self.dictionary["Time string"] == "":
			self.dictionary["Time string"] = self.Date.Now()["Formats"]["HH:MM DD/MM/YYYY"]

		# If the "Add time" switch is True
		if self.dictionary["Add"]["Time"] == True:
			# Add the time string
			self.dictionary["Texts"]["To write"] = self.dictionary["Time string"] + ":\n" + self.dictionary["Texts"]["To write"]

		# Get the current Diary Slim dictionary
		current_diary_slim = self.Current_Diary_Slim(date = self.dictionary["Date"], current_diary_slim = self.dictionary["Current Diary Slim"])

		# Create the file
		self.File.Create(current_diary_slim["File"])

		# Get the length of the file
		length = self.File.Contents(current_diary_slim["File"])["length"]

		# If the file is not empty, add line breaks before the text
		if length != 0:
			self.dictionary["Texts"]["To write"] = "\n\n" + self.dictionary["Texts"]["To write"]

		# If the last character of the text is not a dot
		# And the "Add dot" switch is True
		if (
			self.dictionary["Texts"]["To write"][-1] != "." and
			self.dictionary["Add"]["Dot"] == True
		):
			# Add a dot to the end of the text
			self.dictionary["Texts"]["To write"] += "."

		# Add the text to the file
		self.File.Edit(current_diary_slim["File"], self.dictionary["Texts"]["To write"], "a", next_line = False)

		# If the "verbose" switch is True, show a space separator
		if self.switches["Verbose"] == True:
			print()

		# Define the text to show as the "This text was written to the current Diary Slim" text
		self.dictionary["Texts"]["To show"] = self.language_texts["this_text_was_written_to_the_current_diary_slim"] + ":"

		# If the "Testing" switch is True
		if self.switches["Testing"] == True:
			# Update the information telling the user that the text was not written to the file
			# Because the "testing" switch is True

			# Replace "was" with "was not"
			replace = self.Language.language_texts["was"]
			with_ = self.Language.language_texts["was_not"]

			self.dictionary["Texts"]["To show"] = self.dictionary["Texts"]["To show"].replace(replace, with_)

			# Add the information about the "Testing" switch being True
			replace = ":"
			with_ = " (" + self.language_texts["the_testing_mode_is_on"] + "):"

			self.dictionary["Texts"]["To show"] = self.dictionary["Texts"]["To show"].replace(replace, with_)

		# If the first character of the text to write is a line break
		if self.dictionary["Texts"]["To write"][0] == "\n":
			# Remove it
			self.dictionary["Texts"]["To write"] = self.dictionary["Texts"]["To write"][2:]

		# Add the text to write to the text to show
		self.dictionary["Texts"]["To show"] += "\n" + "[" + self.dictionary["Texts"]["To write"] + "]"

		# If the "First space" switch is True
		if self.dictionary["First space"] == True:
			# Show the first space
			print()

		# If the "Show text" switch is True
		# And the "Verbose" switch is True
		if (
			self.dictionary["Show text"] == True and
			self.dictionary["Verbose"] == True
		):
			# Show the text to show
			print(self.dictionary["Texts"]["To show"])

	@classmethod
	def Return(class_, dictionary):
		# Creates an instance of this class
		instance = class_(dictionary)

		# Get the current Diary Slim dictionary
		current_diary_slim = instance.Current_Diary_Slim()

		# Return the current Diary Slim dictionary
		return current_diary_slim
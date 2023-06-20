# Write_On_Diary_Slim_Module.py

from Diary_Slim.Diary_Slim import Diary_Slim as Diary_Slim

class Write_On_Diary_Slim_Module(Diary_Slim):
	def __init__(self, text, time = None, add_time = True, show_text = True, add_dot = True, check_file_length = True, check_diary_slim = False, verbose = None):
		super().__init__()

		self.text = text
		self.time = time
		self.add_time = add_time
		self.show_text = show_text
		self.check_file_length = check_file_length
		self.check_diary_slim = check_diary_slim
		self.verbose = verbose

		if self.text[-1] != "." and add_dot == True:
			self.text += "."

		self.Write()

	def Write(self):
		if self.time == None:
			self.time = self.Date.Now()["Formats"]["HH:MM DD/MM/YYYY"]

		text_to_append = ""

		if self.add_time == True:
			text_to_append += self.time + ":\n"

		text_to_append += self.text

		if self.check_file_length == True:
			text_to_append = "\n\n" + text_to_append

		date = None

		# If "check_diary_slim" is False, get the most recent Diary Slim
		if self.check_diary_slim == False:
			# Get the most recent month and the most recent Diary Slim
			most_recent_month = list(self.current_year["Year"]["Months"].values())[-1]
			most_recent_diary_slim = list(most_recent_month["Diary Slims"].values())[-1]

			# Create the custom date of the most recent Diary Slim
			date = self.Date.From_String(most_recent_diary_slim["Formats"]["DD-MM-YYYY"], format = "%d-%m-%Y")

		# Create the current year dictionary
		current_year = self.Current_Diary_Slim(date = date)

		self.File.Edit(current_year["File"], text_to_append, "a", next_line = False, verbose = self.verbose)

		if self.switches["verbose"] == True:
			print()

		self.text_to_show = self.language_texts["this_text_was_written_to_the_current_diary_slim"] + ":"

		if self.switches["testing"] == True:
			self.text_to_show = self.text_to_show.replace(self.JSON.Language.language_texts["was"], self.JSON.Language.language_texts["was_not"])
			self.text_to_show = self.text_to_show.replace(":", " (" + self.language_texts["testing_is_true"] + "):")

		if text_to_append[0] == "\n":
			text_to_append = text_to_append[2:]

		self.text_to_show += "\n" + "[" + text_to_append + "]"

		if self.show_text == True and self.verbose == None:
			print(self.text_to_show)

	def __str__(self):
		return self.text_to_show
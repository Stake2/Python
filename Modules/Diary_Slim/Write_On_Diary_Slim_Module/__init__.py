# Write_On_Diary_Slim_Module.py

from Diary_Slim.Diary_Slim import Diary_Slim as Diary_Slim

class Write_On_Diary_Slim_Module(Diary_Slim):
	def __init__(self, text, time = None, custom_date = None, add_time = True, show_text = True, add_dot = True, check_file_length = True, current_diary_slim = True, verbose = None):
		super().__init__()

		self.text = text
		self.custom_date = custom_date
		self.time = time
		self.add_time = add_time
		self.show_text = show_text
		self.check_file_length = check_file_length
		self.current_diary_slim = current_diary_slim
		self.verbose = verbose

		if (
			self.text[-1] != "." and
			add_dot == True
		):
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

		# Get the current Diary Slim dictionary
		current_diary_slim = self.Current_Diary_Slim(date = self.custom_date, current_diary_slim = self.current_diary_slim)

		# Create the file
		self.File.Create(current_diary_slim["File"])

		# Edit the file with the new text
		self.File.Edit(current_diary_slim["File"], text_to_append, "a", next_line = False, verbose = self.verbose)

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
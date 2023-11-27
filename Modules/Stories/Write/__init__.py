# Write.py

from Stories.Stories import Stories as Stories

class Write(Stories):
	def __init__(self, story = None):
		super().__init__(story = story)

		self.register_task = False

		self.Select_Writing_Mode()

		print()
		print(self.large_bar)
		print()

		print(self.language_texts["story, title()"] + ":")

		story_titles = ""

		for language in self.languages["small"]:
			title = self.story["Information"]["Titles"][language]

			if title not in story_titles:
				story_titles += title

			if language != self.languages["small"][-1]:
				story_titles += "\n"

		print(story_titles)
		print()

		self.Define_Chapter()
		self.Define_Files()
		self.Open_Obsidian()

		if self.switches["testing"] == False:
			self.System.Open("https://app.grammarly.com/")
			self.System.Open("https://translate.google.com/")

		self.Finish_Writing()

		if self.chapter["finished_writing"] == True:
			self.Rename_Chapter_Files()

		self.Close_Obsidian()

		self.Define_Task_Dictionary()

		if self.chapter["finished_writing"] == True:
			self.register_task = True

		self.Register_Task()

		if self.chapter["finished_writing"] == False:
			print(self.task_dictionary["Task"]["Descriptions"][self.user_language])
			print()
			print(self.large_bar)

	def Select_Writing_Mode(self):
		options = self.language_texts["writing_modes, type: list"]
		show_text = self.language_texts["writing_modes"]
		select_text = self.language_texts["select_a_writing_mode"]

		chapter_number = self.story["Information"]["Chapters"]["Number"]

		i = 0
		for writing_mode in options:
			english_writing_mode = self.texts["writing_modes, type: list"]["en"][i]

			writing_mode_chapter = int(self.story["Information"]["Chapter status"][english_writing_mode])

			# If the chapter number in the writing mode is equal to the chapter number of the story
			# And the writing mode is not "Write"
			if (
				writing_mode_chapter == chapter_number and
				writing_mode != self.language_texts["write, title()"]
			):
				# Then remove writing mode from options list
				options.remove(writing_mode)

			# If the chapter number in the writing mode is not equal to the chapter number of the story
			if writing_mode_chapter != chapter_number:
				options[i] = options[i] + " (" + self.language_texts["chapter, title()"] + ": " + str(writing_mode_chapter + 1) + ")"

			i += 1

		# Select writing mode
		self.option_info = self.Input.Select(options, show_text = show_text, select_text = select_text)

		# Define names
		self.chapter = {
			"writing_mode": {
				"name": self.texts["writing_modes, type: list"]["en"][self.option_info["number"]],
				"names": {},
				"action": {},
				"present_action": {},
				"past_action": {},
				"past": {}
			}
		}

		for language in self.languages["small"]:
			for item in ["action", "present_action", "past_action", "past"]:
				self.chapter["writing_mode"][item][language] = self.texts["writing_modes_" + item + ", type: list"][language][self.option_info["number"]].lower()

			self.chapter["writing_mode"]["names"][language] = self.texts["writing_modes, type: list"][language][self.option_info["number"]]

		self.writing_mode = self.chapter["writing_mode"]["name"]

	def Define_Chapter(self):
		# Add to the chapter status of the writing mode
		self.story["Information"]["Chapter status"][self.writing_mode] = int(self.story["Information"]["Chapter status"][self.writing_mode]) + 1
		self.story["Information"]["Chapter status"][self.writing_mode] = str(self.story["Information"]["Chapter status"][self.writing_mode])

		# Define chapter number from chapter status
		self.chapter["number"] = self.story["Information"]["Chapter status"][self.writing_mode]
		self.chapter["number_names"] = {}

		for language in self.languages["small"]:
			self.chapter["number_names"][language] = self.Date.texts["number_names, type: list"][language][int(self.chapter["number"])]

		# Update the "Chapter status" file
		self.File.Edit(self.story["Folders"]["Information"]["Chapter status"], self.Text.From_Dictionary(self.story["Information"]["Chapter status"], next_line = True), "w")

		self.chapter["titles"] = {}

		for language in self.languages["small"]:
			full_language = self.languages["full"][language]

			self.chapter["titles"][full_language] = self.Text.Add_Leading_Zeroes(self.chapter["number"])

			if self.writing_mode in ["Revise", "Translate"]:
				self.chapter["titles"][full_language] += " - "
				self.chapter["titles"][full_language] += self.story["Information"]["Chapters"]["Titles"][language][int(self.chapter["number"]) - 1]

		print(self.language_texts["{}_this_chapter"].format(self.chapter["writing_mode"]["present_action"][self.user_language].capitalize()) + ":")
		print(self.chapter["titles"][self.full_user_language])

	def Define_Files(self):
		self.chapter["files"] = {}
		self.chapter["files"]["story"] = {}
		self.chapter["files"]["obsidian"] = {}

		for language in self.languages["small"]:
			full_language = self.languages["full"][language]

			if self.writing_mode in ["Write", "Revise"] and language == "en" or self.writing_mode == "Translate":
				self.chapter["language"] = full_language

				# Story chapter file
				self.chapter["files"]["story"][full_language] = self.story["Folders"]["Chapters"][full_language]["root"] + self.chapter["titles"][full_language] + ".txt"
				self.File.Create(self.chapter["files"]["story"][full_language])

				# Obsidian chapter file
				self.chapter["title"] = self.chapter["titles"][full_language]

				self.chapter["files"]["obsidian"][full_language] = self.story["Folders"]["Obsidian's Vaults"]["Chapters"][full_language] + self.chapter["titles"][full_language] + ".md"
				self.File.Create(self.chapter["files"]["obsidian"][full_language])

		# Define chapter language as full user language on Translate writing mode
		if self.writing_mode == "Translate":
			self.chapter["language"] = self.full_user_language

			# Copy English chapter text into user language chapter file
			text = self.File.Contents(self.chapter["files"]["story"][self.languages["full"]["en"]])["string"]

			self.File.Edit(self.chapter["files"]["obsidian"][self.full_user_language], text, "w")

	def Open_Obsidian(self):
		replace_list = [
			" ",
			"ê",
			"á",
			"ã",
			"â",
			"ç",
			"í",
			"ó",
			"ú",
			"❤️",
			"🎄",
			"🎁"
		]

		replace_with = [
			"%20",
			"%C3%AA",
			"%C3%A1",
			"%C3%A3",
			"%C3%A2",
			"%C3%A7",
			"%C3%AD",
			"%C3%B3",
			"%C3%BA",
			"%E2%9D%A4%EF%B8%8F",
			"%F0%9F%8E%84",
			"%F0%9F%8E%81"
		]

		self.chapter["title_obsidian"] = self.chapter["title"]

		# Remove unaccepted characters from chapter title
		for item in ["?", ":", "\\", "/", '"', "*", "<", ">", "|"]:
			self.chapter["title_obsidian"] = self.chapter["title_obsidian"].replace(item, "")

		# Replace file and unicode characters with encoded characters
		i = 0
		for item in replace_list:
			self.chapter["title_obsidian"] = self.chapter["title_obsidian"].replace(item, replace_with[i])

			i += 1

		# Define Obsidian chapter link
		self.chapter["obsidian_link"] = "obsidian://open?vault=Creativity&file=Literature%2FStories%2F{}%2FChapters%2F{}%2F{}"

		# Format Obsidian chapter link with story title, chapter language, and chapter title
		self.chapter["obsidian_link"] = self.chapter["obsidian_link"].format(self.story["Title"].replace(" ", "%20"), self.chapter["language"], self.chapter["title_obsidian"])

		# Define the Obsidian link to be shown
		self.chapter["obsidian_link_show"] = self.chapter["obsidian_link"].replace("%2F", "/")
		self.chapter["obsidian_link_show"] = self.chapter["obsidian_link_show"].replace("%20", " ") + ".md"

		self.obsidian = {}

		import win32com.client

		# Create shortcut file
		self.obsidian["lnk"] = self.story["Folders"]["Obsidian's Vaults"]["root"] + "Obsidian.lnk"
		self.obsidian["target"] = self.chapter["obsidian_link"]
		self.obsidian["icon"] = self.user_folders["appdata"]["local"] + "/Obsidian/Obsidian.exe"

		# Create shortcut
		shell = win32com.client.Dispatch("WScript.Shell")
		self.obsidian["shortcut"] = shell.CreateShortCut(self.obsidian["lnk"])
		self.obsidian["shortcut"].Targetpath = self.obsidian["target"]
		self.obsidian["shortcut"].IconLocation = self.obsidian["icon"]
		self.obsidian["shortcut"].save()

		# Create Obsidian bat
		self.obsidian["bat"] = self.story["Folders"]["Obsidian's Vaults"]["root"] + "Obsidian.bat"
		self.File.Create(self.obsidian["bat"])

		# Write to Obsidian bat
		text = "@Echo off\nchcp 65001\n" + '"' + self.obsidian["lnk"] + '"'
		self.File.Edit(self.obsidian["bat"], text, "w")

		print()
		print(self.language_texts["obsidian_link"] + ":")
		print(self.chapter["obsidian_link_show"])

		# Open Obsidian bat
		if self.switches["testing"] == False:
			self.System.Open(self.obsidian["bat"])

	def Finish_Writing(self):
		# Ask to start counting writing time
		type_text = self.language_texts["press_enter_to_start_counting_{}_time"].format(self.chapter["writing_mode"]["past_action"][self.user_language])

		self.Input.Type(type_text)

		# Define start writing time
		self.chapter["start_writing_time"] = self.Date.Now()["Formats"]["HH:MM DD/MM/YYYY"]

		print()
		print(self.Date.language_texts["now_time"] + ":")
		print(self.chapter["start_writing_time"])

		# Ask for user to finish writing
		type_text = self.language_texts["press_enter_when_you_finish_{}_the_chapter"].format(self.chapter["writing_mode"]["action"][self.user_language])

		self.Input.Type(type_text)

		# Define finish writing time
		self.chapter["finish_writing_time"] = self.Date.Now(self.chapter["finish_writing_time"])["Formats"]["HH:MM DD/MM/YYYY"]

		# Define time difference
		self.chapter["time_difference"] = self.Date.Difference(self.chapter["start_writing_time"], self.chapter["finish_writing_time"])

		# Make time difference using already defined "started writing time"
		if self.story["Information"]["Writing"]["Time"][self.writing_mode]["first"] != "":
			self.story["Information"]["Writing"]["Time"][self.writing_mode]["last"] = self.Date.From_String(self.story["Information"]["Writing"]["Time"][self.writing_mode]["last"])["Object"]

			dict_ = self.chapter["time_difference"]["Difference"]

			# Add Relativedelta to the "started writing time"
			self.story["Information"]["Writing"]["Time"][self.writing_mode]["last"] = self.story["Information"]["Writing"]["Time"][self.writing_mode]["last"] + self.Date.Relativedelta(**dict_)

			self.story["Information"]["Writing"]["Time"][self.writing_mode]["last"] = self.Date.Now(self.story["Information"]["Writing"]["Time"][self.writing_mode]["last"])["Formats"]["HH:MM DD/MM/YYYY"]

		# Ask if user finished writing the chapter
		self.chapter["finished_writing"] = self.Input.Yes_Or_No(self.language_texts["did_you_finished_{}_the_chapter"].format(self.chapter["writing_mode"]["action"][self.user_language]))

		# Make empty dictionary
		dict_ = {}

		for item in self.texts["writing_modes, type: list"]["en"]:
			dict_[item] = {}
			dict_[item]["first"] = ""
			dict_[item]["last"] = ""

		# Update first writing time with finish writing time
		if self.story["Information"]["Writing"]["Time"][self.writing_mode]["first"] == "":
			self.story["Information"]["Writing"]["Time"][self.writing_mode]["first"] = self.chapter["finish_writing_time"]

		# Define existing dictionary
		if self.chapter["finished_writing"] == False:
			dict_ = self.story["Information"]["Writing"]["Time"]

		# Update writing time JSON file
		file = self.story["Folders"]["Information"]["Writing"]["Time"]
		self.JSON.Edit(file, dict_)

		# Make time difference from past first and last writing times
		if self.chapter["finished_writing"] == True:	
			self.chapter["time_difference"] = self.Date.Difference(self.story["Information"]["Writing"]["Time"][self.writing_mode]["first"], self.story["Information"]["Writing"]["Time"][self.writing_mode]["last"])

		# Show the finish writing time
		item = self.chapter["writing_mode"]["past_action"][self.user_language]

		print()
		print(self.Date.language_texts["after_{}_time"].format(item) + ":")
		print(self.chapter["finish_writing_time"])
		print()

		# Show the time difference
		print(self.Date.language_texts["time_difference"] + ":")
		print(self.chapter["time_difference"]["Text"][self.user_language])
		print()

		print(self.large_bar)

	def Rename_Chapter_Files(self):
		# Ask for the new chapter titles
		if self.writing_mode == "Write":
			for language in self.languages["small"]:
				full_language = self.languages["full"][language]
				translated_language = self.languages["full_translated"][language][self.user_language]

				# Ask for chapter title
				self.chapter["titles"][full_language] += " - " + self.Input.Type(self.language_texts["type_or_paste_the_chapter_title_in_{}"].format(translated_language))

				titles_text = self.JSON.Language.texts["titles, title()"][language]

				# Define titles file
				file = self.story["Folders"]["Chapters"][full_language][titles_text][titles_text]

				# Write new chapter title to titles file
				self.File.Edit(file, self.chapter["titles"][full_language], "a")

		# Rename story chapter file
		for key in self.chapter["files"]["story"]:
			source_file = self.chapter["files"]["story"][key]

			# Write Obsidian text into story chapter file
			self.File.Edit(source_file, self.File.Contents(self.chapter["files"]["obsidian"][key])["string"], "w")

			# Update chapter file path with chapter title
			self.chapter["files"]["story"][key] = self.story["Folders"]["Chapters"][key]["root"] + self.chapter["titles"][key] + ".txt"

			if source_file != self.chapter["files"]["story"][key]:
				self.File.Move(source_file, self.chapter["files"]["story"][key])

		# Rename Obsidian chapter file
		for key in self.chapter["files"]["obsidian"]:
			source_file = self.chapter["files"]["obsidian"][key]

			# Update chapter file path with chapter title
			self.chapter["files"]["obsidian"][key] = self.story["Folders"]["Obsidian's Vaults"]["Chapters"][key] + self.chapter["titles"][key] + ".md"

			if source_file != self.chapter["files"]["obsidian"][key]:
				self.File.Move(source_file, self.chapter["files"]["obsidian"][key])

	def Register_Task(self):
		# Define task dictionary, to use it on Tasks class
		self.task_dictionary = {
			"Task": {
				"Titles": {},
				"Descriptions": {}
			}
		}

		# Define I text based on finished writing or not
		i_text = self.texts["i_started_{}_the_chapter_{}_of_my_story_{}"]

		if self.chapter["finished_writing"] == True:
			i_text = self.texts["i_{}_the_chapter_{}_of_my_story_{}"]

		# Create task titles and descriptions
		for language in self.languages["small"]:
			full_language = self.languages["full"][language]
			translated_user_language = self.languages["full_translated"][self.user_language][language]

			parameters = self.chapter["writing_mode"]["action"][language], self.chapter["number_names"][language], self.story["Titles"][language]

			# Add past writing mode to parameters list
			if self.chapter["finished_writing"] == True:
				parameters = list(parameters)
				parameters[0] = self.chapter["writing_mode"]["past"][language]
				parameters = tuple(parameters)

			# Create task titles
			self.task_dictionary["Task"]["Titles"][language] = i_text[language]
			self.task_dictionary["Task"]["Titles"][language] = self.task_dictionary["Task"]["Titles"][language].format(*parameters)

			# Add translated user language to task name if writing mode is "Translate"
			if self.writing_mode == "Translate":
				self.task_dictionary["Task"]["Titles"][language] += " " + self.JSON.Language.texts["to"][language] + " " + translated_user_language

			self.task_dictionary["Task"]["Titles"][language] += "."

			# Create task descriptions
			self.task_dictionary["Task"]["Descriptions"][language] = self.task_dictionary["Task"]["Titles"][language]

			# Add writing time
			self.task_dictionary["Task"]["Descriptions"][language] += "\n\n"

			text = self.chapter["writing_mode"]["past_action"][language]

			if self.Date.texts["{}_time"][language][0] == "{":
				text = text.capitalize()

			self.task_dictionary["Task"]["Descriptions"][language] += self.Date.texts["{}_time"][language].format(text) + ":" + "\n"
			self.task_dictionary["Task"]["Descriptions"][language] += self.chapter["time_difference"]["Text"][language]

			# Add "still did not finished writing" text to task description if did not finished writing
			if self.chapter["finished_writing"] == False:
				self.task_dictionary["Task"]["Descriptions"][language] += "\n\n"
				self.task_dictionary["Task"]["Descriptions"][language] += self.texts["i_still_did_not_finished_{}_the_chapter"][language].format(self.chapter["writing_mode"]["action"][language]) + "."

		# Register the task with the root method
		Stories.Register_Task(self, self.task_dictionary, register_task = self.register_task)

	def Close_Obsidian(self):
		# Close Obsidian
		self.File.Close("Obsidian")

		# Delete lnk file
		self.File.Delete(self.obsidian["lnk"])

		# Delete bat file
		self.File.Delete(self.obsidian["bat"])
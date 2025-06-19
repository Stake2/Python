# Copy_Story_Titles.py

from Stories.Stories import Stories as Stories

class Copy_Story_Titles(Stories):
	def __init__(self):
		super().__init__()

		# Define the root dictionary
		self.dictionary = {
			"Texts": {
				"Show": "",
				"Select": ""
			},
			"Lists": {},
			"Story title": "",
			"Copy modes": {
				"List": self.texts["copy_modes, type: list"],
				"Language": self.language_texts["copy_modes, type: list"]
			},
			"Copy mode": {},
			"Copy actions": {
				"List": self.texts["copy_actions, type: list"],
				"Language": self.language_texts["copy_actions, type: list"]
			}
		}

		## Define the states dictionary
		self.states = {
			"First change of copy mode": True,
			"Junction mode": False
		}

		# Create the lists of story titles
		self.Create_Titles_Lists()

		# Select the copy mode
		self.Select_Copy_Mode()

		# While the selected story title is not the "[Quit]" text
		while self.dictionary["Story title"] != self.Language.language_texts["quit, title()"]:
			# If the junction mode is deactivated
			if self.states["Junction mode"] == False:
				# Select and copy the story title
				self.Select_And_Copy_Story_Title()

				# If the selected story title is the "[Change mode]" text
				if self.dictionary["Story title"] == "[" + self.language_texts["change_copy_mode"] + "]":
					# Run the "Select_Copy_Mode" method to select a new copy mode
					self.Select_Copy_Mode()

			# If the junction mode is activated
			if self.states["Junction mode"] == True:
				# Join the story titles
				self.Join_Story_Titles()

			# If the story title is the "[Quit]" text, quit
			if self.dictionary["Story title"] == "[" + self.Language.language_texts["quit, title()"] + "]":
				break

	def Create_Titles_Lists(self):
		# Add the copy modes to the "Lists" dictionary, with their empty lists
		for copy_mode in self.dictionary["Copy modes"]["Language"]:
			self.dictionary["Lists"][copy_mode] = []

		# Import the "ascii_uppercase" module
		from string import ascii_uppercase as ascii_uppercase

		# Iterate through the list of all story titles in all languages
		for story_title in self.stories["Titles"]["All"]:
			# Iterate through the list of copy modes in the user language
			for copy_mode in self.dictionary["Copy modes"]["Language"]:
				# If the copy mode is "With quotes"
				# Add quotes around the story title 
				if copy_mode == self.language_texts["with_quotes"]:
					story_title = '"' + story_title + '"'

				# If the copy mode is "Acronym"
				# Separate the letters of the story title
				if copy_mode == self.Language.language_texts["acronym, title()"]:
					# Split the story title
					story_title = story_title.split(" ")

					# Define the empty string
					string = ""

					# Iterate through the words in the split story title
					for word in story_title:
						# Count the uppercase letters inside the word
						uppercase_letters = sum(1 for character in word if character.isupper())

						# If the number of uppercase letters is zero or one
						if uppercase_letters in [0, 1]:
							# If the first letter of the word is not a quote, add the first letter to the acronym
							if word[0] != '"':
								string += word[0]

							# Else, add the second letter, which probably is not a quote
							else:
								string += word[1]

						# If there are more than one uppercase character in the word
						if uppercase_letters > 1:
							# Iterate through the characters in the word
							for character in word:
								# If the character is not a quote
								# And the character is an uppercase letter
								if (
									character != '"' and
									character in ascii_uppercase
								):
									# Add the character
									string += character

					# Define the local story title as the defined string
					story_title = string

				# Add the story title to the list of the current copy mode
				self.dictionary["Lists"][copy_mode].append(story_title)

	def Select_Copy_Mode(self):
		# Define the list of options, which is the list of copy modes in the user language
		options = self.dictionary["Copy modes"]["Language"].copy()

		# Add the "Quit" text to the list of options
		options.append("[" + self.Language.language_texts["quit, title()"] + "]")

		# Define the show and select text
		show_text = self.language_texts["copy_modes"]
		select_text = self.language_texts["select_a_copy_mode"]

		# Ask the user to select a copy mode
		self.dictionary["Copy mode"] = self.Input.Select(options, show_text = show_text, select_text = select_text)["option"]

		# Define the "Copy mode" dictionary
		self.dictionary["Copy mode"] = {
			"Name": self.dictionary["Copy mode"],
			"Texts": {},
			"List": {}
		}

		# Define the text key for the copy mode text
		text_key = "story_title"

		# If the copy mode is the "Acronym" mode
		if self.dictionary["Copy mode"]["Name"] == self.Language.language_texts["acronym, title()"]:
			# Update the text key to "story_acronym"
			text_key = "story_acronym"

		# Define the text of the copy mode
		for item in ["Singular", "Plural"]:
			# Make a copy of the text key
			text_key_copy = text_key

			# If the text key is "story_title"
			# And the item is the "Singular" one
			if (
				text_key == "story_title" and
				item == "Singular"
			):
				# Add the ", type: generic" text to the text key
				text_key_copy += ", type: generic"

			# If the item is the "Plural" one, add an "s" to make the text plural
			if item == "Plural":
				text_key_copy += "s"

			# Define the item text as the language text from inside the "Language" module
			self.dictionary["Copy mode"]["Texts"][item] = self.Language.language_texts[text_key_copy].lower()

		# If the name of the copy mode is "Quit", quit
		if self.dictionary["Copy mode"]["Name"] == "[" + self.Language.language_texts["quit, title()"] + "]":
			quit()

		# Define the "List" dictionary, with the list of story titles of the selected copy mode
		self.dictionary["Copy mode"]["List"] = {
			"Normal": self.dictionary["Lists"][self.dictionary["Copy mode"]["Name"]]
		}

		# Define the other type of lists
		# That are the normal list with some changes
		items = [
			"With actions",
			"With actions (no mode change)"
		]

		# Iterate through the different lists
		for item in items:
			self.dictionary["Copy mode"]["List"][item] = self.dictionary["Copy mode"]["List"]["Normal"].copy()

		# Create the "Junction actions" dictionary with the list of actions
		# Only if the change of mode is the first one
		if self.states["First change of copy mode"] == True:
			self.dictionary["Junction actions"] = {
				"List": [
					"[" + self.Language.language_texts["join_{}"] + "]",
					"[" + self.language_texts["disable_junction_mode"] + "]"
				]
			}

		# Iterate through the copy actions list
		for action in self.dictionary["Copy actions"]["Language"]:
			# Define the value
			value = action

			# If the "{}" text is in the action value, format it with the plural copy mode text
			if "{}" in value:
				value = value.format(self.dictionary["Copy mode"]["Texts"]["Plural"])

			# If the action is not on the junction actions list
			if action not in self.dictionary["Junction actions"]["List"]:
				# Add the value to the list of story titles with actions
				self.dictionary["Copy mode"]["List"]["With actions"].append(value)

				# If the action is not the "Change mode" action
				if action != "[" + self.language_texts["change_copy_mode"] + "]":
					# Add the value to the list of story titles with actions and no mode change
					self.dictionary["Copy mode"]["List"]["With actions (no mode change)"].append(value)

				# If the action is the "Change mode" action
				if action == "[" + self.language_texts["change_copy_mode"] + "]":
					# Add a filler to the list of story titles with actions and no mode change
					self.dictionary["Copy mode"]["List"]["With actions (no mode change)"].append(self.language_texts["filler_formatted"])

			# If the action is the "Join" junction action
			if action == "[" + self.Language.language_texts["join_{}"] + "]":
				# Add it to the "Join" key of the "Junction actions" dictionary
				self.dictionary["Junction actions"]["Join"] = value

				# If the junction mode is deactivated
				if self.states["Junction mode"] == False:
					# Add the value to the list of story titles with actions
					self.dictionary["Copy mode"]["List"]["With actions"].append(value)

			# If the action is the "Disable junction mode" junction action
			if action == "[" + self.language_texts["disable_junction_mode"] + "]":
				# If the junction mode is activated
				if self.states["Junction mode"] == True:
					# Add the value to the list of story titles with actions
					self.dictionary["Copy mode"]["List"]["With actions"].append(value)

				# Add the value to the list of story titles with actions and no mode change
				self.dictionary["Copy mode"]["List"]["With actions (no mode change)"].append(value)

	def Select_And_Copy_Story_Title(self, options = None, select_text = None, select = True, copy = True):
		# If the "options" parameter is None
		if options == None:
			# Define the options list as the list of story titles with actions
			options = self.dictionary["Copy mode"]["List"]["With actions"]

		# Define the show text as the plural copy mode text
		show_text = self.dictionary["Copy mode"]["Texts"]["Plural"].capitalize()

		# If the show text inside the root dictionary is not an empty string
		if self.dictionary["Texts"]["Show"] != "":
			# Define the show text as the original text, two line breaks, and the plural copy mode text
			show_text = self.dictionary["Texts"]["Show"] + "\n\n" + self.dictionary["Copy mode"]["Texts"]["Plural"].capitalize()

		# If the "select_text" parameter is None
		if select_text == None:
			# Define the select text as the "Select one {} to copy" text
			select_text = self.language_texts["select_one_{}_to_copy"]

		# If the select text inside the root dictionary is not an empty string
		if self.dictionary["Texts"]["Select"] != "":
			# Define the select text as the original text, one line break, and the "Please select one {} to copy" text
			select_text = self.dictionary["Texts"]["Select"] + "\n" + self.language_texts["please_select_one_{}_to_copy"]

			# Reset the select text inside the root dictionary to an empty string
			self.dictionary["Texts"]["Select"] = ""

		# Format the select text with the singular copy mode text
		select_text = select_text.format(self.dictionary["Copy mode"]["Texts"]["Singular"])

		# Define the default "number" variable
		number = 0

		# If the "select" parameter is True
		if select == True:
			# Ask the user to select the story title
			self.dictionary["Story title"] = self.Input.Select(options, show_text = show_text, select_text = select_text)

			# Get the option number
			number = self.dictionary["Story title"]["number"]

			# Define the story title as the option
			self.dictionary["Story title"] = self.dictionary["Story title"]["option"]

			# If the story title is the "Change mode" action
			if self.dictionary["Story title"] == "[" + self.language_texts["change_copy_mode"] + "]":
				# It is now not the first time the user changes the copy mode
				self.states["First change of copy mode"] = False

			# If the story title is the "Join" action
			if self.dictionary["Story title"] == self.dictionary["Junction actions"]["Join"]:
				# Activate the junction mode
				self.states["Junction mode"] = True

			# If the story title is the "Disable junction mode" action
			if self.dictionary["Story title"] == "[" + self.language_texts["disable_junction_mode"] + "]":
				# Deactivate the junction mode
				self.states["Junction mode"] = False

			# If the story title is the "[Quit]" text
			if self.dictionary["Story title"] == "[" + self.Language.language_texts["quit, title()"] + "]":
				# Finish copying the story titles and show some information
				self.Finish_Copying()

		# Create a list of items that should not be copied (copy actions and the filler text)
		self.dictionary["Lists"]["Negative"] = []
		self.dictionary["Lists"]["Negative"].extend(self.dictionary["Copy actions"]["Language"])
		self.dictionary["Lists"]["Negative"].append(self.language_texts["filler_formatted"])

		# If the story title is not in the negative list (of items that should not be copied)
		# And the "copy" parameter is True
		if (
			self.dictionary["Story title"] not in self.dictionary["Lists"]["Negative"] and
			copy == True
		):
			# Copy the story title
			self.Text.Copy(self.dictionary["Story title"])

		# If the story title is not the filler text, reset the show text to an empty string
		if self.dictionary["Story title"] != self.language_texts["filler_formatted"]:
			self.dictionary["Texts"]["Show"] = ""

		# If the story title is the filler text
		if self.dictionary["Story title"] == self.language_texts["filler_formatted"]:
			# Add the filler explanation text to the show text, telling the user that they selected a filler text
			self.dictionary["Texts"]["Show"] = self.language_texts["you_selected_a_filler_text, type: explanation"].format(len(self.dictionary["Copy mode"]["List"]["With actions"]), len(options))

		return number

	def Join_Story_Titles(self):
		# Define the "joined story title" variable as an empty string
		joined_story_title = ""

		# Define the local list of story titles
		story_titles = self.dictionary["Copy mode"]["List"]["With actions (no mode change)"].copy()

		# Iterate through the list of items (first and second story title)
		for item in ["First", "Second"]:
			# If the junction mode is activated
			if self.states["Junction mode"] == True:
				# Define the text template for the select text of the story title
				template = self.language_texts["select_{}_to_{}"]

				# Define the list of items to use to format the template
				items = [
					self.Language.language_texts["the_" + item.lower() + ", masculine"] + " " + self.dictionary["Copy mode"]["Texts"]["Singular"],
					self.Language.language_texts["join"]
				]

				# Format the template with the list of items
				select_text = template.format(*items)

				# Select the first story title, and do not copy it
				number = self.Select_And_Copy_Story_Title(options = story_titles, select_text = select_text, copy = False)

				# If the story title is the filler text, ask again for the first story title
				if self.dictionary["Story title"] == self.language_texts["filler_formatted"]:
					# While the story title is the filler text, ask again for the first story title
					while self.dictionary["Story title"] == self.language_texts["filler_formatted"]:
						number = self.Select_And_Copy_Story_Title(options = story_titles, select_text = select_text, copy = False)

				# If the story title is not in the negative list (of items that should not be copied)
				if self.dictionary["Story title"] not in self.dictionary["Lists"]["Negative"]:
					# Define the index in the story titles list as the filler, removing the old selected story title
					story_titles[number] = self.language_texts["filler_formatted"]

			# If the first story title is the "Disable junction mode" text
			if self.dictionary["Story title"] == "[" + self.language_texts["disable_junction_mode"] + "]":
				# Disable the junction mode
				self.states["Junction mode"] = False

			# If the story title is the "[Quit]" text
			if self.dictionary["Story title"] == "[" + self.Language.language_texts["quit, title()"] + "]":
				quit()

			# If the junction mode is activated
			if self.states["Junction mode"] == True:
				# If the item is the second one
				if item == "Second":
					# Add a dash separator to the joined story title
					joined_story_title += " - "

				# Add the story title to the empty string
				joined_story_title += self.dictionary["Story title"]

				# If the story title is not the "Disable junction mode" text
				# And the item is the second one
				if (
					self.dictionary["Story title"] != "[" + self.language_texts["disable_junction_mode"] + "]" and
					item == "Second"
				):
					# Define the story title to be copied as the joined story title
					self.dictionary["Story title"] = joined_story_title

					# Now copy the joined story title
					self.Select_And_Copy_Story_Title(select = False, copy = True)

		# If the first story title is the "Disable junction mode" text
		if self.dictionary["Story title"] == "[" + self.language_texts["disable_junction_mode"] + "]":
			# Disable the junction mode
			self.states["Junction mode"] = False

	def Finish_Copying(self):
		# Show some spaces and a five dash space separator
		print()
		print(self.separators["5"])
		print()

		# Show the information telling the user that they finished copying the story titles with the plural copy mode text
		print(self.language_texts["you_finished_copying_the_{}"].format(self.dictionary["Copy mode"]["Texts"]["Plural"]) + ".")
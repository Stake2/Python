# Copy_Story_Titles.py

from Stories.Stories import Stories as Stories

class Copy_Story_Titles(Stories):
	def __init__(self):
		super().__init__()

		self.switches = {
			"junction": False,
			"first_mode_change": True
		}

		self.show_text = None
		self.select_text = None

		self.Make_Story_Titles_List()

		self.Select_Copy_Mode()

		self.story_title = None

		while self.story_title != self.Language.language_texts["quit, title()"]:
			if self.switches["junction"] == False:
				self.Select_And_Copy_Story_Title()

				if self.story_title == "[" + self.language_texts["change_mode"] + "]":
					self.Select_Copy_Mode()

			if self.switches["junction"] == True:
				self.Join_Story_Titles()

			if self.story_title == "[" + self.Language.language_texts["quit, title()"] + "]":
				break

	def Make_Story_Titles_List(self):
		# Add copy modes to stories dictionary
		self.stories["copy_lists"] = {}

		for copy_mode in self.language_texts["copy_modes, type: list"]:
			self.stories["copy_lists"][copy_mode] = []

		from string import ascii_uppercase as ascii_uppercase

		# Iterate through list of story titles
		for story_title in self.stories["Titles"]["All"]:
			for copy_mode in self.language_texts["copy_modes, type: list"]:
				# Add quotes around story title
				if copy_mode == self.language_texts["with_quotes"]:
					story_title = '"' + story_title + '"'

				# Separate letters of story title
				if copy_mode == self.Language.language_texts["acronym, title()"]:
					story_title = story_title.split(" ")

					string = ""
					for word in story_title:
						uppercase_letters = sum(1 for character in word if character.isupper())

						# If there are only one uppercase character in word
						if uppercase_letters in [0, 1]:
							if word[0] != '"':
								string += word[0]

							else:
								string += word[1]

						# If there are more than one uppercase character in word
						if uppercase_letters > 1:
							for character in word:
								if character in ascii_uppercase and character != '"':
									string += character

					story_title = string

				self.stories["copy_lists"][copy_mode].append(story_title)

	def Select_Copy_Mode(self):
		options = self.language_texts["copy_modes, type: list"].copy()
		options.append("[" + self.Language.language_texts["quit, title()"] + "]")

		show_text = self.language_texts["copy_modes"]
		select_text = self.language_texts["select_a_copy_mode"]

		# Select a copy mode
		self.copy_mode = self.Input.Select(options, show_text = show_text, select_text = select_text)["option"]

		# Create the copy mode dictionary
		self.copy_mode = {
			"name": self.copy_mode,
			"item": self.Language.language_texts["story_title"].lower(),
			"plural_item": self.Language.language_texts["story_titles"].lower()
		}

		# If the copy mode is acronym mode, update item and plural_item keys
		if self.copy_mode["name"] == self.Language.language_texts["acronym, title()"]:
			self.copy_mode.update({
				"item": self.language_texts["story_acronym"].lower(),
				"plural_item": self.language_texts["story_acronyms"].lower()
			})

		if self.copy_mode["name"] == "[" + self.Language.language_texts["quit, title()"] + "]":
			quit()

		# Define story titles list of the copy mode
		self.copy_mode["list"] = self.stories["copy_lists"][self.copy_mode["name"]]

		# Copy the story titles list to add actions to it
		self.copy_mode["list_with_actions"] = self.copy_mode["list"].copy()

		# Copy the story titles list to add actions to it, but not adding the "change mode" action
		self.copy_mode["list, actions, no change mode"] = self.copy_mode["list"].copy()

		# List with quit option added
		self.copy_mode["list, quit"] = self.copy_mode["list"].copy()

		# Add fillers to story titles list with quit action
		# In place of "change mode" and "join" actions
		self.copy_mode["list, quit"].append(self.language_texts["filler_formatted"])
		self.copy_mode["list, quit"].append(self.language_texts["filler_formatted"])
		self.copy_mode["list, quit"].append("[" + self.Language.language_texts["quit, title()"] + "]")

		# Create actions dictionary with actions list
		if self.switches["first_mode_change"] == True:
			self.junction_actions = {
				"list": [
					"[" + self.Language.language_texts["join_{}"] + "]",
					"[" + self.language_texts["disable_junction_mode"] + "]"
				]
			}

		# Iterate through copy actions list
		for action in self.language_texts["copy_actions, type: list"]:
			action_value = action

			# If "{}" is in the action value, format it with the plural item
			if "{}" in action_value:
				action_value = action_value.format(self.copy_mode["plural_item"])

			# If the action is not on the junction actions list
			if action not in self.junction_actions["list"]:
				self.copy_mode["list_with_actions"].append(action_value)

				# If the action is not the "change mode" action, add it to the story titles list without the change mode action
				if action != "[" + self.language_texts["change_mode"] + "]":
					self.copy_mode["list, actions, no change mode"].append(action_value)

				# If the action is the "change mode" action, add a filler to the story titles list without the change mode action
				if action == "[" + self.language_texts["change_mode"] + "]":
					self.copy_mode["list, actions, no change mode"].append(self.language_texts["filler_formatted"])

			# If the action is the "join" junction action, add it to the "join_{}" key of the junction_actions dictionary
			if action == "[" + self.Language.language_texts["join_{}"] + "]":
				self.junction_actions["join_{}"] = action_value

				# If the join mode is deactivated, add the join action to the list with actions
				if self.switches["junction"] == False:
					self.copy_mode["list_with_actions"].append(action_value)

			# If the action is the "disable junction mode" junction action, add it to the story titles list without the change mode action
			if action == "[" + self.language_texts["disable_junction_mode"] + "]":
				# If the join mode is activated, add the disable action to the list with actions
				if self.switches["junction"] == True:
					self.copy_mode["list_with_actions"].append(action_value)

				self.copy_mode["list, actions, no change mode"].append(action_value)

	def Select_And_Copy_Story_Title(self, options = None, select_text = None, select = True, copy = True):
		if options == None:
			options = self.copy_mode["list_with_actions"]

		show_text = self.copy_mode["plural_item"].capitalize()

		if self.show_text != None:
			show_text = self.show_text + "\n\n" + self.copy_mode["plural_item"].capitalize()

		if select_text == None:
			select_text = self.language_texts["select_one_{}_to_copy"]

		if self.select_text != None:
			select_text = self.select_text + "\n" + self.language_texts["please_select_one_{}_to_copy"]

			self.select_text = None

		select_text = select_text.format(self.copy_mode["item"])

		# Select story title
		if select == True:
			self.story_title = self.Input.Select(options, show_text = show_text, select_text = select_text)["option"]

			# If the story title is the change mode action, it is not the first time that the copy mode changes
			if self.story_title == "[" + self.language_texts["change_mode"] + "]":
				self.switches["first_mode_change"] = False

			# If the story title is the join action, activate join mode
			if self.story_title == self.junction_actions["join_{}"]:
				self.switches["junction"] = True

			# If the story title is the disable junction mode action, deactivate join mode
			if self.story_title == "[" + self.language_texts["disable_junction_mode"] + "]":
				self.switches["junction"] = False

			# Check if the story title is the quit text
			self.Check_Story_Title()

		# Create a list of items that should not be copied (copy actions and the filler)
		self.negative_lists = []
		self.negative_lists.extend(self.language_texts["copy_actions, type: list"])
		self.negative_lists.append(self.language_texts["filler_formatted"])

		# Copy the story title if it is not in the list above, and copy is true
		if self.story_title not in self.negative_lists and copy == True:
			self.Text.Copy(self.story_title)

		# If the story title is not the filler, reset show_text to none
		if self.story_title != self.language_texts["filler_formatted"]:
			self.show_text = None

		# If the story title is the filler, add filler explanation to the show_text
		if self.story_title == self.language_texts["filler_formatted"]:
			self.show_text = self.language_texts["you_selected_a_filler_text, type: explanation"].format(len(self.copy_mode["list_with_actions"]), len(options))

	def Check_Story_Title(self):
		# Check if the story title is the quit text, if it is, show the "finished copying story titles" text
		if self.story_title == "[" + self.Language.language_texts["quit, title()"] + "]":
			self.Finish_Copying()

	def Join_Story_Titles(self):
		# Create the empty string which will be the joined story title
		joined_story_title = ""

		select_text = self.language_texts["select_{}_to_{}"].format(self.Language.language_texts["the_first, masculine"] + " " + self.copy_mode["item"], self.Language.language_texts["join"])

		# Select the first story title, do not copy
		self.Select_And_Copy_Story_Title(options = self.copy_mode["list, actions, no change mode"], select_text = select_text, copy = False)

		# If the story title is the filler, ask again
		if self.story_title == self.language_texts["filler_formatted"]:
			# While the story title is the filler, ask again
			while self.story_title == self.language_texts["filler_formatted"]:
				self.Select_And_Copy_Story_Title(options = self.copy_mode["list, actions, no change mode"], select_text = select_text, copy = False)

		if self.story_title == "[" + self.Language.language_texts["quit, title()"] + "]":
			quit()

		if self.story_title != "[" + self.language_texts["disable_junction_mode"] + "]":
			# Add the first story title to the empty string
			joined_story_title += self.story_title

			select_text = self.language_texts["select_{}_to_{}"].format(self.Language.language_texts["the_second, masculine"] + " " + self.copy_mode["item"], self.Language.language_texts["join"])

			# Select the second story title, do not copy
			self.Select_And_Copy_Story_Title(options = self.copy_mode["list, quit"], select_text = select_text, copy = False)

			# If the story title is the filler, ask again
			if self.story_title == self.language_texts["filler_formatted"]:
				# While the story title is the filler, ask again
				while self.story_title == self.language_texts["filler_formatted"]:
					self.Select_And_Copy_Story_Title(options = self.copy_mode["list, quit"], select_text = select_text, copy = False)

			if self.story_title == "[" + self.Language.language_texts["quit, title()"] + "]":
				quit()

			# Add the separator and the second story title to the joined story title
			joined_story_title += " - " + self.story_title

			# Define the story title to be copied
			self.story_title = joined_story_title

			self.Select_And_Copy_Story_Title(select = False, copy = True)

		# If the first story title is the disable junction mode action, disable junction mode
		if self.story_title == "[" + self.language_texts["disable_junction_mode"] + "]":
			self.switches["junction"] = False

	def Finish_Copying(self):
		print()
		print("-----")
		print()
		print(self.language_texts["finished_copying_the_{}"].format(self.copy_mode["plural_item"]) + ".")
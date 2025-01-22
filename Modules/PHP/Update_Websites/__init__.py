# Update_Websites.py

from PHP.PHP import PHP as PHP

class Update_Websites(PHP):
	def __init__(self, dictionary = {}):
		super().__init__()

		# Define the root dictionary
		self.dictionary = {
			"Websites": {
				"Dictionary": {},
				"To update": []
			},
			"Languages": {},
			"URL": {},
			"Verbose": False
		}

		# Define the "States" dictionary
		self.states = {
			"Select website": True,
			"First time updating": True,
			"Create list of websites": False,
			"Update more websites": False,
			"One website": True
		}

		# Create the list of keys to use to update the root dictionary
		keys = list(self.dictionary.keys())

		# Remove the "Websites" key
		keys.remove("Websites")

		# Iterate through the keys of the root dictionary
		for key in self.dictionary:
			# If the key is inside the parameter dictionary
			if key in dictionary:
				# Update the key in the root dictionary
				self.dictionary[key] = dictionary[key]

		# Define the languages for the websites
		self.Define_Languages()

		# Define the server to use to update the websites
		self.Define_Server()

		# Define the websites that are going to be updated
		# Either by asking the user to select them, or using the ones that came from the "dictionary" parameter
		self.Define_Websites(dictionary)

		# Manage the server used to update the websites, opening it in this case
		self.Manage_Server(open = True)

		# Update the websites on the list of websites
		self.Update_Websites()

		# If the "Create list of websites" state is False
		if self.states["Create list of websites"] == False:
			# Define the "Update more websites" state as True
			self.states["Update more websites"] = True

			# While the "Update more websites" state is True
			while self.states["Update more websites"] == True:
				# Ask if the user wants to update more websites
				self.states["Update more websites"] = self.Input.Yes_Or_No(self.language_texts["update_more_websites"])

				# If the answer is yes
				if self.states["Update more websites"] == True:
					# Ask the user to select the website
					self.Select_Website()

					# Show a space separator
					print()

					# Update the selected website
					self.Update_Websites()

		# Close the server as all selected or defined websites were updated
		self.Manage_Server(close = True)

		# Open Git to commit the changes to the repository of the websites
		self.Open_Git()

		# Show a five dash space separator
		print()
		print(self.separators["5"])
		print()

		# Define the text to show
		text = self.language_texts["you_finished_updating_this_website"]

		# If the "One website" state is False
		if self.states["One website"] == False:
			# Define the text as its plural version
			text = self.language_texts["you_finished_updating_these_websites"]

		# Show the information text with a colon
		print(text + ":")

		# Show the list of updated websites
		for website in self.dictionary["Websites"]["Dictionary"].values():
			# Get the website title
			website_title = website["Titles"][self.user_language]

			# Show it with a tab
			print("\t" + website_title)

	def Define_Languages(self):
		# Define the "Languages" dictionary
		self.dictionary["Languages"] = {
			"Small": [],
			"Full": {},
			"Full translated": {}
		}

		# Add the "General" language
		self.dictionary["Languages"]["Small"].append("general")
		self.dictionary["Languages"]["Full"]["general"] = "General"
		self.dictionary["Languages"]["Full translated"]["general"] = {}

		# Iterate through the list of small languages
		for language in self.languages["small"]:
			self.dictionary["Languages"]["Full translated"]["general"][language] = self.Language.texts["general, title()"][language]

		# Add the other languages
		for language in self.languages["small"]:
			self.dictionary["Languages"]["Small"].append(language)

			# Add the full language
			full_language = self.languages["full"][language]

			self.dictionary["Languages"]["Full"][language] = full_language

		# Iterate through the list of small languages
		for language in self.languages["small"]:
			# Add the full translated language
			self.dictionary["Languages"]["Full translated"][language] = self.languages["full_translated"][language]

	def Define_Websites(self, dictionary):
		# Iterate through the dictionary of websites
		for title, website in self.websites["Dictionary"].items():
			# If the title of the current website is in the "Remove from websites tab" list
			if title in self.websites["Remove from websites tab"]:
				# Iterate through the titles inside the "Titles" dictionary of the website
				for language, title in website["Titles"].items():
					# Remove the website title from the list in the current language
					self.websites["List"][language].remove(title)

		# If the "Select website" state is True
		if self.states["Select website"] == True:
			# Use the "Select_Website" method to select the website
			self.Select_Website()

		# If the "Website" key is inside the parameter dictionary
		if "Website" in dictionary:
			# Create the "Websites" list using the website title as its first item
			dictionary["Websites"] = [
				dictionary["Website"]
			]

		# If the "Websites" key is inside the parameter dictionary
		if "Websites" in dictionary:
			# Iterate through the websites inside the parameter dictionary
			for website_title in dictionary["Websites"]:
				# If the current website title is inside the list of English website titles
				if website_title in self.websites["List"]["en"]:
					# Add it to the "To update" list
					self.dictionary["To update"].append(website_title)

			# Update the "Select website" state to False
			self.states["Select website"] = False

		# Iterate through the website titles inside the "To update" list
		for website_title in self.dictionary["Websites"]["To update"]:
			# Get the website dictionary
			website = self.websites["Dictionary"][website_title]

			# Add the links of the website
			website["Links"] = {}

			# Iterate through the small languages inside the "Languages" dictionary of the root dictionary
			for language in self.dictionary["Languages"]["Small"]:
				# Get the full language
				full_language = self.dictionary["Languages"]["Full"][language]

				# Define the "generate website" link template
				template = self.url["Generate"]["Templates"]["With language"]

				# Define the list of items to use to format the link template above
				items = [
					website["Titles"]["en"], # The website title in English
					full_language # The full language
				]

				# Format the link template with the list of items, making the website link in the current language
				link = template.format(*items)

				# If the website title is the same as the next year
				if website_title == str(self.current_year + 1):
					# Add the "next_year" parameter to the link
					link += "&next_year=true"

				# Add the formatted link to the "Links" dictionary
				website["Links"][language] = link

			# Add the website dictionary to the websites "Dictionary" key
			self.dictionary["Websites"]["Dictionary"][website_title] = website

		# If the number of websites is more than one
		if len(self.dictionary["Websites"]["To update"]) > 1:
			# Update the "One website" state to False
			self.states["One website"] = False

	def Select_Website(self):
		# Ask if the user wants to create a list of websites to update
		self.states["Create list of websites"] = self.Input.Yes_Or_No(self.language_texts["create_a_list_of_websites_to_update"])

		# If the user do not want to create a list of websites
		if self.states["Create list of websites"] == False:
			# Define the dictionary for the "Select" method of the "Input" module
			dictionary = {
				"options": self.websites["List"]["en"],
				"language_options": self.websites["List"][self.user_language],
				"show_text": self.language_texts["websites, title()"],
				"select_text": self.language_texts["select_a_website_to_update_its_html_contents"]
			}

			# Ask the user to select a website
			website_title = self.Input.Select(**dictionary)["option"]

			# Add the website title to the "To update" list
			self.dictionary["Websites"]["To update"].append(website_title)

		# If the user wants to create a list of websites
		if self.states["Create list of websites"] == True:
			self.Create_Websites_List()

	def Create_Websites_List(self):
		# Define the parameters dictionary to use to select the websites
		parameters = {
			"options": self.websites["List"]["en"].copy(),
			"language_options": self.websites["List"][self.user_language].copy(),
			"show_text": self.language_texts["websites, title()"],
			"select_text": self.language_texts["select_a_website_to_add_it_to_the_list"]
		}

		# Define a local dictionary to store the selected option and the "Selected" list
		dictionary = {
			"Option": "",
			"Selected": {},
			"Remove list": []
		}

		# Define the custom options for the lists of options
		dictionary, parameters = self.Define_Custom_Options(dictionary, parameters)

		# Iterate through the list of small languages
		for language in self.languages["small"]:
			# Create the empty language lists inside the "Selected" dictionary
			dictionary["Selected"][language] = []

		# While the selected option is not the "[Finish selection]" text
		while dictionary["Option"] != "Finish selection":
			# Show a five dash space separator
			print()
			print(self.separators["5"])
			print()

			# Show the "List:" text
			print(self.Language.language_texts["list, title()"] + ":")

			# If the "Selected" list in the user language is not empty
			if dictionary["Selected"][self.user_language] != []:
				# Show the website titles with a tab before them
				for title in dictionary["Selected"][self.user_language]:
					print("\t" + title)

			# If the list is empty, show the "[Empty]" text
			else:
				print("[" + self.Language.language_texts["empty, title(), feminine"] + "]")

			# Ask the user to select the website
			# Passing the dictionary of parameters to the "Select" method of the "Input" module
			selected = self.Input.Select(**parameters)

			# Update the "Option" key
			dictionary["Option"] = selected["option"]

			# If the selected option is not in the "Remove list"
			if dictionary["Option"] not in dictionary["Remove list"]:
				# Iterate through the list of small languages
				for language in self.languages["small"]:
					# Define the key to be used to get the option for the current language
					key = "option"

					if language == self.user_language:
						key = "language_option"

					# Add the selected website to the "Selected" list of the current language
					dictionary["Selected"][language].append(selected[key])

				# Remove the selected website from the lists of options
				parameters["options"].remove(selected["option"])
				parameters["language_options"].remove(selected["language_option"])

			# If the selected option is in the "Custom options" dictionary
			if dictionary["Option"] in dictionary["Custom options"]:
				# Get the custom option dictionary
				custom_option = dictionary["Custom options"][dictionary["Option"]]

				# If the "List" key is inside the custom option dictionary
				if "List" in custom_option:
					# Define the "Selected" English websites list as the list inside the custom option dictionary
					dictionary["Selected"]["en"] = custom_option["List"]

				# Define the selected option as the "Finish selection" option so the while loop ends
				dictionary["Option"] = "Finish selection"

		# Update the root "To update" list of websites with the local English "Selected" list
		self.dictionary["Websites"]["To update"] = dictionary["Selected"]["en"]

	def Define_Custom_Options(self, dictionary, parameters):
		# Define the "Custom options" dictionary
		dictionary["Custom options"] = {
			"Update all websites": {
				"List": self.websites["List"]["en"]
			},
			"Update all story websites": {
				"List": self.websites["Per type"]["Story"]["en"],
				"Item": "story"
			},
			"Update all year websites": {
				"List": self.websites["Per type"]["Year"],
				"Item": "year"
			},
			"Finish selection": {}
		}

		# Iterate through the custom options inside the dictionary
		for key, option in dictionary["Custom options"].items():
			# Iterate through the languages inside the defined list
			# (The English language and the user language)
			for language in ["en", self.user_language]:
				# Define the default parameter key for the dictionary
				parameter_key = "options"

				if language == self.user_language:
					parameter_key = "language_options"

				# Define the text key for the custom option
				text_key = key.lower().replace(" ", "_")

				# If the "story" or "year" text is inside the option
				if (
					"story" in key or
					"year" in key
				):
					# Define the text key as the template key
					text_key = "update_all_{}_websites"

				# Define the texts dictionary from where to get the option text
				texts = self.texts

				# If the text key is inside the "Texts" dictionary of the "Language" module, define it as the texts dictionary
				if text_key in self.Language.texts:
					texts = self.Language.texts

				# Get the text for the option
				text = texts[text_key][language]

				# If the "story" or "year" text is inside the option
				if (
					"story" in key or
					"year" in key
				):
					# Define the item text
					text_key = option["Item"].lower().replace(" ", "_") + ", title()"
					item_text = self.Language.texts[text_key][language].lower()

					# Format the text template with the item of the option
					text = text.format(item_text)

				# If the current language is the user language
				if language == self.user_language:
					# Add brackets around the text
					text = "[" + text + "]"

				# Add the option text to the list of options in the defined language
				parameters[parameter_key].append(text)

		# Add all of the custom options to the "Remove list"
		for key in dictionary["Custom options"]:
			dictionary["Remove list"].append(key)

		# Remove the "Finish selection" key of the "Custom options" dictionary
		dictionary["Custom options"].pop("Finish selection")

		# Return the dictionary and parameters
		return dictionary, parameters

	def Update_Websites(self):
		# If the "One website" state is False, then there is more than one website to update
		if self.states["One website"] == False:
			# Show a five dash space separator
			print()
			print(self.separators["5"])

			# Define the information text as its plural version
			text = self.language_texts["updating_these_websites"]

			# Show the information text
			print()
			print(text + ":")

			# Show the list of websites
			for website in self.dictionary["Websites"]["Dictionary"].values():
				# Get the website title
				website_title = website["Titles"][self.user_language]

				# Show it with a tab
				print("\t" + website_title)

		# Define the "w" (website) variable
		w = 1

		# Define the length of the list of websites for easier typing
		length = str(len(list(self.dictionary["Websites"]["To update"])))

		# Define the list of dictionary keys
		keys = list(self.dictionary["Websites"]["Dictionary"].keys())

		# Iterate through the website dictionaries inside the "Dictionary" key
		for key, website in self.dictionary["Websites"]["Dictionary"].items():
			# Show the website title in the user language
			website_title = website["Titles"][self.user_language]

			# Show a five dash space separator
			print()
			print(self.separators["5"])
			print()

			# If there are more websites to update
			if self.states["One website"] == False:
				# Show the "Number:" text, the number of the current website, and the total number of websites
				print(self.Language.language_texts["number, title()"] + ":")
				print("\t" + str(w) + "/" + length)
				print()

			# Show the "Updating this website:" text
			print(self.language_texts["updating_this_website"] + ":")

			# Show the website title in the user language
			print("\t" + website_title)

			# Iterate through the list of small languages inside the "Languages" dictionary
			for language in self.dictionary["Languages"]["Small"]:
				# Get the translated language in the user language
				translated_language = self.dictionary["Languages"]["Full translated"][language][self.user_language]

				# Get the link of the website in the current language
				link = website["Links"][language]

				# Open the link if the "testing" switch is False
				if self.switches["Testing"] == False:
					self.System.Open(link, verbose = False)

				# If the "verbose" switch is True
				# Or the "Verbose" key of the root dictionary is True
				if (
					self.switches["Verbose"] == True or
					self.dictionary["Verbose"] == True
				):
					# Create the link text with the current language translated into the user language
					texts = self.Language.language_texts

					text = texts["link, title()"] + " " + texts["in"] + " " + translated_language

					# Show the link of the website
					print()
					print(text + ":")
					print("\t" + link)

				# Open the link if the "testing" switch is False
				if self.switches["Testing"] == False:
					# Wait for 1 milisecond before opening the next link
					self.Date.Sleep(1)

			# If the website is not the last one
			if key != keys[-1]:
				# Ask for user input before continuing to the next website
				self.Input.Type(self.Language.language_texts["continue, title()"])

			# Add one to the "w" number
			w += 1

		# Show a five dash space separator
		print()
		print(self.separators["5"])

		# Ask for user input when the pages finish loading
		self.Input.Type(self.language_texts["press_enter_when_the_pages_finish_loading"])

	def Open_Git(self):
		# Get the list of files on the apps "Shortcuts" folder
		files = self.Folder.Contents(self.folders["Apps"]["Shortcuts"]["root"])["file"]["list"]

		# Iterate through the list of files
		for file in files:
			# If the "Git" or "GitHub" text is inside the file
			if (
				"Git" in file or
				"GitHub" in file
			):
				# If the "bat" or "exe" extension is in the file
				if (
					".bat" in file or
					".exe" in file
				):
					# Define the Git file as the current file
					git_file = file

		# If the "Testing" switch is False, open the Git file
		if self.switches["Testing"] == False:
			self.System.Open_Link(git_file, verbose = False)
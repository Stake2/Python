# Open_Friend_File.py

from Friends.Friends import Friends as Friends

import re

class Open_Friend_File(Friends):
	def __init__(self):
		super().__init__()

		# Select a file name to open
		self.Select_File_Name()

		# Define the root dictionary, with the "Search" and "States" dictionaries
		self.dictionary = {
			"States": {
				"Selected a Friend": False,
				"Found file": False,
				"Found multiple files": False,
				"Search": False
			}
		}

		# Ask the user if they want to search for the friend file
		self.dictionary["States"]["Search"] = self.Input.Yes_Or_No(self.language_texts["search_for_friend_{}_file"].format(self.file_name[self.user_language]))

		# Search for a friend if the search is activated
		if self.dictionary["States"]["Search"] == True:
			self.Search_Friend_File()

		# If the search is activated
		if self.dictionary["States"]["Search"] == True:
			# If a friend file was found
			if self.dictionary["States"]["Found file"] == True:
				# Define the friend file
				self.Define_Friend_File()

			# Show information about the state of the searching and opening
			self.Show_Information()

			# Open the Friend file
			if self.dictionary["States"]["Found file"] == True:
				# Open the file
				self.Open_Friend_File()

		# If the search is deactivated
		# Or a friend file was not found
		if (
			self.dictionary["States"]["Search"] == False or
			self.dictionary["States"]["Found file"] == False
		):
			# If the search is deactivated
			if self.dictionary["States"]["Search"] == False:
				# Show a separator
				print()
				print(self.separators["5"])

			# Select a friend
			# And also update the "Selected a Friend" state in the "States" dictionary
			self.dictionary["States"] = self.Select_Friend(states = self.dictionary["States"])["States"]

			# If the file name is "Social Network"
			if self.file_name["en"] == "Social Network":
				# List the Friend Social Networks list
				social_networks = self.friend["Social Networks"]

				# Define the select text
				select_text = self.language_texts["select_one_social_network_to_open_its_profile_file"]

				# Select a Friend Social Network
				self.social_network = self.Select_Social_Network(social_networks = social_networks, select_text = select_text)

			# Define the friend file
			self.Define_Friend_File()

			# Show information about the state of the searching and opening
			self.Show_Information()

			# Open the file
			self.Open_Friend_File()

	def Search_Friend_File(self):
		# Define the "Search" dictionary
		self.dictionary["Search"] = {
			"Information item": {},
			"Information items": self.information_items,
			"Found": {},
			"First space": False
		}

		# If the file name in English is "Social Network"
		if self.file_name["en"] == "Social Network":
			# Define the Social Network Information items to be selected
			self.dictionary["Search"]["Information items"] = self.Social_Networks.information_items

			self.dictionary["Search"]["First space"] = True

		# Add the "Accept enter" key to the Information items dictionary
		self.dictionary["Search"]["Information items"]["Accept enter"] = False

		# Select the information item and get its dictionary
		dictionary = self.Select_Information_Item(self.dictionary["Search"]["Information items"])

		# Define the information item dictionary
		self.information_item = dictionary["Item"]

		# Define the search query
		self.dictionary["Search"]["Query"] = dictionary["Information"]

		# Update the "Exact match" key of the States dictionary
		self.dictionary["States"]["Exact match"] = self.information_item["States"]["Exact match"]

		# Update the "Information item" inside the "Search" dictionary
		self.dictionary["Search"]["Information item"] = self.information_item

		# Define a basic Social Networks list
		social_networks_list = [
			"One"
		]

		# Iterate through the Friends dictionaries
		for friend in self.friends["Dictionary"].values():
			# Define the friend file for the "Information" file name
			friend["File"] = friend["Files"][self.file_name["Plural"]["en"]]

			# If the file name is "Social Network"
			if self.file_name["en"] == "Social Network":
				social_networks_list = friend["Social Networks"]["List"]

			# Iterate through the local list of Social Networks
			for social_network in social_networks_list:
				# Update the "self.social_network" variable
				social_network = self.Select_Social_Network(social_network)

				# If the file name is "Social Network"
				# And the social network is inside the list of social networks of the friend
				if (
					self.file_name["en"] == "Social Network" and
					social_network["Name"] in friend["Social Networks"]["Dictionary"]
				):
					# Define the friend file for the "Social Network" file name
					friend["File"] = friend["Files"][self.file_name["Plural"]["en"]][social_network["Name"]]["Profile"]

					# Change the Information dictionary to the Social Network Information dictionary
					friend["Information"] = friend["Social Networks"]["Dictionary"][social_network["Name"]]

				# Create the search "Results" list
				self.dictionary["Search"]["Results"] = []

				# If the information item is inside the Friend/Social Network Information dictionary
				if self.information_item["Name"] in friend["Information"]:
					# If the search needs an exact match
					if self.dictionary["States"]["Exact match"] == True:
						# Search using Regex
						self.dictionary["Search"]["Results"] = re.findall(r"\b" + self.dictionary["Search"]["Query"] + r"\b", friend["Information"][self.information_item["Name"]], re.IGNORECASE)

					# If the search does not need an exact match
					if self.dictionary["States"]["Exact match"] == False:
						# If the selected information item is inside the Information dictionary
						# And the search query is inside the selected information
						if (
							self.information_item["Name"] in friend["Information"] and
							self.dictionary["Search"]["Query"] in friend["Information"][self.information_item["Name"]]
						):
							# Append the search query to the results list
							self.dictionary["Search"]["Results"].append(self.dictionary["Search"]["Query"])

					# If the search results are not empty
					if self.dictionary["Search"]["Results"] != []:
						# Add the friend name to the found friends
						# With the friend file as the value
						dictionary = {
							"Name": friend["Name"],
							"File": friend["File"],
							"Social Network": social_network
						}

						# If the information item is "Origin Social Network"
						if self.information_item["Name"] == "Origin Social Network":
							# Define the "Social Network" key inside the local Friend dictionary as the search query
							dictionary["Social Network"] = self.dictionary["Search"]["Query"]

						# Define the root Friend dictionary as the local Friend dictionary
						self.dictionary["Search"]["Found"][friend["Name"]] = dictionary

						# Define the Friend dictionary as the local Friend dictionary
						self.friend = friend

						self.dictionary["States"]["Found file"] = True

		# If the friend file was found
		if self.dictionary["States"]["Found file"] == True:
			# Define the "self" Social Network as the Social Network inside the Friend Found dictionary
			self.social_network = list(self.dictionary["Search"]["Found"].values())[0]["Social Network"]

			# If the found friends are more than one
			if len(self.dictionary["Search"]["Found"]) >= 2:
				# Select a friend from the found friends list
				select_text = self.language_texts["select_a_friend_from_the_list_of_found_friends"]

				friends = list(self.dictionary["Search"]["Found"].keys())

				print()
				print(self.separators["5"])

				self.Select_Friend(friends_list = friends, select_text = select_text)

				# Define the "self" Social Network as the Social Network inside the Friend Found dictionary
				self.social_network = self.dictionary["Search"]["Found"][self.friend["Name"]]["Social Network"]

				# Define the "Found multiple files" state as True
				self.dictionary["States"]["Found multiple files"] = True

	def Define_Friend_File(self):
		# If the file name is "Information"
		if self.file_name["en"] == "Information":
			# Get the Friend information file
			self.friend["File"] = self.friend["Files"]["Information"]

			self.dictionary["States"]["Found file"] = True

		# If the file name is "Social Network"
		# And the user selected a friend
		if (
			self.file_name["en"] == "Social Network" and
			self.dictionary["States"]["Selected a Friend"] == True
		):
			# Get the Social Network profile file
			self.friend["File"] = self.friend["Files"]["Social Networks"][self.social_network["Name"]]["Profile"]

			self.dictionary["States"]["Found file"] = True

	def Show_Information(self):
		# If the file name is "Social Network"
		# And the user searched for a friend
		if (
			self.file_name["en"] == "Social Network" and
			self.dictionary["States"]["Search"] == True
		):
			# Update the language information item to add the Social Network name
			self.information_item[self.user_language] = self.information_item[self.user_language].lower() + " " + self.language_texts["of_the_social_network"] + ' "' + self.social_network["Name"] + '"'

		# Define the local file name
		file_name = self.file_name

		if self.file_name["en"] == "Information":
			file_name = file_name["Plural"]

		file_name = file_name[self.user_language].lower()

		# Show a separator
		separator = self.separators["5"]

		# If a friend file was not found
		if self.dictionary["States"]["Found file"] == False:
			separator = "---"

		print()
		print(separator)
		print()

		# Define the show text of opening the [file name] friend file
		show_text = self.language_texts["opening_this_{}_friend_file"].format(file_name) + ":\n"

		# If the friend file was found and the user selected a friend
		if (
			self.dictionary["States"]["Found file"] == True and
			self.dictionary["States"]["Selected a Friend"] == True
		):
			# Add the friend file to the show text
			show_text += "\t" + self.friend["File"]

		if self.dictionary["States"]["Found file"] == True:
			# Define the Friend text
			friend_text = self.language_texts["friend, title()"] + ":" + "\n" + \
			"\t" + self.friend["Name"]

			# Show the "Friend" text and name
			print(friend_text)

			# If the file name is "Social Network"
			if self.file_name["en"] == "Social Network":
				# If the "Search" key is not present in the root dictionary
				# Or it is present
				# And the information item is not "Origin Social Network"
				if (
					"Search" not in self.dictionary or
					"Search" in self.dictionary and
					self.dictionary["Search"]["Information item"]["Name"] != "Origin Social Network"
				):
					# Define the Social Network text
					social_network_text = self.Language.language_texts["social_network"] + ":" + "\n" + \
					"\t" + self.social_network["Name"]

					# Show the "Social Network" text and name
					print()
					print(social_network_text)

		# Show the search query if the user searched for a Friend file
		if self.dictionary["States"]["Search"] == True:
			# If the Friend file was found, show a space
			if self.dictionary["States"]["Found file"] == True:
				print()

			print(self.Language.language_texts["search, title()"] + ":")
			print("\t" + self.dictionary["Search"]["Query"])

		# If the user searched for a friend
		# And did not selected a friend
		# Or the user searched for a friend
		# And multiple friend files were found
		if (
			self.dictionary["States"]["Search"] == True and
			self.dictionary["States"]["Selected a Friend"] == False or
			self.dictionary["States"]["Search"] == True and
			self.dictionary["States"]["Found multiple files"] == True
		):
			# Define the basic text template
			template = "[Found or not]" + ":\n" + \
			"\t" + "{}" + "\n\n" + \
			"[Additional information]"

			# Define the local information item
			information_item = self.information_item[self.user_language]

			if self.file_name["en"] != "Social Network":
				# Transform the information item into lowercase
				information_item = information_item.lower()

			# If the friend file was found
			if self.dictionary["States"]["Found file"] == True:
				# Update the template
				template = template.replace("[Found or not]", self.language_texts["found_{}"] + " {}")

				template = template.replace("[Additional information]", self.language_texts["on_the_friend_{}_file_below"])

				# Add a format slot for the friend file
				template += ":\n" + \
				"\t" + "{}"

				# Define the list of items to be used to format the text template
				items = []

				# Define the exact match item
				item = self.information_item["Gender"]["Words"]["Part of"]

				if self.dictionary["States"]["Exact match"] == True:
					item = self.information_item["Gender"]["Words"]["This"]

				# Add it
				items.append(item)

				# Add the rest of the items
				rest = [
					information_item,
					self.dictionary["Search"]["Query"],
					file_name,
					self.friend["File"]
				]

				items.extend(rest)

			# If the friend file was not found
			if self.dictionary["States"]["Found file"] == False:
				# Update the template
				template = template.replace("[Found or not]", self.language_texts["could_not_find_{}_in_friend_{}_files"])

				template = template.replace("[Additional information]", self.language_texts["executing_the_method_to_select_a_friend_{}_file"] + "...")

				# Define the list of items to be used to format the text template
				items = [
					self.information_item["Gender"]["Words"]["This"] + " " + information_item,
					file_name,
					self.dictionary["Search"]["Query"],
					file_name
				]

			# Format the template with the items list
			show_text = template.format(*items)

		# Show the information text
		print()
		print(show_text)

		# Show the verbose text if the file was found
		if self.dictionary["States"]["Found file"] == True:
			verbose_text = self.System.Open(self.friend["File"], open = False, verbose = False)

			print(verbose_text)

		# Show a separator
		print()
		print(self.separators["5"])

	def Open_Friend_File(self):
		self.System.Open(self.friend["File"], verbose = False)
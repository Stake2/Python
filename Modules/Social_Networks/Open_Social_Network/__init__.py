# Open_Social_Network.py

# Import the root class
from Social_Networks.Social_Networks import Social_Networks as Social_Networks

class Open_Social_Network(Social_Networks):
	def __init__(self, social_networks = None):
		# Run the root class to import its methods and variables
		super().__init__()

		# Define the root "open social network" dictionary
		self.open_social_network = {
			"Social networks": {
				"Numbers": {
					"Total": 0,
					"Iteration": 1
				},
				"List": [],
				"Dictionary": {}
			},
			"Link type": self.social_networks["Link types"]["Dictionary"]["Profile"],
			"Input text": self.language_texts["press_enter_to_open_the_next_social_network"]
		}

		# Define the root spaces dictionary
		self.spaces = {
			"First": True,
			"Second": False
		}

		# Define the root states dictionary
		self.states = {
			"First separator": True,
			"One social network": False,
			"Imported numbers": False,
			"Imported input text": False
		}

		# Define the "Social networks" dictionary
		self.Define_Social_Networks(social_networks)

	def Define_Social_Networks(self, social_networks):
		# If the "social networks" parameter is "None"
		if social_networks == None:
			# Define the select text as the "Select one social network to open" text in the user language
			select_text = self.language_texts["select_one_social_network_to_open"]

			# Ask the user to select the social network to be opened
			self.Select_Social_Network(select_text = select_text)

			# Add the selected social network to the list of social networks
			self.open_social_network["Social networks"]["List"] = [
				self.social_network["Name"]
			]

		# If the "social networks" parameter is not "None"
		if social_networks != None:
			# If the type of the social networks parameter is a list
			if type(social_networks) == list:
				# Define the local list of social networks as the "social networks" parameter
				self.open_social_network["Social networks"]["List"] = social_networks

			# If the type of the social networks parameter is a dictionary
			if type(social_networks) == dict:
				# Define a list of keys to import
				to_import = [
					"Numbers",
					"Custom links",
					"Do not open",
					"Input texts",
					"Input text"
				]

				# Define a list of keys to import to the root "Social networks" dictionary
				social_network_keys = [
					"Numbers",
					"Custom links",
					"Do not open",
					"Input texts"
				]

				# Iterate through the list
				for key in to_import:
					# If the key is inside the parameter dictionary
					if key in social_networks:
						# If the key inside the list of keys to import to the root "Social networks" dictionary
						if key in social_network_keys:
							# Add it to the "Social networks" dictionary
							self.open_social_network["Social networks"][key] = social_networks[key]

						# If not
						else:
							# Add it to the root "Open social network" dictionary
							self.open_social_network[key] = social_networks[key]

						# If the key is "Numbers"
						if key == "Numbers":
							# Change the "Imported numbers" state to True
							self.states["Imported numbers"] = True

						# If the key is "Input text"
						if key == "Input text":
							# Change the "Imported input text" state to True
							self.states["Imported input text"] = True

				# If the "List" of social networks inside the parameter dictionary is not empty
				if social_networks["List"] != []:
					# Define the list of social networks of the "Open social networks" dictionary as the one inside the parameter dictionary
					self.open_social_network["Social networks"]["List"] = social_networks["List"]

				# If the "Link type" key is inside the parameter dictionary
				if "Link type" in social_networks:
					# Update the "Link type" of the root dictionary with the one inside the parameter dictionary
					self.open_social_network["Link type"] = self.social_networks["Link types"][social_networks["Link type"]]

				# If the "States" key is inside the parameter dictionary
				if "States" in social_networks:
					# Change the value of the "First separator" state with the one inside the parameter dictionary
					self.states["First separator"] = social_networks["States"]["First separator"]

				# If the "Spaces" key is present inside the parameter dictionary
				if "Spaces" in social_networks:
					# Iterate through the list of spaces inside the parameter dictionary
					for space in social_networks["Spaces"]:
						# Update the root space with the space inside the parameter dictionary
						self.spaces[space] = social_networks["Spaces"][space]

		# If the total number of social networks is zero
		if self.open_social_network["Social networks"]["Numbers"]["Total"] == 0:
			# Get the total number of social networks
			self.open_social_network["Social networks"]["Numbers"]["Total"] = len(self.open_social_network["Social networks"]["List"])

		# If the total number of social networks is one
		if self.open_social_network["Social networks"]["Numbers"]["Total"] == 1:
			# Change the "One social network" state to True
			self.states["One social network"] = True

		# Iterate through the list of social networks
		for social_network_name in self.open_social_network["Social networks"]["List"]:
			# If the current social network is inside the root "Social networks" dictionary
			if social_network_name in self.social_networks["Dictionary"]:
				# Get the social network dictionary
				social_network = self.social_networks["Dictionary"][social_network_name]

				# Add it to the local social networks "Dictionary"
				self.open_social_network["Social networks"]["Dictionary"][social_network_name] = social_network

		# Open the social networks
		self.Open_Social_Networks()

	def Open_Social_Networks(self):
		# Create a shortcut to the root "Social networks" dictionary
		social_networks_dicitonary = self.open_social_network["Social networks"]

		# Iterate through the social network names and dictionaries inside the root "Social networks" dictionary
		for social_network_name, social_network in social_networks_dicitonary["Dictionary"].items():
			# Update the root "social_network" variable with the dictionary of the current social network
			self.Select_Social_Network(social_network)

			# Define the default link to open as the root social network link
			link_to_open = self.social_network["Information"]["Link"]

			# If the social network contains an "Opening link"
			if "Opening link" in self.social_network["Information"]:
				# Define the local opening link
				opening_link = self.social_network["Information"]["Opening link"]

				# Use it as the link to open
				link_to_open = opening_link

			# If the link type is "Profile"
			# And the social network profile contains a "Profile link", use it as the link to open
			if (
				self.open_social_network["Link type"]["en"] == "Profile" and
				"Profile link" in self.social_network["Profile"]
			):
				link_to_open = self.social_network["Profile"]["Profile link"]

			# If there is a "Custom links" dictionary inside the "Social networks" dictionary of the "Open social networks" dictionary
			# And the current social network contains a custom link inside "Custom links", use that link as the link to open
			if (
				"Custom links" in self.open_social_network["Social networks"] and
				social_network_name in self.open_social_network["Social networks"]["Custom links"]
			):
				link_to_open = self.open_social_network["Social networks"]["Custom links"][social_network_name]

			# If the social network contains an "Opening link"
			# And the opening link is "Use executable"
			if (
				"Opening link" in self.social_network["Information"] and
				opening_link == self.Language.language_texts["use_executable"]
			):
				# Define the link to open as the shortcut of the social network
				link_to_open = self.social_network["Shortcut"]

			# Define the root link to open as the local one
			self.social_network["Link to open"] = link_to_open

			# Define the root "Open" switch as True
			social_network["Open"] = True

			# If the "Do not open" key is present inside the root "Social networks" dictionary
			# And the current social network is inside of that list
			if (
				"Do not open" in social_networks_dicitonary and
				social_network_name in social_networks_dicitonary["Do not open"]
			):
				# Change the root "Open" switch to False
				social_network["Open"] = False

			# If the the root "Open" switch is True
			if social_network["Open"] == True:
				# Open the social network link
				self.System.Open(link_to_open, verbose = False)

			# Show information about the opening of the social network link
			self.Show_Information(social_network_name, social_network)

			# If there are more than one social network to open
			# And the current social network is not the last one
			# Or the "Numbers" dictionary was imported from the "social networks" parameter dictionary
			# Or the "Input text" key was imported from the "social networks" parameter dictionary
			if (
				self.states["One social network"] == False and
				social_network_name != self.open_social_network["Social networks"]["List"][-1] or
				self.states["Imported numbers"] == True or
				self.states["Imported input text"] == True
			):
				# Create a shortcut to the input text
				input_text = self.open_social_network["Input text"]

				# If the "Input texts" key is inside the root "Social networks" dictionary
				# And the social network name is inside that dictionary
				if (
					"Input texts" in social_networks_dicitonary and
					social_network_name in social_networks_dicitonary["Input texts"]
				):
					# Get the input text related to the current social network
					input_text = social_networks_dicitonary["Input texts"][social_network_name]

				# If the user language is inside the input text
				if self.language["Small"] in input_text:
					# Get the input text in the user language
					input_text = input_text[self.language["Small"]]

				# If the "{social_network}" format string is inside the input text
				if "{social_network}" in input_text:
					# Format it with the name of the social network
					input_text = input_text.replace("{social_network}", social_network_name)

				# Ask for the user input using the defined input text
				self.Input.Type(input_text)

			# If the "Numbers" dictionary were not imported from the "social networks" parameter dictionary
			if self.states["Imported numbers"] == False:
				# Add one to the "Iteration" number
				self.open_social_network["Social networks"]["Numbers"]["Iteration"] += 1

	def Show_Information(self, social_network_name, social_network):
		# If there are multiple social networks to open
		# And the current social network is not the first one
		# Or the "Numbers" dictionary were imported from the "social networks" parameter dictionary
		# And the "Iteration" number is not one (the first number)
		if (
			self.states["One social network"] == False and
			social_network_name != self.open_social_network["Social networks"]["List"][0] or
			self.states["Imported numbers"] == True and
			self.open_social_network["Social networks"]["Numbers"]["Iteration"] != 1
		):
			# If the first space is on
			if self.spaces["First"] == True:
				# Show a space separator
				print()

		# If there is only one social network to open
		# If there are multiple
		# And the current social network is the first one
		# Or the "Numbers" dictionary were imported from the "social networks" parameter dictionary
		if (
			self.states["One social network"] == True or
			self.states["One social network"] == False and
			social_network_name == self.open_social_network["Social networks"]["List"][0] or
			self.states["Imported numbers"] == True
		):
			# If the "First separator" state is True
			if self.states["First separator"] == True:
				# Show a five dash space separator
				print(self.separators["5"])
				print()

		# If there are multiple social networks to open
		if self.states["One social network"] == False:
			# Create a shortcut to the number of the current social network
			current_number = self.open_social_network["Social networks"]["Numbers"]["Iteration"]

			# Create a shortcut to the total number of social networks
			total_number = self.open_social_network["Social networks"]["Numbers"]["Total"]

			# Combine the current and total numbers with a slash in between
			number_text = "[" + str(current_number) + "/" + str(total_number) + "]"

			# If the current social network is not the first one
			if social_network_name != self.open_social_network["Social networks"]["List"][0]:
				# Show a one dash space separator
				print(self.separators["1"])
				print()

			# Show the "Social network number" text and the "[current number]/[total number]" numbers
			print(self.Language.language_texts["social_network_number"] + ":")
			print("\t" + number_text)
			print()

			# Show the "Social network" text and the social network name
			print(self.Language.language_texts["social_network"] + ":")
			print("\t" + social_network_name)

		# Define the text template as the default one
		text_template = self.language_texts["opening_the_social_network_{}_on_its_{}_page_with_this_link"]

		# If there are custom links in the dictionary
		if "Custom links" in self.open_social_network["Social networks"]:
			# Change the template text to reflect that
			text_template = self.language_texts["opening_the_social_network_{}_with_this_link"]

		# If the social network has a shortcut
		if "Shortcut" in self.social_network:
			# Change the template text to reflect that
			text_template = self.language_texts["opening_the_executable_of_the_social_network_{}"]

		# Define the text template items
		items = [
			self.social_network["Name"],
			self.open_social_network["Link type"][self.language["Small"]].lower()
		]

		# If there is only one "{}" format string in the text template
		if text_template.count("{}") == 1:
			# Remove the last items
			items.pop(-1)

		# Format the text template with the list of items to create the text
		text = text_template.format(*items)

		# If the social network "Open" switch is True
		if social_network["Open"] == True:
			# Show the text and the link to open
			print()
			print(text + ":")
			print("\t" + self.social_network["Link to open"])

			# If the link type is "Profile"
			if self.open_social_network["Link type"]["en"] == "Profile":
				# To-Do: Show information about the link, splitting the template link
				variable = True
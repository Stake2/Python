# Open_Social_Network.py

from Social_Networks.Social_Networks import Social_Networks as Social_Networks

class Open_Social_Network(Social_Networks):
	def __init__(self, social_networks = None):
		super().__init__()

		# Define the root dictionary
		self.dictionary = {
			"Social Networks": {
				"Numbers": {
					"Total": 0,
					"Iteration": 1
				},
				"List": [],
				"Dictionary": {}
			},
			"Link type": self.social_networks["Link types"]["Dictionary"]["Profile"],
			"States": {
				"Select Social Network": True,
				"Type": "Profile",
				"First separator": True
			},
			"Spaces": {
				"First": True,
				"Second": False
			}
		}

		# If the "Social Networks" parameter is "None"
		if social_networks == None:
			# Select the Social Network
			self.Select_Social_Network()

			# Add the selected Social Network to the Social Networks list
			self.dictionary["Social Networks"]["List"] = [
				self.social_network["Name"]
			]

		# If the "Social Networks" parameter is not "None"
		if social_networks != None:
			# If the type of the Social Networks parameter is a list
			if type(social_networks) == list:
				# Define the local list of Social Networks as the "Social Networks" parameter dictionary
				self.dictionary["Social Networks"]["List"] = social_networks

			# If the type of the Social Networks parameter is a dictionary
			if type(social_networks) == dict:
				# If the parameter list of Social Networks is not empty
				if social_networks["List"] != []:
					# Define the local list of Social Networks as the "List" dictionary inside the "Social Networks" parameter dictionary
					self.dictionary["Social Networks"]["List"] = social_networks["List"]

				# If the "Custom links" key is present inside the "Social Networks" parameter dictionary
				if "Custom links" in social_networks:
					# Define the "Custom links" key as the "Custom links" dictionary inside the "Social Networks" parameter dictionary
					self.dictionary["Social Networks"]["Custom links"] = social_networks["Custom links"]

				# If the "Type" key is inside the "Social Networks" parameter dictionary
				if "Type" in social_networks:
					# Update the "Link type" key of the root dictionary
					# With the "Link type" dictionary of the same name
					self.dictionary["Link type"] = self.social_networks["Link types"][social_networks["Type"]]

				# If the "States" key is inside the "Social Networks" parameter dictionary
				if "States" in social_networks:
					# Update the "First separator" key of the "States" dictionary inside the root dictionary
					# With the "First separator" key of the dictionary of the same name
					self.dictionary["States"]["First separator"] = social_networks["States"]["First separator"]

				# If the "Spaces" key is present inside the "Social Networks" parameter dictionary
				if "Spaces" in social_networks:
					# Iterate through the list of spaces
					for space in ["First", "Second"]:
						# If the space key is present inside the "Social Networks" parameter dictionary
						if space in social_networks["Spaces"]:
							# Update the space key of the "Spaces" dictionary inside the root dictionary
							# With the new value as the space key inside the "Social Networks" parameter dictionary
							self.dictionary["Spaces"][space] = social_networks["Spaces"][space]

		# Get the number of social networks
		self.dictionary["Social Networks"]["Numbers"]["Total"] = len(self.dictionary["Social Networks"]["List"])

		# Iterate through the "Social Networks" list
		for social_network in self.dictionary["Social Networks"]["List"]:
			# Get the "Social Network" dictionary
			social_network = self.social_networks["Dictionary"][social_network]

			# If the current Social Network is inside the root "Social Networks" dictionary
			if social_network["Name"] in self.social_networks["Dictionary"]:
				# Add it to the local "Social Networks" dictionary
				self.dictionary["Social Networks"]["Dictionary"][social_network["Name"]] = social_network

		# Open the Social Networks
		self.Open_Social_Networks()

	def Open_Social_Networks(self):
		# Iterate through the list of Social Networks to open
		for key, social_network in self.dictionary["Social Networks"]["Dictionary"].items():
			# Update the "self.social_network" variable
			self.Select_Social_Network(social_network)

			# Define the default link to open as the Social Network link
			self.social_network["Link to open"] = self.social_network["Information"]["Link"]

			# If the Social Network contains an "Opening link", use it
			if "Opening link" in self.social_network["Information"]:
				self.social_network["Link to open"] = self.social_network["Information"]["Opening link"]

			# If the link type is "Profile"
			# And the Social Network profiile contains a "Profile link", use it
			if (
				self.dictionary["Link type"]["en"] == "Profile" and
				"Profile link" in self.social_network["Profile"]
			):
				self.social_network["Link to open"] = self.social_network["Profile"]["Profile link"]

			# If there is a "Custom links" dictionary inside the "Social Networks" dictionary of the root dictionary
			# And the current Social Network of the loop contains a custom link
			if (
				"Custom links" in self.dictionary["Social Networks"] and
				self.social_network["Name"] in self.dictionary["Social Networks"]["Custom links"]
			):
				# Use it
				self.social_network["Link to open"] = self.dictionary["Social Networks"]["Custom links"][social_network["Name"]]

			# Show information about the opening of the Social Network link
			self.Show_Information()

			# Open the Social Network link
			self.Open_Social_Network()

			# Add to the "Iteration" number
			self.dictionary["Social Networks"]["Numbers"]["Iteration"] += 1

	def Show_Information(self):
		if self.dictionary["Spaces"]["First"] == True:
			print()

		# If there is only one Social Network to open
		# Or there are more than one Social Network to open
		# And the current Social Network is the first one
		if (
			self.dictionary["Social Networks"]["Numbers"]["Total"] == 1 or
			self.dictionary["Social Networks"]["Numbers"]["Total"] >= 2 and
			self.social_network["Name"] == self.dictionary["Social Networks"]["List"][0]
		):
			# If the "First separator" state is True
			if self.dictionary["States"]["First separator"] == True:
				# Show a separator
				print(self.separators["5"])
				print()

		# If there are more than one Social Network to open
		if self.dictionary["Social Networks"]["Numbers"]["Total"] >= 2:
			# Get the current and total numbers
			# And store them in short variables for easier typing
			current_number = self.dictionary["Social Networks"]["Numbers"]["Iteration"]
			total_number = self.dictionary["Social Networks"]["Numbers"]["Total"]

			# Make the number text
			number_text = str(current_number) + "/" + str(total_number)

			if self.social_network["Name"] != self.dictionary["Social Networks"]["List"][0]:
				print("-")
				print()

			# Show the "Social Networks" and the "[Current number]/[Total number]" texts
			print(self.Language.language_texts["number, title()"] + ":")
			print("\t" + number_text)
			print()

			# Show the "Social Network" text and the Social Network name
			print(self.Language.language_texts["social_network"] + ":")
			print("\t" + self.social_network["Name"])
			print()

		# Define the text template
		template = self.language_texts["opening_the_social_network_{}_on_its_{}_page_with_this_link"]

		# If there are custom links in the dictionary
		if "Custom links" in self.dictionary["Social Networks"]:
			# Change the template text
			template = self.language_texts["opening_the_social_network_{}_with_this_link"]

		# Define the text template items
		items = [
			self.social_network["Name"],
			self.dictionary["Link type"][self.user_language].lower()
		]

		# Format the text template with the items
		text = template.format(*items)

		print(text + ":")
		print("\t" + self.social_network["Link to open"])

		# If the link type is "Profile"
		if self.dictionary["Link type"]["en"] == "Profile":
			# To-Do: Show information about the link, splitting the template link
			variable = True

		# If there are more than one Social Network to open
		# And the current Social Network is the last one
		if (
			self.dictionary["Social Networks"]["Numbers"]["Total"] >= 2 and
			self.social_network["Name"] == self.dictionary["Social Networks"]["List"][-1]
		):
			# Show a separator
			print()
			print(self.separators["5"])

	def Open_Social_Network(self):
		# Open the Social Network link
		self.System.Open(self.social_network["Link to open"], verbose = False)
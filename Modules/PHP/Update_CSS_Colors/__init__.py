# Update_CSS_Colors.py

from PHP.PHP import PHP as PHP

class Update_CSS_Colors(PHP):
	def __init__(self):
		super().__init__()

		# Define the root dictionary
		self.Define_Root_Dictionary()

		# Create the color selectors
		self.Create_Color_Selectors()

		# Update the "Colors.css" file
		self.Update_Color_Files()

		# Show the information about the execution of the methods
		self.Show_Information()

	def Define_Root_Dictionary(self):
		# Create the root dictionary
		# With the selectors dictionary
		self.dictionary = {
			"Files": {
				"Colors JSON": self.folders["Mega"]["PHP"]["JSON"]["Colors"],
				"Colors CSS": self.folders["Mega"]["Websites"]["CSS"]["Colors"]
			},
			"Texts": {},
			"States": {
				"File was updated": False
			},
			"Selectors": {
				"Border": {
					"Formats": {
						"Selector": "border_{number}px_solid_{color_class}",
						"Content": "border: {number}px solid var(--{color}-color);"
					}
				},
				"Border color": {
					"Formats": {
						"Selector": "border_color_{color_class}",
						"Content": "border-color: var(--{color}-color);"
					}
				},
				"Background color": {
					"Formats": {
						"Selector": "background_{color_class}",
						"Content": "background-color: var(--{color}-color);"
					}
				},
				"Background hover color": {
					"Formats": {
						"Selector": "background_hover_{color_class}:hover",
						"Content": "background-color: var(--{color}-color);"
					}
				},
				"Text color": {
					"Formats": {
						"Selector": "text_{color_class}",
						"Content": "color: var(--{color}-color);"
					}
				},
				"Text hover color": {
					"Formats": {
						"Selector": "text_hover_{color_class}:hover",
						"Content": "color: var(--{color}-color);"
					}
				},
				"Box shadow": {
					"Formats": {
						"Selector": "box_shadow_{color_class}",
						"Content": "box-shadow: var(--box-shadow-{color}) !important;"
					}
				}
			}
		}

		# Read the "Colors.json" file
		self.colors = self.JSON.To_Python(self.dictionary["Files"]["Colors JSON"])

	def Create_Color_Selectors(self):
		# Iterate through the colors list
		for color_name in self.colors["List"]:
			# Get the Color dictionary
			color = {
				"Key": color_name.lower().replace(" ", "-"),
				**self.colors["Dictionary"][color_name]
			}

			# Update the Color dctionary inside the root Colors dictionary with the local Color dictionary
			self.colors["Dictionary"][color_name] = color

		# Update the "Colors JSON" text inside the "Texts" dictionary of the root dictionary
		self.dictionary["Texts"]["Colors JSON"] = self.colors

		# ---------- #

		# Create the text to be written inside the "Colors.css" file

		# Create the templates dictionary
		templates = {
			"Color": "--{}-color: {};",

			"Box shadow": "\t" + "--box-shadow-[Color key]: 0 -8px 20px var(--spread-btn) [Color code]60," + "\n" + \
			"\t" + "0 8px 20px var(--spread-btn) [Color code]60," + "\n" + \
			"\t" + "0 6px 20px var(--spread-btn) [Color code]60," + "\n" + \
			"\t" + "0 -6px 20px var(--spread-btn) [Color code]60!important;",

			"Heading": "/*" + "\n" + \
			"\n" + \
			"----------" + "\n" + \
			"\n" + \
			"{}" + "\n" + \
			"\n" + \
			"----------" + "\n" + \
			"\n" + \
			"*/" + "\n\n"
		}

		# Create the root text

		# Add the heading text
		text = templates["Heading"].format("Color variables")

		# Add the "Body" tag
		text += "body {" + "\n"

		# Iterate through the colors list
		for color_name in self.colors["List"]:
			# Get the Color dictionary
			color = self.colors["Dictionary"][color_name]

			# Format the color template
			color = templates["Color"].format(color["Key"], color["Code"])

			# Add the color to the root text
			text += "\t" + color

			# Add a line break to the root text
			text += "\n"

		# Close the "Body" tag and add two line breaks
		text += "}" + "\n\n"

		# ----- #

		# Create the box shadows

		# Add the heading text
		text += templates["Heading"].format("Box shadows")

		# Add the "Body" tag
		text += "body {" + "\n"

		# Iterate through the colors list
		for color_name in self.colors["List"]:
			# Get the Color dictionary
			color = self.colors["Dictionary"][color_name]

			# Create the box shadow
			box_shadow = templates["Box shadow"].replace("[Color key]", color["Key"])
			box_shadow = box_shadow.replace("[Color code]", color["Code"])

			# Add the box shadow to the root text
			text += box_shadow

			# Add a line break to the root text
			text += "\n"

			# If the color name is not the last one, add a line break to the root text
			if color_name != self.colors["List"][-1]:
				text += "\n"

		# Close the "Body" tag and add two line breaks
		text += "}" + "\n\n"

		# ----- #

		# Create CSS classes of the colors

		# Iterate through the selectors list
		keys = list(self.dictionary["Selectors"].keys())

		for key in keys:
			# Get the selector Formats dictionary
			selector = self.dictionary["Selectors"][key]["Formats"]

			# Define the list of numbers to use to format
			numbers = [1]

			# Define the list of numbers of the "Border" selector
			if key == "Border":
				numbers = [1, 3, 4]

			# Add the heading text
			text += templates["Heading"].format(key + "s")

			# Iterate through the numbers list
			for number in numbers:
				# Iterate through the colors list
				for color_name in self.colors["List"]:
					# Get the Color dictionary
					color = self.colors["Dictionary"][color_name]

					# Define the "to replace" dictionary
					to_replace = {
						"{color}": color["Key"],
						"{color_class}": color["Key"].replace("-", "_"),
						"{number}": str(number)
					}

					# Create the selector text
					selector_text = selector["Selector"]

					# Create the content of the CSS class
					content = selector["Content"]

					# Replace the texts to replace inside the "to replace" dictionary
					for text_to_replace, replace_with in to_replace.items():
						if text_to_replace in selector_text:
							selector_text = selector_text.replace(text_to_replace, replace_with)

						if text_to_replace in content:
							content = content.replace(text_to_replace, replace_with)

					# If the key is "Border"
					# And the color is the first one
					if (
						key == "Border" and
						color_name == self.colors["List"][0]
					):
						number_text = self.Date.texts["number_names, type: list"]["en"][number].title() + " (" + str(number) + ")"

						text += templates["Heading"].format(number_text + " pixel border colors")

					# Create the CSS class
					css_class = "." + selector_text + " {" + "\n" + \
					"\t" + content + "\n" + \
					"}"

					# Add the color to the root text
					text += css_class

					# If the color name is not the last one, add a line break to the root text
					if color_name != self.colors["List"][-1]:
						text += "\n\n"

				# If the key is "Border"
				# And the number is not the last one
				if (
					key == "Border" and
					number != numbers[-1]
				):
					text += "\n\n"

			# If the number of keys is not one (1)
			# And the selector is not the last one, add a line break to the root text
			if (
				len(keys) != 1 and
				key != keys[-1]
			):
				text += "\n\n"

		# ----- #

		# Update the "Colors CSS" text inside the "Texts" dictionary of the root dictionary
		self.dictionary["Texts"]["Colors CSS"] = text

	def Update_Color_Files(self):
		# Store the old file text inside the "On file" key
		self.dictionary["Texts"]["On file"] = self.File.Contents(self.dictionary["Files"]["Colors CSS"])["string"]

		# Update the "Colors.css" file
		self.File.Edit(self.dictionary["Files"]["Colors CSS"], self.dictionary["Texts"]["Colors CSS"], "w")

		# Store the updated file text inside the "Updated text" key
		self.dictionary["Texts"]["Updated text"] = self.dictionary["Texts"]["Colors CSS"]

	def Show_Information(self):
		# Define the texts variable for easier typing
		texts = self.dictionary["Texts"]

		# Update the "File was updated" state
		if texts["On file"] != texts["Updated text"]:
			self.dictionary["States"]["File was updated"] = True

		# Define the text to show
		text_to_show = self.language_texts["the_file_of_colors_was_not_modified"]

		# If the "File was updated" state is True
		if self.dictionary["States"]["File was updated"] == True:
			text_to_show = self.language_texts["the_file_of_colors_was_updated_with_new_contents"]

		# Show space and five dash separators
		print()
		print(self.separators["5"])
		print()

		# Show the text to show
		print(text_to_show + ".")
		print()

		# If the "File was updated" state is True
		if self.dictionary["States"]["File was updated"] == True:
			# Show the file
			print(self.File.language_texts["file, title()"] + ":")
			print("\t" + self.dictionary["Files"]["Colors CSS"])
			print()

		# Show a five dash separator
		print(self.separators["5"])
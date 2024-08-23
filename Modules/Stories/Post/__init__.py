# Post.py

from Stories.Stories import Stories as Stories

from copy import deepcopy

class Post(Stories):
	def __init__(self, run_as_module = False):
		super().__init__()

		# Define the root dictionary
		self.dictionary = {
			"Chapters": {
				"Numbers": {
					"Last posted chapter": 1
				},
				"Titles": {}
			},
			"Chapter": {}
		}

		# Define the "States" dictionary
		self.states = {
			"Run as module": run_as_module,
			"Select chapter": False,
			"Ask for skipping": True
		}

		# If the "Run as module" state is True
		if self.states["Run as module"] == True:
			# Define the "Ask for skipping" state as False
			self.states["Ask for skipping"] = False

		# Import sub-classes method
		self.Import_Sub_Classes()

		# If the "Run as module" state is False
		# And the last posted chapter of the story is the last one
		if (
			self.states["Run as module"] == False and
			self.story["Information"]["Chapters"]["Numbers"]["Last posted chapter"] == self.story["Information"]["Chapters"]["Numbers"]["Total"]
		):
			# Get the story title and define the select text
			select_text = self.language_texts["the_selected_story_{}_has_all_of_its_chapters_posted_please_select_another_one"].format(self.story["Titles"][self.user_language])

			# Ask the user to select another story
			self.Select_Story(select_text_parameter = select_text)

		# Define the steps of chapter posting
		self.Define_Steps()

		# Ask if the user wants to select a chapter
		self.Select_Chapter()

		# If the user did not select a chapter
		if self.states["Select chapter"] == False:
			# Define the chapter to be posted
			self.Define_Chapter()

		# Run the chapter posting steps
		self.Run_Steps()

		# Register the chapter task if the "Run as module" state is False
		if self.states["Run as module"] == False:
			self.Register_Task()

	def Import_Sub_Classes(self):
		from Social_Networks.Open_Social_Network import Open_Social_Network as Open_Social_Network

		self.Open_Social_Network = Open_Social_Network

	def Define_Steps(self):
		# Define the default steps dictionary
		self.dictionary["Steps"] = {
			"Create the covers": {
				"Text key": "cover_creation"
			},
			"Update websites": {
				"Text key": "websites_update"
			},
			"Post on story websites": {
				"Text key": "story_website_chapter_posting"
			},
			"Post on Social Networks": {
				"Text key": "social_network_posting"
			}
		}

		# Iterate through the chapter posting steps
		for key, step in self.dictionary["Steps"].items():
			# Update the step dictionary with new keys
			self.dictionary["Steps"][key] = {
				"Key": key,
				"Text key": step["Text key"],
				"Text": self.language_texts[step["Text key"]],
				"Skip": False,
				"Can skip": True,
				"Method": getattr(self, key.title().replace(" ", "_"))
			}

			# If the "Can skip" key is present inside the root step dictionary
			if "Can skip" in step:
				# Update the key inside the local step dictionary
				self.dictionary["Steps"][key]["Can skip"] = step["Can skip"]

	def Run_Steps(self):
		# Iterate through the step key and dictionaries inside the "Steps" dictionary
		for key, step in self.dictionary["Steps"].items():
			# If the "Can skip" switch is True
			if step["Can skip"] == True:
				# Ask if the user wants to skip the posting step
				self.Skip(step)

			# If the "Skip" state is False
			if self.dictionary["Steps"][key]["Skip"] == False:
				# Define the "run" variable as True
				run = True

				# If the "Run as module" state is True
				# And the key is not "Create the covers"
				if (
					self.states["Run as module"] == True and
					key != "Create the covers"
				):
					# Define the "run" variable as False
					# To only update the chapter covers ("Create the covers" method)
					# And not run the other chapter posting steps
					run = False

				# If the "run" variable is True, run the method
				if run == True:
					step["Method"]()

	def Skip(self, step, custom_text = None):
		# If the custom text parameter is not None
		if custom_text != None:
			# Define the chapter posting step text as the custom text
			step["Text"] = custom_text

		# If the "Ask for skipping" state is True
		# And the "Skip" state of the chapter posting step is False
		if (
			self.states["Ask for skipping"] == True and
			step["Skip"] == False
		):
			# Define the input text with the step text
			input_text = self.Language.language_texts["skip_the, feminine"] + " " + step["Text"]

			# Ask if the user wants to skip this chapter posting step
			step["Skip"] = self.Input.Yes_Or_No(input_text)

		# If the "Skip" state is True
		if step["Skip"] == True:
			# Show the "You skipped the [step text]" text
			print()
			print(self.Language.language_texts["you_skipped_the, feminine"] + " " + step["Text"] + ".")

			# Show a five dash space separator text
			print()
			print(self.separators["5"])

		# Update the root step dictionary with the local one
		self.dictionary["Steps"][step["Key"]] = step

		# Return the step dictionary
		return step

	def Select_Chapter(self):
		# Ask if the user wants to select a chapter
		self.states["Select chapter"] = self.Input.Yes_Or_No(self.language_texts["select_chapter"])

		# If the user wants to select a chapter
		if self.states["Select chapter"] == True:
			# Ask the user to select a chapter from the list
			chapter_number = self.Input.Select(self.dictionary["Chapters"]["Titles"])["Option"]["Number"]

			# Define the Chapter dictionary
			self.Define_Chapter(chapter_number)

	def Define_Chapter(self, chapter_number = None):
		# Define the chapter "Titles" key
		self.dictionary["Chapters"]["Titles"] = deepcopy(self.story["Information"]["Chapters"]["Titles"])

		# Update the last posted chapter number with the number inside the story "Information" dictionary
		self.dictionary["Chapters"]["Numbers"]["Last posted chapter"] = self.story["Information"]["Chapters"]["Numbers"]["Last posted chapter"]

		# ---------- #

		# Define the defined chapter if there is not one in the root dictionary
		if "Defined chapter" not in self.dictionary:
			self.dictionary["Defined chapter"] = 1

		# Define the "Chapter" dictionary, with the defined chapter
		self.dictionary["Chapter"] = {
			"Number": self.dictionary["Defined chapter"],
			"Numbers": {
				"Leading zeroes": self.dictionary["Defined chapter"],
				"Names": {}
			},
			"Titles": {},
			"Titles (with leading zeroes)": {},
			"Links": {},
			"Post cards": {},
			"Folders": {},
			"Files": {}
		}

		# ---------- #

		# If the last posted chapter is not the last chapter already
		if self.dictionary["Chapters"]["Numbers"]["Last posted chapter"] != self.story["Information"]["Chapters"]["Numbers"]["Total"]:
			# Add one to the last posted chapter number
			self.dictionary["Chapters"]["Numbers"]["Last posted chapter"] += 1

		# Update the "Last posted chapter" key on the story "Information" dictionary
		self.story["Information"]["Chapters"]["Numbers"]["Last posted chapter"] = self.dictionary["Chapters"]["Numbers"]["Last posted chapter"]

		# Update the "Chapters.json" file of the story with the new "last posted chapter" number
		self.JSON.Edit(self.story["Folders"]["Information"]["Chapters"], self.story["Information"]["Chapters"])

		# ---------- #

		# Update the "Chapter" and "Leading zeroes" number keys
		self.dictionary["Chapter"]["Number"] = self.dictionary["Chapters"]["Numbers"]["Last posted chapter"]

		# If the "chapter number" parameter is not None
		if chapter_number != None:
			# Define it as the chapter number
			self.dictionary["Chapter"]["Number"] = chapter_number

		# Define the chapter number with leading zeroes
		self.dictionary["Chapter"]["Numbers"]["Leading zeroes"] = str(self.Text.Add_Leading_Zeroes(self.dictionary["Chapter"]["Number"]))

		# Iterate through the small languages list
		for language in self.languages["small"]:
			# Create the chapter title variable
			# [Chapter title]
			title = self.dictionary["Chapters"]["Titles"][language][self.dictionary["Chapter"]["Number"] - 1]

			# Add it to the "Titles" dictionary
			self.dictionary["Chapter"]["Titles"][language] = title

			# Add the chapter number with leading zeroes to the chapter title
			# [01 - Chapter Title]
			title = self.dictionary["Chapter"]["Numbers"]["Leading zeroes"] + " - " + title

			# Define the chapter title inside the "Titles (with leading zeroes)" dictionary
			self.dictionary["Chapter"]["Titles (with leading zeroes)"][language] = title

			# Get the number name of the chapter number
			number_name = self.Date.texts["number_names, type: list"][language][int(self.dictionary["Chapter"]["Number"])]

			# Add it to the "Names" dictionary
			self.dictionary["Chapter"]["Numbers"]["Names"][language] = number_name

		# ---------- #

		# Define the "Covers" folder of the chapter
		self.dictionary["Chapter"]["Folders"]["Covers"] = {
			"root": "",
			"Name": self.Cover_Folder_Name(self.dictionary["Chapter"]["Number"])
		}

		# Define the root folder
		folder_name = self.dictionary["Chapter"]["Folders"]["Covers"]["Name"]

		self.dictionary["Chapter"]["Folders"]["Covers"]["root"] = self.story["Folders"]["Covers"]["Landscape"][self.full_user_language]["root"] + folder_name + "/"

		# ---------- #

		# Fill the chapter "Files" dictionary
		for language in self.languages["small"]:
			# Get the full language
			full_language = self.languages["full"][language]

			# Define the chapters folder in the current language
			file = self.story["Folders"]["Chapters"][full_language]["root"]

			# Add the chapter title in the current language and the text extension
			file += self.dictionary["Chapter"]["Titles (with leading zeroes)"][language] + ".txt"

			# Define the language chapter file in the "Files" dictionary
			self.dictionary["Chapter"]["Files"][language] = file

		# ---------- #

		# Show information about the chapter

		# If the "Run as module" state is False
		# Or it is True
		# And the "chapter number" parameter is not None
		if (
			self.states["Run as module"] == False or
			self.states["Run as module"] == True and
			chapter_number != None
		):
			# Show a five dash space separator
			print()
			print(self.separators["5"])
			print()

			# Show the chapter number and total chapter number
			print(self.language_texts["chapter_number"] + ":")
			print(self.dictionary["Chapter"]["Numbers"]["Leading zeroes"])
			print()

			# Show the chapter title
			chapter_title = self.dictionary["Chapter"]["Titles"][self.user_language]

			print(self.Language.language_texts["title, title()"] + ":")
			print(chapter_title)

	def Create_The_Covers(self):
		# Iterate through the "Cover types" dictionary
		for cover_type in self.stories["Cover types"]["Dictionary"].values():
			# Define the skip text template
			template = self.language_texts["cover_creation"] + " " + self.Language.language_texts["in_{}_mode"]

			# Define the skip text, formatting it with the cover type title
			text = template.format("[" + cover_type["Titles"][self.user_language] + "]")

			# Ask if the user wants to skip the creation of the cover with the specific type
			self.Skip(self.dictionary["Steps"]["Create the covers"], custom_text = text)

			# If the "Skip" state of the "Create cover" step is False
			if self.dictionary["Steps"]["Create the covers"]["Skip"] == False:
				# Create the cover
				self.Create_Cover(cover_type)

	def Create_Cover(self, cover_type):
		# Define the default list of chapter titles
		chapter_titles = [
			self.dictionary["Chapter"]["Titles (with leading zeroes)"]["en"]
		]

		# If the "Run as module" state is True
		if self.states["Run as module"] == True:
			# Define the list of chapter titles as the titles of the story
			chapter_titles = self.story["Information"]["Chapters"]["Titles"]["en"]

			# Update the "Chapter" dictionary
			self.dictionary["Chapter"] = {
				"Number": 1,
				"Numbers": {
					"Leading zeroes": 1
				}
			}

		# Iterate through the small languages list
		for language in self.languages["small"]:
			# Get the full and translated languages
			full_language = self.languages["full"][language]
			translated_language = self.languages["full_translated"][language][self.user_language]

			# Define the default text key for the template
			text_key = "opening_the_photoshop_file_of_chapter_covers, type: long"

			# If the "Run as module" state is True
			if self.states["Run as module"] == True:
				# Update the text key for the template
				text_key += ", plural"

			# Get the template of the explanation text with the key
			# About opening the Photoshop file of the chapter covers, in the current cover type, and the current language
			template = self.language_texts[text_key]

			# Define the list of items to use in the template
			items = [
				cover_type["Titles"][self.user_language], # The title of the cover type in the user language
				translated_language, # The translated language
				cover_type["Titles"][self.user_language], # The title of the cover type in the user language
				self.stories["Cover types"]["Extension"].upper() # The extension of the cover file
			]

			# If the "Run as module" state is True
			if self.states["Run as module"] == True:
				# Update the list of items to use in the template
				items = [
					cover_type["Titles"][self.user_language], # The title of the cover type in the user language
					translated_language, # The translated language
					self.story["Information"]["Chapters"]["Numbers"]["Total"], # The total number of chapters of the story
					cover_type["Titles"][self.user_language], # The title of the cover type in the user language
					self.stories["Cover types"]["Extension"].upper() # The extension of the cover file
				]

			# Format the template with the list of items, making the explanation text
			text = template.format(*items)

			# Show a five dash space separators
			print()
			print(self.separators["5"])
			print()

			# Show the "opening the Photoshop cover file" text
			print(text)

			# Get the language Photoshop cover file of the story in the current cover type
			file = self.story["Folders"]["Covers"][cover_type["Title"]][full_language]["Photoshop"]

			# Open the Photoshop file
			self.System.Open(file)

			# Iterate through the English chapter titles
			c = 1
			for chapter_title in chapter_titles:
				# If the "Run as module" state is False
				if self.states["Run as module"] == False:
					# Show a space separator
					print()

					# Copy the chapter title
					self.Copy_Title(language)

					# Ask the user for input when they finish rendering the cover
					self.Input.Type(self.language_texts["press_enter_when_you_finish_rendering_the_cover"])

					# Show a space separator
					print()

				# If the "Run as module" state is True
				if self.states["Run as module"] == True:
					# Define the "Chapter" dictionary of the current chapter
					self.Define_Chapter(c)

					# If the chapter title is the first one
					if chapter_title == chapter_titles[0]:
						# Ask for the user to press Enter before continuing to the next chapter
						self.Input.Type(self.Language.language_texts["continue, title()"])

					# If the chapter title is not the first one
					if chapter_title != chapter_titles[0]:
						# Show a space separator
						print()

				# If the "Run as module" state is False
				if self.states["Run as module"] == False:
					# Show a five dash space separator
					print(self.separators["5"])
					print()

				# Move the cover file to the cover folders
				self.Move_Cover(language, full_language, cover_type)

				# Add one to the "c" number
				c += 1

			# If the language is the last one
			if language == self.languages["small"][-1]:
				# Show a five dash space separator
				print()
				print(self.separators["5"])

	def Copy_Title(self, language):
		# Define the type text
		type_text = self.language_texts["press_enter_to_copy_the_chapter_title"]

		# Show the full current language in the user language
		print(self.languages["full_translated"][language][self.user_language] + ":")

		# Show the chapter title in the user language
		print(self.dictionary["Chapter"]["Titles (with leading zeroes)"][language])

		# Ask for user input to copy the chapter title
		self.Input.Type(type_text)

		# Copy the chapter title
		self.Text.Copy(self.dictionary["Chapter"]["Titles (with leading zeroes)"][self.user_language], verbose = False)

	def Move_Cover(self, language, full_language, cover_type):
		# Cover type folder:
		# "[Cover_Type]/"
		# 
		# Example:
		# "/Landscape/"
		folder_name = cover_type["Titles"][self.user_language] + "/"

		# Full language and chapter number folders:
		# "[Full_Language]/X - XX/"
		# 
		# Example:
		# "/English/1 - 10/"
		# 
		# Complete:
		# "/Landscape/English/1 - 10/"
		folder_name += full_language + "/" + self.dictionary["Chapter"]["Folders"]["Covers"]["Name"] + "/"

		# Define the file name
		file_name = "PSD copy"

		# If the "Run as module" state is True
		if self.states["Run as module"] == True:
			# Define the file name as and underline plus the chapter number with leading zeroes
			file_name = "_" + self.dictionary["Chapter"]["Numbers"]["Leading zeroes"]

		# Add the extension to the file name
		file_name += "." + self.stories["Cover types"]["Extension"]

		# Define the source file
		# With the cover type folder in the current language and the file name above
		# 
		# Example:
		# "/[Cover type folder]/PSD copy.png"
		# "/[Cover type folder]/_01.png" (Run as module = True)
		source_file = self.story["Folders"]["Covers"][cover_type["Title"]][full_language]["root"] + file_name

		# Show the source file
		print(self.File.language_texts["source_file"] + ":")
		print(source_file)

		# ---------- #

		# Update the file name
		file_name = self.dictionary["Chapter"]["Numbers"]["Leading zeroes"] + "." + self.stories["Cover types"]["Extension"]

		# Define the cover file to the chapter covers folder of the story folder inside the "Mega Stories" folder
		destination_file = self.story["Folders"]["Covers"]["root"] + folder_name + file_name

		# Show the copy information with the name of the folder, and the destination file
		print()
		print(self.language_texts["copying_the_cover_to_the_{}_folder"].format(self.language_texts["mega_stories"]) + ":")
		print(destination_file)

		# Copy the source file to the destination location
		self.File.Copy(source_file, destination_file)

		# ---------- #

		# Copy the cover file to the chapter covers folder of the story folder inside the "Images" folder of the "Mega Websites" folder
		# If the cover type is "Landscape"
		if cover_type["Key"] == "Landscape":
			# Get the destination folder ("Images" on "Mega Websites")
			destination_folder = self.story["Folders"]["Covers"]["Websites"]["Chapters"]["root"]

			# Add the chapter number with leading zeroes to the destination folder
			# Defining the chapter folder
			destination_folder += self.dictionary["Chapter"]["Numbers"]["Leading zeroes"] + "/"

			# Define the destination file with the full language as the file name
			# 
			# Complete example:
			# "/Chapters/01/English.png"
			destination_file = destination_folder + full_language + "." + self.stories["Cover types"]["Extension"]

			# Show the copy information with the name of the folder, and the destination file
			print()
			print(self.language_texts["copying_the_cover_to_the_{}_folder"].format(self.language_texts["website_story_covers"]) + ":")
			print(destination_file)

			# Copy the source file to the destination location
			self.File.Copy(source_file, destination_file)

		# Delete the render file (the original source file)
		self.File.Delete(source_file)

	def Update_Websites(self):
		# Import the "Update websites" sub-class of the "PHP" module
		from PHP.Update_Websites import Update_Websites as Update_Websites

		# Define the dictionary to update the story website
		dictionary = {
			"Website": self.story["Title"],
			"Verbose": True
		}

		# Update the website of the selected story
		Update_Websites(dictionary)

	def Copy_Chapter_Text(self, language, full_language):
		# Get the language chapter file
		chapter_file = self.dictionary["Chapter"]["Files"][language]

		# Get the chapter text from the file above
		chapter_text = self.File.Contents(chapter_file)["string"]

		# Define the type text
		type_text = self.language_texts["press_enter_to_copy_the_chapter_text"]

		# Ask for user input before copying the chapter text
		self.Input.Type(type_text)

		# Copy the chapter text
		self.Text.Copy(chapter_text, verbose = False)

	def Post_On_Story_Websites(self):
		# Show a five dash separator
		print()
		print(self.separators["5"])
		print()

		# Iterate through the dictionary of story websites
		for key, story_website in self.stories["Story websites"]["Dictionary"].items():
			# Iterate through the list of small languages
			for language in self.languages["small"]:
				# Get the full language
				full_language = self.languages["full"][language]

				# Define the link of the story website
				story_link = self.story["Information"]["Links"][key]["Edit story"]

				# If the "Add chapter" key is inside the "Links" dictionary
				if "Add chapter" in self.story["Information"]["Links"][key]:
					# Update the story link to that one
					story_link = self.story["Information"]["Links"][key]["Add chapter"]

				# Get the language link
				story_link = story_link[language]

				# Define the "Social Networks" dictionary to use in the "Open_Social_Network" sub-class
				# With the list of social networks to open, and their custom links
				social_networks = {
					"List": [
						key
					],
					"Custom links": {
						key: story_link
					},
					"States": {
						"First separator": False
					},
					"Spaces": {
						"First": False
					}
				}

				# If the language is not the first one
				if language != self.languages["small"][0]:
					# Define the first space of the "Open_Social_Network" class as True
					social_networks["Spaces"]["First"] = True

				# If the story website is not the first one
				# And the language is the first one
				if (
					key != self.stories["Story websites"]["List"][0] and
					language == self.languages["small"][0]
				):
					# Show an additional space separator
					print()

				# Open the story website social network on the story page in the current language, with the custom link
				self.Open_Social_Network(social_networks)

				# Show a space separator
				print()

				# Copy the chapter title
				self.Copy_Title(language)

				# Copy the chapter text
				self.Copy_Chapter_Text(language, full_language)

				# If the language is the user language
				if language == self.user_language:
					# Get the link of the posted chapter on the story website from the user
					input_text = self.language_texts["paste_the_link_of_the_chapter_on"] + " " + story_website["Name"]

					self.dictionary["Chapter"]["Links"][key] = self.Input.Type(input_text, accept_enter = False, next_line = True)

				# Show a space separator and a three dash separator (for each language)
				print()
				print(self.separators["5"])

	def Post_On_Social_Networks(self):
		# Define the website chapter link
		# With the "chapter" parameter to automatically open the chapter when the website loads
		self.dictionary["Chapter"]["Links"]["Website"] = self.story["Information"]["Links"]["Website"]["Link"].replace(" ", "%20") + "?chapter={}#".format(str(self.dictionary["Chapter"]["Number"]))

		# Define the "Social networks" dictionary with the list of the social networks
		social_networks = {
			"List": [
				"Discord",
				"WhatsApp",
				"Instagram",
				"Facebook",
				"Twitter",
				"Wattpad",
				"Spirit Fanfics"
			],
			"To open": [],
			"Dictionary": {}
		}

		# Add social networks to the "To open" list
		for key in social_networks["List"]:
			# If the key is not "Instagram"
			# And is not a story website
			if (
				key != "Instagram" and
				key not in self.stories["Story websites"]["List"]
			):
				# Add it to the "To open" list
				social_networks["To open"].append(key)

		# Only get the "Social Network" dictionary of these social networks:
		# Wattpad, Spirit Fanfics, Twitter, and Facebook
		for key in social_networks["List"]:
			social_networks["Dictionary"][key] = self.social_networks["Dictionary"][key]

		# ---------- #

		# Show a space and a five dash separator
		print()
		print(self.separators["5"])

		# Get the root post template in the user language from its file
		file = self.stories["Folders"]["Database"]["Post templates"][self.user_language]

		template = self.File.Contents(file)["string"]

		# Make an underlined version of the story title
		self.story["Titles"]["Underlined"] = self.story["Titles"][self.user_language].replace(" ", "_")

		# ---------- #

		# Create the "Social Network" post card

		# Define the "Make_Post_Cards" dictionary
		dictionary = {
			"Key": "Social Network",
			"Link key": "Website",
			"Template": template
		}

		# Make the post cards
		self.Make_Post_Cards(dictionary)

		# ---------- #

		# Create the second "Social Network" post card

		# Get the root post template in the user language from its file
		file = self.stories["Folders"]["Database"]["Post templates"]["Story websites"][self.user_language]

		template = self.File.Contents(file)["string"]

		# Iterate through the dictionary of story websites
		for key, story_website in self.stories["Story websites"]["Dictionary"].items():
			# Define the "Make_Post_Cards" dictionary
			dictionary = {
				"Key": "Social Network (" + key + ")",
				"Link key": key,
				"Template": template
			}

			# Define the list of items
			dictionary["Items"] = [
				story_website["Name"], # The name of the story website
				self.dictionary["Chapter"]["Links"][key], # The chapter link of the website of the story
				self.story["Titles"]["Underlined"], # The underlined story title, for the story hashtag in the end
				story_website["Name"].replace(" ", "_") # The name of the story website on the hashtag format
			]

			# Make the post cards
			self.Make_Post_Cards(dictionary)

		# ---------- #

		# Get the root post template in the user language from its file
		file = self.stories["Folders"]["Database"]["Post templates"][self.user_language]

		template = self.File.Contents(file)["string"]

		# Iterate through the list of story websites
		for key in self.stories["Story websites"]["List"]:
			# Define the "Make_Post_Cards" dictionary
			dictionary = {
				"Key": key,
				"Template": template
			}

			# Make the post cards
			self.Make_Post_Cards(dictionary)

		# ---------- #

		# Post the chapter on the social networks

		# Create the last card variable
		last_card = ""

		# Iterate through the social networks inside the "To open" list
		for key in social_networks["To open"]:
			# Define the "Social Networks" dictionary to use in the "Open_Social_Network" sub-class
			social_networks_dictionary = {
				"List": [
					key
				],
				"Custom links": {
					key: self.social_networks["Dictionary"][key]["Information"]["Opening link"]
				},
				"States": {
					"First separator": True
				}
			}

			# If the social network is "Discord"
			if key == "Discord":
				# Define the custom link as the "#stories" channel on my Discord server
				social_networks_dictionary["Custom links"][key] = "https://discord.com/channels/311004778777935872/1041558273708540065"

			# If the social network is not "Discord"
			if key != "Discord":
				# Remove the "Custom links" dictionary
				social_networks_dictionary.pop("Custom links")

			# If the social network is the first one
			if key == social_networks["To open"][0]:
				# Remove the first separator
				social_networks_dictionary["States"]["First separator"] = False

			# Open the social network with its custom link
			self.Open_Social_Network(social_networks_dictionary)

			# ---------- #

			# If the social network is the first one
			if key == social_networks["To open"][0]:
				# Open the covers folder of the chapter
				self.System.Open(self.dictionary["Chapter"]["Folders"]["Covers"]["root"])

			# ---------- #

			# Define the card as the generic "Social Network" card
			card = self.dictionary["Chapter"]["Post cards"]["Social Network"]

			# If the social network is not in the defined list
			if key not in ["Facebook", "Twitter"]:
				# Remove the hashtags of the card
				card = self.Remove_Hashtags(card)

			# If the social network is "Discord"
			if key == "Discord":
				# Add the "@Updates" role to the card
				card += "\n\n" + "<@&1172626527175848086>"

			# If the social network is "Facebook"
			if key == "Facebook":
				# Get the hashtags
				hashtags = card.splitlines()[-1]

				# Remove the hashtags of the card
				card = self.Remove_Hashtags(card)

				# Iterate through the list of story websites
				for sub_key in self.stories["Story websites"]["List"]:
					# Get the social network card of the current story website to the root card
					second_card = self.dictionary["Chapter"]["Post cards"]["Social Network ({})".format(sub_key)]

					# Remove the hashtags of the card
					second_card = self.Remove_Hashtags(second_card)

					# Add the second card to the root card
					card += "\n\n" + "-" + "\n\n" + \
					second_card

				# Add the hashtags back
				card += "\n\n" + hashtags

			# If the current card is not the same as the last card
			if card != last_card:
				# Copy the social network post card
				self.Text.Copy(card, verbose = False)

			# Define the last card variable as the current card
			last_card = card

			# Define the input text
			input_text = self.language_texts["press_enter_when_you_finish_posting_the_card_on"]

			# If the social network is "Facebook"
			if key != "Facebook":
				print()
				print(self.Language.language_texts["press_enter_when_you_finish"] + "...")

				input_text = self.language_texts["posting_the_general_card_on"]

			# Wait for the user to finish posting the social network card
			self.Input.Type(input_text + " " + key)

			# ---------- #

			# If the social network is not "Facebook"
			if key != "Facebook":
				# Iterate through the list of story websites
				for sub_key in self.stories["Story websites"]["List"]:
					# Define the social network card of the current story website
					card = self.dictionary["Chapter"]["Post cards"]["Social Network ({})".format(sub_key)]

					# If the social network is in the defined list
					if key in ["Discord", "WhatsApp"]:
						# Remove the hashtags of the card
						card = self.Remove_Hashtags(card)

					# Copy the social network post card for the current story website
					self.Text.Copy(card, verbose = False)

					# Define the input text
					input_text = self.language_texts["posting_the_social_network_card_of"]

					# Wait for the user to finish posting the social network post card of the current story website
					self.Input.Type(input_text + ' "' + sub_key + '"')

		# ---------- #

		# Post the chapter on the story websites

		# Iterate through the list of story websites
		for key in self.stories["Story websites"]["List"]:
			# Define the "Social Networks" dictionary to use in the "Open_Social_Network" sub-class
			social_networks_dictionary = {
				"List": [
					key
				],
				"Custom links": {
					key: self.social_networks["Dictionary"][key]["Links"]["Posts"]
				},
				"States": {
					"First separator": True
				}
			}

			# If the social network is the first one
			if key == social_networks["To open"][0]:
				# Remove the first separator
				social_networks_dictionary["States"]["First separator"] = False

			# Open the social network with its custom link
			self.Open_Social_Network(social_networks_dictionary)

			# ---------- #

			# Define the post card
			card = self.dictionary["Chapter"]["Post cards"][key]

			# Copy the social network post card
			self.Text.Copy(card, verbose = False)

			# Define the input text
			input_text = self.language_texts["press_enter_when_you_finish_posting_the_card_on"]

			# Wait for the user to finish posting the social network card
			self.Input.Type(input_text + " " + key)

	def Make_Post_Cards(self, dictionary):
		# If the "Link key" is not present in the dictionary
		if "Link key" not in dictionary:
			# Use the root key
			dictionary["Link key"] = dictionary["Key"]

		# Define the list of items to use in the template if it is not present
		if "Items" not in dictionary:
			dictionary["Items"] = [
				self.story["Titles"][self.user_language], # The story title in the user language
				self.dictionary["Chapter"]["Numbers"]["Names"][self.user_language], # The number name of the chapter title in the user language
				self.dictionary["Chapter"]["Titles (with leading zeroes)"][self.user_language], # The chapter title in the user language, with leading zeroes
				self.dictionary["Chapter"]["Links"][dictionary["Link key"]], # The chapter link of the website of the story
				self.story["Titles"]["Underlined"] # The underlined story title, for the story hashtag in the end
			]

		# If the story website is "Wattpad"
		if dictionary["Key"] == "Wattpad":
			dictionary["Items"][3] += "\n"

		# Format the story website template with the list of items, making the story website post card
		self.dictionary["Chapter"]["Post cards"][dictionary["Key"]] = dictionary["Template"].format(*dictionary["Items"])

		# Replace the "One more chapter" text with the "The first chapter" text if the chapter is the first one of the story
		if int(self.dictionary["Chapter"]["Number"]) <= 1:
			self.dictionary["Chapter"]["Post cards"][dictionary["Key"]] = self.dictionary["Chapter"]["Post cards"][dictionary["Key"]].replace(self.language_texts["one_more_chapter"], self.language_texts["the_first_chapter"])

		# Replace the "One more chapter" text with the "The last chapter" text if the chapter is the last one of the story
		if int(self.dictionary["Chapter"]["Number"]) == len(self.dictionary["Chapters"]["Titles"][self.user_language]):
			self.dictionary["Chapter"]["Post cards"][dictionary["Key"]] = self.dictionary["Chapter"]["Post cards"][dictionary["Key"]].replace(self.language_texts["one_more_chapter"], self.language_texts["the_last_chapter"])

	def Remove_Hashtags(self, card):
		# Transform the card into a list of lines
		card = card.splitlines()

		# Remove the hashtags
		card.pop(-1)
		card.pop(-1)

		# Transform the list into a text with line breaks
		card = self.Text.From_List(card, next_line = True)

		# Return the card
		return card

	def Register_Task(self):
		# Create the task dictionary, to use it on the "Tasks" class
		self.task_dictionary = {
			"Task": {
				"Titles": {},
				"Custom state text": self.Language.texts["posted"]
			}
		}

		# Add the task titles in all languages
		for language in self.languages["small"]:
			# Get the "I published the chapter number" text template in the current language
			template = self.texts["i_published_the_chapter_number_{}_of_my_story_{}_on_the_story_website"][language]

			# Add a comma and the "on" text
			template += ", " + self.Language.texts["on, style: in"][language] + " "

			# Add the names of the story websites

			# Iterate through the list of story websites
			for key in self.stories["Story websites"]["List"]:
				# If the story website is the last one
				if key == self.stories["Story websites"]["List"][-1]:
					# Add a comma and the "and on" text
					template += ", " + self.Language.texts["and_on, style: in"][language] + " "

				# Add the name of the story website
				template += key

			# Add the "with the title" text
			template += ", " + self.Language.texts["with_the_title"][language] + ': "{}"'

			# Define the list of items to use in the template
			items = [
				self.dictionary["Chapter"]["Numbers"]["Names"][language], # The number name of the chapter in the current language
				self.dictionary["Chapter"]["Number"], # The number of the chapter
				self.story["Titles"][language], # The story title in the current language
				self.dictionary["Chapter"]["Titles"][language] # The chapter title in the current language
			]

			# Format the template and get the task title in the current language
			title = template.format(*items)

			# Add the title to the "Titles" dictionary
			self.task_dictionary["Task"]["Titles"][language] = title

		# Register the task with the root method
		Stories.Register_Task(self, self.task_dictionary)
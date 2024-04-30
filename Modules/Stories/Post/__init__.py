# Post.py

from Stories.Stories import Stories as Stories

from copy import deepcopy

class Post(Stories):
	def __init__(self, run_as_module = False):
		super().__init__()

		# Define the root dictionary
		self.dictionary = {
			"Steps": {
				"Create the covers": {
					"Text key": "cover_creation"
				},
				"Update websites": {
					"Text key": "websites_update"
				},
				"Post on Wattpad": {
					"Text key": "wattpad_chapter_posting"
				},
				"Post on Social Networks": {
					"Text key": "social_network_posting"
				}
			},
			"Chapters": {
				"Numbers": {
					"Last posted chapter": 1
				},
				"Titles": {}
			}
		}

		# Define "States" dictionary
		self.states = {
			"Run as module": run_as_module,
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

		# Define the chapter to be posted
		self.Define_Chapter()

		# Define the steps of chapter posting
		self.Define_Steps()

		# Run the chapter posting steps
		self.Run_Posting_Steps()

		# Register the chapter task if the "Run as module" state is False
		if self.states["Run as module"] == False:
			self.Register_Task()

	def Import_Sub_Classes(self):
		from Social_Networks.Open_Social_Network import Open_Social_Network as Open_Social_Network

		self.Open_Social_Network = Open_Social_Network

	def Define_Chapter(self):
		# Define the chapter "Titles" key
		self.dictionary["Chapters"]["Titles"] = deepcopy(self.story["Information"]["Chapters"]["Titles"])

		# Define the "Chapter" dictionary
		self.dictionary["Chapter"] = {
			"Number": 1,
			"Numbers": {
				"Leading zeroes": 1,
				"Names": {}
			},
			"Titles": {},
			"Titles (with leading zeroes)": {},
			"Links": {
				"Website": "",
				"Wattpad": ""
			},
			"Cards": {}
		}

		# Update the last posted chapter number with the number inside the story "Information" dictionary
		self.dictionary["Chapters"]["Numbers"]["Last posted chapter"] = self.story["Information"]["Chapters"]["Numbers"]["Last posted chapter"]

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

		self.dictionary["Chapter"]["Numbers"]["Leading zeroes"] = str(self.Text.Add_Leading_Zeroes(self.dictionary["Chapter"]["Number"]))

		# Iterate through the small languages list
		for language in self.languages["small"]:
			# Get the full language
			full_language = self.languages["full"][language]

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

		# Show information about the chapter

		# Show a five dash space separator
		print()
		print(self.separators["5"])
		print()

		# Show the chapter number and total chapter number
		print(self.Language.language_texts["number, title()"] + ":")
		print(self.dictionary["Chapter"]["Numbers"]["Leading zeroes"])
		print()

		# Show the chapter title
		chapter_title = self.dictionary["Chapter"]["Titles"][self.user_language]

		print(self.Language.language_texts["title, title()"] + ":")
		print(chapter_title)

	def Define_Steps(self):
		# Iterate through the chapter posting steps
		for key, step in self.dictionary["Steps"].items():
			# Update the step dictionary
			self.dictionary["Steps"][key] = {
				"Key": key,
				"Text key": step["Text key"],
				"Text": self.language_texts[step["Text key"]],
				"Skip": False,
				"Method": getattr(self, key.title().replace(" ", "_"))
			}

	def Run_Posting_Steps(self):
		# Iterate through the step key and dictionaries inside the "Steps" dictionary
		for key, step in self.dictionary["Steps"].items():
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

		# Update the root step dictionary with the local one
		self.dictionary["Steps"][step["Key"]] = step

		# Return the step dictionary
		return step

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

			# Show a five dash space separator
			print(self.separators["5"])
			print()

			# Show the "opening the Photoshop cover file" text
			print(text)

			# Get the language Photoshop cover file of the story in the current cover type
			file = self.story["Folders"]["Covers"][cover_type["Title"]][full_language]["Photoshop"]

			# Open the Photoshop file
			self.System.Open(file)

			# Show a space separator
			print()

			# Iterate through the English chapter titles
			for chapter_title in chapter_titles:
				# If the "Run as module" state is True
				if self.states["Run as module"] == True:
					# Update the chapter number with leading zeroes
					self.dictionary["Chapter"]["Numbers"]["Leading zeroes"] = str(self.Text.Add_Leading_Zeroes(self.dictionary["Chapter"]["Number"]))

					# Show a five dash separator
					print()
					print(self.separators["5"])
					print()

					# Show the "Chapter number:" text
					print(self.language_texts["chapter_number"] + ":")

					# Show the chapter number followed by the total chapter number
					print("[" + str(self.dictionary["Chapter"]["Number"]) + "/" + str(self.story["Information"]["Chapters"]["Numbers"]["Total"]) + "]")
					print()

				# If the "Run as module" state is False
				if self.states["Run as module"] == False:
					# Copy the chapter title
					self.Copy_Title(language)

					# Ask the user for input when they finish rendering the cover
					self.Input.Type(self.language_texts["press_enter_when_you_finish_rendering_the_cover"])

					# Show a space separator
					print()

				# If the "Run as module" state is True
				if self.states["Run as module"] == True:
					# Add one to the chapter number
					self.dictionary["Chapter"]["Number"] += 1

					# If the "testing" switch is True
					# And the chapter title is the first one
					if (
						self.switches["testing"] == True and
						chapter_title == chapter_titles[0]
					):
						# Ask for the user to press Enter before continuing to the next chapter
						self.Input.Type(self.Language.language_texts["continue, title()"])

				# Move the cover file to the cover folders
				self.Move_Cover(language, full_language, cover_type)

			# If the "Run as module" state is True
			if self.states["Run as module"] == True:
				print()

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
		folder_name += full_language + "/" + self.Cover_Folder_Name(self.dictionary["Chapter"]["Number"]) + "/"

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

		# Update the website of the selected story
		Update_Websites(module_website = self.story["Title"])

	def Copy_Chapter_Text(self, language, full_language):
		# Define the chapters folder in the language
		chapter_file = self.story["Folders"]["Chapters"][full_language]["root"]

		# Add the chapter title in the current language and the text extension
		chapter_file += self.dictionary["Chapter"]["Titles (with leading zeroes)"][language] + ".txt"

		# Get the chapter text from the file above
		chapter_text = self.File.Contents(chapter_file)["string"]

		# Define the type text
		type_text = self.language_texts["press_enter_to_copy_the_chapter_text"]

		# Ask for user input before copying the chapter text
		self.Input.Type(type_text)

		# Copy the chapter text
		self.Text.Copy(chapter_text, verbose = False)

	def Post_On_Wattpad(self):
		# Show a five dash separator
		print()
		print(self.separators["5"])
		print()

		# Iterate through the small languages list
		for language in self.languages["small"]:
			# Get the full and translated languages
			full_language = self.languages["full"][language]
			translated_language = self.languages["full_translated"][language][self.user_language]

			# Define the Wattpad link variable for easier typing
			# With the Wattpad link of the story in the current language
			wattpad_link = self.story["Information"]["Wattpad"][language]["Link"]

			# Define the "Social Networks" dictionary to use in the "Open_Social_Network" sub-class
			# With the list of social networks to open, and their custom links
			social_networks = {
				"List": [
					"Wattpad"
				],
				"Custom links": {
					"Wattpad": wattpad_link
				},
				"States": {
					"First separator": False
				},
				"Spaces": {
					"First": False
				}
			}

			# Open the "Wattpad" social network on the story page in the current language, with the custom link
			self.Open_Social_Network(social_networks)

			# Show a space separator
			print()

			# Copy the chapter title
			self.Copy_Title(language)

			# Copy the chapter text
			self.Copy_Chapter_Text(language, full_language)

			# Show a space separator and a three dash separator (for each language)
			print()
			print(self.separators["3"])

			# If the language is the first one, show an additional space separator
			if language == self.languages["small"][0]:
				print()

	def Post_On_Social_Networks(self):
		# Make an underlined version of the story title
		self.story["Titles"]["Underlined"] = self.story["Titles"][self.user_language].replace(" ", "_")

		# Define the website chapter link
		# With the "chapter" parameter to automatically open the chapter when the website loads
		self.dictionary["Chapter"]["Links"]["Website"] = self.story["Information"]["Website"]["Link"].replace(" ", "%20") + "?chapter={}#".format(str(self.dictionary["Chapter"]["Number"]))

		# Define the "Social networks" dictionary with the list of the social networks
		social_networks = {
			"List": [
				"Wattpad",
				"Twitter, Facebook"
			],
			"Dictionary": {}
		}

		# Only get the "Social Network" dictionary of these social networks:
		# Wattpad, Twitter, and Facebook
		for social_network in ["Wattpad", "Twitter", "Facebook"]:
			social_networks["Dictionary"][social_network] = self.social_networks["Dictionary"][social_network]

		# Define the "Social Network" dictionary of the "Twitter" and "Facebook" social networks as "Twitter"
		social_networks["Dictionary"]["Twitter, Facebook"] = social_networks["Dictionary"]["Twitter"]

		# Show a space and a five dash separator
		print()
		print(self.separators["5"])

		# Get the link of the posted chapter on Wattpad from the user
		self.dictionary["Chapter"]["Links"]["Wattpad"] = self.Input.Type(self.language_texts["paste_the_wattpad_chapter_link"])

		# Get the "Wattpad" post template in the user language from its file
		file = self.stories["Folders"]["Database"]["Post templates"]["Wattpad"][self.user_language]

		template = self.File.Contents(file)["string"]

		# Define the list of items to use in the template
		items = [
			self.story["Titles"]["Underlined"], # The underlined story title, for the story hashtag
			self.dictionary["Chapter"]["Titles (with leading zeroes)"][self.user_language], # The chapter title in the user language
			self.dictionary["Chapter"]["Numbers"]["Names"][self.user_language], # The number name of the chapter title in the user language
			self.dictionary["Chapter"]["Links"]["Wattpad"], # The Wattpad link for the chapter
			self.story["Titles"]["Underlined"] # The underlined story title, for the story hashtag in the end
		]

		# Format the "Wattpad" template with the list of items, making the Wattpad post card
		self.dictionary["Chapter"]["Cards"]["Wattpad"] = template.format(*items)

		# ---------- #

		# Get the "Twitter & Facebook" post template in the user language from its file
		file = self.stories["Folders"]["Database"]["Post templates"]["Twitter, Facebook"][self.user_language]

		template = self.File.Contents(file)["string"]

		# Define the list of items to use in the template
		items = [
			self.dictionary["Chapter"]["Links"]["Website"], # The link of the chapter on the story website
			self.story["Titles"]["Underlined"] # The underlined story title, for the story hashtag
		]

		# Format the "Twitter & Facebook" template with the list of items, making the Twitter and Facebook post card
		self.dictionary["Chapter"]["Cards"]["Twitter, Facebook"] = template.format(*items)

		# Replace the "One more chapter" text with the "The first chapter" text if the chapter is the first one of the story
		if int(self.dictionary["Chapter"]["Number"]) <= 1:
			self.dictionary["Chapter"]["Cards"]["Wattpad"] = self.dictionary["Chapter"]["Cards"]["Wattpad"].replace(self.language_texts["one_more_chapter"], self.language_texts["the_first_chapter"])

		# Replace the "One more chapter" text with the "The last chapter" text if the chapter is the last one of the story
		if int(self.dictionary["Chapter"]["Number"]) == len(self.dictionary["Chapters"]["Titles"][self.user_language]):
			self.dictionary["Chapter"]["Cards"]["Wattpad"] = self.dictionary["Chapter"]["Cards"]["Wattpad"].replace(self.language_texts["one_more_chapter"], self.language_texts["the_last_chapter"])

		# Copy the cards and open the social network links to post the cards
		for social_network in social_networks["List"]:
			# If the social network is "Wattpad"
			if social_network == "Wattpad":
				# Copy the "Wattpad" card
				self.Text.Copy(self.dictionary["Chapter"]["Cards"]["Wattpad"], verbose = False)

				# Define the "Social Networks" dictionary to use in the "Open_Social_Network" sub-class
				social_networks = {
					"List": [
						"Wattpad"
					],
					"Custom links": {
						"Wattpad": self.social_networks["Dictionary"]["Wattpad"]["Profile"]["Links"]["Conversations"]
					},
					"States": {
						"First separator": False
					}
				}

				# Open the "Wattpad" social network
				self.Open_Social_Network(social_networks)

				# Wait for the user to finish posting the Wattpad card
				self.Input.Type(self.language_texts["press_enter_when_you_finish_posting_the_card_on_{}"].format(social_network))

				# Show a space and a five dash separator
				print()
				print(self.separators["5"])

			# If the social network is "Twitter, Facebook"
			if social_network == "Twitter, Facebook":
				# Copy the "Wattpad" card
				self.Text.Copy(self.dictionary["Chapter"]["Cards"]["Wattpad"], verbose = False)

				# Define the "Social Networks" dictionary to use in the "Open_Social_Network" sub-class
				social_networks = {
					"List": [
						"Twitter",
						"Facebook"
					],
					"Custom links": {
						"Twitter": self.social_networks["Dictionary"]["Twitter"]["Profile"]["Links"]["Profile"],
						"Facebook": self.social_networks["Dictionary"]["Facebook"]["Profile"]["Links"]["Profile"]
					},
					"States": {
						"First separator": False
					}
				}

				# Open the "Twitter" and "Facebook" social networks
				self.Open_Social_Network(social_networks)

				# Update the "social network" name
				social_network = social_network.replace(", ", " " + self.Language.language_texts["and"] + " ")

				# Wait for the user to finish posting
				self.Input.Type(self.language_texts["paste_the_first_part_of_the_card_of_{}_on_the_post_text_box"].format(social_network))

				# Copy the Twitter and Facebook card
				self.Text.Copy(self.dictionary["Chapter"]["Cards"]["Twitter, Facebook"], verbose = False)

				# Wait for the user to finish posting the Twitter and Facebook card
				self.Input.Type(self.language_texts["paste_the_second_part_of_the_card_of_{}_on_the_post_text_box"].format(social_network))

			# If the social network is not the last one
			if social_network != social_networks["List"][-1]:
				# Show a space separator and a five dash separator
				print()
				print(self.separators["5"])

	def Register_Task(self):
		# Create the task dictionary, to use it on the "Tasks" class
		self.task_dictionary = {
			"Task": {
				"Titles": {}
			}
		}

		# Add the task titles in all languages
		for language in self.languages["small"]:
			# Get the "I published the chapter number" text template in the current language
			template = self.texts["i_published_the_chapter_number_{}_of_my_story_{}_on_the_story_website_and_on_wattpad_with_the_title"][language]

			# Define the list of items to use in the template
			items = [
				self.dictionary["Chapter"]["Numbers"]["Names"][language], # The number name of the chapter in the current language
				self.dictionary["Chapter"]["Number"], # The number of the chapter
				self.story["Titles"][language] # The story title in the current language
			]

			# Format the template and get the task title in the current language
			title = template.format(*items)

			# Add the chapter title
			title += ': "' + self.dictionary["Chapter"]["Titles (with leading zeroes)"][language] + '"'

			# Add the title to the "Titles" dictionary
			self.task_dictionary["Task"]["Titles"][language] = title

		# Register the task with the root method
		Stories.Register_Task(self, self.task_dictionary)
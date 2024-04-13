# Post.py

from Stories.Stories import Stories as Stories

class Post(Stories):
	def __init__(self, run_as_module = False):
		super().__init__()

		self.run_as_module = run_as_module

		# Import sub-classes method
		self.Import_Sub_Classes()

		# Define the "Post" dictionary
		self.Define_The_Post_Dictionary()

		# If the "Run as module" state is False
		if self.post["States"]["Run as module"] == False:
			# If a story is not selected
			# Or a story is selected
			# And its last posted chapter is the last one
			if (
				self.story == None or
				self.story != None and
				int(self.post["Last posted chapter"]) == self.story["Information"]["Chapters"]["Number"]
			):
				# Get the story title and define the select text
				select_text = self.language_texts["the_selected_story_{}_has_all_of_its_chapters_posted_please_select_another_one"].format(story_title)

				# Ask the user to select another story
				self.Select_Story(select_text_parameter = select_text)

			# Define the chapter to post
			self.Define_Chapter()

		# Run the posting steps
		self.Run_Posting_Steps()

		# Register the chapter task if the "Run as module" state is False
		if self.post["States"]["Run as module"] == False:
			self.Register_Task()

	def Import_Sub_Classes(self):
		from Social_Networks.Open_Social_Network import Open_Social_Network as Open_Social_Network

		self.Open_Social_Network = Open_Social_Network

	def Define_The_Post_Dictionary(self):
		# Define the "Post" dictionary
		self.post = {
			"States": {
				"Ask for skipping": True,
				"Run as module": self.run_as_module
			},
			"Steps": {
				"Create_Cover": {
					"Text key": "cover_creation"
				},
				"Update_Websites": {
					"Text key": "websites_update"
				},
				"Post_On_Wattpad": {
					"Text key": "wattpad_chapter_posting"
				},
				"Post_On_Social_Networks": {
					"Text key": "social_network_posting"
				}
			},
			"Last posted chapter": 1,
			"Extension": "png",
			"Chapter titles": {},
			"Chapter": {}
		}

		# Define the "Ask for skipping" state
		if self.post["States"]["Run as module"] == True:
			self.post["States"]["Ask for skipping"] = False

		# Iterate through the posting steps
		for key, step in self.post["Steps"].items():
			# Get the text using the text key
			self.post["Steps"][key] = {
				"Key": key,
				"Text key": step["Text key"],
				"Text": self.language_texts[step["Text key"]],
				"Skip": False
			}

		# If the story is not None, get the last posted chapter number
		if self.story != None:
			self.post["Last posted chapter"] = self.story["Information"]["Chapters"]["Last posted chapter"]

		# Define the "Chapter titles" key
		self.post["Chapter titles"] = self.story["Information"]["Chapters"]["Titles"]

	def Run_Posting_Steps(self):
		# Execute the posting steps
		for key, step in self.post["Steps"].items():
			# Ask if the user wants to skip the posting step
			self.Skip(step)

			# If the "Skip" state is False
			if self.post["Steps"][key]["Skip"] == False:
				# Define the "run" variable as True
				run = True

				# If the "Run as module" state is True
				# And the key is not "Create_Cover"
				if (
					self.post["States"]["Run as module"] == True and
					key != "Create_Cover"
				):
					# Define the "run" variable as False
					run = False

				# Get the method to run it
				method = getattr(self, key)

				# If the "run" variable is True, run the method
				if run == True:
					method()

	def Skip(self, step, custom_text = None):
		# If the custom text parameter is not None
		if custom_text != None:
			# Define the posting step text as the custom text
			step["Text"] = custom_text

		# If the "Ask for skipping" state is True
		# And the "Skip" state of the posting step is False
		if (
			self.post["States"]["Ask for skipping"] == True and
			step["Skip"] == False
		):
			# Define the input text with the step text
			input_text = self.Language.language_texts["skip_the, feminine"] + " " + step["Text"]

			# Ask if the user wants to skip this posting step
			step["Skip"] = self.Input.Yes_Or_No(input_text)

		# If the "Skip" state is True
		if step["Skip"] == True:
			# Show the "You skipped the" [posting step text] text
			print()
			print(self.Language.language_texts["you_skipped_the"] + " " + step["Text"] + ".")

		# Update the root step dictionary with the local one
		self.post["Steps"][step["Key"]] = step

		# Return the step
		return step

	def Define_Chapter(self):
		# Define the "Chapter" dictionary
		self.post["Chapter"] = {
			"Number": self.post["Last posted chapter"],
			"Numbers": {
				"Leading zeroes": 0,
				"Names": {}
			},
			"Titles": {}
		}

		# Remove the chapters that were already posted
		c = 0

		while c <= int(self.post["Chapter"]["Number"]):
			for language in self.languages["small"]:
				self.post["Chapter titles"][language].pop(0)

			i += 1

		# Define the "last posted chapter" variable for faster typing
		self.post["Last posted chapter"] = self.post["Chapter"]["Number"]

		if self.post["Last posted chapter"] != self.story["Information"]["Chapters"]["Number"]:
			# Add one to the last posted chapter number
			self.post["Last posted chapter"] = self.post["Last posted chapter"] + 1

		# Update the "Last posted chapter" key
		self.story["Information"]["Chapters"]["Last posted chapter"] = self.post["Last posted chapter"]

		# Update the "Chapters.json" file of the story with the new "last posted chapter"
		self.JSON.Edit(self.story["Folders"]["Information"]["Chapters"], self.story["Information"]["Chapters"])

		# Update the "Total" and "Leading zeroes" keys
		self.post["Chapter"]["Number"] = self.post["Last posted chapter"]
		self.post["Chapter"]["Numbers"]["Leading zeroes"] = str(self.Text.Add_Leading_Zeroes(self.post["Chapters"]["Number"]))

		# Iterate through the small languages list
		for language in self.languages["small"]:
			# Get the full language
			full_language = self.languages["full"][language]

			# Create the chapter title with the chapter number and dash separator
			title = self.post["Chapter"]["Leading zeroes"] + " - "

			# Add the chapter title
			title += self.post["Chapter titles"][language][self.post["Chapter"]["Number"] - 1]

			# Define the chapter title inside the dictionary
			self.post["Chapter"]["Titles"][language] = title

		# Iterate through the small languages list
		for language in self.languages["small"]:
			# Get the number name
			number_name = self.Date.texts["number_names, type: list"][language][int(self.post["Chapter"]["Number"])]

			# Add it
			self.post["Chapter"]["Numbers"]["Names"][language] = number_name

	def Create_Cover(self):
		# Iterate through the "Cover types" dictionary
		for cover_type in self.stories["Cover types"]["Dictionary"].values():
			# Define the skip text template
			template = self.language_texts["cover_creation"] + " " + self.Language.language_texts["in_{}_mode"]

			# Define the skip text
			text = template.format("[" + cover_type["Titles"][self.user_language] + "]")

			# Ask if the user wants to skip the creation of the cover with the specific type
			self.Skip(self.post["Steps"]["Create_Cover"], custom_text = text)

			# If the "Skip" state of the "Create_Cover" step is False
			if self.post["Steps"]["Create_Cover"]["Skip"] == False:
				# Copy the language chapter titles and move the language chapter covers
				# (If the "Run as module" state is False)
				if self.post["States"]["Run as module"] == False:
					# Iterate through the small languages list
					for language in self.languages["small"]:
						# Get the full language
						full_language = self.languages["full"][language]

						# Get the template
						template = self.language_texts["opening_the_photoshop_file_of_chapter_covers, type: long"]

						# Define the list of items
						items = [
							cover_type["Titles"][self.user_language],
							translated_language,
							cover_type["Titles"][self.user_language],
							self.post["Extension"].upper()
						]

						# Format the template with the list of items, making the text
						text = template.format(*items)

						# Show the "opening the cover file" text
						print(self.separators["5"])
						print()
						print(text)

						# Get the language Photoshop cover file of the story
						file = self.story["Folders"]["Covers"][cover_type["Title"]][full_language]["Photoshop"]

						# Open the Photoshop file
						self.System.Open(file)

						# Show a space separator and copy the chapter title in the language
						print()

						# Copy the chapter title
						self.Copy_Title(language)

						# Ask the user for input when it finishes rendering the cover
						self.Input.Type(self.language_texts["press_enter_when_you_finish_rendering_the_cover"])

						# Show a space separator and move the cover file
						print()

						self.Move_Cover(language, full_language, cover_type)

				# If the "Run as module" state is True
				if self.post["States"]["Run as module"] == True:
					# Iterate through the small languages list
					for language in self.languages["small"]:
						# Get the full and translated language
						full_language = self.languages["full"][language]
						translated_language = self.languages["full_translated"][language][self.user_language]

						# Update the "Chapter" dictionary
						self.post["Chapter"] = {
							"Number": 1,
							"Numbers": {
								"Leading zeroes": 0
							}
						}

						# Get the template
						template = self.language_texts["opening_the_photoshop_file_of_chapter_covers, type: long, plural"]

						# Define the list of items
						items = [
							cover_type["Titles"][self.user_language],
							translated_language,
							self.story["Information"]["Chapters"]["Number"],
							cover_type["Titles"][self.user_language],
							self.post["Extension"].upper()
						]

						# Format the template with the list of items, making the text
						text = template.format(*items)

						# Show the "opening the cover file" text
						print(self.separators["5"])
						print()
						print(text)

						# Get the language Photoshop cover file of the story
						file = self.story["Folders"]["Covers"][cover_type["Title"]][full_language]["Photoshop"]

						# Open the Photoshop file
						self.System.Open(file)

						# Ask the user for input before moving the cover files
						self.Input.Type(self.language_texts["press_enter_when_you_finish_rendering_the_covers"])

						# Define the variable with the list of English chapter titles for faster typing
						chapter_titles = self.story["Information"]["Chapters"]["Titles"]["en"]

						# Iterate through the English chapter titles
						for chapter_title in chapter_titles:
							# Make the number with leading zeroes
							self.post["Chapter"]["Numbers"]["Leading zeroes"] = str(self.Text.Add_Leading_Zeroes(self.post["Chapter"]["Number"]))

							# Show a five dash separator
							print()
							print(self.separators["5"])
							print()

							# Show the "Chapter number" text
							print(self.language_texts["chapter_number"] + ":")

							# Show the chapter number followed by the total chapter number, for testing purposes
							print("[" + str(self.post["Chapter"]["Number"]) + "/" + str(self.story["Information"]["Chapters"]["Number"]) + "]")
							print()

							# Move the cover file
							self.Move_Cover(language, full_language, cover_type)

							# Add one to the chapter number
							self.post["Chapter"]["Number"] += 1

							# If the "testing" switch is True
							# And the chapter title is the first one
							if (
								self.switches["testing"] == True and
								chapter_title == chapter_titles[0]
							):
								# Ask for the user to press Enter after pausing inside the first chapter
								self.Input.Type(self.Language.language_texts["continue, title()"])

						print()

	def Copy_Title(self, language):
		# Define the type text
		type_text = self.language_texts["press_enter_to_copy_the_chapter_title"]

		# Show the chapter title
		print(self.languages["full_translated"][language][self.user_language] + ":")
		print(self.post["Chapter"]["Titles"][self.user_language])

		# Ask for user input to copy the chapter title
		self.Input.Type(type_text)

		# Copy the chapter title
		self.Text.Copy(self.post["Chapter"]["Titles"][self.user_language], verbose = False)

	def Move_Cover(self, language, full_language, cover_type):
		# "[Cover_Type]/"
		# 
		# Example:
		# "/Landscape/"
		folder_name = cover_type["Key"] + "/"

		# "[Full_Language]/X - XX/"
		# 
		# Example:
		# "/English/1 - 10/"
		# 
		# Complete:
		# "/Landscape/English/1 - 10/"
		folder_name += full_language + "/" + self.Cover_Folder_Name(self.post["Chapter"]["Number"]) + "/"

		# Define the file name
		# 
		# Example:
		# "01.png"
		file_name = self.post["Chapter"]["Numbers"]["Leading zeroes"] + "." + self.post["Extension"]

		# Define the source file
		# With the Photoshop render folder, the chapter number with leading zeroes, and the extension
		# 
		# Example:
		# "C:/[Photoshop render root folder]/_01.png"
		source_file = self.folders["Art"]["Photoshop"]["Render"]["root"] + "_" + file_name

		# Show the source file
		print(self.File.language_texts["source_file"] + ":")
		print(source_file)

		# Copy the cover file to the chapter covers folder of the story folder inside the "Mega Stories" folder
		destination_file = self.story["Folders"]["Covers"]["root"] + folder_name + file_name

		# Show the copy information with the name of the folder, and the destination file
		print()
		print(self.language_texts["copying_the_cover_to_the_{}_folder"].format(self.language_texts["mega_stories"]) + ":")
		print(destination_file)

		# Copy the file
		self.File.Copy(source_file, destination_file)

		# Copy the cover file to the chapter covers folder of the story folder inside the "Images" folder of the "Mega Websites" folder
		# If the cover type is "Landscape"
		if cover_type["Key"] == self.Language.texts["landscape, title()"]["en"]:
			# Get the folder
			destination_folder = self.story["Folders"]["Covers"]["Websites"]["Chapters"]["root"]

			# Add the chapter number with leading zeroes folder
			destination_folder += self.post["Chapter"]["Numbers"]["Leading zeroes"] + "/"

			# Define the destination file with the full language as the file name
			# 
			# Example:
			# "[Destination folder]/English.png"
			destination_file = destination_folder + full_language + "." + self.post["Extension"]

			# Show the copy information with the name of the folder, and the destination file
			print()
			print(self.language_texts["copying_the_cover_to_the_{}_folder"].format(self.language_texts["website_story_covers"]) + ":")
			print(destination_file)

			# Copy the file
			self.File.Copy(source_file, destination_file)

		# Delete the render file (the source file)
		self.File.Delete(source_file)

	def Update_Websites(self):
		# Import the "Update_Websites" sub-class of the "Code" module
		from Code.Update_Websites import Update_Websites as Update_Websites

		# Update the website of the selected story
		Update_Websites(self.switches, module_website = self.story["Title"])

	def Copy_Chapter_Text(self, language, full_language):
		# Define the chapter file
		chapter_file = self.story["Folders"]["Chapters"][full_language]["root"]

		# Add the chapter title
		chapter_file += self.post["Chapter"]["Titles"][language] + ".txt"

		# Get the chapter text
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
			# Get the full and translated language
			full_language = self.languages["full"][language]
			translated_language = self.languages["full_translated"][language][self.user_language]

			# Open the "Wattpad" social network on the story page of the current language
			wattpad_link = self.story["Information"]["Wattpad"][language]["Link"]

			# Define the "Social networks" dictionary to use in the "Open_Social_Network" sub-class
			social_networks = {
				"List": [
					"Wattpad"
				],
				"Custom links": {
					"Wattpad": wattpad_link
				}
			}

			# Open the "Wattpad" social network
			self.Open_Social_Network(social_networks)

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

		# Define the "Social networks" dictionary with the list of the social networks
		social_networks = {
			"List": [
				"Wattpad",
				"Twitter, Facebook"
			]
		}

		# Only get the "Social Network" dictionary of these social networks:
		# Wattpad, Twitter, and Facebook
		for social_network in self.social_networks.keys():
			if social_network in ["Wattpad", "Twitter", "Facebook"]:
				social_networks[social_network] = self.social_networks["Dictionary"][social_network]

		# Define the social network of the "Twitter" and "Facebook" social networks as "Twitter"
		social_networks["Twitter, Facebook"] = social_networks["Twitter"]

		# Get the chapter link from the user
		self.post["Chapter"]["Link"] = self.Input.Type(self.language_texts["paste_the_wattpad_chapter_link"])

		# Show a space separator and a five dash separator
		print()
		print(self.separators["5"])

		# Get the "Wattpad" post template
		file = self.stories["Folders"]["Database"]["Post templates"]["Wattpad"][self.user_language]

		template = self.File.Contents(file)["string"]

		# Define the list of items
		items = [
			self.story["Titles"]["Underlined"],
			self.post["Chapter"]["Titles"][self.user_language],
			self.post["Chapter"]["Numbers"]["Names"][self.user_language],
			self.post["Chapter"]["Wattpad link"],
			self.story["Titles"]["Underlined"]
		]

		# Format the "Wattpad" post template
		self.post["Chapter"]["Cards"]["Wattpad"] = template.format(*items)

		# Create the website chapter link
		self.post["Chapter"]["Chapter link"] = self.story["Information"]["Website"]["Link"].replace(" ", "%20") + "?chapter={}#".format(str(self.post["Chapter"]["Number"]))

		# ---------- #

		# Get the "Twitter & Facebook" post template
		file = self.stories["Folders"]["Database"]["Post templates"]["Twitter, Facebook"][self.user_language]

		template = self.File.Contents(file)["string"]

		# Define the list of items
		items = [
			self.post["Chapter"]["Chapter link"],
			self.story["Titles"]["Underlined"]
		]

		# Format the "Twitter & Facebook" template
		self.post["Chapter"]["Cards"]["Twitter, Facebook"] = template.format(*items)

		# Replace the "One more chapter" text with the "The first chapter" text if the chapter is the first one of the story
		if int(self.post["Chapter"]["Number"]) <= 1:
			self.post["Chapter"]["Cards"]["Wattpad"] = self.post["Chapter"]["Cards"]["Wattpad"].replace(self.language_texts["one_more_chapter"], self.language_texts["the_first_chapter"])

		# Replace the "One more chapter" text with the "The last chapter" text if the chapter is the last one of the story
		if int(self.post["Chapter"]["Number"]) == len(self.post["Chapter titles"][self.user_language]) - 1:
			self.post["Chapter"]["Cards"]["Wattpad"] = self.post["Chapter"]["Cards"]["Wattpad"].replace(self.language_texts["one_more_chapter"], self.language_texts["the_last_chapter"])

		# Copy the cards and open the Social Network links to post the cards
		for social_network in social_networks["List"]:
			if social_network == "Wattpad":
				# Copy the "Wattpad" card
				self.Text.Copy(self.post["Chapter"]["Cards"]["Wattpad"], verbose = False)

				# Define the "Social networks" dictionary to use in the "Open_Social_Network" sub-class
				social_networks = {
					"List": [
						"Wattpad"
					],
					"Custom links": {
						"Wattpad": self.social_networks["Wattpad"]["Profile"]["Links"]["Conversations"]
					}
				}

				# Open the "Wattpad" social network
				self.Open_Social_Network(social_networks)

				# Wait for the user to finish posting the Wattpad card
				self.Input.Type(self.language_texts["press_enter_when_you_finish_posting_the_card_on_{}"].format(social_network), first_space = False)

			if social_network == "Twitter, Facebook":
				# Copy the "Wattpad" card
				self.Text.Copy(self.post["Chapter"]["Cards"]["Wattpad"], verbose = False)

				# Define the "Social networks" dictionary to use in the "Open_Social_Network" sub-class
				social_networks = {
					"List": [
						"Twitter",
						"Facebook"
					],
					"Custom links": {
						"Twitter": self.social_networks["Twitter"]["Profile"]["Links"]["Profile"],
						"Facebook": self.social_networks["Facebook"]["Profile"]["Links"]["Profile"]
					}
				}

				# Open the "Twitter" and "Facebook" social networks
				self.Open_Social_Network(social_networks)

				# Wait for the user to finish posting
				self.Input.Type(self.language_texts["paste_the_first_part_of_the_card_of_{}_on_the_post_text_box"].format(social_network), first_space = False)

				# Copy the Twitter and Facebook card
				self.Text.Copy(self.post["Chapter"]["Cards"]["Twitter, Facebook"], verbose = False)

				# Wait for the user to finish posting the Twitter and Facebook card
				self.Input.Type(self.language_texts["paste_the_second_part_of_the_card_of_{}_on_the_post_text_box"].format(social_network))

			# If the social network is not the last one
			if social_network != social_networks["List"][-1]:
				# Show a space separator and a five dash separator
				print()
				print(self.separators["5"])

		# Write to the "Post template" file
		mixed_cards = self.post["Chapter"]["Cards"]["Wattpad"] + "\n\n-----\n\n" + self.post["Chapter"]["Cards"]["Twitter, Facebook"]

		self.File.Edit(self.story["Folders"]["Information"]["Post template"], mixed_cards, "w")

	def Register_Task(self):
		# Create the task dictionary
		self.task_dictionary = {
			"Task": {
				"Titles": {}
			}
		}

		# Add the task titles
		for language in self.languages["small"]:
			# Get the "I published the chapter" template in the current language
			template = self.texts["i_published_the_chapter_{}_of_my_story_{}_on_wattpad_and_stake2_website"][language]

			# Define the list of items
			items = [
				self.post["Chapter"]["Numbers"]["Names"][language],
				self.post["Chapter"]["Titles"][language]
			]

			# Format the template and define the task title in the current language
			self.task_dictionary["Task"]["Titles"][language] = template.format(*items)

		# Register the task with the root method
		Stories.Register_Task(self, self.task_dictionary, register_task = True)
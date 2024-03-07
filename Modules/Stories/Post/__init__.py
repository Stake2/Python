# Post.py

from Stories.Stories import Stories as Stories

class Post(Stories):
	def __init__(self, run_as_module = False):
		super().__init__()

		self.run_as_module = run_as_module

		from Social_Networks.Open_Social_Network import Open_Social_Network as Open_Social_Network

		self.Open_Social_Network = Open_Social_Network

		self.story["Chapter"] = {}

		# Define post steps
		self.post_steps = [
			"Create_Cover",
			"Update_Websites",
			"Post_On_Wattpad",
			"Post_On_Social_Networks"
		]

		# Define texts of post steps
		texts = [
			self.language_texts["cover_creation"],
			self.language_texts["websites_update"],
			self.language_texts["wattpad_chapter_posting"],
			self.language_texts["social_network_posting"]
		]

		self.post_steps_texts = {}
		self.step_skips = {}

		i = 0
		for post_step in self.post_steps:
			self.post_steps_texts[post_step] = texts[i]
			self.step_skips[post_step] = False

			i += 1

		self.ask_for_skipping = True

		if self.run_as_module == True:
			self.ask_for_skipping = False

		post = None

		if self.story != None:
			post = self.story["Information"]["Chapters"]["Last posted chapter"]

		# Select story and define chapter to be posted
		if self.run_as_module == False:
			if (
				self.story == None or
				self.story != None and
				int(post) == self.story["Information"]["Chapters"]["Number"]
			):
				select_text = None

				if (
					self.story != None and
					int(post) == self.story["Information"]["Chapters"]["Number"]
				):
					story_title = self.story["Titles"][self.user_language]
					select_text = self.language_texts["the_selected_story_{}_has_all_of_its_chapters_posted_please_select_another_one"].format(story_title)

				self.Select_Story(select_text_parameter = select_text)

			self.Define_Chapter()

		# Execute post steps
		for item in self.post_steps:
			self.Skip(item)

			if self.step_skips[item] == False:
				run = True

				if (
					self.run_as_module == True and
					item != "Create_Cover"
				):
					run = False

				method = getattr(self, item)

				if run == True:
					method()

		# Register chapter task
		if self.run_as_module == False:
			self.Register_Task()

	def Skip(self, item, custom_text = None):
		if custom_text != None:
			self.step_skips[item] = False
			self.post_steps_texts[item] = custom_text

		if (
			self.ask_for_skipping == True and
			self.step_skips[item] == False
		):
			input_text = self.JSON.Language.language_texts["skip_the, feminine"] + " " + self.post_steps_texts[item]

			self.step_skips[item] = self.Input.Yes_Or_No(input_text)

		if self.step_skips[item] == True:
			print()
			print(self.language_texts["you_skipped_the"] + " " + self.post_steps_texts[item] + ".")

	def Define_Chapter(self):
		if self.switches["testing"] == False:
			self.System.Open(self.story["Folders"]["Information"]["Chapter status"])

		# Remove chapter titles that were posted before the last posted chapter title
		self.chapter_titles = self.story["Information"]["Chapters"]["Titles"][self.user_language].copy()

		i = 1
		while i <= int(self.story["Information"]["Chapter status"]["Post"]):
			self.chapter_titles.pop(0)

			i += 1

		# Add one to last posted chapter number
		self.story["Information"]["Chapter status"]["Post"] = str(int(self.story["Information"]["Chapter status"]["Post"]) + 1)

		# Define the "Chapter" dictionary
		self.story["Chapter"] = {
			"Number": self.story["Information"]["Chapter status"]["Post"],
			"Leading zeroes": int(self.story["Information"]["Chapter status"]["Post"])
		}

		self.story["Chapter"]["Leading zeroes"] = str(self.Text.Add_Leading_Zeroes(self.story["Chapter"]["Number"]))

		# Make the chapter titles dictionary
		self.story["chapter_titles"] = {}

		for language in self.languages["small"]:
			full_language = self.languages["full"][language]

			self.story["chapter_titles"][language] = ""
			self.story["chapter_titles"][language] += str(self.Text.Add_Leading_Zeroes(self.story["Information"]["Chapter status"]["Post"])) + " - "
			self.story["chapter_titles"][language] += self.story["Information"]["Chapters"]["Titles"][language][int(self.story["Information"]["Chapter status"]["Post"]) - 1]

		# Define chapter number name
		self.story["chapter_number_name"] = self.Date.language_texts["number_names, type: list"][int(self.story["Chapter"]["Number"])]

		self.story["chapter_number_names"] = {}

		for language in self.languages["small"]:
			self.story["chapter_number_names"][language] = self.Date.texts["number_names, type: list"][language][int(self.story["Chapter"]["Number"])]

		text_to_write = self.Text.From_Dictionary(self.story["Information"]["Chapter status"], next_line = True)
		self.File.Edit(self.story["Folders"]["Information"]["Chapter status"], text_to_write, "w")

	def Create_Cover(self):
		# Create cover types dictionary
		self.cover_types = {
			"List": [
				"portrait, title()",
				"landscape, title()"
			],
			"Extension": "png"
		}

		list_ = []

		# Populate cover types dictionary
		i = 0
		for item in self.cover_types["List"]:
			english_text = self.JSON.Language.texts[item]["en"]

			self.cover_types[english_text] = {
				"Name": english_text,
				"Title": self.JSON.Language.language_texts[item],
				"Extension": self.cover_types["Extension"]
			}

			# Define the "Titles" dictionary
			self.cover_types[english_text]["Titles"] = {}

			for language in self.languages["small"]:
				self.cover_types[english_text]["Titles"][language] = self.JSON.Language.texts[item][language]

			list_.append(english_text)

			i += 1

		self.cover_types["List"] = list_

		self.skip_create_cover_type = False

		# Iterate through cover types list
		for self.cover_type in self.cover_types["List"]:
			self.cover_type = self.cover_types[self.cover_type]

			# Ask if the user wants to skip the creation of the cover with the specific type
			self.Skip("cover_creation_in_{}_mode", self.language_texts["cover_creation"] + " " + self.JSON.Language.language_texts["in_{}_mode"].format("[" + self.cover_type["Title"] + "]"))

			# If skip is false
			if self.step_skips["cover_creation_in_{}_mode"] == False:
				# Copy the language titles and move the language covers
				if self.run_as_module == False:
					for language in self.languages["small"]:
						full_language = self.languages["full"][language]

						print()

						self.Copy_Title(language)

						self.Input.Type(self.language_texts["press_enter_when_you_finish_rendering_the_cover"])

						print()

						self.Move_Cover(language, full_language)

				# if the module execution is activated, update all of the chapter covers
				if self.run_as_module == True:
					for language in self.languages["small"]:
						# Define the full and translated language
						full_language = self.languages["full"][language]
						translated_language = self.languages["full_translated"][language][self.user_language]

						# Define the template
						template = self.language_texts["opening_the_photoshop_file_of_chapter_covers, type: long"]

						# Define the list of items
						items = [
							self.cover_type["Title"],
							translated_language,
							self.cover_type["Title"],
							self.cover_type["Extension"].upper()
						]

						# Format the template with the list of items, making the text
						text = template.format(*items)

						# Show the "opening the cover file" text
						print(self.large_bar)
						print()
						print(text)

						# Define the cover file
						folder = self.story["Folders"]["Covers"]["Photoshop"][language]["root"]

						file = folder + self.cover_type["Titles"][self.user_language] + "_" + ".psd"

						self.System.Open(file)

						# Ask for user input before moving the covers
						self.Input.Type(self.language_texts["press_enter_when_you_finish_rendering_the_covers"])

						print()

						# Define the format text
						text = self.JSON.Language.language_texts["format, title()"] + ":" + "\n" + "[" + self.cover_type["Title"] + "] " + self.JSON.Language.language_texts["and_in"] + " [" + translated_language + "]"

						if language != self.languages["small"][0]:
							print(self.large_bar)
							print()
							print(self.language_texts["now_render_the_covers_in"] + " " + translated_language + ".")
							print()
							print(text)

							self.Input.Type(self.JSON.Language.language_texts["continue, title()"])

						self.story["Chapter"]["Number"] = 1

						if language == self.languages["small"][0]:
							print(self.large_bar)
							print()
							print(text)

						# Define the list of English chapter titles for easier typing
						chapter_titles = self.story["Information"]["Chapters"]["Titles"]["en"]

						# Iterate through the English chapter titles
						for chapter_title in chapter_titles:
							self.story["Chapter"]["Leading zeroes"] = str(self.Text.Add_Leading_Zeroes(self.story["Chapter"]["Number"]))

							print()
							print(self.large_bar)
							print()
							print(self.JSON.Language.language_texts["number, title()"] + ":")
							print("[" + str(self.story["Chapter"]["Number"]) + "/" + str(self.story["Information"]["Chapters"]["Number"]) + "]")
							print()

							self.Move_Cover(language, full_language)

							self.story["Chapter"]["Number"] += 1

							if (
								self.switches["testing"] == True and
								chapter_title == chapter_titles[0]
							):
								self.Input.Type(self.JSON.Language.language_texts["continue, title()"])

						print()

	def Copy_Title(self, language, post_chapter = False):
		type_text = self.language_texts["press_enter_to_copy_the_chapter_title_and_paste_it_on_the_vegas_title_media"]

		if post_chapter == True:
			type_text = self.language_texts["press_enter_to_copy_the_chapter_title"]

		# Show the chapter title
		print(self.languages["full_translated"][language][self.user_language] + ":")
		print(self.story["chapter_titles"][language])

		self.Input.Type(type_text)

		# Copy chapter title
		self.Text.Copy(self.story["chapter_titles"][language], verbose = False)

	def Move_Cover(self, language, full_language):
		# Define the folder name
		folder_name = ""

		# [Cover_Type]/
		folder_name += self.cover_type["Name"] + "/"

		# [Full_Language]/X - XX/
		folder_name += full_language + "/" + self.Cover_Folder_Name(self.story["Chapter"]["Number"]) + "/"

		# Define the source file
		source_file = self.folders["Art"]["Photoshop"]["Render"]["root"] + "_" + self.story["Chapter"]["Leading zeroes"] + "." + self.cover_type["Extension"]

		# Show them
		print(self.File.language_texts["source_file"] + ":")
		print(source_file)

		file_name = self.story["Chapter"]["Leading zeroes"] + "." + self.cover_type["Extension"]

		# Copy the cover file to the Mega Stories Story covers folder
		destination_file = self.story["Folders"]["Covers"]["root"] + folder_name + file_name

		# Show the copy information
		print()
		print(self.language_texts["copying_the_cover_to_the_{}_folder"].format(self.language_texts["mega_stories"]) + ":")
		print(destination_file)

		self.File.Copy(source_file, destination_file)

		# Copy the cover file to Mega Websites Story covers folder if cover type is Landscape
		if self.cover_type["Name"] == self.JSON.Language.texts["landscape, title()"]["en"]:
			# Define the folder
			destination_folder = self.story["Folders"]["Covers"]["Websites"]["Chapters"]["root"]

			# Add the chapter folder
			destination_folder += self.story["Chapter"]["Leading zeroes"] + "/"

			# Add the file name with the full language
			destination_file = destination_folder

			destination_file += full_language + "." + self.cover_type["Extension"]

			# Show the copy information
			print()
			print(self.language_texts["copying_the_cover_to_the_{}_folder"].format(self.language_texts["website_story_covers"]) + ":")
			print(destination_file)

			self.File.Copy(source_file, destination_file)

		# Delete the render file
		self.File.Delete(source_file)

	def Update_Websites(self):
		from Code.Update_Websites import Update_Websites as Update_Websites

		Update_Websites(self.switches, module_website = self.story["Title"])

	def Copy_Chapter_Text(self, language, full_language):
		# Get the chapter file
		self.story["Folders"]["Chapters"][full_language][self.story["Chapter"]["Number"]] = self.story["Folders"]["Chapters"][full_language]["root"]

		self.story["Folders"]["Chapters"][full_language][self.story["Chapter"]["Number"]] += self.story["chapter_titles"][language] + ".txt"

		# Get the chapter text
		chapter_text = self.File.Contents(self.story["Folders"]["Chapters"][full_language][self.story["Chapter"]["Number"]])["string"]

		type_text = self.language_texts["press_enter_to_copy_the_chapter_text"]

		self.Input.Type(type_text)

		# Copy the chapter text
		self.Text.Copy(chapter_text, verbose = False)

	def Post_On_Wattpad(self):
		print()
		print(self.large_bar)
		print()

		for language in self.languages["small"]:
			full_language = self.languages["full"][language]
			translated_language = self.languages["full_translated"][language][self.user_language]

			# Open the "Wattpad" social network on the story page
			wattpad_link = self.story["Information"]["Wattpad"][language]["Link"]

			social_networks = {
				"List": [
					"Wattpad"
				],
				"Custom links": {
					"Wattpad": wattpad_link
				}
			}

			self.Open_Social_Network(social_networks)

			# Copy the chapter title
			self.Copy_Title(language, post_chapter = True)

			# Copy the chapter text
			self.Copy_Chapter_Text(language, full_language)

			print()
			print("---")

			if language == self.languages["small"][0]:
				print()

	def Post_On_Social_Networks(self):
		self.story["title_underlined"] = self.story["Titles"][self.user_language].replace(" ", "_")

		social_networks = {
			"List": [
				"Wattpad",
				"Twitter, Facebook"
			]
		}

		# Only get the Social Network dictionary of Wattpad, Twitter, and Facebook
		for social_network in self.social_networks.keys():
			if social_network in ["Wattpad", "Twitter", "Facebook"]:
				social_networks[social_network] = self.social_networks["Dictionary"][social_network]

		social_networks["Twitter, Facebook"] = social_networks["Twitter"]

		# Get the chapter link
		self.story["Information"]["Wattpad"]["Chapter link"] = self.Input.Type(self.language_texts["paste_the_wattpad_chapter_link"])

		print()
		print(self.large_bar)

		# Formatthe  Wattpad template
		social_networks["Wattpad"]["Card"] = self.JSON.To_Python(self.stories["Folders"]["Database"]["Social Network post templates"]["Wattpad"])[self.user_language]

		social_networks["Wattpad"]["Card"] = social_networks["Wattpad"]["Card"].format(self.story["title_underlined"], self.story["chapter_number_name"], self.story["Chapter"]["Number"], self.story["Information"]["Wattpad"]["Chapter link"], self.story["title_underlined"])

		# Make the website chapter link
		self.story["Information"]["Website"]["Chapter link"] = self.story["Information"]["Website"]["link"].replace(" ", "%20") + "?chapter={}#".format(str(self.story["Chapter"]["Number"]))

		# Format the Twitter & Facebook template
		social_networks["Twitter, Facebook"]["Card"] = self.JSON.To_Python(self.stories["Folders"]["Database"]["Social Network post templates"]["Twitter, Facebook"])[self.user_language]

		social_networks["Twitter, Facebook"]["Card"] = social_networks["Twitter, Facebook"]["Card"].format(self.story["Information"]["Website"]["Chapter link"], self.story["title_underlined"])

		# Replace the "One more chapter" text with the "The first chapter" text if the chapter is the first one of the story
		if int(self.story["Chapter"]["Number"]) <= 1:
			social_networks["Wattpad"]["Card"] = social_networks["Wattpad"]["Card"].replace(self.language_texts["one_more_chapter"], self.language_texts["the_first_chapter"])

		# Replace the "One more chapter" text with the "The last chapter" text if the chapter is the last one of the story
		if int(self.story["Chapter"]["Number"]) == len(self.story["Titles"][self.user_language]) - 1:
			social_networks["Wattpad"]["Card"] = social_networks["Wattpad"]["Card"].replace(self.language_texts["one_more_chapter"], self.language_texts["the_last_chapter"])

		# Copy the cards and open the Social Network links to post the cards
		for social_network in social_networks["List"]:
			if social_network == "Wattpad":
				# Copy the Wattpad card
				self.Text.Copy(self.social_networks["Wattpad"]["Card"], verbose = False)

				# Open Wattpad
				self.Open_Social_Network(social_network_parameter = "Wattpad", custom_link = self.social_networks["Wattpad"]["Profile"]["Links"]["Conversations"], first_space = False)

				# Wait for the user to finish posting the Wattpad card
				self.Input.Type(self.language_texts["press_enter_when_you_finish_posting_the_card_on_{}"].format(social_network), first_space = False)

			if social_network == "Twitter, Facebook":
				# Copy the Wattpad card
				self.Text.Copy(social_networks["Wattpad"]["Card"], verbose = False)

				# Open Twitter
				self.Open_Social_Network(social_network_parameter = ["Twitter", "Facebook"], custom_link = [self.social_networks["Twitter"]["profile"]["profile"], self.social_networks["Facebook"]["profile"]["profile"]], first_space = False)

				# Wait for the user to finish posting
				self.Input.Type(self.language_texts["paste_the_first_part_of_the_card_of_{}_on_the_post_text_box"].format(social_network), first_space = False)

				# Copy the Twitter and Facebook card
				self.Text.Copy(social_networks["Twitter, Facebook"]["Card"], verbose = False)

				# Wait for the user to finish posting the Twitter and Facebook card
				self.Input.Type(self.language_texts["paste_the_second_part_of_the_card_of_{}_on_the_post_text_box"].format(social_network))

			if social_network != social_networks["List"][-1]:
				print()
				print(self.large_bar)

		# Write to the post template file
		self.mixed_cards = social_networks["Wattpad"]["Card"] + "\n\n---\n\n" + social_networks["Twitter, Facebook"]["Card"]
		self.File.Edit(self.story["Folders"]["Information"]["Post template"], self.mixed_cards, "w")

	def Register_Task(self):
		# Create the task dictionary
		self.task_dictionary = {
			"Task": {
				"Titles": {}
			}
		}

		# Add the task titles
		for language in self.languages["small"]:
			self.task_dictionary["Task"]["Titles"][language] = self.texts["i_published_the_chapter_{}_of_my_story_{}_on_wattpad_and_stake2_website"][language]

			self.task_dictionary["Task"]["Titles"][language] = self.task_dictionary["Task"]["Titles"][language].format(self.story["chapter_number_names"][language], self.story["Titles"][language])

		# Register the task with the root method
		Stories.Register_Task(self, self.task_dictionary, register_task = True)
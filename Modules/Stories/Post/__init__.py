# Post.py

from Stories.Stories import Stories as Stories

from Social_Networks.Open_Social_Network import Open_Social_Network as Open_Social_Network

from Code.Update_Websites import Update_Websites as Update_Websites

class Post(Stories):
	def __init__(self, run_as_module = False, story = None):
		super().__init__(select_story = False)

		self.run_as_module = run_as_module
		self.story = story

		# Define post steps
		self.post_steps = [
			"Create_Cover",
			"Update_Websites",
			"Post_On_Wattpad",
			"Post_On_Social_Networks",
		]

		# Define texts of post steps
		texts = [
			self.language_texts["cover_creation"],
			self.language_texts["websites_update"],
			self.language_texts["wattpad_chapter_posting"],
			self.language_texts["social_network_posting"],
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
			post = self.story["Information"]["Chapter status"]["Post"]

		# Select story and define chapter to be posted
		if self.run_as_module == False:
			if self.story == None or self.story != None and int(post) == len(self.story["Information"]["Chapter titles"][self.user_language]):
				select_text = None

				if self.story != None and int(post) == len(self.story["Information"]["Chapter titles"][self.user_language]):
					story_title = self.story["Information"]["Titles"][self.user_language]
					select_text = self.language_texts["the_selected_story_{}_has_all_of_its_chapters_posted_please_select_another_one"].format(story_title)

				self.Select_Story(select_text_parameter = select_text)

			self.Define_Chapter()

		# Execute post steps
		for item in self.post_steps:
			self.Skip(item)

			if self.step_skips[item] == False:
				run = True

				if self.run_as_module == True and item != "Create_Cover":
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

		if self.ask_for_skipping == True and self.step_skips[item] == False:
			self.step_skips[item] = self.Input.Yes_Or_No(self.language_texts["skip_the"] + " " + self.post_steps_texts[item])

		if self.step_skips[item] == True:
			print()
			print(self.language_texts["you_skipped_the"] + " " + self.post_steps_texts[item] + ".")

	def Define_Chapter(self):
		if self.global_switches["testing"] == False:
			self.File.Open(self.story["folders"]["Information"]["Chapter status"])

		# Remove chapter titles that were posted before the last posted chapter title
		self.chapter_titles = self.story["Information"]["Chapter titles"][self.user_language].copy()

		i = 1
		while i <= int(self.story["Information"]["Chapter status"]["Post"]):
			self.chapter_titles.pop(0)

			i += 1

		# Add one to last posted chapter number
		self.story["Information"]["Chapter status"]["Post"] = str(int(self.story["Information"]["Chapter status"]["Post"]) + 1)

		# Define chapter number
		self.story["chapter_number"] = int(self.story["Information"]["Chapter status"]["Post"])

		# Make chapter titles
		self.story["chapter_titles"] = {}

		for language in self.small_languages:
			full_language = self.full_languages[language]

			self.story["chapter_titles"][language] = ""
			self.story["chapter_titles"][language] += str(self.Text.Add_Leading_Zeros(self.story["Information"]["Chapter status"]["Post"])) + " - "
			self.story["chapter_titles"][language] += self.story["Information"]["Chapter titles"][language][int(self.story["Information"]["Chapter status"]["Post"]) - 1]

		# Define chapter number name
		self.story["chapter_number_name"] = self.Date.language_texts["number_names, type: list"][int(self.story["chapter_number"])]

		self.story["chapter_number_names"] = {}

		for language in self.small_languages:
			self.story["chapter_number_names"][language] = self.Date.texts["number_names, type: list"][language][int(self.story["chapter_number"])]

		text_to_write = self.Text.From_Dictionary(self.story["Information"]["Chapter status"], next_line = True)
		self.File.Edit(self.story["folders"]["Information"]["Chapter status"], text_to_write, "w")

	def Create_Cover(self):
		# Create cover types dictionary
		self.cover_types = {
			"list": [
				"portrait, title()",
				"landscape, title()",
			],
			"extension": "jpg",
		}

		list_ = []

		# Populate cover types dictionary
		i = 0
		for item in self.cover_types["list"]:
			english_text = self.texts[item]["en"]

			self.cover_types[english_text] = {
				"name": english_text,
				"title": self.language_texts[item],
				"extension": self.cover_types["extension"],
				"sony_vegas_file": self.story["folders"]["Sony Vegas Covers"] + english_text + ".veg",
			}

			list_.append(english_text)

			i += 1

		self.cover_types["list"] = list_

		self.skip_create_cover_type = False

		# Iterate through cover types list
		for self.cover_type in self.cover_types["list"]:
			self.cover_type = self.cover_types[self.cover_type]

			# Ask if the user wants to skip the creation of the cover with the specific type
			self.Skip("cover_creation_in_{}_mode", self.language_texts["cover_creation"] + " " + self.language_texts["in_{}_mode"].format("[" + self.cover_type["title"] + "]"))

			# If skip is false
			if self.step_skips["cover_creation_in_{}_mode"] == False:
				text = self.language_texts["opening_the_vegas_file_of_chapter_covers, type: long"]

				# Show create cover text
				print()
				print(self.large_bar)
				print()
				print(text.format(self.cover_type["title"], self.cover_type["title"], self.cover_type["extension"].upper()))

				# Open Sony Vegas file
				if self.global_switches["testing"] == False:
					self.File.Open(self.cover_type["sony_vegas_file"])

				# Copy language titles and move language covers
				if self.run_as_module == False:
					for language in self.small_languages:
						full_language = self.full_languages[language]

						print()

						self.Copy_Title(language)

						self.Input.Type(self.language_texts["press_enter_when_you_finish_rendering_the_cover"])

						print()

						self.Move_Cover(language, full_language)

				# if module execution is activate, update all of the chapter covers
				if self.run_as_module == True:
					self.Input.Type(self.language_texts["press_enter_when_you_finish_rendering_the_covers"])

					for language in self.small_languages:
						full_language = self.full_languages[language]
						translated_language = self.translated_languages[language][self.user_language]

						if language != self.small_languages[0]:
							print(self.large_bar)
							print()

							self.Input.Type(self.language_texts["now_render_the_covers_in"] + " " + translated_language, first_space = False)

						text = self.language_texts["format, title()"] + ":" + "\n" + "[" + self.cover_type["title"] + "] " + self.language_texts["and_in"] + " [" + translated_language + "]"

						self.story["chapter_number"] = 1

						if language != self.small_languages[0]:
							print()

						print(self.large_bar)
						print()
						print(text)
						print()

						for chapter_title in self.story["Information"]["Chapter titles"]["en"]:
							print(self.story["chapter_number"])

							self.Move_Cover(language, full_language)

							self.story["chapter_number"] += 1

						print()

				# Close Sony Vegas after updating the chapter cover in the specified cover type
				if self.global_switches["testing"] == False:
					self.File.Close("vegas110")

	def Copy_Title(self, language, post_chapter = False):
		type_text = self.language_texts["press_enter_to_copy_the_chapter_title_and_paste_it_on_the_vegas_title_media"]

		if post_chapter == True:
			type_text = self.language_texts["press_enter_to_copy_the_chapter_title"]

		# Show chapter title
		print(self.translated_languages[language][self.user_language] + ":")
		print(self.story["chapter_titles"][language])

		self.Input.Type(type_text)

		# Copy chapter title
		self.Text.Copy(self.story["chapter_titles"][language], verbose = False)

	def Move_Cover(self, language, full_language):
		folder_name = ""

		# [Cover_Type]/
		if self.cover_type["name"] != self.texts["landscape, title()"]["en"]:
			folder_name += self.cover_type["name"] + "/"

		# [Full_Language]/X - XX/
		folder_name += full_language + "/" + self.Cover_Folder_Name(self.story["chapter_number"]) + "/"

		# Source file name
		source_file_name = self.cover_type["name"]

		# File name number
		if self.run_as_module == False:
			source_file_name += "_0000"

		# Add chapter number for module execution
		if self.run_as_module == True:
			source_file_name += "_0000" + str(self.Text.Add_Leading_Zeros(self.story["chapter_number"]))

		# Add last two zeroes for non-module execution
		if self.run_as_module == False:
			source_file_name += "00"

		source_file = self.root_folders["sony_vegas_files"]["render"] + source_file_name + "." + self.cover_type["extension"]
		destination_file = self.root_folders["sony_vegas_files"]["render"] + str(self.story["chapter_number"]) + "." + self.cover_type["extension"]

		print(source_file)
		print(destination_file)

		# Rename file "[Cover_Type]_0000XX.extension" to "XX.extension"
		self.File.Move(source_file, destination_file)

		source_file = destination_file

		file_name = str(self.story["chapter_number"]) + "." + self.cover_type["extension"]

		# Copy cover file to Mega Stories Story covers folder
		destination_file = self.story["folders"]["Covers"]["root"] + folder_name + file_name

		print()
		print(self.language_texts["copying_the_cover_to_the_{}_folder"].format(self.language_texts["mega_stories"]) + ":")
		print(destination_file)

		self.File.Copy(source_file, destination_file)

		# Copy cover file to Mega Websites Story covers folder if cover type is Landscape
		if self.cover_type["name"] == self.texts["landscape, title()"]["en"]:
			destination_file = self.story["folders"]["Websites Story Covers"] + folder_name + file_name

			print()
			print(self.language_texts["copying_the_cover_to_the_{}_folder"].format(self.language_texts["website_story_covers"]) + ":")
			print(destination_file)

			self.File.Copy(source_file, destination_file)

		# Delete render file
		self.File.Delete(source_file)

	def Update_Websites(self):
		Update_Websites(self.global_switches, module_website = self.story["title"])

	def Copy_Chapter_Text(self, language, full_language):
		# Get chapter file
		self.story["folders"]["Chapters"][full_language][self.story["chapter_number"]] = self.story["folders"]["Chapters"][full_language]["root"]
		self.story["folders"]["Chapters"][full_language][self.story["chapter_number"]] += self.story["chapter_titles"][language] + ".txt"

		# Get chapter text
		chapter_text = self.File.Contents(self.story["folders"]["Chapters"][full_language][self.story["chapter_number"]])["string"]

		type_text = self.language_texts["press_enter_to_copy_the_chapter_text"]

		self.Input.Type(type_text)

		# Copy chapter text
		self.Text.Copy(chapter_text, verbose = False)

	def Post_On_Wattpad(self):
		print()
		print(self.large_bar)
		print()

		for language in self.small_languages:
			full_language = self.full_languages[language]
			translated_language = self.translated_languages[language][self.user_language]

			# Open Wattpad on story page
			wattpad_link = self.story["Information"]["Wattpad"]["links"][language]

			Open_Social_Network(social_network_parameter = "Wattpad", custom_link = wattpad_link, first_space = False)

			# Copy chapter title
			self.Copy_Title(language, post_chapter = True)

			# Copy chapter text
			self.Copy_Chapter_Text(language, full_language)

			print()
			print("---")

			if language == self.small_languages[0]:
				print()

	def Post_On_Social_Networks(self):
		self.story["title_underlined"] = self.story["Information"]["Titles"][self.user_language].replace(" ", "_")

		social_networks = {
			"list": [
				"Wattpad",
				"Twitter, Facebook",
			],
		}

		# Remove Social Networks that are not Wattpad, Twitter, and Facebook
		for social_network in self.social_networks.keys():
			if social_network in ["Wattpad", "Twitter", "Facebook"]:
				social_networks[social_network] = self.social_networks[social_network]

		social_networks["Twitter, Facebook"] = social_networks["Twitter"]

		# Get chapter link
		self.story["Information"]["Wattpad"]["Chapter link"] = self.Input.Type(self.language_texts["paste_the_wattpad_chapter_link"])

		print()
		print(self.large_bar)

		# Format Wattpad template
		social_networks["Wattpad"]["Card"] = self.Language.JSON_To_Python(self.stories["folders"]["Database"]["Social Network Card Templates"]["Wattpad"])[self.user_language]

		social_networks["Wattpad"]["Card"] = social_networks["Wattpad"]["Card"].format(self.story["title_underlined"], self.story["chapter_number_name"], self.story["chapter_number"], self.story["Information"]["Wattpad"]["Chapter link"], self.story["title_underlined"])

		# Make website chapter link
		self.story["Information"]["Website"]["Chapter link"] = self.story["Information"]["Website"]["link"].replace(" ", "%20") + "?({})#".format(str(self.story["chapter_number"]))

		# Format Twitter & Facebook template
		social_networks["Twitter, Facebook"]["Card"] = self.Language.JSON_To_Python(self.stories["folders"]["Database"]["Social Network Card Templates"]["Twitter, Facebook"])[self.user_language]

		social_networks["Twitter, Facebook"]["Card"] = social_networks["Twitter, Facebook"]["Card"].format(self.story["Information"]["Website"]["Chapter link"], self.story["title_underlined"])

		# Replace "One more chapter" with "The first chapter" if the chapter is the first one of the story
		if int(self.story["chapter_number"]) <= 1:
			social_networks["Wattpad"]["Card"] = social_networks["Wattpad"]["Card"].replace(self.language_texts["one_more_chapter"], self.language_texts["the_first_chapter"])

		# Replace "One more chapter" with "The last chapter" if the chapter is the last one of the story
		if int(self.story["chapter_number"]) == len(self.story["Information"]["Titles"][self.user_language]) - 1:
			social_networks["Wattpad"]["Card"] = social_networks["Wattpad"]["Card"].replace(self.language_texts["one_more_chapter"], self.language_texts["the_last_chapter"])

		# Copy cards and open Social Network links to post cards
		for social_network in social_networks["list"]:
			if social_network == "Wattpad":
				# Copy Wattpad card
				self.Text.Copy(self.social_networks["Wattpad"]["Card"], verbose = False)

				# Open Wattpad
				Open_Social_Network(social_network_parameter = "Wattpad", custom_link = self.social_networks["Wattpad"]["profile"]["conversations"], first_space = False)

				# Wait for user to finish posting Wattpad card
				self.Input.Type(self.language_texts["press_enter_when_you_finish_posting_the_card_on_{}"].format(social_network), first_space = False)

			if social_network == "Twitter, Facebook":
				# Copy Wattpad card
				self.Text.Copy(social_networks["Wattpad"]["Card"], verbose = False)

				# Open Twitter
				Open_Social_Network(social_network_parameter = ["Twitter", "Facebook"], custom_link = [self.social_networks["Twitter"]["profile"]["profile"], self.social_networks["Facebook"]["profile"]["profile"]], first_space = False)

				# Wait for user to finish posting
				self.Input.Type(self.language_texts["paste_the_first_part_of_the_card_of_{}_on_the_post_text_box"].format(social_network), first_space = False)

				# Copy Twitter and Facebook card
				self.Text.Copy(social_networks["Twitter, Facebook"]["Card"], verbose = False)

				# Wait for user to finish posting Twitter and Facebook card
				self.Input.Type(self.language_texts["paste_the_second_part_of_the_card_of_{}_on_the_post_text_box"].format(social_network))

			if social_network != social_networks["list"][-1]:
				print()
				print(self.large_bar)

		# Write to post template file
		self.mixed_cards = social_networks["Wattpad"]["Card"] + "\n\n---\n\n" + social_networks["Twitter, Facebook"]["Card"]
		self.File.Edit(self.story["folders"]["Information"]["Post template"], self.mixed_cards, "w")

	def Register_Task(self):
		# Create task dictionary
		self.task_dictionary = {
			"names": {}
		}

		# Add task names
		for language in self.small_languages:
			self.task_dictionary["names"][language] = self.texts["i_published_the_chapter_{}_of_my_story_{}_on_wattpad_and_stake2_website"][language]
			self.task_dictionary["names"][language] = self.task_dictionary["names"][language].format(self.story["chapter_number_names"][language], self.story["Information"]["Titles"][language])

		# Register task with root method
		Stories.Register_Task(self, self.task_dictionary, register_task = True)
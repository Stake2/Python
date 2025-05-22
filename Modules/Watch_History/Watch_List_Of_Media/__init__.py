# Watch_List_Of_Media.py

from Watch_History.Watch_History import Watch_History as Watch_History

from Watch_History.Watch_Media import Watch_Media as Watch_Media

from copy import deepcopy

class Watch_List_Of_Media(Watch_History):
	def __init__(self):
		super().__init__()

		# Define the root dictionary
		self.dictionary = {
			"Files": {
				"Watch list": self.folders["Watch list"]
			},
			"Texts": {
				"Finish selection": "[" + self.Language.language_texts["finish_selection"] + "]"
			},
			"Numbers": {
				"Media list item": 2
			},
			"Option": "",
			"Media types": {},
			"Media title": "",
			"Media list": {
				"Number": 0,
				"List": [],
				"Titles": [],
				"Dictionary": {},
				"File list": False
			},
			"Switches": {
				"Is media item": False
			}
		}

		# Define the media list
		self.Define_Media_List()

		# Open the list of media to watch
		self.Watch_The_Media()

	def Define_Media_List(self):
		# Define a shortcut for the watch list file
		file = self.dictionary["Files"]["Watch list"]

		# If the file exists and is not empty
		if (
			self.File.Exist(file) == True and
			self.File.Contents(file)["lines"] != []
		):
			# Get the dictionary from the watch list
			lines = self.File.Contents(file)["lines"]

			# Iterate through the list of media to watch on the dictionary
			i = 0
			for line in lines.copy():
				# If there is a semicolon and a space on the line
				if "; " in line:
					# If the data dictionary is not present, add it
					if "Data" not in self.dictionary["Media list"]:
						self.dictionary["Media list"]["Data"] = {}

					# Define the split variable
					split = line.split(";") 

					# Get the data as the second item on the split
					data = split[1]

					# Define the key as the current number plus one plus the line (without data)
					key = str(i + 1)

					# Update the line on the list of lines
					lines[i] = split[0]

					# If the media is not inside the root data dictionary, add it
					if key not in self.dictionary["Media list"]["Data"]:
						self.dictionary["Media list"]["Data"][key] = {}

					# Add the media to the dictionary to know from what media this dictionary is
					self.dictionary["Media list"]["Data"][key]["Media"] = lines[i]

					# If there is no comma on the data
					if ", " not in data:
						# Get the re-watching times
						data = data.replace("x", "")

						# Create the re-watching dictionary with the data
						self.dictionary["Media list"]["Data"][key]["Re-watching"] = {
							"Times": int(data)
						}

					# If there is a comma on the data
					if ", " in data:
						# Split the data
						data = data.split(", ")

						# Get the re-watching times
						times = data[0].replace("x", "")

						# Add the re-watching times and media item keys to the media data dictionary
						self.dictionary["Media list"]["Data"][key].update({
							"Re-watching": {
								"Times": int(times)
							},
							"Item": data[1]
						})

				i += 1

			# Define the keys of the media list as the list of lines
			self.dictionary["Media list"]["List"] = lines

			# Change the "File list" switch to True
			self.dictionary["Media list"]["File list"] = True

		# Define the media number variable
		media_number = 0

		# While the option is not the finish selection text
		# And the media title is not the last one
		while (
			self.dictionary["Option"] != self.dictionary["Texts"]["Finish selection"] and
			self.dictionary["Media title"] != self.dictionary["Media list"]["List"][-1]
		):
			# If the media list came from a file
			# And the "media_number" variable is lesser than the number of media titles
			if (
				self.dictionary["Media list"]["File list"] == True and
				media_number < len(self.dictionary["Media list"]["List"])
			):
				# Define the current media title as the media title inside the media list
				self.dictionary["Media title"] = self.dictionary["Media list"]["List"][media_number]

			# Define the media dictionary
			dictionary = self.Select_The_Media(media_number)

			# If the selected option is not inside the media list
			if self.dictionary["Option"] not in self.dictionary["Media list"]["List"]:
				# Define the media list item number as 2
				self.dictionary["Numbers"]["Media list item"] = 2

			# If the selected option is the finish selection text
			if self.dictionary["Option"] == self.dictionary["Texts"]["Finish selection"]:
				# Show a space separator
				print()

			# If the local media dictionary is not None
			# And the media list did not come from a file
			if (
				dictionary != None and
				self.dictionary["Media list"]["File list"] == False
			):
				# Show the "current media list" text
				print(self.language_texts["current_media_list"] + ":")

				# Show the current media list using the method
				self.Show_Media_List()

			# Add one to the media number
			media_number += 1

		# Update the list of titles
		self.dictionary["Media list"]["List"] = list(self.dictionary["Media list"]["Dictionary"].keys())

	def Select_The_Media(self, media_number):
		# Define the root dictionary
		dictionary = {
			"Media": {},
			"Media is defined": False,
			"Watch list of media": True
		}

		# If the media list did not come from a file
		if self.dictionary["Media list"]["File list"] == False:
			# Ask the user to select a media type, returning its dictionary
			media_type = self.Select_Media_Type()

			# Get the key
			key = media_type["Plural"]["en"]

			# If the key is not inside the dictionary, add it
			if key not in self.dictionary["Media types"]:
				self.dictionary["Media types"][key] = media_type

		# If the media list came from a file
		if self.dictionary["Media list"]["File list"] == True:
			# Iterate through the list of English plural media types
			i = 0
			for key in self.media_types["Plural"]["en"]:
				# If the key is not inside the dictionary, add it
				if key not in self.dictionary["Media types"]:
					# Get the media type dictionary
					media_type = self.Select_Media_Type(options = {"number": i})

					# Add it to the dictionary
					self.dictionary["Media types"][key] = media_type

				# Add one to the "i" variable
				i += 1

		# Iterate through the list of media type dictionaries
		for media_type in self.dictionary["Media types"].values():
			# Get the list of media for the current media type
			media_list = self.Get_Media_List(media_type)

			# If the media list is not empty (there is media titles inside it)
			if self.dictionary["Media list"]["List"] != []:
				# Add the finish selection text to the end of the local media list
				media_list.append(self.dictionary["Texts"]["Finish selection"])

			# Define the local dictionary
			dictionary.update({
				"Media type": media_type,
				"Media": {
					"select": True,
					"list": {}
				}
			})

			# If the media list did not come from a file
			if self.dictionary["Media list"]["File list"] == False:
				# Update the media list of the media type dictionary with the local one
				dictionary["Media type"]["Media list"] = media_list

			# If the media list came from a file
			if self.dictionary["Media list"]["File list"] == True:
				# If the selected media title is inside the local media list
				if self.dictionary["Media title"] in media_list:
					# Define the media title to be selected
					dictionary["Media"]["Title"] = self.dictionary["Media title"]

				# If the selected media title is not inside the local media list
				if self.dictionary["Media title"] not in media_list:
					# Define it as empty to ignore it
					dictionary["Media"]["Title"] = ""

			# If the media title is not empty
			if dictionary["Media"]["Title"] != "":
				# Get the new dictionary of the current media
				new_dictionary = self.Select_Media(deepcopy(dictionary))

				# Update the local dictionary with the returned media dictionary above
				dictionary.update(deepcopy(new_dictionary))

			# If the media title is not inside the defined list
			# Empty, finish selection text
			if dictionary["Media"]["Title"] not in ["", self.dictionary["Texts"]["Finish selection"]]:
				# Define a local key
				key = str(media_number + 1)

				# Define the title addon
				addon = ""

				# Switch the "Is media item" switch to False
				self.dictionary["Switches"]["Has media item"] = False

				# If the media has an item list
				# And the media item is not the media
				if (
					new_dictionary["Media"]["States"]["Media item list"] == True and
					new_dictionary["Media"]["States"]["Media item is media"] == False
				):
					# Switch the "Is media item" switch to True
					self.dictionary["Switches"]["Has media item"] = True

				# If the "Data" key is inside the media list dictionary
				# And the media title key is present in the dictionary
				if (
					"Data" in self.dictionary["Media list"] and
					key in self.dictionary["Media list"]["Data"]
				):
					# Get the data dictionary for the current media
					data = self.dictionary["Media list"]["Data"][key]

					# If the "Item" key is inside the data dictionary
					if "Item" in data:
						# Update the local dictionary with the defined item inside the "Data" dictionary
						new_dictionary = self.Define_Media_Item(new_dictionary, media_item = data["Item"])

						# Switch the "Is media item" switch to True
						self.dictionary["Switches"]["Has media item"] = True

					# If the "Re-watching" key is inside the data dictionary
					if "Re-watching" in data:
						# Add the data re-watching dictionary to the new dictionary
						new_dictionary["Re-watching"] = data["Re-watching"]

						# Create the title addon
						addon = " (" + self.language_texts["re_watched, capitalize()"] + " " + str(data["Re-watching"]["Times"]) + "x)"

				# Define more details and variables for the media using the "Watch_Media" sub-class
				new_dictionary = Watch_Media(new_dictionary, run_as_module = True, open_media = False).dictionary

				# Update the local dictionary with the returned media dictionary above
				dictionary.update(deepcopy(new_dictionary))

				# Show a five dash space separator
				print()
				print(self.separators["5"])

				# Show the singular media type in the user language
				print()
				print(dictionary["Media type"]["Singular"][self.user_language] + ":")

				# Define the "Include media title" variable as the "Has media item" switch
				include_media_title = self.dictionary["Switches"]["Has media item"]

				# Show the media title
				self.Show_Media_Title(dictionary, include_media_title = include_media_title)

				# Show the title text
				print()
				print(self.Language.language_texts["title, title()"] + ":")

				# Define the title to the media item title with the media title
				title = dictionary["Media"]["Episode"]["with_title_default"]

				# Add the title addon
				title += addon

				# Show the title
				print("\t" + title)

				# Define the media title key and list the media list keys
				key = dictionary["Media"]["Title"]
				keys = list(self.dictionary["Media list"]["Dictionary"].keys())

				# If the media title is not inside the media list
				if dictionary["Media"]["Title"] not in self.dictionary["Media list"]["List"]:
					# Define the media list item number as 2
					self.dictionary["Numbers"]["Media list item"] = 2

				# If the media title is inside the media list
				if dictionary["Media"]["Title"] in self.dictionary["Media list"]["Dictionary"]:
					# If the "[Media title]" + " (2x)" text is already inside the list of keys of the media list
					if dictionary["Media"]["Title"] + " (2x)" in keys:
						# Add one to the media list item number
						self.dictionary["Numbers"]["Media list item"] += 1

					# Define the key as the media title plus the " ([Media item list number]x)" text
					key = dictionary["Media"]["Title"] + " (" + str(self.dictionary["Numbers"]["Media list item"]) + "x)"

				# Add the media dictionary to the root media list dictionary, with the correct key defined above
				self.dictionary["Media list"]["Dictionary"][key] = new_dictionary

				# Add the title to the list of media titles
				self.dictionary["Media list"]["Titles"].append(title)

				# Turn the "Media is defined" switch to True
				dictionary["Media is defined"] = True

		# Update the root "Option" key
		self.dictionary["Option"] = dictionary["Media"]["Title"]

		# If the "Media is defined" switch is True
		if dictionary["Media is defined"] == True:
			# Return the local dictionary
			return dictionary

	def Watch_The_Media(self):
		# Show a ten dash space separator
		print()
		print(self.separators["10"])

		# Show the text about starting to watch the list of media
		print()
		print(self.language_texts["starting_to_watch_the_list_of_media"] + "...")

		# Get the number of media in the list
		self.dictionary["Media list"]["Number"] = len(self.dictionary["Media list"]["List"])

		# Define the media item number
		media_item_number = 1

		# List the keys
		keys = list(self.dictionary["Media list"]["Dictionary"].keys())

		# Iterate through the media titles inside the media list
		for media_title in keys:
			# Get the media dictionary
			media_dictionary = self.dictionary["Media list"]["Dictionary"][media_title]

			# Get the episode title
			episode_title = self.dictionary["Media list"]["Titles"][media_item_number - 1]

			# If the media title is not the first one
			if media_item_number != 1:
				# Show a three dash space separator
				print()
				print(self.separators["3"])

			# Show the number of the current media and the total number of medias to watch
			print()
			print(self.Language.language_texts["number, title()"] + ":")
			print("\t" + str(media_item_number) + "/" + str(self.dictionary["Media list"]["Number"]))

			# Show the "List of media to watch" text
			print()
			print(self.language_texts["list_of_media_to_watch"] + ":")

			# Show the media list using the method, showing the current media title as "Watching"
			self.Show_Media_List(episode_title, media_item_number)

			# Define a local key
			key = str(media_item_number)

			# If the "Data" key is inside the media list dictionary
			# And the media title key is present in the dictionary
			if (
				"Data" in self.dictionary["Media list"] and
				key in self.dictionary["Media list"]["Data"]
			):
				# Get the data dictionary for the current media
				data = self.dictionary["Media list"]["Data"][key]

				# If the "Item" key is inside the data dictionary
				if "Item" in data:
					# Update the local dictionary with the defined item inside the "Data" dictionary
					media_dictionary = self.Define_Media_Item(media_dictionary, media_item = data["Item"])

			# Watch the media using the "Watch_Media" sub-class
			Watch_Media(media_dictionary)

			# If the key is not the last one
			if media_title != keys[-1]:
				# Ask for user input before continuing
				text = self.Language.language_texts["continue, title()"]

				self.Input.Type(text)

			# Add one to the media item number
			media_item_number += 1

		# Show a five dash space separator
		print()
		print(self.separators["5"])
		print()

		# Show the text telling the user that they finished watching their media list
		print(self.language_texts["you_finished_watching_your_list_of_media"] + ".")
		print()

		# Show the list of watched media
		print(self.language_texts["list_of_watched_media"] + ":")

		# Show the media list using the method
		self.Show_Media_List()

		# Show a five dash space separator
		print()
		print(self.separators["5"])

	def Show_Media_List(self, media_title = None, media_item_number = None):
		# Define the local number
		number = 1

		# Iterate through the media titles inside the media list
		for title in self.dictionary["Media list"]["Titles"]:
			# Define the text as the number as a string
			text = str(number)

			# If the current title is the parameter media title, add the "Watching" text
			if title == media_title:
				text += " (" + self.language_texts["watching, title()"] + ")"

			# If the parameter media title is not None
			# And the number of media in the media list is greater than the local number
			# And the current title is not the parameter media title
			if (
				media_title != None and
				number <= media_item_number and
				title != media_title
			):
				# Add the "Watched" text to the full text
				text += " (" + self.language_texts["watched, title()"] + ")"

			# Add a colon and the media title to the full text
			text += ": " + title

			# Show the full text
			print("\t" + text)

			# Add one to the local number
			number += 1
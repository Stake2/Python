# Create_Year_Summary.py

# Import the root class
from Years.Years import Years as Years

# Import some useful modules
import importlib
from copy import deepcopy

class Create_Year_Summary(Years):
	def __init__(self):
		# Run the root class to import its methods and variables
		super().__init__()

		# Define the root "summary" dictionary
		self.summary = {
			"Year": {},
			"Date": {},
			"Allowed days": [
				29,
				30,
				31
			],
			"Texts": {},
			"Files": {},
			"States": {
				"Is summary date": False
			},
			"Websites": {}
		}

		# Import the "Date" and "Websites" keys from the root "Summary" dictionary
		for key in ["Date", "Websites"]:
			self.summary[key] = self.years["Summary"][key]

		# ---------- #

		# Check if the current year has a year summary
		self.Check_The_Year()

		# Check if today is an allowed day to create the year summary
		self.Check_The_Day()

		# If it is
		if self.summary["States"]["Is summary date"] == True:
			# Collect the year data
			self.Collect_Year_Data()

			# Create the year summary texts
			self.Create_Year_Summary_Texts()

			# Write the year summary to the summary files
			self.Write_Year_Summary_To_Files()

			# Show information about the year summary
			self.Show_Year_Summary_Information()

	def Check_The_Year(self):
		# Define the summary "Years" dictionary
		self.summary["Years"] = {
			"Numbers": {
				"Total": 0
			},
			"List": self.years["List"],
			"Dictionary": {}
		}

		# Iterate through the year numbers and dictionaries inside the root "Years" dictionary
		for year_number, year in self.years["Dictionary"].items():
			# Get the "Files" dictionary in the user language
			files = year["Files"][self.language["Small"]]

			# If the "Summary.txt" file exists
			# And the summary file is not empty
			if (
				"Summary" in files and
				self.File.Contents(files["Summary"])["Lines"] != []
			):
				# Remove the year from the list of years it already has a year summary
				self.summary["Years"]["List"].remove(year_number)

		# If the list of years is empty
		# That means the user already created a year summary for the current year
		if self.summary["Years"]["List"] == []:
			# Show a ten dash space separator
			print()
			print(self.separators["10"])
			print()

			# Show the "You already created the year summary for this year" text in the user language
			print(self.language_texts["you_already_created_the_year_summary_for_this_year"] + ":")
			print(self.years["Current year"]["Number"])

			# Exit the program execution
			quit()

		# If the list of years is not empty
		if self.summary["Years"]["List"] != []:
			# Define the summary "Year" dictionary as the current year dictionary
			self.summary["Year"] = self.years["Dictionary"][self.current_year_number]

	def Check_The_Day(self):
		# If the current day is in the list of allowed days to create the year summary
		# Or the "Testing" switch is True
		if (
			self.date["Units"]["Day"] in self.summary["Allowed days"] or
			self.switches["Testing"] == True
		):
			# Then the current date is the summary date
			self.summary["States"]["Is summary date"] = True

		# If the summary date is not today
		if self.summary["States"]["Is summary date"] == False:
			# Define the list of dates
			dates = [
				"Today"
			]

			# Extend it with the list of allowed days
			dates.extend(self.summary["Allowed days"])

			# Iterate through the list of dates
			for date in dates:
				# If the date is "Today"
				if date == "Today":
					# Define the date dictionary as the today date
					date_dictionary = self.date

				# If the date is not "Today"
				if date != "Today":
					# Define the date string as December and format it with the day and year
					date_string = "{}/12/{}".format(date, self.date["Units"]["Year"])

					# Create the date dictionary from the date string and format
					date_dictionary = self.Date.From_String(date_string, format = "%d/%m/%Y")

				# Define the date format to use
				date_format = "[Day] [Month name] [Year], [Day name]"

				# Get the current date text in the defined date format
				date_text = date_dictionary["Formats"][date_format][self.language["Small"]]

				# Add the date text to the root summary "Texts" dictionary
				self.summary["Texts"][date] = date_text

			# ---------- #

			# Show a ten dash space separator
			print()
			print(self.separators["10"])
			print()

			# Show the "Executing the year summary creator" text in the user language
			print(self.language_texts["executing_the_year_summary_creator"] + "...")
			print()

			# ---------- #

			# Show the date of today
			print(self.Language.language_texts["today_is"] + ":")
			print("\t" + self.summary["Texts"]["Today"])
			print()

			# ---------- #

			# Show the information text which says today is not an allowed day to create the year summary
			text = self.language_texts["today_is_not_an_allowed_day_to_create, type: explanation"]

			print(text + ".")
			print()

			# ---------- #

			# Show the "You can create the year summary on these days" text in the user language
			print(self.language_texts["you_can_create_the_year_summary_on_these_days"] + ":")

			# Iterate through the days inside the list of allowed days
			for day in self.summary["Allowed days"]:
				# Get the date text of the day
				date_text = self.summary["Texts"][day]

				# Show the date text
				print("\t" + date_text)

	def Collect_Year_Data(self):
		# Show a ten dash space separator
		print()
		print(self.separators["10"])

		# Iterate through the list of small languages,
		# to define the language year summary files inside the summary "Files"
		for language in self.languages["Small"]:
			self.summary["Files"][language] = self.years["Current year"]["Files"][language]["Summary"]

		# Update the root "date" dictionary
		self.date = self.Date.Now()

		# Define the text to write as that date in the user timezone format
		text_to_write = self.date["Timezone"]["DateTime"]["Formats"]["HH:MM DD/MM/YYYY"]

		# Write the text to the "Edited in.txt" file
		self.File.Edit(self.years["Current year"]["Files"]["Edited in"], text_to_write, "w")

		# ---------- #

		# Define the summary "Header" with the "Author" key
		self.summary["Header"] = {
			"Author": self.years["Author"]
		}

		# ---------- #

		# Define the created and edited in texts inside the summary "Header" dictionary
		keys = [
			"Created",
			"Edited"
		]

		# Iterate through the keys
		for key in keys:
			key += " in"

			# Get the contents of the file
			contents = self.File.Contents(self.years["Current year"]["Files"][key])

			# Add the first line to the "Header" dictionary
			self.summary["Header"][key] = contents["Lines"][0]

		# Create the summary "Numbers" dictionary
		self.summary["Numbers"] = {
			"Things done in the year": 0
		}

		# ---------- #

		# Create the summary "Histories" dictionary
		self.summary["Histories"] = {}

		# Define the classes to be imported
		classes = [
			"Tasks",
			"GamePlayer",
			"Watch_History",
			"Friends"
		]

		# Iterate through the list of classes
		for class_title in classes:
			# Import the module of the class
			module = importlib.import_module("." + class_title, class_title)

			# Get the object of the module
			object = getattr(module, class_title)

			# Run the class object to define its variable
			object = object()

			# Create the class dictionary
			class_dictionary = {
				"Title": class_title,
				"Object": object,
				"History": {}
			}

			# Add the class "history" dictionary to the "History" key
			class_dictionary["History"] = class_dictionary["Object"].history

			# Create a shortcut to the "History" dictionary
			history = class_dictionary["History"]

			# If the class is not the first one
			if class_title != classes[0]:
				# Show a five dash space separator
				print()
				print(self.separators["5"])

			# Show the current class
			print()
			print(self.Language.language_texts["class_being_executed"] + ":")
			print("\t" + history["Class title"])

			# If the history "Key" is an empty string, define it as the root history key
			if history["Key"] == "":
				history["Key"] = class_title

			# If the current year folder of the history folder, define it as the history folder
			folder = history["Folder"] + self.current_year_number + "/"

			if self.Folder.Exists(folder) == True:
				history["Folder"] = folder

			# ---------- #

			# Define the history "Entries file" key with the "[history key].json" file
			history["Entries file"] = history["Folder"] + history["Key"] + ".json"

			# Read the "Entries" file to get the entries
			history["Entries"] = self.JSON.To_Python(history["Entries file"])

			# Create a shortcut to the entries "Numbers" dictionary
			numbers = history["Entries"]["Numbers"]

			# Iterate through the keys and number keys inside the class history "Numbers" dictionary
			for key, number_key in history["Numbers"].items():
				# If the number key is empty, define it as "Total"
				if number_key == "":
					number_key = "Total"

				# Get the number from the entries "Numbers" dictionary with the number key
				number = numbers[number_key]

				# If the number is a dictionary
				if type(numbers[number_key]) == dict:
					# Get the total number for the current year
					number = number[self.current_year_number]

				# Add the number to the history "Numbers" dictionary
				history["Numbers"][key] = number

			# ---------- #

			# Define the history "Types list" with first item being "Normal"
			history["Types list"] = [
				"Normal"
			]

			# If the "By type" key exists inside the history dictionary
			# Then define the entries by their type
			if "By type" in history:
				# Define the list of types as the English plural types of the class history
				history["Types list"] = history["Types"]["Plural"]["en"]

				# Define the "By type folders" dictionary using the "Types folder" of the class history dictionary
				history["By type folders"] = {
					"root": history["Folder"] + history["Types folder"] + "/"
				}

				# Define the "Entries by type" dictionary
				history["Entries by type"] = {}

				# Iterate through the list of English plural types
				for entry_type in history["Types list"]:
					# Define the local by type folders dictionary with the entry type as a folder
					folders = {
						"root": history["By type folders"]["root"] + entry_type + "/"
					}

					# Define the by type "Entries.json" file
					folders["Entries"] = folders["root"] + "Entries.json"

					# Read the by type "Entries.json" file
					history["Entries by type"][entry_type] = self.JSON.To_Python(folders["Entries"])

					# Add the local folders dictionary to the "By type folders" dictionary
					history["By type folders"][entry_type] = folders

			# ---------- #

			# If the "Dictionary" key exists inside the class history "Entries" dictionary
			# And the class object contains a method called "Define_Year_Summary_Data"
			if (
				"Dictionary" in history["Entries"] and
				hasattr(class_dictionary["Object"], "Define_Year_Summary_Data")
			):
				# Define the class history "Data" dictionary
				history["Data"] = {
					# The maximum number of lines to add to the summary header
					"Number": 5,

					# The empty text dictionary
					"Text": {}
				}

				# Iterate through the list of entry types
				for entry_type in history["Types list"]:
					# Create a shortcut to the the normal root "entries" dictionary
					entries = history["Entries"]

					# If the entry type is not "Normal"
					if entry_type != "Normal":
						# Create a shortcut to the by type "entries" dictionary
						entries = history["Entries by type"][entry_type]

					# Get the entries "Dictionary"
					entries = entries["Dictionary"]

					# Iterate through the list of small languages
					for language in self.languages["Small"]:
						# Define the language dictionary inside the class history data "Text" dictionary
						if language not in history["Data"]["Text"]:
							history["Data"]["Text"][language] = ""

						# Create a local list of entries with the entry dictionaries
						local_entries = list(entries.values())

						# Update the local entries list to be a dictionary containing the number of entries and the list
						local_entries = {
							"Number": len(local_entries),
							"List": local_entries
						}

						# Define the iteration number as the total number of entries
						# Example: 50
						iteration_number = local_entries["Number"]

						# Define the maximum as the class history data "Number"
						# Example: 5
						maximum_number = history["Data"]["Number"]

						# If the iteration number is lesser than the maximum number
						# Example: 3 is lesser than 5
						if iteration_number < maximum_number:
							# Define the iteration number as zero 
							iteration_number = 0

							# Define the maximum number as the total number of entries
							maximum_number = local_entries["Number"]

						# If the iteration number is greater than or equal to the class history data "Number"
						# Example: 30 is greater than or equal to 5 (the data number)
						if iteration_number >= history["Data"]["Number"]:
							# While it is not equal to the total number of entries less the class history data "Number"
							# Example: While 50 is not equal to (50 - 5 = 45)
							# In this example, we are going to get the entries from number 45 to 50
							while iteration_number != (local_entries["Number"] - history["Data"]["Number"]):
								# Remove one from the i number
								iteration_number -= 1

						# If the entry type is not "Normal"
						if entry_type != "Normal":
							# Get the entry type dictionary
							type_dictionary = history["Types"][entry_type]

							# Define the singular entry type
							singular_entry_type = type_dictionary["Singular"]

							# Define the plural entry type
							plural_entry_type = type_dictionary["Plural"]

							# Get the gender from the type dictionary
							gender = type_dictionary["Gender"]

							# If the "Entry type texts" key is inside the history dictionary
							if "Entry type texts" in history:
								# Create a shortcut to the entry type texts dictionary
								shortcut = history["Entry type texts"][plural_entry_type["en"]]

								# Update the singular entry type to be the one inside the "Entry type texts" dictionary
								singular_entry_type = shortcut["Singular"]

								# Update the plural entry type to be the one inside the "Entry type texts" dictionary
								plural_entry_type = shortcut["Plural"]

								# Define the gender as the "masculine" one
								gender = "masculine"

							# Define the local number as the total number of entries
							number = local_entries["Number"]

							# If the number is zero
							if number == 0:
								# Update it to two to use the plural text
								number = 2

							# Define the singular or plural text based on the total number of entries
							text_by_number = self.Text.By_Number(number, singular_entry_type, plural_entry_type)

							# Get the text by number in the user language
							text_by_number = text_by_number[language]

							# Define the type header as the number of local entries plus the language entry type
							entry_type_header = str(local_entries["Number"]) + " " + text_by_number.lower()

							# If the total number of entries is not zero
							if local_entries["Number"] != 0:
								# Get the plural "last" text in the type gender
								last_text = self.Language.texts["last, plural, " + gender][language]

								# Get the number name of the maxmium number
								number_name = self.Date.texts["number_names, type: list"][language][maximum_number]

								# Add the last text and number name inside parentheses and a colon to the entry type header
								entry_type_header += " (" + last_text + " " + number_name + ")" + ":"

							# Add the entry type header to the class history data "Text" in the current language
							history["Data"]["Text"][language] += "\t" + entry_type_header

							# Add a line break
							history["Data"]["Text"][language] += "\n"

						# While the iteration number is not equal to the total number of entries
						while iteration_number != local_entries["Number"]:
							# Get the entry dictionary from the list
							entry = local_entries["List"][iteration_number]

							# Define the entry text using the "Define_Year_Summary_Data" method of the current class
							# This makes possible for classes that have a history to tell the "Years" module how they want their data to be shown on the year summary
							entry_text = class_dictionary["Object"].Define_Year_Summary_Data(entry, language)

							# Define the number key as "Number"
							number_key = "Number"

							# If the class has a number key, use it
							if "Number key" in history:
								number_key = history["Number key"]

							# Add the entry number to the entry text
							entry_text = str(entry[number_key]) + ". " + entry_text

							# Define the tab initially as one tab
							tab = "\t"

							# If the entry type is not "Normal"
							if entry_type != "Normal":
								# Update the tab to be two tabs
								tab = "\t\t"

							# Update the entry text to add the tab and a line break
							entry_text = tab + entry_text + "\n"

							# Add the entry text to the class history data "Text" in the current language
							history["Data"]["Text"][language] += entry_text

							# Add one to the iteration number
							iteration_number += 1

						# If the entry type is not the last one
						if entry_type != history["Types list"][-1]:
							# Add a line break to the class history data "Text" in the current language
							history["Data"]["Text"][language] += "\n"

			# Remove the "Entries" key as it is not needed anymore
			history.pop("Entries")

			# If the "By type" key is inside the class history dictionary
			if "By type" in history:
				# Remove the "Entries by type" key as it is not needed anymore
				history.pop("Entries by type")

			# Add the class history dictionary to the summary "Histories" dictionary
			self.summary["Histories"][class_dictionary["Title"]] = history

		# Iterate through the list of classes
		for class_title in classes:
			# Get the class history dictionary
			class_history = self.summary["Histories"][class_title]

			# Iterate through the numbers inside the class history "Numbers" dictionary
			for number in class_history["Numbers"].values():
				# Add the number to the "Things done in the year" number
				self.summary["Numbers"]["Things done in the year"] += number

		# ---------- #

		# Get the number of memory images from the current year

		# Get the memories "Dates.txt" file
		file = self.years["Current year"]["Files"]["Image"]["Memories"]["Dates"]

		# Get the number of lines
		memories = self.File.Contents(file)["Length"]

		# Add the number of memories to the "Numbers" dictionary
		self.summary["Numbers"]["Memories"] = memories

		# Add that number to the "Things done in the year" number
		self.summary["Numbers"]["Things done in the year"] += memories

		# ---------- #

		# Make a copy of the root year summary "Websites" dictionary
		self.summary["Websites"] = deepcopy(self.years["Summary"]["Websites"])

		# If the total number of summary websites is not zero
		if self.summary["Websites"]["Numbers"]["Total"] != 0:
			# Iterate through the names and websites inside the websites "Dictionary" (of where to post the year summary)
			for name, website in self.summary["Websites"]["Dictionary"].items():
				# Iterate through the keys and links inside the website "Links" dictionary
				for link_key, link in website["Links"].items():
					# Replace the "{current_year}" text template with the current year number
					link = link.replace("{current_year}", self.years["Current year"]["Number"])

					# Update the link inside the website "Links" dictionary
					website["Links"][link_key] = link

				# Update the root website dictionary inside the websites "Dictionary"
				self.summary["Websites"]["Dictionary"][name] = website

	def Create_Year_Summary_Texts(self):
		# Define the summary "Text" dictionary
		self.summary["Text"] = {}

		# Define the list of classes that have detailed texts
		self.summary["Detailed histories"] = [
			"Tasks",
			"Watch_History",
			"GamePlayer"
		]

		# Iterate through list of small languages
		for language in self.languages["Small"]:
			# Define the language summary text initially as an empty string
			self.summary["Text"][language] = ""

			# Define the "Summary of my year of [Current year]" text template
			text_template = self.texts["summary_of_my_year_of_{current_year}"][language]

			# Replace the "{current_year}" text template with the current year number
			text = text_template.replace("{current_year}", self.years["Current year"]["Number"])

			# Add it to the language summary text with two line breaks at the end
			self.summary["Text"][language] += text + "\n\n"

			# ---------- #

			# Iterate through the keys and header texts inside the summary "Header"
			for key, header_text in self.summary["Header"].items():
				# Define the text key for the key
				text_key = key.lower().replace(" ", "_")

				# If the underline is not inside the text key
				if "_" not in text_key:
					# Add the ", title()" text
					text_key += ", title()"

				# Define the texts dictionary to be used as the "texts" dictionary of the "Language" utility class
				texts = self.Language.texts

				# If the text key is inside the "texts" dictionary of this class (Years)
				if text_key in self.texts:
					# Define the texts dictionary as that one
					texts = self.texts

				# Get the key text using the text key and the current language
				text = texts[text_key][language]

				# Add a colon, a space, and the header text to the text
				text += ": " + header_text

				# Add a line break
				text += "\n"

				# If the key is "Author"
				if key == "Author":
					# Add another line break
					text += "\n"

				# Add the text to the root summary "Text" dictionary in the current language
				self.summary["Text"][language] += text

			# Add one line break, a five dash space separator, and two line breaks to the summary "Text" dictionary in the current language
			self.summary["Text"][language] += "\n" + \
			self.separators["5"] + \
			"\n\n"

			# ---------- #

			# Create a shortcut to the current year current language folder
			folder = self.years["Current year"]["Folders"][language]

			# If the "Goodbye" key and file is inside the current language folder
			if "Goodbye" in folder:
				# Create a shortcut to the "Goodbye.txt" file
				file = self.years["Current year"]["Files"][language]["Goodbye"]

				# Get the contents of the file
				contents = self.File.Contents(file)

				# If the file is not empty
				if contents["Lines"] != []:
					# Define the text as the "Goodbye text for the year:" text
					text += self.texts["goodbye_text_for_the_year"][language] + ":" + "\n"
					
					# Add the goodbye text that is inside the file
					text += contents["String"]

					# Add two line breaks, a five dash space separator, and two line breaks
					self.summary["Text"][language] += "\n\n" + \
					self.separators["5"] + \
					"\n\n"

					# Add the text to the summary "Text" dictionary in the current language
					self.summary["Text"][language] += text

			# ---------- #

			# Define the text template as the "Things done in the year of {}" text in the current language
			text_template = self.Language.texts["things_done_in_the_year_of_{}"][language]

			# Format it with the current year number to create the text
			text = text_template.format(self.years["Current year"]["Number"])

			# Add a colon
			text += ": "

			# Add the total number of things done in the current year
			text += str(self.summary["Numbers"]["Things done in the year"])

			# Add the "the sum of numbers below" text in the current language around parentheses
			text += " (" + self.texts["the_sum_of_numbers_below"][language] + ")"

			# Add the text and a line break to the summary "Text" dictionary in the current language
			self.summary["Text"][language] += text + "\n"

			# ---------- #

			# Iterate through the class histories inside the summary "Histories" dictionary
			for class_history in self.summary["Histories"].values():
				# Get the list of the number keys
				number_keys = list(class_history["Numbers"].keys())

				# Iterate through the number keys and numbers inside the class history "Numbers" dictionary
				for number_key, number in class_history["Numbers"].items():
					# Define the text key for the number key
					text_key = number_key.lower().replace(" ", "_")

					# Define the text as the text in the current language using the text key
					text = self.Language.texts[text_key][language]

					# Add a colon and the number
					text += ": " + str(number)

					# Add a line break
					text += "\n"

					# If the number is not zero
					# And the text is not inside the summary text in the current language
					if (
						number != 0 and
						text not in self.summary["Text"][language]
					):
						# Add the text to the summary "Text" dictionary in the current language
						self.summary["Text"][language] += text

			# ---------- #

			# Define the text as the "Memories of the year in images" text in the current language
			text = self.texts["memories_of_the_year_in_images"][language] + ": "

			# Add the number of image memories in the year
			text += str(self.summary["Numbers"]["Memories"])

			# Add two line breaks, a five dash space separator, and two line breaks
			text += "\n\n" + \
			self.separators["5"] + \
			"\n\n"

			# Add the text to the summary "Text" dictionary in the current language
			self.summary["Text"][language] += text

			# ---------- #

			# Get the list of class history keys
			class_histories = list(self.summary["Histories"].keys())

			# Iterate through the list of classes
			for class_title in class_histories:
				# If the class is not inside the list of detailed classes
				if class_title not in self.summary["Detailed histories"]:
					# Remove the class history from the local list of class histories
					class_histories.remove(class_title)

			# ---------- #

			# Iterate through the list of class history keys
			for key in class_histories:
				# Get the class history dictionary
				class_history = self.summary["Histories"][key]

				# Define the keys and values of the class history "Numbers" dictionary
				keys = list(class_history["Numbers"].keys())
				values = list(class_history["Numbers"].values())

				# Define the number key and number as the first key and value
				number_key, number = keys[0], values[0]

				# Get the number of entries
				entries_number = list(class_history["Numbers"].values())[0]

				# Define the text as the total number of entries
				entry_text = str(entries_number) + " "

				# Define the text key
				text_key = number_key.lower().replace(" ", "_")

				# Add the text in the current language to the entry text
				entry_text += self.Language.texts[text_key][language].lower()

				# Create a shortcut to the class history "Data" dictionary
				data = class_history["Data"]

				# If the "By type" key is not inside the class history dictionary
				# Only add the " (last [number])" text if the "By type" mode is not activated on the class history
				if "By type" not in class_history:
					# Define the default gender as the "feminine" one
					gender = "feminine"

					# If the "Gender" key is inside the class history dictionary
					if "Gender" in class_history:
						# Use that gender
						gender = class_history["Gender"]

						# Get the plural "last" text in the type gender
						last_text = self.Language.texts["last, plural, " + gender][language]

						# Get the number name of the maxmium number
						number_name = self.Date.texts["number_names, type: list"][language][data["Number"]]

						# Add the last text and number name inside parentheses and a colon to the entry text
						entry_text += " (" + last_text + " " + number_name + ")" + ":"

				# Add a colon and a line break to the entry text
				entry_text += ":" + "\n"

				# Add the class history data text in the current language
				entry_text += data["Text"][language]

				# If the class history is not the last one, add a line break to the entry text
				if key != class_histories[-1]:
					entry_text += "\n"

				# Add the detailed history text to the summary "Text" dictionary in the current language
				self.summary["Text"][language] += entry_text

			# If the total number of summary websites is not zero
			if self.summary["Websites"]["Numbers"]["Total"] != 0:
				# Add a line break to the summary "Text" dictionary in the current language
				self.summary["Text"][language] += "\n"

				# List the website names where to post the year summary
				website_names = list(self.summary["Websites"]["Dictionary"].keys())

				# Iterate through the list of website names
				for website_name in website_names:
					# Get the website dictionary
					website = self.summary["Websites"]["Dictionary"][website_name]

					# Define the text template as the "Year summary on the {} website" text
					text_template = self.texts["year_summary_on_the_{}_website"][language]

					# Define the text as the text template formatted with the website name
					text = text_template.format(website_name) + ":"

					# Add a line break
					text += "\n"

					# Add the website link in the current language
					text += website["Links"][language]

					# If the website name is not the last one
					if website_name != website_names[-1]:
						# Add two line breaks to the text
						text += "\n\n"

					# Add the text to the summary "Text" dictionary in the current language
					self.summary["Text"][language] += text

		# ---------- #

		# Iterate through list of small languages
		for language_number, language in enumerate(self.languages["Small"]):
			# Get the language text
			language_text = self.summary["Text"][language]

			# Remove the last space if it is present
			if language_text[-1] == "\n":
				language_text = language_text[:-1]

			# Update the text inside the root summary "Text" dictionary
			self.summary["Text"][language] = language_text

	def Write_Year_Summary_To_Files(self):
		# Iterate through the list of small languages
		for language in self.languages["Small"]:
			# Get the language file
			language_file = self.summary["Files"][language]

			# Get the language text
			language_text = self.summary["Text"][language]

			# Write the language text to the language file
			self.File.Edit(language_file, language_text, "w")

	def Show_Year_Summary_Information(self):
		# Show a ten dash space separator
		print()
		print(self.separators["10"])

		# Show the "The year summary of this year was created" text in the user language
		print()
		print(self.language_texts["the_year_summary_of_this_year_was_created"] + ":")
		print("\t" + self.years["Current year"]["Number"])

		# Show the "Year summary in [full user language]" text in the user language
		print()
		print(self.language_texts["year_summary_in"] + " " + self.language["Full"] + ":")

		# Create a shortcut to the year summary text in the user language
		summary_text = self.summary["Text"][self.language["Small"]]

		# Show the year summary text in the user language
		print("[" + summary_text + "]")

		# Create a shortcut to the year summary file in the user language
		summary_file = self.summary["Files"][self.language["Small"]]

		# Open the year summary file
		self.System.Open(summary_file, verbose = False)

		# ---------- #

		# Show a ten dash space separator
		print()
		print(self.separators["10"])

		# Define the text template as the "The program has finished the creation of the year summary for the year of {}" text in the user language
		text_template = self.language_texts["the_program_has_finished_the_creation_of_the_year_summary_for_the_year_of_{}"]

		# Format it with the current year number to create the text
		text = text_template.format(self.years["Current year"]["Number"])

		# Show the information about the creation of the year summary
		print()
		print(text + ".")

		# ---------- #

		# Show a text telling the user to post the year summary on the summary websites
		print()
		print(self.language_texts["post_the_year_summary_on_these_websites"] + ":")

		# If the total number of summary websites is not zero
		if self.summary["Websites"]["Numbers"]["Total"] != 0:
			# Iterate through the names and websites inside the websites "Dictionary" (of where to post the year summary)
			for name, website in self.summary["Websites"]["Dictionary"].items():
				# Show a space
				print()

				# Show the website name with a tab and a colon
				print(name + ":")

				# Show the website link in the user language
				print(website["Links"][self.language["Small"]])
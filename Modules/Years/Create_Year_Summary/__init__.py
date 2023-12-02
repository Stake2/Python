# Create_Year_Summary.py

from Years.Years import Years as Years

# Import the "importlib" module
import importlib

class Create_Year_Summary(Years):
	def __init__(self):
		super().__init__(select_year = False)

		# Define the Summary dictionary
		self.summary = {
			"Texts": {},
			"Files": {},
			"States": {
				"Is summary date": False
			},
			"Date": self.years["Summary"]["Date"]
		}

		# Define the year
		self.Define_The_Year()

		if self.switches["testing"] == True:
			self.summary["States"]["Is summary date"] = True

		if self.year != None:
			self.Check_Day()

			if self.summary["States"]["Is summary date"] == True:
				self.Define_Summary_Files()
				self.Define_Year_Data()
				self.Define_Summary_Text()
				self.Write_Summary_To_Files()
				self.Show_Summary_Information()

	def Define_The_Year(self):
		# Define the "Years" dictionary
		self.summary["Years"] = {
			"Numbers": {
				"Total": 0
			},
			"List": self.years["List"],
			"Dictionary": {}
		}

		# Itearate through the years' list
		for year in self.years["List"]:
			self.year = self.years["Dictionary"][year]

			# Get the English files dictionary
			files = self.year["Files"][self.user_language]

			# If the "Summary" file in English exists
			# And the summary file is not empty
			if (
				"Summary" in files and
				self.File.Contents(files["Summary"])["lines"] != []
			):
				# Remove the year from the years' list
				# Because its summary file is already created and filled
				self.summary["Years"]["List"].remove(year)

		# If the years' list is empty
		# That means the user already created a summary for the current year
		# And show that information to the user
		if self.summary["Years"]["List"] == []:
			print()
			print("--------------------")
			print()
			print(self.language_texts["you_already_created_the_summary_for_this_year"] + ":")
			print(self.years["Current year"]["Number"])
			print()
			print("--------------------")

		# Define the local Year dictoinary as None
		self.year = None

		# If the years' list is not empty
		if self.summary["Years"]["List"] != []:
			# Define the local Year dictionary as the only year inside the years' list (the current year)
			current_year = self.years["Current year"]["Number"]

			self.year = self.years["Dictionary"][current_year]

	def Check_Day(self):
		# If the current day and month is the same as the summary day and month
		if (
			self.date["Units"]["Day"] == self.summary["Date"]["Units"]["Day"] and
			self.date["Units"]["Month"] == self.summary["Date"]["Units"]["Month"]
		):
			# Then the current date is the summary date
			self.summary["States"]["Is summary date"] = True

		# If the summary date is not today
		if self.summary["States"]["Is summary date"] == False:
			# Define the date template text of the summary date
			template = self.Date.language_texts["{} {} {}"]

			# Iterate through the date types
			for item in ["Summary", "Today"]:
				date = self.summary["Date"]

				if item == "Today":
					date = self.date

				# Define the list of items
				items = [
					date["Units"]["Day"], # Day number
					date["Timezone"]["DateTime"]["Texts"]["Month name"][self.user_language], # Month name in the user language
					self.years["Current year"]["Number"] # Current year number
				]

				# Format the template
				self.summary["Texts"][item] = template.format(*items)

			print()
			print("--------------------")
			print()
			print(self.language_texts["executing_the_year_summary_creator"] + "...")
			print()

			# Show the information and summary date
			template = self.language_texts["today_is_not_{}_run_this_program_again_when_it_is"]

			text = template.format(self.summary["Texts"]["Summary"])

			print(text + ".")
			print()

			# Show the date of today
			print(self.JSON.Language.language_texts["today_is"] + ":")
			print(self.summary["Texts"]["Today"])
			print()
			print("--------------------")

	def Define_Summary_Files(self):
		for language in self.languages["small"]:
			self.summary["Files"][language] = self.years["Current year"]["Files"][language]["Summary"]

	def Define_Year_Data(self):
		# Update the "Edited in" date to now
		self.date = self.Date.Now()

		text_to_write = self.date["Timezone"]["DateTime"]["Formats"]["HH:MM DD/MM/YYYY"]

		self.File.Edit(self.year["Files"]["Edited in"], text_to_write, "w")

		# Define the summary header keys
		self.summary["Header"] = {
			"Author": self.years["Author"]
		}

		# Define the created and edited in texts on the summary header
		keys = [
			"Created",
			"Edited"
		]

		for key in keys:
			key += " in"

			contents = self.File.Contents(self.year["Files"][key])

			self.summary["Header"][key] = contents["lines"][0]

		# Define the classes to be imported
		classes = [
			"Tasks",
			"GamePlayer",
			"Watch_History",
			"Friends"
		]

		# Import them
		for title in classes:
			# Import the module
			module = importlib.import_module("." + title, title)

			# Get the sub-class
			sub_class = getattr(module, title)

			# Add the sub-class to the current module
			setattr(self, title, sub_class())

		# Create the Summary Numbers dictionary
		self.summary["Numbers"] = {
			"Things done": 0
		}

		# Create the Summary Histories dictionary
		self.summary["Histories"] = {}

		current_year = str(self.years["Current year"]["Number"])

		# Iterate through the classes list
		for key in classes:
			class_object = getattr(self, key)

			# Define the local "History" dictionary as the module "History" dictionary
			history = class_object.history

			# Define the class name
			history["Class"] = key

			# Define the class object
			history["Class object"] = class_object

			# If the history key is empty, define it as the root history key
			if history["Key"] == "":
				history["Key"] = key

			# If the year folder exists, define it as the history folder
			folder = history["Folder"] + current_year + "/"

			if self.Folder.Exist(folder) == True:
				history["Folder"] = folder

			# Define the History entries file
			history["Entries file"] = history["Folder"] + history["Key"] + ".json"

			# Read the Entries file
			history["Entries"] = self.JSON.To_Python(history["Entries file"])

			# Define the Entries numbers variable for easier typing
			numbers = history["Entries"]["Numbers"]

			# Iterate through the classes numbers
			for key, number_key in history["Numbers"].items():
				# If the number key is empty, define it as "Total"
				if number_key == "":
					number_key = "Total"

				# Get the number from the Entries file
				number = numbers[number_key]

				# If the number is a dictionary
				if type(numbers[number_key]) == dict:
					# Get the number by year
					number = number[current_year]

				# Add the number to the summary numbers dictionary
				history["Numbers"][key] = number

			# Define the types list
			history["Types list"] = [
				"Normal"
			]

			# Define Entries per type if they exists
			if "Per type" in history:
				# Define the types list as the English plural types of the class
				history["Types list"] = history["Types"]["Plural"]["en"]

				# Define the per type folders
				history["Per type folders"] = {
					"root": history["Folder"] + history["Types folder"] + "/"
				}

				# Define the per type Entries dictionary
				history["Entries per type"] = {}

				# Iterate through the English plural types list
				for entry_type in history["Types list"]:
					# Define the local folders dictionary
					folders = {
						"root": history["Per type folders"]["root"] + entry_type + "/"
					}

					# Define the "Entries.json" file
					folders["Entries"] = folders["root"] + "Entries.json"

					# Read the per type "Entries.json" file
					history["Entries per type"][entry_type] = self.JSON.To_Python(folders["Entries"])

					# Add the local folders dictionary to the per type folders dictionary
					history["Per type folders"][entry_type] = folders

			if (
				"Dictionary" in history["Entries"] and
				hasattr(history["Class object"], "Define_Year_Summary_Data")
			):
				# Define the History Data dictionary
				history["Data"] = {
					"Number": 5,
					"Text": {}
				}

				# Iterate through the entry types list
				for entry_type in history["Types list"]:
					# Define the normal Entries root dictionary
					entries = history["Entries"]

					# Define the Entries root dictionary per type if the entry type is not empty
					if entry_type != "Normal":
						entries = history["Entries per type"][entry_type]

					# Get the Entries dictionary
					entries = entries["Dictionary"]

					for language in self.languages["small"]:
						# Define the empty language text key if it does not exist
						if language not in history["Data"]["Text"]:
							history["Data"]["Text"][language] = ""

						# Define the language entry type if the entry type is not "Normal"
						if entry_type != "Normal":
							type_dictionary = history["Types"][entry_type]

							language_entry_type = type_dictionary["Plural"][language]

							# Add the language entry type to the text variable
							history["Data"]["Text"][language] += "\t" + language_entry_type

						# Define the entries list
						local_entries = list(entries.values())

						# Define the Entries dictionary with the entries number and list
						local_entries = {
							"Number": len(local_entries),
							"List": local_entries
						}

						# Define the i and last number numbers
						i = local_entries["Number"]

						last_number = history["Data"]["Number"]

						# If the i number is lesser than the data number
						if i < history["Data"]["Number"]:
							# Define the i number as zero (0)
							i = 0

							last_number = local_entries["Number"]

						# If the i number is greater than or equal to the data number
						if i >= history["Data"]["Number"]:
							# While it is not equal to the entries number less the data number
							while i != local_entries["Number"] - history["Data"]["Number"]:
								# Remove one from the i number
								i -= 1

						# If the entry type is not "Normal"
						if entry_type != "Normal":
							# Add the "last [number]" text
							gender = type_dictionary["Gender"]

							history["Data"]["Text"][language] += " (" + self.JSON.Language.texts["last, plural, " + gender][language] + " " + self.Date.texts["number_names, type: list"][language][last_number] + ")"

							# Add a colon and line break
							history["Data"]["Text"][language] += ":" + "\n"

						number = 1
						# While the i variable is not equal to the entries number
						while i != local_entries["Number"]:
							entry = local_entries["List"][i]

							# Define the entry text using the method of the current class
							# This makes possible for classes that have a History to tell the "Years" module how they want their data to be shown on the year summary
							entry_text = history["Class object"].Define_Year_Summary_Data(entry, language)

							entry_number = str(entry["Number"])

							# Add the item number to the entry text
							entry = entry_number + ". " + entry_text

							# Define the tab variable
							tab = "\t"

							# Define the tab variable as two tabs if the entry type is not "Normal"
							if entry_type != "Normal":
								tab = "\t\t"

							# Define the text
							history["Data"]["Text"][language] += tab + entry + "\n"

							number += 1
							i += 1

						if entry_type != history["Types list"][-1]:
							history["Data"]["Text"][language] += "\n"

			# Remove the "Entries" key as it is not needed anymore
			history.pop("Entries")

			if "Per type" in history:
				# Remove the "Entries per type" key per type as they is not needed anymore
				history.pop("Entries per type")

			# Add the History dictionary to the Summary dictionary
			self.summary["Histories"][history["Class"]] = history

		# Add all History numbers to the "Things done" number
		for history in self.summary["Histories"].values():
			for number in history["Numbers"].values():
				self.summary["Numbers"]["Things done"] += number

	def Define_Summary_Text(self):
		# Define the summary Text dictionary
		self.summary["Text"] = {}

		# Define the classes that have detailed texts
		self.summary["Detailed classes"] = [
			"Tasks",
			"Watch_History",
			"GamePlayer"
		]

		# Iterate through the small languages list
		for language in self.languages["small"]:
			# Define the language summary text
			self.summary["Text"][language] = ""

			# Add the header texts
			for key in self.summary["Header"]:
				text_key = key.lower().replace(" ", "_")

				if "_" not in text_key:
					text_key += ", title()"

				# Define the texts dictionary to be used
				texts = self.JSON.Language.texts

				if text_key in self.texts:
					texts = self.texts

				# Add the header text to the language summary text
				self.summary["Text"][language] += texts[text_key][language] + ": " + self.summary["Header"][key]

				# Add a line break
				self.summary["Text"][language] += "\n"

			# Add a separator
			self.summary["Text"][language] += "\n" + "-----" + "\n\n"

			# Add the "This Year I" text if it exists and is not empty
			folder = self.year["Folders"][language]

			if "This Year I" in folder:
				file = self.year["Files"][language]["This Year I"]

				contents = self.File.Contents(file)

				if contents["lines"] != []:
					# Add the "This Year I" text
					self.summary["Text"][language] += contents["string"]

					# Add a separator
					self.summary["Text"][language] += "\n\n" + "-----" + "\n\n"

			# Add the "Things done in {year}" text
			text = self.JSON.Language.texts["things_done_in"][language] + " " + str(self.years["Current year"]["Number"]) + ": "

			text += str(self.summary["Numbers"]["Things done"])

			text += " (" + self.texts["the_sum_of_numbers_below"][language] + ")"

			self.summary["Text"][language] += text + "\n"

			# Iterate through the Histories dictionary
			for key, history in self.summary["Histories"].items():
				number_keys = list(history["Numbers"].keys())

				# Iterate through the History Numbers dictionary
				for number_key, number in history["Numbers"].items():
					# Define the text key
					text_key = number_key.lower().replace(" ", "_")

					# Define the text with the number
					text = self.JSON.Language.texts[text_key][language] + ": " + str(number)

					# Add a line break to the text
					text += "\n"

					# If the number is not zero
					if number != 0:
						# Add the text to the language summary text
						self.summary["Text"][language] += text

			# Add a separator
			self.summary["Text"][language] += "\n" + "-----" + "\n\n"

			# Get the Histories list
			histories = list(self.summary["Histories"].keys())

			# Iterate through the Histories dictionary
			for key, history in self.summary["Histories"].items():
				# If the History Class is not inside the detailed classes list
				if history["Class"] not in self.summary["Detailed classes"]:
					# Remove the History from the local Histories list
					histories.remove(key)

			# Iterate through the Histories dictionary
			for key in histories:
				# Define the local History dictionary
				history = self.summary["Histories"][key]

				# If the History Class is inside the detailed classes list
				if history["Class"] in self.summary["Detailed classes"]:
					# Define the History Numbers variable for easier typing
					numbers = history["Numbers"]

					# Define the keys and values
					keys = list(numbers.keys())
					values = list(numbers.values())

					# Get the first number key and number
					number_key, number = keys[0], values[0]

					# Define the text key
					text_key = number_key.lower().replace(" ", "_")

					# Define the number text
					text = self.JSON.Language.texts[text_key][language]

					# Define the History Data variable for easier typing
					data = history["Data"]

					# Only add the " (last [number])" text if the "per type" mode is not activated on the History
					if "Per type" not in history:
						gender = "feminine"

						if "Gender" in history:
							gender = history["Gender"]

						text += " (" + self.JSON.Language.texts["last, plural, " + gender][language] + " " + self.Date.texts["number_names, type: list"][language][data["Number"]] + ")"

					# Add a colon and a line break
					text += ":" + "\n"

					# Add the History Data text
					text += data["Text"][language]

					# Add a line break if the History is not the last one
					if history["Class"] != histories[-1]:
						text += "\n"

					# Add the detailed History text to the language summary text
					self.summary["Text"][language] += text

		# Iterate through the small languages list
		for language in self.languages["small"]:
			# Remove the last space if it exists
			if self.summary["Text"][language][-1] == "\n":
				self.summary["Text"][language] = self.summary["Text"][language][:-1]

	def Write_Summary_To_Files(self):
		for language in self.languages["small"]:
			text = self.summary["Text"][language]

			self.File.Edit(self.summary["Files"][language], text, "w")

	def Show_Summary_Information(self):
		# Show a separator
		print()
		print(self.large_bar)
		print()

		# Show the year in which its summary was created
		print(self.language_texts["the_summary_of_this_year_was_created"] + ":")
		print("\t" + self.year["Number"])

		# Define the type text
		type_text = self.language_texts["show_year_summary"] + "? (" + self.JSON.Language.language_texts["can_be_long, masculine"] + ")"

		# Ask the user if the program should show the summary text (can be long)
		self.summary["States"]["Show"] = self.Input.Yes_Or_No(type_text)

		# Show the summary text if the user wants to see it
		if self.summary["States"]["Show"] == True:
			# Show the summary text in the user language
			print()
			print(self.large_bar)
			print()
			print(self.JSON.Language.language_texts["summary_in"] + " " + self.languages["full"][self.user_language] + ":")
			print("\t" + "[")

			for line in self.summary["Text"][self.user_language].splitlines():
				print("\t\t" + line)

			print("\t" + "]")

		# Open the user language summary file
		self.System.Open(self.summary["Files"][self.user_language])

		# Show the information about the ending of the program
		print()
		print(self.language_texts["the_program_has_finished_the_creation_of_the_year_summary_for"] + " " + self.year["Number"] + ".")

		# Show a separator
		print()
		print(self.large_bar)
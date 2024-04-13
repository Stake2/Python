# Create_Survival_Diary_File.py

from Project_Zomboid.Project_Zomboid import Project_Zomboid as Project_Zomboid

from copy import deepcopy

class Create_Survival_Diary_File(Project_Zomboid):
	def __init__(self):
		super().__init__()

		# Define the root dictionary
		self.dictionary = {
			"Cities": {},
			"Survivors": {},
			"City": {},
			"Survivor": {}
		}

		# Define the "States" dictionary
		self.states = {
			"Used pre-defined values": False
		}

		# Select the city
		self.Select_A_City()

		# Select the survivor
		self.Select_A_Survivor()

		# If the pre-defined city and survivor were present
		if (
			self.project_zomboid["Pre-defined values"]["City"] != "" and
			self.project_zomboid["Pre-defined values"]["Character"] != ""
		):
			# Define the "Used pre-defined values" state as True
			self.states["Used pre-defined values"] = True

		# Update the information about the survivor (dates, survival day, files)
		self.Update_Information()

		# Show information about the newly created survival diary file
		self.Show_Information()

		# Open the file
		self.Open_File()

	def Select_A_City(self):
		# Define the local "Cities" dictionary
		self.dictionary["Cities"] = deepcopy(self.project_zomboid["Cities"])

		# Remove cities with no survivors
		for city, dictionary in deepcopy(self.dictionary["Cities"]["Dictionary"]).items():
			if dictionary["Survivors"]["List"] == []:
				# Remove the city
				self.dictionary["Cities"]["Names"].remove(city)

				# Remove the dictionary
				self.dictionary["Cities"]["Dictionary"].pop(city)

		# If the pre-defined city is an empty string, ask the user to select a city
		if self.project_zomboid["Pre-defined values"]["City"] == "":
			# Define the state
			state = "Kentucky"

			# Define the show and select texts
			show_text = self.language_texts["{}_cities"].format(state)
			select_text = self.language_texts["select_a_{}_city_to_use"].format(state)

			# Ask for the user to select the city
			city = self.Input.Select(self.dictionary["Cities"]["Names"], show_text = show_text, select_text = select_text)["option"]

		# If the city inside the pre-defined values dictionary is not an empty string
		if self.project_zomboid["Pre-defined values"]["City"] != "":
			# Define the city as the pre-defined city
			city = self.project_zomboid["Pre-defined values"]["City"]

		# Get the "City" dictionary
		self.dictionary["City"] = self.dictionary["Cities"]["Dictionary"][city]

	def Select_A_Survivor(self):
		# If the pre-defined survivor is an empty string, ask the user to select a survivor
		if self.project_zomboid["Pre-defined values"]["Survivor"] == "":
			# Define the show and select texts
			show_text = self.JSON.Language.language_texts["survivors, title()"]
			select_text = self.language_texts["select_a_survivor_from_{}_to_survive_as_them"].format(self.dictionary["City"]["Name"])

			# Ask for the user to select the survivor
			survivor = self.Input.Select(self.dictionary["City"]["Survivors"]["List"], show_text = show_text, select_text = select_text)["option"]

		# If the survivor inside the pre-defined values dictionary is not an empty string
		if self.project_zomboid["Pre-defined values"]["Survivor"] != "":
			# Define the survivor as the pre-defined survivor
			survivor = self.project_zomboid["Pre-defined values"]["Survivor"]

		# Get the "Survivor" dictionary
		self.dictionary["Survivor"] = self.dictionary["City"]["Survivors"]["Dictionary"][survivor]

	def Update_Information(self):
		# Define the Dates variable for easier typing
		self.dates = self.dictionary["Survivor"]["Dates"]

		# Add to the day number
		self.dates["Numbers"]["Day"] += 1

		# Add to the survival day number
		self.dates["Numbers"]["Survival day"] += 1

		# Add to the files number
		self.dictionary["Survivor"]["Numbers"]["Files"] += 1

		# Update the "Survivor.json" file
		self.JSON.Edit(self.dictionary["Survivor"]["Folders"]["Survivor"], self.dictionary["Survivor"])

		# ----- #

		# Define the date
		day = str(self.dates["Numbers"]["Day"])
		month = self.Text.Add_Leading_Zeroes(self.dates["Numbers"]["Month"])
		year = str(self.dates["Numbers"]["Year"])

		self.dictionary["Date"] = self.Date.From_String(day + "/" + month + "/" + year, format = "%d/%m/%Y")

		# Define the "File" dictionary
		self.dictionary["File"] = {}

		# Define the file name template
		self.dictionary["File"]["File name template"] = self.Date.language_texts["day, title()"] + " {}, {}, {}"

		# Define the list of items of the file name template
		items = [
			str(self.dates["Numbers"]["Survival day"]), # The survival day
			self.dictionary["Date"]["Texts"]["Day name"][self.user_language], # The day name in the user language
			self.dictionary["Date"]["Formats"]["DD-MM-YYYY"] # And the "Day-Month-Year" format of the current date
		]

		# Format the file name template with the items
		self.dictionary["File"]["Name"] = self.dictionary["File"]["File name template"].format(*items)

		# Define the header template of the diary
		self.dictionary["File"]["Header template"] = self.Date.language_texts["today_is_day_{} {} {}, {}"] + "." + \
		"\n" + \
		self.JSON.Language.language_texts["it_is"].capitalize() + " {} {}." + \
		"\n\n"

		# Define the number name of the day
		day_number_name = self.Date.language_texts["number_names, type: list"][self.dates["Numbers"]["Day"]].capitalize()

		# Define the list of items of the diary template
		items = [
			day_number_name.lower(), # The day number name
			self.dictionary["Date"]["Texts"]["Month name"][self.user_language], # The month name
			self.dictionary["Date"]["Units"]["Year"], # The year
			self.dictionary["Date"]["Formats"]["DD/MM/YYYY"], # The "Day-Month-Year" format of the current date
			self.dictionary["Date"]["Texts"]["Day gender"][self.user_language], # The day gender
			self.dictionary["Date"]["Texts"]["Day name"][self.user_language] # And the day name
		]

		# Create the diary header by formatting the template with the items
		self.dictionary["File"]["Header"] = self.dictionary["File"]["Header template"].format(*items)

		# Create the survival diary file
		self.dictionary["File"]["File"] = self.dates["Folders"]["Year"]["Month"]["root"] + self.dictionary["File"]["Name"] + ".txt"
		self.File.Create(self.dictionary["File"]["File"])

		# Write the diary header to the survival diary file
		self.File.Edit(self.dictionary["File"]["File"], self.dictionary["File"]["Header"], "w")

	def Show_Information(self):
		# Show some spaces and a five dash space separator
		print()
		print(self.separators["5"])
		print()

		# Show the information about the pre-defined values that were used
		if self.states["Used pre-defined values"] == True:
			print(self.language_texts["the_class_used_predefined_city_and_survivor"] + ".")
			print()

		# Show the city
		print(self.JSON.Language.language_texts["city, title()"] + ":")
		print("\t" + self.dictionary["City"]["Name"])
		print()

		# Show the survivor
		print(self.JSON.Language.language_texts["survivor, title()"] + ":")
		print("\t" + self.dictionary["Survivor"]["Name"])
		print()

		# Show the survival diary file name and file
		print(self.language_texts["this_survival_diary_file_was_created"] + ":")
		print("\t" + self.dictionary["File"]["Name"])
		print()
		print("\t" + self.dictionary["File"]["File"])

		# Show a space and a five dash space separator
		print()
		print(self.separators["5"])

	def Open_File(self):
		self.System.Open(self.dictionary["File"]["File"], verbose = False)
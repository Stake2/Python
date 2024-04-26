# Add_A_New_Survivor.py

from Project_Zomboid.Project_Zomboid import Project_Zomboid as Project_Zomboid

class Add_A_New_Survivor(Project_Zomboid):
	def __init__(self):
		super().__init__()

		# Define the root dictionary
		self.dictionary = {
			"Survivor": {},
			"City": {}
		}

		# Type the information about the survivor
		self.Type_Survivor_Information()

		# Create the folder of the survivor
		self.Create_Survivor_Folder()

		# Update the files of the survivor
		self.Update_Files()

		# Execute the root class again to define the variables of the survivor
		super().__init__()

		# Create the first survival diary file
		self.Create_Survival_Diary_File()

	def Type_Survivor_Information(self):
		# Define the default local "Survivor" dictionary
		survivor = {
			"Name": "",
			"City": "",
			"Details": {
				"Gender": "",
				"Age": 27,
				"Date of birth": "01/01/1966"
			},
			"Folders": {
				"root": "",
				"Survivor": ""
			},
			"Diary": {
				"Numbers": {
					"Survival day": 0,
					"Day": 8,
					"Month": 7,
					"Year": 1993
				},
				"Folders": {}
			}
		}

		# Ask for the name of the survivor
		survivor["Name"] = self.Input.Type(self.language_texts["type_the_name_of_the_survivor"], accept_enter = False, next_line = True)

		# ---------- #

		# Show the text telling the user to type the details about the survivor
		print()
		print(self.separators["5"])
		print()
		print(self.language_texts["type_the_details_of_the_survivor"] + ":")

		# Ask for the details of the survivor
		details = {
			"Gender": {
				"Lists": {
					"en": self.Language.texts["genders, type: list"]["en"],
					"Language": self.Language.language_texts["genders, type: list"]
				}
			},
			"Age": {
				"Format": {
					"Regex": "^([2][7-9]|[3-9][0-9]|100)$",
					"Example": "27"
				}
			},
			"Date of birth": {
				"Format": {
					"Regex": "^(0[0-9]|3[0-1])/(0[0-9]|1[0-2])/(1893|196[0-6]|19[0-5][0-9])$",
					"Example": "01/01/1966"
				}
			}
		}

		# Iterate through the details in the "Details" dictionary
		for key, detail in details.items():
			# Define the text key of the detail
			text_key = key.lower().replace(" ", "_")

			if "_" not in text_key:
				text_key += ", title()"

			# Define the text of the detail
			text = self.Language.language_texts[text_key]

			# If the "Lists" key is inside the "Detail" dictionary
			if "Lists" in detail:
				# Define the plural text key
				text_key = key.lower().replace(" ", "_") + "s"

				if "_" not in text_key:
					text_key += ", title()"

				# Create the plural text
				plural_text = self.Language.language_texts[text_key]

				# Define the parameters dictionary for the "Select" method of the "Input" class
				parameters = {
					"options": detail["Lists"]["en"],
					"language_options": detail["Lists"]["Language"],
					"show_text": text,
					"select_text": plural_text
				}

				# Ask the user to select an option from the list
				typed = self.Input.Select(**parameters)["option"]

			# If the "Format" key is inside the "Detail" dictionary
			if "Format" in detail:
				# Define the format variable for easier typing
				format = detail["Format"]

				# Update the detail text to add the example
				new_text = text + ":" + "\n" + \
				"(" + self.Language.language_texts["leave_empty_to_use_the_default_value"] + ': "' + format["Example"] + '")'

				# Ask for the detail
				typed = self.Input.Type(new_text, next_line = True)

				# If the typed value is an empty string
				if typed == "":
					# Define the typed variable as the default detail value
					typed = format["Example"]

					# Show the default detail
					print(text + ":")
					print(typed)

				# If the typed value is not an empty string
				if typed != "":
					# Import the "re" module
					import re

					# Search for the regex in the typed value
					search = re.search(format["Regex"], typed)

					# If the value does not match the regex
					if search == None:
						# Ask for the detail again
						typed = self.Input.Type(new_text, accept_enter = False, next_line = True, regex = format)

			# Add the detail to the "Details" dictionary of the "Survivor" dictionary
			survivor["Details"][key] = typed

		# ---------- #

		# Ask the user to select the city of the survivor
		city = self.Select_City()

		# Add the city name to the "Survivor" dictionary
		survivor["City"] = city["Name"]

		# Add the city to the root dictionary
		self.dictionary["City"] = city

		# ---------- #

		# Define the root "Survivor" dictionary as the local dictionary
		self.dictionary["Survivor"] = survivor

	def Create_Survivor_Folder(self):
		# Define and create the survivor folder
		root_folder = self.project_zomboid["Folders"]["Survivors"]["root"]

		self.dictionary["Survivor"]["Folders"]["root"] = root_folder + self.dictionary["Survivor"]["Name"] + "/"
		self.Folder.Create(self.dictionary["Survivor"]["Folders"]["root"])

		# Define and create the "Survivor.json" file
		self.dictionary["Survivor"]["Folders"]["Survivor"] = self.dictionary["Survivor"]["Folders"]["root"] + "Survivor.json"
		self.File.Create(self.dictionary["Survivor"]["Folders"]["Survivor"])

	def Update_Files(self):
		# Update the "Survivor.json" file
		self.Update_Dictionary(self.dictionary["Survivor"])

	def Create_Survival_Diary_File(self):
		# Update the "Survivor" dictionary inside the root dictionary
		self.dictionary["Survivor"] = self.project_zomboid["Survivors"]["Dictionary"][self.dictionary["Survivor"]["Name"]]

		# Import the sub-class
		from Project_Zomboid.Create_Survival_Diary_File import Create_Survival_Diary_File as Create_Survival_Diary_File

		# Add it to this class
		self.Create_Survival_Diary_File = Create_Survival_Diary_File

		# Execute the sub-class with the root dictionary
		self.Create_Survival_Diary_File(self.dictionary)
# Manage.py

from GamePlayer.GamePlayer import GamePlayer as GamePlayer

class Manage(GamePlayer):
	def __init__(self):
		super().__init__()

		methods = {
			"Iterate_Through_Game_List": self.language_texts["iterate_through_game_list"],
			"Convert_History": self.language_texts["convert_history"]
		}

		# Get the keys and values
		for name in ["keys", "values"]:
			methods[name] = list(getattr(methods, name)())

		# Add the methods to method keys list
		for method in methods.copy():
			if method not in ["keys", "values"]:
				methods[method] = getattr(self, method)

		# Select the method
		method = methods[self.Input.Select(methods["keys"], language_options = methods["values"])["option"]]
		method()

	def Iterate_Through_Game_List(self):
		from copy import deepcopy

		# Iterate through English game types list
		i = 0
		for game_type in self.game_types["Types"]["en"]:
			# Define the key of the game type for getting game type folders
			key = game_type.lower().replace(" ", "_")

			# Define the language game type
			language_game_type = self.game_types["Types"][self.user_language][i]

			# Get game with all "watching statuses", not just the "Watching" and "Re-watching" ones
			game_list = self.Get_Game_List(self.game_types[game_type], self.texts["statuses, type: list"]["en"])

			# Sort the game item list as case insensitive
			game_list = sorted(game_list, key = str.lower)

			# Show language game type
			print()
			print("----------")
			print()
			print(language_game_type + ":")

			game_types_to_remove = []

			# Remove a game type from the list (optional)
			if game_type not in game_types_to_remove:
				# For game in game item list
				for self.game_title in game_list:
					# Define root dictionary with game type and game
					self.dictionary = {
						"Type": self.game_types[game_type],
						"Game": {
							"Title": self.game_title
						}
					}

					# Show game title
					print()
					print("\t" + "---")
					print()
					print("\t" + self.dictionary["Game"]["Title"] + ":")

					# Select game and define its variables, returning the game dictionary (without asking user to select the game)
					self.dictionary = self.Select_Game(self.dictionary)

					self.game = self.dictionary["Game"]

			if self.switches["testing"] == True and game_type != self.game_types["Types"]["en"][-1] and game_type not in game_types_to_remove:
				self.Input.Type(self.JSON.Language.language_texts["continue, title()"])

			i += 1

	def Convert_History(self):
		from copy import deepcopy

		# Copy the switches dictionary
		switches_dictionary = deepcopy(self.switches)

		# Import the Play class
		from GamePlayer.Play import Play as Play

		self.Play = Play
		self.Play.Register = None

		# Import the Register class
		from GamePlayer.Register import Register as Register

		self.Register = Register

		# Get the History dictionary to update the sessions number
		self.dictionaries["History"] = self.JSON.To_Python(self.folders["play_history"]["history"])

		self.years_list = range(2021, self.date["Units"]["Year"] + 1)

		# Iterate through years list (of years that contain a "GamePlayer" folder)
		for self.year in self.years_list:
			# Convert the year number into a string
			self.year = str(self.year)

			# Define year dictionary with year number and folders
			self.year = {
				"Number": self.year,
				"folders": {
					"root": self.folders["play_history"]["root"] + self.year + "/",
				},
				"Sessions dictionary": deepcopy(self.template),
				"Lists": {}
			}

			print()
			print("----------")
			print()
			print(self.Date.language_texts["year, title()"] + ": " + self.year["Number"])

			# Define the history folders
			for folder_name in ["Per Game Type"]:
				key = folder_name.lower().replace(" ", "_")

				# Define the folder
				self.year["folders"][key] = {
					"root": self.year["folders"]["root"] + folder_name + "/"
				}

				self.Folder.Create(self.year["folders"][key]["root"])

			# Define the "Files" folder inside the "Per Game Type"
			self.year["folders"]["per_game_type"]["files"] = {
				"root": self.year["folders"]["per_game_type"]["root"] + "Files/"
			}

			exist = False

			# Define and create the "Sessions.json" file
			self.year["folders"]["sessions"] = self.year["folders"]["root"] + "Sessions.json"

			if self.File.Exist(self.year["folders"]["sessions"]) == True:
				exist = True

			self.File.Create(self.year["folders"]["sessions"])

			# Define and create the "Entry list.txt" file
			self.year["folders"]["entry_list"] = self.year["folders"]["root"] + "Entry list.txt"
			self.File.Create(self.year["folders"]["entry_list"])

			# Define the per game type "Files" folders
			for game_type in self.game_types["Types"]["en"]:
				key = game_type.lower().replace(" ", "_")

				# Create the game type folder
				self.year["folders"]["per_game_type"][key] = {
					"root": self.year["folders"]["per_game_type"]["root"] + game_type + "/"
				}

				self.Folder.Create(self.year["folders"]["per_game_type"][key]["root"])

				# Create the "Files" game type folder
				self.year["folders"]["per_game_type"][key]["files"] = {
					"root": self.year["folders"]["per_game_type"][key]["root"] + "Files/"
				}

				self.Folder.Create(self.year["folders"]["per_game_type"][key]["files"]["root"])

				# Define and create the game type "Sessions.json" file
				self.year["folders"]["per_game_type"][key]["sessions"] = self.year["folders"]["per_game_type"][key]["root"] + "Sessions.json"
				self.File.Create(self.year["folders"]["per_game_type"][key]["sessions"])

				# Define and create the game type "Entry list.txt" file
				self.year["folders"]["per_game_type"][key]["entry_list"] = self.year["folders"]["per_game_type"][key]["root"] + "Entry list.txt"
				self.File.Create(self.year["folders"]["per_game_type"][key]["entry_list"])

				# Define the game type "Games" file
				self.year["folders"]["per_game_type"][key]["games"] = self.year["folders"]["per_game_type"][key]["root"] + "Games.txt"

				if self.File.Exist(self.year["folders"]["per_game_type"][key]["games"]) == True:
					# Create game type lists dictionary and read "Games" file
					self.year["Lists"][game_type] = {
						"Games": self.File.Contents(self.year["folders"]["per_game_type"][key]["games"])["lines"]
					}

			# Define the entry files
			for file_name in ["Games", "Categories", "Time Spent", "Times"]:
				key = file_name.lower().replace(" ", "_")

				# Define the entry file
				self.year["folders"][key] = self.year["folders"]["root"] + file_name + ".txt"

				if self.File.Exist(self.year["folders"][key]) == True:
					# Get the list of lines inside the file
					self.year["Lists"][file_name] = self.File.Contents(self.year["folders"][key])["lines"]

			if "Games" in self.year["Lists"] and self.year["Number"] != list(self.years_list)[-1] and exist == False:
				self.Input.Type("Finished creating files")

			if "Games" in self.year["Lists"]:
				# Add to total number
				self.year["Sessions dictionary"]["Numbers"]["Total"] = len(self.year["Lists"]["Games"])

				# Define the game type dictionaries
				self.game_type_dictionaries = {}

				# Iterate through the English plural game types
				for game_type in self.game_types["Types"]["en"]:
					# Create game type dictionary with game number and game item list (with all game titles)
					self.game_type_dictionaries[game_type] = {
						"Number": 1,
						"Game list": self.Get_Game_List(self.game_types[game_type], self.texts["statuses, type: list"]["en"])
					}

				remove_list = self.File.Contents(self.Folder.folders["apps"]["root"] + "Test.txt")["lines"]

				self.old_history = {
					"current_year": self.Years.years[self.year["Number"]],
					"folders": self.year["folders"],
					"old_history": {
						"Number": self.year["Number"]
					},
					"Sessions": self.dictionaries["Sessions"],
					"Game type": self.dictionaries["Game type"],
					"Played": self.dictionaries["Played"],
					"Change year": True
				}

				# If the "Sessions.json" is not empty and has sessions, get Sessions dictionary from it
				if self.File.Contents(self.year["folders"]["sessions"])["lines"] != [] and self.JSON.To_Python(self.year["folders"]["sessions"])["Entries"] != []:
					self.dictionaries["Sessions"] = self.JSON.To_Python(self.year["folders"]["sessions"])

				# Iterate through the games list
				e = 0
				for entry in self.year["Lists"]["Games"]:
					# Define the Entry dictionary
					entry = {
						"Game title": entry,
						"Type": self.year["Lists"]["Categories"][e],
						"Session duration": {
							"Before": {},
							"After": self.Date.From_String(self.year["Lists"]["Times"][e], "%H:%M %d/%m/%Y"),
							"Text": self.year["Lists"]["Time Spent"][e]
						},
						"Date": {}
					}

					entry["Date"] = entry["Session duration"]["After"]
					entry["Session duration"]["Before"] = entry["Session duration"]["After"]

					if " and " in entry["Session duration"]["Text"]:
						split = entry["Session duration"]["Text"].split(" and ")
						hours = split[0]
						minutes = split[1]

						if " hours" in hours:
							entry["Session duration"]["Hours"] = int(hours.split(" hours")[0])
							hours = "hours"

						elif " hour" in hours:
							entry["Session duration"]["Hours"] = int(hours.split(" hour")[0])
							hours = "hour"

						if " minutes" in minutes:
							entry["Session duration"]["Minutes"] = int(minutes.split(" minutes")[0])
							minutes = "minutes"

						elif " minute" in minutes:
							entry["Session duration"]["Minutes"] = int(minutes.split(" minute")[0])
							minutes = "minute"

						entry["Session duration"]["Text"] = {
							"en": str(entry["Session duration"]["Hours"]) + " " + hours + " and " + str(entry["Session duration"]["Minutes"]) + " " + minutes,
							"pt": ""
						}

						entry["Session duration"]["Text"]["pt"] = str(entry["Session duration"]["Hours"]) + " hora"

						if hours == "hours":
							entry["Session duration"]["Text"]["pt"] += "s"

						entry["Session duration"]["Text"]["pt"] += " e " + str(entry["Session duration"]["Minutes"]) + " " + "minuto"

						if minutes == "minutes":
							entry["Session duration"]["Text"]["pt"] += "s"

						entry["Session duration"]["Before"] = self.Date.Now(entry["Session duration"]["Before"]["Object"] - self.Date.Relativedelta(hours = entry["Session duration"]["Hours"]))

						entry["Session duration"]["Before"] = self.Date.Now(entry["Session duration"]["Before"]["Object"] - self.Date.Relativedelta(minutes = entry["Session duration"]["Minutes"]))

					elif " minutes" in entry["Session duration"]["Text"]:
						entry["Session duration"]["Minutes"] = int(entry["Session duration"]["Text"].split(" minutes")[0])

						entry["Session duration"]["Text"] = {
							"en": str(entry["Session duration"]["Minutes"]) + " minutes",
							"pt": str(entry["Session duration"]["Minutes"]) + " minutos"
						}

						entry["Session duration"]["Before"] = self.Date.Now(entry["Session duration"]["Before"]["Object"] - self.Date.Relativedelta(minutes = entry["Session duration"]["Minutes"]))

					elif " minute" in entry["Session duration"]["Text"]:
						entry["Session duration"]["Minutes"] = int(entry["Session duration"]["Text"].split(" minute")[0])

						entry["Session duration"]["Text"] = {
							"en": str(entry["Session duration"]["Minutes"]) + " minute",
							"pt": str(entry["Session duration"]["Minutes"]) + " minuto"
						}

						entry["Session duration"]["Before"] = self.Date.Now(entry["Session duration"]["Before"]["Object"] - self.Date.Relativedelta(minutes = entry["Session duration"]["Minutes"]))

					elif " hours" in entry["Session duration"]["Text"]:
						entry["Session duration"]["Hours"] = int(entry["Session duration"]["Text"].split(" hours")[0])

						entry["Session duration"]["Text"] = {
							"en": str(entry["Session duration"]["Hours"]) + " hours",
							"pt": str(entry["Session duration"]["Hours"]) + " horas"
						}

						entry["Session duration"]["Before"] = self.Date.Now(entry["Session duration"]["Before"]["Object"] - self.Date.Relativedelta(hours = entry["Session duration"]["Hours"]))

					elif " hour" in entry["Session duration"]["Text"]:
						entry["Session duration"]["Hours"] = int(entry["Session duration"]["Text"].split(" hour")[0])

						entry["Session duration"]["Text"] = {
							"en": str(entry["Session duration"]["Hours"]) + " hour",
							"pt": str(entry["Session duration"]["Hours"]) + " hora"
						}

						entry["Session duration"]["Before"] = self.Date.Now(entry["Session duration"]["Before"]["Object"] - self.Date.Relativedelta(hours = entry["Session duration"]["Hours"]))

					text = entry["Session duration"]["Text"]
					entry["Session duration"].pop("Text")
					entry["Session duration"]["Text"] = text

					entry["Dates"] = {
						"Timezone": entry["Date"]["Formats"]["HH:MM DD/MM/YYYY"]
					}

					if entry["Game title"] == self.year["Lists"]["Games"][0]:
						print()

					# Define the progress text with progress (current number and sessions number)
					# Game type, entry time and name
					progress_text = "-----" + "\n" + \
					"\n" + \
					str(e + 1) + "/" + str(len(self.year["Lists"]["Games"])) + ":" + "\n" + "\n" + \
					self.JSON.Language.language_texts["type, title()"] + ":" + "\n" + \
					"[" + entry["Type"] + "]" + "\n" + \
					"\n" + \
					self.Date.language_texts["date, title()"] + ":" + "\n" + \
					"[" + entry["Date"]["Formats"]["HH:MM DD/MM/YYYY"] + '] "' + entry["Date"]["Object"].strftime("%Z") + '"' + " (Timezone)" + "\n" + \
					"[" + entry["Date"]["UTC"]["DateTime"]["Formats"]["HH:MM DD/MM/YYYY"] + "] (UTC)" + "\n" + \
					"\n" + \
					self.JSON.Language.language_texts["entry, title()"] + ":" + "\n" + \
					"[" + entry["Game title"] + "]" + "\n" + \
					"\n" + \
					self.language_texts["session_duration"] + ":" + "\n"

					for key in entry["Session duration"]:
						text = entry["Session duration"][key]

						if key in ["Text", "Hours", "Minutes"]:
							if type(text) == dict and self.user_language in text:
								text = text[self.user_language]

							else:
								text = str(text)

							progress_text += "[" + text + "]"

							if key != list(entry["Session duration"].keys()):
								progress_text += "\n"

					# Show the progress text
					print(progress_text)

					# Define default game dictionary
					self.dictionary = {}

					# If testing is True and the game title is not inside the remove list
					# Or testing is False and the remove list is empty

					local_e = e

					if local_e != 0:
						local_e = e + 1

					if (
						self.switches["testing"] == True and str(local_e) not in remove_list or
						self.switches["testing"] == False and remove_list == []
					):
						# Find the game and get game titles
						for game_title in self.game_type_dictionaries[entry["Type"]]["Game list"]:
							if game_title in entry["Game title"]:
								# Define the root dictionary with game type and game
								self.dictionary = {
									"Type": self.game_types[entry["Type"]],
									"Game": {
										"Title": game_title
									}
								}

								# Select game and define its variables, returning the game dictionary (without asking user to select the game)
								self.dictionary = self.Select_Game(self.dictionary)

								self.Replace_Year_Number(self.dictionary["Type"]["Folders"]["per_game_type"], str(self.date["Units"]["Year"]), self.year["Number"])

						if self.dictionary != {}:
							self.dictionary["Old history"] = self.old_history

							# Define game dictionary to speed up typing
							self.game = self.dictionary["Game"]

							self.dictionaries["Played"] = self.game["Played"]
							self.old_history["Played"] = self.game["Played"]
							self.dictionary["Old history"]["Played"] = self.old_history["Played"]

							# Show game title
							print("\t" + self.game["Title"] + ":")

							states_dictionary = deepcopy(self.game["States"])

							states_dictionary["Re-playing"] = False
							states_dictionary["Christmas"] = False
							states_dictionary["Completed game"] = False
							states_dictionary["First game session in year"] = False
							states_dictionary["First game type session in year"] = False

							# If the "25/12" text is inside the Timezone time string (25 = day, 12 = month, Christmas day)
							if "25/12" in entry["Date"]["Formats"]["HH:MM DD/MM/YYYY"]:
								# Set the "Christmas" state as True
								states_dictionary["Christmas"] = True

							states_dictionary["First game session in year"] = False

							# If the game title is the first game title inside the Games list
							if entry["Game title"] == self.year["Lists"]["Games"][0]:
								# Set the "First game session in year" state as True
								states_dictionary["First game session in year"] = True

							states_dictionary["First game type session in year"] = False

							# If the game title is the first game title inside the game type Games list
							if entry["Game title"] == self.year["Lists"][entry["Type"]]["Games"][0]:
								# Set the "First game type session in year" state as True
								states_dictionary["First game type session in year"] = True

							# Add Entry dictionary to root dictionary
							self.dictionary["Entry"] = entry

							# Add the "Old history" dictionary to add the year folder
							self.dictionary["Old history"].update({
								"Game title": entry["Game title"]
							})

							for dictionary_name in ["Sessions", "Game type", "Played"]:
								self.dictionaries[dictionary_name] = self.old_history[dictionary_name]

							# Run the "Play" class to define more game variables
							self.dictionary = self.Play(self.dictionary, open_game = False).dictionary

							self.game = self.dictionary["Game"]

							self.game["States"] = states_dictionary
							self.dictionary["Game"]["States"] = states_dictionary

							self.game["States"]["Finished playing"] = True

							# Keep the original switches inside the "Switches.json" file before running the "Register" class
							self.Global_Switches.Switch(switches_dictionary)

							setattr(Register, "old_history", self.old_history)

							# Run the "Register" class to register the game unit
							register_dictionaries = self.Register(self.dictionary).dictionaries

							for key in ["Sessions", "Game type", "Played"]:
								self.old_history[key] = register_dictionaries[key]

							self.dictionary["Old history"] = self.old_history

							if progress_text[-1] == "\n":
								progress_text = progress_text[:-1]

							print()
							print(progress_text)

							if entry["Game title"] != self.year["Lists"]["Games"][-1] and self.switches["testing"] == True:
								self.Input.Type(self.JSON.Language.language_texts["continue, title()"] + " (" + self.JSON.Language.language_texts["next, feminine"].title() + " " + self.JSON.Language.language_texts["entry"] + ")")

							print()

						else:
							text = self.JSON.Language.Item({
								"en": "The game is not inside the Game Info Database",
								"pt": "O jogo não está dentro do Banco de Dados de Informações de Jogos"
							})

							print("\t" + "[" + entry["Game title"] + "]")
							print()
							print("\t" + text + ".")
							print()
							quit("----------")

					e += 1

				# Delete the history files
				for file_name in ["Games", "Categories", "Time Spent", "Times"]:
					key = file_name.lower().replace(" ", "_")

					# Delete the entry file
					self.File.Delete(self.year["folders"][key])

				for game_type in self.game_types["Types"]["en"]:
					key = game_type.lower().replace(" ", "_")

					self.File.Delete(self.year["folders"]["per_game_type"][key]["games"])

				# Delete the "Per Game Type" folders
				for folder_name in ["Files", "Folders"]:
					folder = self.year["folders"]["per_game_type"]["root"] + folder_name + "/"
					self.Folder.Delete(folder)

			from GamePlayer.GamePlayer import GamePlayer as GamePlayer

			self.old_history = {
				"current_year": self.Years.years[self.year["Number"]],
				"folders": self.year["folders"],
				"old_history": {
					"Number": self.year["Number"]
				},
				"Sessions": self.dictionaries["Sessions"],
				"Game type": self.dictionaries["Game type"],
				"Change year": True
			}

			# Add the keys and values of the dictionary to the pre-baked "GamePlayer" class
			for key, value in self.old_history.items():
				setattr(GamePlayer, key, value)

			GamePlayer = GamePlayer()

			if "Games" in self.year["Lists"] and self.year["Number"] != list(self.years_list)[-1]:
				self.Input.Type(self.JSON.Language.language_texts["continue, title()"] + " (" + self.JSON.Language.language_texts["next, masculine"].title() + " " + self.Date.language_texts["year, title()"] + ")")

		# Update the "History.json" file with the new History dictionary
		self.JSON.Edit(self.folders["play_history"]["history"], self.dictionaries["History"])

	def Replace_Year_Number(self, folders, to_replace, replace_with):
		for key, value in folders.items():
			value = folders[key]

			if type(value) == str:
				folders[key] = folders[key].replace(to_replace, replace_with)

			if type(value) == dict:
				self.Replace_Year_Number(value, to_replace, replace_with)
# Register.py

from GamePlayer.GamePlayer import GamePlayer as GamePlayer

class Register(GamePlayer):
	def __init__(self, dictionary):
		super().__init__()

		# Ask for entry information
		if self.run_as_module == False:
			self.Type_Entry_Information()

		self.dictionary["Entry"].update({
			"Times": {},
			"Diary Slim": {
				"Text": "",
				"Clean text": ""
			},
			"States": {
				"Post on the Social Networks": False
			}
		})

		# If the Time dictionary is not empty, get the UTC and Timezone times
		if self.dictionary["Entry"]["Time"] != {}:
			self.dictionary["Entry"]["Times"] = {
				"UTC": self.Date.To_String(self.dictionary["Entry"]["Time"]["utc"]),
				"Timezone": self.Date.Now(self.dictionary["Entry"]["Time"]["date"].astimezone())["hh:mm DD/MM/YYYY"]
			}

		# If the Time dictionary is empty, define the UTC and Timezone times as the current year number
		if self.dictionary["Entry"]["Time"] == {}:
			self.dictionary["Entry"]["Times"] = {
				"UTC": self.current_year["Number"],
				"Timezone": self.current_year["Number"]
			}

		# Define the media variable to make typing the media dictionary easier
		self.game = self.dictionary["Game"]

		self.Check_Media_Status()

		if self.game["States"]["Re-playing"] == False and self.game["States"]["Completed game"] == True:
			self.Check_Media_Dates()

		# Database related methods
		self.Register_In_JSON()
		self.Create_Entry_File()

		self.Add_Entry_File_To_Year_Folder()

		self.Define_Diary_Slim_Text()

		self.Post_On_Social_Networks()

		self.Write_On_Diary_Slim()

		self.Show_Information()

	def Type_Entry_Information(self):
		# To-Do: Make this method
		pass

	def Post_On_Social_Networks(self):
		self.social_networks = [
			"WhatsApp",
			"Instagram",
			"Facebook",
			"Twitter",
		]

		self.social_networks_string = self.Text.From_List(self.social_networks, break_line = False, separator = ", ")
		self.first_three_social_networks = ""

		for social_network in self.social_networks:
			if social_network != self.social_networks[-1]:
				self.first_three_social_networks += social_network

				if social_network != "Facebook":
					self.first_three_social_networks += ", "

		self.twitter_social_network = self.social_networks[-1]

		self.posted_on_social_networks_text_template = self.language_texts["i_posted_the_text_of_the_played_game_on_the_status_of_{}_and_tweet_on_{}"] + "."

		self.dictionary["Entry"]["Diary Slim"]["Posted on the Social Networks text"] = self.posted_on_social_networks_text_template.format(self.first_three_social_networks, self.twitter_social_network)

		text = self.language_texts["post_on_the_social_networks"] + " (" + self.social_networks_string + ")"

		self.dictionary["Entry"]["States"]["Post on the Social Networks"] = self.Input.Yes_Or_No(text)

		if self.dictionary["Entry"]["States"]["Post on the Social Networks"] == True:
			from Social_Networks.Open_Social_Network import Open_Social_Network as Open_Social_Network

			Open_Social_Network(option_info = {"type": "profile"}, social_network_parameter = "WhatsApp", first_space = False, second_space = False)

			self.Input.Type(self.language_texts["press_enter_to_copy_the_text_of_the_played_game"])

			self.Text.Copy(self.dictionary["Entry"]["Diary Slim"]["Clean text"])

		print()
		print("-----")
		print()

	def Write_On_Diary_Slim(self):
		# Add "Posted on Social Networks" text if the user wanted to post the entry text on the Social Networks
		if self.dictionary["Entry"]["States"]["Post on the Social Networks"] == True:
			self.dictionary["Entry"]["Diary Slim"]["Text"] += "\n\n" + self.dictionary["Entry"]["Diary Slim"]["Posted on the Social Networks text"]

		from Diary_Slim.Write_On_Diary_Slim_Module import Write_On_Diary_Slim_Module as Write_On_Diary_Slim_Module

		Write_On_Diary_Slim_Module(self.dictionary["Entry"]["Diary Slim"]["Text"], add_time = False, add_dot = False)
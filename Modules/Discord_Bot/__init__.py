# Discord_Bot.py

# Import some useful modules
import importlib
import asyncio
import logging

# Import discord.py modules
import discord
from discord.ext import commands as bot_commands

class Discord_Bot():
	def __init__(self):
		# Import some utility classes
		self.Import_Utility_Classes()

		# Define the folders of the module
		self.folders = self.Define_Folders(object = self, files = ["Bot"]).folders

		# Defines the basic variables
		self.Define_Basic_Variables()

		# Define the text dictionaries of the class
		self.Define_Texts()

		# Define the bot
		self.Define_Bot()

	def Import_Utility_Classes(self):
		# Define the classes to be imported
		classes = [
			"Define_Folders",
			"JSON"
		]

		# Iterate through the list of classes
		for class_title in classes:
			# If the class is not already inside this class (Christmas)
			# Or the class is "Define_Folders"
			if (
				hasattr(self, class_title) == False or
				class_title == "Define_Folders"
			):
				# Import the module
				module = importlib.import_module("." + class_title, "Utility")

				# Get the sub-class
				sub_class = getattr(module, class_title)

				# If the module title is not "Define_Folders"
				if class_title != "Define_Folders":
					# Run the sub-class to define its variable
					sub_class = sub_class()

				# Add the sub-class to the current class
				setattr(self, class_title, sub_class)

		# ---------- #

		# Define the "Language" class as the same class inside the "JSON" class
		self.Language = self.JSON.Language

	def Define_Basic_Variables(self):
		# Get the dictionary of modules
		self.modules = self.JSON.To_Python(self.folders["Python"]["Modules"]["Modules"])

		# Create a list of the modules that will not be imported
		self.modules["Remove list"] = [
			"Define_Folders",
			"Modules",
			"Language",
			"JSON"
		]

		# Iterate through the list of utility modules
		for module_title in self.modules["Utility"]["List"]:
			# If the module title is not inside the remove list
			if module_title not in self.modules["Remove list"]:
				# Import the module
				module = importlib.import_module("." + module_title, "Utility")

				# Get the sub-class of the module
				sub_class = getattr(module, module_title)

				# Add the sub-class to the current class
				setattr(self, module_title, sub_class())

		# ---------- #

		# Get the switches dictionary from the "Global Switches" class
		self.switches = self.Global_Switches.switches["Global"]

		# ---------- #

		# Import some variables from the "Language" class

		# Import the "languages" dictionary
		self.languages = self.Language.languages

		# Import the "language" dictionary
		self.language = self.Language.language

		# Import the "separators" dictionary
		self.separators = self.Language.separators

		# ---------- #

		# Import the "folders" dictionary from the "Folder" class
		self.folders = self.Folder.folders

		# ---------- #

		# Import the "Sanitize" method from the "File" class
		self.Sanitize = self.File.Sanitize

		# ---------- #

		# Get the current date from the "Date" class
		self.date = self.Date.date

	def Define_Texts(self):
		# Define the "Texts" dictionary
		self.texts = self.JSON.To_Python(self.module["Files"]["Texts"])

		# Define the "Language texts" dictionary
		self.language_texts = self.Language.Item(self.texts)

	def Verbose(self, text):
		# Show a five dash space separator
		print()
		print(self.separators["5"])
		print()

		# Show the verbose text
		print(text)

	def Define_Bot(self):
		# Get the bot dictionary from the module's "Bot.json" file
		self.bot = self.JSON.To_Python(self.module["Files"]["Bot"])

		# ---------- #

		# Define the log handler
		self.bot["Log handler"] = logging.FileHandler(filename = "Discord.log", encoding = "utf-8", mode = "w")

		# ---------- #

		# Define the default bot intents
		self.bot["Intents"] = discord.Intents.default()

		# Define the message content intent as True to allow the bot to read messages
		self.bot["Intents"].message_content = True

		# ---------- #

		# Create a shortcut to the bot "Activity" dictionary
		activity = self.bot["Activity"]

		# Define the bot activity object
		activity["Object"] = discord.CustomActivity(
			# Define the name of the activity
			name = activity["Emoji"] + " " + activity["Name"],
			emoji = discord.PartialEmoji(name = activity["Emoji"])
		)

		# Define the bot client with its intents and activity
		self.bot["Client"] = discord.Client(
			intents = self.bot["Intents"],
			activity = activity["Object"]
		)

		# Create a shortcut to the bot "Client" object
		client = self.bot["Client"]
			
		# Say that the bot has logged in
		@client.event
		async def on_ready():
			# Get the logged in text
			text = self.language_texts["i_have_logged_in_as_{}"]

			# Format it with the bot name
			text = text.format(client.user)

			# Show the text
			self.Verbose(text)

		# Handle messages received by the bot
		@client.event
		async def on_message(message):
			# If the message was not sent from an allowed server
			# Or the message channel is not in the list of allowed channels
			# Or the message is from the bot itself
			if (
				message.guild.id not in self.bot["Allowed servers"] or
				message.channel.id not in self.bot["Allowed channels"] or
				message.author == client.user
			):
				# Ignore the message
				return

		# ---------- #

		# Define the bot commands
		self.bot["Commands"] = bot_commands.Bot(command_prefix = "!", intents = self.bot["Intents"])

		# Create a shortcut to the bot commands
		bot = self.bot["Commands"]

		# Add a "Hello world!" command
		@bot.command()
		async def hello_world(context, argument):
			# Send a message saying "Hello world!"
			await context.send("Hello world!")

		# Add a "Hello [name]!" command
		@bot.command()
		async def hello(context, name):
			# Send a message saying "Hello [name]!"
			await context.send("Hello {}!".format(name))

		# ---------- #

		# Run the bot client with its token and custom parameters
		self.bot["Client"].run(
			# The bot token
			self.bot["Token"],

			# Log related parameters
			log_handler = self.bot["Log handler"],
			log_level = logging.DEBUG
		)

# If the script file is being executed directly
if __name__ == "__main__":
	# Run the "Discord_Bot" class
	Discord_Bot()
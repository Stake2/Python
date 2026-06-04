# Discord_Bot.py

# Import some useful modules
import importlib
import asyncio
import logging

# Import the discord.py modules
import discord
from discord.ext import commands as bot_commands

# Define the main "Discord_Bot" class
class Discord_Bot():
	def __init__(self):
		# Define the variables of the class
		self.Define_Variables()

		# Define the bot
		self.Define_Bot()

	def Define_Variables(self):
		# Import the "JSON" class
		from Utility.JSON import JSON as JSON

		# Instance it and add it to the current class
		self.JSON = JSON()

		# Import the "folders" dictionary from the "JSON" class
		self.folders = self.JSON.folders

		# ---------- #

		# Get the dictionary of Python modules
		self.modules = self.JSON.To_Python(self.folders["Python"]["Modules"]["Modules"])

		# Define a list of utility classes to not import
		do_not_import = [
			"API",
			"Date",
			"Folder",
			"Input",
			"System",
			"Text"
		]

		# Iterate through the list of utility classes
		for class_title in self.modules["Utility"]["List"]:
			# If the class is not already inside the self class (Discord_Bot)
			# And the class title is not inside the list of utility classes to not import
			if (
				hasattr(self, class_title) == False and
				class_title not in do_not_import
			):
				# Import the module of the class
				module = importlib.import_module("." + class_title, "Utility")

				# Get the class object inside the module
				class_object = getattr(module, class_title)

				# If the class title is not "Modules"
				if class_title != "Modules":
					# Run the class object to define its attributes
					class_object = class_object()

				# Add the class object to the root class
				setattr(self, class_title, class_object)

		# ---------- #

		# Define the module dictionary and the module folders and files
		self.Modules(class_object = self)

		# ---------- #

		# Import the switches dictionary from the "Global Switches" class
		self.switches = self.Global_Switches.switches["Global"]

		# ---------- #

		# Define the "Language" class as the same class inside the "JSON" class
		self.Language = self.JSON.Language

		# Import some attributes from the "Language" class

		# Import the "languages" dictionary
		self.languages = self.Language.languages

		# Import the "language" dictionary
		self.language = self.Language.language

		# Import the "separators" dictionary
		self.separators = self.Language.separators

		# ---------- #

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
		# Define and create the "Bot.json" file
		self.module["Files"]["Bot"] = self.module["Folders"]["Files"]["root"] + "Bot.json"
		self.File.Create(self.module["Files"]["Bot"])

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
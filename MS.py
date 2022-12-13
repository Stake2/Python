# Module_Selector.py

# To-Do: Use for loop in modules list to show modules, and use Text.Select to select one of the modules if no argument is present

import argparse

text_modules = False

if text_modules == True:
	import Block_Websites
	import Christmas
	import Code
	import Diary
	import Diary_Slim
	import Food_Time
	import Friends
	import GamePlayer
	import Project_Zomboid
	import Python
	import Social_Networks
	import SproutGigs
	import Stories
	import Tasks
	import Watch_History
	import Years
	add_import = ""

parser = argparse.ArgumentParser()

parser.add_argument("-testing", "--testing", action="store_true", help="Activates the testing mode of modules")
parser.add_argument("-verbose", "--verbose", action="store_true", help="Activates the verbose mode of modules")
parser.add_argument("-user_information", "--user-information", "-userinformation", action="store_true", help="Activates the showing of user information on the Language class")

parser.add_argument("-block_websites", "--block_websites", action="store_true", help="Runs the Block_Websites module")

parser.add_argument("-christmas", "--christmas", "-natal", action="store_true", help="Runs the Christmas module")

parser.add_argument("-code", "--code", action="store_true", help="Runs the Code module")

parser.add_argument("-diary", "--diary", "-diario", "--diario", "-diário", "--diário", action="store_true", help="Runs the Diary module")

parser.add_argument("-diary_slim", "--diary_slim", "--diary-slim", "-diario_slim", "-diário_slim", "-slim", action="store_true", help='Runs the "Diary_Slim" module')

parser.add_argument("-food_time", "--food_time", "--food-time", "-foodtime", "--foodtime", "-fdt", action="store_true", help='Runs the "Food_Time" module')
parser.add_argument("-set", "-set_food_time", "-sfdt", "-setar", action="store_true", help='Sets the current food time, the time the food was eaten, using the module "Food_Time"')
parser.add_argument("-check", "-check_food_time", "-cfdt", action="store_true", help='Checks the current food time, the time the food was eaten, using the module "Food_Time"')

parser.add_argument("-friends", "-friend", "-amigos", "-amigo", action="store_true", help="Runs the Friends module")

parser.add_argument("-gameplayer", "--gameplayer", "-gp", "-games", "-jogos", "-jogar", action="store_true", help="Runs the GamePlayer module")

parser.add_argument("-project_zomboid", "-zomboid", "-project-zomboid", action="store_true", help="Runs the Project_Zomboid module")

parser.add_argument("-python", action="store_true", help="Runs the Python module")

parser.add_argument("-social_networks", "--social_networks", action="store_true", help="Runs the Social_Networks module")

parser.add_argument("-sproutgigs", "--sproutgigs", action="store_true", help="Runs the SproutGigs module")

parser.add_argument("-stories", "--stories", "-story", "-histórias", "-história", action="store_true", help="Runs the Stories module")

parser.add_argument("-tasks", "--tasks", "-task", "--task", "-tarefa", "-tarefas", action="store_true", help="Runs the Tasks module")

parser.add_argument("-watch_history", "--watch-history", "-watch-history", "-watch", "--watch", "-assistir", "-watch_3", action="store_true", help="Runs the Watch_History module")

parser.add_argument("-years", "--years", action="store_true", help="Runs the Years module")

add_argument = ""

arguments = parser.parse_args()

switches = ["testing", "verbose", "user_information"]

has_switches = False

for switch in switches:
	if hasattr(arguments, switch) and getattr(arguments, switch) == True:
		has_switches = True

# Update Switches file if there are Switch arguments
if has_switches == True:
	from Global_Switches import Global_Switches as Global_Switches
	from File import File as File
	from Text import Text as Text

	Global_Switches = Global_Switches()
	File = File()
	Text = Text()

	# Get switches file
	switches_file = Global_Switches.switches_file

	dictionary = File.Dictionary(switches_file)
	dictionary_backup = dictionary.copy()

	for switch in switches:
		dictionary[switch.capitalize().replace("_", " ")] = False

		if hasattr(arguments, switch) and getattr(arguments, switch) == True:
			dictionary[switch.capitalize().replace("_", " ")] = True			

	# Update Switches file
	File.Edit(switches_file, Text.From_Dictionary(dictionary), "w")

	new_dictionary = {}

	for key in dictionary.copy():
		new_dictionary[key.lower().replace(" ", "_")] = dictionary[key]

	dictionary = new_dictionary

	# Show Global Switches
	File.Language.Show_Global_Switches(dictionary, show_ending = True)

# Reset Switches file if no Switch argument is present
if has_switches == False:	
	from File import File as File
	from Text import Text as Text

	# Define dictionary
	dictionary = {
		"Testing": False,
		"Verbose": False,
		"User information": False,
	}

	new_dictionary = {}

	for key in dictionary.copy():
		new_dictionary[key.lower().replace(" ", "_")] = dictionary[key]

	from Global_Switches import Global_Switches as Global_Switches

	Global_Switches = Global_Switches()

	# Get switches file
	switches_file = Global_Switches.switches_file

	File = File(new_dictionary)
	Text = Text(new_dictionary)

	# Reset
	File.Edit(switches_file, Text.From_Dictionary(dictionary), "w")

if arguments.block_websites:
	import Block_Websites

	Block_Websites.Run()

if arguments.christmas:
	import Christmas

	Christmas.Run()

if arguments.code:
	import Code

	Code.Run()

if arguments.diary:
	import Diary

	Diary.Run()

if arguments.diary_slim:
	import Diary_Slim

	Diary_Slim.Run()

if arguments.food_time:
	from Food_Time import Food_Time as Food_Time

	if arguments.set:
		Food_Time()

	if arguments.check:
		Food_Time(register_time = False)

if arguments.friends:
	import Friends

	Friends.Run()

if arguments.gameplayer:
	import GamePlayer

	GamePlayer.Run()

if arguments.project_zomboid:
	import Project_Zomboid

	Project_Zomboid.Run()

if arguments.python:
	import Python

	Python.Run()

if arguments.social_networks:
	import Social_Networks

	Social_Networks.Run()

if arguments.sproutgigs:
	import SproutGigs

	SproutGigs.Run()

if arguments.stories:
	import Stories

	Stories.Run()

if arguments.tasks:
	import Tasks

	Tasks.Run()

if arguments.watch_history:
	import Watch_History

	Watch_History.Run()

if arguments.years:
	import Years

	Years.Run()

# Update switches file with the state of the switches before execution of modules
if has_switches == True:
	from File import File as File

	dictionary = {
		"Testing": False,
		"Verbose": False,
		"User information": False,
	}

	new_dictionary = {}

	for key in dictionary.copy():
		new_dictionary[key.lower().replace(" ", "_")] = dictionary[key]

	File = File(new_dictionary)

	File.Edit(switches_file, Text.From_Dictionary(dictionary), "w")
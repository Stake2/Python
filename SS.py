from Script_Helper import *

import argparse

test_scripts = True

if test_scripts == True:
	import Block_Websites
	import Christmas
	import Code
	import Diary
	import Diary_Slim
	import Food_Time
	import Friends_Manager
	import GamePlayer
	import Music_Database
	import Project_Zomboid_Manager
	import Python_Module_Manager
	import Social_Networks
	import SproutGigs
	import Story_Manager
	import Study
	import Tasks
	import Text_Generator
	import Unified_Remote_Manager
	import Watch_History
	import Year_Summary_Manager
	add_import = ""

script_selector_parser = argparse.ArgumentParser()
script_selector_parser.add_argument("-language", "-lang", "-idioma", action="store", help="""Selects the language of the scripts, options: 
pt, ptbr (Brazilian Portuguese)
en, enus (English).""")

script_selector_parser.add_argument("-block_websites", "--block_websites", action="store_true", help="Runs the Block_Websites.py script.")

script_selector_parser.add_argument("-christmas", "--christmas", "-natal", action="store_true", help="Runs the Christmas.py script.")

script_selector_parser.add_argument("-code", "--code", action="store_true", help="Runs the Code.py script.")
script_selector_parser.add_argument("-update_websites", "--update_websites", "--update-websites", action="store_true", help="Runs the Update_Websites class of the Code.py script.")

script_selector_parser.add_argument("-diary", "--diary", "-diario", "--diario", "-diário", "--diário", action="store_true", help="Runs the Diary.py script.")

script_selector_parser.add_argument("-diary_slim", "--diary_slim", "--diary-slim", "-diario_slim", "-diário_slim", "-slim", action="store_true", help="Runs the Diary_Slim.py script.")

script_selector_parser.add_argument("-food_time", "--food_time", "--food-time", "-foodtime", "--foodtime", "-fdt", action="store_true", help="Runs the Food_Time.py script.")
script_selector_parser.add_argument("-sfdt", "-set_food_time", "-set", "-set", "-setar", action="store_true", help="Sets the current food time, the time the food was eaten, using the module Food_Time.py.")
script_selector_parser.add_argument("-cfdt", "-check_food_time", "-check", action="store_true", help="Checks the current food time, the time the food was eaten, using the module Food_Time.py.")

script_selector_parser.add_argument("-friends_manager", "--friends_manager", "--friends-manager", "-friends", "--friends", "-friend", "--friend", "-amigos", "-amigo", action="store_true", help="Runs the Friends_Manager.py script.")

script_selector_parser.add_argument("-gameplayer", "--gameplayer", "-gp", "-games", "-jogos", "-jogar", action="store_true", help="Runs the GamePlayer.py script.")

script_selector_parser.add_argument("-music_database", "--music_database", "--music-database", action="store_true", help="Runs the Music_Database.py script.")

script_selector_parser.add_argument("-project_zomboid_manager", "-project_zomboid", "-zomboid", "-project-zomboid", action="store_true", help="Runs the Project_Zomboid_Manager.py script.")

script_selector_parser.add_argument("-python_module_manager", "-python", "-module-manager", action="store_true", help="Runs the Python_Module_Manager.py script.")

script_selector_parser.add_argument("-social_networks", "--social_networks", action="store_true", help="Runs the Social_Networks.py script.")

script_selector_parser.add_argument("-sproutgigs", "--sproutgigs", action="store_true", help="Runs the SproutGigs.py script.")

script_selector_parser.add_argument("-story_manager", "--story-manager", "-stories", "--stories", "-storymanager", "-story", "-histórias", "-história", action="store_true", help="Runs the Story_Manager.py script.")

script_selector_parser.add_argument("-study", "--study", action="store_true", help="Runs the Study.py script.")

script_selector_parser.add_argument("-tasks", "--tasks", "-task", "--task", "-tarefa", "-tarefas", action="store_true", help="Runs the Tasks.py script.")

script_selector_parser.add_argument("-text_generator", "-textgenerator", "--text-generator", "-text", "-texto", action="store_true", help="Runs the Text_Generator.py script.")

script_selector_parser.add_argument("-unified_remote_manager", action="store_true", help="Runs the Unified_Remote_Manager.py script.")

script_selector_parser.add_argument("-watch_history", "--watch-history", "-watch-history", "-watch", "--watch", "-assistir", "-audiovisual_media_network", "-watch_3", action="store_true", help="Runs the Watch_History.py function.")

#script_selector_parser.add_argument("-media_network_manager", "-media_network", "-mnm", "-rede_de_midia", action="store_true", help="Runs the Media_Network_Manager.py script.")

script_selector_parser.add_argument("-year_summary_manager", "-year-summary", "-year_summary", "-manage_year", "-gerenciador_de_sumário_de_ano", "-gerenciador_de_sumario_de_ano", "-gerenciar_ano", action="store_true", help="Runs the Year_Data_Manager.py script.")

add_argument = ""

script_selector_arguments = script_selector_parser.parse_args()

if script_selector_arguments.block_websites:
	import Block_Websites

	Block_Websites.Function_Choose()

if script_selector_arguments.christmas:
	import Christmas

	Christmas.Christmas()

if script_selector_arguments.code:
	import Code

	Code.Function_Choose()

if script_selector_arguments.update_websites:
	from Code.Update_Websites import Update_Websites

	Update_Websites()

if script_selector_arguments.diary:
	import Diary

	Diary.Function_Choose()

if script_selector_arguments.diary_slim:
	import Diary_Slim

	Diary_Slim.Function_Choose()

if script_selector_arguments.food_time:
	import Food_Time

	if script_selector_arguments.sfdt:
		Food_Time.Food_Time()

	if script_selector_arguments.cfdt:
		Food_Time.Food_Time(register_time = False)

if script_selector_arguments.friends_manager:
	import Friends_Manager

	Friends_Manager.Function_Choose()

if script_selector_arguments.gameplayer:
	import GamePlayer

	GamePlayer.Play_Game()

if script_selector_arguments.music_database:
	import Music_Database

	Music_Database.Function_Choose()

if script_selector_arguments.project_zomboid_manager:
	import Project_Zomboid_Manager

	Project_Zomboid_Manager.Function_Choose()

if script_selector_arguments.python_module_manager:
	import Python_Module_Manager

	Python_Module_Manager.Function_Choose()

if script_selector_arguments.social_networks:
	import Social_Networks

	Social_Networks.Function_Choose()

if script_selector_arguments.sproutgigs:
	import SproutGigs

	SproutGigs.SproutGigs()

if script_selector_arguments.story_manager:
	import Story_Manager

	Story_Manager.Function_Choose()

if script_selector_arguments.study:
	import Study

	Study.Function_Choose()

if script_selector_arguments.tasks:
	import Tasks

	Tasks.Function_Choose()

if script_selector_arguments.text_generator:
	import Text_Generator

	Text_Generator.Choose()

if script_selector_arguments.unified_remote_manager:
	import Unified_Remote_Manager

	Unified_Remote_Manager.Function_Choose()

if script_selector_arguments.watch_history:
	import Watch_History

	Watch_History.Function_Choose()

if script_selector_arguments.year_summary_manager:
	import Year_Summary_Manager

	Year_Summary_Manager.Function_Choose()

'''
if script_selector_arguments.media_network_manager:
	import Media_Network_Manager

	Media_Network_Manager.Function_Choose()
'''
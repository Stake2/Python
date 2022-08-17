import Diario
import Food_Time
import GamePlayer
import Tasks
import Tasks_Class
import Watch_History
import Water
import Website_Bot
import Text_Generator

from Script_Helper import *

import argparse

script_selector_parser = argparse.ArgumentParser()
script_selector_parser.add_argument("-block", "-b", action="store_true", help="Blocks the function selection feature.")
script_selector_parser.add_argument("-lang", "-language", action="store", help="""Selects the language of the script, options: 
ptbr (Brazilian Portuguese)
enus (English).""")

script_selector_parser.add_argument("-diario", "-d", "-diary", "-diário", action="store_true", help="Runs the Diario.py function.")

script_selector_parser.add_argument("-water", "-wt", "-agua", "-água", action="store_true", help="Runs the Water.py script.")
script_selector_parser.add_argument("-awt", "-awater", "-addwater", "-add--water", "-adicionaragua", "-adicionarágua", "-adicionar--agua", "-adicionar--água", action="store_true", help="Adds to the water consumed on the current day, using the module Water.py.")
script_selector_parser.add_argument("-cwt", "-cwater", "-checkwater", "-check--water", "-checaragua", "-checarágua", "-checar--agua", "-checar--água", "-ver--agua", "-ver--água", "-veragua","-verágua", action="store_true", help="Checks the water consumed on the current day, using the module Water.py.")
script_selector_parser.add_argument("-rwt", "-rwater", "-resetwater", "-reset--water", "-resetaragua", "-resetarágua", "-resetar--agua", "-resetar--água", "-redefinir--agua", "-redefinir--água", "-redefiniragua","-redefinirágua", action="store_true", help="Resets the water consumed on the current day, using the module Water.py.")

script_selector_parser.add_argument("-foodtime", "-fdtime", "-fdt", "-food--time", "-food_time", "-tempodacomida", "-tempo--da--comida", "-tempocomida", "-tempo--comida", action="store_true", help="Runs the Food_Time.py script.")
script_selector_parser.add_argument("-sfdt", "-sfdtime", "-setfoodtime", "-set--food--time", "-setartempodacomida", "-setar--tempo--da--comida", "-marcartempoquecomeu", action="store_true", help="Sets the current food time, the time the food was eaten, using the module Food_Time.py.")
script_selector_parser.add_argument("-cfdt", "-cfdtime", "-checkfoodtime", "-check--food--time", "-checktime", "-checartempodacomida", "-checar--tempo--da--comida", "-checartempocomida", action="store_true", help="Checks the current food time, the time the food was eaten, using the module Food_Time.py.")

script_selector_parser.add_argument("-gameplayer", "-gp", "-games", "-jogos", "-listadejogos", "-lista--de--jogos", "-listar--jogos", "-jogador--de--jogos", "-jogadordejogos", "-jogador_de_jogos", action="store_true", help="Runs the GamePlayer.py script.")
script_selector_parser.add_argument("-nostop", "-nstp", "-no_stop", "-semparar", "-sem_parar", "-sem--parar", action="store", help="Turns the NoStop option on or off for the module GamePlayer.py.")
script_selector_parser.add_argument("-minutestyle", "-minstyle", "-gameplayer_minute_style", "-estilominuto", action="store", help="Turns the MinuteStyle option on or off for the module GamePlayer.py.")
script_selector_parser.add_argument("-fast", "-fst", "-fastmode", "-fast--mode", "-modorapido", "-modorápido", action="store", help="Turns the FastMode option on or off for the module GamePlayer.py.")
script_selector_parser.add_argument("-mulfldr", "-multifldr", "-multifolder", "-multipasta", action="store", help="Turns the MinuteStyle option on or off for the module GamePlayer.py.")

script_selector_parser.add_argument("-bot", "-robo", "-robô", action="store_true", help="Runs the Website_Bot.py script.")
script_selector_parser.add_argument("-bf", "-botf", "-botfunc", "-botfunction", "-funçãodorobô", "-funcaodorobo", action="store", help="Runs the selected function using the Website_Bot.py script.")
script_selector_parser.add_argument("-sbot", "-selectedbot", "-selected--bot", "-botselecionado", "-bot--selecionado", action="store", help="Runs the selected function using the Website_Bot.py script.")

script_selector_parser.add_argument("-tasks", "-task", "-tarefa", "-tarefas", action="store_true", help="Runs the Tasks.py script.")
script_selector_parser.add_argument("-tasks_class", "-task_class", "-tarefa_classe", "-tarefas_classe", action="store_true", help="Runs the Tasks_Class.py script.")

script_selector_parser.add_argument("-watch_class", "-watch", "-assistir_classe", "-watchclassscript", "-watch_3", action="store_true", help="Runs the Watch_Class.py function.")

script_selector_parser.add_argument("-text_generator", "-textgenerator", "-text--generator", action="store_true", help="Runs the Text_Generator.py script.")

script_selector_arguments = script_selector_parser.parse_args()

no_stop_option = script_selector_arguments.nostop

has_arguments = False

blocking_scripts = False

if script_selector_arguments.block:
	print("Blocking other scripts.")

	blocking_scripts = True

	file = smallthingsdonefile
	open_file = o(file, "r")
	filetext = open_file.readlines()
	open_file.close()

	print(filetext[-1])

if script_selector_arguments.diario:
	has_arguments = True

	import Diario

	Diario.Choose()

if script_selector_arguments.water:
	has_arguments = True

	import Water

	if script_selector_arguments.lang:
		Water.SetLanguage(script_selector_arguments.lang)

	else:
		Water.SetLanguage(global_language)

	Water.Set_Water_Day()

	if script_selector_arguments.cwt:
		Water.CheckWater()

	if script_selector_arguments.awt:
		Water.Add_Water()

	if script_selector_arguments.rwt:
		Water.Reset_Water()

if script_selector_arguments.foodtime:
	has_arguments = True

	import Food_Time

	if script_selector_arguments.sfdt:
		Food_Time.Set_Food_Time()

	if script_selector_arguments.cfdt:
		Food_Time.Check_Food_Time()

if script_selector_arguments.gameplayer:
	has_arguments = True

	import GamePlayer

	script_name = "GamePlayer.py"

	try:
		GamePlayer.Play_Game()

	except KeyboardInterrupt:
		GamePlayer.Register_Played_Time_To_File()

if script_selector_arguments.bot:
	has_arguments = True

	import Website_Bot

	if script_selector_arguments.bf:
		if str(script_selector_arguments.bf) == "wattpad_log_all_messages":
			Website_Bot.Wattpad_Bot_LogAllMessagesSS()

		if str(script_selector_arguments.bf) == "run_discord_bot":
			Website_Bot.Run_Discord_Bot()

		if str(script_selector_arguments.bf) == "discord_bot":
			Website_Bot.Run_Discord_Bot()

		if str(script_selector_arguments.bf) == "run discord bot":
			Website_Bot.Run_Discord_Bot()

		if str(script_selector_arguments.bf) == "discord bot":
			Website_Bot.Run_Discord_Bot()

if script_selector_arguments.tasks:
	has_arguments = True

	import Tasks

	Tasks.Choose()

if script_selector_arguments.tasks_class:
	has_arguments = True

	import Tasks_Class

	Tasks_Class.Function_Choose()

if script_selector_arguments.watch_class:
	has_arguments = True

	watch_script_name = "Watch_History.py"

	import Watch_History

	Watch_History.Function_Choose()

if script_selector_arguments.text_generator:
	has_arguments = True

	import Text_Generator

	Text_Generator.Choose()
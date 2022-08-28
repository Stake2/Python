# Block_Websites.py

from Script_Helper import *

import os

class Block_Websites(object):
	def __init__(self, parameter_switches = None):
		# Verbose variable
		self.verbose = False

		self.testing_script = False

		self.parameter_switches = parameter_switches

		self.Define_Basic_Variables()
		self.Define_Folders()
		self.Define_Files()
		self.Define_Texts()
		self.Define_Lists()

	def Define_Basic_Variables(self):
		self.option = True

		# Global Switches dictionary
		self.global_switches = {
			"write_to_file": self.option,
			"create_files": self.option,
			"create_folders": self.option,
			"move_files": self.option,
			"verbose": self.verbose,
		}

		self.global_switches["testing_script"] = self.testing_script

		if self.parameter_switches != None:
			self.global_switches = self.parameter_switches
			self.testing_script = self.global_switches["testing_script"]

		if self.global_switches["testing_script"] == True:
			print(Language_Item_Definer("Testing script: Yes", "Testando script: Sim"))

		if self.global_switches["verbose"] == True:
			print(Language_Item_Definer("Verbose on", "Verbose ligado") + ".")

		if self.global_switches["testing_script"] == True:
			self.global_switches["write_to_file"] = False
			self.global_switches["create_files"] = False

		self.dot_text = ".txt"

	def Define_Folders(self):
		name = __name__

		if "." in __name__:
			name = __name__.split(".")[0]

		self.module_text_files_folder = script_text_files_folder + name + "/"
		Create_Folder(self.module_text_files_folder, self.global_switches)

		self.module_folder = scripts_modules_folder + name + "/"

		self.system32_folder = Sanitize_File_Path(os.environ["COMSPEC"].replace("cmd.exe", ""))

		self.drivers_etc_folder = self.system32_folder + "drivers/etc/"

		self.database_folder = self.module_text_files_folder + "Database/"
		Create_Folder(self.database_folder, self.global_switches)

		self.database_domains_folder = self.database_folder + "Domains/"
		Create_Folder(self.database_domains_folder, self.global_switches)

		self.database_websites_folder = self.database_folder + "Websites/"
		Create_Folder(self.database_websites_folder, self.global_switches)

		self.allowed_to_unblock_folder = self.database_websites_folder + "Allowed To Unblock/"
		Create_Folder(self.allowed_to_unblock_folder, self.global_switches)

	def Define_Files(self):
		self.hosts_file = self.drivers_etc_folder + "hosts"

		self.hour_config_file = self.module_text_files_folder + "Hour Config" + self.dot_text
		Create_Text_File(self.hour_config_file, self.global_switches)

		self.blocked_by_default_file = self.module_text_files_folder + "Blocked By Default" + self.dot_text
		Create_Text_File(self.blocked_by_default_file, self.global_switches)

		self.additional_map_file = self.module_text_files_folder + "Additional Map" + self.dot_text
		Create_Text_File(self.additional_map_file, self.global_switches)

		self.websites_to_block_file = self.database_websites_folder + "To Block" + self.dot_text
		Create_Text_File(self.websites_to_block_file, self.global_switches)

		self.allowed_to_unlock_by_user_file = self.allowed_to_unblock_folder + "By User" + self.dot_text
		Create_Text_File(self.allowed_to_unlock_by_user_file, self.global_switches)

		self.allowed_to_unlock_by_modules_file = self.allowed_to_unblock_folder + "By Modules" + self.dot_text
		Create_Text_File(self.allowed_to_unlock_by_modules_file, self.global_switches)

		self.log_file = self.module_text_files_folder + "Log" + self.dot_text
		Create_Text_File(self.log_file, self.global_switches)

	def Define_Texts(self):
		self.hosts_file_header = """# Copyright (c) 1993-2009 Microsoft Corp.
#
# This is a sample HOSTS file used by Microsoft TCP/IP for Windows.
#
# This file contains the mappings of IP addresses to host names. Each
# entry should be kept on an individual line. The IP address should
# be placed in the first column followed by the corresponding host name.
# The IP address and the host name should be separated by at least one
# space.
#
# Additionally, comments (such as these) may be inserted on individual
# lines or following the machine name denoted by a '#' symbol.
#
# For example:
#
#      102.54.94.97     rhino.acme.com   # source server
#       38.25.63.10     x.acme.com       # x client host
#
# localhost name resolution is handled within DNS itself.
#	127.0.0.1       localhost
#	::1      localhost

"""

		self.redirect_ip = "127.0.0.1"
		self.redirect_ip_space = self.redirect_ip + "     "

		self.task_name = "Re-Block Websites"

		self.website_unblocked_text = Language_Item_Definer("Website unblocked", "Site desbloqueado")

		self.reason_to_unlock_text = Language_Item_Definer("Reason to unlock", "Razão para liberar")

		self.the_websites_are_text = Language_Item_Definer("The websites are", "Os sites estão") + " "

		self.websites_to_block_header = "\n" + "## Websites to be blocked by conditions" + "\n" + "#" + "\n\n"

		self.working_time_text = Language_Item_Definer("working time", "horário de trabalho")

		self.not_in_working_hours_text = Language_Item_Definer("You are not in {}, all websites are unlocked", "Você não está em {}, todos os sites estão desbloqueados").format(self.working_time_text)

		self.log_texts = {}
		self.log_texts["Blocking State"] = Language_Item_Definer("Blocking State", "Estado de Bloqueio") + ": \n"
		self.log_texts["Blocked"] = Language_Item_Definer(self.the_websites_are_text + "locked because you are in " + self.working_time_text, self.the_websites_are_text + "bloqueados porque você está " + self.working_time_text)
		self.log_texts["Unlocked"] = Language_Item_Definer(self.the_websites_are_text + "unlocked because you are not in " + self.working_time_text, self.the_websites_are_text + "desbloqueados porque você não está no " + self.working_time_text)
		self.log_texts["Log"] = self.log_texts["Blocking State"] + "{}" + "." + "\n\n" + Language_Item_Definer("This file will be updated every {} minutes, reopen it to update", "Este arquivo vai ser atualizado a cada {} minutos, reabra-o para atualizar") + "." + "\n" + Language_Item_Definer("Last update in", "Última atualização em") + ": {}"

	def Define_Lists(self):
		self.blocked_by_default = Create_Array_Of_File(self.blocked_by_default_file)

		self.additional_maps = Create_Array_Of_File(self.additional_map_file)

		self.websites_to_block = Create_Array_Of_File(self.websites_to_block_file)

		self.allowed_to_unlock_by_user = Make_Setting_Dictionary(Create_Array_Of_File(self.allowed_to_unlock_by_user_file))
		self.allowed_to_unlock_by_modules = Make_Setting_Dictionary(Create_Array_Of_File(self.allowed_to_unlock_by_modules_file))

		self.allowed_to_unlock = {}
		self.allowed_to_unlock["User"] = self.allowed_to_unlock_by_user
		self.allowed_to_unlock["Modules"] = self.allowed_to_unlock_by_modules

		self.domain_folders = {}

		for website in self.websites_to_block:
			self.domain_folders[website] = self.database_domains_folder + website + "/"
			Create_Folder(self.domain_folders[website])

		self.domain_files = {}

		for website in self.websites_to_block:
			self.domain_files[website] = self.domain_folders[website] + "Domains" + self.dot_text
			Create_Text_File(self.domain_files[website])

		self.map_dict = {
		"Blocked By Default": self.blocked_by_default,
		"Additional Maps": self.additional_maps,
		}

		self.hour_config = Make_Setting_Dictionary(self.hour_config_file, convert_to = int, read_file = True)
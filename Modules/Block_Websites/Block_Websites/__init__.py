# Block_Websites.py

from Global_Switches import Global_Switches as Global_Switches

from Language import Language as Language
from File import File as File
from Folder import Folder as Folder
from Date import Date as Date
from Input import Input as Input
from Text import Text as Text

class Block_Websites(object):
	def __init__(self, parameter_switches = None):
		self.parameter_switches = parameter_switches

		self.Define_Basic_Variables()
		self.Define_Module_Folder()
		self.Define_Texts()

		from Social_Networks.Social_Networks import Social_Networks as Social_Networks
		self.Social_Networks = Social_Networks()

		self.Define_Files()
		self.Define_Lists()

	def Define_Basic_Variables(self):
		# Global Switches dictionary
		self.global_switches = Global_Switches().global_switches

		if self.parameter_switches != None:
			self.global_switches.update(self.parameter_switches)

		self.Language = Language(self.global_switches)
		self.File = File(self.global_switches)
		self.Folder = Folder(self.global_switches)
		self.Date = Date(self.global_switches)
		self.Input = Input(self.global_switches)
		self.Text = Text(self.global_switches)

		self.app_settings = self.Language.app_settings
		self.small_languages = self.Language.languages["small"]
		self.full_languages = self.Language.languages["full"]
		self.translated_languages = self.Language.languages["full_translated"]

		self.user_language = self.Language.user_language
		self.full_user_language = self.Language.full_user_language

		self.Sanitize = self.File.Sanitize

		self.folders = self.Folder.folders
		self.root_folders = self.folders["root"]
		self.user_folders = self.folders["user"]
		self.apps_folders = self.folders["apps"]
		self.mega_folders = self.folders["mega"]
		self.notepad_folders = self.folders["notepad"]

		self.date = self.Date.date

	def Define_Module_Folder(self):
		name = self.__module__

		if "." in name:
			name = name.split(".")[0]

		if name == "__main__":
			name = "Block_Websites"

		self.module_folder = self.apps_folders["modules"]["root"] + name + "/"
		self.Folder.Create(self.module_folder)

		self.module_text_files_folder = self.apps_folders["app_text_files"] + name + "/"
		self.Folder.Create(self.module_text_files_folder)

		self.texts_file = self.module_text_files_folder + "Texts.json"
		self.File.Create(self.texts_file)

	def Define_Texts(self):
		self.large_bar = "-----"
		self.dash_space = "-"

		self.texts = self.Language.JSON_To_Python(self.texts_file)

		self.language_texts = self.Language.Item(self.texts)

		self.texts["redirect_ip"] = "127.0.0.1"
		self.texts["redirect_ip_space"] = self.texts["redirect_ip"] + "     "
		self.texts["task_name"] = "Re-Block Websites"
		self.texts["websites_to_block_header"] = "\n## Websites to be blocked by conditions\n#\n\n"
		self.texts["log"] = self.language_texts["blocking_state"] + ":\n{}\n\n" + self.language_texts["this_file_will_be_updated_every_{}_minutes_reopen_it_to_update"] + ".\n" + self.language_texts["last_update_in"] + ": {}"

	def Define_Files(self):
		self.hosts_file = self.root_folders["system32"]["drivers/etc"] + "hosts"

		self.additional_maps_file = self.module_text_files_folder + "Additional maps.txt"
		self.File.Create(self.additional_maps_file)

		self.blocked_by_default_file = self.module_text_files_folder + "Blocked by default.txt"
		self.File.Create(self.blocked_by_default_file)

		self.hosts_file_header_file = self.module_text_files_folder + "Hosts file header.txt"
		self.File.Create(self.hosts_file_header_file)

		self.hour_config_file = self.module_text_files_folder + "Hour config.txt"
		self.File.Create(self.hour_config_file)

		self.log_file = self.module_text_files_folder + "Log.txt"
		self.File.Create(self.log_file)

		# Social Networks Folder and Files
		self.social_networks_text_folder = self.Social_Networks.social_networks_text_folder

		self.social_networks_file = self.Social_Networks.social_networks_file

	def Define_Lists(self):
		self.hosts_file_header = self.File.Contents(self.hosts_file_header_file)["string"]

		self.blocked_by_default = self.File.Contents(self.blocked_by_default_file)["lines"]

		self.additional_maps = self.File.Contents(self.additional_maps_file)["lines"]

		self.websites_to_block = self.File.Contents(self.social_networks_file)["lines"]
		self.websites_to_block.remove("Habitica")

		self.domains = {}

		i = 0
		for website in self.websites_to_block:
			self.domains_file = self.social_networks_text_folder + website + "/Additional Domains.txt"

			self.domains[website] = self.File.Contents(self.domains_file)["lines"]

			i += 1

		self.map_dict = {
			"Blocked by default": self.blocked_by_default,
			"Additional maps": self.additional_maps,
		}

		self.hour_config = self.File.Dictionary(self.hour_config_file, convert = int)
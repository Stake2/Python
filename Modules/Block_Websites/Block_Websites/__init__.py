# Block_Websites.py

class Block_Websites(object):
	def __init__(self):
		self.Define_Basic_Variables()

		self.module = {
			"name": self.__module__.split(".")[0],
			"key": self.__module__.split(".")[0].lower().replace(" ", "_")
		}

		if self.module["name"] == "__main__":
			self.module["name"] = "Block_Websites"
			self.module["key"] = self.module["name"].lower().replace(" ", "_")

		# Define module folders
		from Utility.Define_Folders import Define_Folders as Define_Folders

		Define_Folders(self)

		self.folders["apps"]["modules"][self.module["key"]] = self.Folder.Contents(self.folders["apps"]["modules"][self.module["key"]]["root"], lower_key = True)["dictionary"]

		self.Define_Texts()

		from Social_Networks.Social_Networks import Social_Networks as Social_Networks
		self.Social_Networks = Social_Networks()

		self.Define_Files()
		self.Define_Lists()

	def Define_Basic_Variables(self):
		from Utility.Global_Switches import Global_Switches as Global_Switches

		from Utility.File import File as File
		from Utility.Folder import Folder as Folder
		from Utility.Date import Date as Date
		from Utility.Input import Input as Input
		from Utility.JSON import JSON as JSON
		from Utility.Text import Text as Text

		self.switches = Global_Switches().switches["global"]

		self.File = File()
		self.Folder = Folder()
		self.Date = Date()
		self.Input = Input()
		self.JSON = JSON()
		self.Text = Text()

		self.languages = self.JSON.Language.languages

		self.user_language = self.JSON.Language.user_language
		self.full_user_language = self.JSON.Language.full_user_language

		self.Sanitize = self.File.Sanitize

		self.folders = self.Folder.folders

		self.date = self.Date.date

	def Define_Texts(self):
		self.large_bar = "-----"
		self.dash_space = "-"

		self.texts = self.JSON.To_Python(self.folders["apps"]["module_files"][self.module["key"]]["texts"])

		self.language_texts = self.JSON.Language.Item(self.texts)

		self.texts["redirect_ip"] = "127.0.0.1"
		self.texts["redirect_ip_space"] = self.texts["redirect_ip"] + "     "
		self.texts["task_name"] = "Re-Block Websites"
		self.texts["all_websites_are_unlocked_header"] = "# All websites are unlocked"
		self.texts["log"] = self.language_texts["blocking_state"] + ":\n{}\n\n" + self.language_texts["this_file_will_be_updated_every_{}_minutes_reopen_it_to_update"] + ".\n" + self.language_texts["last_update_in"] + ": {}"

		self.texts["header"] = "#######################################" + "\n" \
		"#          " + "Block_Websites.py" + "          #" + "\n" + \
		"#######################################" + "\n\n"

	def Define_Files(self):
		self.hosts_file = self.folders["root"]["system32"]["drivers/etc"] + "hosts"

		self.additional_maps_file = self.folders["apps"]["module_files"][self.module["key"]]["root"] + "Additional maps.txt"
		self.File.Create(self.additional_maps_file)

		self.blocked_by_default_file = self.folders["apps"]["module_files"][self.module["key"]]["root"] + "Blocked by default.txt"
		self.File.Create(self.blocked_by_default_file)

		self.hosts_file_header_file = self.folders["apps"]["module_files"][self.module["key"]]["root"] + "Hosts file header.txt"
		self.File.Create(self.hosts_file_header_file)

		self.hour_config_file = self.folders["apps"]["module_files"][self.module["key"]]["root"] + "Hour config.txt"
		self.File.Create(self.hour_config_file)

		self.log_file = self.folders["apps"]["module_files"][self.module["key"]]["root"] + "Log.txt"
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
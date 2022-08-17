# Open_Data_File_Of_Media.py

# Script Helper importer
from Script_Helper import *

from Watch_History.Watch_History import Watch_History as Watch_History

from Watch_History.Select_Media_Type_And_Media import Select_Media_Type_And_Media as Select_Media_Type_And_Media

class Open_Data_File_Of_Media(Watch_History):
	def __init__(self):
		super().__init__()

		self.choice_info = Select_Media_Type_And_Media(custom_media_array = "all")

		self.media_details_file = self.choice_info.media_details_file

		print(Language_Item_Definer("Opening this Media Details file", "Abrindo esse arquivo de Detalhes de Mídia") + ": ")
		print(self.media_details_file)

		Open_Text_File(self.media_details_file)
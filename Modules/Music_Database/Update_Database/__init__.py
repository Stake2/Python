# Update_Database.py

from Script_Helper import *

from Music_Database.Music_Database import Music_Database as Music_Database

class Update_Database(Music_Database):
	def __init__(self):
		super().__init__()

		self.Update()

	def Update(self):
		print(Language_Item_Definer("The Music Library Database files were updated succesfully", "Os arquivos do Banco de Dados da Biblioteca de Música foram atualizados com sucesso") + ".")
# Play_Alarm.pyw

from Food_Time.Food_Time import Food_Time as Food_Time

class Play_Alarm(Food_Time):
	def __init__(self):
		super().__init__(show_text = False)

		# Define alarm sound file
		self.alarm_file = self.apps_folders["app_text_files"][self.module["key"]]["root"] + "Air horn sound effects meme 2018.mp3"

		# Open alarm sound file on browser
		import subprocess
		subprocess.Popen('"C:\Program Files (x86)\Mozilla Firefox\Firefox.exe" ' + '"' + "file:///" + self.alarm_file + '"')

if __name__ == "__main__":
	Play_Alarm()
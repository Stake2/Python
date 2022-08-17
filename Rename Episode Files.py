from Script_Helper import *
from os.path import expanduser
import re

downloads_folder = Sanitize_File_Path(expanduser("~")) + "Downloads/"
equestria_girls_folder = Sanitize_File_Path(r"C:\Mídias\My Little Pony Equestria Girls\Better Together S01\Dublado")

number_file = downloads_folder + "Number.txt"
Create_Text_File(number_file)
number = int(Create_Array_Of_File(number_file)[0])

episodes_file = r"C:\Mega\My Little Pony\Friendship Is Magic\Texts - Textos\Português Brasileiro\Lista de Episódios\Equestria Girls\Com Seções.txt"
episode_titles = Create_Array_Of_File(episodes_file, add_none = True)

files = List_Files(downloads_folder, add_none = False)

youtube_id = False

for file in files:
	if ".description" in file:
		youtube_id = file

		if "youtube-1280x720-" in youtube_id:
			youtube_id = youtube_id.split("youtube-1280x720-")[-1]

		extensions = ["mkv", "webm", "description", "jpg", "json"]

		for extension in extensions:
			if "." + extension in youtube_id:
				youtube_id = youtube_id.split("." + extension)[0]

		if len(youtube_id) == 11:
			youtube_link = "https://www.youtube.com/watch?v=" + youtube_id

			for file in files:
				if ".description" in file and youtube_link not in Read_String(file):
					Append_To_File(file, "\n\n" + youtube_link)

episode_title = re.sub(" \([0-9][0-9]-[0-9][0-9]-[0-9][0-9][0-9][0-9]\)", "", episode_titles[number])

for old_file in files:
	if youtube_id != False and youtube_id in old_file:
		new_file = re.sub("MLP.*-youtube-.*-" + youtube_id, Remove_Non_File_Characters(episode_title), old_file)
		new_file = new_file.replace(downloads_folder, equestria_girls_folder)
		Move_File(old_file, new_file)
		print()
		print(episode_title)
		print(new_file)

		Write_To_File(number_file, str(number + 1))
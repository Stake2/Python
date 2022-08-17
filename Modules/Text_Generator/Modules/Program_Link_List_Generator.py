import pyperclip

program_names = [
"MegaSync",
"Mozilla Firefox",
"Tor Project",
"Lightshot",
"Foobar2000",
"Notepad++",
"Python",
"ConEmu",
"XAMPP",
"Speccy",
"Winrar",
"Java Windows",
["VLC Media Player", "vlc-protocol-master"],
"MPV",
"MPV.net",
"mps-youtube",
"Syncplay",
"Youtube-DL",
"Youtube-DLG-0.4",
"4K Video Downloader",
"FastStone Image Viewer",
"FastStone MaxView",
"Discord",
"Slack Desktop App",
"Free Download Manager 3.9",
"HTTracker",
"FormatFactory",
"AntRenamer",
"Advanced Renamer",
"Everything",
"FreeFileSync",
"Audacity",
["FL Studio 12", "Xfer Serum", "Drum Pack"],
"Steam",
"Git",
"RobotSoft Mouse And Keyboard Recorder",
"Gif Animator",
"Bandicam",
"Sony Vegas Pro 11, 12",
"Paint Tool SAI ver 1.1.0",
"MediBang Paint",
"Windows Loader 2.2.2 By Daz",
"7+ Taskbar Tweaker",
"Daemon Tools Lite",
"Hamachi",
"TeamViewer",
"AnyDesk",
"Input Director",
"Cold Turkey - The only blocker for distracting websites that actually works. (even doesn't let you uninstall it when blocking is active)",
"Flux - Automatically adjust your computer screen to match lighting",
"Keypirinha - A fast launcher for keyboard ninjas on Windows. You can think of Keypirinha as an alternative to Launchy and a cousin of Alfred",
"Dropit",
]

program_links = [
"https://mega.nz/downloadapp",
"https://www.mozilla.org/en-US/firefox/new/",
"https://www.torproject.org/download/",
"https://app.prntscr.com/en/download.html",
"https://foobar2000.org/download",
"https://notepad-plus-plus.org/download/",
["https://www.python.org/downloads/", "https://github.com/winpython/winpython"],
"https://conemu.github.io/en/Downloads.html",
["https://www.apachefriends.org/index.html", "https://sourceforge.net/projects/xampp/files/XAMPP%20Windows/7.3.2/xampp-win32-7.3.2-0-VC15-installer.exe/download"],
"https://www.ccleaner.com/speccy/download",
["https://rarlab.com/download.htm", "https://thepiratebay.org/torrent/32161984/WinRAR_5.71_FINAL___Key_[TheWindowsForum]"],
"https://www.java.com/en/download/win10.jsp",
["https://www.videolan.org/vlc/", "https://github.com/stefansundin/vlc-protocol"],
"https://mpv.io/installation/",
"https://github.com/stax76/mpv.net/releases",
"https://github.com/mps-youtube/mps-youtube/releases",
"https://syncplay.pl/download/",
"https://github.com/ytdl-org/youtube-dl/",
"https://mrs0m30n3.github.io/youtube-dl-gui/",
"https://www.4kdownload.com/products/product-videodownloader",
["https://www.faststone.org/FSIVDownload.htm", "https://thepiratebay.org/description.php?id=33626221"],
"https://thepiratebay.org/description.php?id=17815380",
"https://discord.com/download",
"https://slack.com/intl/en-br/downloads/instructions/windows",
"https://www.freedownloadmanager.org/download.htm",
"https://www.httrack.com/page/2/en/index.html",
"https://format-factory.en.softonic.com/download",
"https://www.antp.be/software/renamer/download",
"https://www.advancedrenamer.com/download",
"https://www.voidtools.com/downloads/",
"https://freefilesync.org/download.php",
"https://www.audacityteam.org/download/",
[["https://thepiratebay.org/description.php?id=14681048",
"https://thepiratebay.org/description.php?id=14681048"],
["https://thepiratebay.org/description.php?id=16653364"],
["https://audioz.download/samples/104778-download_cymatics-terror-drums-for-dubstep-with-bonuses-wav.html",
"https://vsthouse.ru/load/semply_presety/semply/cymatics_terror_drums_for_dubstep_wav_sehmply_dubstep_sehmply_udarnykh/14-1-0-14164"]],
"https://store.steampowered.com/about/",
"https://git-scm.com/download/win",
"https://thepiratebay.org/description.php?id=7126909",
"https://www.gif-animator.com/",
"https://thepiratebay.org/description.php?id=30567036",
["https://kickass.sx/torrent/sony-vegas-pro-11-0-682-32-bit-patch-keygen-di-chingliu-t335775.html", "https://mega.nz/file/rkVHFSjD#plbtO1fKoW-np2LyZdHTO_Bj7AXRZhPqxyEeeSHpWhI"],
["https://kickass.sx/torrent/easy-paint-tool-sai-ver-1-1-0-t3307978.html",
"https://www.systemax.jp/en/sai/",
"https://www.systemax.jp/bin/sai-1.2.5-ful-en.exe"],
["https://medibangpaint.com/en/app-download/",
"https://medibangpaint.com/static/installer/MediBangPaintPro/MediBangPaintProSetup-25.3-32bit.exe"],
"https://officialkmspico.net/Windows_Loader_v.2.2.2.rar",
"https://rammichael.com/7-taskbar-tweaker",
"https://www.daemon-tools.cc/eng/products/dtLite",
"https://vpn.net/",
"https://www.teamviewer.com/en/download/windows/",
"https://anydesk.com/en/downloads",
"https://inputdirector.com/downloads.html",
["https://getcoldturkey.com/",
"https://kickass.sx/torrent/cold-turkey-blocker-pro-v3-10-activator-flrv-t3983775.html"],
"https://justgetflux.com/",
"https://keypirinha.com/",
"https://www.dropitproject.com/",
]

all_programs = ""

i = 0
text_number = 0
for program_name in program_names:
	if type(program_links[i]) != list:
		name_string = str(text_number + 1) + " - " + program_name + " - " + program_links[i]

		#print(name_string)

		text_number += 1

		if i != len(program_names) - 1:
			all_programs += name_string + "\n"

		if i == len(program_names) - 1:
			all_programs += name_string

	if type(program_links[i]) == list and type(program_name) != list:
		#print()

		program_array = program_links[i]

		#print(str(i + 1) + " - " + program_name)

		if i != len(program_names) - 1:
			all_programs += str(i + 1) + " - " + program_name + "\n"

		if i == len(program_names) - 1:
			all_programs += str(i + 1) + " - " + program_name

		c = 0
		while c <= len(program_array) - 1:
			array_string = program_array[c]

			if i != len(program_names) - 1:
				all_programs += array_string + "\n"

			if i == len(program_names) - 1:
				all_programs += array_string

			#print(array_string)

			c += 1

		if i != len(program_names) - 1:
			all_programs += "\n"

		text_number += 1

	if type(program_name) == list and type(program_links[i]) == list and type(program_links[i][0]) != list:
		#print(str(text_number + 1) + " - " + program_name[0] + " - " + program_links[i][0])

		if i != len(program_names) - 1:
			all_programs += str(text_number + 1) + " - " + program_name[0] + " - " + program_links[i][0] + "\n"

		if i == len(program_names) - 1:
			all_programs += str(text_number + 1) + " - " + program_name[0] + " - " + program_links[i][0]

		c = 1
		while c <= 1:
			program_name = program_name[c]
			program_link = program_links[i][c]

			if i != len(program_names) - 1:
				all_programs += program_name + " - " + program_link + "\n"

			if i == len(program_names) - 1:
				all_programs += program_name + " - " + program_link

			#print(program_name + " - " + program_link)

			c += 1

		if i != len(program_names) - 1:
			all_programs += "\n"

		text_number += 1

	if type(program_name) == list and type(program_links[i]) == list and type(program_links[i][0]) == list:
		#print(str(text_number + 1) + " - " + program_name[0] + " - " + program_links[i][0])

		#if i != len(program_names) - 1:
			#all_programs += str(text_number + 1) + " - " + program_name[0] + " - " + program_links[i][0][0] + "\n" + "\n"

		#if i == len(program_names) - 1:
			#all_programs += str(text_number + 1) + " - " + program_name[0] + " - " + program_links[i][0][0]

		c = 0
		v = 0
		while c <= len(program_name) - 1:
			selected_program_name = program_name[c]

			if c == 0:
				#print(str(text_number + 1) + " - " + program_name[c])
				all_programs += str(text_number + 1) + " - " + program_name[c]

			if c != 0:
				#print(program_name[c])
				all_programs += program_name[c]

			if i != len(program_names) - 1:
				all_programs += "\n"

			v = 0
			while v <= len(program_links[i][c]) - 1:
				program_link = program_links[i][c][v]

				if i != len(program_names) - 1:
					all_programs += program_link

				if i == len(program_names) - 1:
					all_programs += program_link

				if i != len(program_names) - 1:
					all_programs += "\n"

				v += 1

			if i != len(program_names) - 1:
				all_programs += "\n"

			c += 1

		#c = 1
		#v = 0
		#while c <= 2:
		#	program_name = program_name[v]
		#	program_link = program_links[i][v][v]
		#	print(program_links[i][v][v])
		#
		#	if i != len(program_names) - 1:
		#		all_programs += program_name + " - " + program_link + "\n"
		#
		#	if i == len(program_names) - 1:
		#		all_programs += program_name + " - " + program_link
		#
		#	#print(program_name + " - " + program_link)
		#
		#	c += 1
		#	v += 1

		if i != len(program_names) - 1:
			all_programs += "\n"

		text_number += 1

	i += 1

print()
print(all_programs)

pyperclip.copy(all_programs)
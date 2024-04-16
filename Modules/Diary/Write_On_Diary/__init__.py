# Write_On_Diary.py

from Diary.Diary import Diary as Diary

class Write_On_Diary(Diary):
	def __init__(self):
		super().__init__()

		self.diary_chapter_file = self.File.Contents(self.current_diary_file)["lines"][0]

		print()
		print(self.separators["5"])
		print()
		print(self.language_texts["current_diary_chapter"] + ":")
		print(self.diary_chapter_file)

		self.Select_Presenter()

	def Select_Presenter(self):
		self.show_text = self.language_texts["presenters, title()"]
		self.select_text = self.language_texts["select_a_presenter_to_write_as"]

		self.selected_presenter = self.Input.Select(self.presenters, show_text = self.show_text, select_text = self.select_text)["option"]

		self.Type(self.selected_presenter)

	def Type(self, presenter):
		self.presenter = presenter

		self.format_text = self.presenter_format_texts[self.presenter]
		self.format_text_item = self.format_text.split("{}: ")[-1].replace("{}", "")

		self.presenter_text = None

		while self.presenter_text not in self.finish_texts:
			self.presenter_text = self.Input.Lines(self.presenter + ": " + self.format_text_item, line_options_parameter = {"capitalize": True, "dots": True, "next_line": False})["string"]

			if self.presenter_text not in self.presenter_numbers:
				format_text = self.format_text

				text_to_append = self.Date.Now()["Formats"]["HH:MM DD/MM/YYYY"] + ":" + "\n" + format_text.format(self.presenter, self.presenter_text)

				if self.File.Contents(self.diary_chapter_file)["lines"] != []:
					text_to_append = "\n" + text_to_append

				self.File.Edit(self.diary_chapter_file, text_to_append, "a")

			if self.presenter_text in self.presenter_numbers:
				self.Type(self.presenters[int(self.presenter_text) - 1])
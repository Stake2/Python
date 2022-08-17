# Update_Chapter_Covers.py

# Script Helper importer
from Script_Helper import *

from Story_Manager.Story_Manager import *
from Story_Manager.Post_Chapter import Post_Chapter as Post_Chapter

class Update_Chapter_Covers(Story_Manager):
	def __init__(self):
		super().__init__(runned_function_name = "Update_Chapter_Covers")

		self.module_dict = {
			"story_covers_folder": self.story_covers_folder,
			"website_images_story_covers_folder": self.website_images_story_covers_folder,
			"story_vegas_files_folder": self.story_vegas_files_folder,
			"english_chapter_titles": self.english_chapter_titles,
			"english_chapter_titles_not_none": self.english_chapter_titles_not_none,
			"portuguese_chapter_titles": self.portuguese_chapter_titles,
			"copy_title": False,
			"skip_chapter_cover_creation": False,
		}

		print("---")
		print()
		print(Language_Item_Definer("Updating chapter covers of the story", "Atualizando capas de capítulo da história") + ' "' + self.language_story_name + '"' + "...")
		print()

		Post_Chapter(run_as_module = True, module_dict = self.module_dict)

		print("---")
		print()
		print(Language_Item_Definer("Finished updating the chapter covers", "Terminou de atualizar as capas de capítulos") + ".")
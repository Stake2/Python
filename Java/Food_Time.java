import print.print;
import functions.functions;
import language.language;

import java.util.*;
import java.io.IOException;

public class Food_Time {
	String dot_text = ".txt";

	static Map<String, Boolean> global_switches = new HashMap<String, Boolean>();

	String food_time_folder = "C:/Mega/Bloco De Notas/Dedicação/Food and Water Registers/Food Times/";

	String english_food_file = food_time_folder + "Time that I finished eating" + dot_text;
	String portuguese_food_file = food_time_folder + "Tempo que terminei de comer" + dot_text;

	String food_file = language.Language_Item_Definer(english_food_file, portuguese_food_file);

	static String[] this_is_the_time_text = {"This is the time that you", "Essa e a hora que voce"};

	static String english_prefix_text = this_is_the_time_text[0] + " ";
	static Map<String, String> english_food_time_show_texts = new HashMap<String, String>();

	static String portuguese_prefix_text = this_is_the_time_text[1] + " ";
	static Map<String, String> portuguese_food_time_show_texts = new HashMap<String, String>();

	public static void main(String[] args) {
		Food_Time self = new Food_Time();

		global_switches.put("write_to_file", true);

		english_food_time_show_texts.put("Ate", english_prefix_text + "ate");
		english_food_time_show_texts.put("Drink Water", english_prefix_text + "can drink water");
		english_food_time_show_texts.put("Hungry", english_prefix_text + "will be hungry");

		portuguese_food_time_show_texts.put("Ate", portuguese_prefix_text + "comeu");
		portuguese_food_time_show_texts.put("Drink Water", portuguese_prefix_text + "pode beber água");
		portuguese_food_time_show_texts.put("Hungry", portuguese_prefix_text + "irá ter fome");
	}
}

class Check_Food_Time {
	public static void main(String[] args) {
		Food_Time self = new Food_Time();

		print.print(" ");

		String[] lines = functions.Read_Lines(self.food_file);

		for (String line : lines) {
			print.print(line);
		}
	}
}

class Set_Food_Time {
	public static void main(String[] args) {
		Food_Time self = new Food_Time();

		print.print(functions.Now());

		String[] lines = functions.Read_Lines(self.food_file);

		print.print(" ");

		for (String line : lines) {
			print.print(line);
		}

		print.print(self.english_food_time_show_texts.get("Ate"));
	}
}
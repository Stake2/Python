package language;

import java.util.*;

public class language {
	static Locale locale = Locale.getDefault();

	static String global_language = locale.getLanguage();
	static String country = locale.getCountry();

	static String english = "en";
	static String english_full = "English";

	static String brazilian_portuguese = "pt";
	static String brazilian_portuguese_full = "Português Brasileiro";		

	public static void main(String[] args) {

	}

	public static String Language_Item_Definer(String english_item, String portuguese_item) {
		String choosen_item = "";

		if (global_language == english) {
			choosen_item = english;
		}

		if (global_language == brazilian_portuguese) {
			choosen_item = portuguese_item;
		}

		return choosen_item;
	}
}
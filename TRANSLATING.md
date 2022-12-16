I changed all of my Python modules and created new classes as utilities to use in them.<br>
The classes are these:<br>
Date<br>
File<br>
Folder<br>
Global_Switches<br>
Input<br>
Language<br>
Text<br>

I also changed the way that the language works and added a "Texts.json" file on each of the module folders in the "App Text Files" folder.<br>
Each text key has its English text in lowercase with spaces replaced by underscores and is a JSON dictionary containing the text in the languages with the ISO 639-1 Code as the key.<br>
Example:
```
"this_is_a_text": {
	"en": "This is a text",
	"pt": "Isto é um texto",
	"es": "Este es un texto",
	"fr": "Établi",
	"it": "Creato",
	"jp": "提起されました (Teiki sa remashita)",
	"no": "ble reist"
}
```

The "Texts.json" files contain the text of each module in the two languages that I know, Portuguese and English.<br>
If you want to translate my modules, simply clone this repository, and create a text file called "Settings.txt" on the root folder of the clone folder.<br>
Open the "Texts.json" file of the module that you want to translate, and start translating the JSON lines to your language, using the ISO 639-1 code of the language of the translated text as a key.<br>
The translated texts must follow the exact capitalization and spaces of the English text, and have other characters that are not letters or numbers too, like the format one "{}".<br>
Some texts have ", title()" in them, which means that it is only a word, and it will have its first letter in uppercase, if ", title()" is not present, then the first letter is in lowercase.<br>
Phrases do not need ", title()" in their text key, they can have lower or uppercase first letters.<br>
<br>
Some texts are lists, they have "type: list" after their text key, in this case, copy the whole English text list, change the key to the language you are translating to, and translate all items.<br>
Some text lists can have two mixed languages, like "text_key, type: list, en - pt", in that case, the text is the English text followed by a space, dash, space, and then the text of the translated language.<br>
The two language codes are always at the end of the whole text key.<br>
You need to copy the whole text dictionary, and modify the "pt" part of the text key to the ISO 639-1 code of the language you are translating to.<br>
Some texts are dicts (dictionaries), like this: "text_key, type: dict, en: pt", in this case, the "en" part is the keys, and the "pt" part is the values.<br>
You need to copy the whole text dictionary, like in lists, and change the "pt" part to the ISO 639-1 code of the language you are translating to.<br>
If the English text contains "{}", those characters can exist in the text key, but no other non-letter and non-number characters may exist in the text key, such as "(", or ")".<br>
There can also be texts of type "format" and type "regex", to better describe the purpose of the text.<br>
The texts must contain no dots at the end of the text, except those with the "explanation" type.<br>
Those texts with the "explanation" type can be long, have the "\n" text to add line breaks, and can have dots at the end.<br>
They always have the first line of the text as their text key.<br>
Some languages can have "masculine" and "feminine" text for each word, such as in Portuguese, "created" translates to "criado" (masculine) and "criada" (feminine).<br>
If the language you are translating my module to also has words for each gender, you can make the key of your language code a dictionary, like this:<br>

```
"created": {
	"en": "created",
	"pt": {
		"masculine": "criado",
		"feminine": "criada"
	}
}
```

The key "pt" is a dictionary, containing the "masculine" key for the masculine text, and the "feminine" key for the feminine text.<br>
The "Language" class will always choose the "masculine" key as the default text when creating the "language_texts" dictionary.<br>
And can be accessed like this: "language_texts["text_key"]", the class will create two gender keys on the language_texts dictionary.<br>
`language_texts["text_key, masculine"]`<br>
`language_texts["text_key, feminine"]`<br>

And the masculine and feminine keys can also be accessed as the sub-key of the text key, like this: `language_texts["text_key"]["masculine"]`.<br>

All of the utility classes are imported at the start of the main class of each module.<br>
The main class have the name of the module name, and is a sub-folder of the module folder, like "Watch_History.Watch_History".<br>
All main classes of all of the modules have three main methods, "Define_Basic_Variables()", to define Global_Switches, import languages, user language, folders from Folder class, and current date from Date class.<br>
"Define_Module_Folder", to define the module folder on the "App Text Files" folder and its "Texts.json" file.<br>
And "Define_Texts", to use the "JSON_To_Python" method of the "Language" class to read the "Texts.json" file, and use the "Item" method of the "Language" class to create the "language_texts" dictionary.<br>

Soon I will make a module on the root folder called "Translator_Helper.py", to help you translate my modules to your language.<br>
Allowing you to choose your native language or the language you know, to translate to, choose a module to translate, and show all of the English texts for you to translate.<br>
For you to translate my modules, you need to know English first, to understand the English texts of the modules and translate them.<br>
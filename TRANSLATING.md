I changed all of my Python modules and created new classes as utilities to use in them.<br>
The classes are these:<br>
[Define_Folders](https://github.com/Stake2/Python/blob/main/Modules/Utility/Define_Folders/__init__.py)<br>
[Modules](https://github.com/Stake2/Python/blob/main/Modules/Utility/Modules/__init__.py)<br>
[System](https://github.com/Stake2/Python/blob/main/Modules/Utility/System/__init__.py)<br>
[File](https://github.com/Stake2/Python/blob/main/Modules/Utility/File/__init__.py)<br>
[Folder](https://github.com/Stake2/Python/blob/main/Modules/Utility/Folder/__init__.py)<br>
[Global_Switches](https://github.com/Stake2/Python/blob/main/Modules/Utility/Global_Switches/__init__.py)<br>
[Language](https://github.com/Stake2/Python/blob/main/Modules/Utility/Language/__init__.py)<br>
[JSON](https://github.com/Stake2/Python/blob/main/Modules/Utility/Language/__init__.py)<br>
[Date](https://github.com/Stake2/Python/blob/main/Modules/Utility/Date/__init__.py)<br>
[Input](https://github.com/Stake2/Python/blob/main/Modules/Utility/Input/__init__.py)<br>
[Text](https://github.com/Stake2/Python/blob/main/Modules/Utility/Text/__init__.py)<br>
[API](https://github.com/Stake2/Python/blob/main/Modules/Utility/API/__init__.py)<br>
<br>
I also changed the way that the language works and added a "Texts.json" file on each of the module folders in the "Module files" folder.<br>
You can now translate my modules, translate them by adding the [ISO 639-1 language code](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes) to the "Texts.json" of the module you want to translate.<br>
<br>
Each text key has its English text in lowercase with spaces replaced by underscores and is a JSON dictionary containing the text in the languages with the [ISO 639-1 language code](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes) as the key.<br>
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
If you want to translate my modules, simply clone this repository and create a text file called "Settings.txt" in the root folder of the clone folder.<br>
Open the "Texts.json" file of the module that you want to translate, and start translating the JSON lines to your language, using the ISO 639-1 language code of the language of the translated text as a key.<br>
The translated texts must follow the exact capitalization and spaces of the English text, and have other characters that are not letters or numbers too, like the format one `"{}"`.<br>
Some texts have `", title()"` in them, which means that it is only a word, and it will have its first letter in uppercase<br>
If `", title()"` is not present, then the first letter is in lowercase.<br>
Phrases do not need `", title()"` in their text key; they can have lower or uppercase first letters.<br>
<br>
Some texts are lists, they have `"type: list"` after their text key.<br>
In this case, copy the whole English text list, change the key to the language you are translating to, and translate all list items.<br>
Some text lists can have two mixed languages, like `"text_key, type: list, en - pt"`, in that case, the text is the English text followed by a space, dash, space, and then the text of the translated language.<br>
The two language codes are always at the end of the whole text key.<br>
You need to copy the whole text dictionary, and modify the `"pt"` part of the text key to the ISO 639-1 language code of the language you are translating to.<br>
Some texts are dicts (dictionaries), like this: `"text_key, type: dict, en: pt"`, in this case, the `"en"` part is the keys, and the `"pt"` part is the values.<br>
You need to copy the whole text dictionary, like in lists, and change the `"pt"` part to the ISO 639-1 language of the language you are translating to.<br>
If the English text contains `"{}"`, those characters can exist in the text key, but no other non-letter and non-number characters may exist in the text key, such as `"("`, or `")"`.<br>
There can also be texts of type `"format"` and type `"regex"`, to better describe the purpose of the text.<br>
The texts must contain no dots at the end of the text, except those with the `"explanation"` type.<br>
Those texts with the `"explanation"` type can be long, have the `"\n"` text to add line breaks, and can have dots at the end.<br>
They always have the first line of the text as their text key.<br>
Some languages can have `"masculine"` and `"feminine"` text for each word, such as in Portuguese, `"created"` translates to `"criado" (masculine)` and `"criada" (feminine)`.<br>
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
The key `"pt"` is a dictionary, containing the `"masculine"` key for the masculine text, and the `"feminine"` key for the feminine text.<br>
The [Language](https://github.com/Stake2/Python/blob/main/Modules/Utility/Language/__init__.py) class will always choose the `"masculine"` key as the default text when creating the `"language_texts"` dictionary.<br>
The text can be accessed like this:<br>
`language_texts["text_key"]`<br>
<br>
The class will create two gender keys on the language_texts dictionary:<br>
`language_texts["text_key, masculine"]`<br>
`language_texts["text_key, feminine"]`<br>
<br>
And the masculine and feminine keys can also be accessed as the sub-key of the text key, like this:<br>
`language_texts["text_key"]["masculine"]`<br>
<br>
All of the utility classes are imported at the start of the main class of each usage module.<br>
The main class has the name of the module, and is a sub-folder of the module folder, like `"Watch_History.Watch_History"`.<br>
The usage and utility modules are listed and categorized in the [Modules.json](https://github.com/Stake2/Python/blob/main/Modules/Modules.json) file.<br>
<br>
All main classes of all of the usage modules have three main methods:<br>
`"Import_Classes()"`, to import the `"Define_Folders"`, `"JSON"`, and `"Language"` modules.<br>
`"Define_Basic_Variables()"`, to get the `switches` dictionary, import the module languages, get the user language, get the `folders` dictionary from the [Folder](https://github.com/Stake2/Python/blob/main/Modules/Utility/Folder/__init__.py) class, and the current date dictionary from the [Date](https://github.com/Stake2/Python/blob/main/Modules/Utility/Date/__init__.py) class.<br>
And `"Define_Texts()"`, to use the `"To_Python()"` method of the [JSON](https://github.com/Stake2/Python/blob/main/Modules/Utility/JSON/__init__.py) class to read the `"Texts.json"` file, and use the `"Item()"` method of the `"Language"` class to create the `"language_texts"` dictionary with texts in the user language.<br>
<br>
Soon, I will make a module in the root folder called `"Translator_Helper.py"`, to help you translate my modules to your language.<br>
Allowing you to choose your native language or the language you know, to translate to, choose a module to translate, and show all of the English texts for you to translate.<br>
For you to translate my modules, you need to know English first, to understand the English texts of the modules and translate them.<br>
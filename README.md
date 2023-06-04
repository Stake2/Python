# Python

![Python 3.8.10](https://img.shields.io/badge/Python-3.8.10-brightgreen.svg)
[![Contributors](https://img.shields.io/github/contributors/Stake2/Python.svg)](https://github.com/Stake2/Python/graphs/contributors)

All of my Python projects, modules, scripts, and utilities.<br>
Made by me, [Stake2](https://github.com/Stake2).

## License
Using [MIT License](https://github.com/Stake2/Python/blob/main/LICENSE)<br>

## COC
Read [Code of Conduct](https://github.com/Stake2/Python/blob/main/CODE_OF_CONDUCT.md)<br>

## Contribute
[How to Contribute](https://github.com/Stake2/Python/blob/main/CONTRIBUTING.md)<br>

[Translating](https://github.com/Stake2/Python/blob/main/TRANSLATING.md)<br>

## Installing
- Install the requirements in the [Requirements file](https://github.com/Stake2/Python/blob/main/requirements.txt)
```
$ pip install -r requirements.txt
```
- Add the [Modules folder](https://github.com/Stake2/Python/tree/main/Modules) to your PATH or copy its contents into your Python modules folder

- To list all modules avaliable to run (MS = Module Selector)
```
$ py MS.py -help
```

- To run a specific module
```
$ py MS.py -[Lowercased module name]
$ py MS.py -m [Module name typed in any case, with spaces or underlines]
$ py MS.py -module [Module name typed in any case, with spaces or underlines]
```

- You can also run the MS script without any arguments and it will list the available modules for you to select one
```
$ MS.py

# Output example:

Modules:
[1] - Block_Websites
[2] - Christmas
[3] - Code
[4] - Database
[5] - Diary
[6] - Diary_Slim
[7] - Food_Time
[8] - Friends
[9] - GamePlayer
[10] - Project_Zomboid
[11] - Python
[12] - Social_Networks
[13] - SproutGigs
[14] - Stories
[15] - Tasks
[16] - Text_Generator
[17] - Watch_History
[18] - Years

Select a module from the list to execute it: |
```

## Connection of Python files to [PHP files](https://github.com/Stake2/PHP) and [Websites](https://github.com/Stake2/Websites)
The ["Update_Websites"](https://github.com/Stake2/Python/tree/main/Modules/Code/Update_Websites) class of the ["Code.py"](https://github.com/Stake2/Python/tree/main/Modules/Code) module helps the user generate a website (generate its HTML contents).<br>
It does that by opening a local server ([XAMPP](https://www.apachefriends.org/)), asking the user to select a website or create a list of websites to update.<br>
And opening each one of the websites using the ``/generate`` route of the [PHP Index file](https://github.com/Stake2/PHP/blob/main/Index.php), in each supported language (currently ``General``, ``English``, and ``Portuguese``).<br>
Then it opens a "Github" shortcut that opens the [ConEmu](https://conemu.github.io/) console program in the [Websites](https://github.com/Stake2/Websites) folder, for the user to execute ``git`` operations to push the website changes and generated HTML files to the [Websites Repository](https://github.com/Stake2/Websites).

The ["Tasks.py"](https://github.com/Stake2/Python/tree/main/Modules/Tasks) Python module generates the JSON database files which are read by the ["Tasks.php"](https://github.com/Stake2/PHP/blob/main/Websites/Tasks/Generators/Tasks.php) HTML tab generator written in PHP.<br>
In order to generate the "Tasks" tab on the [Tasks](https://thestake2.netlify.app/Tasks/) website.<br>
And also generate the "Completed tasks" tabs on all year websites.

The ["Watch_History.py"](https://github.com/Stake2/Python/tree/main/Modules/Watch_History) Python module generates the JSON database files which are read by the ["Watched.php"](https://github.com/Stake2/PHP/blob/main/Websites/Watch%20History/Generators/Watched.php) HTML tab generator written in PHP.<br>
In order to generate the ["Watched things"](https://thestake2.netlify.app/Watch%20History/?tab=1) and ["Past registries"](https://thestake2.netlify.app/Watch%20History/?tab=3) tabs on the [Watch History](https://thestake2.netlify.app/Watch%20History/) website.<br>
And also generate the "Watched things" tabs on all year websites.

The ["Years.py"](https://github.com/Stake2/Python/tree/main/Modules/Years) Python module generates the year summary files read by the ["Summary.php"](https://github.com/Stake2/PHP/blob/main/Websites/Years/Generators/Summary.php) HTML tab generator written in PHP.<br>
In order to generate "Summary" tabs on all year websites website.

[PHP: Connection of PHP files to Python modules](https://github.com/Stake2/PHP#connection-of-php-files-to-python-modules)

## Translating
Check the [Code of Conduct](https://github.com/Stake2/Python/blob/main/CODE_OF_CONDUCT.md).<br>
You can now translate my modules, translate them by adding the [ISO 639-1 language code](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes) to the "Texts.json" of the module you want to translate.<br>
<br>
Soon I will make a module on the root folder called "Translator_Helper.py", to help you translate my modules to your language.<br>
Allowing you to choose your native language or the language you know, to translate to, choose a module to translate, and show all of the English texts for you to translate.<br>
For you to translate my modules, you need to know English first, to understand the English texts of the modules and translate them.<br>
<br>
You can find more explanation about how to translate and how the ["Language"](https://github.com/Stake2/Python/blob/main/Modules/Language/__init__.py) class works in the [Translating](https://github.com/Stake2/Python/blob/main/TRANSLATING.md) file.<br>
Each module also has a "Descriptions.json" file on its root folder, I ask you to translate the descriptions of the module you are translating.
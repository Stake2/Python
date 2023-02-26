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
> pip install -r requiriments.txt
```
- Add the [Modules folder](https://github.com/Stake2/Python/tree/main/Modules) to your PATH or copy its contents into your Python modules folder

- To list all modules avaliable to run (MS = Module Selector)
```
> py MS.py --help
```

- To run a specific module
```
> py MS.py -[Lowercased module name]
> py MS.py -m [Module name typed in any case, with spaces or underlines]
> py MS.py -module [Module name typed in any case, with spaces or underlines]
```

- You can also run the MS script without any arguments and it will list the available modules for you to select one
```
> MS.py

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

# pm-replacement
auto practice scheduler

Sample usage: `python scheduler_new.py [name of excel] [number of practices] [maximum number of members missing]`

arguments:
1) path to excel file (see example for format) - ex. test_twice.xlsx
2) number of desired practices. code will provide +1 date for filming - ex. 4
3) (optional) optional argument to generate non-full house practice schedule. denotes maximum number of members that can be missing - ex. 2

answers to questions that i had:
- main: https://stackoverflow.com/questions/419163/what-does-if-name-main-do#419185
- GUIs: https://www.tutorialspoint.com/python/python_gui_programming.htm

- added 2 lines asking for user input during generate_practice_times() (full house implementation) to reduce amount of stuff printed on screen

## Refactor
1. `Schedule class` renamed (capitalized)
2. `schedule.sched` is now `Schedule.array`
3. Defined new method for calculating `Schedule.array` - [Calling a class function inside of __init__](https://stackoverflow.com/questions/12646326/calling-a-class-function-inside-of-init)
4. Question: should it be `def calculate_num_blocks(self, start, end):` or `def calculate_num_blocks(self)`? A: [it looks like](https://realpython.com/instance-class-and-static-methods-demystified/#class-methods) - is `calculate_num_blocks` a staticmethod? (ok watch [this](https://www.youtube.com/watch?v=rq8cL2XMM5M))
5. Created `visualize(self):` class method to replace `visualize_week`
⋅⋅* `toprint` --> `vis_array` --> `self.array`, `toprintdays` --> `days`
6. Refactored `create_members_from_excel` method
⋅⋅* Moved `other` into Schedule object


- [Markdown Cheatsheet](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet)
- [PEP 8](https://www.python.org/dev/peps/pep-0008/)


Refactor: make generate_practice_times_2() dry: [here](https://www.codementor.io/blog/pythonic-code-6yxqdoktzt) and [here](https://pythontips.com/2013/08/04/args-and-kwargs-in-python-explained/)

- Schedule.py: clean compare_schedules and get_practice_range

To clean:
- get_practice_range --> clean (break into helpers)
- get_practice_range --> think this can be moved into Ex/Schedule objects
- suggest_prac
- missing_memb_practices
- get_time (move into Schedule obj (used in whos_missing)
- whos_missing
- IMPLEMENTATION 1 - instead of for loop comparing over and over, compare all at once

# pm-replacement
auto practice scheduler

> python scheduler_new.py [name of excel] [number of practices] [o] [maximum number of members missing]

arguments:
1) path to excel file (see example for format) - ex. test_twice.xlsx
2) number of desired practices. code will provide +1 date for filming - ex. 4
3) (optional) include "o" as an argument to generate non-full house practice schedule. otherwise, will provide full house only practices. if no argument for 4 provided, assumes maximum missing 1 member
4) (optional) specify maximum number of members that can be missing

answers to questions that i had:
- main: https://stackoverflow.com/questions/419163/what-does-if-name-main-do#419185
- GUIs: https://www.tutorialspoint.com/python/python_gui_programming.htm

- added 2 lines asking for user input during generate_practice_times() (full house implementation) to reduce amount of stuff printed on screen

## Refactor
1. `Schedule class` renamed (capitalized)
2. `schedule.sched` is now `Schedule.array`
3. Defined new method for calculating `Schedule.array` - [Calling a class function inside of __init__](https://stackoverflow.com/questions/12646326/calling-a-class-function-inside-of-init)
4. Question: should it be `def calculate_num_blocks(self, start, end):` or `def calculate_num_blocks(self)`? A: [it looks like](https://realpython.com/instance-class-and-static-methods-demystified/#class-methods) - is `calculate_num_blocks` a staticmethod? (ok watch [this](https://www.youtube.com/watch?v=rq8cL2XMM5M))

CURRENT: in `def visualize(self):`, cleaning the dtdt shitshow



- [Markdown Cheatsheet](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet)
- [PEP 8](https://www.python.org/dev/peps/pep-0008/)

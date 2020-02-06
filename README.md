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

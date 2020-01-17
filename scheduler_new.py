# Script to generate practice schedules based on member avails
# Takes member avails (array of 7) as input
# Studio avails similar to member avails as input
# ideas on ipad rn

import sys
from sys import argv
import dtconvert
import datetime
import pprint
import copy
import calendar
import pandas as pd

class schedule:
    def __init__(self, start, end, name):
        format = '%H:%M'    # hours and minutes only
        self.start = start
        self.end = end
        self.name = name
        if isinstance(start, str):
            self.start = datetime.datetime.strptime(start, format)       # converts to datettime object
            self.start = datetime.time(self.start.hour, self.start.minute)
        if isinstance(end, str):
            self.end = datetime.datetime.strptime(end, format)
            self.end = datetime.time(self.end.hour, self.end.minute)

        # get difference
        t_hr = self.end.hour - self.start.hour
        t_min = self.end.minute - self.start.minute

        # in 30 min blocks:
        num_half_hr = int(t_min/30)
        sched_size = 2 * t_hr + num_half_hr
        # # in 15 min blocks:
        # num_q_hr = int(t_min/15)
        # sched_size = 4 * t_hr + num_q_hr

        # using t_hr and min, generate array size
        self.sched = [[True for x in range(sched_size)] for y in range(7)]

    def mod_sched(self):
        # do we even need this method
        self.arr.append(self.start + self.end)
        print(self.arr)

class ex_schedule:      # ex for exclusive, excluding
    def __init__(self, start, end, num_members):
        format = '%H:%M'    # hours and minutes only
        self.start = start
        self.end = end
        self.name = "schedule (including non-fullhouse)"
        if isinstance(start, str):
            self.start = datetime.datetime.strptime(start, format)       # converts to datettime object
            self.start = datetime.time(self.start.hour, self.start.minute)
        if isinstance(end, str):
            self.end = datetime.datetime.strptime(end, format)
            self.end = datetime.time(self.end.hour, self.end.minute)

        # get difference
        t_hr = self.end.hour - self.start.hour
        t_min = self.end.minute - self.start.minute

        # in 30 min blocks:
        num_half_hr = int(t_min/30)
        sched_size = 2 * t_hr + num_half_hr
        # # in 15 min blocks:
        # num_q_hr = int(t_min/15)
        # sched_size = 4 * t_hr + num_q_hr

        # using t_hr and min, generate array size
        self.sched = [[[True for z in range(num_members)] for x in range(sched_size)] for y in range(7)]

def visualize_day(schedule, day):
    st_t = schedule.start
    e_t = schedule.end
    arr2d = schedule.sched

    # Prints an informative banner at the top of the visualization
    print("######### VISUALIZING " + str(day) + " #########")       # todo: there's a strptime method that converts int to day of week
    print(st_t, end=" - ")
    print(e_t)
    print("-")

    diff_hr = e_t.hour - st_t.hour
    diff_min = e_t.minute - st_t.minute
    diff = diff_hr * 2 + int(diff_min/30)        # number of 1/2 hr slots

    for i in range(diff): # convert to datetime.datetime object, add timedelta, convert back
        dtdt = datetime.datetime.combine(datetime.date(1, 1, 1), st_t)
        diff_i = datetime.timedelta(minutes=30*i)
        comb = dtdt + diff_i
        comb = comb.time()
        print(comb.strftime("%H:%M"), end="\t|")           # prints without seconds

        if arr2d[day][i] is True:
            print(" |")
        else:
        # if arr2d[day][i] is False:
            print("x|")

def visualize_week(schedule):
    st_t = schedule.start
    e_t = schedule.end
    arr2d = schedule.sched

    # Prints an informative banner at the top of the visualization
    print("\n######### VISUALIZING WEEK: " + schedule.name + " #########")       # todo: there's a strptime method that converts int to day of week
    print(st_t, end=" - ")
    print(e_t)
    print(" ")

    diff_hr = e_t.hour - st_t.hour
    diff_min = e_t.minute - st_t.minute
    diff = diff_hr * 2 + int(diff_min/30)        # number of 1/2 hr slots

    # Create toprint array that stores time (0) and schedules (1->7)
    # Not great because index is now off by 1  ¯\_(ツ)_/¯
    toprint = [ [],
                [], [], [], [], [], [], [] ]
    toprintdays = ["S", "M", "T", "W", "R", "F", "S" ]

    # Setting up the time on the very left as toprint[0]
    for i in range(diff): # convert to datetime.datetime object, add timedelta, convert back
        dtdt = datetime.datetime.combine(datetime.date(1, 1, 1), st_t)
        diff_i = datetime.timedelta(minutes=30*i)
        comb = dtdt + diff_i
        comb = comb.time()
        toprint[0].append(comb.strftime("%H:%M"))           # appends without seconds

    # Saving all the stuff in arr2d into toprint (since we already have the information)
    for day_i in range(len(arr2d)):
        # Ex: sunday in arr2d is 0, save at 0+1 in toprint
        toprint[day_i+1] = arr2d[day_i]

    # Right column of times:
    toprint.append(toprint[0])

    # The actual printing part of this method
    # HEADER:
    print("#####", end=" ")
    for d in toprintdays: print("(" + d + ") ", end="")
    print("#####")
    # SCHEDULE:
    for i in range(len(toprint[0])):
        for j in range(len(toprint)):
            temp = toprint[j][i]
            if temp is True: temp = "   "
            elif temp is False: temp = " x "
            else: temp = str(toprint[j][i]) #   + "\t"
            print(temp, end=" ")
        print("")
    print()

# prints the 3D part of ex_schedule a little nicer
def visualize_ex_week(ex_schedule):
    st_t = ex_schedule.start
    e_t = ex_schedule.end
    arr3d = ex_schedule.sched

    # Prints an informative banner at the top of the visualization
    print("\n######### VISUALIZING WEEK: " + ex_schedule.name + " #########")       # todo: there's a strptime method that converts int to day of week
    print(st_t, end=" - ")
    print(e_t)
    print(" ")

    diff_hr = e_t.hour - st_t.hour
    diff_min = e_t.minute - st_t.minute
    diff = diff_hr * 2 + int(diff_min/30)        # number of 1/2 hr slots

    # Create toprint array that stores time (0) and schedules (1->7)
    # Not great because index is now off by 1  ¯\_(ツ)_/¯
    toprint = [ [],
                [], [], [], [], [], [], [] ]
    toprintdays = ["S", "M", "T", "W", "R", "F", "S" ]

    # Setting up the time on the very left as toprint[0]
    for i in range(diff): # convert to datetime.datetime object, add timedelta, convert back
        dtdt = datetime.datetime.combine(datetime.date(1, 1, 1), st_t)
        diff_i = datetime.timedelta(minutes=30*i)
        comb = dtdt + diff_i
        comb = comb.time()
        toprint[0].append(comb.strftime("%H:%M"))           # appends without seconds

    # Saving all the stuff in arr2d into toprint (since we already have the information)
    for day_i in range(len(arr3d)):
        # Ex: sunday in arr2d is 0, save at 0+1 in toprint
        toprint[day_i+1] = arr3d[day_i]

    # Right column of times:
    toprint.append(toprint[0])
    print(toprint)
    # need to separate first and last part of toprint into different varts, rewrite the printing part of the method
    print(toprint[8])
    print(len(toprint[0]))
    exit()
    print(len(toprint[1][1]))

    # The actual printing part of this method
    # # TODO: REWRITE THIS - see ipad
    # HEADER:
    print("#####", end=" ")
    for d in toprintdays: print("(" + d + ") ", end="")
    print("#####")
    # SCHEDULE:
    for i in range(len(toprint[0])):
        for j in range(len(toprint)):
            for t in range(len(toprint[0][0])):
                temp = toprint[j][i][t]
                if temp is True: temp = "   "
                elif temp is False: temp = " x "
                else: temp = str(toprint[j][i]) #   + "\t"
            print(temp, end=" ")
        print("")
    print()

# HELPER for changing member schedule
def modify_schedule(m_sched, dt_se, i):
    m_sched_mod = m_sched
    first_pass = True                                            # Lazy switch for init all false

    for dt_range in dt_se:
        dt_start = dt_range[0]
        dt_end = dt_range[1]

        if ((dt_start is True) and (dt_end is True)):           # Case 1: completely free this day (there should only be 1 dt_range in dt_se)
            for s in range(len(m_sched_mod.sched[i])):          # Set all to True
                m_sched_mod.sched[i][s] = True
            return m_sched_mod

        if first_pass is True:                                  # Only do this the first time
            for s in range(len(m_sched_mod.sched[i])):          # Otherwise will overwrite changes with every dt_range
                m_sched_mod.sched[i][s] = False                 # Set all to False (init all false)
                first_pass = False

        if ((dt_start is False) and (dt_end is False)):         # Case 2: completely busy (there should only be 1 dt_range in dt_se)
            return m_sched_mod

        # Case 3: modifications to m_sched_mod happen here
        # Get difference between start of master schedule and start of member avail (on day i)
        t_hr_start = dt_start.hour - m_sched_mod.start.hour
        t_min_start = dt_start.minute - m_sched_mod.start.minute
        num_halfhr_start = int(t_min_start/30)
        t_hr_end = dt_end.hour - m_sched_mod.start.hour
        t_min_end = dt_end.minute - m_sched_mod.start.minute
        num_halfhr_end = int(t_min_end/30)

        # Turn the difference into num "slots" (to be used in the schedule list)
        num_slot_start = t_hr_start * 2 + num_halfhr_start
        num_slot_end = t_hr_end * 2 + num_halfhr_end

        for j in range(num_slot_end)[num_slot_start:]:
            m_sched_mod.sched[i][j] = True

    return m_sched_mod

def member_schedule(master, avails, name, test):
    m_sched = schedule(master.start, master.end, name)          # Set array/schedule size to same as master

    for i in range(len(m_sched.sched)):                         # Modify array with avails
        day_avail = avails[i]                                   # At this step, still strings (no dateetime conversion)
        # print("day avail: ", end="")
        # print(day_avail)

        if test: print(str(i) + ": ", end="")
        dt_se = dtconvert.convert_to_datetime(day_avail, master, test)    # UPDATE: dt_se is the 2D list ("ranges")

        m_sched = modify_schedule(m_sched, dt_se, i)            # new version

    # NEXT TODO: Modify to add exceptions - right now exceptions are still None
    return m_sched

# HELPER for generate_practice_times()
# Both t and m are schedule objects (start, end, sched)
### t - temp, could be master, could be ouput of previous iteration of this function (mod)
### m - member to compare
def compare_schedules(t, m):
    mod = copy.copy(t)
    mod.name = str(t.name) + " + " + str(m.name)

    for d, day in enumerate(mod.sched):         # Ah yes enumerate is a thing
        for i, timeslot in enumerate(day):
            # Check if both m and t free at this time (AND)
            free = timeslot & m.sched[d][i]
            mod.sched[d][i] = free
    return mod

# HELPER for generate_practice_times()
# returns all potential practice times in a range (per day)
# mod is a schedule object
def get_practice_range(n, mod):
    r_comb = []
    print("Weekly Schedule:")
    for i, schedlist in enumerate(mod.sched):               # schedlist is list of True, False

        print(calendar.day_abbr[(i-1)%7], end=": ")         # for python's calendar function to work, need to shift all by 1

        true_range = []                                     # saves indices
        true_range_dt = []
        switch = 0
        for j, bool in enumerate(schedlist):
            if bool is True and switch == 0:
                # print(i)
                switch = 1
                true_range.append(j)
            if bool is False and switch == 1:
                switch = 0
                true_range.append(j)
        if len(true_range) == 1:
            true_range.append(len(schedlist))

        # true_range stores the indices: use them to find associated datetime objects
        st_t = mod.start
        e_t = mod.end
        dtdt = datetime.datetime.combine(datetime.date(1,1,1), st_t)      # TODO: arbitrary dtdt (1,1,1)

        for ind in true_range:
            diff_i = datetime.timedelta(minutes=30*ind)     # diff_i is the hrs/mins after start time
            comb = dtdt + diff_i                         # where dtdt is the starting date and time
            comb = comb.time()
            true_range_dt.append(comb)

        if not true_range_dt: # Catch for days with no practice times
            print("None")
            r_comb.append(None)
            pass

        start = True                    # Boolean switch for start - end
        single_range = True             # Boolean switch for number of ranges
        if len(true_range_dt) > 2: single_range = False

        t_r_comb = []
        t1 = []

        for idj, j in enumerate(true_range_dt):
            if single_range is True:
                t_r_comb = [[true_range_dt[0], true_range_dt[1]]]
                print(str(true_range_dt[0].strftime("%H:%M")) + "-" + str(true_range_dt[1].strftime("%H:%M")))
                r_comb.append(t_r_comb)
                break
            else:
                if start is True:
                    print(str(j.strftime("%H:%M")), end="-")
                    t1.append(j)
                    start = False
                else:
                    t1.append(j)
                    t_r_comb.append(t1)
                    t1 = []

                    if not (idj+1 == len(true_range_dt)):
                        print(str(j.strftime("%H:%M")), end=", ")

                    else:
                        print(str(j.strftime("%H:%M")))
                        r_comb.append(t_r_comb)

                    start = True

    suggest_prac(n, r_comb)

    return r_comb

# uses get_practice_range output (r_comb) to suggest n practice dates and 1 filming date
def suggest_prac(n, r_comb):

    print()
    print("Suggested dates:")                   # 0 = sun
    weekday = datetime.date.today()
    idx = (weekday.weekday() + 1) % 7           # need weekdays shifted by 1 (wait can we do this with iso or whatever it's called?)
    i = 1

    n += 1                                      # this is for the filming

    # for loop n + 1 times
    while(n is not 0):
        # get n index where r_comb isn't None
        # if (thing at idx+1 is not None:):
        j = (idx+i-1)%7

        # STORE practice dates + PRINT
        if r_comb[j] is not None:
            if n == 1:
                print("\nFILMING: ", end="")

            print((weekday + datetime.timedelta(days=i-1)).strftime("%A, %B %d %Y"), end=": ")
            for dt in r_comb[j]:
                print(dt[0].strftime("%H:%M"), end="-")
                print(dt[1].strftime("%H:%M"), end=" ")
            print()
                # print(r_comb[j])                # this is just showing what's in rcomb (datetime stuff)
            n -= 1

        i += 1

        # print(idx)
    # for now: suggestions are just the range (make mod for earlier? or nah too complicated?)
    return weekday

# This method does all of the heavy lifting: generates the practice schedule
# IMPLEMENTATION 1: return times all members free
def generate_practice_times(n, master, members_in):
    print("Generating full house practice times...")

    print("Members: ", end="")
    for memb in members_in:
        print(memb.name, end=", ")
    print()

    #  members - list of all members (as member_schedule objects)
    print("Schedule set from: " + str(master.start) + " - " + str(master.end))

    ### IMPLEMENTATION 1: ###
    ###  FULL HOUSE ONLY  ###
    # Use compare_schedules helper to determine free times
    mod = None                                                      # is this the first schedule
    for i, m in enumerate(members_in):
        if mod is None:
            mod = compare_schedules(members_in[0], members_in[1])
            visualize_week(mod)
        else:
            try:
                mod = compare_schedules(mod, members_in[i+1])             # Why this doesn't feel right lol
                visualize_week(mod)
            except: pass
    visualize_week(mod)                                             # Visualizing modified week outside of the method

    get_practice_range(n, mod)                                         # returns range of true (Sun --> Mon)
    return mod

# IMPLEMENTATION 2: test with more members, return "best" times (doesn't have to be all free) (kenny array idea)
def generate_practice_times_2(n, master, members_in, max_num_memb_missing):
    m = max_num_memb_missing
    print("Generating best practice times (missing max", m, "member(s))...")

    practice = ex_schedule('9:00', '22:00', len(members_in))      # practice is a ex_schedule object that takes total number of members for TF array

    print("Members: ", end="")
    for memb in members_in:
        print(memb.name, end=", ")
    print()

    #  members - list of all members (as member_schedule objects)
    print("Schedule set from: " + str(master.start) + " - " + str(master.end))

    # for testing, so we can see the schedules
    for m in members_in:
        # visualize_week(m)
        print("", end="")

    visualize_ex_week(practice)
    # may need to make a new/simplified visualize_week that just prints number of members who can come to each time slot

    ### IMPLEMENTATION 2: ###
    ###  ACCEPTS NON-FULL HOUSE PRACTICES  ###

    '''
    method for when it's okay to miss m number of members
    new variable - max number of members missing

    '''


# Returns list of member_schedule objects
def create_members_from_excel(master, excel_path, test):
    members_arr = []

    twice = pd.read_excel(excel_path, header=1)      # setting the header = 1 removes the title
    if test:
        print(twice.head)
        print(twice.columns)

    # for i in range(10):          # CHANGE when TESTING VALUES
    for i, row in twice.iterrows():
        week = []
        name = twice['NAME'].iloc[i]                # same as twice.columns[0]. TODO: maybe put a check on this?
        # print(twice.columns[0])
        # from 1 to 7
        for d in range(7):                          # TODO: set for d in range(7): ---> for d in range(8): once exceptions (other) can be handled
            day_header = twice.columns[d+1]
            if test: print(day_header, end=": ")
            day_avail = twice[day_header].iloc[i]
            if test: print(day_avail)
            week.append(day_avail)

        week.append(None)                           # TODO: this is a placeholder for exceptions (other)
        if test: print(name)
        member = member_schedule(master, week, name, test)

        if test: visualize_week(member)
        members_arr.append(member)

    return members_arr


def main():
    try:
        path = sys.argv[1]
        if not path.endswith(".xlsx"):
            print("Please enter valid path to excel file.")
            exit(1)
    except:
        print("Error: path to excel file (argument 1).")
        exit(1)

    try:
        n = int(sys.argv[2])
    except:
        print("Please specify number of desired practices in second argument.")
        exit(1)

     # Create grid/master schedule
    master = schedule('9:00', '22:00', "master")
    members_arr = create_members_from_excel(master, path, False)         # 3rd var for testing: if test=True, will print everything

    # Checks if there is argument 3, 4 - request for optimal schedule (-o) will be ignored without specifying number of missing members (-m)
    try:
        fullhouse = sys.argv[3]
        max_num_memb_missing = sys.argv[4]
    except:
        generate_practice_times(n, master, members_arr)
        exit(1)

    if fullhouse == "o":        # this if/else format may need to be changed in the future if there are other options
        try:
            max_num_memb_missing = int(max_num_memb_missing)
            generate_practice_times_2(n, master, members_arr, max_num_memb_missing)
            # note to self: exit() out of method for testing will still print the exception text
        except Exception as e:
            print("Maximum number of members missing (arg 4) must be an integer.")
            return e

    else:
        print("Invalid: 3rd argument is not 'o'")

    pass

if __name__ == '__main__':
    sys.exit(main())

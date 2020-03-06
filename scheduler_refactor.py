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
import math
import calendar
import pandas as pd
import numpy as np

class Schedule:
    def __init__(self, start, end, name):               # Constructor
        self.start = start                              # Schedule start time (ex. 9:00)
        self.end = end                                  # Schedule end time (ex. 22:00)
        self.name = name                                # Schedule name (ex. member name, final schedule, etc)
        self.array = self.create_array()                # Schedule array (2D array of days of week (7) x half hour blocks)

    def create_array(self):
        # Converts start/end time to datettime if entered as string
        if isinstance(self.start, str):
            self.start = datetime.datetime.strptime(self.start, '%H:%M')
            self.start = datetime.time(self.start.hour, self.start.minute)
        if isinstance(self.end, str):
            self.end = datetime.datetime.strptime(self.end, '%H:%M')
            self.end = datetime.time(self.end.hour, self.end.minute)

        # Generate array from number of (30 minute) blocks
        num_blocks = self.calculate_num_blocks(self.start, self.end)

        return [[True for x in range(num_blocks)] for y in range(7)]

    # maybe
    # watch this first https://www.youtube.com/watch?v=rq8cL2XMM5M
    @staticmethod
    def calculate_num_blocks(start, end):
        # Determining size of array: get difference
        total_hrs = end.hour - start.hour
        total_mins = end.minute - start.minute

        # Determining size of array: in 30 min blocks (rounded)
        num_half_hr = int(total_mins/30)
        num_blocks = 2 * total_hrs + num_half_hr

        return num_blocks

    # mid-REFACTOR: Instead of visualize schedule method, use method inside Schedule object
    def visualize(self):
        # Banner
        print("\n######### VISUALIZING WEEK: " + self.name + " #########")
        print(self.start, "-", self.end, "\n")

        num_blocks = self.calculate_num_blocks(self.start, self.end)

        # Create toprint array that stores time (0) and schedules (1->7)
        # Not great because index is now off by 1  ¯\_(ツ)_/¯
        toprint = [ [],
                    [], [], [], [], [], [], [] ]
        toprintdays = ["S", "M", "T", "W", "R", "F", "S" ]

        # Setting up the time on the very left as toprint[0]
        # Convert to datetime.datetime object, add timedelta, convert back
        # MID-REFACTOR - clean this up here
        # is there really no better way than to use a full datetime object?
        # https://stackoverflow.com/questions/100210/what-is-the-standard-way-to-add-n-seconds-to-datetime-time-in-python
        dtdt = datetime.datetime.combine(datetime.date(1, 1, 1), self.start)
        dtdt = self.start
        print(self.start)
        exit(1)
        for i in range(num_blocks):
            num_blocks_i = datetime.timedelta(minutes=30*i)
            comb = dtdt + num_blocks_i
            comb = comb.time()
            toprint[0].append(comb.strftime("%H:%M"))

        # Saving all the stuff in array into toprint (since we already have the information)
        for day_i in range(len(self.array)):
            # Ex: sunday in array is 0, save at 0+1 in toprint
            toprint[day_i+1] = self.array[day_i]

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
        self.array = [[[True for z in range(num_members)] for x in range(sched_size)] for y in range(7)]

def visualize_week(schedule):
    st_t = schedule.start
    e_t = schedule.end
    arr2d = schedule.array

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
def visualize_ex_week(ex_schedule, membs):
    st_t = ex_schedule.start
    e_t = ex_schedule.end
    days = ex_schedule.array

    # Prints an informative banner at the top of the visualization
    print("\n######### VISUALIZING WEEK: " + ex_schedule.name + " #########")       # todo: there's a strptime method that converts int to day of week
    print(st_t, end=" - ")
    print(e_t)
    print("Members: "+ membs[:-2])
    print(" ")

    diff_hr = e_t.hour - st_t.hour
    diff_min = e_t.minute - st_t.minute
    diff = diff_hr * 2 + int(diff_min/30)        # number of 1/2 hr slots

    # Create toprint array that stores time (0) and schedules (1->7)
    # index is now off by 1  ¯\_(ツ)_/¯
    times = []
    toprintdays = ["S", "M", "T", "W", "R", "F", "S" ]

    # setting up times in "times" array
    for i in range(diff): # convert to datetime.datetime object, add timedelta, convert back
        dtdt = datetime.datetime.combine(datetime.date(1, 1, 1), st_t)
        diff_i = datetime.timedelta(minutes=30*i)
        comb = dtdt + diff_i
        comb = comb.time()
        times.append(comb.strftime("%H:%M"))           # appends without seconds

    # The actual printing part of this method:
    # HEADER:
    print("#####", end=" ")
    for tpd in toprintdays:
        num_space = len(days[0][1])-1
        half_1 = int(num_space/2)
        half_2 = num_space-half_1
        print("(", end="")
        for s in range(half_1):
            print(" ", end="")
        print(tpd, end="")
        for t in range(half_2):
            print(" ", end="")
        print(")", end="")
    print(" #####")
    # SCHEDULE:
    for i in range(len(times)):                 # i: 0-26 (9:00) = m: 0-26 ([T,T,T])
        print(times[i], end=" ")
        for d in range(len(days)):          # d: 0-6 (sun)
            array = days[d][i]
            # import pdb; pdb.set_trace()
            print("[", end="")
            for am in array:
                if am is True:  print("-", end="")
                elif am is False:  print("*", end="")
                else:
                    print("error")
                    exit()
            print("]", end="")
        print(" ", end=times[i])
        print()

# HELPER for changing member schedule
def modify_schedule(m_sched, dt_se, i):
    m_sched_mod = m_sched
    first_pass = True                                            # Lazy switch for init all false

    for dt_range in dt_se:
        dt_start = dt_range[0]
        dt_end = dt_range[1]

        if ((dt_start is True) and (dt_end is True)):           # Case 1: completely free this day (there should only be 1 dt_range in dt_se)
            for s in range(len(m_sched_mod.array[i])):          # Set all to True
                m_sched_mod.array[i][s] = True
            return m_sched_mod

        if first_pass is True:                                  # Only do this the first time
            for s in range(len(m_sched_mod.array[i])):          # Otherwise will overwrite changes with every dt_range
                m_sched_mod.array[i][s] = False                 # Set all to False (init all false)
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
            m_sched_mod.array[i][j] = True

    return m_sched_mod

def member_schedule(master, avails, name, test):
    m_sched = Schedule(master.start, master.end, name)          # Set array/schedule size to same as master

    for i in range(len(m_sched.array)):                         # Modify array with avails
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

    for d, day in enumerate(mod.array):         # Ah yes enumerate is a thing
        for i, timeslot in enumerate(day):
            # Check if both m and t free at this time (AND)
            free = timeslot & m.array[d][i]
            mod.array[d][i] = free
    return mod

# def compare_schedules_2(t, m):

# HELPER for generate_practice_times()
# returns all potential practice times in a range (per day)
# mod is a schedule object
def get_practice_range(n, mod, ex_pract, members_in):

    members = []                                            # array to use in whos_missing
    for memb in members_in:
        members.append(memb.name)

    skip = False
    r_comb = []
    print("Weekly Schedule:")

    for i, schedlist in enumerate(mod.array):               # schedlist is list of True, False
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
            elif j == len(schedlist)-1 and bool is True:    # for the last timeslot
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

        if not true_range_dt:                           # Catch for days with no practice times
            print("None", end=" ")
            r_comb.append(None)
            skip = True
            pass

        start = True                    # Boolean switch for start - end
        single_range = True             # Boolean switch for number of ranges
        if len(true_range_dt) > 2: single_range = False

        t_r_comb = []
        t1 = []

        for idj, j in enumerate(true_range_dt):
            if single_range is True:
                t_r_comb = [[true_range_dt[0], true_range_dt[1]]]
                print(str(true_range_dt[0].strftime("%H:%M")) + "-" + str(true_range_dt[1].strftime("%H:%M")), end=" ")
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

        if(): print()
        elif ex_pract is not False:
            print("| missing: ", whos_missing(schedlist, ex_pract.array[i], members))            # compare mod to ex_pract and see who's missing
        else: print()

    suggest_prac(n, r_comb)

    return r_comb

def whos_missing(mods, day, members):
    missing = []
    m_time = []

    # print(day) # sunday (for i=0)
    # print(day[0]) # sunday at 9
    # print(day[0][m]) # sunday at 9 for first member

    # who's missing, when
    for t, time in enumerate(mods):                                             # compare schedlist[i = 0-26]
        if time is True:
            f = [i for i, bool in enumerate(day[t]) if bool==False]             # if FREE, check if day[0 to 26] FREE (f = [] if no False)
            if f:                                                               # if NOT free, f gives to get m index
                for m in f:
                    m_time = [members[m], t]
                    missing.append(m_time)
    # print(missing)

    # clean missing array
    clean = []
    if missing:
        for m in missing:
            if any(m[0] in n for n in clean):
                clean[next((i for i, sublist in enumerate(clean) if m[0] in sublist))].append(m[1])
            else:
                clean.append(m)
    # print(clean)

    if clean:
        s = ""
        for m in clean:
            s += m[0] + " (" + gimme_time(master.start, m[1]) + "-" + gimme_time(master.start, m[-1]+1) + "), "
        return s[:-2]
    else:
        return


def gimme_time(st_t, i):
    dtdt = datetime.datetime.combine(datetime.date(1, 1, 1), st_t)
    diff_i = datetime.timedelta(minutes=30*i)
    comb = dtdt + diff_i
    comb = comb.time()
    return comb.strftime("%H:%M")          # appends without seconds


def missing_memb_practices(ex_schedule, m, master):
    name = "Missing " + str(m) + " member(s)"
    mod_sched = member_schedule(master, ["free" for i in range(7)], name, False)

    for d, day in enumerate(ex_schedule.array):       # d: 0-6, [a,....,a] (26 a, a=[T,T,T])
        for i, timeslot in enumerate(day):
            if (np.sum(timeslot) >= (len(timeslot) - m)):                     # counts number of True
                mod_sched.array[d][i] = True
            else:
                mod_sched.array[d][i] = False
    return mod_sched

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
    membs = ""
    for memb in members_in:
        membs += memb.name + ", "
    print("Members: "+ membs[:-2])

    text = input("View member schedules? [y/n, default is no] ")

    # See the schedules
    if text is "y":
        for m in members_in:
            visualize_week(m)

    #  members - list of all members (as member_schedule objects)
    print("Schedule set from: " + str(master.start) + " - " + str(master.end))

    text = input("Visualize comparison? [y/n] ")
    if text is "y": view_comp_sched = True
    else: view_comp_sched = False

    ### IMPLEMENTATION 1: ###
    ###  FULL HOUSE ONLY  ###
    # Use compare_schedules helper to determine free times
    mod = None
    for i, m in enumerate(members_in):
        if mod is None:
            mod = compare_schedules(members_in[0], members_in[1])
            if view_comp_sched:
                visualize_week(mod)
        else:
            try:
                mod = compare_schedules(mod, members_in[i+1])
                if view_comp_sched:
                    visualize_week(mod)
            except: pass
    visualize_week(mod)                                                # visualizing modified week outside of the method

    get_practice_range(n, mod, False, members_in)                                  # returns range of true (Sun --> Mon)
    return mod

# IMPLEMENTATION 2: test with more members, return "best" times (doesn't have to be all free) (kenny array idea)
def generate_practice_times_2(n, master, members_in, max_num_memb_missing):
    mn = max_num_memb_missing
    print("Generating best practice times (missing max", mn, "member(s))...")

    practice = ex_schedule('9:00', '22:00', len(members_in))      # practice is a ex_schedule object that takes total number of members for TF array

    membs = ""
    for memb in members_in:
        membs += memb.name + ", "
    print("Members: "+ membs[:-2])

    #  members - list of all members (as member_schedule objects)
    print("Schedule set from: " + str(master.start) + " - " + str(master.end))

    print("Generating full house practice times...")
    text = input("View member schedules? [y/n, default is no] ")

    # See the schedules
    if text is "y":
        for m in members_in:
            visualize_week(m)

    #### IMPLEMENTATION 2: ####
    #  WITH N MISSING MEMBERS #
    for i, m in enumerate(members_in):
        for d in range(7):                                  # d: days of the week (0-6)
            for hr in range(len(practice.array[0])):        # hr: hours in the day
                practice.array[d][hr][i] = m.array[d][hr]

        # print(practice.array[0]) # monday
        # print(practice.array[0][0]) # monday at 9
        # print(practice.array[0][0][i]) # monday at 9 for first member
        # print(m.array[0]) # member monday
        # print(m.array[0][0]) # member monday at 9

    visualize_ex_week(practice, membs)

    mod_practice = missing_memb_practices(practice, mn, master)                  # converts ex_schedule to schedule with max_num_memb_missing in consideration
    visualize_week(mod_practice)
    get_practice_range(n, mod_practice, practice, members_in)                    # returns range of true (Sun --> Mon)
    # next todo: get_practice_range printing who's missing

    '''
    method for when it's okay to miss m number of members
    new variable - max number of members missing

    '''

# Returns list of member_schedule objects
def create_members_from_excel(master, excel_path, test):
    members_arr = []
    others = [["",""],["*** OTHER ***", ""]]

    twice = pd.read_excel(excel_path, header=1)      # setting the header = 1 removes the title
    if test:
        print(twice.head)
        print(twice.columns)

    # for i in range(2):          # CHANGE when TESTING VALUES
    for i, row in twice.iterrows():
        week = []
        name = twice['NAME'].iloc[i]                # same as twice.columns[0]. TODO: maybe put a check on this?
        # print(twice.columns[0])
        # from 1 to 7
        for d in range(7):
            day_header = twice.columns[d+1]
            if test: print(day_header, end=": ")
            day_avail = twice[day_header].iloc[i]
            if test: print(day_avail)
            week.append(day_avail)

        # TODO: set for d in range(7): ---> for d in range(8): once exceptions (other) can be handled
        # for now: i = 8
        day_header = twice.columns[7+1]
        other = twice[day_header].iloc[i]
        try:
            if math.isnan(other):   other = '-'
        except: pass
        others.append([name.upper() + ":\t", other])

        week.append(None)                           # TODO: this is a placeholder for exceptions (other)
        if test: print(name)
        member = member_schedule(master, week, name, test)

        if test: visualize_week(member)
        members_arr.append(member)

    return members_arr, others

# master is global fuck this
# master = Schedule('9:00', '22:00', "master")

def main():

    master = Schedule('9:00', '22:30', "Master")
    visualize_week(master)
    # mid-REFACTOR
    master.visualize()
    exit(1)

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

    # # Create grid/master schedule
    # master = schedule('9:00', '22:00', "master")
    try:
        members_arr, others = create_members_from_excel(master, path, False)         # 3rd var for testing: if test=True, will print everything
    except:
        members_arr, others = create_members_from_excel(master, path, True)         # 3rd var for testing: if test=True, will print everything
        print("Error reading excel.")
        exit()

    # Checks if there is argument 3, 4 - request for optimal schedule (-o) will be ignored without specifying number of missing members (-m)
    try:
        fullhouse = sys.argv[3]
        max_num_memb_missing = sys.argv[4]
    except:
        generate_practice_times(n, master, members_arr)
        for o in others: print(o[0], o[1].replace("\n", "; "))
        exit(1)

    if fullhouse == "o":        # this if/else format may need to be changed in the future if there are other options
        try:
            max_num_memb_missing = int(max_num_memb_missing)
            generate_practice_times_2(n, master, members_arr, max_num_memb_missing)
            for o in others: print(o[0], o[1].replace("\n", "; "))

            # note to self: exit() out of method for testing will still print the exception text
        except Exception as e:
            print("Maximum number of members missing (arg 4) must be an integer.")
            return e

    else:
        print("Invalid: 3rd argument is not 'o'")

    pass

if __name__ == '__main__':
    sys.exit(main())

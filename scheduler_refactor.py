# Script to generate practice schedules based on member avails
# Takes member avails (array of 7) as input
# Studio avails similar to member avails as input
# ideas on ipad rn

import sys
from sys import argv
import datetime
import pprint
import copy
import calendar
import numpy as np

import dtconvert
import membexcel
from Schedule import Schedule, ExSchedule

# Create grid/master schedule
MASTER = Schedule('9:00', '22:30', "Master", None)

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
            s += m[0] + " (" + get_time(MASTER.start, m[1]) + "-" + get_time(MASTER.start, m[-1]+1) + "), "
        return s[:-2]
    else:
        return

# mid-refactor: this is definitely not dry
def get_time(st_t, i):
    dtdt = datetime.datetime.combine(datetime.date(1, 1, 1), st_t)
    diff_i = datetime.timedelta(minutes=30*i)
    comb = dtdt + diff_i
    comb = comb.time()
    return comb.strftime("%H:%M")          # appends without seconds

def missing_memb_practices(ex_schedule, m, MASTER):
    name = "Missing " + str(m) + " member(s)"
    mod_sched = membexcel.member_schedule(MASTER, ["free" for i in range(7)], name, False)

    for d, day in enumerate(ex_schedule.exarray):       # d: 0-6, [a,....,a] (26 a, a=[T,T,T])
        for i, timeslot in enumerate(day):
            if (np.sum(timeslot) >= (len(timeslot) - m)):                     # counts number of True
                mod_sched.array[d][i] = True
            else:
                mod_sched.array[d][i] = False
    return mod_sched

# Heavy lifting: generates the practice schedule
def gen_pract_times(n, MASTER, members_in, num_missing):
    membs = ""
    for memb in members_in:
        membs += memb.name + ", "
    print("Members: "+ membs[:-2])

    if not num_missing:
        print("Generating full house practice times...")
    else:
        print("Generating best practice times (missing max", num_missing, "member(s))...")
        practice = ExSchedule('9:00', '22:30', len(members_in), membs)

    # See the schedules
    text = input("View member schedules? [y/n, default is no] ")
    if text.lower() == "y":
        for m in members_in:
            m.visualize()

    print("Schedule set from: " + str(MASTER.start) + " - " + str(MASTER.end))

    if not num_missing:
        text = input("Visualize comparison? [y/n] ")
        if text.lower() == "y":     view_comp_sched = True
        else:                       view_comp_sched = False

        print("### IMPLEMENTATION 1: ###\n###  FULL HOUSE ONLY  ###")
        mod = None
        for i, m in enumerate(members_in):      # nasty for loop comparing every schedule
            if mod is None:
                mod = compare_schedules(members_in[0], members_in[1])
                if view_comp_sched:
                    mod.visualize()
            else:
                try:
                    mod = compare_schedules(mod, members_in[i+1])
                    if view_comp_sched:
                        mod.visualize()
                except: pass
        mod.visualize()
        for m in members_in: m.print_other()
        get_practice_range(n, mod, False, members_in)

        return mod

    else:
        print("#### IMPLEMENTATION 2: ####\n#  WITH N MISSING MEMBERS #")
        for i, m in enumerate(members_in):
            for d in range(7):                                      # d: days of the week (0-6)
                for hr in range(len(practice.exarray[0])):          # hr: hours in the day
                    practice.exarray[d][hr][i] = m.array[d][hr]

            # print(practice.exarray[0]) # monday
            # print(practice.exarray[0][0]) # monday at 9
            # print(practice.exarray[0][0][i]) # monday at 9 for first member
            # print(m.array[0]) # member monday
            # print(m.array[0][0]) # member monday at 9

        practice.visualize()
        # converts ex_schedule to schedule with num_missing in consideration
        simple_sched = missing_memb_practices(practice, num_missing, MASTER)
        simple_sched.visualize()
        for m in members_in: m.print_other()
        # returns range of true (Sun --> Mon)
        get_practice_range(n, mod_practice, practice, members_in)
        return

# HELPER - gen_pract_times()
def compare_schedules(orig_sched, comp_sched):
    print("Comparing schedules: ", orig_sched.name, comp_sched.name)
    new_sched = copy.copy(orig_sched)
    new_sched.name = str(orig_sched.name) + " + " + str(comp_sched.name)

    # Check if both sched free at this time
    for d, day in enumerate(new_sched.array):
        for i, timeslot in enumerate(day):
            new_sched.array[d][i] = timeslot & comp_sched.array[d][i]
    return new_sched

# HELPER - gen_pract_times()
# returns all potential practice times in a range (per day)
# mod is a schedule object
def get_practice_range(n, mod, ex_pract, members_in):
    skip = False
    r_comb = []

    print("######### Weekly Schedule: #########")
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
        dtdt = datetime.datetime.combine(datetime.date(1,1,1), st_t)

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
            print("| missing: ", whos_missing(schedlist, ex_pract.exarray[i], [m.name for m in members_in]))            # compare mod to ex_pract and see who's missing
        else: print()

    suggest_prac(n, r_comb)

    return r_comb

# uses get_practice_range output (r_comb) to suggest n practice dates and 1 filming date
def suggest_prac(n, r_comb):

    print()
    print("######### Suggested dates: #########")                   # 0 = sun
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
                print("\n######### FILMING: #########")

            print((weekday + datetime.timedelta(days=i-1)).strftime("%A, %B %d %Y"), end=": ")
            for dt in r_comb[j]:
                print(dt[0].strftime("%H:%M"), end="-")
                print(dt[1].strftime("%H:%M"), end=" ")
            print()
                # print(r_comb[j])                # this is just showing what's in rcomb (datetime stuff)
            n -= 1
        i += 1

    return weekday


###################################
############## main ###############
###################################


def main():
    # Procressing input: excel file
    try:
        path = sys.argv[1]
        if not path.endswith(".xlsx"):
            print("Please enter valid path to excel file.")
            exit(1)
    except:
        print("Error: path to excel file (argument 1).")
        exit(1)

    # Processing input: how many practices
    try:
        n = int(sys.argv[2])
    except:
        print("Please specify number of desired practices in second argument.")
        exit(1)

    try:
        members_in = membexcel.create_members_from_excel(MASTER, path, False)
        print("Finished reading member schedules from excel file.")
    except:
        print("Error reading excel file.")
        exit(1)

    # Check: number of missing members specified?
    try:
        num_missing = int(sys.argv[3])
        gen_pract_times(n, MASTER, members_in, num_missing)
    except:
        print("\nInvalid or missing arg 3: number of members missing (arg 3) must be an integer.")
        text = input("Default to 0 members missing? [enter any key to continue, or n to exit] ")
        gen_pract_times(n, MASTER, members_in, num_missing=None) if "n" not in text.lower() else exit(1)
    pass

if __name__ == '__main__':
    sys.exit(main())

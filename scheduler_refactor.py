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

# mid-refactor: this is definitely not dry
def get_time(i):
    comb = get_time_raw(i)
    return comb.strftime("%H:%M")          # appends without seconds

def get_time_raw(i):
    dtdt = datetime.datetime.combine(datetime.date(1, 1, 1), MASTER.start)
    diff_i = datetime.timedelta(minutes=30*i)
    comb = dtdt + diff_i
    comb = comb.time()
    return comb

def str_convert(str_time):
    # Converts start/end time to datettime if entered as string
    if isinstance(str_time, str):
        str_time = datetime.datetime.strptime(str_time, '%H:%M')
        return datetime.time(str_time.hour, str_time.minute)
    return str_time

# Heavy lifting: generates the practice schedule
def gen_pract_times(num_pract, MASTER, members_in, num_missing):
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
        get_practice_range(num_pract, mod, False, members_in)

        return mod

    else:
        print("\n\n\n#### IMPLEMENTATION 2: ####\n# WITH N MISSING MEMBERS  #")
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
        get_practice_range(num_pract, simple_sched, practice, members_in)
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
def get_practice_range(n, final_avails, ex_pract, members_in):
    dt_ranges = []
    skip = False

    print("\n######### Weekly Schedule: #########")
    for i, day_avails in enumerate(final_avails.array):     # day_avails is list of True, False

        # Prints the day of week ("Sun: "), shifted back by 1 to start on sunday
        print(calendar.day_abbr[(i-1)%7], end=": ")

        try:
            true_ranges = get_ranges(day_avails)

            # Use indices in true_ranges to find associated datetime objects
            # Store in true_range_dt
            dt_range = []
            true_range_dt = []
            for ranges in true_ranges:
                dt_range.append([get_time_raw(time) for time in ranges])
                true_range_dt.append([get_time(time) for time in ranges])
            dt_ranges.append(dt_range)

            for t_i, t_range in enumerate(true_range_dt):
                start = t_range[0]
                end = t_range[1]
                print(start, end="-")
                if t_i is not 0 and len(true_range_dt) > 1:
                    print(end, end="")
                elif len(true_range_dt) is 1:
                    print(end, end="")
                else:
                    print(end, end=", ")

        except:
            print("None", end="")
            dt_ranges.append(None)
            pass

        if(): print()
        elif ex_pract is not False:
            print("\t| missing: ", whos_missing(day_avails, ex_pract.exarray[i], [m.name for m in members_in]))            # compare final_avails to ex_pract and see who's missing
        else: print()

    suggest_prac(n, dt_ranges)
    return dt_ranges

def get_ranges(day_avails):
    true_ranges = []
    switch = 0                                          # Track when T <-> F

    for j, timeslot in enumerate(day_avails):           # Enumerate used to check last timeslot
        if timeslot is True and switch == 0:
            switch = 1
            true_ranges.append(j)
        if timeslot is False and switch == 1:
            switch = 0
            true_ranges.append(j)
        elif j == len(day_avails)-1 and timeslot is True:    # Last timeslot check
            true_ranges.append(j)
    # Split true_ranges into lists of size 2
    true_ranges = [true_ranges[x:x+2] for x in range(0, len(true_ranges), 2)]

    if len(true_ranges[0]) == 1:
        true_ranges.append(len(day_avails))
    return true_ranges

# uses get_practice_range output (dt_ranges) to suggest n practice dates and 1 filming date
def suggest_prac(n, dt_ranges):
    print()
    print("######### Suggested dates: #########")
    weekday = datetime.date.today()
    idx = (weekday.weekday() + 1) % 7           # 0 = sun
    i = 1
    n += 1                                      # Index for the filming

    while(n is not 0):
        # get n index where dt_ranges isn't None
        # if (thing at idx+1 is not None:):
        j = (idx+i-1)%7

        # STORE practice dates + PRINT
        if dt_ranges[j] is not None:
            if n == 1:
                print("\n######### FILMING: #########")

            print((weekday + datetime.timedelta(days=i-1)).strftime("%A, %B %d %Y"), end=": ")
            for dt in dt_ranges[j]:
                print(dt[0].strftime("%H:%M"), end="-")
                print(dt[1].strftime("%H:%M"), end=" ")
            print()
                # print(dt_ranges[j])                # this is just showing what's in rcomb (datetime stuff)
            n -= 1
        i += 1

    return weekday

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

def whos_missing(mods, day, members):
    missing = []
    m_time = []

    # print(day) # sunday (for i=0)
    # print(day[0]) # sunday at 9
    # print(day[0][m]) # sunday at 9 for first member

    for t, time in enumerate(mods):                                             # compare schedlist[i = 0-26]
        if time is True:
            # if FREE, check if day[0 to 26] FREE (f = [] if no False)
            f = [i for i, bool in enumerate(day[t]) if bool==False]
            # if NOT free, f gives to get m index
            if f:
                for m in f:
                    m_time = [members[m], t]
                    missing.append(m_time)

    # clean missing array
    clean = []
    if missing:
        for m in missing:
            if any(m[0] in n for n in clean):
                clean[next((i for i, sublist in enumerate(clean) if m[0] in sublist))].append(m[1])
            else:
                clean.append(m)

    if clean:
        s = ""
        for m in clean:
            s += m[0] + " (" + get_time(m[1]) + "-" + get_time(m[-1]+1) + "), "
        return s[:-2]
    else:
        return


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
        num_pract = int(sys.argv[2])
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
        gen_pract_times(num_pract, MASTER, members_in, num_missing)
    except:
        print("\nInvalid or missing arg 3: number of members missing (arg 3) must be an integer.")
        text = input("Default to 0 members missing? [enter any key to continue, or n to exit] ")
        gen_pract_times(num_pract, MASTER, members_in, num_missing=None) if "n" not in text.lower() else exit(1)
    pass

if __name__ == '__main__':
    sys.exit(main())

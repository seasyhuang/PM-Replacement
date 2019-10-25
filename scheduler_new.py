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

def member_schedule(master, avails, name):
    m_sched = schedule(master.start, master.end, name)          # Set array/schedule size to same as master

    for i in range(len(m_sched.sched)):                         # Modify array with avails
        day_avail = avails[i]                                   # At this step, still strings (no dateetime conversion)
        # print("day avail: ", end="")
        # print(day_avail)

        print(str(i) + ": ", end="")
        dt_se = dtconvert.convert_to_datetime(day_avail, master)                  # UPDATE: dt_se is the 2D list ("ranges")

        m_sched = modify_schedule(m_sched, dt_se, i)            # new version


    # NEXT TODO: Modify to add exceptions - right now exceptions are still None
    # print("Exceptions: " + str(avails[7]))

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
def get_practice_range(mod):
    for i, schedlist in enumerate(mod.sched):               # schedlist is list of True, False

        print(calendar.day_abbr[(i-1)%7], end=": ")         # for python's calendar function to work, need to shift all by 1

        true_range = []                                     # saves indices
        true_range_dt_to_string = []
        switch = 0
        for i, bool in enumerate(schedlist):
            if bool is True and switch == 0:
                # print(i)
                switch = 1
                true_range.append(i)
            if bool is False and switch == 1:
                switch = 0
                true_range.append(i)
        if len(true_range) == 1:
            true_range.append(len(schedlist))

        # true_range stores the indices: use them to find associated datetime objects
        st_t = mod.start
        e_t = mod.end
        dtdt = datetime.datetime.combine(datetime.date(1, 1, 1), st_t)
        for ind in true_range:
            diff_i = datetime.timedelta(minutes=30*ind)
            comb = dtdt + diff_i
            comb = comb.time()
            true_range_dt_to_string.append(str(comb.strftime("%H:%M")))

        if not true_range_dt_to_string: # Catch for days with no practice times
            print("None")
            pass

        start = True                    # Boolean switch for start - end
        single_range = True             # Boolean switch for number of ranges
        if len(true_range_dt_to_string) > 2: single_range = False
        for idj, j in enumerate(true_range_dt_to_string):
            if single_range is True:
                print(true_range_dt_to_string[0] + "-" + true_range_dt_to_string[1])
                break
            else:
                if start is True:
                    print(j, end="-")
                    start = False
                else:
                    if not (idj+1 == len(true_range_dt_to_string)):
                        print(j, end=", ")
                    else:
                        print(j)
                    start = True

        # start_range = true_range[0]       # this won't work if true_range is extended for multiple ranges
        # end_range = true_range[1]         # maybe true_range = 2d array? --> start = true_range[i][0]

        # if true_range is empty, return None

        # TODO: datetime for date, not just weekly schedule --> for now, just hardcode
        # my_date = date.today()
        # calendar.day_name[my_date.weekday()]
    range = []
    return range

# This method does all of the heavy lifting: generates the practice schedule
# IMPLEMENTATION 1: return times all members free
# IMPLEMENTATION 2: test with more members, return "best" times (doesn't have to be all free) (kenny array idea)
# -- idea for option: specify how many practices needed
def generate_practice_times(master, members_in):
    print("Generating practice times...")

    print("Members: ", end="")
    for memb in members_in:
        print(memb.name, end=", ")
    print()

    #  members - list of all members (as member_schedule objects)
    print("Schedule set from: " + str(master.start) + " - " + str(master.end))

    # # for testing, so we can see the schedules
    # for m in members_in:
    #     visualize_week(m)

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

    # CURRENTLY prints instead of returning
    get_practice_range(mod)                                         # returns range of true (Sun --> Mon)

# Returns list of member_schedule objects
def create_members_from_excel(master, excel_path):
    members_arr = []

    twice = pd.read_excel(excel_path, header=1)      # setting the header = 1 removes the title
    print(twice.head)
    print(twice.columns)

    # for i in range(10):          # CHANGE when TESTING VALUES
    for i in range(len(twice.columns)):
        week = []
        name = twice['NAME'].iloc[i]                # same as twice.columns[0]. TODO: maybe put a check on this?
        # print(twice.columns[0])
        # from 1 to 7
        for d in range(7):                          # TODO: set for d in range(7): ---> for d in range(8): once exceptions (other) can be handled
            day_header = twice.columns[d+1]
            print(day_header, end=": ")
            day_avail = twice[day_header].iloc[i]
            print(day_avail)
            week.append(day_avail)

        week.append(None)                           # TODO: this is a placeholder for exceptions (other)
        print(name)
        member = member_schedule(master, week, name)

        visualize_week(member)
        members_arr.append(member)

    return members_arr

    # member1_2 = member_schedule(master, member_1_2cases, "member 1 with 2 inputs")
    # member2 = member_schedule(master, member_2, "member 2")
    # member3 = member_schedule(master, member_3, "member 3")

##########################################
# move this eventually to a test class
member_1 = [
    "10:30-21:00",
    "Free",
    "10:30-21:00",
    "6- 8",
    "6-8",
    "1pm-6pm",
    "1pm-6:00pm",
    None ]
member_1_2cases = [
    "6-8, 9-10",                # 9-10 is interpreted as 9am-10am --> actually this may be the best case
    "Free",
    "10:30am-4:00pm, 18:00-21:00",
    "6- 8",
    "6-8, 9pm-10pm",
    "1pm-6pm",
    "1pm-6:00pm",
    None ]
member_2 = [
    "free",
    "6pm-9pm",
    "6pm-8pm",
    "6pm-8pm",
    "6pm-8pm",
    "6pm-8pm",
    "free",
    None ]
member_3 = [
    "After 6",
    "After 12h",
    "After 6h",
    "After 5",
    "After 10 am",
    "Free",
    "Free except 16h30-18h30",
    None ]

# var1 = argv[1]
##########################################

def main():
    """ Create grid/master schedule """
    master = schedule('9:00', '22:00', "master")

    ###### Testing ######
    # member1 = member_schedule(master, member_1, "member 1")
    # member1_2 = member_schedule(master, member_1_2cases, "member 1 with 2 inputs")
    # member2 = member_schedule(master, member_2, "member 2")
    # member3 = member_schedule(master, member_3, "Cindy")
    # visualize_week(member3)
    # exit(1)

    ###### Testing with excel ######
    twice = "test_twice.xlsx"
    members_arr = create_members_from_excel(master, twice)
    generate_practice_times(master, members_arr)
    exit(1)

    # visualize_day(member1, 5)     # 0 = sunday
    visualize_week(member1_2)
    visualize_week(member2)
    ###### Testing End ######

    # members = [member1, member2, member3]                     # Creating member_schedule objects as input
    members = [member1_2, member2]                              # testing with case: 2 inputs
    generate_practice_times(master, members)                    # generate_practice_times method only takes member_schedule OBJECTS as input

    pass



if __name__ == '__main__':
    sys.exit(main())

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

# HELPER for extracting avails --> datetime time objects
# Ex str input: "10:30-21:00" --> out: start and end (dt time objs)
def convert_to_datetime(str):
    # str = "10:30-21:00"               # UPDATE: that allow 2+ ranges
    ranges = []                         # Store all start, end pairs together (in separate arrays) inside "ranges"
    split_string = [st_end.strip() for st_end in str.split(',')]
    for str in split_string:
        start = 0
        end = 0

        try:    avail = str.lower()                         # Safety: if the string is a word ("Free")
        except: avail = str

        if avail == 'free':                                 # Case: if it's the word free then set to True
            start = True
            end = True
        elif avail is None:
            start = False
            end = False
        else:                                               # It's a time, so further processing has be done
            avail.replace(" ", "")                          # Removing whitespace
            times = avail.split("-")                        # Split into start and end time
            times = [t.replace(" ", "") for t in times]     # Safety whitespace

            # print("splitting:", end=" ")
            # print(times)
            # TODO: striptime has functionality that can detect weekday = could use + w/ gui? (%a/%A)

            dt_av = []
            for time in times:
                converted = convert(time)
                dt_av.append(converted)

            start = dt_av[0]
            end = dt_av[1]

        ranges.append([start, end])
    return ranges

# HELPER to convert whatever input time is in --> datetime time object
# Text parsing in a bad way that tries to predict what members input
# Ex: 6pm, 6:00, 6
def convert(time):
    # 6 --> make assumptions --> pass through strptime
    if time.isdigit():   # checks if numeric only: "6:00".isdigit() --> false
        try:
            time = int(time)
            if time < 9:    time = str(time) + ":00pm"
            else:           time = str(time) + ":00am"
            dt_time = datetime.datetime.strptime(time, "%I:%M%p").time()
            return dt_time
        except Exception:
            return False

    # 6:00pm --> pass through strptime
    elif len(time) > 5:
        dt_time = datetime.datetime.strptime(time, "%I:%M%p").time()
        return dt_time

    # 6pm --> fix so it's 6:00pm --> pass through strptime
    elif ":" not in time:
        apm = time[-2:]             # get am or pm
        t = time[:-2]               # get time (ex. 6)
        time = t + ":00" +  apm     # fix to add :00
        dt_time = datetime.datetime.strptime(time, "%I:%M%p").time()
        return dt_time

    # 6:00, 12:00
    elif ((":" in time) and (len(time) < 6)):
        dt_time = datetime.datetime.strptime(time, '%H:%M').time()
        return dt_time

    else:
        return False

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
    print("######### VISUALIZING WEEK: " + schedule.name + " #########")       # todo: there's a strptime method that converts int to day of week
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
                m_sched_mod.sched[i][s] = False                 # Set all to False
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

        # TODO: pretty sure this logic doesn't work but i need to visualize it first
        for j in range(num_slot_end)[num_slot_start:]:
            m_sched_mod.sched[i][j] = True


    return m_sched_mod

def member_schedule(master, avails, name):
    m_sched = schedule(master.start, master.end, name)          # Set array/schedule size to same as master

    for i in range(len(m_sched.sched)):                         # Modify array with avails
        day_avail = avails[i]                                   # At this step, still strings (no dateetime conversion)
        # print("day avail: ", end="")
        # print(day_avail)

        dt_se = convert_to_datetime(day_avail)                  # UPDATE: dt_se is the 2D list ("ranges")

        print(dt_se)
        print(dt_se[0])

        # TODO: next step is to change modify_schedule so it takes in dt_se (ranges) instead of dt_start, dt_end individually
        m_sched = modify_schedule(m_sched, dt_se, i)            # new version
        visualize_week(m_sched)
        exit(1)


    # TODO: Modify to add exceptions
    # print("Exceptions: " + str(avails[7]))

    return m_sched

# HELPER for generate_practice_times()
# Both t and m are schedule objects (start, end, sched)
### t - temp, could be master, could be ouput of previous iteration of this function (mod)
### m - member to compare
def compare_schedules(t, m):
    mod = copy.copy(t)
    mod.name = "updated"

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
    for i, schedlist in enumerate(mod.sched):

        print(calendar.day_abbr[(i-1)%7], end=": ")        # for python's calendar function to work, need to shift all by 1

        # print(schedlist)
        # looks at the the schedlist for each day, find all "ranges" of True
        true_range = []
        true_range_dt_to_string = []
        switch = 0
        for i, bool in enumerate(schedlist):
            if bool is True and switch == 0:
                # print(i)
                switch = 1
                true_range.append(i)
            if bool is False and switch == 1:
                switch = 0
                true_range.append(i-1)
        # print(true_range)

        # (currently only one range) true_range stores the indices: use them to find associated datetime objects
        # maybe use logic from visualize helper?
        st_t = mod.start
        e_t = mod.end
        dtdt = datetime.datetime.combine(datetime.date(1, 1, 1), st_t)
        for ind in true_range:
            diff_i = datetime.timedelta(minutes=30*ind)
            comb = dtdt + diff_i
            comb = comb.time()
            true_range_dt_to_string.append(str(comb.strftime("%H:%M")))

        for j in true_range_dt_to_string:   # super gross printing method but whatever for now
            print(j, end="-")               # TODO: fix how gross it is
        print()

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

    #  members - list of all members (as member_schedule objects)
    print("Schedule set from: " + str(master.start) + " - " + str(master.end))

    # for testing, so we can see the schedules
    for m in members_in:
        visualize_week(m)

    ### IMPLEMENTATION 1: ###
    ###  FULL HOUSE ONLY  ###
    # Use compare_schedules helper to determine free times
    mod = None
    for i, m in enumerate(members_in):
        if mod is None:
            mod = compare_schedules(members_in[0], members_in[1])
        else:
            mod = compare_schedules(mod, members_in[i])             # Why this doesn't feel right lol
    visualize_week(mod)                                             # Visualizing modified week outside of the method

    # CURRENTLY prints instead of returning
    get_practice_range(mod)                                         # returns range of true (Sun --> Mon)

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
    "6-8, 9-10",            # here is the 2 inputs
    "Free",
    "10:30-21:00",
    "6- 8",
    "6-8, 9-10",            # here is the 2 inputs
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
    "free",
    "4pm-6pm",
    "4pm-6pm",
    "5pm-7pm",
    "4pm-6pm",
    "4pm-6pm",
    "2pm-4pm",
    None ]

# var1 = argv[1]
##########################################

def main():
    """ Create grid/master schedule """
    master = schedule('9:00', '22:00', "master")

    ex_start = '10:00'  # start at 10am
    ex_end = '16:30'    # end 4:30pm

    ###### Testing ######
    # member1 = member_schedule(master, member_1, "member 1")
    member1_2 = member_schedule(master, member_1_2cases, "member 1 with 2 inputs")
    member2 = member_schedule(master, member_2, "member 2")
    member3 = member_schedule(master, member_3, "member 3")

    # print(member1.start)
    # print(member1.end)
    # print(len(member1.sched[0]))

    # visualize_day(member1, 5)     # 0 = sunday
    visualize_week(member1_2)
    visualize_week(member2)
    # exit(1)
    ###### Testing End ######

    # members = [member1, member2, member3]                    # Creating member_schedule objects as input
    members = [member1_2, member2]                        # testing with case: 2 inputs
    generate_practice_times(master, members)        # generate_practice_times method only takes member_schedule OBJECTS as input

    pass



if __name__ == '__main__':
    sys.exit(main())

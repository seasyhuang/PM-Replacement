# Script to generate practice schedules based on member avails
# Takes member avails (array of 7) as input
# Studio avails similar to member avails as input
# ideas on ipad rn

import sys
from sys import argv
import datetime
import pprint

class schedule:
    def __init__(self, start, end):
        format = '%H:%M'    # hours and minutes only
        self.start = start
        self.end = end
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
    # str = "10:30-21:00"
    start = 0
    end = 0

    try:       # create this avail thing that will be split into start and end
        avail = str.lower()
        # could remove whitespace too ?? # TODO:
    except:
        avail = str

    # Case: if it's the word free then set to True
    if avail == 'free':
        start = True
        end = True
    elif avail is None:
        start = False
        end = False
    else:                                               # It's a time, so further processing gotta be done
        avail.replace(" ", "")                          # Removing whitespace
        times = avail.split("-")                        # Split into start and end time
        times = [t.replace(" ", "") for t in times]     # Safety whitespace

        # print("splitting:", end=" ")
        # print(times)
        # TODO: striptime has functionality that can detect weekday = could use + w/ gui? (%a/%A)

        dt_av = []
        for time in times:
            converted = convert(time)
            # print(converted)
            dt_av.append(converted)

        start = dt_av[0]
        end = dt_av[1]

    return start, end

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
    print("######### VISUALIZING WEEK #########")       # todo: there's a strptime method that converts int to day of week
    print(st_t, end=" - ")
    print(e_t)
    print("-")

    diff_hr = e_t.hour - st_t.hour
    diff_min = e_t.minute - st_t.minute
    diff = diff_hr * 2 + int(diff_min/30)        # number of 1/2 hr slots

    # create toprint array that stores time (0) and schedules (1->7)
    # not great because index is now off by 1  ¯\_(ツ)_/¯
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
        print()

# HELPER for changing member schedule
def modify_schedule(m_sched, dt_start, dt_end, i):
    m_sched_mod = m_sched

    if ((dt_start is True) and (dt_end is True)):
        for s in range(len(m_sched_mod.sched[i])):          # Set all to True
            m_sched_mod.sched[i][s] = True
        return m_sched_mod

    for s in range(len(m_sched_mod.sched[i])):          # Set all to false
        m_sched_mod.sched[i][s] = False

    if ((dt_start is False) and (dt_end is False)):
        return m_sched_mod
    # print(m_sched_mod.sched[i])

    # print(m_sched_mod.start)
    # print(m_sched_mod.end)
    # print(i)        # --> 0 is sunday

    # Get difference between start of master schedule and start of member avail (on day i)
    t_hr_start = dt_start.hour - m_sched_mod.start.hour
    t_min_start = dt_start.minute - m_sched_mod.start.minute
    num_halfhr_start = int(t_min_start/30)
    t_hr_end = dt_end.hour - m_sched_mod.start.hour
    t_min_end = dt_end.minute - m_sched_mod.start.minute
    num_halfhr_end = int(t_min_end/30)

    # Turn the difference into num "slots" (to be used in the schedule list)
    # print("diff: ", end="")
    # print(str(t_hr_start) + ":" + str(t_min_start))
    # print(str(t_hr_end) + ":" + str(t_min_end))
    num_slot_start = t_hr_start * 2 + num_halfhr_start
    num_slot_end = t_hr_end * 2 + num_halfhr_end

    # print("num slots start: " + str(num_slot_start))
    # print("num slots end: " + str(num_slot_end))

    # TODO: pretty sure this logic doesn't work but i need to visualize it first
    for j in range(num_slot_end)[num_slot_start:]:
        # print(j)
        m_sched_mod.sched[i][j] = True

    # print(m_sched_mod.sched[i])

    return m_sched_mod

def member_schedule(master, avails):
    m_sched = schedule(master.start, master.end)        # Set array/schedule size to same as master

    for i in range(len(m_sched.sched)):                 # Modify array with avails
        day_avail = avails[i]
        # print("day avail: ", end="")
        # print(day_avail)

        dt_start, dt_end = convert_to_datetime(day_avail)   # Where dt_start and end are the avails members put in
        # print(str(dt_start) + ", " + str(dt_end))

        m_sched = modify_schedule(m_sched, dt_start, dt_end, i)
        # print("---")


    # TODO: Modify to add exceptions
    # print("Exceptions: " + str(avails[7]))

    return m_sched

# Both t and m are schedule objects (start, end, sched)
### t - temp, could be master, could be ouput of previous iteration of this function (mod)
### m - member to compare
def compare_schedules(t, m):
    print(t.sched)
    print(m.sched)
    return mod

# This method does all of the heavy lifting: generates the practice schedule
# IMPLEMENTATION 1: return times all members free
# IMPLEMENTATION 2: test with more members, return "best" times (doesn't have to be all free) (kenny array idea)
# -- idea for option: specify how many practices needed
def generate_practice_times(master, members_in):
    print("Generating practice times...")


    #  members - list of all memebrs (for member in members, do:
    #  member1 = member_schedule(master, member_1)

    print("Schedule set from: " + str(master.start) + " - " + str(master.end))

    # members is an array holding member_schedule objects (after everything in members_in is converted)
    members = []
    for member in members_in:
        members.append(member_schedule(master, member))

    # for testing, so we can see the schedules
    for m in members:
        visualize_week(m)

    ### IMPLEMENTATION 1: ###
    ###  FULL HOUSE ONLY  ###
    # Use compare_schedules helper to determine free times




    # return list of practice times, --> which can be visualized outside of the method

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

    # "10:30-21:00",
    # "10:30-21:00",
    # "10:30-21:00",
    # "10:30-21:00",
    # "10:30-21:00",
    # "10:30-21:00",
    # "10:30-21:00",
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
    "4pm-6pm",
    "4pm-6pm",
    "4pm-6pm",
    "1pm-8pm",
    None ]

# var1 = argv[1]
##########################################

def main():
    """ Create grid/master schedule """
    master = schedule('9:00', '22:00')

    ex_start = '10:00'  # start at 10am
    ex_end = '16:30'    # end 4:30pm

    ###### Testing ######
    member1 = member_schedule(master, member_1)
    member2 = member_schedule(master, member_2)

    # print(member1.start)
    # print(member1.end)
    # print(len(member1.sched[0]))

    # visualize_day(member1, 5)     # 0 = sunday
    # visualize_week(member1)
    # visualize_week(member2)
    ###### Testing End ######

    # modify members to include names? lmao
    members = [member_1, member_2]

    generate_practice_times(master, members)

    pass



if __name__ == '__main__':
    sys.exit(main())

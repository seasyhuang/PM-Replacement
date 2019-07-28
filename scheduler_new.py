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

        print("splitting:", end=" ")
        print(times)
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

def visualize(schedule, day):
    st_t = schedule.start
    e_t = schedule.end
    arr2d = schedule.sched

    print(st_t, end=" - ")
    print(e_t)
    print("-")

    diff_hr = e_t.hour - st_t.hour
    diff_min = e_t.minute - st_t.minute
    diff = diff_hr * 2 + int(diff_min/30)        # number of 1/2 hr slots

    for i in range(diff):
        # convert to datetime.datetime object, add timedelta, convert back
        dtdt = datetime.datetime.combine(datetime.date(1, 1, 1), st_t)
        diff_i = datetime.timedelta(minutes=30*i)
        comb = dtdt + diff_i
        comb = comb.time()
        print(comb.strftime("%H:%M"), end="\t|")           # prints without seconds

        if arr2d[day][i] is True:
            print(" |")
        if arr2d[day][i] is False:
            print("x|")

    exit(1)



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

    print("num slots start: " + str(num_slot_start))
    print("num slots end: " + str(num_slot_end))

    # TODO: pretty sure this logic doesn't work but i need to visualize it first
    for j in range(num_slot_end-num_slot_start)[num_slot_start:]:
        m_sched_mod.sched[i][j] = True

    print(m_sched_mod.sched[i])

    return m_sched_mod

def member_schedule(master, avails):
    m_sched = schedule(master.start, master.end)    # Set array/schedule size to same as master

    for i in range(len(m_sched.sched)):               # Modify array with avails
        day_avail = avails[i]
        print("day avail: ", end="")
        print(day_avail)

        dt_start, dt_end = convert_to_datetime(day_avail)
        print(str(dt_start) + ", " + str(dt_end))

        m_sched = modify_schedule(m_sched, dt_start, dt_end, i)
        print("---")


    # TODO: Modify to add exceptions
    print(avails[7])

    return m_sched

##########################################
# move this eventually to a test class
member_1 = [
    "10:30-21:00",
    "Free",
    "FREE",
    "10:30-21:00",
    "6- 8",
    "6-8",
    "1pm-9pm",

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
    master = schedule('9:00', '21:00')

    ex_start = '10:00'  # start at 10am
    ex_end = '16:30'    # end 4:30pm

    member1 = member_schedule(master, member_1)
    visualize(member1, 6)

    ###### Testing ######
    print(member1.start)
    print(member1.end)
    # pprint.pprint(member1.arr)
    print(len(member1.sched[0]))

    pass



if __name__ == '__main__':
    sys.exit(main())

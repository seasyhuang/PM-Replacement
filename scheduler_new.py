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
        self.arr = [[True for x in range(sched_size)] for y in range(7)]

    def mod_sched(self):
        # do we even need this method
        self.arr.append(self.start + self.end)
        print(self.arr)

# helper for extracting avails --> datetime time objects
# example str input: "10:30-21:00"
def convert_to_datetime(str):
    str = "10:30-21:00"
    start = 0
    end = 0

    try:
        # create this avail thing that will be split into start and end
        avail = str.lower()
        # could remove whitespace too ?? # TODO:
    except:
        avail = str

    # Case: if it's the word free then set to True
    if avail == 'free':
        start, end = True
    elif avail is None:
        start, end = False
    else:
        # it's a time, so further processing gotta be done
        times = avail.split("-")
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

# Helper to convert whatever input time is in --> datetime
# examples: 6pm, 6:00, 6 (how to handle this one?)
def convert(time):
    # 6 --> make assumptions --> pass through strptime
    if x:   #numeric only
        do stuff
        return dt_time
    # TODO: regex stuff

    # 6pm --> fix so it's 6:00pm --> pass through strptime
    if ":" not in time:
        apm = time[-2:]             # get am or pm
        t = time[:-2]               # get time (ex. 6)
        time = t + ":00" +  apm     # fix to add :00
        dt_time = datetime.datetime.strptime(time, "%I:%M%p").time()
        return dt_time

    # 6:00
    elif:
        # TODO: regex stuff
        dt_time = datetime.datetime.strptime(time, '%H:%M').time()
        return dt_time

    else:
        return False

def member_schedule(master, avails):
    # Set array/schedule size to same as master
    m_sched = schedule(master.start, master.end)

    # Modify array with avails
    for i in range(len(m_sched.arr)):
        day_avail = avails[i]
        print(day_avail)

        dt_start, dt_end = convert_to_datetime(day_avail)
        print(str(dt_start) + ", " + str(dt_end))

    # Modify to add exceptions
    print(avails[7])

    return m_sched

##########################################
# move this eventually to a test class
member_1 = [
    "10:30-21:00",
    "Free",
    "FREE",
    "free",
    "free",
    "free",
    "1pm-9pm",
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

    ###### Testing ######
    print(member1.start)
    print(member1.end)
    # pprint.pprint(member1.arr)
    print(len(member1.arr[0]))

    pass



if __name__ == '__main__':
    sys.exit(main())

# Script to generate practice schedules based on member avails
# Takes member avails (array of 7) as input
# Studio avails similar to member avails as input
# ideas on ipad rn

import sys
from sys import argv
from datetime import datetime

##########################################
# move this eventually to a test class
member_1 = [
    "10:30am-9pm",
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

# var1 = argv[1]
##########################################

def main():
    """Main entry point for the script."""

    # for testing
    # member_avails = [member_1, member_2]
    member_avails = [member_1]

    schedule = []

    extr_avails = []
    for member_av in member_avails:
        extr_avails.append(extract_avails(member_av))

    generate_schedule(extr_avails)

    pass

def extract_avails(avails):
    """ stuff """
    extracted_avails = [None, None, None, None, None, None, None, None]

    for i in range(len(avails)):
        day = avails[i]
        print(day)

        try:
            pr_day = day.lower() # could remove whitespace too ?? pr for processed
        except:
            pr_day = day

        if pr_day == 'free':
            extracted_avails[i] = None
        elif pr_day is None:
            extracted_avails[i] = None
        else:
            # it's a time, so further processing gotta be done
            times = pr_day.split("-")
            print(times)
            # TODO: striptime has functionality that can detect weekday = could use + w/ gui? (%a/%A)

            dt_av = []                          # this is an array to store start + end (does not consider NOT)
                                                # maybe need to change this implementation later
            for time in times:
                # if 6pm --> 6:00pm
                if ":" not in time:
                    apm = time[-2:]             # get am or pm
                    t = time[:-2]               # get time (ex. 6)
                    time = t + ":00" +  apm     # fix to add :00

                converted = datetime.strptime(time, "%I:%M%p").time()
                # print(converted)
                dt_av.append(converted)

            extracted_avails[i] = dt_av

    print(extracted_avails)
    return extracted_avails

def generate_schedule(extr_avails):
    # move this into extracted_avails eventually
    sun = None
    mon = None
    tues = None
    wed = None
    thurs = None
    fri = None
    sat = None
    print("wee woop schedule here u go")

if __name__ == '__main__':
    sys.exit(main())

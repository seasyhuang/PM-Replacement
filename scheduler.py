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
    """Main entry point for the script."""

    # for testing
    member_avails = [member_1, member_2, member_3]

    all_extr_avails = []
    for member_av in member_avails:
        all_extr_avails.append(extract_avails(member_av))

    schedule = generate_schedule(all_extr_avails)
    print_week(schedule)


    pass

def extract_avails(avails):
    """ Maybe changed later to drop down menus/have two options """
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
    schedule = [ None, None, None, None, None, None, None, None ]
    for idx in range(len(schedule)):
        schedule[idx] = [ datetime.strptime("9:00am", "%I:%M%p").time(), datetime.strptime("11:00pm", "%I:%M%p").time() ]

    print("wee woop schedule here u go")

    # passes: check conflict, then change
    for member_avail in extr_avails:
        mod_member_avail = [ None, None, None, None, None, None, None, None ]

        # Set up
        for day_idx in range(len(member_avail)-1):  # ignoring exceptions
            if member_avail[day_idx] is None:       # set to 9am - 11pm for simplicity
                # print("None is now 9am-11pm")
                mod_member_avail[day_idx] = [ datetime.strptime("9:00am", "%I:%M%p").time(), datetime.strptime("11:00pm", "%I:%M%p").time() ]
            else:
                mod_member_avail[day_idx] = member_avail[day_idx]

        # print(mod_member_avail)
        # exit()

        ######## MODIFY SCHEDULE LOOP: ########
        for i in range(7):
            # Temporary schedule, replaces schedule[i] at end of the loop
            mod_sched_day = [ None, None ]

            # Set day start and end
            member_start = mod_member_avail[i][0]
            member_end = mod_member_avail[i][1]

            sched_start = schedule[i][0]
            sched_end = schedule[i][1]

            # Booleans
            sched_start_earlier = sched_start < member_start
            sched_end_later = member_end < sched_end

            print("schedule: " + str(sched_start) + "-" + str(sched_end))
            print("member: " + str(member_start) + "-" + str(member_end))
            # print(member_end<sched_end)

            # Case 1: Schedule is more free than member (schedule ST is earlier than member ST, and schedule ET is later than member ET)
            # Change schedule to member avails
            if(sched_start_earlier and sched_end_later):
                mod_sched_day[0] = member_start
                mod_sched_day[1] = member_end
                print("CASE 1 - New schedule for this day: " + str(mod_sched_day[0]) + "-" + str(mod_sched_day[1]))

            # Case 2: Member more free than schedule
            # Keep schedule, no change
            elif(not sched_start_earlier and not sched_end_later):
                mod_sched_day[0] = sched_start
                mod_sched_day[1] = sched_end
                print("CASE 2 - No schedule change: " + str(mod_sched_day[0]) + "-" + str(mod_sched_day[1]))

            # Case 3: Schedule start earlier and end earlier, overlap
            # change schedule start to member start, schedule end stay same
            elif(sched_start_earlier and not sched_end_later and member_start < sched_end):
                mod_sched_day[0] = member_start
                mod_sched_day[1] = sched_end
                print("CASE 3 - New SS = Old MS, New SE = Old SE: " + str(mod_sched_day[0]) + "-" + str(mod_sched_day[1]))

            # Case 4: Schedule start later and end later, overlap
            # Keep schedule start, change schedule end to member end
            elif(not sched_start_earlier and sched_end_later and sched_start < member_end):
                mod_sched_day[0] = sched_start
                mod_sched_day[1] = member_end
                print("CASE 4 - New SS = Old SS, New SE = Old ME: " + str(mod_sched_day[0]) + "-" + str(mod_sched_day[1]))

            # Case 5: No overlap
            else:
                mod_sched_day = None
                print("CASE 5 - Member and Schedule not compatible.")

            schedule[i] = mod_sched_day

    return schedule

def print_week(week):
    # Where week is an array of size 7 (min, doesn't handle exceptions well yet)
    print("---------------------")

    # Make sure that week is long enough
    if len(week) < 7:
        print("Input incompatible.")
        exit()

    days = [ "Sun", "Mon", "Tues", "Wed", "Thurs", "Fri", "Sat" ]

    for i in range(7):
        try:    practice_start = week[i][0]
        except: practice_start = None
        try:    practice_end = week[i][1]
        except: practice_end = None

        if(practice_start is None):
            print(days[i] + ": None")
        else:
            print(days[i] + ": " + str(practice_start) + " - " + str(practice_end))

    print("---------------------")

if __name__ == '__main__':
    sys.exit(main())

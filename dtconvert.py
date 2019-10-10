import datetime

# HELPER for extracting avails --> datetime time objects
def convert_to_datetime(str):
    ranges = []
    split_string = [st_end.strip().lower() for st_end in str.split(' ')]

    # Does the string have "free"
    if "free" in split_string:
        if len(split_string) > 1:
            # check "after"
            split_string.pop(0)
            print("----")
            bef_betw_aft(split_string)
            # NEXT TODO: helper to deal with "before" and "after"
        else:
            ranges.append([True, True])
            return ranges

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

# Ex str input: "10:30-21:00" --> out: start and end (dt time objs)
def old_convert_to_datetime(str):
    # str = "10:30-21:00"                                                   # UPDATE: that allow 2+ ranges
    ranges = []                                                             # Store all start, end pairs together (in separate arrays) inside "ranges"
    split_string = [st_end.strip().lower() for st_end in str.split(' ')]
    print(split_string)

    # First step: does the string have "Free"
    if "free" in split_string:
        print()

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

# HELPER for convert_to_datetime:
# parses "before", "between", or "after" strings, converts to datetime object
def bef_betw_aft(list):
    dt = 0

    # before/after case
    # list is size 2, unless we have [after, 1, pm] # todo: address this (meiling and audrey)

    # between case
    # list is size 3


    return dt

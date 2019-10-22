import datetime

# HELPER for extracting avails --> datetime time objects
def convert_to_datetime(str, master):
    ranges = []
    split_string = [st_end.strip().lower() for st_end in str.split(' ')]
    print(split_string)

    # first check: if string is 'not' 'avail', reject
    if (split_string[0].startswith('n') and split_string[1].startswith('av')):
        return [[False, False]]

    # Does the string have "free"
    if "free" in split_string:
        if len(split_string) > 1:
            split_string.pop(0)
            ranges = bef_betw_aft(split_string, master)
            return ranges
        else:
            return [[True, True]]
    # no 'free':
    else:
        try:                                                # 1) just avails, 'after 5'
            ranges = bef_betw_aft(split_string, master)
            return ranges
        except:                                             # 2) not avail
            exit(1)
    return ranges

# HELPER to convert whatever input time is in --> datetime time object
# Text parsing in a bad way that tries to predict what members input
# Ex: 6pm, 6:00, 6
def convert(time):
    time = french(time)
    fr = ['13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23']
    try:    hr, min = [hrm for hrm in time.split(':')]
    except: pass

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

    # 16:30
    elif hr in fr:
        try:    dt_time = datetime.datetime.strptime(time, "%H:%M").time()
        except: dt_time = datetime.datetime.strptime(time, "%Hh%M").time()      # not sure this does anything
        return dt_time


    # 6:00, 12:00
    elif ((":" in time) and (len(time) < 6)):
        hrmin = time.split(":")
        hr = int(hrmin[0])
        min = int(hrmin[1])

        if(hr < 9):
            time = str(hr) + ":" + str(min) + "pm"
        else:
            time = str(hr) + ":" + str(min) + "am"

        dt_time = datetime.datetime.strptime(time, "%I:%M%p").time()
        return dt_time

    else:
        return False

# HELPER for convert_to_datetime:
# Parses "before", "between", or "after" strings, converts to two pre-dt times
# DT CONVERSION done in this method!!
# Master needed to get schedule start and end time
def bef_betw_aft(list, master):
    # times = bef_betw_aft(split_string, master)
    # ranges.append([convert(times[0]), convert(times[1])])

    converted = []
    id = list[0].lower().strip()            # after, before, between

    if id == 'after':
        converted.append([
            convert(list[1]),
            convert(master.end.strftime("%I:%M%p"))
            ])

    if id == 'before':
        converted.append([
            convert(master.start.strftime("%I:%M%p")),
            convert(list[1])
            ])

    if id == 'between':
        try:
            se = extract_again(list[1:])
        except:
            print("error running extract_again()")
            exit(1)

        converted.append([
            convert(se[0]),
            convert(se[1])
            ])

    if id == 'except':
        try:
            se = extract_again(list[1:])
        except:
            print("error running extract_again()")
            exit(1)

        converted.append([
            convert(master.start.strftime("%I:%M%p")),
            convert(se[0])
            ])
        converted.append([
            convert(se[1]),
            convert(master.end.strftime("%I:%M%p"))
            ])

    return converted

# messy helper
# in: list, with 'except'/'between'/etc removed
def extract_again(list):
    string = list[0]
    # case 1: 16h30-18h30 (doesn't work with 15 min intervals)
    split_string = [st.strip().lower() for st in string.split('-')]
    # fixing french h/hr
    for i in range(len(split_string)):
        t = split_string[i]
        split_string[i] = french(t)
    return split_string

def french(string):
    if len(string) > 3:
        return string.replace('h', ':')
    else:
        return string.replace('h', '')

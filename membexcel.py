import math
import pandas as pd

from Schedule import Schedule
import dtconvert

# Returns members_arr, a list of member_schedule objects
def create_members_from_excel(MASTER, excel_path, test):
    members_arr = []

    # Read_excel: setting header=1 removes the title
    xsheet = pd.read_excel(excel_path, header=1)
    if test:    print(xsheet.head, xsheet.columns)

    # For every member in the sheet, get avails and assign to Schedule object
    for i, row in xsheet.iterrows():
        week = []

        # Check if sheet is set up properly: name must be at A2
        try:    name = xsheet['NAME']
        except:
            print("Name is not properly formatted.")
            exit(1)

        # Getting avails from SUN - SAT (1 to 7)
        for d in range(7):
            weekday = xsheet.columns[d+1]         # SUN, MON, ...
            if test:    print(weekday, end=": ")
            avail = xsheet[weekday].iloc[i]
            if test:    print(avail)
            week.append(avail)

        name = row[0]
        other = xsheet[xsheet.columns[7+1]].iloc[i]

        # If other was left blank
        try:
            if math.isnan(other):   other = '-'
        except: pass

        member = member_schedule(MASTER, week, name, other)

        if test:
            print(name, member.name)
            member.visualize()

        members_arr.append(member)
    return members_arr


def member_schedule(MASTER, avails, name, other):
    m_sched = Schedule(MASTER.start, MASTER.end, name, other)   # Set array/schedule size to same as MASTER

    for i in range(len(m_sched.array)):                         # Modify array with avails
        day_avail = avails[i]                                   # At this step, still strings (no dateetime conversion)
        dt_se = dtconvert.convert_to_datetime(day_avail, MASTER, False)    # UPDATE: dt_se is the 2D list ("ranges")
        m_sched = modify_schedule(m_sched, dt_se, i)            # new version
    return m_sched


# HELPER for changing member schedule
def modify_schedule(m_sched, dt_se, i):
    m_sched_mod = m_sched
    first_pass = True                                            # Lazy switch for init all false

    for dt_range in dt_se:
        dt_start = dt_range[0]
        dt_end = dt_range[1]

        if ((dt_start is True) and (dt_end is True)):           # Case 1: completely free this day (there should only be 1 dt_range in dt_se)
            for s in range(len(m_sched_mod.array[i])):          # Set all to True
                m_sched_mod.array[i][s] = True
            return m_sched_mod

        if first_pass is True:                                  # Only do this the first time
            for s in range(len(m_sched_mod.array[i])):          # Otherwise will overwrite changes with every dt_range
                m_sched_mod.array[i][s] = False                 # Set all to False (init all false)
                first_pass = False

        if ((dt_start is False) and (dt_end is False)):         # Case 2: completely busy (there should only be 1 dt_range in dt_se)
            return m_sched_mod

        # Case 3: modifications to m_sched_mod happen here
        # Get difference between start of MASTER schedule and start of member avail (on day i)
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
            m_sched_mod.array[i][j] = True

    return m_sched_mod

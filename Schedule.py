import datetime

class Schedule:
    def __init__(self, start, end, name, other):        # Constructor
        self.start = self.str_convert(start)                              # Schedule start time (ex. 9:00)
        self.end = self.str_convert(end)                                  # Schedule end time (ex. 22:00)
        self.name = name                                # Schedule name (ex. member name, final schedule, etc)
        self.other = other                              # Schedule exceptions/"other"
        self.array = self.create_array()                # Schedule array (2D array of days of week (7) x half hour blocks)

    def str_convert(self, str_time):
        # Converts start/end time to datettime if entered as string
        if isinstance(str_time, str):
            str_time = datetime.datetime.strptime(str_time, '%H:%M')
            return datetime.time(str_time.hour, str_time.minute)
        return str_time

    def create_array(self):
        # Generate array from number of (30 minute) blocks
        num_blocks = self.calculate_num_blocks(self.start, self.end)
        return [[True for x in range(num_blocks)] for y in range(7)]

    @staticmethod
    def calculate_num_blocks(start, end):
        # Determining size of array: get difference
        total_hrs = end.hour - start.hour
        total_mins = end.minute - start.minute

        # Determining size of array: in 30 min blocks (rounded)
        num_half_hr = int(total_mins/30)
        num_blocks = 2 * total_hrs + num_half_hr

        return num_blocks

    def prep_visualize(self):
        # Banner
        print("\n######### VISUALIZING WEEK: " + self.name + " #########")
        print(self.start, "-", self.end, "\n")

        num_blocks = self.calculate_num_blocks(self.start, self.end)
        days = ["S", "M", "T", "W", "R", "F", "S" ]
        times = []

        # Fill times column (from datetime obj)
        # Convert to datetime.datetime object, add timedelta, convert back - arbitrary datetime.date(1, 1, 1)
        dtdt = datetime.datetime.combine(datetime.date(1, 1, 1), self.start)
        for i in range(num_blocks):
            num_blocks_i = datetime.timedelta(minutes=30*i)
            combined = (dtdt + num_blocks_i).time()
            times.append(combined.strftime("%H:%M"))

        return days, times

    def visualize(self):
        days, times = self.prep_visualize()

        # HEADER:
        print("#####", end=" ")
        for d in days: print("(" + d + ") ", end="")
        print("#####")

        # SCHEDULE:
        for t in range(len(times)):
            print(times[t], end=" ")
            for d in range(7):
                slot = self.array[d][t]
                if slot is True: slot = "   "
                elif slot is False: slot = " x "
                print(slot, end=" ")
            print(times[t])
        print()

class ExSchedule(Schedule):
    def __init__(self, start, end, num_members, list_membs):
        Schedule.__init__(self, start, end, "ExSched", None)
        self.num_members = num_members
        self.list_membs = list_membs
        self.exarray = self.create_exarray()

    def create_exarray(self):
        num_blocks = Schedule.calculate_num_blocks(self.start, self.end)
        return [[[True for z in range(self.num_members)] for x in range(num_blocks)] for y in range(7)]

    def visualize(self):
        days, times = Schedule.prep_visualize(self)
        print("Members: "+ self.list_membs[:-2])

        # HEADER:
        print("##### ", end="")
        # print(days)
        # print(times)
        for d in days:
            num_spaces = len(self.exarray[0][1]) - 1
            left_half = int(num_spaces / 2)
            right_half = num_spaces - left_half

            print("(", end="")
            print(''.join([" " for x in range(left_half)]), end=d)
            print(''.join([" " for x in range(right_half)]), end=")")
        print(" #####")

        # SCHEDULE:
        for i in range(len(times)):                     # i: 0-26 (9:00) = m: 0-26 ([T,T,T])
            print(times[i], end=" ")
            for d in range(len(self.exarray)):          # d: 0-6 (sun)
                array = self.exarray[d][i]
                print("[", end="")
                for memb_avail in array:
                    print("-", end="") if memb_avail is True else print("*", end="")
                print("]", end="")
            print(" ", end=times[i]+"\n")

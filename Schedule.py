import datetime

class Schedule:
    def __init__(self, start, end, name, other):        # Constructor
        self.start = start                              # Schedule start time (ex. 9:00)
        self.end = end                                  # Schedule end time (ex. 22:00)
        self.name = name                                # Schedule name (ex. member name, final schedule, etc)
        self.other = other                              # Schedule exceptions/"other"
        self.array = self.create_array()                # Schedule array (2D array of days of week (7) x half hour blocks)

    def create_array(self):
        # Converts start/end time to datettime if entered as string
        if isinstance(self.start, str):
            self.start = datetime.datetime.strptime(self.start, '%H:%M')
            self.start = datetime.time(self.start.hour, self.start.minute)
        if isinstance(self.end, str):
            self.end = datetime.datetime.strptime(self.end, '%H:%M')
            self.end = datetime.time(self.end.hour, self.end.minute)

        # Generate array from number of (30 minute) blocks
        num_blocks = self.calculate_num_blocks(self.start, self.end)

        return [[True for x in range(num_blocks)] for y in range(7)]

    # watch this first https://www.youtube.com/watch?v=rq8cL2XMM5M
    @staticmethod
    def calculate_num_blocks(start, end):
        # Determining size of array: get difference
        total_hrs = end.hour - start.hour
        total_mins = end.minute - start.minute

        # Determining size of array: in 30 min blocks (rounded)
        num_half_hr = int(total_mins/30)
        num_blocks = 2 * total_hrs + num_half_hr

        return num_blocks

    def visualize(self):
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

        # Printing visualization of schedule
        # HEADER:
        print("#####", end=" ")
        for d in days: print("(" + d + ") ", end="")
        print("#####")
        # SCHEDULE:
        for t in range(len(times)):
            print(times[t], end="")
            for d in range(7):
                slot = self.array[d][t]
                if slot is True: slot = "   "
                elif slot is False: slot = " x "
                print(slot, end=" ")
            print(times[t])
        print()

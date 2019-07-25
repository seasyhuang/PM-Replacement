import datetime

# d = datetime.date(2016, 07, 24)       adding the 0 is wrong
# d = datetime.date(2016, 7, 24)
d = datetime.date.today()
print(d)

print(d.weekday())      # monday is 0, sunday 6
print(d.isoweekday())   # monday is 1, sunday 7

# adding 7 days to today using a timedelta
tdelta = datetime.timedelta(days=7)
print(d + tdelta)

# if we subtract a date from a date, we get a timedelta as a result
bday = datetime.date(2019, 9, 24)
until_bday = bday - d
print(until_bday)       # how much time until until_bday
print(until_bday.days)  # how many days until bday
print(until_bday.total_seconds())  # a method that converts days to seconds

# time - naive
# t = datetime.time(hrs, mins, sec, microseconds)
t = datetime.time(6, 30, 12)
print(t)
print(t.hour)
print(t.minute)

# datetime
# dt = datetime.datetime(year, month, day, hr, min, sec, milisec)
dt = datetime.datetime(2019, 7, 22, 12, 30, 45, 10000)
print(dt)
print(dt.date())
print(dt.time())

# adding and subtracting tdelta durations
tdelta = datetime.timedelta(days=7)
print("Adding 7 days: ", end="")
print(dt + tdelta)

print("Adding 7 hours: ", end="")
print(dt + datetime.timedelta(hours=7))

# now and today
dt_today = datetime.datetime.today()
dt_now = datetime.datetime.now()
dt_utcnow = datetime.datetime.utcnow()

print(dt_today)
print(dt_now)
print(dt_utcnow)

# pip install pytz
# for handling timezones
import pytz

# a timezone aware datetime using utc
dt2 = datetime.datetime(2016, 7, 27, 12, 30, 45, tzinfo=pytz.UTC)    # 12:30:45pm
print(dt2)
# >> 2016-07-27 12:30:45+00:00

dt_utcnow = datetime.datetime.utcnow().replace(tzinfo=pytz.UTC)

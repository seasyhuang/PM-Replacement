### Individual day tests ### 
# Case 1: Schedule more free than member
# Sched: 7am - 11pm
# Member: 12pm - 10pm
# Expected Results: 12pm - 10pm (same as member avails)
schedule[i] = [datetime.strptime("7:00am", "%I:%M%p").time(), datetime.strptime("11:00pm", "%I:%M%p").time()]
mod_member_avail[i] = [datetime.strptime("12:00pm", "%I:%M%p").time(), datetime.strptime("10:00pm", "%I:%M%p").time()]

# Case 2: Member more free than schedule
# Sched: 1pm - 2pm
# Member: 12pm - 11pm
# Expected Results: 1pm - 2pm (same as schedule)
schedule[i] = [datetime.strptime("1:00pm", "%I:%M%p").time(), datetime.strptime("2:00pm", "%I:%M%p").time()]
mod_member_avail[i] = [datetime.strptime("12:00pm", "%I:%M%p").time(), datetime.strptime("11:00pm", "%I:%M%p").time()]

# Case 3: Schedule start earlier and end earlier, overlap
# Sched: 10am - 2pm
# Member: 12pm - 4pm
# Expected Results: 12pm - 2pm
schedule[i] = [datetime.strptime("10:00am", "%I:%M%p").time(), datetime.strptime("2:00pm", "%I:%M%p").time()]
mod_member_avail[i] = [d'tetime.strptime("12:00pm", "%I:%M%p").time(), datetime.strptime("4:00pm", "%I:%M%p").time()]

# Case 4: Schedule start later and end later, overlap
# Sched: 3pm - 9pm
# Member: 10am - 5pm
# Expected Results: 3pm - 5pm
schedule[i] = [datetime.strptime("3:00pm", "%I:%M%p").time(), datetime.strptime("9:00pm", "%I:%M%p").time()]
mod_member_avail[i] = [datetime.strptime("10:00am", "%I:%M%p").time(), datetime.strptime("5:00pm", "%I:%M%p").time()]

# Case 5: No overlap
# Sched: 11am - 3pm
# Member: 5pm - 9pm
# Expected Results: None
schedule[i] = [datetime.strptime("11:00am", "%I:%M%p").time(), datetime.strptime("3:00pm", "%I:%M%p").time()]
mod_member_avail[i] = [datetime.strptime("5:00pm", "%I:%M%p").time(), datetime.strptime("9:00pm", "%I:%M%p").time()]

# Swapped
schedule[i] = [datetime.strptime("5:00pm", "%I:%M%p").time(), datetime.strptime("9:00pm", "%I:%M%p").time()]
mod_member_avail[i] = [datetime.strptime("11:00am", "%I:%M%p").time(), datetime.strptime("3:00pm", "%I:%M%p").time()]

import datetime
time_start = datetime.datetime(2024,4,18,19,0,0)
time_end = datetime.datetime(2024,4,18,20,0,0)
current_time = datetime.datetime.now()
print((time_start <= current_time <= time_end))
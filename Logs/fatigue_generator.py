import random
import datetime

start_date = datetime.date(2023, 3, 1)
end_date = datetime.date(2023, 5, 1)
work_start_time = datetime.time(9, 0, 0)
work_end_time = datetime.time(16, 0, 0)
fatigue_probability = [0.2, 0.3, 0.5, 0.7, 0.9, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.2]

with open('fatigue_log.txt', 'w') as file:
    num_rows = 0
    while num_rows < 500:
        date = start_date + datetime.timedelta(days=random.randint(0, (end_date - start_date).days))
        time = datetime.time(hour=random.randint(work_start_time.hour, work_end_time.hour), minute=random.randint(0, 59))
        datetime_str = datetime.datetime.combine(date, time).strftime('%Y-%m-%d %H:%M:%S')
        fatigue_probability_index = (time.hour - work_start_time.hour) % len(fatigue_probability)
        if random.random() < fatigue_probability[fatigue_probability_index]:
            file.write(f"{datetime_str}, fatigue\n")
            num_rows += 1

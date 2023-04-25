import random
import datetime

start_date = datetime.date(2023, 3, 1)
end_date = datetime.date(2023, 5, 1)
delta = datetime.timedelta(days=1)

with open("posture_log1.txt", "w") as f:
    while start_date <= end_date:
        date_str = start_date.strftime("%Y-%m-%d")
        for hour in range(9, 17):
            for minute in range(0, 60, 15):
                timestamp_str = f"{date_str} {hour:02d}:{minute:02d}:00"
                time = datetime.datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
                if time.weekday() < 5:  # Only log on weekdays
                    prob = 0.05  # Probability of bad posture is least in the morning
                    if hour >= 12:
                        prob += (hour - 11) * 0.01  # Increase probability for each hour past 11am
                    if hour >= 16:
                        prob += (hour - 15) * 0.02  # Increase probability more for each hour past 4pm
                    if random.random() < prob:  # Log bad posture with the calculated probability
                        f.write(f"{timestamp_str}, bad posture\n")
        start_date += delta

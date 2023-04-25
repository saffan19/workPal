import calendar
import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
import pandas as pd
import matplotlib.pyplot as plt
import os


import tkinter as tk
from tkcalendar import DateEntry
import pandas as pd
from tkinter import ttk


import tkinter as tk
from tkcalendar import DateEntry
import pandas as pd
from tkinter import ttk


class DashboardApp:
    def __init__(self, master):
        
        self.master = master
        self.master.geometry("600x400")
        self.master.title("Posture Analysis")


######################
        # Get the screen width and height
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()

        # Calculate the x and y coordinates for the window to be centered
        x = int((screen_width / 2) - (600 / 2))
        y = int((screen_height / 2) - (400 / 2))

        # Set the window to be centered and show it
        self.master.geometry(f"600x400+{x}+{y-100}")
        self.master.update()


######################


        # create a frame for the date picker, buttons, and title
        frame = tk.Frame(self.master, bg="black")
        frame.pack(fill="both", expand=True)

        # create title
        title_label = tk.Label(frame, text="Posture Stats", font=("Helvetica", 16), bg="black", fg="white")
        title_label.pack(fill="x", pady=(10, 0))

        # create date picker
        cal = DateEntry(frame, width=12, background='darkblue',
                        foreground='white', borderwidth=2)
        cal.pack(padx=10, pady=10)

        # create day-wise report button
        daywise_report_btn = ttk.Button(
            frame, text="Day-wise Report", width=20, 
            command=lambda: self.generate_daywise_report(cal.get_date()), 
            style="Daywise.TButton"
        )
        daywise_report_btn.pack(padx=10, pady=5)

        # create weekly report button
        weekly_report_btn = ttk.Button(
            frame, text="Weekly Report", width=20, 
            command=lambda: self.generate_weekly_report(cal.get_date() - pd.DateOffset(days=7)), 
            style="Weekly.TButton"
        )
        weekly_report_btn.pack(padx=10, pady=5)

        # create weekly report button
        monthly_report_btn = ttk.Button(
            frame, text="Monthly Report", width=20, 
            command=lambda: self.generate_monthly_report(cal.get_date()), 
            style="Monthly.TButton"
        )
        monthly_report_btn.pack(padx=10, pady=5)

        # define styles for the buttons
        s = ttk.Style()
        s.configure("Daywise.TButton", foreground="teal", bg="teal", font=("Helvetica", 12), 
                    borderwidth=0, bordercolor="teal", borderradius=5, transition="0.3s")
        s.map("Daywise.TButton", background=[("active", "teal")])
        s.configure("Weekly.TButton", foreground="black", background="pink", font=("Helvetica", 12), 
                    borderwidth=0, bordercolor="pink", borderradius=5, transition="0.3s")
        s.map("Weekly.TButton", background=[("active", "pink")])
        s.configure("Monthly.TButton", foreground="black", background="pink", font=("Helvetica", 12), 
                    borderwidth=0, bordercolor="pink", borderradius=5, transition="0.3s")
        s.map("Monthly.TButton", background=[("active", "pink")])

    def generate_daywise_report(self, day):
        df = pd.read_csv('./Logs/posture_log.txt', names=['timestamp', 'status'], delimiter=', ')
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df[df['timestamp'].dt.date == day]  # filter by date
        print(df)
        print(day)
        df = df[df['status'] == 'bad posture']
        freq_by_hour = df.groupby(df['timestamp'].dt.hour).count()
        print('---')
        print(freq_by_hour)
        print('---')
        plt.figure(figsize=(10, 6))
        plt.plot(freq_by_hour.index, freq_by_hour['status'])
        plt.title(f"Frequency of Bad Posture for {day.strftime('%Y-%m-%d')}")
        plt.xlabel('Time (hour)')
        plt.ylabel('Frequency')
        plt.xticks(range(min(freq_by_hour.index), max(freq_by_hour.index)+1)) # modify x-axis range
        plt.grid(True)
        plt.autoscale()
        plt.show()

    def generate_weekly_report(self, start_date):
        end_date = start_date + pd.DateOffset(days=7)
        df = pd.read_csv('./Logs/posture_log.txt', names=['timestamp', 'status'], delimiter=', ')
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df[df['status'] == 'bad posture']
        start_ts = pd.Timestamp(start_date)
        end_ts = pd.Timestamp(end_date)
        df = df[df['timestamp'].between(start_ts, end_ts)]
        freq_by_day = df.groupby(df['timestamp'].dt.date).count()

        plt.figure(figsize=(10, 6))
        plt.plot(freq_by_day.index, freq_by_day['status'])
        plt.title(f"Weekly Report of Bad Posture ({start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')})")
        plt.xlabel('Date')
        plt.ylabel('Frequency')
        plt.grid(True)
        plt.autoscale()
        plt.show()

    def generate_monthly_report(self, date):
        start_date = date.replace(day=1)
        end_date = start_date + pd.offsets.MonthEnd(1)
        df = pd.read_csv('./Logs/posture_log.txt', names=['timestamp', 'status'], delimiter=', ')
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df[df['status'] == 'bad posture']
        start_ts = pd.Timestamp(start_date)
        end_ts = pd.Timestamp(end_date)
        df = df[df['timestamp'].between(start_ts, end_ts)]
        freq_by_day = df.groupby(df['timestamp'].dt.day).count()

        plt.figure(figsize=(10, 6))
        plt.plot(freq_by_day.index, freq_by_day['status'])
        plt.title(f"Monthly Report of Bad Posture ({start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')})")
        plt.xlabel('Day of the Month')
        plt.ylabel('Frequency')
        plt.xticks(freq_by_day.index)
        plt.grid(True)
        plt.autoscale()
        plt.show()



if __name__ == "__main__":
    root = tk.Tk()
    DashboardApp(root)
    root.mainloop()

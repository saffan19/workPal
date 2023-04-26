import calendar
import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np
from PIL import Image, ImageTk
from tkinter import Label
from tkinter import *
from tkinter import PhotoImage
import PIL.Image




class DashboardApp:
    def __init__(self, master):
        self.master = master
        self.master.geometry("600x400")
        self.master.title("Analysis")
        self.master.resizable(False, False)
        
# ######################Background Code start##################
        # fp = open("./Resources/bg1.jpg","rb")
        # bg_image = PIL.Image.open(fp)
        # bg_image = bg_image.resize((600, 400), PIL.Image.ANTIALIAS)
        # bg_photo = ImageTk.PhotoImage(bg_image)

        # bg_label = tk.Label(self.master, image=bg_photo)
        # bg_label.place(x=0, y=0)
        # bg_label.image = bg_photo

# ######################backgorund Code end####################


        # Get the screen width and height
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()

        # Calculate the x and y coordinates for the window to be centered
        x = int((screen_width / 2) - (600 / 2))
        y = int((screen_height / 2) - (400 / 2))

        # Set the window to be centered and show it
        self.master.geometry(f"600x400+{x}+{y-100}")
        self.master.update()



        # Load the background image
        bg_image = PIL.Image.open("./Resources/bg1.jpg")
        bg_image = bg_image.resize((600, 400))
        self.bg_photo = ImageTk.PhotoImage(bg_image)

        # Create the frame and set its background image
        frame = Frame(root, bg="black", width=600, height=400,highlightthickness=0)
        self.bg_label = Label(frame, image=self.bg_photo)
        self.bg_label.place(x=0, y=0)
        frame.pack(fill="both", expand=True)




        # create a frame for the date picker, buttons, and title
        # frame = Frame(self.master, bg="black")
        # frame.pack(fill="both", expand=True)

        # # create a frame for the date picker, buttons, and title
        # frame = tk.Frame(self.master, bg="black")
        # frame.pack(fill="both", expand=True)




        # create title
        title_label = tk.Label(frame, text="WorkPal Stats", font=("Helvetica", 16), bg="grey", fg="white")
        title_label.pack(pady=(10, 0))

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



        # worst posture hour button
        worst_pos_btn = ttk.Button(
            frame, text="Worst Hours", width=20, 
            command=lambda: self.generate_worst_posture_hour(cal.get_date() - pd.DateOffset(days=7)), 
            style="Worst.TButton"
        )
        worst_pos_btn.pack(padx=10, pady=5)


    def generate_daywise_report(self, day):
        df_posture = pd.read_csv('./Logs/posture_log.txt', names=['timestamp', 'status'], delimiter=', ')
        df_posture['timestamp'] = pd.to_datetime(df_posture['timestamp'])
        df_posture = df_posture[df_posture['timestamp'].dt.date == day]  # filter by date
        
        df_fatigue = pd.read_csv('./Logs/fatigue_log.txt', names=['timestamp', 'status'], delimiter=', ')
        df_fatigue['timestamp'] = pd.to_datetime(df_fatigue['timestamp'])
        df_fatigue = df_fatigue[df_fatigue['timestamp'].dt.date == day]  # filter by date
        
        freq_posture_by_hour = df_posture[df_posture['status'] == 'bad posture'].groupby(df_posture['timestamp'].dt.hour).count()
        freq_fatigue_by_hour = df_fatigue[df_fatigue['status'] == 'fatigue'].groupby(df_fatigue['timestamp'].dt.hour).count()
        
        plt.figure(figsize=(10, 6))
        plt.plot(freq_posture_by_hour.index, freq_posture_by_hour['status'], label='Bad Posture')
        plt.plot(freq_fatigue_by_hour.index, freq_fatigue_by_hour['status'], label='Fatigue')
        
        plt.title(f"Frequency of Bad Posture and Fatigue for {day.strftime('%Y-%m-%d')}")
        plt.xlabel('Time (hour)')
        plt.ylabel('Frequency')
        plt.xticks(range(min(freq_posture_by_hour.index), max(freq_posture_by_hour.index)+1)) # modify x-axis range
        plt.grid(True)
        plt.legend()
        plt.autoscale()
        plt.show()

    # def generate_weekly_report1(self, start_date):
    #     end_date = start_date + pd.DateOffset(days=7)
    #     df = pd.read_csv('./Logs/posture_log.txt', names=['timestamp', 'status'], delimiter=', ')
    #     df['timestamp'] = pd.to_datetime(df['timestamp'])
    #     df = df[df['status'] == 'bad posture']
    #     start_ts = pd.Timestamp(start_date)
    #     end_ts = pd.Timestamp(end_date)
    #     df = df[df['timestamp'].between(start_ts, end_ts)]
    #     freq_by_day = df.groupby(df['timestamp'].dt.date).count()

    #     plt.figure(figsize=(10, 6))
    #     plt.plot(freq_by_day.index, freq_by_day['status'])
    #     plt.title(f"Weekly Report of Bad Posture ({start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')})")
    #     plt.xlabel('Date')
    #     plt.ylabel('Frequency')
    #     plt.grid(True)
    #     plt.autoscale()
    #     plt.show()
    def generate_weekly_report(self, start_date):
        end_date = start_date + pd.DateOffset(days=7)
        
        df_posture = pd.read_csv('./Logs/posture_log.txt', names=['timestamp', 'status'], delimiter=', ')
        df_posture['timestamp'] = pd.to_datetime(df_posture['timestamp'])
        df_posture = df_posture[df_posture['status'] == 'bad posture']
        posture_start_ts = pd.Timestamp(start_date)
        posture_end_ts = pd.Timestamp(end_date)
        df_posture = df_posture[df_posture['timestamp'].between(posture_start_ts, posture_end_ts)]
        
        df_fatigue = pd.read_csv('./Logs/fatigue_log.txt', names=['timestamp', 'status'], delimiter=', ')
        df_fatigue['timestamp'] = pd.to_datetime(df_fatigue['timestamp'])
        df_fatigue = df_fatigue[df_fatigue['status'] == 'fatigue']
        fatigue_start_ts = pd.Timestamp(start_date)
        fatigue_end_ts = pd.Timestamp(end_date)
        df_fatigue = df_fatigue[df_fatigue['timestamp'].between(fatigue_start_ts, fatigue_end_ts)]
        
        freq_posture_by_day = df_posture.groupby(df_posture['timestamp'].dt.date).count()
        freq_fatigue_by_day = df_fatigue.groupby(df_fatigue['timestamp'].dt.date).count()

        plt.figure(figsize=(10, 6))
        plt.plot(freq_posture_by_day.index, freq_posture_by_day['status'], label='Bad Posture')
        plt.plot(freq_fatigue_by_day.index, freq_fatigue_by_day['status'], label='Fatigue')

        plt.title(f"Weekly Report of Bad Posture and Fatigue ({start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')})")
        plt.xlabel('Date')
        plt.ylabel('Frequency')
        plt.grid(True)
        plt.legend()
        plt.autoscale()
        plt.show()

    # def generate_monthly_report1(self, date):
    #     start_date = date.replace(day=1)
    #     end_date = start_date + pd.offsets.MonthEnd(1)
    #     df = pd.read_csv('./Logs/posture_log.txt', names=['timestamp', 'status'], delimiter=', ')
    #     df['timestamp'] = pd.to_datetime(df['timestamp'])
    #     df = df[df['status'] == 'bad posture']
    #     start_ts = pd.Timestamp(start_date)
    #     end_ts = pd.Timestamp(end_date)
    #     df = df[df['timestamp'].between(start_ts, end_ts)]
    #     freq_by_day = df.groupby(df['timestamp'].dt.day).count()

    #     plt.figure(figsize=(10, 6))
    #     plt.plot(freq_by_day.index, freq_by_day['status'])
    #     plt.title(f"Monthly Report of Bad Posture ({start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')})")
    #     plt.xlabel('Day of the Month')
    #     plt.ylabel('Frequency')
    #     plt.xticks(freq_by_day.index)
    #     plt.grid(True)
    #     plt.autoscale()
    #     plt.show()
    def generate_monthly_report(self, date):
        start_date = date.replace(day=1)
        end_date = start_date + pd.offsets.MonthEnd(1)
        
        # Read bad posture log file
        df_posture = pd.read_csv('./Logs/posture_log.txt', names=['timestamp', 'status'], delimiter=', ')
        df_posture['timestamp'] = pd.to_datetime(df_posture['timestamp'])
        df_posture = df_posture[df_posture['status'] == 'bad posture']
        start_ts = pd.Timestamp(start_date)
        end_ts = pd.Timestamp(end_date)
        df_posture = df_posture[df_posture['timestamp'].between(start_ts, end_ts)]
        freq_posture_by_day = df_posture.groupby(df_posture['timestamp'].dt.day).count()
        
        # Read fatigue log file
        df_fatigue = pd.read_csv('./Logs/fatigue_log.txt', names=['timestamp', 'status'], delimiter=', ')
        df_fatigue['timestamp'] = pd.to_datetime(df_fatigue['timestamp'])
        df_fatigue = df_fatigue[df_fatigue['status'] == 'fatigue']
        start_ts = pd.Timestamp(start_date)
        end_ts = pd.Timestamp(end_date)
        df_fatigue = df_fatigue[df_fatigue['timestamp'].between(start_ts, end_ts)]
        freq_fatigue_by_day = df_fatigue.groupby(df_fatigue['timestamp'].dt.day).count()

        plt.figure(figsize=(10, 6))
        plt.plot(freq_posture_by_day.index, freq_posture_by_day['status'], label='Bad Posture')
        plt.plot(freq_fatigue_by_day.index, freq_fatigue_by_day['status'], label='Fatigue')
        plt.title(f"Monthly Report of Bad Posture and Fatigue ({start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')})")
        plt.xlabel('Day of the Month')
        plt.ylabel('Frequency')
        plt.xticks(freq_posture_by_day.index)
        plt.grid(True)
        plt.legend()
        plt.autoscale()
        plt.show()




    def generate_worst_posture_hour1(self,start_date):
        end_date = start_date + pd.DateOffset(days=7)
        df = pd.read_csv('./Logs/posture_log.txt', names=['timestamp', 'status'], delimiter=', ')
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df[df['status'] == 'bad posture']
        start_ts = pd.Timestamp(start_date)
        end_ts = pd.Timestamp(end_date)
        df = df[df['timestamp'].between(start_ts, end_ts)]
        freq_by_day = df.groupby(df['timestamp'].dt.date).count()

        df['hour'] = df['timestamp'].dt.hour
        freq_by_hour = df.groupby('hour').count()

        plt.figure(figsize=(10, 6))
        plt.plot(freq_by_hour.index, freq_by_hour['status'])
        plt.title(f"Worst Posture Hours ({start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')})")
        plt.xlabel('Hour')
        plt.ylabel('Frequency')
        plt.grid(True)
        plt.autoscale()
        plt.show()
    def generate_worst_posture_hour(self, start_date):
        end_date = start_date + pd.DateOffset(days=7)
        posture_df = pd.read_csv('./Logs/posture_log.txt', names=['timestamp', 'status'], delimiter=', ')
        fatigue_df = pd.read_csv('./Logs/fatigue_log.txt', names=['timestamp', 'status'], delimiter=', ')
        
        posture_df['timestamp'] = pd.to_datetime(posture_df['timestamp'])
        posture_df = posture_df[posture_df['status'] == 'bad posture']
        start_ts = pd.Timestamp(start_date)
        end_ts = pd.Timestamp(end_date)
        posture_df = posture_df[posture_df['timestamp'].between(start_ts, end_ts)]
        
        fatigue_df['timestamp'] = pd.to_datetime(fatigue_df['timestamp'])
        fatigue_df = fatigue_df[fatigue_df['status'] == 'fatigue']
        fatigue_df = fatigue_df[fatigue_df['timestamp'].between(start_ts, end_ts)]
        
        posture_freq_by_hour = posture_df.groupby(posture_df['timestamp'].dt.hour).count()
        fatigue_freq_by_hour = fatigue_df.groupby(fatigue_df['timestamp'].dt.hour).count()

        plt.figure(figsize=(10, 6))
        plt.plot(posture_freq_by_hour.index, posture_freq_by_hour['status'], label='Bad Posture')
        plt.plot(fatigue_freq_by_hour.index, fatigue_freq_by_hour['status'], label='Fatigue')
        plt.legend()
        plt.title(f"Worst Posture Hours ({start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')})")
        plt.xlabel('Hour')
        plt.ylabel('Frequency')
        plt.grid(True)
        plt.autoscale()
        plt.show()


if __name__ == "__main__":
    root = tk.Tk()
    DashboardApp(root)
    root.mainloop()

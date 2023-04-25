import tkinter as tk
import psutil
import subprocess
class App:
    def __init__(self, master):
        
        self.master = master
        self.master.geometry("600x400")
        self.master.title("WorkPal")
###################################################
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()

        # Calculate the x and y coordinates for the window to be centered
        x = int((screen_width / 2) - (600 / 2))
        y = int((screen_height / 2) - (400 / 2))

        # Set the window to be centered and show it
        self.master.geometry(f"600x400+{x}+{y-100}")
        self.master.update()
###################################################
        #To toggle view buttons on and off
        self.viewFace=False
        self.viewPose=False


        # Create a frame for the left side of the app
        left_frame = tk.Frame(self.master, bg="black", width=300, height=400)
        left_frame.pack(side="left", fill="both", expand=True)

        # Add the WorkPal logo to the left frame
        logo_img = tk.PhotoImage(file="./Resources/logo.png")
        logo = tk.Label(left_frame, image=logo_img, bg="black")
        logo.image = logo_img # to prevent image from being garbage collected
        logo.place(relx=0.5, rely=0.3, anchor="center")

        # Add the WorkPal title to the left frame
        title = tk.Label(left_frame, text="WorkPal", bg="black", fg="white", font=("Helvetica", 20, "bold"), highlightthickness=0)
        title.place(relx=0.5, rely=0.6, anchor="center")

        # Create a frame for the right side of the app
        right_frame = tk.Frame(self.master, bg="#f2f2f2", width=300, height=400, bd=0)
        right_frame.pack(side="right", fill="both", expand=True)

        #checkbox values variables:
        self.fatigue_analysis_var = tk.BooleanVar()
        self.posture_analysis_var = tk.BooleanVar()

        # Create checkboxes for posture analysis
        posture_analysis_cb = tk.Checkbutton(right_frame, text="Enable posture analysis", variable=self.posture_analysis_var, bg="#f2f2f2", font=("Helvetica", 12), command=self.run_posture_analysis)
        posture_analysis_cb.place(relx=0.5, rely=0.2, anchor="center")

        # Create a button to view pose
        self.view_pose_btn = tk.Button(right_frame, text="View Pose", bg="#cccccc", fg="black", font=("Helvetica", 12), bd=0, borderwidth=0, highlightthickness=0, padx=10, pady=5, state="disabled",command=self.view_pose)
        self.view_pose_btn.place(relx=0.5, rely=0.3, anchor="center")


        # Create checkboxes for fatigue analysis
        fatigue_analysis_cb = tk.Checkbutton(right_frame, text="Enable fatigue analysis", variable=self.fatigue_analysis_var, bg="#f2f2f2", font=("Helvetica", 12),command=self.run_fatigue_analysis)
        fatigue_analysis_cb.place(relx=0.5, rely=0.5, anchor="center")

        # Create a button to view face
        self.view_face_btn = tk.Button(right_frame, text="View Face", bg="#cccccc", fg="black", font=("Helvetica", 12), bd=0, borderwidth=0, highlightthickness=0, padx=10, pady=5, state="disabled",command=self.view_face)
        self.view_face_btn.place(relx=0.5, rely=0.6, anchor="center")




        # Create a button to generate report
        generate_report_btn = tk.Button(right_frame, text="View Report", bg="teal", fg="white", font=("Helvetica", 14), bd=0, borderwidth=0, highlightthickness=0, padx=20, pady=10,command=self.generate_report)
        generate_report_btn.place(relx=0.5, rely=0.8, anchor="center")

        # Store the process running the posture analysis script
        self.posture_analysis_process = None

        #Store the process running the fatigue analysis script
        self.fatigue_analysis_process= None


        #Store the process running the posture view
        self.view_pose_process= None
        #S

        # Enable or disable the view pose button based on the state of the posture analysis checkbox
        self.posture_analysis_var.trace("w", self.update_view_pose_btn_state)

        self.fatigue_analysis_var.trace("w", self.update_view_face_btn_state)


        # #FOR SHOWING CPU USAGE#####################################################
        self.cpu_percent = psutil.cpu_percent()

        self.cpu_usage_label = tk.Label(master, text="CPU Usage:"+str(self.cpu_percent) + " %")
        self.cpu_usage_label.pack()
        self.cpu_usage_label.place(relx=0.90, rely=0.95, anchor="center")
        self.update_cpu_usage_label()

        
    def update_cpu_usage_label(self):
        # Get the current CPU usage
        self.cpu_percent = psutil.cpu_percent()
        self.cpu_usage_label.config(text="CPU Usage:"+str(self.cpu_percent) + " %")
        root.after(1000, self.update_cpu_usage_label)
        #self.master.after(1000, self.update_cpu_usage_label)


        


        # ################################################################################

    def update_view_pose_btn_state(self, *args):
        if self.posture_analysis_var.get():
            self.view_pose_btn["state"] = "normal"
        else:
            self.view_pose_btn["state"] = "disabled"
    def update_view_face_btn_state(self, *args):
        if self.fatigue_analysis_var.get():
            self.view_face_btn["state"] = "normal"
        else:
            self.view_face_btn["state"] = "disabled"
    def run_posture_analysis(self):
        if self.posture_analysis_var.get():
            # If the checkbox is checked, start the posture analysis script
            self.posture_analysis_process = subprocess.Popen(["python", "./ModelExecutables/poseAnalysis.py"])############
        else:
            # If the checkbox is unchecked, stop the posture analysis script
            if self.posture_analysis_process is not None:
                self.posture_analysis_process.terminate()
            if self.viewPose is not None:
                self.view_pose_process.terminate()
    
    def view_pose(self):
        self.viewPose=~self.viewPose
        print("POSE IS ",self.viewPose)
        if self.viewPose:
            self.posture_analysis_process.terminate()
            self.view_pose_process=subprocess.Popen(["python", "./ModelExecutables/poseAnalysis.py","1"])############

        else:
            if self.viewPose is not None:
                self.view_pose_process.terminate()
            self.posture_analysis_process = subprocess.Popen(["python", "./ModelExecutables/poseAnalysis.py"])

    def view_face(self):
        self.viewFace=~self.viewFace
        print("Face IS ",self.viewFace)


    def generate_report(self):
        subprocess.Popen(["python", "./App/dashboardApp.py"])


        
    def run_fatigue_analysis(self):
        if self.fatigue_analysis_var.get():
            self.fatigue_analysis_process=subprocess.Popen(["python","./ModelExecutables/fatigueAnalysis.py"])###############
        else:
            # If the checkbox is unchecked, stop the posture analysis script
            if self.fatigue_analysis_process is not None:
                self.fatigue_analysis_process.terminate()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()

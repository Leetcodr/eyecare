#-----------------------------------------------------------------------------
#								Imports
from time import time, sleep, gmtime, strftime, localtime
from tkinter import Tk, Canvas, Label, Button, LabelFrame
from tkinter.ttk import Button as ttkButton
from playsound import playsound
import win32api
import sv_ttk
import plyer

import sys
import os

# https://stackoverflow.com/questions/31836104/pyinstaller-and-onefile-how-to-include-an-image-in-the-exe-file
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    path = os.path.join(base_path, relative_path)
    return path

plyer_path = resource_path("plyer")
sys.path.append(plyer_path)

sound_path = resource_path(r'assets\sound.wav')

#-----------------------------------------------------------------------------
#								MainWindow
class MainWindow:
    def __init__(self):
        self.window = Tk()
        self.window.title("Eyecare")
        self.window.geometry("400x270")
        self.window.resizable(False, False)
        self.window.configure(bg= "#F7F7F7")

        self.light = "#F7F7F7"
        self.dark = "#212121"
        self.light_text = "#3A3A3A"
        self.dark_text = "#CCCCCC"

        self.current_theme = "light"    
        self.about_window = None        
        self.start_time = 0
        self.enable_timer = False
        self.input_info = None

        self.place_items()
        self.theme()    
        self.window.mainloop()
    

    def place_items(self):
        self.canvas = Canvas(self.window, bg = self.light, width = 400, height = 270)
        self.canvas.place(x = 0, y = 0)

        self.time_label = Label(self.window,font=("Inter",31),text="00:20:00")
        self.time_label.place(relx=0.5, rely=0.5, x=0, y=-35, anchor="center")

        self.status_label = Label(self.window,font=("Calibri",13),text="Press Start")
        self.status_label.place(relx=0.5, rely=0.5, x=0, y=4, anchor="center")

        self.theme_button = Button(text="Change Theme", command=self.theme, borderwidth=0, foreground=self.light_text)
        self.theme_button.place(x=15.0, y=5.0, width=86.0, height=30.0)

        self.about_button = Button(text="About", command=self.open_about, borderwidth=0, foreground=self.light_text)
        self.about_button.place(x=345.0, y=5.0, width=40.0, height=30.0)

        self.start_stop_button = ttkButton(text="Start", command=self.control, style="Accent.TButton")
        self.start_stop_button.place(x=210.0, y=190.0, width=130.0, height=40.0)

        self.test_button = ttkButton(text="Test", command=self.alert)
        self.test_button.place(x=65.0, y=190.0, width=130.0, height=40.0)


    def theme(self):     
        if self.current_theme == "light":   # if current theme is light, set to dark
            self.set_theme(self.dark, self.dark_text)
            try:
                self.about_window.set_theme(self.dark, self.light)
            except:
                pass

            self.current_theme = "dark"
        else:                               # if current theme is dark, set to light
            self.set_theme(self.light, self.light_text)
            try:
                self.about_window.set_theme(self.light, self.dark)
            except:
                pass

            self.current_theme = "light"


    def set_theme(self,theme_color, text_color):
            self.canvas.config(bg= theme_color)
            self.time_label.config(bg= theme_color)
            self.status_label.config(background= theme_color)
            self.theme_button.config(background= theme_color, foreground= text_color)
            self.about_button.config(background= theme_color, foreground= text_color)
            (sv_ttk.set_theme("light")) if theme_color == self.light else (sv_ttk.set_theme("dark"))


    def alert(self, status_label_text= None, title= "test", message= "test"):
        self.status_label.config(text=status_label_text)
        plyer.notification.notify(title= title, message= message)
        playsound(sound_path)


    def update(self, status_label_text, start_stop_button_text, time_label_text= None):
        self.status_label.config(text= status_label_text)
        self.start_stop_button.config(text= start_stop_button_text)
        if time_label_text:
            self.time_label.config(text= time_label_text)


    def log(self, text= "", end= "\n"):
        print(strftime("%I:%M:%S %p", localtime()), text, end= end)


    def control(self):
        if not self.start_time:
            self.update("Started", "Stop")
            self.log(text="\t\t-Started")
            self.enable_timer = True
            self.get_time()
        else:
            self.update("Stopped", "Start", "00:20:00")
            self.log(text="\t\t-Stopped")
            self.enable_timer = False  
            self.start_time = False

        
    def get_time(self):
        if not self.enable_timer :
            return

        now = time()
        begin_outside = 1200     #1200 is no. of seconds in 20 minutes
        end_outside = 1222     #1222 is 1200 sec + 20 sec break + 2 sec reaction time
        elapsed_time = int(now - self.start_time)

        if not self.start_time:
            self.start_time = now

        if elapsed_time < begin_outside:
            self.time_label.config(text= strftime("%H:%M:%S", gmtime(self.start_time+begin_outside-now)))
            if elapsed_time == (begin_outside - 120):   # get user info 2 minutes before 
                self.input_info = win32api.GetLastInputInfo()

        elif elapsed_time == begin_outside:
            if self.input_info == win32api.GetLastInputInfo():  # if user is inactive
                self.control()
            sleep(0.5)                 # wait time to avoid alerts twice
            self.log(end=" - ")
            self.alert(status_label_text="Look Outside", title="Look Outside!", message="eyecare")

        elif elapsed_time > begin_outside and elapsed_time < end_outside:
            self.time_label.config(text="00:20:00")

        elif elapsed_time == end_outside:
            self.start_time = now    # reset time
            self.log(text="\t-Break")
            if self.input_info != (win32api.GetLastInputInfo()):    # if user is active
                self.alert(status_label_text="Started", title="Back to Work..", message="eyecare")
        
        self.time_label.after(500,self.get_time)


    def open_about(self):
        try:
            if self.about_window.about.winfo_exists():
                pass
        except:
            self.about_window = AboutWindow()
            
            if self.current_theme == "light":
                (self.about_window.set_theme(self.light, self.dark))  
            
            else: 
                (self.about_window.set_theme(self.dark, self.light))

#-----------------------------------------------------------------------------
#								AboutWindow
class AboutWindow(MainWindow):    
    def __init__(self):
        self.about = Tk()
        self.about.title("About")
        self.about.resizable(False, False)
        self.about.geometry("400x270+400+270")

        self.frame = LabelFrame(self.about, text="About")
        self.frame.pack(expand='yes', fill='both',padx=15,pady=15)

        self.credit = Label(self.frame,font=("Calibri",13),text='\nMade by Atharva Baradkar \n Using:\n Figma, Tkinter\nSun Valley Theme\n\n\n\n\n version: v2.0.0')
        self.credit.pack()


    def set_theme(self, theme_color_1, theme_color_2):
        self.about.config(background= theme_color_1)
        self.credit.config(background= theme_color_1, foreground= theme_color_2)
        self.frame.config(background= theme_color_1, foreground= theme_color_2)
     
#-----------------------------------------------------------------------------
#								Driver Code
if __name__ == "__main__":
    a = MainWindow()
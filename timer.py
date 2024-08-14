from tkinter import *
import tkinter as tk
from tkinter import messagebox
import csv
from tkinter import filedialog
import threading
import time
from tkinter.ttk import Progressbar

importedValue = False
subtasks = []
extend = False
skip = False
running = True
pause = False
timerStarted = False
subtaskStatistics = []
extended = False

entryYvalue = 130
timerYvalue = 165
totalTimeYvalue = 200

def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        win.destroy()

def skipFalse():
    global skip
    skip = False

# The function starts the timer for the subtask passed in.
def start(position, hours, minutes, seconds):

    global skip, extend
    global pause
    global running
    global now

    skipTask = False            # Tracks whether the current task is skipped         
    exit = False       

    progress["value"] = 0       # Resets the progress bar to 0 

    # Convert the total time to seconds
    totalSecs = hours*3600 + minutes*60 + seconds
    endTotalSecs = totalSecs    # Stores the initial total seconds.
    endExtendSecs = 0           # Stores the total extended amount of seconds

    while running == True and exit!= True and totalSecs >-1:
        while totalSecs > -1 and pause == False:

            if skip == True:
                skip =False
                exit = True
                skipTask = True

                # Calculates the amount of time spent for the subtask before it was skipped 
                finalTotalSecs = endTotalSecs - totalSecs
                fm = 0
                fh = 0
                fs = 0
                if finalTotalSecs > 3600:
                    fh = finalTotalSecs // 3600
                
                if finalTotalSecs > 60:
                    fm = (finalTotalSecs % 3600) // 60
                
                fs = (finalTotalSecs % 3600) % 60
                
                # Updates the subtaskStatistics[] to include the actual time spent on the task
                subtaskStatistics[position]["hours"] = fh
                subtaskStatistics[position]["seconds"] = fs
                subtaskStatistics[position]["minutes"] = fm

                break

            # Extends time for the current subtask  
            if extend == True:
                try:
                    extendsec = int(extendSec.get())
                    extendMin = int(extendmins.get())
                    extendHrs = int(extendhrs.get())

                    # Adds the extended seconds to the initial time
                    extendTotalSecs = extendHrs*3600 + extendMin*60 + extendsec
                    endExtendSecs += extendTotalSecs

                    newTotalSec = endTotalSecs + extendTotalSecs
                    
                    # Update the progress bar to show the extended time
                    if now == True:
                        nowTotalSecs = totalSecs
                        progress_progress = 100 / newTotalSec * (endTotalSecs - nowTotalSecs) 
                        progress['value'] = progress_progress
                        now = False

                    totalSecs += extendTotalSecs
                    extend = False

                except:
                    # Show error message when user enters non integers when extending hours, minutes, or seconds
                    errorMessage.configure(text="Error: All hours, minutes, and seconds should be integers! Please enter integers only and click extend button again!")
                    
                    # Calls threading object to allow the Timer to work separately with 5 seconds before configuring
                    # the error message.
                    threading.Timer(5.0, lambda: errorMessage.config(text="")).start()

                    # Set the extended seconds, minutes, and hours back to 0
                    extendSec.set('00')
                    extendmins.set('00')
                    extendhrs.set('00')
   
    if skipTask != True:

        endTotal = endExtendSecs + endTotalSecs
        
        tm = 0
        th = 0
        ts = 0
        if endTotal > 3600:
            th = endTotal // 3600
        
        if endTotal > 60:
            tm = (endTotal % 3600) // 60
        
        ts = (endTotal % 3600) % 60
        
        # Update the subtaskStatistics [] to include the actual time spent
        subtaskStatistics[position]["hours"] = th
        subtaskStatistics[position]["seconds"] = ts
        subtaskStatistics[position]["minutes"] = tm
    
    extended = False

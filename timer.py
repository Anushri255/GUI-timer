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



def importCSV():

    global entryYvalue
    global timerYvalue
    global totalTimeYvalue
    global timerStarted
    duplicate = False

    if timerStarted != True:
        try:
            userChoiceFile = filedialog.askopenfilename()

            importedFile = userChoiceFile

            # Initialize headings and rows list
            tasks = []
            rows = []

            # Creates a new list of all the tasks imported
            newSubtask = []

            if userChoiceFile.endswith(".csv"):
                importedFile = userChoiceFile

                # Initialize headings and rows list
                tasks = []
                rows = []

                newSubtask = [] # Creates a new list of all the tasks imported

                # Read csv file
                with open(importedFile, 'r') as csvfile:

                    # Create a csv reader object
                    csvreader = csv.reader(csvfile)

                    # Extract field names through first row
                    tasks = next(csvreader)

                    try:
                        for row in csvreader:
                                newSubtask.append({
                                    "subtask": row[0],
                                    "hours": int(row[1]),
                                    "minutes": int(row[2]),
                                    "seconds": int(row[3])
                                })
                    except Exception:
                        messagebox.showerror("Error", "Uh oh! Looks like the file you were trying to import was formatted incorrectly.\nPlease ensure that it imports the correct data types.")
                        return
                    
                    for num1 in subtasks:
                        for num2 in newSubtask:
                            if num1['subtask'] == num2['subtask']:
                                duplicate = True
                                break
                    
                    for i, num1 in enumerate(newSubtask):
                        for num2 in newSubtask[i+1:]:
                            if num1['subtask'] == num2['subtask']:
                                duplicate = True
                                break
                    
                    if duplicate == True:
                        messagebox.showerror("Error", "The name of the subtask in that file already exists!")
                        duplicate = False
                        return
                    
                    for num in newSubtask:
                        subtasks.append(num)

                # Print all the content
                for row in rows:
                    for col in row:
                        print("%10s" % col, end=" "),
                    print('\n')


                # Iterates through a {} containing subtasks imported from another CSV file
                for num in newSubtask:

                    # Creates Entry Widgets for hour, minute, and second 
                    sec = StringVar()
                    Entry(win, textvariable=sec, width = 2, font = 'Digital-7').place(x=320, y=entryYvalue)
                    sec.set(num["seconds"])
                    mins= StringVar()
                    Entry(win, textvariable = mins, width =2, font = 'Digital-7').place(x=280, y=entryYvalue)
                    mins.set(num["minutes"])
                    hrs= StringVar()
                    Entry(win, textvariable = hrs, width =2, font = 'Digital-7').place(x=242, y=entryYvalue)
                    hrs.set(num["hours"])
                    border_frame = Frame(win, bd=1, relief=SOLID)
                    subtaskName = StringVar()
                    subtaskName.set(num["subtask"])
                    subtaskName_entry = Entry(win, textvariable=subtaskName, width=20, borderwidth=1, relief='solid')
                    subtaskName_entry.place(x=10, y=entryYvalue)

                    #This stores the subtask name into the variable 'startName'
                    startName = str(num['subtask'])    
                                                            
                    # creates a button to allow users to start the timer from a specific sub task
                    startHere = Button(win, font=('DS-Digital Bold', 7), text='Start Timer Here', bd='2', bg='#FFFFE0', command=lambda startName=startName: startTimerPosition(startName))
                    startHere.place(x=150, y=entryYvalue)

                    # Changes the y coordinate to format the GUI
                    entryYvalue += 20      
                    timerYvalue += 20      
                    totalTimeYvalue += 20  
                    addSubtaskButton.place(x=350, y=entryYvalue)  
                    startTimerButton.place(y=timerYvalue+90)
                    
                    totalseconds.place(y=totalTimeYvalue)
                    totalminutes.place(y=totalTimeYvalue)
                    totalhours.place(y=totalTimeYvalue)
                    skip.place(y=timerYvalue + 130)
                    resumeButton.place(y=timerYvalue + 130)
                    pauseButton.place(y=timerYvalue + 130)
                    
                    extendTaskButton.place(y=totalTimeYvalue + 140)
                    extendedSecs.place(y=totalTimeYvalue + 140)
                    extendedMins.place( y=totalTimeYvalue + 140)
                    extendedHours.place(y=totalTimeYvalue + 140)
                    extendTimeLabel.place(y=totalTimeYvalue + 140)
                    progress.place(y= totalTimeYvalue+2)


                    finishedImport()
            else:
                messagebox.showerror("Error", "The file you are trying to import is not a CSV file!")
        except:
            messagebox.showerror("Unknown Error", "Please try to import again")
    else:
        errorMessage.configure(text="Error: Please wait until the timer has finished")
        threading.Timer(5.0, lambda: errorMessage.config(text="")).start()




def exportStats():
    try:
        global timerStarted

        if timerStarted != True:
            exportFileName = filedialog.asksaveasfilename(defaultextension=".doc")
            
            with open(f'{exportFileName}', 'w') as f:
                f.write("{:<20} {:<20} {:<23}\n".format("Task Name", "Planned Time", "Actual Time Spent"))
                f.write("\n")

                for task, stats in zip(subtasks, subtaskStatistics):
                    f.write("{:<23} {:02d}:{:02d}:{:02d} {:>10} {:02d}:{:02d}:{:02d}\n".format(
                        task["subtask"], task["hours"], task["minutes"], task["seconds"], "",
                        stats["hours"], stats["minutes"], stats["seconds"]
                    ))
        else:
            errorMessage.configure(text="Error: Please wait until the timer has finished")
            threading.Timer(5.0, lambda: errorMessage.config(text="")).start()

    except:
        messagebox.showerror("Error", "Please enter file name and click save to export a file with statistics.")




# This function will start the timer from the subtask defined by the user
def startTimerPosition(name):
    global totalTimeYvalue
    global timerStarted

    if timerStarted == False:
        index = 0  # Stores the position of the subtask 
        
        # Loop to find the position of the subtask defined by the user
        for num in subtasks:
            if num["subtask"] == name:
                break
            index += 1

        timerStarted = True


        l = Label(win,text = "", bg="light blue", font = 'Digital-7')
        for i, subtask in enumerate(subtasks):
            if i >= index:
                l.configure(text = "Task in progress: " + subtask["subtask"])
                l.place(x=120, y=totalTimeYvalue+40)
                start(i, subtask["hours"], subtask["minutes"], subtask["seconds"])
                
                # Update the GUI
                timerSec.set('00')
                timerMins.set('00')
                timerHrs.set('00')
        
        timerStarted = False
        l.configure(text="")
    else:
        errorMessage.configure(text="Error: Please wait until the timer has finished adding")
        threading.Timer(5.0, lambda: errorMessage.config(text="")).start()



# Create the GUI 
win = Tk()
win.geometry('700x400')
win.config(bg='light blue')
win.resizable(False, True)

# Create Label Widget to display an error message to the user.
errorMessage = Label(win, text="", bg="light blue", fg="red", font=('Digital-7', 10))
errorMessage.place(x=10, y=5)

Label(win, font =('DS-Digital Bold',18), text = 'Countdown Timer',bg='#D3D3D3').place(x=105,y=75)

# Assigned button widget to a variable for easier y-value modification in other function 
startTimerButton = Button(win, font =('DS-Digital Bold',10), text='Start Timer', bd ='2',bg = '#98FB98',command=startEachSubtask)
startTimerButton.place(x=260, y=timerYvalue + 90)

#Create Entry Widgets for hours, mins and secs
sec = StringVar()
Entry(win, textvariable=sec, width = 2, font = 'Digital-7').place(x=320, y=entryYvalue)
sec.set('00')
mins= StringVar()
Entry(win, textvariable = mins, width =2, font = 'Digital-7').place(x=280, y=entryYvalue)
mins.set('00')
hrs= StringVar()
Entry(win, textvariable = hrs, width =2, font = 'Digital-7').place(x=242, y=entryYvalue)
hrs.set('00')
border_frame = Frame(win, bd=1, relief=SOLID)
subtaskName = StringVar()
subtaskName.set('')
Entry(win, textvariable=subtaskName, width=20, borderwidth=1, relief='solid').place(x=10, y=entryYvalue)


addSubtaskButton = Button(win, font =('DS-Digital Bold',10), text='Add Subtask', bd ='2',bg = '#98FB98',command=addSubtask)
addSubtaskButton.place(x=350, y=entryYvalue)

pauseButton = Button(win, font =('DS-Digital Bold',10), text='Pause Timer', bd ='2',bg = '#D8BFD8',command=pause_f)
pauseButton.place(x=260, y=timerYvalue + 130)

resumeButton = Button(win, font =('DS-Digital Bold',10), text='Resume Timer', bd ='2',bg = '#D8BFD8',command=resume)
resumeButton.place(x=350, y=timerYvalue + 130)

skip = Button(win, font =('DS-Digital Bold',10), text='Skip Task', bd ='2',bg = '#D8BFD8',command = skipTask)
skip.place(x=180, y=timerYvalue + 130)

extendSec = StringVar()
extendedSecs = Entry(win, textvariable=extendSec, width = 2, font = 'Digital-7')
extendSec.set('00')
extendedSecs.place(x=350, y=totalTimeYvalue + 140)

extendmins= StringVar()
extendedMins = Entry(win, textvariable = extendmins, width =2, font = 'Digital-7')
extendmins.set('00')
extendedMins.place(x=320, y=totalTimeYvalue + 140)

extendhrs= StringVar()
extendedHours = Entry(win, textvariable = extendhrs, width =2, font = 'Digital-7')
extendhrs.set('00')
extendedHours.place(x=290, y=totalTimeYvalue + 140)

extendTimeLabel = Label(win, text = ' Extend Task:', bg='light blue',font = 'Digital-7 12')
extendTimeLabel.place(x=180, y=totalTimeYvalue + 140)

extendTaskButton = Button(win, font =('DS-Digital Bold',10), text='Extend', bd ='2',bg = '#D8BFD8', command = extendTask)
extendTaskButton.place(x=380, y=totalTimeYvalue + 140)


importCsvButton = Button(win, font =('DS-Digital Bold',10), text='Import csv', bd ='2',bg = '#FFC0CB',command=importCSV)
importCsvButton.place(x=80, y=30)
exportCsvButton = Button(win, font =('DS-Digital Bold',10), text='Export csv', bd ='2',bg = '#FFC0CB',command=exportCSV)
exportCsvButton.place(x=180, y=30)
exportStatsBtn = Button(win, font =('DS-Digital Bold',10), text='Export Statistics', bd ='2',bg = '#FFC0CB',command=exportStats)
exportStatsBtn.place(x=280, y=30)


timerSec = StringVar()
totalseconds = Label(win, textvariable=timerSec, width = 2, font = 'Digital-7')
totalseconds.place(x=320, y=totalTimeYvalue)
timerSec.set('00')
timerMins = StringVar()
totalminutes = Label(win, textvariable = timerMins, width =2, font = 'Digital-7')
totalminutes.place(x=280, y=totalTimeYvalue)
timerMins.set('00')
timerHrs= StringVar()
totalhours = Label(win, textvariable = timerHrs, width =2, font = 'Digital-7')
totalhours.place(x=242, y=totalTimeYvalue)
timerHrs.set('00')

progress = Progressbar(win, orient = HORIZONTAL,
              length = 100, mode = 'determinate')
progress.pack(pady = 10)
progress.place(x=360, y= totalTimeYvalue+2)

win.protocol("WM_DELETE_WINDOW", on_closing)

win.mainloop()
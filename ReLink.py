#!/usr/bin/env python3

#Library imports
from tkinter import *
from tkinter import StringVar
import time
from functools import partial

class App:
# Class to manage ReLink PiHat
# ---------------------------------------


    def __init__(self, master):
    # Init function for class
    # -----------------------
    
        frame = Frame(master)
        frame.pack()
        

        #arrays of IO states and GPIO pins (we always use J pin number convention in this program)
        self.IOState=[0,0,0,0]
        self.jPin   =[15,22,29,36,]
        self.AllState = 0

        
        # Create and position each of the buttons 
        self.ChannelButton15 = Button(frame, text="15",bg = "red",height=1, width=1)
        self.ChannelButton15.grid(row=7,column=2); 
        self.ChannelButton22 = Button(frame, text="22",bg = "red",height=1, width=1)
        self.ChannelButton22.grid(row=10,column=3); 
        self.ChannelButton29 = Button(frame, text="29",bg = "red",height=1, width=1)
        self.ChannelButton29.grid(row=14,column=2); 
        self.ChannelButton36 = Button(frame, text="36",bg = "red",height=1, width=1)
        self.ChannelButton36.grid(row=17,column=3); 

        # create on and off actions for each button
        action_toggle15= partial(self.ToggleOnOff, 0, self.ChannelButton15)
        action_toggle22= partial(self.ToggleOnOff, 1, self.ChannelButton22)
        action_toggle29= partial(self.ToggleOnOff, 2, self.ChannelButton29)
        action_toggle36= partial(self.ToggleOnOff, 3, self.ChannelButton36)

        #associate the actions with the button
        self.ChannelButton15.config(command=action_toggle15)
        self.ChannelButton22.config(command=action_toggle22)
        self.ChannelButton29.config(command=action_toggle29)
        self.ChannelButton36.config(command=action_toggle36)

        # Create the GPIO labels alongside the buttons
        l15 = Label(frame, text = "GPIO22", height=1, width=6);
        l15.grid (row=7, column=0)
        l22 = Label(frame, text = "GPIO25", height=1, width=6);
        l22.grid (row=10, column=4)
        l29 = Label(frame, text = "GPIO05", height=1, width=6);
        l29.grid (row=14, column=0)
        l36 = Label(frame, text = "GPIO16", height=1, width=6);
        l36.grid (row=17, column=4)

        # Create the Toggle All button
        ToggleAllButton = Button(frame, text="Toggle All",  height=1, width=25, command =self.ToggleAll)
        ToggleAllButton.grid(row=20, column=0,columnspan=5)

    
    def ToggleAll(self):
    # toggle all i/os on or off
    # -------------------------
    
        if self.AllState==1:
            self.AllState = 0
            bgclr="red"
            fgclr="black"
        else:
            self.AllState = 1
            bgclr="green"
            fgclr="white"

        # update the button colours according to the IO state
        self.ChannelButton15.config(fg = fgclr , bg = bgclr)
        self.ChannelButton22.config(fg = fgclr , bg = bgclr)
        self.ChannelButton29.config(fg = fgclr , bg = bgclr)
        self.ChannelButton36.config(fg = fgclr , bg = bgclr)

        # put the new i/o states in the array of i/o states
        for idx in range(4):    
            GPIO.output(self.jPin[idx] ,self.AllState)
            self.IOState[idx] = self.AllState

    
    def ToggleOnOff(self, idx, button):
        # Toggle an i/o on or off
        # -----------------------
        if (self.IOState[idx] == 0):
            self.IOState[idx] = 1
            button.config(bg="green", fg="white")
        else:
            self.IOState[idx] = 0
            button.config(bg="red", fg="black")
        GPIO.output(self.jPin[idx] ,self.IOState[idx])
        
    
    
    def SetAllOff(self):
        # Drive all outputs to the 'off' state
        # ------------------------------------
        
        for idx in range(4):    
            GPIO.output(self.jPin[idx] ,0)
            self.IOState[idx] = 0

# Main program
# ------------

import RPi.GPIO as GPIO

#Turn off GPIO warnings
GPIO.setwarnings(False)

#Set the GPIO numbering convention to be header pin numbers
GPIO.setmode(GPIO.BOARD)

#Configure each GPIO pin as an output
GPIO.setup(15,GPIO.OUT)
GPIO.setup(22,GPIO.OUT)
GPIO.setup(29,GPIO.OUT)
GPIO.setup(36,GPIO.OUT)


#Create our window using Tkinter
root = Tk()
root.title('ReLink PiHat')
root.resizable(width=FALSE, height=FALSE)

app = App(root)

#Turn all the GPIO off to start with
app.SetAllOff()

#Main loop - responds to dialog events
root.mainloop()

#we exit the main loop if user has closed the window
#reset the GPIO and end the program
GPIO.cleanup()

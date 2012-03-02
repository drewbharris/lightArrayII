#! /usr/bin/python
# requires pyPortMidi
import pypm
import time

INPUT=0
OUTPUT=1
latency=10
      
class LightArray():
    def __init__(self):
        self.lightOne = 42
        self.lightTwo = 43
        self.lightThree = 44
        self.lightFour = 45
        self.lightFive = 46
        self.MidiOut = None
        
    def initialize(self):
        pypm.Initialize()
        midiOutput = self.selectFirebox()
        if (midiOutput >= 0):
            self.MidiOut = pypm.Output(midiOutput, latency)
            return True
        else:
            print "Couldn't select Firebox."
            return False

    def writeAll(self, value):
        self.one(value)
        self.two(value)
        self.three(value)
        self.four(value)
        self.five(value)
    def one(self, value):
        self.MidiOut.WriteShort(0xb0,self.lightOne,value)

    def two(self, value):
        self.MidiOut.WriteShort(0xb0,self.lightTwo,value)

    def three(self, value):
        self.MidiOut.WriteShort(0xb0,self.lightThree,value)

    def four(self, value):
        self.MidiOut.WriteShort(0xb0,self.lightFour,value)

    def five(self, value):
        self.MidiOut.WriteShort(0xb0,self.lightFive,value)
        
    def printDevices(self, InOrOut):
        for loop in range(pypm.CountDevices()):
            interf,name,inp,outp,opened = pypm.GetDeviceInfo(loop)
            if ((InOrOut == INPUT) & (inp == 1) | (InOrOut == OUTPUT) & (outp ==1)):
                print loop, name," ",
                if (inp == 1): print "(input) ",
                else: print "(output) ",
                if (opened == 1): print "(opened)"
                else: print "(unopened)"
    
    def selectFirebox(self):
        midiOut = -1
        for loop in range(pypm.CountDevices()):
            interf,name,inp,outp,opened = pypm.GetDeviceInfo(loop)
            if (outp == 1):
                if "FIREBOX" in name:
                    midiOut = loop            
        return midiOut    

lights = LightArray()
available = lights.initialize()
if available:
    print "\n\
welcome to lightarray.\n\n\
available programs:\n\
1. turn lights on\n\
2. turn lights off\n\
3. enter a value 0-127\n\
4. exit\n"
    running = True
    while (running):
        prog = int(raw_input("type program number:\n "))
        if (prog == 1):
            lights.writeAll(127)
        elif (prog == 2):
            lights.writeAll(0)
        elif (prog == 3):
            value = int(raw_input("type a value:\n "))
            if (0 <= value <= 127):
                lights.writeAll(value)
            else:
                print "invalid value.\n\n"
        elif (prog == 4):
            running = False
        else:
            print "invalid option. please try again."
    


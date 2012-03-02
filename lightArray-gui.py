#! /usr/bin/python
# File: hello2.py

import Tkinter
import pypm
import time

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
    
    def selectFirebox(self):
        midiOut = -1
        for loop in range(pypm.CountDevices()):
            interf,name,inp,outp,opened = pypm.GetDeviceInfo(loop)
            if (outp == 1):
                if "FIREBOX" in name:
                    midiOut = loop            
        return midiOut    



class gui(Tkinter.Tk):
    def __init__(self,parent):
        Tkinter.Tk.__init__(self,parent)
        self.parent = parent
        self.initialize()
        self.lights = None

    def initialize(self):
        self.grid()


        button = Tkinter.Button(self,text=u"on",command=self.On,background='black')
        button.grid(column=0,row=3)
        
        button = Tkinter.Button(self,text=u"off",command=self.Off)
        button.grid(column=1,row=3)
        
        button = Tkinter.Button(self,text=u"connect",command=self.Connect)
        button.grid(column=2,row=3)
        
        button = Tkinter.Button(self,text=u"disconnect",command=self.Disconnect)
        button.grid(column=3,row=3)

        self.current_value = Tkinter.StringVar()
        
        label = Tkinter.Label(self,textvariable=self.current_value)
        label.grid(column=0,row=1,columnspan=4,sticky='N')
        
        label = Tkinter.Label(self,text='L I G H T A R R A Y')
        label.grid(column=0,row=0,columnspan=4,sticky='N')
        
        self.connect_label = Tkinter.Label(self,text='disconnected',foreground='red')
        self.connect_label.grid(column=0,row=4,columnspan=4,sticky='N')
        
        self.valueSlider = Tkinter.Scale(self,command=self.Value,orient='horizontal',bd='0',
                                         from_='0',to='127',length='200',relief='flat')
        self.valueSlider.grid(column=0,row=2,columnspan=6,sticky='N')

        self.grid_columnconfigure(0,weight=1)
        self.resizable(True,False)
        
        self.current_value.set("idle")

    def Connect(self):
        self.lights = LightArray()
        available = self.lights.initialize()
        if available:
            self.connect_label['fg'] = 'green'
            self.connect_label['text'] = 'connected'
            self.lights.writeAll(self.valueSlider.get())
        else:
            self.Error()
            self.lights = None
    
    def Disconnect(self):
        pypm.Terminate()
        self.lights = None
        self.connect_label['fg'] = 'red'
        self.connect_label['text'] = 'disconnected'
        
    def On(self):
        self.valueSlider.set('127')
        
    def Off(self):
        self.valueSlider.set('0')
        
    def Value(self, value):
        if (self.lights != None):
            self.lights.writeAll(int(value))
        if value == '127':
            self.current_value.set('on')
        elif value == '0':
            self.current_value.set('off')
        else:
            self.current_value.set(value)
            
    def Error(self):
        self.current_value.set('couldn\'t connect to firebox :(')

if __name__ == "__main__":
    app = gui(None)
    app.title('lightArray')
    app.mainloop()
    

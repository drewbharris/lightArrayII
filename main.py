# requires pyPortMidi
import pypm
import web

INPUT=0
OUTPUT=1
latency=10
midiOutSet=False

urls = (
    '/', 'main'
)
app = web.application(urls, globals())

class main:
	def GET(self):
		lights = LightArray()
		available = lights.initialize()
		if available:
			return "Firebox selected."
		else:
			return "Could not select Firebox."

class LightArray():
	def __init__(self):
		self.lightOne = 42
		self.lightTwo = 43
		self.lightThree = 44
		self.lightFour = 45
		self.lightFive = 46
		
	def initialize(self):
		pypm.Initialize()
		midiOutput = self.SelectFirebox()
		if (midiOutput >= 0):
			MidiOut = pypm.Output(midiOutput, latency)
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
		
	def PrintDevices(self, InOrOut):
		for loop in range(pypm.CountDevices()):
			interf,name,inp,outp,opened = pypm.GetDeviceInfo(loop)
			if ((InOrOut == INPUT) & (inp == 1) | (InOrOut == OUTPUT) & (outp ==1)):
				print loop, name," ",
				if (inp == 1): print "(input) ",
				else: print "(output) ",
				if (opened == 1): print "(opened)"
				else: print "(unopened)"
	
	def SelectFirebox(self):
		midiOut = -1
		for loop in range(pypm.CountDevices()):
			interf,name,inp,outp,opened = pypm.GetDeviceInfo(loop)
			if (outp == 1):
				if "FIREBOX" in name:
					midiOut = loop			
		return midiOut	
	
if __name__ == "__main__":
    app.run()



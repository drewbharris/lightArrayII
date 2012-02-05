# requires pyPortMidi
import pypm
import web
import threading
import time

INPUT=0
OUTPUT=1
latency=10

urls = (
    '/(.*)', 'main'
)

render = web.template.render('templates/')
app = web.application(urls, globals())

class main:
	def GET(self, page):
		lights = LightArray()
		available = lights.initialize()
		if available:
			if (page == "on"):
				lights.writeAll(127)
				return render.index("on")
			elif (page == "off"):
				lights.writeAll(0)
				return render.index("off")
			elif (page == "fadeon"):
				for i in range(127):
					lights.writeAll(i)
				return render.index("fadeon")
			elif (page == "fadeoff"):
				for i in range(127):
					lights.writeAll(127-i)
				return render.index("fadeoff")
			else:
				return render.index("idle")
		else:
			return render.index("error")
	
		
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

if __name__ == "__main__":
    app.run()



#!/usr/bin/env python
# encoding: utf-8

import sys
import os
import serial

ser = serial.Serial("/dev/tty.usbserial-A6008hrf", 31250)

def sendMidi(status, controller, value):
	ser.write(bytes((status,)))
	ser.write(bytes((controller,)))
	ser.write(bytes((value,)))

def main():
	sendMidi(176, 37, 127)
	sendMidi(176, 42, 127)
	sendMidi(176, 43, 127)
	sendMidi(176, 44, 127)

if __name__ == '__main__':
	main()


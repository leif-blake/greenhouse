#This is a collection of functions for communicating with the Arduino
import serial
from serial import Serial
from datetime import datetime

class ArduinoSerial(Serial):

	def setupArduino():
		arduino.write("log;".encode())
		inputData = arduino.readline()
		parseCommand(inputData)

		setOutputs()

	def resetArduino():
		arduino.setDTR(False)
		sleep(1)
		# toss any data already received, see
		arduino.flushInput()
		arduino.setDTR(True)
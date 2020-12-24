#This is a collection of functions for communicating with the Arduino
import serial
from serial import Serial
from datetime import datetime

class ArduinoSerial(Serial):
	def __init__(self, port, baud, timeout_s):
		#configure serial
		arduino = Serial('/dev/' + port,
	                     baudrate=baud,
	                     timeout=timeout_s,
	                     )

	def open():
		arduino.open()

	def close():
		arduino.close()

	def readline():
		return arduino.readline()

	def write(data):
		arduino.write(data)

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

	def setOutputs():
		outputFields, outputValues = calcOutputs()

		numOutputs = 1
		outputString = "stp;" + str(numOutputs)
		for i in range(0,numOutputs):
			outputString =+ (outputFields[i] + ","
							+ str(outputValues[i]) + ";")

		arduino.write(outputString.encode())
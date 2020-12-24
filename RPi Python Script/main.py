import serial
from serial import Serial
from datetime import datetime

### FUNCTION MODULES ###
import mariadbConnect

### GLOBAL VARIABLES ###

dataLogInt = 20 #Logging interval in seconds

port = 'ttyUSB0'
arduino = Serial('/dev/' + port,
	                     baudrate=baud,
	                     timeout=timeout_s,
	                     )

### FUNCTIONS ###

#Start up arduino serial connection, log data, and set outputs
def setupArduino():
	try:
		arduino.open()
	except Exception as error:
		print ("ERROR: Failed to connect on " + str(port) + ": " + str(error))
		sleep(5)
	arduino.write("log;".encode())
	inputData = arduino.readline()
	parseMSG(inputData)

	setOutputs()

#Reset Arduino serial connection
def resetArduino():
	arduino.setDTR(False)
	sleep(1)
	# toss any data already received
	arduino.flushInput()
	arduino.setDTR(True)

#Calculates desired outputs based on most recent sesnor data logged to database
def calcOutputs():
	viewConn = openViewConnection()
	viewCur = viewConn.cursor()

	try:
		viewCur.excecute("SELECT * from greenhouse.data ORDER BY timestamp DESC LIMIT 2")
	except Exception as error:
		print("ERROR: Failed to get data from database: " + str(error))

	dbData = cur.fetchall()

	viewConn.close()

	for i in range(0,2):
		for j in range(0,8):
			dbData[i][j] = int(dbData[i][j])

	#Currently hardcoded F1 as only output, needs to change
	outputFields = ['F1']
	outputValues = [0]
	#set F1 if temperature above 25C
	if(dbData[0][0] > 25):
		outputValues[0] = 1

	logConn = openLogConnection()
	logCur = conn.cursor()

	try:
		cur.execute('INSERT INTO greenhouse.output (' 
					+ fields + 'timestamp) VALUES (' 
					+ values + '\''
					+ datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '\')')
	except Exception as error:
		print("ERROR: Failed to log to database: " + str(error))

	conn.close()

	return outputFields, outputValues

#Commands arduino to set outputs
def setOutputs():
	outputFields, outputValues = calcOutputs()

	numOutputs = 1
	outputString = "stp;" + str(numOutputs)
	for i in range(0,numOutputs):
		outputString =+ (outputFields[i] + ","
						+ str(outputValues[i]) + ";")

	arduino.write(outputString.encode())

#Print message received from arduino
def msgReceived(parsedData):
	print('LOG: Command \'' + parsedData[0] + '\' successfully received by arduino')

#Arduino received unkonwn command
def processError(parsedData):
	print('Error: Arduino unable to process command: ' +  parsedData[0])

#Parses a message received from the Arduino
def parseMSG(inputData):
	print("LOG: Data input from Arduino: " + str(inputData))
	try:
		inputData =  inputData.decode().rstrip()
	except Exception as error:
		print ("ERROR: Failed to decode data (" + str(inputData) + ") from Arduino: " + str(error))

	try:
		keyVals = inputData.split(';')
		command = keyVals[0]
		if command == 'dta': #data dump from arduino
			logDataDB(keyVals[1:]) #log into database w/o command
		elif command == 'rst': #request for setup
			setupArduino()
		elif command == 'thx': #acknowledgement of command
			msgReceived(keyVals[1:])
		elif command == 'err': #error
			processError(keyVals[1:])
		else:
			print("Unknown command from Arduino: " + command)
	except Exception as error:
		print("ERROR: Failed to parse data from Arduino: " + str(error))

### MAIN CODE ###

lastLogTime = datetime.now()
print (datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
#main loop, switch between passive reading mode and logging data/setting outputs
while(True):
	#connect to arduino
	while(not arduino.is_open):
		setupArduino();

	#sit in read mode, wait for data from arduino
	while((datetime.now() - lastLogTime).seconds < dataLogInt):
		try:
			inputData = ''
			inputData = arduino.readline()
		except Exception as error:
			print("ERROR: Failed to read from arduino while awaiting data from Arduino: " + str(error))
		if(inputData):
				parseMSG(inputData)

	#Once log time interval has passed, log sensor data
	try:
		print("LOG: Attempting to log data")
		arduino.write("log;".encode())
	except Exception as error:
		print("ERROR: Failed to write to Arduino: " + str(error))
	try:
		inputData = ''
		inputData = arduino.readline()
	except Exception as error:
		print("ERROR: Failed to get data from Arduino: " + str(error))
	parseMSG(inputData)

	lastLogTime = datetime.now()


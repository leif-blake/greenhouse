#This is a collection of functions to read and store data to the mariadb database
import serial
from datetime import datetime
from serial import Serial
import mariadb

#Settings for opening a connection to the MariaDB database for logging data
def openLogConnection():
	try:
		conn = mariadb.connect(
	      user="greenhouse_logger",
	      password="lumbernotlogs",
	      host="localhost",
	      port=3306)
	except Exception as error:
		print("ERROR: Failed to connect to MariaDB as logger: " + str(error))
	return conn

#Settings for opening a connection to the MariDB data base for reading data
def openViewConnection():
	try:
		conn = mariadb.connect(
	      user="greenhouse_viewer",
	      password="showmethatdata",
	      host="localhost",
	      port=3306)
	except Exception as error:
		print("ERROR: failed to connect to MariaDB as viewer: " + str(error))
	return conn

#Write sensor data to database
def logDataDB(parsedData):
	fields = ''
	values = ''
	#Split data into fields and values by comma delimitter
	for item in parsedData:
		keyValPair = item.split(',')
		fields += keyValPair[0]
		fields += ", "
		values += keyValPair[1]
		values += ", "

	conn = openLogConnection()
	cur = conn.cursor()

	#Log sensor values and fields into database
	try:
		cur.execute('INSERT INTO greenhouse.data (' 
					+ fields + 'timestamp) VALUES (' 
					+ values + '\''
					+ datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '\')')
	except Exception as error:
		print("ERROR: Failed to log to database: " + str(error))

	conn.close()
	
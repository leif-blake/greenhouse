# IMPORTS
from time import sleep
from serial import Serial
from datetime import datetime
import logging

# LOCAL MODULES
import mariadb_connect as dbConn
import arduino_serial
import config
from logger_setup import setupLog

# GLOBAL VARS
dataLogInt = config.data_log_int()  # Logging interval in seconds
arduino = arduino_serial.ArduinoSerial()

# LOGGING
logger = logging.getLogger(__name__)
setupLog(logger)

# FUNCTIONS
# Start up arduino serial connection, log data, and set outputs
def setup_arduino():
    try:
        if not arduino.open():
            return False
        input_data = ''
        input_data = arduino.get_data()
        parse_msg(input_data)
        calc_outputs()
        command_out()
        return True
    except:
        logger.exception('Error in setting up Arduino')


# Calculates desired outputs based on most recent sensor data logged to database
def calc_outputs():
    try:
        db_data = dbConn.get_data_db()
        logger.debug('DB Data: ' + str(db_data))

        # Currently hardcoded F1 as only output, needs to change
        output_vals = []

        # set F1 if temperature above 25C
        if db_data[0][0] > 25:
            output_vals[0] = 1

        dbConn.log_outputs_db(output_vals)
    except:
        logger.exception('Error in calculating outputs')


# Commands arduino to set outputs
def command_out():
    try:
        output_fields = config.o_fields()
        output_vals = dbConn.get_outputs_db()

        arduino.set_outputs(output_fields, output_vals)
    except:
        logger.exception('Error in writing outputs to Arduino')


# Print message received from arduino
def msg_received(parsed_data):
    logger.info('Command \'' + str(parsed_data[0]) + '\' successfully received by arduino')


# Process error when Arduino received unknown command
def proc_err(parsed_data):
    logger.warning('Arduino unable to process command: ' + str(parsed_data[0]))


# Parses a message received from the Arduino and calls the appropriate function depending on the command
def parse_msg(input_data):
    logger.info('Data input from Arduino: ' + str(input_data))
    try:
        input_data = input_data.decode().rstrip()
    except:
        logger.exception('Failed to decode data (' + str(input_data) + ') from Arduino')

    try:
        key_vals = input_data.split(';')  # splits data into list of key value pairs
        command = key_vals[0]  # first key is the command, no associated value
        if command == 'dta':  # data dump from arduino
            dbConn.log_data_db(key_vals[1:])  # log into database w/o command
        elif command == 'rst':  # request for setup
            setup_arduino()
        elif command == 'thx':  # acknowledgement of command
            msg_received(key_vals[1:])
        elif command == 'err':  # error
            proc_err(key_vals[1:])
        else:
            logger.warning('Unknown command from Arduino: ' + str(command))
    except:
        logger.exception('Failed to parse data from Arduino: ' + str(input_data))


# MAIN CODE
lastLogTime = datetime.now()
logger.info('Started')

# main loop, switch between passive reading mode and logging data/setting outputs
while True:
    # connect to arduino
    while not arduino.is_open():
        if not setup_arduino():
            logger.warning('Error in connecting to Arduino, trying again in 5 seconds')
            sleep(5)

    # sit in read mode, wait for data from arduino
    while (datetime.now() - lastLogTime).seconds < dataLogInt:
        inputData = ''
        inputData = arduino.read_line()
        if inputData:
            parse_msg(inputData)

    # Once log time interval has passed, log sensor data
    logger.info('Attempting to log data')
    arduino.write("log;")
    inputData = ''
    inputData = arduino.read_line()
    parse_msg(inputData)

    lastLogTime = datetime.now()

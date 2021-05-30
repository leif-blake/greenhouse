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

# LOGGING
logger = logging.getLogger(__name__)
setupLog(logger)

# GLOBAL VARS
dataLogInt = config.data_log_int()  # Logging interval in seconds
arduino = arduino_serial.ArduinoSerial()


# FUNCTIONS
# Calculate and send new outputs to arduino
def set_outputs():
    calc_outputs()
    command_out()


# Calculates desired outputs based on most recent sensor data logged to database
def calc_outputs():
    logger.debug('calculating outputs')
    try:
        data_dict = dbConn.query_db('data',entries=3)
        old_output_dict = dbConn.query_db('output')

        # Set new outputs as most recent entry from old outputs
        new_output_dict = {i: old_output_dict.get(i)[0] for i in old_output_dict}
        new_output_dict.pop('timestamp')  # timestamp will be auto-generated at time of DB write

        # set F1 if most recent temperature above 25C
        if data_dict['T1'][0] > 25:
            new_output_dict['F1'] = 1

        logger.debug('Output Dictionary: ' + str(new_output_dict))

        dbConn.log_outputs_db(new_output_dict)
    except:
        logger.exception('Error in calculating outputs')


# Commands arduino to set outputs
def command_out():
    logger.debug('Sending outputs to arduino')
    output_dict = dbConn.query_db('output')
    try:
        output_dict.pop('timestamp')  # Don't write timestamp from db to arduino

        output_fields = []
        output_vals = []
        for key, val in output_dict.items():
            output_fields.append(key)
            output_vals.append(val[0])

        arduino.set_outputs(output_fields, output_vals)
    except:
        logger.exception('Could not write outputs to Arduino')
        logger.debug('Output dict: ' + str(output_dict))


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
            dbConn.log_data_db(key_vals[1:])  # log sensor data into database
            set_outputs()
        elif command == 'rst':  # request for setup
            arduino.get_data()
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

# *********************************************************************************************************************
# Main loop, switch between passive reading mode and logging data/setting outputs
while True:

    # connect to arduino
    while not arduino.is_open():
        if not arduino.open():
            logger.warning('Could not connect to Arduino, trying again in 5 seconds')
            sleep(5)

    # sit in read mode, wait for data from arduino
    while (datetime.now() - lastLogTime).seconds < dataLogInt:
        inputData = ''
        inputData = arduino.read_line()
        if inputData:
            parse_msg(inputData)

    # Once log time interval has passed, log sensor data
    arduino.get_data()

    lastLogTime = datetime.now()
# *********************************************************************************************************************




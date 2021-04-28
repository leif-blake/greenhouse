# IMPORTS
from time import sleep
from serial import Serial
from datetime import datetime

# LOCAL MODULES
import mariadb_connect as dbConn
import arduino_serial

# GLOBAL VARS
dataLogInt = 20  # Logging interval in seconds
port = 'ttyUSB0'
arduino = arduino_serial.ArduinoSerial(port='/dev' + port,
                                       baud=11500,
                                       timeout_s=10)


# FUNCTIONS
# Start up arduino serial connection, log data, and set outputs
def setup_arduino():
    arduino.open()
    input_data = arduino.get_data()
    parse_msg(input_data)
    calc_outputs()
    command_out()


# Calculates desired outputs based on most recent sensor data logged to database
def calc_outputs():
    db_data = dbConn.get_data_db()

    # Currently hardcoded F1 as only output, needs to change
    output_fields = ['F1']
    output_vals = [0]

    # set F1 if temperature above 25C
    if db_data[0][0] > 25:
        output_vals[0] = 1

    dbConn.log_outputs_db(output_vals)


# Commands arduino to set outputs
def command_out():
    output_fields = dbConn.outputFields
    output_vals = dbConn.get_outputs_db()

    arduino.set_outputs(output_fields, output_vals)


# Print message received from arduino
def msg_received(parsed_data):
    print('LOG: Command \'' + parsed_data[0] + '\' successfully received by arduino')


# Process error when Arduino received unknown command
def proc_err(parsed_data):
    print('Error: Arduino unable to process command: ' + parsed_data[0])


# Parses a message received from the Arduino and calls the appropriate function depending on the command
def parse_msg(input_data):
    print("LOG: Data input from Arduino: " + str(input_data))
    try:
        input_data = input_data.decode().rstrip()
    except Exception as error:
        print("ERROR: Failed to decode data (" + str(input_data) + ") from Arduino: " + str(error))

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
            print("Unknown command from Arduino: " + command)
    except Exception as error:
        print("ERROR: Failed to parse data from Arduino: " + str(error))


# MAIN CODE
lastLogTime = datetime.now()
print("LOG: Start time: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

# main loop, switch between passive reading mode and logging data/setting outputs
while True:
    # connect to arduino
    while not arduino.is_open():
        setup_arduino()

    # sit in read mode, wait for data from arduino
    while (datetime.now() - lastLogTime).seconds < dataLogInt:
        inputData = ''
        inputData = arduino.read_line()
        if inputData:
            parse_msg(inputData)

    # Once log time interval has passed, log sensor data
    print("LOG: Attempting to log data")
    arduino.write("log;".encode())
    inputData = ''
    inputData = arduino.read_line()
    parse_msg(inputData)

    lastLogTime = datetime.now()

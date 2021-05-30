# This files serves to retrieve i/o field names and global variables

# IMPORTS
import csv
import subprocess
import logging

# LOCAL MODULES
import mariadb_connect as dbConn
from logger_setup import setupLog


# LOGGING
logger = logging.getLogger(__name__)
setupLog(logger)


# Return type: list of Strings
# def o_fields():
#     try:
#         return read_config()['outputs']
#     except:
#         logger.exception('Failed to read config file')
#
#
# # Return type: list of Strings
# def i_fields():
#     try:
#         return read_config()['inputs']
#     except:
#         logger.exception('Failed to read config file')


# Return type: int
def max_o_val():
    try:
        return int(read_config()['maxOutputVal'][0])
    except:
        logger.exception('Failed to read config file')


# Return type: int
def data_log_int():
    try:
        return int(read_config()['dataLogInt_s'][0])
    except:
        logger.exception('Failed to read config file')


# Return type: String
# Gets port from arduino-cli command, then updates the config file and returns the port
def arduino_port(curr_port='/dev/ttyACM0'):
    try:
        # Capture the port of the arduino (takes first Arduino in list, assumes Arduino is connected)
        boardList = subprocess.run(['arduino-cli', 'board', 'list'], capture_output=True)
        boardListSplit = str(boardList).split('\\n')
        port = boardListSplit[1].split(' ')[0]

        # Read the configuration files into a dictionary, replace the port with the correct port
        config_dict = read_config()
        config_dict['arduinoPort'] = [port]

        # Write config back to csv
        with open('../config.csv', 'w+', newline='') as configfile:
            writer = csv.writer(configfile, delimiter=',')
            for key in config_dict:
                writer.writerow([key] + config_dict[key])

        # Return new value of port stored in csv
        return port
    except:
        logger.exception('Failed to read config file')
        return curr_port


# Return type: int
def arduino_baud():
    try:
        return int(read_config()['arduinoBaud'][0])
    except:
        logger.exception('Failed to read config file')


# Return type: int
def arduino_timeout():
    try:
        return int(read_config()['arduinoTimeOut_s'][0])
    except:
        logger.exception('Failed to read config file')


# Reads the configuration files into a dictionary
def read_config():
    try:
        with open('../config.csv', newline='') as configfile:
            reader = csv.reader(configfile, delimiter=',')
            config_dict = {}
            for row in reader:
                config_dict[row[0]] = row[1:]

        return config_dict
    except:
        logger.exception('Failed to read config file')

# This files serves to retrieve i/o field names and global variables

# IMPORTS
import csv

# LOCAL MODULES
import mariadb_connect as dbConn


# Return type: list of Strings
def o_fields():
    try:
        return read_config()['outputs']
    except Exception as error:
        print("ERROR: Failed to read config file: " + str(error))


# Return type: list of Strings
def i_fields():
    try:
        return read_config()['inputs']
    except Exception as error:
        print("ERROR: Failed to read config file: " + str(error))


# Return type: int
def max_o_val():
    try:
        return int(read_config()['maxOutputVal'][0])
    except Exception as error:
        print("ERROR: Failed to read config file: " + str(error))


# Return type: int
def data_log_int():
    try:
        return int(read_config()['dataLogInt_s'][0])
    except Exception as error:
        print("ERROR: Failed to read config file: " + str(error))


# Return type: String
def arduino_port():
    try:
        return read_config()['arduinoPort'][0]
    except Exception as error:
        print("ERROR: Failed to read config file: " + str(error))


# Return type: int
def arduino_baud():
    try:
        return int(read_config()['arduinoBaud'][0])
    except Exception as error:
        print("ERROR: Failed to read config file: " + str(error))


# Return type: int
def arduino_timeout():
    try:
        return int(read_config()['arduinoTimeOut_s'][0])
    except Exception as error:
        print("ERROR: Failed to read config file: " + str(error))


# Reads the configuration files into a dictionary
def read_config():
    with open('../config.csv', newline='') as configfile:
        reader = csv.reader(configfile, delimiter=',')
        config_dict = {}
        for row in reader:
            config_dict[row[0]] = row[1:]

    return config_dict

# TODO: Implement function that updates config.csv AND edits+recompiles Arduino code
# def update_io():
#     oFields = dbConn.get_fields_db('output')
#     iFields = dbConn.get_fields_db('data')
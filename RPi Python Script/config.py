# This files serves to retrieve i/o field names and global variables

# IMPORTS
import csv

# LOCAL MODULES
import mariadb_connect as dbConn


def o_fields():
    try:
        return read_config()['outputs']
    except Exception as error:
        print("ERROR: Failed to read config file: " + str(error))


def i_fields():
    try:
        return read_config()['inputs']
    except Exception as error:
        print("ERROR: Failed to read config file: " + str(error))


def max_o_val():
    try:
        return read_config()['maxOutputVal']
    except Exception as error:
        print("ERROR: Failed to read config file: " + str(error))


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
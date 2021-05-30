# A collection of functions to read and store data from/to the mariadb database.
# NOTE: Includes passwords for database: should be password protected

# IMPORTS
from datetime import datetime
import mariadb
import logging

# LOCAL MODULES
import config
from logger_setup import setupLog

# LOGGING
logger = logging.getLogger(__name__)
setupLog(logger)

# FUNCTIONS
# Settings for opening a connection to the MariaDB database for logging data
def open_log_conn():
    try:
        conn = mariadb.connect(
            user="greenhouse_logger",
            password="lumbernotlogs",
            host="localhost",
            port=3306)
    except:
        logger.exception('Failed to connect to MariaDB as logger')
    return conn


# Settings for opening a connection to the MariDB data base for reading data
def open_view_conn():
    try:
        conn = mariadb.connect(
            user="greenhouse_viewer",
            password="showmethatdata",
            host="localhost",
            port=3306)
        return conn
    except:
        logger.exception('Failed to connect to MariaDB as viewer')


# Write parsed sensor data to database
def log_data_db(parsed_data):
    fields = ''
    values = ''
    # Split data into fields and values by comma delimiter
    for item in parsed_data:  # fix for non-operational temperature/humidity sensors
        keyValPair = item.split(',')
        if not keyValPair[1] == 'nan':  # return value from uninitialized temp/humid sensor
            fields += keyValPair[0]
            fields += ", "
            values += keyValPair[1]
            values += ", "

    # Log sensor values and fields into database
    conn = open_log_conn()
    cur = conn.cursor()
    try:
        cur.execute('INSERT INTO greenhouse.data ('
                    + fields + 'timestamp) VALUES ('
                    + values + '\''
                    + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '\')')
    except:
        logger.exception('Failed to log to database')
    conn.close()


# Read data from database, returns as dictionary
# Columns are sensors/outputs, rows are entries
def query_db(table, entries=1):
    conn = open_view_conn()
    cur = conn.cursor()

    try:
        cur.execute('SELECT * from greenhouse.' + table + ' ORDER BY timestamp DESC LIMIT ' + str(entries))
    except:
        logger.exception('Failed to get data from database')

    db_dict = {}
    db_data = []
    db_columns = []
    try:
        # Filtering results of query and creating a dictionary
        db_data = transpose(cur.fetchall())
        db_columns = [i[0] for i in cur.description]
        db_dict = {db_columns[i]: db_data[i] for i in range(len(db_columns))}
    except:
        logger.exception('Failed to create dictionary from query results')

    logger.debug('Dictionary: ' + str(db_dict))
    # logger.debug('descr: ' + str(cur.description))
    # logger.debug('db_data: ' + str(db_data))
    # logger.debug('db_columns: ' + str(db_columns))
    # logger.debug('len(db_columns): ' + str(len(db_columns)))

    conn.close()
    return db_dict


# Takes list/tuple of tuples and returns 2D list
# def db_data_to_list(db_tuples, entries=1):
#     db_lists = []
#     # Convert tuples into lists
#     try:
#         for i in range(0, entries):
#             db_lists.append(list(db_tuples[i]))
#     except:
#         logger.exception('Failed to convert tuples to lists')
#         logger.debug('List of tuples: ' + str(db_tuples))
#
#     # Convert all values from database from strings into integers
#     # for i in range(0, entries):
#     #     for j in range(0, len(db_lists[i])):
#     #         try:
#     #             if str.isdigit(db_lists[i][j]):  # Check if item can be converted to integer
#     #                 db_lists[i][j] = int(db_lists[i][j])
#     #         except:
#     #             logger.exception('Failed to convert item ' + str(i) + ',' + str(j) + ' to integer: ')
#     #             logger.debug('outputs: ' + str(db_lists))
#
#     return db_lists


# Write output states to database
def log_outputs_db(new_output_dict):
    # retrieve most recent output entry from database
    db_outputs = query_db('output')

    # Check for manual overrides in latest entry
    for key in new_output_dict:
        try:
            if db_outputs[key][0] > config.max_o_val():  # indicates manual override
                new_output_dict[key] = db_outputs[key][0]
        except:
            logger.exception('Failed to compare current and desired outputs')

    fields = ''
    values = ''
    try:
        for key, val in new_output_dict.items():
            logger.debug('key: ' + key)
            fields += key
            fields += ','
            values += str(val)
            values += ','
    except:
        logger.exception('Failed to create db write strings')

    # Write outputs to database
    conn = open_log_conn()
    cur = conn.cursor()

    try:
        cur.execute('INSERT INTO greenhouse.output ('
                    + fields + 'timestamp) VALUES ('
                    + values + '\''
                    + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '\')')
    except:
        logger.exception('Failed to write to database')

    conn.close()


# Returns a list of the fields for the database from a specified table
# def get_fields_db(table):
#     conn = open_view_conn()
#     cur = conn.cursor()
#
#     try:
#         cur.excecute("SHOW COLUMNS FROM greenhouse." + table)
#     except:
#         logger.exception('Failed to get data from database')
#
#     db_fields = cur.()
#     conn.close()
#
#     db_fields = []


# Transposes a 2d list/tuple and returns the result
def transpose(list_2d):
    return [[row[i] for row in list_2d] for i in range(len(list_2d[0]))]

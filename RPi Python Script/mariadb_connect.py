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
    except:
        logger.exception('Failed to connect to MariaDB as viewer')
    return conn


# Write parsed sensor data to database
def log_data_db(parsed_data):
    fields = ''
    values = ''
    # Split data into fields and values by comma delimiter
    for item in parsed_data:  # fix for non-operational temperature/humidity sensors
        keyValPair = item.split(',')
        if not keyValPair[1] == 'nan':
            fields += keyValPair[0]
            fields += ", "
            values += keyValPair[1]
            values += ", "
    # print('DEBUG: fields: ' + fields)
    # print('DEBUG: values: ' + values)

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


# Read sensor data from database, returns as double list of integers.
# Columns are sensors, rows are entries
def get_data_db(entries=1):
    conn = open_view_conn()
    cur = conn.cursor()

    try:
        cur.execute("SELECT * from greenhouse.data ORDER BY timestamp DESC LIMIT " + str(entries))
    except:
        logger.exception('Failed to get data from database')

    db_data = cur.fetchall()
    conn.close()

    return db_data_to_list(db_data, entries=entries)


# Read output states from database
def get_outputs_db(entries=1):
    conn = open_view_conn()
    cur = conn.cursor()

    try:
        cur.execute("SELECT * from greenhouse.output ORDER BY timestamp DESC LIMIT " + str(entries))
    except:
        logger.exception('Failed to get data from database')

    db_outputs = cur.fetchall()
    print("DEBUG: Current database outputs: ")
    print(db_outputs)
    conn.close()

    return db_data_to_list(db_outputs, entries=entries)


# Takes list of tuples and return 2D list of integers (excepting timestamp)
def db_data_to_list(db_tuples, entries):
    db_lists = []
    # Convert tuples into lists
    try:
        for i in range(0, entries):
            db_lists[i] = list(db_tuples[i])
    except:
        logger.exception('Failed to convert tuples to lists')
    # Convert all values from database from strings into integers
    for i in range(0, entries):
        try:
            for j in range(0, len(db_lists[i]) - 1):  # last value in row is timestamp
                db_lists[i][j] = int(db_lists[i][j])
        except:
            logger.exception('Failed to convert output' + str(i) + ' to integer: ' + str(error))


# Write output states to database
def log_outputs_db(output_vals):
    # retrieve most recent output entry from database
    db_outputs = (get_outputs_db())[0]

    # Check for manual overrides in latest entry
    try:
        for i in range(0, len(db_outputs)):
            if db_outputs[i] > config.max_o_val():  # indicates manual override
                output_vals[i] = db_outputs
    except:
        logger.exception('Failed to compare current and desired outputs')

    # Write outputs to database
    conn = open_log_conn()
    cur = conn.cursor()

    try:
        cur.execute('INSERT INTO greenhouse.output ('
                    + config.o_fields() + 'timestamp) VALUES ('
                    + output_vals + '\''
                    + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '\')')
    except:
        logger.exception('Failed to write to database')

    conn.close()


# Returns a list of the fields for the database from a specified table
def get_fields_db(table):
    conn = open_view_conn()
    cur = conn.cursor()

    try:
        cur.excecute("SHOW COLUMNS FROM greenhouse." + table)
    except:
        logger.exception('Failed to get data from database')

    db_table = cur.fetchall()
    conn.close()

    db_fields = []

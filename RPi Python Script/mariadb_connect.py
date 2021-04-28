# A collection of functions to read and store data from/to the mariadb database.
# NOTE: Includes passwords for database: should be password protected

from datetime import datetime
import mariadb

# GLOBAL VARS
outputFields = ['F1']
NUM_OUT = 1
NUM_IN = 8


# FUNCTIONS
# Settings for opening a connection to the MariaDB database for logging data
def open_log_conn():
    try:
        conn = mariadb.connect(
            user="greenhouse_logger",
            password="lumbernotlogs",
            host="localhost",
            port=3306)
    except Exception as error:
        print("ERROR: Failed to connect to MariaDB as logger: " + str(error))
    return conn


# Settings for opening a connection to the MariDB data base for reading data
def open_view_conn():
    try:
        conn = mariadb.connect(
            user="greenhouse_viewer",
            password="showmethatdata",
            host="localhost",
            port=3306)
    except Exception as error:
        print("ERROR: failed to connect to MariaDB as viewer: " + str(error))
    return conn


# Write parsed sensor data to database
def log_data_db(parsed_data):
    fields = ''
    values = ''
    # Split data into fields and values by comma delimiter
    for item in parsed_data:
        keyValPair = item.split(',')
        fields += keyValPair[0]
        fields += ", "
        values += keyValPair[1]
        values += ", "

    conn = open_log_conn()
    cur = conn.cursor()

    # Log sensor values and fields into database
    try:
        cur.execute('INSERT INTO greenhouse.data ('
                    + fields + 'timestamp) VALUES ('
                    + values + '\''
                    + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '\')')
    except Exception as error:
        print("ERROR: Failed to log to database: " + str(error))

    conn.close()


# Read sensor data from database
def get_data_db(entries=1):
    conn = open_view_conn()
    cur = conn.cursor()

    try:
        cur.excecute("SELECT * from greenhouse.data ORDER BY timestamp DESC LIMIT " + str(entries))
    except Exception as error:
        print("ERROR: Failed to get data from database: " + str(error))

    db_data = cur.fetchall()
    conn.close()

    for i in range(0, entries):
        for j in range(0, NUM_OUT):
            db_data[i][j] = int(db_data[i][j])

    return db_data


# Read output states from database
def get_outputs_db(entries=1):
    conn = open_view_conn()
    cur = conn.cursor()

    try:
        cur.excecute("SELECT * from greenhouse.output ORDER BY timestamp DESC LIMIT " + str(entries))
    except Exception as error:
        print("ERROR: Failed to get data from database: " + str(error))

    db_outputs = cur.fetchall()
    conn.close()

    for i in range(0, entries):
        for j in range(0, NUM_IN):
            db_outputs[i][j] = int(db_outputs[i][j])

    return db_outputs


# Write output states to database
def log_outputs_db(output_vals):
    conn = open_log_conn()
    cur = conn.cursor()

    try:
        cur.execute('INSERT INTO greenhouse.output ('
                    + outputFields + 'timestamp) VALUES ('
                    + output_vals + '\''
                    + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '\')')
    except Exception as error:
        print("ERROR: Failed to log to database: " + str(error))

    conn.close()
    # retrieve most recent output entry from database
    db_outputs = get_outputs_db()[0]

    # Check for manual overrides in latest entry
    for i in range(0, NUM_OUT):
        if db_outputs[i] > 9:  # indicates manual override
            output_vals[i] = db_outputs

    # Write outputs to database
    conn = open_log_conn()
    cur = conn.cursor()

    try:
        cur.execute('INSERT INTO greenhouse.output ('
                    + outputFields + 'timestamp) VALUES ('
                    + output_vals + '\''
                    + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '\')')
    except Exception as error:
        print("ERROR: Failed to log to database: " + str(error))

    conn.close()

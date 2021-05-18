# A wrapper class of Serial for communicating with the Arduino
# IMPORTS
from serial import Serial
from time import sleep
import config
import logging

# LOCAL MODULES
from logger_setup import setupLog

# LOGGING
logger = logging.getLogger(__name__)
setupLog(logger)


class ArduinoSerial(Serial):
    arduino = None
    port = None
    baud = None
    timeout_s = None

    # initialization
    def __init__(self):
        try:
            port = config.arduino_port()
            baud = config.arduino_baud()
            timeout_s = config.arduino_timeout()
            try:
                self.arduino = Serial(port=port,
                                      baudrate=baud,
                                      timeout=timeout_s)
            except:
                logger.exception('Failed to init Serial')
        except:
            logger.exception('Failed to get config params')

    def is_open(self):
        try:
            return self.arduino.is_open
        except:
            logger.exception('Failed to get status of Serial')

    def open(self):
        try:
            self.arduino.open()
            return True
        except:
            logger.exception('Failed to connect on ' + str(self.port))
            return False

    def close(self):
        try:
            self.arduino.close()
        except:
            logger.exception('Failed to close Serial')

    def read_line(self):
        try:
            return self.arduino.readline()
        except:
            logger.exception('Failed to read from Arduino')
            return ''

    def write(self, data):
        try:
            self.arduino.write(data.encode())
        except:
            logger.exception('Failed to write to Arduino')

    def get_data(self):
        self.write("log;")
        input_data = self.read_line()

        return input_data

    def reset(self):
        self.arduino.setDTR(False)
        sleep(1)
        # toss any data already received
        self.arduino.flushInput()
        self.arduino.setDTR(True)

    def set_outputs(self, output_fields, output_vals):
        num_outputs = len(output_vals)
        output_string = "stp;" + str(num_outputs)
        for i in range(0, num_outputs):
            output_string += (output_fields[i] + ","
                              + str(output_vals[i]) + ";")

        self.write(output_string)

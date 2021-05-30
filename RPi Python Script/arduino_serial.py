# A wrapper class of Serial for communicating with the Arduino
# IMPORTS
import serial
from serial import Serial
from time import sleep
import config
import logging
import sys

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

    # initialization, does not open serial since port is set to none
    def __init__(self):
        self.get_serial_params()
        try:
            self.arduino = Serial(port=None,
                                  baudrate=self.baud,
                                  timeout=self.timeout_s,
                                  write_timeout=self.timeout_s)
        except:
            logger.exception('Failed to create Serial')

    def is_open(self):
        try:
            return self.arduino.is_open
        except:
            logger.exception('Failed to get status of Serial')

    def get_serial_params(self):
        try:
            self.baud = config.arduino_baud()
            self.timeout_s = config.arduino_timeout()
        except:
            logger.exception('Failed to get serial config params')

    def open(self):
        try:
            self.port = config.arduino_port()
            self.arduino.port = self.port
            if not self.is_open():
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
        except KeyboardInterrupt:
            logger.info('Keyboard Interrupt, exiting program')
            sys.exit(0)
        except serial.SerialException:
            logger.exception('Could not read on ' + str(self.port) + ". Reconnecting")
            self.open()
        except:
            logger.exception('Failed to read from Arduino')
            return ''

    def write(self, data):
        try:
            self.arduino.write(data.encode())
        except serial.SerialException:
            logger.exception('Could not read on ' + str(self.port) + ". Reconnecting")
            self.open()
        except:
            logger.exception('Failed to write to Arduino')

    def get_data(self):
        logger.info('Attempting to log data')
        self.write("log;")

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

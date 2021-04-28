# A wrapper class of Serial for communicating with the Arduino
# IMPORTS
from serial import Serial
from time import sleep


class ArduinoSerial(Serial):
    arduino = None
    port = None
    baud = None
    timeout_s = None

    # initialization
    def __init__(self, port, baud, timeout_s):
        self.port = port
        self.baud = baud
        self.timeout_s = timeout_s
        self.arduino = Serial('/dev/' + port,
                              baudrate=baud,
                              timeout=timeout_s,
                              )

    def is_open(self):
        return self.arduino.is_open

    def open(self):
        try:
            self.arduino.open()
            return True
        except Exception as error:
            print("ERROR: Failed to connect on " + str(self.port) + ": " + str(error))
            return False

    def close(self):
        self.arduino.close()

    def read_line(self):
        try:
            return self.arduino.readline()
        except Exception as error:
            print("ERROR: Failed to read from arduino while awaiting data from Arduino: " + str(error))

    def write(self, data):
        try:
            self.arduino.write(data.encode())
        except Exception as error:
            print("ERROR: Failed to write to Arduino: " + str(error))

    def get_data(self):
        self.write("log;".encode())
        input_data = self.read_line()

        return input_data

    def reset(self):
        self.arduino.setDTR(False)
        sleep(1)
        # toss any data already received, see
        self.arduino.flushInput()
        self.arduino.setDTR(True)

    def set_outputs(self, output_fields, output_vals):
        num_outputs = len(output_vals)
        output_string = "stp;" + str(num_outputs)
        for i in range(0, num_outputs):
            output_string += (output_fields[i] + ","
                              + str(output_vals[i]) + ";")

        self.write(output_string.encode())

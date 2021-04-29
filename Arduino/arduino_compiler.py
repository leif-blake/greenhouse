# Compiles and uploads main.ino to the Arduino

# IMPORTS
import subprocess
from shutil import which
import csv

# Install the latest version of arduino-cli if it is not installed, assumes arduino avr core
if which('arduino-cli') is None:
    subprocess.run(['curl', '-fsSL', 'https://raw.githubusercontent.com/arduino/arduino-cli/master/install.sh', '|',
                    'sh'])
    subprocess.run(['arduino-cli', 'core', 'install', 'arduino:avr'])


# Capture the port of the arduino (takes first Arduino in list, assumes Arduino is connected)
boardList = subprocess.run(['arduino-cli', 'board', 'list'], capture_output=True)
boardListSplit = str(boardList).split('\\n')
print(boardListSplit)
port = boardListSplit[1].split(' ')[0]


# Read the configuration files into a dictionary, replace the port with the correct port, and write back to csv
with open('../config.csv', newline='') as configfile:
    reader = csv.reader(configfile, delimiter=',')
    config_dict = {}
    for row in reader:
        config_dict[row[0]] = row[1:]
    config_dict['arduinoPort'] = [port]
with open('../config.csv', 'w+', newline='') as configfile:
    writer = csv.writer(configfile, delimiter=',')
    for key in config_dict:
        writer.writerow([key] + config_dict[key])

# Compile main.ino and upload to board
# Assume Arduino Uno Board
subprocess.run(['arduino-cli', 'compile', '-b', 'arduino:avr:uno', '-v', 'main'])
subprocess.run(['arduino-cli', 'upload', '-b', 'arduino:avr:uno', '-p', port, 'main'])


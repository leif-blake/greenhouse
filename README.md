# greenhouse

As shown in "Arduni RPi Comms.pdf", the Arduino collects sensor data and controls the outputs of the system. The RPi log data to an internal MariaDB database, and calculates the desired outputs, which are then communicated to the Arduino. The RPi also runs a grafana server for data visualization.

# Current State of Project:
- Serial comms between RPi and Arduino for communicating reset, outputs, and data collection
- Database logging and reading
- Setting one output (fan) - Hardcoded
- Reading data from one sensor (humidity and temp). This should generalize very easily, only need to add fields into database

# TODO:
- Implement resets of Raspberry Pi and Arduino (timeouts)
- Implemement remaining outputs into "stp" - Should be easy to add to, perhaps through array. Easiest to set all outputs every time, also avoids confusion between RPi and Arduino as to which outputs are set
- Generalized function for setting outputs based on all available input data
- Manual Output Overrides

# Rpi Setup
The raspberry pi should be set up in headless mode, with a mariadb server as outlined in "mariaDBConnect.py". **Needs more details**

1. Install Raspbian Lite on a microSD card using RPi Imager (or other methods):
https://www.raspberrypi.org/software/
2. Add the file "ssh" (no extensions) to the boot partition of the microSD card
3. Insert the microSD card into the RPi and power on. Use ethernet to ssh into the RPi. You should now be able to set up wifi using the command raspi-config
4. Install mariadb, with users, passwords as outline in "mariaDBConnect.py": https://pimylifeup.com/raspberry-pi-mysql/
5. Setup mariadb to start at boot: https://mariadb.com/kb/en/systemd/
6. Install grafana server (ARMv7 for Debian) and set up to run on boot: https://grafana.com/docs/grafana/latest/installation/debian
7. Set up your python script to run in the background on boot: https://www.raspberrypi-spy.co.uk/2015/02/how-to-autorun-a-python-script-on-raspberry-pi-boot/
8. Optional: Install Arduino CLI to compile and run arduino code from RPi: https://www.arduino.cc/pro/cli https://arduino.github.io/arduino-cli/latest/installation/

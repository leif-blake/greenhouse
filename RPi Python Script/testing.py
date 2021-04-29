import csv

port = '/dev/ttyACM0'

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

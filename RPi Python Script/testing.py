import mariadbConnect as dbConn

ioIDs = {
	1:"T1",
	2:"T2",
	3:"T3",
	4:"T4",
	5:"M1",
	6:"M2",
	7:"M3",
	8:"M4",
	9:"F1"
}

rawData = "1,25;3,6;17,8"
keyVals = rawData.split(';')
print(keyVals)

names = ""
values = []
for item in keyVals:
	keyValPair = item.split(',')
	names += str(ioIDs.get(int(keyValPair[0])))
	names += ", "
	values.append(int(keyValPair[1]))
names = names[:-2]
values = tuple(values)

print(names)
print(values)


def log_data_db(data):
	names = ""
	values = []
	for item in data:
		keyValPair = item.split(',')
		names += str(ioIDs.get(int(keyValPair[0])))
		names += ", "
		values.append(int(keyValPair[1]))
	names = names[:-2]
	values = tuple(values)

	conn = dbConn.open_log_conn()
	cur = conn.cursor()
	
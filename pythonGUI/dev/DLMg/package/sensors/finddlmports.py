import serial


def dlmfindcomports():
    com1, com2 = "", ""
    successa = False
    successb = False
    successboth = False
    for comNum in range(0, 255):
        comname = "COM" + str(comNum)
        try:
            ser = serial.Serial(comname, timeout=0.01)
            try:
                for lineNum in range(0, 10):
                    dataline = ser.readline().decode().split(',')
                    if len(dataline) == 5:
                        sensorid = dataline[0]
                        if sensorid == "A" or sensorid == "B":
                            com1 = comname
                            successa = True
                        elif sensorid == "C" or sensorid == "D":
                            com2 = comname
                            successb = True
            finally:
                ser.close()
        except serial.SerialException:
            continue
    if successa and successb:
        successboth = True
    return [com1, com2, successboth]
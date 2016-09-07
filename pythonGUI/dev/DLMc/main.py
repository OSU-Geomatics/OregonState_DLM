import sys
import serial
import COMLogger
import time


def run(argv):
    # Parse Argument
    if len(argv) == 1:
        outputfilename = 'DLM_' + time.strftime('%Y%m%d-%H%M%S') + '.txt'
        com1, com2, success = dlmfindcomports()
    elif len(argv) == 2:
        outputfilename = argv[1]
        com1, com2, success = dlmfindcomports()
    elif len(argv) == 4:
        outputfilename = argv[1]
        com1 = argv[2]
        com2 = argv[3]
        success = True
    else:
        print("Wrong Number of Inputs")
        print("Option 0: DLMc.exe")
        print("Option 1: DLMc.exe test.txt")
        print("Option 2: DLMc.exe test.txt COM3 COM4")
        return 0

    baud1, baud2 = "921600", "921600"  # Baud rate for DLM using Teensy doesn't matter
    if success:
        COMLogger.run(["DLMc", outputfilename, com1, baud1, com2, baud2])
    else:
        print("ERROR: Could not detect DLM data on the COM ports")


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


if __name__ == '__main__':
    run(sys.argv)
    print("Success!")
    time.sleep(1)

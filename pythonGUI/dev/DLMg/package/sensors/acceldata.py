import serial
import threading
import time

# do data handling and plotting based on gui inputs
# 1) finish acceldata reader/writer handlers
# 2) develop plotwidget to handle pointers to variables
# 3) generate update functions

class acceldata4:
    def __init__(self, com1, com2):
        self.com1 = com1
        self.com2 = com2
        self.A = Accelerometer()
        self.B = Accelerometer()
        self.C = Accelerometer()
        self.D = Accelerometer()

    def startReaderThread(self, comport, flag):
        print("Starting Thread")
        com1thread = threading.Thread(target=readDLMcsv, args=(comport, self.A, self.B, self.C, self.D, flag))
        com1thread.daemon = True
        com1thread.start()
        print("Thread Started")

    def startWriterThread(self, filename, flag):
        print('temp')


def readDLMcsv(comport, AccelA, AccelB, AccelC, AccelD, flag):
    # Try to open the COM port
    try:
        baud = 100
        ser = serial.Serial(comport, baud) # Teensy doesnt care what Baud rate you put in
    except serial.SerialException:
        print("Unable to open COM port: " + comport)
        return

    ser.flushInput()

    # keep looping and reading serial data
    tailmessage = bytes(0)
    while True:
        if flag[0]:
            alldataline = ser.read(ser.inWaiting())
            parsedlines = alldataline.decode().split('\n')
            for line in parsedlines:
                dataline = line.split(',')
                if len(dataline) == 5:
                    ax = float(dataline[2])
                    ay = float(dataline[3])
                    az = float(dataline[4])
                    tot = (ax ** 2 + ay ** 2 + az ** 2) ** (1. / 2)
                    linetime = float(dataline[1]) / 1000
                    ID = dataline[0]

                    if ID == "A":
                        AccelA.append([linetime, ax, ay, az, tot])
                        AccelA.ID = "A"
                    elif ID == "B":
                        AccelB.append([linetime, ax, ay, az, tot])
                        AccelB.ID = "B"
                    elif ID == "C":
                        AccelC.append([linetime, ax, ay, az, tot])
                        AccelC.ID = "C"
                    elif ID == "D":
                        AccelD.append([linetime, ax, ay, az, tot])
                        AccelD.ID = "D"
                    elif ID == "c":
                        AccelC.append([linetime, ax, ay, az, tot])
                        AccelC.ID = "c"
                    elif ID == "d":
                        AccelD.append([linetime, ax, ay, az, tot])
                        AccelD.ID = "d"
                    else:
                        tailmessage = dataline
                        if tailmessage[0] != '':
                            print(tailmessage)
        else:
            time.sleep(.05)

class Accelerometer:
    def __init__(self):
        self.time = []
        self.x = []
        self.y = []
        self.z = []
        self.tot = []
        self.dataindex = 0
        self.saveindex = 0
        self.datalock = threading.Lock()
        self.ID = ""

    def append(self, newdata):
        self.datalock.acquire()
        self.time.append(newdata[0])
        self.x.append(newdata[1])
        self.y.append(newdata[2])
        self.z.append(newdata[3])
        self.tot.append(newdata[4])
        self.dataindex += 1
        self.datalock.release()

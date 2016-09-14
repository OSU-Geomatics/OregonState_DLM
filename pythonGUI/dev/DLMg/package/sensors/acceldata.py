import serial
import threading
import time
import random
import numpy as np

class acceldata4:
    def __init__(self, com1, com2):
        self.com1 = com1
        self.com2 = com2
        self.A = Accelerometer()
        self.B = Accelerometer()
        self.C = Accelerometer()
        self.D = Accelerometer()

    def startReaderThread(self, comport, flag):
        com1thread = threading.Thread(target=readDLMcsv, args=(comport, self.A, self.B, self.C, self.D, flag))
        com1thread.daemon = True
        com1thread.start()

    def writeData(self, filename):
        self.A.datalock.acquire()
        self.B.datalock.acquire()
        self.C.datalock.acquire()
        self.D.datalock.acquire()
        maxind = np.amax((self.A.dataindex, self.B.dataindex, self.C.dataindex, self.D.dataindex))
        f = open(filename, 'w')
        for i in range(0,maxind):
            self.writeIndData(f, self.A, i)
            self.writeIndData(f, self.B, i)
            self.writeIndData(f, self.C, i)
            self.writeIndData(f, self.D, i)

        f.close()
        self.A.datalock.release()
        self.B.datalock.release()
        self.C.datalock.release()
        self.D.datalock.release()

    def writeIndData(self, f, X, ind):
        if X.dataindex > ind:
            tmillis = X.time[ind] * 1000
            t = "%.0f" % tmillis
            x = "%.3f" % X.x[ind]
            y = "%.3f" % X.y[ind]
            z = "%.3f" % X.z[ind]
            tot = "%0.3f" % X.tot[ind]

            f.write(X.ID + "," + t + "," + x + "," + y + "," + z + "," + tot + "\n")

    def addDummyData(self):
        self.A.adddummy(10000)
        self.B.adddummy(10000)
        self.C.adddummy(10000)
        self.D.adddummy(10000)


def readDLMcsv(comport, AccelA, AccelB, AccelC, AccelD, flag):
    # Try to open the COM port
    try:
        baud = 100
        ser = serial.Serial(comport, baud)  # Teensy doesnt care what Baud rate you put in
    except serial.SerialException:
        print("Unable to open COM port: " + comport)
        return



    # keep looping and reading serial data
    tailmessage = bytes(0)
    usedtobe = False
    while True:
        if flag[0]:
            if not usedtobe:
                usedtobe = True
                AccelA.flush()
                AccelB.flush()
                AccelC.flush()
                AccelD.flush()
                ser.flushInput()
                ser.flush()

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
            usedtobe = False

class Accelerometer:
    def __init__(self):
        self.time = []
        self.x = []
        self.y = []
        self.z = []
        self.tot = []
        self.dataindex = 0
        self.saveindex = 0
        self.throwoutindex = 0
        self.datalock = threading.Lock()
        self.ID = ""
        self.nthrowout = 50

    def append(self, newdata):
        if self.throwoutindex > self.nthrowout:
            self.datalock.acquire()
            self.time.append(newdata[0])
            self.x.append(newdata[1])
            self.y.append(newdata[2])
            self.z.append(newdata[3])
            self.tot.append(newdata[4])
            self.dataindex += 1
            self.datalock.release()
        else:
            self.throwoutindex += 1

    def adddummy(self, N):
        for i in range(0,N):
            t = i
            x = random.random()
            y = random.random()
            z = random.random()
            tot = (x**2+y**2+z**2)**(1/2)
            self.append((t, x, y, z, tot))

    def flush(self):
        self.datalock.acquire()
        self.time = []
        self.x = []
        self.y = []
        self.z = []
        self.tot = []
        self.dataindex = 0
        self.saveindex = 0
        self.throwoutindex = 0
        self.datalock.release()

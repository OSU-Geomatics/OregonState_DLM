import serial
import threading

# do data handling and plotting based on gui inputs
# 1) finish acceldata reader/writer handlers
# 2) develop plotwidget to handle pointers to variables
# 3) generate update functions

class acceldata4:
    def __init__(self, com1, com2):
        preallocatesize = 60*60*100
        self.com1 = com1
        self.com2 = com2
        self.A = Accelerometer()
        self.B = Accelerometer()
        self.C = Accelerometer()
        self.D = Accelerometer()

    def startReaderThread(self, comport, flag):
        print('temp')

    def startWriterThread(self, filename, flag):
        print('temp')

class Accelerometer:
    def __init__(self):
        self.time = []
        self.x = []
        self.y = []
        self.z = []
        self.tot = []
        self.dataindex = 0
        self.saveindex = 0
        self.isPlotting = [False, False, False, True]
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

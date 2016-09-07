import sys
import serial
import threading
import time

def run(argv):
    # Parse arguments
    nargs = len(argv)
    div, mod = divmod(nargs, 2)
    if mod == 0 and div > 1:
        filename = argv[1]
        comports = []
        baudrates = []
        for iarg in range(2, nargs, 2):
            comports.append(argv[iarg])
            baudrates.append(int(argv[iarg+1]))
    else:
        print("Wrong Number of Inputs")
        print("Option 1: COMLogger.exe COM1 9600")
        print("Option 2: COMLogger.exe COM1 9600 COM2 9600 ... etc")

        return 0

    writeLock = threading.Lock()
    keepWriting = [True]
    allThreads = []
    f = open(filename, "w")
    print("Opened " + filename)
    initialthreadnum = threading.activeCount()
    for port, baud in zip(comports, baudrates):
        iThread = threading.Thread(target=writeSerial, args=(port, baud, f, writeLock, keepWriting))
        iThread.daemon = True
        iThread.start()
        allThreads.append(iThread)

    time.sleep(0.1)

    while keepWriting[0]:
        key = input('Press "Q", then "Enter" to end logging: ')
        if key == "Q" or key == "q":
            keepWriting[0] = False
            print("Received request to close file")

    print("Waiting for writing operations to finish")
    while initialthreadnum != threading.activeCount():
        print("Number of Threads Still Alive: " + str(threading.activeCount() - initialthreadnum))
        time.sleep(0.25)

    print("Closing File")
    f.close()


def writeSerial(comport, baudrate, filehandle, lock, keepwriting):
    # try to open serial port
    try:
        ser = serial.Serial(comport, baudrate)
        print("Opened  " + comport + " at " + str(baudrate) + " baud")
    except serial.SerialException:
        print("Unable to open " + comport + " at " + str(baudrate))
        return 0

    nbad = 0
    haswarned = False
    ser.flushInput()
    ser.flushOutput()
    ser.flush()
    while keepwriting[0]:
        # read data
        alldataline = ser.readline().decode()
        # write data
        lock.acquire()
        filehandle.write(alldataline[0:-2] + '\n')
        lock.release()
        nAvailable = ser.inWaiting()
        if nAvailable>5000:
            nbad += 1

        if nbad > 100 and not haswarned:
            print("WARNING, serial read on " + comport + "is not keeping up...may be losing data")
            print("Try restarting the program ")
            haswarned = True

    # close Serial port
    ser.close()
    print("Closed " + comport)
    return 1

if __name__ == '__main__':
    run(sys.argv)


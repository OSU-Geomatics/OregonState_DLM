import sys
import serial
import time

if len(sys.argv)==5:
    script, filename, comPort, baud, dt = sys.argv
else:
    print("Using Default Test Parameters")
    filename = "D:\Dropbox\OSU\DLM_Accelerometers\GUI\testdata\TestCOM3.log"
    comPort = "COM100"
    baud = 921600
    dt = 0.0025
print("Writing Text File to COM Port")
print(filename)
print("Opening COM PORT" + comPort)    
f = open(filename)
ser = serial.Serial(comPort, baud)
print("Writing Data At " + dt + " times per second")

for line in f:
    line2write = line + '\r'
    line2print = comPort + " : \"" + line[:-1] + "\""
    print(line2print.ljust(100), end='\r')
    ser.write(line2write.encode())
    time.sleep(float(dt))

close(serial)

#!/usr/bin/env python
import serial
import time

portPath = "/dev/ttyACM0"
baud = 38400

def createSerial(portPath, baud_rate):
    return serial.Serial(portPath, baud_rate)

def serialOutput(serial):
    data = serial.readline().decode('utf-8')
    data = data.strip()
    sep = data.split(",")
    #print(sep)
    return sep

def flushSerial(serial_port):
    #serial_port.setDTR(False)
    #time.sleep(1)
    serial_port.flushInput()
    serial_port.flushOutput()
    #time.sleep(1)
    #serial_port.setDTR(True)

serial_obj = createSerial(portPath, baud)
flushSerial(serial_obj)
while 1:
    #data = serialOutput(serial_obj)
    print(serial_obj.readline().decode('utf-8'))
    flushSerial(serial_obj)
    

#print(data[0])

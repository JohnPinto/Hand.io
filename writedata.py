#!/usr/bin/env python
import serial
from serial import tools
from serial.tools import list_ports
import time
import struct

baud = 115200

class SerialObject():
    port = None
    ser = None

    def __init__(self, baud):
        self.baud = baud
        
        self.__getPort()

        print("Serial port:", self.port)
        print("Baud:", baud)

        self.ser = serial.Serial(self.port, baud)
    
    def __getPort(self):
        serial.tools.list_ports.grep

        try:
            search = serial.tools.list_ports.grep(True)
            next(search)
        except Exception:
            port_list = serial.tools.list_ports.comports()
            for p in port_list:
                if 'arduino' in p.description.lower():
                    self.port = p.device
                    break
            else:
                    self.port = port_list[-1].device

    def __flushSerial(self):
        self.ser.flush()
        self.ser.reset_input_buffer()
        self.ser.reset_output_buffer()

    def serialOutputText(self):
        self.__flushSerial()
        data = self.ser.readline().decode("utf-8")

        if data[:3] == "a/g" and data[-1:] == "\n":
            print(data)

    def dumpOutputText(self):
        self.__flushSerial()
        print(self.ser.readline().decode("utf-8"))
    
    def serialOutputBin(self):
        self.__flushSerial()
        data = self.ser.readline()

        if data[:1] == b"$" and data[-1:] == b"\n":
            #data[]
            print(data)

    def dumpOutputBin(self):
        self.__flushSerial()
        print(self.ser.readline())

def main():
    ser = SerialObject(baud)

    while 1:
        #ser.dumpOutputText()
        #ser.serialOutputText()
        ser.serialOutputBin()
        #ser.dumpOutputBin()

if __name__ == '__main__':
    main()


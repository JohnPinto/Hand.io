#!/usr/bin/env python
import time
import struct

import serial
from serial import tools
from serial.tools import list_ports

import pandas as pd
from sklearn import model_selection
from sklearn import metrics
from sklearn.neighbors import KNeighborsClassifier

baud = 115200
algorithm = "knn"
dataset_path = "handio_data.csv"

class Classifier():
    result = None
    algorithm = None
    dataset = None
    clf = None
    dataset_x = None
    dataset_y = None

    def __init__(self, dataset, algorithm):
        self.algorithm = algorithm

        self.dataset = pd.read_csv(dataset, header=None)

        self.dataset_x = self.dataset.values[:, 1:7]
        self.dataset_y = self.dataset.values[:, 0]

        if self.algorithm == "knn":
            self.clf = KNeighborsClassifier(n_neighbors=4).fit(self.dataset_x,self.dataset_y)

    def classify(self,data):
        self.result = self.clf.predict(pd.DataFrame(data).T)
        print(self.result)

      
class SerialObject():
    port = None
    ser = None
    data = None

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

    def getData(self):
        return self.data

    def updateData(self):
        self.data = self.checkedOutputText()

    def showData(self):
        print(self.data)
    

    def checkedOutputText(self):
        self.__flushSerial()
        data = self.ser.readline().decode("utf-8")

        if data[:1] == "$" and data[-1:] == "\n":
            sensor_data = data.split("\t")[1:-1]
            return (sensor_data)

    def dumpOutputText(self):
        self.__flushSerial()
        print(self.ser.readline().decode("utf-8"))
    
    def checkedOutputBin(self):
        self.__flushSerial()
        data = self.ser.readline()

        if data[:1] == b"$" and data[-1:] == b"\n":
            print(data)

    def dumpOutputBin(self):
        self.__flushSerial()
        print(self.ser.readline())

    def serialClose(self):
        self.ser.close()

def main():
    ser = SerialObject(baud)
    clf = Classifier(dataset_path, algorithm)

    while 1:
        try:
            ser.updateData()
            ser.showData()
        except:
            ser.serialClose()
            clf.classify(ser.getData())
            print("\n",pd.DataFrame(ser.getData()).T)
            print("keyboard interrupt")
            break

if __name__ == '__main__':
    main()


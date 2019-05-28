#!/usr/bin/env python
import time
import struct
import json

import serial
from serial import tools
from serial.tools import list_ports

import pandas as pd
from sklearn import model_selection
from sklearn import metrics
from sklearn.neighbors import KNeighborsClassifier

baud = 115200
algorithm = "knn"
dataset_path = "dataset.csv"
commands_path = "command.json"

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
    data = ".\n"

    def __init__(self, baud):
        self.baud = baud
        
        self.__getPort()

        print("Serial port:", self.port)
        print("Baud:", baud)

        self.ser = serial.Serial(self.port, baud, timeout=0.5)
    
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
        data = self.checkedOutput()

        if data == None:
            return
            
        self.data = data
        

    def showData(self):
        print(self.data)
    

    def checkedOutput(self):
        self.__flushSerial()
        
        data = self.ser.readline().decode("utf-8")

        if data[:1] == "$" and data[-1:] == "\n":
            sensor_data = data.split("\t")[1:-1]
            return (sensor_data)
        elif data[:1] == ".":
            print ("No")

    def dumpOutput(self):
        self.__flushSerial()
        print(self.ser.readline().decode("utf-8"))

    def serialClose(self):
        self.ser.close()
        
class HandIO():
    sensor = None
    actuator =  None
    classifier = None
    command = None

    def __init__(self, serial, classifier, commands):
        self.sensor = serial
        self.classifier = classifier
        self.__loadJson(commands)

    def init(self):
        while 1:
            try:
                print(self.sensor.checkedOutput())
            except:
                print("Keyboard Interrupt")
                break
            
    def __loadJson(self, file_path):
        with open(file_path, "r") as json_file:
            self.command = json.load(json_file)
        
    def chooseDevice(self):
        print("coiso")

    def chooseAction(self):
        print("coiso")

    def soundSignal(self):
        print("OK")

def main():
    ser = SerialObject(baud)
    clf = Classifier(dataset_path, algorithm)
    hio = HandIO(ser, clf, commands_path)
    
    hio.init()

if __name__ == '__main__':
    main()


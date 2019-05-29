#!/usr/bin/env python
import time
import struct
import json

from pygame import mixer

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
commands_path = "commands.json"
sounds_path = "sounds.json"

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
        return(self.result)

      
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

    def dump(self):
        self.__flushSerial()
        return(self.ser.readline().decode("utf-8"))

    def serialClose(self):
        self.ser.close()
        
class HandIO():
    sensor = None
    actuator =  None
    classifier = None
    commands = None
    data = None
    state = 0
    device = None
    action = None
    sounds = None
    mixer = mixer

    def __init__(self, serial, classifier, commands, sounds):
        self.sensor = serial
        self.classifier = classifier
        self.__loadCommands(commands)
        self.__loadSounds(sounds)
        self.mixer.init()

    def init(self):
        while 1:
            try:
                self.__waitSignal()
                self.__chooseDevice(self.__classify())
                self.__soundSignal()
                self.__waitSignal()
                self.__chooseAction(self.__classify())
                self.__soundSignal()
                self.__cleanSelection()
            except:
                print("Keyboard Interrupt")
                self.sensor.serialClose()
                break
            
    def __loadCommands(self, file_path):
        with open(file_path, "r") as json_file:
            self.commands = json.load(json_file)
        json_file.close()

    def __loadSounds(self, file_path):
        with open(file_path, "r") as json_file:
            self.sounds = json.load(json_file)
        json_file.close()

    def __waitSignal(self):
        while self.__processSerial(self.sensor.dump()) == ".":
            continue
        else:
            while self.__processSerial(self.sensor.dump()) != ".":
                continue

    def __classify(self):
        if self.data is not None:
            return self.classifier.classify(self.data)
        else:
            return ("Unable to classify due to lack of data")

    def __processSerial(self, data):
        if data[:1] == "$" and data[-1:] == "\n":
            sensor_data = data.split("\t")[1:-1]
            self.data = sensor_data
            return sensor_data
        elif data[:1] == ".":
            return "."
        
    def __chooseDevice(self, result):
        if result == "u" or result == "d":
            self.device = self.commands[result[0]]
            print(self.device)
        else:
            print("Unknown device")


    def __chooseAction(self, result):
        if result == "u" or result == "d":
            self.action = self.commands[self.device][result[0]]
            print (self.action)
        else:
            print("Unknown command")

    def __soundSignal(self):
        if self.device == "tv" and self.action is None:
            self.__loadAndPlay(self.sounds[self.device])
        elif self.device == "ac" and self.action is None:
            self.__loadAndPlay(self.sounds[self.device])
        if self.device == "ac" and self.action == "ac_on":
            self.__loadAndPlay(self.sounds[self.action])
        elif self.device == "ac" and self.action == "ac_off":
            self.__loadAndPlay(self.sounds[self.action])
        if self.device == "tv" and self.action == "tv_on":
            self.__loadAndPlay(self.sounds[self.action])
        elif self.device == "tv" and self.action == "tv_off":
            self.__loadAndPlay(self.sounds[self.action])

    def __loadAndPlay(self, file):
        self.mixer.music.load(file)
        self.mixer.music.play()
    
    def __cleanSelection(self):
        self.device = None
        self.action = None


def main():
    ser = SerialObject(baud)
    clf = Classifier(dataset_path, algorithm)
    time.sleep(1)
    hio = HandIO(ser, clf, commands_path, sounds_path)
    
    hio.init()

if __name__ == '__main__':
    main()


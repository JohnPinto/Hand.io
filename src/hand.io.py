#!/usr/bin/env python
import time
import struct
import json

from pygame import mixer as mx

from classifier import Classifier

from in_out import Sensor, Actuator


class HandIO():
    __sensor = None
    __actuator =  None
    __classifier = None
    __commands = None
    __data = None
    __state = 0
    __device = None
    __action = None
    __sounds = None
    __mixer = mx
    __ircodes = None

    def __init__(self, sensor, actuator, classifier, commands = "../json/commands.json", 
                                                     sounds   = "../json/sounds.json", 
                                                     ircodes  = "../json/ircodes.json"):
        self.__sensor = sensor
        self.__actuator = actuator
        self.__classifier = classifier
        self.__loadCommands(commands)
        self.__loadSounds(sounds)
        self.__loadIRCodes(ircodes)
        self.__mixer.init()

    def init(self):
        while 1:
            try:
                print("Choose a device")
                self.__waitSignal()

                if self.__chooseDevice(self.__classify()) == False:
                    self.__cleanSelection()
                    continue
                
                self.__soundSignal()

                print("Choose an Action")
                self.__waitSignal()

                if self.__chooseAction(self.__classify()) == False:
                    self.__cleanSelection()
                    continue

                self.__soundSignal()

                self.__cleanSelection()
            except:
                print("Keyboard Interrupt")
                self.__sensor.serialClose()
                break

    def record(self, command):
        while 1:
            try:
                self.__waitSignal()
            except:
                print("Keyboard Interrupt")
                self.__sensor.serialClose()
                break

            
    def __loadCommands(self, file_path):
        with open(file_path, "r") as json_file:
            self.__commands = json.load(json_file)
        json_file.close()

    def __loadSounds(self, file_path):
        with open(file_path, "r") as json_file:
            self.__sounds = json.load(json_file)
        json_file.close()

    def __loadIRCodes(self, file_path):
        with open(file_path, "r") as json_file:
            self.__ircodes = json.load(json_file)
        json_file.close()


    #TODO Melhorar essa parte do código
    def __waitSignal(self):
        while self.__processSerial(self.__sensor.read()) == ".":
            continue
        else:
            while self.__processSerial(self.__sensor.read()) != ".":
                continue

    def __classify(self):
        if self.__data is not None:
            return self.__classifier.classify(self.__data)
        else:
            return ("Unable to classify due to lack of data")

    def __processSerial(self, data):
        if data[:1] == "$" and data[-1:] == "\n":
            sensor_data = data.split("\t")[1:-1]
            self.__data = sensor_data
            return sensor_data
        else:
            return "."
        
    def __chooseDevice(self, result):
        if result in self.__commands:
            self.__device = self.__commands[result]
            print(self.__device)
            return True
        else:
            print(result)
            print("Unknown device")
            return False


    def __chooseAction(self, result):
        if result in self.__commands and self.__device is not None:
            self.__action = self.__commands[self.__device][result]
            print (self.__action)
            return True
        else:
            print(result)
            print("Unknown command")
            return False

    def __soundSignal(self):
        if self.__device is not None and self.__action is None:
            self.__loadAndPlay(self.__sounds[self.__device])
        elif self.__device is not None and self.__action is not None:
            self.__loadAndPlay(self.__sounds[self.__action])

    def __loadAndPlay(self, file):
        self.__mixer.music.load(file)
        self.__mixer.music.play()
    
    def __cleanSelection(self):
        self.__device = None
        self.__action = None

    def __sendCommand(self):
        return True


def main():
    sensor = Sensor()
    actuator = Actuator()
    clf = Classifier("knn")
    time.sleep(1)
    hio = HandIO(sensor, actuator, clf)
    
    hio.init()
    
if __name__ == '__main__':
    main()


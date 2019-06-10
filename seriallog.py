#!/usr/bin/env python
import serial
import threading
import csv
import re
import time
import io
import os

portPath = "/dev/ttyACM1"
baud = 38400
filename = "data.csv"
timeout = time.time() + 3
command = ""

def create_serial_obj(portPath, baud_rate):
    return serial.Serial(portPath, baud_rate)

def return_serial(serial):
    data = serial.readline().decode('utf-8')
    data = data.strip()
    sep = data.split(",")
    #print(sep)
    return sep

def refresh_serial(serial_port):
    #serial_port.setDTR(False)
    time.sleep(1)
    serial_port.flushInput()
    time.sleep(1)
    #serial_port.setDTR(True)


def csv_write(data, f_name):
    #data.insert(0,command)
    print(data)
    with open(f_name, "a", newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(data)

def read_serial(serial,filename):
    while 1:
        csv_write(return_serial(serial), filename)


serial_obj = create_serial_obj(portPath, baud)
refresh_serial(serial_obj)
#tr = threading.Thread(target=read_serial, args=(serial_obj, filename))
#tr.start()
while 1:
    #command = input("Entre com o comando")
    if (time.time() > timeout):
        break
    #tr.join()
    csv_write(return_serial(serial_obj), filename)

os.system("tail -n 1 data.csv > new_data.csv")


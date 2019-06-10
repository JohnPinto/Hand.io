import json
import serial
from serial import tools
from serial.tools import list_ports


class SerialObject():
    __port = None
    __serial = None
    __devices =  None

    def __init__(self, baud, device):
        self.baud = baud
        
        self.__loadDevices("../json/devices.json")

        self.__getPort(device)

        print("Serial port:", self.__port)
        print("Baud:", baud)

        self.__serial = serial.Serial(self.__port, baud)
    
    def __getPort(self, device):
        try:
            search = serial.tools.list_ports.grep(True)
            next(search)
        except Exception:
            port_list = serial.tools.list_ports.comports()
            for p in port_list:
                if self.__devices[device] in p.serial_number:
                    self.__port = p.device
                    break
            else:
                    self.__port = port_list[-1].device

    def __loadDevices(self, file_path):
        with open(file_path, "r") as json_file:
            self.__devices = json.load(json_file)
        json_file.close()

    def __flushSerial(self):
        self.__serial.flush()
        self.__serial.reset_input_buffer()
        self.__serial.reset_output_buffer()

    def read(self):
        self.__flushSerial()
        return(self.__serial.readline().decode("utf-8"))

    def serialClose(self):
        self.__serial.close()

    def send(self, data):
        self.__serial.write(data)

class Sensor(SerialObject):

    def __init__(self, baud = 115200, device = "sensor"):
        super().__init__(baud, device)

class Actuator(SerialObject):

    def __init__(self, baud = 57600, device = "actuator"):
        super().__init__(baud, device)
import json
import serial
from abc import ABC
from serial import tools
from serial.tools import list_ports


class SerialObject(ABC):
    _port = None
    _serial = None
    _devices =  None

    def __init__(self, baud, device):
        self.baud = baud
        
        self._loadDevices("json/devices.json")

        self._getPort(device)
    
        print("Serial port:", self._port)
        print("Baud:", baud)

        self._serial = serial.Serial(self._port, baud)
    
    def _getPort(self, device):
        try:
            search = serial.tools.list_ports.grep(True)
            next(search)
        except Exception:
            port_list = serial.tools.list_ports.comports()
            for p in port_list:
                if self._devices[device] in p.serial_number:
                    self._port = p.device
                    break
            else:
                    self._port = port_list[-1].device

    def _loadDevices(self, file_path):
        with open(file_path, "r") as json_file:
            self._devices = json.load(json_file)
        json_file.close()

    def _flushSerial(self):
        self._serial.flush()
        self._serial.reset_input_buffer()
        self._serial.reset_output_buffer()

    def serialClose(self):
        self._serial.close()
 
class Sensor(SerialObject):

    def __init__(self, baud = 115200, device = "sensor"):
        super().__init__(baud, device)
    
    def read(self):
        self._flushSerial()
        return(self._serial.readline().decode("utf-8"))

class Actuator(SerialObject):

    def __init__(self, baud = 57600, device = "actuator"):
        super().__init__(baud, device)

    def send(self, data):
        self._serial.write(data.encode())

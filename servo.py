import smbus
import time

class Servo:
    def __init__(self):
        self.bus = smbus.SMBus(1)

        self.address = 0x05

    def writeNumber(self, value):
        self.bus.write_byte(self.address, value)
        return -1

    def readNumber(self):
        number = self.bus.read_byte(self.address)
        return number

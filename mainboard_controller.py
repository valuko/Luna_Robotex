import serial
import time
from datetime import datetime

class MainboardController:
    port = "COM6"
    motor = ""
    # l+002r-112b+502

    fspeedbuf=0
    tspeedbuf=0

    def __init__(self):
        self.motor = serial.Serial(self.port, 9600, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE)
        self.motor.write('d50\n')
        time.sleep(3)
        self.motor.write('d150\n')
        time.sleep(0.5)
        self.motor.write('j\n')

    def circlearound(self, speed=150):
        self.motor.write('ca' + str(speed) + '\n')

    def forwardspeed(self, speed=150):
        self.fspeedbuf=speed

    def turnleft(self, speed=150):
        self.backwheel(speed)

    def turnright(self, speed=150):
        self.backwheel(-speed)

    def backwheel(self, speed=150):
        self.tspeedbuf = speed

    def sendwheelcommand(self):
        self.motor.write('f' + str(self.fspeedbuf).zfill(3)+'t'+str(self.tspeedbuf).zfill(3)+ '\n')

    def dribbler_on(self):
        self.currentturningspeed = 0

    def dribbler_init(self):
        self.motor.write('d50\n')

    def dribbler_on(self):
        self.motor.write('d150\n')


    def kick(self):
        self.stopwheels()
        time.sleep(1)
        self.motor.write('l\n')
        time.sleep(0.1)


    def checkforball(self):
        self.motor.write('i\n')
        line = self.motor.readline().strip()
        print(line)

    def stopwheels(self):
        self.fspeedbuf = 0
        self.tspeedbuf = 0
        self.sendwheelcommand()

    def stopall(self):
        self.fspeedbuf = 0
        self.tspeedbuf = 0
        self.sendwheelcommand()
        self.dribbler_init()

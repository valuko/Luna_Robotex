import serial

class MainboardController:
    port = "COM6"
    motor = ""
    # l+002r-112b+502

    def __init__(self):
        self.motor = serial.Serial(self.port, 9600, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE)
        self.currentforwardspeed = 0

    def circlearound(self, speed=150):
        self.motor.write('ca' + str(speed) + '\n')

    def forwardspeed(self, speed=150):
        self.motor.write('mf' + str(speed) + '\n')
        self.currentforwardspeed = speed

    def turnleft(self, speed=150):
        self.backwheel(speed)

    def turnright(self, speed=150):
        self.backwheel(-speed)

    def backwheel(self, speed=150):
        self.motor.write('t' + str(speed) + '\n')
        self.currentturningspeed = speed

    def dribbler_on(self):
        self.currentturningspeed = 0

    def dribbler_on(self):
        self.motor.write('d50\n')

    def charge_kicker(self):
        self.currentturningspeed = 0

    def kick(self):
        self.currentturningspeed = 0
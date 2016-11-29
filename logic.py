mainboard = ''


class Logic:
    def __init__(self, mainboard):
        self.mainboard = mainboard

    def movetoball(self, balldetails):
        self.mainboard.forwardspeed()
        if balldetails[0] > 340:
            self.mainboard.turnleft()
        elif balldetails[0] < 300:
            self.mainboard.turnright()
        elif (balldetails[0] > 300 and balldetails[0] < 340):
            self.mainboard.backwheel(0)

    def aimandshoot(self, goaldetails):
        self.mainboard.forwardspeed()
        if goaldetails[0] > 330:
            self.mainboard.turnleft()
        elif goaldetails[0] < 310:
            self.mainboard.turnright()
        elif (goaldetails[0] > 310 and goaldetails[0] < 330):
            self.mainboard.kick()

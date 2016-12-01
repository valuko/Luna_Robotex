mainboard = ''


class Logic:
    def __init__(self, mainboard):
        self.mainboard = mainboard

    def movetoball(self, balldetails):
        if balldetails==[0,0,0]:
            self.mainboard.circlearound()
        else:
            self.mainboard.forwardspeed()
            if balldetails[0] > 330:
                self.mainboard.turnleft()
            elif balldetails[0] < 310:
                self.mainboard.turnright()
            elif (balldetails[0] > 310 and balldetails[0] < 330):
                self.mainboard.backwheel(0)

    def aimandshoot(self, goaldetails):
        print (goaldetails)
        if goaldetails==[0, 0]:
            self.mainboard.circlearound()
        else:
            self.mainboard.forwardspeed()
            if goaldetails[0] > 325:
                self.mainboard.turnleft()
            elif goaldetails[0] < 315:
                self.mainboard.turnright()
            elif (goaldetails[0] > 315 and goaldetails[0] < 325):
                self.mainboard.kick()

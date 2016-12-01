mainboard = ''


class Logic:
    leftT = 350
    rightT = 290
    goalMin = 315
    goalMax = 325

    def __init__(self, mainboard):
        self.mainboard = mainboard

    def isBallFound(self, balldetails):
        return balldetails != [0, 0, 0]

    def movetoball(self, balldetails):
        if balldetails == [0,0,0]:
            self.mainboard.circlearound(speed=55)
        else:
            self.mainboard.forwardspeed()
            if balldetails[0] > self.leftT:
                self.mainboard.turnleft()
            elif balldetails[0] < self.rightT:
                self.mainboard.turnright()
            elif balldetails[0] >= self.rightT and balldetails[0] <= self.leftT:
                self.mainboard.backwheel(0)
                self.mainboard.forwardspeed()

    def aimandshoot(self, goaldetails):
        print (goaldetails)
        goal_scored = False
        if goaldetails == [0, 0]:
            self.mainboard.circlearound()
        else:
            self.mainboard.forwardspeed()
            if goaldetails[0] > self.goalMax:
                self.mainboard.turnleft()
            elif goaldetails[0] < self.goalMin:
                self.mainboard.turnright()
            elif (goaldetails[0] >= self.goalMin and goaldetails[0] <= self.goalMax):
                self.mainboard.kick()
                goal_scored = True
        return goal_scored

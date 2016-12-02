import cv2
import numpy as np
import ConfigParser
import imutils


class Detector:
    ballmin1 = 0
    ballmin2 = 0
    ballmin3 = 0
    ballmax1 = 0
    ballmax2 = 0
    ballmax3 = 0

    goalmin1 = 0
    goalmin2 = 0
    goalmin3 = 0
    goalmax1 = 0
    goalmax2 = 0
    goalmax3 = 0

    def __init__(self):
        config = ConfigParser.RawConfigParser()

        config.read('example.cfg')
        self.ballmin1 = config.getint('Ball', 'min1')
        self.ballmin2 = config.getint('Ball', 'min2')
        self.ballmin3 = config.getint('Ball', 'min3')
        self.ballmax1 = config.getint('Ball', 'max1')
        self.ballmax2 = config.getint('Ball', 'max2')
        self.ballmax3 = config.getint('Ball', 'max3')

        config.read('example.cfg')
        self.goalmin1 = config.getint('Goal', 'min1')
        self.goalmin2 = config.getint('Goal', 'min2')
        self.goalmin3 = config.getint('Goal', 'min3')
        self.goalmax1 = config.getint('Goal', 'max1')
        self.goalmax2 = config.getint('Goal', 'max2')
        self.goalmax3 = config.getint('Goal', 'max3')

    def ball_coordinates(self, frame):
        balldetails = [0, 0, 0]

        # Convert BGR to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        hsv = cv2.GaussianBlur(hsv, (11, 11), 0)

        # define range of orange color in HSV
        lower_ball = np.array([self.ballmin1, self.ballmin2, self.ballmin3])
        upper_ball = np.array([self.ballmax1, self.ballmax2, self.ballmax3])

        ballmask = cv2.inRange(hsv, lower_ball, upper_ball)
        ballmask = cv2.erode(ballmask, None, iterations=2)
        ballmask = cv2.dilate(ballmask, None, iterations=2)

        ballcontours = cv2.findContours(ballmask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

        if len(ballcontours) > 0:

            ballcontour = max(ballcontours, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(ballcontour)

            if radius > 5:
                # draw the circle and centroid on the frame,
                # then update the list of tracked points
                cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
                cv2.circle(frame, (int(x), int(y)), 5, (0, 0, 255), -1)
                balldetails = [x, y, radius]
        else:
            balldetails = [0, 0, 0]
        cv2.imshow('frame', frame)
        return balldetails

    def goal_coordinates(self, frame):
        # Convert BGR to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        #hsv = cv2.GaussianBlur(hsv, (11, 11), 0)
        kernel = np.ones((5, 5), np.uint8)

        # define range of orange color in HSV
        lower_goal = np.array([self.goalmin1, self.goalmin2, self.goalmin3])
        upper_goal = np.array([self.goalmax1, self.goalmax2, self.goalmax3])

        goalmask = cv2.inRange(hsv, lower_goal, upper_goal)
        #goalmask = cv2.erode(goalmask, None, iterations=2)
        #goalmask = cv2.dilate(goalmask, None, iterations=2)
        #goalcontours = cv2.findContours(goalmask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

        goalmask = cv2.erode(goalmask, kernel, iterations=2)
        goalmask = cv2.dilate(goalmask, kernel, iterations=2)
        goalcontours = cv2.findContours(goalmask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[-2]

        if len(goalcontours) > 0:
            # find the largest contour in the mask, then use
            # it to compute the minimum enclosing circle and
            # centroid
            c = max(goalcontours, key=cv2.contourArea)
            rect = cv2.minAreaRect(c)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            cv2.drawContours(frame, [box], 0, (0, 0, 255), 2)
            goaldetails = [rect[0][0], rect[0][1]]
        else:
            goaldetails = [0, 0]
        cv2.imshow('frame', frame)
        return goaldetails

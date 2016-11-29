import cv2
import time
from detector import Detector
from mainboard_controller import MainboardController
from logic import Logic

camera = cv2.VideoCapture(1)
detect = Detector()
mainboard = MainboardController()
logic = Logic(mainboard)
state = "movingtoball"
balldetails = ""
goaldetails = ""
seeingaball = False
ballindribler = False

# right - 0, left - 1, back - 2

# Possible states: movingtoball, aimandshoot

while True:
    (frameready, frame) = camera.read()

    if frameready:

        if state == "movingtoball":
            balldetails = detect.ball_coordinates(frame)

            # if balldetails != [0, 0, 0]:
            #     seeingaball = True
            # else:
            #     seeingaball = False

            logic.movetoball(balldetails)

        elif state == "aimandshoot":
            goaldetails = detect.goal_coordinates(frame)
            logic.aimandshoot(goaldetails)

        if (ballindribler):
            state = "aimandshoot"
        else:
            state = "movingtoball"

        mainboard.sendwheelcommand()
        print(state)

    keypress = cv2.waitKey(100) & 0xFF
    if keypress == 27:
        mainboard.stopall()
        camera.release()
        cv2.destroyAllWindows()
        break
    if keypress == 8:
        # mainboard.dribbler_init()
        # time.sleep(3)
        mainboard.checkforball()
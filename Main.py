import cv2
import time
from detector import Detector
from mainboard_controller import MainboardController
from logic import Logic

camera = cv2.VideoCapture(1)
detect = Detector()
mainboard = MainboardController()
logic = Logic(mainboard)
state = "initiating"
balldetails = ""
seeingaball = False


# right - 0, left - 1, back - 2

while True:
    (frameready, frame) = camera.read()
    if frameready:
        balldetails = detect.ball_coordinates(frame)

        if balldetails != [0, 0, 0]:
            seeingaball = True
        else:
            seeingaball = False
            print("Not seeing the ball")

        if ((state == "initiating" or state=="circlingaround") and seeingaball): state = "movingtoball"
        elif (state == "initiating" and seeingaball): state = "circlingaround"

        if state== "movingtoball":
            logic.movetoball(balldetails)


    keypress = cv2.waitKey(50) & 0xFF
    if keypress == 27:
        camera.release()
        cv2.destroyAllWindows()
        break
    if keypress == 8:
        mainboard.forwardspeed()
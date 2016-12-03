import cv2
import time
import threading
from detector import Detector
from mainboard_controller import MainboardController
from referee_controller import RefereeController
from logic import Logic

camera = cv2.VideoCapture(0)
detect = Detector()
mainboard = MainboardController()
logic = Logic(mainboard)
referee_controller = RefereeController()

# Define the states
STATE_BALL_NOT_FOUND = 'ballnotfound'
STATE_BALL_FOUND = 'ballfound'
STATE_GRAB_BALL = 'grabball'
STATE_BALL_GRABBED = 'ballgrabbed'
STATE_MOVE_TO_BALL = 'movetoball'
STATE_FIND_BALL = 'findball'
STATE_FIND_GOAL = 'findgoal'
STATE_GOAL_SCORED = 'goalscored'
STATE_BALL_LOST = 'balllost'

state = STATE_FIND_BALL
balldetails = ""
goaldetails = ""
seeingaball = False
ballindribler = False
ballclose = False
# right - 0, left - 1, back - 2
find_attempts = 0
fail_attempts = 0

# Take init actions here
mainboard.charge_kicker(5)
mainboard.dribbler_init()
#time.sleep(2)
#mainboard.charge_kicker()
#time.sleep(2)


# Start the referee module
td1 = threading.Thread(target=referee_controller.listen)
td1.start()

while True:
    if referee_controller.game_status():
        (frameready, frame) = camera.read()

        if not frameready:
            print "Frame not ready for reading"
        else:
            if state == STATE_FIND_BALL:
                #scan for ball
                balldetails = detect.ball_coordinates(frame)
                if logic.isBallFound(balldetails):
                    state = STATE_MOVE_TO_BALL
                    find_attempts = 0
                else:
                    # Perform further scans for the ball
                    find_attempts += 1

            if state == STATE_MOVE_TO_BALL:
                balldetails = detect.ball_coordinates(frame)
                if logic.isBallFound(balldetails):
                    fail_attempts = 0
                    logic.movetoball(balldetails)
                    if balldetails[1] > 450:
                        state = STATE_GRAB_BALL
                else:
                    fail_attempts += 1
                    print 'ball lost!'
                    if fail_attempts > 10:
                        # Ball lost state
                        state = STATE_BALL_LOST

            if state == STATE_GRAB_BALL:
                mainboard.dribbler_on()
                ballfound = mainboard.detect_ball_catch()
                ballindribler = True
                state = STATE_BALL_GRABBED

            if state == STATE_BALL_GRABBED:
                goaldetails = detect.goal_coordinates(frame)
                result = logic.turnandshoot(goaldetails)
                if result:
                    print "GOAL SCORED!!!"
                    state = STATE_GOAL_SCORED
                    mainboard.dribbler_shut_down()
                    time.sleep(1)
                    # Pause dribbler... or not, decide later
                    mainboard.pause_dribbler()
                    continue

            if state == STATE_BALL_LOST:
                mainboard.motor_shut_down()
                state = STATE_FIND_BALL

            print(state)

        keypress = cv2.waitKey(50) & 0xFF
        if keypress == 27:
            mainboard.motor_shut_down()
            mainboard.dribbler_shut_down()
            camera.release()
            cv2.destroyAllWindows()
            break


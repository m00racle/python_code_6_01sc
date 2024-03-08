"""  
Robot Brain and controllers
"""

# from soar.robot.pioneer import PioneerRobot
from robot_PioneerMod import PioneerMod
# import robot_spec as spec
from robot_spec import *
import robot_io as io
from math import pi
from soar.sim.geometry import Point
# set the the robot
robot = PioneerMod()


# specify the robot spec:
# put robot_spec and its init arguments
def SonarCondition(inp:tuple):
    """  
    function conditon for switch SM
    Given
        inp: tuple = remember inp here is the output of Paralle SM
        inp = (Point, io.InputSensor)
        thus it is not directly io.InputSensor
        NOTE: the io.InputSensor is inp[1]
    
    Return : boolean if condition met
    """
    sonar3 = inp[1].sonars[3]
    # if sonar3 is None means it out of bound > 1.5
    sonar3 = sonar3 if sonar3 != None else 1.5
    sonar4 = inp[1].sonars[4]
    # if sonar4 is None means it out of bound > 1.5
    sonar4 = sonar4 if sonar4 != None else 1.5
    return (sonar3 <= 0.5 or sonar4 <= 0.5)

robot_spec = Cascade(Parallel(GoalGenerator(robot, Point(12, -9)), Wire(robot)), Switch(SonarCondition, Brake(robot), DynamicMoveToPoint(robot)))
# brain options:
verbose_ = True
cheat_ = False



#  This function is called when the brain is loaded
def on_load():
    # set the robot initial behavior:
    robot.behavior = robot_spec

#  This function is called when the start button is pushed
def on_start():
    robot.behavior.start()

#  This function is called every step_duration seconds. By default, it is called 10 times/second
def on_step(step_duration):
    robot.behavior.step(io.SensorInput(robot, cheat=cheat_),verbose=verbose_).execute()

# This function is called when the stop button is pushed
def on_stop():
    pass

# This function is called when the robot's controller is shut down
def on_shutdown():
    pass

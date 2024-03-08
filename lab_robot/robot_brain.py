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
squarePoints = [Point(1.5, -3.0), Point(3.5, -1.0), Point(6.0, -3.5), Point(7.0, 0.0)]
robot_spec = Cascade(Parallel(FollowFigure(robot, squarePoints), Wire(robot)), DynamicMoveToPoint(robot))
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

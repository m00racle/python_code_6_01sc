"""  
Robot Brain and controllers
"""

# from soar.robot.pioneer import PioneerRobot
from robot_PioneerMod import PioneerMod
import robot_spec as spec
import robot_io as io
from math import pi

# specify the robot spec:
robot_spec = spec.RotateTSM2 #TODO: chage this to specify the robot.
# brai options:
verbose_ = True
cheat_ = False

# set the the robot
robot = PioneerMod()

#  This function is called when the brain is loaded
def on_load():
    # set the robot initial behavior:
    robot.behavior = robot_spec(robot, -2*pi)

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

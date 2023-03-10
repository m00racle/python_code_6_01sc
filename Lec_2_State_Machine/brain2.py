"""  
This is the brain template

At the moment we will use Pioneer robot since I don't have time to
inherit the BaseRobot class
"""

from soar.robot.pioneer import PioneerRobot
import robot_brains as rb
import math


# specified the RobotBrain SM:
robot_brain = rb.DesignLab2

robot = PioneerRobot()

#  This function is called when the brain is loaded
def on_load():
    robot.behavior = robot_brain(robot)
    robot.timer = 0
    
#  This function is called when the start button is pushed
def on_start():
    robot.behavior.start()

#  This function is called every step_duration seconds. By default, it is called 10 times/second
def on_step(step_duration):
    print(f'time: {robot.timer} seconds')
    print(f'robot pose: {robot.pose}')
    print(f'robot theta: {robot.pose[2]*180/math.pi} degree')
    robot.timer += step_duration
    robot.behavior.step(None, verbose=True).execute()


# This function is called when the stop button is pushed
def on_stop():
    pass


# This function is called when the robot's controller is shut down
def on_shutdown():
    pass
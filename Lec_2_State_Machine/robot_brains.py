"""  
This is the definition of robot behaviors
Should be used as part of the brain2.py

All robot brains here is sub class of SM
"""
import math
from state_machine import SM
# from soar.robot.pioneer import PioneerRobot
from soar.robot.base import BaseRobot

# helper functions:
def action(fvel: float = 0.0, rvel: float = 0.0)-> tuple:
    """  
    helper function (GLOBAL) to define the actions commands to the robot.
    """
    return (fvel, rvel)

class RobotBrain(SM):
    """  
    Robot Brain with ability to read odometry and sonar data
    """
    def __init__(self, robot: BaseRobot) -> None:
        self.robot = robot
        self.startState = 'start'

# SM for robot Design Lab2
class DesignLab2(RobotBrain):
    """  
    brain for Pioneer robot in Design lab 2
    """

    def getNextValues(self, state, inp, **kwargs) -> tuple:
        degree = self.robot.pose[2] * 180/math.pi
        print(f'robot rvel: {self.robot.rv}')
        if ((degree >= 90 and self.robot.rv >= 0)):
            return (self.robot.pose, action(rvel=-math.pi))
        else:
            return (self.robot.pose, action(rvel=math.pi))
"""  
This is the definition of robot behaviors
Should be used as part of the brain2.py

All robot brains here is sub class of SM
"""
import math
from state_machine import SM
from soar.robot.base import BaseRobot
import io601 as io

class RobotBrain(SM):
    """  
    Robot Brain with ability to read odometry and sonar data
    """
    def __init__(self, robot:BaseRobot) -> None:
        self.robot = robot
        self.startState = 'start'

# SM for robot Design Lab2
class DesignLab2(RobotBrain):
    """  
    brain for Pioneer robot in Design lab 2
    """

    def getNextValues(self, state, inp, **kwargs) -> tuple:
        return (None, io.Action(self.robot, fvel=1))
"""  
Try to mimick the lib601 io package
"""
from soar.robot.base import BaseRobot

class Action:
    """  
    given command to robot action
    """
    def __init__(self, robot:BaseRobot, fvel:float = 0.0, rvel:float = 0.0) -> None:
        self.fvel = fvel
        self.rvel = rvel
        self.robot = robot

    def execute(self):
        self.robot.rv = self.rvel
        self.robot.fv = self.fvel
    
    def __str__(self) -> str:
        return '<rv=' + str(float(self.rvel)) + ' rad/s; fv=' + str(float(self.fvel)) + ' m/s>'
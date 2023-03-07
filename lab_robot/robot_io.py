"""  
libraries for input and output of robot
NOTE: we use PioneerMod directly since the BaseRobot does not have sonar sensors
"""
# from soar.robot.pioneer import PioneerRobot
from robot_PioneerMod import PioneerMod

class Action:
    """  
    give command to robot action
    """
    def __init__(self, robot:PioneerMod, fvel:float = 0.0, rvel:float = 0.0) -> None:
        self.robot = robot
        self.fvel = fvel
        self.rvel = rvel
    
    def execute(self)->None:
        """  
        pass commands to the robot
        """
        self.robot.rv = self.rvel
        self.robot.fv = self.fvel

    def __str__(self) -> str:
        """  
        for verbose = True
        string outputs when the class instance is called
        """
        return '<rv=' + str(float(self.rvel)) + ' rad/s; fv=' + str(float(self.fvel)) + ' m/s>'

class SensorInput:
    """  
    enclose the sensor inputs
    odometry and sonars at this moment
    TODO: analog inputs?
    """

    def __init__(self, robot:PioneerMod, cheat=False) -> None:
        # self.robot = robot
        self.odometry = robot.pose if cheat else robot.odometry
        self.sonars = robot.sonars # sonars is a function NOT attribute of PioneerMod

    def __str__(self) -> str:
        return '< odometry= ' + str(self.odometry) + '; sonars= ' + str(self.sonars) + ' >'
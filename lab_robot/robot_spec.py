"""  
sub classes of RobotSM
different types of robot controller
this is describe what job the robot is intended to do.
"""

from robot_sm import RobotSM
import robot_io as io
from math import pi

# test robot just move forward.
class TestForward(RobotSM):
    def getNextValues(self, state, inp, **kwargs) -> tuple:
        return (None, io.Action(self.robot, fvel=1))

class TestRotateForward(RobotSM):
    def getNextValues(self, state, inp, **kwargs) -> tuple:
        return (None, io.Action(self.robot, rvel=-1, fvel=1))

class TestRotate(RobotSM):
    def getNextValues(self, state, inp, **kwargs) -> tuple:
        return (None, io.Action(self.robot, rvel=pi/2))
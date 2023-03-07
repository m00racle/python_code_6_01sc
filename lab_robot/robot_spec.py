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
        if self.done(state): return (self.robot.odometry.x, io.Action(self.robot, fvel=0.0))
        return (self.robot.odometry.x, io.Action(self.robot, fvel=1.0))
    
    def done(self, state) -> bool:
        if state == "start": return False
        if state >= 2 : return True
        return False


class TestRotateForward(RobotSM):
    def getNextValues(self, state, inp, **kwargs) -> tuple:
        return (None, io.Action(self.robot, rvel=-1, fvel=1))

class TestRotate(RobotSM):
    def getNextValues(self, state, inp, **kwargs) -> tuple:
        if self.done(state): return (self.robot.odometry.t, io.Action(self.robot, rvel=0))
        theta = self.robot.odometry.t
        return (theta, io.Action(self.robot, rvel=pi/2))
    
    def done(self, state) -> bool:
        if state == "start" : return False
        if state >= pi : return True
        return False
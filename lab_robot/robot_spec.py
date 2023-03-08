"""  
sub classes of RobotSM
different types of robot controller
this is describe what job the robot is intended to do.
"""

from robot_sm import RobotSM
import robot_io as io
from math import pi
from robot_PioneerMod import PioneerMod
from soar.sim.geometry import normalize_angle_180, normalize_angle_360

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

class RotateTSM(RobotSM):
    def __init__(self, robot: PioneerMod, deltaHeading:float, initVal='start') -> None:
        self.rotationalGain = 3.0
        self.angleEpsilon = 0.01
        self.distEpsilon = 0.01
        self.deltaHeading = deltaHeading
        super().__init__(robot, initVal)

    def getNextValues(self, state, inp:io.SensorInput, **kwargs) -> tuple:
        if self.done(state): return (state, io.Action(self.robot))
        currentTheta = inp.odometry.t
        if state == "start":
            # set the target theta
            thetaTarget = normalize_angle_180(currentTheta + self.deltaHeading)
        else:
            (thetaTarget, thetaLast) = state
        newState = (thetaTarget, currentTheta)
        action = io.Action(self.robot, rvel= self.rotationalGain * normalize_angle_180(thetaTarget - currentTheta))
        return (newState, action)

    def done(self, state) -> bool:
        if state == 'start':
            return False
        else:
            (thetaTarget, thetaLast) = state
            return self.robot.odometry.is_near((self.robot.odometry.x, self.robot.odometry.y, thetaTarget),\
                self.distEpsilon, self.angleEpsilon)

class RotateTSM2(RotateTSM):
    """  
    TODO: 
    Change this machine so that it rotates through an angle,
    so you could give it 2 pi or minus 2 pi to have it rotate all the way around
    """
    def getNextValues(self, state, inp: io.SensorInput, **kwargs) -> tuple:
        if self.done(state): return (state, io.Action(self.robot))
        currentTheta = inp.odometry.t
        if state == "start":
            # set the target theta
            thetaTarget = (currentTheta + self.deltaHeading)
        else:
            (thetaTarget, thetaLast) = state
        newState = (thetaTarget, currentTheta)
        action = io.Action(self.robot, rvel= self.rotationalGain * (thetaTarget - currentTheta))
        return (newState, action)

    def done(self, state) -> bool:
        if state == 'start':
            return False
        else:
            (thetaTarget, thetaLast) = state
            # return self.robot.odometry.is_near((self.robot.odometry.x, self.robot.odometry.y, thetaTarget),\
            #     self.distEpsilon, self.angleEpsilon)
            return abs(thetaTarget - thetaLast) < self.angleEpsilon
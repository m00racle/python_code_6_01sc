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
        return (self.robot.pose, io.Action(self.robot, fvel=1.0))

class TestRotateForward(RobotSM):
    def getNextValues(self, state, inp, **kwargs) -> tuple:
        return (self.robot.pose, io.Action(self.robot, rvel=-1, fvel=1))

class TestRotate(RobotSM):
    def __init__(self, robot: PioneerMod, speed:float, initVal='start') -> None:
        self.speed = speed
        super().__init__(robot, initVal)

    def getNextValues(self, state, inp, **kwargs) -> tuple:
        if self.done(state): return (self.robot.odometry.t, io.Action(self.robot, rvel=0))
        theta = self.robot.odometry.t
        return (self.robot.pose, io.Action(self.robot, rvel=self.speed))

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

class RotateTSM3(RotateTSM):
    """  
    Using nudge principle and norm 360 to create full rotate.
    """
    def getNextValues(self, state, inp: io.SensorInput, **kwargs) -> tuple:
        if self.done(state): return (state, io.Action(self.robot))
        currentTheta = inp.odometry.t
        if state == "start":
            thetaTarget = normalize_angle_180(currentTheta + self.deltaHeading)
            if abs(thetaTarget) < self.angleEpsilon :
                # nudge it
                print('nudge')
                if self.deltaHeading < 0:
                    thetaTarget = normalize_angle_180(thetaTarget + self.angleEpsilon)
                else:
                    thetaTarget = normalize_angle_180(thetaTarget - self.angleEpsilon)
            print(f'normalized theta target: {thetaTarget}')
        else:
            (thetaTarget, thetaLast) = state
        newState = (thetaTarget, currentTheta)
        # determine speed:
        # speed is depending on which way the self.headingdelta is:
        speed = (normalize_angle_180(thetaTarget - currentTheta))
        if self.deltaHeading > 0 and speed < 0:
            speed = -speed
        if self.deltaHeading < 0 and speed > 0:
            speed = -speed
        action = io.Action(self.robot, rvel= self.rotationalGain * speed)
        return (newState, action)

class ForwardTSM(RobotSM):
    """  
    Robot SM for forward to specific distance 
    The measurement here in distance based.
    """
    def __init__(self, robot: PioneerMod, delta:float, initVal='start') -> None:
        self.forwardGain = 1.0
        self.distTargetEpsilon = 0.01
        self.deltaDesired = delta
        super().__init__(robot, initVal)

    def getNextValues(self, state, inp: io.SensorInput, **kwargs) -> tuple:
        # if done robot stays put: (waiting for the next command)
        if self.done(state): return (state, io.Action(self.robot))
        # get current x,y coordinate position:
        currentPos = inp.odometry.point()
        if state == 'start':
            print(f'Starting forward {self.deltaDesired}')
            startPos = currentPos
        else:
            (startPos, lastPos) = state
        newState = (startPos, currentPos)
        diff = self.deltaDesired - startPos.distance(currentPos)
        velocity = self.forwardGain * diff
        action = io.Action(self.robot, fvel=velocity)
        return (newState, action)

    def done(self, state) -> bool:
        if state == 'start':
            return False
        else:
            starPos, lastPos = state
            return abs(self.deltaDesired - starPos.distance(lastPos)) < self.distTargetEpsilon
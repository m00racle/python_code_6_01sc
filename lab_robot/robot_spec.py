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

class XYDriver(RobotSM):
    """  
    set movement by Sensor inputs and goal points
    """
    def __init__(self, robot: PioneerMod, initVal='start') -> None:
        self.robot = robot
        self.forwardGain = 2.0
        self.rotationGain = 2.0
        self.angleEps = 0.05
        self.distEps = 0.02
        self.startState = False
    
    def getNextValues(self, state, inp, **kwargs) -> tuple:
        (goalPoint, sensors) = inp
        robotPose = sensors.odometry
        # remember odometry is now Pose type:
        robotPoint = robotPose.point()
        # we can call the point to return Point(x, y) of the Robot.
        # also we get to access the Point.angle_to function from Pose
        robotTheta = robotPose.t

        if goalPoint == None:
            return (True, io.Action(self.robot))
        
        # set the heading to the intended point
        headingTheta = robotPoint.angle_to(goalPoint)
        
        # rotate the robot to the goalPoint
        if abs(normalize_angle_180(headingTheta - robotTheta)) > self.angleEps:
            return (False, io.Action(self.robot, rvel=self.rotationGain * normalize_angle_180(headingTheta - robotTheta)))
        # then move toward the goal point:
        r = robotPoint.distance(goalPoint)
        if r > self.distEps:
            # moving toward the goal point:
            return (False, io.Action(self.robot, fvel=self.forwardGain * r))
        # oher than both then we will just stop
        return (True, io.Action(self.robot))

    def done(self, state) -> bool:
        return state

class SpyroGyra(RobotSM):
    """  
    The class intended working with XYDriver class to create spiral running robot
    """
    def __init__(self, robot: PioneerMod, incr:float, initVal='start') -> None:
        self.robot = robot
        self.distEps = 0.02
        self.incr = incr
        self.startState = ('east', 0, None)

    def getNextValues(self, state, inp: io.SensorInput, **kwargs) -> tuple:
        (direction, length, subGoal) = state
        robotPose = inp.odometry
        robotPoint = robotPose.point()
        
        if subGoal == None :
            subGoal = robotPoint
        
        if robotPoint.is_near(subGoal, self.distEps):
            # change the stte
            length = length + self.incr
            
            if direction == 'east':
                direction = 'north'
                subGoal.y += length
            elif direction == 'north':
                direction = 'west'
                subGoal.x -= length
            elif direction == 'west':
                direction = 'south'
                subGoal.y -= length
            else: # south
                direction = 'east'
                subGoal.x += length
            print(f'new: {direction}, {length}, {subGoal}')
        
        return ((direction, length, subGoal), (subGoal, inp))

class Cascade(RobotSM):
    """  
    Cascade class similar to the SM but for robot
    """
    def __init__(self, m1 : RobotSM, m2: RobotSM) -> None:
        self.m1 = m1
        self.m2 = m2
        self.log = {}
        self.startState = (m1.startState, m2.startState)

    def getNextValues(self, state, inp, **kwargs) -> tuple:
        (s1, s2) = state
        (next_s1, o1) = self.m1.getNextValues(s1, inp)
        (next_s2, o2) = self.m2.getNextValues(s2, o1)
        return ((next_s1, next_s2), o2)
    
class Parallel(RobotSM):
    """  
    Parallel class for Robot
    """
    def __init__(self, m1: RobotSM, m2: RobotSM) -> None:
        """  
        initialize:
        m1 : RobotSM = robot state machine
        m2 : RobotSM = robot state machine
        """
        self.m1 = m1
        self.m2 = m2
        self.startState = (m1.startState, m2.startState)

    def getNextValues(self, state, inp, **kwargs) -> tuple:
        """  
        Parallel settings -> see https://github.com/m00racle/python_code_6_01sc/blob/b8e20b14023a533bfcb68faaa3645150ad644933/Lec_2_State_Machine/parallel.py#L31

        Return: tuple = next states and outputs
        """
        (s1, s2) = state
        (next_s1, o1) = self.m1.getNextValues(s1, inp)
        (next_s2, o2) = self.m2.getNextValues(s2, inp)
        return ((next_s1, next_s2), (o1, o2))
    
class Constant(RobotSM):
    """  
    Equivalent for class Fixed in SM -> see https://github.com/m00racle/python_code_6_01sc/blob/b8e20b14023a533bfcb68faaa3645150ad644933/Lec_2_State_Machine/state_machine.py#L455

    but this one is for robot
    """
    def __init__(self, robot: PioneerMod, k, initVal='start') -> None:
        super().__init__(robot, initVal)
        # NOTE: k here is constant can be anything including Point object
        self.k = k
    
    def getNextValues(self, state, inp: io.SensorInput, **kwargs) -> tuple:
        """  
        always return state and constant -> see https://github.com/m00racle/python_code_6_01sc/blob/b8e20b14023a533bfcb68faaa3645150ad644933/Lec_2_State_Machine/state_machine.py#L466

        """
        return (state, self.k)
    
class Wire(RobotSM):
    """  
    Equivalent to SM Wire -> see https://github.com/m00racle/python_code_6_01sc/blob/b8e20b14023a533bfcb68faaa3645150ad644933/Lec_2_State_Machine/state_machine.py#L441
    but for robot
    """
    def getNextValues(self, state, inp: io.SensorInput, **kwargs) -> tuple:
        """  
        output always satate and input
        """
        return (state, inp)
    
class FollowBound(RobotSM):
    """  
    Design lab 2: Controlling Robots
    4. Following Boundaries
    -- when there is nothing nearby, move forward
    -- as soon as it reaches obstacles in front i should follow the boundary
    ROBOT MUST BE between 0.3 to 0.5 from the side.
    """
    def getNextValues(self, state, inp: io.SensorInput, **kwargs) -> tuple:
        curState = state
        sonar3 = inp.sonars[3]
        sonar4 = inp.sonars[4]
        sonar3 = sonar3 if sonar3 != None else 1.5
        sonar4 = sonar4 if sonar4 != None else 1.5
        avgSonar = (sonar4 + sonar3)/2
        theta = (inp.odometry.t)%(2*pi)

        # gains
        fGain = 1
        rGain = 2
        if curState == 'start':
            # move forward
            rv = 0
            fv = (avgSonar - 0.4)*fGain
            
            if avgSonar < 0.5 :
                
                if (theta < 0.02 and theta >= 0.0) or (theta < 2*pi and theta > 2*pi - 0.02):
                    nextState = 'east'
                elif theta < pi/2 + 0.02 and theta > pi/2 - 0.02:
                    nextState = 'north'
                elif theta < pi + 0.02 and theta > pi - 0.02:
                    nextState = 'west'
                else:
                    nextState = 'south'
            else:
                nextState = 'start'
        elif curState == 'east':
            fv = 0
            rv = rGain * (pi/2 - theta)
            if theta < pi/2 + 0.02 and theta > pi/2 - 0.02:
                nextState = 'start'
            else:
                nextState = 'east'

        elif curState == 'north':
            fv = 0
            rv = rGain * (pi - theta)
            if theta < pi + 0.02 and theta > pi - 0.02:
                nextState = 'start'
            else:
                nextState = 'north'

        elif curState == 'west':
            fv = 0
            rv = rGain * (3*pi/2 - theta)
            if theta < 3*pi/2 + 0.02 and theta > 3*pi/2 - 0.02:
                nextState = 'start'
            else:
                nextState = 'west'
        else:
            fv = 0
            rv = rGain * (2*pi - theta) if theta < 2*pi and theta > 2*pi/3 - 0.02 else -0.02
            if (theta <  0.02 and theta > 0) or (theta > 2*pi - 0.02 and theta < 2*pi):
                nextState = 'start'
            else:
                nextState = 'south' 
        return (nextState, io.Action(self.robot, fvel = fv, rvel = rv))
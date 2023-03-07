"""  
Modify Pioneer Robot
"""
from soar.robot.pioneer import PioneerRobot
from math import sin, cos

# create class odometry to circumvent the Pose challenge:
class Odometry:
    def __init__(self, x, y, t) -> None:
        self.x = x # x corrdinate
        self.y = y # y coordinate
        self.t = t # theta heading

    def __str__(self) -> str:
        return '(' + str(self.x) + ', ' + str(self.y) + ', ' + str(self.t) + ')'
        
    def transform(self, other):
        """  
        given tuple of (x, y, t)
        returns: Odometry 
        """
        return Odometry(self.x + other[0], self.y + other[1], self.t + other[2])


# modify PioneerRobot to have odometry:
class PioneerMod(PioneerRobot):
    """  
    modify the Pioneer Robot 
    adding odomtry on it
    """
    def __init__(self, **options):
        # add odometry as this is not the same as post
        self.odometry = Odometry(0.0, 0.0, 0.0)
        super().__init__(**options)
    
    def on_step(self, duration):
        # update odometry:
        if self.simulated:
            theta = self.pose[2]
            d_t = self.rv*duration
            new_theta = theta + d_t
            if self.rv != 0:
                d_x = self.fv*(sin(new_theta)-sin(theta))/self.rv
                d_y = self.fv*(cos(theta)-cos(new_theta))/self.rv
            else:
                d_x, d_y = self.fv*cos(theta)*duration, self.fv*sin(theta)*duration
            newOdo = self.odometry.transform((d_x, d_y, d_t))
        super().on_step(duration)
        self.odometry = newOdo

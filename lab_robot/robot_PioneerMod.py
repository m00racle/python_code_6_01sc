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

    def __getitem__(self, val):
        return self.xyt_tuple()[val]


    def xyt_tuple(self):
        """  
        return tuple of x, y, theta 
        used to make subscriptable Odometry
        """
        return self.x, self.y, self.t
        
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
        """  
        Transform odometry based on the changes of pose before and after the superclass updates:
        """
        start_pose = self.pose
        super().on_step(duration)
        od_x = self.pose.x - start_pose.x
        od_y = self.pose.y - start_pose.y
        od_t = self.pose.t - start_pose.t
        newOdo = self.odometry.transform((od_x, od_y, od_t))
        self.odometry = newOdo

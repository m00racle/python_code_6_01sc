"""  
Modify Pioneer Robot
"""
from soar.robot.pioneer import PioneerRobot
from math import sqrt, pi, sin, cos
from soar.sim.geometry import normalize_angle_180

# create class odometry to circumvent the Pose challenge:
class Odometry:
    def __init__(self, x, y, t) -> None:
        self.x = x # x corrdinate
        self.y = y # y coordinate
        self.t = t # theta heading

    def __str__(self) -> str:
        return '(' + str(self.x) + ', ' + str(self.y) + ', ' + str(self.t) + ')'

    def __getitem__(self, val):
        """  
        Make odometry instance act like tuple
        Indexable and Subscriptable
        """
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
        return Odometry(self.x + other[0], self.y + other[1], (self.t + other[2]) % (2.0*pi))

    def is_near(self, other: tuple , dist_eps: float, angle_eps: float)->bool:
        """  
        Args:
        other: tuple or Odometry type = the target x, y, t
        dist_eps: float = The distance epsilon within which to consider the odometry is close
        angle_eps : float = The angle epsilon

        Returns: bool = True if the distance within dist_eps and  normalized difference between the angle
        is within angle_eps
        """
        # finding distance
        distance = sqrt(abs(other[0] - self[0])**2 + abs(other[1] - self[1])**2)
        dist_angle = abs(normalize_angle_180(self[2] - other[2]))

        return distance < dist_eps and dist_angle < angle_eps



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
        # ======= POSE (GPS) based odometry ===================
        # start_pose = self.pose
        # super().on_step(duration)
        # od_x = self.pose.x - start_pose.x
        # od_y = self.pose.y - start_pose.y
        # od_t = self.pose.t - start_pose.t
        # newOdo = self.odometry.transform((od_x, od_y, od_t))
        # self.odometry = newOdo
        # =========uncomment to this and comment the other to use GPS based odometry

        # ======== manual sensor odometry ============================================
        theta = self.odometry[2]
        d_t = self.rv * duration
        new_theta = theta + d_t
        if self.rv != 0:
            d_x = self.fv * (sin(new_theta) - sin(theta))/self.rv
            d_y = self.fv * (cos(theta) - cos(new_theta))/self.rv
        else:
            d_x, d_y = self.fv * cos(theta) * duration, self.fv * sin(theta) * duration
        new_odo = self.odometry.transform((d_x, d_y, d_t))
        self.odometry = new_odo
        super().on_step(duration)
        # ===== uncomment above and comment the other to use manual sensor odometry
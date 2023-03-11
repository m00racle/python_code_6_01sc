"""  
Modify Pioneer Robot
"""
from soar.robot.pioneer import PioneerRobot
from math import sqrt, pi, sin, cos
from soar.sim.geometry import normalize_angle_180, Pose

# modify PioneerRobot to have odometry:
class PioneerMod(PioneerRobot):
    """  
    modify the Pioneer Robot 
    adding odomtry on it
    """
    def __init__(self, **options):
        # add odometry as this is not the same as post
        self.odometry = Pose(0.0, 0.0, 0.0)
        super().__init__(**options)
    
    def on_step(self, duration):
        """  
        Transform odometry based on the changes of pose before and after the superclass updates:
        CAUTION: If there are problems in the Odometry accuracies here is where you tweak it!
        """

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
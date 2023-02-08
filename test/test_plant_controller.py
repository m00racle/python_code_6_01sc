import os, sys, unittest, io

# set the code and test directory location
test_dir = os.path.dirname(__file__)
source_dir = os.path.normpath(test_dir + "/../Lec_2_State_Machine")

sys.path.append(source_dir)

from feedback_sm import Feedback
from cascade import Cascade
# sourcwe
import plants_controller as pc

class TestRobotPlantController(unittest.TestCase):
    """  
    Test cases for simulating and test robot for 
    Plant and controller
    """

    def test_wall_robot_movement_towards_desired_range(self):
        """  
        given combined plant and contoller
        test the robot movement towards wall limit
        """
        robot = Feedback(Cascade(pc.WallController(-1.5, 1.0), pc.WallWorld(0.1, 5)))

        # assert 
        self.assertEqual(robot.run(30), \
            [5, 4.4000000000000004, 3.8900000000000001, 3.4565000000000001,\
             3.088025, 2.77482125, 2.5085980624999999, 2.2823083531249999,\
             2.0899621001562498, 1.9264677851328122, 1.7874976173628905,\
             1.6693729747584569, 1.5689670285446884, 1.483621974262985,\
             1.4110786781235374, 1.3494168764050067, 1.2970043449442556,\
             1.2524536932026173, 1.2145856392222247, 1.1823977933388909,\
             1.1550381243380574, 1.1317824056873489, 1.1120150448342465,\
             1.0952127881091096, 1.0809308698927431, 1.0687912394088317,\
             1.058472553497507, 1.049701670472881, 1.0422464199019488,\
             1.0359094569166565])
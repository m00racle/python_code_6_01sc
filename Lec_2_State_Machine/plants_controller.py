"""  
the plant and controller
used to model a robot controller and simulate the world 
"""

from state_machine import SM

class WallController(SM):
    """  
    State Machine: Wall Controller
    subclass of State Machine SM
    """

class WallWorld(SM):
    """  
    State Machine : Wall World simulate the external world interact with the robot
    subclass of State Machine SM
    """
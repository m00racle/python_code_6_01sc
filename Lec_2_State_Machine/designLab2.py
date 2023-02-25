"""  
Design Lab 2
Controlling Robots

Goals: 
• Experiment with state machines controlling real machines (real machine will be ignored)
• Investigate real-world distance sensors on 6.01 robots: sonars 
• Build and demonstrate a state machine to make the robot do a task: following a boundary

NOTE: since I don't have access to the deprecated lib601 I have to make some adjustmnents
"""

import state_machine as sm
from soar.robot.pioneer import PioneerRobot

def action(fvel: float, rvel: float):
    """  
    helper function to make it clearer forward velocity
    and rotation velocity
    """
    return (fvel, rvel)

# define brain as state machine
class SMLab2(sm.SM):
    """  
    class represent the brain behavior for robot
    """
    def getNextValues(self, state, inp, **kwargs) -> tuple:
        return (state, (action(fvel=0.0, rvel=0.5)))


# THE ROBOT FUNCTIONS: 
# NOTE: after this we will only modify the SMLab2 for the robot behavior.
# ROBOT FUNCTIONS will only be used for debugging purposes
# TODO: find a way to make the robot leve trace whenever it translates.
robot = PioneerRobot()
mySm = SMLab2()

def on_load():
    # we make the robot like an SM by controlling its brain:
    robot.behavior = mySm

def on_start():
    # using the state machine start:
    robot.behavior.start()

def on_step(step_duration):
    # using the state machine step:
    (robot.fv, robot.rv) = robot.behavior.step(step_duration)
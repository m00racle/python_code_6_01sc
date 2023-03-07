"""  
Robot Brain and controllers
"""

from soar.robot.pioneer import PioneerRobot
import robot_spec as spec
import robot_io as io

# specify the robot spec:
robot_spec = spec.TestForward #TODO: chage this to specify the robot.

# set the the robot
robot = PioneerRobot()

#  This function is called when the brain is loaded
def on_load():
    robot.behavior = robot_spec(robot)

#  This function is called when the start button is pushed
def on_start():
    robot.behavior.start()

#  This function is called every step_duration seconds. By default, it is called 10 times/second
def on_step(step_duration):
    # for testing only
    print(f'robot data: {robot.to_dict()}')
    robot.behavior.step(io.SensorInput(robot),verbose=True).execute()

# This function is called when the stop button is pushed
def on_stop():
    pass

# This function is called when the robot's controller is shut down
def on_shutdown():
    pass

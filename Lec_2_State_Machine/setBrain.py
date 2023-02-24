from soar.robot.pioneer import PioneerRobot
# to be use or run using SOAR not else

robot = PioneerRobot()

def on_load():
    robot.count = 0
    # NOTE: count is not default attribute for robot
    # this is added to test the robot setting

def on_step(step_duration):
    print(f'\nstep duration: {step_duration}')
    print(f'robot count: {robot.count}')
    print(f'sonar readings: {robot.sonars}')
    print(f'robot forward speed: {robot.fv}')
    print(f'robot rotate speed: {robot.rv} rad/sec')

    if robot.count < 100 :
        robot.fv = 1
    else:
        on_stop()

    robot.rv = 60/180 #pi/6 rad/s
    robot.count += 1


def on_stop():
    robot.fv = 0
    robot.rv = 0

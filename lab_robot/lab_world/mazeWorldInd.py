from soar.sim.world import *
from math import pi

# preps the size
world_size = (4.0, 4.0)
robot_start = (1, 3.5, pi)
# Now for the obstacles:
wall1 = Wall((3,1),(2,1))
wall2 = Wall((3,3),(3,0))
wall3 = Wall((1,0),(1,2))
wall4 = Wall((1,2),(2,2))
wall5 = Wall((1,3),(3,3))

# put all the walls in one list
obstacles = [wall1, wall2, wall3, wall4, wall5]

# put the world together
world = World(world_size, robot_start, obstacles)
from soar.sim.world import *
from math import pi

"""  
World small with only a box somewhere inside.
The box is created with arranging 4 Walls 
"""
world = World(initial_position=(1.5, 2.5, 1.5*pi),
dimensions=(3.05,3.05),
objects=[
Wall((1.00,1.00),(1.44,1.00)),
Wall((1.44, 1.00),(1.44,1.29)),
Wall((1.44,1.29),(1.00,1.29)),
Wall((1.00,1.29),(1.00,1.00))])
from soar.sim.world import *
from math import pi

world = World(
dimensions=(4.0,4.0),
initial_position=(0.25,0.25,pi),
objects=[
Wall((0.5 ,-0.5),(0.5, 1.5)),
Wall((0.5, 1.5),(1.5, 1.5)),
Wall((0.5, 2.5),(2.5, 2.5)),
Wall((2.5, 2.5),(2.5, -0.5)),
Wall((2.5, 0.5),(1.5, 0.5))
])
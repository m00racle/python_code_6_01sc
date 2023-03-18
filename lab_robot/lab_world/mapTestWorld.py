from soar.sim.world import *
from math import pi

world = World(
initial_position=(2.0,0.5,pi),
dimensions=(4.05,6.05),
objects=[
Wall((1.5,3.0),(3.0,3.0)),
Wall((3.0, 3.0),(3.0,3.5)),
Wall((3.0,3.5),(2.0,3.5)),
Wall((2.0,3.5),(2.0,4.5)),
Wall((2.0,4.5),(1.5,4.5)),
Wall((1.5,4.5),(1.5,3.0)),

Wall((1.0,1.5),(3.0,1.5)),
Wall((3.0, 1.5),(3.0,2.0)),
Wall((3.0,2.0),(1.0,2.0)),
Wall((1.0,2.0),(1.0,1.5))
])
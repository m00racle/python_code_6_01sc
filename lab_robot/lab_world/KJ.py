from soar.sim.world import *
from math import pi

world = World(
dimensions=(4.0,3.0), initial_position=(1.0,2.5,0.0*pi),
objects=[
Wall((1.0,0.),(1.0,1.0)),
Wall((1.0,1.0),(2.0,1.0)),
Wall((3.0,1.0),(3.0,2.0)),
Wall((1.0,2.0),(3.0,2.0))
])
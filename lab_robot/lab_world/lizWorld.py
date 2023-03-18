from soar.sim.world import *
from math import pi

world = World(
dimensions=(10.0, 10.0), 
initial_position=(1.0,1.0,pi*0.0),
objects=[
Wall((2,2),(1.5,7)),
Wall((1.5,7),(5,8)),
Wall((5,10),(8,8)),
Wall((8,8),(6,5)),
Wall((5.5,5.5),(6,5)),
Wall((6,5),(5.5,4.5)),
Wall((5.5,4.5),(5,5)),

Wall((5, 5), (4, 4)),
Wall((4, 4), (6, 3)),
Wall((8, 5), (7, 0.4)),

Wall((2, 2), (2, 0))
])
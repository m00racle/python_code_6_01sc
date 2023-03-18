from soar.sim.world import *
from math import pi

"""  
Weird world 3 x 3 ish but with weird arrangement of boxes
"""

world = World(initial_position=(1.0, 1.5, 0.0*pi),
dimensions=(3.05,3.05),
objects=[
Wall((0.00,2.00),(0.44,2.00)),
Wall((0.44,2.00),(0.44,2.29)),
Wall((0.44,2.29),(0.00,2.29)),
Wall((0.00,2.29),(0.00,2.00)),
Wall((1.8, 0), (1.8, 3.05)),
Wall((2.2, 0), (2.2, 3.05)),
Wall((2.6, 0), (2.6, 3.05)),
Wall((2.8, 0), (2.8, 3.05))
])
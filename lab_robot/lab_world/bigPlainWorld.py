from soar.sim.world import *

world = World(dimensions=(10.0, 10.0), initial_position=(1.0, 1.0, 1.5707),
objects=[Wall((2,0),(2,7)),
Wall((2,7),(6,7)),
Wall((7,0),(7,3)),
Wall((5,5),(5.5,5.5)),
Wall((5.5,5.5),(6,5)),
Wall((6,5),(5.5,4.5)),
Wall((5.5,4.5),(5,5)),
Wall((3,2),(5,2))])
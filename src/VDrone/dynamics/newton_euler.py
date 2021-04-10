# **********************************************************************************************************************
#   FileName:
#       newton_euler.py
#
#   Description:
#       Simulation of the Newton-Euler representation of quadrotor dynamics
#
#   4/8/21 | Brandon Braun | brandonbraun653@gmail.com
# **********************************************************************************************************************

import numpy as np
from VDrone.dynamics.abstract import IDynamics


class NewtonEulerSim(IDynamics):

    def __init__(self):
        super().__init__()

    def step(self, dt: float) -> bool:
        pass



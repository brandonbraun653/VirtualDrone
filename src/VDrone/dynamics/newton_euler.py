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
    """ A highly theoretical approach to modeling the quadcopter """

    def __init__(self):
        super().__init__()

        # ---------------------------------------------------------
        # Physical Properties
        # ---------------------------------------------------------
        # Total mass of the drone
        self.mass = 0.0

        # Distance from motor rotation axis to drone center of mass. This is assumed
        # to be symmetrical on all axis.
        self.moment_arm_length = 0.0

        # Moment of inertia
        self.Ixx = 0.0
        self.Iyy = 0.0
        self.Izz = 0.0

        # ---------------------------------------------------------
        # Linear Position (Inertial Frame)
        # ---------------------------------------------------------
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0

        # ---------------------------------------------------------
        # Linear Velocity (Inertial Frame)
        # ---------------------------------------------------------
        self.p = 0.0    # X-axis
        self.q = 0.0    # Y-axis
        self.r = 0.0    # Z-axis

        # ---------------------------------------------------------
        # Rotation Angles (Inertial Frame)
        # ---------------------------------------------------------
        self.phi = 0.0      # Rotation angle about the x-axis
        self.theta = 0.0    # Rotation angle about the y-axis
        self.psi = 0.0      # Rotation angle about the z-axis

        # ---------------------------------------------------------
        # Motor models
        # ---------------------------------------------------------
        self.motors = [4]


    def step(self, input: np.ndarray, state: np.ndarray, dt: float) -> bool:
        pass




    def rotation_matrix_to_interial(self, phi: float, theta: float, psi: float) -> np.ndarray:
        """
        Calculates the current rotation matrix from the body frame to the inertial frame.
        """
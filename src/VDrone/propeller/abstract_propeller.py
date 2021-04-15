# **********************************************************************************************************************
#   FileName:
#       abstract_propeller.py
#
#   Description:
#       An abstract interface to describe a propeller physics model
#
#   4/10/21 | Brandon Braun | brandonbraun653@gmail.com
# **********************************************************************************************************************

import numpy as np
from VDrone.interface import TransferFunction


class IPropeller(TransferFunction):

    def __init__(self):
        super().__init__()

        self.pitch = 0.0
        self.diameter = 0.0

    def tf_evaluate(self, sig_in: np.ndarray, dt: float = 0.0) -> np.ndarray:
        raise NotImplementedError

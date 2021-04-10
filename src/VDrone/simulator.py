# **********************************************************************************************************************
#   FileName:
#       simulator.py
#
#   Description:
#       Utility for generically running a simulation on a system model
#
#   4/9/21 | Brandon Braun | brandonbraun653@gmail.com
# **********************************************************************************************************************

from typing import Any


class Simulator:

    def __init__(self):
        pass

    def initialize(self, t0: float, x0: Any):
        pass

    def attach_model(self, model: Any):
        pass

    def run(self, tf: float, ts: float):
        """
        Runs the simulation on the model
        Args:
            tf: Final time to execute to
            ts: Sampling rate resolution

        Returns:

        """
        pass
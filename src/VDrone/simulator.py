# **********************************************************************************************************************
#   FileName:
#       simulator.py
#
#   Description:
#       Utility for generically running a simulation on a system model
#
#   4/9/21 | Brandon Braun | brandonbraun653@gmail.com
# **********************************************************************************************************************

import numpy as np
from typing import Any
from VDrone.interface import TransferFunction
from VDrone.propeller.model import StandardProp


class Simulator:
    """ Takes a mathematical system and simulates its behavior """

    def __init__(self):
        self.t0 = 0.0
        self.tf = 0.0
        self.model = TransferFunction()
        self._sim_data = []

    def attach_model(self, model: TransferFunction):
        self.model = model

    def run(self, t0: float, tf: float, ts: float) -> None:
        """
        Runs the simulation on the model
        Args:
            t0: Initial time to start at
            tf: Final time to execute to
            ts: Sampling rate resolution

        Returns:
            None
        """
        time_steps = np.arange(t0, tf, ts)
        for t in time_steps:
            output = self.model.tf_evaluate(sig_in=0.0, dt=ts)
            self._sim_data.append([t, output])

    def plot(self):
        pass


def main():
    sim = Simulator()
    prop = StandardProp()
    prop.pitch = 3.5
    prop.diameter = 45



if __name__ == "__main__":
    main()
# **********************************************************************************************************************
#   FileName:
#       abstract.py
#
#   Description:
#       Abstract interface for the drone dynamics modeling instances
#
#   4/8/21 | Brandon Braun | brandonbraun653@gmail.com
# **********************************************************************************************************************

import numpy as np
from abc import ABCMeta, abstractmethod, abstractproperty


class IDynamics:
    __metaclass__ = ABCMeta

    def __init__(self):
        self._step_resolution = 0.001

    @property
    def resolution(self) -> float:
        return self._step_resolution

    @resolution.setter
    def resolution(self, val: float) -> None:
        self._step_resolution = val

    @abstractmethod
    def step(self, control: np.ndarray, last_state: np.ndarray, dt: float) -> np.ndarray:
        """
        Args:
            control: System control input vector
            last_state: Last system state
            dt: How far forward to step the simulation in seconds
        Returns:
            System state vector
        """
        raise NotImplementedError

    @abstractmethod
    def get_state(self) -> np.ndarray:
        raise NotImplementedError

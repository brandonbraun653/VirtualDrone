# **********************************************************************************************************************
#   FileName:
#       abstract_motor.py
#
#   Description:
#       Declares the base interface that all motor simulation types should adhere to
#
#   4/8/21 | Brandon Braun | brandonbraun653@gmail.com
# **********************************************************************************************************************

from abc import ABCMeta, abstractmethod, abstractproperty


class IMotor:
    __metaclass__ = ABCMeta

    def set_controller(self, controller) -> None:
        """
        Assigns a control system to the motor to simulate more realistic conditions
        Args:
            controller: Control system implementation

        Returns:
            None
        """
        raise NotImplementedError

    def step(self, control: float, last_state: float, dt: float) -> float:
        """
        Steps the simulation model forward with the given controller input
        Args:
            control: Reference control signal input
            last_state: Last system state
            dt: Time step to move the model forward by

        Returns:
            float: Current motor angular speed
        """
        raise NotImplementedError

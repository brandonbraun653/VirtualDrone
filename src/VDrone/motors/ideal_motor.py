# **********************************************************************************************************************
#   FileName:
#       ideal_motor.py
#
#   Description:
#       Models an idealistic motor
#
#   4/8/21 | Brandon Braun | brandonbraun653@gmail.com
# **********************************************************************************************************************

from VDrone.motors.abstract_motor import IMotor


class IdealMotor(IMotor):
    """ Motor type that instantly achieves the desired output """

    def __init__(self):
        pass

    def set_controller(self, controller) -> None:
        pass

    def step(self, control: float, dt: float) -> float:
        pass


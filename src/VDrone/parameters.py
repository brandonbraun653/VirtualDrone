# **********************************************************************************************************************
#   FileName:
#       parameters.py
#
#   Description:
#       Lists out supported IO data parameters that are understood by the simulator
#
#   4/13/21 | Brandon Braun | brandonbraun653@gmail.com
# **********************************************************************************************************************

import copy
import time
import numpy as np
from abc import ABCMeta, abstractmethod
from typing import Any
from threading import RLock
from enum import Enum, auto
from VDrone.nanopb.sim_pb2 import HeartBeat
from VDrone.nanopb.ahrs_pb2 import GyroSample, AccelSample, MagSample
from google.protobuf.message import DecodeError


class ParameterID(Enum):
    """ List of supported parameters that the system maintains info on"""
    INVALID = 0

    # Simulator Internals
    HEARTBEAT = auto()

    # Sensor measurements
    ACCEL_DATA = auto()
    GYRO_DATA = auto()
    MAG_DATA = auto()


class IParameter:
    __metaclass__ = ABCMeta

    def __init__(self, param_type: Any):
        """
        Initialize the parameter interface
        Args:
            param_type: Parameter type
        """
        self._param_type = param_type
        self._param_data = None

    def update(self, new_value: Any) -> bool:
        """
        Updates the old parameter data with the new value
        Args:
            new_value: New data to update with

        Returns:
            True: Update was successful
            False: Update was not successful
        """
        if isinstance(new_value, self._param_type):
            self._param_data = copy.deepcopy(new_value)
            return True
        else:
            return False

    def value(self) -> Any:
        """
        Gets the current stored value and returns it as a copy. This prevents unwanted
        modification of the tracked data by those who consume it.
        Returns:
            A copy of the stored data
        """
        return copy.deepcopy(self._param_data)

    def serialize(self) -> str:
        """
        Serializes the parameter data for transmission via the network protocol
        Returns:
            str
        """
        return ""

    def deserialize(self, data: str) -> bool:
        """
        Converts the protobuf data into the format used in the simulator
        Args:
            data: Serialized protobuf data

        Returns:
            True: The conversion was successful
            False: The conversion was not successful
        """
        return False

    @abstractmethod
    def is_valid(self) -> bool:
        """
        Checks the validity of the parameter data. Because this is so subjective, leave it up to
        the inheriting classes to define what this means.
        Returns:
            True: Data is valid
            False: Data is not valid
        """
        raise NotImplementedError

    @property
    def id(self):
        """
        Which parameter this is modeling
        Returns:
            ParameterID
        """
        raise ParameterID.INVALID

    @property
    def param_type(self):
        return self._param_type


class DefaultParameter(IParameter):
    """ Most basic parameter type that is always valid once assigned """

    def __init__(self, param_type, initial_value: Any = None):
        """
        Initialize the default parameter object
        Args:
            param_type: Type of the tracked parameter
            initial_value: Initial value of the tracked parameter
        """
        super().__init__(param_type)

        # Default construct the data from the type if user didn't pass anything in
        self._param_data = initial_value if initial_value else param_type()

    def is_valid(self) -> bool:
        """
        Validity is simply determined by whether or not the data is assigned
        Returns:
            True: Data is valid
            False: Data is not valid
        """
        return self._param_data is not None


class TimedParameter(IParameter):
    """ A parameter type whose validity depends on a timeout"""

    def __init__(self, param_type, initial_value: Any = None, timeout: float or int = 1.0):
        """
        Initialize the timed parameter object
        Args:
            param_type: Type of the tracked parameter
            initial_value: Initial value of the tracked parameter
            timeout: How frequently the parameter must be update before being considered stale
        """
        super().__init__(param_type)
        self._param_timeout = timeout
        self._last_update = time.time()

        # Default construct the data from the type if user didn't pass anything in
        self._param_data = initial_value if initial_value is not None else param_type()

    def update(self, new_value) -> bool:
        """
        Updates the parameter with new data performing a type check to ensure
        the underlying structure isn't changed at runtime.
        Args:
            new_value: New data to be set

        Returns:
            True: Update was successful
            False: Update was not successful
        """
        if isinstance(new_value, self._param_type):
            self._param_data = new_value
            self._last_update = time.time()
            return True
        else:
            return False

    def is_valid(self) -> bool:
        """
        Checks if the parameter has timed out
        Returns:
            True: Data has been consistently updated
            False: Data has not been updated within the timeout window
        """
        return (time.time() - self._last_update) < self._param_timeout


class HeartBeatData(TimedParameter):
    """ Stores a virtual heart beat signal that indicates the sim is alive """

    def __init__(self, timeout: float or int = 1.0):
        super().__init__(param_type=int, initial_value=0, timeout=timeout)
        self._protobuf_data = HeartBeat()

    @property
    def id(self):
        return ParameterID.HEARTBEAT

    def serialize(self) -> str:
        self.update(new_value=time.time())
        self._protobuf_data.data.timestamp = self.value()
        return self._protobuf_data.SerializeToString()

    def deserialize(self, data: str) -> bool:
        """
        Converts the protobuf gyro data into the format used in the simulator
        Args:
            data: Serialized protobuf data

        Returns:
            True: The conversion was successful
            False: The conversion was not successful
        """
        try:
            parsed_bytes = self._protobuf_data.ParseFromString(data)
        except DecodeError:
            return False

        return self.update(new_value=self._protobuf_data.data.timestamp)


class GyroData(TimedParameter):
    """ Stores gyroscope data with a validity timeout """

    KEY_X = 0
    KEY_Y = 1
    KEY_Z = 2

    def __init__(self, timeout: float or int = 1.0):
        super().__init__(param_type=type(np.ndarray((3, 1))), initial_value=np.zeros((3, 1)), timeout=timeout)
        self._protobuf_data = GyroSample()

    @property
    def id(self):
        return ParameterID.GYRO_DATA

    def serialize(self) -> str:
        raw_data = self.value()
        self._protobuf_data.x = raw_data[self.KEY_X]
        self._protobuf_data.y = raw_data[self.KEY_Y]
        self._protobuf_data.z = raw_data[self.KEY_Z]
        return self._protobuf_data.SerializeToString()

    def deserialize(self, data: str) -> bool:
        """
        Converts the protobuf gyro data into the format used in the simulator
        Args:
            data: Serialized protobuf data

        Returns:
            True: The conversion was successful
            False: The conversion was not successful
        """
        try:
            parsed_bytes = self._protobuf_data.ParseFromString(data)
        except DecodeError:
            return False

        raw_data = self.param_type()
        raw_data[self.KEY_X] = self._protobuf_data.x
        raw_data[self.KEY_Y] = self._protobuf_data.y
        raw_data[self.KEY_Z] = self._protobuf_data.z

        return self.update(new_value=raw_data)


class AccelData(TimedParameter):
    """ Stores accelerometer data with a validity timeout """

    KEY_X = 0
    KEY_Y = 1
    KEY_Z = 2

    def __init__(self, timeout: float or int = 1.0):
        super().__init__(param_type=type(np.ndarray((3, 1))), initial_value=np.zeros((3, 1)), timeout=timeout)
        self._protobuf_data = AccelSample()

    @property
    def id(self):
        return ParameterID.ACCEL_DATA

    def serialize(self) -> str:
        raw_data = self.value()
        self._protobuf_data.data.x = raw_data[self.KEY_X]
        self._protobuf_data.data.y = raw_data[self.KEY_Y]
        self._protobuf_data.data.z = raw_data[self.KEY_Z]
        return self._protobuf_data.SerializeToString()

    def deserialize(self, data: str) -> bool:
        """
        Converts the protobuf gyro data into the format used in the simulator
        Args:
            data: Serialized protobuf data

        Returns:
            True: The conversion was successful
            False: The conversion was not successful
        """
        try:
            parsed_bytes = self._protobuf_data.ParseFromString(data)
        except DecodeError:
            return False

        raw_data = self.param_type()
        raw_data[self.KEY_X] = self._protobuf_data.data.x
        raw_data[self.KEY_Y] = self._protobuf_data.data.y
        raw_data[self.KEY_Z] = self._protobuf_data.data.z

        return self.update(new_value=raw_data)


class MagData(TimedParameter):
    """ Stores magnetometer data with a validity timeout """

    KEY_X = 0
    KEY_Y = 1
    KEY_Z = 2

    def __init__(self, timeout: float or int = 1.0):
        super().__init__(param_type=type(np.ndarray((3, 1))), initial_value=np.zeros((3, 1)), timeout=timeout)
        self._protobuf_data = MagSample()

    @property
    def id(self):
        return ParameterID.MAG_DATA

    def serialize(self) -> str:
        raw_data = self.value()
        self._protobuf_data.data.x = raw_data[self.KEY_X]
        self._protobuf_data.data.y = raw_data[self.KEY_Y]
        self._protobuf_data.data.z = raw_data[self.KEY_Z]
        return self._protobuf_data.SerializeToString()

    def deserialize(self, data: str) -> bool:
        """
        Converts the protobuf gyro data into the format used in the simulator
        Args:
            data: Serialized protobuf data

        Returns:
            True: The conversion was successful
            False: The conversion was not successful
        """
        try:
            parsed_bytes = self._protobuf_data.ParseFromString(data)
        except DecodeError:
            return False

        raw_data = self.param_type()
        raw_data[self.KEY_X] = self._protobuf_data.data.x
        raw_data[self.KEY_Y] = self._protobuf_data.data.y
        raw_data[self.KEY_Z] = self._protobuf_data.data.z

        return self.update(new_value=raw_data)

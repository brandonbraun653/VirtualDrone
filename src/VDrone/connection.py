# **********************************************************************************************************************
#   FileName:
#       connection.py
#
#   Description:
#       Implements a drone object
#
#   4/13/21 | Brandon Braun | brandonbraun653@gmail.com
# **********************************************************************************************************************

import json
import zmq
from typing import Any
from pathlib import Path
from loguru import logger
from time import sleep
from enum import Enum, IntEnum, auto
from threading import Thread, Event
from VDrone.parameters import *
from VDrone.utility import find_parent_path


class SimConnection(Thread):
    """
    Manages a connection to a simulated flight controller over ZMQ
    """

    class Signals(IntEnum):
        """ Supported event signals for the simulator connection """
        KILL = auto()

    class TxSockets(Enum):
        """ Supported sockets for transmitting data """
        SENSOR = "sensor"       # All system sensor data

    class RxSockets(Enum):
        """ Supported sockets for receiving data """
        SYS_CONTROL = "system_control"      # System control input
        USER_INPUT = "user_input"           # User IO input. Think physical device interfaces (switches, button, etc)

    def __init__(self):
        """ Power up the drone class """
        super().__init__()

        # ---------------------------------------------------------
        # Public Attributes: Modify to change the system behavior
        # ---------------------------------------------------------
        # How long the heartbeat signal may be missing before the connection is considered stale (seconds)
        self.stale_connection_timeout = 5.0

        # ---------------------------------------------------------
        # Private configuration
        # ---------------------------------------------------------
        # Initialize the logger
        logger.add("drone_log.log")

        # Initialize event signaling
        self._event_signals = {}
        for key in self.Signals:
            self._event_signals[key.value] = Event()

        # ZMQ Resources
        self._zmq_context = zmq.Context(io_threads=8)
        self._zmq_pub_sockets = {key.value: self._zmq_context.socket(zmq.PUB) for key in self.TxSockets}
        self._zmq_sub_sockets = {key.value: self._zmq_context.socket(zmq.SUB) for key in self.RxSockets}
        self._boot_zmq()

        # Flight controller connection status
        self._fcs_connected = TimedParameter(bool, initial_value=False, timeout=0.5)

    def kill(self) -> None:
        """
        Kills the drone simulation thread
        Returns:
            None
        """
        self._event_signals[self.Signals.KILL].set()
        logger.debug("Drone kill signal set")

    def run(self) -> None:
        logger.info("Running the thread!")
        while not self._event_signals[self.Signals.KILL].is_set():
            sleep(1)
            logger.info("Hello world")
        logger.info("Exiting the program")

    def transmit(self, parameter, value, timestamp):
        """
        Transmits a piece of data to the flight software
        Args:
            parameter:
            value:
            timestamp:

        Returns:

        """
        # Cache the data as a copy in a queue. Don't look at the parameter manager
        pass

    def receive(self, parameter) -> Any:
        """
        Receives
        Args:
            parameter:

        Returns:

        """
        # Pull out the copy from the queue
        pass

    def signal_event(self, signal: Signals) -> None:
        """
        Signal a system event within the virtual drone
        Args:
            signal: Which signal to set

        Returns:
            None
        """
        self._event_signals[signal.value].set()

    def connect(self, timeout: float or int) -> bool:
        """
        Attempts to connect to the remote flight controller software
        Args:
            timeout: How long to attempt in seconds
        Returns:
            True: Successfully connected within the timeout window
            False: Did not connect or connection was rejected
        """
        pass

    def is_connected(self) -> bool:
        """
        Checks if the virtual drone is connected up to the flight software
        Returns:
            True: Still connected
            False: Not connected
        """
        return self._fcs_connected.is_valid()

    def _boot_zmq(self) -> None:
        """
        Powers up the various ZMQ resources for communicating with the flight
        controller software.
        Returns:
            None
        """
        cfg = self._load_sim_ports()
        port_format = "{}://{}".format(cfg['transport'], cfg['bind_ip'])

        # Configure the PUB sockets
        for topic in self._zmq_pub_sockets.keys():
            bind_to = "{}:{}".format(port_format, cfg['port'][topic])
            self._zmq_pub_sockets[topic].bind(bind_to)
            logger.debug("Bind pub socket [{}] to {}".format(topic, bind_to))

        # Configure the SUB sockets
        for topic in self._zmq_sub_sockets.keys():
            conn_to = "{}:{}".format(port_format, cfg['port'][topic])
            self._zmq_sub_sockets[topic].connect(conn_to)
            logger.debug("Connect sub socket [{}] to {}".format(topic, conn_to))

    def _rx_message_pump(self) -> None:
        """
        Process incoming messages from the flight software
        Returns:
            None
        """
        pass

    @staticmethod
    def _load_sim_ports() -> dict:
        """
        Pulls the simulator configuration port information from disk
        Returns:
            dict
        """
        project_root = find_parent_path(Path.cwd(), "Valkyrie")
        config_file = Path(project_root, 'src', 'database', 'sim_ports.json')
        with config_file.open() as f:
            return json.load(f)

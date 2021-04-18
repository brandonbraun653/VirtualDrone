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
from pyutils.path import find_parent_path
from queue import Queue, Empty
from typing import Union, List, Dict
from pathlib import Path
from loguru import logger
from time import sleep
from enum import Enum, IntEnum
from threading import Thread, Event
from VDrone.parameters import *


class SimConnection(Thread):
    """
    Manages a connection to a simulated flight controller over ZMQ
    """

    class Signals(IntEnum):
        """ Supported event signals for the simulator connection """
        KILL = auto()

    class TxSocket(Enum):
        """ Supported sockets for transmitting data """
        SENSOR = "sensor"  # All system sensor data
        SIM_INTERNAL = "tx_sim"

    class TxTopics(Enum):
        """ Supported topics to publish data on for TX sockets """
        HEARTBEAT = "tx_heartbeat"
        ACCEL_DATA = "accel"
        GYRO_DATA = "gyro"
        MAG_DATA = "mag"

    class RxSocket(Enum):
        """ Supported sockets for receiving data """
        SIM_INTERNAL = "rx_sim"  # Data exclusive to sim operations
        SYS_CONTROL = "system_control"  # System control input
        USER_INPUT = "user_input"  # User IO input. Think physical device interfaces (switches, button, etc)

    class RxTopics(Enum):
        """ Supported topics to receive data on for RX sockets """
        HEARTBEAT = "rx_heartbeat"

    class DataFlow(Enum):
        """ Classifies the direction data is flowing """
        TX = "tx"
        RX = "rx"

    def __init__(self, processing_period: float = 0.01):
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
        # Initialize the file logger for this class
        logger.add("drone_log.log", level="TRACE")

        # Initialize event signaling
        self._event_signals = {}
        for key in self.Signals:
            self._event_signals[key.value] = Event()

        # Networking information
        self._pump_rate = processing_period
        self._data_map = SimData()

        # ZMQ Resources
        self._zmq_context = zmq.Context(io_threads=8)
        self._zmq_pub_sockets = {key.value: self._zmq_context.socket(zmq.PUB) for key in
                                 self.TxSocket}  # type: Dict[str, zmq.Socket]
        self._zmq_sub_sockets = {key.value: self._zmq_context.socket(zmq.SUB) for key in
                                 self.RxSocket}  # type: Dict[str, zmq.Socket]
        self._boot_zmq()

        # Flight controller connection status
        self._fcs_connected = TimedParameter(bool, initial_value=False, timeout=0.5)

        # Data queues
        self._tx_queue = Queue()  # type: Queue[IParameter]
        self._rx_queue = Queue()  # type: Queue[IParameter]

    def kill(self) -> None:
        """
        Kills the drone simulation thread
        Returns:
            None
        """
        self._event_signals[self.Signals.KILL].set()
        logger.debug("Drone kill signal set")

    def run(self) -> None:
        logger.info("Executing the SimConnection thread")
        while not self._event_signals[self.Signals.KILL].is_set():
            self._rx_message_pump()
            self._tx_message_pump()
            sleep(self._pump_rate)

        logger.info("Exiting the program")

    def transmit(self, data: IParameter) -> None:
        """
        Transmits a piece of data to the flight software
        Args:
            data: Parameter instance to be transmitted

        Returns:
            None
        """
        self._tx_queue.put(data, block=True, timeout=0.05)

    def receive(self) -> Union[IParameter, None]:
        """
        Receives data from the RX queue
        Returns:
            IParameter or None
        """
        try:
            return self._rx_queue.get_nowait()
        except Empty:
            return None

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
        # Receive data until heart beat is found a few times, or timeout
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
        for socket in self._zmq_pub_sockets.keys():
            if socket not in cfg['port'].keys():
                logger.error("Missing port configuration for {}".format(socket))
            bind_to = "{}:{}".format(port_format, cfg['port'][socket])
            self._zmq_pub_sockets[socket].bind(bind_to)
            logger.debug("Bind pub socket [{}] to {}".format(socket, bind_to))

        # Configure the SUB sockets
        for socket in self._zmq_sub_sockets.keys():
            if socket not in cfg['port'].keys():
                logger.error("Missing port configuration for {}".format(socket))

            # Do the connection
            conn_to = "{}:{}".format(port_format, cfg['port'][socket])
            self._zmq_sub_sockets[socket].connect(conn_to)
            logger.debug("Connect sub socket [{}] to {}".format(socket, conn_to))

            # Subscribe to various topics
            for topic in self._data_map.get_socket_subscriber_list(socket):
                self._zmq_sub_sockets[socket].setsockopt_string(zmq.SUBSCRIBE, topic.value)
                logger.debug("Subscribed socket {} to topic {}".format(socket, topic.value))

    def _rx_message_pump(self) -> None:
        """
        Process incoming messages from the flight software
        Returns:
            None
        """
        # Check each socket for available data
        for socket in self._zmq_sub_sockets.keys():
            more_data = True
            while more_data:
                try:
                    # Receive the next message from the socket. It's expected that each message
                    # is a key value pair of {topic, data}.
                    msg = self._zmq_sub_sockets[socket].recv_multipart(flags=zmq.NOBLOCK)
                    if len(msg) != 2 or not isinstance(msg, list):
                        raise zmq.ZMQError()

                    # Update the connection status if the heart beat is sent
                    if msg[0].decode('utf-8') == self.RxTopics.HEARTBEAT.value:
                        self._fcs_connected.update(True)
                        continue

                    # Reconstruct the data into the expected type
                    param = self._parameter_rx_factory(topic=self.RxTopics(msg[0]), serialized_data=msg[1])

                    # Push to the queue
                    if isinstance(param, IParameter):
                        self._rx_queue.put(item=param, block=True, timeout=0.1)

                except (zmq.ZMQError, ValueError) as e:
                    more_data = False

    def _tx_message_pump(self) -> None:
        """
        Pulls items from the transmit queue and pushes it through the ZMQ connection
        Returns:
            None
        """
        while not self._tx_queue.empty():
            try:
                param = self._tx_queue.get_nowait()
                if not param:
                    continue

                socket = self._data_map.get_socket_from_parameter(param.id)
                topic = self._data_map.get_topic_from_parameter(param.id)

                encoded_topic = topic.value.encode('utf-8')
                serialized_data = param.serialize()
                self._zmq_pub_sockets[socket.value].send_multipart([encoded_topic, serialized_data])
                logger.trace("Send -- Topic: {}".format(topic.value))
            except Exception as e:
                logger.error("{} exception: {}".format(type(e).__name__, str(e)))

    def _parameter_rx_factory(self, topic: RxTopics, serialized_data: str) -> Union[IParameter, None]:
        """
        Converts serialized data back into the appropriate registered type
        Args:
            topic: Which topic data was received under
            serialized_data: The raw data from the topic

        Returns:
            A parameter class containing the data else None if not convertible
        """
        new_object = self._data_map.get_param_type_from_topic(topic)
        if not new_object:
            logger.error("No message type associated with topic {}".format(topic))
            return None

        if not new_object.deserialize(serialized_data):
            logger.error("Failed to convert data for type {} on topic {}".format(type(new_object), topic))

        return new_object

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


class SimData:
    """ A collection of mappings for data passed around through the sim """

    def __init__(self):
        self._mapping = {
            SimConnection.TxSocket.SIM_INTERNAL: {
                SimConnection.TxTopics.HEARTBEAT: {
                    "direction": SimConnection.DataFlow.TX,
                    "param_id": ParameterID.HEARTBEAT,
                    "param_type": HeartBeatData
                }
            },
            SimConnection.TxSocket.SENSOR: {
                SimConnection.TxTopics.GYRO_DATA: {
                    "direction": SimConnection.DataFlow.TX,
                    "param_id": ParameterID.GYRO_DATA,
                    "param_type": GyroData
                },
                SimConnection.TxTopics.ACCEL_DATA: {
                    "direction": SimConnection.DataFlow.TX,
                    "param_id": ParameterID.ACCEL_DATA,
                    "param_type": AccelData
                },
                SimConnection.TxTopics.MAG_DATA: {
                    "direction": SimConnection.DataFlow.TX,
                    "param_id": ParameterID.MAG_DATA,
                    "param_type": MagData
                }
            },
            SimConnection.RxSocket.SIM_INTERNAL: {
                SimConnection.RxTopics.HEARTBEAT: {
                    "direction": SimConnection.DataFlow.RX,
                    "param_id": ParameterID.HEARTBEAT,
                    "param_type": HeartBeatData
                }
            },
            SimConnection.RxSocket.SYS_CONTROL: {},
            SimConnection.RxSocket.USER_INPUT: {}
        }

    def get_socket_from_parameter(self, param_id: ParameterID) -> SimConnection.TxSocket:
        """
        Gets the socket associated with a parameter type
        Args:
            param_id: The parameter to look up

        Returns:
            Which socket the parameter is transmitted or received on
        """
        for socket in self._mapping.keys():
            for topic in self._mapping[socket].keys():
                if self._mapping[socket][topic]['param_id'] == param_id:
                    return socket

    def get_topic_from_parameter(self, param_id: ParameterID) -> Union[SimConnection.TxTopics, SimConnection.RxTopics]:
        """
        Finds the topic associated with a parameter type
        Args:
            param_id: The parameter to look up

        Returns:
            Which topic the parameter is transmitted or received on
        """
        for socket in self._mapping.keys():
            for topic in self._mapping[socket].keys():
                if self._mapping[socket][topic]['param_id'] == param_id:
                    return topic

    def get_param_type_from_topic(self, topic: Union[SimConnection.RxTopics, SimConnection.TxTopics]) -> Union[
        None, IParameter]:
        """
        Finds the data type associated with a topic
        Args:
            topic: The topic to look up

        Returns:
            Core protocol buffer type that understands how to translate network data
        """
        for socket in self._mapping.keys():
            if topic in self._mapping[socket].keys():
                # This creates a new instance of the class type stored in the mapping
                return self._mapping[socket][topic]['param_type']()

    def get_socket_subscriber_list(self, socket_id: Union[SimConnection.RxSocket, str]) -> List[SimConnection.RxTopics]:
        """
        Gets all topics a given socket is subscribed to
        Args:
            socket_id: Which socket to look up

        Returns:
            List of subscribed topics
        """
        if isinstance(socket_id, str):
            sid = SimConnection.RxSocket(socket_id)
        else:
            sid = socket_id

        topic_list = []
        for topic in self._mapping[sid].keys():
            if isinstance(topic, SimConnection.RxTopics):
                topic_list.append(topic)

        return topic_list

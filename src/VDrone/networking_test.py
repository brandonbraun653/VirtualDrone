# **********************************************************************************************************************
#   FileName:
#       networking_test.py
#
#   Description:
#       Build up a simple network test to ensure that the system is communicating ok
#
#   4/13/21 | Brandon Braun | brandonbraun653@gmail.com
# **********************************************************************************************************************

import signal
import random
import time

from pathlib import Path
from threading import Event

import numpy as np
from VDrone.parameters import *
from VDrone.database import *

main_loop_kill = Event()


def sig_int_handler(signum, frame):
    main_loop_kill.set()


def main() -> None:
    # Register the system teardown functionality
    main_loop_kill.clear()
    signal.signal(signal.SIGINT, sig_int_handler)

    db = ParameterDatabase()
    db.create(entry=Entry(param_id=ParameterID.GYRO_DATA, param_data=GyroData(timeout=0.5)))
    db.set(param_id=ParameterID.GYRO_DATA, new_value=np.zeros((3, 1)))
    my_data = db.get(param_id=ParameterID.GYRO_DATA)
    print(my_data)

    while not main_loop_kill.is_set():
        # topic = b'accel'
        #
        # data = ahrs_pb2.GyroSample()
        # data.x = random.uniform(-10.0, 10.0)
        # data.y = random.uniform(-10.0, 10.0)
        # data.z = random.uniform(-10.0, 10.0)
        #
        # # socket.send(topic)
        # socket.send_multipart([topic, data.SerializeToString()])
        # print("Sent [{}, {}]".format(topic, data))
        time.sleep(0.1)

    print("Exiting the 'sim'")


if __name__ == '__main__':
    main()

# **********************************************************************************************************************
#   FileName:
#       networking_test.py
#
#   Description:
#       Build up a simple network test to ensure that the system is communicating ok
#
#   4/13/21 | Brandon Braun | brandonbraun653@gmail.com
# **********************************************************************************************************************

import sys
import signal
import numpy as np
from loguru import logger
from pathlib import Path
from threading import Event
from VDrone.connection import SimConnection
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
    gyro_data = db.get_param(param_id=ParameterID.GYRO_DATA)

    conn = SimConnection()
    conn.start()
    conn.connect(timeout=5.0)

    while not main_loop_kill.is_set():
        conn.transmit(gyro_data)
        time.sleep(1)

    conn.kill()
    conn.join()
    print("Exiting the 'sim'")


if __name__ == '__main__':
    logger.remove()
    logger.add(sys.stdout, level="TRACE")
    main()

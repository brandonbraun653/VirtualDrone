import zmq
import json
import signal
import random
import time
import msgpack

from pathlib import Path
from threading import Event


main_loop_kill = Event()

def get_root(current: Path, root: str) -> Path:
  """ Recursively finds the desired root path

  Args:
      current (Path): Starting path to search from
      root (str): Stem inside the path

  Returns:
      Path: The found path or the system drive mount point
  """
  if current.stem == root or current.is_mount():
    return current
  else:
    return get_root(current.parent)


def parse_json(file: Path):
  """Parses a given json file into a dictionary

  Args:
      file (Path): The JSON file to be parsed
  """
  with file.open() as f:
    return json.load(f)


def sig_int_handler(signum, frame):
  main_loop_kill.set()


def main() -> None:
  project_root = get_root(Path.cwd(), "Valkyrie")
  json_cfg = parse_json(Path(project_root, 'src', 'cfg', 'sim', 'ports.json'))

  gyro_port = json_cfg['base_port'] + json_cfg['sensors']['gyroscope']
  context = zmq.Context()
  socket = context.socket(zmq.PUB)
  socket.bind("tcp://127.0.0.1:{}".format(gyro_port))
  print("Bound to port: {}".format(gyro_port))

  main_loop_kill.clear()
  signal.signal(signal.SIGINT, sig_int_handler)

  while not main_loop_kill.is_set():
    topic = b'gyro_x'
    data = random.uniform(-10.0, 10.0)

    # socket.send(topic)
    socket.send_multipart([topic, msgpack.packb(data, use_bin_type=True)])
    print("Sent [{}, {}]".format(topic, data))
    time.sleep(1)

  print("Exiting the 'sim'")




if __name__ == '__main__':
  main()
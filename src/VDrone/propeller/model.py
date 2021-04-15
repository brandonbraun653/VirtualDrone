# **********************************************************************************************************************
#   FileName:
#       model.py
#
#   Description:
#       Various model types for quadcopter propellers
#
#   4/12/21 | Brandon Braun | brandonbraun653@gmail.com
# **********************************************************************************************************************
import numpy as np
from VDrone.propeller.abstract_propeller import IPropeller


class StandardProp(IPropeller):

    def __init__(self):
        super().__init__()
        self.set_tf_input_size(shape=(1, 0))
        self.set_tf_output_size(shape=(1, 0))

    def tf_evaluate(self, sig_in: np.ndarray, dt: float = 0.0) -> np.ndarray:
        return sig_in

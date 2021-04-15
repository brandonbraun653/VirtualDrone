# **********************************************************************************************************************
#   FileName:
#       interface.py
#
#   Description:
#       High level system interface for modeling transfer functions
#
#   4/10/21 | Brandon Braun | brandonbraun653@gmail.com
# **********************************************************************************************************************

import numpy as np


class TransferFunction:

    def __init__(self):
        self._in_size = ()
        self._out_size = ()

    def set_tf_input_size(self, shape: tuple) -> None:
        """
        Set the transfer function's input matrix shape
        Args:
            shape: Shape of the input matrix to the transfer function (row, column)

        Returns:
            None
        """
        self._in_size = shape

    def set_tf_output_size(self, shape: tuple) -> None:
        """
        Sets the transfer function's output matrix shape

        Args:
            shape: Shape of the output matrix from the transfer function

        Returns:
            None
        """
        self._out_size = shape

    def tf_evaluate(self, sig_in: np.ndarray, dt: float = 0.0) -> np.ndarray:
        """
        Evaluates the transfer function for the given input
        Args:
            sig_in: Input signal to evaluate
            dt: Time step to evaluate over

        Returns:
            Output of the transfer function
        """
        raise NotImplementedError

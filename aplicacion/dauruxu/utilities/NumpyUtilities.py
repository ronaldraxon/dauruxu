import numpy as np


class NumpyUtilities:

    @staticmethod
    def generate_sequence_of_int_numbers(start_number, end_number, step, close_interval):
        if close_interval:
            return np.arange(start_number, end_number+1, step)
        else:
            return np.arange(start_number, end_number, step)

    @staticmethod
    def convert_integer_list_to_integer_np_array(integer_list):
        return np.asarray(integer_list, dtype=np.int32)

    @staticmethod
    def convert_float_list_to_float32_np_array(float_list):
        return np.asarray(float_list, dtype=np.float32)

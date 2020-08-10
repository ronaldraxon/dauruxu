"""
c4ufb.utilities.EncodingUtilities.py
====================================
module for data request and training schedules
"""


import json
import base64
import io
import ast
from joblib import dump, load


class EncodingUtilities:

    @staticmethod
    def create_bytes_buffer():
        return io.BytesIO()

    @staticmethod
    def get_bytes_stream_from_bytes_buffer(buffer):
        return buffer.getvalue()

    @staticmethod
    def get_bytes_buffer_from_bytes_stream(bytes_stream):
        return io.BytesIO(bytes_stream)

    @staticmethod
    def dump_object_into_byte_buffer_with_joblib(obj, buffer):
        dump(obj, buffer)
        return buffer

    @staticmethod
    def load_object_from_buffer_with_joblib(buffer):
        return load(buffer)

    @staticmethod
    def encode_string_to_json(obj):
        return json.loads(obj)

    @staticmethod
    def decode_json_to_string(obj):
        return json.dumps(obj)

    @staticmethod
    def list_string_to_list(str_list):
        return ast.literal_eval(str_list)

    @staticmethod
    def encode_to_base64(obj):
        return base64.b64encode(obj)

    @staticmethod
    def decode_from_base64(obj):
        return base64.b64decode(obj)

    # model to bytes_stream methods

    @staticmethod
    def model_to_byte_stream(model):
        buffer = EncodingUtilities.create_bytes_buffer()
        dump(model, buffer)
        return buffer

    @staticmethod
    def get_buffer_value(buffer):
        return buffer.getvalue()

    @staticmethod
    def close_buffer(buffer):
        buffer.close()

    @staticmethod
    def bytes_stream_to_buffer(bytes_stream):
        buffer = EncodingUtilities.get_bytes_buffer_from_bytes_stream(bytes_stream)
        return buffer

    @staticmethod
    def buffer_to_model(buffer):
        return load(buffer)

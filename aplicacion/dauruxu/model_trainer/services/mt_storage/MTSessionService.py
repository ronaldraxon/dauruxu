"""
model_trainer.services.MTSessionService.py
==========================================
Module for called .
call
"""
from model_trainer.models.mt_storage.MTSession import MTSession
from utilities.PandasUtilities import PandasUtilities as Pu
from utilities.EncodingUtilities import EncodingUtilities as Eu


class MTSessionService:

    @staticmethod
    def create_new_mt_point(code, clean_data):
        mt_point = MTSession()
        mt_point.code = code
        mt_point.clean_data = Eu.encode_string_to_json(clean_data)
        mt_point.save()

    @staticmethod
    def get_mt_point_clean_data_as_data_frame(code):
        mt_session = MTSession.objects.filter(code=code).first()
        return Pu.convert_json_string_to_pandas_data_frame(mt_session.clean_data)

    @staticmethod
    def delete_mt_point_by_code(code):
        MTSession.objects.filter(code=str(code)).delete()


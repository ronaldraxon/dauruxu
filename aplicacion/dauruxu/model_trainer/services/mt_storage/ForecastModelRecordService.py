"""
model_trainer.services.ForecastModelRecordService.py
====================================================
Module for called .
call
"""

from model_trainer.models.mt_storage.ForecastModelRecord import ForecastModelRecord, ModelStatus
from utilities.EncodingUtilities import EncodingUtilities as Eu
from django.utils import timezone


class ForecastModelRecordService:

    @staticmethod
    def create_new_model_record(code, input_variables, response_variable, model_task_type):
        forecast_model_db_record = ForecastModelRecord()
        forecast_model_db_record.code = code
        forecast_model_db_record.training_request_datetime = timezone.datetime.now()
        forecast_model_db_record.model_status = ModelStatus.TO_TRAIN.value
        forecast_model_db_record.model_task_type = model_task_type
        forecast_model_db_record.input_variables = input_variables
        forecast_model_db_record.response_variable = response_variable
        forecast_model_db_record.save()
        return str(forecast_model_db_record.model_id)

    @staticmethod
    def get_model_info_by_code(code):
        return ForecastModelRecord.objects. \
            filter(code=code, is_last_model=True).first()

    @staticmethod
    def set_model_record_status_to_active_and_last_model(model_id):
        model_record = ForecastModelRecord.objects.get(model_id=model_id)
        model_record.model_status = ModelStatus.ACTIVE.value
        model_record.is_last_model = True
        model_record.save()

    @staticmethod
    def set_training_start_in_model_record(model_id):
        model_record = ForecastModelRecord.objects.get(model_id=model_id)
        model_record.training_start_datetime = timezone.datetime.now()
        model_record.model_status = ModelStatus.IN_TRAINING.value
        model_record.save()

    @staticmethod
    def set_training_end_time_in_model_record(model_id):
        model_record = ForecastModelRecord.objects.get(model_id=model_id)
        model_record.training_end_datetime = timezone.datetime.now()
        model_record.model_status = ModelStatus.TRAINED.value
        model_record.save()

    @staticmethod
    def get_input_variables_by_uuid(model_id):
        return ForecastModelRecord.objects.get(model_id=model_id).input_variables

    @staticmethod
    def persist_model(forecast_model, model_id):
        model_buffer = Eu.model_to_byte_stream(forecast_model.model_base)
        model_stream = Eu.get_buffer_value(model_buffer)
        record = ForecastModelRecord.objects.get(model_id=model_id)
        record.model_base = model_stream
        record.main_score = forecast_model.main_score
        record.model_type = forecast_model.model_type
        record.is_rfe_model = forecast_model.rfe_model
        record.metrics = forecast_model.test_score
        record.model_best_params = forecast_model.process.best_params_
        record.model_grid_search_params = forecast_model.params_grid
        record.save()
        Eu.close_buffer(model_buffer)

    @staticmethod
    def retrieve_active_model_record_by_code(code):
        return ForecastModelRecord.objects.filter(code=code,
                                                  is_last_model=True).first()

    @staticmethod
    def exist_an_active_model_by_code(code):
        return ForecastModelRecord.objects.filter(code=code, is_last_model=True).exists()

    @staticmethod
    def retrieve_functional_model_by_uuid(model_id):
        model_record = ForecastModelRecord.objects.get(model_id=model_id)
        model_stream = model_record.model_base
        model_buffer = Eu.bytes_stream_to_buffer(model_stream)
        model = Eu.buffer_to_model(model_buffer)
        Eu.close_buffer(model_buffer)
        return model

    @staticmethod
    def retrieve_functional_model(code):
        model_record = ForecastModelRecord.objects. \
            filter(code=code, is_last_model=True).first()
        model_stream = model_record.model_base
        model_buffer = Eu.bytes_stream_to_buffer(model_stream)
        model = Eu.buffer_to_model(model_buffer)
        Eu.close_buffer(model_buffer)
        return model

    @staticmethod
    def update_existing_forecast_model_to_deprecated(code):
        model_record = ForecastModelRecordService.retrieve_active_model_record_by_code(code)
        model_record.model_status = ModelStatus.DEPRECATED.value
        model_record.is_last_model = False

    @staticmethod
    def get_input_variables_list_by_uuid(model_id):
        return Eu.list_string_to_list(ForecastModelRecord.objects.get(model_id=model_id).input_variables)

    @staticmethod
    def get_response_variable_by_uuid(model_id):
        return ForecastModelRecord.objects.get(model_id=model_id).response_variable

    @staticmethod
    def get_model_record_by_uuid(model_id):
        return ForecastModelRecord.objects.get(model_id=model_id)

    @staticmethod
    def get_model_task_type_by_uuid(model_id):
        return ForecastModelRecord.objects.get(model_id=model_id).model_task_type

    @staticmethod
    def delete_model_records_by_code(code):
        ForecastModelRecord.objects.filter(code=str(code)).delete()

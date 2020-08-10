"""
model_trainer.services.MTPropertiesService.py
=============================================
Module for called .
call
"""
from background_task.models import Task
from django.db.utils import ProgrammingError

from model_trainer.models.configuration.MTProperties import MTProperties
from apps_administration.services.PropertyService import PropertyService
from utilities.PandasUtilities import PandasUtilities as Pu

import logging


logger = logging.getLogger(__name__)

mt_properties = MTProperties()


class MTPropertiesService:

    @staticmethod
    def get_types_of_models_to_generate():
        return mt_properties.MODELS_TO_TRAIN

    @staticmethod
    def get_rfe_enabling_flag():
        return mt_properties.ENABLE_RFE

    @staticmethod
    def get_test_data_size_percentage():
        return mt_properties.TEST_DATA_SET_SIZE

    @staticmethod
    def get_shuffle_seed():
        return mt_properties.DATA_SHUFFLE_SEED

    @staticmethod
    def get_exploration_type():
        return mt_properties.EXPLORATION_TYPE

    @staticmethod
    def get_cross_validation_folds():
        return mt_properties.CROSS_VALIDATION_FOLDS

    @staticmethod
    def get_model_check_period():
        return mt_properties.CHECK_MODEL_PERFORMANCE_NUM

    @staticmethod
    def get_grid_params_attribute_with_key(params_key):
        return getattr(mt_properties, params_key)

    @staticmethod
    def retrieve_model_training_schedule_by_code(code):
        return Task.objects.filter(verbose_name=str(code))

    @staticmethod
    def delete_background_tasks_by_code(code):
        Task.objects.filter(verbose_name=str(code)).delete()

    @staticmethod
    def request_and_update_mt_general_properties(model_trainer_params):
        properties = Pu.convert_django_query_set_to_pandas_data_frame(model_trainer_params)
        properties = Pu.set_pandas_data_frame_index(properties, 'key')
        model_checking_time_period = PropertyService.get_model_checking_time_period()
        mt_properties.update_property_values(properties, model_checking_time_period)


try:
    MTPropertiesService.request_and_update_mt_general_properties(PropertyService.get_model_trainer_properties())
    logger.info("Model Trainer properties updated successful")
except ProgrammingError:
    logger.warning("Model Trainer properties was initialized with default values")

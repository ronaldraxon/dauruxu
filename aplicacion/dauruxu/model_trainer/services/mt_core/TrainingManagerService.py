"""
model_trainer_services.TrainingManagerService.py
==========================================
Facade module for the training management
"""

from model_trainer.services.mt_core.TrainingAssistant import TrainingAssistant as Ta
from model_trainer.models.mt_core.ForecastModel import ForecastModel as Fm
import logging

logger = logging.getLogger(__name__)


class TrainingManager:

    @staticmethod
    def create_async_regression_training_for_new_point(code, input_variables, response_variable, clean_data):
        Ta.register_new_point_and_schedule_training(code, input_variables,
                                                    response_variable, clean_data, Fm.ModelTaskType.REGRESSION.value)

    @staticmethod
    def get_model_info_by_code(code):
        Ta.get_model_info_by_code(code)

    @staticmethod
    def create_sync_regression_training_for_new_point(code, input_variables, response_variable, clean_data):
        Ta.register_new_point_and_request_train(code, input_variables, response_variable, clean_data)

    @staticmethod
    def retrain_existing_regression_model_with_code(code, grid_params):
        Ta.request_train_for_existing_code(code, grid_params)

    @staticmethod
    def get_scheduled_training_by_code(code):
        return Ta.retrieve_model_training_schedule_by_code(code)

    @staticmethod
    def delete_model_by_code(code):
        Ta.delete_point(code)

    @staticmethod
    def update_model_trainer_general_params(model_trainer_params):
        Ta.update_model_trainer_general_properties(model_trainer_params)
        pass

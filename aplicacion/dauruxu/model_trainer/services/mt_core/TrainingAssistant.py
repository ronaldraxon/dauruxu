"""
model_trainer_services.TrainingAssistant.py
===========================================
module for data request and training schedules
"""

from model_trainer.services.mt_core.TrainingService import TrainingService
from model_trainer.services.configuration.MTPropertiesService import MTPropertiesService as PropRecord
from model_trainer.services.mt_storage.MTSessionService import MTSessionService as Mtss
from model_trainer.services.mt_storage.ForecastModelRecordService import ForecastModelRecordService as Fmrs

SCHEDULE_TO_EXECUTE_ASAP = 0


class TrainingAssistant:

    # Public methods open for the TrainingManagerService class
    @staticmethod
    def register_new_point_and_schedule_training(code, input_variables, response_variable,
                                                 clean_data, model_task_type):
        Mtss.create_new_mt_point(code, clean_data)
        model_uuid = Fmrs.create_new_model_record(code, input_variables, response_variable, model_task_type)
        TrainingAssistant.__schedule_training__(code, model_uuid, SCHEDULE_TO_EXECUTE_ASAP)

    @staticmethod
    def get_model_info_by_code(code):
        return Fmrs.get_model_info_by_code(code)

    @staticmethod
    def register_new_point_and_request_train(code, input_variables, response_variable,
                                             clean_data, model_task_type):
        Mtss.create_new_mt_point(code, clean_data)
        model_uuid = Fmrs.create_new_model_record(code, input_variables, response_variable, model_task_type)
        TrainingService.generate_best_model_without_schedule(code, model_uuid)

    @staticmethod
    def request_train_for_existing_code(code, grid_params):
        pass

    @staticmethod
    def retrieve_model_training_schedule_by_code(code):
        return PropRecord.retrieve_model_training_schedule_by_code(code)

    @staticmethod
    def delete_point(code):
        Fmrs.delete_model_records_by_code(code)
        Mtss.delete_mt_point_by_code(code)
        PropRecord.delete_background_tasks_by_code(code)

    @staticmethod
    def update_model_trainer_general_properties(model_trainer_params):
        PropRecord.request_and_update_mt_general_properties(model_trainer_params)

    @staticmethod
    def __schedule_training__(code, model_uuid, next_session):
        TrainingService.generate_best_model_with_schedule(code,
                                                          model_uuid=model_uuid,
                                                          verbose_name=code,
                                                          schedule=next_session)



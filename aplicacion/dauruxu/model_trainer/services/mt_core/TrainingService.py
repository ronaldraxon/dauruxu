"""
model_trainer_services.TrainingAssistant.py
===========================================
module for model training
"""
from enum import Enum
from background_task import background
from model_trainer.services.configuration.MTPropertiesService import MTPropertiesService as PropRecord
from model_trainer.services.mt_storage.MTSessionService import MTSessionService as Mtss
from model_trainer.services.mt_storage.ForecastModelRecordService import ForecastModelRecordService as Fmrs
from model_trainer.models.mt_core.ForecastModelFactory import ForecastModelFactory as Mf
from sklearn.model_selection import train_test_split

import logging

logger = logging.getLogger(__name__)


class ExplorationType(Enum):
    FIXED = "FIXED"
    SYSTEMATIC = "SYSTEMATIC"


class TrainingService:

    @staticmethod
    @background(queue='model-training-queue')
    def generate_best_model_with_schedule(code, model_id):
        TrainingService.process_model_creation(code, model_id)

    @staticmethod
    def generate_best_model_without_schedule(code, model_id):
        TrainingService.process_model_creation(code, model_id)

    @staticmethod
    def process_model_creation(code, model_id):
        Fmrs.set_training_start_in_model_record(model_id)
        models_to_train = TrainingService.get_empty_model_shells(PropRecord.get_types_of_models_to_generate(),
                                                                 Fmrs.get_model_task_type_by_uuid(model_id),
                                                                 PropRecord.get_rfe_enabling_flag())
        train_inputs, test_inputs, train_target, test_target = TrainingService.get_training_and_test_data(code, model_id)
        best_model = TrainingService.train_and_evaluate_models(models_to_train, train_inputs, train_target, test_inputs,
                                                               test_target, model_id)
        TrainingService.persist_model(best_model, code, model_id)

    @staticmethod
    def get_empty_model_shells(model_type_list, model_task_type, rfe_enabled):
        model_shells = list()
        for model_type in model_type_list:
            model = TrainingService.create_model_shell(model_type, model_task_type, False)
            model_shells.append(model)
            if rfe_enabled:
                rfa_model = TrainingService.create_model_shell(model_type, model_task_type, True)
                model_shells.append(rfa_model)
        return model_shells

    @staticmethod
    def create_model_shell(model_type, model_task_type, create_with_rfe):
        model = Mf.create_model_shell(model_type, model_task_type, create_with_rfe)
        if create_with_rfe:
            model.params_grid = dict()
        else:
            model.params_grid = PropRecord.get_grid_params_attribute_with_key(model.params_key)
        model.prepare_grid_search(cross_v=PropRecord.get_cross_validation_folds())
        return model

    @staticmethod
    def get_training_and_test_data(code, model_id, ):
        clean_data = Mtss.get_mt_point_clean_data_as_data_frame(code)
        return train_test_split(clean_data[Fmrs.get_input_variables_list_by_uuid(model_id)],
                                clean_data[Fmrs.get_response_variable_by_uuid(model_id)],
                                test_size=PropRecord.get_test_data_size_percentage(),
                                random_state=PropRecord.get_shuffle_seed(), shuffle=True)

    @staticmethod
    def train_and_evaluate_models(models_to_train, train_inputs, train_target, test_inputs, test_target, model_id):
        if PropRecord.get_exploration_type() == ExplorationType.FIXED.name:
            logger.info("performing fixed exploration training for model record {0}".format(model_id))
            best_model = TrainingService.perform_fixed_exploration_training(models_to_train, train_inputs,
                                                                            train_target, test_inputs, test_target)
        else:
            logger.info("performing systematic exploration training for model record {0}".format(model_id))
            best_model = TrainingService.perform_systematic_exploration_training(models_to_train, train_inputs,
                                                                                 train_target, test_inputs, test_target)
        Fmrs.set_training_end_time_in_model_record(model_id)
        return best_model

    @staticmethod
    def perform_fixed_exploration_training(models_to_train, train_inputs, train_target, test_inputs, test_target):
        best_model = None
        higher_score = 0
        for model in models_to_train:
            TrainingService.fit_and_eval_model(model, train_inputs, train_target, test_inputs, test_target)
            if model.main_score > higher_score:
                higher_score = model.main_score
                best_model = model
        return best_model

    @staticmethod
    def perform_systematic_exploration_training(models_to_train, train_inputs, train_target, test_inputs, test_target):
        higher_score = 0
        best_model = None
        for model in models_to_train:
            TrainingService.fit_and_eval_model(model, train_inputs, train_target, test_inputs, test_target)
            if model.main_score > higher_score:
                higher_score = model.main_score
                best_model = model
            if model.main_score >= PropRecord.get_grid_params_attribute_with_key(model.params_key):
                break
        return best_model

    @staticmethod
    def fit_and_eval_model(model, train_inputs, train_target, test_inputs, test_target):
        model.fit_model(train_inputs=train_inputs, train_target=train_target)
        model.eval_model(train_inputs=train_inputs, train_target=train_target,
                         test_inputs=test_inputs, test_target=test_target)

    @staticmethod
    def compare_models_main_scores_and_get_best(scores_list):
        higher_score = 0
        item_index = -1
        selected_index = 0
        for score in scores_list:
            item_index = item_index + 1
            if score > higher_score:
                higher_score = score
                selected_index = item_index
        return selected_index

    @staticmethod
    def persist_model(model, code, model_id):
        Fmrs.persist_model(model, model_id)
        if Fmrs.exist_an_active_model_by_code(code=code):
            Fmrs.update_existing_forecast_model_to_deprecated(code=code)
            Fmrs.set_model_record_status_to_active_and_last_model(model_id)
        else:
            Fmrs.set_model_record_status_to_active_and_last_model(model_id)
        # Agendar próximo
        TrainingService.generate_best_model_with_schedule(code,
                                                          model_id=model_id,
                                                          verbose_name=code,
                                                          schedule=0)
        # schedule=PropRecord.get_model_check_period())

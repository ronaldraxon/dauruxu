"""
model_trainer.models.mt_core.ForecastModelFactory.py
====================================================
Modulo para la fabrica del  ForecastModel
"""
from model_trainer.models.mt_core.LinearModel import LinearModel
from model_trainer.models.mt_core.RandomForestModel import RandomForestModel
from model_trainer.models.mt_core.XGBTreeModel import XGBTreeModel
from model_trainer.models.mt_core.SVMModel import SVMModel
from model_trainer.models.mt_core.ForecastModel import ForecastModel


class ForecastModelFactory:
    """
     Clase para el manejo de la fabrica del ForecastModel
    """

    @staticmethod
    def create_model_shell(model_type, model_task_type, create_with_rfe):
        # Colocar excepeción por si no comparece con algun tipo
        if model_type == ForecastModel.ModelType.LINEAR.name:
            model_shell = LinearModel()
            model_shell.create_model(model_task_type, create_with_rfe)
            return model_shell
        if model_type == ForecastModel.ModelType.RANDOM_FOREST.name:
            model_shell = RandomForestModel()
            model_shell.create_model(model_task_type, create_with_rfe)
            return model_shell
        if model_type == ForecastModel.ModelType.XG_BOOST_TREE.name:
            model_shell = XGBTreeModel()
            model_shell.create_model(model_task_type, create_with_rfe)
            return model_shell
        if model_type == ForecastModel.ModelType.SVM.name:
            model_shell = SVMModel()
            model_shell.create_model(model_task_type, create_with_rfe)
            return model_shell

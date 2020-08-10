"""
model_trainer.models.mt_core.SVMModel.py
========================================
Modulo para el modelo de la prediccion
"""

from sklearn.svm import LinearSVC, LinearSVR
from model_trainer.models.mt_core.ForecastModel import ForecastModel


class SVMModel(ForecastModel):
    """
Clase  para la administracion y la creacion del modelo
"""
    def create_model(self, model_task_type, rfe_enable):
        self._model_type = self.ModelType.SVM.name
        if model_task_type == self.ModelTaskType.REGRESSION.name:
            self._initialize_model_(self.ModelTaskType.REGRESSION, LinearSVR(),
                                    self.GridSearchParamKey.SVM_REGRESSION_GS_PARAMS.value, rfe_enable)
        else:
            self._initialize_model_(self.ModelTaskType.CLASSIFICATION, LinearSVC(),
                                    self.GridSearchParamKey.SVM_CLASSIFICATION_GS_PARAMS.value, rfe_enable)

    def fit_model(self, train_inputs, train_target):
        self._process.fit(train_inputs, train_target)
        self._model_base = self._process.best_estimator_

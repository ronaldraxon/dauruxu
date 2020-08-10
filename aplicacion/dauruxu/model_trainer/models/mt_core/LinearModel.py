"""
model_trainer.models.mt_core.ForecastModel.py
============================================
Modulo para el modelo de la prediccion Lineal
"""
from sklearn.linear_model import LinearRegression, SGDClassifier
from model_trainer.models.mt_core.ForecastModel import ForecastModel


class LinearModel(ForecastModel):
    """
     Clase para implementar el modelo lineal
    """
    def create_model(self, model_task_type, rfe_enable):
        self._model_type = self.ModelType.LINEAR.name
        if model_task_type == self.ModelTaskType.REGRESSION.name:
            self._initialize_model_(self.ModelTaskType.REGRESSION, LinearRegression(),
                                    self.GridSearchParamKey.LINEAR_REGRESSION_GS_PARAMS.value, rfe_enable)
        else:
            self._initialize_model_(self.ModelTaskType.CLASSIFICATION, SGDClassifier(),
                                    self.GridSearchParamKey.LINEAR_CLASSIFICATION_GS_PARAMS.value, rfe_enable)

    def fit_model(self, train_inputs, train_target):
        self._process.fit(train_inputs, train_target)
        self._model_base = self._process.best_estimator_

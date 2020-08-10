"""
model_trainer.models.mt_core.RandomForestModel.py
=================================================
Modulo para la prediccion del modelo de manera Randomica
"""
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from model_trainer.models.mt_core.ForecastModel import ForecastModel


class RandomForestModel(ForecastModel):

    def create_model(self, model_task_type, rfe_enable):
        self._model_type = self.ModelType.RANDOM_FOREST.name
        if model_task_type == self.ModelTaskType.REGRESSION.name:
            self._initialize_model_(self.ModelTaskType.REGRESSION, RandomForestRegressor(),
                                    self.GridSearchParamKey.RANDOM_FOREST_REGRESSION_GS_PARAMS.value, rfe_enable)
        else:
            self._initialize_model_(self.ModelTaskType.CLASSIFICATION, RandomForestClassifier(),
                                    self.GridSearchParamKey.RANDOM_FOREST_CLASSIFICATION_GS_PARAMS.value, rfe_enable)

    def fit_model(self, train_inputs, train_target):
        self._process.fit(train_inputs, train_target.values.flatten())
        self._model_base = self._process.best_estimator_

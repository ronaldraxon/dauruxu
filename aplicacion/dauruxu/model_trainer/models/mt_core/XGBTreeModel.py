"""
model_trainer.models.mt_core.ForecastModel.py
============================================
Modulo para el modelo de prediccion con arboles de decision
"""
from xgboost import XGBClassifier, XGBRegressor
from model_trainer.models.mt_core.ForecastModel import ForecastModel


class XGBTreeModel(ForecastModel):

    def create_model(self, model_task_type, rfe_enable):
        self._model_type = self.ModelType.XG_BOOST_TREE.name
        if model_task_type == self.ModelTaskType.REGRESSION.name:
            self._initialize_model_(self.ModelTaskType.REGRESSION, XGBRegressor(),
                                    self.GridSearchParamKey.XGBOOST_TREE_REGRESSION_GS_PARAMS.value, rfe_enable)
        else:
            self._initialize_model_(self.ModelTaskType.CLASSIFICATION, XGBClassifier(),
                                    self.GridSearchParamKey.XGBOOST_TREE_CLASSIFICATION_GS_PARAMS.value, rfe_enable)

    def fit_model(self, train_inputs, train_target):
        self._process.fit(train_inputs, train_target)
        self._model_base = self._process.best_estimator_

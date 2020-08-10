"""
model_trainer.models.mt_core.ForecastModel.py
============================================
Modulo para el modelo de la prediccion
"""
import abc
from enum import Enum
from sklearn.feature_selection import RFE
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score, mean_squared_error, f1_score, accuracy_score


class ForecastModel(metaclass=abc.ABCMeta):
    _training_score = dict()
    _test_score = dict()
    _main_score = 0
    _params_grid = dict()
    _params_key = None
    _threshold_key = None
    _model_type = None
    _rfe_model = False
    _model_task_type = None
    _model_base = None
    _process = None
    _score = dict()

    @abc.abstractmethod
    def create_model(self, model_task_type, rfe_enabled):
        raise NotImplementedError

    def _initialize_model_(self, model_task_type, model, params_key, rfe_enabled):
        self._model_task_type = model_task_type
        self._model_base = model
        if rfe_enabled:
            self.create_rfe_model()
            self._rfe_model = True
        self._params_key = params_key

    def create_rfe_model(self):
        self._model_base = RFE(self._model_base)

    def prepare_grid_search(self, cross_v=3, verbosity=0):
        self._process = GridSearchCV(estimator=self._model_base,
                                     param_grid=self._params_grid, cv=cross_v, verbose=verbosity)

    @abc.abstractmethod
    def fit_model(self, train_inputs, train_target):  # Buscar la forma de arreglar los datos para que sea genérico
        raise NotImplementedError

    def predict_model(self, input_data):
        predictions = self._model_base.predict(input_data)
        return predictions

    def eval_regression_model(self, inputs, test_target):
        predicted_outputs = self.predict_model(inputs)
        r2 = r2_score(predicted_outputs, test_target)
        mse = mean_squared_error(predicted_outputs, test_target)
        return {"r2": r2, "mse": mse}

    def eval_classification_model(self, inputs, test_target):
        predicted_outputs = self.predict_model(inputs)
        accuracy = accuracy_score(predicted_outputs, test_target)
        f1 = f1_score(predicted_outputs, test_target)
        return {"accuracy": accuracy, "f1": f1}

    def eval_model(self, train_inputs, train_target, test_inputs, test_target):
        if self._model_task_type == self.ModelTaskType.REGRESSION:
            self._training_score = self.eval_regression_model(train_inputs, train_target)
            self._test_score = self.eval_regression_model(test_inputs, test_target)
            self._main_score = self._test_score.get("r2")
            self._threshold_key = "R2_THRESHOLD"
        elif self._model_task_type == self.ModelTaskType.CLASSIFICATION:
            self._training_score = self.eval_classification_model(train_inputs, train_target)
            self._test_score = self.eval_classification_model(test_inputs, test_target)
            self._main_score = self._test_score.get("accuracy")
            self._threshold_key = "ACCURACY_THRESHOLD"

    @property
    def test_score(self):
        return self._test_score

    @property
    def training_score(self):
        return self._training_score

    @property
    def threshold_key(self):
        return self._threshold_key

    @property
    def main_score(self):
        return self._main_score

    @property
    def model_base(self):
        return self._model_base

    @property
    def process(self):
        return self._process

    @property
    def model_type(self):
        return self._model_type

    @property
    def rfe_model(self):
        return self._rfe_model

    @property
    def model_task_type(self):
        return self._model_task_type

    @property
    def params_key(self):
        return self._params_key

    @property
    def params_grid(self):
        return self._params_grid

    @params_grid.setter
    def params_grid(self, params):
        self._params_grid = params

    class ModelTaskType(Enum):
        """
              Tipo de tarea para el modelo
               """
        REGRESSION = "REGRESSION"
        CLASSIFICATION = "CLASSIFICATION"

    class ModelType(Enum):
        """
        Enumeracion con el tipo de modelo a predecir
        """
        LINEAR = "Linear Model"
        RANDOM_FOREST = "Random Forest"
        SVM = "Support Vector Machine"
        XG_BOOST_TREE = "Extreme Gradient boosted tree"

    class GridSearchParamKey(Enum):
        """
            Enumeracion  con los parametros del  GridSearch
            """
        LINEAR_REGRESSION_GS_PARAMS = "LINEAR_REGRESSION_GS_PARAMS"
        RANDOM_FOREST_REGRESSION_GS_PARAMS = "RANDOM_FOREST_REGRESSION_GS_PARAMS"
        XGBOOST_TREE_REGRESSION_GS_PARAMS = "XGBOOST_TREE_REGRESSION_GS_PARAMS"
        SVM_REGRESSION_GS_PARAMS = "SVM_REGRESSION_GS_PARAMS"
        LINEAR_CLASSIFICATION_GS_PARAMS = "LINEAR_CLASSIFICATION_GS_PARAMS"
        RANDOM_FOREST_CLASSIFICATION_GS_PARAMS = "RANDOM_FOREST_CLASSIFICATION_GS_PARAMS"
        XGBOOST_TREE_CLASSIFICATION_GS_PARAMS = "XGBOOST_TREE_CLASSIFICATION_GS_PARAMS"
        SVM_CLASSIFICATION_GS_PARAMS = "SVM_CLASSIFICATION_GS_PARAMS"

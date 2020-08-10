"""
model_trainer.models.storage.MTProperties.py
============================================
Modulo Singleton para el  model_trainer. Esta clase evita varias solicitudes a apps_administration
para las  propiedades de almacenamiento adecuadas para actividades del model_trainer
"""

import ast


class MTProperties(object):

    instance = None

    class __MTProperties:
        def __init__(self):
            self.R2_THRESHOLD = 0.9
            self.ACCURACY_THRESHOLD = 0.9
            self.CROSS_VALIDATION_FOLDS = 3
            self.MODELS_TO_TRAIN = ['LINEAR']
            self.EXPLORATION_TYPE = "FIXED"
            self.LINEAR_REGRESSION_GS_PARAMS = dict()
            self.RANDOM_FOREST_REGRESSION_GS_PARAMS = dict()
            self.XGBOOST_TREE_REGRESSION_GS_PARAMS = dict()
            self.SVM_REGRESSION_GS_PARAMS = dict()
            self.LINEAR_CLASSIFICATION_GS_PARAMS = dict()
            self.RANDOM_FOREST_CLASSIFICATION_GS_PARAMS = dict()
            self.XGBOOST_TREE_CLASSIFICATION_GS_PARAMS = dict()
            self.SVM_CLASSIFICATION_GS_PARAMS = dict()
            self.ENABLE_RFE = True
            self.RFE_LENGTH = 5
            self.CHECK_MODEL_PERFORMANCE = "EVERY_7_DAYS"
            self.CHECK_MODEL_PERFORMANCE_NUM = 604800
            self.DAYS_FOR_TESTING = 7
            self.TEST_DATA_SET_SIZE = 0.20
            self.DATA_SHUFFLE_SEED = 1920

        def __str__(self):
            return '{0!r}'.format(self)

        def update_property_values(self, properties, model_checking_time_period):
            """Actualiza los valores de la clase singleton
                   - **parameters**::
                        :param properties:Pandas DataFrame containing property values
                   """
            self.R2_THRESHOLD = float(properties.loc['R2_THRESHOLD'].value)
            self.ACCURACY_THRESHOLD = float(properties.loc['ACCURACY_THRESHOLD'].value)
            self.CROSS_VALIDATION_FOLDS = int(properties.loc['CROSS_VALIDATION_FOLDS'].value)
            self.MODELS_TO_TRAIN = list(properties.loc['MODELS_TO_TRAIN'].value.split(" "))
            self.EXPLORATION_TYPE = properties.loc['EXPLORATION_TYPE'].value
            self.LINEAR_REGRESSION_GS_PARAMS = ast.literal_eval(properties.loc['LINEAR_REGRESSION_GS_PARAMS'].value)
            self.RANDOM_FOREST_REGRESSION_GS_PARAMS = ast.literal_eval(properties.loc['RANDOM_FOREST_REGRESSION_GS_PARAMS'].value)
            self.XGBOOST_TREE_REGRESSION_GS_PARAMS = ast.literal_eval(properties.loc['XGBOOST_TREE_REGRESSION_GS_PARAMS'].value)
            self.SVM_REGRESSION_GS_PARAMS = ast.literal_eval(properties.loc['SVM_REGRESSION_GS_PARAMS'].value)
            self.LINEAR_CLASSIFICATION_GS_PARAMS = ast.literal_eval(properties.loc['LINEAR_CLASSIFICATION_GS_PARAMS'].value)
            self.RANDOM_FOREST_CLASSIFICATION_GS_PARAMS = ast.literal_eval(properties.loc['RANDOM_FOREST_CLASSIFICATION_GS_PARAMS'].value)
            self.XGBOOST_TREE_CLASSIFICATION_GS_PARAMS = ast.literal_eval(properties.loc['XGBOOST_TREE_CLASSIFICATION_GS_PARAMS'].value)
            self.SVM_CLASSIFICATION_GS_PARAMS = ast.literal_eval(properties.loc['SVM_CLASSIFICATION_GS_PARAMS'].value)
            self.ENABLE_RFE = bool(properties.loc['ENABLE_RFE'].value)
            self.RFE_LENGTH = int(properties.loc['RFE_LENGTH'].value)
            self.CHECK_MODEL_PERFORMANCE = properties.loc['CHECK_MODEL_PERFORMANCE'].value
            self.CHECK_MODEL_PERFORMANCE_NUM = model_checking_time_period
            self.DAYS_FOR_TESTING = int(properties.loc['DAYS_FOR_TESTING'].value)
            self.TEST_DATA_SET_SIZE = float(properties.loc['TEST_DATA_SET_SIZE'].value)
            self.DATA_SHUFFLE_SEED = int(properties.loc['DATA_SHUFFLE_SEED'].value)

    def __new__(cls):
        if not MTProperties.instance:
            MTProperties.instance = MTProperties.__MTProperties()
        return MTProperties.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name, **kwargs):
        return setattr(self.instance, name)



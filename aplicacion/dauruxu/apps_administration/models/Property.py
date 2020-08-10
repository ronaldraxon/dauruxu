"""
apps_administration.models.Property.py
======================================
Modulo para la administracion  de las propiedades
generales de la aplicacion
"""

from django.db import models
from django.utils.safestring import mark_safe
from utilities import TypeUtilities as Tu
from enum import Enum


class PropertyType(Enum):
    APP_ADMIN = "APP_ADMIN"
    DATA_REGISTRY = "DATA_REGISTRY"
    DATA_PREPROCESS = "DATA_PREPROCESS"
    MODEL_TRAINER = "MODEL_TRAINER"
    DATA_CALENDAR = "DATA_CALENDAR"
    PREDICTION_DISPATCHER = "PREDICTION_DISPATCHER"


class PropertyBehaviorTime:
    DAILY = 86400
    TYPES = {
        "EVERY_7_DAYS": DAILY * 7,
        "EVERY_30_DAYS": DAILY * 30,
        "EVERY_60_DAYS": DAILY * 60,
        "EVERY_90_DAYS": DAILY * 90,
        "EVERY_120_DAYS": DAILY * 120,
    }


class PropertyKey(Enum):
    """Clase que contiene las distintas propiedades de la aplicacion
       :param Enum: Contiene el tipo de Aplicacion a la
        cual se le va a realizar la consulta de sus respectivas
        propiedades
    """

    # DATA_CALENDAR
    MINIMUM_YEAR = 'MINIMUM_YEAR', 'DATA_CALENDAR', "1990"
    MAXIMUM_YEAR = 'MAXIMUM_YEAR', 'DATA_CALENDAR', "2050"

    # DATA_REGISTRY
    MINIMUM_DATASET_SIZE = 'MINIMUM_DATASET_SIZE', 'DATA_REGISTRY', '100'

    # DATA_PREPROCESS
    DEFAULT_INPUT_TRANSFORMATIONS = 'DEFAULT_INPUT_TRANSFORMATIONS', 'DATA_PREPROCESS', "IMPUTE_MEDIAN"
    DEFAULT_RESPONSE_TRANSFORMATIONS = 'DEFAULT_RESPONSE_TRANSFORMATIONS', 'DATA_PREPROCESS', "IMPUTE_MEDIAN"
    CHECK_DATA_BEHAVIOR = 'CHECK_DATA_BEHAVIOR', 'DATA_PREPROCESS', "EVERY_30_DAYS"
    CHECK_DATA_BEHAVIOR_NUM = 'CHECK_DATA_BEHAVIOR_NUM', 'DATA_PREPROCESS', "2592000"

    # MODEL_TRAINER
    R2_THRESHOLD = 'R2_THRESHOLD', 'MODEL_TRAINER', "0.9"
    ACCURACY_THRESHOLD = 'ACCURACY_THRESHOLD', 'MODEL_TRAINER', "0.9"
    CROSS_VALIDATION_FOLDS = 'CROSS_VALIDATION_FOLDS', 'MODEL_TRAINER', "3"
    MODELS_TO_TRAIN = 'MODELS_TO_TRAIN', 'MODEL_TRAINER', "LINEAR"  # "LINEAR RANDOM_FOREST SVM XG_BOOST_TREE"
    EXPLORATION_TYPE = 'EXPLORATION_TYPE', 'MODEL_TRAINER', "FIXED"
    LINEAR_REGRESSION_GS_PARAMS = 'LINEAR_REGRESSION_GS_PARAMS', 'MODEL_TRAINER', "{}"
    RANDOM_FOREST_REGRESSION_GS_PARAMS = 'RANDOM_FOREST_REGRESSION_GS_PARAMS', 'MODEL_TRAINER', "{'n_estimators':[80,100,120,140],'max_depth':[5,6,7,8]}"
    XGBOOST_TREE_REGRESSION_GS_PARAMS = 'XGBOOST_TREE_REGRESSION_GS_PARAMS', 'MODEL_TRAINER', "{'booster':['gbtree'], 'objective':['reg:squarederror'], 'n_estimators':[80,100,120,140], 'max_depth':[5,6,7,8]}"
    SVM_REGRESSION_GS_PARAMS = 'SVM_REGRESSION_GS_PARAMS', 'MODEL_TRAINER', "{}"
    LINEAR_CLASSIFICATION_GS_PARAMS = 'LINEAR_CLASSIFICATION_GS_PARAMS', 'MODEL_TRAINER', "{}"
    RANDOM_FOREST_CLASSIFICATION_GS_PARAMS = 'RANDOM_FOREST_CLASSIFICATION_GS_PARAMS', 'MODEL_TRAINER', "{}"
    XGBOOST_TREE_CLASSIFICATION_GS_PARAMS = 'XGBOOST_TREE_CLASSIFICATION_GS_PARAMS', 'MODEL_TRAINER', "{}"
    SVM_CLASSIFICATION_GS_PARAMS = 'SVM_CLASSIFICATION_GS_PARAMS', 'MODEL_TRAINER', "{}"
    ENABLE_RFE = 'ENABLE_RFE', 'MODEL_TRAINER', "False"
    RFE_LENGTH = 'RFE_LENGTH', 'MODEL_TRAINER', "5"
    CHECK_MODEL_PERFORMANCE = "CHECK_MODEL_PERFORMANCE", 'MODEL_TRAINER', "EVERY_7_DAYS"
    CHECK_MODEL_PERFORMANCE_NUM = "CHECK_MODEL_PERFORMANCE", 'MODEL_TRAINER', "604800"
    DAYS_FOR_TESTING = 'DAYS_FOR_TESTING', 'MODEL_TRAINER', "7"
    TEST_DATA_SET_SIZE = 'TEST_DATA_SET_SIZE', 'MODEL_TRAINER', "0.20"
    DATA_SHUFFLE_SEED = 'DATA_SHUFFLE_SEED', 'MODEL_TRAINER', "1920"

    # PREDICTION_DISPATCHER
    LOW_BOUNDARY_DAY = "LOW_BOUNDARY_DAY", 'PREDICTION_DISPATCHER', "1"
    HIGH_BOUNDARY_DAY = "HIGH_BOUNDARY_DAY", 'PREDICTION_DISPATCHER', "31"
    FORECAST_INITIAL_WINDOW = "FORECAST_INITIAL_WINDOW", 'PREDICTION_DISPATCHER', "7"
    ENABLE_PREDICTION_STORING = "ENABLE_PREDICTION_STORING", 'PREDICTION_DISPATCHER', "True"


class Property(models.Model):
    """Clase para registrar las propiedades de validacion del sistema.
     """
    key = models.CharField(max_length=150, primary_key=True, unique=True,
                           help_text=mark_safe("<strong>The name of the property.</strong>"))
    type = models.CharField(choices=Tu.get_tuple_from_enum(PropertyType), max_length=25,
                            default=PropertyType.APP_ADMIN.value,
                            help_text=mark_safe("<strong>The type of the property.</strong>"))
    value = models.CharField(max_length=2000,
                             help_text=mark_safe("<strong>The value of the property.</strong>"))

    class Meta:
        """Clase para hacer referencia a la tabla asociada en la base de datos (apps_administration_property).
        """
        db_table = "apps_administration_property"

"""
model_trainer.models.storage.ForecastModelRecord.py
=======================================================
Modulo para la definicion del modelo
"""

from django.db import models
from django.utils.safestring import mark_safe
from model_trainer.models.mt_core.ForecastModel import ForecastModel
from enum import Enum
from utilities import TypeUtilities as Tu
from uuid import uuid4


class ModelStatus(Enum):
    """
     Enumeracion para el estado de los modelos
    """
    ACTIVE = "ACTIVE"
    IN_TRAINING = "IN_TRAINING"
    TO_TRAIN = "TO_TRAIN"
    TRAINED = "TRAINED"
    DEPRECATED = "DEPRECATED"


class ForecastModelRecord(models.Model):
    """Clase para validaciones de los registros del modelo mt_core
    """

    model_id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    model_task_type = models.CharField(choices=Tu.get_tuple_from_enum(ForecastModel.ModelTaskType),
                                       max_length=20, null=True,
                                       help_text=mark_safe("<strong>Task type of the model.</strong>"))
    is_last_model = models.BooleanField(default=False, help_text=mark_safe(
                                        "<strong>Tag to describe whether is the current model  .</strong>"))
    code = models.CharField(db_index=True, max_length=256, null=True,
                            help_text=mark_safe("<strong>The identifier which the training task is "
                                                "associated with.</strong>"))
    input_variables = models.CharField(max_length=4000, null=True, blank=True,
                                       help_text=mark_safe("<strong>Input variables to build the model.</strong>"))
    response_variable = models.CharField(max_length=500, null=True, blank=True,
                                         help_text=mark_safe(
                                              "<strong>Variable or classes variables the model is going to predict"
                                              "or classify.</strong>"))
    is_rfe_model = models.BooleanField(default=False)
    selected_rfe_input_variables = models.CharField(max_length=4000, null=True, blank=True,
                                                    help_text=mark_safe("<strong>Input variables selected "
                                                                        "by the rfe process.</strong>"))
    model_status = models.CharField(choices=Tu.get_tuple_from_enum(ModelStatus), max_length=20, null=True,
                                    help_text=mark_safe("<strong>Description of the training status.</strong>"))
    model_type = models.CharField(choices=Tu.get_tuple_from_enum(ForecastModel.ModelType), max_length=100,
                                  null=True, help_text=mark_safe("<strong>Model type.</strong>"))
    model_base = models.BinaryField(null=True, help_text=mark_safe("<strong>Model representation in Bytes.</strong>"))
    model_grid_search_params = models.TextField(null=True, help_text=mark_safe("<strong>Grid search hyperparameters."
                                                                               "</strong>"))
    model_best_params = models.TextField(null=True, help_text=mark_safe("<strong>Metrics selected and suitable "
                                                                        "for the model.</strong>"))
    main_score = models.DecimalField(max_digits=5, decimal_places=2, default=0.00,
                                     help_text=mark_safe("<strong>Model main metric used to compare it with "
                                                         "other models.</strong>"))
    metrics = models.TextField(null=True, help_text=mark_safe("<strong>Metrics selected and suitable "
                                                              "for the model.</strong>"))
    training_request_datetime = models.DateTimeField(null=True,
                                                     help_text=mark_safe(
                                                         "<strong>Datetime of the training request.</strong>"))
    training_start_datetime = models.DateTimeField(null=True,
                                                   help_text=mark_safe(
                                                       "<strong>Datetime when the training starts.</strong>"))
    training_end_datetime = models.DateTimeField(null=True,
                                                 help_text=mark_safe(
                                                     "<strong>Datetime when the training ends.</strong>"))

    class Meta:
        """Clase para hacer referencia a la tabla asociada en la base de datos.

        """
        db_table = "mt_forecast_model_record"

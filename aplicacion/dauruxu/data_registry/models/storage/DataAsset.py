"""
data_registry.models.DataAsset.py
=================================
Modulo de definición del activo de datos destinado a una tarea de minería.
"""

from django.db import models
from django.utils.safestring import mark_safe
from utilities import TypeUtilities as Tu
from enum import Enum
from django.utils import timezone


class DataMiningTask(Enum):
    """
    Enumeracion que define el tipo de tarea de minería de datos que se va a realizar
    """
    REGRESSION = "REGRESSION"
    CLASSIFICATION = "CLASSIFICATION"


class DataAsset(models.Model):
    """
        Clase DataAsset que contiene el activo de los datos
    """
    code = models.CharField(null=False, primary_key=True, unique=True, max_length=256,
                            help_text=mark_safe("<strong>Identifier for the data asset.</strong>"))
    context = models.CharField(null=False, max_length=200,
                               help_text=mark_safe("<strong>Description of the data asset context.</strong>"))
    registry_date = models.DateTimeField(null=True, default=timezone.now,
                                         help_text=mark_safe("<strong>Data asset registry date.</strong>"))
    data_mining_task = models.CharField(choices=Tu.get_tuple_from_enum(DataMiningTask), null=False, max_length=20,
                                        help_text=mark_safe("<strong>The expected data mining task to execute "
                                                            "with the data asset.</strong>"))
    input_variables = models.TextField(null=True, help_text=mark_safe("<strong>Input variables names.</strong>"))
    input_variables_data_types = models.TextField(null=True, help_text=mark_safe("<strong>Input variables "
                                                                                 "data types.</strong>"))
    is_a_time_series_based_dataset = models.BooleanField(default=False,
                                                         help_text=mark_safe("<strong>Determina si es un conjunto de "
                                                                             "datos corresponde a una serie temporal "
                                                                             "o si contiene un campo de fecha el cual "
                                                                             "sea relevante en la tarea "
                                                                             "de minería.</strong>"))
    main_date_field_name = models.CharField(max_length=24, null=True,
                                            help_text=mark_safe("<strong>Si la variable is_a_time_series_based_dataset "
                                                                "es afirmativa, aquí deberá especificar el nombre del "
                                                                "campo correspondiente a la fecha y que será empleado"
                                                                "para la integración con el calendario .</strong>"))
    response_variable = models.CharField(max_length=24, null=True,
                                         help_text=mark_safe("<strong>Variables names containing the "
                                                             "values the model is going to predict "
                                                             "or classify.</strong>"))
    response_variable_data_type = models.CharField(max_length=10, null=True, blank=True,
                                                   help_text=mark_safe("<strong>Response variables "
                                                                       "data type.</strong>"))
    number_of_classes = models.IntegerField(null=True, default=0,
                                            help_text=mark_safe("<strong>Number of classes to predict "
                                                                "(Only for classification tasks).</strong>"))
    raw_data = models.TextField(null=True, help_text=mark_safe("<strong>Raw data for further "
                                                               "data mining task execution</strong>"))

    class Meta:
        """Clase para hacer referencia a la tabla asociada en la base de datos (dr_data_asset).
      """
        db_table = "dr_data_asset"

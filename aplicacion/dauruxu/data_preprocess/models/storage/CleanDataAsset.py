"""
model_trainer.models.storage.CleanData.py
=========================================
Módulo para la definición de la clase de
datos limpios
"""
from django.db import models
from django.utils.safestring import mark_safe
from utilities import TypeUtilities as Tu
from django.utils import timezone
from enum import Enum
import uuid


class DataMiningTask(Enum):
    REGRESSION = "REGRESSION"
    CLASSIFICATION = "CLASSIFICATION"


class CleanDataAsset(models.Model):
    """Esta clase define los campos para un activo de datos limpios
    """
    code = models.CharField(null=False, primary_key=True, unique=True, max_length=256,
                            help_text=mark_safe("<strong>Identificador de activo de datos.</strong>"))
    context = models.CharField(null=False, max_length=200,
                               help_text=mark_safe("<strong>Descripción del contexto del activo de datos.</strong>"))
    registry_date = models.DateTimeField(null=True, default=timezone.now,
                                         help_text=mark_safe("<strong>Fecha inicial de registro del activo de datos.</strong>"))
    updated_on = models.DateTimeField(null=True,
                                      help_text=mark_safe("<strong>Fecha de última actualización de datos.</strong>"))
    data_mining_task = models.CharField(choices=Tu.get_tuple_from_enum(DataMiningTask), null=False, max_length=20,
                                        help_text=mark_safe("<strong>La tarea de minería de datos definida para el "
                                                            "activo de datos.</strong>"))
    input_variables = models.TextField(null=True, help_text=mark_safe("<strong>Variables de entrada.</strong>"))
    response_variable = models.CharField(max_length=24, null=True,
                                         help_text=mark_safe("<strong>Nombre de la variable objetivo "
                                                             "o de respuesta.</strong>"))
    number_of_classes = models.IntegerField(null=True, default=0,
                                            help_text=mark_safe("<strong>Número de clases a predecir "
                                                                "(Sólo para tareas de clasificación).</strong>"))

    clean_data = models.TextField(null=True, help_text=mark_safe("<strong>Datos limpios para la generación de "
                                                                 "modelos</strong>"))

    class Meta:
        """Clase para referenciar el modelo de datos limpios en la base de datos.
        """
        db_table = "dp_clean_data_asset"

"""
data_preprocess.models.storage.DataPreprocessReport.py
======================================================
Módulo para la definición de las clases y métodos para
la administración de registros de preproceso.
"""

from data_calendar.services.CalendarService import CalendarService
from django.utils.safestring import mark_safe
from django.utils import timezone
from django.db import models
from enum import Enum
import uuid


class DataPreprocessStatus(Enum):
    """Enumeración para el estado del registro preproceso.
    """
    TO_PROCESS = "TO_PROCESS"
    IN_PROCESS = "IN_PROCESS"
    DONE = "DONE"


class DataPreprocessManager(models.Manager):
    """Clase para la gestión de la clase de registro de preproceso
    """

    def create_new_data_preprocess_report(self, code, inputs_transformations, response_transformations):
        """Crea un nuevo registro de preproceso de activo de datos.

        - **parameters**::
              :param code: Identificador de activo de datos.
              :param calendar_integration_fields: Campos seleccionados para integrar del calendario.
              :param inputs_transformations: Transformaciones para campos de entrada.
              :param response_transformations: Transformaciones para campo de salida.
        - **return**::
              :return: Una instancia de reporte de preproceso de activo de datos.
        """
        data_preprocess = self.create(code=code,
                                      preprocess_request_date=CalendarService.now_with_time_zone(),
                                      preprocess_status=DataPreprocessStatus.TO_PROCESS.name,
                                      inputs_transformations=inputs_transformations,
                                      response_transformations=response_transformations)
        self.override_current_data_asset_preprocess_report(data_preprocess, code)
        return data_preprocess

    def override_current_data_asset_preprocess_report(self, new_preprocess, code):
        """Busca el preproceso actual y lo deroga para colocar el nuevo preproceso como actual.

        - **parameters**::
                :param new_preprocess: proceso a colocar como actual.
                :param code: Identificador del activo de datos.
        """
        try:
            current_preprocess = self.get(code=code, is_the_current_data_preprocess=True)
            current_preprocess.is_the_current_data_preprocess = False
            current_preprocess.save()
            self.set_data_asset_preprocess_as_current(new_preprocess)
        except DataAssetPreprocessReport.DoesNotExist:
            self.set_data_asset_preprocess_as_current(new_preprocess)

    def set_data_asset_preprocess_as_current(self, new_preprocess):
        """Coloca el proceso relacionado como actual.

        - **parameters**::
                :param new_preprocess: proceso a colocar como actual.
        """
        new_preprocess.is_the_current_data_preprocess = True
        new_preprocess.save()

    def set_current_data_preprocess_to_in_process(self, code):
        """Busca el preproceso de activo de datos actual y actualiza su estado a en proceso (IN_PROCESS)

        - **parameters**::
              :param code: Identificador del activo de datos.
        """
        data_preprocess = self.get(code=code, is_the_current_data_preprocess=True)
        data_preprocess.preprocess_status = DataPreprocessStatus.IN_PROCESS.name
        data_preprocess.save()


class DataAssetPreprocessReport(models.Model):
    """Clase de definición de preproceso para activo de datos.
    """
    objects = DataPreprocessManager()
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(null=False, max_length=256, default='', db_index=True,
                            help_text=mark_safe("<strong>Identificador de activo de datos.</strong>"))
    preprocess_request_date = models.DateTimeField(null=False, default=timezone.now,
                                                   help_text=mark_safe("<strong>Fecha y hora en que se solicitó "
                                                                       "el preprocesamiento del "
                                                                       "activo de datos.</strong>"))
    preprocess_fulfillment_date = models.DateTimeField(null=True,
                                                       help_text=mark_safe("<strong>Fecha y hora en que culminó el "
                                                                           "preprocesamiento de datos.</strong>"))

    preprocess_status = models.CharField(max_length=10, null=False, default=DataPreprocessStatus.TO_PROCESS.name,
                                         help_text=mark_safe("<strong>Estado de procesamiento "
                                                             "para el activo de datos management creation "
                                                             "status.</strong>"))
    inputs_transformations = models.TextField(null=True, help_text=mark_safe("<strong>Transformaciones "
                                                                             "para cada variable de entrada</strong>"))
    inputs_pipeline = models.BinaryField(help_text=mark_safe("<strong>Binario del archivo de preprocesamiento que "
                                                             "incluye las transformaciones implementadas para "
                                                             "las variables de entrada</strong>"))
    response_transformations = models.TextField(null=True, help_text=mark_safe("<strong>Nombre de transformaciones "
                                                                               "para la variable objetivo o "
                                                                               "de respuesta.</strong>"))
    response_pipeline = models.BinaryField(help_text=mark_safe("<strong>Binario del archivo de preprocesamiento "
                                                               "que incluye las transformaciones implementadas "
                                                               "para la variable de salida</strong>"))
    is_the_current_data_preprocess = models.BooleanField(null=False, default=False,
                                                         help_text=mark_safe(
                                                             "<strong>Indica si es manifiesto de procesamiento "
                                                             "actual y a utilizar para tareas consecuentes</strong>"))

    class Meta:
        """Clase para referenciar la tabla asociada en la base de datos.
        """
        db_table = "dp_data_asset_preprocess_report"

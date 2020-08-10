"""
prediction_dispatcher.models.storage.PDPropertiesService.py
===========================================================
Módulo para la administración de la entidad Forecast.


"""

from django.db import models
from django.utils.safestring import mark_safe
from prediction_dispatcher.models.storage.PredictionsHeader import PredictionsHeader
import uuid


class PredictionManager(models.Manager):

    def create_new_forecast(self, prediction_header):
        """Crear un nuevo registro del modelo de prediction.

        - **parameters**::
              :param prediction_header: Identificacion del modelo de prediccion
        - **return**::
              :return: Prediction record  created.
        """
        self.create(forecast_header=prediction_header)


class Prediction(models.Model):
    """
        Clase para el manejo y validacion del modelo de prediccion
    """
    objects = PredictionManager()
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False,
                          help_text=mark_safe("<strong>Forecast identifier.</strong>"))
    input_variables = models.CharField(max_length=4000, null=True, blank=True,
                                       help_text=mark_safe("<strong>Input variables to build the model.</strong>"))
    response_variable = models.CharField(max_length=500, null=True, blank=True,
                                         help_text=mark_safe(
                                             "<strong>Variable or classes variables the model is going to predict"
                                             "or classify.</strong>"))
    input_values = models.TextField(null=True, help_text=mark_safe("<strong>Input values used for prediction</strong>"))
    response_values = models.TextField(null=True, help_text=mark_safe("<strong>Values of the response</strong>"))
    forecast_header = models.ForeignKey(PredictionsHeader, null=True, related_name='forecast_breakdown', db_index=True,
                                        on_delete=models.CASCADE)

    class Meta:
        """Clase para hacer referencia a la tabla asociada en la base de datos
        """
        db_table = "pd_prediction"

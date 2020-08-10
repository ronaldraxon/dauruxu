"""
prediction_dispatcher.models.storage.PredictionsHeader.py
=========================================================
Modulo para la administracion de la entidad ForecastHeader.
Contiene información sobre el encabezado del modelo mt_core.
"""

from django.db import models
from django.utils.safestring import mark_safe
from django.core.validators import MinValueValidator
from django.utils import timezone
import uuid


class PredictionsHeaderManager(models.Manager):
    """
    Clase para el PredictionsHeaderManager
    """

    def create_new_forecast_header(self, code, forecast_quantity):
        """
               - **parameters**::

                     :param code:
                     :param from_date:
                     :param to_date:
                     :param forecast_quantity:

               - **parameters**::
                     :return:
        """
        forecast_header = self.create(code=code,
                                      request_date=timezone.now(),
                                      forecast_quantity=forecast_quantity)
        return forecast_header


class PredictionsHeader(models.Model):
    """Class for manage and validate forecastHeader records.
    """
    objects = PredictionsHeaderManager()
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False,
                          help_text=mark_safe("<strong>Forecast header identifier.</strong>"))
    request_date = models.DateTimeField(null=True,
                                        help_text=mark_safe("<strong>Date of the mt_core request.</strong>"))
    code = models.CharField(db_index=True, max_length=256, null=True,
                            help_text=mark_safe("<strong>The identifier which the prediction header is "
                                                "associated with.</strong>"))
    forecast_quantity = models.IntegerField(null=True, validators=[MinValueValidator(1)],
                                            help_text=mark_safe("<strong>Forecast counter.</strong>"))
    observations = models.CharField(max_length=2000, null=True, default=" ",
                                    help_text=mark_safe("<strong>Forecast observations or issues to .</strong>"))

    class Meta:
        """Class to reference the associated table in the database
        """
        db_table = "pd_prediction_header"

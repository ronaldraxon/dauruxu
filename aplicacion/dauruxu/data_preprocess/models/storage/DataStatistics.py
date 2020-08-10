"""
data_preprocess.models.storage.DataStatistics.py
================================================
Módulo para la definición de datos de las
estadísticas de un activo de datos
"""

from django.db import models

import uuid

from django.utils.safestring import mark_safe

from data_preprocess.models.storage.DataAssetPreprocessReport import DataAssetPreprocessReport


class DataStatistics(models.Model):
    """Clase con el modelo de datos para persistir las estadísticas de un activo de datos
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(null=True,  max_length=256,
                            help_text=mark_safe("<strong>Identificador de activo de datos</strong>"))
    data_asset_preprocess = models.ForeignKey(DataAssetPreprocessReport, related_name='statistics',
                                              on_delete=models.CASCADE, default=uuid.uuid4,
                                              help_text=mark_safe("<strong>Llave de relación con el reporte "
                                                                     "de preproceso</strong>"))
    statistics = models.TextField(null=True, help_text=mark_safe("<strong>Estadísticas en formato json</strong>"))

    class Meta:
        """Clase para referencia del modelo de datos en la instancia de la base de datos.
        """
        db_table = "dp_data_statistics"

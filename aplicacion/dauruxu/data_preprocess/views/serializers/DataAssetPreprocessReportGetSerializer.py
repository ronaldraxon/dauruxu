"""
data_preprocess.views.serializers.DataAssetPreprocessReportGetSerializer.py
===========================================================================
Módulo para la definición del serializador del modelo de datos
del reporte de preprocesamiento de activo de datos (Sólo consulta)
"""

from rest_framework import serializers
from data_preprocess.models.storage.DataAssetPreprocessReport import DataAssetPreprocessReport


class DataAssetPreprocessReportGetSerializer(serializers.ModelSerializer):

    class Meta:
        model = DataAssetPreprocessReport
        fields = ('code', 'preprocess_request_date', 'preprocess_fulfillment_date',
                  'preprocess_status', 'inputs_transformations', 'inputs_pipeline',
                  'response_transformations', 'response_pipeline', 'is_the_current_data_preprocess')

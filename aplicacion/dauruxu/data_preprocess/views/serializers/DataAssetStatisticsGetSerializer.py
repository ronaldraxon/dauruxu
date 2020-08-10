"""
data_preprocess.views.serializers.DataStatisticsGetSerializer.py
================================================================
Modulo para la definición del serializador de solicitudes de
creación de preprocesos de activo de datos (Sólo creación).
"""

from rest_framework import serializers
from data_preprocess.models.storage.DataStatistics import DataStatistics


class DataAssetStatisticsGetSerializer(serializers.ModelSerializer):

    class Meta:
        model = DataStatistics
        fields = ("code", "data_asset_preprocess", "statistics")

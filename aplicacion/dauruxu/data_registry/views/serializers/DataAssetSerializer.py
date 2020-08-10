"""
data_registry.views.serializers.DataAssetSerializer.py
======================================================
Modulo para la serializacion de un activo de datos
"""

from rest_framework import serializers
from data_registry.models.storage.DataAsset import DataAsset


class DataAssetSerializer(serializers.ModelSerializer):

    class Meta:
        model = DataAsset
        fields = '__all__'


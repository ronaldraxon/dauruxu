"""
data_preprocess.views.serializers.CleanDataAssetGetSerializer.py
================================================================
Módulo para la definición del serializador del modelo de datos
del activo de datos limpio
"""

from rest_framework import serializers
from data_preprocess.models.storage.CleanDataAsset import CleanDataAsset


class CleanDataAssetGetSerializer(serializers.ModelSerializer):

    class Meta:
        model = CleanDataAsset
        fields = ('code', 'context', 'registry_date',
                  'updated_on', 'data_mining_task', 'input_variables',
                  'response_variable', 'number_of_classes',
                  'clean_data')

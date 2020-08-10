"""
data_registry.views.serializers.DataAssetRowSerializer.py
==============================================================
Modulo para la serializacion del data Asset
"""

from rest_framework import serializers
from data_registry.models.storage.DataAsset import DataAsset
from django.utils.safestring import mark_safe
from utilities.PandasUtilities import PandasUtilities as Pu
import ast
import logging

logger = logging.getLogger(__name__)


class DataAssetRowSerializer(serializers.Serializer):
    """
        Clase serializadora del activo de Datos
    """
    code = serializers.CharField(max_length=256,
                                 help_text=mark_safe("<strong>Identifier for the data asset.</strong>"))
    raw_data = serializers.JSONField(required=True,
                                     help_text=mark_safe("<strong>Raw data to be updated to "
                                                         "an existing data asset.</strong>"))


    def update(self, instance, data):
        variables = ast.literal_eval(instance.input_variables)
        variables.extend(ast.literal_eval(instance.response_variable))
        raw_data = Pu.convert_list_of_dict_to_pandas_data_frame(data.data.pop('raw_data'))
        raw_data_columns = list(raw_data.columns)
        if len(list(set(raw_data_columns) - set(variables))) > 0:
            raise serializers.ValidationError('The raw data provided does not contain the same fields of the existent'
                                              'data asset.')
        else:
            current_raw_data = ast.literal_eval(instance.raw_data)
            current_raw_data = Pu.convert_list_of_dict_to_pandas_data_frame(current_raw_data)
            current_raw_data = current_raw_data.append(raw_data, ignore_index=True)
            instance.raw_data = str(list(current_raw_data.T.to_dict().values()))
            instance.save()


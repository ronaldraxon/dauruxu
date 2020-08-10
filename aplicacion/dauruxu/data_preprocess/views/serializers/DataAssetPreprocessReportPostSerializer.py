"""
data_preprocess.views.serializers.DataPreprocessReportPostSerializer.py
=======================================================================
Modulo para la definición del serializador de solicitudes de
creación de preprocesos de activo de datos (Sólo creación).
"""

from rest_framework import serializers
from data_preprocess.models.storage.DataAssetPreprocessReport import DataAssetPreprocessReport
from data_preprocess.views.serializers.TransformationLayoutSerializer import TransformationLayoutSerializer
from django.utils.safestring import mark_safe
from data_preprocess.services.configuration.DataPreProcessPropertiesService import DataPreprocessPropertiesService


class DataAssetPreprocessReportPostSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=256,
                                 help_text=mark_safe("<strong>Identificador del activo de datos.</strong>"))
    inputs_transformations = TransformationLayoutSerializer(many=True, allow_null=True)
    response_transformations = TransformationLayoutSerializer(many=True, allow_null=True)

    def create(self, validated_data):
        code = validated_data.pop('code')
        valid_input_transformations = validated_data.pop('inputs_transformations')
        valid_response_transformations = validated_data.pop('response_transformations')
        data_asset_preprocess = DataAssetPreprocessReport. \
            objects.create_new_data_preprocess_report(code=code,
                                                      inputs_transformations=valid_input_transformations,
                                                      response_transformations=valid_response_transformations)
        return data_asset_preprocess

    def update(self, instance, validated_data):
        print("Implementar actualización")
        pass

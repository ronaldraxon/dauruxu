"""
data_preprocess.views.serializers.TransformationLayoutSerializer.py
===================================================================
Módulo base para la definición del serializador de
detalles de transformación (Hace parte del serializador de creación)
"""
from data_preprocess.models.core.TransformationFactory import TransformationsFactory
from django.utils.safestring import mark_safe
from rest_framework import serializers

TRANSFORMATIONS_CHOICES = TransformationsFactory.get_transformations_as_choices()


class TransformationLayoutSerializer(serializers.Serializer):

    transformation_name = serializers.CharField(allow_blank=False, min_length=3, max_length=10,
                                                help_text=mark_safe("<strong>Nombre de "
                                                                    "la transformación "
                                                                    "deseada (debe ser único en "
                                                                    "toda la secuencia).</strong>"))
    transformation_type = serializers.ChoiceField(choices=TRANSFORMATIONS_CHOICES, allow_blank=True,
                                                  help_text=mark_safe("<strong>Idenfificador del tipo "
                                                                      "la transformación deseada.</strong>"))
    fields_involved = serializers.ListField(allow_empty=True,
                                            help_text=mark_safe("<strong>Nombre de campos a "
                                                                "involucrar en la transformación</strong>"))
    transformation_params = serializers.DictField(allow_empty=True,
                                                  help_text=mark_safe("<strong>Parámetros de "
                                                                      "la transformación deseada.</strong>"))

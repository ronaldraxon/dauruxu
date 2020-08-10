"""
model_trainer.views.serializers.PointSerializer.py
=======================================================
Module for the serialization of Point entity.
"""
from model_trainer.models.mt_storage.MTSession import MTSession
from rest_framework import serializers
from django.utils.safestring import mark_safe


class MTSessionSerializer(serializers.ModelSerializer):
    input_variables = serializers.ListField(allow_empty=False,
                                            child=serializers.CharField(min_length=5, max_length=100),
                                            max_length=40,
                                            help_text=mark_safe("<strong>List of input variables.</strong>"))
    response_variable = serializers.CharField(min_length=1, max_length=100,
                                              help_text=mark_safe("<strong>response variable</strong>"))
    clean_data = serializers.JSONField(required=True,
                                       help_text=mark_safe("<strong>Data to be used for model training</strong>"))

    class Meta:
        model = MTSession
        fields = ('code', 'input_variables', 'response_variable', 'clean_data')
"""
model_trainer.views.serializers.RetrainRequestSerializer.py
===========================================================
Module for the serialization of Point entity.
"""

from rest_framework import serializers
from model_trainer.models.mt_storage.MTSession import MTSession


class RetrainRequestSerializer(serializers.ModelSerializer):
    param_grid = serializers.JSONField(required=True)

    class Meta:
        model = MTSession
        fields = ('code', 'param_grid')

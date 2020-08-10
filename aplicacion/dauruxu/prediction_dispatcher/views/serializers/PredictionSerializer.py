"""
prediction_dispatcher.view.serializers.PredictionSerializer.py
==============================================================
Module for the serialization of Forecast entity.
"""

from rest_framework import serializers
from prediction_dispatcher.models.storage.Prediction import Prediction


class PredictionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Prediction
        fields = '__all__'

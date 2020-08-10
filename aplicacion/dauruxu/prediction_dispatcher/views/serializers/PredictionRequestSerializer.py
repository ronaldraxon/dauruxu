"""
prediction_dispatcher.view.serializers.PredictionRequest.py
===========================================================
XXXX.
"""

from prediction_dispatcher.models.storage.Prediction import Prediction
from rest_framework import serializers


class PredictionRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = Prediction
        fields = ('input_variables', 'input_values')


"""
prediction_dispatcher.view.serializers.PredictionHeaderSerializer.py
=====================================================================
Modulo serializador
"""

from rest_framework import serializers

from prediction_dispatcher.models.storage.PredictionsHeader import PredictionsHeader
from prediction_dispatcher.views.serializers.PredictionSerializer import PredictionSerializer


class PredictionHeaderSerializer(serializers.ModelSerializer):
    prediction_results = PredictionSerializer(many=True)

    class Meta:
        model = PredictionsHeader
        fields = ('code', 'request_date', 'forecast_quantity', 'observations', 'prediction_results')

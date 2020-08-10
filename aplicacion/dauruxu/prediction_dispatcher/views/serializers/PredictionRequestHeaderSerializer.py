"""
prediction_dispatcher.view.serializers.PredictionHeaderSerializer.py
=====================================================================
Modulo de
"""

from rest_framework import serializers
from prediction_dispatcher.services.core.ValidationService import ValidationService
from prediction_dispatcher.models.storage.PredictionsHeader import PredictionsHeader
from prediction_dispatcher.views.serializers.PredictionRequestSerializer import PredictionRequestSerializer

import logging

logger = logging.getLogger(__name__)


def __validate_code__(code):
    logger.debug("Verifying code {}".format(code))
    code_has_process = ValidationService.validate_code_for_process(code)
    code_has_model = ValidationService.validate_code_for_model(code)
    if not code_has_process:
        raise serializers.ValidationError('The provided code ' + str(code) + "has not assigned process.")
    if not code_has_model:
        raise serializers.ValidationError('The provided code ' + str(code) + "has not assigned model.")


class PredictionRequestHeaderSerializer(serializers.ModelSerializer):
    prediction_request = PredictionRequestSerializer(many=True)

    class Meta:
        model = PredictionsHeader
        fields = ('code', 'prediction_request')

    def create(self, data):
        code = data.pop('code')
        __validate_code__(code)
        pass

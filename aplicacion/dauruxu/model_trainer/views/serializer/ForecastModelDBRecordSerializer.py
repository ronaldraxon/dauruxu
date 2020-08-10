"""
repository.ForecastModelDBRecordSerializer.py
=====================================
Module for the serialization of ForecastModel entity.
"""

from rest_framework import serializers
from model_trainer.models.mt_storage.ForecastModelRecord import ForecastModelRecord


class ForecastModelDBRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = ForecastModelRecord
        fields = ('model_id', 'code', 'model_type', 'model_task_type', 'model_status', 'is_last_model',
                  'input_variables', 'response_variable', 'model_grid_search_params', 'model_best_params',
                  'metrics', 'training_request_datetime', 'training_start_datetime', 'training_end_datetime',
                  'model_base')

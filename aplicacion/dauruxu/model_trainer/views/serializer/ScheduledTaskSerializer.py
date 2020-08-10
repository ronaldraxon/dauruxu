"""
model_trainer.views.serializers.ScheduledTaskSerializer.py
===========================================================
Module for the serialization of scheduled tasks .
"""

from rest_framework import serializers
from background_task.models import Task
from model_trainer.models.mt_storage.MTSession import MTSession


class ScheduledTaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ('verbose_name', 'task_name', 'task_params', 'priority',
                  'queue', 'attempts', 'failed_at', 'last_error', 'locked_by')


class MTPointScheduledTasksSerializer(serializers.ModelSerializer):
    scheduled_data = ScheduledTaskSerializer(many=True)

    class Meta:
        model = MTSession
        fields = ('code', 'scheduled_data')

"""
data_calendar.serializer.CalendarSerializer.py
==============================================
Modulo para la serializacion del calendario
"""

from rest_framework import serializers
from data_calendar.models.Calendar import Calendar


class CalendarSerializer(serializers.ModelSerializer):

    class Meta:
        model = Calendar
        fields = '__all__'

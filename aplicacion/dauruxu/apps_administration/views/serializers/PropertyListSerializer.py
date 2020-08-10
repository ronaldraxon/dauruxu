"""
apps_migrations.views.serializers.PropertyListSerializer.py
====================================
Module for the serialization a list of Property entity.
"""

from rest_framework import serializers
from apps_administration.models.Property import Property


class PropertyListSerializer(serializers.ModelSerializer):
    """ Clase Serializadora para las propiedades de la aplicacion
       """
    class Meta:
        model = Property
        fields = '__all__'

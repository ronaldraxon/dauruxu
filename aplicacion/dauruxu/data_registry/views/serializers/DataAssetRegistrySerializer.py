"""
data_registry.views.serializers.DataAssetRegistrySerializer.py
==============================================================
Modulo para la serializacion de un nuevo registro de un nuevo dataAsset
"""
from data_registry.models.storage.DataAsset import DataAsset
from django.utils.safestring import mark_safe
from data_registry.services.configuration.DataRegistryPropertiesService import DataRegistryPropertiesService
from rest_framework import serializers
import logging

logger = logging.getLogger(__name__)


class DataAssetRegistrySerializer(serializers.ModelSerializer):
    """
     Clase Serializadora del registro del dataAsset
    """
    input_variables = serializers.ListField(allow_empty=False,
                                            child=serializers.CharField(min_length=5, max_length=20),
                                            max_length=100,
                                            help_text=mark_safe("<strong>List of input variables.</strong>"))
    input_variables_data_types = serializers.ListField(allow_empty=False,
                                                       child=serializers.CharField(min_length=1, max_length=10),
                                                       max_length=100,
                                                       help_text=mark_safe("<strong>List of data types of "
                                                                           "input variables. It matches the order"
                                                                           "of the input variables .</strong>"))
    main_date_field_name = serializers.ListField(allow_empty=False,
                                                 child=serializers.CharField(min_length=5, max_length=20),
                                                 max_length=1,
                                                 help_text=mark_safe(
                                                  "<strong>Si la variable is_a_time_series_based_dataset "
                                                  "es afirmativa, aquí deberá especificar el nombre del "
                                                  "campo correspondiente a la fecha y que será empleado"
                                                  "para la integración con el calendario .</strong>"))
    response_variable = serializers.ListField(allow_empty=False,
                                              child=serializers.CharField(min_length=5, max_length=20),
                                              max_length=1,
                                              help_text=mark_safe("<strong>List of response variables.</strong>"))
    raw_data = serializers.JSONField(required=True,
                                     help_text=mark_safe("<strong>Raw data for further "
                                                         "preprocess</strong>"))

    class Meta:
        model = DataAsset
        fields = ('code', 'context', 'data_mining_task', 'input_variables', 'is_a_time_series_based_dataset',
                  'main_date_field_name', 'input_variables_data_types', 'response_variable',
                  'response_variable_data_type', 'number_of_classes', 'raw_data')

    def create(self, data):
        self.__validate_data_set_size__(data.get('raw_data'))
        return DataAsset.objects.create(**data)

    def __validate_data_set_size__(self, data_set):
        """
              Validar el tamanio del set de Datos
        """
        logger.debug("Verifying data set size for registry")
        data_set_size = len(data_set)
        minimum_set_size = DataRegistryPropertiesService.get_minimum_dataset_size()
        if not data_set_size >= minimum_set_size:
            raise serializers.ValidationError('The dataset only contains {0} observation(s). Be sure that your dataset '
                                              'has at least {1} observations'.format(len(data_set), minimum_set_size))

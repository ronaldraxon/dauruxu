"""
apps_administration.services.PropertyService.py
===============================================
Modulo encargado de la administracion de las propiedades
de la aplicacion
"""
from django.db.models import QuerySet

from apps_administration.models.Property import Property, PropertyType, PropertyKey, PropertyBehaviorTime
from apps_administration.views.serializers.PropertyListSerializer import PropertyListSerializer
from utilities.NumpyUtilities import NumpyUtilities
import ast
import logging

logger = logging.getLogger(__name__)


class PropertyService:

    @staticmethod
    def create_property(property_serializer):
        """Metodo encargado de almacenar  las propiedades generales de la aplicacion
            :param property_serializer:Contiene los valores de las propiedades a almacenar

            :return: Mensaje  con la propiedad que se ha creado.
        """
        logger.info("Attempting to create property")
        property_serializer.save()

    @staticmethod
    def retrieve_all_properties():
        """Metodo encargado de almacenar  las propiedades generales de la aplicacion
                  :param property_serializer:Contiene los valores de las propiedades a almacenar

                  :return: Mensaje  con la propiedad que se ha creado.
              """
        logger.info("Attempting to search all property")
        return Property.objects.all()

    @staticmethod
    def retrieve_property(key):
        """Metodo encargado de devolver las propiedades generales de la aplicacion especificada
                  :param key:Llave de la propiedad a recuperar

                  :return: Serializador que contiene la lista de las propiedades para la llave especificada
              """
        logger.info("Attempting to search properties with id: " + key)
        return PropertyListSerializer(Property.objects.get(key=key)).data

    @staticmethod
    def retrieve_property_enum(enum):
        key = enum.name
        return Property.objects.get(key=key)

    @staticmethod
    def retrieve_property_value_by_enum(enum):
        key = enum.name
        return Property.objects.get(key=key).value

    @staticmethod
    def retrieve_property_enum_by_key(key):
        return Property.objects.get(key=key)

    @staticmethod
    def retrieve_integer_array_property_by_enum(enum):
        key = enum.name
        property_list = Property.objects.get(key=key).value
        property_list = ast.literal_eval(property_list)
        return NumpyUtilities.convert_integer_list_to_integer_np_array(property_list)

    @staticmethod
    def retrieve_float_array_property_by_enum(enum):
        key = enum.name
        property_list = Property.objects.get(key=key).value
        property_list = ast.literal_eval(property_list)
        return NumpyUtilities.convert_float_list_to_float32_np_array(property_list)

    @staticmethod
    def retrieve_string_array_property_by_enum(enum):
        property_list = Property.objects.get(key=enum).value
        return ast.literal_eval(property_list)

    @staticmethod
    def retrieve_string_property_by_name(name):
        return str(Property.objects.get(key=name).value)

    @staticmethod
    def retrieve_decimal_property_by_name(name):
        return float(Property.objects.get(key=name).value)

    @staticmethod
    def retrieve_integer_property_by_name(name):
        return int(Property.objects.get(key=name).value)

    @staticmethod
    def retrieve_decimal_property_by_enum(enum):
        key = enum.name
        value = Property.objects.get(key=key).value
        if value == "None":
            return None
        else:
            return float(value)

    @staticmethod
    def retrieve_integer_property_by_enum(enum):
        key = enum.name
        value = Property.objects.get(key=key).value
        if value == "None":
            return None
        else:
            return int(value)

    @staticmethod
    def retrieve_property_value(enum):
        key = enum.value
        return key

    @staticmethod
    def delete_point(key):
        """ Borrado de las propiedades de la aplicacion por su llave
                   """
        logger.info("Attempting to delete property")
        Property.objects.filter(key=key).delete()

    @staticmethod
    def create_default_properties() -> QuerySet:
        """ Creacion de las propiedades por defecto de la aplicacion
           - **return**::
                    :return: Query set con todas las propiedades creadas.
        """
        Property.objects.all().delete()
        for prop in PropertyKey:
            length = len(prop.value)
            name_key = str(prop.value[0])
            name_type = str(prop.value[1])
            default_value = ""
            if length > 1:
                default_value = str(prop.value[2])
            try:
                Property.objects.get(key=name_key)
            except Property.DoesNotExist:
                property_item = Property()
                property_item.key = name_key
                property_item.type = name_type
                property_item.value = default_value
                property_item.save()
        return PropertyService.retrieve_all_properties()

    @staticmethod
    def get_data_behavior_checking_time_period() -> int:
        # TODO:: Validar funcion de este metodo.
        value = PropertyService.retrieve_property_enum(PropertyKey.CHECK_DATA_BEHAVIOR)
        numeric_value = PropertyBehaviorTime.TYPES.get(value, -1)
        if numeric_value == -1:
            numeric_value = PropertyBehaviorTime.DAILY * 30
        return numeric_value

    @staticmethod
    def get_model_checking_time_period():
        """ Obtener el periodo de tiempo de comprobacion del modelo
            """
        return PropertyBehaviorTime.TYPES \
            .get(PropertyService.retrieve_string_property_by_name(PropertyKey.CHECK_MODEL_PERFORMANCE.name))

    @staticmethod
    def get_data_registry_properties() -> QuerySet:
        """ Query set que contiene las propiedades del Model Trainer
         """
        return PropertyService.get_application_properties_by_type(PropertyType.DATA_REGISTRY.value)

    @staticmethod
    def get_data_preprocess_properties():
        """ Gets a query set containing the model trainer properties
        """
        return PropertyService.get_application_properties_by_type(PropertyType.DATA_PREPROCESS.value)

    @staticmethod
    def get_model_trainer_properties() -> QuerySet:
        """  Query set que contiene las propiedades del Model Trainer
         """
        return PropertyService.get_application_properties_by_type(PropertyType.MODEL_TRAINER.value)

    @staticmethod
    def get_data_calendar_properties() -> QuerySet:
        """ Query set que contiene las propiedades del data calendar
         """
        return PropertyService.get_application_properties_by_type(PropertyType.DATA_CALENDAR.value)

    @staticmethod
    def get_prediction_dispatcher_properties() -> QuerySet:
        """ Query set que contiene las propiedades del data calendar
         """
        return PropertyService.get_application_properties_by_type(PropertyType.PREDICTION_DISPATCHER.value)

    @staticmethod
    def get_application_properties_by_type(property_type) -> QuerySet:
        """ Query set que contiene las propiedades del tipo de propiedad especificado
        """
        query_set = Property.objects.filter(type=property_type).values('key', 'value')
        if query_set.exists():
            return query_set
        else:
            PropertyService.create_default_properties()
            return Property.objects.filter(type=property_type).values('key', 'value')

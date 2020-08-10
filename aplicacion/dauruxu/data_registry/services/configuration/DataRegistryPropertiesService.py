"""
data_registry.model.DRPropertiesService.py
=========================================
Modulo para el llamado del singleton para obtener las propiedades de la aplicacion
"""

from utilities.PandasUtilities import PandasUtilities as Pu
from django.db.utils import ProgrammingError

from apps_administration.services.PropertyService import PropertyService
from data_registry.models.configuration.DataRegistryProperties import DataRegistryProperties
import logging


logger = logging.getLogger(__name__)

dr_properties = DataRegistryProperties()


class DataRegistryPropertiesService:
    """
    Clase Servicio para las propiedades del Data Registry
    """

    @staticmethod
    def request_and_update_dr_general_properties(data_registry_params):
        """Peticion para la actualizacion general del calendario
                 - **parameters**::
                      :param data_registry_params:Query set de parametros a ser actualizados dentro de la peticion
            """
        properties = Pu.convert_django_query_set_to_pandas_data_frame(data_registry_params)
        properties = Pu.set_pandas_data_frame_index(properties, 'key')
        dr_properties.update_property_values(properties)

    @staticmethod
    def get_minimum_dataset_size():
        return dr_properties.MINIMUM_DATASET_SIZE

    @staticmethod
    def is_data_preprocess_enabled():
        return dr_properties.REQUEST_DATA_PROCESSING


try:
    DataRegistryPropertiesService.request_and_update_dr_general_properties(PropertyService.get_data_registry_properties())
    logger.info("Data Registry properties updated successful")
except ProgrammingError:
    logger.warning("Data Registry properties was initialized with default values")





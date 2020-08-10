"""
data_calendar.services.configuration.DataCalendarPropertiesService.py
=====================================================================
Modulo para el llamado del singleton de la clase data_calendar
"""

from utilities.PandasUtilities import PandasUtilities as Pu
from django.db.utils import ProgrammingError

from apps_administration.services.PropertyService import PropertyService
from data_calendar.models.configuration.DataCalendarProperties import DataCalendarProperties
import logging


logger = logging.getLogger(__name__)

data_calendar_properties = DataCalendarProperties()


class DataCalendarPropertiesService:

    @staticmethod
    def request_and_update_data_calendar_general_properties(data_calendar_params):
        """Peticion para la actualizacion general del calendario
                 - **parameters**::
                      :param data_calendar_params:Query set de parametros a ser actualizados dentro de la peticion
            """
        properties = Pu.convert_django_query_set_to_pandas_data_frame(data_calendar_params)
        properties = Pu.set_pandas_data_frame_index(properties, 'key')
        data_calendar_properties.update_property_values(properties)

    @staticmethod
    def get_minimum_year():
        return data_calendar_properties.MINIMUM_YEAR

    @staticmethod
    def get_maximum_year():
        return data_calendar_properties.MAXIMUM_YEAR


try:
    DataCalendarPropertiesService.request_and_update_data_calendar_general_properties(PropertyService.get_data_calendar_properties())
    logger.info("Data Calendar properties updated successful")
except ProgrammingError:
    logger.warning("Data Calendar properties was initialized with default values")





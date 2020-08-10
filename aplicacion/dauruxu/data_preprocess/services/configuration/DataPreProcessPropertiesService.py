"""
data_Preprocess.services.configuration.DataPreprocessPropertiesService.py
=========================================================================
Module for called of Singleton.
Creation, consultation of points and raw calendar.
"""

from utilities.PandasUtilities import PandasUtilities as Pu
from django.db.utils import ProgrammingError

from apps_administration.services.PropertyService import PropertyService
from data_calendar.services.CalendarService import CalendarService
from data_preprocess.models.configuration.DataPreprocessProperties import DataPreprocessProperties
import logging


logger = logging.getLogger(__name__)

data_preprocess_properties = DataPreprocessProperties()


class DataPreprocessPropertiesService:

    @staticmethod
    def request_and_update_dp_general_properties(properties):
        properties = Pu.convert_django_query_set_to_pandas_data_frame(properties)
        properties = Pu.set_pandas_data_frame_index(properties, 'key')
        data_preprocess_properties.update_property_values(properties)

    @staticmethod
    def request_and_update_calendar_fields(calendar_fields):
        data_preprocess_properties.update_calendar_fields(calendar_fields)
    
    @staticmethod
    def get_calendar_fields():
        return data_preprocess_properties.DEFAULT_CALENDAR_FIELDS


try:
    DataPreprocessPropertiesService.\
        request_and_update_dp_general_properties(PropertyService.get_data_preprocess_properties())
    DataPreprocessPropertiesService.\
        request_and_update_calendar_fields(CalendarService.get_available_calendar_fields_as_choices())
    logger.info("Data Preprocess properties updated successful")
except ProgrammingError:
    logger.warning("Data Preprocess properties was initialized with default values")



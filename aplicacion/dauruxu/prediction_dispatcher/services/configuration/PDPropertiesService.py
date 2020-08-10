"""
prediction_dispatcher.services.configuration.PDPropertiesService.py
===================================================================
Modulo para la administracion de la entidad ForecastHeader.
Contiene información sobre el encabezado del modelo mt_core.
"""

from apps_administration.services.PropertyService import PropertyService
from django.db.utils import ProgrammingError
from prediction_dispatcher.models.configuration.PDProperties import FDProperties
from utilities.PandasUtilities import PandasUtilities as Pu
import logging


logger = logging.getLogger(__name__)

mt_properties = FDProperties()


class FDPropertiesService:

    @staticmethod
    def request_and_update_pd_general_properties(model_trainer_params):
        """Peticion para la actualizacion general de las propiedades de la palicacion
                         - **parameters**::
                              :param model_trainer_params:Query set de parametros a ser actualizados dentro de la peticion
                    """
        properties = Pu.convert_django_query_set_to_pandas_data_frame(model_trainer_params)
        properties = Pu.set_pandas_data_frame_index(properties, 'key')
        mt_properties.update_property_values(properties)


try:
    FDPropertiesService.request_and_update_pd_general_properties(PropertyService.get_prediction_dispatcher_properties())
    logger.info("Prediction Dispatcher properties updated successful")
except ProgrammingError:
    logger.warning("Prediction Dispatcher properties was initialized with default values")

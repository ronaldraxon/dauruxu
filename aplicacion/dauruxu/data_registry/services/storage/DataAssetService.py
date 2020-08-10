"""
data_registry.services.storage.PointService.py
======================================
Modulo para el servicio del DataAsset
"""

from data_registry.services.configuration.DataRegistryPropertiesService import DataRegistryPropertiesService
from data_registry.models.storage.DataAsset import DataAsset

import logging

logger = logging.getLogger(__name__)


class DataAssetService:

    @staticmethod
    def create_data_asset(data_asset):
        """Peticion para la creacion del DataAsset
                         - **parameters**::
                              :param data_asset:Data asset a ser almacenado
                    """
        logger.debug("Attempting to create a data asset")
        data_asset.save()
        #if DataRegistryPropertiesService.is_data_preprocess_enabled():
        #    print("summon data preprocess")


    @staticmethod
    def update_data_asset(code, data_asset_row):
        """Peticion para la actualizacion del DataAsset
                               - **parameters**::
                                    :param data_asset:Data asset a ser actualizado
                                     :param code:Identificador para recuperar el activo de datos
                          """
        logger.debug("Attempting to update a data asset")
        data_asset = DataAssetService.retrieve_data_asset(code=code)
        data_asset_row.update(data_asset, data_asset_row)

    @staticmethod
    def retrieve_data_asset(code):
        """Peticion para la recuperacion del DataAsset
                                 - **parameters**::
                                       :param code:Identificador para recuperar el activo de datos
                            """
        logger.debug("Attempting to get a data asset with code: "+str(code))
        return DataAsset.objects.get(code=code)

    @staticmethod
    def retrieve_raw_data_from_data_asset_by_code(code):
        """Peticion para la recuperacion de los datos sin procesar desde un dataAsset
                                  - **parameters**::
                                        :param code:Identificador para recuperar el activo de datos
                             """
        logger.debug("Attempting to get raw data from an existing data asset with code: " + str(code))
        return DataAsset.objects.get(code=code).raw_data

    @staticmethod
    def is_an_existing_code(code):
        return DataAsset.objects.filter(code=code).exists()

    @staticmethod
    def delete_data_asset(code):
        """Peticion para la eliminacion de los datos de un dataAsset
                                       - **parameters**::
                                             :param code:Identificador para eliminar el activo de datos
                                  """
        logger.debug("Attempting to delete a data asset")
        DataAsset.objects.filter(code=code).delete()







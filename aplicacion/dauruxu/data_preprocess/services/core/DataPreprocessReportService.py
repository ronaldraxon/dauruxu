"""
data_preprocess.service.core.DataPreprocessReportService.py
===========================================================
Módulo para la definición de la clase fachada y sus métodos para el registro
y consulta de preproceso de activos de datos.
"""

from data_registry.services.storage.DataAssetService import DataAssetService
from data_preprocess.models.storage.DataAssetPreprocessReport import DataAssetPreprocessReport
from data_preprocess.models.storage.DataStatistics import DataStatistics
from data_preprocess.models.storage.CleanDataAsset import CleanDataAsset
from data_preprocess.services.core.PipelineComposerService import PipelineComposer as Pc
from background_task import background
from collections import OrderedDict
from utilities.PandasUtilities import PandasUtilities as Pu
from utilities.EncodingUtilities import EncodingUtilities as Eu
import numpy as np
import pandas as pd

import ast
import logging

logger = logging.getLogger(__name__)


class DataPreprocessReportService:
    """Clase fachada para la definición de métodos principales de servicio para el
    preprocesamiento de activos de datos. Los métodos relacionados en esta clase, son
    los que deberían llamarse desde la capa de vista.
    """

    @staticmethod
    def create_data_asset_preprocess(data_preprocess_serializer):
        """Función que genera el preprocesamiento de activo de datos a partir de un serializador con la información
        de la solicitud y el conjunto de datos extraído.

        - **parameters**::
                     :param data_preprocess_serializer:
                     :param data_asset: El activo de datos solicitado del registro de datos  (data_registry)
        - **return**::
                     :return: El manifiesto actual de preprocesamiento de activo de datos
        """
        logger.debug("Creando preprocesamiento de activo de datos.")
        data_preprocess = data_preprocess_serializer.save()
        DataPreprocessReportService.create_input_and_response_pipelines(str(data_preprocess.id), data_preprocess.code)
        return data_preprocess_serializer

    @staticmethod
    # @background(queue='data-preprocess-queue')
    def create_input_and_response_pipelines(data_preprocess_id, code):
        data_preprocess = DataAssetPreprocessReport.objects.get(id=data_preprocess_id)
        data_asset = DataPreprocessReportService.get_data_asset_from_data_registry(code)
        data_frame = Pu.convert_list_of_dict_to_pandas_data_frame(ast.literal_eval(data_asset.raw_data))

        #implementar llamado a sacar estadísticas del dataframe

        inputs_data_frame = data_frame[ast.literal_eval(data_asset.input_variables)]
        response_data_frame = data_frame[ast.literal_eval(data_asset.response_variable)]

        inputs_pipeline = DataPreprocessReportService. \
            create_single_fitted_pipelines(eval(data_preprocess.inputs_transformations), inputs_data_frame)
        response_pipeline = DataPreprocessReportService. \
            create_single_fitted_pipelines(eval(data_preprocess.response_transformations), response_data_frame)

        #Métodos para persisir pipelines

        #Ronald verificar
        print(inputs_pipeline.get_feature_names())
        print(inputs_pipeline.transform(inputs_data_frame))
        print(response_pipeline.transform(response_data_frame))
        return inputs_pipeline, response_pipeline

    @staticmethod
    def create_single_fitted_pipelines(transformations, data_frame=None):
        pipeline = Pc.compose_column_transformer_pipeline(transformations)
        pipeline.fit(data_frame)
        return pipeline

    @staticmethod
    def get_current_data_preprocess_report(code):
        """Get the current calendar management for the specified point code. A point could have many calendar management since
        its creation, but there should be only one tagged as current.

               - **parameters**::
                     :param code: The point code the calendar management is related with
               - **return**::
                     :return: El manifiesto actual de preprocesamiento de activo de datos
               """
        logger.debug("Extrayendo el manifiesto de preprocesamiento para el activo de datos {}.".format(code))
        data_management = DataAssetPreprocessReport.objects \
            .filter(code=code, is_the_current_data_preprocess=True).first()
        return data_management

    @staticmethod
    def get_current_data_statistics(code):
        """Get the current calendar management for the specified point code. A point could have many calendar management since
        its creation, but there should be only one tagged as current.

               - **parameters**::
                     :param code: The point code the calendar management is related with
               - **return**::
                     :return: El manifiesto actual de preprocesamiento de activo de datos
               """
        logger.debug("Extrayendo el manifiesto de preprocesamiento para el activo de datos {}.".format(code))
        data_management = DataAssetPreprocessReport.objects \
            .filter(code=code, is_the_current_data_preprocess=True).first()
        return DataStatistics.objects.filter(data_asset_preprocess_id=data_management.id)

    @staticmethod
    def get_current_clean_data_asset(code):
        """Get the current calendar management for the specified point code. A point could have many calendar management since
        its creation, but there should be only one tagged as current.

               - **parameters**::
                     :param code: The point code the calendar management is related with
               - **return**::
                     :return: El manifiesto actual de preprocesamiento de activo de datos
               """
        logger.debug("Extrayendo el manifiesto de preprocesamiento para el activo de datos {}.".format(code))
        return CleanDataAsset.objects.get(code=code)

    @staticmethod
    def get_data_asset_from_data_registry(code):
        """Get the current calendar management for the specified point code. A point could have many calendar management since
        its creation, but there should be only one tagged as current.

               - **parameters**::
                     :param code: The point code the calendar management is related with
               - **return**::
                     :return: El manifiesto actual de preprocesamiento de activo de datos
               """
        logger.debug("Extrayendo el manifiesto de preprocesamiento para el activo de datos {}.".format(code))
        return DataAssetService.retrieve_data_asset(code)

    @staticmethod
    def is_data_asset_in_data_registry(code):
        """Verifica si existe un activo de datos registrado con el código identificador.

               - **parameters**::
                     :param code: Identificador del activo de datos
               - **return**::
                     :return:
               """
        logger.debug("Extrayendo el manifiesto de preprocesamiento para el activo de datos {}.".format(code))
        return DataAssetService.is_an_existing_code(code)

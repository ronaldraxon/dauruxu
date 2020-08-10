"""
data_preprocess.services.core.PipelineComposer.py
=================================================
Módulo base para la fabricación de tubería (pipeline) a
partir de un conjunto de transformaciones.
"""

from data_preprocess.models.core.TransformationFactory import TransformationsFactory as Tf
from data_preprocess.services.configuration.DataPreProcessPropertiesService import DataPreprocessPropertiesService
from sklearn.compose import ColumnTransformer
import ast
DEFAULT_CALENDAR_FIELDS = DataPreprocessPropertiesService.get_calendar_fields()


class PipelineComposer:

    @staticmethod
    def compose_column_transformer_pipeline(transformations):
        transformation_list = list()
        PipelineComposer.populate_transformations_list(transformation_list, transformations)
        return ColumnTransformer(transformation_list, remainder='drop')

    @staticmethod
    def populate_transformations_list(transformations_list, transformations):
        for transformation in transformations:
            transformations_list.append(PipelineComposer.
                                        create_transformation_tuple(str(transformation.get("transformation_name")),
                                                                    Tf.get_transformation(
                                                                    transformation.get("transformation_type"),
                                                                    transformation.get("transformation_params")),
                                                                    transformation.get("fields_involved")))

    @staticmethod
    def create_transformation_tuple(name, transformer, columns) -> tuple:
        return tuple((name, transformer, columns))

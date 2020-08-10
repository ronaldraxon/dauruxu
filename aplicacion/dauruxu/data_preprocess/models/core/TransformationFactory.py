"""
data_preprocess.models.core.TransformationFactory.py
====================================================
Módulo base para la fabricación de transformaciones a
incluir en una tubería (pipeline) de preprocesamiento.
"""

from sklearn.preprocessing import PowerTransformer
from data_preprocess.models.core.custom.TwiceSquareRoot import TwiceSquareRoot
from data_preprocess.models.core.custom.CalendarIntegration import CalendarIntegration
from data_preprocess.models.core.custom.CMinMaxScaler import CMinMaxScaler
from utilities import TypeUtilities as Tu


def create_new_MinMaxScaler():
    return CMinMaxScaler()


class TransformationsFactory:
    """
       Clase para la definición de fábrica de transformaciones de la libreria scikit o bien personalizadas
       del paquete custom
    """

    class __Transformations:
        TYPES = {
            "CALENDAR_INTEGRATION": CalendarIntegration(),
            "TWICE_SQUARE_ROOT": TwiceSquareRoot(),
            "POWER_TRANSFORMER": PowerTransformer(),
            "POWER_TRANSFORMER_BOX_COX": PowerTransformer(method='box-cox'),
            "POWER_TRANSFORMER_YEO_JOHNSON": PowerTransformer(method='yeo-johnson'),
            "MINMAX_SCALER": create_new_MinMaxScaler()
        }



    @staticmethod
    def __get_transformation_with_parameters__(transformation_type, dictionary_of_parameters=None):
        """Privado - Construye una transformación y le asigna los parámetros correspondientes

            :param transformation_type: Tipo de transformación a fabricar, de los tipos disponibles en la clase
            __Transformations
            :param dictionary_of_parameters: Diccionario con los parámetros para la transformación construida
        """

        #trans_template = TransformationsFactory.__Transformations
        transformation = TransformationsFactory.__Transformations.TYPES.get(transformation_type)
        #transformation = trans_template.TYPES
        #print(transformation)
        #print(id(transformation))
        for attribute, value in dictionary_of_parameters.items():
            transformation.__setattr__(attribute, Tu.get_correct_instance_from_object_as_string(value))
        return transformation

    @staticmethod
    def get_transformation(transformation_type, dictionary_of_parameters=None) -> object:
        """Público - Define el tipo de construcción de transformación a partir del parámetro de diccionario.

            :param transformation_type: Tipo de transformación a fabricar, de los tipos disponibles en la clase
            __Transformations
            :param dictionary_of_parameters: Diccionario con los parámetros para la transformación construida. Si contiene valores
            la construcción de la tranformación se efectuará con los parámetros establecidos
        """
        if dictionary_of_parameters is None:
            return TransformationsFactory.__Transformations.TYPES.get(transformation_type)
        else:
            return TransformationsFactory. \
                __get_transformation_with_parameters__(transformation_type=transformation_type,
                                                       dictionary_of_parameters=dictionary_of_parameters)

    @staticmethod
    def get_transformations_as_choices():
        """Público - Extrae los tipos de trasnformaciones como lista de tuplas para su uso en los serializadores
        """
        return Tu.get_tuple_from_dict_key(TransformationsFactory.__Transformations.TYPES.keys())

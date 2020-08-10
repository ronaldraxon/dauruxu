"""
data_preprocess.models.configuration.DataPreprocessProperties.py
================================================================
Módulo para almacenamiento de la clase singleton de propiedades.
"""


class DataPreprocessProperties(object):
    """Clase para la definición de propiedades del
    preprocesamiento de activos de datos
    """
    instance = None

    class __DataPreprocessProperties:
        def __init__(self):
            DataPreprocessProperties.__instance__ = self
            self.DEFAULT_CALENDAR_FIELDS = list()
            self.DEFAULT_INPUT_TRANSFORMATIONS = list()
            self.DEFAULT_RESPONSE_TRANSFORMATIONS = list()
            self.CHECK_DATA_BEHAVIOR = "EVERY_30_DAYS"
            self.CHECK_DATA_BEHAVIOR_NUM = 2592000

        def __str__(self):
            return '{0!r}'.format(self)

        def update_property_values(self, properties):
            """Actualiza los valores de propiedades de la aplicación

                :param properties: DataFrame de pandas que contiene los valores de las propiedades
            """
            self.DEFAULT_INPUT_TRANSFORMATIONS = list(properties.loc['DEFAULT_INPUT_TRANSFORMATIONS'].value.split(" "))
            self.DEFAULT_RESPONSE_TRANSFORMATIONS = list(
                properties.loc['DEFAULT_RESPONSE_TRANSFORMATIONS'].value.split(" "))
            self.CHECK_DATA_BEHAVIOR = properties.loc['CHECK_DATA_BEHAVIOR'].value
            self.CHECK_DATA_BEHAVIOR_NUM = int(properties.loc['CHECK_DATA_BEHAVIOR_NUM'].value)

        def update_calendar_fields(self, calendar_fields):
            """Actualiza los valores de la propiedad de campos de calendario que pueden ser empleados por defecto

                :param calendar_fields: Lista de campos disponibles en el servicio de calendario
            """
            self.DEFAULT_CALENDAR_FIELDS = calendar_fields

    def __new__(cls):
        if not DataPreprocessProperties.instance:
            DataPreprocessProperties.instance = DataPreprocessProperties.__DataPreprocessProperties()
        return DataPreprocessProperties.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name, **kwargs):
        return setattr(self.instance, name, **kwargs)

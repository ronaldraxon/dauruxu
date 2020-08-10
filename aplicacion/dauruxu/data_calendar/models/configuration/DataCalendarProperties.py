"""
data_calendar.models.configuration.DataCalendarProperties.py
============================================================
Modulo Singleton para el  data_calendar. Esta clase evita varias solicitudes a apps_administration
para las  propiedades de almacenamiento adecuadas para actividades del data_calendar
"""


class DataCalendarProperties(object):
    instance = None

    class __DataCalendarProperties:
        def __init__(self):
            DataCalendarProperties.__instance__ = self
            self.MINIMUM_YEAR = 1990
            self.MAXIMUM_YEAR = 2050

        def __str__(self):
            return '{0!r}'.format(self)

        def update_property_values(self, properties):
            """Actualiza los valores de la clase singleton
            - **parameters**::
                 :param properties:Pandas DataFrame containing property values
            """
            self.MINIMUM_YEAR = int(properties.loc['MINIMUM_YEAR'].value)
            self.MAXIMUM_YEAR = int(properties.loc['MAXIMUM_YEAR'].value)

    def __new__(cls):
        if not DataCalendarProperties.instance:
            DataCalendarProperties.instance = DataCalendarProperties.__DataCalendarProperties()
        return DataCalendarProperties.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name, **kwargs):
        return setattr(self.instance, name, **kwargs)

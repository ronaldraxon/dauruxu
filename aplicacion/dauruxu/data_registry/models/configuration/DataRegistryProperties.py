"""
data_registry.models.configuration.DRProperties.py
==================================================
Modulo Singleton para data_registry. Esta clase evita  que se realicen varias solicitudes de apps_administration
para  las propiedades de almacenamiento adecuadas para el data_registry
"""


class DataRegistryProperties(object):
    instance = None

    class __DataRegistryProperties:
        def __init__(self):
            DataRegistryProperties.__instance__ = self
            self.MINIMUM_DATASET_SIZE = 100
            #self.REQUEST_DATA_PROCESSING = True

        def __str__(self):
            return '{0!r}'.format(self)

        def update_property_values(self, properties):
            """
                      Llamado para actualizacion de los  valores de las propiedades  para data_calendar
                      """
            self.MINIMUM_DATASET_SIZE = int(properties.loc['MINIMUM_DATASET_SIZE'].value)
            #self.REQUEST_DATA_PROCESSING = bool(properties.loc['REQUEST_DATA_PROCESSING'].value)

    def __new__(cls):
        if not DataRegistryProperties.instance:
            DataRegistryProperties.instance = DataRegistryProperties.__DataRegistryProperties()
        return DataRegistryProperties.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name, **kwargs):
        return setattr(self.instance, name, **kwargs)

